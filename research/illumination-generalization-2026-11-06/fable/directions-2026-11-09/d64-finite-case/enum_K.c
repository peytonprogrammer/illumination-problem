/* d64: C port of d52 enum_K.py (same search, same pruning, same canonical form).
   Enumerates transitive W-sets K (W = <V0,V1,H0,H1>, d <= dmax cells) whose <V_i,H_j>-orbits
   are cvx/smooth/rfx/cone/int, class x = (0,0) has only cvx/rfx/cone orbits, at most zmax rfx,
   at most one cone, cvx + 2 cone <= zmax + 4; leaves must have genus 0 (p - z = 4).
   Output: one canonical form per line, "d z cone p | g0 row ; g1 row ; g2 row ; g3 row".
   Build: cc -O2 -o enum_K enum_K.c ; run: ./enum_K zmax dmax > out.txt */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DM 24
enum { CVX = 1, SMOOTH = 2, RFX = 4, CONE = 8, INT = 16 };
static int G[4][DM];
static int zmax, dmax;
static long long nodes = 0;
/* classes (0,0),(1,0),(0,1),(1,1): generators a = cls0, b = 2 + cls1 */
static const int CA[4] = {0, 1, 0, 1}, CB[4] = {2, 2, 3, 3};
static const int ALLOWED[4] = {CVX | RFX | CONE, 31, 31, 31};
/* classes touched by generator g */
static const int CLS_OF_GEN[4][2] = {{0, 2}, {1, 3}, {0, 1}, {2, 3}};

/* trace: returns length; *closed = 1 if cycle; else endF/endB: 1 fixed, 0 open */
static int trace(int a, int b, int c0, int *cells, int *closed, int *endF, int *endB) {
    int L = 0, cur = c0, g = a, nxt;
    int fw[64], bk[64], nf = 0, nb = 0;
    fw[nf++] = c0;
    *closed = 0;
    for (;;) {
        nxt = G[g][cur];
        if (nxt == -1) { *endF = 0; break; }
        if (nxt == cur) { *endF = 1; break; }
        if (nxt == c0) { *closed = 1; break; }
        fw[nf++] = nxt;
        cur = nxt;
        g = (g == a) ? b : a;
    }
    if (*closed) {
        if (cells) memcpy(cells, fw, nf * sizeof(int));
        return nf;
    }
    cur = c0; g = b;
    for (;;) {
        nxt = G[g][cur];
        if (nxt == -1) { *endB = 0; break; }
        if (nxt == cur) { *endB = 1; break; }
        bk[nb++] = nxt;
        cur = nxt;
        g = (g == a) ? b : a;
    }
    if (cells) {
        for (int i = 0; i < nb; i++) cells[L++] = bk[nb - 1 - i];
        for (int i = 0; i < nf; i++) cells[L++] = fw[i];
    }
    return nf + nb;
}

/* type of a complete orbit, 0 if invalid, -1 if partial */
static int otype(int L, int closed, int eF, int eB) {
    if (closed) return L == 2 ? CONE : L == 4 ? INT : 0;
    if (eF && eB) return L == 1 ? CVX : L == 2 ? SMOOTH : L == 3 ? RFX : 0;
    return -1;
}

static int partial_ok(int L, int closed, int eF, int eB, int allowed) {
    if (closed) {
        int t = L == 2 ? CONE : L == 4 ? INT : 0;
        return t && (t & allowed);
    }
    int nf = eF + eB;
    if (nf == 2) {
        int t = L == 1 ? CVX : L == 2 ? SMOOTH : L == 3 ? RFX : 0;
        return t && (t & allowed);
    }
    if (nf == 1)
        return ((allowed & CVX) && L <= 1) || ((allowed & SMOOTH) && L <= 2) || ((allowed & RFX) && L <= 3);
    return ((allowed & CVX) && L <= 1) || ((allowed & SMOOTH) && L <= 2) || ((allowed & RFX) && L <= 3) ||
           ((allowed & CONE) && L <= 2) || ((allowed & INT) && L <= 4);
}

static int local_ok(const int *touched, int nt, int g) {
    for (int k = 0; k < 2; k++) {
        int cls = CLS_OF_GEN[g][k];
        for (int i = 0; i < nt; i++) {
            int cl, eF = 0, eB = 0;
            int L = trace(CA[cls], CB[cls], touched[i], NULL, &cl, &eF, &eB);
            if (!partial_ok(L, cl, eF, eB, ALLOWED[cls])) return 0;
        }
    }
    return 1;
}

/* counts over cells 0..n-1; returns z, cone, cvx via pointers; *bad if a complete orbit is invalid */
static void counts(int n, int *z, int *cone, int *cvx, int *bad) {
    int cells[64];
    *z = *cone = *cvx = *bad = 0;
    for (int cls = 0; cls < 4; cls++) {
        char seen[DM] = {0};
        for (int c = 0; c < n; c++) {
            if (seen[c]) continue;
            int cl, eF = 0, eB = 0;
            int L = trace(CA[cls], CB[cls], c, cells, &cl, &eF, &eB);
            for (int i = 0; i < L; i++) seen[cells[i]] = 1;
            int t = otype(L, cl, eF, eB);
            if (t == RFX) (*z)++;
            else if (t == CONE) (*cone)++;
            else if (t == CVX) (*cvx)++;
            else if (t == 0) *bad = 1;
        }
    }
}

static int counts_ok(int n) {
    int z, cone, cvx, bad;
    counts(n, &z, &cone, &cvx, &bad);
    return z <= zmax && cone <= 1 && cvx + 2 * cone <= zmax + 4;
}

/* ---- canonical form and hash set ---- */
typedef struct { unsigned char f[4 * DM]; int d; } Form;
static Form *store = NULL;
static long nstore = 0, capstore = 0;
static long *table = NULL;
static long tabsize = 1L << 22;

static void canon(int n, unsigned char *best) {
    unsigned char form[4 * DM];
    int lab[DM], order[DM];
    int have = 0;
    for (int s = 0; s < n; s++) {
        for (int i = 0; i < n; i++) lab[i] = -1;
        int len = 0, k = 0;
        lab[s] = 0; order[len++] = s;
        while (k < len) {
            int u = order[k++];
            for (int g = 0; g < 4; g++) {
                int v = G[g][u];
                if (lab[v] < 0) { lab[v] = len; order[len++] = v; }
            }
        }
        for (int g = 0; g < 4; g++)
            for (int i = 0; i < n; i++) form[g * n + i] = (unsigned char)lab[G[g][order[i]]];
        if (!have || memcmp(form, best, 4 * n) < 0) { memcpy(best, form, 4 * n); have = 1; }
    }
}

static unsigned long hashf(const unsigned char *f, int len) {
    unsigned long h = 1469598103934665603UL;
    for (int i = 0; i < len; i++) { h ^= f[i]; h *= 1099511628211UL; }
    return h;
}

static void insert(int n) {
    unsigned char best[4 * DM];
    canon(n, best);
    unsigned long h = hashf(best, 4 * n) ^ (unsigned long)n * 0x9E3779B97F4A7C15UL;
    long i = (long)(h & (tabsize - 1));
    while (table[i] >= 0) {
        Form *F = &store[table[i]];
        if (F->d == n && memcmp(F->f, best, 4 * n) == 0) return;
        i = (i + 1) & (tabsize - 1);
    }
    if (nstore == capstore) {
        capstore = capstore ? 2 * capstore : 4096;
        store = realloc(store, capstore * sizeof(Form));
    }
    memcpy(store[nstore].f, best, 4 * n);
    store[nstore].d = n;
    table[i] = nstore++;
    if (nstore * 2 > tabsize) { fprintf(stderr, "hash table full\n"); exit(2); }
}

static void leaf(int n) {
    int z, cone, cvx, bad;
    counts(n, &z, &cone, &cvx, &bad);
    if (bad) return;
    /* every orbit is complete at a leaf; recount partials as a check */
    if (cvx + 2 * cone - z != 4) return;
    insert(n);
}

static void rec(int n, int ptr) {
    nodes++;
    while (ptr < 4 * n && G[ptr % 4][ptr / 4] != -1) ptr++;
    if (ptr == 4 * n) { leaf(n); return; }
    int c = ptr / 4, g = ptr % 4;
    int t[2];
    /* wall */
    G[g][c] = c;
    t[0] = c;
    if (local_ok(t, 1, g) && counts_ok(n)) rec(n, ptr + 1);
    G[g][c] = -1;
    /* glue to an existing later cell with a free g-slot */
    for (int c2 = c + 1; c2 < n; c2++) {
        if (G[g][c2] != -1) continue;
        G[g][c] = c2; G[g][c2] = c;
        t[0] = c; t[1] = c2;
        if (local_ok(t, 2, g) && counts_ok(n)) rec(n, ptr + 1);
        G[g][c] = -1; G[g][c2] = -1;
    }
    /* new cell */
    if (n < dmax) {
        G[g][c] = n; G[g][n] = c;
        t[0] = c; t[1] = n;
        if (local_ok(t, 2, g) && counts_ok(n + 1)) rec(n + 1, ptr + 1);
        G[g][c] = -1; G[g][n] = -1;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: enum_K zmax dmax\n"); return 1; }
    zmax = atoi(argv[1]); dmax = atoi(argv[2]);
    if (dmax > DM) return 1;
    table = malloc(tabsize * sizeof(long));
    for (long i = 0; i < tabsize; i++) table[i] = -1;
    for (int g = 0; g < 4; g++) for (int i = 0; i < DM; i++) G[g][i] = -1;
    rec(1, 0);
    for (long k = 0; k < nstore; k++) {
        Form *F = &store[k];
        int n = F->d;
        printf("%d |", n);
        for (int g = 0; g < 4; g++) {
            for (int i = 0; i < n; i++) printf(" %d", F->f[g * n + i]);
            if (g < 3) printf(" ;");
        }
        printf("\n");
    }
    fprintf(stderr, "zmax %d dmax %d genus0 shapes %ld nodes %lld\n", zmax, dmax, nstore, nodes);
    return 0;
}
