# Certifying 20-wall lattice rooms with a corner-only parity class

The grid is specified in advance. A qualifying room is a strictly simple orthogonal lattice polygon in which one of the four parity classes has no grid point in the interior or in the relative interior of a wall. Zero or one interior lattice point is allowed. A legal billiard path can reflect at a smooth wall point and cannot pass through a polygon corner.

## The census

Exactly 20 maximal walls means eight reflex and twelve convex corners. Each unit square is incident to exactly one grid point of the chosen class. An incident corner contributes either one or three squares. Thus area is at most 36. The existing block enumerator runs in all four grid alignments with its endpoint-count filter removed. At exactly 20 walls it gives 913,622 distinct shapes up to square symmetries and translation. Independently, a cell-at-a-time enumerator checks completed vertex stars, Euler characteristic and exactly eight reflex vertices. After expanding the first census to oriented shapes, the counts agree for every area and alignment, including the zero bins.

## Whole rooms and pairs of tiles

We use the preceding [cylinder lemma](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d13-cylinder-cover/theory.md). A lift in the open cylinder joins a lift in its closure by a segment in the unrolled strip. Folding back gives a physical billiard path. The room-level computation covers open faces, shared edges and individual interior grid vertices. It accepts a whole room when no positive-dimensional source region and no nonlattice pair remains. The previous lattice census supplies a replayed path for each distinct interior lattice pair.

The successive direction bounds are 5, 9, 14 and 18. The last two stages also use the symmetry of the nonillumination relation. Any resource limit leaves the room to be checked by the next stage. The remaining rooms are tested on every unordered pair of unit tiles, including equal tiles. For each surviving source polygon and each target polygon paired with it, we take the smallest enclosing coordinate radius about a vertex of its own tile. We check every polygon vertex using integer arithmetic and round radii upwards to multiples of 1/65536. Taking the maximum over all products with the same chosen centers gives a safe enclosure. The center itself may be a regular grid point. If both displacements vanish, the earlier lattice path census deals with any distinct interior pair.

## Two displacement ranges

The [18-wall shear proof](../two18/README.md) defines a simultaneous affine shear on the marked unfolding and tracks both lifts separately. Let L be the least common multiple of twice the horizontal component widths. Transposing the room gives the analogous vertical shear. Let A denote the largest absolute coordinate deviation from the two designated centers, and choose the axis on which it is transverse.

For **0 < A ≤ 1/(8L)**, choose K = ceil(1/(8LA)). The phase KLA lies in [1/8,1/4]. The other endpoint's phase lies between zero and the larger phase. We check an enclosing box for the four ordinary coordinates and these two phases. Integer rounding enlarges the box at the threshold.

For **A ≥ 1/(8L)**, use K=1. The transverse phase at each endpoint now equals its actual signed transverse displacement times L. Keeping that equality in the strip formula lets us certify parameter ranges for which treating the phases as independent would be too weak. The bounds overlap at the threshold.

Each illuminated leaf provides a power j and a small direction (p,q). Both endpoints undergo the same affine map. An open-cylinder lift at one end and a lift in the closure at the other end give a legal path after pulling back. Integer transverse strip levels are checked separately. All bisections include their interfaces.

For some boxes just one of the two axes already suffices. If either chosen tile side perpendicular to that axis is a physical wall, an interior pair cannot have zero transverse displacement at both endpoints. In this proof we take the larger of the two transverse displacements irrespective of the other coordinates. The other coordinates retain their *full* initial bounds in both ranges. This is the additional geometric test in alternate.py.

An isolated nonlattice candidate can instead be checked by an explicit unfolded target image. The exact planar replay follows grid crossings, reflects at a wall, rejects a simultaneous crossing at a physical corner, and checks the actual physical endpoint. The bounded candidate search proves illumination only when it produces a witness.

## Checks

The complete proof audit matches every successive run to the exact cell list, every terminal run to its expected unordered tile pairs, every saved shear input to an enclosing box, and every needed lattice-room record to the earlier path census. The Python shear verifier reconstructs row-folded cylinder labels with exact rational arithmetic and replays each bisection. The known 22-wall control retains its dark lattice pair in translated coordinates.

## The 12-square room with fourfold rotational symmetry

From top to bottom its unit-square rows are `##.#`, `.###`, `###.`, and `#.##`. This is the 20-wall room left open in the earlier [small-area cylinder census](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d13-cylinder-cover/README.md). The following calculation addresses the continuum of endpoints in this particular room.

For each unresolved tile pair, partition each tile into 16 by 16 bins, assigning internal grid lines consistently by floor and clamping the far side to the last bin. Enclose each possible source and target polygon by all bins in its coordinate bounding box. A dark pair has to survive in both directions. Intersecting the forward bin relation with the transpose of the reverse relation leaves 181,158 bin pairs. The verifier subsequently treats the bins as closed, so their interfaces are included.

Three certificates cover the resulting endpoint boxes.

* **A fixed cylinder direction.** Pull a small direction back through an integer shear and test its strip labels. This test includes the singular integer levels and the cylinder closures.
* **An explicit reflected path valid for a box.** Fix a reflected and translated image of the target tile. Between the tiles the segment crosses a sequence of vertical and horizontal grid lines. At the next grid vertex the sign of the orientation determinant decides which crossing comes first. The determinant is affine in each of the four endpoint coordinates separately, so its extrema on the box occur among its 16 vertices. Where both orders are possible, check both and require the intervening physical grid vertex to be regular. Every permitted traversal must end in the requested target tile and sheet. Straight travel along a grid line is conservatively excluded when it could meet a grid vertex. For a true interior endpoint on a tile seam, a crossing at time zero or one merely changes its tile representation. During replay the Python verifier propagates physical cells and orientation signs independently of the C++ search.
* **A shear about rational transverse coordinates.** For each mark choose a rational transverse height h relative to its tile, possibly different at the two ends. Take M equal to the row period L times the least common multiple of the two denominators. A shear by M fixes both rational reference heights modulo every applicable row circumference. For transverse distance A=max |y−h|>0 choose K=ceil(1/(8MA)). In the strip index the unbounded shear displacement can then be replaced by two bounded signed phases. For every possible pair of signs and choice of larger displacement the certificate checks the full enclosing phase rectangle, splitting it as needed. A claimed leaf must also establish A>0: either a reference height is outside its box or one mark at its reference would lie on a physical wall. This test permits both endpoints arbitrarily close to their respective rational lines and does not require the longitudinal coordinates to be near a grid point.

A fourth terminal condition sends four small neighborhoods to the earlier grid-corner shear test. Each has coordinate radius at most 1/64. Their 32 proof trees and 6,452 illuminated boxes are checked separately. The full bin-pair replay includes 15,106 explicit-path leaves and 10,094 rational- or integer-reference shear calls. Each of the latter contains its own checked phase partition. The stored negative control on the 22-wall example retains the known dark pair.

The sheet half-turn used to pair cylinders commutes with these shears. In a unit-height band the half-turn sends the height h to 1−h and reverses the horizontal coordinate. The two orders of application differ there by a whole shear period, a multiple of the band circumference. Thus matching labels on the quotient always yields compatible lifts for the original two physical marks.
