# d159 review: time-pairing (snapshot 2026-11-22 04:35)

**Verdict: sound with gaps.** Every computation in the note checks out exactly. The joint-interval lemma is true, but it says no more than the one-sided test "the chord slope lies in I_S". The R22 example refutes the converse of the complementary-window test, and the same failure occurs unchanged in the lit room R22-L1-005. Nothing in the note moves the W ≤ 20 existence question.

Files: `checks.py` (exact Fractions; tracer and polygon builder copied from d158; d8 tracer and decider imported unchanged) and `checks.log`. Total CPU time is 1.1 s. The script uses only named rooms (R22-base, R22-L1-005, DB55) and runs no room search. It enumerates directions in a fixed room in two places: §1 (DB55 shots and the stress test) and §1b.

## Chart model used for the checks

`checks.py` cuts each room at every line x = k. At each integer horizontal travel u, a chart records the following:

- The open piece of x = k that the ray meets. This is a door piece or, at a vertical-wall bounce, a wall piece.
- The sheet map y = ε·v + c.

Floor and ceiling bounces follow from consecutive windows on fixed sheets. I_S and I_T are intersections of open intervals in s, so each is an open interval.

## 1. The joint-interval criterion

- **The proof is correct.** For a common slope s, the forward line sits at offset (s−s₀)t₁ from the chord and the backward line at (s₀−s)(D−t₂). These offsets have opposite signs.
  - At a door gate, t₁ = t₂, so the chord passes between the two crossings inside the open gate.
  - At a bounce (horizontal) gate, the chord's transverse monotonicity and the intermediate value theorem put the chord's crossing time between t₁ and t₂.
  - Convexity of each copy then keeps the chord inside the copy.
- **It is an iff, but only in a weak sense.** If a legal chord exists, then s₀ ∈ I_S. Conversely, s₀ ∈ I_S means the chord itself traverses the chart and ends at T′. So these conditions are equivalent:
  - I_S ∩ I_T ≠ ∅
  - s₀ ∈ I_S
  - s₀ ∈ I_T
  - s₀ ∈ I_S ∩ I_T

  The note's added sentence, "their open intersection contains s₀", is the correct formulation. "Overlap" is a correct test but is no stronger than the one-sided test.
- **Endpoints are handled correctly.** Open windows exclude every gate endpoint, so a chord through a corner has s₀ on the boundary of I_S. In R22, s₀ = 2 = sup I_S = inf I_T.
- **Tests:**
  - Three known DB55 shots from (1,1) to (9,1): −37/8 (D = 16), −32/5 (D = 10) and −7/5 (D = 10). Each has s₀ in I_S, in I_T and in the overlap. For −37/8 the values are I_S = (−65/14, −60/13), I_T = (−51/11, −23/5) and overlap (−51/11, −60/13).
  - Stress test: reference rays from a fixed source for 100 directions and D ≤ 10 or D ≤ 8, with every interior lattice target on the final section. The script compares the following four statements: overlap, s₀ ∈ I_S, s₀ ∈ I_T, and "the exact tracer says the chord is legal on this chart". They agree in all instances: 1500/1500 in DB55, 90/90 in R22 and 197/197 in R22-L1-005. No case occurs where s₀ lies outside a non-empty overlap.

## 2. The R22 example (all exact)

- The windows are W₁ = (1,3), W₂ = (3,5), W₃ = (5,6) and W₄ = (7,9), with sheets y = 2−v, v−4, v−4 and 10−v. The source section is (−1,1). The script derives these from the room cells, not from the note.
- I_S = (7/4, 2), I_T = (2, 9/4), s₀ = 8/4 = 2, and the overlap is empty.
- Time pairing:
  - W₁ = (1,3) and the reflected W₃ = (2,3) overlap.
  - W₂ = (3,5) is self-paired and contains the forced midpoint 4.
  - The broken line through (0,0), (1,9/4), (2,4), (3,23/4), (4,8) is symmetric about (2,4) and stays in every window. It crosses the bounce levels 1, 3 and 7 at t = 4/9, 10/7 and 32/9, each inside its required interval.
- Slope 2 (direction (−1,2)): the path is (0,0) → (−1/2,1) → (−1,0) → (−1/2,−1) → (0,0) at u = 2, then stops at the reflex vertex (1,2). The d8 tracer with displacement (−4,8) stops at (1,2) with ok = False.
- Slope 15/8: the d8 tracer with displacement (−4,15/2) gives (2,5/2) with ok = True, which matches the note.
- All four window endpoints, (0,±1), (1,1) and (1,2), are reflex vertices.

## 3. R22-L1-005

- **Same failure.** R22-L1-005 adds the cell (0,−3), which gives 20 walls. The column chart has identical windows and sheets in both rooms, so I_S, I_T and the empty overlap are unchanged. Both tracers reproduce the stop at (1,2) and the endpoint (2,5/2).
- **The room is lit.**
  - d8 `certify` accepts the stored witness as (−24,−16).
  - The d8 decider returns EARLY after 42 states with (0,0)–(2,2) lit. Its own witness is (18,−12).
  - In R22 the same witness fails. The decider returns DONE after 5184 states with the pair dark.
  - The witness path in direction (−3,−2) reaches T at u = 24 and bounces at (1/2,−3) on the new floor.
  - Its chart has s₀ = −2/3 ∈ I_S = I_T = (−15/22, −15/23).
  - In R22 the same direction stops at the vertex (1,−2).

## Gaps

1. **Medium: the two-sided criterion adds nothing.** Overlap is equivalent to s₀ ∈ I_S, so "forcing a common forward/backward slope for the same chart" means exactly "forcing the chord to be legal on that chart". The note's Scope section presents the first as a possible route to a selection proof. It is a restatement, not a reduction. State the lemma as "legal ⟺ s₀ ∈ I_S ∩ I_T (equivalently s₀ ∈ I_S)". Drop the claim that it identifies what interval compatibility "must mean beyond" the window comparison.
2. **Medium: strict gates miss some legal shots.** A legal reflection at a smooth lattice wall point that ends a cut or door lies in no strict-gate chart. The criterion is exact for one chart, but the set of strict charts does not cover every legal shot. In the R22 column chart, the ray from (0,0) in direction (2,3) reflects legally at the smooth point (2,3), which ends a cut. The door (0,1) at x = 4 ends at the smooth point (4,0). An all-itinerary theorem must close these endpoints or choose decompositions whose door endpoints are all vertices. Some rooms, such as an L shape, have no such decomposition.
3. **Low: the end sections are redundant.** The proof uses only gates with t in (0,D). The t = 0 constraint on I_T and the t = D constraint on I_S are satisfied by the chord automatically. Choosing the door piece or the chamber cross-section changes I_T but not the iff. The R22 values do not depend on this choice.
4. **Low: the sign hypothesis matters only for bounce gates.** The "prescribed nonzero transverse sign" hypothesis is needed only when bounces are written as time windows. With door windows on fixed sheets, every slope's interval test is already correct.
5. **Low: one stated range is wrong for L1-005.** "All of this geometry is shared" is slightly false: column 0 is (−3,2) in R22-L1-005, not (−2,2). The windows the chart uses are identical, as verified, so no conclusion changes.
6. **Low: the midpoint test is not a theorem.** The "second midpoint test after truncation" is a correct description of this one ray: it returns to S at u = 2, and the remaining length-2 shot has its midpoint at (1,2). The note does not formulate it as a general test, and it shouldn't be cited as one.

## 4. Scope

- **Refuted:** "a chart is infeasible iff two complementary-time windows have disjoint images under (t,y) ↦ (D−t, S+Y−y)". The R22 chart is infeasible, yet every complementary pair is compatible, and a symmetric broken line meets every window and bounce constraint. The failure is identical in the lit room R22-L1-005. So this chart's failure can't be what makes R22 dark, and a W ≤ 20 lighting proof can't be built from this chart.
- **Proved:** for one strict chart, a legal chord to the fixed image T′ exists iff s₀ ∈ I_S ∩ I_T, which is equivalent to s₀ ∈ I_S. The necessity of disjoint-window pairing (y(t) + y(D−t) = S+Y) is also correct and is trivial.
- **Precise open theorem:** for every strictly simple orthogonal lattice room with W ≤ 20 and every pair of regular lattice points S, T, some itinerary, with its image T′, has s₀ ∈ I_S. Here the itineraries include charts whose gate endpoints are smooth wall points, which gap 2 covers. By the lemma, this is the W ≤ 20 illumination statement itself, restated.
