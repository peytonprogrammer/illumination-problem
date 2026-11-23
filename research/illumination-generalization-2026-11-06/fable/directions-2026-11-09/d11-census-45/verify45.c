/* verify45.c -- independent exact billiard tracer in the room plane.
 *
 * Shares no code with the origami shooter.  The room is a list of canonical45
 * tiles (i, j, h).  Boundary edges are tile edges covered once; a corner is a
 * boundary vertex whose two boundary edges are not collinear.
 *
 * verify45(...) follows the billiard path from S in room direction (dx,dy)
 * (primitive integers) with the reflection law, using exact integer
 * arithmetic: positions are stored times M = lcm(|dx|,|dy|,|dx+dy|,|dx-dy|)
 * (zero factors skipped), so every event (crossing of a line x in Z, y in Z,
 * x+y in 2Z, x-y in 2Z) has an integer position.  The time t (in units of
 * the primitive step) is kept as K = M t.  It returns 1 iff the path meets no
 * corner for 0 < t < m, stays in the room, and is at T at t = m.
 */
#include <stdlib.h>
#include <string.h>

#define VG 128
#define VO 64
static int ecnt[4][VG][VG];          /* 0: H (x,y)-(x+1,y); 1: V (x,y)-(x,y+1); 2: D+ (x,y)-(x+1,y+1); 3: D- (x,y+1)-(x+1,y) */
static int vin[VG][VG];              /* lattice point belongs to the room */
static int vcorner[VG][VG];
static int bdir[VG][VG];             /* for flat boundary points: wall type 0..3 */
static int stamp = 0;

static void tri_of(int i, int j, int h, int *x, int *y) {
    /* written independently: "/" squares (i+j even) are cut by the diagonal through (i,j); */
    int slash = ((i + j) % 2 + 2) % 2 == 0;
    int X[4] = {i, i + 1, i + 1, i}, Y[4] = {j, j, j + 1, j + 1};   /* BL, BR, TR, TL */
    int idx[3];
    if (slash) { if (h == 0) { idx[0] = 0; idx[1] = 1; idx[2] = 2; } else { idx[0] = 0; idx[1] = 3; idx[2] = 2; } }
    else       { if (h == 0) { idx[0] = 0; idx[1] = 1; idx[2] = 3; } else { idx[0] = 1; idx[1] = 2; idx[2] = 3; } }
    for (int k = 0; k < 3; k++) { x[k] = X[idx[k]]; y[k] = Y[idx[k]]; }
}

static void edge_slot(int x1, int y1, int x2, int y2, int *ty, int *ex, int *ey) {
    if (y1 == y2) { *ty = 0; *ex = x1 < x2 ? x1 : x2; *ey = y1; return; }
    if (x1 == x2) { *ty = 1; *ex = x1; *ey = y1 < y2 ? y1 : y2; return; }
    int lx = x1 < x2 ? x1 : x2;
    int ly = y1 < y2 ? y1 : y2;
    if ((x2 - x1) * (y2 - y1) > 0) { *ty = 2; *ex = lx; *ey = ly; }
    else { *ty = 3; *ex = lx; *ey = ly; }
}

static int nT, Ti[64], Tj[64], Th[64];

static void build(int n, const int *ti, const int *tj, const int *th) {
    for (int a = 0; a < nT; a++) {      /* clear previous room */
        int x[3], y[3];
        tri_of(Ti[a], Tj[a], Th[a], x, y);
        for (int k = 0; k < 3; k++) {
            int ty, ex, ey;
            edge_slot(x[k], y[k], x[(k + 1) % 3], y[(k + 1) % 3], &ty, &ex, &ey);
            ecnt[ty][ex + VO][ey + VO] = 0;
            vin[x[k] + VO][y[k] + VO] = 0; vcorner[x[k] + VO][y[k] + VO] = 0; bdir[x[k] + VO][y[k] + VO] = -1;
        }
    }
    nT = n;
    for (int a = 0; a < n; a++) { Ti[a] = ti[a]; Tj[a] = tj[a]; Th[a] = th[a]; }
    for (int a = 0; a < n; a++) {
        int x[3], y[3];
        tri_of(ti[a], tj[a], th[a], x, y);
        for (int k = 0; k < 3; k++) {
            int ty, ex, ey;
            edge_slot(x[k], y[k], x[(k + 1) % 3], y[(k + 1) % 3], &ty, &ex, &ey);
            ecnt[ty][ex + VO][ey + VO]++;
            vin[x[k] + VO][y[k] + VO] = 1; bdir[x[k] + VO][y[k] + VO] = -1;
        }
    }
    /* boundary edges at each vertex */
    static int nbd[VG][VG], bd[VG][VG][4];
    for (int a = 0; a < n; a++) {
        int x[3], y[3];
        tri_of(ti[a], tj[a], th[a], x, y);
        for (int k = 0; k < 3; k++) nbd[x[k] + VO][y[k] + VO] = 0;
    }
    for (int a = 0; a < n; a++) {
        int x[3], y[3];
        tri_of(ti[a], tj[a], th[a], x, y);
        for (int k = 0; k < 3; k++) {
            int ty, ex, ey;
            edge_slot(x[k], y[k], x[(k + 1) % 3], y[(k + 1) % 3], &ty, &ex, &ey);
            if (ecnt[ty][ex + VO][ey + VO] == 1) {
                int p[2][2] = {{x[k], y[k]}, {x[(k + 1) % 3], y[(k + 1) % 3]}};
                for (int u = 0; u < 2; u++) { int *c = &nbd[p[u][0] + VO][p[u][1] + VO]; if (*c < 4) bd[p[u][0] + VO][p[u][1] + VO][(*c)++] = ty; }
            }
        }
    }
    for (int a = 0; a < n; a++) {
        int x[3], y[3];
        tri_of(ti[a], tj[a], th[a], x, y);
        for (int k = 0; k < 3; k++) {
            int X = x[k] + VO, Y = y[k] + VO;
            if (nbd[X][Y] == 0) continue;
            if (nbd[X][Y] != 2 || bd[X][Y][0] != bd[X][Y][1]) vcorner[X][Y] = 1;   /* pinch (4 edges) also counts as corner */
            else bdir[X][Y] = bd[X][Y][0];
        }
    }
    stamp++;
}

static long long gcdll(long long a, long long b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { long long t = a % b; a = b; b = t; } return a; }
static long long lcmll(long long a, long long b) { if (a == 0) return b; if (b == 0) return a; return a / gcdll(a, b) * (b < 0 ? -b : b); }

static long long floordiv(long long a, long long b) { long long q = a / b; if ((a % b != 0) && ((a < 0) != (b < 0))) q--; return q; }

static void reflect(int ty, long long *ex, long long *ey) {
    long long a = *ex, b = *ey;
    if (ty == 0) { *ey = -b; }
    else if (ty == 1) { *ex = -a; }
    else if (ty == 2) { *ex = b; *ey = a; }
    else { *ex = -b; *ey = -a; }
}

int verify45(int n, const int *ti, const int *tj, const int *th,
             int sx, int sy, int dx, int dy, int m, int tx, int ty_) {
    build(n, ti, tj, th);
    long long M = 1;
    M = lcmll(M, dx); M = lcmll(M, dy); M = lcmll(M, dx + dy); M = lcmll(M, dx - dy);
    if (M < 0) M = -M;
    long long X = (long long)sx * M, Y = (long long)sy * M, ex = dx, ey = dy, K = 0, KEND = (long long)m * M;
    for (int guard = 0; guard < 10000000; guard++) {
        long long best = -1;
        /* candidate crossings, strictly ahead */
        long long cand[4][2] = {{X, ex}, {Y, ey}, {X + Y, ex + ey}, {X - Y, ex - ey}};
        long long per[4] = {M, M, 2 * M, 2 * M};
        for (int c = 0; c < 4; c++) {
            long long pos = cand[c][0], rate = cand[c][1], P = per[c];
            if (rate == 0) continue;
            /* next multiple of P strictly ahead of pos in the direction of rate */
            long long target = rate > 0 ? (floordiv(pos, P) + 1) * P : floordiv(pos - 1, P) * P;
            long long dist = target - pos;
            if (dist % rate != 0) return 0;       /* event off the integer grid: theory violated */
            long long dt = dist / rate;
            if (dt <= 0) return 0;
            if (best < 0 || dt < best) best = dt;
        }
        if (best < 0) return 0;
        X += ex * best; Y += ey * best; K += best;
        if (K > KEND) return 0;
        int lat = (X % M == 0) && (Y % M == 0);
        if (lat != (K % M == 0)) return 0;
        if (lat) {
            long long qx = X / M, qy = Y / M;
            if (qx < -VO + 1 || qy < -VO + 1 || qx > VO - 2 || qy > VO - 2) return 0;
            int QX = (int)qx + VO, QY = (int)qy + VO;
            if (!vin[QX][QY]) return 0;
            if (vcorner[QX][QY]) return 0;
            if (K == KEND) return qx == tx && qy == ty_;
            if (bdir[QX][QY] >= 0) reflect(bdir[QX][QY], &ex, &ey);
            continue;
        }
        /* interior point of a unit edge: which line? */
        int ty = -1, ex0 = 0, ey0 = 0;
        if (X % M == 0) { ty = 1; ex0 = (int)(X / M); ey0 = (int)floordiv(Y, M); }
        else if (Y % M == 0) { ty = 0; ex0 = (int)floordiv(X, M); ey0 = (int)(Y / M); }
        else if ((X + Y) % (2 * M) == 0) { ty = 3; ex0 = (int)floordiv(X, M); ey0 = (int)floordiv(Y, M); }
        else if ((X - Y) % (2 * M) == 0) { ty = 2; ex0 = (int)floordiv(X, M); ey0 = (int)floordiv(Y, M); }
        else return 0;
        if (ex0 < -VO + 1 || ey0 < -VO + 1 || ex0 > VO - 2 || ey0 > VO - 2) return 0;
        int c = ecnt[ty][ex0 + VO][ey0 + VO];
        if (c == 0) return 0;               /* left the room */
        if (c == 1) reflect(ty, &ex, &ey);
    }
    return 0;
}
