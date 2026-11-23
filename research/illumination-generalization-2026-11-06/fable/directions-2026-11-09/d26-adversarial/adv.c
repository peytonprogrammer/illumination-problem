/* adv.c -- adversarial search for dark pairs in orthogonal lattice rooms, W <= WMAX.
 * Exact integer tracer in the 4-fold unfolding (square = (cell, sheet), h = right, v = up,
 * label = room point at the bottom-left corner). From each copy of an interior point S, each
 * primitive direction (p,q) is followed lattice step by lattice step until a corner.
 * ml[S][T] = shortest corner-free unfolded segment S->T; cnt[S][T] = number of such segments
 * with length <= L0*diam. diam = cell-graph (L1) diameter + 1.
 * usage: adv check L0 LCAP [v] < rooms        (room line: "A x0 y0 x1 y1 ...")
 *        ADV_OBJ=1 makes the sa objective (and every reported "rho") L/A instead of L/diam,
 *        where L is the longest shortest-path over same-class pairs.
 *        adv sa SEED NRESTART NIT AMIN AMAX BOX T0 L0 LCAP [seedfile]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>
#define G 80
#define OFF 6
typedef struct { unsigned char c[G][G]; } Room;
static uint64_t rs = 88172645463325252ULL;
static inline uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline int ri(int n) { return (int)(rnd() % (uint64_t)n); }
static double ru(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int BOX = 64, AMIN = 21, AMAX = 400, WMAX = 20;
static int lw, lh, lW;
static const int SX[4] = {1, -1, 1, -1}, SY[4] = {1, 1, -1, -1};

static int validate(Room *r) {
    int x0 = G, x1 = -1, y0 = G, y1 = -1, A = 0;
    for (int x = 0; x < G; x++) for (int y = 0; y < G; y++) if (r->c[x][y]) {
        A++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    if (!A) return 0;
    int w = x1 - x0 + 1, h = y1 - y0 + 1;
    if (w > BOX || h > BOX || A < AMIN || A > AMAX) return 0;
    if (x0 != OFF || y0 != OFF) {
        Room t; memset(&t, 0, sizeof t);
        for (int x = 0; x < w; x++) for (int y = 0; y < h; y++) t.c[OFF + x][OFF + y] = r->c[x0 + x][y0 + y];
        *r = t;
    }
    int W = 0;
    for (int X = OFF; X <= OFF + w; X++) for (int Y = OFF; Y <= OFF + h; Y++) {
        int a = r->c[X - 1][Y - 1], b = r->c[X][Y - 1], c = r->c[X - 1][Y], d = r->c[X][Y], k = a + b + c + d;
        if (k == 2 && a == d) return 0;
        if (k == 1 || k == 3) W++;
    }
    if (W > WMAX) return 0;
    static int qx[G * G], qy[G * G]; static unsigned char seen[G][G];
    static const int DX[4] = {1, -1, 0, 0}, DY[4] = {0, 0, 1, -1};
    for (int pass = 0; pass < 2; pass++) {      /* pass 0: room connected; pass 1: complement connected */
        memset(seen, 0, sizeof seen);
        int want = pass ? (w + 2) * (h + 2) - A : A, len = 0, k = 0;
        if (pass) { qx[0] = OFF - 1; qy[0] = OFF - 1; }
        else { for (int y = OFF; y < OFF + h; y++) if (r->c[OFF][y]) { qx[0] = OFF; qy[0] = y; break; } }
        seen[qx[0]][qy[0]] = 1; len = 1;
        while (k < len) {
            int x = qx[k], y = qy[k]; k++;
            for (int d = 0; d < 4; d++) {
                int nx = x + DX[d], ny = y + DY[d];
                if (nx < OFF - 1 || ny < OFF - 1 || nx > OFF + w || ny > OFF + h) continue;
                if (seen[nx][ny] || r->c[nx][ny] == pass) continue;
                seen[nx][ny] = 1; qx[len] = nx; qy[len] = ny; len++;
            }
        }
        if (len != want) return 0;
    }
    lw = w; lh = h; lW = W;
    return A;
}

typedef struct { double rho; int npmax, mincnt, nmin, P, A, diam, unlit, npairs, sx, sy, tx, ty, W; } Res;
static int cid[G][G], pid[G][G];
static int *Hh, *Vv, *lab, *cxs, *cys, *px, *py, *bq, *bd;
static float *ml; static unsigned short *cnt; static unsigned char *act;
typedef struct { int p, q; double n; } Dir;
static Dir *dirs; static int ndirs; static double RMAX = 300;
static int gcd_(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int dcmp(const void *a, const void *b) { double x = ((const Dir *)a)->n - ((const Dir *)b)->n; return x < 0 ? -1 : x > 0; }
static void init(void) {
    int n = AMAX + 8;
    Hh = malloc(4 * n * sizeof(int)); Vv = malloc(4 * n * sizeof(int)); lab = malloc(4 * n * sizeof(int));
    cxs = malloc(n * sizeof(int)); cys = malloc(n * sizeof(int)); px = malloc(n * sizeof(int)); py = malloc(n * sizeof(int));
    bq = malloc(n * sizeof(int)); bd = malloc(n * sizeof(int)); act = malloc(n);
    ml = malloc((size_t)n * n * sizeof(float)); cnt = malloc((size_t)n * n * sizeof(short));
    int R = (int)RMAX; dirs = malloc(sizeof(Dir) * (size_t)(R + 1) * (R + 1)); ndirs = 0;
    for (int p = 0; p <= R; p++) for (int q = 0; q <= R; q++)
        if (gcd_(p, q) == 1 && p * p + q * q <= R * R) { dirs[ndirs].p = p; dirs[ndirs].q = q; dirs[ndirs].n = sqrt(p * p + q * q); ndirs++; }
    qsort(dirs, ndirs, sizeof(Dir), dcmp);
}
static inline int stepdir(int a, int p, int q) {
    if (q == 0) return Hh[a];
    if (p == 0) return Vv[a];
    int i = 1, j = 1, ex = q, ey = p;
    while (i < p || j < q) { if (ex < ey) { a = Hh[a]; i++; ex += q; } else { a = Vv[a]; j++; ey += p; } }
    return Vv[Hh[a]];
}
static int bfs(int A, int s) {              /* cell BFS, returns farthest cell, depth in bd */
    for (int i = 0; i < A; i++) bd[i] = -1;
    int len = 1, k = 0; bq[0] = s; bd[s] = 0;
    static const int DX[4] = {1, -1, 0, 0}, DY[4] = {0, 0, 1, -1};
    while (k < len) { int c = bq[k++]; for (int d = 0; d < 4; d++) { int o = cid[cxs[c] + DX[d]][cys[c] + DY[d]]; if (o >= 0 && bd[o] < 0) { bd[o] = bd[c] + 1; bq[len++] = o; } } }
    return bq[len - 1];
}
static void evaluate(const Room *r, double L0, double LCAP, Res *R) {
    int A = 0, P = 0;
    memset(cid, -1, sizeof cid); memset(pid, -1, sizeof pid);
    for (int x = OFF; x < OFF + lw; x++) for (int y = OFF; y < OFF + lh; y++) if (r->c[x][y]) { cxs[A] = x; cys[A] = y; cid[x][y] = A++; }
    for (int X = OFF; X <= OFF + lw; X++) for (int Y = OFF; Y <= OFF + lh; Y++)
        if (r->c[X - 1][Y - 1] + r->c[X][Y - 1] + r->c[X - 1][Y] + r->c[X][Y] == 4) { px[P] = X; py[P] = Y; pid[X][Y] = P++; }
    for (int c = 0; c < A; c++) for (int s = 0; s < 4; s++) {
        int q = 4 * c + s, i = cxs[c], j = cys[c];
        Hh[q] = r->c[i + SX[s]][j] ? 4 * cid[i + SX[s]][j] + s : 4 * c + (s ^ 1);
        Vv[q] = r->c[i][j + SY[s]] ? 4 * cid[i][j + SY[s]] + s : 4 * c + (s ^ 2);
        int X = i + (SX[s] < 0), Y = j + (SY[s] < 0);
        int k = r->c[X - 1][Y - 1] + r->c[X][Y - 1] + r->c[X - 1][Y] + r->c[X][Y];
        lab[q] = (k == 1 || k == 3) ? -1 : (k == 4 ? pid[X][Y] : -2);
    }
    int e = bfs(A, 0); e = bfs(A, e); int diam = bd[e] + 1;
    memset(R, 0, sizeof *R); R->A = A; R->P = P; R->diam = diam; R->W = lW;
    for (size_t i = 0; i < (size_t)P * P; i++) { ml[i] = 1e30f; cnt[i] = 0; }
    for (int i = 0; i < P; i++) act[i] = 1;
    double L = L0 * diam;
    for (int stage = 0;; stage++) {
        if (L > 2 * RMAX) L = 2 * RMAX;
        for (int S = 0; S < P; S++) {
            if (!act[S]) continue;
            float *row = ml + (size_t)S * P; unsigned short *crow = cnt + (size_t)S * P;
            for (int s = 0; s < 4; s++) {
                int a = 4 * cid[px[S] - (SX[s] < 0)][py[S] - (SY[s] < 0)] + s;
                for (int di = 0; di < ndirs && 2 * dirs[di].n <= L; di++) {
                    int p = dirs[di].p, q = dirs[di].q;
                    if ((q == 0 && (s & 2)) || (p == 0 && (s & 1))) continue;
                    int K = (int)(L / dirs[di].n), cur = a; float n2 = (float)(p * p + q * q);
                    for (int m = 1; m <= K; m++) {
                        cur = stepdir(cur, p, q);
                        int l = lab[cur];
                        if (l == -1) break;
                        if (!(m & 1) && l >= 0 && l != S) { float v = (float)m * m * n2; if (v < row[l]) row[l] = v; if (!stage && crow[l] < 65535) crow[l]++; }
                        if (cur == a) break;
                    }
                }
            }
        }
        int un = 0;
        for (int S = 0; S < P; S++) {
            act[S] = 0;
            for (int T = S + 1; T < P; T++) if (!((px[S] ^ px[T]) & 1) && !((py[S] ^ py[T]) & 1)) {
                float v = ml[(size_t)S * P + T], u = ml[(size_t)T * P + S]; if (u < v) v = u;
                if (v > 1e29f) { act[S] = 1; un++; }
            }
        }
        R->unlit = un;
        if (!un || L >= LCAP * diam || L >= 2 * RMAX) break;
        L *= 2; if (L > LCAP * diam) L = LCAP * diam;
    }
    R->mincnt = 1 << 30; double best = -1;
    for (int S = 0; S < P; S++) for (int T = S + 1; T < P; T++) if (!((px[S] ^ px[T]) & 1) && !((py[S] ^ py[T]) & 1)) {
        float v = ml[(size_t)S * P + T], u = ml[(size_t)T * P + S]; if (u < v) v = u;
        int c = cnt[(size_t)S * P + T];
        R->npairs++;
        if (c < R->mincnt) { R->mincnt = c; R->nmin = 0; }
        if (c == R->mincnt) R->nmin++;
        double rho = v > 1e29f ? 2 * LCAP : sqrt(v) / diam;
        if (rho > best + 1e-9) { best = rho; R->npmax = 0; R->sx = px[S] - OFF; R->sy = py[S] - OFF; R->tx = px[T] - OFF; R->ty = py[T] - OFF; }
        if (rho > best - 1e-9) R->npmax++;
    }
    R->rho = best < 0 ? 0 : best;
    if (!R->npairs) R->mincnt = 0;
}
static void printroom(FILE *f, const Room *r, int A) {
    fprintf(f, "%d", A);
    for (int x = OFF; x < OFF + lw; x++) for (int y = OFF; y < OFF + lh; y++) if (r->c[x][y]) fprintf(f, " %d %d", x - OFF, y - OFF);
    fprintf(f, "\n");
}
static int readroom(FILE *f, Room *r) {
    int A; if (fscanf(f, "%d", &A) != 1) return 0;
    memset(r, 0, sizeof *r);
    for (int i = 0; i < A; i++) { int x, y; if (fscanf(f, "%d %d", &x, &y) != 2) return 0; r->c[x + OFF][y + OFF] = 1; }
    return A;
}
static void insline(Room *r, int ax, int c) {
    for (int x = G - 2; x >= c; x--) for (int y = 0; y < G; y++) { if (ax) r->c[y][x + 1] = r->c[y][x]; else r->c[x + 1][y] = r->c[x][y]; }
}
static void delline(Room *r, int ax, int c) {
    for (int x = c; x < G - 1; x++) for (int y = 0; y < G; y++) { if (ax) r->c[y][x] = r->c[y][x + 1]; else r->c[x][y] = r->c[x + 1][y]; }
}
static void mutate(Room *r) {
    int w = lw, h = lh, t = ri(100);
    if (t < 22) { int ax = ri(2), n = ri(3) ? 1 : 2, c = OFF + ri(ax ? h : w); for (int k = 0; k < n; k++) insline(r, ax, c); }
    else if (t < 42) { int ax = ri(2), n = ri(3) ? 1 : 2, c = OFF + ri(ax ? h : w); for (int k = 0; k < n; k++) delline(r, ax, c); }
    else if (t < 72) {
        for (int tries = 0; tries < 400; tries++) {
            int x = OFF + ri(w), y = OFF + ri(h), d = ri(4);
            static const int DX[4] = {1, -1, 0, 0}, DY[4] = {0, 0, 1, -1};
            if (!r->c[x][y] || r->c[x + DX[d]][y + DY[d]]) continue;
            int ox = DY[d] ? 1 : 0, oy = DX[d] ? 1 : 0, lo = 0, hi = 0, out = ri(2);
            while (r->c[x + ox * (hi + 1)][y + oy * (hi + 1)] && !r->c[x + ox * (hi + 1) + DX[d]][y + oy * (hi + 1) + DY[d]]) hi++;
            while (r->c[x + ox * (lo - 1)][y + oy * (lo - 1)] && !r->c[x + ox * (lo - 1) + DX[d]][y + oy * (lo - 1) + DY[d]]) lo--;
            for (int k = lo; k <= hi; k++) { if (out) r->c[x + ox * k + DX[d]][y + oy * k + DY[d]] = 1; else r->c[x + ox * k][y + oy * k] = 0; }
            break;
        }
    } else if (t < 97) {
        int a = 1, b = 1; while (a < 40 && ri(5) < 3) a++; while (b < 40 && ri(5) < 3) b++;
        int x = OFF - 1 + ri(w + 2), y = OFF - 1 + ri(h + 2), v = ri(2);
        for (int i = x; i < x + a && i < G - 2; i++) for (int j = y; j < y + b && j < G - 2; j++) r->c[i][j] = (unsigned char)v;
    } else {
        int ax = ri(2); if ((ax ? h : w) * 2 > BOX) return;
        for (int c = OFF + (ax ? h : w) - 1; c >= OFF; c--) insline(r, ax, c);
    }
}
#define NB 30
static struct { long n; double sum, mx; int minc; Room room; Res res; } st[9][NB];
static void record(const Room *r, const Res *R) {
    int rr = (R->W - 4) / 2, b = (int)(2 * log2((double)R->A)); if (rr > 8) rr = 8; if (b >= NB) b = NB - 1;
    if (!R->npairs) return;
    if (!st[rr][b].n) st[rr][b].minc = 1 << 30;
    st[rr][b].n++; st[rr][b].sum += R->rho;
    if (R->mincnt < st[rr][b].minc) st[rr][b].minc = R->mincnt;
    if (R->rho > st[rr][b].mx) { st[rr][b].mx = R->rho; st[rr][b].room = *r; st[rr][b].res = *R; }
}
static void pres(const char *tag, const Room *r, const Res *R) {
    printf("%s rho %.4f npmax %d mincnt %d nmin %d unlit %d A %d W %d diam %d P %d pairs %d pair (%d,%d)-(%d,%d) box %dx%d\nROOM ",
           tag, R->rho, R->npmax, R->mincnt, R->nmin, R->unlit, R->A, R->W, R->diam, R->P, R->npairs, R->sx, R->sy, R->tx, R->ty, lw, lh);
    printroom(stdout, r, R->A); fflush(stdout);
}
int main(int argc, char **argv) {
    if (argc > 1 && !strcmp(argv[1], "check")) {
        double L0 = atof(argv[2]), LCAP = atof(argv[3]); int verbose = argc > 4;
        AMIN = 1; AMAX = 4200; WMAX = 1000; init();
        Room r; Res R;
        while (readroom(stdin, &r)) {
            if (!validate(&r)) { printf("INVALID\n"); continue; }
            evaluate(&r, L0, LCAP, &R); pres("CHECK", &r, &R);
            if (verbose || R.unlit) for (int S = 0; S < R.P; S++) for (int T = S + 1; T < R.P; T++) if (!((px[S] ^ px[T]) & 1) && !((py[S] ^ py[T]) & 1)) {
                float v = ml[(size_t)S * R.P + T], u = ml[(size_t)T * R.P + S]; if (u < v) v = u;
                if (v > 1e29f) printf("UNLIT %d %d %d %d\n", px[S] - OFF, py[S] - OFF, px[T] - OFF, py[T] - OFF);
                else if (verbose) printf("P %d %d %d %d %.0f %d %d\n", px[S] - OFF, py[S] - OFF, px[T] - OFF, py[T] - OFF, v, cnt[(size_t)S * R.P + T], cnt[(size_t)T * R.P + S]);
            }
        }
        return 0;
    }
    rs ^= (uint64_t)atoll(argv[2]) * 0x9E3779B97F4A7C15ULL; for (int i = 0; i < 20; i++) rnd();
    int NR = atoi(argv[3]), NIT = atoi(argv[4]); AMIN = atoi(argv[5]); AMAX = atoi(argv[6]); BOX = atoi(argv[7]);
    double T0 = atof(argv[8]), L0 = atof(argv[9]), LCAP = atof(argv[10]);
    FILE *sf = argc > 11 ? fopen(argv[11], "r") : NULL;
    init();
    long nev = 0, ncand = 0; time_t tend = time(NULL) + (getenv("ADV_TLIM") ? atol(getenv("ADV_TLIM")) : 1000000);
    for (int rst = 0; rst < NR && time(NULL) < tend; rst++) {
        Room cur, cand, best; Res R, Rc, Rb; int ok = 0;
        if (sf && readroom(sf, &cur)) ok = validate(&cur);
        if (!ok) {
            for (;;) {
                memset(&cur, 0, sizeof cur);
                int w = 2 + ri(BOX < 24 ? BOX - 1 : 23), h = 2 + ri(BOX < 24 ? BOX - 1 : 23);
                for (int x = 0; x < w; x++) for (int y = 0; y < h; y++) cur.c[OFF + x][OFF + y] = 1;
                int sA = AMIN, sW = WMAX; AMIN = 1; WMAX = 20;
                if (validate(&cur)) for (int k = 0; k < 60; k++) { cand = cur; mutate(&cand); if (validate(&cand)) cur = cand; else validate(&cur); }
                AMIN = sA; WMAX = sW;
                if (validate(&cur)) break;
            }
        }
        evaluate(&cur, L0, LCAP, &R); if (getenv("ADV_OBJ")) R.rho *= (double)R.diam / R.A; nev++; record(&cur, &R); best = cur; Rb = R;
        for (int it = 0; it < NIT && time(NULL) < tend; it++) {
            double T = T0 * pow(0.02, (double)it / NIT);
            validate(&cur); cand = cur; mutate(&cand);
            if (!validate(&cand)) continue;
            evaluate(&cand, L0, LCAP, &Rc); if (getenv("ADV_OBJ")) Rc.rho *= (double)Rc.diam / Rc.A; nev++; record(&cand, &Rc);
            if (Rc.unlit) { ncand++; pres("CAND", &cand, &Rc); }
            double f = R.rho - 0.002 * (R.mincnt > 500 ? 500 : R.mincnt), fc = Rc.rho - 0.002 * (Rc.mincnt > 500 ? 500 : Rc.mincnt);
            if (fc >= f || ru() < exp((fc - f) / T)) { cur = cand; R = Rc; if (R.rho > Rb.rho) { best = cur; Rb = R; } }
        }
        validate(&best); pres("BEST", &best, &Rb);
        printf("restart %d done, evals %ld cands %ld\n", rst, nev, ncand); fflush(stdout);
    }
    printf("STATS r areabin(lo) n mean_rho max_rho min_mincnt | max room: A diam P pair\n");
    for (int rr = 0; rr < 9; rr++) for (int b = 0; b < NB; b++) if (st[rr][b].n) {
        printf("S %d %d %ld %.3f %.3f %d | %d %d %d\n", rr, (int)pow(2, b / 2.0), st[rr][b].n, st[rr][b].sum / st[rr][b].n, st[rr][b].mx, st[rr][b].minc, st[rr][b].res.A, st[rr][b].res.diam, st[rr][b].res.P);
        validate(&st[rr][b].room); pres("BINMAX", &st[rr][b].room, &st[rr][b].res);
    }
    return 0;
}
