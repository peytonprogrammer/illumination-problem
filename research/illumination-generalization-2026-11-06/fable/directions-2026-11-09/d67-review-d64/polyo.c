/* d67: independent brute force (no d64/d52/d10 code). Redelmeier enumeration of all fixed
   polyominoes with n <= NMAX cells. Keep those that are strictly simple (no hole, no pinch),
   have r <= 8 reflex vertices, and are normalized (gcd of maximal horizontal edge lengths = 1,
   same for vertical). For each parity class (p, q) compute the number of blocks of B_x: the
   finest partition of cells invariant under V0, V1, H0, H1 (reflections across even/odd lines,
   identity at walls) that merges every 2-cycle of g = V_p H_q. In scope: some class with
   1 < blocks < n. Prints per n: fixed polyominoes, fixed rooms (strictly simple, r <= 8,
   normalized), fixed in-scope rooms.
   Build: cc -O2 -o polyo polyo.c ; run: ./polyo NMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NM 18
#define W (2 * NM + 4)
#define OFF (NM + 1)
static int nmax;
static int cx[NM + 1], cy[NM + 1];
static unsigned char occ[W][W];          /* occ[x + OFF][y + 1] */
static unsigned char seen[W][W];
static long long nfixed[NM + 1], nroom[NM + 1], nscope[NM + 1];

static int has(int x, int y) {
    int X = x + OFF, Y = y + 1;
    if (X < 0 || X >= W || Y < 0 || Y >= W) return 0;
    return occ[X][Y];
}

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

static int idx_of[W][W];
static int par[NM + 1];
static int findp(int a) { while (par[a] != a) { par[a] = par[par[a]]; a = par[a]; } return a; }

static int nblocks(int n, int G[4][NM + 1], int p, int q) {
    int stA[4096], stB[4096], sp = 0;
    for (int i = 0; i < n; i++) par[i] = i;
    for (int u = 0; u < n; u++) {
        int v = G[p][G[2 + q][u]];
        if (v != u && G[p][G[2 + q][v]] == u && u < v) { stA[sp] = u; stB[sp] = v; sp++; }
    }
    while (sp) {
        sp--;
        int a = stA[sp], b = stB[sp];
        int ra = findp(a), rb = findp(b);
        if (ra == rb) continue;
        par[ra] = rb;
        for (int g = 0; g < 4; g++) {
            if (sp >= 4090) { fprintf(stderr, "stack\n"); exit(2); }
            stA[sp] = G[g][a]; stB[sp] = G[g][b]; sp++;
        }
    }
    int k = 0;
    for (int i = 0; i < n; i++) if (findp(i) == i) k++;
    return k;
}

static void check(int n) {
    nfixed[n]++;
    int minx = 1 << 30, maxx = -(1 << 30), miny = 1 << 30, maxy = -(1 << 30);
    for (int i = 0; i < n; i++) {
        if (cx[i] < minx) minx = cx[i];
        if (cx[i] > maxx) maxx = cx[i];
        if (cy[i] < miny) miny = cy[i];
        if (cy[i] > maxy) maxy = cy[i];
    }
    /* vertices: pinch, reflex count, Euler characteristic */
    int V = 0, E = 0, r = 0;
    for (int x = minx; x <= maxx + 1; x++)
        for (int y = miny; y <= maxy + 1; y++) {
            int a = has(x - 1, y - 1), b = has(x, y - 1), c = has(x - 1, y), d = has(x, y);
            int k = a + b + c + d;
            if (k == 0) continue;
            V++;
            if (k == 2 && ((a && d) || (b && c))) return;     /* pinch */
            if (k == 3) r++;
        }
    if (r > 8) return;
    for (int x = minx; x <= maxx; x++)          /* horizontal unit edges [x,x+1] at height y */
        for (int y = miny; y <= maxy + 1; y++) if (has(x, y - 1) || has(x, y)) E++;
    for (int x = minx; x <= maxx + 1; x++)
        for (int y = miny; y <= maxy; y++) if (has(x - 1, y) || has(x, y)) E++;
    if (V - E + n != 1) return;                 /* hole */
    /* normalization: maximal boundary runs, broken at corners (vertex count 1 or 3) */
    int gh = 0, gv = 0;
    for (int y = miny; y <= maxy + 1; y++) {
        int run = 0;
        for (int x = minx; x <= maxx + 1; x++) {
            /* vertex (x, y) ends the run if it is a corner */
            int k = has(x - 1, y - 1) + has(x, y - 1) + has(x - 1, y) + has(x, y);
            if (run && (k == 1 || k == 3)) { gh = gcd(gh, run); run = 0; }
            if (x <= maxx && (has(x, y - 1) != has(x, y))) run++;
            else if (run) { fprintf(stderr, "run error\n"); exit(3); }
        }
    }
    for (int x = minx; x <= maxx + 1; x++) {
        int run = 0;
        for (int y = miny; y <= maxy + 1; y++) {
            int k = has(x - 1, y - 1) + has(x, y - 1) + has(x - 1, y) + has(x, y);
            if (run && (k == 1 || k == 3)) { gv = gcd(gv, run); run = 0; }
            if (y <= maxy && (has(x - 1, y) != has(x, y))) run++;
            else if (run) { fprintf(stderr, "run error v\n"); exit(3); }
        }
    }
    if (gh != 1 || gv != 1) return;
    nroom[n]++;
    int G[4][NM + 1];
    for (int i = 0; i < n; i++) idx_of[cx[i] + OFF][cy[i] + 1] = i;
    for (int i = 0; i < n; i++) {
        int x = cx[i], y = cy[i];
        for (int pp = 0; pp < 2; pp++) {
            int nx = (((x % 2) + 2) % 2 == pp) ? x - 1 : x + 1;
            G[pp][i] = has(nx, y) ? idx_of[nx + OFF][y + 1] : i;
            int ny = (((y % 2) + 2) % 2 == pp) ? y - 1 : y + 1;
            G[2 + pp][i] = has(x, ny) ? idx_of[x + OFF][ny + 1] : i;
        }
    }
    for (int p = 0; p < 2; p++)
        for (int q = 0; q < 2; q++) {
            int k = nblocks(n, G, p, q);
            if (k > 1 && k < n) { nscope[n]++; return; }
        }
}

/* Redelmeier: cells with y > 0, or y == 0 and x >= 0 */
static int ux[64 * NM * NM], uy[64 * NM * NM];
static void rec(int n, int ustart, int uend) {
    /* untried set is ux/uy[ustart..uend) */
    for (int k = ustart; k < uend; k++) {
        int x = ux[k], y = uy[k];
        cx[n] = x; cy[n] = y;
        occ[x + OFF][y + 1] = 1;
        check(n + 1);
        if (n + 1 < nmax) {
            int ne = uend;
            /* copy remaining untried (k+1..uend) and add new neighbours */
            int base = uend;
            for (int j = k + 1; j < uend; j++) { ux[ne] = ux[j]; uy[ne] = uy[j]; ne++; }
            int dx[4] = {1, -1, 0, 0}, dy[4] = {0, 0, 1, -1};
            int added[4][2], na = 0;
            for (int d = 0; d < 4; d++) {
                int a = x + dx[d], b = y + dy[d];
                if (!(b > 0 || (b == 0 && a >= 0))) continue;
                if (seen[a + OFF][b + 1]) continue;
                seen[a + OFF][b + 1] = 1;
                added[na][0] = a; added[na][1] = b; na++;
                ux[ne] = a; uy[ne] = b; ne++;
            }
            rec(n + 1, base, ne);
            for (int j = 0; j < na; j++) seen[added[j][0] + OFF][added[j][1] + 1] = 0;
        }
        occ[x + OFF][y + 1] = 0;
    }
}

int main(int argc, char **argv) {
    nmax = atoi(argv[1]);
    if (nmax > NM) return 1;
    ux[0] = 0; uy[0] = 0;
    seen[0 + OFF][0 + 1] = 1;
    rec(0, 0, 1);
    for (int n = 1; n <= nmax; n++)
        printf("n %d fixed %lld rooms_fixed %lld inscope_fixed %lld\n", n, nfixed[n], nroom[n], nscope[n]);
    return 0;
}
