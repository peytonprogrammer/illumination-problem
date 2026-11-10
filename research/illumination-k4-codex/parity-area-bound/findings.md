# Finite tile cap for canonical parity-room enumeration

Status: proof and fixed-room controls completed by Codex; independent Opus
review requested. This is an enumeration completeness bound for a restricted
class, not a global lower bound.

## Exact identity

Let P be a strictly simple polygon made from N canonical unit right-isosceles
triangles. Let W count maximal straight walls. Define

- A: even-even lattice points;
- B: odd-odd lattice points;
- C: the two mixed-parity classes.

Use the canonical diagonal through A and B in each unit square. Every tile
has one A angle pi/4, one B angle pi/4, and one C angle pi/2. Assume P is a
parity room: every occupied non-A lattice point is a genuine polygon corner.
Let E_A be the sum of the angles at genuine A corners, in units of pi/4.
Smooth boundary A points and interior A points do not contribute to E_A.

**Theorem.**

    4(W-2) = 3N + E_A.

In particular,

    N <= floor((4W-8)/3).

**Proof.** Summing each triangle's B and C angles gives 3N*pi/4. At an
occupied B or C point, the incident tile angles sum to its polygon corner
angle, because that point is a genuine corner by hypothesis. Thus this
quantity is exactly the sum of all non-A polygon corner angles. Add the
remaining A-corner angles E_A*pi/4. A strictly simple polygon with W corners
has total interior angle (W-2)*pi, proving the identity. E_A>=0 gives the cap.

This is the mixed canonical-triangle version of the angle/incidence ledger
already used for orthogonal parity bases in research-note.tex. With S unit
squares, N=2S, it gives 3S<=2W-4, equivalently the earlier 3S<=4r+4.

## Caps relevant to Opus's enumeration

| Maximum walls W | Maximum canonical triangles N | Maximum area in unit squares |
| ---: | ---: | ---: |
| 21 | 25 | 25/2 |
| 26 | 32 | 16 |

The first cap makes the proposed search below 22 walls finite in tile count.
The second covers the proposed parity-room isolation catalogue up to 26
walls. These are safe caps, not claims that the maximum tile counts occur.

## A finite rooted universe

Suppose there is an interior A mark. Translate it to the origin by an even
integer translation. All eight canonical tiles incident to it must be present;
their union is the square [-1,1]^2. They form a connected eight-vertex set in
the tile adjacency graph, where adjacency means sharing a full unit edge.

The entire occupied tile graph is connected. Otherwise components meet at
most along isolated vertices, so the polygon interior would be disconnected,
contrary to strict simplicity.

For any occupied tile, choose a shortest occupied graph path from the root
star to that tile. After its first star tile, the path contains only tiles
outside the star, with no repetition. There are N-8 such tiles in total.
Consequently every occupied tile lies at dual-graph distance at most N-8
from the root star, in both the occupied graph and the full canonical tiling.

Each root tile's vertices have coordinate absolute value at most one.
Moving across a shared tile edge introduces vertices differing by at most
one in either coordinate from a shared vertex. Induction along the path
gives an optional coordinate bound

    |x|, |y| <= N-7

for every occupied lattice vertex relative to the root mark. Hence:

| Wall cap | Root-star dual radius | Safe vertex-coordinate box |
| ---: | ---: | --- |
| 21 | 17 | [-18,18]^2 |
| 26 | 24 | [-25,25]^2 |

A complete recursion over edge-connected tile subsets containing that fixed
star and with N up to the cap therefore needs no arbitrary search window.
The rooted graph ball is a derived universe. The area theorem alone does
not certify a particular enumerator's recursion, duplicate removal, mark
selection or pruning rules.

Two distinct interior A marks have disjoint eight-tile stars, since a
canonical triangle has exactly one A vertex. Thus N>=16 is an additional
necessary condition for the requested two-mark search. It is not sufficient
for a geometrically valid parity room.

## Exact extension with transparent non-A points

For a strictly simple canonical room that is not a parity room, let S_BC
count smooth non-A boundary lattice points and I_BC count interior non-A
lattice points. The same angle ledger gives

    4(W-2) = 3N + E_A - 4S_BC - 8I_BC.

Each smooth point contributes pi and each interior point 2pi to the tile
angle sum, although neither belongs to the maximal polygon corner sum.
Subtracting those contributions proves the formula.

This explains precisely why the cap is restricted. Our known simple22 room
has N=30, E_A=6, S_BC=4 and I_BC=0:

    4(22-2) = 3*30 + 6 - 4*4 = 80.

It exceeds the parity-only cap26 without violating the corrected identity.
It must not be excluded by the new cap. Bounding the transparent points,
or proving a darkness-preserving reduction that removes them, remains a
separate part of the general problem.

The restriction also explains scaling. Parity is a condition on the chosen
unit lattice; integer enlargement on that fixed lattice can introduce many
non-A smooth or interior lattice points and leave the parity class. The cap
is not an area bound for all dark rooms of a fixed wall count.

## Fixed controls

check.py verifies the exact canonical tile types, B/C angle sums, boundary
corner angles, corrected identities, root-star distances and coordinate
bounds on the frozen rooms:

| Room | W | N | E_A | S_BC | I_BC |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mixed simple room | 24 | 27 | 7 | 0 | 0 |
| Historical orthogonal reconstruction | 34 | 38 | 14 | 0 | 0 |
| Jain reconstruction | 28 | 32 | 8 | 0 | 0 |
| Wolecki contact control | 22 | 24 | 8 | 0 | 0 |
| Known simple22, negative parity control | 22 | 30 | 6 | 4 | 0 |

Wolecki's repeated-vertex room numerically satisfies this ledger, but is
outside the strictly simple theorem's stated scope; it is not used to infer
a general contact-room bound.

The stored Jain mesh uses eight noncanonical internal square diagonals.
The checker replaces only those internal diagonals in full unit squares
with the canonical A-B diagonal, without changing the occupied room, area,
wall geometry or tile count. It verifies that each replaced pair really
covers a full square. A lone triangle with a noncanonical boundary diagonal
would fail the hypotheses rather than be silently repaired.

No new rooms, directions or optical paths are enumerated by the checks.

## Reproduce

    python3 -B .context/illumination-k4-codex/parity-area-bound/check.py

Frozen input hashes are in check.json; sources are the existing independent
snapshots in isolation-review/inputs/. The file manifest locks the report,
checker and receipt. Independent review and the enumeration itself remain
separate.
