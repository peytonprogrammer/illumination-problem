/* band2.c -- two-band covering certificates. Adapted from d28-band-stabilization/band.c (trace copied).
 * Skeleton: polyomino cells. Two distinct cell rows B1, B2 (same axis, so the bands are parallel) get
 * heights g1, g2 (odd); all other rows have height 1. Crossing a row of height h in a chord [a,b]
 * shifts the unfolded x by h*q/p mod 2(b-a), so direction (q,p) depends on (g1,g2) only through
 * (g1 mod 2*L1*p, g2 mod 2*L2*p), L_i = lcm of chord widths of row B_i (two-band Lemma B, README).
 * For p <= PMAX, every odd residue pair, every q in [0, QF*p] coprime to p (QF = lcm of all chord
 * widths; independent of g1, g2), every source and sign: follow the path to a corner or closure.
 * Certificate: smallest PC such that every odd residue pair mod (2 L1 lcm(1..PC), 2 L2 lcm(1..PC)) is
 * covered by some p <= PC. Computed by lifting the uncovered set U from level PC-1 to PC.
 * usage: band2 AXIS B1 B2 PMAX [dup1 dup2 [pairlist]] < room
 *   dup_i: duplicate row B_i dup_i extra times before stretching its lowest copy (total gap g_i + dup_i)
 *   pairlist: comma-separated pair indices to certify (default all)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define GS 40
#define UCAP 20000000LL
static int c[GS][GS], H_, B1, B2;
static int has(int x, int y) { return x >= 0 && y >= 0 && x < GS && y < GS && c[x][y]; }
static int npt, ptx[400], pty[400], pid[GS][GS];
static int npair, pa[4000], pb[4000], pidx[400][400];
static long long gcdl(long long a, long long b) { while (b) { long long t = a % b; a = b; b = t; } return a; }
static long long capHits = 0, nTraj = 0;
static unsigned char *hit;
static void trace(int s, int sx, int sy, int q, int p, long long g1, long long g2) {
    long long u = (long long)ptx[s] * p; int Y = pty[s];
    int sx0 = sx, sy0 = sy; long long steps = 0;
    nTraj++;
    for (;;) {
        if (steps > 0) {
            if (u % p == 0) {
                int x = (int)(u / p);
                int ll = has(x - 1, Y - 1), lr = has(x, Y - 1), ul = has(x - 1, Y), ur = has(x, Y), k = ll + lr + ul + ur;
                if (k == 1 || k == 3 || k == 0) return;
                if (k == 4) { int t = pid[x][Y]; if (t == s && sx == sx0 && sy == sy0) return; hit[t] = 1; }
                else { if ((ll && lr) || (ul && ur)) sy = -sy; else if ((ll && ul) || (lr && ur)) sx = -sx; else return; }
            } else {
                long long fx = u / p; int r = sy > 0 ? Y : Y - 1;
                if (!has((int)fx, r)) sy = -sy;
            }
        }
        if (++steps > 20000000) { capHits++; return; }
        int r = sy > 0 ? Y : Y - 1, col;
        if (u % p == 0) col = (int)(u / p) - (sx < 0); else col = (int)(u / p);
        if (!has(col, r)) { fprintf(stderr, "BUG no cell\n"); exit(1); }
        int a = col, b = col + 1; while (has(a - 1, r)) a--; while (has(b, r)) b++;
        long long wp = (long long)(b - a) * p, pos = u - (long long)a * p;
        long long v = sx > 0 ? pos : 2 * wp - pos;
        long long h = (r == B1) ? g1 : (r == B2) ? g2 : 1;
        v = (v + (h % (2 * wp)) * q) % (2 * wp);
        if (v > 0 && v <= wp) { pos = v; sx = 1; } else { pos = (2 * wp - v) % (2 * wp); sx = -1; }
        u = (long long)a * p + pos; Y += sy;
    }
}
static long long lcml(long long a, long long b) { return a / gcdl(a, b) * b; }
int main(int argc, char **argv) {
    int AX = atoi(argv[1]), b1 = atoi(argv[2]), b2 = atoi(argv[3]), PMAX = atoi(argv[4]);
    int d1 = argc > 5 ? atoi(argv[5]) : 0, d2 = argc > 6 ? atoi(argv[6]) : 0;
    int A; if (scanf("%d", &A) != 1) return 1;
    int cx[400], cy[400], ymax = 0;
    for (int i = 0; i < A; i++) { scanf("%d %d", &cx[i], &cy[i]); if (AX) { int t = cx[i]; cx[i] = cy[i]; cy[i] = t; } if (cy[i] > ymax) ymax = cy[i]; }
    /* new row index of each old row (lowest copy), copies */
    int base[GS], ny = 0;
    for (int y = 0; y <= ymax; y++) { base[y] = ny; ny += 1 + (y == b1 ? d1 : 0) + (y == b2 ? d2 : 0); }
    for (int i = 0; i < A; i++) { int y = cy[i], k = 1 + (y == b1 ? d1 : 0) + (y == b2 ? d2 : 0);
        for (int j = 0; j < k; j++) c[cx[i] + 1][base[y] + j + 1] = 1; }
    B1 = base[b1] + 1; B2 = base[b2] + 1;
    for (int x = 0; x < GS; x++) for (int y = 0; y < GS; y++) if (c[x][y] && y + 1 > H_) H_ = y + 1;
    memset(pid, -1, sizeof pid);
    for (int X = 1; X < GS; X++) for (int Y = 1; Y < GS; Y++) if (has(X - 1, Y - 1) + has(X, Y - 1) + has(X - 1, Y) + has(X, Y) == 4) { ptx[npt] = X; pty[npt] = Y; pid[X][Y] = npt++; }
    for (int i = 0; i < npt; i++) for (int j = i + 1; j < npt; j++) if (!((ptx[i] ^ ptx[j]) & 1) && !((pty[i] ^ pty[j]) & 1)) { pa[npair] = i; pb[npair] = j; pidx[i][j] = npair++; }
    long long L1 = 1, L2 = 1, QF = 1;
    for (int y = 0; y < H_; y++) for (int x = 0; x < GS; x++) if (c[x][y] && !has(x - 1, y)) { int b = x; while (has(b, y)) b++; long long w = b - x;
        QF = lcml(QF, w); if (y == B1) L1 = lcml(L1, w); if (y == B2) L2 = lcml(L2, w); }
    printf("# axis %d rows %d,%d dup %d,%d -> skeleton rows %d,%d  L1=%lld L2=%lld QF=%lld points %d pairs %d PMAX=%d\n",
        AX, b1, b2, d1, d2, B1 - 1, B2 - 1, L1, L2, QF, npt, npair, PMAX);
    for (int i = 0; i < npair; i++) printf("# pair %d (%d,%d)-(%d,%d)\n", i, ptx[pa[i]] - 1, pty[pa[i]] - 1, ptx[pb[i]] - 1, pty[pb[i]] - 1);
    unsigned char *sel = calloc(npair, 1);
    if (argc > 7) { char *t = strtok(argv[7], ","); while (t) { int k = atoi(t); if (k >= 0 && k < npair) sel[k] = 1; t = strtok(NULL, ","); } }
    else memset(sel, 1, npair);
    /* horizontal p = 0 witness: constant in (g1, g2) */
    unsigned char *lit0 = calloc(npair, 1);
    for (int i = 0; i < npair; i++) if (pty[pa[i]] == pty[pb[i]]) { int ok = 1, x0 = ptx[pa[i]], x1 = ptx[pb[i]]; if (x0 > x1) { int t = x0; x0 = x1; x1 = t; }
        for (int x = x0 + 1; x < x1; x++) if (pid[x][pty[pa[i]]] < 0) ok = 0; lit0[i] = ok; }
    hit = malloc(npt);
    if (getenv("PT")) { long long g1, g2; sscanf(getenv("PT"), "%lld,%lld", &g1, &g2);
        for (int i = 0; i < npair; i++) { int mp = lit0[i] ? 0 : -1;
            for (int p = 1; p <= PMAX && mp < 0; p++) for (int q = 0; q <= QF * p && mp < 0; q++) { if (gcdl(q, p) != 1) continue;
                for (int s = 0; s < npt && mp < 0; s++) for (int sg = 0; sg < 4; sg++) { if (q == 0 && (sg & 1)) continue;
                    memset(hit, 0, npt); trace(s, (sg & 1) ? -1 : 1, (sg & 2) ? -1 : 1, q, p, g1, g2);
                    int t1 = pa[i] == s ? pb[i] : pb[i] == s ? pa[i] : -1; if (t1 >= 0 && hit[t1]) { mp = p; break; } } }
            printf("PT %lld %lld %d %d\n", g1, g2, i, mp); }
        return 0; }
    /* uncovered sets per pair: residues (a, b) mod (Q1, Q2), odd */
    long long Q1 = 2 * L1, Q2 = 2 * L2, lc = 1;
    int **Ua = malloc(sizeof(int *) * npair), **Ub = malloc(sizeof(int *) * npair); long long *Un = calloc(npair, sizeof(long long));
    int *done = calloc(npair, sizeof(int)), aborted = 0, lastP = 0;
    if (b1 == b2) { fprintf(stderr, "rows must differ\n"); return 1; }
    for (int i = 0; i < npair; i++) { Ua[i] = Ub[i] = NULL; if (!sel[i]) continue; if (lit0[i]) { done[i] = -1; continue; }
        Ua[i] = malloc(sizeof(int) * Q1 * Q2); Ub[i] = malloc(sizeof(int) * Q1 * Q2);
        for (long long a = 1; a < Q1; a += 2) for (long long b = 1; b < Q2; b += 2) { Ua[i][Un[i]] = (int)a; Ub[i][Un[i]] = (int)b; Un[i]++; } }
    for (int p = 1; p <= PMAX && !aborted; p++) {
        int need = 0; for (int i = 0; i < npair; i++) if (sel[i] && !done[i]) need = 1; if (!need) break;
        long long M1 = 2 * L1 * p, M2 = 2 * L2 * p, h1 = M1 / 2, h2 = M2 / 2;
        unsigned char *tab = calloc((size_t)h1 * h2 * npair, 1);
        for (long long r1 = 1; r1 < M1; r1 += 2) for (long long r2 = 1; r2 < M2; r2 += 2) {
            unsigned char *row = tab + ((r1 / 2) * h2 + r2 / 2) * npair;
            for (int q = 0; q <= QF * p; q++) { if (gcdl(q, p) != 1) continue;
                for (int s = 0; s < npt; s++) for (int sg = 0; sg < 4; sg++) { if (q == 0 && (sg & 1)) continue;
                    memset(hit, 0, npt); trace(s, (sg & 1) ? -1 : 1, (sg & 2) ? -1 : 1, q, p, r1, r2);
                    for (int t = 0; t < npt; t++) if (hit[t] && t != s) { int a = s < t ? s : t, b = s < t ? t : s;
                        if (!((ptx[a] ^ ptx[b]) & 1) && !((pty[a] ^ pty[b]) & 1)) row[pidx[a][b]] = 1; } } }
        }
        long long nlc = lcml(lc, p), k = nlc / lc, nQ1 = 2 * L1 * nlc, nQ2 = 2 * L2 * nlc;
        for (int i = 0; i < npair; i++) { if (!sel[i] || done[i]) continue;
            if (Un[i] * k * k > UCAP) { printf("# pair %d: lifted set %lld exceeds cap at p=%d; stop\n", i, Un[i] * k * k, p); aborted = 1; break; }
            int *na = malloc(sizeof(int) * (Un[i] * k * k + 1)), *nb = malloc(sizeof(int) * (Un[i] * k * k + 1)); long long m = 0;
            for (long long e = 0; e < Un[i]; e++) for (long long j1 = 0; j1 < k; j1++) for (long long j2 = 0; j2 < k; j2++) {
                long long a = Ua[i][e] + j1 * Q1, b = Ub[i][e] + j2 * Q2;
                if (!tab[(((a % M1) / 2) * h2 + (b % M2) / 2) * npair + i]) { na[m] = (int)a; nb[m] = (int)b; m++; } }
            free(Ua[i]); free(Ub[i]); Ua[i] = na; Ub[i] = nb; Un[i] = m;
            printf("L p=%d pair %d Q=(%lld,%lld) uncovered %lld of %lld\n", p, i, nQ1, nQ2, m, (nQ1 / 2) * (nQ2 / 2));
            if (m <= (getenv("ULMAX") ? atoll(getenv("ULMAX")) : 64)) for (long long e = 0; e < m; e++) printf("UL %d %d %d %d\n", p, i, na[e], nb[e]);
            if (!m) done[i] = p; }
        if (!aborted) { lc = nlc; Q1 = nQ1; Q2 = nQ2; lastP = p; }
        free(tab); fflush(stdout);
    }
    for (int i = 0; i < npair; i++) { if (!sel[i]) continue;
        if (done[i] == -1) { printf("C %d cover P=0 (horizontal)\n", i); continue; }
        if (done[i]) { printf("C %d cover P=%d\n", i, done[i]); continue; }
        /* structure of U: slit lines (total gap g+dup = 0 mod Q), distinct coordinates, sample */
        long long s1 = 0, s2 = 0, n1 = 0, n2 = 0; char *seen1 = calloc(Q1, 1), *seen2 = calloc(Q2, 1);
        for (long long e = 0; e < Un[i]; e++) { if ((Ua[i][e] + d1) % Q1 == 0) s1++; if ((Ub[i][e] + d2) % Q2 == 0) s2++;
            if (!seen1[Ua[i][e]]++) n1++; if (!seen2[Ub[i][e]]++) n2++; }
        printf("C %d nocover at P=%d Q=(%lld,%lld) uncovered %lld; on slit line g1+dup1=0: %lld, g2+dup2=0: %lld; distinct g1 %lld, g2 %lld; sample",
            i, lastP, Q1, Q2, Un[i], s1, s2, n1, n2);
        for (long long e = 0; e < Un[i] && e < 12; e++) printf(" (%d,%d)", Ua[i][e], Ub[i][e]); printf("\n");
        if (Un[i] <= 500) for (long long e = 0; e < Un[i]; e++) printf("U %d %d %d\n", i, Ua[i][e], Ub[i][e]);
        free(seen1); free(seen2); }
    printf("# trajectories %lld capHits %lld\n", nTraj, capHits);
    return 0;
}
