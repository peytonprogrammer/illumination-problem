/* d98: independent enumerator of the quotient shapes K (d64 README section 2).

   Objects: transitive W-sets on d cells, W = <V0, V1, H0, H1> (four involutions, fixed
   points are walls), up to relabelling of cells. For class (i, j) every <V_i, H_j>-orbit is
   cvx (path 1), smooth (path 2), rfx (path 3), cone (2-cycle) or int (4-cycle). Class (0,0)
   has only cvx, rfx, cone. z = #rfx over all classes, cone <= 1, cvx + 2 cone - z = 4.

   Algorithm (differs from enum_K.c, which grows a W-set cell by cell from one cell):
   fix d and the class-(0,0) skeleton first. Class (0,0) orbits are cvx, rfx, cone, so
   V0 and H0 are determined up to relabelling by (a, b, c) with a + 3b + 2c = d. Then
   assign V1 and H1 on the fixed d cells by backtracking, check classes (1,0), (0,1), (1,1),
   the global budget, transitivity, and dedupe with a DFS-based canonical form (not BFS).

   Usage:  ./skel enum ZWANT DMIN DMAX   -> one line per shape: "d z cone sing | canon"
           ./skel canon < enum_K-output  -> same line format for each input W-set
   Generator rows in canon are in the order V0 V1 H0 H1. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXD 20
enum { V0 = 0, V1 = 1, H0 = 2, H1 = 3 };
static int d, zwant;
static int G[4][MAXD];
static long long nodes, leaves;
/* skeleton symmetry: blk[c] = interchangeable block id (cvx cells: one block each, all of
   kind 0; rfx triples: kind 1); blkfirst[c] = first cell of c's block; kind[c] */
static int Z, CONE, CVX; /* complete-orbit counts, maintained incrementally */
static int kind[MAXD], blkfirst[MAXD], blklen[MAXD];

/* --- orbit analysis of <g, h> through cell c on a possibly partial W-set ---
   Returns length L; *cyc = 1 if closed; *nfix = number of fixed ends (0..2) for a path. */
static int orbit(int g, int h, int c, int *cyc, int *nfix, int *mark) {
    int L = 1;
    if (mark) mark[c] = 1;
    *cyc = 0; *nfix = 0;
    /* walk direction starting with g, then direction starting with h */
    int gens[2] = {g, h};
    for (int dir = 0; dir < 2; dir++) {
        int cur = c, gen = gens[dir];
        for (;;) {
            int nx = G[gen][cur];
            if (nx < 0) break;
            if (nx == cur) { (*nfix)++; break; }
            if (nx == c) { *cyc = 1; return L; }
            L++;
            if (mark) mark[nx] = 1;
            cur = nx;
            gen = (gen == g) ? h : g;
        }
    }
    return L;
}

/* 0 bad; else type code for complete orbits: 1 cvx 2 smooth 3 rfx 4 cone 5 int; 6 partial ok */
static int classify(int L, int cyc, int nfix, int nopen) {
    if (cyc) return L == 2 ? 4 : L == 4 ? 5 : 0;
    if (nopen == 0) return L <= 3 ? L : 0;
    if (nfix >= 1) return L <= 3 ? 6 : 0;
    return L <= 4 ? 6 : 0;
}

static int orbit_ok(int g, int h, int c, int only00) {
    int cyc, nfix;
    int L = orbit(g, h, c, &cyc, &nfix, NULL);
    int nopen = cyc ? 0 : 2 - nfix;
    int t = classify(L, cyc, nfix, nopen);
    if (!t) return 0;
    if (only00 && (t == 2 || t == 5)) return 0;
    return 1;
}

/* complete-orbit tallies over all four classes */
static int CLS[4][2] = {{V0, H0}, {V1, H0}, {V0, H1}, {V1, H1}};
static void tally(int *z, int *cone, int *cvx, int *sing) {
    int mark[MAXD];
    *z = *cone = *cvx = *sing = 0;
    for (int k = 0; k < 4; k++) {
        memset(mark, 0, sizeof mark);
        int s = 0;
        for (int c = 0; c < d; c++) {
            if (mark[c]) continue;
            int cyc, nfix;
            int L = orbit(CLS[k][0], CLS[k][1], c, &cyc, &nfix, mark);
            int nopen = cyc ? 0 : 2 - nfix;
            if (nopen) continue;
            int t = classify(L, cyc, nfix, 0);
            if (t == 1) { (*cvx)++; s = 1; }
            else if (t == 3) { (*z)++; s = 1; }
            else if (t == 4) { (*cone)++; s = 1; }
        }
        *sing += s;
    }
}

static int transitive(void) {
    int seen[MAXD] = {0}, st[MAXD], sp = 0, cnt = 1;
    seen[0] = 1; st[sp++] = 0;
    while (sp) {
        int u = st[--sp];
        for (int g = 0; g < 4; g++) {
            int v = G[g][u];
            if (!seen[v]) { seen[v] = 1; cnt++; st[sp++] = v; }
        }
    }
    return cnt == d;
}

/* --- DFS canonical form: min over start cells; generator visit order V1 H1 V0 H0 --- */
static const int ORD[4] = {V1, H1, V0, H0};
static int lab[MAXD], order_[MAXD], nlab;
static void dfs(int u) {
    lab[u] = nlab; order_[nlab++] = u;
    for (int k = 0; k < 4; k++) {
        int v = G[ORD[k]][u];
        if (lab[v] < 0) dfs(v);
    }
}
static void canon(int n, unsigned char *best) {
    unsigned char f[4 * MAXD];
    int have = 0;
    for (int s = 0; s < n; s++) {
        for (int i = 0; i < n; i++) lab[i] = -1;
        nlab = 0;
        dfs(s);
        for (int i = 0; i < n; i++)
            for (int g = 0; g < 4; g++) f[4 * i + g] = (unsigned char)lab[G[g][order_[i]]];
        if (!have || memcmp(f, best, 4 * n) < 0) { memcpy(best, f, 4 * n); have = 1; }
    }
}

/* --- hash set of forms (per d run; cleared between d) --- */
#define HBITS 24
static unsigned char (*hs)[4 * MAXD];
static char *used;
static long nset;
static int hs_insert(const unsigned char *f, int n) {
    unsigned long h = 1469598103934665603UL;
    for (int i = 0; i < 4 * n; i++) { h ^= f[i]; h *= 1099511628211UL; }
    long i = (long)(h & ((1L << HBITS) - 1));
    while (used[i]) {
        if (memcmp(hs[i], f, 4 * n) == 0) return 0;
        i = (i + 1) & ((1L << HBITS) - 1);
    }
    used[i] = 1; memcpy(hs[i], f, 4 * n); nset++;
    if (nset * 2 > (1L << HBITS)) { fprintf(stderr, "hash full\n"); exit(2); }
    return 1;
}

static void emit(int n, int z, int cone, int sing) {
    unsigned char f[4 * MAXD];
    canon(n, f);
    if (!hs_insert(f, n)) return;
    printf("%d %d %d %d |", n, z, cone, sing);
    for (int i = 0; i < 4 * n; i++) printf(" %d", f[i]);
    printf("\n");
}

static void leaf(void) {
    leaves++;
    int z, cone, cvx, sing;
    tally(&z, &cone, &cvx, &sing);
    if (z != zwant || cone > 1 || cvx + 2 * cone - z != 4) return;
    if (!transitive()) return;
    emit(d, z, cone, sing);
}

/* a block is untouched if none of its cells has V1 or H1 assigned */
static int untouched(int f) {
    for (int i = f; i < f + blklen[f]; i++) if (G[V1][i] != -1 || G[H1][i] != -1) return 0;
    return 1;
}
/* Symmetry breaking: if j lies in an untouched block, every untouched block of the same kind
   with a smaller first cell (and > c) could be swapped with it by a skeleton automorphism
   that fixes the partial assignment. Allow only the smallest such block. */
static int allowed_partner(int c, int j) {
    int f = blkfirst[j];
    if (f <= c || kind[j] > 1 || !untouched(f)) return 1;
    for (int i = c + 1; i < f; i++)
        if (blkfirst[i] == i && kind[i] == kind[j] && untouched(i)) return 0;
    return 1;
}
/* prune if the component of cell 0 has no unassigned slot but misses some cell */
static int closed_component(void) {
    int seen[MAXD] = {0}, st[MAXD], sp = 0, cnt = 1;
    seen[0] = 1; st[sp++] = 0;
    while (sp) {
        int u = st[--sp];
        for (int g = 0; g < 4; g++) {
            int v = G[g][u];
            if (v < 0) return 0;
            if (!seen[v]) { seen[v] = 1; cnt++; st[sp++] = v; }
        }
    }
    return cnt < d;
}

/* slots: index s -> cell s/2, generator V1 (s even) or H1 (s odd) */
static void rec(int s) {
    nodes++;
    while (s < 2 * d && G[(s & 1) ? H1 : V1][s >> 1] != -1) s++;
    if (s == 2 * d) { leaf(); return; }
    int c = s >> 1, g = (s & 1) ? H1 : V1;
    int other = (g == V1) ? H0 : V0; /* class (1,0) uses V1,H0 ; class (0,1) uses V0,H1 */
    int partner = (g == V1) ? H1 : V1;
    if (closed_component()) return;
    for (int j = c; j < d; j++) {
        if (G[g][j] != -1) continue;
        if (j > c && !allowed_partner(c, j)) continue;
        G[g][c] = j; G[g][j] = c;
        int ok = orbit_ok(g, other, c, 0) && orbit_ok(g, partner, c, 0);
        if (ok && j != c) ok = orbit_ok(g, other, j, 0) && orbit_ok(g, partner, j, 0);
        int dz = 0, dcone = 0, dcvx = 0;
        if (ok) {
            /* orbits completed by this assignment (both classes touched by g, cells c and j) */
            int reps[4], nr = 0;
            int gens[2][2] = {{g, other}, {g, partner}};
            int cells2[2] = {c, j};
            for (int k = 0; k < 2; k++)
                for (int t = 0; t < 2; t++) {
                    int cyc, nfix, mark[MAXD] = {0};
                    int L = orbit(gens[k][0], gens[k][1], cells2[t], &cyc, &nfix, mark);
                    if (!cyc && nfix < 2) continue;
                    int rep = 0;
                    while (!mark[rep]) rep++;
                    int dup = 0;
                    for (int q = 0; q < nr; q++) if (reps[q] == rep + MAXD * k) dup = 1;
                    if (dup) continue;
                    reps[nr++] = rep + MAXD * k;
                    int ty = classify(L, cyc, nfix, 0);
                    if (ty == 1) dcvx++; else if (ty == 3) dz++; else if (ty == 4) dcone++;
                }
            ok = Z + dz <= zwant && CONE + dcone <= 1 && CVX + dcvx + 2 * (CONE + dcone) <= zwant + 4;
        }
        Z += dz; CONE += dcone; CVX += dcvx;
        if (ok) rec(s + 1);
        Z -= dz; CONE -= dcone; CVX -= dcvx;
        G[g][c] = -1; G[g][j] = -1;
    }
}

static void run_skeleton(int a, int b, int c) {
    for (int g = 0; g < 4; g++) for (int i = 0; i < MAXD; i++) G[g][i] = -1;
    int k = 0;
    for (int i = 0; i < a; i++, k++) {
        G[V0][k] = k; G[H0][k] = k;
        kind[k] = 0; blkfirst[k] = k; blklen[k] = 1;
    }
    for (int i = 0; i < b; i++, k += 3) {
        G[V0][k] = k + 1; G[V0][k + 1] = k; G[V0][k + 2] = k + 2;
        G[H0][k] = k; G[H0][k + 1] = k + 2; G[H0][k + 2] = k + 1;
        for (int t = 0; t < 3; t++) { kind[k + t] = 1; blkfirst[k + t] = k; blklen[k + t] = 3; }
    }
    for (int i = 0; i < c; i++, k += 2) {
        G[V0][k] = k + 1; G[V0][k + 1] = k;
        G[H0][k] = k + 1; G[H0][k + 1] = k;
        kind[k] = kind[k + 1] = 2; blkfirst[k] = blkfirst[k + 1] = k; blklen[k] = blklen[k + 1] = 2;
    }
    Z = b; CONE = c; CVX = a;
    rec(0);
}

static void read_canon(void) {
    char line[4096];
    while (fgets(line, sizeof line, stdin)) {
        char *p = strchr(line, '|');
        if (!p) continue;
        d = atoi(line);
        p++;
        for (int g = 0; g < 4; g++) {
            for (int i = 0; i < d; i++) G[g][i] = (int)strtol(p, &p, 10);
            if (g < 3) p = strchr(p, ';') + 1;
        }
        /* enum_K row order is (V0, V1, H0, H1) by its comment "a = cls0, b = 2 + cls1" */
        int z, cone, cvx, sing;
        tally(&z, &cone, &cvx, &sing);
        unsigned char f[4 * MAXD];
        canon(d, f);
        printf("%d %d %d %d |", d, z, cone, sing);
        for (int i = 0; i < 4 * d; i++) printf(" %d", f[i]);
        printf("\n");
    }
}

int main(int argc, char **argv) {
    if (argc >= 2 && strcmp(argv[1], "canon") == 0) { read_canon(); return 0; }
    if (argc < 5) { fprintf(stderr, "usage\n"); return 1; }
    zwant = atoi(argv[2]);
    int dmin = atoi(argv[3]), dmax = atoi(argv[4]);
    hs = malloc((1L << HBITS) * sizeof *hs);
    used = malloc(1L << HBITS);
    for (d = dmin; d <= dmax; d++) {
        memset(used, 0, 1L << HBITS); nset = 0; nodes = leaves = 0;
        /* class (0,0): a cvx, b rfx, c cone; a + 3b + 2c = d, b <= zwant, c <= 1, a + 2c <= zwant + 4 */
        for (int b = 0; b <= zwant; b++)
            for (int c = 0; c <= 1; c++) {
                int a = d - 3 * b - 2 * c;
                if (a < 0 || a + 2 * c > zwant + 4) continue;
                run_skeleton(a, b, c);
            }
        fprintf(stderr, "z %d d %d shapes %ld nodes %lld leaves %lld\n", zwant, d, nset, nodes, leaves);
        fflush(stdout);
    }
    return 0;
}
