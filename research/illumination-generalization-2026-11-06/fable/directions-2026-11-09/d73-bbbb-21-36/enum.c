/* enum.c -- d73: all strictly simple orthogonal lattice rooms with r <= RMAX reflex
 * corners and area <= AMAX, via skeleton + dimensions.
 *
 * Every room P has a unique skeleton: X = distinct vertex x-coordinates x_0<..<x_C,
 * Y likewise (y_0<..<y_R). The grid rectangles [x_i,x_i+1]x[y_j,y_j+1] are each in or
 * out of P, giving a C x R 0/1 matrix S with every row/column nonempty and adjacent
 * columns (rows) different. Conversely every such S that is a strictly simple room with
 * r <= RMAX, together with widths w_i >= 1 and heights h_j >= 1, gives a room whose
 * skeleton is S. So rooms <-> (S, w, h) bijectively.
 *
 * Skeletons are enumerated column by column (column = bitmask of R rows). The corners
 * on the vertical line between two columns depend only on those two columns, so the
 * corner counts are exact incrementally: prune at reflex > RMAX, convex > RMAX+4,
 * pinch, or (corners so far + 2 for the closing line) > 2*RMAX+4.
 * At completion: rows nonempty, adjacent rows differ, connected, convex-reflex == 4
 * (with connectivity and no pinch, that means no hole).
 *
 * For each (S,w,h) with area <= AMAX: expand, classify parity classes (relative to the
 * room's own lower-left corner at (0,0); "every class regular" is translation- and
 * symmetry-invariant), and keep one representative per D4 orbit (lexicographically
 * minimal triple key).
 *
 * usage: enum RMAX AMAX AOUTMIN outfile  -> counts on stdout; BBBB rooms with area
 * in [AOUTMIN, AMAX] and >= 2 interior points written as "area W x0 y0 x1 y1 ..."
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int RMAX, AMAX, AOUT;
static FILE *out;
static int R;                 /* rows of the skeleton */
static int cols[16], C;       /* column masks */
static int cv[512][512], rf[512][512], pn[512][512];
static long long nskel = 0, nodes = 0;
static long long cnt_all[64][64], cnt_q2[64], cnt_b[64], cnt_b2[64], cnt_fixed[64];
static long long cnt_bpts[64];

static void line_counts(int a, int b, int *c, int *r, int *p) {
    *c = *r = *p = 0;
    for (int j = 0; j <= R; j++) {
        int ll = (a >> (j - 1)) & (j > 0), ul = (a >> j) & (j < R) & 1;
        int lr = (b >> (j - 1)) & (j > 0), ur = (b >> j) & (j < R) & 1;
        ll &= 1; lr &= 1;
        int k = ll + ul + lr + ur;
        if (k == 1) (*c)++;
        else if (k == 3) (*r)++;
        else if (k == 2 && ll == ur) (*p)++;
    }
}

/* ---- room expansion and classification ---- */
static int w[16], h[16];
static int G[40][40];         /* cells of expanded room */
static int RW, RH;

static int key_cmp_ident_vs(int t) {
    /* build transformed triple and compare against identity; return <0 if transformed smaller */
    int Ct, Rt, ct[16], wt[16], ht[16];
    int swap = t >> 2, fx = t & 1, fy = (t >> 1) & 1;
    /* cell (i,j) -> (i',j'): first optional transpose, then flips */
    if (!swap) { Ct = C; Rt = R; } else { Ct = R; Rt = C; }
    for (int i = 0; i < Ct; i++) ct[i] = 0;
    for (int i = 0; i < C; i++)
        for (int j = 0; j < R; j++)
            if ((cols[i] >> j) & 1) {
                int a = swap ? j : i, b = swap ? i : j;
                if (fx) a = Ct - 1 - a;
                if (fy) b = Rt - 1 - b;
                ct[a] |= 1 << b;
            }
    for (int i = 0; i < Ct; i++) { int s = swap ? h[i] : w[i]; wt[fx ? Ct - 1 - i : i] = s; }
    for (int j = 0; j < Rt; j++) { int s = swap ? w[j] : h[j]; ht[fy ? Rt - 1 - j : j] = s; }
    if (Ct != C) return Ct < C ? -1 : 1;
    for (int i = 0; i < C; i++) if (ct[i] != cols[i]) return ct[i] < cols[i] ? -1 : 1;
    for (int i = 0; i < C; i++) if (wt[i] != w[i]) return wt[i] < w[i] ? -1 : 1;
    for (int j = 0; j < R; j++) if (ht[j] != h[j]) return ht[j] < h[j] ? -1 : 1;
    return 0;
}

static int has(int x, int y) { return x >= 0 && y >= 0 && x < RW && y < RH && G[x][y]; }

static void room(int area, int refl) {
    int Wc = 2 * refl + 4;
    cnt_fixed[area]++;
    for (int t = 1; t < 8; t++) if (key_cmp_ident_vs(t) < 0) return;
    cnt_all[area][Wc]++;
    /* expand */
    RW = 0; for (int i = 0; i < C; i++) RW += w[i];
    RH = 0; for (int j = 0; j < R; j++) RH += h[j];
    int x = 0;
    for (int i = 0; i < C; i++) {
        for (int dx = 0; dx < w[i]; dx++) {
            int y = 0;
            for (int j = 0; j < R; j++) {
                int on = (cols[i] >> j) & 1;
                for (int dy = 0; dy < h[j]; dy++) G[x + dx][y + dy] = on;
                y += h[j];
            }
        }
        x += w[i];
    }
    int reg[4] = {0, 0, 0, 0}, nint = 0;
    for (int X = 0; X <= RW; X++)
        for (int Y = 0; Y <= RH; Y++) {
            int ll = has(X - 1, Y - 1), lr = has(X, Y - 1), ul = has(X - 1, Y), ur = has(X, Y);
            int k = ll + lr + ul + ur;
            if (k == 4) { nint++; reg[(X & 1) * 2 + (Y & 1)] = 1; }
            else if (k == 2) reg[(X & 1) * 2 + (Y & 1)] = 1;   /* no pinch, so k==2 is smooth */
        }
    int bbbb = reg[0] && reg[1] && reg[2] && reg[3];
    if (!bbbb) { if (nint >= 2) cnt_q2[area]++; }
    else {
        cnt_b[area]++;
        if (nint >= 2) {
            cnt_b2[area]++;
            if (area >= AOUT && out) {
                fprintf(out, "%d %d", area, Wc);
                for (int X = 0; X < RW; X++) for (int Y = 0; Y < RH; Y++) if (G[X][Y]) fprintf(out, " %d %d", X, Y);
                fputc('\n', out);
            }
        }
    }
    for (int X = 0; X < RW; X++) for (int Y = 0; Y < RH; Y++) G[X][Y] = 0;
}

static int csum[16];
static void rec_w(int i, int area, int refl) {
    if (i == C) { room(area, refl); return; }
    int rest = 0; for (int k = i + 1; k < C; k++) rest += csum[k];
    for (w[i] = 1; area + w[i] * csum[i] + rest <= AMAX; w[i]++) rec_w(i + 1, area + w[i] * csum[i], refl);
}
static int minA_h(void) { int s = 0; for (int i = 0; i < C; i++) s += __builtin_popcount(cols[i]); return s; }
static void rec_h(int j, int refl, int cellsrest) {
    if (j == R) {
        for (int i = 0; i < C; i++) { csum[i] = 0; for (int k = 0; k < R; k++) if ((cols[i] >> k) & 1) csum[i] += h[k]; }
        rec_w(0, 0, refl);
        return;
    }
    /* current minimal area with h[0..j-1] fixed, rest = 1 */
    for (h[j] = 1;; h[j]++) {
        int a = 0;
        for (int i = 0; i < C; i++) for (int k = 0; k < R; k++) if ((cols[i] >> k) & 1) a += (k <= j) ? h[k] : 1;
        if (a > AMAX) break;
        rec_h(j + 1, refl, cellsrest);
    }
}

static int connected(void) {
    int full = 0, seen[16] = {0};
    int st[256], sp = 0;
    int i0 = 0, j0 = __builtin_ctz(cols[0]);
    seen[i0] |= 1 << j0; st[sp++] = i0 * 16 + j0;
    while (sp) {
        int v = st[--sp], i = v / 16, j = v % 16; full++;
        int ni[4] = {i - 1, i + 1, i, i}, nj[4] = {j, j, j - 1, j + 1};
        for (int d = 0; d < 4; d++) {
            int a = ni[d], b = nj[d];
            if (a < 0 || a >= C || b < 0 || b >= R) continue;
            if (!((cols[a] >> b) & 1) || ((seen[a] >> b) & 1)) continue;
            seen[a] |= 1 << b; st[sp++] = a * 16 + b;
        }
    }
    int tot = 0; for (int i = 0; i < C; i++) tot += __builtin_popcount(cols[i]);
    return full == tot;
}

static void skeleton(int conv, int refl) {
    /* rows nonempty and adjacent rows differ */
    int all = 0; for (int i = 0; i < C; i++) all |= cols[i];
    if (all != (1 << R) - 1) return;
    for (int j = 0; j + 1 < R; j++) {
        int same = 1;
        for (int i = 0; i < C; i++) if (((cols[i] >> j) & 1) != ((cols[i] >> (j + 1)) & 1)) { same = 0; break; }
        if (same) return;
    }
    if (conv - refl != 4) return;
    if (!connected()) return;
    nskel++;
    rec_h(0, refl, 0);
}

static void dfs(int conv, int refl, int cells) {
    nodes++;
    int a = C ? cols[C - 1] : 0;
    /* try closing */
    if (C > 0) {
        int c2 = conv + cv[a][0], r2 = refl + rf[a][0];
        if (!pn[a][0] && r2 <= RMAX && c2 <= RMAX + 4) skeleton(c2, r2);
    }
    if (C >= 15) return;
    for (int b = 1; b < (1 << R); b++) {
        if (b == a) continue;
        if (pn[a][b]) continue;
        int c2 = conv + cv[a][b], r2 = refl + rf[a][b];
        if (r2 > RMAX || c2 > RMAX + 4 || c2 + r2 + 2 > 2 * RMAX + 4) continue;
        int nc = cells + __builtin_popcount(b);
        if (nc > AMAX) continue;
        cols[C++] = b;
        dfs(c2, r2, nc);
        C--;
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: enum RMAX AMAX AOUTMIN outfile|-\n"); return 1; }
    RMAX = atoi(argv[1]); AMAX = atoi(argv[2]); AOUT = atoi(argv[3]);
    out = strcmp(argv[4], "-") ? fopen(argv[4], "w") : NULL;
    for (R = 1; R <= RMAX + 1; R++) {
        for (int a = 0; a < (1 << R); a++)
            for (int b = 0; b < (1 << R); b++) line_counts(a, b, &cv[a][b], &rf[a][b], &pn[a][b]);
        C = 0;
        dfs(0, 0, 0);
        fprintf(stderr, "R=%d nodes=%lld skeletons=%lld\n", R, nodes, nskel);
    }
    printf("# RMAX %d AMAX %d skeletons %lld nodes %lld\n", RMAX, AMAX, nskel, nodes);
    for (int A = 1; A <= AMAX; A++) {
        long long tot = 0;
        for (int W = 0; W < 64; W++) if (cnt_all[A][W]) { printf("AW %d %d %lld\n", A, W, cnt_all[A][W]); tot += cnt_all[A][W]; }
        printf("A %d fixed %lld free %lld q_elig %lld bbbb %lld bbbb_elig %lld\n", A, cnt_fixed[A], tot, cnt_q2[A], cnt_b[A], cnt_b2[A]);
    }
    if (out) fclose(out);
    return 0;
}
