# d181 review: open-collar gluing and remote-wall return

Date: 2026-11-22. Reviewer: independent referee. Reviewed files:
`d95-review-queue/snapshots/1921/l1-open-collar-gluing.md` and
`l1-remote-wall-return.md`. Cited reviews read: d112, d113, d124, d152, d161.
Linked notes read: effective-chamber, resonant-gluing, adjacent-arm-illumination,
whole-room-decomposition, every-direction, stretch-stability, uniform-tail.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.1 CPU seconds and uses exact `Fraction` arithmetic. `trace()` is copied
verbatim from d175. Rooms are DBas and DB55 from d110 `geom.ROOMS`, and the
d161 six-wall L(3,3,3) hall. Only corridor length or arm length varies. Every
traced velocity is the one a note's construction prescribes. No room, ray,
direction or word search was run.

## Bottom line

| Note / claim | Verdict |
| --- | --- |
| Open-collar theorem: thresholds m, H, Z from d124 | Sound |
| Chamber-to-corridor depth extension (width ≥ 1/(18H²)) | Sound. The true one-leg width is 1/(12H²); 1/(18H²) is conservative |
| Embedding of cap-avoiding witnesses | Sound |
| Case analysis of all pairs | Sound and complete |
| Class where both requirements follow (d161 ends, d112 partial-mouth rectangles) | Sound. The class is narrow |
| Remote-wall return: slope, error identity, bound, phase bookkeeping | Sound. 18/18 exact traces past the threshold reach the target; 2 traces below it miss, as the proof allows |
| Obstruction section | Sound. Crosses are lit by d161. The DB55 top-line stretch has no reviewed all-real-pair result at L=3 |
| Both notes as a whole | **Sound with fixable gaps.** No High gaps. One Medium gap, about explicit thresholds |

Neither note proves L1 or an unconditional N₀. Together they reduce the
fixed-chamber long-corridor tail to a one-chamber condition, stated below as
the open-end condition. They also show that the gluing route alone can't bound
area at W ≤ 20.

## What I verified

### 1. Open-collar theorem

**Thresholds.** d124 uses m = 4·max(area A, area B), H = 1+2F₍₃ₘ₎ and
L ≥ 36wH². A plane set of diameter D has area at most πD²/4 < D². So the note's
m = 4⌈D²⌉ is at least d124's m. H and Z only grow with m, so the note's Z is at
least d124's threshold. d124's theorem then applies verbatim. No monotonicity
argument inside the d124 proof is needed. Also w ≤ D, since the mouth is a
chord of the sealed chamber. On the named rooms (log §1):

| Room | m (d124) | m (note) | digits of Z (d124) | digits of Z (note) |
| --- | ---: | ---: | ---: | ---: |
| DBas | 96 | 208 | 122 | 263 |
| DB55 | 100 | 200 | 127 | 253 |

The diameter-only form roughly doubles the exponent. That cost is harmless for
a tail theorem.

**Chamber-to-corridor depth.** d124 states the one-leg version in one
sentence: phase hs+φ(s)−target, derivative h+a. I checked the arithmetic. The
slope interval I = α ± 1/(12H²) has width 1/(6H²). One leg removes at most one
exceptional slope, so some component has width at least 1/(12H²). The note
uses 1/(18H²), which is the two-leg value and therefore conservative. The
phase range is then at least (z+a)/(18H²). This exceeds 2w at z ≥ 36wH²,
because a > 0. Either image ±t of the target height then gives a legal entry.
The argument never uses the target coordinates, so it covers every real mark.

**Embedding.** The test domain T_A is A plus a strip of width w and depth Z.
A path in T_A that never meets the distal cap uses only A's walls and the
strip's long sides. Both are walls of the assembled room when L ≥ Z. So the
path is legal in the room as it stands. The horizontal-sign remark is also
correct. Inside the strip every wall is horizontal except the cap. So
horizontal velocity keeps its sign after entry until the cap. Consequences:

- A witness for requirement 1 never enters the strip. It can still run along
  the mouth line with zero horizontal velocity. Those points are interior in
  the room.
- A witness for requirement 2 enters once and stops at depth z.

The embedding doesn't need the sign remark. The remark explains why the test
is equivalent to a cap-free statement (Low gap 3).

**Case analysis.** Points lie in A, on A's mouth, in the open corridor, on
B's mouth, or in B. Here's the coverage:

| Pair | Covered by |
| --- | --- |
| A–A | requirement 1 |
| A–(mouth or corridor at depth z < Z) | requirement 2 |
| A–(corridor at depth z ≥ Z, including B's mouth at z = L) | d124 one-leg |
| A–B | d124 all-real cross pair |
| corridor–corridor, mouth–mouth | chord in the closed corridor rectangle |
| B-side pairs | symmetric |

The chord case is right. A chord between two interior points of the closed
corridor rectangle can touch the boundary only along a mouth line. That happens
only if both points lie on the same mouth, which is interior. The list is
complete, including L = Z.

### 2. The class where both requirements follow

**d161 ends.** Suppose T_A is a d161 hall with full-side arms and the cap is
the strip arm's terminal cap. Then T_A is a rectangle, L, T or plus. d161
lights every real pair in it:

- bar pairs and seam pairs use a straight chord;
- adjacent-arm pairs reflect only on the parallel sides of one arm, strictly
  between its mouth and the mark depth.

No d161 shot reaches any cap. So requirements 1 and 2 hold. The d161 review
confirmed contacts only on parallel sides.

I re-ran the d161 construction in L(3,3,3) (log §2). The hall is
[−5,0]×[−2,0] and the upper arm is capped at y=4. The right arm is extended to
a cap at x=1000, with A's mouth at x=1. Six pairs ran, with strip depths 0 to
996:

- 3 cases use the right arm, 1 uses the upper arm, and 2 are direct;
- one path has 3,489 contacts;
- every path reaches its target, touches no cap, and reflects only on
  parallel sides.

**d112 partial-mouth rectangles.** d112's chamber-to-corridor shot reflects
only on the chamber's vertical walls. It enters the door once and reaches depth
z with no strip contact, for every z ≥ 0. Same-chamber pairs use a chord.
Requirements 1 and 2 hold.

**Mixing.** The requirements are per end, so the two end types mix freely.

**Scope.** The class adds only these ends:

- L, T and plus-shaped ends whose mouth spans a full terminal arm;
- rectangles with any mouth.

The pairing of two rectangles is already in d112 at L > 4d. The new cases
cost Z ≈ 10²⁵⁰ on named-size chambers. The note doesn't overstate this.

### 3. Remote-wall return

**Slope formula.** Insert horizontal travel 2(L+d) at each of the m mouth
contacts. Matching the total developed rise sX + 2m(L+d)s to s₀X + 4mkw gives
the stated s.

**Error identity.** With e = (L+d)s − 2kw, each excursion rises 4kw + 2e. The
total rise then gives 2me = −X(s−s₀). This is correct.

**Bound.** s−s₀ = 2m[2kw − (L+d)s₀]/[X+2m(L+d)]. For k nearest
(L+d)s₀/(2w), |2kw − (L+d)s₀| ≤ w. That gives the stated bound. Equality occurs
at a rounding tie: DBas 3f at L=5000 attains it.

**Phase bookkeeping.**

- Outward corridor rise: Ls = 2kw + e − ds, so the phase change is e − ds
  modulo 2w. The entrance height tends to yᵢ − σᵢds₀.
- The bounce is at yᵢ + σᵢe and the exit at yᵢ + σᵢ(e+ds).
- The return adds 2e. The excursion folds an even number of times, so the
  vertical sign is preserved. Horizontal velocity reverses, as at the deleted
  mouth reflection.
- The running error is x(s−s₀) + 2je. That equals (s−s₀)(x − jX/m), so
  |error| ≤ X|s−s₀|, uniformly. It vanishes at x = X, j = m.

All of this checks.

**Exact traces (log §3).** In each case B's far wall spans the whole corridor
height, so Jᵢ = (0,w) and d is B's depth. I built the sealed witness from a
prescribed launch, traced it in the sealed chamber, and read off the mouth
contacts. I then traced the prescribed slope s in the full dumbbell at
L = 30, 101, 2003/3 and 5000.

| Case | Room, A | m | s₀ | d·s₀ | Result |
| --- | --- | ---: | --- | --- | --- |
| 3a | DBas, left | 1 | 1/20 | 1/5 | 4/4 lengths reach T |
| 3b | DBas, left (mouth, left wall, mouth) | 2 | 1/50 | 2/25 | 4/4 |
| 3c | DBas, right (B depth 5) | 1 | 1/30 | 1/6 | 4/4 |
| 3d | DB55, left, downward sign | 1 | 1/25 | 1/5 | 4/4 |
| 3e | DB55, left, floor bounce + 10 wall contacts | 1 | 1/20 | 1/4 | 2/4: L=2003/3 and 5000 reach T |

In every success, the path behaves as predicted:

- it makes exactly m bounces on B's far wall;
- it has no contact with B's horizontal walls;
- its far-wall heights converge to yᵢ;
- the identities hold exactly.

Two controls behave as the note predicts:

- At L=101, keeping the slope s₀ misses T in all four cases checked. In
  DB55 it hits a corner.
- Case 3f in DBas is steep: s₀ = 1/4, d·s₀ = 1 > y = 1/4, so the return
  hypothesis fails. The prescribed slope hits B's horizontal walls and misses
  T at all three lengths, 30, 101 and 5000.

**The 3e misses at L = 30 and 101 are threshold effects, not counterexamples.**
The sealed witness has a wall contact at height 39/20, which is 1/20 below the
mouth lip. At L=30 the error there is 43·|s−s₀| = 0.17 > 1/20. So that contact
moves into the open mouth and the path leaves early. The uniform bound gives an
explicit sufficient length:

- In A: 2mXw/N < μ_A.
- In B: (2mX + X + 2md)w/N < μ_B.

Here N = X + 2m(L+d). For 3e this means L > 1087. In practice L = 2003/3
already works.

### 4. Obstruction section

- r ≤ (20−4)/2 = 8 and at most r+1 = 9 pieces: correct.
- Odd crosses: the area is 16b−16, the arm width is 4 and the wall lengths are
  4 and b−2, with gcd 1 (log §4). Every inscribed rectangle has a side ≤ 4
  (d124 review). A transverse arm cut leaves a complementary chamber of
  diameter at least b. So no corridor longer than Z(D) exists. Correct.
- DB55 top-line stretch: it has 12 walls, chamber width 5, odd H unbounded and
  corridor length 3. Its wall gcds are 1, since 5 and 3 are horizontal and H
  and 2 are vertical. The chamber diameter is √(25+H²). So D, and hence Z, is
  unbounded at W = 12. Correct.
- cov279: d126 and whole-room-decomposition give the cut-independent lower
  bound 2q/3 on the largest attached chamber. Correct as cited.

**Which families are lit by reviewed results:**

- **Odd crosses:** yes, every real pair. They are plus-signs in the d161 class.
  cross-placement and d87 also cover lattice pairs.
- **cov279 stretch:** every same-parity interior lattice pair, by thin-room
  (d127, Sound). Not every real pair.
- **DB55 top-line stretch at L = 3:** I found no reviewed theorem that lights
  every real pair for all odd H.
  - d112 needs L > 20.
  - d124's capped arm covers one growing arm, and here two grow together.
  - d152 states that the L ≥ 21 tail "says nothing" at L = 3.
  - stretch-stability lights only the named pair (2,2)–(4,4), in all three
    classes.

  The note doesn't claim this family is lit. It is the cleanest named W=12
  family outside every reviewed whole-room theorem.

## Gaps

### High

None.

### Medium

1. **Remote-wall return: "sufficiently large L" has no stated value.** The
   proof supplies one immediately, since |error| ≤ X|s−s₀| ≤ 2mXw/N in A.
   Add the explicit condition 2mXw/N < μ_A and (2mX+X+2md)w/N < μ_B. Here μ_A
   is the least gate margin of the reference shot. μ_B is the least clearance
   margin minᵢ dist([yᵢ−ds₀, yᵢ+ds₀], ∂Jᵢ). Without it, 3e looks like a
   counterexample at L = 101. Any later uniformity argument needs this
   formula, because it shows exactly which quantities a diameter-only tail
   must bound: X, m, μ_A and μ_B.

### Low

1. **Open collar, one-leg width.** The one-leg component has width at least
   1/(12H²). 1/(18H²) is valid but is the two-leg constant. Say so, or keep
   it and note that it's conservative.
2. **Open collar, thresholds.** Add one sentence: the note's Z is at least
   d124's because area < D² and H increases with m. The proof then needs
   nothing new from d124.
3. **Open collar, cleaner statement of the test.** Requirements 1 and 2
   together are equivalent to a cap-free condition, with no Z in it. Let A_∞
   be A with its mouth opened onto a semi-infinite strip of width w. The
   condition is that every pair with at least one point in A is lit in A_∞.
   - The sign argument shows that a path in A_∞ entering the strip never
     returns.
   - Depths ≥ Z are covered by d124 in A_∞ as well.

   This form doesn't depend on Z or L, and it is the natural hypothesis for
   induction.
4. **Remote-wall hypothesis wording.** State that each open horizontal run
   from B's mouth to the wall lies in the room's interior for heights in Jᵢ.
   Also state that the wall point is not a vertex. "Ends at a solid vertical
   wall" implies both but doesn't say them.
5. **Remote-wall s₀ = 0 case.** It is asserted in one sentence. It is correct
   when the horizontal line through the contacts is clear to a wall in B and
   back, but give the one-line proof.
6. **Obstruction section, coverage of the families.** Say which families
   reviewed results light. Crosses are lit by d161. cov279 lattice pairs are
   lit by d127. The DB55 top-line stretch at L = 3 has no reviewed all-real
   result. The last point matters for L1, as explained below.

## What this means for L1

**What the two notes give.** Take a room made of two fixed lattice chambers
joined by a straight corridor. The results are:

1. If each end satisfies the open-end condition, every real pair is lit for
   L ≥ Z = 36wH², with H = 1+2F₍₁₂⌈D²⌉₎. This is low gap 3's form of
   requirements 1 and 2.
2. The open-end condition is proved for rectangles with any mouth. It is also
   proved for L, T and plus-shaped ends whose mouth spans a full terminal arm.
3. A same-end pair whose sealed witness uses the mouth with common-depth
   clearance is lit for all large L. The threshold depends on the pair, through
   X, m and the margins.

**What they don't give.** A bound N₀(20):

- Z depends on chamber diameter, not on W. The DB55 top-line stretch shows
  that D is unbounded already at W = 12 with L = 3. Odd crosses and cov279
  show that W ≤ 20 doesn't force any corridor longer than Z(D).
- The remote-return lemma is pairwise, with no uniform threshold over real
  pairs.

**Cleanest statement of what remains.** Any proof of L1 by gluing must
supply all three of the following.

- **(OE) Open-end lemma.** For every end chamber A of a separating corridor
  in a W ≤ 20 room, every pair in A_∞ with a point in A is lit. Failing that,
  every pair dark in A_∞ must be lit by a remote return, with a threshold
  uniform over real pairs. The open case is a nonrectangular end with a pair
  whose sealed shots all need the deleted mirror. The note names it correctly.
- **(WT) Wall-dependent threshold.** Replace Z(D) by a length that depends
  only on W and w, or on another quantity bounded at fixed W. Without (WT),
  a corridor that grows linearly while its chambers grow never reaches the
  exponential Z(D). An example is the DB55 top-line stretch with L and H both
  increasing.
- **(NC) No-corridor rooms.** Prove a separate whole-room theorem for rooms
  with no long separating corridor. Odd crosses already have one (d161).
  cov279 is open for real pairs. The DB55 top-line stretch at L = 3 is open
  for real pairs and is the smallest test case, at 12 walls.

The DB55 top-line stretch, all odd H at L = 3, is the first concrete target
for (NC). It has only 12 walls. Its chambers are rectangles, so (OE) already
holds there. No length threshold can help at a fixed L = 3, so it needs a
direct whole-room argument.
