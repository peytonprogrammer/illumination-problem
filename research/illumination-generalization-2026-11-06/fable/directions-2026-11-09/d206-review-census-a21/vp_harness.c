/* Feed queries to the production verify_plane.c: n cells.. sx sy dx dy m tx ty */
#include <stdio.h>
int verify_plane(int, const int *, const int *, int, int, int, int, int, int, int);
int main(void) {
    int n, cx[64], cy[64], sx, sy, dx, dy, m, tx, ty;
    while (scanf("%d", &n) == 1) {
        for (int i = 0; i < n; i++) scanf("%d %d", &cx[i], &cy[i]);
        scanf("%d %d %d %d %d %d %d", &sx, &sy, &dx, &dy, &m, &tx, &ty);
        printf("%d\n", verify_plane(n, cx, cy, sx, sy, dx, dy, m, tx, ty));
    }
    return 0;
}
