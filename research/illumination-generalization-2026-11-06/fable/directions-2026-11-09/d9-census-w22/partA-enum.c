/* partA-enum.c -- copy of enum_rooms.c with an ALL flag (argv[7] = "all"):
 * write every kept room, not only eligible ones.
 *
 * enum_rooms.c -- exhaustive enumeration of strictly simple polyomino rooms.
 *
 * Redelmeier enumeration of fixed polyominoes with at most NMAX cells.  For
 * every polyomino:
 *   - per lattice point, a 4-bit mask of the surrounding cells;
 *   - reject pinch points (exactly two diagonal cells);
 *   - reject holes: with no pinch point the closed union is a surface with
 *     boundary, and it is a disc iff V - E + F == 1;
 *   - W = number of corners (lattice points with 1 or 3 cells); keep W <= WMAX;
 *   - keep one representative per free polyomino: the fixed polyomino whose
 *     normalised key is minimal over the 8 lattice symmetries.
 * Counts per (area, W) are written for all kept rooms.  Rooms with at least
 * two interior lattice points of one parity class ("eligible") are written,
 * normalised (min x = min y = 0), one per line: "area W x0 y0 x1 y1 ...".
 *
 * Parallel split: nodes of size SPLIT are dealt round-robin to NJ jobs; nodes
 * of size < SPLIT are processed by job 0 only.
 *
 * usage: enum_rooms NMAX WMAX NJ J outfile countsfile   (outfile "-" = stdout)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 24
#define SPLIT 11

static int NMAX, WMAX, NJ, J, ALL;
static int GW;                        /* grid width for cells */
static unsigned char *seen, *occ;     /* cell grid */
static unsigned char *pm;             /* lattice point masks */
static int PW;                        /* lattice grid width */
static int px[MAXN + 1], py[MAXN + 1];
static long long cnt_split = 0;
static long long rooms[MAXN + 1][4 * MAXN + 8];
static long long elig[MAXN + 1][4 * MAXN + 8];
static long long fixed_nodes = 0;
static long long fixed_by_size[MAXN + 1];
static FILE *out;

static inline int cid(int x, int y) { return (y + 1) * GW + (x + NMAX + 1); }
static inline int pid(int x, int y) { return (y + 1) * PW + (x + NMAX + 1); }

typedef struct { int w, h; uint32_t row[MAXN + 1]; } Key;

static void make_key(int k, int t, Key *K) {
    int ax[MAXN + 1], ay[MAXN + 1];
    int mnx = 1 << 20, mny = 1 << 20, mxx = -(1 << 20), mxy = -(1 << 20);
    for (int i = 0; i < k; i++) {
        int x = px[i], y = py[i], a, b;
        switch (t) {
        case 0: a = x;  b = y;  break;
        case 1: a = -x; b = y;  break;
        case 2: a = x;  b = -y; break;
        case 3: a = -x; b = -y; break;
        case 4: a = y;  b = x;  break;
        case 5: a = -y; b = x;  break;
        case 6: a = y;  b = -x; break;
        default: a = -y; b = -x; break;
        }
        ax[i] = a; ay[i] = b;
        if (a < mnx) mnx = a; if (a > mxx) mxx = a;
        if (b < mny) mny = b; if (b > mxy) mxy = b;
    }
    K->w = mxx - mnx + 1; K->h = mxy - mny + 1;
    memset(K->row, 0, sizeof(uint32_t) * (K->h));
    for (int i = 0; i < k; i++) K->row[ay[i] - mny] |= (uint32_t)1 << (ax[i] - mnx);
}

static int key_cmp(const Key *A, const Key *B) {
    if (A->w != B->w) return A->w < B->w ? -1 : 1;
    if (A->h != B->h) return A->h < B->h ? -1 : 1;
    for (int r = 0; r < A->h; r++)
        if (A->row[r] != B->row[r]) return A->row[r] < B->row[r] ? -1 : 1;
    return 0;
}

static void process(int k) {
    fixed_nodes++; fixed_by_size[k]++;
    /* lattice point masks */
    for (int i = 0; i < k; i++) {
        int x = px[i], y = py[i];
        pm[pid(x, y)] |= 8; pm[pid(x + 1, y)] |= 4;
        pm[pid(x, y + 1)] |= 2; pm[pid(x + 1, y + 1)] |= 1;
    }
    int V = 0, W = 0, pinch = 0, icls[4] = {0, 0, 0, 0};
    for (int i = 0; i < k; i++) {
        for (int d = 0; d < 4; d++) {
            int X = px[i] + (d & 1), Y = py[i] + (d >> 1);
            int p = pid(X, Y);
            int m = pm[p];
            if (!m) continue;
            pm[p] = 0;
            V++;
            int c = __builtin_popcount(m);
            if (c == 1 || c == 3) W++;
            else if (c == 4) icls[((X & 1) << 1) | (Y & 1)]++;
            else if (m == 9 || m == 6) pinch = 1;
        }
    }
    if (pinch || W > WMAX) return;
    int adj = 0;
    for (int i = 0; i < k; i++) {
        if (occ[cid(px[i] + 1, py[i])]) adj++;
        if (occ[cid(px[i], py[i] + 1)]) adj++;
    }
    int E = 4 * k - adj;
    if (V - E + k != 1) return;          /* hole */
    Key K0, K;
    make_key(k, 0, &K0);
    for (int t = 1; t < 8; t++) {
        make_key(k, t, &K);
        if (key_cmp(&K, &K0) < 0) return;  /* not the canonical representative */
    }
    rooms[k][W]++;
    int e = 0;
    for (int c = 0; c < 4; c++) if (icls[c] >= 2) e = 1;
    if (e) elig[k][W]++;
    if (!e && !ALL) return;
    /* write normalised cells from the canonical key */
    fprintf(out, "%d %d", k, W);
    for (int r = 0; r < K0.h; r++)
        for (int c = 0; c < K0.w; c++)
            if (K0.row[r] >> c & 1) fprintf(out, " %d %d", c, r);
    fputc('\n', out);
}

static int allowed(int x, int y) {
    if (y < 0 || y >= NMAX) return 0;
    if (y == 0 && x < 0) return 0;
    if (x <= -NMAX || x >= NMAX) return 0;
    return 1;
}

static void rec(int n, const int *untried, int nu) {
    int buf[4 * MAXN + 8];
    int U[4 * MAXN + 8];
    memcpy(U, untried, sizeof(int) * nu);
    while (nu > 0) {
        int c = U[--nu];
        int x = c % GW - NMAX - 1, y = c / GW - 1;
        int s = n + 1;
        if (s == SPLIT) {
            long long me = cnt_split++;
            if (me % NJ != J) continue;
        }
        px[n] = x; py[n] = y; occ[c] = 1;
        if (s >= SPLIT || J == 0) process(s);
        if (s < NMAX) {
            int m = nu, added = 0;
            memcpy(buf, U, sizeof(int) * nu);
            int nb[4][2] = {{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}};
            int addl[4];
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

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: enum_rooms NMAX WMAX NJ J outfile countsfile\n"); return 1; }
    NMAX = atoi(argv[1]); WMAX = atoi(argv[2]); NJ = atoi(argv[3]); J = atoi(argv[4]);
    ALL = argc > 7 && !strcmp(argv[7], "all");
    if (NMAX > MAXN || NMAX < SPLIT) { fprintf(stderr, "NMAX out of range\n"); return 1; }
    out = strcmp(argv[5], "-") ? fopen(argv[5], "w") : stdout;
    GW = 2 * NMAX + 4; PW = 2 * NMAX + 6;
    seen = calloc((size_t)GW * (NMAX + 4), 1);
    occ = calloc((size_t)GW * (NMAX + 4), 1);
    pm = calloc((size_t)PW * (NMAX + 6), 1);
    int start = cid(0, 0);
    seen[start] = 1;
    int U[1] = {start};
    rec(0, U, 1);
    FILE *cf = fopen(argv[6], "w");
    fprintf(cf, "# fixed_nodes_processed %lld\n", fixed_nodes);
    for (int k = 1; k <= NMAX; k++) fprintf(cf, "# fixed area %d %lld\n", k, fixed_by_size[k]);
    for (int k = 1; k <= NMAX; k++)
        for (int w = 4; w <= WMAX; w += 2)
            if (rooms[k][w])
                fprintf(cf, "# count area %d W %d rooms %lld eligible %lld\n", k, w, rooms[k][w], elig[k][w]);
    fprintf(cf, "# DONE\n");
    fclose(cf);
    fclose(out);
    return 0;
}
