/* check_rooms.c -- prototype of the per-room d44 check.  No ray or direction search.
 *
 * For each room and each mark class (origin parity), compute the canonical class
 * partitions B_b, B_c, B_d (finest G-invariant partition of the n sheets that
 * contains the 2-cycles of g_x), exactly as roomtools.class_congruence, and test
 * whether some pair S != T of interior lattice points of the mark class has all
 * four endpoint lift pairs separated by all three partitions (a_image as in
 * roomtools).  Sheet = cell (one top face per cell).  g_(cx,cy) crosses the vertical
 * edge of parity cx, then the horizontal edge of parity cy (staying put at a wall),
 * matching d4_monodromy.Room.
 *
 * Input (stdin): one room per line, "n x0 y0 x1 y1 ...".
 * Output: one line per positive (room, mark class, pair); a summary on stderr.
 * Flags: argv[1] = "v" prints per-room partition block counts and separation.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXC 128
#define G 48                                /* coordinate box */
static int n, cx_[MAXC], cy_[MAXC], id[G][G];
static int verbose;
static long long rooms = 0, scope3 = 0, eligible_cls = 0, nontriv[4], all3 = 0, positives = 0;

static int cell(int x, int y) { return (x >= 0 && y >= 0 && x < G && y < G) ? id[x][y] : -1; }

/* g_(px,py) in coordinates shifted so the origin has parity (ox, oy) */
static void gen(int px, int py, int ox, int oy, int *g) {
    for (int k = 0; k < n; k++) {
        int x = cx_[k], y = cy_[k];
        int ex = ((x - ox) & 1) == px ? x - 1 : x + 1;   /* cell across the vertical edge */
        int k1 = cell(ex, y); if (k1 < 0) k1 = k;
        int x1 = cx_[k1], y1 = cy_[k1];
        int ey = ((y1 - oy) & 1) == py ? y1 - 1 : y1 + 1;
        int k2 = cell(x1, ey); if (k2 < 0) k2 = k1;
        g[k] = k2;
    }
}

static int par[MAXC];
static int find(int a) { while (par[a] != a) { par[a] = par[par[a]]; a = par[a]; } return a; }

/* closure of the seeds under the 8 permutations gs[0..7]; returns number of blocks */
static int closure(int gs[8][MAXC], int *seedg) {
    int qa[MAXC * MAXC], qb[MAXC * MAXC], qn = 0;
    for (int i = 0; i < n; i++) par[i] = i;
    for (int i = 0; i < n; i++) {
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
    int nb = 0; for (int i = 0; i < n; i++) if (find(i) == i) nb++;
    return nb;
}

static void inv(const int *g, int *h) { for (int i = 0; i < n; i++) h[g[i]] = i; }

int main(int argc, char **argv) {
    verbose = argc > 1 && argv[1][0] == 'v';
    static int gs[8][MAXC];
    clock_t t0 = clock();
    while (scanf("%d", &n) == 1) {
        int mnx = 1 << 20, mny = 1 << 20;
        for (int k = 0; k < n; k++) { if (scanf("%d %d", &cx_[k], &cy_[k]) != 2) return 1; }
        for (int k = 0; k < n; k++) { if (cx_[k] < mnx) mnx = cx_[k]; if (cy_[k] < mny) mny = cy_[k]; }
        memset(id, -1, sizeof id);
        int sx = 2 - mnx, sy = 2 - mny;          /* even shift keeps parity classes */
        sx += sx & 1; sy += sy & 1;
        if (n > MAXC) return 2;
        for (int k = 0; k < n; k++) { cx_[k] += sx; cy_[k] += sy; if (cx_[k] >= G || cy_[k] >= G) return 3; id[cx_[k]][cy_[k]] = k; }
        rooms++;
        /* corner classes (absolute parity), lattice point census */
        int ccls = 0;
        int ipx[MAXC * 2], ipy[MAXC * 2], ni = 0;
        for (int x = 1; x < G - 1; x++) for (int y = 1; y < G - 1; y++) {
            int c = (cell(x - 1, y - 1) >= 0) + (cell(x, y - 1) >= 0) + (cell(x - 1, y) >= 0) + (cell(x, y) >= 0);
            if (c == 1 || c == 3) ccls |= 1 << ((x & 1) * 2 + (y & 1));
            if (c == 4) { ipx[ni] = x; ipy[ni] = y; ni++; }
        }
        int nc = __builtin_popcount(ccls);
        if (nc >= 3) scope3++;
        for (int o = 0; o < 4; o++) {
            int ox = o >> 1, oy = o & 1;
            int S[MAXC], ns = 0;
            for (int i = 0; i < ni; i++) if ((ipx[i] & 1) == ox && (ipy[i] & 1) == oy) S[ns++] = i;
            if (ns < 2) continue;
            if (ns > 64) return 4;
            eligible_cls++;
            /* gs: g_A, g_b, g_c, g_d and inverses; classes b=(1,0), c=(1,1), d=(0,1) */
            gen(0, 0, ox, oy, gs[0]); gen(1, 0, ox, oy, gs[1]); gen(1, 1, ox, oy, gs[2]); gen(0, 1, ox, oy, gs[3]);
            for (int t = 0; t < 4; t++) inv(gs[t], gs[4 + t]);
            /* lift representatives of each mark point: cell SW and a cell outside its g_A orbit */
            int L[MAXC][2];
            for (int s = 0; s < ns; s++) {
                int x = ipx[S[s]], y = ipy[S[s]];
                int sw = cell(x - 1, y - 1), q[4] = {sw, cell(x, y - 1), cell(x - 1, y), cell(x, y)};
                int p = gs[0][sw], other = -1;
                for (int k = 0; k < 4; k++) if (q[k] != sw && q[k] != p) { other = q[k]; break; }
                L[s][0] = sw; L[s][1] = other;
            }
            unsigned long long ok[MAXC]; for (int s = 0; s < ns; s++) ok[s] = ~0ULL;
            int alive = 1, nbk[4] = {0};
            for (int x = 1; x <= 3 && alive; x++) {
                int nb = closure(gs, gs[x]); nbk[x] = nb;
                if (nb == 1) { alive = 0; break; }
                nontriv[x]++;
                /* a-image: cycle of induced g_A on blocks */
                int blk[MAXC], img[MAXC], cyc[MAXC];
                for (int i = 0; i < n; i++) blk[i] = find(i);
                for (int i = 0; i < n; i++) img[blk[i]] = blk[gs[0][i]], cyc[i] = -1;
                for (int i = 0; i < n; i++) if (blk[i] == i && cyc[i] < 0) {
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
            if (verbose) printf("room %lld origin parity (%d,%d) marks %d blocks b c d = %d %d %d corner classes %d\n",
                                rooms, ox, oy, ns, nbk[1], nbk[2], nbk[3], nc);
            if (!alive) continue;
            all3++;
            for (int s = 0; s < ns; s++) for (int u = s + 1; u < ns; u++) if (ok[s] >> u & 1) {
                positives++;
                printf("POSITIVE room %lld n %d corner_classes %d S (%d,%d) T (%d,%d)\n", rooms, n, nc,
                       ipx[S[s]] - sx, ipy[S[s]] - sy, ipx[S[u]] - sx, ipy[S[u]] - sy);
            }
        }
    }
    double sec = (double)(clock() - t0) / CLOCKS_PER_SEC;
    fprintf(stderr, "rooms %lld scope>=3classes %lld eligible(room,class) %lld nontrivial B_b %lld B_c %lld B_d %lld "
            "all-three-separating %lld positive pairs %lld cpu %.3f s (%.2f us/room)\n",
            rooms, scope3, eligible_cls, nontriv[1], nontriv[2], nontriv[3], all3, positives, sec, 1e6 * sec / (rooms ? rooms : 1));
    return 0;
}
