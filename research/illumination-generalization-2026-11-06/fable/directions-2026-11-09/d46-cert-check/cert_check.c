/* cert_check.c -- d46 finite check for 5 <= r <= 8 (design: ../d44-cert-check-sizing).
 * No ray, direction, or illumination search.
 *
 * Pipeline per job:
 *   1. Shape DFS (from d44 count_rooms.c): compressed shapes as row bit masks, bottom
 *      to top, pruned on the corner budget.  The job split assigns depth-SPLIT
 *      prefixes round-robin (index mod NJ == JOB); shapes with fewer rows go to job 0.
 *   2. Symmetry: a shape is processed only if it is the lex-least of its 8 images.
 *      For a symmetric shape, a weight vector (w, h) is kept only if it is lex-least
 *      under the shape's stabilizer.  A room is (shape, w, h) with a unique compressed
 *      shape, so every free room is generated exactly once.
 *   3. Parity patterns: the parities of the corner x and y coordinates fix the corner
 *      classes and rho_y (reflex corners per absolute parity class).  Out of scope
 *      (fewer than 3 corner classes) patterns are skipped when SCOPE3 = 1.  The allowed
 *      area set A is computed per pattern and PER AREA n: n in A iff F*(rho, n, r)
 *      holds (FSTAR = 1).  FSTAR = 0 keeps every area; FSTAR = 2 keeps every area and
 *      applies F* per room from the materialised cells (validation mode).
 *   4. Weights with those parities are enumerated; the last row's height is solved
 *      for each n in A, so only rooms with area in A are produced.
 *   5. CHECK = 1: the room is materialised; its corners, rho and classes are recounted
 *      from the cells and must match the pattern (else exit 3); then the d44 check:
 *      B_b, B_c, B_d (finest G-invariant partitions containing the 2-cycles of g_x)
 *      and separation of all four endpoint lift pairs, for every same-class pair of
 *      interior lattice marks.  A positive prints full coordinates and exits 10.
 *
 * usage: cert_check WMIN WMAX AMIN AMAX CAP5R FSTAR SCOPE3 CHECK NJ JOB SPLIT
 *        cert_check stdin [v]      (check rooms "n x0 y0 x1 y1 ..." read from stdin)
 *        cert_check fstar_dump RMIN RMAX NMIN NMAX   (F* on every rho vector)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/resource.h>

#define WID 10
#define NM (1 << WID)
#define AM 128

static int WMIN, WMAX, AMIN, AMAX, CAP5R, FSTAR, SCOPE3, CHECK, NJ = 1, JOB = 0, SPLIT = 3;
static unsigned char cost[NM][NM], pinch[NM][NM];
static int *bl[NM], gstart[NM][2 * WID + 4];   /* candidates grouped by cost, popcount ascending */
static int rows[16], m;

/* ---------------- F* ---------------- */
static int fs_n[64][AM], fs_delta[64][AM][32], fs_zmin[64][AM][32];

static void fs_prep(void) {
    for (int r = 0; r < 64; r++)
        for (int n = 1; n < AM; n++) {
            int k = 0;
            for (int d = 3; d <= n; d++) {
                if (n % d) continue;
                int delta = n / d;
                if (delta < 3) continue;
                int zmin = (d & 1) ? (d + 2) / 4 : (d + 3) / 4;
                if (zmin < 1) zmin = 1;
                if (zmin * delta <= r) { fs_delta[r][n][k] = delta; fs_zmin[r][n][k] = zmin; k++; }
            }
            fs_n[r][n] = k;
        }
}

static int fstar_pass(const int *rho, int n, int r) {
    for (int k = 0; k < fs_n[r][n]; k++) {
        int dl = fs_delta[r][n][k], s = 0;
        for (int y = 0; y < 4; y++) s += rho[y] / dl;
        if (s >= fs_zmin[r][n][k]) return 1;
    }
    return 0;
}

/* ---------------- per-room check (ported from d44 check_rooms.c) ---------------- */
#define MAXC 128
#define G 48
static int n_, cx_[MAXC], cy_[MAXC], id[G][G];
static int cell(int x, int y) { return (x >= 0 && y >= 0 && x < G && y < G) ? id[x][y] : -1; }

static void gen(int px, int py, int ox, int oy, int *g) {
    for (int k = 0; k < n_; k++) {
        int x = cx_[k], y = cy_[k];
        int ex = ((x - ox) & 1) == px ? x - 1 : x + 1;
        int k1 = cell(ex, y); if (k1 < 0) k1 = k;
        int x1 = cx_[k1], y1 = cy_[k1];
        int ey = ((y1 - oy) & 1) == py ? y1 - 1 : y1 + 1;
        int k2 = cell(x1, ey); if (k2 < 0) k2 = k1;
        g[k] = k2;
    }
}

static int par[MAXC];
static int find(int a) { while (par[a] != a) { par[a] = par[par[a]]; a = par[a]; } return a; }

static int closure(int gs[8][MAXC], const int *seedg) {
    static int qa[MAXC * MAXC], qb[MAXC * MAXC];
    int qn = 0;
    for (int i = 0; i < n_; i++) par[i] = i;
    for (int i = 0; i < n_; i++) {
        int j = seedg[i];
        if (j != i && seedg[j] == i && i < j) {
            int ra = find(i), rb = find(j);
            if (ra != rb) { par[ra] = rb; qa[qn] = i; qb[qn] = j; qn++; }
        }
    }
    while (qn) {
        qn--; int a = qa[qn], b = qb[qn];
        for (int t = 0; t < 8; t++) {
            int u = gs[t][a], v = gs[t][b];
            int ra = find(u), rb = find(v);
            if (ra != rb) { par[ra] = rb; qa[qn] = u; qb[qn] = v; qn++; }
        }
    }
    int k = 0; for (int i = 0; i < n_; i++) if (find(i) == i) k++;
    return k;
}

static void inv(const int *g, int *h) { for (int i = 0; i < n_; i++) h[g[i]] = i; }

/* results of the last check_room call */
static int ck_r, ck_conv, ck_rho[4], ck_cls, ck_pairs, ck_pos, ck_nbk[4][4], ck_ns[4];
static int ck_S[64][2], ck_T[64][2], ck_np;   /* positive pairs (shifted back) */
static int ck_posO[64];

/* cells already in cx_, cy_ (n_ of them).  Fills id, scans lattice points, runs the
 * partition test if DOCHECK.  Returns number of positive pairs. */
static int check_room(int docheck) {
    static int gs[8][MAXC];
    int mnx = 1 << 20, mny = 1 << 20, mxx = -(1 << 20), mxy = -(1 << 20);
    for (int k = 0; k < n_; k++) {
        if (cx_[k] < mnx) mnx = cx_[k]; if (cy_[k] < mny) mny = cy_[k];
        if (cx_[k] > mxx) mxx = cx_[k]; if (cy_[k] > mxy) mxy = cy_[k];
    }
    int sx = 2 - mnx, sy = 2 - mny; sx += sx & 1; sy += sy & 1;   /* even shift keeps parity */
    if (mxx + sx + 2 >= G || mxy + sy + 2 >= G || n_ > MAXC) { fprintf(stderr, "room too large\n"); exit(4); }
    for (int k = 0; k < n_; k++) { cx_[k] += sx; cy_[k] += sy; id[cx_[k]][cy_[k]] = k; }
    int x0 = mnx + sx, x1 = mxx + sx + 1, y0 = mny + sy, y1 = mxy + sy + 1;
    ck_r = ck_conv = ck_cls = ck_pairs = ck_pos = ck_np = 0;
    memset(ck_rho, 0, sizeof ck_rho); memset(ck_nbk, 0, sizeof ck_nbk); memset(ck_ns, 0, sizeof ck_ns);
    int ipx[MAXC * 2], ipy[MAXC * 2], ni = 0;
    for (int x = x0; x <= x1; x++) for (int y = y0; y <= y1; y++) {
        int c = (cell(x - 1, y - 1) >= 0) + (cell(x, y - 1) >= 0) + (cell(x - 1, y) >= 0) + (cell(x, y) >= 0);
        int cl = (x & 1) * 2 + (y & 1);
        if (c == 1) { ck_conv++; ck_cls |= 1 << cl; }
        if (c == 3) { ck_r++; ck_rho[cl]++; ck_cls |= 1 << cl; }
        if (c == 4) { ipx[ni] = x; ipy[ni] = y; ni++; }
    }
    if (docheck) for (int o = 0; o < 4; o++) {
        int ox = o >> 1, oy = o & 1;
        int S[MAXC], ns = 0;
        for (int i = 0; i < ni; i++) if ((ipx[i] & 1) == ox && (ipy[i] & 1) == oy) S[ns++] = i;
        ck_ns[o] = ns;
        if (ns < 2) continue;
        if (ns > 64) { fprintf(stderr, "too many marks\n"); exit(4); }
        ck_pairs += ns * (ns - 1) / 2;
        gen(0, 0, ox, oy, gs[0]); gen(1, 0, ox, oy, gs[1]); gen(1, 1, ox, oy, gs[2]); gen(0, 1, ox, oy, gs[3]);
        for (int t = 0; t < 4; t++) inv(gs[t], gs[4 + t]);
        int L[MAXC][2];
        for (int s = 0; s < ns; s++) {
            int x = ipx[S[s]], y = ipy[S[s]];
            int sw = cell(x - 1, y - 1), q[4] = {sw, cell(x, y - 1), cell(x - 1, y), cell(x, y)};
            int p = gs[0][sw], other = -1;
            for (int k = 0; k < 4; k++) if (q[k] != sw && q[k] != p) { other = q[k]; break; }
            L[s][0] = sw; L[s][1] = other;
        }
        uint64_t ok[64]; for (int s = 0; s < ns; s++) ok[s] = ~0ULL;
        int alive = 1;
        for (int x = 1; x <= 3 && alive; x++) {
            int k = closure(gs, gs[x]); ck_nbk[o][x] = k;
            if (k == 1) { alive = 0; break; }
            int blk[MAXC], img[MAXC], cyc[MAXC];
            for (int i = 0; i < n_; i++) blk[i] = find(i);
            for (int i = 0; i < n_; i++) img[blk[i]] = blk[gs[0][i]], cyc[i] = -1;
            for (int i = 0; i < n_; i++) if (blk[i] == i && cyc[i] < 0) {
                int j = i; while (cyc[j] < 0) { cyc[j] = i; j = img[j]; }
            }
            int any = 0;
            for (int s = 0; s < ns; s++) {
                int a0 = cyc[blk[L[s][0]]], a1 = cyc[blk[L[s][1]]];
                for (int u = s + 1; u < ns; u++) {
                    int b0 = cyc[blk[L[u][0]]], b1 = cyc[blk[L[u][1]]];
                    if (a0 == b0 || a0 == b1 || a1 == b0 || a1 == b1) ok[s] &= ~(1ULL << u);
                    if (ok[s] >> u & 1) any = 1;
                }
            }
            if (!any) alive = 0;
        }
        if (!alive) continue;
        for (int s = 0; s < ns; s++) for (int u = s + 1; u < ns; u++) if (ok[s] >> u & 1) {
            if (ck_np < 64) {
                ck_S[ck_np][0] = ipx[S[s]] - sx; ck_S[ck_np][1] = ipy[S[s]] - sy;
                ck_T[ck_np][0] = ipx[S[u]] - sx; ck_T[ck_np][1] = ipy[S[u]] - sy;
                ck_posO[ck_np] = o; ck_np++;
            }
            ck_pos++;
        }
    }
    for (int k = 0; k < n_; k++) { id[cx_[k]][cy_[k]] = -1; cx_[k] -= sx; cy_[k] -= sy; }
    return ck_pos;
}

/* ---------------- shape DFS (from d44 count_rooms.c) ---------------- */
static int bit(int a, int x) { return x >= 0 && x < WID ? (a >> x) & 1 : 0; }

static void prep(void) {
    for (int a = 0; a < NM; a++)
        for (int b = 0; b < NM; b++) {
            int c = 0, p = 0;
            for (int x = 0; x <= WID; x++) {
                int q0 = bit(a, x - 1), q1 = bit(a, x), q2 = bit(b, x - 1), q3 = bit(b, x);
                int s = q0 + q1 + q2 + q3;
                if (s & 1) c++;
                if (s == 2 && ((q0 && q3) || (q1 && q2))) p = 1;
            }
            cost[a][b] = c; pinch[a][b] = p;
        }
    for (int a = 0; a < NM; a++) {
        bl[a] = malloc(sizeof(int) * NM); int k = 0;
        for (int c = 0; c <= 2 * WID + 2; c++) {
            gstart[a][c] = k;
            for (int pc = 1; pc <= WID; pc++)
                for (int b = 1; b < NM; b++)
                    /* a mask with top bit hb forces K >= hb + 1 columns, and K + 1 vertical lines
                       carry >= 2 corners each, so W >= 2 (hb + 2): skip masks that can't fit WMAX */
                    if (cost[a][b] == c && __builtin_popcount(b) == pc && b != a && (a == 0 || (a & b)) &&
                        !pinch[a][b] && 2 * (32 - __builtin_clz(b) + 1) <= WMAX) bl[a][k++] = b;
        }
        gstart[a][2 * WID + 3] = k;
    }
}

static int simple_room(int K) {
    int H = m + 2, Wd = K + 2;
    unsigned char g[18][18]; memset(g, 0, sizeof g);
    for (int j = 0; j < m; j++) for (int i = 0; i < K; i++) if (rows[j] >> i & 1) g[j + 1][i + 1] = 1;
    int st[400], sp = 0, seen = 1, tot = 0;
    for (int y = 0; y < H; y++) for (int x = 0; x < Wd; x++) if (!g[y][x]) tot++;
    g[0][0] = 2; st[sp++] = 0;
    static const int d[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    while (sp) {
        int v = st[--sp], y = v / Wd, x = v % Wd;
        for (int k = 0; k < 4; k++) {
            int yy = y + d[k][1], xx = x + d[k][0];
            if (yy < 0 || yy >= H || xx < 0 || xx >= Wd || g[yy][xx]) continue;
            g[yy][xx] = 2; seen++; st[sp++] = yy * Wd + xx;
        }
    }
    if (seen != tot) return 0;
    int cs, ctot = 0, sy = -1, sx = -1;
    for (int y = 1; y <= m; y++) for (int x = 1; x <= K; x++) if (g[y][x] == 1) { ctot++; if (sy < 0) { sy = y; sx = x; } }
    g[sy][sx] = 3; cs = 1; sp = 0; st[sp++] = sy * Wd + sx;
    while (sp) {
        int v = st[--sp], y = v / Wd, x = v % Wd;
        for (int k = 0; k < 4; k++) {
            int yy = y + d[k][1], xx = x + d[k][0];
            if (g[yy][xx] != 1) continue;
            g[yy][xx] = 3; cs++; st[sp++] = yy * Wd + xx;
        }
    }
    return cs == ctot;
}

/* ---------------- per-shape state ---------------- */
static int K, W_cur, r_cur, ACAP;
static int nstab, stab[8];                      /* non-identity stabilizer elements */
static int ncorner, crn_i[64], crn_j[64], crn_ref[64];
static int xp[WID + 1], yp[16];                 /* parity of X_i (i = 0..K), Y_j (j = 0..m) */
static int wmin[WID], hmin[16], colhmin[WID];
static int cw[WID], ch[16];
static int pat_rho[4], pat_cls;
static uint64_t Aset;                           /* allowed areas (bit n), current pattern */
static int Amax_pat;

/* statistics, indexed [W][area] */
static long long st_shapes[24], st_pat[24], st_pat_scope[24], st_pat_pass[24];
static long long st_gen[24][AM], st_fixed[24][AM], st_pass[24][AM], st_chk[24][AM], st_pairs[24][AM], st_pos[24][AM];
static long long st_mismatch = 0, dumpctr = 0;
static long long DUMP_EVERY = 0;     /* env DUMP_EVERY=k: print every k-th room passing F* to stderr */

static void transform_shape(int t, int *nr, int *ncl, int *N) {
    int sw = t >> 2 & 1, fx = t & 1, fy = t >> 1 & 1;
    *nr = sw ? K : m; *ncl = sw ? m : K;
    for (int j = 0; j < *nr; j++) N[j] = 0;
    for (int j = 0; j < m; j++) for (int i = 0; i < K; i++) if (rows[j] >> i & 1) {
        int i1 = fx ? K - 1 - i : i, j1 = fy ? m - 1 - j : j;
        if (sw) N[i1] |= 1 << j1; else N[j1] |= 1 << i1;
    }
}

/* 1 if the current shape is the least of its orbit; fills stab[] */
static int canonical_shape(void) {
    int N[16], nr, ncl;
    nstab = 0;
    for (int t = 1; t < 8; t++) {
        transform_shape(t, &nr, &ncl, N);
        if (nr != m) { if (nr < m) return 0; continue; }
        if (ncl != K) { if (ncl < K) return 0; continue; }
        int cmp = 0;
        for (int j = 0; j < m && !cmp; j++) cmp = N[j] < rows[j] ? -1 : N[j] > rows[j] ? 1 : 0;
        if (cmp < 0) return 0;
        if (cmp == 0) stab[nstab++] = t;
    }
    return 1;
}

/* weight vector image under stabilizer element t: returns -1, 0, 1 for image <, ==, > (w, h) */
static int cmp_image(int t) {
    int sw = t >> 2 & 1, fx = t & 1, fy = t >> 1 & 1;
    int nw[WID], nh[16];
    for (int i2 = 0; i2 < K; i2++) nw[i2] = sw ? ch[fy ? m - 1 - i2 : i2] : cw[fx ? K - 1 - i2 : i2];
    for (int j2 = 0; j2 < m; j2++) nh[j2] = sw ? cw[fx ? K - 1 - j2 : j2] : ch[fy ? m - 1 - j2 : j2];
    for (int i = 0; i < K; i++) if (nw[i] != cw[i]) return nw[i] < cw[i] ? -1 : 1;
    for (int j = 0; j < m; j++) if (nh[j] != ch[j]) return nh[j] < ch[j] ? -1 : 1;
    return 0;
}

static void report_positive(int area) {
    printf("POSITIVE W %d r %d area %d corner_classes %d rho %d %d %d %d widths", W_cur, r_cur, area,
           __builtin_popcount(ck_cls), ck_rho[0], ck_rho[1], ck_rho[2], ck_rho[3]);
    for (int i = 0; i < K; i++) printf(" %d", cw[i]);
    printf(" heights"); for (int j = 0; j < m; j++) printf(" %d", ch[j]);
    printf(" rows"); for (int j = 0; j < m; j++) printf(" %d", rows[j]);
    printf("\n");
    for (int p = 0; p < ck_np; p++) {
        int o = ck_posO[p];
        printf("POSITIVE_PAIR origin_parity (%d,%d) S (%d,%d) T (%d,%d) blocks b c d %d %d %d\n", o >> 1, o & 1,
               ck_S[p][0], ck_S[p][1], ck_T[p][0], ck_T[p][1], ck_nbk[o][1], ck_nbk[o][2], ck_nbk[o][3]);
    }
    printf("POSITIVE_CELLS %d", n_);
    for (int k = 0; k < n_; k++) printf(" %d %d", cx_[k], cy_[k]);
    printf("\n");
    fflush(stdout);
}

static void emit_room(int area) {
    int rstab = 1;
    for (int s = 0; s < nstab; s++) {
        int c = cmp_image(stab[s]);
        if (c < 0) return;                      /* another orbit member is the representative */
        if (c == 0) rstab++;
    }
    int W = W_cur;
    st_gen[W][area]++; st_fixed[W][area] += 8 / rstab;
    int need_cells = CHECK || FSTAR == 2 || DUMP_EVERY;
    if (!need_cells) { st_pass[W][area]++; return; }
    /* materialise */
    n_ = 0;
    int X[WID + 1], Y[17];
    X[0] = 0; for (int i = 0; i < K; i++) X[i + 1] = X[i] + cw[i];
    Y[0] = 0; for (int j = 0; j < m; j++) Y[j + 1] = Y[j] + ch[j];
    for (int j = 0; j < m; j++) for (int i = 0; i < K; i++) if (rows[j] >> i & 1)
        for (int y = Y[j]; y < Y[j + 1]; y++) for (int x = X[i]; x < X[i + 1]; x++) { cx_[n_] = x; cy_[n_] = y; n_++; }
    if (n_ != area) { fprintf(stderr, "area mismatch\n"); exit(3); }
    int pos = check_room(CHECK && FSTAR != 2);  /* corner scan, plus the check when F* is already applied */
    if (ck_r != r_cur || ck_conv != r_cur + 4 || ck_cls != pat_cls ||
        memcmp(ck_rho, pat_rho, sizeof pat_rho)) {
        st_mismatch++;
        fprintf(stderr, "pattern/room mismatch W %d area %d\n", W, area); exit(3);
    }
    if (FSTAR == 2) {
        if (SCOPE3 && __builtin_popcount(ck_cls) < 3) return;
        if (!fstar_pass(ck_rho, area, ck_r)) return;
        if (CHECK) pos = check_room(1);
    }
    st_pass[W][area]++;
    if (DUMP_EVERY && ++dumpctr % DUMP_EVERY == 0) {   /* sample for external cross-checks */
        fprintf(stderr, "%d", n_);
        for (int k = 0; k < n_; k++) fprintf(stderr, " %d %d", cx_[k], cy_[k]);
        fprintf(stderr, "\n");
    }
    if (!CHECK) return;
    st_chk[W][area]++;
    st_pairs[W][area] += ck_pairs;
    if (pos) {
        st_pos[W][area] += pos;
        report_positive(area);
        if (r_cur <= 8) { printf("ABORT positive with r <= 8\n"); fflush(stdout); exit(10); }
    }
}

/* rows 0..m-2 choose h; last row solved per n in Aset */
static int rowc[16];
static void rec_h(int j, int area) {
    if (j == m - 1) {
        int c = rowc[j];
        uint64_t A = Aset >> (area + 1) << (area + 1);
        while (A) {
            int n = __builtin_ctzll(A); A &= A - 1;
            int rem = n - area;
            if (rem % c) continue;
            int h = rem / c;
            if (h < hmin[j] || ((h - hmin[j]) & 1)) continue;
            ch[j] = h; emit_room(n);
        }
        return;
    }
    int rest = 0; for (int jj = j + 1; jj < m; jj++) rest += hmin[jj] * rowc[jj];
    for (int h = hmin[j]; area + h * rowc[j] + rest <= Amax_pat; h += 2) { ch[j] = h; rec_h(j + 1, area + h * rowc[j]); }
}

static void rec_w(int i, int s) {          /* s = sum_{i' < i} w_i' colhmin_i' */
    if (i == K) {
        for (int j = 0; j < m; j++) { int c = 0; for (int q = 0; q < K; q++) if (rows[j] >> q & 1) c += cw[q]; rowc[j] = c; }
        rec_h(0, 0);
        return;
    }
    int rest = 0; for (int q = i + 1; q < K; q++) rest += wmin[q] * colhmin[q];
    for (int w = wmin[i]; s + w * colhmin[i] + rest <= Amax_pat; w += 2) { cw[i] = w; rec_w(i + 1, s + w * colhmin[i]); }
}

/* FT[r][rho code]: bit n set iff F*(rho, n, r).  rho code = rho0<<12 | rho1<<8 | rho2<<4 | rho3. */
static uint64_t *FT[16];
static uint64_t *ftable(int r) {
    if (!FT[r]) {
        FT[r] = calloc(1 << 16, sizeof(uint64_t));
        for (int code = 0; code < (1 << 16); code++) {
            int rho[4] = {code >> 12 & 15, code >> 8 & 15, code >> 4 & 15, code & 15};
            if (rho[0] + rho[1] + rho[2] + rho[3] != r) continue;
            for (int n = 1; n < 64; n++) if (fstar_pass(rho, n, r)) FT[r][code] |= 1ULL << n;
        }
    }
    return FT[r];
}
static uint64_t range_mask;                     /* areas AMIN..ACAP */
static int line_n[17], line_i[17][24], line_ref[17][24];
static int rowpar[16];

static void leaf_pattern(int code, int cls, int par) {
    int W = W_cur;
    st_pat[W]++;
    if (SCOPE3 && FSTAR != 2 && __builtin_popcount(cls) < 3) return;
    st_pat_scope[W]++;
    Aset = range_mask & (par ? 0xAAAAAAAAAAAAAAAAULL : 0x5555555555555555ULL);
    if (FSTAR == 1) Aset &= ftable(r_cur)[code];
    if (!Aset) return;
    st_pat_pass[W]++;
    pat_rho[0] = code >> 12 & 15; pat_rho[1] = code >> 8 & 15; pat_rho[2] = code >> 4 & 15; pat_rho[3] = code & 15;
    pat_cls = cls;
    for (int i = 0; i < K; i++) { colhmin[i] = 0; for (int j = 0; j < m; j++) if (rows[j] >> i & 1) colhmin[i] += hmin[j]; }
    Amax_pat = 63 - __builtin_clzll(Aset);
    rec_w(0, 0);
}

/* add the corners on horizontal line j (y parity yp[j]) to (code, cls) */
static inline void add_line(int j, int *code, int *cls) {
    for (int k = 0; k < line_n[j]; k++) {
        int cl = xp[line_i[j][k]] * 2 + yp[j];
        *cls |= 1 << cl;
        if (line_ref[j][k]) *code += 1 << (4 * (3 - cl));
    }
}

/* partial = min area of rows 0..j-1; rows j.. at least height 1 */
static void rec_ypat(int j, int partial, const int *cmin, int code, int cls, int par) {
    if (j == m) { leaf_pattern(code, cls, par); return; }
    int rest = 0; for (int jj = j + 1; jj < m; jj++) rest += cmin[jj];
    for (int b = 0; b < 2; b++) {
        yp[j + 1] = b;
        int hp = yp[j] ^ b;                        /* parity of h_j */
        hmin[j] = hp ? 1 : 2;
        if (partial + hmin[j] * cmin[j] + rest > ACAP) continue;
        int c2 = code, l2 = cls;
        add_line(j + 1, &c2, &l2);
        rec_ypat(j + 1, partial + hmin[j] * cmin[j], cmin, c2, l2, par ^ (hp & rowpar[j]));
    }
}

static void rec_xpat(int i) {
    if (i == K) {
        int cmin[16], tot = 0;
        for (int j = 0; j < m; j++) {
            cmin[j] = 0; rowpar[j] = 0;
            for (int q = 0; q < K; q++) if (rows[j] >> q & 1) { cmin[j] += wmin[q]; rowpar[j] ^= wmin[q] & 1; }
            tot += cmin[j];
        }
        if (tot > ACAP) return;
        int code = 0, cls = 0;
        yp[0] = 0; add_line(0, &code, &cls);
        rec_ypat(0, 0, cmin, code, cls, 0);
        return;
    }
    for (int b = 0; b < 2; b++) { xp[i + 1] = b; wmin[i] = (xp[i] ^ b) ? 1 : 2; rec_xpat(i + 1); }
}

static void close_shape(int corners, int uni, int cells) {
    int W = corners;
    if (W > WMAX || W < WMIN || !(uni & 1)) return;
    K = 32 - __builtin_clz(uni);
    if (uni != (1 << K) - 1) return;
    for (int i = 0; i + 1 < K; i++) {
        int same = 1;
        for (int j = 0; j < m; j++) if (((rows[j] >> i) & 1) != ((rows[j] >> (i + 1)) & 1)) { same = 0; break; }
        if (same) return;
    }
    ACAP = AMAX;
    if (CAP5R && 5 * (W - 4) / 2 < ACAP) ACAP = 5 * (W - 4) / 2;
    if (cells > ACAP) return;
    if (!canonical_shape()) return;            /* symmetry-invariant tests: cheaper one first */
    if (!simple_room(K)) return;
    st_shapes[W]++;
    W_cur = W; r_cur = (W - 4) / 2;
    ncorner = 0;
    for (int j = 0; j <= m; j++) for (int i = 0; i <= K; i++) {
        int a = j > 0 ? rows[j - 1] : 0, b = j < m ? rows[j] : 0;
        int s = bit(a, i - 1) + bit(a, i) + bit(b, i - 1) + bit(b, i);
        if (s == 1 || s == 3) { crn_i[ncorner] = i; crn_j[ncorner] = j; crn_ref[ncorner] = s == 3; ncorner++; }
    }
    if (ncorner != W) { fprintf(stderr, "corner count mismatch\n"); exit(3); }
    for (int j = 0; j <= m; j++) line_n[j] = 0;
    for (int c = 0; c < ncorner; c++) { int j = crn_j[c]; line_i[j][line_n[j]] = crn_i[c]; line_ref[j][line_n[j]] = crn_ref[c]; line_n[j]++; }
    range_mask = 0; for (int n = AMIN; n <= ACAP; n++) range_mask |= 1ULL << n;
    xp[0] = 0; rec_xpat(0);
}

static long long splitctr = 0;
static void dfs(int prev, int corners, int uni, int cells) {
    if (m == SPLIT && (splitctr++ % NJ) != JOB) return;
    if (m >= SPLIT || JOB == 0) close_shape(corners + cost[prev][0], uni, cells);
    for (int c0 = 0; corners + c0 + 2 <= WMAX && c0 <= 2 * WID + 2; c0++)
        for (int k = gstart[prev][c0]; k < gstart[prev][c0 + 1]; k++) {
            int b = bl[prev][k], pc = __builtin_popcount(b);
            if (cells + pc > AMAX) break;
            rows[m++] = b;
            dfs(b, corners + c0, uni | b, cells + pc);
            m--;
        }
}

static double cpu_sec(void) {
    struct rusage u; getrusage(RUSAGE_SELF, &u);
    return u.ru_utime.tv_sec + u.ru_stime.tv_sec + 1e-6 * (u.ru_utime.tv_usec + u.ru_stime.tv_usec);
}

int main(int argc, char **argv) {
    memset(id, -1, sizeof id);
    fs_prep();
    if (argc >= 2 && !strcmp(argv[1], "fstar_dump")) {
        int r0 = atoi(argv[2]), r1 = atoi(argv[3]), n0 = atoi(argv[4]), n1 = atoi(argv[5]);
        for (int r = r0; r <= r1; r++)
            for (int a = 0; a <= r; a++) for (int b = 0; a + b <= r; b++) for (int c = 0; a + b + c <= r; c++) {
                int rho[4] = {a, b, c, r - a - b - c};
                for (int n = n0; n <= n1; n++) printf("%d %d %d %d %d %d %d\n", r, rho[0], rho[1], rho[2], rho[3], n, fstar_pass(rho, n, r));
            }
        return 0;
    }
    if (argc >= 2 && !strcmp(argv[1], "stdin")) {
        int verbose = argc > 2;
        long long rooms = 0, pos = 0;
        while (scanf("%d", &n_) == 1) {
            if (n_ > MAXC) return 2;
            for (int k = 0; k < n_; k++) if (scanf("%d %d", &cx_[k], &cy_[k]) != 2) return 1;
            rooms++;
            int p = check_room(1); pos += p;
            printf("room %lld n %d r %d corner_classes %d rho %d %d %d %d pairs %d positives %d fstar %d",
                   rooms, n_, ck_r, __builtin_popcount(ck_cls), ck_rho[0], ck_rho[1], ck_rho[2], ck_rho[3], ck_pairs, p,
                   fstar_pass(ck_rho, n_, ck_r));
            if (verbose) for (int o = 0; o < 4; o++) if (ck_ns[o] >= 2)
                printf(" | o(%d,%d) marks %d bcd %d %d %d", o >> 1, o & 1, ck_ns[o], ck_nbk[o][1], ck_nbk[o][2], ck_nbk[o][3]);
            printf("\n");
            for (int q = 0; q < ck_np; q++)
                printf("  POSITIVE origin_parity (%d,%d) S (%d,%d) T (%d,%d)\n", ck_posO[q] >> 1, ck_posO[q] & 1,
                       ck_S[q][0], ck_S[q][1], ck_T[q][0], ck_T[q][1]);
        }
        fprintf(stderr, "rooms %lld positive pairs %lld cpu %.3f\n", rooms, pos, cpu_sec());
        return 0;
    }
    if (argc < 12) {
        fprintf(stderr, "usage: cert_check WMIN WMAX AMIN AMAX CAP5R FSTAR SCOPE3 CHECK NJ JOB SPLIT\n"); return 1;
    }
    WMIN = atoi(argv[1]); WMAX = atoi(argv[2]); AMIN = atoi(argv[3]); AMAX = atoi(argv[4]);
    CAP5R = atoi(argv[5]); FSTAR = atoi(argv[6]); SCOPE3 = atoi(argv[7]); CHECK = atoi(argv[8]);
    NJ = atoi(argv[9]); JOB = atoi(argv[10]); SPLIT = atoi(argv[11]);
    if (WMAX > 2 * WID + 2 || AMAX >= 64 || WMAX >= 24) { fprintf(stderr, "range too large\n"); return 1; }
    if (getenv("DUMP_EVERY")) DUMP_EVERY = atoll(getenv("DUMP_EVERY"));
    prep();
    m = 0;
    for (int c0 = 0; c0 + 2 <= WMAX && c0 <= 2 * WID + 2; c0++)
        for (int k = gstart[0][c0]; k < gstart[0][c0 + 1]; k++) {
            int b = bl[0][k], pc = __builtin_popcount(b);
            if (pc > AMAX) break;
            m = 0; rows[m++] = b;
            dfs(b, c0, b, pc);
        }
    double sec = cpu_sec();
    long long T[8] = {0};
    for (int W = WMIN; W <= WMAX; W += 2) {
        printf("SHAPES W %d shapes %lld patterns %lld in_scope %lld fstar_pass %lld\n", W, st_shapes[W], st_pat[W], st_pat_scope[W], st_pat_pass[W]);
        T[0] += st_shapes[W];
        for (int a = AMIN; a <= AMAX; a++) if (st_gen[W][a] || st_fixed[W][a]) {
            printf("CELL W %d area %d generated %lld fixed %lld passed %lld checked %lld pairs %lld positives %lld\n",
                   W, a, st_gen[W][a], st_fixed[W][a], st_pass[W][a], st_chk[W][a], st_pairs[W][a], st_pos[W][a]);
            T[1] += st_gen[W][a]; T[2] += st_pass[W][a]; T[3] += st_chk[W][a]; T[4] += st_pairs[W][a]; T[5] += st_pos[W][a];
        }
    }
    printf("SUMMARY job %d of %d W %d..%d area %d..%d cap5r %d fstar %d scope3 %d check %d split %d prefixes %lld "
           "shapes %lld rooms_generated %lld rooms_passing_fstar %lld rooms_checked %lld pairs_checked %lld positives %lld cpu_s %.2f\n",
           JOB, NJ, WMIN, WMAX, AMIN, AMAX, CAP5R, FSTAR, SCOPE3, CHECK, SPLIT, splitctr,
           T[0], T[1], T[2], T[3], T[4], T[5], sec);
    return 0;
}
