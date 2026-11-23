/* negtest45.c -- sanity test of verify45: every lit certificate in a shoot45
 * output must replay (positive), and must be REJECTED when the target is
 * replaced by the source (wrong target) or the direction is rotated by 90
 * degrees (wrong direction, accepted only if that path happens to work too).
 * usage: negtest45 shoot.out
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int verify45(int n, const int *ti, const int *tj, const int *th, int sx, int sy, int dx, int dy, int m, int tx, int ty);
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    static char line[16384];
    int n = 0, ti[64], tj[64], th[64];
    long long pos = 0, pos_ok = 0, wrongT = 0, wrongT_rej = 0, rot = 0, rot_rej = 0;
    while (fgets(line, sizeof line, f)) {
        char *p = line;
        if (line[0] == 'R') {
            p += 2; strtol(p, &p, 10); n = (int)strtol(p, &p, 10); strtol(p, &p, 10);
            for (int a = 0; a < n; a++) { ti[a] = (int)strtol(p, &p, 10); tj[a] = (int)strtol(p, &p, 10); th[a] = (int)strtol(p, &p, 10); }
        } else if (line[0] == 'P') {
            char X, L; int sx, sy, tx, ty, dx, dy, m;
            if (sscanf(line, "P %c %d %d %d %d %c %d %d %d", &X, &sx, &sy, &tx, &ty, &L, &dx, &dy, &m) != 9 || L != 'L') continue;
            pos++; pos_ok += verify45(n, ti, tj, th, sx, sy, dx, dy, m, tx, ty);
            wrongT++; wrongT_rej += !verify45(n, ti, tj, th, sx, sy, dx, dy, m, sx, sy);
            rot++; rot_rej += !verify45(n, ti, tj, th, sx, sy, -dy, dx, m, tx, ty);
        }
    }
    printf("certificates %lld replayed %lld | wrong target %lld rejected %lld | rotated direction %lld rejected %lld\n",
           pos, pos_ok, wrongT, wrongT_rej, rot, rot_rej);
    return 0;
}
