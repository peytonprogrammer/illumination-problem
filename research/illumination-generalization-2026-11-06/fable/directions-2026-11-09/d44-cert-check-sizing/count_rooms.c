/* count_rooms.c -- count strictly simple polyomino rooms by (W, area) through
 * compressed shapes.  Sizing tool for d44; no illumination or ray search.
 *
 * Every room is a unique compressed shape (no two adjacent rows equal, no two
 * adjacent columns equal) with positive column widths w_i and row heights h_j.
 * Stretching keeps corners, strict simplicity, and simple connectivity, so W is a
 * property of the shape.  Area = sum_j h_j * c_j with c_j = sum_{i in row j} w_i.
 *
 * Shapes: rows bottom to top as bit masks of width <= 9 (W <= 20 forces <= 9 rows
 * and <= 9 columns).  Corners on the line between two rows depend only on the two
 * masks, so the DFS prunes on the corner budget.
 *
 * usage: count_rooms WMAX AMAX MODE [WMIN CAP5R PROBES SEED BETA D GAMMA WCAP]
 *   MODE 0: exact fixed counts per (W, area) for area <= AMAX (all W <= WMAX).
 *   MODE 1: also materialise each room (area <= AMAX) and count canonical ones
 *           under the 8 lattice symmetries (free counts), for validation.
 *   MODE 2: Knuth random-probe estimate of the same fixed counts (and of the
 *           number of shapes), PROBES root-to-leaf probes of the shape DFS.
 *           BETA > 1 picks child b with probability ~ BETA^(budget left after b)
 *           times GAMMA^(cells left after b) (importance sampling); weights
 *           stay unbiased.
 *           D: shapes with <= D rows or <= D columns are counted exactly
 *           (the column case by transposition); probes cover the rest.
 *   MODE 3: print PROBES random rooms (shape by probe, geometric weights), not
 *           uniform; for timing samples only.
 *           WCAP: count only rooms with every width and height <= WCAP.
 *   WMIN: count only shapes with W >= WMIN.  CAP5R: count only area <= 5r.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#define WID 9
#define NM 512
static int WMAX, AMAX, MODE, WMIN = 4, CAP5R = 0, WCAP = 1000;
static unsigned char cost[NM][NM], pinch[NM][NM];
static int nb[NM], *bl[NM];            /* candidate successors sorted by cost */
static long long fixedc[24][48], freec[24][48], shapes[24];
static int rows[16], m;

static int popc(int x) { return __builtin_popcount(x); }

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
        bl[a] = malloc(sizeof(int) * NM); nb[a] = 0;
        for (int c = 0; c <= 2 * WID + 2; c++)
            for (int b = 1; b < NM; b++)
                if (cost[a][b] == c && b != a && (a == 0 || (a & b)) && !pinch[a][b]) bl[a][nb[a]++] = b;
    }
}

/* ---- materialised room, for MODE 1 canonical check ---- */
static int cw[WID], ch[16], K;
static uint64_t grid[48];              /* row bitmaps of the stretched room, y up */
static int GWd, GHd;

static int canonical(void) {
    /* key = list of rows (bitmaps) after transform, compare lexicographically with
       (width, height) first.  Return 1 if identity is minimal (ties allowed). */
    static uint64_t T[48];
    for (int t = 1; t < 8; t++) {
        int tw = (t >= 4) ? GHd : GWd, th = (t >= 4) ? GWd : GHd;
        if (tw != GWd || th != GHd) {
            if (tw < GWd || (tw == GWd && th < GHd)) return 0;
            continue;
        }
        for (int y = 0; y < th; y++) T[y] = 0;
        for (int y = 0; y < GHd; y++)
            for (int x = 0; x < GWd; x++)
                if (grid[y] >> x & 1) {
                    int a, b;
                    switch (t) {
                    case 1: a = GWd - 1 - x; b = y; break;
                    case 2: a = x; b = GHd - 1 - y; break;
                    case 3: a = GWd - 1 - x; b = GHd - 1 - y; break;
                    case 4: a = y; b = x; break;
                    case 5: a = GHd - 1 - y; b = x; break;
                    case 6: a = y; b = GWd - 1 - x; break;
                    default: a = GHd - 1 - y; b = GWd - 1 - x; break;
                    }
                    T[b] |= 1ULL << a;
                }
        for (int y = 0; y < th; y++) {
            if (T[y] < grid[y]) return 0;
            if (T[y] > grid[y]) break;
        }
    }
    return 1;
}

static int W_cur, base_cnt, ACAP;

static void emit_room(int area) {
    int y = 0;
    for (int j = 0; j < m; j++) {
        uint64_t r = 0; int x = 0;
        for (int i = 0; i < K; i++) { if (rows[j] >> i & 1) r |= ((1ULL << cw[i]) - 1) << x; x += cw[i]; }
        for (int t = 0; t < ch[j]; t++) grid[y++] = r;
    }
    GHd = y; GWd = 0; for (int i = 0; i < K; i++) GWd += cw[i];
    if (canonical()) freec[W_cur][area]++;
}

static void rec_h(int j, int area) {
    if (j == m) { emit_room(area); return; }
    int c = 0; for (int i = 0; i < K; i++) if (rows[j] >> i & 1) c += cw[i];
    int rest = 0;
    for (int jj = j + 1; jj < m; jj++) for (int i = 0; i < K; i++) if (rows[jj] >> i & 1) rest += cw[i];
    for (int h = 1; area + h * c + rest <= ACAP; h++) { ch[j] = h; rec_h(j + 1, area + h * c); }
}

static int colsz[WID];

static void rec_w(int i, int s) {           /* s = sum_{i'<i} w_i' colsz_i' */
    if (i == K) {
        if (MODE == 1) { rec_h(0, 0); return; }
        long long poly[48]; memset(poly, 0, sizeof poly); poly[0] = 1;
        for (int j = 0; j < m; j++) {
            int c = 0; for (int q = 0; q < K; q++) if (rows[j] >> q & 1) c += cw[q];
            long long np[48]; memset(np, 0, sizeof np);
            for (int a = 0; a <= ACAP; a++) if (poly[a])
                for (int b = a + c, h = 1; b <= ACAP && h <= WCAP; b += c, h++) np[b] += poly[a];
            memcpy(poly, np, sizeof poly);
        }
        for (int a = 0; a <= AMAX; a++) fixedc[W_cur][a] += poly[a];
        return;
    }
    int rest = 0; for (int q = i + 1; q < K; q++) rest += colsz[q];
    for (int w = 1; w <= WCAP && s + w * colsz[i] + rest <= ACAP; w++) { cw[i] = w; rec_w(i + 1, s + w * colsz[i]); }
}

static int simple_room(void) {
    /* complement connected (no hole) and cells connected; flood the complement inside a (K+2) x (m+2) box from the corner */
    int H = m + 2, Wd = K + 2;
    unsigned char g[18][18]; memset(g, 0, sizeof g);
    for (int j = 0; j < m; j++) for (int i = 0; i < K; i++) if (rows[j] >> i & 1) g[j + 1][i + 1] = 1;
    int st[400], sp = 0, seen = 1, tot = 0;
    for (int y = 0; y < H; y++) for (int x = 0; x < Wd; x++) if (!g[y][x]) tot++;
    g[0][0] = 2; st[sp++] = 0;
    while (sp) {
        int v = st[--sp], y = v / Wd, x = v % Wd;
        int d[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        for (int k = 0; k < 4; k++) {
            int yy = y + d[k][1], xx = x + d[k][0];
            if (yy < 0 || yy >= H || xx < 0 || xx >= Wd || g[yy][xx]) continue;
            g[yy][xx] = 2; seen++; st[sp++] = yy * Wd + xx;
        }
    }
    if (seen != tot) return 0;
    /* cells connected */
    int cs = 0, ctot = 0, sy = -1, sx = -1;
    for (int y = 1; y <= m; y++) for (int x = 1; x <= K; x++) if (g[y][x] == 1) { ctot++; if (sy < 0) { sy = y; sx = x; } }
    g[sy][sx] = 3; cs = 1; sp = 0; st[sp++] = sy * Wd + sx;
    while (sp) {
        int v = st[--sp], y = v / Wd, x = v % Wd;
        int d[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        for (int k = 0; k < 4; k++) {
            int yy = y + d[k][1], xx = x + d[k][0];
            if (g[yy][xx] != 1) continue;
            g[yy][xx] = 3; cs++; st[sp++] = yy * Wd + xx;
        }
    }
    return cs == ctot;
}

static void close_shape(int corners, int uni, int cells) {
    int W = corners;
    if (W > WMAX || W < WMIN || !(uni & 1)) return;
    K = 32 - __builtin_clz(uni);
    if (uni != (1 << K) - 1) return;
    for (int i = 0; i + 1 < K; i++) {           /* adjacent columns must differ */
        int same = 1;
        for (int j = 0; j < m; j++) if (((rows[j] >> i) & 1) != ((rows[j] >> (i + 1)) & 1)) { same = 0; break; }
        if (same) return;
    }
    ACAP = AMAX;
    if (CAP5R && 5 * (W - 4) / 2 < ACAP) ACAP = 5 * (W - 4) / 2;
    if (cells > ACAP) return;
    if (!simple_room()) return;
    shapes[W]++;
    for (int i = 0; i < K; i++) { colsz[i] = 0; for (int j = 0; j < m; j++) colsz[i] += rows[j] >> i & 1; }
    W_cur = W; base_cnt = cells;
    if (MODE != 9) rec_w(0, 0);
}

static void dfs(int prev, int corners, int uni, int cells) {
    close_shape(corners + cost[prev][0], uni, cells);
    for (int k = 0; k < nb[prev]; k++) {
        int b = bl[prev][k];
        int c = corners + cost[prev][b];
        if (c + 2 > WMAX) break;
        if (cells + popc(b) > AMAX) continue;
        rows[m++] = b;
        dfs(b, c, uni | b, cells + popc(b));
        m--;
    }
}

/* ---- MODE 2: Knuth estimator ---- */
static double BETA = 1.0, BP[64], GAMMA = 1.0, GP[64];
static int DEXACT = 0;   /* MODE 2: rows <= D and columns <= D handled exactly */
static double ex[24][48];
static uint64_t rng = 88172645463325252ULL;
static uint64_t xr(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static double est[24][48], est2[24], shp[24], shp2[24];

static void probe(void) {
    double wt = 1.0, tot[24] = {0}, ts[24] = {0};
    int prev = 0, corners = 0, uni = 0, cells = 0;
    m = 0;
    for (;;) {
        int cand[NM], nc = 0;
        double pw[NM], tw = 0;
        for (int k = 0; k < nb[prev]; k++) {
            int b = bl[prev][k];
            int c = corners + cost[prev][b];
            if (c + 2 > WMAX) break;
            if (cells + popc(b) > AMAX) continue;
            pw[nc] = BP[WMAX - c] * GP[AMAX - cells - popc(b)]; tw += pw[nc];
            cand[nc++] = b;
        }
        if (!nc) break;
        double u = (double)(xr() >> 11) / 9007199254740992.0 * tw;
        int k = 0; while (k < nc - 1 && u >= pw[k]) { u -= pw[k]; k++; }
        int b = cand[k];
        wt *= tw / pw[k];
        corners += cost[prev][b]; uni |= b; cells += popc(b); rows[m++] = b; prev = b;
        int W = corners + cost[prev][0];
        if (W >= WMIN && W <= WMAX && m > DEXACT) {
            long long save[48], sh = shapes[W];
            memcpy(save, fixedc[W], sizeof save);
            close_shape(W, uni, cells);
            if (32 - __builtin_clz(uni) <= DEXACT) { memcpy(fixedc[W], save, sizeof save); shapes[W] = sh; continue; }
            for (int a = 0; a <= AMAX; a++) { double d = (double)(fixedc[W][a] - save[a]); est[W][a] += wt * d; tot[W] += wt * d; }
            ts[W] += wt * (double)(shapes[W] - sh);
            memcpy(fixedc[W], save, sizeof save); shapes[W] = sh;
        }
    }
    for (int W = 0; W < 24; W++) { est2[W] += tot[W] * tot[W]; shp[W] += ts[W]; shp2[W] += ts[W] * ts[W]; }
}

/* exact part: shapes with m <= D rows (all), plus their transposes when k > D */
static void dfs_shallow(int prev, int corners, int uni, int cells) {
    int W = corners + cost[prev][0];
    if (W >= WMIN && W <= WMAX) {
        long long save[48]; memcpy(save, fixedc[W], sizeof save);
        close_shape(W, uni, cells);
        int k = 32 - __builtin_clz(uni);
        for (int a = 0; a <= AMAX; a++) { double d = (double)(fixedc[W][a] - save[a]); ex[W][a] += (k > DEXACT ? 2 : 1) * d; }
        memcpy(fixedc[W], save, sizeof save);
    }
    if (m == DEXACT) return;
    for (int k = 0; k < nb[prev]; k++) {
        int b = bl[prev][k];
        int c = corners + cost[prev][b];
        if (c + 2 > WMAX) break;
        if (cells + popc(b) > AMAX) continue;
        rows[m++] = b;
        dfs_shallow(b, c, uni | b, cells + popc(b));
        m--;
    }
}

/* ---- MODE 3: emit random rooms (not uniform) with W in [WMIN, WMAX], area in [21, 5r] ---- */
static long long emitted = 0, want = 0;
static void emit_random(int W) {
    int K0 = 32 - __builtin_clz(rows[0] | 0), uni = 0;
    for (int j = 0; j < m; j++) uni |= rows[j];
    (void)K0;
    K = 32 - __builtin_clz(uni);
    int cap = 5 * (W - 4) / 2;
    for (int tries = 0; tries < 200; tries++) {
        int area = 0;
        for (int i = 0; i < K; i++) { cw[i] = 1; while (xr() % 3 == 0) cw[i]++; }
        for (int j = 0; j < m; j++) { ch[j] = 1; while (xr() % 3 == 0) ch[j]++; }
        for (int j = 0; j < m; j++) for (int i = 0; i < K; i++) if (rows[j] >> i & 1) area += cw[i] * ch[j];
        if (area < 21 || area > cap) continue;
        printf("%d", area);
        int y = 0;
        for (int j = 0; j < m; j++) for (int t = 0; t < ch[j]; t++, y++) {
            int x = 0;
            for (int i = 0; i < K; i++) { if (rows[j] >> i & 1) for (int u = 0; u < cw[i]; u++) printf(" %d %d", x + u, y); x += cw[i]; }
        }
        printf("\n"); emitted++; return;
    }
}

static int shape_ok(int W, int uni, int cells) {
    long long sh = shapes[W];
    int saveM = MODE; MODE = 9;              /* close_shape without weight counting */
    close_shape(W, uni, cells);
    MODE = saveM;
    int ok = shapes[W] > sh; shapes[W] = sh; return ok;
}

static void probe_emit(void) {
    int prev = 0, corners = 0, uni = 0, cells = 0;
    m = 0;
    for (;;) {
        int cand[NM], nc = 0; double pw[NM], tw = 0;
        for (int k = 0; k < nb[prev]; k++) {
            int b = bl[prev][k]; int c = corners + cost[prev][b];
            if (c + 2 > WMAX) break;
            if (cells + popc(b) > AMAX) continue;
            pw[nc] = BP[WMAX - c] * GP[AMAX - cells - popc(b)]; tw += pw[nc]; cand[nc++] = b;
        }
        if (!nc) return;
        double u = (double)(xr() >> 11) / 9007199254740992.0 * tw;
        int k = 0; while (k < nc - 1 && u >= pw[k]) { u -= pw[k]; k++; }
        int b = cand[k];
        corners += cost[prev][b]; uni |= b; cells += popc(b); rows[m++] = b; prev = b;
        int W = corners + cost[prev][0];
        if (W >= WMIN && W <= WMAX && shape_ok(W, uni, cells)) { emit_random(W); return; }
    }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: count_rooms WMAX AMAX MODE [WMIN CAP5R PROBES SEED BETA D GAMMA WCAP]\n"); return 1; }
    WMAX = atoi(argv[1]); AMAX = atoi(argv[2]); MODE = atoi(argv[3]);
    if (argc > 4) WMIN = atoi(argv[4]);
    if (argc > 5) CAP5R = atoi(argv[5]);
    prep();
    if (MODE == 3) {
        want = argc > 6 ? atoll(argv[6]) : 1000;
        if (argc > 7) rng ^= (uint64_t)atoll(argv[7]) * 0x9E3779B97F4A7C15ULL;
        if (argc > 8) BETA = atof(argv[8]);
        double gm = argc > 10 ? atof(argv[10]) : 1.0;
        for (int i = 0; i < 64; i++) { BP[i] = pow(BETA, i); GP[i] = pow(gm, i); }
        for (long long it = 0; emitted < want && it < 1000 * want; it++) probe_emit();
        return 0;
    }
    if (MODE == 2) {
        long long P = argc > 6 ? atoll(argv[6]) : 100000;
        if (argc > 8) BETA = atof(argv[8]);
        if (argc > 7) rng ^= (uint64_t)atoll(argv[7]) * 0x9E3779B97F4A7C15ULL;
        if (argc > 9) DEXACT = atoi(argv[9]);
        if (argc > 10) GAMMA = atof(argv[10]);
        if (argc > 11) WCAP = atoi(argv[11]);
        for (int i = 0; i < 64; i++) GP[i] = pow(GAMMA, i);
        for (int i = 0; i < 64; i++) BP[i] = pow(BETA, i);
        if (DEXACT) { m = 0; dfs_shallow(0, 0, 0, 0); }
        for (long long i = 0; i < P; i++) probe();
        for (int W = WMIN; W <= WMAX; W += 2) {
            double s = 0; for (int a = 0; a <= AMAX; a++) s += est[W][a];
            double mean = s / P, var = est2[W] / P - mean * mean;
            double sm = shp[W] / P, sv = shp2[W] / P - sm * sm;
            double e = 0; for (int a = 0; a <= AMAX; a++) e += ex[W][a];
            printf("W %d est_fixed_rooms %.4g (exact part %.4g, sampled part %.4g se %.2g) | sampled shapes %.4g se %.2g\n",
                   W, e + mean, e, mean, sqrt(var / P), sm, sqrt(sv / P));
            for (int a = 1; a <= AMAX; a++) if (est[W][a] > 0 || ex[W][a] > 0)
                printf("  W %d area %d est_fixed %.4g\n", W, a, ex[W][a] + est[W][a] / P);
        }
        return 0;
    }
    for (int k = 0; k < nb[0]; k++) {
        int b = bl[0][k];
        if (cost[0][b] + 2 > WMAX) break;
        m = 0; rows[m++] = b;
        dfs(b, cost[0][b], b, popc(b));
    }
    for (int W = 4; W <= WMAX; W += 2) {
        printf("W %d shapes %lld\n", W, shapes[W]);
        for (int a = 1; a <= AMAX; a++)
            if (fixedc[W][a] || freec[W][a])
                printf("  W %d area %d fixed %lld free %lld\n", W, a, fixedc[W][a], freec[W][a]);
    }
    return 0;
}
