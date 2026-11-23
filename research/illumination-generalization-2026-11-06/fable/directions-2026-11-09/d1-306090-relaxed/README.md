# Relaxed 30-60-90 dark-room search (Direction 1)

The relaxed (2,3,6) model can't beat 22 walls. A simple C-clean room with two
interior A points needs at least 27 walls, and a 27-wall room exists. The
lower bound combines a hand argument (window lemma, below) with an exhaustive
CP-SAT run in the hex radius-6 window. The hand argument shows that hex
radius 6 contains every room with 26 or fewer walls.

Status: hex radius 6 (1,296 tiles) finished OPTIMAL at 27 in 337 s, with lower bound 27. Combined with the window lemma, 27 is the exact minimum for simple C-clean rooms in the whole (2,3,6) tiling. No room with W <= 21 exists in this class.

Phase 2 (transparent C points allowed): no dark room with W <= 23 was found.
The fold family has no member with W <= 23 (hand proof), and its smallest
member found has 43 walls. CEGAR excludes W <= 21 with at most 3 transparent
C points. K = 4 is open. See [Phase 2](#phase-2-rooms-dark-despite-transparent-c-points).

## Setting and model

- Coordinates `(x, y)` mean the physical point `(x, sqrt(3) y)`. The metric is
  `dx^2 + 3 dy^2`, so every predicate is exact integer or `Fraction` arithmetic.
- A lattice `L = <(12,0), (6,6)>`. C points are `(1/2)L \ L`. B points are
  `L + (6,2)` and `L + (12,4)`.
- A room is a finite union of tiles with one simple closed boundary.
- C-clean means every C point in the closed room has exactly 1 tile (90 degree
  corner) or 3 tiles (270 degree corner).
- The relaxed model requires C-clean, S = (0,0) interior (12 tiles), and at
  least one more interior A point. B points are free. `--strict` also forces
  every B point to be a corner, as `.context/illumination_306090.py` line 121
  does.
- Wall count W is the number of polygon corners after collinear merging.

## Task 1: attempts to refute the claims

All three claims survive. Output: `verify-claims.json`, `verify-lemmas.json`.

| Claim | Check | Result |
| --- | --- | --- |
| Midpoint of a primitive A-to-A vector is a C point | All 8,816 primitive `(a,b)` with `max(|a|,|b|) <= 60`; every `t = j/6` (and `j/60` for short vectors) | PASS, 0 failures |
| No other C, no A, B only at `t = 1/3, 2/3` on a primitive piece | Same enumeration; B appears on 2,182 vectors, always at both thirds | PASS |
| Non-primitive `d = k d0`: first C at `t = 1/(2k)` | All 5,824 non-primitive vectors in range | PASS |
| The three classes of `(1/2)L / L` are edge midpoints | Direct | PASS |
| Pinwheel: 12 walls, six 270-degree C corners, six 30-degree tips, B flat | `check_room.py` on the 18-tile room | PASS; 6 flat B, no transparent C |
| All 64 choices of the six extra tiles | Each is C-clean | 12 to 18 walls |

Shots from the pinwheel's single interior A toward all 1,458 A points within
20 edge lengths all hit a C corner, each at `tau <= 1/2`. A lit control
(6-wall hexagon, 42 transparent C points) shows 366 open shots out of 516.
This confirms the shooter can detect light.

### The parity argument, checked by hand

The argument is sound for simple and non-simple rooms alike:

1. Every wall lies on a mirror line of the (2,3,6) reflection group.
   Unfolding a billiard path across walls gives a straight segment from S to
   an image T' of T. Reflections preserve vertex classes, so T' is an A point.
   T' differs from S because the path has positive length.
2. Write `T' - S = k d0` with `d0` primitive. The point `S + d0/2` lies in
   `(1/2)L \ L`, so it's a C point. It sits at fraction `1/(2k) <= 1/2` of
   the segment, strictly inside.
3. That point of the segment is a point of the closed room with class C. If
   it lies on a wall, the path reflects there or touches it. C-clean means it
   has 1 or 3 tiles, so it's a polygon vertex and the path is illegal.

Holes considered and closed:

- Boundary A points don't matter. The argument only needs S and T to be
  interior A points; other A points never need to block.
- Non-primitive segments are covered by item 2.
- A C point on a flat wall (2 adjacent tiles) is transparent: light reflects
  there legally. C-clean excludes it.
- A C point with 2 opposite tiles is a pinch point. The simple-polygon
  requirement excludes it.
- The certificate only covers S and T at A points. Rooms dark for other
  pairs, or dark through transparent C points, are outside this model. See
  "Exact decider design" below.

## Tasks 2 and 3: search results

Solver: OR-Tools CP-SAT 9.15 in `.context/illumination-venv`. Every run
finished with a conclusive status well inside the 30-minute cap.

| Run | Window | Tiles | Result |
| --- | --- | ---: | --- |
| `search-strict-para2.json` | parallelogram r=2 | 192 | INFEASIBLE (regression) |
| `search-strict-para3.json` | parallelogram r=3 | 432 | INFEASIBLE (regression) |
| `search-strict-para3-noturn.json` | same, no redundant turning constraint | 432 | INFEASIBLE |
| `search-sanity-one-interior-para2.json` | r=2, one interior A | 192 | OPTIMAL 12 (the pinwheel) |
| `search-sanity-one-interior-strict-para2.json` | r=2, one interior A, strict | 192 | OPTIMAL 18 |
| `search-relaxed-para2.json` | parallelogram r=2 | 192 | INFEASIBLE |
| `search-relaxed-para3.json` | parallelogram r=3 | 432 | OPTIMAL 27 |
| `search-relaxed-hex4.json` | hex r=4 | 576 | OPTIMAL 27 |
| `search-relaxed-hex5.json` | hex r=5 | 900 | OPTIMAL 27 |
| `search-relaxed-hex6.json` | hex r=6 | 1,296 | OPTIMAL 27 (337 s) |
| `search-relaxed-hex6-le26-tdist4.json` | hex r=6, W <= 26, T within hex distance 4 (lemma cut) | 1,296 | INFEASIBLE (419 s) |
| `search-relaxed-para3-noturn.json` | parallelogram r=3, no turning constraint | 432 | OPTIMAL 27 |
| `search-relaxed-hex4-noturn.json` | hex r=4, no turning constraint | 576 | OPTIMAL 27 |
| `search-relaxed-hex5-noturn.json` | hex r=5, no turning constraint | 900 | FEASIBLE 27, bound 20 (time cap 550 s) |
| `search-relaxed-hex6-le26-noturn.json` | hex r=6, W <= 26, no turning constraint | 1,296 | UNKNOWN, bound 19 (time cap 1,700 s) |

The `noturn` runs drop the redundant constraint "sum of turning = 360
degrees". Where they finish, they agree with the main runs. This cross-checks
the turning encoding. Without it, hex 6 doesn't finish in 30 minutes, so the
hex-6 certificate relies on that constraint. The constraint is a theorem for
simple polygons.

The hex window of radius r holds every lattice triangle whose three A vertices
lie within hex distance r of S = (0,0).

**Regression.** With `--strict`, the code reproduces the old simple-polygon
result: INFEASIBLE for every W at parallelogram radius 3 (and radius 2). This
is the same result as `.context/306090-large-simple-result.json` and is
stronger than "infeasible for W <= 21". The old `--max-walls 21` run allowed
holes and contacts; this model is simple-only and does not re-run that class.

### Why hex radius 6 is enough (window lemma)

Let a simple C-clean room have interior A points S and T and W <= 26 walls.
Let n1 and n3 count C points with 1 and 3 tiles. Let k count A and B corners.

1. Every C point in the room is a corner. The turning sum gives
   `360 = 90 n1 - 90 n3 + sum(A,B turning)`, and each A or B corner turns at
   most 150 degrees. So `W = n1 + n3 + k` with `150 k >= 360 + 90 (n3 - n1)`.
2. The six edge midpoints of an interior A point each have exactly 3 tiles.
   S and T are not adjacent, since the shared midpoint would have 4 tiles. So
   `n3 >= 12`. With W <= 26 this forces `n1 + 4 n3 <= 59`, so `n3 <= 14`.
   Check L1 in `verify_lemmas.py`. The same inequality alone gives W >= 22.
3. Tiles with different C vertices that share an edge share their A vertex
   (check L2). A 1-tile C group touches the rest of the room only through its
   AB edge, so it's a leaf with the same A vertex as its neighbor. A 3-tile
   group at the midpoint of lattice edge `uv` has A vertices `u` and `v`
   (check L3).
4. So the 3-tile groups form a connected set of lattice edges: the 6 edges at
   S, the 6 at T, and at most 2 more. Enumeration (check L4) shows this
   requires hex distance(S, T) <= 4. Every room A vertex then lies within hex
   distance 5 of S.
5. Every tile with an A vertex within distance 5 lies in the hex-6 window
   (check L5).

So no room with W <= 26 exists anywhere if none exists in hex radius 6.
Steps 1 to 3 are proofs written here. `verify_lemmas.py` checks each step by
exhaustive exact enumeration. Steps 2 and 4 also give a sharper fact: exactly
two interior A points, at hex distance 2, 3, or 4.

## Task 4: independent checker

`check_room.py` shares no code with `search_relaxed.py`. It re-derives vertex
classes from lattice membership. For each room it checks:

- each tile's shape: labels, right angle at C, side lengths;
- simplicity: tile edge-connectivity, one boundary cycle with all degrees 2,
  and shoelace area equal to total tile area;
- corners and interior angles from the polygon alone, cross-checked against
  tile counts at every vertex; turning sum 360;
- the interior A points, by tile count and by strict point-in-polygon;
- tile counts at every C point;
- darkness: from each interior A point it fires an exact billiard toward
  every A point X with |X - S| <= 30 edge lengths (3,258 directions). Each
  shot runs for the unfolded length |X - S|. The checker records whether a
  corner is hit first and confirms the corner comes at `tau <= 1/(2 gcd)`.

`run_checks.py` runs the checker on every reported room. Output:
`check-results.json`. Every reported 27-wall room passes. All 3,258 shots from
S and from T hit a corner (3,141 first at a C corner, 117 first at a B
corner). The wall count agrees with the solver.

## The 27-wall room

`search-relaxed-para3.json`, picture `search-relaxed-para3.png`. It has
42 tiles, S = (0,0), T = (-24,0) (two lattice steps apart along `e1`). The
bridge is a half-star at A point (-12,0), which is flat.

Angles: eight 30, two 60, three 120, fourteen 270 (all 14 C points). It has
2 interior B points and 8 flat B points, which the strict model forbids.

Corners in boundary order (x, y meaning (x, sqrt(3) y)), label, angle:

```
(-36,0) A 30    (-30,0) C 270   (-30,-2) B 120  (-27,-3) C 270
(-30,-6) A 30   (-21,-3) C 270  (-18,-6) A 60   (-15,-3) C 270
(-12,-4) B 120  (-9,-3) C 270   (-6,-6) A 60    (-3,-3) C 270
(6,-6) A 30     (3,-3) C 270    (6,-2) B 120    (6,0) C 270
(12,0) A 30     (3,3) C 270     (6,6) A 30      (-3,3) C 270
(-6,6) A 30     (-6,0) C 270    (-18,0) C 270   (-18,6) A 30
(-21,3) C 270   (-30,6) A 30    (-27,3) C 270
```

## Verified versus assumed

Verified by computation:

- the midpoint and B-position claims up to `max(|a|,|b|) <= 60`;
- the pinwheel's 12 walls and its C status;
- strict regression INFEASIBLE at radius 2 and 3;
- relaxed optimum 27 in parallelogram r=3 and hex r=4, 5, and 6;
- the five window-lemma steps by exhaustive enumeration;
- checker results for every reported room.

Proved by hand, written above:

- the parity argument;
- the window lemma that makes hex r=6 sufficient.

Assumed:

- CP-SAT's INFEASIBLE and OPTIMAL claims are correct. No solver proof log was
  produced. Two hex-6 formulations agree: the full optimization, and W <= 26
  with the lemma's T-distance cut.
- The per-point turning values in the table rows are right. The `noturn`
  runs agree at parallelogram r=3 and hex r=4. Hex 6 without the constraint
  timed out.
- The table encoding (contiguous fans, C sizes 3 or 9 slots, Euler
  characteristic 1 plus a connectivity tree) captures exactly the simple
  C-clean rooms. The sanity runs (pinwheel 12, strict regression) support
  this. They do not prove it.

Out of scope:

- rooms with holes;
- pairs not at A points;
- rooms dark through transparent C points (covered in Phase 2 below).

For rooms with holes the turning sum is `360 (1 - h)`, and the window lemma
fails.

## Exact decider design (not implemented)

The known 22-wall square-tiling room keeps transparent vertices on mirror
seams. To search that class in the (2,3,6) tiling, the parity certificate
must be replaced with an exact pair-illumination decider.

1. **Translation surface.** Unfold the room by the 12-element dihedral group
   into a translation surface X. Transparent C points (4 tiles, or 2 tiles on
   a wall) become regular points with cone angle 2 pi. Genuine corners become
   cone points or marked points. X is a branched cover of the torus `C / L'`
   for the lattice `L'` spanned by the tile vertices, branched only over
   torsion points. So X is a Veech (arithmetic) surface.
2. **Combinatorial encoding.** Encode X as a finite permutation
   representation: an "origami" over the hexagonal torus. Use the sheets,
   the monodromy around each puncture, and the lifts of S and of every image
   of T.
3. **Finite reduction.** Every S-to-T direction is rational for `L'`, so it is
   a parabolic direction. The affine maps of X that fix the lifts of S and T
   form a finite-index subgroup `Gamma'` of SL(2,Z). Directions in one
   `Gamma'` orbit give the same answer. `Gamma'` has finitely many cusps.
4. **Per-cusp test.** For each cusp direction, compute the cylinder
   decomposition of X. Decide whether a lift of T lies on the leaf through S
   before a cone point. This is exact rational arithmetic on a finite
   cylinder diagram.
5. **Search integration.** Run CEGAR, as the square-grid "ray cut" runs do.
   CP-SAT proposes a room with W <= 21 and C points allowed to be
   transparent. The decider either certifies it dark or returns an
   illuminating segment. In the second case, add a cut: at least one C point
   that segment crosses must become a genuine corner, or the tile set must
   change.

Cost: sheets and cusps grow with room area. The rooms of interest have under
about 60 tiles, so the cusp count should stay small.

Risk: computing `Gamma'` needs an SL(2,Z) coset enumeration on the monodromy
data. Without `surface_dynamics` or `flatsurf` installed, that code would be
new and would need its own audit. Validate it first against the shooter in
`check_room.py` and against the square-grid 22-wall room.

## Phase 2: rooms dark despite transparent C points

A transparent C point is a C point that isn't a corner: 2 tiles forming a flat
boundary point, or 4 tiles (interior). Phase 1 forbade them. Phase 2 allows
them and asks whether a simple room with two interior A points and at most 23
walls can still have a dark A pair.

Result: no dark room with W <= 23 was found. Two exact scopes exclude part
of that range.

- **Fold family.** No member has W <= 23. The hand bound is W >= 25 for 3
  copies (24 if all three meet at one point) and W >= 28 for 2 or 4
  copies. The smallest fold room found has 43 walls. Its proof of darkness
  is complete.
- **CEGAR.** No simple room with W <= 21, two interior A points, and at most
  K transparent C points has a dark A pair, for K <= 3. The window is proved
  sufficient for each K. K = 4 is open: 4 of 10 T values ran to the budget
  as UNKNOWN with no candidate. See the scope table below.
- **Dark candidates with W <= 23.** None. The only dark rooms found are fold
  rooms with W >= 43.

### Task 1: fold family

**Setting.** A base B is a simple C-clean polyform. S and T are A points on
the boundary of B, each flat: B has exactly the 6 tiles on one side of a
mirror line `l1` through S, and of a mirror line `l2` through T. The room is
`Q = B u s1 B` (F2) or `Q = B u s1 B u s2 B` (F3), with `s_k` the reflection
in `l_k`. Copies meet only along their seam. S and T must be interior to Q.

**Seam shape (hand).** Near the seam, B lies on one side of `l1`, otherwise
B and `s1 B` overlap. For a lattice-direction `l1`, the C points `S +- (6,0)`
on `l1` get one tile from S's half star. Exactly 2 tiles breaks C-clean.
Any 3-tile set there contains a tile whose mirror image is also in the set,
so B would overlap `s1 B`. So each point has 1 tile and is a 90-degree corner
of B. The seam is therefore exactly one lattice edge, centered on S, with two
90-degree C corners as endpoints. In Q, each endpoint is two 90-degree corners, so it's a flat,
transparent C point. One consequence: a seam holds a single A point, so S and
T can't share a seam.

**Wall bound (hand).** Every corner of a copy survives in Q except at seam
endpoints. Each endpoint removes at most 2 corners. So `W(Q) >= 2 w_B - 4`
(F2) and `W(Q) >= 3 w_B - 8` (F3). Equality holds when the endpoints are
90-degree corners. If all three F3 copies met at one point, the loss is at
most 9, which gives `W >= 3 w_B - 9`. For a base, the turning sum gives
`n1 + 4 n3 <= 2.5 w_B - 6`.

- F3, both seams on lattice lines. The two C points of S's half star at 60
  and 120 degrees have 2 tiles from S, so each needs a third tile and is a
  3-tile corner. The same holds at T. That gives `n3 >= 4` unless S and T are
  adjacent, and adjacent A points are always lit (P4). The 4 seam endpoints
  give `n1 >= 4`. So `20 <= 2.5 w_B - 6`, so `w_B >= 11` and `W >= 25`.
- F3 with one or two altitude seams. An altitude half star has 3 such C
  points, so `n3 >= 5` and `w_B >= 11` again. `W >= 25`.
- F2. T is interior to Q but not on the seam, so T is interior to B or to
  `s1 B`. Its 6 star midpoints all need 3 tiles, plus 2 at S: `n3 >= 8`
  (adjacent pairs excluded). A lattice seam adds `n1 >= 2`, so
  `34 <= 2.5 w_B - 6`. An altitude seam gives `n3 >= 9` instead. Either
  way `w_B >= 16` and `W >= 28`.
- F4 or more copies: `W >= 4 w_B - 16 >= 28`.

So no fold room has W <= 23, and the shooter task for W <= 23 is vacuous.
The base-first CP-SAT run `phase2-fold-F3-edge-hex4.json` agrees. Without
copy-disjointness it found min `w_B = 11` OPTIMAL in hex 4, and every
11-wall base made overlapping copies.

**Direct F3 search.** `phase2_fold2.py` models B, its two copies, and Q
together for a fixed T, `l2`, and side. `l1` is the x-axis. The model needs
disjoint copies, seam-only contacts, a C-clean base, a simple Q, and S and T
interior. It minimizes W(Q). `phase2_fold2_sweep.py` runs every T with
`hexdist(S,T) <= 4`, all 6 lines `l2`, and both sides, in the hex-5 window.
Reflections in the x-axis and the y-axis preserve the family, so the sweep
uses one T per orbit (`j >= 0`, `2i + j >= 0`). Output:
`phase2-fold2-sweep-d4-r5.json`. Of the 216 runs (18 T, 300 s each), 199
are INFEASIBLE, 13 OPTIMAL, and 4 UNKNOWN with lower bounds 38, 38, 47, and
48. The minimum is W = 43 at T = (0,2) in lattice coordinates, `l2` direction
(-1,1). The y-axis mirror image of that room is the 43-wall room below. The
next values are 45, 45, 54, and 55.

The hex-5 window isn't proved sufficient for this minimum. The hand bound of
25 is the proved lower bound. Values between 25 and the minimum found are
open.

**The 43-wall fold room** (`phase2-fold2-T-2_2-l1_1-s0.json`). S = (0,0),
T = (-12,12), `l1` = x-axis, `l2` = the line through T in direction (1,1).
The base has 22 tiles and 17 walls; Q has 66 tiles and `3*17 - 8 = 43` walls.
Base corners:

```text
(-12,8) (-9,9) (-3,3) (-6,2) (-6,0) (6,0) (6,2) (3,3) (6,6) (0,6) (0,8)
(-3,9) (0,12) (-6,12) (-6,14) (-9,15) (-15,9)
```

Room corners:

```text
(-39,15) (-33,9) (-30,10) (-30,12) (-18,12) (-18,10) (-12,8) (-9,9) (-3,3)
(-6,2) (-6,-2) (-3,-3) (-9,-9) (-12,-8) (-15,-9) (-9,-15) (-6,-14) (-6,-12)
(0,-12) (-3,-9) (0,-8) (0,-6) (6,-6) (3,-3) (6,-2) (6,2) (3,3) (6,6) (0,6)
(0,8) (-3,9) (0,12) (-6,12) (-6,14) (-12,16) (-15,15) (-18,18) (-21,15)
(-24,16) (-27,15) (-30,18) (-33,15) (-36,16)
```

Interior A points: exactly S and T. Transparent C points: (-6,0), (6,0),
(-15,9), (-9,15), the 4 seam endpoints. `phase2_certify.py` reports
(`phase2-certify.json`):

- shooter, bound 40, both orders S->T and T->S: no legal path (5,814
  targets each);
- `mirror_exact` from S, all 12 mirror directions: 10 hit a corner, 2 are
  periodic;
- fold conditions: base C-clean, and every non-corner point of Q whose
  preimage is a base corner lies in exactly 2 copies with 90 degrees each.

**Fold proof**, adapted from the manuscript's parity, seam-endpoint reversal,
and reversals-do-not-help lemmas:

1. Let `f: Q -> B` fold each copy onto B. A billiard path in Q from S to T
   that avoids corners maps to a billiard path in B. A transversal seam
   crossing becomes a reflection off the seam, which is a wall of B.
2. Passing straight through a seam endpoint in Q maps to arriving at a
   90-degree corner of B whose two walls are perpendicular mirrors. The
   folded velocity becomes `-v`: a reversal. The fold conditions show that
   the seam endpoints are the only non-corner points of Q over base corners.
3. Reversals don't help. After a reversal the folded path retraces itself
   back to S. A second reversal before S makes it periodic. Reaching T while
   retracing means an earlier prefix reached T. Otherwise, past S it's a new
   path from S with fewer reversals. So a path with reversals implies a
   reversal-free path from S to T in B that avoids every corner of B.
4. Parity. Unfold the reversal-free B path in the tiling. It becomes a
   segment from S to an A point `T*`. Write `T* - S = m p` with p primitive
   in L. Then `S + p/2` is a C point on the segment. Its fold image is a C
   point of B on the path. B is C-clean, so that point is a corner of B. That
   contradicts step 3.
5. Legs along a seam line. Within Q, a seam line meets Q only in the seam,
   which ends perpendicularly at the flat boundary through its endpoints. Such
   a leg bounces back and forth along the seam forever, so it never leaves.
   A path from S starts on `l1` only in the 2 directions that
   `mirror_exact` reports periodic.

So S and T are mutually dark. The proof uses machine checks for B C-clean,
the fold conditions, and simplicity of Q. The rest is the hand argument
above.

### Task 2: CEGAR for W <= 21

**Loop** (`phase2_cegar.py`). CP-SAT proposes a simple room with W <= 21,
S = (0,0) interior, a selected interior A point T, and at most K transparent
C points. `phase2_shoot.find_paths` searches A-lattice images of T in length
order, first to bound 12, then to bound 40. If it finds a legal path, the
loop adds a support cut for each of up to 6 paths. If it finds none, the
proposal is a dark candidate: the loop saves it, runs `mirror_exact`, and
adds an exact no-good.

**Cut soundness.** For a legal path, its support is computed as follows.
Each leg is split at every crossing with the 6 tiling line families. Every
tile that contains a crossing point or a sub-segment midpoint is "present".
At each reflection point, the tiles on the far side of the wall line are
"absent". The cut forbids T selected AND all present AND all absent. Each
open sub-segment lies inside one tile or one edge. So any room that contains
the present tiles holds a neighborhood of every non-reflection path point. A
room that also lacks the absent tiles has a flat wall at every reflection
point. The same path is then legal in that room, so a cut removes only lit
(room, T) pairs. P3 checks this with 399 exact sample points per leg, on
the 124 legal paths (317 reflections) among 200 random shots in an 11-wall
room with 39 transparent C points. `phase2-verify.json` records P1 to P4,
all PASS.

**Window lemma, transparent case** (hand proof, enumeration P1).

1. Turning: transparent C points turn 0. So `360 = 90 n1 - 90 n3 +
   sum(A,B turning)` still holds, and W <= 21 gives `n1 + 4 n3 <= 46`, so
   `n3 <= 11` (P2).
2. A star midpoint of an interior A point has 2 tiles (a cap: transparent,
   one A vertex), 3 (a 3-tile corner, spanning), or 4 (transparent,
   spanning). A non-star 2-tile flat C point can also span, if its tiles
   share the B vertex. Spanning edges therefore number at most
   `n3 + t - caps`. Non-star spanning edges number at most
   `n3 + t - 12 <= t - 1 <= K - 1 = e`.
3. Tile adjacency joins different C groups only through a shared A vertex.
   So the spanning edges form a connected graph that contains both stars.
4. Adjacent S, T are always lit, by the direct segment through their shared
   midpoint (P4). For D = hexdist(S,T) >= 2, connecting the stars needs a
   path of at least D - 2 extra edges, so D <= K + 1.
5. Ellipse: every A vertex v of the room obeys
   `d(S,v) + d(v,T) <= 2e + 6 - D`. Take v's shortest extra-edge path to
   the stars, of length a. If it's disjoint from the connecting path, of
   length c >= D - 2, then `a + c <= e` and the sum is at most
   `2a + D + 2 <= 2e + 6 - D`. If it first meets that path at u, then
   `d(S,u) + d(u,T) <= c + 2`, and the sum is at most `2e + 4 - D`.
6. Every tile whose A vertex obeys step 5 lies in the window, hex radius
   `2e + 7`. By the 12 symmetries of the tiling, T can be fixed in the
   30-degree wedge `0 <= j <= i`, so every interior A pair is covered.

P1 checks steps 4 and 5 by exhaustive enumeration for K = 2, 3, 4 (387,580
configurations at K = 4).

**Scope.** W <= 21, simple rooms, A pairs only, every T in the wedge with
`2 <= hexdist <= K + 1`. INFEASIBLE means that every proposal was lit by a
found path. So the shooter bound limits only candidate detection, not the
INFEASIBLE claims.

| K (max transparent) | Window | T tested | Result |
| --- | --- | --- | --- |
| 2 | hex 5 | (1,1) (2,0) (2,1) (3,0) | all INFEASIBLE, structural (0 cuts) |
| 3 | ellipse, hex 11, 300-684 tiles | 7 T, `hexdist` 2 to 4 | all INFEASIBLE: (1,1) after 12 iterations and 66 cuts, (2,0) after 13 iterations and 71 cuts, others structural |
| 4 | ellipse, hex 13, up to 960 tiles | (1,1) (2,0) (2,1) (2,2) only | all UNKNOWN at 1,700 s with 3 workers, no candidate: (1,1) 69 iterations and 350 cuts, (2,0) 52 and 304, (2,1) 2 and 6, (2,2) no first solve. (3,0) (3,1) (3,2) (4,0) (4,1) (5,0) not run |

A sanity run (K = 2, T = (2,0), W <= 26) exercised the loop: 36 iterations,
169 cuts, lit paths of up to 20 legs, no candidate (UNKNOWN at the budget).

### Tasks 3 and 4: candidates and doubts

No candidate with W <= 23 exists in either scope, so Task 4 had nothing to
re-verify. The only dark rooms found are fold rooms with W >= 43.

Open doubts:

- CP-SAT's INFEASIBLE and OPTIMAL claims are trusted. No proof logs exist.
- Cut soundness rests on the argument above plus P3's sampled check. A bug
  in `support` that drops a tile would make a cut too strong.
- The CEGAR proves only K <= 3. At K = 4, every run hit the 1,700 s budget.
  Every room those runs proposed was lit, but the search isn't exhaustive.
  Rooms with W <= 21 and 4 or more transparent C points are open. This gap
  matters: an F3 fold room has exactly 4 transparent C points, as does the
  22-wall square-tiling room. The window radius grows as `2K + 5`.
- The fold sweep's hex-5 window and `hexdist(S,T) <= 4` aren't proved
  sufficient. The fold-family statement for W <= 23 relies on the hand bound
  instead.
- The fold proof adapts the manuscript lemmas by hand. Nobody has reviewed
  the adaptation.
- Rooms with holes and pairs at non-A points remain out of scope.

## Commands

```sh
PY=.context/illumination-venv/bin/python   # has ortools; check/verify scripts need only python3
python3 verify_claims.py
python3 verify_lemmas.py
$PY search_relaxed.py --strict --window para --radius 3 --out strict-para3
$PY search_relaxed.py --radius 3 --seconds 1700 --out relaxed-para3
$PY search_relaxed.py --window hex --radius 6 --seconds 1700 --workers 12 --out relaxed-hex6
$PY search_relaxed.py --window hex --radius 6 --max-walls 26 --t-max-dist 4 --seconds 550 --workers 7 --out relaxed-hex6-le26-tdist4
python3 run_checks.py
python3 check_room.py <room.json> --bound 30
# phase 2
$PY phase2_verify.py                      # P1-P4 -> phase2-verify.json
python3 phase2_driver.py 3 3 1700 4       # CEGAR, K=3, every wedge T, ellipse window
python3 phase2_driver.py 4 1 1700 3       # CEGAR, K=4 (stopped after 4 T; partial)
python3 phase2_fold2_sweep.py 4 5         # direct F3 fold search, hexdist(S,T) <= 4, hex-5 window
$PY phase2_certify.py 40 43               # shooter, mirror_exact, fold conditions on fold rooms with W <= 43
```

Run each command from this directory.
