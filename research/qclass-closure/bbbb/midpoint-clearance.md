# What shortest-path clearance can prove about condition (ii)

**Result.** For a same-parity interior lattice pair, the strict first-corner distance test of [shortest.md](shortest.md) can succeed only for a pair that is already directly visible. This remains true if one computes the exact distance to the forbidden set on the normalized ordered-pair surface. The obstruction applies simultaneously to all midpoint classes. It does not imply darkness. At area 501 a named example has at least 228 regular candidates in each class and a legal midpoint at (233,2), yet every candidate fails both versions of the test.

## Exact obstruction

Let δ be the intrinsic distance in the *closed physical room* P, allowing corners and boundary segments for metric comparisons. Let K be the physical polygon vertices, c(U)=δ(U,K), and let ρ be the smaller planar distance from either endpoint to K. On the normalized marked pair surface use the flat metric in which the projections to the room double preserve path length locally off the vertices. In particular each projection folded to P is length-nonincreasing, also for paths through vertices.

Write M for the infimum of the distances from all marked starts to all regular coincidence candidates. Write F for the corresponding minimum distance to a point where either projection is a physical corner. Then

    M ≥ δ(S,T)/2,                    F = min(c(S),c(T)) ≥ ρ.

The first inequality follows by folding the two tracks of any route to a coincidence. One goes from S to its physical location and the other from T. Concatenating the first and the reversed second is a walk in P of length at most twice the route length. The same argument holds if the route hits forbidden points.

For the equality for F, projection gives the lower bound. Choose the endpoint attaining the smaller c and a shortest physical route from it to K. The route is straight up to its terminal corner. Indeed a metric minimizer cannot turn in the interior or in the interior of a straight wall, and any earlier corner would be closer. From a lift of the chosen mark, follow that segment on the room double. It lifts to the normalized pair surface starting over the marked pair. At the initial point both coordinates have local degree two over the base, so the first projection on each normalized branch has local degree one. At every later noncorner first coordinate the segment continues unless the second coordinate is a corner. In particular, at an intermediate regular point over a base pole with both coordinates regular, the local relation is u²=v² and each normalized branch projects isometrically. At ordinary base points continuation is unramified. An early second-coordinate corner would have physical distance less than min(c(S),c(T)), which is impossible. Completing the lifted segment therefore realizes F. The roles of the coordinates can be interchanged.

If S,T lack a legal direct segment, a shortest physical walk between them meets a polygon vertex. Otherwise local straightness in each planar disk or boundary half-disk makes the entire walk a single legal straight segment. Splitting at its first and last vertices, which may coincide, gives

    δ(S,T) ≥ c(S)+c(T),       hence       M ≥ (c(S)+c(T))/2 ≥ F ≥ ρ.

Thus even the *exact* first-forbidden distance cannot yield M<F for such a pair. For a directly visible same-parity pair, its direct midpoint is a regular lattice point, and the two halves give M=|S−T|/2 by the matching lower bound. Consequently M<F holds **exactly** for the directly visible pairs with |S−T|<2 min(c(S),c(T)). The planar version has the identical characterization with ρ in place of F. These statements concern the strict test. A particular minimizing route, or a longer straight route, can still be clean beyond F.

## What the candidate count adds

By d78–d79 a nondirect pair in the stated large-area range has d ≥ n−8. The total regular count is at least 2d−2r. Removing the capacity of the other three parities leaves at least 2d−2r−3 floor(n/2) in each parity, hence at least 28 at n=120. There is also a useful simultaneous bound. The complement of the marked union among **all off-diagonal** ordered sheet pairs has valency n−1−d ≤ 7. Applying the same diagonal budget to the complement gives

    missing regular branches + missing reflex branches = 2(n−1−d) ≤ 14.

Every physical regular lattice lift on the room double supplies exactly one off-diagonal branch in the full relation (local degree two). Thus at most 14 such lifts in the *entire room double* are missing from the marked union, counting all four parities together. Even if zero are missing, membership gives no control of the straight segment joining a specified start to that lift. In cov4181 seven members of one class are all unreachable in that class, and a single physical corner obstructs shortest routes to candidates in two classes. [Midpoint budget](midpoint-necessity.md) · [cov4181 exact routes](shortest.md) · [large-area bound](eight-sheet.md)

## An exact control inside the requested range

Use d75’s saved DB55 corridor length 451. Its two 5×5 chambers are joined along 2≤y≤3 between x=5 and x=456. The strictly simple room has area 501, four reflex corners and gcd 1 for the wall lengths on each axis (horizontal lengths include 5 and 451, vertical lengths include 2 and 5). The chamber interiors contain lattice points of every parity. The marks S=(1,1), T=(457,1) have the same parity and the direct segment misses the corridor. The per-parity bound is 2(501−8)−8−3·250=228.

The exact physical distance is √17+451+√2. A path must reach the first mouth, travel across the corridor and leave its far mouth. The corresponding three lower bounds are attained together at y=2 by walking through both lower mouth corners. Each endpoint has intrinsic corner distance √2, realized at (0,0) and (456,2) respectively. Thus every candidate has distance at least (√17+451+√2)/2 > 228 while F=√2.

Nevertheless the saved right-wall reversal slope −37/8 lights this pair. Increasing d69's original corridor length from 3 to 451 adds 448 horizontal units at this slope, an even integral vertical displacement of −2072. Both doorway phases and the mirror height therefore persist. The path has 464 units of absolute horizontal travel, so its midpoint is 232 horizontal units from S, in the corridor. The first mouth height is 5/2. Continuing 228 units to x=233 gives unfolded height −1052, which folds to the smooth wall y=2. The right mouth height is 21/8, the right-wall turn height is 1/2, and the path ends at T. This locates one reachable candidate in the marked union without choosing a new direction. Even the ratio M/F grows without bound along the same saved branch at lengths 451+80j (j≥0): the added vertical displacement is −370j, both marks retain parity, and the horizontal wall gcd remains one. [Exact replay](midpoint-clearance-check.py) · [saved reversal branch](reversal.md) · [d75 named controls](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d75-review-corridor/review.md)

## What remains for condition (ii)

The missing step is to find a clean start-to-candidate route *beyond* the first accessible corner, where a forbidden point on an unrelated route is irrelevant. The example proves that the gap in the distance comparison can be arbitrarily large even for normalized rooms with four reflex corners. The physical distance inequalities hold for arbitrary interior marks, including rational nonlattice marks. The integral midpoint count and the identification of the direct midpoint as a candidate above use same-parity lattice marks. General condition (ii) remains open already for those marks.
