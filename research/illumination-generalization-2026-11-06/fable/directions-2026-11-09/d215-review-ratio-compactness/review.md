# D215: review of ratio compactness

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: [note-snapshot.md](note-snapshot.md).
Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
1.0 CPU-second under `nice -n 10` and reports 22 PASS, 0 FAIL.

To rerun it, use `nice -n 10 python3 -B checks.py`.

`checks.py` imports the d212 exact tracer and the d213 `stair_room` helper
unchanged. Every traced ray is the note's prescribed direction: (k, D) for
Claim 5, and (6, D) or (k, D) for Claim 6. No room class, direction, word, or
room size was searched. The only room is the named offset staircase, plus a
y-scaled copy for rational gains. Network use: the two arXiv abstract pages.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Chart-wise compactness statement | CORRECT |
| 2 | Interior section: closed dark locus, LMW and Wolecki, pinned marks | CORRECT WITH GAPS |
| 3 | Uniform face neighborhoods by codimension | CORRECT WITH GAPS (proof read only) |
| 4 | Effective radius ρ and the bound by B(p) | CORRECT |
| 5 | Staircase reflected construction, lower mark x = 2 | CORRECT |
| 6 | Nondirect pair, lower mark x = 1 | CORRECT |
| | **Overall** | **CORRECT WITH GAPS** |

No mathematical error was found. The gaps are about citation precision and
unstated hypotheses in the face induction. None changes a conclusion.

## Claim 1: chart-wise compactness

- **Parameter space.** Fix the order type, including coordinate equalities.
  Then every positive gap vector realizes the same strictly simple marked
  room. Intersections of axis-parallel edges depend only on coordinate
  comparisons, and those are fixed. After translation and separate span
  normalization, X is the product of open simplices of dimensions k−1 and
  l−1. Separate axis scaling diag(λ, μ) maps reflections in axis-parallel
  walls to reflections and corners to corners, so it preserves illumination.
- **Compactification.** K is the product of the closed simplices. It's
  compact. A span can't fully collapse because each simplex sums to 1. Keeping
  labels on zero coordinates is a sound choice; it avoids false
  identifications.
- **Finite subcover.** Each z in K has a relatively open V with a certificate
  for all of V∩X. Compactness gives a finite subcover, and the union covers X.
  Integral realizations are exactly the rational points of X, so the lattice
  statement follows. The caveats are right: compactness gives no radius and no
  algorithm, and an uncovered face neighborhood can hold infinitely many
  rational ratios.

## Claim 2: interior section

- **Closed dark locus.** A legal itinerary is stable under small perturbation.
  It uses strict transversality, strict interior hits and corner clearance. So
  the lit set is open in X, and the dark locus is relatively closed. Correct.
- **Wolecki (arXiv 1905.09358).** The abstract says that in a rational
  polygonal billiard, "the set of pairs of points that do not illuminate each
  other ... is finite." The note's reading is right. Orthogonal rooms with real
  side lengths are rational polygons, since all angles are multiples of π/2.
- **Lelièvre–Monteil–Weiss (arXiv 1407.2975).** The abstract states the
  result only as an extension of Hubert–Schmoll–Troubetzkoy to non-lattice
  translation surfaces. It does not state the polygon corollary verbatim. The
  note's "finitely many dark targets for each source" is the standard reading
  of the paper body. This review did not read the body, so the exact
  polygon-level wording is UNVERIFIED here.
- **Pinned marks.** The argument is correct. When a chart fixes each mark at
  the intersection of two supporting lines, the mark fiber over each room is a
  single point. Wolecki's finite exceptional set can contain that point, so
  fiberwise finiteness says nothing. The dark locus is closed, so nearby lit
  realizations can't certify a dark limit. Approximation can't discharge an
  exceptional specified pair.
- **22-wall example.** An orthogonal room with 22 walls has (22−4)/2 = 9
  reflex vertices. That is consistent with "outside the eight-reflex budget."
  The existence of the example comes from project context and wasn't
  rechecked.

**Gaps.**

1. Low. Cite the theorem numbers in LMW and Wolecki for the polygon
   statements, not only the arXiv pages.
2. Low. Say that "illuminate" in both papers excludes paths that hit
   vertices. The note's legality convention must match this.
3. Low. The "d212" link uses a path
   (`../../illumination-generalization-2026-11-06/fable/...`) that doesn't
   resolve from this directory. The d213 and d214 links have the same problem, and `l1-selection-obstruction.md` is not in this directory. These links probably resolve from the note's source location, not from this snapshot.

## Claim 3: uniform face neighborhoods by codimension

This review checked the proof by reading only. The codimension-one step is
correct. Through a transparent layer of thickness ε the straight chord drifts
by (transverse/normal speed) × ε. The rest of the itinerary uses strict
inequalities. For a parallel stack at one crossing, the chord has no
reflection inside the stack, so the drift is the slope times the total
thickness. Choosing one radius so that the sum of all drift bounds and
endpoint perturbations is below the smallest margin removes the dependence on
the order of restoration. It also handles very unequal thicknesses. The note
correctly says that relative face interiors aren't compact, and that each
higher-codimension point needs its own neighborhood.

**Gaps.**

1. Medium. Restoring a layer moves every level beyond it, including the marks
   and the far endpoint. "Entry displacement" covers this only if the chord's
   direction is allowed to vary continuously with the target. Say that the
   certificate fixes the itinerary and the endpoints, not the direction.
2. Low. "Stable marks" should mean that neither mark lies in a collapsing
   layer or on a collapsing seam. The stopping list covers this only in part.
3. Low. Sufficiency only. The note says so, but the final list of stopping
   cases isn't exhaustive. A seam crossing at a coincident reflection on a
   surviving wall is one example.

## Claim 4: effective radius

∂p/∂vᵢ = Σ cₘ mᵢ v^(m−eᵢ). On [−1, 1]ⁿ each monomial has absolute value at
most 1, so Σᵢ |∂ᵢp| ≤ Σ |cₘ| Σᵢ mᵢ = B(p). K lies in the unit cube and is
convex, so the segment from z to v stays in the cube. Hence
|p(v) − p(z)| ≤ B‖v − z‖∞ < p(z)/2 on the relative sup ball of radius ρ.
The factor 2 gives the "half slack" statement, and the min with 1 is harmless.

The log checks the gradient bound at 1,500 random points for 300 random
polynomials. It also checks p ≥ p(z)/2 on sampled ball points. Applied to the
three linear tests of Claim 6, the formula gives 11/370, which is half of
11/185, as expected.

The construction of the sign list is sound. Unfolded wall coordinates are
affine in the gaps. Leg endpoints are rational, and their denominators carry
recorded signs. A separating line fixed at z gives sign tests that imply
disjointness. Discarding positive gap factors at a face is legitimate,
because they're positive on X.

## Claim 5: reflected construction (lower mark at x = 2)

- **Symmetry.** A 180-degree rotation maps the staircase with gains (x, y) to
  the one with (y, x) and swaps S and T. So x ≤ y is no loss, and α ≤ 1/2.
- **Existence of k.** The sequence k ≡ 3, 5 (mod 6) satisfies k₍ᵢ₊₁₎ < 2kᵢ,
  so the union of (1/k, 2/k) is (0, 2/3). The log checks this up to 10⁵.
- **Path.** The slope is s = k/D < 2/(x+2) ≤ 1. The crossings are 2+s in
  (1, 3), 2+kα in (3, 4), and the fold of 2+k ≡ 5 or 1 (mod 6) in [3, 6] at
  5 ∓ s, which lies in (4, 6). The proof holds for every real x, y ≥ 0.

Exact traces confirm the construction in each of these cases:

- All 3,721 rooms with 0 ≤ x, y ≤ 60. For x > y the ray starts at T and goes
  down and to the left in the original room.
- Every admissible k, not only the smallest, on a subgrid (527 traces).
- y = ⌊x^1.5⌋ for x = 0..200. There k grows like √x, for example k = 15 at
  x = 196.
- The √2 family for t = 0..200, in both orders.
- 336 rooms with rational gains x/q and y/q for q = 2, 3, 7, using y-axis
  scaling.

The note's scope statements are accurate. The result covers one pair and one
width assignment, not the full chart.

## Claim 6: nondirect pair (lower mark at x = 1)

- **(15, 21).** D = 40, slope 6/40. The crossings are 23/20, 71/20 and 103/20.
  The developed value is 137/20, reflected at x = 6. The direct abscissa is
  27/10. All values are exact. The room has area 126. The ray (6, 40) reaches
  T by exact trace, and the direct chord doesn't.
- **Region.** The algebra is right: b+c−2a > 0 is 6a/D < 1, and c > b and
  2a+2b−c > 0 put the middle crossing in (3, 4). The direct abscissa is below
  3 when c > b. On the grid 0..60 (a = 1), all 929 region rooms are lit by
  (6, D), and the direct chord is never legal there. The √2 family lies in the
  region exactly for t ≥ 3. The note doesn't need the smaller cases.
- **a = 0.** The first crossing 1 + 6a/D carries the positive factor a, so
  discarding it, as Claim 4 allows, is correct.
- **Radius.** The values are 11/185 at (1, 15, 21)/37 and
  (2−√2)/(5(1+√2)) ≈ 0.0485 at the √2 face. Both were checked with exact
  arithmetic, the second in Q(√2). The ball is the ambient sup ball. It is
  valid, and in the ambient cube it is sharp. It's conservative in the
  simplex plane, which is fine.
- **x^(3/2) construction.** The interval (2/α, 3/α) has length 1/α > 4 when
  α < 1/4 (that is, y > 3x + 4). The classes 0 and 4 (mod 6) have gaps 4 and
  2, so the interval contains one. For x ≥ 1 the slope is below 1. On
  y = ⌊x^1.5⌋ the condition α < 1/4 first holds at x = 12, and all 189 such
  x ≤ 200 trace legal. On 3,300 rooms with y = 3x+5..3x+59, every admissible
  k traces legal.

**Observation (not claimed).** The same ray (6, D) also lights the 929 grid
rooms of the mirror region b > c, 2a+2c−b > 0, b+c > 2a. There the middle
crossing is in (4, 5), with one extra reflection at x = 4. So the
(6, D) certificate covers both sides of the line b = c away from that line and
from a = 0 corners. Adding this region would enlarge the note's certified part
of this pair's ratio triangle at no cost.

## Which lemma advanced

**L1.** The note gives a correct compactness reduction for each chart, an
effective radius, and uniform codimension face neighborhoods under explicit
transparency hypotheses. The named staircase pair (mark at x = 2) is now
proved lit for every real gain pair, including the x^(3/2) regime. Its ratio
gap is closed. No census changes. The compactness reduction does not reduce
the 22–121 lift obligation by itself.

## First case still open

The note is right that the first open case is an exceptional *specified* mark
pair in one positive, nondegenerate eight-reflex chart, with both marks
pinned to supporting-line intersections. No cited theorem and no perturbation
argument excludes it. For the x = 1 staircase pair, the uncovered part of the
ratio triangle is the strip near b = c, where neither (6, D) region applies.
It also includes the band 2a+2b ≤ c with α ≥ 1/4, between the region and the
x^(3/2) construction. That is the smallest concrete open sub-case in this
note's own slice.
