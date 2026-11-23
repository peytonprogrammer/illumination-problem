/* shootall.c -- all-pairs exact shooting on a marked origami (from slit45.write_origami).
 *
 * For every primitive (p,q), p,q >= 0, 1 <= p+q <= BOUND, the straight-line
 * map F (one lattice step in direction (p,q), Christoffel word as in d11's
 * shoot45) is a permutation of the squares.  Squares whose bottom-left point
 * is a corner block.  Each cycle of F is cut at its blocked squares into
 * corner-free segments; any two lattice points on one segment are joined by
 * a billiard path.  The lit relation on eligible points is accumulated as
 * bitsets.  Stops early once every eligible pair is lit (unless BEST=1).
 *
 * For the designated pair (S,T) it also reports
 *   first: the witness in the first direction (by p+q) that lights it,
 *   best : the witness of minimum Euclidean length m^2 (p^2+q^2), over all
 *          directions with p+q <= BOUND (always scans all directions).
 * Witness = S, room direction g^-1 (p,q) with g the square's D4 element, m steps.
 *
 * usage: shootall BOUND file   -> one line of key=value output; unlit pairs on
 *        following lines "U i j" (eligible indices), at most 200.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static const int GM[8][4] = { {1,0,0,1}, {0,-1,1,0}, {-1,0,0,-1}, {0,1,-1,0},
                              {1,0,0,-1}, {-1,0,0,1}, {0,1,1,0}, {0,-1,-1,0} };
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

int main(int argc, char **argv) {
    int bound = atoi(argv[1]);
    FILE *fp = fopen(argv[2], "r");
    int nsq; if (fscanf(fp, "%d", &nsq) != 1) return 2;
    int *H = malloc(nsq * sizeof(int)), *V = malloc(nsq * sizeof(int)), *lab = malloc(nsq * sizeof(int)), *sqg = malloc(nsq * sizeof(int));
    for (int i = 0; i < nsq; i++) if (fscanf(fp, "%d", &H[i]) != 1) return 2;
    for (int i = 0; i < nsq; i++) if (fscanf(fp, "%d", &V[i]) != 1) return 2;
    for (int i = 0; i < nsq; i++) if (fscanf(fp, "%d", &lab[i]) != 1) return 2;
    for (int i = 0; i < nsq; i++) if (fscanf(fp, "%d", &sqg[i]) != 1) return 2;
    int npt, nel; if (fscanf(fp, "%d %d", &npt, &nel) != 2) return 2;
    int *corner = malloc(npt * sizeof(int)), *el = malloc(npt * sizeof(int));
    for (int i = 0; i < npt; i++) if (fscanf(fp, "%d %d", &corner[i], &el[i]) != 2) return 2;
    int S, T; if (fscanf(fp, "%d %d", &S, &T) != 2) return 2;
    fclose(fp);
    int W = (nel + 63) / 64;
    uint64_t *lit = calloc((size_t)nel * W, 8), *mask = calloc(W, 8);
    long long total = (long long)nel * (nel - 1) / 2, nlit = 0;
    int *blk = malloc(nsq * sizeof(int)), *F = malloc(nsq * sizeof(int)), *seen = malloc(nsq * sizeof(int));
    int *seg = malloc(nsq * sizeof(int));
    for (int s = 0; s < nsq; s++) blk[s] = corner[lab[s]];
    int first_d[3] = {0, 0, 0}, have_first = 0;   /* room dx, dy, m */
    long long best_len = -1; int best_d[5] = {0};  /* dx dy m p q */
    int last_sum = 0, ndir = 0;
    unsigned char word[4096];
    for (int sum = 1; sum <= bound; sum++) {
        for (int p = sum; p >= 0; p--) {
            int q = sum - p;
            if (gcd(p, q) != 1) continue;
            ndir++;
            int L = 0;
            if (p >= 1 && q >= 1) {
                int a = 1, b = 1;
                while (a < p || b < q) {
                    long uv = (a < p) ? (long)q * a : 1L << 60;
                    long uh = (b < q) ? (long)p * b : 1L << 60;
                    if (uv < uh) { word[L++] = 0; a++; } else { word[L++] = 1; b++; }
                }
            }
            for (int s = 0; s < nsq; s++) {
                int c = s;
                if (q == 0) c = H[s];
                else if (p == 0) c = V[s];
                else { for (int t = 0; t < L; t++) c = word[t] ? V[c] : H[c]; c = H[V[c]]; }
                F[s] = c;
            }
            /* designated pair: from each S lift follow F */
            if (S >= 0) {
                for (int s = 0; s < nsq; s++) {
                    if (el[lab[s]] != S || corner[lab[s]]) continue;
                    int c = F[s], m = 1;
                    while (c != s && !blk[c]) {
                        if (el[lab[c]] == T) {
                            const int *g = GM[sqg[s]];   /* inverse of orthogonal g is its transpose */
                            int dx = g[0] * p + g[2] * q, dy = g[1] * p + g[3] * q;
                            if (!have_first) { have_first = 1; first_d[0] = dx; first_d[1] = dy; first_d[2] = m; }
                            long long len = (long long)m * m * (p * p + q * q);
                            if (best_len < 0 || len < best_len) { best_len = len; best_d[0] = dx; best_d[1] = dy; best_d[2] = m; best_d[3] = p; best_d[4] = q; }
                            break;
                        }
                        c = F[c]; m++;
                    }
                }
            }
            if (nlit == total) continue;
            /* segments: rotate each cycle to start at a blocked square, cut at blocked squares */
            for (int s = 0; s < nsq; s++) seen[s] = 0;
            for (int s0 = 0; s0 < nsq; s0++) {
                if (seen[s0]) continue;
                int len = 0, c = s0, start = 0;
                do { seg[len++] = c; seen[c] = 1; c = F[c]; } while (c != s0);
                for (int i = 0; i < len; i++) if (blk[seg[i]]) { start = i; break; }
                int lo = 0, cnt = 0;   /* lo: offset of current segment's first member */
                memset(mask, 0, W * 8);
                for (int t = 0; t <= len; t++) {
                    int sq_ = seg[(start + t) % len];
                    int flush = (t == len) || (t > 0 && blk[sq_]);
                    if (flush) {
                        if (cnt >= 2)
                            for (int u = lo; u < t; u++) {
                                int e = el[lab[seg[(start + u) % len]]];
                                if (e >= 0) { uint64_t *row = lit + (size_t)e * W; for (int w = 0; w < W; w++) row[w] |= mask[w]; }
                            }
                        memset(mask, 0, W * 8); cnt = 0; lo = t + 1;
                        if (t == len) break;
                        continue;
                    }
                    if (t == 0 && blk[sq_]) { lo = 1; continue; }
                    int e = el[lab[sq_]];
                    if (e >= 0) { mask[e >> 6] |= 1ULL << (e & 63); cnt++; }
                }
            }
            long long pc = 0, dg = 0;
            for (int e = 0; e < nel; e++) {
                uint64_t *row = lit + (size_t)e * W;
                for (int w = 0; w < W; w++) pc += __builtin_popcountll(row[w]);
                dg += row[e >> 6] >> (e & 63) & 1;
            }
            nlit = (pc - dg) / 2;
            last_sum = sum;
        }
    }
    printf("ndir=%d nel=%d pairs=%lld lit=%lld unlit=%lld lastsum=%d", ndir, nel, total, nlit, total - nlit, last_sum);
    if (S >= 0) {
        if (have_first) printf(" first=%d,%d,%d best=%d,%d,%d bestpq=%d,%d", first_d[0], first_d[1], first_d[2], best_d[0], best_d[1], best_d[2], best_d[3], best_d[4]);
        else printf(" first=none best=none");
    }
    printf("\n");
    int shown = 0;
    for (int e = 0; e < nel && shown < 200; e++)
        for (int f = e + 1; f < nel && shown < 200; f++)
            if (!(lit[(size_t)e * W + (f >> 6)] >> (f & 63) & 1)) { printf("U %d %d\n", e, f); shown++; }
    return 0;
}
