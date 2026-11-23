# Every 18-wall room in the corner-only parity class is illuminated

**Computer-assisted theorem.** Let a strictly simple orthogonal polygon have exactly 18 walls and vertices on a specified square grid. Suppose some parity class contains only polygon corners among its grid points in the closed polygon. Every two distinct interior points are joined by a corner-avoiding specular billiard path. The endpoint coordinates can be arbitrary real numbers.

There are seven reflex corners. The [incidence count](../README.md) bounds the number of unit cells by 32. The [previous census](../offgrid/results/eighteen-audit.txt) included all 141,887 eligible shapes up to translation and square symmetry. That calculation, together with the earlier lattice path certificates, settled 141,885 shapes. Here we finish the remaining two. Both have 18 cells.

## Locating the possible pairs

Each remaining room had 18 unresolved unordered tile pairs. We reran the tile-pair calculation and exported every surviving product of a source polygon and a possible target polygon. For each tile pair there is a fixed pair of grid points about which the entire residual is concentrated. All 146,308 polygon products lie within coordinate distance 1/17 of the designated grid point at each end. This follows by checking every vertex of every closed polygon with integer arithmetic. Each designated grid point is on the physical boundary, so an interior endpoint always differs from its grid point.

## Choosing a shear from the endpoint positions

Unfold four reflected copies of the room to its square-tiled translation surface. A horizontal row of physical width w unfolds to a band of circumference 2w. Let L be the least common multiple of these circumferences. A horizontal shear with derivative (x,y) ↦ (x−Ly,y) fixes the two boundary lines of each unit-height band pointwise when measured modulo its circumference: use displacement −L times the height above the lower boundary. Consequently the maps glue to an affine automorphism of the marked surface and preserve all corner lifts. The same construction applies after transposing the room. The horizontal and transposed periods are (8,16) and (8,12) in the two rooms.

For a possible pair choose the largest absolute coordinate displacement from its two designated grid points. Transpose coordinates if necessary so that this displacement, A, is vertical. Then 0 < A ≤ 1/17. Put K = ceil(1/(8LA)). For the two endpoints let t_i = K L times the unsigned vertical displacement. At the endpoint attaining A, its phase t satisfies

    1/8 ≤ t ≤ max(1/4, L/17).

Indeed K=1 gives t=LA, and K≥2 implies LA<1/8 and t<1/8+LA. The other phase lies between zero and t. As A tends to zero the required shear power can grow without bound. The certificate checks one bounded set of phases for all these powers.

## Certifying a legal path

For each parameter box the certificate chooses an integer j and a small primitive direction (p,q). Apply the same shear to both lifts, with exponent jK. In a square with lower-left corner (a,b), write σ=+1 or −1 for the two sheet choices with positive horizontal orientation. In the local chart the transverse strip index is the floor of

    q(x−a) − p Y − σ q j K L (y−y₀),

where Y=y−b for σ=+1 and Y=1−y+b for σ=−1, and y₀ is the designated grid height. Dropping a whole row period does not change a label. This formula is affine in the four original coordinate displacements and the two phases. The interval calculation treats them as independent variables over enclosing boxes and uses both possible sheets at each end. It never assumes that a shear preserves the four physical lifts as a set. Each chosen lift is tracked through the shear.

The proof trees cover these boxes by successive bisection. A leaf either violates the smaller-phase inequality or exhibits one endpoint lift in an open cylinder and the other in its closure, up to the sheet half-turn. The half-turn preserves physical projection and commutes with the shear. In an unrolled cylinder a straight segment to the target stays in the open strip until its endpoint. Pulling it back through the shear gives a straight, corner-avoiding segment before projection to the physical room. Integer strip boundaries are checked separately for openness. Endpoints on interior tile edges are included.

The 36 tile pairs, two choices of axis, and two choices of larger endpoint give 144 complete proof trees, with 853 illuminated boxes. All of the first census's unresolved regions are covered.

## Verification

Run `bash replay.sh /path/to/new-directory` here. It re-exports and checks the residual polygons, regenerates the proof trees with integer arithmetic and undefined-behavior checks, and verifies both saved and regenerated certificates. The separate Python verifier follows the bisection tree, folds the infinite row back into the physical room using exact fractions, and queries the project's Python cylinder implementation. It also compares 40,608 strip and integer-leaf entries against direct positive and negative sheared directions, up to renaming cylinder labels. See [the replay log](replay.log) and [the verifier](verify.py). These checks share the underlying cylinder lemma and the earlier enumeration. This is a local research result pending outside review.
