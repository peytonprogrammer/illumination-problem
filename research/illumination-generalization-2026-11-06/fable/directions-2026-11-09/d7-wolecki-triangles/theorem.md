# Wall-count lower bounds for clean rooms from Wolecki triangles

Every clean room built from an allowed triangle with `n >= 6` has at least 26
walls. The only triangle that reaches the 26 to 27 range is 30-60-90. Every
other allowed triangle with `n >= 6` either admits no clean room or needs at
least 32 walls. The target "at least 22 walls for `n >= 6`" holds with margin.

For `n = 4` (45-45-90), the counting gives 22, and 23 unless the two stars
share a corner. The best clean room that this direction constructs has 24
walls.

All hand proofs in this file are unreviewed. The section
[What to re-derive first](#what-to-re-derive-first) lists the steps to check.

## Result

Notation: `u = pi/n`, and `n` is even. The triangle has angles
`(1, b, c) * u` at `A`, `B`, `C`, with `b + c = n - 1` and `b < c`.
`W` is the number of walls of the room.

| Triangle class | Condition | Clean rooms with two interior A points | Best room found |
| --- | --- | --- | --- |
| Closed star | `3c >= 2n` | None. No room at all, clean or not. | Not applicable |
| Right, `n >= 8` | `2c = n`, `n >= 8` | None | Not applicable |
| 30-60-90 | `(n, b) = (6, 2)` | `W >= 26` by hand; `W >= 27` with d1's search | 27 |
| 45-45-90 | `(n, b) = (4, 1)` | `W >= 22`; `W >= 23` unless the stars share a corner | 24 |
| 22.5-45-112.5 | `(n, b) = (8, 2)` | `W >= 32`, exact | 32 |
| 60-degree family | `3b = n`, `n >= 12` | `W >= 4n` (48, 72, 96, ...) | `4n + 2` |
| Generic obtuse | all other triangles with `n/2 < c < 2n/3` | `W >= 4n + 2` (42, 58, 66, ...) | `4n + 2` for five triangles |

The closed-star class contains every isosceles triangle with `n >= 6`,
including 30-30-120. Tokarsky's 9-72-99 triangle is `(n, b) = (20, 8)`,
generic obtuse: `82 <= W`, and this direction constructs a room with 84 walls.

## Setting and notation

### Triangles

Wolecki's Lemma 3.1 (arXiv 1905.09358) covers a triangle `ABC` with angle
`pi/n` at `A` and `m * pi/n` at `B`. Here `n` is even and `0 < m < n - 1`.
In such a triangle, no billiard trajectory from `A` returns to `A`.

- Write the angles as `(1, b, c) * u` with `u = pi/n` and `b + c = n - 1`.
- `n - 1` is odd, so `b != c`. Label the vertices so that `b < c`.
- Then `c >= n/2`. The triangle is right (`c = n/2`, `b = n/2 - 1`) or obtuse
  (`c > n/2`). No allowed triangle is acute.
- Side lengths: `|BC| < |AC| < |AB|`. Write `R = |AB|` and `r = |AC|`.
- This file writes a triangle as `(n, b)` or as `(1, b, c)`.

### Rooms

A room is a strictly simple polygon `Q` with these properties:

- `Q` is a finite union of tiles. Each tile is an isometric copy of the
  triangle, and distinct tiles have disjoint interiors.
- A continuous fold map `f: Q -> ABC` exists that is an isometry on each tile.
- `Q` contains two distinct interior points `S` and `T` with `f(S) = f(T) = A`.

A point of `Q` that folds to a vertex `V` is a `V` point. An interior A point
is an A point in the interior of `Q`.

A billiard path in `Q` is a polygonal path that obeys the reflection law at
walls. A path that reaches a corner of `Q` stops there. A path may pass
through `S`, `T`, or any other non-corner point at intermediate times.

### Obstruction set and clean rooms

For a vertex `V` with angle `v * u`, write the angle as `p * pi/q` in lowest
terms. Then `q = n / gcd(v, n)` and `p = v / gcd(v, n)`.

The obstruction set is

```
E = { V in {B, C} : v divides n and n/v is even }
```

Equivalently, `V` is in `E` when its angle is `pi/q` with `q` even.

A room is clean when every `V` point with `V` in `E` is a corner of `Q`.
"Every point" means every point of the closed polygon, including boundary
points.

Values of `E`:

- Right triangles: `C` is in `E`. `B` is in `E` only for `n = 4`.
- 45-45-90: `E = {B, C}`. 30-60-90: `E = {C}`.
- `(1, 2, 5)` with `n = 8`: `E = {B}`.
- Closed-star triangles: `E` can be nonempty, for example `E = {B}` for
  `(1, 1, n - 2)`. These triangles admit no room, so `E` doesn't matter.
- Every other triangle with `n/2 < c < 2n/3`: `E` is empty. Every room is
  clean, and every room is dark between interior A points.

Proof of the last three items. `c >= n/2` and `c < n`, so `c` divides `n`
only when `c = n/2`. For the obtuse triangles with `c < 2n/3`, the inequality
`n/3 - 1 < b < n/2 - 1` holds. If `b = n/k`, then `n(k - 3) < 3k`. The
solutions are `k = 3` (`n >= 12`, and `n/b = 3` is odd) and `(n, b) = (8, 2)`
(`n/b = 4`). For a right triangle, `b = n/2 - 1` divides `n` only if it
divides 2, so `n` is 4 or 6. PROVED. `verify.py` check V1 confirms the
classification for `n <= 40`.

## Theorem 1: the clean-room condition

**Theorem 1.** Let `Q` be a clean room. Then no billiard path in `Q` joins
two interior A points, equal or distinct. PROVED.

The three kinds of vertex class behave as follows:

- `q` odd: the class never obstructs. Its points are free.
- `q` even and `p > 1`: the class obstructs, and every point of the class is
  automatically a corner.
- `q` even and `p = 1` (the set `E`): the class obstructs only at corners.
  The clean condition is exactly the requirement on this class.

At least one of `B`, `C` has `q` even, because one of `b`, `c` is odd.

### Proof

**Step 1: local structure.** Let `P` be a `V` point with `k` tiles around it.
`P` is an interior point of `Q` if `k * v = 2n`, and then `k` is even. `P` is
a flat wall point if `k * v = n`. In every other case `P` is a corner
(Lemma L1). In both non-corner cases `v` divides `n`, so `p = 1`. The number
of tiles is `2q` for an interior point and `q` for a flat point.

**Step 2: the surface.** Let `D` be the group that the linear parts of the
three side reflections generate. `D` is dihedral of order `2n`. Let `M` be
the unfolding surface: `2n` copies of the triangle, indexed by `D`, with copy
`h` glued to copy `h * s_i` along side `i`. `M` is a translation surface.
The lifts of `V` have cone angle `2 * pi * p`. `A` has one lift `O`, and `O`
is a regular point.

**Step 3: the involution.** `n` is even, so `-I` is in `D` and is central.
Left multiplication by `-I` is an isometry `tau` of `M` with derivative `-I`.
`tau` fixes no point inside a copy and no interior point of a side, because
no `s_i` equals `-I`. The lifts of `V` correspond to cosets of a dihedral
subgroup of order `2q`. That subgroup contains `-I` exactly when `q` is even.
So the fixed points of `tau` are the lifts of the vertices with `q` even.

**Step 4: the lift.** Suppose a billiard path `g: [0, L] -> Q` joins interior
A points and avoids corners. Unfold `g` at each wall reflection. The result
is a path `G` in `M` with constant direction, and `G(0) = G(L) = O`.
If `g` passes through a tile vertex `P`, then `P` is an interior point or a
flat point. By step 1, `p = 1`, and a disc of `2q` tiles around the lift is
flat. For a flat point, reflect the half-disc of `q` tiles across the wall to
get the disc. So `G` is a straight geodesic that passes only through regular
points and removable cone points.

**Step 5: the midpoint.** Let `T1` be the first time `t > 0` with
`G(t) = O`. The path `t -> tau(G(T1 - t))` starts at `O` with the same
direction as `G`. Geodesics through regular points are unique, so
`G(t) = tau(G(T1 - t))` on `[0, T1]`. The point `X = G(T1/2)` is fixed by
`tau`, and `X != O` because `T1` is the first return.

**Step 6: the contradiction.** By step 3, `X` is a lift of a vertex `V` in
`{B, C}` with `q` even. By step 4, `p = 1`. So `V` is in `E`, and
`g(T1/2)` is a `V` point that isn't a corner. The room isn't clean. This
contradiction proves the theorem.

Steps 2, 3, and 5 follow Wolecki's proof of Lemma 3.1. Steps 1, 4, and 6
adapt it to rooms.

### What the condition doesn't say

The condition is sufficient, not necessary. A room with a non-corner point of
a class in `E` can still be dark. Those fold-type rooms are out of scope.
The three lit controls in `shoot_checks.py` show that you can't drop the
condition. Each control has a non-corner point of a class in `E`. Each has a
path between interior A points.

## Structure lemmas

### L1: tiling and fans

**Lemma L1.** In a room:

1. Two tiles meet in a common edge, a common vertex, or not at all. Two tiles
   that share an edge are mirror images in that edge.
2. The tiles at a tile vertex `P` form one fan: consecutive tiles share an
   edge. If `P` is a `V` point with `k` tiles, the angle of `Q` at `P` is
   `k * v * u`.
3. `P` is interior exactly when `k * v = 2n`, and then `k` is even. `P` is
   flat exactly when `k * v = n`. In every other case `P` is a corner.
4. The tiles of `Q` are connected through shared edges.
5. Turning sum: the sum of `n - k * v` over the corners equals `2n`.

PROVED.

Proof. Let two tiles share a segment. The fold map agrees on the segment, so
the segment lies in the same side of the triangle for both tiles. The two
isometries agree on a segment of that side, so the two edges coincide. The
tiles lie on opposite sides of the edge, so they are mirror images.

Suppose a tile vertex `P` lies inside an edge `e` of a tile `t`. If `Q`
contains points on the other side of `e` near `P`, a tile there shares a
segment with `e`. That tile is the mirror of `t`, and `P` isn't a vertex.
If not, a tile that touches `e` only at `P` makes `P` a pinch point. A
strictly simple polygon has no pinch point. This proves item 1.

`Q` is locally a sector at every point, which gives item 2. Item 3 follows
from the angle, and an interior fan alternates orientation, so `k` is even.
The interior of `Q` stays connected after you remove the tile vertices,
which gives item 4. Item 5 is the exterior-angle sum in units of `u`.

Two consequences:

- In a fan at a B point, the spokes alternate between type `BA` and type
  `BC`. The same holds for the other classes.
- A non-corner `V` point forces `v` to divide `n`.

### Stars and hypothesis H

The star `St(S)` of an interior A point `S` is the set of the `2n` tiles at
`S`. It has `n` B-tips at distance `R` from `S` and `n` C-tips at distance
`r`. B-tips and C-tips alternate, at angular steps of `u`. The star has `2n`
boundary edges, all of type `BC`. Each tip carries two star tiles that share
a spoke.

- Right triangle: the star is a convex regular `n`-gon. The B-tips are its
  vertices and the C-tips are the midpoints of its sides.
- Obtuse triangle: the star is a nonconvex `2n`-gon. Each C-tip is a reflex
  vertex of the star with angle `2c * u > pi`.

**Hypothesis H.** Every C point of `Q` is a corner of `Q` with at most three
tiles.

**Lemma L0.** H holds in these two cases. PROVED.

- The triangle is obtuse with `3c < 2n`. Any room qualifies.
- The triangle is right and the room is clean. Then every C point has
  exactly one or exactly three tiles.

Proof. A C point with `k` tiles has `k * c <= 2n`. In the obtuse case
`k <= 3`, and `k * c` is never `n` or `2n`. In the right case `k <= 4`. Two
tiles give a flat point and four give an interior point. `C` is in `E`, so
a clean room excludes both.

Lemmas L2 to L7 assume H.

### L2: two stars share almost nothing

**Lemma L2.** Let `S` and `S'` be distinct interior A points. Their stars
share no tile, no edge, and no C-tip. PROVED.

Proof. A tile has one A vertex, so the stars share no tile. A shared edge
has type `BC`, because a shared spoke gives `S = S'`. Let its C endpoint be
`C0`. Then `C0` carries two tiles of each star, four tiles in total. H
excludes that. A shared C-tip also carries four tiles.

### L3: exit tiles

An exit tile of `S` is a tile outside `St(S)` that shares an edge with a tile
of `St(S)`. Write it as `(M, B0, C0)`. It is the mirror of the star tile
`(S, B0, C0)` in the line `B0 C0`. Call `M` its centre.

**Lemma L3.** Let `e = (M, B0, C0)` be an exit tile of `S`. PROVED.

1. `M` isn't an interior A point. So `M` lies on the boundary, and the fan at
   `M` is linear.
2. `C0` has exactly three tiles, and the edge `M C0` is a wall segment.
3. `e` is an end tile of the fan at `M`, and the end spoke is `M C0`.
4. `e` is an exit tile of one star only, through one edge only.
5. A centre `M` has at most two exit tiles.

Proof. If `M` is interior, then `e` is in `St(M)` and shares an edge with
`St(S)`. L2 excludes that. `C0` carries two star tiles and `e`, so by H it
has exactly three tiles and is a corner. Its fan is linear: `e`, then
`(S, B0, C0)`, then the second star tile. So `e` is an end of that fan, and
its edge `M C0` has no tile on the other side. The only possible neighbour
of `e` at `M` is across the spoke `M B0`. Item 4 holds because `e` has one
`BC` edge. Item 5 holds because a linear fan has two ends.

### L4: corners that belong to a centre

Let `M` be a boundary A point. An inner C-tip of `M` is the far endpoint of
a C-type spoke that two tiles of the fan at `M` share. Define

```
N(M) = { M, if M is a corner } union { inner C-tips of M }
```

A non-tip corner is a corner of `Q` that isn't a tip of any star.

**Lemma L4.** PROVED.

1. Every point of `N(M)` is a non-tip corner.
2. For distinct boundary A points `M` and `M'`, the sets `N(M)` and `N(M')`
   are disjoint.
3. `N(M)` is nonempty.

Proof. An inner C-tip `X` carries two tiles with A vertex `M`. H makes `X` a
corner. Tiles with A vertex `M` aren't star tiles, because `M` isn't
interior. If `X` is a C-tip of a star, or an inner C-tip of `M'`, then `X`
carries four tiles. H excludes that. If `M` isn't a corner, its fan has `n`
tiles and `n - 1` inner spokes. At least `n/2 - 1 >= 1` of them have type C.

### L5: centres with two exit tiles

**Lemma L5.** Let `M` be the centre of two exit tiles. Let `m` be the number
of tiles in the fan at `M`. PROVED.

1. `m` is even. The end spokes have type C, and the inner spokes alternate
   B, C, ..., B.
2. If `m = 2`, the two exit tiles belong to two different stars, and the
   common B vertex `P` is a B-tip of both stars.
3. If `m >= 4`, then `|N(M)| >= 2`, except when `m = n = 4`.
4. If `m = n = 4`, the two exit tiles belong to two different stars `S1`,
   `S2`. `M` is the midpoint of `S1 S2`, and `|S1 S2| = 4r`.

Proof. By L3, both end spokes have type C. Spokes alternate, so `m` is even.

Let `m = 2`. The exit tiles are `(M, P, C0)` and `(M, P, C0')`, mirror
images in the line `M P`. Their star centres are the mirrors of `M` in the
lines `P C0` and `P C0'`. Those two lines differ, and `M` lies on neither.
Two different lines can't both be the perpendicular bisector of the same
segment. So the star centres differ.

Let `m >= 4`. The fan has `m/2 - 1` inner C-tips, and `M` is a corner unless
`m = n`. For `m != n` the count is at least 2. For `m = n >= 6` the count is
`n/2 - 1 >= 2`. For `m = n = 4` the count is 1.

Let `m = n = 4`. `M` is flat, so the end spokes `M C0` and `M C4` are
opposite. The triangle is 45-45-90, so `M C0` is perpendicular to the edge
`B C0`. The star centre of the first exit tile is `2 C0 - M`. The star centre
of the second is `2 C4 - M`.

**Corollary (exit-tile count).** Take any set of exit tiles. Let `delta`
count the centres that have two exit tiles and `|N(M)| = 1`. Those are the
centres with `m = 2`, and the centres with `m = n = 4`. Then

```
number of non-tip corners >= (number of exit tiles) - delta
```

Proof. Each centre `M` with one exit tile has `|N(M)| >= 1`. Each centre with
two has `|N(M)| >= 2` unless `delta` counts it. The sets `N(M)` are disjoint.

### L6: shared B-tips

Let `x` be the number of B-tips that `St(S)` and `St(T)` share.

**Lemma L6.** PROVED.

1. If `x >= 1`, then `3b < n`.
2. `x <= 1`.
3. If `x = 1` with shared tip `P`, then `T = 2P - S` and `2mb = n` for an
   integer `m >= 2`.
4. Among triangles with `n/2 <= c < 2n/3`, only `(4, 1)` and `(8, 2)` allow
   `x = 1`. For both, `m = 2`, and the fan at `P` has six or seven tiles in
   a clean room.

Proof of item 1. At a shared tip `P`, the two S tiles and the two T tiles
are four different tiles. By L2 no S tile shares an edge with a T tile. The
outer edges of both pairs have type `BC`. Spokes at `P` alternate, so the
gap between the pairs holds an even number of tiles, at least two. If `P` is
a boundary point, `6b < 2n`. If `P` is interior, `8b <= 2n`.

Proof of item 2, obtuse case. Let `P1` and `P2` be two shared tips. `S` and
`T` both lie at distance `R` from `P1` and `P2`. So `T` is the mirror of `S`
in the line `P1 P2`, and `St(T)` is the mirror of `St(S)`. The interiors of
the stars are disjoint, so the interior of `St(S)` misses the line. So no
B-tip of `St(S)` lies strictly beyond the line, and `P1`, `P2` are adjacent
B-tips. Let `C_S` and `C_T` be the C-tips between them in the two stars.
Both are reflex, so the segments `P1 C_S`, `C_S P2`, `P2 C_T`, `C_T P1` bound
a rhombus. `Q` is a closed disc, so the rhombus lies in `Q`. Then `C_S` is an
interior point of `Q`. H excludes that.

Proof of item 2, right case. The stars are convex polygons with disjoint
interiors. A line separates them, and `P1`, `P2` lie on it. So `P1 P2` is a
side of both polygons. Its midpoint is a C-tip of both stars. L2 excludes
that.

Proof of item 3. Count the A spokes at `P` from the S pair to the T pair.
Each step turns by `2b * u`. So `T` is `S` rotated about `P` by `2mb * u`
with `m >= 2`, and `(m + 1) b <= n`. The two circles of radius `R` about `S`
and `T` meet at `P` and at the mirror `P'` of `P` in the line `S T`. Seen
from `S`, the angle from `P` to `P'` is `(n - 2mb) * u` in absolute value.
That is an even multiple of `u`, so `P'` is a B-tip of `St(S)`. The same
holds for `T`. If `P' != P`, then `x >= 2`. So `P' = P`, the rotation angle
is `pi`, and `2mb = n`.

Proof of item 4. `b = n/(2m) <= n/4` gives `c >= 3n/4 - 1`. With `c < 2n/3`
this forces `n < 12`. Check `n = 4, 6, 8, 10`: the cases are `(4, 1)`,
`(8, 2)`, and triangles with `3c >= 2n`. For `(4, 1)` and `(8, 2)`, `B` is in
`E`, and eight tiles at `P` make `P` interior. A clean room excludes that.
So only one of the two gaps at `P` is full.

`verify.py` check V4 builds the configuration that item 3 forces, for every
obtuse triangle with `3b < n` and `n <= 40`. Only `(8, 2)` gives a valid
room. CHECKED BY COMPUTATION.

### L7: the connection between the stars

**Lemma L7.** Assume `x = 0` and `n >= 6`. Then `Q` has at least two non-tip
corners. PROVED.

Proof. Take a shortest chain of tiles `t_0, ..., t_k` from `St(S)` to
`St(T)`, where consecutive tiles share an edge. L1 gives the chain. By L2,
`k >= 2`. `t_1` is an exit tile of `S` and `t_(k-1)` is an exit tile of `T`.
By L3 item 4, they differ. If their centres differ, L4 gives two non-tip
corners. If the centres agree, `x = 0` excludes `m = 2` by L5 item 2. Then
L5 item 3 gives `|N(M)| >= 2`.

## Theorem 2: classification and bounds

**Theorem 2.** Let the triangle be `(1, b, c)` with `n` even, `b + c = n - 1`,
and `b < c`. Let `Q` be a room with two distinct interior A points. In cases
2, 3, 4, and 5, assume also that `Q` is clean. In cases 6 and 7 every room
is clean.

1. Closed star, `3c >= 2n`: no such `Q` exists.
2. Right, `n >= 8`: no such `Q` exists.
3. 30-60-90: `W >= 26`.
4. 45-45-90: `W >= 22`. If the two stars share no B-tip, `W >= 23`.
5. `(8, 2)`: `W >= 32`, and a clean room with `W = 32` exists.
6. Generic obtuse (`n/2 < c < 2n/3`, `b` doesn't divide `n`): `W >= 4n + 2`.
7. 60-degree family (`3b = n`, `n >= 12`): `W >= 4n`.

The seven cases cover every allowed triangle.

**Corollary.** For every allowed triangle with `n >= 6`, every clean room has
at least 26 walls. Every clean room from a triangle other than 30-60-90 has
at least 32 walls.

Proof of the corollary. Cases 6 and 7 need `n >= 10` and `n >= 12`, so their
bounds are at least 42 and 48.

### Case 1: closed-star triangles

PROVED. Suppose a tile lies outside `St(S)`. By L1 item 4, an exit tile
exists at some C-tip `C0`. `C0` then carries three tiles with total angle
`3c * u >= 2 * pi`. If `3c > 2n`, the angle is too large. If `3c = 2n`, `C0`
is interior with an odd number of tiles, which L1 excludes. So `Q = St(S)`,
and `Q` has one interior A point.

This case needs no clean hypothesis. It covers `(1, 1, n - 2)` for `n >= 6`,
because `n - 2 >= 2n/3`. `verify.py` check V2 tests all 732 single-tile
attachments for `n <= 20`. All fail. CHECKED BY COMPUTATION.

### Case 2: right triangles with n >= 8

PROVED. Let `h = |BC| = R sin u`, and note `r = R cos u`. By L0, every
C point has one or three tiles. Take a shortest chain `t_0, t_1, ...` from
`St(S)` to `St(T)`.

- `t_1` is an exit tile `(M, B, C_i)` at the C-tip `C_i` on side `i`.
- By L3, `M C_i` is a wall. So `t_2` is the mirror `y = (M, B, C')` of `t_1`
  in the spoke `M B`.
- `M` isn't interior, so `t_2` isn't a T tile, and `t_3` exists.
- Let `w_near = (M', B, C')` be the mirror of `y` in `B C'`. Let `w_far` be
  the image of `y` under the point reflection in `C'`.
- `t_3` lies across `B C'` or across `M C'`. Across `B C'`, `t_3` is
  `w_near`. Across `M C'`, the point `C'` has two tiles, so it has three.
  The third tile at `C'` is `w_near` or `w_far`.
- So `Q` contains `w_near` or `w_far`.
- Let `C_j` be the C-tip on the other star side at `B`. `C_j` needs a third
  tile. It is `N = (M_j, B, C_j)` or `F = (M_j, B'', C_j)`, where `B''` is
  the other end of that side.

`B` carries the two star tiles, `t_1`, and `y`. The free wedge at `B` has
angle `4u`, between the rays `B C_j` and `B C'`.

Sub-case `n >= 10`. A fifth tile at `B` needs `5b <= 2n`, so `n <= 10`. For
`n = 10` it makes `B` interior with five tiles. So `B` has four tiles.
`w_near` and `N` are fifth tiles at `B`, so `Q` contains `w_far` and `F`. Place `B` at the origin with the bisector of
the free wedge on the x-axis. Then `w_far` is the mirror of `F` in the
x-axis. The vertex `C_j` of `F` has y-coordinate `-h sin 2u < 0`. The vertex
`M_j` has y-coordinate `-h sin 2u + r cos 2u = R cos 3u > 0`. So the interior
of `F` meets the x-axis, and `F` overlaps `w_far`. Two tiles can't overlap.

Sub-case `n = 8`. The free wedge is a right angle. Place `B` at the origin,
`C_j = (h, 0)`, and `C' = (0, h)`. `N` and `F` share the leg from `(h, 0)` to
`(h, r)`. `w_near` and `w_far` share the leg from `(0, h)` to `(r, h)`.
`r > h`, so the legs cross at `(h, h)`, inside both legs. Each of `N`, `F`
overlaps each of `w_near`, `w_far`. `Q` contains one tile from each pair.

`verify.py` check V3 confirms the overlaps for `n = 8, ..., 40`, and confirms
that `n = 6` has none. Check V5 finds no room in the arc family for
`n = 8, 10, 12`. CHECKED BY COMPUTATION.

For these triangles, any dark room of this type is a fold-type room.

### Case 3: 30-60-90

PROVED: `W >= 26`. The star is a regular hexagon, and `E = {C}`.

- C-tips: 12 corners. L2 makes them distinct, and L0 gives three tiles each.
- Exit tiles: the third tile at each C-tip is an exit tile. An exit tile has
  one C vertex, so the 12 exit tiles are distinct.
- `x = 0` by L6 item 1, because `3b = n`. So no centre has `m = 2`, and
  `delta = 0`. The exit-tile count gives 12 non-tip corners.
- B-tip corners: each star has at least one. See the next paragraph. The
  two are distinct because `x = 0`.

Total: `12 + 12 + 2 = 26`.

B-tip corners. Each of the six exit tiles of `S` contains one of the two
B-tips next to its C-tip. A B point is flat with three tiles and interior
with six. If a B-tip contains no exit tile, it has two tiles and is a corner.
If not, every B-tip contains exactly one exit tile. Then one outer star edge
at each B-tip is a wall, so no B-tip is interior. Suppose every B-tip has
three tiles. Then each exit tile `(M, B, C0)` has walls `M C0` and `M B`. The
star and its six exit tiles are closed under adjacency, so they are all of
`Q`. That contradicts the existence of `T`. So a B-tip has four or five
tiles and is a corner.

`W >= 27`: d1's exact search (CP-SAT, hex radius 6, plus its window lemma)
gives 27 as the minimum. d1's C-clean condition is the clean condition here.
CHECKED BY COMPUTATION, in `d1-306090-relaxed/`, not re-run here.

Upper bound: `build.py` reproduces a 27-wall room with 42 tiles. Its angles
match d1's room: eight 30, two 60, three 120, fourteen 270.

### Case 4: 45-45-90

PROVED: `W >= 22`. The star is a square, and `E = {B, C}`.

- C-tips: 8 corners.
- B-tips: `8 - x` points, all corners because `B` is in `E`. `x <= 1` by L6.
- Exit tiles: 8, one for each C-tip, as in case 3.
- `delta <= 1`. See the next paragraph.

Total: `W >= 8 + (8 - x) + (8 - delta)`.

Bound on `delta`. A centre with `m = 2` sits in a gap at a shared B-tip `P`.
By L6 item 4, one gap at `P` is full, so at most one such centre exists, and
only when `x = 1`. A centre with `m = 4` is the midpoint of `S T` with
`|S T| = 4r`, by L5. At most one exists. If `x = 1`, then `|S T| = 2R`, and
`2R != 4r`. So `delta <= 1` in both cases.

- `x = 1`: `W >= 8 + 7 + 7 = 22`. Here `T = 2P - S`: the squares share a
  corner and are point reflections of each other.
- `x = 0`: `W >= 8 + 8 + 7 = 23`.

The counting stops at 22. This direction doesn't decide whether a clean room
with 22 or 23 walls exists. The best clean room found has 24 walls, 27
tiles, and `x = 0`. Its corners:

- seven A corners with one tile
- eight B corners, with 2, 2, 3, 3, 3, 3, 5, and 6 tiles
- nine C corners with three tiles

This direction constructs no clean room with `x = 1` for 45-45-90. The
18-tile shared-corner skeleton has no clean completion that adds one tile at
each C-tip (V5). Larger completions aren't searched.

d1's README records a 22-wall square-tiling room with transparent vertices.
That room isn't clean, so this case doesn't cover it.

### Case 5: the triangle (1, 2, 5)

PROVED: `W >= 32`. Here `n = 8`, `E = {B}`, and H holds by L0.

- C-tips: 16 corners. B-tips: `16 - x` corners, because `B` is in `E`.
- `x = 0`: L7 gives two non-tip corners, so `W >= 34`.
- `x = 1`: by L6 item 4 a gap at `P` holds two tiles with a common A vertex
  `M`. They are exit tiles, so `M` is a boundary point and `N(M)` is
  nonempty. `W >= 16 + 15 + 1 = 32`.

Upper bound: the two-star room has 34 tiles and 32 walls. Its corners:

- one A corner with two tiles
- 14 B corners with two tiles, and the shared tip `P` with six tiles
- 14 C corners with two tiles, and two C corners with three tiles

CHECKED BY COMPUTATION (`verify.py` V4 and V5).

So 32 is the exact minimum, and every 32-wall clean room has `x = 1`.

### Case 6: generic obtuse triangles

PROVED: `W >= 4n + 2`. `b` doesn't divide `n`, so every B point is a corner.
H holds, so every C point is a corner. `x = 0`, because L6 item 3 needs `b`
to divide `n`. The `2n` C-tips and `2n` B-tips are distinct corners. L7 adds
two non-tip corners.

`E` is empty, so the bound holds for every room with two interior A points.

Upper bound: the arc room joins the stars through four tiles of one fan. It
has `4n + 2` walls for `(10, 3)`, `(14, 4)`, `(14, 5)`, `(16, 5)`, and
`(16, 6)`. For those five triangles the minimum is exactly `4n + 2`.
CHECKED BY COMPUTATION (V5).

For 9-72-99, `(20, 8)`, the four-tile arc overlaps. A six-tile arc gives 84
walls. So `82 <= minimum <= 84`.

### Case 7: the 60-degree family

PROVED: `W >= 4n`. Here `b = n/3`, `E` is empty, and H holds. A B point is
flat with three tiles and interior with six. `x = 0` by L6 item 1.

Let `y` be the number of B-tips that aren't corners. Such a tip has more than
two tiles, so an exit tile contains it. An exit tile has one B vertex, so
these `y` exit tiles are distinct. `delta = 0`, so the exit-tile count gives
`y` non-tip corners. L7 gives two. So

```
W >= 2n + (2n - y) + max(y, 2) >= 4n
```

Upper bound: the four-tile arc room has `4n + 2` walls for `(12, 4)` and
`(18, 6)`. The gap of 2 is open.

## Answers to the four listed points

**(a) Shared tiles, edges, and forced corners.** Under H, two stars share no
tile, no edge, and no C-tip (L2). They share at most one B-tip (L6). A shared
B-tip occurs only for 45-45-90 and `(1, 2, 5)`, and then `T = 2P - S`. The
forced C-tip corners of two stars are always distinct.

**(b) Right triangles against obtuse triangles.** For a right triangle,
`2C = pi`, and each C-tip is flat in the star. A clean room attaches a third
tile at each C-tip, which gives `n` exit tiles for each star. For an obtuse
triangle, the star is a `2n`-gon with genuine corners at all `2n` tips. Then
nothing is forced except the connection (L7). `2B = pi` can't occur with
`b < c`.

**(c) Triangles where nothing attaches to the star.** These are the
triangles with `3c >= 2n`, including 30-30-120 and every isosceles triangle
with `n >= 6`. No room exists (case 1). Right triangles with `n >= 8` allow
attachments, but no clean room (case 2).

**(d) n = 4.** The counting gives `W >= 22`, and `W >= 23` unless the squares
share a corner (case 4).

## Bounds from the turning sum alone

These bounds use only L1 item 5 and the C-tips. They are weaker than
Theorem 2. PROVED.

- Right, clean: each C-tip contributes `-n/2`. The convex corners contribute
  at most `n - 1` each and must total at least `n^2 + 2n`. So
  `W >= 3n + 4`. For 30-60-90 this is 22, the hand bound that d1 records.
- Obtuse: each C-tip contributes at most `n - 2c`. So
  `W >= 2n + ceil(2n(c - b)/(n - 1)) >= 2n + 7`.

## Triangles where 22 isn't excluded

Only 45-45-90. The proved bound is 22, and 23 if the stars share no B-tip.
The smallest clean room constructed has 24 walls and no shared B-tip. For every triangle with
`n >= 6`, the proved bound is at least 26.

## Computation

All geometry is exact, in `Z[zeta_2n]`. The code takes signs from floats only
after an exact zero test.

`rooms.analyze` validates a tile set. It checks label consistency, edge
multiplicity, overlaps, edge connectivity, one boundary cycle, strict
simplicity, the area identity, fan angles, and the turning sum. It counts
walls in two independent ways.

| Check | Content | Result |
| --- | --- | --- |
| V1 | Classification and bounds, 190 triangles with `n <= 40` | PASS |
| V2 | Closed-star triangles, `n <= 20`: 732 attachments | PASS, all invalid |
| V3 | Right triangles, `n = 6, ..., 40`: the case 2 overlaps | PASS |
| V4 | Shared B-tip configuration, obtuse, `n <= 40` | PASS, valid only for `(8, 2)` |
| V5 | Constructed rooms against the proved bounds | PASS |
| Shooter | Three lit controls, three clean rooms | PASS |
| Hill-climb | Five triangles, 1,500 to 2,500 steps, 2 to 3 seeds | No improvement |

V5 results, as walls constructed against the proved bound:

| `(n, b)` | Angles in degrees | Proved bound | Constructed |
| --- | --- | --- | --- |
| `(4, 1)` | 45, 45, 90 | 22 | 24 |
| `(6, 2)` | 30, 60, 90 | 26 (27 with d1) | 27 |
| `(8, 2)` | 22.5, 45, 112.5 | 32 | 32 |
| `(10, 3)` | 18, 54, 108 | 42 | 42 |
| `(12, 4)` | 15, 60, 105 | 48 | 50 |
| `(14, 4)` | 12.9, 51.4, 115.7 | 58 | 58 |
| `(14, 5)` | 12.9, 64.3, 102.9 | 58 | 58 |
| `(16, 5)` | 11.25, 56.25, 112.5 | 66 | 66 |
| `(16, 6)` | 11.25, 67.5, 101.25 | 66 | 66 |
| `(18, 6)` | 10, 60, 110 | 72 | 74 |
| `(20, 8)` | 9, 72, 99 | 82 | 84 |

Shooter results (`shoot_checks.py`, exact unfolding, finite range):

- Lit controls: hexagon star, 48 of 60 shots arrive. Octagon star, 13 of
  178. `(1, 2, 5)` two-star room with `P` made interior, 2 of 1,128.
- Clean rooms: `(1, 2, 5)` 32-wall room, 0 of 1,412. 30-60-90 27-wall room,
  0 of 336. `(1, 3, 6)` 42-wall room, 0 of 1,536.

The shooter is a final check on Theorem 1 over a finite range. It isn't a
proof of darkness. Theorem 1 is.

The hill-climb is a falsification attempt, not a proof. It starts from the
constructed rooms and never finds a room under the starting count: 24, 27,
32, 42, and 50 walls.

## Status of each step

| Step | Status |
| --- | --- |
| Values of `E` and the list of triangle classes | PROVED; V1 for `n <= 40` |
| Theorem 1 (clean rooms are dark) | PROVED |
| L0 to L5, L7, and the exit-tile count | PROVED |
| L6 (shared B-tips) | PROVED; item 4 also CHECKED BY COMPUTATION (V4) |
| Case 1 (closed star) | PROVED; V2 |
| Case 2 (right, `n >= 8`) | PROVED; overlaps CHECKED BY COMPUTATION (V3) |
| Case 3, `W >= 26` | PROVED |
| Case 3, `W >= 27` | CHECKED BY COMPUTATION (d1, not re-run here) |
| Case 4, `W >= 22` | PROVED |
| Case 5, `W >= 32` | PROVED |
| Case 5, a 32-wall clean room exists | CHECKED BY COMPUTATION |
| Case 6, `W >= 4n + 2` | PROVED |
| Case 6, equality for five triangles | CHECKED BY COMPUTATION |
| Case 7, `W >= 4n` | PROVED |
| Minimum is 24 for 45-45-90 clean rooms | CONJECTURAL |
| Minimum is `4n + 2` for the 60-degree family | CONJECTURAL |
| Minimum is `4n + 2` for every generic obtuse triangle | CONJECTURAL; for `(20, 8)` the best room has 84 walls |

PROVED means a hand proof in this file. No second reader has checked these
proofs.

## What to re-derive first

1. **L3 item 2 and the exit-tile count.** Every bound that is tight or
   nearly tight uses it: 22, 26, and `4n`. Check that the edge `M C0` is a
   wall, and that the sets `N(M)` are disjoint.
2. **Theorem 1, steps 4 and 5.** Check the lift through flat wall points,
   and the first-return symmetry `G(t) = tau(G(T1 - t))`.
3. **Case 2.** The claim is strong: no clean room for a right triangle with
   `n >= 8`. Check that `t_2` and `t_3` are forced, and the sign of
   `R cos 3u`.
4. **Case 3, B-tip corners.** Check the closure argument that gives one
   B-tip corner for each star.
5. **Case 4, the bound on `delta`.** Check L5 item 4 and the comparison of
   `2R` with `4r`.
6. **L6 item 2, the rhombus.** Check that the rhombus lies in `Q` and makes
   `C_S` interior.
7. **L1.** The proof that the fold map and strict simplicity force an
   edge-to-edge tiling is short. Every later lemma depends on it.

## Out of scope: fold-type rooms

A fold-type room is dark although some point of a class in `E` isn't a
corner. Theorem 2 doesn't cover such rooms. Two remarks:

- For generic obtuse triangles and the 60-degree family, `E` is empty. No
  fold-type distinction exists, and the bounds hold for every room.
- For right triangles with `n >= 8`, every dark room of this type is a
  fold-type room, by case 2.

## Files and commands

All files are in this directory.

| File | Purpose |
| --- | --- |
| `theorem.md` | This file |
| `rooms.py` | Exact arithmetic, room validator `analyze`, billiard shooter |
| `build.py` | Constructions: two-star room, arc family |
| `verify.py` | Checks V1 to V5; writes `verify-results.json` |
| `shoot_checks.py` | Shooter checks; writes `shoot-checks.json` |
| `local_search.py` | Hill-climb; writes `local-search-<n>-<b>.json` |
| `wolecki-src/` | arXiv 1905.09358 source, downloaded, read only as data |

In its output, `verify.py` labels closed-star triangles `dead` and right
triangles with `n >= 8` `right-dead`.

Run from this directory:

```
python3 verify.py                      # about 3 minutes; last run: ALL_PASS True
python3 shoot_checks.py                # last run: ALL_PASS True
python3 build.py 8,2 10,3              # arc family for the listed (n, b)
python3 local_search.py 8,2,2000,3     # n, b, steps, seeds
```
