/* Enumerate combinatorial types (order types) of strictly simple orthogonal
 * polygons: cell sets on an nx x ny index grid such that every grid line
 * 0..nx and 0..ny carries a polygon vertex, the set is connected, has no
 * hole and no pinch point, and has at most Wmax vertices.
 * Output: one line "nx ny W mask" per type, canonical under the 8 symmetries
 * (flag canon=1) or all (canon=0).  Cells are bit i + nx*j.
 * Usage: enum_types nx ny Wmax canon
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64;
static int nx, ny, Wmax, canon;
static unsigned char c[10][10];           /* c[i+1][j+1] */
static u64 total[64];

static int pt(int i, int j) {             /* cells around grid point (i,j) */
    int a = c[i][j], b = c[i+1][j], d = c[i][j+1], e = c[i+1][j+1];
    int n = a + b + d + e;
    if (n == 2 && ((a && e) || (b && d))) return -1;   /* pinch */
    return (n == 1 || n == 3);
}
static u64 mask_of(int tr, int fx, int fy, int *onx, int *ony) {
    u64 m = 0; int mx = tr ? ny : nx, my = tr ? nx : ny;
    for (int i = 0; i < nx; i++) for (int j = 0; j < ny; j++) if (c[i+1][j+1]) {
        int a = fx ? nx-1-i : i, b = fy ? ny-1-j : j;
        if (tr) { int t = a; a = b; b = t; }
        m |= 1ULL << (a + mx*b);
    }
    *onx = mx; *ony = my; return m;
}
static void finish(int W, unsigned vx, unsigned vy) {
    if (vx != (1u << (nx+1)) - 1 || vy != (1u << (ny+1)) - 1) return;
    /* connectivity */
    int n = 0, sx = -1, sy = -1;
    for (int i = 1; i <= nx; i++) for (int j = 1; j <= ny; j++) if (c[i][j]) { n++; sx = i; sy = j; }
    static int st[128][2]; unsigned char seen[10][10] = {{0}};
    int sp = 0, cnt = 0; st[sp][0] = sx; st[sp][1] = sy; sp++; seen[sx][sy] = 1;
    while (sp) { sp--; int i = st[sp][0], j = st[sp][1]; cnt++;
        int d[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        for (int k = 0; k < 4; k++) { int a = i+d[k][0], b = j+d[k][1];
            if (a>=1&&a<=nx&&b>=1&&b<=ny&&c[a][b]&&!seen[a][b]) { seen[a][b]=1; st[sp][0]=a; st[sp][1]=b; sp++; } } }
    if (cnt != n) return;
    /* no hole: outside (with border ring) 4-connected */
    unsigned char s2[10][10] = {{0}}; sp = 0; st[sp][0] = 0; st[sp][1] = 0; sp++; s2[0][0] = 1; cnt = 0;
    while (sp) { sp--; int i = st[sp][0], j = st[sp][1]; cnt++;
        int d[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        for (int k = 0; k < 4; k++) { int a = i+d[k][0], b = j+d[k][1];
            if (a>=0&&a<=nx+1&&b>=0&&b<=ny+1&&!c[a][b]&&!s2[a][b]) { s2[a][b]=1; st[sp][0]=a; st[sp][1]=b; sp++; } } }
    if (cnt != (nx+2)*(ny+2) - n) return;
    int ox, oy; u64 m0 = mask_of(0,0,0,&ox,&oy);
    if (canon) {
        for (int g = 1; g < 8; g++) {
            int tx, ty; u64 m = mask_of(g>>2, g&1, (g>>1)&1, &tx, &ty);
            if (tx < nx || (tx == nx && m < m0)) return;   /* keep the smallest (nx, mask) */
        }
    }
    total[W]++;
    printf("%d %d %d %llu\n", nx, ny, W, m0);
}
static void rec(int pos, int W, unsigned vx, unsigned vy) {
    if (pos == nx*ny) { finish(W, vx, vy); return; }
    int i = pos % nx, j = pos / nx;
    for (int v = 0; v < 2; v++) {
        c[i+1][j+1] = v;
        int w = W; unsigned ax = vx, ay = vy; int ok = 1, r;
        /* grid point (i,j) is surrounded by c[i][j],c[i+1][j],c[i][j+1],c[i+1][j+1] */
        r = pt(i, j); if (r < 0) ok = 0; else if (r) { w++; ax |= 1u<<i; ay |= 1u<<j; }
        if (ok && i == nx-1) { r = pt(nx, j); if (r < 0) ok = 0; else if (r) { w++; ax |= 1u<<nx; ay |= 1u<<j; } }
        if (ok && j == ny-1) { r = pt(i, ny); if (r < 0) ok = 0; else if (r) { w++; ax |= 1u<<i; ay |= 1u<<ny; }
            if (ok && i == nx-1) { r = pt(nx, ny); if (r < 0) ok = 0; else if (r) { w++; ax |= 1u<<nx; ay |= 1u<<ny; } } }
        if (ok && w <= Wmax) {
            /* every horizontal line below the current row must already carry a vertex */
            if (i == nx-1 && j >= 1) { for (int l = 0; l < j; l++) if (!((ay>>l)&1)) ok = 0; }
            if (ok) rec(pos+1, w, ax, ay);
        }
    }
    c[i+1][j+1] = 0;
}
int main(int argc, char **argv) {
    nx = atoi(argv[1]); ny = atoi(argv[2]); Wmax = atoi(argv[3]); canon = atoi(argv[4]);
    rec(0, 0, 0, 0);
    for (int w = 4; w <= Wmax; w += 2) fprintf(stderr, "nx=%d ny=%d W=%d count=%llu\n", nx, ny, w, total[w]);
    return 0;
}
