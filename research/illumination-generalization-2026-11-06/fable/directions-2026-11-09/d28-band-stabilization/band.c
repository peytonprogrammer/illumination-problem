/* band.c -- exact band-twist tracer for one stretched row of an orthogonal lattice room.
 * Skeleton: polyomino cells. Row CB (cell row index) is given height g >= 1; all other rows have height 1.
 * Tracked points: interior lattice points of the skeleton (never inside the stretched row).
 * A billiard path with primitive direction (+-q, +-p), p >= 1, is traced level by level; x is kept as u/p.
 * Crossing a row of height h in a chord [a,b] shifts the unfolded x by h*q/p modulo 2(b-a).  So the
 * behaviour for direction (q,p) depends on g only through g mod 2*L*p, L = lcm(chord widths of row CB).
 * For every p <= PMAX, every residue of g mod 2Lp, every q in [0, QF*p] coprime to p (QF = lcm of all
 * chord widths of all rows: the horizontal multi-twist by 2*QF fixes all lattice points), every source
 * and sign pair, the path is followed until it meets a corner or returns to its start (complete test).
 * usage: band AXIS CB PMAX GMAX [dup] < room   (room: "A x0 y0 x1 y1 ..."; AXIS=1 transposes first;
 *        dup=k duplicates row CB k extra times in the skeleton before stretching the lowest copy)
 * output: "G g pair minp q" for every odd g <= GMAX and pair; minp=-1 when no witness with p<=PMAX,
 *         then N_min separation flag (1 = separated = proved dark by the cited lemma).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define GS 40
static int c[GS][GS], W_, H_, CB;
static int has(int x, int y) { return x >= 0 && y >= 0 && x < GS && y < GS && c[x][y]; }
static int npt, ptx[400], pty[400], pid[GS][GS];
static int npair, pa[4000], pb[4000], pidx[400][400];
static long long gcdl(long long a, long long b) { while (b) { long long t = a % b; a = b; b = t; } return a; }
static long long capHits = 0, nTraj = 0;
static unsigned char *hit; /* per trajectory: target marks */
/* trace from point s with signs; g = height of row CB; marks hit[t]=1 for interior tracked points met */
static void trace(int s, int sx, int sy, int q, int p, long long g) {
    long long u = (long long)ptx[s] * p; int Y = pty[s];
    int sx0 = sx, sy0 = sy; long long steps = 0;
    nTraj++;
    for (;;) {
        /* at level Y, x = u/p, about to move in direction (sx,sy); handle the point first unless start */
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
        long long h = (r == CB) ? g : 1;
        v = (v + (h % (2 * wp)) * q) % (2 * wp);
        if (v > 0 && v <= wp) { pos = v; sx = 1; } else { pos = (2 * wp - v) % (2 * wp); sx = -1; }
        u = (long long)a * p + pos; Y += sy;
    }
}
/* N_min separation in the explicit room with row CB of height g */
static int *par_, *kap_[4];
static int fnd(int a) { while (par_[a] != a) { par_[a] = par_[par_[a]]; a = par_[a]; } return a; }
static int EH; static unsigned char *E; /* explicit cells E[x*EH+y] */
static int *cidE;
static int ehas(int x, int y) { return x >= 0 && y >= 0 && x < GS && y < EH && E[x * EH + y]; }
static void sepall(int g, unsigned char *sep) {
    EH = H_ + g + 2; E = calloc(GS * EH, 1); cidE = malloc(sizeof(int) * GS * EH);
    int n = 0;
    for (int x = 0; x < GS; x++) for (int y = 0; y < H_; y++) if (c[x][y]) {
        if (y < CB) E[x * EH + y] = 1; else if (y > CB) E[x * EH + y + g - 1] = 1;
        else for (int j = 0; j < g; j++) E[x * EH + y + j] = 1; }
    for (int x = 0; x < GS; x++) for (int y = 0; y < EH; y++) cidE[x * EH + y] = E[x * EH + y] ? n++ : -1;
    par_ = malloc(sizeof(int) * n); for (int g4 = 0; g4 < 4; g4++) kap_[g4] = malloc(sizeof(int) * n);
    int *qa = malloc(sizeof(int) * 8 * n), *qb = malloc(sizeof(int) * 8 * n);
    for (int cls = 0; cls < 4; cls++) {
        int ox = cls & 1, oy = cls >> 1, any = 0;
        for (int i = 0; i < npair; i++) if ((ptx[pa[i]] & 1) == ox && (pty[pa[i]] & 1) == oy) any = 1;
        if (!any) continue;
        for (int x = 0; x < GS; x++) for (int y = 0; y < EH; y++) if (E[x * EH + y]) {
            int cc = cidE[x * EH + y];
            for (int pr = 0; pr < 2; pr++) {
                int nx = ((((x - ox) % 2 + 2) % 2) == pr) ? x - 1 : x + 1;
                kap_[pr][cc] = ehas(nx, y) ? cidE[nx * EH + y] : cc;
                int ny = ((((y - oy) % 2 + 2) % 2) == pr) ? y - 1 : y + 1;
                kap_[2 + pr][cc] = ehas(x, ny) ? cidE[x * EH + ny] : cc;
            } }
        for (int i = 0; i < n; i++) par_[i] = i;
        int qh = 0, qt = 0;
        for (int X = 0; X < GS; X++) for (int Y = 0; Y < EH; Y++) {
            if (((X - ox) & 1) == 0 && ((Y - oy) & 1) == 0) continue;
            int ll = ehas(X - 1, Y - 1), lr = ehas(X, Y - 1), ul = ehas(X - 1, Y), ur = ehas(X, Y), k = ll + lr + ul + ur;
            int A[2], B[2], np = 0;
            if (k == 4) { A[0] = cidE[(X - 1) * EH + Y - 1]; B[0] = cidE[X * EH + Y]; A[1] = cidE[X * EH + Y - 1]; B[1] = cidE[(X - 1) * EH + Y]; np = 2; }
            else if (k == 2) { int cs[2], m = 0;
                if (ll) cs[m++] = cidE[(X - 1) * EH + Y - 1]; if (lr) cs[m++] = cidE[X * EH + Y - 1];
                if (ul) cs[m++] = cidE[(X - 1) * EH + Y]; if (ur) cs[m++] = cidE[X * EH + Y];
                A[0] = cs[0]; B[0] = cs[1]; np = 1; }
            for (int t = 0; t < np; t++) { int a = fnd(A[t]), b = fnd(B[t]); if (a != b) { par_[a] = b; qa[qt] = A[t]; qb[qt] = B[t]; qt++; } }
        }
        while (qh < qt) { int a0 = qa[qh], b0 = qb[qh]; qh++;
            for (int g4 = 0; g4 < 4; g4++) { int a = fnd(kap_[g4][a0]), b = fnd(kap_[g4][b0]);
                if (a != b) { par_[a] = b; qa[qt] = kap_[g4][a0]; qb[qt] = kap_[g4][b0]; qt++; } } }
        for (int i = 0; i < npair; i++) if ((ptx[pa[i]] & 1) == ox && (pty[pa[i]] & 1) == oy) {
            int s = 1;
            for (int e = 0; e < 2 && s; e++) ;
            int Sx = ptx[pa[i]], Sy = pty[pa[i]], Tx = ptx[pb[i]], Ty = pty[pb[i]];
            if (Sy > CB) Sy += g - 1; if (Ty > CB) Ty += g - 1;
            for (int u = 0; u < 4 && s; u++) for (int w = 0; w < 4; w++)
                if (fnd(cidE[(Sx - 1 + (u & 1)) * EH + Sy - 1 + (u >> 1)]) == fnd(cidE[(Tx - 1 + (w & 1)) * EH + Ty - 1 + (w >> 1)])) { s = 0; break; }
            sep[i] = s;
        }
    }
    free(E); free(cidE); free(par_); for (int g4 = 0; g4 < 4; g4++) free(kap_[g4]); free(qa); free(qb);
}
int main(int argc, char **argv) {
    int AX = atoi(argv[1]); CB = atoi(argv[2]); int PMAX = atoi(argv[3]), GMAX = atoi(argv[4]), dup = argc > 5 ? atoi(argv[5]) : 0;
    int A; if (scanf("%d", &A) != 1) return 1;
    for (int i = 0; i < A; i++) { int x, y; scanf("%d %d", &x, &y); if (AX) { int t = x; x = y; y = t; }
        for (int j = 0; j <= (y == CB ? dup : 0); j++) c[x + 1][(y > CB ? y + dup : y + j) + 1] = 1; }
    CB += 1; /* shifted by 1 */
    for (int x = 0; x < GS; x++) for (int y = 0; y < GS; y++) if (c[x][y]) { if (x + 1 > W_) W_ = x + 1; if (y + 1 > H_) H_ = y + 1; }
    memset(pid, -1, sizeof pid);
    for (int X = 1; X < GS; X++) for (int Y = 1; Y < GS; Y++) if (has(X - 1, Y - 1) + has(X, Y - 1) + has(X - 1, Y) + has(X, Y) == 4) { ptx[npt] = X; pty[npt] = Y; pid[X][Y] = npt++; }
    for (int i = 0; i < npt; i++) for (int j = i + 1; j < npt; j++) if (!((ptx[i] ^ ptx[j]) & 1) && !((pty[i] ^ pty[j]) & 1)) { pa[npair] = i; pb[npair] = j; pidx[i][j] = npair++; }
    long long L = 1, QF = 1; int nch = 0;
    for (int y = 0; y < H_; y++) for (int x = 0; x < GS; x++) if (c[x][y] && !has(x - 1, y)) { int b = x; while (has(b, y)) b++; long long w = b - x;
        QF = QF / gcdl(QF, w) * w; if (y == CB) { L = L / gcdl(L, w) * w; nch++; printf("# band chord x=[%d,%d] w=%lld\n", x - 1, b - 1, w); } }
    printf("# points %d pairs %d  band row %d chords %d L=%lld QF=%lld PMAX=%d GMAX=%d\n", npt, npair, CB - 1, nch, L, QF, PMAX, GMAX);
    for (int i = 0; i < npair; i++) printf("# pair %d (%d,%d)-(%d,%d)%s\n", i, ptx[pa[i]] - 1, pty[pa[i]] - 1, ptx[pb[i]] - 1, pty[pb[i]] - 1,
        ((pty[pa[i]] <= CB) != (pty[pb[i]] <= CB)) ? " opposite" : " same-side");
    int ng = GMAX + 1; short *minp = malloc(sizeof(short) * ng * npair), *minq = malloc(sizeof(short) * ng * npair);
    for (int i = 0; i < ng * npair; i++) minp[i] = -1;
    /* horizontal direction: constant in g */
    for (int i = 0; i < npair; i++) if (pty[pa[i]] == pty[pb[i]]) { int ok = 1, x0 = ptx[pa[i]], x1 = ptx[pb[i]]; if (x0 > x1) { int t = x0; x0 = x1; x1 = t; }
        for (int x = x0 + 1; x < x1; x++) if (pid[x][pty[pa[i]]] < 0) ok = 0;
        if (ok) for (int g = 1; g <= GMAX; g++) { minp[g * npair + i] = 0; minq[g * npair + i] = 1; } }
    hit = malloc(npt);
    for (int p = 1; p <= PMAX; p++) {
        long long M = 2 * L * p; unsigned char *tab = calloc((size_t)M * npair, 1); short *tq = malloc(sizeof(short) * M * npair);
        for (long long res = 0; res < M; res++) {
            long long g = res ? res : M;
            if (!(g & 1) || g > GMAX) { if (g > GMAX) continue; if (!(g & 1)) continue; }
            for (int q = 0; q <= QF * p; q++) { if (gcdl(q, p) != 1) continue;
                for (int s = 0; s < npt; s++) for (int sg = 0; sg < 4; sg++) { if (q == 0 && (sg & 1)) continue;
                    memset(hit, 0, npt); trace(s, (sg & 1) ? -1 : 1, (sg & 2) ? -1 : 1, q, p, g);
                    for (int t = 0; t < npt; t++) if (hit[t] && t != s) { int a = s < t ? s : t, b = s < t ? t : s;
                        if (!((ptx[a] ^ ptx[b]) & 1) && !((pty[a] ^ pty[b]) & 1)) { int i = pidx[a][b]; if (!tab[res * npair + i]) { tab[res * npair + i] = 1; tq[res * npair + i] = (short)q; } } } } }
        }
        for (int g = 1; g <= GMAX; g += 2) { long long res = g % M; long long g0 = res ? res : M; if (g0 > GMAX) { fprintf(stderr, "BUG res\n"); exit(1); }
            for (int i = 0; i < npair; i++) if (minp[g * npair + i] < 0 && tab[res * npair + i]) { minp[g * npair + i] = (short)p; minq[g * npair + i] = tq[res * npair + i]; } }
        free(tab); free(tq);
    }
    int quiet = argc > 6 ? atoi(argv[6]) : 0;
    /* covering certificates: smallest PC such that every odd g in one period 2L*lcm(1..PC) has a witness with p <= PC.
       By periodicity of each Lit_p (period 2Lp) this proves the pair lit for EVERY odd g >= 1. */
    for (int i = 0; i < npair; i++) { long long lc = 1; int found = 0, lastPC = 0; long long lastUn = 0, firstUn = 0;
        for (int PC = 1; PC <= PMAX; PC++) { lc = lc / gcdl(lc, PC) * PC; long long Q = 2 * L * lc; if (Q + 1 > GMAX) break;
            long long un = 0, fu = 0; for (long long g = 1; g <= Q; g += 2) { int m = minp[g * npair + i]; if (m < 0 || m > PC) { if (!un) fu = g; un++; } }
            lastPC = PC; lastUn = un; firstUn = fu; if (!un) { found = PC; break; } }
        if (found) printf("C %d cover PC=%d\n", i, found); else printf("C %d nocover upto PC=%d uncovered %lld first g=%lld\n", i, lastPC, lastUn, firstUn); }
    if (quiet) { long long nun = 0; int mx = 0, mg = 0; for (int g = 1; g <= GMAX; g += 2) for (int i = 0; i < npair; i++) { int m = minp[g * npair + i]; if (m < 0) { nun++; if (nun <= 40) printf("U %d %d\n", g, i); } else if (m > mx) { mx = m; mg = g; } }
        printf("# quiet: unlit(p<=PMAX) %lld  max minp %d at g=%d\n", nun, mx, mg); return 0; }
    unsigned char *sep = malloc(npair);
    for (int g = 1; g <= GMAX; g += 2) { int need = 0; for (int i = 0; i < npair; i++) if (minp[g * npair + i] < 0) need = 1;
        memset(sep, 2, npair); if (need) sepall(g, sep);
        if (!quiet) for (int i = 0; i < npair; i++) printf("G %d %d %d %d %d\n", g, i, minp[g * npair + i], minp[g * npair + i] < 0 ? 0 : minq[g * npair + i], minp[g * npair + i] < 0 ? sep[i] : -1); }
    printf("# trajectories %lld capHits %lld\n", nTraj, capHits);
    return 0;
}
