# Exact corner-parity profiles for every integral L

This is a general form of the ALREADY ACCEPTED torus-corner multiplicity obstruction, not a newly discovered mechanism or an availability theorem. Its purpose is to state exactly where that full-group necessary restriction is present and where it disappears. Hand derivation only; no room/orbit census, discovery check or clock.

Let P=[0,A]x[0,B] union [0,a]x[B,H], with integral 0<a<A, 0<B<H. Put gx=gcd(A,a), gy=gcd(H,B). The absolute period lattice is Lambda=2gx Z x 2gy Z, as proved in coverage-frontier.md. The unique genuine cone has torus image c=(a,B). Use c as origin on R^2/Lambda.

## Five regular corner classes, with multiplicity

Every physical convex corner becomes one regular marked point after four-copy unfolding. The five regular marked points have representatives

O=(0,0), X=(A,0), Y=(0,H), E=(A,B), K=(a,H).

All are fixed points of J, and all map into the four two-torsion classes of the period torus. In coordinates modulo 2 put

alpha=a/gx, eta=(A-a)/gx,
beta=B/gy, theta=(H-B)/gy.

Then their respective two-torsion vectors relative to c are

(alpha,beta), (eta,beta), (alpha,theta), (eta,0), (0,theta).

Minus signs disappear modulo 2. Because gcd(a/gx,(A-a)/gx)=1, the pair (alpha,eta) is one of (1,1),(1,0),(0,1). The pair (beta,theta) has the same three possibilities. This uses coordinate coprimality, not a restriction on room size or metric aspect.

Let w(v) count the five REGULAR marks over class v. The cone itself is excluded from w. The complete symbolic parity table is below; columns list the nonzero weight MULTISET, so no unrecorded basis identification is needed.

| (alpha,eta) | (beta,theta) | w(0) | nonzero weights |
|---|---|---:|---|
| (1,1) | (1,1) | 0 | 3,1,1 |
| (1,1) | (1,0) | 1 | 2,2,0 |
| (1,1) | (0,1) | 0 | 3,1,1 |
| (1,0) | (1,1) | 1 | 2,2,0 |
| (1,0) | (1,0) | 2 | 1,1,1 |
| (1,0) | (0,1) | 2 | 1,1,1 |
| (0,1) | (1,1) | 0 | 3,1,1 |
| (0,1) | (1,0) | 2 | 1,1,1 |
| (0,1) | (0,1) | 1 | 2,2,0 |

Each row follows by substituting into the displayed five vectors. This table is an exhaustive algebraic parity split, not a census of rooms or endpoint orbits.

## Consequence for the ENTIRE affine group

A global affine F fixes the unique cone and induces a linear unimodular map on the intrinsic period torus with this origin. It permutes the five regular corner marks and therefore preserves w exactly. Modulo 2 its matrix acts in GL(2,F2), which permutes the three nonzero classes.

- If w(0)=0, the unique nonzero class of weight 3 is fixed. The allowed mod-2 image is contained in its two-element stabilizer.
- If w(0)=1, the unique EMPTY nonzero class is fixed. Again the allowed image is contained in a two-element stabilizer.
- If w(0)=2, all three nonzero weights are equal. This weight invariant imposes NO restriction on the mod-2 matrix beyond membership in GL(2,F2).

These are necessary upper bounds, not claims that every allowed matrix is realized by a genuine affine map. No pointwise corner fixation, arbitrary translation adjustment, Z restriction or normalization of the physical sign group is assumed.

For a proposed ordered-pair construction the actual four original target classes are

[(epsilon_x t-a, epsilon_y u-B)] modulo Lambda,
(epsilon_x,epsilon_y) in {+1,-1}^2.

The SAME realized torus matrix acts on the source class and these four classes. This remains F(Gq), not G F(q). The corner-profile condition constrains that matrix only as above; it cannot supply a missing lift, sheet or affine realization.

## Calibration and limitation

For A=H=8, a=B=4, both parity pairs are (1,1). The weight-3 class is the relative diagonal class. Its preservation is consistent with the accepted exact-q obstruction. The previously accepted H2/Rx seed still survives; this table is not a new all-four obstruction on that room.

For the assigned normalized odd-d family A=H=2d+1, a=B=d, gcds are 1 and both parity pairs are (1,0). Thus w(0)=2 and every nonzero class has weight 1, for BOTH d=1 and d=3 modulo4. The old heavy-class argument is unavailable on the entire residual family, including all original target lifts. This does not prove full affine freedom inside the cone fiber: its non-Weierstrass points can still have additional invariants that the torus weights do not see.

The current positive diagonal proof and conditional all-word subgroup residual therefore cannot be joined into a universal result using only the accepted L8 corner-parity mechanism. A genuinely stronger full-group endpoint action or invariant remains necessary. General native L affine-seed coverage, ten-wall illumination and the broad r<=8 goal remain OPEN.
