/* verify_plane.c -- second, independent exact tracer for lit-path certificates.
 *
 * Works in the room plane, not in an unfolding.  The billiard ball moves from
 * lattice point to lattice point along a primitive direction (+-p, +-q).
 * Within one lattice step, integer event times u in [0, p*q] mark crossings of
 * vertical grid lines (u = q*a) and horizontal grid lines (u = p*b).  A
 * crossing into a cell outside the room reflects the corresponding velocity
 * component.  At each lattice point: a corner (1 or 3 cells) is illegal; an
 * interior point is crossed straight; a flat boundary point reflects the
 * component normal to its wall.  Axis directions run along grid lines.
 *
 * It shares no code with shoot.c.  It reads only the cell list.
 */
#include <stdlib.h>
#include <string.h>

#define VP_MAXC 64
static int vp_n, vp_cx[VP_MAXC], vp_cy[VP_MAXC];

static int vp_has(int x, int y) {
    for (int i = 0; i < vp_n; i++)
        if (vp_cx[i] == x && vp_cy[i] == y) return 1;
    return 0;
}

/* number of cells around lattice point (x,y); -1 for a pinch point */
static int vp_around(int x, int y) {
    int ll = vp_has(x - 1, y - 1), lr = vp_has(x, y - 1), ul = vp_has(x - 1, y), ur = vp_has(x, y);
    int k = ll + lr + ul + ur;
    if (k == 2 && ((ll && ur) || (lr && ul))) return -1;
    return k;
}

/* Returns 1 iff the billiard path from (sx0,sy0) with initial direction
 * (dx, dy) (primitive, integers) reaches lattice point (tx,ty) after exactly m
 * lattice steps, meeting no corner on the way (endpoints included). */
int reflections;
int verify_plane(int ncell, const int *cx, const int *cy,
                 int sx0, int sy0, int dx, int dy, int m, int tx, int ty) {
    reflections = 0;
    vp_n = ncell;
    memcpy(vp_cx, cx, sizeof(int) * ncell);
    memcpy(vp_cy, cy, sizeof(int) * ncell);
    if (vp_around(sx0, sy0) != 4) return 0;     /* source must be interior */
    int p = abs(dx), q = abs(dy);
    int ex = dx > 0 ? 1 : (dx < 0 ? -1 : 0), ey = dy > 0 ? 1 : (dy < 0 ? -1 : 0);
    int X = sx0, Y = sy0;
    if (p == 0 || q == 0) {
        if (p + q != 1) return 0;
        for (int step = 1; step <= m; step++) {
            int nx = X + ex, ny = Y + ey;
            int k = vp_around(nx, ny);
            if (k == 1 || k == 3 || k == 0 || k == -1) return 0;
            if (k == 2) {
                /* cells behind the point (on the side we came from) */
                int b1, b2;
                if (ex) { int bx = ex > 0 ? nx - 1 : nx; b1 = vp_has(bx, ny - 1); b2 = vp_has(bx, ny); }
                else    { int by = ey > 0 ? ny - 1 : ny; b1 = vp_has(nx - 1, by); b2 = vp_has(nx, by); }
                if (b1 && b2) { ex = -ex; ey = -ey; reflections++; }   /* wall across the line: bounce back */
                else return 0;                          /* grazing a wall: not expected from interior start */
            }
            X = nx; Y = ny;
        }
        return X == tx && Y == ty;
    }
    /* current cell entered from (X,Y) in direction (ex,ey) */
    int ci = ex > 0 ? X : X - 1, cj = ey > 0 ? Y : Y - 1;
    if (!vp_has(ci, cj)) return 0;
    for (int step = 1; step <= m; step++) {
        int a = 1, b = 1;                 /* next vertical / horizontal crossing indices */
        while (a < p || b < q) {
            long uv = (a < p) ? (long)q * a : 1L << 60;
            long uh = (b < q) ? (long)p * b : 1L << 60;
            if (uv < uh) {                /* cross a vertical grid line */
                if (vp_has(ci + ex, cj)) ci += ex; else { ex = -ex; reflections++; }
                a++;
            } else {                      /* cross a horizontal grid line */
                if (vp_has(ci, cj + ey)) cj += ey; else { ey = -ey; reflections++; }
                b++;
            }
        }
        int QX = ci + (ex > 0), QY = cj + (ey > 0);
        int k = vp_around(QX, QY);
        if (k != 2 && k != 4) return 0;
        if (k == 4) { ci += ex; cj += ey; }
        else if (vp_has(ci + ex, cj)) { ci += ex; ey = -ey; reflections++; }   /* horizontal wall */
        else if (vp_has(ci, cj + ey)) { cj += ey; ex = -ex; reflections++; }   /* vertical wall */
        else return 0;
        X = QX; Y = QY;
    }
    return X == tx && Y == ty;
}
