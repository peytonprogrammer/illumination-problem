# D227 review: pinned pairs, local freedom and end-bounce sign patterns

Date: 2026-11-23. Reviewer: Opus, independent. Note under review:
[note-snapshot.md](note-snapshot.md). Checks: [checks.py](checks.py), output
[checks.log](checks.log): 60 PASS, 0 FAIL, 0.06 CPU-seconds at `nice -n 10`.
The tracer is a general exact orthogonal-polygon tracer (Fractions). It reuses
the first-hit pattern from d226 `checks.py`, rewritten for arbitrary vertex
lists.

## Verdict

Every mathematical claim holds as stated. The main new fact is a lit witness
for the six-reflex example. For every m ≥ 1, the pair (0,0),(4t,4t) is lit by
direction (1,2) with two reflections, both inside the middle tier. The
mechanism generalizes: a roof–floor double bounce in a slab between two pins
produces exactly the (−,+) pattern that end bounces can't. So the example
obstructs only the end-bounce move, as the note says. It doesn't point toward
a pinned dark pair.

| Claim | Verdict |
| --- | --- |
| 1. Local freedom, five quadrant types | CORRECT |
| 2. Dilation equivalence, primitive caveat | CORRECT |
| 3. R22 deformation lit, chart preserved | CORRECT (traced t = 1, 2, 5) |
| 4. Graze determinant test | CORRECT |
| 5. Sign-pattern theorem | CORRECT WITH GAPS (scope of "precisely") |
| 6. Clearance threshold | CORRECT |
| 7. Six-reflex example | CORRECT as stated; **the pair is LIT** |
| 8. Interval-chain test, R22 components | CORRECT |

## Claim 1: local freedom — CORRECT

- The proof is complete. A vertical wall on x = Xᵢ can't have an endpoint at
  p, because that endpoint would be a vertex equal to p. So its nearer
  endpoint is on another refined level, at least δₚ away.
- Checked at six pins: both R22 marks, both marks of deformed R22 with t = 2,
  and both marks of the six-reflex room with m = 1. Each open square of radius
  δₚ misses every edge, and all four quadrants are occupied.
- The quadrant census at all R22 grid points gives ext 19, convex 13,
  smooth 6, reflex 9 and interior 2. Convex and reflex types occur exactly at
  the 13 + 9 vertices, and there's no pinch.

## Claim 2: dilation — CORRECT

Similarity preserves legality, so integer dilation preserves darkness and
every listed invariant. The converse is vacuous. The primitive-representative
caveat is accurate. Local clearance gives no upper bound on the minimum gap.
D214 claim 7 still requires witness transfer.

## Claim 3: R22 deformation — CORRECT

For t = 1, 2 and 5 the checks confirm the following:

- The room is orthogonal and strictly simple, with 22 walls and 9 reflex
  vertices.
- The x and y rank vectors of the vertices match the dilation, so the chart is
  unchanged.
- The least refined gap is t. Both marks are pinned and interior, and T stays
  even.
- The exact trace of S → (2t, 2t+2) has no reflection. The crossing at y = t is
  t²/(t+1), which is 1/2, 4/3 and 25/6.
- In the dilated room, the chord S → (2t, 2t) dies at the reflex corner (t, t).

The map (x, y) ↦ (x, φ(y)) with φ strictly increasing is a homeomorphism that
keeps edges axial. That proves simplicity for every t ≥ 1, not only the three
traced values. The parity claim is coordinate parity: (2t, 2t+2) ≡ (2t, 2t)
mod 2.

## Claim 4: graze determinant — CORRECT

The expansion is an identity once det(v, c) = 0 (checked on 3 cases × 4 values
of t). For R22 it gives −2t, with the corner on the clockwise side as
required.

The proof is sound under the stated hypotheses: every vertex moves affinely,
the chart is fixed, the contacts are isolated and transverse, and the macro
direction is nonaxial. Two small points:

- A local square at a reflex graze contains only the two edges that bound the
  missing quadrant. A slightly shifted line crosses those edges if and only if
  it enters that quadrant. That is exactly the determinant sign.
- "Clearance outside the squares persists" needs every vertex to be tc + e
  with fixed e, not only the grazed corners. The phrase "affine scaling family"
  implies this.

## Claim 5: sign-pattern theorem — CORRECT WITH GAPS

The identity K[a(1−α) − bα]/(D+a+b) is exact. With a, b ≥ 0, q(α) is affine
and nonincreasing, so (−,+) is impossible for every longitudinal end move. The
gaps concern the word "precisely".

1. **Repeated end bounces.** Take e or f ≥ 2. The ray returns to the end-tier
   interface on a wall and bounces again before it crosses. Then
   a = 2e·d₀ and b = 2f·d₃ are still nonnegative, so (−,+) stays impossible.
   The switch point becomes θ = e·d₀/(e·d₀ + f·d₃), not only d₀/(d₀+d₃). With
   d₀ = d₃ and e, f ≤ 3, θ ranges over {1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4}.
   The sentence "(+,−) needs the actual θ strictly between those pins" should
   say "some attainable θ". The list of patterns is unchanged.
2. **Transverse end moves.** Reflecting a developed endpoint across an
   end-tier vertical wall shifts gate i by (1−α)Δ₀ + αΔ₃. With Δ₀ < 0 < Δ₃
   this is (−,+). Such a shift is at least twice the distance to that wall, so
   it is a new winding, not a micro repair. The theorem should still name its
   move set: longitudinal end bounces only.
3. **Interior double bounces** realize (−,+), as shown under claim 7. They
   fall outside the theorem's move set too.

## Claim 6: clearance threshold — CORRECT

X′ᵢ = Xᵢ + σ′qᵢ holds exactly (9 test points). The threshold is just
σ′|qᵢ| < mᵢ and σ′hⱼ < gⱼ rearranged. One remark: D′, qᵢ and mᵢ all scale
together under dilation. The bound is scale-free, so it's a condition on the
shape of the passage, not a size threshold. The note's wording "for a fixed
passage" is consistent with that.

## Claim 7: six-reflex example — CORRECT as stated; the pair is LIT

Geometry, checked for m = 1, 2, 3:

- The room is orthogonal and strictly simple, with 16 walls and 6 reflex
  vertices.
- S and T are interior and pinned. The x gaps are
  (t+1, t, t, 2t, t, 2t, t) and the y gaps are (m, t, 2t, t, m). The minimum
  gap is m, and both gcds are 1.
- The unbounced chord dies at the reflex corner (t, t).
- On their first pass, the floor, roof and double end-bounce chords each
  reflect off a middle-tier wall. For m = 1, the floor chord hits x = 11 at
  (11, 19/2), and the roof chord hits the E2 roof at (726/23, 33).

The demands (−,+) at α = 1/4 and 3/4 and the "both signs wrong" analysis are
correct.

**Lighting test for m = 1** (t = 11, T = (44, 44)). I traced 20 hand-chosen
directions, each up to 400 reflections, with no sweep. Seven directions are
lit:

| Direction | Reflections | Route |
| --- | --- | --- |
| (1, 2) | 2 | (0,0) → (33/2, 33) E2 roof → (55/2, 11) E2 floor → (44,44) |
| (1, 3) | 4 | E2 roof/floor zigzag, reflections at (11,33), (55/3,11), (77/3,33), (33,11) |
| (1, 4) | 6 | E2 roof/floor zigzag, three roof and three floor hits |
| (3, 4) | 8 | includes the E2 side walls x = 44 and x = 0 |
| (22, −23) | 8 | the floor-bounce direction: its first pass fails at x = 11, but the ray continues and reaches T |
| (3, 2) | 14 | transverse folds in E1 and E2 |
| (3, 5) | 47 | long route through every tier |

The other 13 directions fail: (1,1), (22,23), (11,−12), (5,2), (−1,1), (−1,2),
(−1,−1), (3,1), (2,3), (1,−2), (2,1), (−3,2) and (5,4). Each dies at a corner
or reaches the 400-reflection cap.

The minimal witness is uniform in m. Direction (1, 2) crosses y = t at t/2,
reflects off the E2 roof at (3t/2, 3t) and the E2 floor at (5t/2, t), crosses
y = 3t at 7t/2, and ends at (4t, 4t). The exact trace confirms this for
m = 1, 2, 3 and 7.

**Why it works.** The witness inserts a roof–floor double bounce in the slab
of length L = 2t between the two pins, which moves the developed target from
D to D + 2L. Gate i moves by one of two amounts:

- −Kα·2L/(D+2L) < 0 if the gate is below the bounced slab
- +K(1−α)·2L/(D+2L) > 0 if the gate is above it

This is exactly the (−,+) pattern, with the switch at the bounced slab. Here
the displacements are (−t/2, +t/2) (checked). The move is legal when both
bounces land on walls and the chain test passes. That holds here because the
E2 roof over (0, 3t) and the E2 floor over (t, 4t) are long walls. So end
bounces give (+), (−) and (+,−), and interior double bounces give (−,+). The
note's "first open implication" has a positive answer in its own example.

## Claim 8: interval chain, R22 components — CORRECT

- R22 at y = 1: the lower components are (−1, 1) and (3, 5), the upper one is
  (0, 4), and the openings are (0, 1) and (3, 4). The direct ray crosses at
  x = 1, the endpoint of the opening for its own component.
- The chain test is necessary and sufficient for a straight monotone
  traversal, by slab convexity.
- My implementation agrees with the tracer on all seven test chords. It passes
  deformed R22 for t = 1, 2, 5, rejects dilated R22 for the same t, and
  rejects the unbounced six-reflex chord.

## Which lemma advanced

**L1**, pinned-pair route: negative controls and one positive mechanism, with
no closure. Claims 1–4, 6 and 8 are sound reformulations and controls. This
review adds a lit witness for the note's six-reflex example and a short proof
that an interior double bounce realizes the (−,+) pattern. That is the
current PROGRAM step (interior-bounce sign patterns, l1-interior-bounce.md).
No B(r) and no dark family follow.

## First case still open

The next open step is a combined move lemma for a monotone passage. Say an
ordered graze demand has length k. Is it always met by end bounces together
with interior double bounces, possibly several slabs each bounced several
times, with walls at the bounce points and a valid interval chain? That
includes demands like (−,+,−). The first open configuration is an ordered
(−,+) demand where every slab between the two pins has its roof or floor
entirely gate over the needed abscissa. Then no wall is available for an
interior double bounce. The six-reflex room isn't such a case, and I know no
example with r ≤ 8.
