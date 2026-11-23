/* Test of the lemma path families of theorems.md on metric rooms.
 *
 * Input (stdin):
 *   TYPE nx ny mask nrec
 *   nrec lines: X1 Y1 X2 Y2 lem swap p1a p1c p1e p2a p2c p2e r2a r2i nc (a i j c e) x nc
 *   then either
 *     ALL B            every gap vector with sum(x gaps) <= B and sum(y gaps) <= B
 *     ROOM gx.. gy..   one room with the given gap lengths (repeat)
 *   END
 * Options (argv): pairs=all|same|diff  shoot=N (direction bound for uncovered pairs,
 *   0 = skip)  dump=N (print the first N traced certificates per type)
 *
 * For every room and every pair of distinct interior lattice points the
 * recipe of the pair's position types is solved with exact integer
 * arithmetic, and each solution is traced in the room by an integer billiard
 * tracer that does not use the recipe.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
typedef __int128 i128;

#define MAXB 40
static int W_, H_;                       /* room bounding box */
static unsigned char cell[MAXB + 2][MAXB + 2];   /* cell[i+1][j+1] */
#define C(i, j) cell[(i) + 1][(j) + 1]

static int npt(int x, int y) { return C(x - 1, y - 1) + C(x, y - 1) + C(x - 1, y) + C(x, y); }

/* Billiard tracer. Start at lattice point (x,y), unfolded displacement
 * (DX,DY). Returns 1 if no vertex is met in (0,1]; end point and end signs in
 * *ex,*ey,*esx,*esy (signs after reflection if the end point is on a wall).
 * Returns 0 if a vertex is met, -1 on an inconsistency. */
static int trace(int x, int y, ll DX, ll DY, int *ex, int *ey, int *esx, int *esy) {
    int sx = DX > 0 ? 1 : (DX < 0 ? -1 : 0), sy = DY > 0 ? 1 : (DY < 0 ? -1 : 0);
    ll ax = DX < 0 ? -DX : DX, ay = DY < 0 ? -DY : DY;
    if (ax == 0 || ay == 0) {            /* axis-parallel: lattice point every unit step */
        ll n = ax + ay;
        for (ll s = 1; s <= n; s++) {
            x += sx; y += sy;
            int k = npt(x, y);
            if (k == 4) continue;
            if (k != 2) return 0;
            /* flat wall point: wall must be perpendicular to the motion */
            int horiz = (C(x - 1, y - 1) && C(x, y - 1)) || (C(x - 1, y) && C(x, y));
            if (sx != 0) { if (horiz) return -1; sx = -sx; }
            else { if (!horiz) return -1; sy = -sy; }
        }
        *ex = x; *ey = y; *esx = sx; *esy = sy; return 1;
    }
    int cx = sx > 0 ? x : x - 1, cy = sy > 0 ? y : y - 1;
    if (!C(cx, cy)) return -1;
    ll i = 1, j = 1;                     /* next vertical / horizontal crossing index */
    for (;;) {
        ll l = i * ay, r = j * ax;       /* compare i/ax with j/ay */
        if (l < r) {                     /* vertical grid line */
            if (C(cx + sx, cy)) cx += sx; else sx = -sx;
            i++;
        } else if (l > r) {
            if (C(cx, cy + sy)) cy += sy; else sy = -sy;
            j++;
        } else {                         /* lattice point */
            int px = sx > 0 ? cx + 1 : cx, py = sy > 0 ? cy + 1 : cy;
            int k = npt(px, py);
            if (k == 4) { cx += sx; cy += sy; }
            else if (k == 2) {
                int horiz = (C(px - 1, py - 1) && C(px, py - 1)) || (C(px - 1, py) && C(px, py));
                int vert = (C(px - 1, py - 1) && C(px - 1, py)) || (C(px, py - 1) && C(px, py));
                if (horiz) { sy = -sy; cx += sx; }
                else if (vert) { sx = -sx; cy += sy; }
                else return 0;           /* pinch: not in a strictly simple room */
                if (!C(cx, cy)) return -1;
            } else return 0;
            if (i == ax && j == ay) { *ex = px; *ey = py; *esx = sx; *esy = sy; return 1; }
            i++; j++;
        }
        if (i > ax + 1 || j > ay + 1) return -1;
    }
}

/* ------------------------------------------------------------ recipes */
typedef struct {
    int lem, swap, p1a, p1c, p1e, p2a, p2c, p2e, r2a, r2i, nc;
    int ca[2], ci[2], cj[2], cc[2], ce[2];
} Recipe;
static int nx, ny;
static unsigned long long mask;
static Recipe *rec; static int nrec;
static int *lut;                         /* (X1,Y1,X2,Y2) -> recipe index + 1, sign = reversed */
#define LD 34
static int gx[20], gy[20], cxs[20], cys[20];
static ll coord(int axis, int idx) { return axis == 0 ? cxs[idx] : cys[idx]; }

static ll fdiv(i128 a, i128 b) { i128 q = a / b; if ((a % b != 0) && ((a < 0) != (b < 0))) q--; return (ll)q; }
static ll cdiv(i128 a, i128 b) { return -fdiv(-a, b); }

/* statistics per lemma code */
#define NL 9
static ll st_pairs[NL], st_ok[NL], st_allcls[NL], st_nosol[NL], st_badtrace[NL], st_cand[NL], st_hole[NL];
static ll st_rooms, st_unc, st_unc_lit, st_unc_lit2, st_unc_undecided, st_maxk1, st_maxlen;
static int dump_left, opt_pairs = 0, opt_shoot = 0, opt_shoot2 = 0, opt_dump = 0, opt_k1max = 20000;

static int check_cons(const Recipe *R, int c, const ll *Pt, const ll *Qt) {
    int a = R->ca[c], o = 1 - a;
    ll L = 2 * coord(a, R->ci[c]) - coord(a, R->cj[c]);
    ll ctr = coord(o, R->cc[c]), w = llabs(coord(o, R->ce[c]) - ctr);
    ll Ua = Qt[a] - Pt[a], Uo = Qt[o] - Pt[o];
    if (Ua == 0) return 0;
    if (!((Pt[a] < L && L < Qt[a]) || (Qt[a] < L && L < Pt[a]))) return 0;
    /* o* = Pt[o] + (L-Pt[a])*Uo/Ua in (ctr-w, ctr+w) */
    i128 num = (i128)(L - Pt[a]) * Uo, lo = (i128)(ctr - w - Pt[o]) * Ua, hi = (i128)(ctr + w - Pt[o]) * Ua;
    if (Ua > 0) return lo < num && num < hi;
    return hi < num && num < lo;
}

static void print_room(void) {
    printf("  type nx=%d ny=%d mask=%llu gx=", nx, ny, mask);
    for (int i = 0; i < nx; i++) printf("%d,", gx[i]);
    printf(" gy=");
    for (int j = 0; j < ny; j++) printf("%d,", gy[j]);
    printf("\n");
}

/* Solve the recipe for the ordered pair (S,T) of room points. Returns number of classes solved. */
static void do_pair(const Recipe *R, const int *S, const int *T) {
    int l = R->lem;
    const int *P = R->swap ? T : S, *Q = R->swap ? S : T;
    st_pairs[l]++;
    ll Qr[2] = {Q[0], Q[1]};
    if (R->r2a >= 0) Qr[R->r2a] = 2 * coord(R->r2a, R->r2i) - Qr[R->r2a];
    int ex, ey, esx, esy;
    if (R->p2a < 0) {                    /* A, A2: one segment */
        st_cand[l]++;
        int r = trace(P[0], P[1], Qr[0] - P[0], Qr[1] - P[1], &ex, &ey, &esx, &esy);
        if (r == 1 && ex == Q[0] && ey == Q[1]) { st_ok[l]++; st_allcls[l]++; }
        else { st_badtrace[l]++; printf("BADTRACE lem=%d r=%d S=(%d,%d) T=(%d,%d)\n", l, r, S[0], S[1], T[0], T[1]); print_room(); }
        return;
    }
    int a2 = R->p2a, a1 = R->p1a;
    ll c2 = coord(a2, R->p2c), w2 = llabs(coord(a2, R->p2e) - c2);
    ll c1 = 0, w1 = 0;
    if (a1 >= 0) { c1 = coord(a1, R->p1c); w1 = llabs(coord(a1, R->p1e) - c1); }
    int cT = R->nc - 1, ca = R->ca[cT];
    ll L2 = 2 * coord(ca, R->ci[cT]) - coord(ca, R->cj[cT]);
    int ncls = (a1 >= 0) ? 4 : 2, found[4] = {0, 0, 0, 0}, nfound = 0, holes = 0;
    ll k1lim = (a1 >= 0) ? opt_k1max : 0;
    for (ll kk = 0; kk <= 2 * k1lim && nfound < ncls; kk++) {
        ll k1 = (kk & 1) ? (kk + 1) / 2 : -(kk / 2);
        for (int e1 = 0; e1 < (a1 >= 0 ? 2 : 1); e1++) {
            ll Pt[2] = {P[0], P[1]};
            int eps1 = e1 ? -1 : 1;
            if (a1 >= 0) Pt[a1] = c1 + eps1 * (P[a1] - c1) + 2 * w1 * k1;
            ll D1 = L2 - Pt[ca], DT = Qr[ca] - Pt[ca];
            if (D1 == 0 || (D1 > 0) != (DT > 0) || llabs(DT) <= llabs(D1)) continue;
            ll aD1 = llabs(D1), aDT = llabs(DT), Po = Pt[a2];
            for (int e2 = 0; e2 < 2; e2++) {
                int cls = e1 * 2 + e2;
                if (found[cls]) continue;
                int eps2 = e2 ? -1 : 1;
                ll base = c2 + eps2 * (Qr[a2] - c2);
                i128 lo = (i128)(c2 - w2 - Po) * aDT - (i128)(base - Po) * aD1;
                i128 hi = (i128)(c2 + w2 - Po) * aDT - (i128)(base - Po) * aD1;
                i128 m = (i128)2 * w2 * aD1;
                ll klo = fdiv(lo, m) + 1, khi = cdiv(hi, m) - 1;
                for (ll k2 = klo; k2 <= khi && !found[cls]; k2++) {
                    ll Qt[2] = {Qr[0], Qr[1]};
                    Qt[a2] = base + 2 * w2 * k2;
                    int okc = 1;
                    for (int c = 0; c < R->nc; c++) if (!check_cons(R, c, Pt, Qt)) { okc = 0; break; }
                    if (!okc) continue;
                    ll V[2] = {Qt[0] - Pt[0], Qt[1] - Pt[1]};
                    if (a1 >= 0) V[a1] *= eps1;
                    st_cand[l]++;
                    int r = trace(P[0], P[1], V[0], V[1], &ex, &ey, &esx, &esy);
                    if (r == 1 && ex == Q[0] && ey == Q[1]) {
                        found[cls] = 1; nfound++;
                        if (llabs(k1) > st_maxk1) st_maxk1 = llabs(k1);
                        if (llabs(V[0]) + llabs(V[1]) > st_maxlen) st_maxlen = llabs(V[0]) + llabs(V[1]);
                        if (dump_left > 0) {
                            dump_left--;
                            printf("DUMP %d %d %lld %lld %d %d lem=%d cells=", P[0], P[1], V[0], V[1], Q[0], Q[1], l);
                            for (int i = 0; i < W_; i++) for (int j = 0; j < H_; j++) if (C(i, j)) printf("%d,%d;", i, j);
                            printf("\n");
                        }
                    } else if (l == 4 && r == 0) {
                        holes++;         /* Lemma B2 allows one corner hit */
                    } else {
                        st_badtrace[l]++;
                        printf("BADTRACE lem=%d r=%d S=(%d,%d) T=(%d,%d) V=(%lld,%lld) end=(%d,%d)\n", l, r, S[0], S[1], T[0], T[1], V[0], V[1], ex, ey);
                        print_room();
                    }
                }
            }
        }
    }
    st_hole[l] += holes;
    if (nfound > 0) st_ok[l]++;
    if (nfound == ncls) st_allcls[l]++;
    if (nfound == 0) { st_nosol[l]++; printf("NOSOL lem=%d S=(%d,%d) T=(%d,%d)\n", l, S[0], S[1], T[0], T[1]); print_room(); }
    else if (nfound < ncls && l != 4) { printf("CLASSMISS lem=%d found=%d/%d S=(%d,%d) T=(%d,%d)\n", l, nfound, ncls, S[0], S[1], T[0], T[1]); print_room(); }
}

static int gcd_(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

/* brute-force shooter for pairs without a certificate */
static int shoot(const int *S, const int *T, int bound, int *bu, int *bv, int *bsteps) {
    for (int s = 1; s <= bound; s++) for (int u = 0; u <= s; u++) {
        int v = s - u;
        if (gcd_(u, v) != 1) continue;
        for (int sg = 0; sg < 4; sg++) {
            int dx = (sg & 1) ? -u : u, dy = (sg & 2) ? -v : v;
            if ((u == 0 && (sg & 1)) || (v == 0 && (sg & 2))) continue;
            int x = S[0], y = S[1], sx = dx, sy = dy, steps = 0;
            int lim = 4 * (W_ + 1) * (H_ + 1) + 8;
            while (steps < lim) {
                int ex, ey, esx, esy;
                int r = trace(x, y, sx, sy, &ex, &ey, &esx, &esy);
                if (r != 1) break;
                steps++;
                if (ex == T[0] && ey == T[1]) { *bu = dx; *bv = dy; *bsteps = steps; return 1; }
                x = ex; y = ey; sx = esx * u; sy = esy * v;
                if (x == S[0] && y == S[1] && sx == dx && sy == dy) break;
            }
        }
    }
    return 0;
}

static int pts[MAXB * MAXB][2], ptype[MAXB * MAXB][2];
static void do_room(void) {
    cxs[0] = 0; for (int i = 0; i < nx; i++) cxs[i + 1] = cxs[i] + gx[i];
    cys[0] = 0; for (int j = 0; j < ny; j++) cys[j + 1] = cys[j] + gy[j];
    W_ = cxs[nx]; H_ = cys[ny];
    memset(cell, 0, sizeof cell);
    for (int i = 0; i < nx; i++) for (int j = 0; j < ny; j++) if ((mask >> (i + nx * j)) & 1)
        for (int x = cxs[i]; x < cxs[i + 1]; x++) for (int y = cys[j]; y < cys[j + 1]; y++) C(x, y) = 1;
    int n = 0, ix = 0;
    for (int x = 1; x < W_; x++) {
        while (cxs[ix + 1] <= x) ix++;
        int iy = 0;
        for (int y = 1; y < H_; y++) {
            while (cys[iy + 1] <= y) iy++;
            if (npt(x, y) != 4) continue;
            pts[n][0] = x; pts[n][1] = y;
            ptype[n][0] = (cxs[ix] == x) ? 2 * ix : 2 * ix + 1;
            ptype[n][1] = (cys[iy] == y) ? 2 * iy : 2 * iy + 1;
            n++;
        }
    }
    st_rooms++;
    dump_left = opt_dump;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
        int same = ((pts[a][0] ^ pts[b][0]) & 1) == 0 && ((pts[a][1] ^ pts[b][1]) & 1) == 0;
        if ((opt_pairs == 1 && !same) || (opt_pairs == 2 && same)) continue;
        int key = ((ptype[a][0] * LD + ptype[a][1]) * LD + ptype[b][0]) * LD + ptype[b][1];
        int v = lut[key];
        if (v == 0) { printf("NOLUT\n"); exit(1); }
        const Recipe *R = &rec[abs(v) - 1];
        const int *S = v > 0 ? pts[a] : pts[b], *T = v > 0 ? pts[b] : pts[a];
        if (R->lem == 0) {
            st_unc++;
            if (opt_shoot > 0) {
                int u, w, s;
                if (shoot(S, T, opt_shoot, &u, &w, &s)) st_unc_lit++;
                else if (opt_shoot2 > opt_shoot && shoot(S, T, opt_shoot2, &u, &w, &s)) {
                    st_unc_lit++; st_unc_lit2++;
                    printf("BOUND2 S=(%d,%d) T=(%d,%d) dir=(%d,%d) steps=%d\n", S[0], S[1], T[0], T[1], u, w, s); print_room();
                } else {
                    st_unc_undecided++;
                    printf("UNDECIDED S=(%d,%d) T=(%d,%d) bound=%d\n", S[0], S[1], T[0], T[1], opt_shoot2 > opt_shoot ? opt_shoot2 : opt_shoot);
                    print_room(); printf("  cells=");
                    for (int i = 0; i < W_; i++) for (int j = 0; j < H_; j++) if (C(i, j)) printf("%d,%d;", i, j);
                    printf("\nSTOPPED after rooms=%lld\n", st_rooms); fflush(stdout); exit(3);
                }
            }
            continue;
        }
        if (R->lem == 8) {               /* Lemma D has no fixed family: confirm by shooting */
            int u, w, s;
            st_pairs[8]++;
            if (shoot(S, T, opt_shoot > 0 ? opt_shoot : 40, &u, &w, &s) || (opt_shoot2 > 0 && shoot(S, T, opt_shoot2, &u, &w, &s))) st_ok[8]++;
            else { st_nosol[8]++; printf("NOSOL lem=8 S=(%d,%d) T=(%d,%d)\n", S[0], S[1], T[0], T[1]); print_room(); }
            continue;
        }
        do_pair(R, S, T);
    }
}

static void rec_gaps(int axis, int pos, int left, int B) {
    int n = axis == 0 ? nx : ny; int *g = axis == 0 ? gx : gy;
    if (pos == n) { if (axis == 0) rec_gaps(1, 0, B, B); else do_room(); return; }
    for (int v = 1; v <= left - (n - 1 - pos); v++) { g[pos] = v; rec_gaps(axis, pos + 1, left - v, B); }
}

int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "pairs=same")) opt_pairs = 1;
        else if (!strcmp(argv[i], "pairs=diff")) opt_pairs = 2;
        else if (!strncmp(argv[i], "shoot=", 6)) opt_shoot = atoi(argv[i] + 6);
        else if (!strncmp(argv[i], "shoot2=", 7)) opt_shoot2 = atoi(argv[i] + 7);
        else if (!strncmp(argv[i], "dump=", 5)) opt_dump = atoi(argv[i] + 5);
        else if (!strncmp(argv[i], "k1max=", 6)) opt_k1max = atoi(argv[i] + 6);
    }
    lut = malloc(sizeof(int) * LD * LD * LD * LD);
    char tok[64];
    ll ntypes = 0;
    while (scanf("%63s", tok) == 1) {
        if (!strcmp(tok, "TYPE")) {
            if (scanf("%d %d %llu %d", &nx, &ny, &mask, &nrec) != 4) return 1;
            ntypes++;
            free(rec); rec = calloc(nrec, sizeof(Recipe));
            memset(lut, 0, sizeof(int) * LD * LD * LD * LD);
            for (int r = 0; r < nrec; r++) {
                int X1, Y1, X2, Y2; Recipe *R = &rec[r];
                if (scanf("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d", &X1, &Y1, &X2, &Y2, &R->lem, &R->swap,
                          &R->p1a, &R->p1c, &R->p1e, &R->p2a, &R->p2c, &R->p2e, &R->r2a, &R->r2i, &R->nc) != 15) return 1;
                for (int c = 0; c < R->nc; c++)
                    if (scanf("%d %d %d %d %d", &R->ca[c], &R->ci[c], &R->cj[c], &R->cc[c], &R->ce[c]) != 5) return 1;
                lut[((X1 * LD + Y1) * LD + X2) * LD + Y2] = r + 1;
                if (X1 != X2 || Y1 != Y2) lut[((X2 * LD + Y2) * LD + X1) * LD + Y1] = -(r + 1);
            }
        } else if (!strcmp(tok, "ALL")) {
            int B; if (scanf("%d", &B) != 1) return 1;
            rec_gaps(0, 0, B, B);
        } else if (!strcmp(tok, "ROOM")) {
            for (int i = 0; i < nx; i++) if (scanf("%d", &gx[i]) != 1) return 1;
            for (int j = 0; j < ny; j++) if (scanf("%d", &gy[j]) != 1) return 1;
            do_room();
        } else if (!strcmp(tok, "END")) break;
    }
    const char *nm[NL] = {"none", "A", "A2", "B", "B2", "C-par", "C-perp", "C-same", "D"};
    printf("SUMMARY types=%lld rooms=%lld maxk1=%lld maxlen=%lld\n", ntypes, st_rooms, st_maxk1, st_maxlen);
    for (int l = 1; l < NL; l++)
        printf("LEMMA %s pairs=%lld lit=%lld allclasses=%lld nosol=%lld badtrace=%lld candidates=%lld holes=%lld\n",
               nm[l], st_pairs[l], st_ok[l], st_allcls[l], st_nosol[l], st_badtrace[l], st_cand[l], st_hole[l]);
    printf("UNCOVERED pairs=%lld shot_lit=%lld needed_bound2=%lld undecided=%lld\n", st_unc, st_unc_lit, st_unc_lit2, st_unc_undecided);
    return 0;
}
