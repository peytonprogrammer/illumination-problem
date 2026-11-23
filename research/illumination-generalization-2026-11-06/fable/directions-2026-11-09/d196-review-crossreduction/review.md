# Review of d196: crossing reduction and the W=10 stopping-rule test

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: `snapshot.md`, sha256 `3eeee9e873120bf4...` (prefix 3eeee9e8 confirmed).
Bases: [d187 review](../d187-review-chartdescent/review.md) (81·G(C)², H(C)),
[d188 review](../d188-review-mixedseed/review.md) (mixed seeds, one row per seed),
[PROGRAM.md](../PROGRAM.md) last section (stopping rule).

Checks: [checks.py](checks.py), output [checks.log](checks.log). The log has
27 PASS lines and 0 failures in 0.001 CPU seconds. The only polygons are the
ledger realization and the chart 3,4,2,0,1 at five named gap vectors. The only
vectors are (n,n+1,n+2,n+3) at n = 5, 100, 10⁶. No room, ray, direction, word,
or size search was run.

## Verdict

**PASS WITH CORRECTIONS.** Confidence: high on (a), (c), (d) and on the
stopping-rule conclusion; medium on the assessment of the proposed route.

The note answers the stopping rule correctly: no numerical N0 follows from
reviewed results. Every computation I checked is exact. The corrections are
about framing. The most important one is that the proposed "exact bilinear
area" route is equivalent, up to constants, to the G(C) bound that already
failed. Its only real gain, minimum over products instead of maximum, was
already allowed by the d187 review.

| Item | Verdict |
| --- | --- |
| (a) At most four wall gaps per axis; 81·G² sharpens to 16·G² | **Correct.** Also ≤ 15·G², and chart-specific counts are 7–8 (Low 2) |
| (b) No numerical N0; G(C) not bounded by reviewed results | **Correct.** "Unevaluated", not "unbounded", which the note says correctly |
| (b) Missing step: occupied crossing supplying the next independent normal with controlled height | **Right step.** It matches d187 §4 (H(C)) and d188 §5 |
| (c) Dimension drops by one per independent normal | **Correct** (rank-nullity). It needs total dimension and bounded height (Medium 2) |
| (d) Growth rays reduce to occupied crossings read off the chart | **Correct as a dichotomy.** The subsequence step is non-effective (Medium 3) |
| (e) First open case: all eight gaps growing comparably | **Correct and realizable.** It is the generic case, not the smallest one (Low 4) |
| (f) Small-area witness via occupied cells | **Not distinct as stated** (Medium 1) |

## Checks (a)–(f)

### (a) Wall gaps and the 16·G(C)² bound

- The word LLLRLLLRLR from an east edge gives E,N,W,S,W,S,E,N,E,N and closes
  with 7 L and 3 R (log §1).
- The ledger realization (2,0),(4,0),…,(2,2) has directions
  E,N,W,N,W,S,E,S,E,S and turn word LLRLLLRLRL. That is the cyclic rotation of
  LLLRLLLRLR by one. Rotating it 90° and starting one edge later reproduces the
  note's vertex template exactly, with x = (−2,0,−1,−4,−3), y = (2,4,3,0,1)
  (log §2). So the template is right up to rotation and cyclic start (Low 1).
- The realization has 5 distinct x and 5 distinct y, so 4 wall gaps per axis,
  all equal to 1. It's simple, its area is 8, and area = Σ M_ij a_i b_j with
  Σ M = 8.
- The general claim holds for any length: 5 vertical edges give at most 5
  x lines, so k_x ≤ 4, and likewise k_y ≤ 4. Marks subdivide but never add wall
  lines. So d187's k_x k_y ≤ 81 becomes 16, and area ≤ Σ M · m(U) m(V) ≤ 16 G².
- The bilinear identity is exact by disjoint cell interiors (checked at five
  gap vectors in log §4).

### (b) "No N0" and the missing step

The d187 review (§4) reduced G(C) to one missing estimate: an explicit
factor-height bound H(C). The d188 review replaced the probe with a mixed seed
that yields one bounded row on at least one axis per seed. It named the missing
input as a fixed-period mixed transfer at occupied crossings with explicit seed
constants. Neither review bounds G(C). Fixed-template finiteness (d189–d192)
leaves constants free when the template varies. So G(C) has no reviewed
numerical value, and the note's conclusion stands.

The identified missing step is the right one. It also sharpens it: the next
normal is needed **uniformly over successive seeds, at every factor, including
the final rank-one factor**. The rank-one example makes this concrete (see (c)).

### (c) Decreasing invariant

If U ⊆ E and h vanishes on U but not on E, then U ⊆ E ∩ ker h and
dim(E ∩ ker h) = dim E − 1. This is correct. To be a usable descent, it needs
four things the note only partly states (Medium 2):

1. The invariant must be **dim E + dim F**, the total over both axes. d188
   guarantees a row on at least one axis per seed, not on a prescribed axis.
2. Each step needs a seed lying in the current E × F with uniformly controlled
   period, clearance, and qMP. Otherwise the row height is not bounded.
3. Each row must have **bounded height**, not just independence. Dimension
   alone never bounds m.
4. Termination takes at most the number of fine gaps on both axes. That is a
   fixed bound for W=10, so depth is not the problem. Height is.

The rank-one example is right, and log §5 confirms it. v = (n,n+1,n+2,n+3) is
primitive, and its minimum largest gap on the line is n+3. h·v = n·Σh + (h₁ +
2h₂ + 3h₃). So for n > 6H, every normal of height ≤ H lies in the rank-2 span of
(1,−2,1,0) and (0,1,−2,1). The third normal must have height at least
((n+3)/6)^(1/3) by Cramer. So "dimension ceases to control witness size" should
read "the last normal has unbounded height". This is the H(C) gap again, not a
new phenomenon (Low 3).

### (d) Reduction to occupied crossings

The bipartite-graph dichotomy is correct. If no diverging x gap and diverging
y gap share an interior cell, the intersections of the growing vertical and
horizontal strips with the room are empty. So the strips have disjoint
interiors in the room. An edge is exactly an occupied rectangle growing in both
directions. The residual list is conservative and honest.

Two caveats:

- Passing to a subsequence to fix bounded gaps and order scales is a
  compactness step. It gives no effective constants by itself. The note says a
  bound counts only if its constants are uniform. It should also say that this
  reduction cannot produce N0 without a uniform version (Medium 3).
- The dichotomy classifies rays. It doesn't by itself bound anything, which the
  note states.

### (e) First open case

The chart with both axes ordered 3,4,2,0,1 is realizable and full-dimensional.
At gap vectors (1,1,1,1)², (2,3,5,7)×(11,13,17,19), (19,1,1,19)×(1,19,19,1),
and (n,…,n+3)×(n+3,n+1,n,n+2) for n = 10 and 1000, the polygon is simple, has
turn word LLLRLLLRLR, and keeps the same occupancy (log §4). For orthogonal
polygons with distinct coordinates, simplicity depends only on the coordinate
order, so all eight gaps vary independently. The slabs from bottom to top have
x intervals (x3,x4), (x3,x0), (x2,x0), (x2,x1), and consecutive slabs overlap.
The chart has 7 occupied cells. Every row and column is occupied, so every cell
is a growing crossing when all gaps grow comparably. The note's description is
correct.

This is the generic open case, not the smallest one. The smallest test is a
retained product in this chart with a rank-one factor whose primitive vector
has large height. That is the (n,n+1,n+2,n+3) situation, and the d187 review's
"product of two lines" test (Low 4).

### (f) Proposed route

See the section on the proposed route below.

## Corrections by severity

**High.** None.

**Medium.**

1. **The exact-area route is not distinct as stated.** Every x gap column and
   every y gap row of a chart has an occupied cell (log §4). So every witness
   satisfies max(Σa, Σb) ≤ area ≤ Σ M · max a · max b. Bounding the minimum
   area on a product is therefore equivalent, up to a square and a constant
   ≤ 15, to bounding min max(m(U), m(V)). The occupied-cell form changes only
   the constant. In this chart it changes 16 to 7. The only real weakening is
   minimum over retained products instead of maximum. The d187 review (§1c)
   already noted that the minimum suffices. The note should say this and drop
   the suggestion that the area form "avoids" the arithmetic estimate.
2. **State the invariant's requirements.** Use dim E + dim F. Each step needs
   a seed in the current E × F with uniform constants and a row of bounded
   height. Depth is bounded for W=10, and the open issue is height alone.
3. **The subsequence step is non-effective.** The crossing dichotomy is a
   compactness classification. Without uniform constants on each branch, it
   cannot yield a numerical N0, however the branches are resolved.

**Low.**

1. The ledger realization matches the template after a 90° rotation and a
   one-edge shift of the start. Say "up to rotation and cyclic start".
2. A full 4×4 occupancy is the bounding rectangle, so Σ M ≤ 15. The ledger
   chart has Σ M = 8 and the stress chart has 7. A hypothetical G = 2 gives 32
   and 28, both under the stopping rule's threshold of about 40. The 64 figure
   reflects the box estimate only. The real obstruction is that G is unknown.
3. Rephrase the rank-one remark. For n > 6H, bounded normals span rank 2 only,
   and the third normal has height at least ((n+3)/6)^(1/3). The issue is the
   height of the last normal, not dimension.
4. Call the all-gaps-comparable cone the generic open case. Name the rank-one
   factor in that chart as the smallest open test.

## Stopping rule

**The "no N0" conclusion is correct.** No reviewed result bounds G(C) or H(C)
for any W=10 chart. d188 gives one row per seed under fixed-period hypotheses
that fail at occupied crossings. d189–d195 give constants only for fixed
templates or fixed stretches. With G unknown, 16·G² (or 7·G² on the stress
chart) is not a number. The stopping rule fires: stop the crossing chain and
report to Daniel with a new route.

## Proposed route

The proposal is plausible as a goal. It isn't distinct from what failed until
it names a mechanism.

- **What is new.** It asks for a small witness on *some* retained product, not
  a height bound on *every* product. That is a real weakening of the target.
- **What is not new.** Using occupied cells instead of the bounding box changes
  constants only (Medium 1). Proving that a given rational dark factor has a
  small positive point is the same arithmetic problem as H(C). The note's own
  "sufficient geometric lemma" (bounded-height normals at each factor) is
  exactly the d187/d188 route.
- **What would make it distinct.** It needs a geometric operation that maps a
  dark room in the chart to a smaller dark room in the same chart, without
  passing through the rational factor. One example is a darkness-preserving
  shrink of a growing gap by a fixed period. Such a lemma would give N0
  directly from the area form, as Σ M · (period bound)². It would also bypass
  heights. Its test case is the stress chart 3,4,2,0,1 with comparable growth.

## First open case

In the chart with both axes ordered 3,4,2,0,1 (7 occupied cells), all eight
wall gaps grow comparably. Every occupied cell is a growing crossing, and no
fixed template exists. The smallest instance is a retained dark product with a
rank-one factor whose primitive gap vector has large height, such as
(n,n+1,n+2,n+3). There, two bounded normals exist, but the third has height at
least ((n+3)/6)^(1/3). Nothing proves such a dark factor exists, and nothing
excludes it.
