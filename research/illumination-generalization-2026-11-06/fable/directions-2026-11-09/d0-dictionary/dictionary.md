# D0: the dictionary between billiard paths and tuple chains

Fable subagent, 2026-11-09. Adversarial check of one statement. One author, no
second reader.

Status tags: **PROVED** (the argument is in this file), **CITED** (classical
fact, quoted from memory, not re-read in this session), **CHECKED BY
COMPUTATION** (with the bound).

## Result

D0 is true in both directions, for the precise statement in section 2.

| Direction | Verdict | Used by |
| --- | --- | --- |
| Room lit implies tuple LIT for some lift pair | **PROVED** | Theorem U for rooms, D1, every dark verdict that comes from a tuple orbit |
| Tuple LIT for some lift pair implies room lit | **PROVED** | D2, the room form of U\*, the "only if" half of the same-fibre conjecture |

No gap was found. The source files leave three points implicit. Section 2 fixes
them. None of them changes a downstream result.

1. **Lifts.** An interior point has two lifts. The room pair is lit exactly when
   at least one of the four lift pairs is LIT. Two of the four are enough:
   `(S+, T+)` and `(S+, T-)`.
2. **Chain.** A chain uses the 2-cycles of `g_a` and of one other entry `g_x`,
   in one state. A walk that changes `x` or changes state is not a straight
   segment.
3. **Directions.** The pure-braid orbit reaches every direction only because the
   decider reads all three arcs `a-b`, `a-c`, `a-d` in every state. With three
   arcs per state, no coset of the pure braid group needs separate treatment.

One correction applies outside the claimed scope. For marks on walls, the tuple
model also counts a segment that runs along a wall. Section 4.7 gives the
details. Interior marks are not affected.

Computation, exact integer arithmetic, no disagreement anywhere:

- All 30 strictly simple polyominoes of area at most 9 that hold a same-class
  interior pair, 30 pairs. Tuple model, a room decider written here, and d8's C
  decider all say lit, 30 of 30. Every witness replays in d8's reflection tracer.
- The 22-wall room is dark on both sides for all four lift pairs. The tuple
  orbit has 3,456 states and the room orbit has 5,184 states.
- Extended test, marks on flat wall points allowed: 1,426 polyominoes of area
  at most 8, 4,164 same-class pairs of regular points. Both sides say lit for
  4,144 and dark for 20.
- State-level test: 5,233,938 comparisons on those polyominoes, 0 mismatches.
  In every state and for each of the three arcs, the chain components equal the
  straight-segment components at the slope that the state's matrix names.

The interior-pair family is small and has no dark pair. The state-level test is
the strong evidence, because it compares complete component partitions.

## 1. Conventions

### 1.1 Room side

- `P` is a strictly simple orthogonal lattice polygon. It is a union of `n`
  unit cells `[i, i+1] x [j, j+1]`. It is edge-connected, has no hole, and has
  no pinch point.
- A lattice point of `P` touches 4 cells (interior), 2 adjacent cells (flat),
  1 cell (convex corner), or 3 cells (reflex corner). The vertices of `P` are
  the convex and reflex corners. Interior and flat points are **regular**.
- Fix an origin `o` in `Z^2`. The classes are `a = o + 2Z^2`, `b = a + (1,0)`,
  `c = a + (1,1)`, and `d = a + (0,1)`. For a pair `(S, T)`, take `o = S`.
- A billiard path reflects in the walls. At a flat lattice point it reflects in
  the wall through that point. A path is legal when it touches no vertex.
- The pair `(S, T)` is **lit** when a legal finite path joins `S` to `T`.

### 1.2 The double and the pillowcase

- `DP` is two copies `P+` (front) and `P-` (back) glued along the boundary. The
  reflection `iota` swaps the copies. An interior point `p` has two lifts `p+`
  and `p-`. A boundary point has one lift.
- Cone angles in `DP`: `2 pi` at interior points, flat points, and all
  non-lattice points. `pi` at convex corners (poles). `3 pi` at reflex corners
  (zeros).
- `B = R^2 / <2Z^2, -1>` with the origin at `o`. `B` is the double of the unit
  square. Its four corners are the images of the classes `a`, `b`, `c`, `d`.
  Call a cell `(i, j)` even when `i + j` has the parity of `o_x + o_y`.
- `pi : R^2 -> B` is the quotient map. It sends even cells to the front face
  and odd cells to the back face. `rho` is the reflection of `B` that swaps the
  faces and fixes the seam.
- `Pi : DP -> B` is `pi` on `P+` and `rho o pi` on `P-`. The two definitions
  agree on walls, because walls lie on lattice lines. `Pi` is a local isometry
  away from the corner fibres, and it has degree `n`.
- The base point `*` is the centre of the front face. The fibre over `*` is one
  point per cell: the front copy of each even cell and the back copy of each
  odd cell. So **sheets are cells**.

### 1.3 The tuple

- `kappa_V^e` sends a cell to its neighbour across the vertical edge whose
  x-coordinate is `e` mod 2 relative to `o`. If that edge is a wall,
  `kappa_V^e` fixes the cell. `kappa_H^f` is the same for horizontal edges.
- `r_ef` applies `kappa_V^e` first, then `kappa_H^f`.
- The tuple is `(g_a, g_b, g_c, g_d) = (r_00, r_10^-1, r_11, r_01^-1)`.
  Products apply the left factor first, and `g_a g_b g_c g_d = 1`.
- **Why the inverses (PROVED).** Lift a small counter-clockwise loop around a
  corner of `B`, with a straight tail from `*`. In the plane the lift is a half
  turn about a lattice point `p`. A wall on the way moves the lift to the other
  copy of the same cell. For the even cell north-east of a class-`a` point, the
  order "vertical edge, then horizontal edge" is counter-clockwise. The same
  holds at class `c`. At classes `b` and `d` that order is clockwise. The check
  for a reflex corner with cells NE, NW, SW gives the 3-cycle NE, SW, NW on both
  sides.
- The cycles of `g_x` are the points of `DP` over corner `x`. The cycle length
  is 1 at a convex corner, 2 at a regular point, and 3 at a reflex corner.
- **Lifts of a class-`a` point `p` (PROVED from the sheet rule).** If `p` is
  interior, `p+` is the 2-cycle {NE cell, SW cell} and `p-` is the 2-cycle
  {NW cell, SE cell}. If `p` is flat, its one lift is the 2-cycle of its two
  cells.

### 1.4 States, labels, chains

- A **state** is a tuple `(t_0, t_1, t_2, t_3)` together with a label on every
  2-cycle of `t_0`. States are taken up to simultaneous conjugation. The base
  state is the tuple of 1.3. Its labels are the regular class-`a` points of
  `DP`.
- The moves are `s_0^2`, `s_1^2`, and their inverses, with
  `s_i : (t_i, t_i+1) -> (t_i t_i+1 t_i^-1, t_i)`. When the entry at `a`
  becomes `k^-1 g k`, a labelled cycle `C` becomes `k(C)`. This is the rule of
  `hurwitz.py`.
- The state set is the orbit of the base state under these moves. This is the
  **pure-braid orbit**. The full braid orbit and the `SL(2,Z)` orbit of d8 are
  different objects. Section 4.3 compares them.
- A **chain at position `j`** (`j` = 1, 2, 3 for `x` = `b`, `c`, `d`) in a state
  is a sequence `A_0, X_1, A_1, ..., X_m, A_m`. Each `A_i` is a 2-cycle of
  `t_0`. Each `X_i` is a 2-cycle of `t_j`. Consecutive terms share a sheet, and
  no term repeats. The number `m >= 1` is the number of mirrors.
- A pair of labels is **LIT** when some state has a chain at some position
  from one label to the other. Otherwise the pair is DARK.

### 1.5 Slopes of a state

- Let `A2 = [[1, 2], [0, 1]]` and `B2 = [[1, 0], [-2, 1]]`, acting on column
  vectors `(p, q)`.
- A word `w = m_1 m_2 ... m_k` in the moves gets the matrix
  `M_w = M(m_1) M(m_2) ... M(m_k)`, with `M(s_0^2) = A2` and `M(s_1^2) = B2`.
- The three slopes of the state reached by `w` are `M_w (1,0)`, `M_w (1,1)`,
  and `M_w (0,1)`, for positions 1, 2, 3. They are defined up to sign. They
  form a Farey triangle, and their parities are `(1,0)`, `(1,1)`, `(0,1)`.

## 2. Statement

**Theorem D0.** Let `P` be a strictly simple orthogonal lattice polygon, and
let `S != T` be interior lattice points of class `a`.

1. **Room and double.** The pair is lit exactly when, for some signs `e` and
   `f`, a straight segment in `DP` joins `S^e` to `T^f` with no pole and no
   zero in its interior. The signs are equal exactly when the path has an even
   number of wall bounces.
2. **Double and tuple.** Let `sigma != tau` be regular points of `DP` over `a`.
   A straight segment with regular interior joins them exactly when the pair of
   labels is LIT.
3. **Explicit form.** A segment with developing vector `2m (p, q)`, `p` and `q`
   coprime, is a chain with `m` mirrors at position `j` in every state reached
   by a word `w` with `M_w e_j = +-(p, q)`. Such a word exists for every coprime
   `(p, q)`, and `j` is the position whose corner has the parity of `(p, q)`.
   Conversely, a chain with `m` mirrors at position `j` in the state of `w` is a
   segment with developing vector `+-2m M_w e_j`.
4. **Lifts.** `(S+, T+)` is LIT exactly when `(S-, T-)` is LIT, and `(S+, T-)`
   exactly when `(S-, T+)`. So the room pair is lit exactly when `(S+, T+)` or
   `(S+, T-)` is LIT.

**Abstract form D0-A.** Let `Q -> B'` be a finite connected cover of a
pillowcase, branched only over the corners. Give `Q` the pulled-back flat
metric. Let `sigma != tau` be 2-cycle points over corners `c_s` and `c_t`. A
straight segment with no point of cycle length other than 2 in its interior
joins them exactly when the following holds for some straight arc `alpha`. The
arc runs from `c_s` to a corner `x != c_s`, with `x = c_t` if `c_t != c_s`, and
`tau` lies in the component of `sigma` in the graph of lifts of `alpha` induced
on 2-cycle points. The genus and the other cycle lengths play no role.

Parts 2 and 3 are D0-A for `Q = DP`, plus the identification of straight arcs
with the arcs of the states.

## 3. Proof

### Step 1: room and double (part 1). PROVED

The fold `DP -> P` is the identity on each copy. It is a local isometry off the
seam, and near a seam point it is a reflection in the wall. So a geodesic of
`DP` that avoids the lifts of the vertices folds to a legal billiard path, and
a legal path from `S` lifts to a unique geodesic from each lift of `S`. A flat
lattice point is a regular seam point: the geodesic goes straight through, and
the path reflects. Each wall bounce crosses the seam once, which gives the
parity rule. Every point of `DP` other than a lift of a vertex has cone angle
`2 pi`.

### Step 2: a segment between corner points is a chain along one straight arc. PROVED

This step proves D0-A.

- Let `gamma` be a straight segment from `sigma` to `tau` with regular interior.
  Develop `Pi o gamma` into `R^2`, starting at a lattice point `v_0` of class
  `c_s`. Near a regular point over a corner, `Pi` is `z -> z^2`. So `Pi o gamma`
  runs into the corner and returns along the same segment. In `R^2` the point
  reflection `z -> 2v - z` identifies the return with the straight continuation.
  So `Pi o gamma` is the image of one straight segment `[v_0, w]` in `R^2`.
- `w` maps to a corner, so `w` is a lattice point. So `w - v_0 = k (p, q)` with
  `p`, `q` coprime and `k >= 1`. The direction is rational.
- The lattice points on the segment are `v_0 + i (p, q)`. Their classes
  alternate between `c_s` and `x = c_s + (p, q)` mod 2. So `k` is even when
  `c_t = c_s`, and `k` is odd with `c_t = x` otherwise.
- Let `alpha` be the image of `[v_0, v_0 + (p, q)]`. It is a simple arc from
  `c_s` to `x`, and its interior misses the corners. `gamma` is a concatenation
  of `k` lifts of `alpha`. The points between consecutive lifts are interior
  points of `gamma`, so they are regular. That is a path in the graph of lifts
  of `alpha` induced on regular points.
- Conversely, take a path without repeats in that graph. At a regular vertex
  the cone angle is `2 pi` and `Pi` is `z -> z^2`, so the two lifts of `alpha`
  at the vertex leave in opposite directions. The concatenation is straight.
  Its interior holds only regular vertices and points that lie over
  non-corner points of `B`.

### Step 3: the arcs of the states are the straight arcs. PROVED, with one classical input

- **Base state.** The tails of the base state are the straight segments from
  `*` to the four corners. The arc "tail to `a`, then tail to `x`" lies in the
  front face. It is isotopic to the straight arc of slope `(1,0)`, `(1,1)`, or
  `(0,1)` for `x` = `b`, `c`, `d`.
- **Graph of an arc.** In a state with tails `delta_0, ..., delta_3`, the lift
  of the arc `delta_0^-1 delta_j` through sheet `i` joins the cycle of `t_0`
  that contains `i` to the cycle of `t_j` that contains `i`. This graph depends
  only on the isotopy class of the arc relative to the corners. The end points
  of the lifts vary continuously in a discrete fibre, so they do not move.
- **Moves are twists (CITED, classical Hurwitz action).** The move `s_i^2`
  replaces a geometric basis by its image under the Dehn twist about the curve
  that encloses tails `i` and `i + 1`. The new tuple is the monodromy of the new
  basis. The label rule of 1.4 follows the points of the fibre over `a`: if the
  new tail to `a` is `w` followed by the old tail, the new cycle of a point is
  the set of sheets from which the lift of `w` ends in its old cycle.
- **Twists are shears.** In the base state, the curve around `a` and `b` is the
  core of the horizontal cylinder of `B`. That cylinder has circumference 2 and
  height 1. The shear `(x, y) -> (x + 2y, y)` descends to `B`, fixes each
  corner, and is one full twist of that cylinder. In the same way, the curve
  around `b` and `c` is the core of the vertical cylinder, and its twist is
  `(x, y) -> (x, y - 2x)`.
- **Induction.** Let `f_M` be the map of `B` induced by a matrix `M` congruent
  to the identity mod 2. It fixes each corner and sends the straight arc of
  slope `v` from `a` to the straight arc of slope `M v`. Suppose the basis of
  the state of `w` is `phi(E)`, with `E` the base basis and `phi` isotopic to
  `f_(M_w)` relative to the corners. The move `m` twists about the image under
  `phi` of a base curve. So the new basis is `phi(h(E))`, where `h` is the base
  twist, and `h` is isotopic to `f_(M(m))`. The new arcs are isotopic to the
  straight arcs of slope `M_w M(m) e_j`.
- **Signs.** The handedness of the two twists is fixed by computation: of the
  four sign choices, only `A2 = [[1,2],[0,1]]`, `B2 = [[1,0],[-2,1]]` passes the
  state-level test. Both twists have the same handedness, which matches the
  braid relation for `[[1,1],[0,1]]` and `[[1,0],[-1,1]]`. Parts 2 and 4 of the
  theorem do not depend on the signs.

### Step 4: every direction occurs (part 3). PROVED

Let `(p, q)` be coprime. Apply powers of `A2` and `B2`:

- If `|p| > |q| > 0`, replace `p` by `p - 2kq` with `|p - 2kq| <= |q|`.
- If `|q| > |p| > 0`, replace `q` by `q - 2kp` with `|q - 2kp| <= |p|`.
- Equality `|p| = |q|` forces `|p| = |q| = 1`, and one more step turns `(1, -1)`
  into `(1, 1)`.

The process ends at `+-(1,0)`, `+-(0,1)`, or `+-(1,1)`. So every coprime vector
is `+-M e_j` with `M` in the group generated by `A2` and `B2`. The position `j`
is the one whose corner has the parity of `(p, q)`, because the matrices are
the identity mod 2.

Steps 2 to 4 give parts 2 and 3.

### Step 5: lifts (part 4). PROVED

`iota` is an isometry of `DP`. It swaps the two lifts of every interior point
and maps straight segments with regular interior to segments of the same kind.
Apply part 2.

### What the proof cites

| Input | Status | Used in |
| --- | --- | --- |
| A Hurwitz move is the monodromy of the half-twisted basis | CITED, classical | Step 3 |
| Every simple arc between two corners of `B` is isotopic to a straight arc | CITED, standard for the four-punctured sphere | Only to equate "LIT" with the arc definition of `theory.md` section 0 |

The second fact is not needed for Theorem D0. It is needed in one place: the
definition of LIT in `theory.md` quantifies over all simple arcs. With the
fact, that definition equals the two definitions here. Without it, straight
arcs are still simple arcs, which is the inclusion that Theorem U needs.

## 4. Points that need care

### 4.1 Lattice points on the segment

A segment from a class-`a` point with developing vector `2m (p, q)` meets
lattice points exactly at the multiples of `(p, q)`. The odd multiples are the
mirrors `X_i`. The even multiples are the `A_i`. A regular point is transparent.
A pole or a zero ends the segment. Every vertex that a path touches is a lattice
point, so grazing a reflex corner is covered.

### 4.2 Parity of the direction

A direction with `(p, q)` congruent to `(1,0)`, `(1,1)`, or `(0,1)` mod 2 meets
classes `a` and `b`, `a` and `c`, or `a` and `d`. It never meets the other two
classes at a lattice point. So "x-lit" in d12 means "lit by a direction of
class `x`", with `b = a + (1,0)`, `c = a + (1,1)`, `d = a + (0,1)`.

### 4.3 Pure braids are enough

- The matrices of the pure moves are the identity mod 2. So one fixed position
  `j` reaches only one third of the directions.
- The decider reads positions 1, 2, and 3 in every state. Step 4 shows that
  this reaches every direction. You do not need to permute corner labels or to
  treat cosets of the pure braid group.
- A decider that read one position only needs the full braid group, with the
  position of `a` tracked. `check_orbit_invariance.py` in d6 reports that this
  scheme gives the same lit set.
- d8 uses a third model: the `SL(2,Z)` orbit of the 4-fold unfolding `X`, with
  one direction (horizontal) per state. All three models scan the same set of
  directions. Their state counts differ: 3,456 for the tuple model and 5,184
  for d8, on the 22-wall room.

### 4.4 Irrational slopes

Step 2 shows that the developing vector between two corner points is a lattice
vector. In room terms: unfold the path by reflections in lattice lines. The
reflections preserve `Z^2` and each parity class. So the unfolded end point is
a class-`a` lattice point, and the direction is rational.

### 4.5 Paths through `S` or `T` midway

A path may pass through `S` or `T` before it ends. Take the part from the last
visit to `S` to the next visit to `T`. It is a legal path with no mark in its
interior. On the tuple side, a chain may contain other lifts of `S` or `T` as
intermediate terms. The sub-chain between consecutive marks is a chain for some
lift pair. Part 4 quantifies over lift pairs, so both sides agree.

### 4.6 The two lifts

- An interior point has two lifts, with the cells of 1.3. A flat point has one.
- No lift pair can be fixed in advance. The proof gives no relation between
  `(S+, T+)` and `(S+, T-)`. The first means an even number of wall bounces.
- In the test family, all 30 interior pairs are LIT for both kinds. The
  22-wall room is DARK for both kinds. So the verdict-level test does not
  separate the two kinds. The state-level test does use the face labels: a
  slope joins `S+` and `S-` to different points. With the faces swapped, the
  22-wall room gives 3,602 mismatches (section 5.5).

### 4.7 Marks on walls: one correction

Part 2 holds for flat points. But a straight segment of `DP` can run along the
seam. In the room that is a path that slides along a wall. d8's `tracer.py`
rejects such a path. The tuple model and d8's orbit decider accept it.

- For interior marks this never happens. An axis-parallel path from an interior
  point runs along an interior edge. It can meet a wall only at a vertex or at a
  flat point of a perpendicular wall.
- For wall marks, read "lit" as "joined by a geodesic of `DP`". In the test
  family, no pair is lit only by a sliding segment (0 pairs where the Python
  room decider ran).

## 5. Computation

Scripts: `d0lib.py`, `run_census.py`, `room22.py`. Exact integers only.

### 5.1 What each test compares

| Tag | Side | Method | Code |
| --- | --- | --- | --- |
| T | Tuple | Marked pure-braid orbit, three arcs per state | `d0lib.tuple_orbit`, on the primitives of `hurwitz.py` |
| R | Room | `SL(2,Z)` orbit of the unfolding `X`, written here | `d0lib.room_orbit` |
| C | Room | d8's `orbit.c`, read and compiled here, fed with the unfolding built here | `orbit_d8` |
| S | State level | Chain components against straight-segment components at slope `M_w e_j` | `d0lib.state_check`, `d0lib.geo_components` |
| W | Witness | Every interior witness, from T through the slope and from R, replayed by d8's reflection tracer | `run_census.replay` |

- The tuple is built from 1.3 with no shared code. It equals the tuple of
  `d10-mechanisms/roomtools.py` on the 22-wall room.
- T also equals `hurwitz.marked_orbit` on the 22-wall room.
- R and C share the method and no code. Their state counts agree on every room
  where both ran.
- S walks straight lines in `X`. It uses no orbit and no braid move on the room
  side. S skips a slope when `|p| + |q| > 400`.

### 5.2 The statement itself: interior pairs, area at most 9

`python3 -B run_census.py 9 2 interior 1 3000000`

| Quantity | Count |
| --- | --- |
| Fixed polyominoes, area 1 to 9 | 13,702 |
| Strictly simple with a same-class interior pair | 30 (2 of area 8, 28 of area 9) |
| Same-class interior pairs | 30 |
| T lit, R lit, C lit | 30, 30, 30 |
| Disagreements | 0 |
| LIT for `(S+, T+)` and for `(S+, T-)` | 30 and 30 |
| `iota` symmetry failures | 0 |
| Witness replays that fail | 0 |
| State-level comparisons, all four classes of the 30 rooms | 193,714 with 0 mismatches |

The 30 rooms are the 2 x 4 rectangle, the rectangle plus one cell, and two
2 x 2 blocks joined by one cell, in every orientation.

Example of part 3. Take the blocks `[0,2]^2` and `[2,4]^2` joined by the cell
`(1,2)`, with `S = (1,1)` and `T = (3,3)`. The tuple witness is a chain with 2
mirrors at position 1 (corner `b`) in a state at word length 2. Its slope is
`+-(3, 2)`, so the developing vector is `+-(12, 8)`. The tracer confirms a
legal path with that vector.

### 5.3 The 22-wall room

`python3 -B room22.py`

| Quantity | Value |
| --- | --- |
| Area, regular points | 15 cells. 8 regular points: `S`, `T` interior, 6 flat. |
| Cycle types `a`, `b`, `c`, `d` | `[2^6,1^3]`, `[3^3,2^2,1^2]`, `[3^3,1^6]`, `[3^3,2^2,1^2]` |
| Tuple orbit, class of `S` | 3,456 states, as in d6 |
| Room orbit | 5,184 states, as in d8. R and C agree. |
| `(S+,T+)`, `(S+,T-)`, `(S-,T+)`, `(S-,T-)` | DARK on the tuple side and dark on the room side, all four |
| DP pairs of class `a` | 15 pairs: 6 LIT, 9 DARK. The LIT set is the same on both sides. |
| All classes | 17 DP pairs: 8 lit, 9 dark, 0 disagreements. 8 room pairs: 4 lit, 4 dark. |
| State-level comparisons | 9,424 with 0 mismatches. 1,520 skipped for large slope. |

The four dark room pairs are `S`-`T`, `S`-(3,1), (5,3)-`T`, and (5,3)-(3,1).
They equal the dark set of the record. The 6 LIT pairs of class `a` are
`S+`-`S-`, `T+`-`T-`, `S+`-(5,3), `S-`-(5,3), `T+`-(3,1), and `T-`-(3,1).

### 5.4 Extended test: flat wall points as marks

The proof of part 2 does not use that the marks are interior. So the same
polygons give a larger test. Every regular point of one class is a mark, in all
four classes. A DP pair is a pair of regular points of `DP` over one class.

`python3 -B run_census.py 7 2 fixed 1 1000000` and
`python3 -B run_census.py 8 2 free 8 60000`

"Fixed" means every orientation. "Free" means one polyomino per symmetry class.

| Area | Rooms | Room pairs | T lit | C lit | Dark on both | Disagreements |
| --- | --- | --- | --- | --- | --- | --- |
| 1 to 4, fixed | 28 | 14 | 14 | 14 | 0 | 0 |
| 5, fixed | 63 | 88 | 76 | 76 | 12 | 0 |
| 6, fixed | 216 | 436 | 436 | 436 | 0 | 0 |
| 7, fixed | 756 | 2,184 | 2,184 | 2,184 | 0 | 0 |
| 8, free | 363 | 1,442 | 1,434 | 1,434 | 8 | 0 |
| Total | 1,426 | 4,164 | 4,144 | 4,144 | 20 | 0 |

- R ran on 1,311 of the 1,426 rooms: every room of area at most 7 that has a
  regular point, and the 250 rooms of area 8 with at most 60,000 states. On
  those rooms the comparison is at the level of DP points: 4,190 DP pairs,
  4,169 lit and 21 dark on both sides, 0 disagreements.
- State level: 1,249,845 comparisons for area at most 7 and 3,984,093 for
  area 8. 0 mismatches. 1,418,298 comparisons were skipped for large slope.
- Orbit sizes: 2,217,412 tuple states and 26,051,622 room states in total.
- The four area-7 polyominoes with a hole are excluded. So are the 6 free
  octominoes with a hole.

Area 9, free, was started and stopped by the author after 200 of 1,248 rooms,
because the full run needs about 65 minutes. The log `log_n9_free_partial.txt`
holds the partial counts: 1,716 room pairs, all lit on T and on C, and
3,857,044 state-level comparisons with 0 mismatches. No summary file exists
for that run. Treat it as partial evidence only.

### 5.5 Negative controls

`python3 -B controls.py 6`. Family: the 307 fixed polyominoes of area at most 6
(451 class instances) and the 22-wall room (3 instances).

| Broken convention | Polyominoes | 22-wall room |
| --- | --- | --- |
| None | 0 mismatches in 78,225 comparisons | 0 in 9,424 |
| Signs `(+2, +2)` in `A2`, `B2` | 386 instances fail | 3 of 3 fail |
| Signs `(-2, -2)` | 386 instances fail | 3 of 3 fail |
| Signs `(-2, +2)` | 324 instances fail | 1 of 3 fails |
| Front lift = {NW, SE} | 8 instances fail (the ones with an interior point) | 1 of 3 fails, 3,602 mismatches |
| No inverses at `b` and `d` | Product is not 1 in 376 instances | 3 of 3 |
| Read position 1 only | 125 of 591 LIT pairs are lost | 1 of 8 |
| Let a walk change corner inside a state | 0 of 12 DARK pairs turn lit | 0 of 9 |

So the signs, the face rule, the inverses, and the three arcs are each tested.
The single-corner rule for chains is not exercised by this family. It rests on
Step 2.

## 6. Which result needs which direction

"Segment" means a straight segment with regular interior.

| Result | Needs | Direction |
| --- | --- | --- |
| Theorem U, abstract, base `B` | Nothing. DARK is defined by arcs. | None |
| Census verdicts read as arc verdicts (U\* tables, 0 of 12,425) | Steps 3 and 4 plus the second cited fact | Tuple and arc, both ways |
| Lemma 0, so G1 and G7 | D0-A over `B` and over `P'` | Both ways, abstract |
| Theorem U for rooms, D1 | Parts 1 and 2 | Room lit implies LIT |
| d6 validation: 22-wall room DARK for all four lifts | Parts 1, 2, 4 | Room lit implies LIT |
| D2, room form of U\*, "only if" of the same-fibre conjecture | Parts 1, 2, 4 | LIT implies room lit |
| d12 Lemma C, Proposition N | D0-A | Segment implies chain |
| d12 "x-lit" read as "lit in a direction of class x" | Part 3 and 4.2 | Both ways |
| d10 section 3.6, d8 verdicts against certificates | Parts 1, 2, 4 | Both ways |

Lemma 0 is now a corollary. Both light rules describe the segments of `Q`, and
the flat metric of `Q` is the same over `B` and over `P'`. One caveat: over
`P'` the marks can lie over two different corners, so the chain ends at an
`x`-vertex. D0-A covers that case. `hurwitz.py` does not implement it.

## 7. Convention mismatches between the files

None of these breaks a proof. Each can mislead a reader.

| Topic | File and convention | Other file and convention |
| --- | --- | --- |
| Class names | d8 `room.cls`, d4: `A`, `C1`, `B`, `C2` for offsets (0,0), (1,0), (1,1), (0,1) | d6, d10, d12: `a`, `b`, `c`, `d` for the same offsets. d8's `B` is corner `c`. |
| Orientation | d4 generators at `C1` and `C2` are clockwise | The tuple uses their inverses. Cycle types and block systems are the same. Hurwitz moves are not. |
| `k` | d8 README: transparent room points outside class A | d6, `roomtools.ledger`: 2-cycles of `g_b`, `g_c`, `g_d`. An interior point counts twice. Both give 4 on the 22-wall room, because its four transparent points are flat. |
| Lattice scale | d12 Proposition N: `a`-points on `Z^2`, other corners on half-lattice points | Rooms, d8, d10: all corners on `Z^2`, `a = o + 2Z^2` |
| "State" | d6, d12: tuple with labels, three directions | d8: one shear image of `X`, one direction. d4: cylinder states. Counts for the 22-wall room: 3,456, 5,184, 10,368. |
| "Lit" on walls | d8 `orbit.c` accepts a segment along a wall | d8 `tracer.py` rejects it. See 4.7. |
| 22-wall coordinates | d8: marks (0,0), (2,2) | Task and record: (1,3), (3,5). The shift is (1,3). |
| Regular points of the 22-wall room | d8 README, V1: "Two of the 8 regular points lie on flat walls" | d8's own cells: six are flat and two are interior (the marks). The README sentence is wrong. V2 therefore started rays at the two marks only. |
| "Degree" | Coordinator log: "k = 4, degree 3" for the 22-wall factor | The factor has degree 5. The 3 is the block size. |
| Lift choice | d8 `nmin.py`: separates when no lift of `p` meets a lift of `q` | d10 section 3: dark when all four lift pairs are dark. Consistent with part 4. |

## 8. Limits

- One author. The proof has no second reader.
- The Hurwitz-action fact and the arc classification are quoted from memory.
- The interior-pair family has 30 pairs, all lit. Its only dark control is the
  22-wall room. The dark side of the verdict-level test rests on wall marks.
- No room in the family has an interior pair that is LIT for one kind of lift
  pair and DARK for the other. That case is covered by proof only.
- The state-level test skips slopes with `|p| + |q| > 400`.
- The extended test stops at area 8. The area-9 run is partial.
- The tuple witnesses are not shortest. Some pass through `S` or `T` midway,
  as in 4.5. The reflection tracer accepts them.
- D0-A for marks over two different corners is proved and not tested.
- Polygons with a pinch point or a hole are outside the statement.

## 9. Files

| File | Purpose |
| --- | --- |
| `dictionary.md` | This file |
| `d0lib.py` | Rooms, the tuple, the unfolding, both deciders, the state-level check |
| `run_census.py` | The tests of section 5 |
| `room22.py`, `room22.json` | The 22-wall room |
| `controls.py`, `controls.json` | Negative controls |
| `orbit_d8` | d8's `orbit.c`, compiled here without change |
| `census_n1-9_interior.json` | Section 5.2, with every pair and witness |
| `census_n1-7_fixed.json`, `census_n8-8_free.json` | Section 5.4 |
| `log_n9_free_partial.txt` | The stopped area-9 run |
| `log_*.txt` | Run logs |

Reproduce, from this directory, at most 2 worker processes:

```sh
cc -O2 -o orbit_d8 ../d8-perturbation-test/orbit.c
python3 -B run_census.py 9 2 interior 1 3000000   # about 7 minutes
python3 -B room22.py                              # under 1 minute
python3 -B run_census.py 7 2 fixed 1 1000000      # about 2 minutes
python3 -B run_census.py 8 2 free 8 60000         # about 5 minutes
python3 -B controls.py 6                          # under 1 minute
python3 -B run_census.py 9 2 free 9 60000 3000    # optional, about 65 minutes
```
