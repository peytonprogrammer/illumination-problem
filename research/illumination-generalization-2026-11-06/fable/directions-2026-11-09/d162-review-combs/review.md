# d162 review: parallel mouths and stacked halls

Snapshot: `d95-review-queue/snapshots/parallel-mouth-combs.2026-11-22-0525.md`.
Checks: [checks.py](checks.py), output in [checks.log](checks.log). The run takes 96 CPU seconds and uses exact `Fraction` arithmetic. `polygon()`, the tracer and the adjacent-arm constructor are copied from d161. The tracer stops at every vertex, convex or reflex. All rooms are named or explicit class members; no room search was run.

## Verdict

**Sound with gaps.** The half-turn theorem and the one-sided stacked-hall theorem are proved for every pair, and every constructed shot traced correctly. That covers 223 half-turn pairs in 3 dumbbells and 203,790 stacked-hall pairs with a mark at or above the roof in 5 members. The note's chosen shot and its second travel candidate both succeed in all of them. The gaps are a structural claim about DB55, a repeated R22 coordinate error, an unproved one-line DB55 claim, and scope wording.

## 1. Half-turn dumbbell

- **Choice of k.** The ordinate at the mouth is e=(bp+akw)/(a+b)=aw(k+bp/(aw))/(a+b). The nearest integer k to −bp/(aw) gives |k+bp/(aw)|≤1/2, so |e|≤aw/(2(a+b))<w/2. At a tie either integer works. The run hit 44 ties.
- **Center fold.** Every kw folds to the centerline: even k because the fold has period 2w, and odd k because w reflects to 0 about w/2. The developed line meets a wall line y=(m+1/2)w only for 0<x<b, since e≠±w/2. Every corridor contact is smooth.
- **Velocity match.** The second half is t↦R(γ(1−t)) with R(z)=2c−z. Its derivative is +γ′(1−t), so the velocity at the center agrees. The whole path is one straight line in the development. The tracer uses unfolded end 2·(developed center)−S and lands on T in every case.
- **DB55 pair (4,1)–(9,4).** Exact: a=1, b=3/2, p=−3/2, −bp/(aw)=9/4, k=2, e=−1/10. Mouth ordinates are 12/5 and 13/5. The path passes (13/2,5/2), the direction is (5,7), and the 4 contacts are on corridor walls.
- **Exhaustive runs.** Every half-lattice mark in the left chamber was paired with its half-turn image. DB55 has 81 marks, H2 has 77 (w=2, b=3), and H3 has 65 (w=2, b=1/2, corridor flush with one chamber wall). All passed with 0 failures, and both mouth ordinates matched ±e. The largest |e|/(w/2) was 5/6.
- **Control pair (1,1)–(9,1).** Its half-turn partner is (12,4), so it isn't a half-turn pair. The saved path at slope −37/8 with x-travel 16 replays exactly. It crosses the mouths at 5/2 and 21/8, reflects at (13,1/2) and ends at (9,1).
- **x-monotone claim.** The claim is true, but the note gives no proof. Every horizontal wall is on an integer line, so the final ordinate is ±(1+εσ)+2K for total vertical travel σ. Reaching y=1 forces σ∈2ℤ. At half-time the mouth ordinate is then ±(1+εσ/2)+2K, an integer, which can't lie in (2,3).

## 2. Stacked-hall theorem

**Proof read.**

- **Sign choices.** The note picks the far end of the mark's own rectangle, which gives clearance ≥u/2. Parents contain the child's interval, so the clearance persists down to the hall.
- **Floor unfold and side fold.** The unfolded travel is E or E+2A with 0<E≤2A, so |dx/dy|≤4A/D.
- **Clearance and the constant 8.** One mark above the roof gives D>c. A leg from height c+d moves at most 4Ad/D<4Ah/c sideways. The bound 4Ah/c≤u/2 is exactly 8Ah≤cu. The inequality is strict because D>c, so each leg clears its rectangle and every lip strictly.
- **Leg folds.** The leg stays inside (l,r)⊂(0,A), so no side fold occurs during a leg.
- **Roof corners.** The path is at height c only when it crosses a leg, strictly inside a mouth. Side bounces therefore never reach a roof corner.
- **Floor corners.** The two candidates differ by 2Af. Both can be in Aℤ only if f=1/2. The note's argument then shows (X_s+X_t)/2∉Aℤ, which is correct. checks.py asserts this on every pair.

**Coverage of all pairs.**

- **Hall–hall and hall–roof-seam pairs.** Both are chords in the open convex hall.
- **Seam marks.** A mark on a child–parent seam uses the child rectangle, and the child satisfies the inequality. A mark on the y=c seam has a zero-length leg, so either sign works.
- **Same, nested and sibling rectangles.** Two marks in the same or nested rectangles, or in siblings, are handled independently at each end. Equal heights fall under the f=1/2 argument.
- **Conclusion.** The bound is proved for every pair of distinct real interior marks.

**Induction step.** This step is correct and redundant. The direct proof already applies to the final room, because the hypothesis is checked per rectangle. Old paths never touch the roof except inside mouths, so opening a roof interval removes no bounce and adds no corner on them.

**Exact tests.** Every pair with at least one mark at y≥c was tested. Hall–hall pairs are open convex chords and weren't traced. Hall marks were tried with both signs, and both travel candidates were traced whenever neither hit a corner.

| Member | Walls | r | Area | 8Ah/(cu) max | Pairs | Failures (chosen / other) | Max leg shift ÷ (u/2) |
|---|---|---|---|---|---|---|---|
| M1: 2-level + sibling, A=6, c=48 | 10 | 3 | 297 | 1 | 29,638 | 0 / 0 | 18/25 |
| M2: three siblings, A=8, c=64 | 14 | 5 | 521 | 1 | 49,855 | 0 / 0 | 8/11 |
| M3: 2-level (strictly inside) + sibling, A=8, c=64 | 14 | 5 | 522 | 1 | 61,456 | 0 / 0 | 8/11 |
| M4: 3 levels, A=5, c=80 | 10 | 3 | 409 | 3/4 | 43,365 | 0 / 0 | 50/83 |
| M5: four unit teeth, A=9, c=72 | 20 | 8 | 652 | 1 | 19,476 | 0 / 0 | 36/73 |

Every rectangle in M1, M2, M3 and M5 sits at equality somewhere. All contacts are on the floor (0<x<A) or on the hall sides (0<y<c).

**Violating members.**

- **V1, a T shape.** It has A=6, c=12 and a tooth [2,3]×[12,16], with 8Ah/(cu)=16. There, 3,678 of 7,196 chosen shots fail. For 110 pairs, every sign choice fails. The d161 adjacent-arm shot lights all 110, since V1 is a hall [2,3]×[0,12] with full-side arms. The construction fails, but the pairs are lit.
- **V2, the M1 shape with c=24.** The inequality fails by a factor of 2, yet the chosen shot succeeds on all 14,854 pairs. The worst leg shift is 18/13 of u/2, still inside the rectangle. Only the second candidate fails, on 417 shots. The constant 8 is a worst-case bound, not a threshold.

**Two-sided section.** I read the proof. The bounds 3c/4…17c/16, 24A/29>3A/4 and the 8A/c direct slope are correct. One explicit member passed: A=24, c=192, mouths [6,8] and its mirror [16,18], at 16Ah=cu. All 52,848 pairs between a stack mark and the lattice hall points or other stack marks passed.

## 3. Nontrivial at W ≤ 20?

Yes. M2 and M3 have 14 walls (r=5), and M5 has 20 walls (r=8). All three are normalized: the wall-length gcd is 1 on each axis. Their area exceeds 64, so the d69 area criterion makes them BBBB at r≤8.

Other certificates don't cover them:

- **Adjacent-arm.** It covers only rectangles, L's, T's and plus shapes.
- **Terrace induction.** It needs southwest closure, which a comb with gaps lacks.
- **Cross placement.** It covers only odd crosses.
- **Whole-room one-closed-end bound.** It applies only for hall depth c≥4A·T² with T=1+F_(12B−1), about 10^9 here.

So the theorem gives new all-pairs certificates for an infinite metric family of BBBB rooms at W≤20. Every member is a tall hall (c≥8Ah/u), and none of the hard named rooms (R22, DB55, cov2929, cov4181) belongs. This doesn't move the W≤20 estimate.

## 4. R22 and DB55

- **R22-base (22 walls, r=9).** y=1/2 meets the room in (−1,1) and (3,5). The note still says "x>4", which d161 already corrected. The second component is 3<x<5. x=3/2 has components (−3,−1) and (1,3), so the gap −1<y<1 is right. No wall spans the bounding width or height. R22 is outside both hall classes.
- **DB55 (12 walls).** Horizontal rows disconnect, vertical columns are intervals, and neither horizontal side spans [0,13]. The note's one-sided argument is right. However, DB55 is exactly hall [0,13]×[2,3] with roots [0,5] and [8,13] of depth 2 on **both** banks. That is a structural member of the note's own two-sided class. It fails only the metric: 16Ah=416 against cu=5, and the mouths lie outside [13/4,13/3]. The coverage conclusion holds, but its reason is incomplete.

## Gaps

1. **Medium: DB55 coverage reasoning.** "Counterexample to coverage by the two hall theorems" rests on a structural argument that only excludes the one-sided class. DB55 is structurally a two-sided stacked hall. State that it fails the two-sided class only on 16Ah≤cu and on the mouth window [A/4,A/3]. Also say which "two hall theorems" are meant.
2. **Low: R22 coordinate.** The second component of y=1/2 is 3<x<5, not x>4. This repeats the d161 gap 3.
3. **Low: unstated hypotheses.** Root intervals must lie in [0,A], and children flush with a parent side are allowed. State both. The proof uses them, and the tests include flush cases.
4. **Low: x-monotone claim unproved.** The claim is true. Add the parity argument from section 1: integer wall lines force even vertical travel, which forces an integer mouth ordinate at half-time.
5. **Low: induction step redundant.** The per-rectangle hypothesis already makes the direct proof apply to the final room. Present the induction as a remark, not as a proof step.
6. **Low: scope.** Members exist at 14–20 walls and are BBBB, but every member is a tall hall that excludes the named hard rooms. Say so, and say that the constant 8 is sufficient, not sharp: V2 violates the bound by 2× and is still fully lit by the same shot.
