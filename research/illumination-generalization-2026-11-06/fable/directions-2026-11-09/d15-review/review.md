# Adversarial review of the r <= 2 illumination theorem

Date: 2026-11-10. Direction d15, second reader.

Review target: `../d15-small-r/theorems.md` (Lemmas A, A2, B, B', B2, C, D and
Theorems 0, 1, 2), `../d15-small-r/lemmas.py`, and the certificate data for
r <= 2. The r = 3 and r = 4 results are out of scope.

## Verdict

The theorem holds. This review found no gap in the proof and no
counterexample.

> Let P be a strictly simple orthogonal polygon with real vertex coordinates
> and at most 2 reflex corners, so at most 8 walls. Then a billiard path that
> touches no vertex joins every two distinct interior points of P.

Two written statements need a correction. Neither correction changes the
theorem.

| Item | Verdict | Note |
| --- | --- | --- |
| Lemma A | CONFIRMED | The proof omits one step. See [Lemma A](#lemma-a). |
| Lemma A2 | CONFIRMED | |
| Lemma B | CONFIRMED | |
| Lemma B' | CONFIRMED | No certificate uses it. Lemma D uses it. |
| Lemma B2 | CONFIRMED | "At least one sign" is sharp. One sentence of the statement is loose. See [Lemma B2](#lemma-b2). |
| Lemma C, par form | CONFIRMED | |
| Lemma C, perp form | CONFIRMED | |
| Lemma C, same form | CONFIRMED WITH CORRECTION | False as written when one corridor serves as both arms. See [The most serious problem](#the-most-serious-problem). |
| Lemma D | CONFIRMED | No certificate at r <= 2 uses it. |
| Theorem 0 | CONFIRMED WITH CORRECTION | The correction is to the Setting. See [Setting](#setting). |
| Theorem 1 | CONFIRMED WITH CORRECTION | Same correction to the Setting. The hand proof is complete. |
| Theorem 2 | CONFIRMED WITH CORRECTION | Same correction to the Setting. The proof is computer-assisted. This review reproduced all 543 certificates with separate code. |

Corrected statements:

- **Setting.** A room P is a strictly simple orthogonal polygon with real
  vertex coordinates. Theorems 0, 1, and 2 hold in that setting.
- **Lemma C, same form.** The doors are on the same side of G and belong to
  two different corridors. Their flat ends are the two corners of that side.
  The opposite side of G lies entirely in the boundary of P.

## The most serious problem

Lemma C, same form, is false as written in one degenerate reading. The
problem doesn't affect Theorem 2.

- **What is wrong.** The lemma asks for "different arms of the same hub". An
  arm includes its flat end. So one corridor whose door is a whole side of G,
  with both door ends flat, counts as two different arms. The proof then uses
  `w1 + w2 < H`. In that reading `w1 = w2 = H`, so the step fails.
- **Explicit failure.** Room: the rectangle [-1, 1] x [0, 1]. Hub
  G = [0, 1] x [0, 1]. The corridor is [-1, 0] x [0, 1]. S = (-1/10, 33/100)
  and T = (-1/5, 9/25). For the sign pair (-1, +1), exactly one pair (k1, k2)
  meets both window conditions. Its segment passes through the corner (1, 0).
  So no valid path of that sign pair exists, and the statement "for every pair
  of signs" fails.
- **Output of `c_same_degenerate.py`:**

  ```
  signs (+1, +1): window solutions [(0, 0, 'a=381/1150', 'b=411/1150', 'x=L at 198/575', 'ok')]
  signs (+1, -1): window solutions [(0, 0, 'a=89/230', 'b=351/230', 'x=L at 22/23', 'ok')]
  signs (-1, +1): window solutions [(0, 0, 'a=-3/10', 'b=3/10', 'x=L at 0', 'vertex')]
  signs (-1, -1): window solutions [(0, 0, 'a=-281/1150', 'b=1689/1150', 'x=L at 352/575', 'ok')]
  ```

- **`lemmas.py` doesn't exclude the reading.** `lemma_C` skips a pair of arm
  objects only when side, F, and E all agree. One corridor with F and E
  swapped passes that test.
- **Why Theorem 2 is safe.** In that reading S and T lie in one corridor, so
  they lie in a common rectangle. `certify_pair` tries Lemma A first. Lemma A
  refuses only when both points lie on the far end line with a vertex between
  them. Then Lemma A2 applies, with the wall opposite to the door. So the
  search never reaches Lemma C for such a pair.
- **Scan.** `scan_same_corridor.py` finds no such certificate. The counts are
  0 of 4 same-form certificates at r = 2, 0 of 200 at r = 3, and 0 of 8,227
  at r = 4.
- **The pair in the example is lit.** Lemma A lights it. Only the internal
  claim of Lemma C fails.

To fix the lemma, add "two different corridors" to the same form. To fix the
code, also skip a pair of arm objects that share a door.

## Other corrections and notes

### Setting

The Setting of `theorems.md` defines a room with integer vertex coordinates.
The Results section and the section on metric-free certificates claim real
edge lengths. No lemma proof uses an integer coordinate, so the claim of real
lengths is correct. Change the Setting to real vertex coordinates.

### Lemma A

The statement is correct. The proof stops at "the open segment misses the
boundary of Q, or it lies in one side of Q". In the second case, the proof
doesn't say why the segment can't run along a wall of P.

The missing step: suppose that a point of the open segment is a wall point
but not a vertex. The wall through that point is parallel to the segment.
A perpendicular wall would enter the interior of Q. Follow the wall toward S.
S is interior, so the wall ends before S, at a vertex on the open segment.
That contradicts the hypothesis. So every point of the segment is interior.

### Lemma B2

- The statement says that the path first reflects in the side opposite to the
  door. In the case `-w < y* < 0` with `x° < L`, the path reflects in the floor
  first. The proof handles that case correctly. Only the sentence is loose.
- "At least one sign" can't be improved to "both signs". The attack found
  2,387 instances at r = 2 where exactly one sign has a valid path.
- The corner case behaves as the proof says. All 3,427 corner-case candidates
  met the vertex, and no other window candidate was invalid.

### Lemma B

The door of Lemma B needn't lie on a grid line. `lemmas.py` uses grid-line
doors only. That restriction is sufficient for r <= 2.

### Tests in theorems.md

The tests in `theorems.md` use lattice points and integer lengths, and the
document says so. This review adds tests with irrational lengths and
non-lattice points. See [Numerical attack](#numerical-attack).

## Combinatorial types

`enum_check.py` enumerates the types with a different method from
`enum_types.c` and `check_types.py`. Those two programs enumerate cell sets.
`enum_check.py` enumerates closed walks of alternating horizontal and vertical
edges on the grid {0, ..., r + 1}^2 and keeps the strictly simple ones. It then
replaces coordinates with ranks and reduces by the 8 symmetries.

| r | Types, this review | Types, author | Missed | Position-type pairs, both counts |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 0 | 15 |
| 2 | 8 | 8 | 0 | 543 |

- **No type is missing.** The two lists are identical for r = 0, 1, 2.
- **Degenerate coincidences are covered.** The walk enumeration allows equal
  coordinates of different walls. The three types on a 2 x 3 grid are those
  cases. They are the aligned Z, the T with its tab on a grid line, and the U
  with equal prongs.
- **Classes by boundary order.** Count the edges between the two reflex
  corners along the boundary. The 8 types split into 4 classes:
  - 2 U shapes, with 1 and 7 edges
  - 1 staircase, with 2 and 6 edges
  - 2 T shapes, with 3 and 5 edges
  - 3 Z shapes, with 4 and 4 edges
- **Position types are complete.** Each coordinate of a real point is on a
  grid line or strictly between two neighboring grid lines. The doubled index
  covers both cases. An interior point on a grid line or on a grid point has
  all neighboring cells in P, and the `interior` test checks that.
- **Pairs of equal position type.** `certify_type` assigns Lemma A without a
  search. That is correct. Two points of one type lie in one cell, or on one
  open grid edge between two cells of P. No grid point lies between them.

## Proof check

Each proof was read for real points and real lengths. The following list
gives the attacks that were tried on each lemma.

- **Lemma A.** Points on a side of Q, on a grid line, and collinear with a
  vertex. A vertex on the open segment forces an axis-parallel segment in a
  side of Q. For the missing step, see [Lemma A](#lemma-a).
- **Lemma A2.** S and T are corners of R, and M is the midpoint of the
  opposite side. M is never a vertex. Nothing depends on a length ratio.
- **Lemma B.** The window (p - w, p + w) is open and has length 2w. The step is
  2w lambda with 0 < lambda < 1, so the window holds a value for every real
  lambda. The three cases cover the window. Checked limits: S on the bottom
  side of Q*, T on the far end, x* = p, a vertical segment, and s1 > q.
- **Lemma B'.** For lambda = 1/2 the two progressions differ by t1 - p modulo
  w. That number isn't a multiple of w, so at most one sign meets p.
- **Lemma B2.** Checked limits: S on a side of G or on the door line, a
  horizontal segment through S, and w = H. The two signs give
  progressions that differ by 2 lambda t, which isn't a multiple of
  2 lambda w. So at most one sign has the corner value in its window.
- **Lemma C, par form.** Phi is strictly decreasing between jumps,
  right-continuous, and jumps upward only. The infimum argument gives a zero
  at a point of continuity, so both crossings lie in the open windows. In the
  hub, |a - f1| < w1 <= H and |b - f2| < w2 <= H. So each crossing is a
  relative interior point of a mirror side, or a flat end.
- **Lemma C, perp form.** The configuration is forced as the proof says. F
  is negative near 0 because a tends to a value less than w1 <= H. F is positive
  for large kappa because b tends to a positive constant. The jumps of b
  accumulate only at kappa = 0. The corner (L, 0) needs (-a)(b - L) = L H,
  and the product is smaller.
- **Lemma C, same form.** With two different corridors, w1 + w2 < H holds.
  The crossing of x = L is then strictly inside (0, H).
- **Lemma D.** The three cases cover all positions. The third case gives a
  straight segment through both doors.
- **Theorem 1.** The case split covers every pair. A convex corner can't lie
  on an open segment between interior points. The reflex vertex is excluded as
  the proof says.

Each lemma uses only the following about the points: which side of a grid
line a point lies on, and that the point is interior. No step uses a rational
ratio.

## Certificates and lemmas.py

### Coverage

`certs.py` rebuilds every certificate with separate code. For each of the 559
position-type pairs with r <= 2, it does the following:

1. It asks `lemmas.py` for the certificate.
2. It finds every lemma instance from the geometry, with code written from the
   lemma statements (`rv.py`).
3. It requires that the certificate names one of those instances: same lemma,
   same door, same flat end, same roles.
4. It traces the prescribed paths of every instance in a room with unit gaps.

Result: 0 problems. Every pair has a certificate, and each certificate matches
an instance. The counts per lemma equal the table in `theorems.md`.

| Lemma | A | A2 | B | B2 | C par | C perp | C same | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Certificates, r <= 2 | 478 | 2 | 65 | 6 | 3 | 1 | 4 | 559 |

The run traced 1,766 instances. By lemma: A 478, A2 124, B 327, B' 224,
B2 481, C 64, D 68. `certs_dump.txt` lists every pair with its
certificate.

### Code reading

Each test in `lemmas.py` implies the lemma hypothesis for every real point of
the position type.

- **`lemma_A`.** The cell hull of the two types is the smallest candidate
  rectangle. The vertex test covers every grid point strictly between two
  types on one grid line. A wall point between them implies a vertex between
  them, so the test is sufficient.
- **`lemma_A2`.** The code checks the cell hull between the line and the wall,
  and the wall over the whole hull. Both are supersets of the lemma's
  rectangle and side.
- **`_lemma_B_canon`.** The corridor rows are checked one by one with both
  side walls. Q* and the flat end are checked on the cell hull of the viewer.
  The strict inequalities on doubled indices imply the strict inequalities of
  hypotheses 2 and 3.
- **`arm_objects`.** The corridor has both walls in every column. The floor of
  the hub is wall over the whole hub side, so the flat end is a straight wall
  point. The arm point is strictly between the walls and off the door line.
- **`lemma_B2` and `lemma_C`.** The viewer test uses the closed hub. The
  opposite side is checked over the whole hub side. For the one missing
  exclusion, see [The most serious problem](#the-most-serious-problem).

### Hand-checked certificates

60 certificates were checked by hand against the shapes. They are 16 of A,
both of A2, 28 of B, all 6 of B2, and all 8 of C. Each one satisfies the hypotheses of its
lemma for every room of the type.

Shapes list rows from top to bottom. Points use doubled index coordinates.
Lines use grid indices. In the eight collinear A rows, the grid point between
the two types is an interior grid point, not a vertex.

| Shape | S | T | Lemma | Objects |
| --- | --- | --- | --- | --- |
| `#./##` | (1, 3) | (3, 1) | B | viewer S; corridor between y = 0 (flat end) and y = 1; door on x = 1 |
| `#./##` | (1, 1) | (3, 1) | A | common rectangle |
| `#./##` | (1, 2) | (2, 1) | A | common rectangle |
| `#./##/.#` | (1, 3) | (3, 1) | B | viewer S; corridor between x = 2 (flat end) and x = 1; door on y = 1 |
| `#./##/.#` | (1, 4) | (3, 1) | B | viewer S; corridor between x = 2 (flat end) and x = 1; door on y = 1 |
| `#./##/.#` | (1, 5) | (3, 1) | C par | arm of S: door on y = 2 from x = 0 (flat end) to x = 1; arm of T: door on y = 1 from x = 2 (flat end) to x = 1 |
| `#./##/.#` | (1, 5) | (3, 2) | B | viewer T; corridor between x = 0 (flat end) and x = 1; door on y = 2 |
| `#./##/.#` | (1, 5) | (3, 3) | B | viewer T; corridor between x = 0 (flat end) and x = 1; door on y = 2 |
| `#./##/#.` | (1, 1) | (3, 3) | B | viewer T; corridor between x = 0 (flat end) and x = 1; door on y = 1 |
| `#./##/#.` | (1, 5) | (3, 3) | B | viewer T; corridor between x = 0 (flat end) and x = 1; door on y = 2 |
| `##/#./##` | (1, 1) | (3, 5) | B | viewer S; corridor between y = 3 (flat end) and y = 2; door on x = 1 |
| `##/#./##` | (2, 1) | (2, 5) | A2 | wall on line x = 0 |
| `##/#./##` | (2, 1) | (3, 5) | B2 | viewer S; door on x = 1 from y = 3 (flat end) to y = 2; wall x = 0 |
| `##/#./##` | (2, 5) | (3, 1) | B2 | viewer S; door on x = 1 from y = 0 (flat end) to y = 1; wall x = 0 |
| `##/#./##` | (3, 1) | (3, 5) | C same | arm of S: door on x = 1 from y = 0 (flat end) to y = 1; arm of T: door on x = 1 from y = 3 (flat end) to y = 2; wall x = 0 |
| `##/#./##` | (1, 2) | (3, 5) | B | viewer S; corridor between y = 3 (flat end) and y = 2; door on x = 1 |
| `##/#./##` | (1, 3) | (3, 1) | B | viewer S; corridor between y = 0 (flat end) and y = 1; door on x = 1 |
| `##/#./##` | (1, 1) | (1, 5) | A | common rectangle |
| `##/#./##` | (1, 5) | (2, 1) | A | common rectangle |
| `#../###/..#` | (1, 5) | (5, 1) | C par | arm of S: door on y = 2 from x = 0 (flat end) to x = 1; arm of T: door on y = 1 from x = 3 (flat end) to x = 2 |
| `#../###/..#` | (1, 3) | (5, 1) | B | viewer S; corridor between x = 3 (flat end) and x = 2; door on y = 1 |
| `#../###/..#` | (1, 5) | (3, 3) | B | viewer S; corridor between y = 1 (flat end) and y = 2; door on x = 1 |
| `#../###/..#` | (1, 5) | (5, 2) | B | viewer T; corridor between x = 0 (flat end) and x = 1; door on y = 2 |
| `#../###/..#` | (2, 3) | (5, 1) | B | viewer S; corridor between x = 3 (flat end) and x = 2; door on y = 1 |
| `#../###/..#` | (1, 3) | (5, 3) | A | common rectangle |
| `##./###/.##` | (1, 5) | (5, 1) | C par | arm of S: door on x = 1 from y = 3 (flat end) to y = 1; arm of T: door on x = 2 from y = 0 (flat end) to y = 2 |
| `##./###/.##` | (1, 3) | (5, 1) | B | viewer S; corridor between x = 3 (flat end) and x = 1; door on y = 1 |
| `##./###/.##` | (1, 5) | (3, 1) | B | viewer T; corridor between y = 3 (flat end) and y = 1; door on x = 1 |
| `##./###/.##` | (1, 5) | (5, 2) | B | viewer T; corridor between x = 0 (flat end) and x = 2; door on y = 2 |
| `##./###/.##` | (2, 5) | (5, 1) | B | viewer S; corridor between y = 0 (flat end) and y = 2; door on x = 2 |
| `##./###/.##` | (3, 5) | (5, 3) | B | viewer S; corridor between y = 0 (flat end) and y = 2; door on x = 2 |
| `##./###/.##` | (1, 4) | (3, 4) | A | common rectangle; collinear |
| `##./###/.##` | (2, 3) | (2, 5) | A | common rectangle; collinear |
| `##./###/.##` | (3, 2) | (5, 2) | A | common rectangle; collinear |
| `##./###/.##` | (4, 1) | (4, 3) | A | common rectangle; collinear |
| `##./###/.##` | (2, 4) | (3, 4) | A | common rectangle; S is an interior grid point |
| `##./###/.##` | (1, 5) | (3, 3) | A | common rectangle |
| `#../###/##.` | (1, 1) | (5, 3) | B | viewer T; corridor between x = 0 (flat end) and x = 2; door on y = 1 |
| `#../###/##.` | (1, 5) | (3, 1) | B | viewer S; corridor between y = 0 (flat end) and y = 2; door on x = 1 |
| `#../###/##.` | (1, 5) | (5, 3) | B | viewer T; corridor between x = 0 (flat end) and x = 1; door on y = 2 |
| `#../###/##.` | (2, 1) | (5, 3) | B | viewer S; corridor between y = 2 (flat end) and y = 1; door on x = 2 |
| `#../###/##.` | (1, 2) | (3, 2) | A | common rectangle; collinear |
| `#../###/##.` | (2, 1) | (2, 3) | A | common rectangle; collinear |
| `#../#.#/###` | (1, 2) | (5, 2) | A2 | wall on line y = 0 |
| `#../#.#/###` | (1, 2) | (5, 3) | B2 | viewer S; door on y = 1 from x = 3 (flat end) to x = 2; wall y = 0 |
| `#../#.#/###` | (1, 3) | (5, 2) | B2 | viewer T; door on y = 1 from x = 0 (flat end) to x = 1; wall y = 0 |
| `#../#.#/###` | (1, 4) | (5, 2) | B2 | viewer T; door on y = 1 from x = 0 (flat end) to x = 1; wall y = 0 |
| `#../#.#/###` | (1, 5) | (5, 2) | B2 | viewer T; door on y = 1 from x = 0 (flat end) to x = 1; wall y = 0 |
| `#../#.#/###` | (1, 3) | (5, 3) | C same | arm of S: door on y = 1 from x = 0 (flat end) to x = 1; arm of T: door on y = 1 from x = 3 (flat end) to x = 2; wall y = 0 |
| `#../#.#/###` | (1, 4) | (5, 3) | C same | same objects as the preceding row |
| `#../#.#/###` | (1, 5) | (5, 3) | C same | same objects as the preceding row |
| `#../#.#/###` | (1, 1) | (5, 3) | B | viewer S; corridor between x = 3 (flat end) and x = 2; door on y = 1 |
| `#../#.#/###` | (1, 3) | (5, 1) | B | viewer T; corridor between x = 0 (flat end) and x = 1; door on y = 1 |
| `#../##./###` | (1, 5) | (5, 1) | C perp | arm of S: door on y = 2 from x = 0 (flat end) to x = 1; arm of T: door on x = 2 from y = 0 (flat end) to y = 1 |
| `#../##./###` | (1, 3) | (5, 1) | B | viewer S; corridor between y = 0 (flat end) and y = 1; door on x = 2 |
| `#../##./###` | (1, 5) | (3, 1) | B | viewer S; corridor between y = 0 (flat end) and y = 2; door on x = 1 |
| `#../##./###` | (1, 5) | (4, 1) | B | viewer S; corridor between y = 0 (flat end) and y = 2; door on x = 1 |
| `#../##./###` | (1, 2) | (3, 2) | A | common rectangle; collinear |
| `#../##./###` | (2, 1) | (2, 3) | A | common rectangle; collinear |
| `#../##./###` | (1, 2) | (1, 2) | A | common rectangle; equal position types |

## Numerical attack

No pair failed. Every prescribed path that was traced is a legal path. Because
no construction failed, no direct search for other paths was needed.

### Method

- **Arithmetic.** All numbers are exact elements of Q(sqrt 2), Q(sqrt 5), or
  Q(sqrt 3). Sign tests are exact. No floating point decides a result.
- **Tracers.** `rv.py` has two billiard tracers that don't use the lemmas. One
  walks wall by wall with fractions. One uses integers without division. A
  trace reports a vertex hit, a miss, or a legal arrival at T.
- **Rooms.** Edge lengths are integers, rationals, or irrationals such as
  multiples of sqrt 2 and powers of the golden ratio. The "extreme" style
  scales some gaps by 1/100 to 30. That gives thin corridors and aspect ratios
  up to about 10^6.
- **Pairs.** Each room gets 52 pairs. They are biased to degenerate
  positions:
  - points on grid lines and on grid points
  - points at distance 10^-9 from a grid line
  - points on a line through two vertices
  - pairs with S + T = 2V for a vertex V
  - pairs whose segment passes through a vertex
  - mirror images in grid lines
  - pairs on one horizontal or vertical line
  - pairs with an image of T on a ray from S through a grid point
- **Engineered pairs.** For instances of Lemmas B, B2, and C, the script
  builds more pairs. In each one, a member of the family passes exactly
  through a flat end, a reflex door end, or the corner of Lemma B2.
- **Checks per pair.** The script builds every instance of every lemma whose
  hypotheses hold, and traces its candidates. The certificate of `lemmas.py`
  must name one of those instances. For Lemmas B, B2, and C the script counts
  the window values per sign exactly.

### Counts

Run 2 uses seed 20261110. Run 3 uses seed 20261111 and the deep retry.

| Quantity | Run 2, 8 two-reflex types | Run 2, L and rectangle | Run 3, 8 two-reflex types |
| --- | --- | --- | --- |
| Rooms | 1,680 (210 per type) | 100 | 480 (60 per type) |
| Pairs | 115,154 | 6,272 | 32,877 |
| Of which engineered pairs | 27,794 | 1,072 | 7,917 |
| Lemma instances evaluated | 511,560 | 24,891 | 146,476 |
| Candidate paths | 2,620,343 | 102,471 | 734,957 |
| Of which over the reflection cap, not traced | 190,119 | 5,680 | 47,793 |
| Pairs whose certificate path traced legal | 113,973 | 6,244 | 32,674 |
| Pairs whose certificate path is over the cap | 1,181 | 28 | 203 |
| Failures | 0 | 0 | 0 |

So each two-reflex type has 270 rooms, and each room has at least 52 pairs.
The total for r = 2 is 2,160 rooms and 148,031 pairs.

More counts for run 2, the 8 two-reflex types:

- **Instances per lemma.** A: 79,440. A2: 35,588. B: 100,348. B': 97,430.
  B2: 124,286. C par: 17,653. C perp: 16,869. C same: 2,876. D: 37,070.
- **Certificates per lemma.** A: 79,440. A2: 136. B: 28,404. B2: 269.
  C par: 3,563. C perp: 466. C same: 2,876.
- **Lemma B.** Every instance has a window value for each sign.
- **Lemma B2.** 3,427 candidates are corner cases, and each one meets the
  vertex. 2,387 instances have a valid path for one sign only.
- **Lemma C.** Every sign pair of every instance has a solution in the open
  windows. For 150 sign pairs, the enumeration of 400 values found none. The
  bisection of the proof then found one, and exact arithmetic confirmed it.
- **Tracer agreement.** 107,041 traces were repeated with the second tracer,
  with 0 mismatches. `tracer_compare.py 40 1` compares both tracers on 23,594
  more traces, including 944 vertex hits and 1,431 misses, with 0 mismatches.

### Limits

- **Reflection cap.** A trace stops at 3,000 reflections. The script counts
  such a candidate as skipped, never as a success or a failure. For 1,181
  pairs of run 2, every sampled candidate of the certificate is over the cap.
  The exact window count still ran for those pairs.
- **Deep retry.** In run 3, Lemma B certificates over the cap were retried
  with a cap of 200,000 reflections. 115 more paths traced legal. The longest
  has 192,074 reflections. 169 Lemma B pairs stayed over that cap.
- **Sampling.** When a window holds more than 8 values, the script traces 8
  values per sign. They are the extremes, the values nearest 0, and random
  values.
- **Shared reading.** `rv.py` encodes this review's reading of the lemmas. The
  tracers and the certificate comparison don't depend on that reading.

### Controls

`controls.py` checks that the harness can report a failure.

- **T room of "Candidates that fail".** No member of the one-door family has
  x* in the door. The 3 members that go straight to the door line miss T. The
  harness finds Lemma B after the role swap, and its paths trace.
- **U room of candidate (i).** The direct segment reports a vertex. The
  V-path of Lemma A2 traces. The harness offers no Lemma A instance.
- **Shots at vertices.** 24 shots, 20 vertex hits, 4 misses, 0 reported legal.

## What the theorem implies

**Confirmed, given the theorem:** an orthogonal room with a dark pair of
interior points has at least 10 walls.

The reason: a strictly simple orthogonal polygon with r reflex corners has
2r + 4 walls. At most 8 walls means r <= 2. Theorems 0, 1, and 2 then light
every pair of distinct interior points.

The statement needs these qualifications:

- **"Room" means a strictly simple orthogonal polygon.** The theorem says
  nothing about pinched rooms, rooms with holes, or slit rooms.
- **"Dark" means that no finite billiard path that avoids every vertex joins
  the points.**
- **It is a lower bound only.** The theorem doesn't say that a room with 10
  walls and a dark pair of interior points exists. At r = 3, `theorems.md`
  leaves 578 position-type pairs open.
- **It doesn't cover boundary points.** Each lemma uses that S and T are
  interior. The project log records a room with 10 walls and a dark pair of
  smooth boundary points. It is the five-square staircase with marks (1, 0)
  and (3, 2). See `../d10-mechanisms/theory.md` and `../coordinator-log.md`. This
  review didn't recheck that pair. It is consistent with the theorem.
- **For boundary points in rooms with at most 8 walls, the theorem gives no
  answer.**

## Files

All files are in this directory.

| File | Purpose | Command |
| --- | --- | --- |
| `review.md` | This document | |
| `enum_check.py` | Independent enumeration of types and pair counts | `python3 -B enum_check.py` |
| `rv.py` | Exact field, room model, two tracers, lemma instances | Library |
| `certs.py` | Cross-check of all 559 certificates | `python3 -B certs.py` |
| `certs_dump.txt` | Every pair with its certificate | `python3 -B certs.py dump` |
| `attack.py` | Numerical attack | `python3 -B attack.py 0,1,2,3 210 20261110 runs/run2` |
| `aggregate.py` | Sums the attack output | `python3 -B aggregate.py runs/run2` |
| `tracer_compare.py` | Comparison of the two tracers | `python3 -B tracer_compare.py 40 1` |
| `controls.py` | Negative controls | `python3 -B controls.py` |
| `c_same_degenerate.py` | The explicit failure of Lemma C, same form | `python3 -B c_same_degenerate.py` |
| `scan_same_corridor.py` | Scan for the degenerate certificate | `python3 -B scan_same_corridor.py 2` |
| `runs/` | Attack output: `run2_type0.json` to `run2_type9.json`, `run3_type0.json` to `run3_type7.json`, and logs | |

Type indices 0 to 7 are the lines of `types_r2.txt`. Index 8 is the L, and
index 9 is the rectangle. For run 3, set `ATTACK_DEEP=200000` and use seed
20261111 with 60 rooms. All runs used at most 2 processes. The directory holds
less than 1 MB.
