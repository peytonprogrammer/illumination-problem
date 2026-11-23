/* Exact illumination decider for marked square-tiled surfaces.

   Input (stdin, whitespace separated):
     N NSRC CAP VERBOSE
     NW  s1 t1  s2 t2 ...   wanted unordered pairs: stop early once all are lit
     h[0..N-1]      right neighbour of each square
     v[0..N-1]      upper neighbour of each square
     lab[0..N-1]    decoration of the lower-left corner of each square:
                    -1 = blocked (a polygon vertex), -2 = free, s >= 0 = source s
   The decorated surface's SL(2,Z) orbit is explored by breadth-first search
   with the generators
     U  : x' = x + y   h' = h,            v'[k] = v[hinv[k]]
     U^-1             h' = h,            v'[k] = v[h[k]]
     L  : y' = y + x   h'[k] = h[vinv[k]], v' = v
     L^-1             h'[k] = h[v[k]],    v' = v
   A square keeps the image of its lower-left corner, so decorations are fixed.
   States are stored up to decoration-preserving relabelling (canonical form:
   minimum over breadth-first numberings started at each lift of the
   lowest-numbered source). In every state the horizontal ray from each source
   lift is followed until it returns or meets a blocked point.
   The matrix M with state = M . original is tracked, so a ray of `steps`
   unit steps in the state is the original developing vector steps*(d, -c).

   Output:
     STATES n
     LIT s t steps dx dy      first witness found for each ordered pair (s,t)
     DONE (orbit exhausted), EARLY (all wanted pairs lit), or CAP
   With VERBOSE = 1 every state also prints "ST a b c d" and one line
   "R s t" per (source, reached source) seen in its horizontal scan.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int N, NSRC;
static long CAP;
static uint8_t *arena;          /* states: h[N] v[N] lab[N] */
static int64_t *mats;           /* 4 per state */
static long nstates, arena_cap;
static long *table;             /* open addressing: state index + 1, 0 = empty */
static long tsize;

static int reach[64][64], wanted[64][64], nwanted_left, VERB;

static uint64_t hashst(const uint8_t *s) {
    uint64_t x = 1469598103934665603ULL;
    for (int i = 0; i < 3 * N; i++) { x ^= s[i]; x *= 1099511628211ULL; }
    return x;
}

static void canon(const int *h, const int *v, const int *lab, uint8_t *out) {
    /* lab codes: 0 blocked, 1 free, 2+s source */
    static uint8_t cand[3 * 512];
    static int newid[512], order[512];
    int first = 1;
    for (int s = 0; s < N; s++) {
        if (lab[s] != 2) continue;
        for (int i = 0; i < N; i++) newid[i] = -1;
        int cnt = 0;
        newid[s] = 0; order[cnt++] = s;
        for (int q = 0; q < cnt; q++) {
            int a = order[q];
            int nb[2] = {v[a], h[a]};          /* visit up, then right */
            for (int t = 0; t < 2; t++)
                if (newid[nb[t]] < 0) { newid[nb[t]] = cnt; order[cnt++] = nb[t]; }
        }
        if (cnt != N) { fprintf(stderr, "surface not connected\n"); exit(2); }
        for (int i = 0; i < N; i++) {
            cand[i] = (uint8_t)newid[h[order[i]]];
            cand[N + i] = (uint8_t)newid[v[order[i]]];
            cand[2 * N + i] = (uint8_t)lab[order[i]];
        }
        if (first || memcmp(cand, out, 3 * N) < 0) { memcpy(out, cand, 3 * N); first = 0; }
    }
    if (first) { fprintf(stderr, "no lift of source 0\n"); exit(2); }
}

static long insert(const uint8_t *s, const int64_t *m) {
    uint64_t hv = hashst(s);
    long pos = (long)(hv & (uint64_t)(tsize - 1));
    while (table[pos]) {
        long id = table[pos] - 1;
        if (memcmp(arena + id * 3 * N, s, 3 * N) == 0) return -1;
        pos = (pos + 1) & (tsize - 1);
    }
    if (nstates >= arena_cap) return -2;
    memcpy(arena + nstates * 3 * N, s, 3 * N);
    memcpy(mats + nstates * 4, m, 4 * sizeof(int64_t));
    table[pos] = nstates + 1;
    nstates++;
    return nstates - 1;
}

static void matmul(const int64_t *L, const int64_t *M, int64_t *out) {
    int64_t r[4];
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++) {
            int64_t a, b, c;
            if (__builtin_mul_overflow(L[2 * i], M[j], &a) ||
                __builtin_mul_overflow(L[2 * i + 1], M[2 + j], &b) ||
                __builtin_add_overflow(a, b, &c)) { fprintf(stderr, "matrix overflow\n"); exit(3); }
            r[2 * i + j] = c;
        }
    memcpy(out, r, sizeof r);
}

int main(void) {
    if (scanf("%d %d %ld %d", &N, &NSRC, &CAP, &VERB) != 4) return 1;
    int nw; if (scanf("%d", &nw) != 1) return 1;
    for (int i = 0; i < nw; i++) {
        int a, b; if (scanf("%d %d", &a, &b) != 2) return 1;
        if (!wanted[a][b]) { wanted[a][b] = wanted[b][a] = 1; nwanted_left++; }
    }
    if (N > 255 || NSRC > 60) { fprintf(stderr, "too large\n"); return 1; }
    int h[512], v[512], lab[512], hi[512], vi[512], h2[512], v2[512];
    for (int i = 0; i < N; i++) scanf("%d", &h[i]);
    for (int i = 0; i < N; i++) scanf("%d", &v[i]);
    for (int i = 0; i < N; i++) { int x; scanf("%d", &x); lab[i] = x == -1 ? 0 : x == -2 ? 1 : 2 + x; }
    arena_cap = CAP;
    arena = malloc((size_t)arena_cap * 3 * N);
    mats = malloc((size_t)arena_cap * 4 * sizeof(int64_t));
    tsize = 1; while (tsize < 2 * arena_cap) tsize <<= 1;
    table = calloc((size_t)tsize, sizeof(long));
    if (!arena || !mats || !table) { fprintf(stderr, "alloc\n"); return 1; }
    uint8_t cur[3 * 512];
    int64_t ident[4] = {1, 0, 0, 1};
    canon(h, v, lab, cur);
    insert(cur, ident);
    static const int64_t G[4][4] = {{1, 1, 0, 1}, {1, -1, 0, 1}, {1, 0, 1, 1}, {1, 0, -1, 1}};
    int capped = 0;
    for (long q = 0; q < nstates; q++) {
        uint8_t *s = arena + q * 3 * N;
        int64_t M[4]; memcpy(M, mats + q * 4, sizeof M);
        int lb[512];
        for (int i = 0; i < N; i++) { h[i] = s[i]; v[i] = s[N + i]; lb[i] = s[2 * N + i]; }
        if (VERB) printf("ST %lld %lld %lld %lld\n", (long long)M[0], (long long)M[1], (long long)M[2], (long long)M[3]);
        /* scan horizontal rays */
        for (int k = 0; k < N; k++) {
            if (lb[k] < 2) continue;
            int src = lb[k] - 2, c = h[k], steps = 1;
            while (c != k && lb[c] != 0) {
                if (lb[c] >= 2) {
                    int t = lb[c] - 2;
                    if (VERB) printf("R %d %d\n", src, t);
                    if (t != src && !reach[src][t]) {
                        if (wanted[src][t] && !reach[t][src]) nwanted_left--;
                        reach[src][t] = 1;
                        /* M^-1 (1,0) = (d, -c) */
                        printf("LIT %d %d %d %lld %lld\n", src, t, steps,
                               (long long)M[3], (long long)-M[2]);
                    }
                }
                c = h[c]; steps++;
            }
        }
        if (nw > 0 && nwanted_left == 0) { printf("STATES %ld\nEARLY\n", nstates); return 0; }
        for (int i = 0; i < N; i++) { hi[h[i]] = i; vi[v[i]] = i; }
        for (int g = 0; g < 4; g++) {
            for (int i = 0; i < N; i++) {
                switch (g) {
                case 0: h2[i] = h[i]; v2[i] = v[hi[i]]; break;
                case 1: h2[i] = h[i]; v2[i] = v[h[i]]; break;
                case 2: h2[i] = h[vi[i]]; v2[i] = v[i]; break;
                default: h2[i] = h[v[i]]; v2[i] = v[i]; break;
                }
            }
            int64_t M2[4];
            matmul(G[g], M, M2);
            canon(h2, v2, lb, cur);
            long r = insert(cur, M2);
            if (r == -2) { capped = 1; break; }
        }
        if (capped) break;
    }
    printf("STATES %ld\n", nstates);
    printf(capped ? "CAP\n" : "DONE\n");
    return 0;
}
