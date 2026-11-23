# An all-direction obstruction to the two whole-room cylinder tests

Already at four reflex corners there are normalized BBBB rooms in which neither whole-room cylinder hypothesis holds in any primitive direction. The obstruction can be checked from the polygon vertices alone. A specified nondirect pair in the example nevertheless has a legal off-class midpoint. The stronger question about an invariant cylinder containing lifts of a specified pair remains open.

## A necessary corner count

For each of the four parity classes e of physical vertices put μ(e) = number of convex vertices minus number of reflex vertices in that class. The sum is 4 by the turning-angle formula. In primitive direction v=(p,q), write L(x,y)=qx−py modulo 2. Its two levels each consist of two parity classes. All four unfolded sheets give the same L at lifts of a physical lattice point, since the mirrors have integer coordinates.

**Lemma.** Assume separate axis wall-length gcds one and at least one reflex vertex. If M has one geometric cylinder in v, or exactly two geometric cylinders interchanged by τ, then on *each* level of L the sum of μ is 2.

* In the one-cylinder case the integral transverse height is 2. Its two convex fixed points in the open cylinder lie at height 1, and all other corners are on the rims at heights 0 and 2. Relative transverse height agrees with L up to an additive constant. Hence one level has exactly two convex vertices and zero reflex vertices. Subtraction from 4 gives the other sum. [Height and fixed-point proofs](convex-cylinder.md)
* In the exchanged case the quotient cylinder has height 1. The two rim trees are on opposite levels and together contain all corners. A tree with t trivalent vertices has t+2 leaves. Those vertices and leaves are exactly the reflex and convex corners on that level. [Rim-tree and normalization proofs](adjacent-cylinders.md)

Thus if no two of the four parity-class counts sum to 2, both hypotheses fail in **every** primitive direction. Only the three nonzero linear forms over the two-element field occur. This argument precedes any test of the actual interval lengths. Passing the count alone gives no decomposition theorem.

## A twelve-wall example at unbounded area

For odd integers b ≥ 7 take the union of the horizontal rectangle [−b,b] × [−2,2] and its transpose. The cross is strictly simple. It has four reflex vertices (±2,±2) and eight convex vertices (±b,±2), (±2,±b). Each axis has maximal wall lengths 4 and b−2, of gcd one. All four parities occur in the central square's interior. Its area is 16b−16, including 128 at b=9, so the obstruction persists in the n ≥ 120 range.

In the order (00,10,01,11) its counts are (−4,4,4,0). Every level sum is divisible by four. In particular no primitive direction supplies either of the two whole-room charts. Periodicity of a rational direction gives no remedy for this obstruction.

Take S=(6,0) and T=(0,6). The midpoint (3,3) of their direct segment is outside the room. An exact legal path, the same for every b above, is

    (6,0) → (4,−2) → (−2,4) → (0,6).

The middle leg follows x+y=2, passing through the central square from (2,0) to (0,2). The first reflection changes the vertical velocity sign at the bottom of the horizontal arm. The second changes the horizontal sign at the left wall of the vertical arm. Both contacts are strictly inside their walls. The three legs take 2, 6 and 2 units of time at unit coordinate speed, giving midpoint (1,1). The all-b illumination conclusion here concerns this specified pair only. D87 separately certified all same-parity interior lattice pairs at b=7,9,11. [D87 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d87-review-cross-corners/review.md)

This is an off-class witness for the same marked pair for which both whole-room tests lack a chart in all directions.

## What remains of the pair-specific question

The local theorem in convex-cylinder.md only asks that both marks have lifts in the closure of *one preserved cylinder*, allowing other cylinders elsewhere. The parity count does not exclude this. Nor does it exclude paths between adjacent cylinders. The reviewed adjacent-cylinder winding equations apply at any individual regular seam without requiring a single quotient cylinder. In a decomposition with more cylinders, the bound of 2r+2 tree edges for the two whole-room rims no longer gives a bound on a given pair's uncovered differences across directions.

There is a useful distinction about the **along-leaf check** also used in convex-cylinder.md. With all directions allowed and regular portions of rim leaves included, that check is logically complete for lattice marks. Indeed, unfold any legal shot. Its displacement between developed integral endpoints is a nonzero integer multiple of a primitive integral direction. In that direction the open segment either lies on a regular cylinder leaf or lies in a single saddle connection between reflex lifts. In the latter case it cannot pass a reflex lift, so it stays on one open rim edge when the edge is cut only at reflex lifts. In either case the exact arc avoids convex lifts as well. Conversely such an arc folds to a legal shot. The same equivalence holds with midpoint parity checked on the arc itself. This observation uses a direction obtained from an existing shot and gives no way to produce that shot. Requiring the cylinder to be preserved by τ is a different test. There is no proof here that it succeeds or fails in every direction for this pair.

## The R22 control

In (4,7) the level is physical x parity and in (7,4) it is y parity. In each split the nine reflex vertices divide 3 and 6, by their coordinates. The corresponding trees have 7 and 13 edges. Both splits satisfy the necessary count above. For each direction d84 found 15 and 33 uncovered half-unit differences on the two circumference-30 rims. These are sampled differences, not counts of dark pairs. Their values depend on the lengths and locations of the paired edge occurrences. [Independent rim check](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d84-review-cylinders/review.md)

The ninth reflex raises the total edge count from 18 at r=8 to 20. Its concrete blocking role in this particular room is stronger than that count: each of the nine corners is the sole forbidden contact of a different certified route between the dark marks. For example, (1,1) alone intercepts the direct diagonal. Any eight of the nine leave one of those relaxed routes unintercepted in the fixed geometry. Changing a corner changes the geometry, so this argument gives no lower bound for other rooms. [Nine single-corner certificates](corner-support.md)

**Verdict.** A universal proof based on finding either whole-room chart is ruled out by the four-reflex cross family. The remaining geometric question is existence of a pair-specific certificate in multi-cylinder decompositions. For the version allowing any legal leaf arc, that existence question is equivalent to illumination itself. No direction sweep was used.
