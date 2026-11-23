/* shoot45.c -- exact LIT filter, k and N_min for canonical45 rooms.
 *
 * Input: room lines "N W i j h i j h ..." (enum45 output).
 * For each room and each class X in {A, B, C} with >= 2 interior points of X
 * (8 tiles for A, B; 4 tiles for C), every unordered pair (S, T):
 *
 *  - LIT certificate by exact shooting in the 8-fold unfolding X(P).  Faces of
 *    X(P) are (tile t, g in D4); face (t,g) develops to g(t).  Across an
 *    interior edge, (t,g) is glued to (t',g); across a wall e, to (t, g rho_e),
 *    rho_e the linear reflection parallel to e.  Pairing each face with its
 *    neighbour across the hypotenuse gives an origami with 4N unit squares;
 *    h = right neighbour, v = up neighbour; every square carries the room
 *    lattice point at its bottom-left corner.  From each of the 8 squares whose
 *    corner is a lift of S, each primitive (p,q), p,q >= 0, p+q <= BOUND, is
 *    followed one lattice step at a time until it meets a corner label (any
 *    polygon vertex, convex or reflex) or returns to its start.  The room
 *    direction of the ray is g^-1 (p,q).
 *    Every certificate (S, room direction, m steps, T) is replayed by
 *    verify45() (independent tracer in the room plane).
 *  - k = number of transparent (interior or flat-boundary) lattice points of
 *    the two other classes.
 *  - N_min (triangle framework, sheets = tiles, g_A = k_AC k_AB, g_B = k_BC k_AB,
 *    g_C = k_AC k_BC): finest G-invariant partition such that the quotient has
 *    no regular point over the two other classes (regular = cycle length 4 over
 *    A or B, 2 over C), built by forced unions to a fixed point.  Separated:
 *    no point of N over X contains images of both S and T.
 *
 * usage: shoot45 BOUND CERTMAX infile outfile survivorfile [problemfile [all]]
 *   per-pair lines are written only for rooms with N <= CERTMAX.
 *   environment CLASSES (default "ABC"): analyse pairs of these classes only.
 *   problemfile (optional): orbit45 input lines for every survivor.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int verify45(int n, const int *ti, const int *tj, const int *th,
             int sx, int sy, int dx, int dy, int m, int tx, int ty);

#define MAXT 40
#define MAXF (8 * MAXT)
#define MAXQ (4 * MAXT)
#define LG 128
#define LO 64

static const int GM[8][4] = { {1,0,0,1}, {0,-1,1,0}, {-1,0,0,-1}, {0,1,-1,0},
                              {1,0,0,-1}, {-1,0,0,1}, {0,1,1,0}, {0,-1,-1,0} };
static int gmul[8][8], ginv[8];
static const int RHO[4] = {4, 5, 6, 7};   /* edge type H, V, D+ (1,1), D- (1,-1) */

static int gfind(int a, int b, int c, int d) {
    for (int g = 0; g < 8; g++) if (GM[g][0] == a && GM[g][1] == b && GM[g][2] == c && GM[g][3] == d) return g;
    fprintf(stderr, "not in D4\n"); exit(9);
}
static void init_group(void) {
    for (int g = 0; g < 8; g++)
        for (int h = 0; h < 8; h++) {   /* (g o h)(x) = g(h(x)) : matrix G*H */
            const int *A = GM[g], *B = GM[h];
            gmul[g][h] = gfind(A[0] * B[0] + A[1] * B[2], A[0] * B[1] + A[1] * B[3],
                               A[2] * B[0] + A[3] * B[2], A[2] * B[1] + A[3] * B[3]);
        }
    for (int g = 0; g < 8; g++) for (int h = 0; h < 8; h++) if (gmul[g][h] == 0) ginv[g] = h;
}

static int cls(int x, int y) { return ((x & 1) == 0 && (y & 1) == 0) ? 0 : ((x & 1) && (y & 1)) ? 1 : 2; }

static void tile_verts(int i, int j, int h, int *x, int *y) {
    int p = (i + j) & 1;
    if (!p) {
        if (!h) { x[0] = i; y[0] = j; x[1] = i + 1; y[1] = j; x[2] = i + 1; y[2] = j + 1; }
        else    { x[0] = i; y[0] = j; x[1] = i; y[1] = j + 1; x[2] = i + 1; y[2] = j + 1; }
    } else {
        if (!h) { x[0] = i; y[0] = j; x[1] = i + 1; y[1] = j; x[2] = i; y[2] = j + 1; }
        else    { x[0] = i + 1; y[0] = j; x[1] = i + 1; y[1] = j + 1; x[2] = i; y[2] = j + 1; }
    }
}

static int etype(int x1, int y1, int x2, int y2, int *ex, int *ey) {
    if (y1 == y2) { *ex = x1 < x2 ? x1 : x2; *ey = y1; return 0; }
    if (x1 == x2) { *ex = x1; *ey = y1 < y2 ? y1 : y2; return 1; }
    *ex = x1 < x2 ? x1 : x2; *ey = y1 < y2 ? y1 : y2;
    return ((x2 - x1) * (y2 - y1) > 0) ? 2 : 3;
}

/* ---------------------------------------------------------------- room */
static int n, ti[MAXT], tj[MAXT], th[MAXT], vx[MAXT][3], vy[MAXT][3];
static int tnb[MAXT][3], tet[MAXT][3];          /* neighbour tile across edge k (-1 wall), edge type */
static int eown[4][LG][LG][2];
static int pid[LG][LG];
static int npt, ptx[4 * MAXT], pty[4 * MAXT], ptcls[4 * MAXT], ptcnt[4 * MAXT], ptnbd[4 * MAXT], ptbt[4 * MAXT][4];
static int ptcorner[4 * MAXT], ptinterior[4 * MAXT];

static void build_room(void) {
    for (int a = 0; a < n; a++) tile_verts(ti[a], tj[a], th[a], vx[a], vy[a]);
    for (int a = 0; a < n; a++)
        for (int k = 0; k < 3; k++) {
            int ex, ey, t = etype(vx[a][k], vy[a][k], vx[a][(k + 1) % 3], vy[a][(k + 1) % 3], &ex, &ey);
            eown[t][ex + LO][ey + LO][0] = eown[t][ex + LO][ey + LO][1] = -1;
        }
    for (int a = 0; a < n; a++)
        for (int k = 0; k < 3; k++) {
            int ex, ey, t = etype(vx[a][k], vy[a][k], vx[a][(k + 1) % 3], vy[a][(k + 1) % 3], &ex, &ey);
            int *o = eown[t][ex + LO][ey + LO];
            if (o[0] < 0) o[0] = a; else if (o[1] < 0) o[1] = a; else { fprintf(stderr, "edge owned 3 times\n"); exit(10); }
            tet[a][k] = t;
        }
    for (int a = 0; a < n; a++)
        for (int k = 0; k < 3; k++) {
            int ex, ey, t = etype(vx[a][k], vy[a][k], vx[a][(k + 1) % 3], vy[a][(k + 1) % 3], &ex, &ey);
            int *o = eown[t][ex + LO][ey + LO];
            tnb[a][k] = o[0] == a ? o[1] : o[0];
        }
    /* lattice points */
    npt = 0;
    for (int a = 0; a < n; a++) for (int k = 0; k < 3; k++) pid[vx[a][k] + LO][vy[a][k] + LO] = -1;
    for (int a = 0; a < n; a++)
        for (int k = 0; k < 3; k++) {
            int X = vx[a][k] + LO, Y = vy[a][k] + LO;
            if (pid[X][Y] < 0) {
                pid[X][Y] = npt; ptx[npt] = vx[a][k]; pty[npt] = vy[a][k]; ptcls[npt] = cls(vx[a][k], vy[a][k]);
                ptcnt[npt] = 0; ptnbd[npt] = 0; npt++;
            }
            ptcnt[pid[X][Y]]++;
        }
    for (int a = 0; a < n; a++)
        for (int k = 0; k < 3; k++)
            if (tnb[a][k] < 0) {
                int p1 = pid[vx[a][k] + LO][vy[a][k] + LO], p2 = pid[vx[a][(k + 1) % 3] + LO][vy[a][(k + 1) % 3] + LO];
                if (ptnbd[p1] < 4) ptbt[p1][ptnbd[p1]] = tet[a][k];
                ptnbd[p1]++;
                if (ptnbd[p2] < 4) ptbt[p2][ptnbd[p2]] = tet[a][k];
                ptnbd[p2]++;
            }
    for (int p = 0; p < npt; p++) {
        ptinterior[p] = ptnbd[p] == 0;
        ptcorner[p] = ptnbd[p] != 0 && (ptnbd[p] != 2 || ptbt[p][0] != ptbt[p][1]);
        int full = ptcls[p] == 2 ? 4 : 8;
        if (ptinterior[p] && ptcnt[p] != full) { fprintf(stderr, "interior count mismatch\n"); exit(11); }
    }
}

/* ---------------------------------------------------------------- origami */
static int nf, glue[MAXF][3], nsq, sqof[MAXF];
static int H[MAXQ], V[MAXQ], LABP[MAXQ], SQG[MAXQ], BLK[MAXQ];

static void build_origami(void) {
    nf = 8 * n;
    for (int a = 0; a < n; a++)
        for (int g = 0; g < 8; g++)
            for (int k = 0; k < 3; k++) {
                int f = 8 * a + g;
                glue[f][k] = tnb[a][k] >= 0 ? 8 * tnb[a][k] + g : 8 * a + gmul[g][RHO[tet[a][k]]];
            }
    for (int f = 0; f < nf; f++) sqof[f] = -1;
    nsq = 0;
    for (int f = 0; f < nf; f++) {
        int a = f / 8, hk = -1;
        for (int k = 0; k < 3; k++) if (tet[a][k] >= 2) hk = k;
        int p = glue[f][hk];
        int b = p / 8, hk2 = -1;
        for (int k = 0; k < 3; k++) if (tet[b][k] >= 2) hk2 = k;
        if (glue[p][hk2] != f) { fprintf(stderr, "hyp gluing not an involution\n"); exit(12); }
        if (sqof[f] < 0) { sqof[f] = sqof[p] = nsq++; }
    }
    if (nsq != 4 * n) { fprintf(stderr, "square count\n"); exit(13); }
    for (int s = 0; s < nsq; s++) { H[s] = V[s] = LABP[s] = SQG[s] = -1; }
    for (int f = 0; f < nf; f++) {
        int a = f / 8, g = f % 8, dx[3], dy[3];
        for (int k = 0; k < 3; k++) { dx[k] = GM[g][0] * vx[a][k] + GM[g][1] * vy[a][k]; dy[k] = GM[g][2] * vx[a][k] + GM[g][3] * vy[a][k]; }
        int bx = dx[0], by = dy[0];
        for (int k = 1; k < 3; k++) { if (dx[k] < bx) bx = dx[k]; if (dy[k] < by) by = dy[k]; }
        int s = sqof[f];
        for (int k = 0; k < 3; k++)
            if (dx[k] == bx && dy[k] == by) {
                int p = pid[vx[a][k] + LO][vy[a][k] + LO];
                if (LABP[s] >= 0 && LABP[s] != p) { fprintf(stderr, "label clash\n"); exit(14); }
                LABP[s] = p;
                if (SQG[s] < 0) SQG[s] = g;
            }
        for (int k = 0; k < 3; k++) {
            int k2 = (k + 1) % 3;
            if (dx[k] == bx + 1 && dx[k2] == bx + 1) { if (H[s] >= 0) { fprintf(stderr, "H twice\n"); exit(15); } H[s] = sqof[glue[f][k]]; }
            if (dy[k] == by + 1 && dy[k2] == by + 1) { if (V[s] >= 0) { fprintf(stderr, "V twice\n"); exit(15); } V[s] = sqof[glue[f][k]]; }
        }
    }
    for (int s = 0; s < nsq; s++) {
        if (H[s] < 0 || V[s] < 0 || LABP[s] < 0) { fprintf(stderr, "incomplete square %d\n", s); exit(16); }
        BLK[s] = ptcorner[LABP[s]];
    }
    /* H and V must be permutations */
    static int seenh[MAXQ], seenv[MAXQ];
    for (int s = 0; s < nsq; s++) seenh[s] = seenv[s] = 0;
    for (int s = 0; s < nsq; s++) { seenh[H[s]]++; seenv[V[s]]++; }
    for (int s = 0; s < nsq; s++) if (seenh[s] != 1 || seenv[s] != 1) { fprintf(stderr, "not a permutation\n"); exit(17); }
    /* interior points: exactly 8 squares carry them */
    static int lc[4 * MAXT];
    for (int p = 0; p < npt; p++) lc[p] = 0;
    for (int s = 0; s < nsq; s++) lc[LABP[s]]++;
    for (int p = 0; p < npt; p++) if (ptinterior[p] && lc[p] != 8) { fprintf(stderr, "interior lift count %d\n", lc[p]); exit(18); }
}

/* ---------------------------------------------------------------- directions */
static int ndir, DP_[4000], DQ_[4000];
static unsigned char WORD[4000][128];
static int WLEN[4000];
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static void make_dirs(int bound) {
    ndir = 0;
    for (int s = 1; s <= bound; s++)
        for (int p = s; p >= 0; p--) {
            int q = s - p;
            if (gcd(p, q) != 1) continue;
            DP_[ndir] = p; DQ_[ndir] = q;
            int L = 0;
            if (p >= 1 && q >= 1) {
                int a = 1, b = 1;
                while (a < p || b < q) {
                    long uv = (a < p) ? (long)q * a : 1L << 60;
                    long uh = (b < q) ? (long)p * b : 1L << 60;
                    if (uv < uh) { WORD[ndir][L++] = 0; a++; } else { WORD[ndir][L++] = 1; b++; }
                }
            }
            WLEN[ndir] = L;
            ndir++;
        }
}
static int step(int s, int d) {
    int p = DP_[d], q = DQ_[d];
    if (q == 0) return H[s];
    if (p == 0) return V[s];
    int c = s;
    for (int t = 0; t < WLEN[d]; t++) c = WORD[d][t] ? V[c] : H[c];
    return H[V[c]];
}

/* ---------------------------------------------------------------- N_min */
static int uf[MAXT];
static int fnd(int a) { while (uf[a] != a) { uf[a] = uf[uf[a]]; a = uf[a]; } return a; }
static int gen[3][MAXT];          /* g_A, g_B, g_C on tiles */
static int qa[MAXT * MAXT * 4], qb[MAXT * MAXT * 4], qt;
static int uni(int a, int b) { int x = fnd(a), y = fnd(b); if (x == y) return 0; uf[x] = y; qa[qt] = a; qb[qt] = b; qt++; return 1; }

static void build_gens(void) {
    int kap[3][MAXT];   /* 0: AB, 1: AC, 2: BC */
    for (int a = 0; a < n; a++)
        for (int k = 0; k < 3; k++) {
            int c1 = cls(vx[a][k], vy[a][k]), c2 = cls(vx[a][(k + 1) % 3], vy[a][(k + 1) % 3]);
            int typ = (c1 != 2 && c2 != 2) ? 0 : (c1 == 0 || c2 == 0) ? 1 : 2;
            kap[typ][a] = tnb[a][k] >= 0 ? tnb[a][k] : a;
        }
    for (int a = 0; a < n; a++) {
        gen[0][a] = kap[1][kap[0][a]];
        gen[1][a] = kap[2][kap[0][a]];
        gen[2][a] = kap[1][kap[2][a]];
    }
}

/* returns separated(0/1); nblocks out */
static int nmin_sep(int X, int S, int T, int *nblk) {
    for (int a = 0; a < n; a++) uf[a] = a;
    qt = 0;
    int qh = 0;
    for (int o = 0; o < 3; o++) {
        if (o == X) continue;
        int L = o == 2 ? 2 : 4;
        static int vis[MAXT];
        for (int a = 0; a < n; a++) vis[a] = 0;
        for (int a = 0; a < n; a++) {
            if (vis[a]) continue;
            int cyc[MAXT], m = 0, c = a;
            do { vis[c] = 1; cyc[m++] = c; c = gen[o][c]; } while (c != a);
            if (m == L) { if (L == 4) { uni(cyc[0], cyc[2]); uni(cyc[1], cyc[3]); } else uni(cyc[0], cyc[1]); }
        }
    }
    for (;;) {
        while (qh < qt) {
            int a = qa[qh], b = qb[qh]; qh++;
            for (int g = 0; g < 3; g++) uni(gen[g][a], gen[g][b]);
        }
        /* regular points of the (closed) quotient over the obstruction classes: collect, then apply */
        int pa[2 * MAXT], pb[2 * MAXT], np = 0;
        for (int o = 0; o < 3; o++) {
            if (o == X) continue;
            int L = o == 2 ? 2 : 4;
            static int vis[MAXT];
            for (int a = 0; a < n; a++) vis[a] = 0;
            for (int a = 0; a < n; a++) {
                int r = fnd(a);
                if (vis[r]) continue;
                int cyc[MAXT + 1], m = 0, c = r;
                do { vis[c] = 1; cyc[m++] = c; c = fnd(gen[o][c]); } while (c != r);
                if (m == L) {
                    if (L == 4) { pa[np] = cyc[0]; pb[np++] = cyc[2]; pa[np] = cyc[1]; pb[np++] = cyc[3]; }
                    else { pa[np] = cyc[0]; pb[np++] = cyc[1]; }
                }
            }
        }
        int added = 0;
        for (int t = 0; t < np; t++) added += uni(pa[t], pb[t]);
        if (!added && qh == qt) break;
    }
    int nb = 0;
    for (int a = 0; a < n; a++) if (fnd(a) == a) nb++;
    *nblk = nb;
    /* cycles of induced g_X on blocks */
    static int cid[MAXT];
    for (int a = 0; a < n; a++) cid[a] = -1;
    int nc = 0;
    for (int a = 0; a < n; a++) {
        int r = fnd(a);
        if (cid[r] >= 0) continue;
        int c = r;
        do { cid[c] = nc; c = fnd(gen[X][c]); } while (c != r);
        nc++;
    }
    static int markS[MAXT];
    for (int c = 0; c < nc; c++) markS[c] = 0;
    for (int a = 0; a < n; a++)
        for (int k = 0; k < 3; k++)
            if (vx[a][k] == ptx[S] && vy[a][k] == pty[S]) markS[cid[fnd(a)]] = 1;
    for (int a = 0; a < n; a++)
        for (int k = 0; k < 3; k++)
            if (vx[a][k] == ptx[T] && vy[a][k] == pty[T] && markS[cid[fnd(a)]]) return 0;
    return 1;
}

/* ---------------------------------------------------------------- stats */
#define NW 64
static long long st_rooms[3][MAXT + 1][NW], st_pairs[3][MAXT + 1][NW], st_lit[3][MAXT + 1][NW], st_unres[3][MAXT + 1][NW];
static long long st_unres_sep[3][MAXT + 1][NW], st_lit_sep[3][MAXT + 1][NW];
static long long st_allrooms[MAXT + 1][NW], st_eligAB[MAXT + 1][NW];
static long long st_verify_fail = 0, st_khist[3][64], st_lit_k[3][64], st_unres_k[3][64];
static int st_maxk_lit[3] = {-1, -1, -1}, st_maxm = 0;

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
    init_group();
    int bound = atoi(argv[1]), certmax = atoi(argv[2]);
    make_dirs(bound);
    FILE *in = strcmp(argv[3], "-") ? fopen(argv[3], "r") : stdin;
    FILE *out = fopen(argv[4], "w"), *sv = fopen(argv[5], "w");
    FILE *pf = argc > 6 ? fopen(argv[6], "w") : NULL;
    int pf_all = argc > 7 && !strcmp(argv[7], "all");   /* problem lines for every pair, not only survivors */
    const char *cl = getenv("CLASSES");
    int cmask = 0;
    for (const char *c = cl ? cl : "ABC"; *c; c++) cmask |= *c == 'A' ? 1 : *c == 'B' ? 2 : *c == 'C' ? 4 : 0;
    static char line[16384];
    long long rid = 0;
    while (fgets(line, sizeof line, in)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        char *pp = line;
        n = (int)strtol(pp, &pp, 10);
        int W = (int)strtol(pp, &pp, 10);
        for (int a = 0; a < n; a++) { ti[a] = (int)strtol(pp, &pp, 10); tj[a] = (int)strtol(pp, &pp, 10); th[a] = (int)strtol(pp, &pp, 10); }
        rid++;
        build_room();
        int Wc = 0;
        for (int p = 0; p < npt; p++) Wc += ptcorner[p];
        if (Wc != W) { fprintf(stderr, "wall count mismatch room %lld (%d vs %d)\n", rid, Wc, W); return 2; }
        build_origami();
        build_gens();
        int Wi = W < NW ? W : NW - 1;
        st_allrooms[n][Wi]++;
        int wr = n <= certmax;
        if (wr) { fprintf(out, "R %lld %d %d", rid, n, W); for (int a = 0; a < n; a++) fprintf(out, " %d %d %d", ti[a], tj[a], th[a]); fputc('\n', out); }
        int eligAB = 0;
        for (int X = 0; X < 3; X++) {
            int ip[4 * MAXT], ni = 0, k = 0;
            for (int p = 0; p < npt; p++) {
                if (ptcls[p] == X && ptinterior[p]) ip[ni++] = p;
                if (ptcls[p] != X && !ptcorner[p]) k++;
            }
            if (ni < 2) continue;
            if (X < 2) eligAB = 1;
            if (!(cmask >> X & 1)) continue;
            st_rooms[X][n][Wi]++;
            static int resolved[4 * MAXT][4 * MAXT], rsrc[4 * MAXT][4 * MAXT], rdx[4 * MAXT][4 * MAXT], rdy[4 * MAXT][4 * MAXT], rm[4 * MAXT][4 * MAXT];
            static int labidx[4 * MAXT];
            for (int a = 0; a < ni; a++) for (int b = 0; b < ni; b++) resolved[a][b] = 0;
            for (int p = 0; p < npt; p++) labidx[p] = -1;
            for (int a = 0; a < ni; a++) labidx[ip[a]] = a;
            for (int a = 0; a < ni; a++) {
                int need = 0;
                for (int b = a + 1; b < ni; b++) if (!resolved[a][b]) need++;
                if (!need) continue;
                int srcsq[8], ns = 0;
                for (int s = 0; s < nsq; s++) if (LABP[s] == ip[a]) srcsq[ns++] = s;
                for (int d = 0; d < ndir && need; d++)
                    for (int u = 0; u < ns && need; u++) {
                        int s0 = srcsq[u], s = s0;
                        for (int m = 1; m <= nsq + 1; m++) {
                            s = step(s, d);
                            if (BLK[s]) break;
                            int b = labidx[LABP[s]];
                            if (b >= 0 && b != a) {
                                int lo = a < b ? a : b, hi = a < b ? b : a;
                                if (!resolved[lo][hi]) {
                                    resolved[lo][hi] = 1;
                                    int g = ginv[SQG[s0]];
                                    rsrc[lo][hi] = a; rm[lo][hi] = m;
                                    rdx[lo][hi] = GM[g][0] * DP_[d] + GM[g][1] * DQ_[d];
                                    rdy[lo][hi] = GM[g][2] * DP_[d] + GM[g][3] * DQ_[d];
                                    if (b > a) need--;
                                }
                            }
                            if (s == s0) break;
                        }
                    }
            }
            for (int a = 0; a < ni; a++)
                for (int b = a + 1; b < ni; b++) {
                    int nb, sep = nmin_sep(X, ip[a], ip[b], &nb);
                    st_pairs[X][n][Wi]++;
                    st_khist[X][k < 64 ? k : 63]++;
                    if (resolved[a][b]) {
                        int src = rsrc[a][b], dst = src == a ? b : a;
                        int ok = verify45(n, ti, tj, th, ptx[ip[src]], pty[ip[src]], rdx[a][b], rdy[a][b], rm[a][b], ptx[ip[dst]], pty[ip[dst]]);
                        if (!ok) st_verify_fail++;
                        if (rm[a][b] > st_maxm) st_maxm = rm[a][b];
                        st_lit[X][n][Wi]++;
                        if (sep) st_lit_sep[X][n][Wi]++;
                        st_lit_k[X][k < 64 ? k : 63]++;
                        if (k > st_maxk_lit[X]) st_maxk_lit[X] = k;
                        if (wr) fprintf(out, "P %c %d %d %d %d L %d %d %d %d k %d nb %d sep %d%s\n", "ABC"[X], ptx[ip[src]], pty[ip[src]],
                                        ptx[ip[dst]], pty[ip[dst]], rdx[a][b], rdy[a][b], rm[a][b], 0, k, nb, sep, ok ? "" : " VERIFYFAIL");
                    } else {
                        st_unres[X][n][Wi]++;
                        if (sep) st_unres_sep[X][n][Wi]++;
                        st_unres_k[X][k < 64 ? k : 63]++;
                        if (wr) fprintf(out, "P %c %d %d %d %d U k %d nb %d sep %d\n", "ABC"[X], ptx[ip[a]], pty[ip[a]], ptx[ip[b]], pty[ip[b]], k, nb, sep);
                        fprintf(sv, "%lld %c %d %d %d %d %d %d k %d nb %d sep %d |", rid, "ABC"[X], n, W, ptx[ip[a]], pty[ip[a]], ptx[ip[b]], pty[ip[b]], k, nb, sep);
                        for (int t = 0; t < n; t++) fprintf(sv, " %d %d %d", ti[t], tj[t], th[t]);
                        fputc('\n', sv);
                    }
                    if (pf && (pf_all || !resolved[a][b])) {
                        fprintf(pf, "%d", nsq);
                        for (int s = 0; s < nsq; s++) fprintf(pf, " %d", H[s]);
                        for (int s = 0; s < nsq; s++) fprintf(pf, " %d", V[s]);
                        for (int s = 0; s < nsq; s++) {
                            int p = LABP[s];
                            fprintf(pf, " %d", p == ip[a] ? 0 : p == ip[b] ? 1 : BLK[s] ? -1 : -2);
                        }
                        fprintf(pf, " # %lld %c %d %d %d %d %s\n", rid, "ABC"[X], ptx[ip[a]], pty[ip[a]], ptx[ip[b]], pty[ip[b]], resolved[a][b] ? "shootLIT" : "survivor");
                    }
                }
        }
        if (eligAB) st_eligAB[n][Wi]++;
    }
    fprintf(out, "# STATS bound %d dirs %d rooms %lld classes %s\n", bound, ndir, rid, cl ? cl : "ABC");
    for (int a = 0; a <= MAXT; a++)
        for (int w = 0; w < NW; w++) {
            if (st_allrooms[a][w]) fprintf(out, "# ROOMS N %d W %d rooms %lld eligibleAB %lld\n", a, w, st_allrooms[a][w], st_eligAB[a][w]);
            for (int X = 0; X < 3; X++)
                if (st_rooms[X][a][w])
                    fprintf(out, "# T %c N %d W %d eligible_rooms %lld pairs %lld lit %lld unresolved %lld lit_sep %lld unres_sep %lld\n",
                            "ABC"[X], a, w, st_rooms[X][a][w], st_pairs[X][a][w], st_lit[X][a][w], st_unres[X][a][w],
                            st_lit_sep[X][a][w], st_unres_sep[X][a][w]);
        }
    for (int X = 0; X < 3; X++) {
        fprintf(out, "# max_k_lit %c %d\n", "ABC"[X], st_maxk_lit[X]);
        for (int k = 0; k < 64; k++)
            if (st_khist[X][k]) fprintf(out, "# K %c %d pairs %lld lit %lld unresolved %lld\n", "ABC"[X], k, st_khist[X][k], st_lit_k[X][k], st_unres_k[X][k]);
    }
    fprintf(out, "# verify_fail %lld\n# max_steps %d\n# DONE\n", st_verify_fail, st_maxm);
    fclose(out); fclose(sv); if (pf) fclose(pf);
    return 0;
}
