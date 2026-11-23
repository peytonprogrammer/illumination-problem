/* check.c -- d56 finite check (spec: ../d50-review-d49/review.md section 7).
 *
 * One process per job.  Built from copies of
 *   ../d9-census-w22/partA-enum.c  (Redelmeier enumeration, SPLIT = 11 round-robin split,
 *                                   canonical representative of the 8 symmetries),
 *   ../d9-census-w22/partA-cert.c  (exact shooter in the 4-fold unfolding, room scaled by the
 *                                   mark denominator, one-cylinder classifier, HNF),
 *   ../d46-cert-check/cert_check.c (pillowcase monodromy gen(), closure, mark lifts),
 *   ../d10-mechanisms/unified_test.py (Par / Rig with live graph / Cut definitions).
 *
 * Set A ("D20"): strictly simple rooms, W = 20, area 20.  Pairs: interior lattice points S, T
 *   with T - S not in 2 Z^2.  Base Lambda = Z^2.
 * Set E: normalized class (iii) rooms (no one-cylinder direction with max(p, q) <= 15), 12 <= W
 *   <= 20, area <= W - 4 (= 2r).  Pairs: interior points S != T of the (1/4)-grid, not both in
 *   Z^2, with sigma~, tau~ in Lambda for some lift pair (sigma~ in {S, rho S}, rho(x, y) =
 *   (x, -y)) for one of the 10 lattices Z^2 < Lambda < (1/4) Z^2 of index 2 or 4.  Pairs inside
 *   (1/2) Z^2 are skipped when area <= 14 (Part A grid run).  The W = 16, area 8 room also gets
 *   the 12 cyclic index-6 lattices at scale 6.  Rooms sampled at CERTRATE also get every
 *   (1/3)-grid pair not in Z^2 x Z^2 (residue (b) regression).
 *
 * Primary test: shoot primitive directions p + q <= 40, then <= 120 for the rest; every hit is
 *   re-checked by verify_plane (independent tracer).  Lit = verified path.
 * Fallback (survivors, and a deterministic CERTRATE-per-million sample of pairs): certificate
 *   test over P_Lambda.  Lambda = Z^2 directly; rectangular Lambda = diag(1/a, 1/b) Z^2 through
 *   the room A R (d47 Prop 2.1, as in ../d49-even-index/check_even.py).  Sheared Lambda: not
 *   implemented, counted as cert_na (see README).  Per lift pair and target: Par via B_x, Rig via
 *   R_y (live graph), Cut over all 2- and 3-block factors where Lemma Z allows.
 *   A pair is certified when, for one admissible Lambda, all 4 lift pairs are certified at every
 *   target.  Tripwires: d50 section 7 list plus Lemma Z bounds.
 *
 * Exit 0 = done (SUMMARY line written), 10 = certified pair (POSITIVE lines), 11 = tripwire.
 *
 * usage: check A NJ J CERTRATE            (enumerate Set A job J of NJ)
 *        check E NJ J CERTRATE            (enumerate Set E job J of NJ)
 *        check stdin MODE CERTRATE        (rooms "area W x0 y0 ..." on stdin; MODE A, E, or
 *                                          X = all interior lattice pairs, any class, no W filter)
 *        check pair BOUND                 (stdin "scale k S x y T x y | area W cells": shoot + cert)
 * Environment: CHECK_CORRUPT=1 corrupts every path before verification (validation only);
 *              CHECK_COUNTONLY=1 with CHECK_NMAX / CHECK_AMIN / CHECK_WLO / CHECK_WHI: count rooms only;
 *              CHECK_TESTROOM="area W cells": process this room first, all pairs (alert-path test);
 *              CHECK_DEBUG=1 prints per lift pair and target the certificate kinds (1 Par, 2 Rig, 4 Cut).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/resource.h>

int verify_plane(int ncell, const int *cx, const int *cy,
                 int sx0, int sy0, int dx, int dy, int m, int tx, int ty);

/* ======================= counters ======================= */
static long long C_rooms, C_rooms_pairs, C_pairs, C_lit40, C_lit120, C_surv, C_vfail, C_reduced, C_c3,
    C_certpairs, C_certified, C_trip, C_certna, C_lpflag, C_tgtcert, C_g3rooms, C_g3pairs, C_g3lit,
    C_g6pairs, C_g6lit, C_corrupt_rej;
static long long C_room_WA[24][24], C_c3_WA[24][24], C_red_WA[24][24];
static long long C_kind[4];             /* certificate instances: Par, Rig, Cut */
static long long C_tw[6];
static int SETMODE;                     /* 'A', 'E', 'X' */
static long long CERTRATE = 10000;      /* per million */
static long long JOBID = 0, ROOMID = 0;
static int COUNTONLY = 0, CORRUPT = 0, DEBUG = 0, CUR_A = 1, CUR_B = 1, CUR_SX, CUR_SY, CUR_TX, CUR_TY;

static uint64_t mix(uint64_t x) {
    x += 0x9E3779B97F4A7C15ULL; x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL; return x ^ (x >> 31);
}
static int sampled(uint64_t a, uint64_t b) {
    return (long long)(mix(mix(JOBID * 1000003ULL + ROOMID) ^ (a * 7919ULL + b)) % 1000000ULL) < CERTRATE;
}

/* ======================= shooter (partA-cert.c) ======================= */
#define MAXC 400
#define G 104
#define MAXI 400
static int n, cx[MAXC], cy[MAXC], cellid[G][G], nsq;
static int H[4 * MAXC], V[4 * MAXC], HI[4 * MAXC], LAB[4 * MAXC], BLK[4 * MAXC];
static const int SX[4] = {1, -1, 1, -1}, SY[4] = {1, 1, -1, -1};
static int has(int x, int y) { return x >= 0 && y >= 0 && x < G && y < G && cellid[x][y] >= 0; }
static int cnt_around(int x, int y) { return has(x - 1, y - 1) + has(x, y - 1) + has(x - 1, y) + has(x, y); }
static long long gcdll(long long a, long long b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { long long t = a % b; a = b; b = t; } return a; }
static int gcd(int a, int b) { return (int)gcdll(a, b); }

static int ndir, ndir40, DP_[12000], DQ_[12000], WLEN[12000];
static unsigned char WORD[12000][240];
static void make_dirs(int bound) {
    ndir = 0;
    for (int s = 1; s <= bound; s++) {
        for (int p = s; p >= 0; p--) {
            int q = s - p;
            if (gcd(p, q) != 1) continue;
            DP_[ndir] = p; DQ_[ndir] = q;
            int L = 0;
            if (p >= 1 && q >= 1) {
                int a = 1, b = 1;
                while (a < p || b < q) {
                    long uv = (a < p) ? (long)q * a : 1L << 60;
                    long uh = (b < q) ? (long)p * b : 1L << 60;
                    if (uv < uh) { WORD[ndir][L++] = 0; a++; } else { WORD[ndir][L++] = 1; b++; }
                }
            }
            WLEN[ndir] = L; ndir++;
        }
        if (s == 40) ndir40 = ndir;
    }
}
static int sq(int c, int sh) { return 4 * c + sh; }
static void build_origami(void) {
    nsq = 4 * n;
    for (int c = 0; c < n; c++)
        for (int sh = 0; sh < 4; sh++) {
            int s = sq(c, sh), i = cx[c], j = cy[c], sx = SX[sh], sy = SY[sh];
            H[s] = has(i + sx, j) ? sq(cellid[i + sx][j], sh) : sq(c, sh ^ 1);
            V[s] = has(i, j + sy) ? sq(cellid[i][j + sy], sh) : sq(c, sh ^ 2);
            int X = i + (sx < 0), Y = j + (sy < 0);
            LAB[s] = X * G + Y;
            int k = cnt_around(X, Y);
            BLK[s] = (k == 1 || k == 3);
        }
    for (int s = 0; s < nsq; s++) HI[H[s]] = s;
}
static int step(int s, int d) {
    int p = DP_[d], q = DQ_[d];
    if (q == 0) return H[s];
    if (p == 0) return V[s];
    int c = s;
    for (int t = 0; t < WLEN[d]; t++) c = WORD[d][t] ? V[c] : H[c];
    return H[V[c]];
}

static int npt, ptx[4 * MAXC], pty[4 * MAXC], ptk[4 * MAXC], mark[G][G], markid = 0;
static int build_room(int area0, const int *ox0, const int *oy0, int scale) {
    if (area0 * scale * scale > MAXC) return 0;
    n = 0;
    for (int c = 0; c < area0; c++)
        for (int a = 0; a < scale; a++)
            for (int b = 0; b < scale; b++) {
                int x = ox0[c] * scale + a + 1, y = oy0[c] * scale + b + 1;
                if (x >= G - 2 || y >= G - 2) { for (int t = 0; t < n; t++) cellid[cx[t]][cy[t]] = -1; return 0; }
                cx[n] = x; cy[n] = y; cellid[x][y] = n; n++;
            }
    markid++; npt = 0;
    for (int c = 0; c < n; c++)
        for (int d = 0; d < 4; d++) {
            int X = cx[c] + (d & 1), Y = cy[c] + (d >> 1);
            if (mark[X][Y] == markid) continue;
            mark[X][Y] = markid;
            ptx[npt] = X; pty[npt] = Y; ptk[npt] = cnt_around(X, Y); npt++;
        }
    build_origami();
    return 1;
}
static void clear_room(void) { for (int c = 0; c < n; c++) cellid[cx[c]][cy[c]] = -1; }

/* res[a][b], a < b: 0 not wanted, 1 lit (bound 40), 5 lit (bound 120), 2 open, 3 verify failure */
static unsigned char res[MAXI][MAXI];
/* Segment shooter.  For direction d, step(., d) is a permutation of the squares of the 4-fold
 * unfolding; cutting its cycles at corner squares (BLK) gives segments.  Two points whose squares lie
 * on one segment are joined by the straight path between them (no corner in between): the source is
 * the earlier one, its sheet gives the signs, m is the position difference.  This is the d9 shooter's
 * path set (it walks the same segments from each source), organised per direction.  Every hit is
 * re-checked by verify_plane. */
static int nxt_[4 * MAXC], prv_[4 * MAXC], segid[4 * MAXC], segpos[4 * MAXC], seglen[4 * MAXC];
static void segments(int d) {
    for (int s = 0; s < nsq; s++) { nxt_[s] = step(s, d); prv_[nxt_[s]] = s; segid[s] = -1; }
    int ns = 0;
    for (int pass = 0; pass < 2; pass++)
        for (int s = 0; s < nsq; s++) {
            if (BLK[s] || segid[s] >= 0 || (pass == 0 && !BLK[prv_[s]])) continue;
            int t = s, k = 0;
            while (!BLK[t] && segid[t] < 0) { segid[t] = ns; segpos[t] = k++; t = nxt_[t]; }
            seglen[ns++] = k;
        }
}
static int psq[MAXI][4];
static int rem_a[MAXI * MAXI / 2], rem_b[MAXI * MAXI / 2];
static void shoot_pairs(int ni, const int *ip) {
    static int r_sh[MAXI][MAXI], r_d[MAXI][MAXI], r_m[MAXI][MAXI], r_src[MAXI][MAXI];
    int nr = 0;
    for (int a = 0; a < ni; a++) {
        for (int sh = 0; sh < 4; sh++)
            psq[a][sh] = sq(cellid[ptx[ip[a]] - (SX[sh] < 0)][pty[ip[a]] - (SY[sh] < 0)], sh);
        for (int b = a + 1; b < ni; b++) if (res[a][b] == 2) { rem_a[nr] = a; rem_b[nr] = b; nr++; }
    }
    for (int d = 0; d < ndir && nr; d++) {
        segments(d);
        int code = d < ndir40 ? 1 : 5, k = 0;
        for (int i = 0; i < nr; i++) {
            int a = rem_a[i], b = rem_b[i], hit = 0;
            for (int u = 0; u < 4 && !hit; u++) {
                int su = psq[a][u], g = segid[su];
                if (g < 0) continue;
                for (int v = 0; v < 4 && !hit; v++) {
                    int sv = psq[b][v];
                    if (segid[sv] != g) continue;
                    int m = segpos[sv] - segpos[su];
                    if (m > 0) { r_src[a][b] = a; r_sh[a][b] = su & 3; r_m[a][b] = m; }
                    else if (m < 0) { r_src[a][b] = b; r_sh[a][b] = sv & 3; r_m[a][b] = -m; }
                    else continue;
                    r_d[a][b] = d; res[a][b] = 10 + code; hit = 1;
                }
            }
            if (!hit) { rem_a[k] = a; rem_b[k] = b; k++; }
        }
        nr = k;
    }
    for (int a = 0; a < ni; a++)
        for (int b = a + 1; b < ni; b++) {
            if (res[a][b] < 10) continue;
            int code = res[a][b] - 10, src = r_src[a][b], sh = r_sh[a][b], d = r_d[a][b], m = r_m[a][b];
            int tgt = src == a ? b : a;
            int dx = SX[sh] * DP_[d], dy = SY[sh] * DQ_[d];
            if (CORRUPT) m += 1;              /* validation: a wrong step count must be rejected */
            int ok = verify_plane(n, cx, cy, ptx[ip[src]], pty[ip[src]], dx, dy, m, ptx[ip[tgt]], pty[ip[tgt]]);
            if (CORRUPT && !ok) C_corrupt_rej++;
            res[a][b] = ok ? code : 3;
        }
}

/* ======================= one-cylinder classifier (partA-cert.c) ======================= */
static int cyc_[4 * MAXC * 16], uf_[4 * MAXC * 16], regl[4 * MAXC * 16];
static int ufind(int a) { while (uf_[a] != a) { uf_[a] = uf_[uf_[a]]; a = uf_[a]; } return a; }
static int cyl_count(int p, int q) {
    int ns = nsq * q;
    for (int t = 0; t < ns; t++) cyc_[t] = -1;
    int nc = 0;
    for (int t = 0; t < ns; t++) {
        if (cyc_[t] >= 0) continue;
        int cur = t;
        while (cyc_[cur] < 0) {
            cyc_[cur] = nc;
            int i = cur / q, j = cur % q, k = (j + p) / q;
            for (int z = 0; z < k; z++) i = H[i];
            cur = V[i] * q + (j + p) % q;
        }
        if (cur != t) { fprintf(stderr, "nxt is not a permutation\n"); exit(5); }
        nc++;
    }
    if (nc == 2) return 2;
    for (int c = 0; c < nc; c++) { regl[c] = 1; uf_[c] = c; }
    for (int s = 0; s < nsq; s++) if (BLK[s]) regl[cyc_[s * q]] = 0;
    for (int s = 0; s < nsq; s++) {
        for (int j = 1; j < q; j++)
            if (regl[cyc_[s * q + j]]) { int a = ufind(cyc_[s * q + j - 1]), b = ufind(cyc_[s * q + j]); if (a != b) uf_[a] = b; }
        if (regl[cyc_[s * q]]) { int a = ufind(cyc_[s * q]), b = ufind(cyc_[HI[s] * q + q - 1]); if (a != b) uf_[a] = b; }
    }
    int comps = 0;
    for (int c = 0; c < nc; c++) if (ufind(c) == c) comps++;
    return comps;
}
static int ncd, CP[400], CQ[400];
static void make_cyl_dirs(int B) {
    ncd = 0;
    for (int s = 2; s <= 2 * B; s++)
        for (int p = 1; p <= B; p++) {
            int q = s - p;
            if (q < 1 || q > B || gcd(p, q) != 1) continue;
            CP[ncd] = p; CQ[ncd] = q; ncd++;
        }
}
/* 1 = class (iii): no one-cylinder direction with max(p, q) <= 15 (room built at scale 1) */
static int is_class3(void) {
    for (int d = 0; d < ncd; d++) if (cyl_count(CP[d], CQ[d]) == 2) return 0;
    return 1;
}

/* ======================= certificate test (unit base of a lattice room) ======================= */
#define CM 160
#define CGR 150
static int cn, ccx[CM], ccy[CM], cgrid[CGR][CGR], c_r;
static int ccell(int x, int y) { return (x >= 0 && y >= 0 && x < CGR && y < CGR) ? cgrid[x][y] : -1; }
static void cgen(int px, int py, int ox, int oy, int *g) {         /* cert_check.c gen() */
    for (int k = 0; k < cn; k++) {
        int x = ccx[k], y = ccy[k];
        int ex = ((x - ox) & 1) == px ? x - 1 : x + 1;
        int k1 = ccell(ex, y); if (k1 < 0) k1 = k;
        int x1 = ccx[k1], y1 = ccy[k1];
        int ey = ((y1 - oy) & 1) == py ? y1 - 1 : y1 + 1;
        int k2 = ccell(x1, ey); if (k2 < 0) k2 = k1;
        g[k] = k2;
    }
}
static int gs[8][CM];
static int upar[CM];
static int cfind(int a) { while (upar[a] != a) { upar[a] = upar[upar[a]]; a = upar[a]; } return a; }
/* closure of seed pairs (i, seed[i]) for i with use[i]; returns blocks into lab[] (0..k-1) */
static int closure(const int *seed, const int *use, int *lab) {
    static int qa[CM * CM], qb[CM * CM];
    int qn = 0;
    for (int i = 0; i < cn; i++) upar[i] = i;
    for (int i = 0; i < cn; i++) if (use[i]) {
        int ra = cfind(i), rb = cfind(seed[i]);
        if (ra != rb) { upar[ra] = rb; qa[qn] = i; qb[qn] = seed[i]; qn++; }
    }
    while (qn) {
        qn--; int a = qa[qn], b = qb[qn];
        for (int t = 0; t < 8; t++) {
            int u = gs[t][a], v = gs[t][b], ra = cfind(u), rb = cfind(v);
            if (ra != rb) { upar[ra] = rb; qa[qn] = u; qb[qn] = v; qn++; }
        }
    }
    int k = 0, idx[CM];
    for (int i = 0; i < cn; i++) idx[i] = -1;
    for (int i = 0; i < cn; i++) { int r = cfind(i); if (idx[r] < 0) idx[r] = k++; lab[i] = idx[r]; }
    return k;
}
typedef struct {
    int d, z, p, lab[CM], ncid[4][CM], nlen[4][CM], npts[4], live[4][CM];
} Factor;
static int qtwo[4][CM];                 /* sheet lies in a 2-cycle of g_c */
static void make_factor(Factor *F, const int *lab, int d) {
    F->d = d; F->z = F->p = 0;
    memcpy(F->lab, lab, sizeof(int) * cn);
    int rep[CM];
    for (int i = cn - 1; i >= 0; i--) rep[lab[i]] = i;
    for (int c = 0; c < 4; c++) {
        int ig[CM], seen[CM];
        for (int b = 0; b < d; b++) { ig[b] = lab[gs[c][rep[b]]]; seen[b] = -1; }
        int k = 0;
        for (int b = 0; b < d; b++) if (seen[b] < 0) {
            int L = 0, j = b;
            while (seen[j] < 0) { seen[j] = k; j = ig[j]; L++; }
            F->nlen[c][k] = L; F->live[c][k] = 0;
            if (L == 3) F->z++;
            if (L == 1) F->p++;
            k++;
        }
        F->npts[c] = k;
        for (int b = 0; b < d; b++) F->ncid[c][b] = seen[b];
        for (int i = 0; i < cn; i++) if (qtwo[c][i]) F->live[c][F->ncid[c][lab[i]]] = 1;
    }
}
static int fpoint(const Factor *F, int c, int sheet) { return F->ncid[c][F->lab[sheet]]; }
static int par_ok(const Factor *F, int x, int s, int q) {       /* q over a */
    if (fpoint(F, 0, s) == fpoint(F, 0, q)) return 0;
    for (int k = 0; k < F->npts[x]; k++) if (F->nlen[x][k] == 2) return 0;
    return 1;
}
static int rig_ok(const Factor *F, int x, int s, int q, int qc) { /* q over corner qc (0 or x) */
    int ok = 0;
    for (int y = 1; y <= 3; y++) {
        if (y == x) continue;
        int id = 1;
        for (int k = 0; k < F->npts[y]; k++) if (F->nlen[y][k] != 1) id = 0;
        if (id) ok = 1;
    }
    if (!ok) return 0;
    int na = F->npts[0], nx = F->npts[x], u[2 * CM];
    for (int i = 0; i < na + nx; i++) u[i] = i;
    #define UF(a) ({ int _a = (a); while (u[_a] != _a) { u[_a] = u[u[_a]]; _a = u[_a]; } _a; })
    for (int b = 0; b < F->d; b++) {
        int va = F->ncid[0][b], vx = F->ncid[x][b];
        if (F->live[0][va] && F->live[x][vx]) { int ra = UF(va), rb = UF(na + vx); if (ra != rb) u[ra] = rb; }
    }
    int st = fpoint(F, 0, s);
    int tg = qc == 0 ? fpoint(F, 0, q) : na + fpoint(F, x, q);
    if (!F->live[0][st]) return tg != st;
    return UF(st) != UF(tg);
    #undef UF
}
static int cut_ok(const Factor *F, int x, int s, int q) {
    if (fpoint(F, 0, s) != fpoint(F, 0, q)) return 0;
    for (int c = 0; c <= x; c += x)
        for (int i = 0; i < cn; i++) if (qtwo[c][i] && F->nlen[c][F->ncid[c][F->lab[i]]] != 2) return 0;
    for (int y = 1; y <= 3; y++) if (y != x && F->npts[y] == 1) return 1;
    return 0;
}
/* all factors with 2 or 3 blocks (transitive label propagation) */
static Factor small_f[64];
static int n_small;
static void enum_small(void) {
    static const int P3[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    n_small = 0;
    for (int k = 2; k <= 3; k++) {
        int np = k == 2 ? 2 : 6, total = np * np * np * np;
        for (int code = 0; code < total; code++) {
            int pi[4][3], cc = code;
            for (int c = 0; c < 4; c++) { int w = cc % np; cc /= np; for (int i = 0; i < k; i++) pi[c][i] = k == 2 ? (w ? 1 - i : i) : P3[w][i]; }
            int lab[CM], st[CM], sp = 0, ok = 1, used = 1;
            for (int i = 0; i < cn; i++) lab[i] = -1;
            lab[0] = 0; st[sp++] = 0;
            while (sp && ok) {
                int s = st[--sp];
                for (int c = 0; c < 4 && ok; c++) {
                    int t = gs[c][s], want = pi[c][lab[s]];
                    if (lab[t] < 0) { lab[t] = want; st[sp++] = t; used |= 1 << want; }
                    else if (lab[t] != want) ok = 0;
                }
            }
            if (!ok || used != (1 << k) - 1) continue;
            for (int i = 0; i < cn && ok; i++) if (lab[i] < 0) ok = 0;
            if (!ok) continue;
            /* canonical relabel and dedupe */
            int map[3] = {-1, -1, -1}, nl = 0, can[CM];
            for (int i = 0; i < cn; i++) { if (map[lab[i]] < 0) map[lab[i]] = nl++; can[i] = map[lab[i]]; }
            int dup = 0;
            for (int f = 0; f < n_small && !dup; f++) if (small_f[f].d == k && !memcmp(small_f[f].lab, can, sizeof(int) * cn)) dup = 1;
            if (dup) continue;
            if (n_small >= 64) { fprintf(stderr, "too many small factors\n"); exit(6); }
            make_factor(&small_f[n_small++], can, k);
        }
    }
}

/* lifts of an interior lattice point of corner class c: the two 2-cycles of g_c around it */
static void lifts(int x, int y, int c, int *L) {
    int sw = ccell(x - 1, y - 1), q[4] = {sw, ccell(x, y - 1), ccell(x - 1, y), ccell(x, y)};
    int p = gs[c][sw], other = -1;
    for (int k = 0; k < 4; k++) if (q[k] != sw && q[k] != p) { other = q[k]; break; }
    L[0] = sw; L[1] = other;
}

static FILE *OUT;
static const char *room_desc;           /* text of the room for POSITIVE / TRIPWIRE lines */
static int last_tw;
static void tripwire(const char *what, const char *pairdesc, int kind, int x, int d, int z, int p, int nn) {
    static const char *KN[3] = {"Par", "Rig", "Cut"};
    C_trip++; last_tw = 1;
    fprintf(OUT, "TRIPWIRE %s kind %s target %d d %d delta %d z %d p %d n %d r %d | %s | %s\n",
            what, KN[kind], x, d, nn / d, z, p, nn, c_r, pairdesc, room_desc);
}

/* Certificate test of marks S, T (lattice points of the cert room, shifted coords) over the unit
 * pillowcase of the cert room.  vmask: bit c set when corner class c (relative to S) is in V.
 * half: Lambda contains (1/2) Z^2.  d20: Set A tripwire.  Returns 1 if all 4 lift pairs are
 * certified at every target. */
static int cert_pair(int Sx, int Sy, int Tx, int Ty, int vmask, int half, int d20, const char *pairdesc) {
    int ox = Sx & 1, oy = Sy & 1;
    CUR_SX = Sx - 2; CUR_SY = Sy - 2; CUR_TX = Tx - 2; CUR_TY = Ty - 2;
    cgen(0, 0, ox, oy, gs[0]); cgen(1, 0, ox, oy, gs[1]); cgen(1, 1, ox, oy, gs[2]); cgen(0, 1, ox, oy, gs[3]);
    for (int t = 0; t < 4; t++) for (int i = 0; i < cn; i++) gs[4 + t][gs[t][i]] = i;
    for (int c = 0; c < 4; c++) for (int i = 0; i < cn; i++) { int j = gs[c][i]; qtwo[c][i] = j != i && gs[c][j] == i; }
    int xt = ((Tx - Sx) & 1) && ((Ty - Sy) & 1) ? 2 : ((Tx - Sx) & 1) ? 1 : ((Ty - Sy) & 1) ? 3 : 0;
    int LS[2], LT[2];
    lifts(Sx, Sy, 0, LS); lifts(Tx, Ty, xt, LT);
    static Factor Bx[4], Ry[4];
    int all1[CM], lab[CM], useq[CM];
    for (int i = 0; i < cn; i++) all1[i] = 1;
    for (int x = 1; x <= 3; x++) {
        for (int i = 0; i < cn; i++) useq[i] = qtwo[x][i];
        int d = closure(gs[x], useq, lab); make_factor(&Bx[x], lab, d);
        d = closure(gs[x], all1, lab); make_factor(&Ry[x], lab, d);
    }
    int vonly[4];
    for (int x = 1; x <= 3; x++) { vonly[x] = 1; for (int i = 0; i < cn; i++) if (qtwo[x][i]) vonly[x] = 0; }
    int nn = cn, r = c_r, cut_any = 0;
    for (int x = 1; x <= 3; x++) if (nn <= 3 * r || (nn <= 4 * r + 4 && vonly[x])) cut_any = 1;
    if (xt == 0 && cut_any) enum_small(); else n_small = 0;
    int flagged = 0;
    last_tw = 0;
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++) {
            int s = LS[i], q = LT[j], allt = 1;
            for (int x = 1; x <= 3; x++) {
                if (xt != 0 && x != xt) continue;
                int got = 0;
                /* Par */
                if (xt == 0 && Bx[x].d >= 2 && par_ok(&Bx[x], x, s, q)) {
                    const Factor *F = &Bx[x]; got |= 1; C_kind[0]++;
                    if (F->z >= 1 && nn > 8 * r) { C_tw[3]++; tripwire("LemmaZ-Par", pairdesc, 0, x, F->d, F->z, F->p, nn); }
                    if (F->z >= 1 && !(vmask >> x & 1) && nn > 4 * r) { C_tw[1]++; tripwire("nonV-zero-n>4r", pairdesc, 0, x, F->d, F->z, F->p, nn); }
                    if (F->z == 0 && F->p != 4) { C_tw[4]++; tripwire("zerofree-not-pillowcase", pairdesc, 0, x, F->d, F->z, F->p, nn); }
                }
                /* Rig via R_y */
                for (int y = 1; y <= 3; y++) {
                    if (y == x) continue;
                    const Factor *F = &Ry[y];
                    if (F->d < 2 || !rig_ok(F, x, s, q, xt == 0 ? 0 : x)) continue;
                    got |= 2; C_kind[1]++;
                    if (F->z == 0 && (F->d != 4 || !half)) { C_tw[0]++; tripwire("zerofree-Rig", pairdesc, 1, x, F->d, F->z, F->p, nn); }
                    if (F->z >= 1 && nn > 5 * r) { C_tw[3]++; tripwire("LemmaZ-Rig", pairdesc, 1, x, F->d, F->z, F->p, nn); }
                    if (F->z >= 1 && !(vmask >> x & 1) && nn > 4 * r) { C_tw[1]++; tripwire("nonV-zero-n>4r", pairdesc, 1, x, F->d, F->z, F->p, nn); }
                    if (F->z == 0 && F->p != 4) { C_tw[4]++; tripwire("zerofree-not-pillowcase", pairdesc, 1, x, F->d, F->z, F->p, nn); }
                    if (d20 && !(nn / F->d == 4 && F->d == 5 && F->z == 2)) { C_tw[2]++; tripwire("D20-shape", pairdesc, 1, x, F->d, F->z, F->p, nn); }
                }
                /* Cut (Lemma Z: n <= 3r, or n <= 4r + 4 with x vertex-only) */
                if (xt == 0 && (nn <= 3 * r || (nn <= 4 * r + 4 && vonly[x])))
                    for (int f = 0; f < n_small; f++) {
                        const Factor *F = &small_f[f];
                        if (!cut_ok(F, x, s, q)) continue;
                        got |= 4; C_kind[2]++;
                        if (F->z >= 1 && nn > 3 * r) { C_tw[3]++; tripwire("LemmaZ-Cut", pairdesc, 2, x, F->d, F->z, F->p, nn); }
                        if (F->z >= 1 && !(vmask >> x & 1) && nn > 4 * r) { C_tw[1]++; tripwire("nonV-zero-n>4r", pairdesc, 2, x, F->d, F->z, F->p, nn); }
                    }
                if (DEBUG) fprintf(OUT, "CERTDBG %s | ab %d %d certroom S %d %d T %d %d | lp %d %d x %d bits %d\n", pairdesc, CUR_A, CUR_B, CUR_SX, CUR_SY, CUR_TX, CUR_TY, i, j, x, got);
                if (got) C_tgtcert++; else allt = 0;
            }
            if (allt) { flagged++; C_lpflag++; }
        }
    return flagged == 4;
}

/* load the cert room: original cells scaled by (a, b); returns 0 if too large */
static int load_cert_room(int area0, const int *ox0, const int *oy0, int a, int b) {
    if (area0 * a * b > CM) return 0;
    for (int i = 0; i < cn; i++) cgrid[ccx[i]][ccy[i]] = -1;
    cn = 0;
    for (int c = 0; c < area0; c++)
        for (int u = 0; u < a; u++)
            for (int v = 0; v < b; v++) {
                int x = ox0[c] * a + u + 2, y = oy0[c] * b + v + 2;
                if (x >= CGR - 2 || y >= CGR - 2) return 0;
                ccx[cn] = x; ccy[cn] = y; cgrid[x][y] = cn; cn++;
            }
    c_r = 0;
    for (int i = 0; i < cn; i++)
        for (int dd = 0; dd < 4; dd++) {
            int X = ccx[i] + (dd & 1), Y = ccy[i] + (dd >> 1);
            int k = (ccell(X - 1, Y - 1) >= 0) + (ccell(X, Y - 1) >= 0) + (ccell(X - 1, Y) >= 0) + (ccell(X, Y) >= 0);
            /* count each reflex lattice point once: from its lower-left-most cell */
            if (k == 3) {
                int first = -1;
                int cand[4] = {ccell(X - 1, Y - 1), ccell(X, Y - 1), ccell(X - 1, Y), ccell(X, Y)};
                for (int t = 0; t < 4; t++) if (cand[t] >= 0) { first = cand[t]; break; }
                if (first == i) c_r++;
            }
        }
    return 1;
}

/* ======================= per-room processing ======================= */
static char roombuf[2048];
static void fmt_room(int area0, int W, const int *ox0, const int *oy0) {
    int L = sprintf(roombuf, "%d %d", area0, W);
    for (int c = 0; c < area0; c++) L += sprintf(roombuf + L, " %d %d", ox0[c], oy0[c]);
    room_desc = roombuf;
}
static int positive_found = 0;

/* lattices for Set E at denominator k: subgroups H of (Z/k)^2 as membership masks */
typedef struct { int k, rect, a, b, half; unsigned char in[6][6]; } Lat;
static Lat LAT4[16], LAT6[16]; static int nlat4, nlat6;
static void add_cyclic(Lat *L, int *nl, int k, int gx, int gy, int ord) {
    Lat t; memset(&t, 0, sizeof t); t.k = k;
    for (int i = 0; i < ord; i++) t.in[(gx * i) % k][(gy * i) % k] = 1;
    for (int j = 0; j < *nl; j++) if (!memcmp(L[j].in, t.in, sizeof t.in)) return;
    L[(*nl)++] = t;
}
static void finish_lat(Lat *L) {
    int k = L->k, cntx = 0, cnty = 0, tot = 0;
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) tot += L->in[i][j];
    for (int i = 0; i < k; i++) cntx += L->in[i][0];
    for (int j = 0; j < k; j++) cnty += L->in[0][j];
    L->rect = cntx * cnty == tot;
    L->a = cntx; L->b = cnty;                     /* Lambda = (1/a) Z x (1/b) Z when rect */
    L->half = k % 2 == 0 && L->in[k / 2][0] && L->in[0][k / 2];
}
static void make_lattices(void) {
    nlat4 = nlat6 = 0;
    for (int x = 0; x < 4; x++) for (int y = 0; y < 4; y++) {
        int o = 1; while ((x * o) % 4 || (y * o) % 4) o++;
        if (o == 2 || o == 4) add_cyclic(LAT4, &nlat4, 4, x, y, o);
    }
    Lat h; memset(&h, 0, sizeof h); h.k = 4;
    for (int x = 0; x < 4; x += 2) for (int y = 0; y < 4; y += 2) h.in[x][y] = 1;
    LAT4[nlat4++] = h;
    for (int x = 0; x < 6; x++) for (int y = 0; y < 6; y++) {
        int o = 1; while ((x * o) % 6 || (y * o) % 6) o++;
        if (o == 6) add_cyclic(LAT6, &nlat6, 6, x, y, 6);
    }
    for (int i = 0; i < nlat4; i++) finish_lat(&LAT4[i]);
    for (int i = 0; i < nlat6; i++) finish_lat(&LAT6[i]);
}
static int lat_has(const Lat *L, int X, int Y, int rhoflip) {       /* X, Y scaled coords */
    int k = L->k, x = ((X % k) + k) % k, y = (((rhoflip ? -Y : Y) % k) + k) % k;
    return L->in[x][y];
}
static int lat_admits(const Lat *L, int SX_, int SY_, int TX_, int TY_) {
    return (lat_has(L, SX_, SY_, 0) || lat_has(L, SX_, SY_, 1)) && (lat_has(L, TX_, TY_, 0) || lat_has(L, TX_, TY_, 1));
}

/* certificate fallback for one pair, coordinates in the scale-k room (origin removed).
 * Returns 1 if certified for some admissible Lambda. */
static int cert_fallback(int area0, const int *ox0, const int *oy0, int k, const Lat *lats, int nl,
                         int SXk, int SYk, int TXk, int TYk, const char *pairdesc) {
    C_certpairs++;
    int certified = 0, any_rect = 0, any_na = 0;
    if (k == 1) {                                   /* Lambda = Z^2 */
        if (!load_cert_room(area0, ox0, oy0, 1, 1)) { C_certna++; return 0; }
        any_rect = 1; CUR_A = CUR_B = 1;
        certified = cert_pair(SXk + 2, SYk + 2, TXk + 2, TYk + 2, 15, 0, SETMODE == 'A', pairdesc);
    } else
        for (int li = 0; li < nl; li++) {
            const Lat *L = &lats[li];
            if (!lat_admits(L, SXk, SYk, TXk, TYk)) continue;
            if (!L->rect) { any_na = 1; continue; }
            int a = L->a, b = L->b;                      /* Lambda = (1/a)Z x (1/b)Z; A = diag(a, b) */
            if (!load_cert_room(area0, ox0, oy0, a, b)) { any_na = 1; continue; }
            any_rect = 1; CUR_A = a; CUR_B = b;
            int sx = SXk * a / k + 2, sy = SYk * b / k + 2, tx = TXk * a / k + 2, ty = TYk * b / k + 2;
            /* V = image of A Z^2 mod 2, as corner classes relative to S */
            int vmask = 0;
            for (int e = 0; e < 4; e++) {
                int vx = (a * (e & 1) + 2) & 1, vy = (b * (e >> 1) + 2) & 1;   /* vertices at even shift 2 */
                int dx = (vx - sx) & 1, dy = (vy - sy) & 1;
                int c = dx && dy ? 2 : dx ? 1 : dy ? 3 : 0;
                vmask |= 1 << c;
            }
            if (cert_pair(sx, sy, tx, ty, vmask, L->half, 0, pairdesc)) certified = 1;
        }
    if (any_na && !any_rect) C_certna++;
    if (certified) {
        C_certified++; positive_found = 1;
        fprintf(OUT, "POSITIVE certified pair | %s | room %s\n", pairdesc, room_desc);
    }
    return certified;
}

/* shoot and certify the selected pairs of the scale-k room.  want(a, b) on point indices. */
typedef int (*WantF)(int, int);
static int ip_[MAXI], ni_;
static int Wk, Wsmall;   /* context for want fns */
static const Lat *Wlats; static int Wnl;

static void run_pairs(int area0, int W, const int *ox0, const int *oy0, int k, WantF want,
                      const Lat *lats, int nl, int is_g3, int is_g6, int count_main) {
    if (!build_room(area0, ox0, oy0, k)) { fprintf(stderr, "room too large for scale %d\n", k); exit(2); }
    ni_ = 0;
    for (int i = 0; i < npt; i++) if (ptk[i] == 4) ip_[ni_++] = i;
    if (ni_ > MAXI) { fprintf(stderr, "too many points\n"); exit(2); }
    long long np = 0;
    for (int a = 0; a < ni_; a++)
        for (int b = a + 1; b < ni_; b++) { res[a][b] = want(ip_[a], ip_[b]) ? 2 : 0; if (res[a][b]) np++; }
    if (!np) { clear_room(); return; }
    if (count_main) C_rooms_pairs++;
    shoot_pairs(ni_, ip_);
    char pd[200];
    for (int a = 0; a < ni_; a++)
        for (int b = a + 1; b < ni_; b++) {
            int r = res[a][b];
            if (!r) continue;
            int SXk = ptx[ip_[a]] - 1, SYk = pty[ip_[a]] - 1, TXk = ptx[ip_[b]] - 1, TYk = pty[ip_[b]] - 1;
            if (is_g3) { C_g3pairs++; if (r == 1 || r == 5) C_g3lit++; }
            else if (is_g6) { C_g6pairs++; if (r == 1 || r == 5) C_g6lit++; }
            else { C_pairs++; if (r == 1) C_lit40++; if (r == 5) C_lit120++; }
            int surv = !(r == 1 || r == 5);
            if (r == 3) C_vfail++;
            if (surv) {
                C_surv++;
                fprintf(OUT, "SURVIVOR %s scale %d S %d %d T %d %d | %s\n", r == 3 ? "VERIFYFAIL" : "OPEN",
                        k, SXk, SYk, TXk, TYk, room_desc);
            }
            if (!is_g3 && (surv || sampled(a, b))) {
                sprintf(pd, "scale %d S %d %d T %d %d lit %d", k, SXk, SYk, TXk, TYk, !surv);
                cert_fallback(area0, ox0, oy0, k, lats, nl, SXk, SYk, TXk, TYk, pd);
            }
        }
    clear_room();
}

static int want_A(int i, int j) { return ((ptx[i] - ptx[j]) & 1) || ((pty[i] - pty[j]) & 1); }
static int want_X(int i, int j) { (void)i; (void)j; return 1; }
static int want_E(int i, int j) {
    int X1 = ptx[i] - 1, Y1 = pty[i] - 1, X2 = ptx[j] - 1, Y2 = pty[j] - 1, k = Wk;
    int z1 = X1 % k == 0 && Y1 % k == 0, z2 = X2 % k == 0 && Y2 % k == 0;
    if (z1 && z2) return 0;
    if (Wsmall && k == 4 && X1 % 2 == 0 && Y1 % 2 == 0 && X2 % 2 == 0 && Y2 % 2 == 0) return 0;
    for (int l = 0; l < Wnl; l++) if (lat_admits(&Wlats[l], X1, Y1, X2, Y2)) return 1;
    return 0;
}
static int want_G3(int i, int j) {
    int z1 = (ptx[i] - 1) % 3 == 0 && (pty[i] - 1) % 3 == 0, z2 = (ptx[j] - 1) % 3 == 0 && (pty[j] - 1) % 3 == 0;
    return !(z1 && z2);
}

static void process_room(int area0, int W, const int *ox0, const int *oy0) {
    ROOMID++;
    fmt_room(area0, W, ox0, oy0);
    if (SETMODE == 'A' || SETMODE == 'X') {
        C_rooms++;
        if (W < 24 && area0 < 24) C_room_WA[W][area0]++;
        if (COUNTONLY) return;
        run_pairs(area0, W, ox0, oy0, 1, SETMODE == 'A' ? want_A : want_X, NULL, 0, 0, 0, 1);
        return;
    }
    /* Set E */
    int testy = SETMODE == 'Y';                      /* test mode: Set E pairs, no room filter */
    if (!testy && (W < 12 || W > 20 || area0 > W - 4)) return;
    if (W < 24 && area0 < 24) C_room_WA[W][area0]++;
    if (!build_room(area0, ox0, oy0, 1)) { fprintf(stderr, "room too large\n"); exit(2); }
    int gx = 0, gy = 0, x0 = -1, y0 = -1, Wc = 0;
    for (int i = 0; i < npt; i++)
        if (ptk[i] == 1 || ptk[i] == 3) {
            Wc++;
            if (x0 < 0) { x0 = ptx[i]; y0 = pty[i]; }
            gx = gcd(gx, ptx[i] - x0); gy = gcd(gy, pty[i] - y0);
        }
    if (Wc != W) { fprintf(stderr, "wall count mismatch\n"); exit(2); }
    if (!testy && (gx > 1 || gy > 1)) { C_reduced++; C_red_WA[W][area0]++; clear_room(); return; }
    int c3 = is_class3();
    clear_room();
    if (!c3 && !testy) return;
    if (c3) { C_c3++; if (W < 24 && area0 < 24) C_c3_WA[W][area0]++; }
    C_rooms++;
    if (COUNTONLY) return;
    Wk = 4; Wsmall = area0 <= 14; Wlats = LAT4; Wnl = nlat4;
    run_pairs(area0, W, ox0, oy0, 4, want_E, LAT4, nlat4, 0, 0, 1);
    if (W == 16 && area0 == 8) {
        Wk = 6; Wsmall = 0; Wlats = LAT6; Wnl = nlat6;
        run_pairs(area0, W, ox0, oy0, 6, want_E, LAT6, nlat6, 0, 1, 0);
    }
    if (sampled(0xABCDEF, 3)) {                     /* residue (b) regression: (1/3)-grid */
        C_g3rooms++;
        run_pairs(area0, W, ox0, oy0, 3, want_G3, NULL, 0, 1, 0, 0);
    }
}

/* ======================= enumerator (partA-enum.c) ======================= */
#define MAXN 24
#define SPLIT 11
static int NMAX, AMIN, WLO, WHI, NJ, J;
static int GW, PW;
static unsigned char *seen, *occ, *pm;
static int px[MAXN + 1], py[MAXN + 1];
static long long cnt_split = 0, fixed_nodes = 0;
static inline int cid(int x, int y) { return (y + 1) * GW + (x + NMAX + 1); }
static inline int pid(int x, int y) { return (y + 1) * PW + (x + NMAX + 1); }
typedef struct { int w, h; uint32_t row[MAXN + 1]; } Key;
static void make_key(int k, int t, Key *K) {
    int ax[MAXN + 1], ay[MAXN + 1], mnx = 1 << 20, mny = 1 << 20, mxx = -(1 << 20), mxy = -(1 << 20);
    for (int i = 0; i < k; i++) {
        int x = px[i], y = py[i], a, b;
        switch (t) {
        case 0: a = x; b = y; break;   case 1: a = -x; b = y; break;
        case 2: a = x; b = -y; break;  case 3: a = -x; b = -y; break;
        case 4: a = y; b = x; break;   case 5: a = -y; b = x; break;
        case 6: a = y; b = -x; break;  default: a = -y; b = -x; break;
        }
        ax[i] = a; ay[i] = b;
        if (a < mnx) mnx = a; if (a > mxx) mxx = a; if (b < mny) mny = b; if (b > mxy) mxy = b;
    }
    K->w = mxx - mnx + 1; K->h = mxy - mny + 1;
    memset(K->row, 0, sizeof(uint32_t) * K->h);
    for (int i = 0; i < k; i++) K->row[ay[i] - mny] |= (uint32_t)1 << (ax[i] - mnx);
}
static int key_cmp(const Key *A, const Key *B) {
    if (A->w != B->w) return A->w < B->w ? -1 : 1;
    if (A->h != B->h) return A->h < B->h ? -1 : 1;
    for (int r = 0; r < A->h; r++) if (A->row[r] != B->row[r]) return A->row[r] < B->row[r] ? -1 : 1;
    return 0;
}
static long long A_count;               /* Set A: canonical rooms with area 20, W 20 */
static void process(int k) {
    fixed_nodes++;
    for (int i = 0; i < k; i++) {
        int x = px[i], y = py[i];
        pm[pid(x, y)] |= 8; pm[pid(x + 1, y)] |= 4; pm[pid(x, y + 1)] |= 2; pm[pid(x + 1, y + 1)] |= 1;
    }
    int Vn = 0, W = 0, pinch = 0;
    for (int i = 0; i < k; i++)
        for (int d = 0; d < 4; d++) {
            int p = pid(px[i] + (d & 1), py[i] + (d >> 1)), m = pm[p];
            if (!m) continue;
            pm[p] = 0; Vn++;
            int c = __builtin_popcount(m);
            if (c == 1 || c == 3) W++;
            else if (m == 9 || m == 6) pinch = 1;
        }
    if (pinch || W < WLO || W > WHI) return;
    int adj = 0;
    for (int i = 0; i < k; i++) { if (occ[cid(px[i] + 1, py[i])]) adj++; if (occ[cid(px[i], py[i] + 1)]) adj++; }
    if (Vn - (4 * k - adj) + k != 1) return;
    Key K0, K;
    make_key(k, 0, &K0);
    for (int t = 1; t < 8; t++) { make_key(k, t, &K); if (key_cmp(&K, &K0) < 0) return; }
    int ox0[MAXN + 1], oy0[MAXN + 1], c = 0;
    for (int r = 0; r < K0.h; r++) for (int col = 0; col < K0.w; col++) if (K0.row[r] >> col & 1) { ox0[c] = col; oy0[c] = r; c++; }
    if (SETMODE == 'A') A_count++;
    process_room(k, W, ox0, oy0);
    if (positive_found || last_tw) { fflush(OUT); }
}
static int allowed(int x, int y) {
    if (y < 0 || y >= NMAX) return 0;
    if (y == 0 && x < 0) return 0;
    if (x <= -NMAX || x >= NMAX) return 0;
    return 1;
}
static void rec(int nn, const int *untried, int nu) {
    int buf[4 * MAXN + 8], U[4 * MAXN + 8];
    memcpy(U, untried, sizeof(int) * nu);
    while (nu > 0) {
        int c = U[--nu];
        int x = c % GW - NMAX - 1, y = c / GW - 1, s = nn + 1;
        if (s == SPLIT) { long long me = cnt_split++; if (me % NJ != J) continue; }
        px[nn] = x; py[nn] = y; occ[c] = 1;
        if ((s >= SPLIT || J == 0) && s >= AMIN) process(s);
        if (s < NMAX) {
            int m = nu, added = 0, addl[4];
            memcpy(buf, U, sizeof(int) * nu);
            int nb[4][2] = {{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}};
            for (int d = 0; d < 4; d++) {
                int a = nb[d][0], b = nb[d][1];
                if (!allowed(a, b)) continue;
                int q = cid(a, b);
                if (seen[q]) continue;
                seen[q] = 1; buf[m++] = q; addl[added++] = q;
            }
            rec(s, buf, m);
            for (int d = 0; d < added; d++) seen[addl[d]] = 0;
        }
        occ[c] = 0;
    }
}

/* ======================= main ======================= */
static double cpu_s(void) {
    struct rusage ru; getrusage(RUSAGE_SELF, &ru);
    return ru.ru_utime.tv_sec + ru.ru_stime.tv_sec + 1e-6 * (ru.ru_utime.tv_usec + ru.ru_stime.tv_usec);
}
static void summary(const char *tag) {
    fprintf(OUT, "# rooms_WA");
    for (int w = 0; w < 24; w++) for (int a = 0; a < 24; a++)
        if (C_room_WA[w][a]) fprintf(OUT, " W%d_A%d:%lld/%lld/%lld", w, a, C_room_WA[w][a], C_red_WA[w][a], C_c3_WA[w][a]);
    fprintf(OUT, "\n# cert_instances par %lld rig %lld cut %lld lift_pairs_flagged %lld targets_certified %lld"
            " tw_zerofreeRig %lld tw_nonV %lld tw_D20shape %lld tw_lemmaZ %lld tw_notpillow %lld corrupt_rejected %lld\n",
            C_kind[0], C_kind[1], C_kind[2], C_lpflag, C_tgtcert, C_tw[0], C_tw[1], C_tw[2], C_tw[3], C_tw[4], C_corrupt_rej);
    fprintf(OUT, "SUMMARY %s set %c job %lld enum_count %lld fixed_nodes %lld rooms %lld rooms_with_pairs %lld reduced %lld c3 %lld"
            " pairs %lld lit40 %lld lit120 %lld survivors %lld verifyfail %lld cert_tested %lld certified %lld"
            " tripwires %lld cert_na %lld g3_rooms %lld g3_pairs %lld g3_lit %lld g6_pairs %lld g6_lit %lld cpu %.2f\n",
            tag, SETMODE, JOBID, A_count, fixed_nodes, C_rooms, C_rooms_pairs, C_reduced, C_c3, C_pairs, C_lit40, C_lit120,
            C_surv, C_vfail, C_certpairs, C_certified, C_trip, C_certna, C_g3rooms, C_g3pairs, C_g3lit, C_g6pairs, C_g6lit, cpu_s());
}

int main(int argc, char **argv) {
    OUT = stdout;
    if (argc < 3) { fprintf(stderr, "see header for usage\n"); return 1; }
    CORRUPT = getenv("CHECK_CORRUPT") && atoi(getenv("CHECK_CORRUPT"));
    DEBUG = getenv("CHECK_DEBUG") && atoi(getenv("CHECK_DEBUG"));
    memset(cellid, -1, sizeof cellid); memset(cgrid, -1, sizeof cgrid);
    make_dirs(120); make_cyl_dirs(15); make_lattices();
    if (!strcmp(argv[1], "A") || !strcmp(argv[1], "E")) {
        if (argc < 5) return 1;
        SETMODE = argv[1][0]; NJ = atoi(argv[2]); J = atoi(argv[3]); CERTRATE = atoll(argv[4]); JOBID = J;
        if (SETMODE == 'A') { NMAX = 20; AMIN = 20; WLO = 20; WHI = 20; }
        else { NMAX = 16; AMIN = 1; WLO = 12; WHI = 20; }
        /* validation only: count rooms (and classes) without pairs, with other ranges */
        COUNTONLY = getenv("CHECK_COUNTONLY") && atoi(getenv("CHECK_COUNTONLY"));
        if (getenv("CHECK_NMAX")) NMAX = atoi(getenv("CHECK_NMAX"));
        if (getenv("CHECK_AMIN")) AMIN = atoi(getenv("CHECK_AMIN"));
        if (getenv("CHECK_WLO")) WLO = atoi(getenv("CHECK_WLO"));
        if (getenv("CHECK_WHI")) WHI = atoi(getenv("CHECK_WHI"));
        if (NMAX < SPLIT || NMAX > 20) { fprintf(stderr, "NMAX out of range\n"); return 1; }
        GW = 2 * NMAX + 4; PW = 2 * NMAX + 6;
        seen = calloc((size_t)GW * (NMAX + 4), 1); occ = calloc((size_t)GW * (NMAX + 4), 1);
        pm = calloc((size_t)PW * (NMAX + 6), 1);
        if (getenv("CHECK_TESTROOM")) {          /* test configuration: one extra room, all pairs, mode X */
            char *pp = getenv("CHECK_TESTROOM");
            int area0 = (int)strtol(pp, &pp, 10), W = (int)strtol(pp, &pp, 10), ox0[64], oy0[64], keep = SETMODE;
            for (int c = 0; c < area0; c++) { ox0[c] = (int)strtol(pp, &pp, 10); oy0[c] = (int)strtol(pp, &pp, 10); }
            SETMODE = 'X'; process_room(area0, W, ox0, oy0); SETMODE = keep;
        }
        int start = cid(0, 0); seen[start] = 1;
        int U[1] = {start};
        rec(0, U, 1);
    } else if (!strcmp(argv[1], "stdin")) {
        SETMODE = argv[2][0]; CERTRATE = argc > 3 ? atoll(argv[3]) : 10000;
        static char line[16384];
        while (fgets(line, sizeof line, stdin)) {
            if (line[0] == '#' || line[0] == '\n') continue;
            char *pp = line;
            int area0 = (int)strtol(pp, &pp, 10), W = (int)strtol(pp, &pp, 10), ox0[64], oy0[64];
            for (int c = 0; c < area0; c++) { ox0[c] = (int)strtol(pp, &pp, 10); oy0[c] = (int)strtol(pp, &pp, 10); }
            if (SETMODE == 'A') A_count++;
            process_room(area0, W, ox0, oy0);
        }
    } else return 1;
    summary(positive_found ? "POSITIVE" : C_trip ? "TRIPWIRE" : "OK");
    fflush(OUT);
    return positive_found ? 10 : C_trip ? 11 : 0;
}
