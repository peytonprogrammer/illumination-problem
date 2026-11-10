# Cover note for an external reviewer

This packet asks for a mathematical review of one elementary theorem:

> Every finite strictly simple orthogonal polygon with at most eight maximal
> walls illuminates every pair of distinct interior points by a finite
> specular path that avoids every corner.

`theorem-and-proof.md` is self-contained. The proofs were produced and cross-reviewed by AI agents; no human has refereed them and nothing is formalized. The exact checks in `reproduce.md` evaluate the constructions on fixed inputs and are not proofs.

## What to examine, in priority order

1. **Theorem 6.8 Step 4 (earlier arrival at a roof corner).** The identity
   F_a(Beta - sigma) = F_a(Beta + sigma) for Beta in aZ is used to show the
   target is hit on the way up before a corner contact. Check that the
   truncated prefix satisfies the path definition of Section 0, including
   the case y_t = d.
2. **Proposition 6.10 (every staircase satisfies F, Ft, Rv, or Rh).** The
   reduction to dimensionless variables, the strict negations of F and Ft,
   and the sign of (6.4) over 2 sqrt(p) <= s < 1 + p.
3. **Lemma 6.3 and Theorem 6.8 Step 1.** The bound ell >= a Q_v and the
   deduction L > 2a from Rv, with T_0 < d and v > h.
4. **Theorem 6.5 (floor chart).** The two-image choice that avoids both
   floor corners, and that the reflected-source windows use only
   rho' < g/c <= (b - a)/(A - b).
5. **Theorem 3.1 (U fixed point).** The monotone iteration, the argument
   that the fixed point is not a jump, and the floor-contact interval
   (M/2, A - M/2).
6. **Lemma 2.2 and its uses.** A source on the base of an L subroom whose
   base is an internal seam of the larger room (Theorem 5.2 and Theorem 6.6).
7. **Placement splits.** Lemma 6.1, Theorem 3.2, Theorem 4.1, and Theorem
   5.2 claim exhaustive case splits including seam points. Check that every
   L subroom used has artificial boundary in one orientation only and that
   the newly reflex corner of P on that boundary is a smooth point of the
   subroom.
8. **Proposition 1.2.** The claim that each k has one turn word, that
   positivity of edge lengths gives exactly the displayed inequalities, and
   the k = 4 simplicity condition a < B or b < c.

`coverage.md` lists every shape, placement, and guard with its proof
reference, and the known soft points.
