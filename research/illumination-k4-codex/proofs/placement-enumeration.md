# L5–L6: finite placement reduction and enumeration correctness

[done] Written proofs, 2026-10-31. Scope: finite unions of canonical right-isosceles triangles, slit-free strictly simple boundary, two distinct interior A marks, at most k transparent B/C vertices. Counts refer to a fixed unit-grid presentation. These lemmas do not bound k or establish global minimality.

## Definitions and hypotheses

A points have even-even coordinates, B points odd-odd coordinates, and C points mixed parity. Each unit square has its A–B diagonal. Each triangle has one vertex of each type. The triangles at an A or B point form eight 45-degree sectors; at C they form four 90-degree sectors. An A cell is the eight-triangle square centered at its A point, not a unit square of the original tiling.

For a room let N be its number of triangles, W its number of maximal straight walls, I the number of interior A points, J the number of interior B/C points, s_A the number of smooth boundary A points and s_N the number of smooth boundary B/C points. Put k=J+s_N. Define Q as three per smooth boundary A point plus the number of incident triangles at each genuine boundary A corner.

An interior lattice point contains its full incident star because the room is open in a neighborhood of that point. Thus both marks force eight triangles, establishing L2 for this class. Distinct A points have disjoint triangle stars: each triangle has exactly one A vertex. The triangle dual graph has one node per triangle and an edge for a shared full triangle edge.

## Counting and the finite window

A strictly simple room is a triangulated disk. If B is its number of atomic boundary vertices, Euler and triangle-edge incidence give

    N = 2(I+J)+B-2,
    B = W+s_A+s_N.

Counting incidences at A vertices gives

    N = 8I+4s_A+sum_corner_A m = 8I+Q+s_A.

Eliminating N yields

    W = 2+6I+Q-2J-s_N,
    3s_A <= Q,
    N <= (4/3)(W-2+2J+s_N) <= (4/3)(W-2+2k).

These are presentation-specific necessary bounds. In particular W<=21,k<=4 imply N<=36; the completed peer run's cap NMAX=38 is conservative.

For completeness of its coordinate window, collapse the source star to one root of the dual graph. A connected N-triangle room has at most N-8 nodes outside that star, so every triangle is reached in at most N-8 steps. Across any canonical shared edge, the neighboring triangle centroid changes by at most 2/3 in either coordinate: vertical/horizontal edges give displacement (±2/3,0) or (0,±2/3), and diagonal edges give (±1/3,±1/3). Source-star centroids have both coordinate magnitudes at most 2/3; a triangle vertex differs from its centroid by at most 2/3 per coordinate. Every vertex therefore satisfies

    |x|, |y| <= (2(N-8)+4)/3.

At N<=38 this is 64/3<24. All eligible triangles and their occupied vertices lie strictly inside the enumerator's [-24,24] square. Rejecting occupation of an incomplete star on the window boundary loses no eligible room.

## L5: placement bound

Translate the source A mark to (0,0). Translation by an even-even vector preserves the tiling. Coordinate sign changes and interchange preserve it too, so the target can be written q with 0<=q_y<=q_x and even coordinates. The source and target stars each contain eight triangles and are disjoint.

Let d be the minimum number of edges in the infinite dual graph between any source-star triangle and any target-star triangle. In a connected room choose a shortest dual path between these two sets. Apart from its endpoints it meets neither star; otherwise trimming produces a shorter path. If it has d_R edges, its d_R-1 intermediate triangles are distinct and outside the two forced stars. Hence

    N >= 16+(d_R-1) >= 15+d,
    d <= N-15.

Equivalently, the count of intermediate connector triangles is at most N-16. This distinction removes the earlier off-by-one wording ambiguity. The bound is necessary, not sufficient for constructing a room.

An infinite-tiling breadth-first expansion from all eight source-star triangles to dual depth NMAX-15 lists every possible target star. At NMAX=38 this gives exactly the following 20 normalized targets:

    (2,0), (2,2),
    (4,0), (4,2), (4,4),
    (6,0), (6,2), (6,4), (6,6),
    (8,0), (8,2), (8,4), (8,6), (8,8),
    (10,0), (10,2), (10,4), (10,6),
    (12,0), (12,2).

The independent reconstruction in `../persisted-replay/scope-check.py` uses exact reflections to generate neighbors without an assumed finite tiling window. The placement (2,0) is directly illuminated: its two forced stars contain the whole open connecting segment.

## L6(a): local fan table

At a vertex of a polygonal disk, a small intersection with the room is one connected angular sector, or the full neighborhood at an interior point. Multiple disjoint occupied angular intervals would be a boundary contact and violate strict simplicity. Consequently a nonempty occupied fan is either a cyclic contiguous proper run or the full ring.

For A and B, m incident triangles give angle m*pi/4. Their nonempty proper runs have m=1,...,7; m=4 is smooth. All the other values are corners, including the concave values 5,6,7. The full ring has m=8. For C the corresponding angle is m*pi/2, with proper runs m=1,2,3, smooth m=2, and full m=4.

A full A ring contributes one to I. A smooth or full B/C ring contributes one exception. Any proper nonsmooth ring contributes exactly one maximal-wall endpoint, hence one to W. Empty rings contribute nothing. In a simple closed polygon, maximal walls and genuine corner vertices have the same count.

These facts give precisely the table in the frozen enumerator. Its `patterns` function omits the empty mask. This is safe specifically because it queries that table only for active vertices already meeting at least one selected triangle. An unused vertex is not active. An arbitrary unoccupied vertex would need the empty option.

## L6(b): branching exhausts eligible rooms

A state assigns tiles 0, 1 or unknown and records at every vertex the known-mask and selected-mask. The active set consists exactly of occupied vertices whose rings are not completely assigned. The root forces the two marked stars selected.

Fix any eligible room R satisfying this root. Inductively take a state whose assignments agree with R. If an active vertex is chosen, R supplies a legal local fan compatible with all known bits. The branch loop includes that option and assigns every still-unknown tile in its ring accordingly. Thus at least one child continues to agree with R.

Each branch assigns at least one previously unknown tile, so depth is finite in the finite window. If active becomes empty while R still has an unselected triangle, edge connectivity of R supplies an edge from a selected triangle to an unselected triangle. Either endpoint of that edge then has a selected incident tile and an unknown incident tile, contradicting the empty active set. Therefore the selected triangles equal R at such a leaf.

The two seeded stars may start disconnected. This proof does not assume otherwise. Additional disconnected components can also be explored, but the terminal connectivity test rejects them. Conversely no connected eligible completion is lost by leaving completely untouched distant triangles empty at a leaf.

## L6(c): pruning conditions

Selected triangle count cannot decrease within a branch. A resolved fan has all incident tiles assigned; its corner, exception and full-A contributions cannot change before backtracking. Consequently upper bounds on selected N, completed k and completed I are necessary conditions.

Let c be the completed corner count, e the completed exception count and b the number of unresolved occupied B/C vertices. Each such B/C fan must eventually be either a corner or an exception. At most k-e can become exceptions, so every completion satisfies

    W >= c+max(0,b-(k-e)).

Ignoring unresolved A corners only weakens this lower bound. Rejecting a branch whose right-hand side exceeds WMAX is safe. A vertex with no compatible legal fan also cannot have an eligible completion.

A satisfied lighting certificate is safe pruning when its required-used tiles U are selected, required-absent tiles Z are absent, and the marks' stars are forced. The universal-completion proof and exact saved-witness replay are in `../persisted-replay/findings.md`. No direction bound is part of this implication.

## L6(d): bookkeeping invariant

For each vertex, `known` records the assigned incident bits, `value` records its selected bits and `nused` is their selected population. A vertex enters active on its first selected tile and leaves active once its full ring is assigned. Completed fan contributions then enter the global totals exactly once.

For each certificate, `rem` is the number of its requirements not currently satisfied, counting unknown as unsatisfied. `sat` is the number of certificates with rem=0. Assigning a tile decrements exactly the counters watching that tile/value; undo increments those same counters. A certificate learned late starts from the current number of unsatisfied requirements; it remains present when backtracking. This invariant holds independently of when it was learned.

A trail reverses tile, bit, active-set and completed-fan changes in reverse order. The precise implementation is supported by 15,000 independently reconstructed state transitions, including locally rejected assignments and late learning, in `../persisted-replay/mechanics.py`. This is implementation evidence in addition to the invariant argument; it is not a formal verification of the Python runtime.

## L6(e): terminal simplicity test

The local-fan condition makes the geometric union a compact planar two-manifold with boundary: one sector at boundary vertices, full neighborhoods at interior vertices, and no pinches. The edge-connectivity test gives connected interior and a connected manifold. A compact connected planar surface has genus zero. If it has b boundary components, its Euler characteristic is 2-b. Thus the terminal check

    vertices - edges + triangles = 1

forces b=1. Its single polygonal boundary is a simple closed curve. Conversely every strictly simple room has edge-connected interior, the local-fan condition and Euler characteristic 1, so it passes. Euler characteristic alone would not suffice if disconnected pieces or boundary contacts were permitted.

## Claim boundary

These arguments establish the mathematical branching, local tables, safe pruning, finite placement coverage and terminal topology for the specified model. They do not supply a complete execution trace of the historical runs. The saved 19 completion logs and all 47,576 certified guards have been audited; the complete historical enumeration has not been independently rerun or converted to a checkable exhaustive proof. The fixed-k bounds do not cover k>=5.

Next move: independent peer review of these lemmas, followed by a proof-producing exclusion encoding only after the target scope is settled.
