/* harness.c -- query cover.c's own certificate for single pairs (d96 referee).
 *
 * Reuses cover.c verbatim (compute_dir, lambda_at, subtract, in_qset) by
 * including it with its main renamed. For a source S treated as a point cell
 * (the code path cover.c uses for 0-dimensional live cells), Q(S) is
 * accumulated over the directions 1 <= p, q <= B in cover.c's order. A target
 * T is CERTIFIED when T is outside every closed polygon of Q(S), i.e. cover.c
 * asserts T in Ill_Theta(S). The first direction after which T leaves Q(S) is
 * printed.
 *
 * stdin: line 1 "area W x0 y0 ...", then lines "sx sy sd tx ty td" (integers,
 * points (sx/sd, sy/sd), (tx/td, ty/td) in file coordinates).
 * stdout: one line per pair: "CERT p q" or "NOCERT".
 * usage: harness B [dump]  (dump: print cover.c's labels for every direction)
 */
#define main cover_main
#include "../d13-cylinder-cover/cover.c"
#undef main

int main(int argc, char **argv) {
    int Bq = atoi(argv[1]);
    int t[4000][2], n = 0;
    for (int p = 1; p <= Bq; p++) for (int q = 1; q <= Bq; q++) if (gcdl(p, q) == 1) { t[n][0] = p; t[n][1] = q; n++; }
    qsort(t, n, sizeof t[0], cmpdir);
    memset(cellid, -1, sizeof cellid);
    int area, W; if (scanf("%d %d", &area, &W) != 2) return 1;
    int ox[MAXCELL], oy[MAXCELL];
    for (int c = 0; c < area; c++) if (scanf("%d %d", &ox[c], &oy[c]) != 2) return 1;
    ncell = area;
    int sx = ox[0], sy = oy[0];
    for (int c = 1; c < area; c++) { if (ox[c] < sx) sx = ox[c]; if (oy[c] < sy) sy = oy[c]; }
    sx -= 1; sy -= 1;
    for (int c = 0; c < area; c++) { CX[c] = ox[c] - sx; CY[c] = oy[c] - sy; cellid[CX[c]][CY[c]] = c; }
    build_surface();
    static Dir dirs[400];
    for (int i = 0; i < n; i++) compute_dir(&dirs[i], t[i][0], t[i][1]);
    if (argc > 2 && !strcmp(argv[2], "dump")) {
        /* labels per direction, cell (file coords), family: strips then line flags */
        for (int i = 0; i < n; i++) {
            Dir *Dd = &dirs[i]; int p = Dd->p, q = Dd->q;
            for (int c = 0; c < ncell; c++) {
                printf("D %d %d C %d %d P", p, q, ox[c], oy[c]);
                for (int k = 0; k < p + q; k++) printf(" %d", Dd->plus[c][k]);
                printf(" PL");
                for (int k = 0; k < p + q - 1; k++) printf(" %d", Dd->pline[c][k]);
                printf(" M");
                for (int k = 0; k < p + q; k++) printf(" %d", Dd->minus[c][k]);
                printf(" ML");
                for (int k = 0; k < p + q - 1; k++) printf(" %d", Dd->mline[c][k]);
                printf("\n");
            }
        }
        return 0;
    }
    ll a, b, d, e, f, g;
    while (scanf("%lld %lld %lld %lld %lld %lld", &a, &b, &d, &e, &f, &g) == 6) {
        Pt S = mkpt(a - (i128)sx * d, b - (i128)sy * d, d), T = mkpt(e - (i128)sx * g, f - (i128)sy * g, g);
        QSet *Q = qnew();
        for (int c = 0; c < ncell; c++) { Poly P = square(CX[c], CY[c]); qpush(Q, c, &P); }
        int cert = -1;
        for (int i = 0; i < n && cert < 0; i++) {
            int l1, l2;
            lambda_at(&dirs[i], S, &l1, &l2);
            if (l1 == NONE) continue;
            QSet *R = subtract(Q, &dirs[i], l1, l2);
            qrelease(Q); Q = R;
            if (!in_qset(Q, T)) cert = i;
        }
        if (cert >= 0) printf("CERT %d %d\n", t[cert][0], t[cert][1]); else printf("NOCERT\n");
        qrelease(Q);
    }
    return 0;
}
