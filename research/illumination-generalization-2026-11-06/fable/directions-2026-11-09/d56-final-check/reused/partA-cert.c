/* partA-cert.c -- part A of the census: all lattice pairs and one-cylinder
 * certificates, for every room on stdin.
 *
 * Input: room lines "area W x0 y0 x1 y1 ..." (from partA-enum ... all).
 * A room scaled by k (each cell a k x k block) has the (1/k)-grid of the
 * original room as its lattice; billiard paths and corners are unchanged.
 *
 * Task 1: every unordered pair of distinct interior lattice points, all
 *   classes.  LIT certificates by exact shooting in the 4-fold unfolding
 *   (same method as shoot.c, primitive directions with p+q <= BOUND), each
 *   re-checked by verify_plane().  Pairs without a verified certificate go
 *   to the survivor file.
 *
 * Task 2: one-cylinder directions.
 *   - Normalisation: gx = gcd of corner x-differences, gy likewise.  A room
 *     with gx > 1 or gy > 1 is the image of a smaller room under
 *     diag(gx, gy); it is counted as "reduced" and skipped.
 *   - For coprime p, q in [1, CYLB], ordered by p + q, the cylinders of M
 *     (marked set = corner lifts) are counted exactly: slots (square, j),
 *     j = 0..q-1, are the open strips between consecutive integer leaves
 *     (q x - p y in Z) on the bottom edge of a square, and also the integer
 *     leaf points at offset j/q.  Both move by the same permutation
 *     nxt(i, j) = (u(r^k(i)), (j+p) mod q), k = floor((j+p)/q).  A point
 *     cycle is a regular closed leaf iff it has no slot (s, 0) whose
 *     bottom-left corner is a corner of the room.  Strips are merged across
 *     regular leaves (union-find).  One-cylinder on DP <=> 2 components on M.
 *   - Lambda = Z-span of (q, p), (q, -p) over the certified directions,
 *     kept in Hermite normal form [[a, b], [0, c]].  X = dual of Lambda, so
 *     |X / Z^2| = a * c.  The search stops as soon as a * c = 1 (X = Z^2).
 *   - CYLB may be "B1:B2": directions with max(p, q) in (B1, B2] are tried
 *     only while the room is in class (ii) with |X / Z^2| > 2.
 *   - c3_parity counts class (iii) rooms in which every tested direction has
 *     a number of strips divisible by 4 (an even number of strips on DP).
 *   - Classes: (i) X = Z^2; (ii) a * c > 1 after all directions; (iii) no
 *     one-cylinder direction found.
 *   - Class (ii): the room is scaled by the exponent e of X / Z^2, and every
 *     pair of interior points of X with at least one point outside Z^2 is
 *     shot as in Task 1.  If the scaled room does not fit, the room is
 *     written to the rooms file as C2BIG.
 *   - Class (iii), area <= GRIDMAX: every pair of interior points of the
 *     (1/2)-grid and of the (1/3)-grid with at least one point outside Z^2 is
 *     shot.  Class (iii) rooms of area <= 12 are written to the rooms file.
 * Survivors: one line per pair without a verified certificate, tagged T1S /
 * T1D (Task 1 same / different class), C2, or G (grid), with the room.
 *
 * usage: partA-cert BOUND CYLB GRIDMAX infile outfile survivorfile roomsfile
 *   Rescue mode: input lines that are survivor lines ("TAG scale k S x y T x y |
 *   area W cells") are re-shot in the room scaled by k with the given BOUND
 *   (<= 200); the output gets "LIT ..." or "UNRESOLVED ..." per line.
 *   CYLB < 0: list mode, |CYLB| is the bound; every direction is tested and
 *   "DIR p q components strips" lines go to the rooms file.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int verify_plane(int ncell, const int *cx, const int *cy,
                 int sx0, int sy0, int dx, int dy, int m, int tx, int ty);

#define MAXC 400
#define G 104
#define MAXI (2 * MAXC)

static int n, cx[MAXC], cy[MAXC];
static int cellid[G][G];
static int nsq;
static int H[4 * MAXC], V[4 * MAXC], HI[4 * MAXC], LAB[4 * MAXC], BLK[4 * MAXC];
static const int SX[4] = {1, -1, 1, -1}, SY[4] = {1, 1, -1, -1};

static int has(int x, int y) { return x >= 0 && y >= 0 && x < G && y < G && cellid[x][y] >= 0; }
static int cnt_around(int x, int y) { return has(x - 1, y - 1) + has(x, y - 1) + has(x - 1, y) + has(x, y); }
static long long gcdll(long long a, long long b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { long long t = a % b; a = b; b = t; } return a; }
static int gcd(int a, int b) { return (int)gcdll(a, b); }

/* shooting directions */
static int ndir, DP_[12000], DQ_[12000];
static unsigned char WORD[12000][200];
static int WLEN[12000];

static void make_dirs(int bound) {
    ndir = 0;
    for (int s = 1; s <= bound; s++)
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
                    if (uv < uh) { WORD[ndir][L++] = 0; a++; }
                    else         { WORD[ndir][L++] = 1; b++; }
                }
            }
            WLEN[ndir] = L;
            ndir++;
        }
}

/* cylinder directions: first all coprime p, q in [1, B1] by p + q, then the
 * ones with max(p, q) in (B1, B2] by p + q */
static int ncd, ncd1, CP[4000], CQ[4000];
static void make_cyl_dirs(int B1, int B2) {
    ncd = 0;
    for (int pass = 0; pass < 2; pass++) {
        int lo = pass ? B1 + 1 : 1, hi = pass ? B2 : B1;
        for (int s = 2; s <= 2 * hi; s++)
            for (int p = 1; p <= hi; p++) {
                int q = s - p, mx = p > q ? p : q;
                if (q < 1 || mx < lo || mx > hi || gcd(p, q) != 1) continue;
                if (ncd >= 4000) { fprintf(stderr, "too many cylinder directions\n"); exit(1); }
                CP[ncd] = p; CQ[ncd] = q; ncd++;
            }
        if (!pass) ncd1 = ncd;
    }
}

static int sq(int c, int sh) { return 4 * c + sh; }

static void build_origami(void) {
    nsq = 4 * n;
    for (int c = 0; c < n; c++)
        for (int sh = 0; sh < 4; sh++) {
            int s = sq(c, sh), i = cx[c], j = cy[c], sx = SX[sh], sy = SY[sh];
            int fx = sh ^ 1, fy = sh ^ 2;
            H[s] = has(i + sx, j) ? sq(cellid[i + sx][j], sh) : sq(c, fx);
            V[s] = has(i, j + sy) ? sq(cellid[i][j + sy], sh) : sq(c, fy);
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

/* ---- exact cylinder count of M in direction (p,q), p,q >= 1 ---- */
static int cyc[4 * MAXC * 64], uf[4 * MAXC * 64], regl[4 * MAXC * 64];
static int ufind(int a) { while (uf[a] != a) { uf[a] = uf[uf[a]]; a = uf[a]; } return a; }

static int cyl_count(int p, int q, int *nstrips) {
    if (q > 64) { fprintf(stderr, "q too large for slot arrays\n"); exit(1); }
    int ns = nsq * q;
    for (int t = 0; t < ns; t++) cyc[t] = -1;
    int nc = 0;
    for (int t = 0; t < ns; t++) {
        if (cyc[t] >= 0) continue;
        int cur = t;
        while (cyc[cur] < 0) {
            cyc[cur] = nc;
            int i = cur / q, j = cur % q, k = (j + p) / q;
            for (int z = 0; z < k; z++) i = H[i];
            cur = V[i] * q + (j + p) % q;
        }
        if (cur != t) { fprintf(stderr, "nxt is not a permutation\n"); exit(5); }
        nc++;
    }
    *nstrips = nc;
    if (nc == 2) return 2;
    for (int c = 0; c < nc; c++) { regl[c] = 1; uf[c] = c; }
    for (int s = 0; s < nsq; s++) if (BLK[s]) regl[cyc[s * q]] = 0;
    for (int s = 0; s < nsq; s++) {
        for (int j = 1; j < q; j++)
            if (regl[cyc[s * q + j]]) { int a = ufind(cyc[s * q + j - 1]), b = ufind(cyc[s * q + j]); if (a != b) uf[a] = b; }
        if (regl[cyc[s * q]]) { int a = ufind(cyc[s * q]), b = ufind(cyc[HI[s] * q + q - 1]); if (a != b) uf[a] = b; }
    }
    int comps = 0;
    for (int c = 0; c < nc; c++) if (ufind(c) == c) comps++;
    return comps;
}

/* HNF of Lambda: rows (ha, hb), (0, hc); ha = 0 means empty */
static long long ha, hb, hc;
static void hnf_add(long long x, long long y) {
    if (x != 0) {
        /* extended gcd of ha, x */
        long long a0 = ha, b0 = x, u0 = 1, v0 = 0, u1 = 0, v1 = 1;
        while (b0) { long long t = a0 / b0, r = a0 - t * b0; a0 = b0; b0 = r;
                     long long tu = u0 - t * u1; u0 = u1; u1 = tu; long long tv = v0 - t * v1; v0 = v1; v1 = tv; }
        if (a0 < 0) { a0 = -a0; u0 = -u0; v0 = -v0; }
        long long g = a0;
        long long nb = u0 * hb + v0 * y;
        long long rest = (x / g) * hb - (ha / g) * y;
        ha = g; hb = nb;
        hc = gcdll(hc, rest);
    } else {
        hc = gcdll(hc, y);
    }
    if (hc) { hb %= hc; if (hb < 0) hb += hc; }
}

/* ---- room construction ---- */
static int npt, ptx[4 * MAXC], pty[4 * MAXC], ptk[4 * MAXC];
static int mark[G][G], markid = 0;

/* builds the room scaled by `scale`; returns 0 if it does not fit */
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
    markid++;
    npt = 0;
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

/* ---- shooting all pairs among selected interior points ----
 * ip[0..ni-1]: point indices; skip[a] && skip[b]: pair not wanted.
 * res[a][b] (a < b): 0 not wanted, 1 lit and verified, 2 unresolved, 3 verify failure */
static int res[MAXI][MAXI];
static void shoot_pairs(int ni, const int *ip, const int *skip) {
    static int res_sh[MAXI][MAXI], res_d[MAXI][MAXI], res_m[MAXI][MAXI], res_src[MAXI][MAXI];
    static int labidx[G * G];
    for (int a = 0; a < ni; a++) for (int b = 0; b < ni; b++) res[a][b] = (a < b && !(skip[a] && skip[b])) ? 2 : 0;
    for (int i = 0; i < npt; i++) labidx[ptx[i] * G + pty[i]] = -1;
    for (int a = 0; a < ni; a++) labidx[ptx[ip[a]] * G + pty[ip[a]]] = a;
    for (int a = 0; a < ni; a++) {
        int need = 0;
        for (int b = a + 1; b < ni; b++) if (res[a][b] == 2) need++;
        if (!need) continue;
        int SXp = ptx[ip[a]], SYp = pty[ip[a]];
        for (int d = 0; d < ndir && need; d++)
            for (int sh = 0; sh < 4 && need; sh++) {
                int c0 = cellid[SXp - (SX[sh] < 0)][SYp - (SY[sh] < 0)];
                int s0 = sq(c0, sh), s = s0;
                for (int m = 1; m <= nsq + 1; m++) {
                    s = step(s, d);
                    if (BLK[s]) break;
                    int b = labidx[LAB[s]];
                    if (b >= 0 && b != a) {
                        int lo = a < b ? a : b, hi = a < b ? b : a;
                        if (res[lo][hi] == 2) {
                            res[lo][hi] = 4;   /* found, not yet verified */
                            res_sh[lo][hi] = sh; res_d[lo][hi] = d; res_m[lo][hi] = m; res_src[lo][hi] = a;
                            if (b > a) need--;
                        }
                    }
                    if (s == s0) break;
                }
            }
    }
    for (int a = 0; a < ni; a++)
        for (int b = a + 1; b < ni; b++) {
            if (res[a][b] != 4) continue;
            int src = res_src[a][b], sh = res_sh[a][b], d = res_d[a][b], m = res_m[a][b];
            int tgt = (src == a) ? b : a;
            int ok = verify_plane(n, cx, cy, ptx[ip[src]], pty[ip[src]], SX[sh] * DP_[d], SY[sh] * DQ_[d], m,
                                  ptx[ip[tgt]], pty[ip[tgt]]);
            res[a][b] = ok ? 1 : 3;
        }
}

/* bitmask of the 8 lattice symmetries that map the room to itself
 * bit t: 0 id, 1 x->-x, 2 y->-y, 3 rot180, 4 diag x<->y, 5 rot90, 6 rot270, 7 antidiag */
static int sym_mask(int area0, const int *ox0, const int *oy0) {
    static int occ[64][64];
    int mx = 0, my = 0;
    for (int c = 0; c < area0; c++) { if (ox0[c] > mx) mx = ox0[c]; if (oy0[c] > my) my = oy0[c]; }
    for (int c = 0; c < area0; c++) occ[ox0[c]][oy0[c]] = 1;
    int mask = 0;
    for (int t = 0; t < 8; t++) {
        int ok = 1;
        for (int c = 0; c < area0 && ok; c++) {
            int x = ox0[c], y = oy0[c], a, b;
            switch (t) {
            case 0: a = x; b = y; break;
            case 1: a = mx - x; b = y; break;
            case 2: a = x; b = my - y; break;
            case 3: a = mx - x; b = my - y; break;
            case 4: a = y; b = x; break;
            case 5: a = my - y; b = x; break;
            case 6: a = y; b = mx - x; break;
            default: a = my - y; b = mx - x; break;
            }
            if (a < 0 || b < 0 || a >= 64 || b >= 64 || !occ[a][b]) ok = 0;
        }
        if (t >= 4 && mx != my) ok = 0;
        if (ok) mask |= 1 << t;
    }
    for (int c = 0; c < area0; c++) occ[ox0[c]][oy0[c]] = 0;
    return mask;
}

/* ---- counters, indexed by original area and W ---- */
#define NA 41
#define NW 64
static long long st_rooms[NA][NW], st_rooms_pairs[NA][NW];
static long long st_same[NA][NW], st_same_lit[NA][NW], st_diff[NA][NW], st_diff_lit[NA][NW];
static long long st_verify_fail = 0, st_unres_total = 0;
static long long st_reduced[NA][NW], st_c1[NA][NW], st_c2[NA][NW], st_c3[NA][NW], st_c3_parity[NA][NW];
static long long st_c2_done[NA][NW], st_c2_big[NA][NW], st_c2_pairs[NA][NW], st_c2_lit[NA][NW], st_c2_withpts[NA][NW];
static long long st_g_rooms[4][NA][NW], st_g_pairs[4][NA][NW], st_g_lit[4][NA][NW];
static long long st_needmax[NA][64];
static long long st_ndirs_hist[64];
static long long st_index[3][1000];          /* |X / Z^2| histogram for C1 (=1), C2 */
static long long st_sym[4][256];              /* [class 1..3][symmetry mask] */
static long long st_twostrip = 0, st_unionfind = 0;

static void write_room(FILE *f, const char *tag, int area0, int W, const int *ox0, const int *oy0) {
    fprintf(f, "%s %d %d", tag, area0, W);
    for (int c = 0; c < area0; c++) fprintf(f, " %d %d", ox0[c], oy0[c]);
    fputc('\n', f);
}

static void write_pair(FILE *sv, const char *tag, int scale, int a, int b, int area0, int W, const int *ox0, const int *oy0) {
    fprintf(sv, "%s scale %d S %d %d T %d %d |", tag, scale, ptx[a] - 1, pty[a] - 1, ptx[b] - 1, pty[b] - 1);
    write_room(sv, "", area0, W, ox0, oy0);
}

int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage: partA-cert BOUND CYLB GRIDMAX infile outfile survivorfile roomsfile\n"); return 1; }
    int bound = atoi(argv[1]);
    int cylb = atoi(argv[2]), listmode = cylb < 0, cylb2;
    if (listmode) cylb = -cylb;
    char *colon = strchr(argv[2], ':');
    cylb2 = colon ? atoi(colon + 1) : cylb;
    int gridmax = atoi(argv[3]);
    make_dirs(bound);
    make_cyl_dirs(cylb, cylb2);
    FILE *in = strcmp(argv[4], "-") ? fopen(argv[4], "r") : stdin;
    FILE *out = fopen(argv[5], "w");
    FILE *sv = fopen(argv[6], "w");
    FILE *rf = fopen(argv[7], "w");
    if (!in || !out || !sv || !rf) { fprintf(stderr, "open failed\n"); return 1; }
    static char line[16384];
    long long rid = 0;
    memset(cellid, -1, sizeof cellid);
    while (fgets(line, sizeof line, in)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        char *pp = line;
        if (line[0] >= 'A' && line[0] <= 'Z') {          /* rescue mode */
            char tag[64]; int k, sx, sy, tx, ty, nr;
            if (sscanf(line, "%63s scale %d S %d %d T %d %d |%n", tag, &k, &sx, &sy, &tx, &ty, &nr) != 6) { fprintf(stderr, "bad survivor line\n"); return 1; }
            pp = line + nr;
            int area0 = (int)strtol(pp, &pp, 10), ox0[64], oy0[64];
            strtol(pp, &pp, 10);   /* W */
            for (int c = 0; c < area0; c++) { ox0[c] = (int)strtol(pp, &pp, 10); oy0[c] = (int)strtol(pp, &pp, 10); }
            if (!build_room(area0, ox0, oy0, k)) { fprintf(stderr, "rescue room too large\n"); return 2; }
            int ip2[2] = {-1, -1}, sk[2] = {0, 0};
            for (int i = 0; i < npt; i++) {
                if (ptx[i] == sx + 1 && pty[i] == sy + 1) ip2[0] = i;
                if (ptx[i] == tx + 1 && pty[i] == ty + 1) ip2[1] = i;
            }
            if (ip2[0] < 0 || ip2[1] < 0 || ptk[ip2[0]] != 4 || ptk[ip2[1]] != 4) { fprintf(stderr, "bad points\n"); return 2; }
            shoot_pairs(2, ip2, sk);
            fprintf(out, "%s %s", res[0][1] == 1 ? "LIT" : (res[0][1] == 3 ? "VERIFYFAIL" : "UNRESOLVED"), line);
            if (res[0][1] != 1) fputs(line, sv);
            clear_room();
            continue;
        }
        int area0 = (int)strtol(pp, &pp, 10), W = (int)strtol(pp, &pp, 10);
        int ox0[64], oy0[64];
        for (int c = 0; c < area0; c++) { ox0[c] = (int)strtol(pp, &pp, 10); oy0[c] = (int)strtol(pp, &pp, 10); }
        rid++;
        if (!build_room(area0, ox0, oy0, 1)) { fprintf(stderr, "room too large\n"); return 2; }
        int Wc = 0;
        for (int i = 0; i < npt; i++) if (ptk[i] == 1 || ptk[i] == 3) Wc++;
        if (Wc != W) { fprintf(stderr, "wall count mismatch room %lld\n", rid); return 2; }
        st_rooms[area0][W]++;

        /* ---------------- Task 1: all pairs of interior lattice points ---------------- */
        int ip[MAXI], skip[MAXI], ni = 0;
        for (int i = 0; i < npt; i++) if (ptk[i] == 4) { ip[ni] = i; skip[ni] = 0; ni++; }
        if (ni >= 2) {
            st_rooms_pairs[area0][W]++;
            shoot_pairs(ni, ip, skip);
            for (int a = 0; a < ni; a++)
                for (int b = a + 1; b < ni; b++) {
                    int same = ((ptx[ip[a]] - ptx[ip[b]]) & 1) == 0 && ((pty[ip[a]] - pty[ip[b]]) & 1) == 0;
                    if (same) st_same[area0][W]++; else st_diff[area0][W]++;
                    if (res[a][b] == 1) { if (same) st_same_lit[area0][W]++; else st_diff_lit[area0][W]++; }
                    else {
                        if (res[a][b] == 3) st_verify_fail++;
                        st_unres_total++;
                        write_pair(sv, res[a][b] == 3 ? (same ? "T1S-VERIFYFAIL" : "T1D-VERIFYFAIL") : (same ? "T1S" : "T1D"),
                                   1, ip[a], ip[b], area0, W, ox0, oy0);
                    }
                }
        }

        /* ---------------- Task 2: one-cylinder certificates ---------------- */
        int gx = 0, gy = 0, x0 = -1, y0 = -1;
        for (int i = 0; i < npt; i++)
            if (ptk[i] == 1 || ptk[i] == 3) {
                if (x0 < 0) { x0 = ptx[i]; y0 = pty[i]; }
                gx = gcd(gx, ptx[i] - x0); gy = gcd(gy, pty[i] - y0);
            }
        if (gx > 1 || gy > 1) { st_reduced[area0][W]++; clear_room(); continue; }
        ha = hb = hc = 0;
        int found = 0, lastmax = 0, oddstrips = 0;
        if (listmode) fprintf(rf, "ROOM %lld\n", rid);
        for (int d = 0; d < ncd && (listmode || ha * hc != 1); d++) {
            /* directions beyond B1 only for class (ii) rooms with |X / Z^2| > 2 */
            if (d >= ncd1 && !listmode && !(found && ha * hc > 2)) break;
            int p = CP[d], q = CQ[d], nstr;
            int comps = cyl_count(p, q, &nstr);
            if (nstr % 4 == 2) oddstrips = 1;
            if (listmode) fprintf(rf, "DIR %d %d %d %d\n", p, q, comps, nstr);
            if (comps != 2) continue;
            if (nstr == 2) st_twostrip++; else st_unionfind++;
            found++;
            hnf_add(q, p); hnf_add(q, -p);
            lastmax = p > q ? p : q;
        }
        clear_room();
        int cls = !found ? 3 : (ha * hc == 1 ? 1 : 2);
        st_sym[cls][sym_mask(area0, ox0, oy0)]++;
        if (cls == 1) {
            st_c1[area0][W]++;
            st_needmax[area0][lastmax]++;
            st_ndirs_hist[found < 63 ? found : 63]++;
            st_index[1][1]++;
        } else if (cls == 2) {
            st_c2[area0][W]++;
            long long idx = ha * hc;
            st_index[2][idx < 999 ? idx : 999]++;
            /* exponent e of X / Z^2: e/a, e/c, e*b/(a*c) integers */
            long long e = 1;
            while (!(e % ha == 0 && e % hc == 0 && (e * hb) % (ha * hc) == 0)) e++;
            if (!build_room(area0, ox0, oy0, (int)e)) {
                st_c2_big[area0][W]++;
                char tag[64]; sprintf(tag, "C2BIG %lld %lld %lld", ha, hb, hc);
                write_room(rf, tag, area0, W, ox0, oy0);
            } else {
                int nx = 0;
                for (int i = 0; i < npt; i++) {
                    if (ptk[i] != 4) continue;
                    long long X = ptx[i] - 1, Y = pty[i] - 1;
                    if ((ha * X + hb * Y) % e != 0 || (hc * Y) % e != 0) continue;   /* not in X */
                    ip[nx] = i; skip[nx] = (X % e == 0 && Y % e == 0); nx++;
                }
                int extra = 0;
                for (int a = 0; a < nx; a++) if (!skip[a]) extra = 1;
                if (extra) st_c2_withpts[area0][W]++;
                shoot_pairs(nx, ip, skip);
                int allok = 1;
                for (int a = 0; a < nx; a++)
                    for (int b = a + 1; b < nx; b++) {
                        if (!res[a][b]) continue;
                        st_c2_pairs[area0][W]++;
                        if (res[a][b] == 1) st_c2_lit[area0][W]++;
                        else {
                            allok = 0; st_unres_total++; if (res[a][b] == 3) st_verify_fail++;
                            write_pair(sv, res[a][b] == 3 ? "C2-VERIFYFAIL" : "C2", (int)e, ip[a], ip[b], area0, W, ox0, oy0);
                        }
                    }
                if (allok) st_c2_done[area0][W]++;
                clear_room();
            }
        } else {
            st_c3[area0][W]++;
            if (!oddstrips) st_c3_parity[area0][W]++;
            if (area0 <= 12) write_room(rf, "C3", area0, W, ox0, oy0);
            if (area0 <= gridmax)
                for (int k = 2; k <= 3; k++) {
                    if (!build_room(area0, ox0, oy0, k)) { fprintf(stderr, "grid room too large\n"); return 2; }
                    int nx = 0;
                    for (int i = 0; i < npt; i++)
                        if (ptk[i] == 4) { ip[nx] = i; skip[nx] = ((ptx[i] - 1) % k == 0 && (pty[i] - 1) % k == 0); nx++; }
                    shoot_pairs(nx, ip, skip);
                    st_g_rooms[k][area0][W]++;
                    for (int a = 0; a < nx; a++)
                        for (int b = a + 1; b < nx; b++) {
                            if (!res[a][b]) continue;
                            st_g_pairs[k][area0][W]++;
                            if (res[a][b] == 1) st_g_lit[k][area0][W]++;
                            else {
                                st_unres_total++; if (res[a][b] == 3) st_verify_fail++;
                                write_pair(sv, res[a][b] == 3 ? "G-VERIFYFAIL" : "G", k, ip[a], ip[b], area0, W, ox0, oy0);
                            }
                        }
                    clear_room();
                }
        }
    }
    fprintf(out, "# STATS bound %d dirs %d cylb %d cylb2 %d cyldirs %d %d gridmax %d rooms %lld\n", bound, ndir, cylb, cylb2, ncd1, ncd, gridmax, rid);
    for (int a = 0; a < NA; a++)
        for (int w = 0; w < NW; w++)
            if (st_rooms[a][w])
                fprintf(out, "# T area %d W %d rooms %lld rooms_with_pairs %lld same %lld same_lit %lld diff %lld diff_lit %lld"
                        " reduced %lld c1 %lld c2 %lld c3 %lld c3_parity %lld c2_done %lld c2_big %lld c2_withpts %lld c2_pairs %lld c2_lit %lld"
                        " g2_rooms %lld g2_pairs %lld g2_lit %lld g3_rooms %lld g3_pairs %lld g3_lit %lld\n",
                        a, w, st_rooms[a][w], st_rooms_pairs[a][w], st_same[a][w], st_same_lit[a][w],
                        st_diff[a][w], st_diff_lit[a][w], st_reduced[a][w], st_c1[a][w], st_c2[a][w], st_c3[a][w], st_c3_parity[a][w],
                        st_c2_done[a][w], st_c2_big[a][w], st_c2_withpts[a][w], st_c2_pairs[a][w], st_c2_lit[a][w],
                        st_g_rooms[2][a][w], st_g_pairs[2][a][w], st_g_lit[2][a][w],
                        st_g_rooms[3][a][w], st_g_pairs[3][a][w], st_g_lit[3][a][w]);
    for (int a = 0; a < NA; a++)
        for (int m = 0; m < 64; m++)
            if (st_needmax[a][m]) fprintf(out, "# needmax area %d maxpq %d rooms %lld\n", a, m, st_needmax[a][m]);
    for (int k = 0; k < 64; k++) if (st_ndirs_hist[k]) fprintf(out, "# ndirs %d rooms %lld\n", k, st_ndirs_hist[k]);
    for (int i = 0; i < 1000; i++) if (st_index[2][i]) fprintf(out, "# c2_index %d rooms %lld\n", i, st_index[2][i]);
    for (int c = 1; c <= 3; c++)
        for (int m = 0; m < 256; m++)
            if (st_sym[c][m]) fprintf(out, "# sym class %d mask %d rooms %lld\n", c, m, st_sym[c][m]);
    fprintf(out, "# certified_dirs two_strip %lld union_find %lld\n", st_twostrip, st_unionfind);
    fprintf(out, "# unresolved_total %lld\n# verify_fail %lld\n# DONE\n", st_unres_total, st_verify_fail);
    fclose(out); fclose(sv); fclose(rf);
    return 0;
}
