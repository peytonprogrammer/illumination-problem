# Spider's home: exact darkness of the idealized grid reconstruction

Status: finite hypotheses checked; written proof independently accepted by Opus (2026-11-01).

## Provenance and scope

Jain's own [project index](https://b1805.github.io/Exploring-Illuminability-Polygonal-Rooms-and-Light-Dynamics/)
links [The Spiders Unilluminable home](https://www.youtube.com/watch?v=ahm4knwln7I)
on George Tokarsky's channel. The description credits Bhavya Jain and states
that the center and four long-wall midpoints are unilluminable. The thumbnail
is the source of the reconstruction. The code checks all 36 cell centers
against that thumbnail. The resulting idealized grid polygon has 16 unit
squares and 28 maximal walls. This is not an original coordinate/settings file.
Equal grid spacing is an explicit reconstruction assumption, consistent with
the author's square ABCD description and the image.

## Convention

A path has positive length, finitely many specular reflections, and cannot
pass through a polygon vertex. Its final point may lie inside a smooth wall.
Thus a ray reaching a marked wall point counts as illumination, whether or
not it subsequently reflects. Tangential travel along a wall cannot bypass
the vertex obstruction. This is a boundary-mark extension of the usual
interior-pair question, not an example of two interior dark marks.

## Proof

Translate the grid so the source is s=(0,0). Call even-even lattice points A.
The four targets are (-2,0), (2,0), (0,2), (0,-2). The finite geometry check
establishes that every lattice point of the closed room outside class A is
a genuine polygon vertex (one or three incident squares).

Suppose a valid finite path joins s to any target, or returns to s. Unfold
its successive reflections. All walls lie on integer horizontal or vertical
lines; reflecting in any such wall preserves both coordinate parities.
The developed target therefore has coordinates q=(2a,2b). The developed
path is a straight segment with positive length, hence q is nonzero.

Let g=gcd(|a|,|b|), and put (u,v)=(a/g,b/g). The point (u,v) lies strictly
between 0 and q, at parameter 1/(2g). At least one of u,v is odd, since
(u,v) is primitive. It is therefore a non-A lattice point. Fold this point
back through the same reflection copies. Grid parity is preserved, so its
physical preimage is a non-A lattice point in the closed room, hence a
polygon vertex. This contradicts validity of the path.

This proof treats arbitrary finite words and all directions without tracing
or sampling rays. The same argument obstructs every positive-length return
to the source. It does not imply darkness is preserved under arbitrary wall
or mark deformations.

## Reproduce

`uv run --with pillow python -B .context/illumination-k4-codex/jain28/reconstruct.py`

`python3 -B .context/illumination-k4-codex/jain28/darkness-check.py`

The first command writes the reconstructed input and geometry receipt. The
second verifies all non-A vertices, the four target-wall incidences, and
parity preservation by every wall reflection. The written argument supplies
the unbounded-word conclusion; a finite numerical test is not its substitute.

## Boundary-event extension used next

At a smooth boundary target, a limiting final segment must reach that target
transversely. A one-corner event is stopped at the target before its final
wall reflection, including equality of target time and limiting wall time.
The final wall is not appended to the reflection word. Earlier contacts and
the unique intervening reflex corner keep their usual event conditions.

Let d be the oriented tangent of the target wall and n its inward normal.
Admissible nearby targets obey h=n·(t-v_wall)>=0. Both t and v_wall move;
using t alone would give the wrong tangent cone. At the base h=0. Under
h>=0, transverse final approach and all other strict finite-word conditions
persist whenever the one-corner determinant has the lighting sign. A
sufficient isolation certificate therefore uses event rows g_i together
with the row dh, all with the >=0 convention. An exact strictly positive
dependence and full rank modulo affine symmetries exclude every non-affine
closed-cone displacement by the same compact-sphere quadratic argument as
for interior marks. If the target is constrained to stay on its wall, h=0
instead. This room's marks are wall-interior points, so exactly one active
normal constraint is required per chosen target; no convex-corner pair of
constraints applies here.
