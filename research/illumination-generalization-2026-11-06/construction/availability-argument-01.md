# AV01: minimum-length selection excludes the desired narrow joint

This hand argument refutes the W-free shortest-chain selection proposed in availability-candidate-01.md. It does not refute arbitrary compatible-joint availability, nor the r<=8 theorem. Independent review is pending.

## Metric and physical fibers

Let M be the compact four-copy translation unfolding of a finite strictly simple orthogonal disk P. Give M its intrinsic flat cone length metric; its genuine reflex cones have total angle 6pi. The finite complete physical fibers X and Y lie in its regular part. A shortest path between X and Y exists: the compact length space M is geodesic, and the minimum of the finitely many endpoint distances is attained. No restriction on lattice area, travel times, directions or reflection counts is involved.

Every subarc of such a path minimizes length between its own endpoints. A minimizer cannot revisit a point, because deletion of a positive-length loop shortens it. Thus it encounters any given surface cone at most once. In this four-copy unfolding each physical reflex corner has one genuine cone; this observation bounds that particular minimizing chain, but does not transfer to arbitrary optical trajectories or imply illumination.

## Local shortcut obstruction, retaining actual prongs

Suppose a minimizer meets cone z. Consider its two outward germs from z, retaining their actual prongs on the 6pi star. These divide the star into angles theta and 6pi-theta. If one is strictly less than pi, choose a positive epsilon small enough that both adjacent length-epsilon arc pieces lie in a cone neighborhood containing no other cone or endpoint. The sector of that smaller angle is a literal Euclidean sector of angle theta<pi. Its straight chord lies inside it and has length

    2 epsilon sin(theta/2) < 2 epsilon.

Replace the two radial pieces by that chord. Both cut points are the SAME actual surface points; the prefix and suffix, including original endpoint lifts, are unchanged. This shortens the path and contradicts its minimality. Therefore BOTH angles are at least pi. This uses a local metric shortcut only; it never straightens a global loop or changes physical endpoint fibers.

At angle exactly pi the chord has equal length and passes through z, so it does not remove the genuine cone. Equality cannot be promoted to a cone-avoiding optical path. A nondegenerate developed triangle at a corner has a strictly smaller-than-pi interior angle. Consequently no cone joint on ANY shortest complete-X/Y metric path supplies that triangle's required narrow sector.

If the minimizer has multiple genuine cones, it also fails the original-endpoint arm premise: its first source arm and last reverse-target arm terminate at different cones. Minimization alone neither removes intervening cones nor creates a common original-endpoint joint.

## Actual dark calibration: Q0, not a low-reflex counterexample

Use Q0 and the accepted all-word physical darkness proof in review/fold-area-invariant.md section 3. Its actual marks are S=(0,0), T=(2,2), with r=9. The closed Euclidean segment S--T lies in P and meets its sole boundary point C=(1,1). For 0<t<1, (t,t) is inside the square (0,1)x(0,1). For 1<t<2, (t,t) is inside (1,2)x(1,2). Both squares lie in Q0 as read from its listed boundary (also from its three-copy staircase assembly).

At C the missing physical quadrant is southeast. The two outward diagonal germs towards S and T bound the northwest-containing sector of angle pi. The lift through this sector is a length-2sqrt(2) metric path on M between some x in X and y in Y, hitting one genuine cone. The exact endpoint lift y is defined by this lift, not substituted by its torus image.

The quotient M->P does not increase curve length: it is locally a reflection folding of Euclidean sectors and preserves lengths on the individual pieces. Every curve from X to Y therefore has length at least the physical Euclidean distance |S-T|=2sqrt(2). The lifted segment attains it, so it is a global complete-fiber minimizer. Yet its middle cone has angle pi, not a narrow sector, and remains forbidden optically. The inherited all-word proof says the physical pair really is dark.

All minimizers fail the desired narrow sector by the general shortcut argument, regardless of other choices at C. This is an actual darkness calibration of the W-free AV01 failure. Since Q0 has nine reflex corners, it is NOT a counterexample to a premise restricted to r<=8 and NOT a qualifying dark counterexample to the native objective.

For Q100=diag(100,1)Q0, the same physical segment and cone C=(100,1) give length sqrt(200^2+2^2), again equal to the physical Euclidean distance. The complementary northwest sector remains pi; no unit-lattice/Farey or weight normalization is inferred from stretching.

## What this settles and what remains

AV01 is false as a darkness-to-narrow-joint selection procedure: length minimization selects precisely paths with no strictly narrow cone angle. The issue is not failure to find a minimum, a numerical cutoff, corner multiplicity, or an arbitrary endpoint-sheet substitution.

A minimum over ALREADY compatible original-endpoint joints could exist under a suitable positive integral objective, but it presupposes the nonempty set whose existence is the central question. It cannot supply that existence. No claim about other extremal orders is disproved here.

The next route must select a non-minimizing configuration by an independently justified global construction, or exploit r<=8 in a different optical implication. Existing local DI02/index-two/axis lemmas cannot be applied to this metric minimizer. No new global positive availability result or corner lower bound follows.

No discovery search, new clock, worker, engine, census or git mutation was used.
