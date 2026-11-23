/* shoot.c -- cheap exact filter + N_min for every eligible room.
 *
 * Input: room lines "area W x0 y0 x1 y1 ..." (from enum_rooms).
 * For each room and each parity class with >= 2 interior lattice points:
 *   - pairs: all unordered pairs of distinct interior points of that class;
 *   - LIT certificates by exact shooting in the 4-fold unfolding (an
 *     origami: square = (cell, sheet), h = right, v = up, label = room point
 *     at the bottom-left corner).  From each copy of S, every primitive
 *     direction (p,q), p,q >= 0, p+q <= BOUND, is followed lattice step by
 *     lattice step until it returns to its start or meets a corner label.
 *     Each certificate is re-checked by verify_plane() (independent tracer);
 *   - k = transparent (interior or flat boundary) lattice points of the
 *     three other classes;
 *   - B_min: finest partition of cells closed under the four edge-crossing
 *     involutions and containing the 2-cycles at transparent non-class points;
 *     N_min separates S,T iff no cell at S is B_min-equivalent to a cell at T.
 * Output (one text block per room), counters, and survivors (pairs with no
 * certificate) in a separate file.
 *
 * usage: shoot BOUND CERTMAX infile outfile survivorfile
 *   infile "-" = stdin; per-room/per-pair lines are written only for area <= CERTMAX
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int verify_plane(int ncell, const int *cx, const int *cy,
                 int sx0, int sy0, int dx, int dy, int m, int tx, int ty);

#define MAXC 40
#define G 48                       /* grid side for cells and points (coords 0..G-2) */
#define MAXP (G * G)

static int n, cx[MAXC], cy[MAXC];
static int cellid[G][G];           /* -1 if absent */
static int nsq;
static int H[4 * MAXC], V[4 * MAXC], LAB[4 * MAXC], BLK[4 * MAXC];
static const int SX[4] = {1, -1, 1, -1}, SY[4] = {1, 1, -1, -1};

static int has(int x, int y) { return x >= 0 && y >= 0 && x < G && y < G && cellid[x][y] >= 0; }
static int cnt_around(int x, int y) { return has(x - 1, y - 1) + has(x, y - 1) + has(x - 1, y) + has(x, y); }

/* primitive directions */
static int ndir, DP_[4000], DQ_[4000];
static unsigned char WORD[4000][128];
static int WLEN[4000];

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

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
                    if (uv < uh) { WORD[ndir][L++] = 0; a++; }   /* vertical line: h */
                    else         { WORD[ndir][L++] = 1; b++; }   /* horizontal line: v */
                }
            }
            WLEN[ndir] = L;
            ndir++;
        }
}

static int sq(int c, int sh) { return 4 * c + sh; }

static void build_origami(void) {
    nsq = 4 * n;
    for (int c = 0; c < n; c++)
        for (int sh = 0; sh < 4; sh++) {
            int s = sq(c, sh), i = cx[c], j = cy[c], sx = SX[sh], sy = SY[sh];
            int fx = sh ^ 1, fy = sh ^ 2;   /* sheet with sx / sy flipped */
            H[s] = has(i + sx, j) ? sq(cellid[i + sx][j], sh) : sq(c, fx);
            V[s] = has(i, j + sy) ? sq(cellid[i][j + sy], sh) : sq(c, fy);
            int X = i + (sx < 0), Y = j + (sy < 0);
            LAB[s] = X * G + Y;
            int k = cnt_around(X, Y);
            BLK[s] = (k == 1 || k == 3);
        }
}

/* next start square after one lattice step from the bottom-left corner of s */
static int step(int s, int d) {
    int p = DP_[d], q = DQ_[d];
    if (q == 0) return H[s];
    if (p == 0) return V[s];
    int c = s;
    for (int t = 0; t < WLEN[d]; t++) c = WORD[d][t] ? V[c] : H[c];
    return H[V[c]];
}

/* union-find */
static int par[MAXC];
static int fnd(int a) { while (par[a] != a) { par[a] = par[par[a]]; a = par[a]; } return a; }

static int qa[MAXC * MAXC * 4], qb[MAXC * MAXC * 4];
static int kap[4][MAXC];

static void bmin(int ox, int oy, int *blk, int *nblk) {
    /* edge-crossing involutions relative to origin parity (ox,oy) */
    for (int c = 0; c < n; c++) {
        int i = cx[c], j = cy[c];
        for (int pr = 0; pr < 2; pr++) {
            int xe = (((i - ox) % 2 + 2) % 2 == pr) ? i : i + 1;
            int nx = (xe == i) ? i - 1 : i + 1;
            kap[pr][c] = has(nx, j) ? cellid[nx][j] : c;
            int ye = (((j - oy) % 2 + 2) % 2 == pr) ? j : j + 1;
            int ny = (ye == j) ? j - 1 : j + 1;
            kap[2 + pr][c] = has(i, ny) ? cellid[i][ny] : c;
        }
    }
    for (int c = 0; c < n; c++) par[c] = c;
    int qh = 0, qt = 0;
    /* seeds: transparent lattice points of the other three classes */
    for (int X = 0; X < G - 1; X++)
        for (int Y = 0; Y < G - 1; Y++) {
            if (((X - ox) & 1) == 0 && ((Y - oy) & 1) == 0) continue;
            int ll = has(X - 1, Y - 1), lr = has(X, Y - 1), ul = has(X - 1, Y), ur = has(X, Y);
            int k = ll + lr + ul + ur;
            int pa[2], pb[2], np = 0;
            if (k == 4) {
                pa[0] = cellid[X - 1][Y - 1]; pb[0] = cellid[X][Y];
                pa[1] = cellid[X][Y - 1]; pb[1] = cellid[X - 1][Y]; np = 2;
            } else if (k == 2) {
                int cs[2], m = 0;
                if (ll) cs[m++] = cellid[X - 1][Y - 1];
                if (lr) cs[m++] = cellid[X][Y - 1];
                if (ul) cs[m++] = cellid[X - 1][Y];
                if (ur) cs[m++] = cellid[X][Y];
                pa[0] = cs[0]; pb[0] = cs[1]; np = 1;
            }
            for (int t = 0; t < np; t++) {
                int a = fnd(pa[t]), b = fnd(pb[t]);
                if (a != b) { par[a] = b; qa[qt] = pa[t]; qb[qt] = pb[t]; qt++; }
            }
        }
    while (qh < qt) {
        int a0 = qa[qh], b0 = qb[qh]; qh++;
        for (int g = 0; g < 4; g++) {
            int a = fnd(kap[g][a0]), b = fnd(kap[g][b0]);
            if (a != b) { par[a] = b; qa[qt] = kap[g][a0]; qb[qt] = kap[g][b0]; qt++; }
        }
    }
    int nb = 0;
    for (int c = 0; c < n; c++) { blk[c] = fnd(c); if (blk[c] == c) nb++; }
    *nblk = nb;
}

/* counters */
static long long st_k7r[41][64], st_k7p[41][64]; static int st_maxk[41][64];
static long long st_rooms[41][64], st_pairs[41][64], st_lit[41][64], st_unres[41][64];
static long long st_litsep = 0, st_unres_sep = 0, st_unres_nosep = 0, st_verify_fail = 0;
static long long st_k7rooms = 0, st_k7pairs = 0;
static int st_maxk_lit = -1;
static long long st_maxk_hist[64], st_khist[64][64];
static int st_maxk_lit_w[64];

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: shoot BOUND CERTMAX infile outfile survivorfile\n"); return 1; }
    int bound = atoi(argv[1]);
    make_dirs(bound);
    int certmax = atoi(argv[2]);
    FILE *in = strcmp(argv[3], "-") ? fopen(argv[3], "r") : stdin;
    FILE *out = fopen(argv[4], "w");
    FILE *sv = fopen(argv[5], "w");
    FILE *nul = fopen("/dev/null", "w");
    char line[4096];
    long long rid = 0;
    memset(cellid, -1, sizeof cellid);
    while (fgets(line, sizeof line, in)) {
        if (line[0] == '#') continue;
        char *pp = line;
        int area = (int)strtol(pp, &pp, 10), W = (int)strtol(pp, &pp, 10);
        n = area;
        for (int c = 0; c < n; c++) {
            cx[c] = (int)strtol(pp, &pp, 10) + 1;   /* shift by 1 so x-1 >= 0 */
            cy[c] = (int)strtol(pp, &pp, 10) + 1;
            cellid[cx[c]][cy[c]] = c;
        }
        rid++;
        FILE *ro = (area <= certmax) ? out : nul;
        /* points */
        int npt = 0, ptx[4 * MAXC], pty[4 * MAXC], ptk[4 * MAXC];
        static int mark[G][G];
        for (int c = 0; c < n; c++)
            for (int d = 0; d < 4; d++) {
                int X = cx[c] + (d & 1), Y = cy[c] + (d >> 1);
                if (mark[X][Y] == (int)rid) continue;
                mark[X][Y] = (int)rid;
                ptx[npt] = X; pty[npt] = Y; ptk[npt] = cnt_around(X, Y); npt++;
            }
        int r = 0, Wc = 0;
        for (int i = 0; i < npt; i++) { if (ptk[i] == 3) r++; if (ptk[i] == 1 || ptk[i] == 3) Wc++; }
        if (Wc != W) { fprintf(stderr, "wall count mismatch room %lld\n", rid); return 2; }
        build_origami();
        fprintf(ro, "R %lld %d %d %d", rid, area, W, r);
        for (int c = 0; c < n; c++) fprintf(ro, " %d %d", cx[c] - 1, cy[c] - 1);
        fputc('\n', ro);
        st_rooms[area][W]++;
        int room_k7 = 0;
        for (int cl = 0; cl < 4; cl++) {
            int ox = cl >> 1, oy = cl & 1;
            int ip[4 * MAXC], ni = 0, k = 0;
            for (int i = 0; i < npt; i++) {
                int same = ((ptx[i] - ox) & 1) == 0 && ((pty[i] - oy) & 1) == 0;
                if (same && ptk[i] == 4) ip[ni++] = i;
                if (!same && (ptk[i] == 2 || ptk[i] == 4)) k++;
            }
            if (ni < 2) continue;
            int blk[MAXC], nblk;
            bmin(ox, oy, blk, &nblk);
            /* internal coordinates are shifted by (1,1): print the class parity in output coordinates */
            fprintf(ro, "K %d %d %d %d\n", ox ^ 1, oy ^ 1, k, nblk);
            /* resolved[a][b] */
            static int res_sh[4 * MAXC][4 * MAXC], res_d[4 * MAXC][4 * MAXC], res_m[4 * MAXC][4 * MAXC];
            static int resolved[4 * MAXC][4 * MAXC], res_src[4 * MAXC][4 * MAXC];
            for (int a = 0; a < ni; a++) for (int b = 0; b < ni; b++) resolved[a][b] = 0;
            /* which labels are class interior points: map label -> a or -1 */
            static int labidx[G * G];
            for (int i = 0; i < npt; i++) labidx[ptx[i] * G + pty[i]] = -1;
            for (int a = 0; a < ni; a++) labidx[ptx[ip[a]] * G + pty[ip[a]]] = a;
            for (int a = 0; a < ni; a++) {
                int need = 0;
                for (int b = a + 1; b < ni; b++) if (!resolved[a][b]) need++;
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
                                if (!resolved[lo][hi]) {
                                    resolved[lo][hi] = 1;
                                    res_sh[lo][hi] = sh; res_d[lo][hi] = d; res_m[lo][hi] = m;
                                    res_src[lo][hi] = a;
                                    if (b > a) need--;
                                }
                            }
                            if (s == s0) break;
                        }
                    }
            }
            for (int a = 0; a < ni; a++)
                for (int b = a + 1; b < ni; b++) {
                    int Sx = ptx[ip[a]], Sy = pty[ip[a]], Tx = ptx[ip[b]], Ty = pty[ip[b]];
                    int sep = 1;
                    for (int u = 0; u < 4 && sep; u++) {
                        int ca = cellid[Sx - 1 + (u & 1)][Sy - 1 + (u >> 1)];
                        for (int w = 0; w < 4; w++) {
                            int cb = cellid[Tx - 1 + (w & 1)][Ty - 1 + (w >> 1)];
                            if (blk[ca] == blk[cb]) { sep = 0; break; }
                        }
                    }
                    st_pairs[area][W]++;
                    if (resolved[a][b]) {
                        int src = res_src[a][b];
                        int sh = res_sh[a][b], d = res_d[a][b], m = res_m[a][b];
                        int S2x = ptx[ip[src]], S2y = pty[ip[src]];
                        int T2x = (src == a) ? Tx : Sx, T2y = (src == a) ? Ty : Sy;
                        int ok = verify_plane(n, cx, cy, S2x, S2y, SX[sh] * DP_[d], SY[sh] * DQ_[d], m, T2x, T2y);
                        if (!ok) st_verify_fail++;
                        st_lit[area][W]++;
                        if (sep) st_litsep++;
                        if (k > st_maxk_lit) st_maxk_lit = k;
                        if (k >= 7) { room_k7 = 1; st_k7pairs++; st_k7p[area][W]++; }
                        if (k > st_maxk[area][W]) st_maxk[area][W] = k;
                        st_maxk_hist[k]++; st_khist[W][k]++;
                        if (k > st_maxk_lit_w[W]) st_maxk_lit_w[W] = k;
                        fprintf(ro, "P %d %d %d %d L %d %d %d %d %d %d%s\n", S2x - 1, S2y - 1, T2x - 1, T2y - 1,
                                sep, SX[sh] * DP_[d], SY[sh] * DQ_[d], m, k, nblk, ok ? "" : " VERIFYFAIL");
                    } else {
                        st_unres[area][W]++;
                        if (sep) st_unres_sep++; else st_unres_nosep++;
                        fprintf(ro, "P %d %d %d %d U %d %d %d\n", Sx - 1, Sy - 1, Tx - 1, Ty - 1, sep, k, nblk);
                        fprintf(sv, "%lld %d %d %d %d %d %d %d %d", rid, area, W, r, Sx - 1, Sy - 1, Tx - 1, Ty - 1, sep);
                        fprintf(sv, " %d %d |", k, nblk);
                        for (int c = 0; c < n; c++) fprintf(sv, " %d %d", cx[c] - 1, cy[c] - 1);
                        fputc('\n', sv);
                    }
                }
        }
        if (room_k7) { st_k7rooms++; st_k7r[area][W]++; }
        for (int c = 0; c < n; c++) cellid[cx[c]][cy[c]] = -1;
    }
    fprintf(out, "# STATS bound %d dirs %d rooms %lld\n", bound, ndir, rid);
    for (int a = 0; a <= 40; a++)
        for (int w = 0; w < 64; w++)
            if (st_rooms[a][w])
                fprintf(out, "# T area %d W %d eligible_rooms %lld pairs %lld lit %lld unresolved %lld"
                        " rooms_k7lit %lld pairs_k7lit %lld maxk_lit %d\n",
                        a, w, st_rooms[a][w], st_pairs[a][w], st_lit[a][w], st_unres[a][w],
                        st_k7r[a][w], st_k7p[a][w], st_maxk[a][w]);
    fprintf(out, "# lit_but_separated %lld\n# unresolved_separated %lld\n# unresolved_not_separated %lld\n",
            st_litsep, st_unres_sep, st_unres_nosep);
    fprintf(out, "# verify_fail %lld\n# max_k_lit %d\n# rooms_with_lit_pair_k_ge7 %lld\n# lit_pairs_k_ge7 %lld\n",
            st_verify_fail, st_maxk_lit, st_k7rooms, st_k7pairs);
    for (int k = 0; k < 64; k++) if (st_maxk_hist[k]) fprintf(out, "# lit_pairs_with_k %d %lld\n", k, st_maxk_hist[k]);
    for (int w = 0; w < 64; w++)
        for (int k = 0; k < 64; k++)
            if (st_khist[w][k]) fprintf(out, "# lit_pairs_W_k %d %d %lld\n", w, k, st_khist[w][k]);
    fprintf(out, "# DONE\n");
    fclose(out); fclose(sv);
    return 0;
}
