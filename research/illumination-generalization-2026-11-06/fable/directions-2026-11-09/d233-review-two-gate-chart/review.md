Advances: L1 — confirms that bounded-axial-reversal vertical itineraries cannot certify lighting on the six-reflex two-gate chart. The obstruction is axial only: the witness is monotone in x with 3 transverse events, so lists built from transverse itineraries are not excluded.

# D233 review: the two-gate chart (`snapshot-l1-two-gate-chart.md`)

This is an adversarial referee review. All arithmetic is exact (`fractions`). The rooms used are the note's family at N ∈ {40, 42, 100}, plus the single rectangle of claim 2. I ran no room, direction, word or size searches. The only ray traced is the stated witness, velocity (1,2). Total CPU is about 0.3 s, well inside the 10-minute budget.

## Verdicts

| # | Claim | Verdict |
|---|-------|---------|
| 1 | Row test for hollow open rectangles (g=2); "zero, one, two or three rows" | CORRECT. The test is exact for any completed primitive dual basis. "Three rows" is an upper bound from Flt(2); it may never occur for parallelograms (inferred, not checked). |
| 2 | Hollow, non-split rectangle with min width 4/5 | CORRECT (recomputed exactly; proof for all covectors) |
| 3 | Chart: strictly simple, 6 reflexes, interior pins | CORRECT: 16 walls, 6 reflexes, both pins interior |
| 4 | Family N even ≥ 40 lies in the chart, unit gates, interior pins | CORRECT (proof, and computed at N=40, 42, 100) |
| 5 | Obstruction N/2 ≤ 2A_t + A_s, so N ≤ 12(r₀+1) | CORRECT. Every attacked step holds. The threshold is conservative: N ≥ 38 already works for r₀=2. |
| 6 | Witness (1,2) lights S,T with no corner contact | CORRECT for every even N ≥ 4, so for all even N ≥ 40. Traced at N=40, 42, 100. Axial reversals: N/2 − 1. |
| 7 | (Review task) N=40 hollowness | Monotone itinerary: 0/8 parity cosets lit, through a split covector of width 1/40. Top-roof single excursion: 0/32 lit. |
| 8 | Scope: no finite list of bounded-reversal vertical itineraries gives an H(C) bound; "closes the test of the list, not the chart" | CORRECT WITH GAPS. The phrasing is right for vertical (axial) itineraries. The stopping-rule sentence drops "vertical", and the "first open case" omits the transverse decomposition. In that decomposition the witness is monotone, so the obstruction says nothing about transverse or two-axis lists. |

## Claim 1: the row test

**Derivation.** Let ℓ, m be a basis of Λ*. The map x ↦ (ℓ(x−v), m(x−v)) sends v+Λ to ℤ² and the open rectangle to an open parallelogram P. A point of ℤ² in P lies on a row u=i with i an integer strictly inside the open u-projection (u_min, u_max). On that row, P meets the line in the open interval (l_i, r_i) cut out by its four open half-planes. That interval contains an integer iff floor(l_i)+1 < r_i. So P is hollow iff every such row has floor(l_i)+1 ≥ r_i. Equality covers an excluded integer endpoint. The test is exact for **any** primitive ℓ that completes to a basis. The shortest-width choice only bounds the row count.

**Row count.** For an axis box, the u-width is W = Σ|J_i||ℓ_i|. If W > 1+2/√3, Hurkens's planar flatness theorem gives a coset point. Otherwise the open projection has length ≤ 2.155, so it contains at most 3 integers. The list "zero, one, two or three" is a correct upper bound. I believe three rows never occur for a hollow parallelogram (lattice-free quadrilaterals have width ≤ 2), but I didn't verify this. It doesn't affect exactness. "Zero rows is a split certificate" is correct.

**Gap (minor).** "Other primitive directions can also give split certificates; the row test need not recognize them" is fine. The row test still returns the right answer, because it is a complete enumeration.

## Claim 2: the rectangle

Recomputed in `geom_witness.py`:

- e1·e2 = 6·(−1/50) + (3/5)(1/5) = 0, so the edges are perpendicular.
- Vertices: (1/2, −1/100), (13/2, 59/100), (12/25, 19/100), (162/25, 79/100). The y-span is (−1/100, 79/100), so the only integer row is y=0.
- Row y=0: parametrize by t ∈ (0, 1/20). Then x = 3/5 − (101/50)t, so the open slice is (499/1000, 3/5), which contains no integer. The rectangle is hollow.
- Width: |ℓ·e1| + |ℓ·e2| = |6p + 3q/5| + |−p/50 + q/5| = (3/5)|10p+q| + (1/50)|−p+10q|. This is an identity, and the script asserts it for |p|,|q| ≤ 60.

**No projection miss, for all covectors (proof).**

- **p ≠ 0, |10p+q| ≥ 2:** the first term is ≥ 6/5.
- **p ≠ 0, |10p+q| ≤ 1:** write q = −10p+δ with |δ| ≤ 1. Then |−p+10q| = |−101p+10δ| ≥ 91, and the second term is ≥ 91/50.
- In both cases the width exceeds 1, so the open projection has length > 1 and contains an integer.
- **p = 0:** the covector (0,q) has width 4|q|/5. Its projection is q·(−1/100, 79/100), which contains 0.

So no primitive covector misses. The minimum width is 4/5, at (0,±1), confirmed over the computed range.

**Scope.** In edge coordinates the box is axis-aligned and the lattice is rational and full-rank (det of the edge matrix is 303/250). The note doesn't claim that this box occurs as a d230 gate box Λ_τ of a real room, and I didn't check that. As a counterexample to a general width rule for non-split hollow boxes, it is valid.

## Claim 3: the chart

I walked the boundary by hand, then checked it with `gatebox.check_room` at three N values.

- **Edges (16):**
  - Right side and top: G on [y0,y1], y1: D–G, D on [y1,y2], y2: D–F, F on [y2,y3], y3: F–H, H on [y3,y4], y4: H–J, J on [y4,y5], y5: E–J.
  - Left side and bottom: E on [y3,y5], y3: C–E, C on [y2,y3], y2: A–C, A on [y0,y2], y0: A–G.
  - The walls x=A and x=E each run unbroken through a level.
- **Reflex corners (6):** (D,y1), (D,y2), (F,y3), (H,y4), (C,y2), (E,y3).
- **Strict simplicity:** the two horizontal edges on y2 (A–C and D–F) are disjoint because C < D. The two on y3 (C–E and F–H) are disjoint because E < F.
- **Interior pins:**
  - S = (C,y1) lies inside the open gate (A,D) at level y1.
  - T = (G,y4) lies inside the open gate (E,H) at level y4, because E < G < H.
- **Transmission intervals:** (A,D), (C,D), (E,F) and (E,H), as stated.

**Computed:** 16 walls and 6 reflexes at N=40, 42 and 100, strictly simple, with S and T interior.

## Claim 4: the family

The family has A=0, C=N−1, D=N, E=2N, F=2N+1, G=5N/2, H=3N, J=4N, and y = −1, 0, 1, 1+B, 2+B, 3+B.

- **Order:** A<C<D<E<F<G<H<J holds iff 2N+1 < 5N/2, that is N > 2. G is an integer because N is even.
- **Gates:** (N−1,N) and (2N,2N+1), both of width 1.
- **Pins:** S = (C,y1) and T = (G,y4).
- **Primitivity:** transverse gaps include D−C = 1, and all axial gaps except B equal 1. Both axes are primitive.
- **Computed:** areas 3704, 4057 and 21254 at N = 40, 42 and 100.

## Claim 5: the obstruction (every step attacked)

**Can an end leg leave its end region before the first or last passage?** No. The lower end {y ≤ 1} meets the rest of the room only through the open gate (N−1,N) at y=1, and both gate endpoints are corners. Likewise the upper end meets the rest only through (2N,2N+1) at y=1+B. By definition, A_s stops at the first passage and A_t at the last.

**Can a reversal happen at a non-integer level?** No. Axial reversals happen only at horizontal walls, and every horizontal wall lies on one of the six integer levels. A vertical wall hit, including a hit on a smooth wall exactly at a level (x=0 at y=0, x=2N at y=2+B), reverses only vx. So the leg's total variation in y is a sum of integer steps whose signed sum is ±1. A_s and A_t are odd.

**Mirrors.**

- Lower-end vertical walls are x = 0 (y∈[−1,1]), x = N (y∈[0,1]) and x = 5N/2 (y∈[−1,0]).
- Upper-end vertical walls are x = 2N (y∈[1+B,3+B]), x = 3N and x = 4N.
- The middle-tier walls x = N−1 and x = 2N+1 can't be reached from the ends.
- Every listed wall has 2a ∈ Nℤ, so x ↦ 2a − x is x ↦ −x mod N.

In the full unfolding, X = x_S + s·p·(absolute axial travel), with the same s and p throughout. This holds because reflections preserve |vx| and |vy|, so **p is the same on both legs**.

**The two congruences.**

- At the first passage, ±x₁ ≡ x_S + s p A_s (mod N), with x₁ ∈ [N−1,N] ≡ [−1,0] and x_S ≡ −1. So s p A_s ∈ [0,2] mod N, and dist(A_s p, Nℤ) ≤ 2.
- Backwards from T, ±x₂ ≡ 5N/2 + s′ p A_t, with x₂ ∈ [2N,2N+1] ≡ [0,1]. So dist(A_t p, N/2 + Nℤ) ≤ 1.
- Closed endpoints are granted, so rays through gate endpoints are covered. Those endpoints are corners anyway.

**Elimination.** Write A_s p = Na + e₁ and A_t p = Nb + N/2 + e₂, with |e₁| ≤ 2 and |e₂| ≤ 1. Then N(aA_t − bA_s) − A_s N/2 = A_s e₂ − A_t e₁. The left side lies in N/2 + Nℤ because A_s is odd, so its absolute value is ≥ N/2. That gives N/2 ≤ A_s + 2A_t. This is correct.

**Several middle passages, middle excursions, early passes through T.** None of these matter. Only the first-entry leg and the last-exit leg enter the argument. p = 0 (vertical rays) violates the second congruence, and p = ∞ (horizontal rays) never changes slab.

**Reversal budget.** An end leg has at most r₀ reversals, so it has at most r₀+1 monotone pieces. Each piece has length ≤ 2, the depth of the end ([−1,1] or [1+B,3+B]). So A_s, A_t ≤ 2(r₀+1), and N ≤ 12(r₀+1). This is correct and slightly wasteful, because the r₀ reversals are shared by both legs.

**Consequence for itineraries.** A box point gives a legal ray (d231 open box ⇒ chord). A closed smooth endpoint gives a legal ray too (d232). Either ray has the itinerary's reversal count. So for r₀ = 2, any lit itinerary needs N ≤ 36, and every itinerary with at most two reversals is hollow in every parity once N ≥ 38. "For N ≥ 40" is correct as stated.

**Consistency with the witness.** At N=40 the witness has A_s = 1, A_t = 39 and p = 1/2. The two distances are 1/2 and 1/2, and N/2 = 20 ≤ 79 (`geom_witness.out`).

## Claim 6: the witness

**Symbolic proof for all even N ≥ 4.**

- From S = (N−1, 0), with dx/dy = 1/2 upward, the ray reaches y=1 at x = N−1/2. That point is inside (N−1,N), and no wall lies between.
- Middle: x rises by B/2 = N+1 to 2N+1/2, inside (2N,2N+1). The ray stays strictly inside (N−1, 2N+1).
- Upper end: after axial travel t from the second crossing, x = 2N+1/2 + t/2.
  - Passes of y = 2+B happen at odd t, at x = 2N+1+k with k = 0…N/2−1.
  - Roof hits (y=3+B) happen at t ≡ 2 mod 4, at x = 2N+3/2+2k, inside (2N,4N).
  - Floor hits (y=1+B) happen at t ≡ 0 mod 4, at x = 2N+5/2+2k, inside the wall (2N+1,3N).
- All these abscissas are half-integers or lie below 5N/2 < 3N. None is a corner: the corners there are 2N, 2N+1, 3N and 4N.
- At t = N−1 (odd), x = 5N/2 at height 2+B, which is T. Earlier passes of y=2+B are at x < 5N/2.
- vx never changes sign, because no vertical wall is reached.
- The axial reversals are the reflections at t = 2, 4, …, N−2. That is **N/2 − 1** reversals.

The argument needs only 2N+1 < 5N/2, so it holds for every even N ≥ 4. There is no first failure.

**Computed** with `gatebox.trace` (exact). The status is `ok`, the endpoint is exactly T, and there is no corner or on-wall-level event.

| N | events | axial reversals | roof / floor hits | x strictly increasing | all abscissas match the note |
|---|---|---|---|---|---|
| 40 | 40 | 19 | 10 / 9 | yes | yes |
| 42 | 42 | 20 | 10 / 10 | yes | yes |
| 100 | 100 | 49 | 25 / 24 | yes | yes |

## Claim 7: independent hollowness at N = 40

`hollow40.py` is my own code; it doesn't import gatebox. It uses the d231 fold u_{j+1} = u_j + p h_j − c_j − 2w_jk_j, re-derived in the script header, and solves p from the endpoint. The column HNF of the integer-scaled Φ gives a lower-triangular basis L, so u = v + Lz with z ∈ ℤ^g in bijection with the coset. Triangular slicing then enumerates **all** coset points in the box exactly. No winding cutoff is needed, so the finite bound is justified by the triangular structure.

**Monotone itinerary.** Visits (a,w,h) are (0,40,1), (39,42,82), (80,40,1). The box is (39,40)×(80,81), with corner endpoints.

- The basis is L = [[1/21, 0], [1679/21, 80]] and covol = 80/21.
- **0 of 8 parity cosets are lit.**
- The certificate is a split. ℓ = (1/80, 1/80) lies in Λ* for every parity: it is n = (1,0,−1), the equal end moduli μ₀ = μ₂ = 1/80. Its width is 1/40.
- The projected window sits about 1/4 from ℤ in every parity, for example (−1/4, −9/40) at 000. This is the note's half-period mismatch: 20/80 = (N/2)/N.

**Single excursion: top-roof bounce, T reached from above.** The visits add (80,80,1) twice after the monotone ones. The events are:

- (39,40) at y=1.
- (80,81) at y=83.
- [80,120) at y=84. The endpoint x=80 is a smooth wall point, so it is closed. The endpoint 120 is a corner.
- The roof (80,160) at y=85.

Result: **0 of 32 parity cosets are lit**, with 720 enumeration nodes in total.

**Controls** (`hollow40_controls.py`). These use synthetic widened boxes on the same lattices. They test the enumerator only and are not room searches.

- With gate 2 widened to (80,101), the monotone lattice gives 21 hits and the excursion lattice gives 22.
- A brute-force k-enumeration with |k₀|,|k₁| ≤ 3 and |k₂| ≤ 60 finds a subset of the enumerator's points.
- The witness's k=0, all-even point reproduces the traced abscissas (79/2, 161/2, 81, 163/2, …) with p = 1/2.

A first sanity check widened both gates by only 1 and still found 0 hits. That is expected: the split window has width 6/80 there. It is not a failure.

**Not done.** I didn't test end-bounce itineraries in the lower end, or a middle roof–floor excursion. By claim 5 they are hollow (proof only).

## Claim 8: scope

**What the proof supports.** Fix any reversal budget r₀. Every even N > 12(r₀+1) gives a room in this chart where the prescribed pair is lit but no ray with ≤ r₀ axial reversals joins it. So every vertical itinerary with ≤ r₀ reversals is hollow in every parity there. Any finite, N-independent list of such itineraries is therefore totally hollow on an unbounded family of lit pairs. Hollowness of the list can't force a bound on area or height. That matches the note, and "closes the test of the list, not the whole chart's illumination problem" is accurate.

**Gaps.**

1. **Transverse decomposition.** The witness never touches a vertical wall, and vx = +1/2 throughout. In the transverse (column) decomposition it is a **monotone itinerary with 3 events**:
   - It crosses x = D at axial travel 2 and x = E at travel 2N+2, both in the middle tier.
   - It crosses x = F at travel 2N+4, in the upper end. This was computed at N = 40, 42 and 100.
   - Its N/2−1 roof and floor bounces are side windings in that decomposition.

   So this family doesn't exclude a finite list of transverse itineraries, or a list over both axes. The headline "every witness needs unboundedly many axial reversals" is correct. The stopping-rule sentence "The finite list of individual itineraries cannot yield H(C)" is correct only when "individual vertical itineraries" is meant.
2. The "first open case" names repeat counters and other templates. It omits the transverse or two-axis list, which this family doesn't touch. This is inferred: I didn't test a transverse list on other rooms of the chart.
3. Claim 2's rectangle is a counterexample to a general box rule. It isn't shown to be a gate box of this chart.

## Scripts and outputs

| Script | Output | Checks | CPU |
|---|---|---|---|
| `geom_witness.py` | `geom_witness.out` | Claim 2 rectangle (perpendicularity, row slice, width identity, minimum width and no projection miss for \|p\|,\|q\| ≤ 60). Claims 3–4 room, walls, reflexes, simplicity, interior pins, order at N=40,42,100. Claim 6 exact witness trace, reversal count, predicted abscissas, x-monotonicity, transverse crossings, obstruction consistency. | 0.17 s |
| `hollow40.py` | `hollow40.out` | Claim 7: exact coset enumeration (HNF plus triangular slicing). Monotone 8 parities and top-roof excursion 32 parities at N=40. Witness parametrization check. | 0.01 s |
| `hollow40_controls.py` | `hollow40_controls.out` | Split covector (1/80,1/80) in Λ* and its projection miss for each monotone parity. Synthetic widened-box positive controls. Brute-force cross-check. | 0.04 s |

`geom_witness.py` imports `../d231-review-gate-box/gatebox.py` for `room_from_tiers`, `check_room`, `interior` and `trace`. The hollowness code is independent of it.

## Which lemma does this advance, and what is the first case still open?

**L1.** The review confirms a negative result. On the six-reflex two-gate chart with its prescribed pins, no finite list of vertical itineraries with bounded axial reversals gives an H(C)-type bound. The reason is the half-period mismatch: 2a ∈ Nℤ at both ends, against a target residue of N/2. The bound is proved for all N, and the witness is proved for all even N.

**First case still open.** Does a finite list over **both** decompositions certify lighting on this chart? Equivalently, is there a family in this chart where every witness has unboundedly many axial **and** transverse reversals? In the present family, the transverse-monotone itinerary with 3 events lights every pair. The note's alternative, a bounded list of templates with unbounded repeat counters, is also open. The witness here is one such template: the upper-end roof–floor period, repeated (N−2)/4 times.

**Verification status.**

- **Computed:** claims 2, 3, 4 and 6 at the named N, and claim 7 at N=40.
- **Proved here:** claims 1 (exactness), 2 (all covectors), 5, and 6 for all even N ≥ 4.
- **Inferred only:** the remark that three rows may never occur, and the scope point that two-axis lists stay open.
