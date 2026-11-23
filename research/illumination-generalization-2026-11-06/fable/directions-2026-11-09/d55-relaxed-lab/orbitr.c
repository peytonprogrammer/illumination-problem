/* orbitr.c -- d55 copy of d9 orbitc.c with the unfolding built by the caller.
 *
 * Same algorithm as d9-census-w22/orbitc.c: SL(2,Z) orbit of the marked
 * origami under the four shears, states canonical up to label-preserving
 * relabelling (BFS, h before v, from every square carrying source 0); each
 * state's horizontal rays from source squares are scanned; a ray stops at a
 * square whose bottom-left label is -1 (cone point) or on return.
 *
 * Change against orbitc.c: the caller (lab.py) passes h, v and the decoration,
 * so walls inside the room (slits) and per-sector cone types (slit tip, pinch,
 * T-foot) are decided in Python.  A cap overflow no longer exits: it reports
 * CAP and the pairs reached so far.
 *
 * Input, one problem per line:  n ns h[0..n-1] v[0..n-1] dec[0..n-1]
 *   dec: source index >= 0, -1 cone point (stops rays), -2 free regular point.
 * Output per problem:  STATUS nstates nunreached i j i j ...
 *   STATUS = ALLLIT (every source pair reached; stopped early),
 *            FULL   (orbit exhausted; unreached pairs are DARK),
 *            CAP    (state cap hit; unreached pairs are UNDECIDED).
 * Memory: arena is allocated for CAP states of the largest key (lazy pages),
 * the hash table is reset slot by slot.
 * usage: orbitr CAP < problems
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXQ 255
#define MAXS 128
static int n, KEYLEN;
static unsigned char *arena;
static long long nst, cap;
static long long *table; static long long tsize; static long long *used;
static unsigned char reach[MAXS][MAXS];

static uint64_t hashk(const unsigned char *k) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < KEYLEN; i++) { h ^= k[i]; h *= 1099511628211ULL; }
    return h;
}

/* 1 new, 0 seen, -1 cap */
static int insert(const unsigned char *k) {
    uint64_t h = hashk(k) & (tsize - 1);
    while (table[h] >= 0) {
        if (!memcmp(arena + table[h] * KEYLEN, k, KEYLEN)) return 0;
        h = (h + 1) & (tsize - 1);
    }
    if (nst >= cap) return -1;
    memcpy(arena + nst * KEYLEN, k, KEYLEN);
    used[nst] = (long long)h;
    table[h] = nst++;
    return 1;
}

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
    if (!have) { fprintf(stderr, "no anchor\n"); exit(5); }
}

int main(int argc, char **argv) {
    cap = argc > 1 ? atoll(argv[1]) : 1000000;
    arena = malloc((size_t)cap * 3 * MAXQ);
    tsize = 1; while (tsize < 2 * cap) tsize <<= 1;
    table = malloc(sizeof(long long) * tsize);
    used = malloc(sizeof(long long) * cap);
    if (!arena || !table || !used) { fprintf(stderr, "alloc\n"); return 2; }
    for (long long i = 0; i < tsize; i++) table[i] = -1;
    nst = 0;
    static char line[1 << 16];
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        char *p = line;
        n = (int)strtol(p, &p, 10);
        int ns = (int)strtol(p, &p, 10);
        if (n > MAXQ || ns > MAXS || ns < 2) { fprintf(stderr, "size\n"); return 1; }
        KEYLEN = 3 * n;
        unsigned char h[MAXQ], v[MAXQ]; signed char dec[MAXQ];
        for (int i = 0; i < n; i++) h[i] = (unsigned char)strtol(p, &p, 10);
        for (int i = 0; i < n; i++) v[i] = (unsigned char)strtol(p, &p, 10);
        for (int i = 0; i < n; i++) dec[i] = (signed char)strtol(p, &p, 10);
        for (int a = 0; a < ns; a++) memset(reach[a], 0, ns);
        int npairs = ns * (ns - 1) / 2, nlit = 0;
        for (long long i = 0; i < nst; i++) table[used[i]] = -1;
        nst = 0;
        unsigned char key[3 * MAXQ];
        canon(h, v, dec, key);
        insert(key);
        long long head = 0;
        const char *status = "FULL";
        while (head < nst) {
            unsigned char cur[3 * MAXQ];
            memcpy(cur, arena + head * KEYLEN, KEYLEN); head++;
            unsigned char *H = cur, *Vv = cur + n; signed char *D = (signed char *)(cur + 2 * n);
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
            if (nlit == npairs) { status = "ALLLIT"; break; }
            unsigned char hi[MAXQ], vi[MAXQ], a2[MAXQ], b2[MAXQ];
            for (int i = 0; i < n; i++) { hi[H[i]] = (unsigned char)i; vi[Vv[i]] = (unsigned char)i; }
            int capped = 0;
            for (int mv = 0; mv < 4 && !capped; mv++) {
                for (int i = 0; i < n; i++) {
                    switch (mv) {
                    case 0: a2[i] = H[i]; b2[i] = Vv[hi[i]]; break;
                    case 1: a2[i] = H[i]; b2[i] = Vv[H[i]]; break;
                    case 2: a2[i] = H[vi[i]]; b2[i] = Vv[i]; break;
                    default: a2[i] = H[Vv[i]]; b2[i] = Vv[i]; break;
                    }
                }
                canon(a2, b2, D, key);
                if (insert(key) < 0) capped = 1;
            }
            if (capped) { status = "CAP"; break; }
        }
        printf("%s %lld %d", status, nst, npairs - nlit);
        for (int a = 0; a < ns; a++)
            for (int b = a + 1; b < ns; b++)
                if (!reach[a][b]) printf(" %d %d", a, b);
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
