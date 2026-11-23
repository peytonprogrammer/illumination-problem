/* orbitc.c -- C twin of orbit.py: complete SL(2,Z)-orbit decider.
 *
 * Input on stdin, one problem per line:
 *   area x0 y0 ... | nsrc sx0 sy0 sx1 sy1 ...
 * Sources must be regular lattice points (interior or flat boundary).
 * Output per problem: number of states, completeness, and for every pair of
 * sources "LIT" or "DARK".
 *
 * Same construction as orbit.py (see its docstring): 4-fold unfolding,
 * coarse decoration (source index / corner / free), canonical relabelling by
 * BFS (h before v) from every square carrying source 0, four shear moves.
 *
 * usage: orbitc CAP < problems
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXQ 160
#define OFF 12
static int n;                       /* squares */
static int KEYLEN;                  /* 3n bytes */
static const int SX[4] = {1, -1, 1, -1}, SY[4] = {1, 1, -1, -1};

static unsigned char *arena;        /* states, KEYLEN bytes each */
static long long nst, cap;
static long long *table; static long long tsize;

static uint64_t hashk(const unsigned char *k) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < KEYLEN; i++) { h ^= k[i]; h *= 1099511628211ULL; }
    return h;
}

static int insert(const unsigned char *k) {   /* 1 if new */
    uint64_t h = hashk(k) & (tsize - 1);
    while (table[h] >= 0) {
        if (!memcmp(arena + table[h] * KEYLEN, k, KEYLEN)) return 0;
        h = (h + 1) & (tsize - 1);
    }
    if (nst >= cap) { fprintf(stderr, "cap exceeded\n"); exit(3); }
    memcpy(arena + nst * KEYLEN, k, KEYLEN);
    table[h] = nst++;
    return 1;
}

/* canonical key of (h, v, dec) */
static void canon(const unsigned char *h, const unsigned char *v, const signed char *dec, unsigned char *best) {
    unsigned char key[3 * MAXQ];
    int num[MAXQ], order[MAXQ];
    int have = 0;
    for (int a = 0; a < n; a++) {
        if (dec[a] != 0) continue;
        for (int i = 0; i < n; i++) num[i] = -1;
        int len = 1, k = 0;
        order[0] = a; num[a] = 0;
        while (k < len) {
            int x = order[k++];
            int y = h[x];
            if (num[y] < 0) { num[y] = len; order[len++] = y; }
            y = v[x];
            if (num[y] < 0) { num[y] = len; order[len++] = y; }
        }
        if (len != n) { fprintf(stderr, "disconnected\n"); exit(4); }
        for (int i = 0; i < n; i++) {
            key[i] = (unsigned char)num[h[order[i]]];
            key[n + i] = (unsigned char)num[v[order[i]]];
            key[2 * n + i] = (unsigned char)dec[order[i]];
        }
        if (!have || memcmp(key, best, KEYLEN) < 0) { memcpy(best, key, KEYLEN); have = 1; }
    }
}

int main(int argc, char **argv) {
    cap = argc > 1 ? atoll(argv[1]) : 20000000;
    char line[8192];
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        char *p = line;
        int area = (int)strtol(p, &p, 10);
        int cx[MAXQ], cy[MAXQ];
        for (int i = 0; i < area; i++) { cx[i] = (int)strtol(p, &p, 10) + OFF; cy[i] = (int)strtol(p, &p, 10) + OFF; }
        while (*p == ' ') p++;
        if (*p != '|') { fprintf(stderr, "bad line\n"); return 1; }
        p++;
        int ns = (int)strtol(p, &p, 10), sx[64], sy[64];
        for (int i = 0; i < ns; i++) { sx[i] = (int)strtol(p, &p, 10) + OFF; sy[i] = (int)strtol(p, &p, 10) + OFF; }
        static int cid[64][64];
        memset(cid, -1, sizeof cid);
        for (int i = 0; i < area; i++) cid[cx[i]][cy[i]] = i;
#define HAS(x, y) ((x) >= 0 && (y) >= 0 && (x) < 64 && (y) < 64 && cid[x][y] >= 0)
        n = 4 * area; KEYLEN = 3 * n;
        unsigned char h[MAXQ], v[MAXQ]; signed char dec[MAXQ];
        for (int c = 0; c < area; c++)
            for (int s = 0; s < 4; s++) {
                int q = 4 * c + s, i = cx[c], j = cy[c];
                h[q] = HAS(i + SX[s], j) ? 4 * cid[i + SX[s]][j] + s : 4 * c + (s ^ 1);
                v[q] = HAS(i, j + SY[s]) ? 4 * cid[i][j + SY[s]] + s : 4 * c + (s ^ 2);
                int X = i + (SX[s] < 0), Y = j + (SY[s] < 0);
                int k = HAS(X - 1, Y - 1) + HAS(X, Y - 1) + HAS(X - 1, Y) + HAS(X, Y);
                dec[q] = (k == 1 || k == 3) ? -1 : -2;
                for (int t = 0; t < ns; t++)
                    if (sx[t] == X && sy[t] == Y) {
                        if (k != 2 && k != 4) { fprintf(stderr, "source not regular\n"); return 1; }
                        dec[q] = (signed char)t;
                    }
            }
        static unsigned char reach[64][64];
        memset(reach, 0, sizeof reach);
        int npairs = ns * (ns - 1) / 2, nlit = 0;
        arena = malloc((size_t)cap * KEYLEN);
        tsize = 1; while (tsize < 2 * cap) tsize <<= 1;
        table = malloc(sizeof(long long) * tsize);
        for (long long i = 0; i < tsize; i++) table[i] = -1;
        nst = 0;
        unsigned char key[3 * MAXQ];
        canon(h, v, dec, key);
        insert(key);
        long long head = 0;
        int complete = 1;
        while (head < nst) {
            unsigned char cur[3 * MAXQ];
            memcpy(cur, arena + head * KEYLEN, KEYLEN); head++;
            unsigned char *H = cur, *Vv = cur + n; signed char *D = (signed char *)(cur + 2 * n);
            /* scan */
            for (int i = 0; i < n; i++) {
                int a = D[i];
                if (a < 0) continue;
                int c = H[i];
                while (c != i && D[c] != -1) {
                    int b = D[c];
                    if (b >= 0 && b != a && !reach[a][b]) { reach[a][b] = reach[b][a] = 1; nlit++; }
                    c = H[c];
                }
            }
            if (nlit == npairs) { complete = 0; break; }
            unsigned char hi[MAXQ], vi[MAXQ], a2[MAXQ], b2[MAXQ];
            for (int i = 0; i < n; i++) { hi[H[i]] = (unsigned char)i; vi[Vv[i]] = (unsigned char)i; }
            for (int mv = 0; mv < 4; mv++) {
                for (int i = 0; i < n; i++) {
                    switch (mv) {
                    case 0: a2[i] = H[i]; b2[i] = Vv[hi[i]]; break;
                    case 1: a2[i] = H[i]; b2[i] = Vv[H[i]]; break;
                    case 2: a2[i] = H[vi[i]]; b2[i] = Vv[i]; break;
                    default: a2[i] = H[Vv[i]]; b2[i] = Vv[i]; break;
                    }
                }
                canon(a2, b2, D, key);
                insert(key);
            }
        }
        printf("states %lld complete %d\n", nst, complete);
        for (int a = 0; a < ns; a++)
            for (int b = a + 1; b < ns; b++)
                printf("  %d %d %d %d %s\n", sx[a] - OFF, sy[a] - OFF, sx[b] - OFF, sy[b] - OFF, reach[a][b] ? "LIT" : "DARK");
        fflush(stdout);
        free(table); free(arena);
    }
    return 0;
}
