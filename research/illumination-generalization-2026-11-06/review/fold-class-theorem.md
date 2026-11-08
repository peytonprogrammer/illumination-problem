# Verified lower bound for strict canonical parity-fold rooms

This is a readable summary of the independently accepted R21 proof, not a new universal illumination theorem. Exact proof inputs and reviews are indexed in fold-normalization-acceptance.json and its dependencies.

## The proved statement

Take a finite strictly simple canonical45 triangle base B with two distinct smooth boundary A marks a,b. Every integer point of B other than genuine corners must be an A point; other smooth/interior A points are allowed.

Assemble finitely many whole congruent copies of B with disjoint interiors into one strictly simple disk Q. The literal inverse-copy maps must agree at every contact, and the actual interior marks S,T must map to a,b respectively. Then darkness of that actual pair requires at least22 maximal walls. Diagonal bases, shared seam endpoints, cycles and arbitrary initial rigid placements are allowed.

The known22-wall example attains this bound within the class. This is the class minimum, not a minimum for arbitrary polygons.

## Why the bound now covers diagonal bases

1. A strict canonical base with two smooth A marks has w>=8 walls. Triangulated-disk Euler and one A vertex per triangle give w=2+6I_A+3s_A+sum(A-corner fan sizes), since the base has no transparent non-A points. Here s_A>=2.
2. A literal whole-copy assembly has W=m(w-4)+4+D, where m is its number of copies and D>=0. Thus W<=21 forces m<=4.
3. Normalize one copy to B. Literal seam agreement makes every other copy map a word in base-wall reflections. Those preserve the whole canonical triangle tiling and A points, so the normalized actual S,T are distinct interior A points.
4. Every transparent non-A point of the normalized Q must be a smooth boundary or interior seam junction. Euler and seam-end counts bound their number by k<=2m-2<=6.
5. The previously accepted all-support canonical45 theorem for W<=21,k<=6 supplies a finite actual S-to-T path. Reversing the rigid normalization preserves that path. Therefore a dark pair in this class cannot have W<=21.

The new work independently proves the counts and normalization. Step5 reuses the historically verified computer-assisted theorem; its large certificates were not replayed in this effort. Both the new hand proof and its full independent peer review retain all endpoint and class assumptions.

## What remains unproved

An arbitrary dark room is not known to admit this decomposition. In particular no argument currently produces a common strict base, whole congruent pieces, literal pointwise seam agreement, and two DISTINCT SMOOTH base endpoint fibers from darkness alone. fold-route-contract.md states that exact missing implication.

The peer's repaired43-wall beveled example shows that an unrestricted orthogonal-only factor claim is false. It still has a diagonal strict parity factor and does not refute the broader route or the W<=21 target.

A proposed extension allowing common-scale similarity placements is separately recorded in fold-similarity-supplement.md. Its review status belongs to its own receipt; the rigid-placement theorem above is already fully accepted.
