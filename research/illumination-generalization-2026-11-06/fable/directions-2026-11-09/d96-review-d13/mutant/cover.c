/* cover.c -- accumulated cylinder certificate (Theorem C, theory.md), exact.
 *
 * Input: one room per line, "TAG area W x0 y0 x1 y1 ..." (TAG optional, any
 * token starting with a letter) or "area W x0 y0 ...". Cells are unit squares.
 *
 * For each room:
 *  1. Pole test: for every pair of convex corners, is there a direction
 *     (p, q), 1 <= p, q <= B, coprime, in which one DP cylinder touches both
 *     poles? If some pair never shares, the room is OBSTRUCTED(B) (Prop. O:
 *     no certificate built from these directions can cover a neighbourhood of
 *     that pair of corners), and step 2 is skipped unless FORCE is set.
 *  2. Theorem C: the room is cut into relatively open cells (open faces,
 *     open edges, points) by the singular lines of the directions processed
 *     so far; only live cells are kept. Each live cell carries Q, a list of
 *     closed convex polygons containing the closure of P \ Ill(s). A cell
 *     dies when Q has no 2D piece. Directions are processed in order of p+q
 *     until every live cell is a point, or the bound is reached.
 *  3. For DONE rooms: every pair (s, t) of distinct live points with t in
 *     Q(s) and s in Q(t) is unresolved (all other pairs are lit by Theorem C
 *     and symmetry of illumination).
 *  Output per room:
 *     ROOM id area W status ndirs maxpq live_pts live_edges live_faces
 *          nonlattice_pts unres_lattice_pairs unres_other_pairs | cells |
 *          unresolved pairs with a non-lattice point, "x/d,y/d;x/d,y/d"
 *  status: DONE (no live cell of dim >= 1), RESID (some live cell of dim >= 1
 *  after all directions), OBST (pole-pair obstruction), BIG (cap hit).
 *
 * Arithmetic: points are (X, Y, D) int64 with D > 0 and gcd 1; products in
 * __int128. Every vertex is the intersection of two lines a x + b y = c with
 * |a|, |b| <= B, so D <= 2 B^2 after reduction (checked: abort if D > 1e6).
 *
 * usage: cover B FORCE MAXLIVE < rooms
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef long long ll;
typedef __int128 i128;

static ll gcdl(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }
static ll floordiv(ll a, ll b) { /* b > 0 */ ll q = a / b; if ((a % b) && (a < 0)) q--; return q; }

/* ------------------------------------------------------------------ room */
#define MAXCELL 64
#define G 72
static int ncell, CX[MAXCELL], CY[MAXCELL], cellid[G][G];
static int incell(int x, int y) { return x >= 0 && y >= 0 && x < G && y < G && cellid[x][y] >= 0; }
static int ptype(int x, int y) { /* 0 out, 1 convex, 3 reflex, 2 flat, 4 interior */
    return incell(x - 1, y - 1) + incell(x, y - 1) + incell(x - 1, y) + incell(x, y);
}
static const int SX[4] = {1, -1, 1, -1}, SY[4] = {1, 1, -1, -1};
static int nsq, Rr[4 * MAXCELL], Uu[4 * MAXCELL], Ri[4 * MAXCELL], MLL[4 * MAXCELL];
static int sqi(int c, int sh) { return 4 * c + sh; }
static int sheet_of(int ex, int ey) { for (int s = 0; s < 4; s++) if (SX[s] == ex && SY[s] == ey) return s; return -1; }

static void build_surface(void) {
    nsq = 4 * ncell;
    for (int c = 0; c < ncell; c++)
        for (int sh = 0; sh < 4; sh++) {
            int i = sqi(c, sh), a = CX[c], b = CY[c], ex = SX[sh], ey = SY[sh];
            Rr[i] = incell(a + ex, b) ? sqi(cellid[a + ex][b], sh) : sqi(c, sheet_of(-ex, ey));
            Uu[i] = incell(a, b + ey) ? sqi(cellid[a][b + ey], sh) : sqi(c, sheet_of(ex, -ey));
            int x = a + (ex == 1 ? 0 : 1), y = b + (ey == 1 ? 0 : 1);
            int t = ptype(x, y);
            MLL[i] = (t == 1 || t == 3);
        }
    for (int i = 0; i < nsq; i++) Ri[Rr[i]] = i;
}

/* ------------------------------------------------------------- labels */
#define MAXPQ 40
#define NONE (-1)
typedef struct {
    int p, q, ncyl;
    /* per cell: plus strips k in [k0-p, k0+q): idx k-(k0-p); lines k in (k0-p, k0+q): idx k-(k0-p)-1
       minus strips k in [m0, m0+p+q): idx k-m0; lines (m0, m0+p+q): idx k-m0-1 */
    int plus[MAXCELL][2 * MAXPQ], minus[MAXCELL][2 * MAXPQ];
    int pline[MAXCELL][2 * MAXPQ], mline[MAXCELL][2 * MAXPQ];
} Dir;

static int cyc_[4 * MAXCELL * MAXPQ], regl_[4 * MAXCELL * MAXPQ], uf_[4 * MAXCELL * MAXPQ];
static int uf2_[4 * MAXCELL * MAXPQ], did_[4 * MAXCELL * MAXPQ];
static int ufind(int *u, int a) { while (u[a] != a) { u[a] = u[u[a]]; a = u[a]; } return a; }

static int slot(int i, int m, int q) { while (m < 0) { i = Ri[i]; m += q; } return i * q + m; }

static void compute_dir(Dir *D, int p, int q) {
    D->p = p; D->q = q;
    int ns = nsq * q;
    for (int t = 0; t < ns; t++) cyc_[t] = -1;
    int nc = 0;
    for (int t = 0; t < ns; t++) {
        if (cyc_[t] >= 0) continue;
        int cur = t;
        while (cyc_[cur] < 0) {
            cyc_[cur] = nc;
            int i = cur / q, j = cur % q, k = (j + p) / q;
            for (int z = 0; z < k; z++) i = Rr[i];
            cur = Uu[i] * q + (j + p) % q;
        }
        if (cur != t) { fprintf(stderr, "not a permutation\n"); exit(3); }
        nc++;
    }
    for (int c = 0; c < nc; c++) { regl_[c] = 1; uf_[c] = c; }
    for (int i = 0; i < nsq; i++) if (MLL[i] && !(i % 7 == 0)) regl_[cyc_[i * q]] = 0;
    for (int i = 0; i < nsq; i++) {
        for (int j = 1; j < q; j++)
            if (regl_[cyc_[i * q + j]]) { int a = ufind(uf_, cyc_[i * q + j - 1]), b = ufind(uf_, cyc_[i * q + j]); if (a != b) uf_[a] = b; }
        if (regl_[cyc_[i * q]]) { int a = ufind(uf_, cyc_[i * q]), b = ufind(uf_, cyc_[Ri[i] * q + q - 1]); if (a != b) uf_[a] = b; }
    }
    /* M-cylinder root per slot; tau merge into uf2 over cycle ids */
    for (int c = 0; c < nc; c++) uf2_[c] = c;
#define MROOT(s) ufind(uf_, cyc_[s])
#define MERGE(s, t) do { int A_ = ufind(uf2_, MROOT(s)), B_ = ufind(uf2_, MROOT(t)); if (A_ != B_) uf2_[A_] = B_; } while (0)
    for (int c = 0; c < ncell; c++) {
        int a = CX[c], b = CY[c], k0 = q * a - p * b, m0 = q * a + p * b;
        for (int k = k0 - p; k < k0 + q; k++) {
            int s1 = slot(sqi(c, 0), k - k0, q), s4 = slot(sqi(c, 3), q * (a + 1) - p * (b + 1) - k - 1, q);
            MERGE(s1, s4);
        }
        for (int k = m0; k < m0 + p + q; k++) {
            int s3 = slot(sqi(c, 2), k - q * a - p * (b + 1), q), s2 = slot(sqi(c, 1), q * (a + 1) + p * b - k - 1, q);
            MERGE(s3, s2);
        }
    }
    for (int c = 0; c < nc; c++) did_[c] = -1;
    int nd = 0;
    for (int c = 0; c < nc; c++) { int r = ufind(uf2_, ufind(uf_, c)); if (did_[r] < 0) did_[r] = nd++; }
    D->ncyl = nd;
#define LAB(s) did_[ufind(uf2_, MROOT(s))]
    for (int c = 0; c < ncell; c++) {
        int a = CX[c], b = CY[c], k0 = q * a - p * b, m0 = q * a + p * b;
        for (int k = k0 - p; k < k0 + q; k++) D->plus[c][k - (k0 - p)] = LAB(slot(sqi(c, 0), k - k0, q));
        for (int k = m0; k < m0 + p + q; k++) D->minus[c][k - m0] = LAB(slot(sqi(c, 2), k - q * a - p * (b + 1), q));
        for (int k = k0 - p + 1; k < k0 + q; k++) {
            int s = slot(sqi(c, 0), k - k0, q);
            D->pline[c][k - (k0 - p) - 1] = regl_[cyc_[s]] ? LAB(s) : NONE;
        }
        for (int k = m0 + 1; k < m0 + p + q; k++) {
            int s = slot(sqi(c, 2), k - q * a - p * (b + 1), q);
            D->mline[c][k - m0 - 1] = regl_[cyc_[s]] ? LAB(s) : NONE;
        }
    }
}

/* ------------------------------------------------------------ geometry */
typedef struct { ll x, y, d; } Pt;
#define MAXV 40
typedef struct { int n; Pt v[MAXV]; } Poly;   /* closed convex set; n = 1 point, 2 segment */

/* reduced point; LIM bounds the denominator (vertices: 1e9, so that cross
   products fit in 128 bits; representative points, used only in lambda_at
   and for reporting: 1e13) */
static Pt mkpt_lim(i128 x, i128 y, i128 d, i128 lim);
static Pt mkpt(i128 x, i128 y, i128 d) { return mkpt_lim(x, y, d, 1000000000LL); }
static Pt mkpt_lim(i128 x, i128 y, i128 d, i128 lim) {
    if (d < 0) { x = -x; y = -y; d = -d; }
    i128 g = d, t;
    i128 ax = x < 0 ? -x : x, ay = y < 0 ? -y : y;
    while (ax) { t = g % ax; g = ax; ax = t; }
    while (ay) { t = g % ay; g = ay; ay = t; }
    if (g == 0) g = 1;
    x /= g; y /= g; d /= g;
    if (d > lim || x > 100 * lim || x < -100 * lim || y > 100 * lim || y < -100 * lim) {
        fprintf(stderr, "coordinate overflow guard\n"); exit(4);
    }
    Pt P = {(ll)x, (ll)y, (ll)d};
    return P;
}
static int pteq(Pt a, Pt b) { return a.x == b.x && a.y == b.y && a.d == b.d; }
static int ptlt(Pt a, Pt b) { /* lexicographic on (x, y) */
    i128 l = (i128)a.x * b.d, r = (i128)b.x * a.d;
    if (l != r) return l < r;
    l = (i128)a.y * b.d; r = (i128)b.y * a.d;
    return l < r;
}
/* sign of cross(o, a, b) */
static int cross_sign(Pt o, Pt a, Pt b) {
    i128 ax = (i128)a.x * o.d - (i128)o.x * a.d, ay = (i128)a.y * o.d - (i128)o.y * a.d; /* scaled by a.d*o.d */
    i128 bx = (i128)b.x * o.d - (i128)o.x * b.d, by = (i128)b.y * o.d - (i128)o.y * b.d; /* scaled by b.d*o.d */
    /* magnitudes: coords <= 4e12/1e9 ... products fit in i128 */
    i128 c = ax * by - ay * bx;
    return (c > 0) - (c < 0);
}
/* value sign of a x + b y - c at P */
static i128 hval(Pt P, ll a, ll b, ll c) { return (i128)a * P.x + (i128)b * P.y - (i128)c * P.d; }

static void normalize(Poly *P) {
    /* dedupe; detect collinear; convex hull (monotone chain) */
    int n = P->n;
    if (n <= 1) return;
    Pt u[2 * MAXV];
    int m = 0;
    for (int i = 0; i < n; i++) u[m++] = P->v[i];
    /* sort */
    for (int i = 1; i < m; i++) { Pt t = u[i]; int j = i - 1; while (j >= 0 && ptlt(t, u[j])) { u[j + 1] = u[j]; j--; } u[j + 1] = t; }
    int k = 0;
    for (int i = 0; i < m; i++) if (k == 0 || !pteq(u[i], u[k - 1])) u[k++] = u[i];
    m = k;
    if (m == 1) { P->n = 1; P->v[0] = u[0]; return; }
    int col = 1;
    for (int i = 1; i < m - 1 && col; i++) if (cross_sign(u[0], u[m - 1], u[i]) != 0) col = 0;
    if (col) { P->n = 2; P->v[0] = u[0]; P->v[1] = u[m - 1]; return; }
    Pt h[2 * MAXV];
    int t = 0;
    for (int i = 0; i < m; i++) { while (t >= 2 && cross_sign(h[t - 2], h[t - 1], u[i]) <= 0) t--; h[t++] = u[i]; }
    int lo = t + 1;
    for (int i = m - 2; i >= 0; i--) { while (t >= lo && cross_sign(h[t - 2], h[t - 1], u[i]) <= 0) t--; h[t++] = u[i]; }
    t--;
    if (t > MAXV) { fprintf(stderr, "MAXV\n"); exit(5); }
    P->n = t;
    for (int i = 0; i < t; i++) P->v[i] = h[i];
}

/* clip by a x + b y <= c (closed) */
static void clip(Poly *P, ll a, ll b, ll c) {
    int n = P->n;
    if (n == 0) return;
    if (n == 1) { if (hval(P->v[0], a, b, c) > 0) P->n = 0; return; }
    Poly out; out.n = 0;
    for (int i = 0; i < n; i++) {
        Pt A = P->v[i], B = P->v[(i + 1) % n];
        i128 fa = hval(A, a, b, c), fb = hval(B, a, b, c);   /* scaled by A.d, B.d (> 0) */
        if (fa <= 0) out.v[out.n++] = A;
        if ((fa < 0 && fb > 0) || (fa > 0 && fb < 0)) {
            /* R = (fb A - fa B) / (fb A.d - fa B.d) with fa, fb the scaled values */
            i128 X = fb * A.x - fa * B.x, Y = fb * A.y - fa * B.y, Dn = fb * A.d - fa * B.d;
            out.v[out.n++] = mkpt(X, Y, Dn);
        }
        if (out.n >= MAXV - 1) { fprintf(stderr, "clip MAXV\n"); exit(5); }
    }
    *P = out;
    normalize(P);
}

static int dimp(const Poly *P) { return P->n >= 3 ? 2 : P->n - 1; }

static Poly square(int a, int b) {
    Poly P; P.n = 4;
    P.v[0] = (Pt){a, b, 1}; P.v[1] = (Pt){a + 1, b, 1}; P.v[2] = (Pt){a + 1, b + 1, 1}; P.v[3] = (Pt){a, b + 1, 1};
    return P;
}

/* range of alpha x + beta y over the vertices: floor of min, ceil of max */
static void lin_range(const Poly *P, ll al, ll be, ll *fmin, ll *cmax) {
    ll lo = 0, hi = 0;
    for (int i = 0; i < P->n; i++) {
        ll num = al * P->v[i].x + be * P->v[i].y, d = P->v[i].d;
        ll f = floordiv(num, d), c = -floordiv(-num, d);
        if (i == 0 || f < lo) lo = f;
        if (i == 0 || c > hi) hi = c;
    }
    *fmin = lo; *cmax = hi;
}

/* ---------------------------------------------------------- live cells */
typedef struct { int cell; Poly P; } QP;
typedef struct { int ref; int n, cap; QP *a; } QSet;
typedef struct { int cell; Poly P; QSet *Q; } Live;

static QSet *qnew(void) { QSet *s = calloc(1, sizeof(QSet)); s->ref = 1; return s; }
static void qpush(QSet *s, int cell, const Poly *P) {
    if (s->n == s->cap) { s->cap = s->cap ? 2 * s->cap : 16; s->a = realloc(s->a, s->cap * sizeof(QP)); }
    s->a[s->n].cell = cell; s->a[s->n].P = *P; s->n++;
}
static void qrelease(QSet *s) { if (--s->ref == 0) { free(s->a); free(s); } }

/* Q minus union of K_D, D in lam: keep the closed faces with both labels
   outside lam. Within a room cell, the union of these faces is the union over
   maximal runs [i1, i2) of kept plus strips and [j1, j2) of kept minus strips
   of the closed parallelograms i1 <= qx - py <= i2, j1 <= qx + py <= j2
   (intersected with the cell); clipping by runs instead of single faces keeps
   Q from fragmenting. */
static QSet *subtract(const QSet *Q, const Dir *D, int l1, int l2) {
    QSet *R = qnew();
    int p = D->p, q = D->q;
    ll ri[2 * MAXPQ + 2][2], rj[2 * MAXPQ + 2][2];
    for (int t = 0; t < Q->n; t++) {
        int c = Q->a[t].cell, a = CX[c], b = CY[c];
        const Poly *P = &Q->a[t].P;
        int k0 = q * a - p * b, m0 = q * a + p * b;
        ll ilo, ihi, jlo, jhi;
        lin_range(P, q, -p, &ilo, &ihi);
        lin_range(P, q, p, &jlo, &jhi);
        if (ilo < k0 - p) ilo = k0 - p;
        if (ihi > k0 + q) ihi = k0 + q;
        if (jlo < m0) jlo = m0;
        if (jhi > m0 + p + q) jhi = m0 + p + q;
        int ni = 0, nj = 0;
        for (ll i = ilo; i < ihi; i++) {
            int lp = D->plus[c][i - (k0 - p)];
            if (lp == l1 || lp == l2) continue;
            if (ni && ri[ni - 1][1] == i) ri[ni - 1][1] = i + 1;
            else { ri[ni][0] = i; ri[ni][1] = i + 1; ni++; }
        }
        for (ll j = jlo; j < jhi; j++) {
            int lm = D->minus[c][j - m0];
            if (lm == l1 || lm == l2) continue;
            if (nj && rj[nj - 1][1] == j) rj[nj - 1][1] = j + 1;
            else { rj[nj][0] = j; rj[nj][1] = j + 1; nj++; }
        }
        for (int u = 0; u < ni; u++)
            for (int v = 0; v < nj; v++) {
                Poly W = *P;
                if (ri[u][0] > ilo) clip(&W, -q, p, -ri[u][0]);
                if (ri[u][1] < ihi) clip(&W, q, -p, ri[u][1]);
                if (rj[v][0] > jlo) clip(&W, -q, -p, -rj[v][0]);
                if (rj[v][1] < jhi) clip(&W, q, p, rj[v][1]);
                if (dimp(&W) == 2) qpush(R, c, &W);
            }
    }
    return R;
}

/* Lambda at a point (x/d, y/d); returns labels in l1, l2 (NONE if absent) */
static void lambda_at(const Dir *D, Pt P, int *l1, int *l2) {
    int p = D->p, q = D->q;
    /* cells whose closure contains P */
    int cs[4], nc = 0;
    ll fx = floordiv(P.x, P.d), fy = floordiv(P.y, P.d);
    int xs[2], nx = 0, ys[2], ny = 0;
    if (P.x % P.d == 0) { xs[nx++] = (int)fx - 1; xs[nx++] = (int)fx; } else xs[nx++] = (int)fx;
    if (P.y % P.d == 0) { ys[ny++] = (int)fy - 1; ys[ny++] = (int)fy; } else ys[ny++] = (int)fy;
    for (int i = 0; i < nx; i++) for (int j = 0; j < ny; j++) if (incell(xs[i], ys[j])) cs[nc++] = cellid[xs[i]][ys[j]];
    if (!nc) { fprintf(stderr, "lambda_at: point outside\n"); exit(6); }
    ll un = (ll)q * P.x - (ll)p * P.y, vn = (ll)q * P.x + (ll)p * P.y;
    *l1 = NONE; *l2 = NONE;
    /* plus */
    if (un % P.d != 0) {
        ll k = floordiv(un, P.d);
        int c = cs[0], k0 = q * CX[c] - p * CY[c];
        *l1 = D->plus[c][k - (k0 - p)];
    } else {
        ll k = un / P.d; int found = 0;
        for (int t = 0; t < nc && !found; t++) {
            int c = cs[t], k0 = q * CX[c] - p * CY[c];
            if (k > k0 - p && k < k0 + q) { *l1 = D->pline[c][k - (k0 - p) - 1]; found = 1; }
        }
        if (!found) { fprintf(stderr, "plus line not found\n"); exit(6); }
    }
    if (vn % P.d != 0) {
        ll k = floordiv(vn, P.d);
        int c = cs[0], m0 = q * CX[c] + p * CY[c];
        *l2 = D->minus[c][k - m0];
    } else {
        ll k = vn / P.d; int found = 0;
        for (int t = 0; t < nc && !found; t++) {
            int c = cs[t], m0 = q * CX[c] + p * CY[c];
            if (k > m0 && k < m0 + p + q) { *l2 = D->mline[c][k - m0 - 1]; found = 1; }
        }
        if (!found) { fprintf(stderr, "minus line not found\n"); exit(6); }
    }
    if (*l1 == NONE) { *l1 = *l2; *l2 = NONE; }
    if (*l1 == *l2) *l2 = NONE;
}

/* a point of the relative interior: the centroid of at most three vertices
   (three non-collinear hull vertices for a 2D cell, the midpoint of a segment) */
static Pt rep_point(const Poly *P) {
    int n = P->n < 3 ? P->n : 3;
    i128 X = 0, Y = 0, Dn = 1;
    for (int i = 0; i < n; i++) {
        X = X * P->v[i].d + (i128)P->v[i].x * Dn;
        Y = Y * P->v[i].d + (i128)P->v[i].y * Dn;
        Dn = Dn * P->v[i].d;
    }
    return mkpt_lim(X, Y, Dn * n, 10000000000000LL);
}

/* is T in some closed polygon of Q? (Q holds 2D convex polygons in CCW order) */
static int in_qset(const QSet *Q, Pt T) {
    for (int t = 0; t < Q->n; t++) {
        const Poly *P = &Q->a[t].P;
        int in = 1;
        for (int i = 0; i < P->n && in; i++) if (cross_sign(P->v[i], P->v[(i + 1) % P->n], T) < 0) in = 0;
        if (in) return 1;
    }
    return 0;
}

/* nearest convex corner (L-inf) to the representative point of P, and the
   largest L-inf distance of a vertex of P from that corner (floating point) */
static double poly_corner(const Poly *P, int np, const int *PX, const int *PY, int *ci) {
    Pt R = rep_point(P);
    double best = 1e18;
    *ci = 0;
    for (int i = 0; i < np; i++) {
        double dx = (double)R.x / R.d - PX[i], dy = (double)R.y / R.d - PY[i];
        double d = (dx < 0 ? -dx : dx) > (dy < 0 ? -dy : dy) ? (dx < 0 ? -dx : dx) : (dy < 0 ? -dy : dy);
        if (d < best) { best = d; *ci = i; }
    }
    double r = 0;
    for (int v = 0; v < P->n; v++) {
        double dx = (double)P->v[v].x / P->v[v].d - PX[*ci], dy = (double)P->v[v].y / P->v[v].d - PY[*ci];
        if (dx < 0) dx = -dx;
        if (dy < 0) dy = -dy;
        if (dx > r) r = dx;
        if (dy > r) r = dy;
    }
    return r;
}

/* ------------------------------------------------------------- driver */
static int B, FORCE, MAXLIVE;
static int ndirs, DP[4000], DQ[4000];
static Dir *DIR;

static int cmpdir(const void *a, const void *b) {
    const int *x = a, *y = b;
    if (x[0] + x[1] != y[0] + y[1]) return x[0] + x[1] - y[0] - y[1];
    if (x[0] != y[0]) return x[0] - y[0];
    return x[1] - y[1];
}

static Live *live, *nlive;
static int nl, capl, nnl, capnl;
static void push_live(Live **arr, int *n, int *cap, int cell, const Poly *P, QSet *Q) {
    if (*n == *cap) { *cap = *cap ? 2 * *cap : 1024; *arr = realloc(*arr, *cap * sizeof(Live)); }
    (*arr)[*n].cell = cell; (*arr)[*n].P = *P; (*arr)[*n].Q = Q; (*n)++;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: cover B FORCE MAXLIVE < rooms\n"); return 1; }
    B = atoi(argv[1]); FORCE = atoi(argv[2]); MAXLIVE = atoi(argv[3]);
    if (B > MAXPQ / 2) { fprintf(stderr, "B too large\n"); return 1; }
    {
        int t[4000][2], n = 0;
        for (int p = 1; p <= B; p++) for (int q = 1; q <= B; q++) if (gcdl(p, q) == 1) { t[n][0] = p; t[n][1] = q; n++; }
        qsort(t, n, sizeof t[0], cmpdir);
        ndirs = n;
        for (int i = 0; i < n; i++) { DP[i] = t[i][0]; DQ[i] = t[i][1]; }
    }
    DIR = malloc(sizeof(Dir));
    memset(cellid, -1, sizeof cellid);
    static char line[65536];
    long long rid = 0;
    while (fgets(line, sizeof line, stdin)) {
        char *pp = line;
        while (*pp == ' ') pp++;
        if (*pp == '#' || *pp == '\n' || !*pp) continue;
        if ((*pp >= 'A' && *pp <= 'Z') || (*pp >= 'a' && *pp <= 'z')) { while (*pp && *pp != ' ') pp++; }
        int area = (int)strtol(pp, &pp, 10), W = (int)strtol(pp, &pp, 10);
        if (area > MAXCELL) { fprintf(stderr, "room too large\n"); return 2; }
        int ox[MAXCELL], oy[MAXCELL];
        for (int c = 0; c < area; c++) { ox[c] = (int)strtol(pp, &pp, 10); oy[c] = (int)strtol(pp, &pp, 10); }
        rid++;
        ncell = area;
        /* shift so that the smallest cell coordinates are 1 */
        int sx = ox[0], sy = oy[0];
        for (int c = 1; c < area; c++) { if (ox[c] < sx) sx = ox[c]; if (oy[c] < sy) sy = oy[c]; }
        sx -= 1; sy -= 1;
        for (int c = 0; c < area; c++) {
            CX[c] = ox[c] - sx; CY[c] = oy[c] - sy;
            if (CX[c] >= G - 2 || CY[c] >= G - 2) { fprintf(stderr, "room too wide\n"); return 2; }
            cellid[CX[c]][CY[c]] = c;
        }
        build_surface();
        /* ---- pole test ---- */
        int np = 0, PX[64], PY[64], PCELL[64];
        for (int c = 0; c < ncell; c++)
            for (int dx = 0; dx < 2; dx++) for (int dy = 0; dy < 2; dy++) {
                int x = CX[c] + dx, y = CY[c] + dy;
                if (ptype(x, y) == 1) { PX[np] = x; PY[np] = y; PCELL[np] = c; np++; }
            }
        static unsigned char shared[64][64];
        memset(shared, 0, sizeof shared);
        int nunshared = np * (np - 1) / 2;
        for (int di = 0; di < ndirs && nunshared > 0; di++) {
            int p = DP[di], q = DQ[di];
            compute_dir(DIR, p, q);
            int lab[64];
            for (int i = 0; i < np; i++) {
                int c = PCELL[i], a = CX[c], b = CY[c], x = PX[i], y = PY[i];
                int dx = (x == a) ? 1 : -1, dy = (y == b) ? 1 : -1;
                int dv = q * dx + p * dy, du = q * dx - p * dy;
                if (dv != 0) { int v = q * x + p * y, k = dv > 0 ? v : v - 1, m0 = q * a + p * b; lab[i] = DIR->minus[c][k - m0]; }
                else { int u = q * x - p * y, k = du > 0 ? u : u - 1, k0 = q * a - p * b; lab[i] = DIR->plus[c][k - (k0 - p)]; }
            }
            for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++)
                if (!shared[i][j] && lab[i] == lab[j]) { shared[i][j] = 1; nunshared--; }
        }
        const char *status = "DONE";
        int maxpq = 0, used = 0, nlp = 0, nle = 0, nlf = 0, nonlat = 0, ull = 0, unl = 0, trunc_ = 0;
        static char ptsbuf[65536]; ptsbuf[0] = 0;
        if (nunshared > 0 && !FORCE) {
            status = "OBST";
        } else {
            /* ---- Theorem C ---- */
            QSet *Q0 = qnew();
            for (int c = 0; c < ncell; c++) { Poly S = square(CX[c], CY[c]); qpush(Q0, c, &S); }
            nl = 0;
            for (int c = 0; c < ncell; c++) {
                int a = CX[c], b = CY[c];
                Poly S = square(a, b); Q0->ref++; push_live(&live, &nl, &capl, c, &S, Q0);
                if (incell(a + 1, b)) { Poly E; E.n = 2; E.v[0] = (Pt){a + 1, b, 1}; E.v[1] = (Pt){a + 1, b + 1, 1}; Q0->ref++; push_live(&live, &nl, &capl, c, &E, Q0); }
                if (incell(a, b + 1)) { Poly E; E.n = 2; E.v[0] = (Pt){a, b + 1, 1}; E.v[1] = (Pt){a + 1, b + 1, 1}; Q0->ref++; push_live(&live, &nl, &capl, c, &E, Q0); }
                if (ptype(a + 1, b + 1) == 4) { Poly V; V.n = 1; V.v[0] = (Pt){a + 1, b + 1, 1}; Q0->ref++; push_live(&live, &nl, &capl, c, &V, Q0); }
            }
            qrelease(Q0);
            int big = 0;
            for (int di = 0; di < ndirs; di++) {
                int p = DP[di], q = DQ[di];
                compute_dir(DIR, p, q);
                nnl = 0;
                int changed = 0;
                for (int t = 0; t < nl; t++) {
                    Live *L = &live[t];
                    int c = L->cell, a = CX[c], b = CY[c], k0 = q * a - p * b, m0 = q * a + p * b;
                    /* split by singular lines crossing the relative interior */
                    Poly pieces[512]; int npc = 1; pieces[0] = L->P;
                    for (int fam = 0; fam < 2; fam++) {
                        ll al = q, be = fam ? p : -p;
                        ll lo, hi; lin_range(&L->P, al, be, &lo, &hi);
                        for (ll k = lo + 1; k < hi; k++) {
                            int lab;
                            if (!fam) { if (k <= k0 - p || k >= k0 + q) continue; lab = DIR->pline[c][k - (k0 - p) - 1]; }
                            else { if (k <= m0 || k >= m0 + p + q) continue; lab = DIR->mline[c][k - m0 - 1]; }
                            if (lab != NONE) continue;
                            int nn = npc;
                            for (int s = 0; s < nn; s++) {
                                Poly *W = &pieces[s];
                                if (W->n == 1) continue;
                                int pos = 0, neg = 0;
                                for (int v = 0; v < W->n; v++) { i128 h = hval(W->v[v], al, be, k); if (h > 0) pos = 1; if (h < 0) neg = 1; }
                                if (!(pos && neg)) continue;
                                if (npc + 2 > 512) { fprintf(stderr, "too many pieces\n"); exit(7); }
                                Poly lo_ = *W, hi_ = *W, mid = *W;
                                clip(&lo_, al, be, k); clip(&hi_, -al, -be, -k);
                                clip(&mid, al, be, k); clip(&mid, -al, -be, -k);
                                pieces[s] = lo_; pieces[npc++] = hi_; pieces[npc++] = mid;
                            }
                        }
                    }
                    if (npc > 1) changed = 1;
                    /* group by lambda */
                    int lam1[512], lam2[512];
                    QSet *qs[512];
                    for (int s = 0; s < npc; s++) {
                        Pt R = rep_point(&pieces[s]);
                        lambda_at(DIR, R, &lam1[s], &lam2[s]);
                        qs[s] = NULL;
                        if (lam1[s] == NONE) { qs[s] = L->Q; L->Q->ref++; continue; }
                        for (int s2 = 0; s2 < s; s2++)
                            if (qs[s2] && lam1[s2] == lam1[s] && lam2[s2] == lam2[s]) { qs[s] = qs[s2]; qs[s]->ref++; break; }
                        if (!qs[s]) { qs[s] = subtract(L->Q, DIR, lam1[s], lam2[s]); if (qs[s]->n != L->Q->n) changed = 1; }
                    }
                    for (int s = 0; s < npc; s++) {
                        if (qs[s]->n == 0) { qrelease(qs[s]); changed = 1; continue; }
                        push_live(&nlive, &nnl, &capnl, c, &pieces[s], qs[s]);
                    }
                    qrelease(L->Q);
                }
                Live *tmp = live; live = nlive; nlive = tmp;
                int tc = capl; capl = capnl; capnl = tc;
                nl = nnl;
                if (changed) { used++; maxpq = p > q ? p : q; }
                if (getenv("COVER_VERBOSE")) {
                    int dm[3] = {0, 0, 0};
                    for (int t = 0; t < nl; t++) dm[dimp(&live[t].P)]++;
                    fprintf(stderr, "  dir %d,%d: ncyl %d live %d dims %d %d %d\n", p, q, DIR->ncyl, nl, dm[0], dm[1], dm[2]);
                }
                if (nl > MAXLIVE) { big = 1; break; }
                int hd = 0;
                for (int t = 0; t < nl; t++) if (live[t].P.n >= 2) { hd = 1; break; }
                if (!hd && (nl == 0 || !getenv("COVER_ALLDIRS"))) break;
            }
            for (int t = 0; t < nl; t++) {
                int d = dimp(&live[t].P);
                if (d == 0) {
                    nlp++;
                    Pt S = live[t].P.v[0];
                    if (S.d != 1) nonlat++;
                    if (getenv("COVER_PTS")) fprintf(stderr, "PT %lld %lld/%lld,%lld/%lld\n", rid, S.x + sx * S.d, S.d, S.y + sy * S.d, S.d);
                }
                else if (d == 1) nle++; else nlf++;
            }
            if (big) status = "BIG";
            else if (nle || nlf) {
                status = "RESID";
                if (getenv("COVER_RINFO")) {
                    /* centres: convex corners and flat boundary points */
                    int nc2 = 0, QX[256], QY[256];
                    for (int x = 0; x < G - 1; x++) for (int y = 0; y < G - 1; y++) {
                        int ty = ptype(x, y);
                        if ((ty == 1 || ty == 2) && nc2 < 256) { QX[nc2] = x; QY[nc2] = y; nc2++; }
                    }
                    /* where is the residue?  For each live cell s: the convex corner
                       nearest (L-inf) to its representative point, and the radius of
                       s around it; same for every polygon of Q(s).  Floating point,
                       for reporting only. */
                    static unsigned char pr[256][256];
                    memset(pr, 0, sizeof pr);
                    double rl = 0, rq = 0;
                    for (int t = 0; t < nl; t++) {
                        int ci; double r = poly_corner(&live[t].P, nc2, QX, QY, &ci);
                        if (r > rl) rl = r;
                        for (int k = 0; k < live[t].Q->n; k++) {
                            int cj; double r2 = poly_corner(&live[t].Q->a[k].P, nc2, QX, QY, &cj);
                            if (r2 > rq) rq = r2;
                        }
                    }
                    /* an open pair (s, t) has s in Q(t) and t in Q(s), so both lie in the
                       boxes of radius rq around convex corners.  Pair the corners: c for s
                       when the live cell of s meets the box around c (exact clip with a
                       rational radius >= rq), c' for t from the polygon of Q(s). */
                    ll RN = (ll)(rq * 1000000) + 2, RD = 1000000;
                    for (int t = 0; t < nl; t++)
                        for (int c = 0; c < nc2; c++) {
                            Poly W = live[t].P;
                            clip(&W, RD, 0, RD * QX[c] + RN); clip(&W, -RD, 0, -RD * QX[c] + RN);
                            clip(&W, 0, RD, RD * QY[c] + RN); clip(&W, 0, -RD, -RD * QY[c] + RN);
                            if (W.n == 0) continue;
                            for (int k = 0; k < live[t].Q->n; k++) {
                                int cj; poly_corner(&live[t].Q->a[k].P, nc2, QX, QY, &cj);
                                pr[c][cj] = pr[cj][c] = 1;
                            }
                        }
                    if (getenv("COVER_DUMP"))
                        for (int t = 0; t < nl; t++) {
                            fprintf(stderr, "LIVE %d", dimp(&live[t].P));
                            for (int v = 0; v < live[t].P.n; v++) fprintf(stderr, " %.5f %.5f", (double)live[t].P.v[v].x / live[t].P.v[v].d + sx, (double)live[t].P.v[v].y / live[t].P.v[v].d + sy);
                            fprintf(stderr, " | Q");
                            for (int k = 0; k < live[t].Q->n; k++) {
                                const Poly *K = &live[t].Q->a[k].P;
                                fprintf(stderr, " [");
                                for (int v = 0; v < K->n; v++) fprintf(stderr, " %.5f %.5f", (double)K->v[v].x / K->v[v].d + sx, (double)K->v[v].y / K->v[v].d + sy);
                                fprintf(stderr, " ]");
                            }
                            fprintf(stderr, "\n");
                        }
                    printf("RINFO %lld live_radius %.6f Q_radius %.6f |", rid, rl, rq);
                    for (int i = 0; i < nc2; i++) for (int j = i; j < nc2; j++)
                        if (pr[i][j]) printf(" (%d,%d)-(%d,%d)", QX[i] + sx, QY[i] + sy, QX[j] + sx, QY[j] + sy);
                    printf("\n");
                }
            }
            else {
                /* pairs of live points (s, t): resolved if t is outside Q(s) or s is outside Q(t) */
                for (int i = 0; i < nl; i++) for (int j = i + 1; j < nl; j++) {
                    Pt S = live[i].P.v[0], T = live[j].P.v[0];
                    if (in_qset(live[i].Q, T) && in_qset(live[j].Q, S)) {
                        if (S.d == 1 && T.d == 1) {
                            ull++;
                            if (getenv("COVER_LL")) fprintf(stderr, "LL %lld,%lld;%lld,%lld\n", S.x + sx, S.y + sy, T.x + sx, T.y + sy);
                            continue;
                        }
                        unl++;
                        size_t L0 = strlen(ptsbuf);
                        if (L0 < sizeof ptsbuf - 128)
                            snprintf(ptsbuf + L0, sizeof ptsbuf - L0, " %lld/%lld,%lld/%lld;%lld/%lld,%lld/%lld",
                                     S.x + sx * S.d, S.d, S.y + sy * S.d, S.d, T.x + sx * T.d, T.d, T.y + sy * T.d, T.d);
                        else trunc_ = 1;
                    }
                }
                if (trunc_) { fprintf(stderr, "pair list truncated\n"); exit(8); }
            }
            for (int t = 0; t < nl; t++) qrelease(live[t].Q);
            nl = 0;
        }
        printf("ROOM %lld %d %d %s %d %d %d %d %d %d %d %d |", rid, area, W, status, used, maxpq, nlp, nle, nlf, nonlat, ull, unl);
        for (int c = 0; c < area; c++) printf(" %d %d", ox[c], oy[c]);
        printf(" |%s\n", ptsbuf);
        fflush(stdout);
        for (int c = 0; c < ncell; c++) cellid[CX[c]][CY[c]] = -1;
    }
    return 0;
}
