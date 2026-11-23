/* enum45.c -- rooms made of canonical45 tiles (polyaboloes).
 *
 * Tiling: lines x in Z, y in Z, x + y in 2Z, x - y in 2Z.  Square (i,j) =
 * [i,i+1]x[j,j+1] is cut along its A-B diagonal: "/" if i+j even, "\" if odd.
 *   "/" : h=0 = (i,j)(i+1,j)(i+1,j+1),  h=1 = (i,j)(i,j+1)(i+1,j+1)
 *   "\" : h=0 = (i,j)(i+1,j)(i,j+1),    h=1 = (i+1,j)(i+1,j+1)(i,j+1)
 * Classes: A = (even,even), B = (odd,odd) (8 tiles, angle pi/4 each),
 *          C = mixed (4 tiles, angle pi/2 each).
 * Symmetry group G of the tiling: translations (a,b) with a+b even, and the
 * 8 linear maps of D4 (fixing the A point at the origin).
 *
 * Room = finite edge-connected set of tiles whose union is a closed disk with
 * a simple boundary: no pinch vertex (tiles around every vertex form one
 * cyclic run) and V - E + F = 1.  W = number of corners = boundary vertices
 * whose run is not a straight angle (A/B: run length != 4; C: != 2).
 *
 * Modes
 *   plain NMAX WMAX OUTMIN FREEFLAG JOBS JOB SPLITDEPTH out counts : every fixed polyabolo up to
 *       NMAX (Redelmeier, translation-normalised, 4 roots).  Counts fixed and
 *       (if FREEFLAG) free polyaboloes per size; writes free rooms with size >=
 *       OUTMIN, W <= WMAX and an eligible pair (two interior points of one
 *       class: A, B (8-tile) or C (4-tile)).
 *   star NMAX WMAX TA TB JOBS JOB SPLITDEPTH out counts : every room with
 *       S = (0,0) and T = (2TA,2TB) interior A points (full stars), size <=
 *       NMAX, W <= WMAX; output only if this embedding is the canonical one
 *       (see README: minimum (T, tile list) over all embeddings g, S', T').
 *   cstar NMAX WMAX U V JOBS JOB SPLITDEPTH out counts : the same for C
 *       pairs: S = (1,0) and T = (1+U, V) interior C points (4-tile stars),
 *       U >= 1, 0 <= V <= U, U + V even; canonical over all C-pair embeddings.
 *   dlist NMAX : print the T vectors (2a,2b), a>=1, 0<=b<=a, for which a
 *       room of size <= NMAX can contain both stars.
 *   cdlist NMAX : the same for C pairs (U,V).
 * Output room line: "N W i j h i j h ..." with the canonical form under G.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define GS 128
#define OFF 64
#define NT (GS * GS * 2)
#define GV (GS + 1)
#define NV (GV * GV)
#define NE (GV * GV * 3)
#define MAXN 40

static int tvx[NT][3], tvy[NT][3], tvid[NT][3], ted[NT][3], nb[NT][3];
static int etile[NE][2];
static int vstar[NV][8], vdeg[NV];

static int tid(int i, int j, int h) { return ((j * GS) + i) * 2 + h; }  /* row-major order (j,i,h) */
static int vid(int x, int y) { return x * GV + y; }
static int cls(int x, int y) { return ((x & 1) == 0 && (y & 1) == 0) ? 0 : ((x & 1) && (y & 1)) ? 1 : 2; }

static int eid(int x1, int y1, int x2, int y2) {
    int mx = x1 < x2 ? x1 : x2, my = y1 < y2 ? y1 : y2;
    if (y1 == y2) return 3 * vid(mx, y1) + 0;
    if (x1 == x2) return 3 * vid(x1, my) + 1;
    return 3 * vid(mx, my) + 2;
}

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

static void init_geom(void) {
    memset(etile, -1, sizeof etile);
    memset(vdeg, 0, sizeof vdeg);
    for (int j = 0; j < GS; j++)
        for (int i = 0; i < GS; i++)
            for (int h = 0; h < 2; h++) {
                int t = tid(i, j, h);
                tile_verts(i, j, h, tvx[t], tvy[t]);
                for (int k = 0; k < 3; k++) tvid[t][k] = vid(tvx[t][k], tvy[t][k]);
                for (int k = 0; k < 3; k++) {
                    int a = k, b = (k + 1) % 3;
                    int e = eid(tvx[t][a], tvy[t][a], tvx[t][b], tvy[t][b]);
                    ted[t][k] = e;
                    if (etile[e][0] < 0) etile[e][0] = t; else etile[e][1] = t;
                }
            }
    for (int t = 0; t < NT; t++)
        for (int k = 0; k < 3; k++) {
            int e = ted[t][k];
            nb[t][k] = etile[e][0] == t ? etile[e][1] : etile[e][0];
        }
    /* vertex stars in ccw order */
    for (int x = 1; x < GS; x++)
        for (int y = 1; y < GS; y++) {
            int v = vid(x, y), m = 0, ts[8];
            double ang[8];
            for (int di = -1; di <= 0; di++)
                for (int dj = -1; dj <= 0; dj++)
                    for (int h = 0; h < 2; h++) {
                        int t = tid(x + di, y + dj, h);
                        if (tvid[t][0] == v || tvid[t][1] == v || tvid[t][2] == v) {
                            int sx = tvx[t][0] + tvx[t][1] + tvx[t][2] - 3 * x;
                            int sy = tvy[t][0] + tvy[t][1] + tvy[t][2] - 3 * y;
                            ts[m] = t; ang[m] = atan2((double)sy, (double)sx); m++;
                        }
                    }
            for (int a = 1; a < m; a++)
                for (int b = a; b > 0 && ang[b] < ang[b - 1]; b--) {
                    double tmp = ang[b]; ang[b] = ang[b - 1]; ang[b - 1] = tmp;
                    int ti = ts[b]; ts[b] = ts[b - 1]; ts[b - 1] = ti;
                }
            int want = cls(x, y) == 2 ? 4 : 8;
            if (m != want) { fprintf(stderr, "star size %d at %d %d\n", m, x, y); exit(5); }
            vdeg[v] = m;
            for (int a = 0; a < m; a++) vstar[v][a] = ts[a];
        }
}

/* ------------------------------------------------------------ room state */
static unsigned char inR[NT];
static int R[MAXN], nR;
static int vref[NV], eref[NE];
static int Vc, Ec;
static int vlist[3 * MAXN + 8], nvl;      /* vertices with vref > 0 (unordered) */
static int vpos[NV];

static void add_tile(int t) {
    inR[t] = 1; R[nR++] = t;
    for (int k = 0; k < 3; k++) {
        if (vref[tvid[t][k]]++ == 0) { Vc++; vpos[tvid[t][k]] = nvl; vlist[nvl++] = tvid[t][k]; }
        if (eref[ted[t][k]]++ == 0) Ec++;
    }
}
static void remove_tile(int t) {
    inR[t] = 0; nR--;
    for (int k = 0; k < 3; k++) {
        if (--vref[tvid[t][k]] == 0) {
            int v = tvid[t][k], p = vpos[v], last = vlist[--nvl];
            vlist[p] = last; vpos[last] = p; Vc--;
        }
        if (--eref[ted[t][k]] == 0) Ec--;
    }
}

/* returns W, or -1 if not strictly simple (pinch or hole) */
static int room_walls(void) {
    if (Vc - Ec + nR != 1) return -1;
    int W = 0;
    for (int a = 0; a < nvl; a++) {
        int v = vlist[a];
        int d = vdeg[v], c = 0, runs = 0;
        for (int s = 0; s < d; s++) {
            int here = inR[vstar[v][s]], prev = inR[vstar[v][(s + d - 1) % d]];
            c += here;
            if (here && !prev) runs++;
        }
        if (c == d) continue;
        if (runs != 1) return -1;
        if (c != d / 2) W++;
    }
    return W;
}

/* full-star (interior) points of the room by class; coordinates absolute */
static int interior_points(int *px, int *py, int *pc) {
    int n = 0;
    for (int a = 0; a < nvl; a++) {
        int v = vlist[a];
        int d = vdeg[v], c = 0;
        for (int s = 0; s < d; s++) c += inR[vstar[v][s]];
        if (c == d) { px[n] = v / GV; py[n] = v % GV; pc[n] = cls(px[n], py[n]); n++; }
    }
    return n;
}

/* ------------------------------------------------------------ symmetry */
static const int GM[8][4] = { {1,0,0,1}, {0,-1,1,0}, {-1,0,0,-1}, {0,1,-1,0},
                              {1,0,0,-1}, {-1,0,0,1}, {0,1,1,0}, {0,-1,-1,0} };

/* tile from 3*centroid (absolute) */
static int tile_from_c3(int X, int Y) {
    if (X < 0 || Y < 0) return -1;
    int i = X / 3, j = Y / 3, a = X % 3, b = Y % 3, p = (i + j) & 1;
    if (i >= GS || j >= GS) return -1;
    if (!p) { if (a == 2 && b == 1) return tid(i, j, 0); if (a == 1 && b == 2) return tid(i, j, 1); }
    else    { if (a == 1 && b == 1) return tid(i, j, 0); if (a == 2 && b == 2) return tid(i, j, 1); }
    fprintf(stderr, "bad centroid %d %d\n", X, Y); exit(6);
}

static int c3x[MAXN], c3y[MAXN];
static void centroids(void) {
    for (int a = 0; a < nR; a++) {
        int t = R[a];
        c3x[a] = tvx[t][0] + tvx[t][1] + tvx[t][2];
        c3y[a] = tvy[t][0] + tvy[t][1] + tvy[t][2];
    }
}

static void isort(int *a, int n) { for (int i = 1; i < n; i++) { int v = a[i], j = i; while (j > 0 && a[j - 1] > v) { a[j] = a[j - 1]; j--; } a[j] = v; } }

/* image of the room under g, translated by -(3*sx, 3*sy) in centroid units, then +3*(ox,oy) ; sorted ids */
static void image(int g, int sx, int sy, int ox, int oy, int *out) {
    for (int a = 0; a < nR; a++) {
        int X = c3x[a] - 3 * sx, Y = c3y[a] - 3 * sy;
        int X2 = GM[g][0] * X + GM[g][1] * Y + 3 * ox, Y2 = GM[g][2] * X + GM[g][3] * Y + 3 * oy;
        out[a] = tile_from_c3(X2, Y2);
        if (out[a] < 0) { fprintf(stderr, "image off grid\n"); exit(7); }
    }
    isort(out, nR);
}

/* image under g, translated by L so that its minimum tile sits in square (OFF,OFF) or (OFF+1,OFF) */
static void norm_image(int g, int *tmp) {
    image(g, OFF, OFF, OFF, OFF, tmp);
    int t0 = tmp[0], i0 = (t0 / 2) % GS, j0 = (t0 / 2) / GS;
    int dx = OFF - i0, dy = OFF - j0;
    if ((dx + dy) & 1) dx += 1;
    for (int a = 0; a < nR; a++) {
        int t = tmp[a], h = t & 1, i = (t / 2) % GS, j = (t / 2) / GS;
        tmp[a] = tid(i + dx, j + dy, h);
    }
}

/* canonical form under G: for each g, translate so the minimum tile sits in square (OFF,OFF) or (OFF+1,OFF) */
static void canon_free(int *best) {
    int tmp[MAXN], have = 0;
    centroids();
    for (int g = 0; g < 8; g++) {
        image(g, OFF, OFF, OFF, OFF, tmp);
        int t0 = tmp[0], i0 = (t0 / 2) % GS, j0 = (t0 / 2) / GS;
        int dx = OFF - i0, dy = OFF - j0;
        if ((dx + dy) & 1) dx += 1;
        for (int a = 0; a < nR; a++) {
            int t = tmp[a], h = t & 1, i = (t / 2) % GS, j = (t / 2) / GS;
            tmp[a] = tid(i + dx, j + dy, h);   /* (dx,dy) in L keeps the diagonal type and h */
        }
        if (!have || memcmp(tmp, best, sizeof(int) * nR) < 0) { memcpy(best, tmp, sizeof(int) * nR); have = 1; }
    }
}

static void write_room(FILE *f, int W, const int *ids) {
    fprintf(f, "%d %d", nR, W);
    for (int a = 0; a < nR; a++) {
        int t = ids[a], h = t & 1, i = (t / 2) % GS - OFF, j = (t / 2) / GS - OFF;
        fprintf(f, " %d %d %d", i, j, h);
    }
    fputc('\n', f);
}

/* ------------------------------------------------------------ counters */
static long long cnt_fixed[MAXN + 1], cnt_free[MAXN + 1], cnt_nodes;
static long long cnt_rooms[MAXN + 1][64], cnt_out[MAXN + 1][64];
static long long cnt_simple_any[MAXN + 1];

static int NMAX, WMAX, OUTMIN, FREEFLAG;
static FILE *fout;

/* ------------------------------------------------------------ plain mode */
static int ROOT;
static int JOBS = 1, JOB = 0, SPLIT = 0, splitctr = 0;
static void plain_process(void) {
    int n = nR;
    if (JOBS > 1 && n < SPLIT && JOB != 0) return;      /* levels above the split: job 0 only */
    cnt_fixed[n]++;
    if (!FREEFLAG && n < OUTMIN) return;
    int W = room_walls();
    if (!FREEFLAG && (W < 0 || W > WMAX)) return;
    int best[MAXN], tmp[MAXN];
    /* free canonical acceptance: the normalised identity image must be <= every normalised image (early exit) */
    centroids();
    norm_image(0, best);
    for (int g = 1; g < 8; g++) {
        norm_image(g, tmp);
        if (memcmp(tmp, best, sizeof(int) * n) < 0) return;
    }
    cnt_free[n]++;
    if (W < 0) return;
    cnt_simple_any[n]++;
    cnt_rooms[n][W]++;
    if (n < OUTMIN || W > WMAX) return;
    int px[3 * MAXN], py[3 * MAXN], pc[3 * MAXN];
    int np = interior_points(px, py, pc), c3[3] = {0, 0, 0};
    for (int a = 0; a < np; a++) c3[pc[a]]++;
    if (c3[0] >= 2 || c3[1] >= 2 || c3[2] >= 2) { cnt_out[n][W]++; write_room(fout, W, best); }
}

static unsigned char seen[NT];
static void rec_plain(int *untried, int nu) {
    int nl[3 * MAXN + 8];
    while (nu > 0) {
        int c = untried[--nu];
        add_tile(c);
        cnt_nodes++;
        int ok = 1;
        if (nR == SPLIT && JOBS > 1) ok = (splitctr++ % JOBS) == JOB;
        if (ok) plain_process();
        if (ok && nR < NMAX) {
            memcpy(nl, untried, sizeof(int) * nu);
            int m = nu, added[3], na = 0;
            for (int k = 0; k < 3; k++) {
                int d = nb[c][k];
                if (d < 0 || d < ROOT || seen[d]) continue;
                seen[d] = 1; nl[m++] = d; added[na++] = d;
            }
            rec_plain(nl, m);
            for (int k = 0; k < na; k++) seen[added[k]] = 0;
        }
        remove_tile(c);
    }
}

/* ------------------------------------------------------------ star mode */
static int isT[NT], dist[NT];
static int TA, TB;
static int starS[8], starT[8];
static int SC = 8, CMODE = 0, SXO = OFF;   /* star size, C-pair mode, x of S */
static int nTin, rejT;

static void bfs_dist(const int *src, int ns) {
    static int q[NT];
    for (int t = 0; t < NT; t++) dist[t] = 1 << 20;
    int qh = 0, qt = 0;
    for (int a = 0; a < ns; a++) { dist[src[a]] = 0; q[qt++] = src[a]; }
    while (qh < qt) {
        int t = q[qh++];
        for (int k = 0; k < 3; k++) { int d = nb[t][k]; if (d >= 0 && dist[d] > dist[t] + 1) { dist[d] = dist[t] + 1; q[qt++] = d; } }
    }
}

static long long cnt_candidates, cnt_reject_canon;

static int lexless(int ta, int tb, const int *ids, int ta2, int tb2, const int *ids2, int n) {
    /* (ta,tb,ids) < (ta2,tb2,ids2) ? -1 / 0 / 1 */
    if (ta != ta2) return ta < ta2 ? -1 : 1;
    if (tb != tb2) return tb < tb2 ? -1 : 1;
    int c = memcmp(ids, ids2, sizeof(int) * n);
    return c < 0 ? -1 : c > 0;
}

static void star_process(void) {
    if (JOBS > 1 && nR < SPLIT && JOB != 0) return;   /* rooms above the split level: job 0 only */
    int W = room_walls();
    if (W < 0) return;
    cnt_candidates++;
    if (W > WMAX) return;
    int n = nR;
    /* canonical embedding test */
    int px[3 * MAXN], py[3 * MAXN], pc[3 * MAXN];
    int np = interior_points(px, py, pc);
    centroids();
    int cur[MAXN], tmp[MAXN];
    image(0, SXO, OFF, SXO, OFF, cur);
    for (int a = 0; a < np; a++)
        for (int b = 0; b < np; b++) {
            if (a == b || pc[a] != pc[b] || (pc[a] == 2) != CMODE) continue;
            int vx = px[b] - px[a], vy = py[b] - py[a];
            for (int g = 0; g < 8; g++) {
                int wx = GM[g][0] * vx + GM[g][1] * vy, wy = GM[g][2] * vx + GM[g][3] * vy;
                if (!(wx >= 1 && wy >= 0 && wy <= wx)) continue;
                int ta = CMODE ? wx : wx / 2, tb = CMODE ? wy : wy / 2;
                if (ta > TA || (ta == TA && tb > TB)) continue;   /* larger key: cannot beat current */
                image(g, px[a], py[a], SXO, OFF, tmp);
                if (lexless(ta, tb, tmp, TA, TB, cur, n) < 0) { cnt_reject_canon++; return; }
            }
        }
    int best[MAXN];
    canon_free(best);
    cnt_rooms[n][W]++;
    cnt_out[n][W]++;
    write_room(fout, W, best);
}

static void rec_star(int *untried, int nu, int delta) {
    int nl[3 * MAXN + 16];
    int popped_T = 0;
    while (nu > 0) {
        int c = untried[--nu];
        int nd = delta < dist[c] ? delta : dist[c];
        add_tile(c);
        if (isT[c]) nTin++;
        cnt_nodes++;
        int lb = (SC - nTin) + (nd >= 1 ? nd - 1 : 0);
        int ok = 1;
        if (nR == SPLIT && JOBS > 1) { ok = (splitctr++ % JOBS) == JOB; }
        if (ok && rejT == 0 && nR + lb <= NMAX) {
            if (nTin == SC) star_process();
            if (nR < NMAX) {
                memcpy(nl, untried, sizeof(int) * nu);
                int m = nu, added[3], na = 0;
                for (int k = 0; k < 3; k++) {
                    int d = nb[c][k];
                    if (d < 0 || seen[d]) continue;
                    seen[d] = 1; nl[m++] = d; added[na++] = d;
                }
                rec_star(nl, m, nd);
                for (int k = 0; k < na; k++) seen[added[k]] = 0;
            }
        }
        if (isT[c]) { nTin--; rejT++; popped_T++; }
        remove_tile(c);
    }
    rejT -= popped_T;
}

static void star_of(int x, int y, int *out) { int v = vid(x, y); for (int a = 0; a < vdeg[v]; a++) out[a] = vstar[v][a]; }

static int min_dist_S(void) { int m = 1 << 20; for (int a = 0; a < SC; a++) if (dist[starS[a]] < m) m = dist[starS[a]]; return m; }

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: see header\n"); return 1; }
    init_geom();
    if (!strcmp(argv[1], "dlist")) {
        int nmax = atoi(argv[2]);
        star_of(OFF, OFF, starS);
        for (int a = 1; 2 * a < OFF - 8; a++)
            for (int b = 0; b <= a; b++) {
                star_of(OFF + 2 * a, OFF + 2 * b, starT);
                bfs_dist(starT, 8);
                int d = min_dist_S();
                int need = 16 + (d >= 1 ? d - 1 : 0);
                if (need <= nmax) printf("%d %d %d\n", a, b, need);
            }
        return 0;
    }
    if (!strcmp(argv[1], "cdlist")) {
        int nmax = atoi(argv[2]);
        SC = 4; SXO = OFF + 1;
        star_of(SXO, OFF, starS);
        for (int u = 1; u < OFF - 8; u++)
            for (int v = (u & 1); v <= u; v += 2) {
                star_of(SXO + u, OFF + v, starT);
                bfs_dist(starT, 4);
                int d = min_dist_S();
                int need = 8 + (d >= 1 ? d - 1 : 0);
                if (need <= nmax) printf("%d %d %d\n", u, v, need);
            }
        return 0;
    }
    if (!strcmp(argv[1], "plain")) {
        NMAX = atoi(argv[2]); WMAX = atoi(argv[3]); OUTMIN = atoi(argv[4]); FREEFLAG = atoi(argv[5]);
        JOBS = atoi(argv[6]); JOB = atoi(argv[7]); SPLIT = atoi(argv[8]);
        fout = fopen(argv[9], "w");
        FILE *fc = fopen(argv[10], "w");
        /* 4 roots: tile orbits under L.  Root in square (OFF,OFF) h=0,1 and (OFF+1,OFF) h=0,1. */
        int roots[4] = { tid(OFF, OFF, 0), tid(OFF, OFF, 1), tid(OFF + 1, OFF, 0), tid(OFF + 1, OFF, 1) };
        for (int r = 0; r < 4; r++) {
            ROOT = roots[r];
            memset(seen, 0, sizeof seen);
            seen[ROOT] = 1;
            int u[1] = { ROOT };
            rec_plain(u, 1);
        }
        fprintf(fc, "# plain NMAX %d WMAX %d OUTMIN %d FREE %d job %d/%d split %d nodes %lld\n", NMAX, WMAX, OUTMIN, FREEFLAG, JOB, JOBS, SPLIT, cnt_nodes);
        for (int n = 1; n <= NMAX; n++) fprintf(fc, "fixed %d %lld free %lld simple %lld\n", n, cnt_fixed[n], cnt_free[n], cnt_simple_any[n]);
        for (int n = 1; n <= NMAX; n++) for (int w = 0; w < 64; w++)
            if (cnt_rooms[n][w]) fprintf(fc, "rooms %d %d %lld eligible_out %lld\n", n, w, cnt_rooms[n][w], cnt_out[n][w]);
        fprintf(fc, "# DONE\n");
        fclose(fout); fclose(fc);
        return 0;
    }
    if (!strcmp(argv[1], "star") || !strcmp(argv[1], "cstar")) {
        NMAX = atoi(argv[2]); WMAX = atoi(argv[3]); TA = atoi(argv[4]); TB = atoi(argv[5]);
        if (!strcmp(argv[1], "cstar")) {
            CMODE = 1; SC = 4; SXO = OFF + 1;
            if (TA < 1 || TB < 0 || TB > TA || ((TA + TB) & 1)) { fprintf(stderr, "bad C vector\n"); return 1; }
        }
        JOBS = atoi(argv[6]); JOB = atoi(argv[7]); SPLIT = atoi(argv[8]);
        fout = fopen(argv[9], "w");
        FILE *fc = fopen(argv[10], "w");
        star_of(SXO, OFF, starS);
        if (CMODE) star_of(SXO + TA, OFF + TB, starT); else star_of(OFF + 2 * TA, OFF + 2 * TB, starT);
        for (int a = 0; a < SC; a++) isT[starT[a]] = 1;
        bfs_dist(starT, SC);
        memset(seen, 0, sizeof seen);
        for (int a = 0; a < SC; a++) { seen[starS[a]] = 1; add_tile(starS[a]); if (isT[starS[a]]) nTin++; }
        int delta = min_dist_S();
        int u[3 * MAXN], nu = 0;
        for (int a = 0; a < SC; a++)
            for (int k = 0; k < 3; k++) { int d = nb[starS[a]][k]; if (d >= 0 && !seen[d]) { seen[d] = 1; u[nu++] = d; } }
        rec_star(u, nu, delta);
        fprintf(fc, "# %s NMAX %d WMAX %d T %d %d job %d/%d split %d nodes %lld simple_candidates %lld canon_rejects %lld\n",
                argv[1], NMAX, WMAX, TA, TB, JOB, JOBS, SPLIT, cnt_nodes, cnt_candidates, cnt_reject_canon);
        for (int n = 1; n <= NMAX; n++) for (int w = 0; w < 64; w++)
            if (cnt_rooms[n][w]) fprintf(fc, "rooms %d %d %lld\n", n, w, cnt_rooms[n][w]);
        fprintf(fc, "# DONE\n");
        fclose(fout); fclose(fc);
        return 0;
    }
    return 1;
}
