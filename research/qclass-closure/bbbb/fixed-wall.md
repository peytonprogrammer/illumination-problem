# Five single-corner obstructions in the fixed 22-wall room

Keep all original walls and the original marks S=(0,0), T=(2,2). A certificate here is two ordinary billiard legs ending for the first time at the same polygon vertex z, one from each mark. Their terminal velocities must point in opposite physical directions. Join the first leg to the reverse of the second at z without reflection. Where the local half-plane swept between these opposite rays lies inside the 270-degree sector, this is a specified straight continuation in the original room chart. It is a diagnostic broken path: it violates exactly the rule forbidding a vertex hit. No boundary edit is involved.

## The bottom reflex corner

With initial velocity (3,−2), the S leg reflects at (1,−2/3) and (0,−4/3), then arrives at z=(1,−2) at time 1 moving (3,−2). Starting backward from T at velocity (−3,−2), the successive reflections are (−1,0), (2,−2), (1,−8/3), (3/2,−3), (2,−8/3). It reaches z at time 3 moving (−3,2). All seven reflections are on open walls. Reversing the T leg makes the velocities match. At z the continuation goes northwest to southeast through the northeast-side half-plane in the room. The ray now **reflects** at the original vertical wall at (1,−8/3); it does not need the square added in the earlier comparison.

## Other certified corners

The following integer displacements specify two unit-time traces, independently terminated at their first forbidden vertex. The last columns give velocities on arrival, allowing different positive speeds on the legs.

| z | Launch from S | Launch from T | Arrival from S | Arrival from T |
| --- | --- | --- | --- | --- |
| (1,−2) | (3,−2) | (−9,−6) | (3,−2) | (−9,6) |
| (1,2) | (3,2) | (3,2) | (3,2) | (−3,−2) |
| (1,1) | (1,1) | (−1,−1) | (1,1) | (−1,−1) |

These were replayed with D8's Fraction tracer.advance on the unchanged R22-base cells. In each call the tracer's first illegal point was the stated z. Each joins two opposite interior directions at a reflex vertex, so at least one of the two straight half-planes is in the room sector. The isometry (x,y) ↦ (2−y,2−x) exchanges S and T. It sends the lower-left cell (i,j) to (1−j,1−i); applying it to the 15-cell list gives exactly the same set. It therefore supplies certificates at (4,1) and (0,1) as well and fixes (1,1).

Thus five distinct reflex corners each block a different path whose other collisions are all legal. The four reflex corners without a certificate in this argument are (0,−1), (1,−1), (3,1) and (3,2). Nothing here asserts that any of these four lacks such a path. Even nine certificates in this fixed room would still require a separate argument to yield a nine-corner lower bound in every room.

[Exact tracer](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d8-perturbation-test/tracer.py) · [Earlier one-square edit](bottom-step.md)
