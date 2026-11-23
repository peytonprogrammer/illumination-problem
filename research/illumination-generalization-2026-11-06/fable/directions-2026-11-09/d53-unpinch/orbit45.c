/* orbit45.c -- complete SL(2,Z)-orbit LIT/DARK decider for a marked origami.
 *
 * Generic-input port of d9's orbitc.c (same moves, scan and canonical form).
 * Input on stdin, one problem per line:
 *   nsq h[0..nsq-1] v[0..nsq-1] dec[0..nsq-1] [# comment]
 * h = right neighbour, v = up neighbour.  dec = 0 (S), 1 (T), -1 (corner:
 * the bottom-left corner is a polygon vertex), -2 (free).  Every lift of S
 * and of T must carry its label (shoot45 writes such lines for survivors).
 *
 * The four shears h'=h, v'=v o h^-1 / v o h and h'=h o v^-1 / h o v, v'=v keep
 * every square's bottom-left corner, so labels never change.  States are
 * stored up to label-preserving relabelling (BFS numbering, h before v, from
 * every square labelled 0; lexicographic minimum).  Scan of a state: from
 * each square labelled 0, follow h until a corner label or the start; a square
 * labelled 1 on the way is a LIT witness (in some primitive direction).  The
 * full orbit covers every primitive direction, so a finished orbit with no
 * witness is a complete DARK decision.
 *
 * usage: orbit45 CAP < problems     (CAP = maximum number of states)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXQ 200
static int n, KEYLEN;
static unsigned char *arena;
static long long nst, cap;
static long long *table;
static long long tsize;

static uint64_t hashk(const unsigned char *k) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < KEYLEN; i++) { h ^= k[i]; h *= 1099511628211ULL; }
    return h;
}
static int insert(const unsigned char *k) {
    uint64_t h = hashk(k) & (tsize - 1);
    while (table[h] >= 0) {
        if (!memcmp(arena + table[h] * KEYLEN, k, KEYLEN)) return 0;
        h = (h + 1) & (tsize - 1);
    }
    if (nst >= cap) return -1;
    memcpy(arena + nst * KEYLEN, k, KEYLEN);
    table[h] = nst++;
    return 1;
}
static void canon(const unsigned char *h, const unsigned char *v, const signed char *dec, unsigned char *best) {
    unsigned char key[3 * MAXQ];
    int num[MAXQ], order[MAXQ], have = 0;
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
    static char line[1 << 16];
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        char *p = line;
        n = (int)strtol(p, &p, 10);
        if (n > MAXQ) { fprintf(stderr, "too many squares\n"); return 1; }
        KEYLEN = 3 * n;
        unsigned char h[MAXQ], v[MAXQ]; signed char dec[MAXQ];
        for (int i = 0; i < n; i++) h[i] = (unsigned char)strtol(p, &p, 10);
        for (int i = 0; i < n; i++) v[i] = (unsigned char)strtol(p, &p, 10);
        for (int i = 0; i < n; i++) dec[i] = (signed char)strtol(p, &p, 10);
        /* keep the connected component of the first S-square.  The unfolding is
         * disconnected when the wall reflections generate a proper subgroup of D4
         * (rooms with only axis-parallel walls); the components are mirror images
         * of each other, so one component decides the pair. */
        {
            int comp[MAXQ], order[MAXQ], len = 0, s0 = -1;
            for (int i = 0; i < n; i++) { comp[i] = -1; if (s0 < 0 && dec[i] == 0) s0 = i; }
            if (s0 < 0) { fprintf(stderr, "no S square\n"); return 3; }
            comp[s0] = 0; order[len++] = s0;
            for (int k = 0; k < len; k++) {
                int x = order[k];
                if (comp[h[x]] < 0) { comp[h[x]] = len; order[len++] = h[x]; }
                if (comp[v[x]] < 0) { comp[v[x]] = len; order[len++] = v[x]; }
            }
            if (len < n) {
                unsigned char h2[MAXQ], v2[MAXQ]; signed char d2[MAXQ];
                for (int k = 0; k < len; k++) { int x = order[k]; h2[k] = (unsigned char)comp[h[x]]; v2[k] = (unsigned char)comp[v[x]]; d2[k] = dec[x]; }
                fprintf(stderr, "component %d of %d squares\n", len, n);
                n = len; KEYLEN = 3 * n;
                memcpy(h, h2, n); memcpy(v, v2, n); memcpy(dec, d2, n);
            }
        }
        char *cm = strchr(p, '#');
        if (cm) { char *e = strchr(cm, '\n'); if (e) *e = 0; }
        arena = malloc((size_t)cap * KEYLEN);
        tsize = 1; while (tsize < 2 * cap) tsize <<= 1;
        table = malloc(sizeof(long long) * tsize);
        if (!arena || !table) { fprintf(stderr, "out of memory\n"); return 5; }
        for (long long i = 0; i < tsize; i++) table[i] = -1;
        nst = 0;
        unsigned char key[3 * MAXQ];
        canon(h, v, dec, key);
        insert(key);
        long long head = 0;
        int lit = 0, capped = 0;
        while (head < nst) {
            unsigned char cur[3 * MAXQ];
            memcpy(cur, arena + head * KEYLEN, KEYLEN); head++;
            unsigned char *H = cur, *Vv = cur + n; signed char *D = (signed char *)(cur + 2 * n);
            for (int i = 0; i < n && !lit; i++) {
                if (D[i] != 0) continue;
                int c = H[i];
                while (c != i && D[c] != -1) { if (D[c] == 1) { lit = 1; break; } c = H[c]; }
            }
            if (lit) break;
            unsigned char hi[MAXQ], vi[MAXQ], a2[MAXQ], b2[MAXQ];
            for (int i = 0; i < n; i++) { hi[H[i]] = (unsigned char)i; vi[Vv[i]] = (unsigned char)i; }
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
            if (capped) break;
        }
        const char *verdict = lit ? "LIT" : capped ? "UNDECIDED_CAP" : "DARK";
        printf("states %lld %s %s\n", nst, verdict, cm ? cm : "");
        fflush(stdout);
        free(table); free(arena);
    }
    return 0;
}
