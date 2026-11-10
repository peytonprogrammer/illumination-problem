# What the three-copy proof does and does not prove

2026-10-31. Theory only; no new rooms or billiard rays searched.

## Established restricted minimum

Define a parity base to be a simple polyomino with two distinct smooth boundary
lattice marks, such that every non-corner lattice point belongs to their common
residue class modulo 2. This allows additional harmless smooth and interior
lattice points; it is broader than the original exact-two-point census.

Such a base has at least ten maximal walls. Translate one mark to (0,0), and
call a lattice vertex odd if at least one coordinate is odd. Each unit square
has exactly three odd vertices. Every occupied odd vertex is an actual corner,
so it meets one square if convex, or three if reflex. Therefore, with A squares,
c convex corners and r reflex corners,

    3A = c_odd + 3r_odd <= c+3r = 4r+4.

Here c-r=4 and w=c+r=2r+4. If w<10, then r<=2 and A<=4.
This supplies a bound without assuming that the two marks are the only safe
lattice points.

The nine free polyominoes of size one through four are the square, domino,
straight and L triominoes, and straight, square, T, L, and S tetrominoes.
This is a classification, not a room search: a four-cell adjacency graph with a
cycle gives the square; a degree-three vertex gives T; otherwise it is a path,
whose unit-step turn patterns give the straight, L, and S cases. The smaller
sizes follow immediately. The square has no smooth marks. Every other shape has
non-corner lattice points in at least two parity classes. None qualifies.
The supplied small-base checker records these facts using integer arithmetic.

Our five-square staircase attains w=10. Every maximal wall in a parity base has
integer length at most two: a longer wall contains consecutive smooth lattice
points, which cannot both have the required parity. Thus a full-wall seam
contains at most one smooth lattice mark. Making preimages of both distinct
marks interior requires at least two seams.

Now allow any number m of congruent copies, with a tree of m-1 full-wall seams,
all seam endpoints distinct, exactly one straight exterior merge per endpoint,
and no other contacts or identifications. Both boundary marks become interior,
so m>=3. The room has

    W = mw - 4(m-1) = m(w-4)+4 >= 3(10-4)+4 = 22.

The three-copy construction attains this bound. Thus 22 is optimal within this
explicitly restricted tree-of-copies class, even with extra harmless lattice
points and an arbitrary number of copies. This does not establish minimality
among all parity constructions, all folded rooms, all polyominoes, or all
orthogonal polygons.

## Why the global bound remains open

For a simple orthogonal polygon, turning angle gives c-r=4. Therefore

    W = c+r = 2r+4.

A global 22-wall lower bound would require a proof that every orthogonal room
with at most eight reflex corners connects every pair of distinct interior
points. Our construction has nine reflex corners. The arithmetic identity is a
necessary reformulation; it supplies no illumination theorem by itself.

Grid complexity does not solve this problem. Dilation preserves darkness and
wall count while introducing arbitrarily many lattice subdivision points.
Primitive grid normalization also leaves unbounded side-length ratios.
Arbitrary real orthogonal side lengths need not even admit a common square
grid. A finite enumeration with fixed grid size, fixed exception count, fixed
mark positions, or a tile bound therefore cannot establish the global result
without a separate completeness theorem.

## The most useful next theoretical test

The extra-safe-points loophole is now closed for bases with fewer than ten
walls by the incidence argument above. The next target is to characterize partial-wall folds, shared seam endpoints,
or seam cycles without passable concave fibers. The tree formula cannot be
applied to those assemblies.

For a genuinely global lower bound, the missing object is an invariant that
counts unavoidable blocking obstructions in terms of reflex corners while
allowing arbitrary lengths and marked points. The working conjecture is that
the nine reflex corners in this room pay for both blocked base routes and the
seams needed to place both marks inside. There is currently no proof that
other nonillumination mechanisms pay the same cost. That conjecture must stay
separate from the restricted theorem.

## Evidence and review

- research-note.tex contains the full geometric proof and restricted theorem.
- lower-bound-check.py and lower-bound-check.json check the nine explicit
  small bases and the attaining staircase; their completeness is justified
  by the classification argument, not inferred from a bounded search.
- geometric-proof-check.py checks the supplied room, folds, seams, and fibers.
- The separate closed-orbit certificate proves darkness of the supplied
  22-wall room without a direction or reflection bound.
