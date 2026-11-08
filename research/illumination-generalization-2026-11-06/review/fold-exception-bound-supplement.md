# Transparent exceptions in a literal parity-fold assembly

Hand corollary to fold-wall-bound-scope.md, within its ORIGINAL R21 effort. Candidate for independent review. No room, ray or orbit computation. This uses the historically accepted W<=21,k<=6 illumination theorem only in its exact canonical presentation.

## Hypotheses and notation

Use the whole-copy assembly and cellulation hypotheses of fold-wall-bound-scope.md. In addition require Q to be a canonical45 triangle disk, every copy map to preserve the integer grid, and every allowed noncorner integer point of B to map to an A point of Q under EVERY copy map. This last condition is explicit: it follows, for example, from a prescribed residue class preserved by all base-wall reflections and an initial placement mapping that class to A. It does not follow merely because two actual marks are A.

All other integer points of B are actual corners. Let k_Q count all interior or smooth-boundary non-A lattice points in Q, exactly as in the historical baseline. Keep its presentation fixed; do not renormalize or remove marks. Use E,I,N_s from the preceding packet.

## Every transparent non-A point is a seam junction

Take a transparent non-A integer point x of Q. If it lies in a copy interior or a smooth copy-wall interior, its inverse image is a noncorner integer point of B, hence in the permitted class, whose image is A by hypothesis. That is impossible. It therefore lies at a copy corner. At a genuine Q boundary corner it would not be transparent. Thus x is either a smooth boundary seam junction or an interior seam junction. This is an inclusion; some such junctions can be A and need not count.

Consequently

    k_Q <= N_s+I.

The seam-end and Euler counts already proved give

    2E >= N_s+4I,
    E=m+I-1,

so

    k_Q <= N_s+I <= 2m-2-I <= 2m-2.           (B)

The possible presence of other smooth/interior allowed-class points does not change this bound: they are A and are not counted in k_Q.

## Baseline consequence

If m<=4 and W(Q)<=21, (B) gives k_Q<=6. The accepted all-support/all-pair canonical45 baseline then proves illumination for EVERY distinct actual interior A pair in Q. This uses no parity-darkness projection theorem and needs no new optical path census. In particular such a Q cannot be a genuine dark parity-fold example with actual distinct interior A marks.

Combining (A) from fold-wall-bound-scope.md with W<=21 shows that a base with w>=8 has m<=4, since

    4m+4 <= m*(w-4)+4 <= W <=21.

Thus EVERY assembly satisfying these explicit grid/class hypotheses with base w>=8 is already covered by the historical theorem under W<=21. No new w>=10 diagonal-base minimum is needed for this restricted consequence.

A hypothetical dark assembly within W<=21 must therefore violate the stated grid/class hypotheses OR have BOTH m>=5 and w<=7. This is a necessary restriction, not existence of such a small base and not a classification of dark rooms. In particular it does not prove that an arbitrary dark room has any such decomposition. That necessity remains the main missing implication in the proposed route.

## Dependencies and trust boundary

The geometric identities are new hand work pending independent review. The optical implication relies on the already reconciled historical theorem under review/baseline-review.md and baseline-check.json, rather than replaying its multi-gigabyte certificates. Formula(B) and the m<=4 implication are independent algebraic derivations. The old theorem's k<=6 hypothesis is used exactly; it has not been removed from arbitrary rooms.
