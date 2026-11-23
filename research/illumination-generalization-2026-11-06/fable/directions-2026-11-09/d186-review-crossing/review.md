# d186 review: occupied crossings and the cross-cap budget

Date: 2026-11-22. Reviewer: independent referee. Reviewed files:
`d95-review-queue/snapshots/2032/l1-crossing-gap-transfer.md` and
`d95-review-queue/snapshots/2032/l1-cross-cap-budget.md`. Both are identical to
the live copies in `.context/qclass-closure/bbbb/`. Reviewed base:
[d182](../d182-review-growthmodes/review.md) and
[d184](../d184-review-gaphyper/review.md). Context read: `stabilizer-orbits.md`
(st279), `primitive-dark-flats.md` (d133), and the d132, d133 and d134 reviews.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.04 CPU seconds with exact `Fraction` arithmetic. `trace()` is copied verbatim
from d184. `shoot()` is the d109 polygon-edge tracer, adapted to a vertex list.
The log has 53 PASS lines and 0 failures.

The only rooms are the st279 (m=5) crossing slice R(a,D) and the d184 DBas
family. Every traced velocity comes from a formula in the notes or is a
velocity printed in a note. Congruences are solved with modular inverses. No
room, ray, direction or word search was run. The st279 residual wasn't
enumerated.

## Bottom line

| Claim | Verdict |
| --- | --- |
| (1a) Nonsemilinear failure of the one-seam transfer | **Correct.** The gate is an exact iff for that route class. Failure on D ∈ 3aℤ, a prime, is verified at 8 named points. Success at D+P is verified at 3 points |
| (1b) Qualitative all-itinerary descent, one gap per axis | **Correct, but conditional** on the d132 finite-flat theorem and d134 marked algebraicity, which still have open gaps |
| (1c) DBas line t₁=10 lit in full | **Correct for every real t₂ > −4.** All 4 named replays match exactly: slope and reflection count. 4 more named values also pass |
| Separated-scales effective transfer | Plausible. I read it but didn't trace it |
| (2) Cap budget: gate congruence, floor-corner count, (1), far-wall return | **Correct** |
| (2) st279 specialization (a+1)(a+3)/24 ≤ D ≤ 4(a+1), a ≤ 93, D ≤ 376 | **Correct.** One hypothesis isn't met at e = −1, but the proof still holds there (Low 1) |
| (2) Three replay rows | **All reproduced exactly:** velocity, route type and reflection count |
| Both notes | **Sound with fixable gaps.** No High gaps. Two Medium gaps |

The notes give row 4 one effective result and one qualitative reduction. The
effective result is a finite, explicit residual box for one crossing geometry.
The qualitative reduction says that unbounded darkness in a chart forces a dark
family with one whole axis frozen. Neither note gives an explicit G(chart).
The missing input is the same one d133 names: a bound on the dark flats, or an
effective substitute for it.

## 1. l1-crossing-gap-transfer.md

### 1a. Nonsemilinear failure of the exact one-seam transfer

**The room.** R(a,D) has these bands: (4−a,5) × [5−D,5], (5,6) × [4,7],
(6,7) × [5,8] and (7,12) × [7,12]. At (a,D) = (4,5) it is st279, m=5. Its area
is 56 = 2m²+6. The log confirms that R(a,D) is strictly simple, with wall gcds
(1,1), at all 8 named points. S = (4,5−a) and T = (6,6) have the same parity
exactly when a is odd. The two cuts are one gap each in the order chart: the
x-gap from 5−D to 4, and the y-gap from 5−a to 5. They cross inside the lower
square.

**The gate is an exact iff for the direct-ascent class.** Write z = 5−x. The
lower leg needs z − c − av ∈ 2Dℤ, and the upper leg needs a(z − e + v) ∈ 6aℤ.
Adding them gives (a+1)z ∈ c + ae + gcd(2D,6a)ℤ. Conversely, any
representation 2Dk + 6al gives v = e − z + 6l, which satisfies both legs. All
reflections are on open lateral walls. The leg meets y = 5 only at z ∈ (0,1)
and y = 6 only at T, so no corner is reachable. The check constructs (z,v) from
the congruence at (4,5), (7,22), (11,34) and (13,90). The exact trace then
reaches T with only lateral reflections: 6, 70, 110 and 60 respectively.

**The failure family.** Take a prime a > 5 with 3a | D. Then the spacing is 6a.
The residues are 5a ± 1 and 3a ± 1 mod 6a, and all exceed a+1. The log
confirms this for a = 7, 11, 13 and 101 at D = 3a and 6a. If a ∤ D, the
spacing is 2·gcd(D,3a) ≤ 6 < a+1, so the gate opens.

**The Presburger argument is correct.** A quantifier-free Presburger formula
in (a,D) has a period P common to all its congruences. For fixed a, every
linear atom is eventually constant in D. So every row is eventually
P-periodic, with the same P. A prime a > P breaks this at D ∈ 3aℤ versus
D+P. The log shows the pattern at (7; 21 → 23), (13; 78 → 90) and
(101; 303 → 363).

The conclusion is about one route class, not darkness. The note says so. It
is consistent with (1b): the all-word dark set is semilinear, but a single
route's failure set is not. At (7,21) and (101,303) the direct gate is closed,
yet the floor route lights the pair (section 2).

### 1b. The qualitative all-itinerary descent

**The argument is correct, given its inputs.** I checked each link.

1. Separate positive scalings diag(λ,μ) conjugate the billiard flow in
   orthogonal rooms. They preserve the order cell. d133 verified this.
2. Finite flatness comes from d132 §3 and its extension lemma. The dark set in
   a cell C is a finite union of full sets L ∩ C, not of pieces of flats. This
   matters. If a flat were only partly dark (for example, the sector
   x₁ > 2x₂), a lit base elsewhere would not exclude it.
3. The connected scaling group fixes each maximal flat. Common dilation makes
   L linear. Subtracting (x,y) from (2x,y) gives L = Lx × Ly.
4. Take the slice p₀ + t·eₓ + u·e_y. It meets Lx × Ly in a product of two
   sets, each empty, a point, or all of ℝ. So the dark part of the slice is a
   finite union of points, full lines t = tᵢ, full lines u = uⱼ, and possibly
   the whole slice.

**What it concludes, exactly.** Suppose one base point on the slice is lit, in
the same cell. Then the dark set on the slice is a finite set of points plus
finitely many full axis-parallel lines. Three consequences follow:

- Dark at unboundedly many points of the slice implies a dark line. Along that
  line one gap is frozen at a fixed value tᵢ or uⱼ, and the other gap is
  arbitrary in the cell.
- Hence there is a K with t, u > K ⇒ lit, but not t > K ⇒ lit. K is not
  computable from the argument.
- The fiber test is sound. Each dark line t = tᵢ meets the horizontal fiber
  through the base at one point. If both fibers are lit except at finitely
  many checked points, the dark set is finite. Its size and location are still
  unknown.

**The freezing step is correct.** The cell is a product of the x-order cell
and the y-order cell. The flat is a product, and the dark set is all of L ∩ C.
So (xₙ, yₘ) stays dark. Normalization and parity are per axis, so they
persist. With y frozen, every growing gap is on the x-axis. That is the
parallel-gap case of d184 (rows 1–2 of d182). The note correctly says that the
frozen y-datum is unbounded across the family. So this reduction gives no
finite census.

**The st279 slice.** At (4,5) the direct route lights the pair: z = 1/5,
v = 24/5, 6 lateral reflections. So the slice isn't wholly dark. The cap
budget (section 2) gives an explicit result here, stronger than "t, u > K".
Every placement with a > 93 or D > 376 is lit. So the st279 slice has no dark
lines at all, and its residual is an explicit finite box.

**The classifying-map paragraph.** The Schwarz–Christoffel orders check: order
2 at a reflex, 0 at a convex vertex, and a unit times du at either point over
∞. The total is 2r = 2g−2, with 2g+2 = 2r+4 prevertices. The construction is
standard: a hyperelliptic family, labelled sections, a Hodge-bundle lift and
the coarse map. It is still written at sketch level. It doesn't check that the
algebraic structure it builds is the one in which d134 proves E algebraic
(Medium 1).

### 1c. DBas line t₁ = 10

**The proof covers every real t₂ > −4**, that is, every corridor length
L > 0. I checked the three conditions.

- **Backward leg.** The backward leg from T hits the cap at travel 2, the
  portal at 6 and the cap at 10. It then crosses the door at 14. For
  1/14 < s < 1/7, the portal hit is at y = 3 − 6s ∈ (2,3), which is strictly
  inside the solid wall. The door crossing is at 3 − 14s ∈ (1,2). The
  right-box height range (−1,5) is never left, so there are no floor or roof
  contacts.
- **Left leg.** The left leg from S to the door stays in (1,3). It meets the
  door at the same height, 3 − 14s.
- **Corridor gluing.** In the period-2 unfolding the leg enters descending at
  phase 2 − 14s and must leave ascending at the same phase. That gives
  (L+28)s ∈ 2ℤ. The window for (L+28)s has length (L+28)/14 > 2, so it
  contains an even integer. All corridor contacts are at interior points,
  because the leg is at height 3 − 14s ∈ (1,2) at both doors.

| t₂ | s from the note's rule | Reflections, traced | Note |
| ---: | --- | ---: | --- |
| 0 | 1/8 | 4 | 1/8, 4 |
| 56 | 1/11 | 8 | 1/11, 8 |
| 500 | 10/133 | 40 | 10/133, 40 |
| 1001 | 74/1033 | 74 | 74/1033, 74 |
| 1/2 | 8/65 | 4 | (extra) |
| 3 | 4/35 | 4 | (extra) |
| 57 | 8/89 | 8 | (extra) |
| 10007 | 718/10039 | 718 | (extra) |

Every trace has the predicted itinerary: corridor contacts, then the cap, the
portal (above y = 2) and the cap. The d184 unfolded `trace()` agrees in each
case. At t₂ = 500 the lower endpoint 38 is itself even. The "least even above"
rule correctly takes 40. This closes d184's suggested next test for t₁ = 10.
The d112 whole-room claim for t₂ > 56 is outside this check, and I didn't
verify it.

### Separated-scales transfer

The bound Y′ ≤ Y + MtY/X + MP₁/2 follows from |k − tY/(XP₁)| ≤ 1/2. The
second period 2(w+t)P₀ is a common multiple of every doubled run width at that
level. The transposed denominator is at most Y′. The cubic threshold then
follows from the d184 threshold with axes exchanged, dropping the −X/M term.
The argument is consistent with d184, but I didn't trace it. The note says
that the diagonal range is not covered. That statement is correct and
important.

## 2. l1-cross-cap-budget.md

**Gate congruence.** The two leg conditions are b(z − c − Av) ∈ 2bDℤ and
A(z − e + bv) ∈ 2AWℤ. Their sum gives (A+b)z ∈ bc + Ae + 2g_Aℤ, with
g_A = gcd(bD, AW). The converse holds because v is real, so it is free. An
open window of length (A+b)w > 2g_A meets every coset. At st279, 2g_a equals
the crossing note's gcd(2D,6a). The log checks this at (7,21) and (101,303).

**Floor-corner counting.**

- Shifting v by 2DW/g_A preserves both legs, because g_A divides both AW
  and bD. The log checks this at two named parameter sets.
- If g_A > 2dW, the floor abscissa moves by 2dDW/g_A < D. So two consecutive
  choices can't both be at corners.
- If g_A ≤ 2dW, a corner hit forces v = (jD − c)/d. Then z depends only on
  j mod 2d, because the shift is 2AD ∈ 2Dℤ. I ⊂ (0,D) holds at most one point
  per class mod 2D, so at most 2d gate values are blocked.
- The window holds more than (A+b)w/(2g_A) − 1 ≥ (A+b)w/(4dW) − 1 > 2d
  solutions.

**Inequality (1).** The gcd of g_a and g_{a+2d} divides
gcd(aW, (a+2d)W) = W·gcd(a,2d). The lcm divides bD. So
g_a·g_{a+2d} ≤ 2dW·bD. Failure gives g ≥ (A+b)w/2 for both values of A.
Multiplying gives (1). This is correct.

**Far-wall return.** The endpoint equation is
d + s(2D − c − e) − b = (2j+1)h. These are the checks.

- **Corner avoidance.** Consecutive roots change d + s(D − c) by
  2h(D−c)/(2D−c−e). That is in (0,h) because c > e. So two consecutive roots
  can't both hit a far-wall corner. The log checks three named instances.
- **No early escape.** The outgoing leg rises less than 1 while under the
  opening. On the return, roof visits are 2h/s apart, which is more than i+w.
  So the previous roof visit lies to the right of the mouth, on solid roof.
  The roof corner at x = i+w is never hit, because that inequality is strict.
- **Existence.** An open interval of length (2D−c−e)δ > 4h contains two
  consecutive roots.

**Final bounds.** Combine (1) with D ≤ 4(a+d)/δ ≤ 8a/δ. That gives
a ≤ 64bdW/(w²δ). D ≤ 4(a+d)/δ needs only the far-wall step. Both are correct.

**st279 specialization.** The data are c = d = b = w = 1, i = 0, W = 3 and
h = a+1.

- A floor corner forces v = jD − 1, so z = 1 + (a+2)v is an integer. That
  can't lie in (0,1). So (1) holds on failure for every a, and the threshold
  aw > 36 isn't needed.
- With e = −1, δ = 1/2 and 2D − c − e = 2D. Far-wall failure therefore gives
  2D·(1/2) ≤ 4(a+1), which is D ≤ 4(a+1). This is sharper than the general
  8(a+1).
- (a+1)(a+3)/24 ≤ 4(a+1) holds exactly for a ≤ 93. At a = 93 it reads
  376 ≤ 376. At a = 94, 9215/24 > 380.
- Hence D ≤ 376.

The general theorem at these data would give a ≤ 384.

**Replay rows.** The log recomputes each velocity from the gate equation
(floor rows) or the far-wall equation (least odd multiple of h above D). It
then traces each one exactly.

| a | D | Velocity | Recomputed | Route by contacts | Reflections |
| ---: | ---: | --- | --- | --- | ---: |
| 7 | 21 | (−23/5, −1) | z = 2/5, e = −1, l = 1 | Floor first, then lateral walls | 5 |
| 7 | 35 | (−1, 4/7) | 70s = 40 = 5h | One far-wall contact, no other vertical contact | 5 |
| 101 | 303 | (−2753/52, −1) | z = 3/52, e = −1, l = 9 | Floor first | 37 |

At (7,21) and (101,303) the direct gate is closed, because 3a divides D. So
these rows show the floor route covering exactly the failure family of (1a).
The point (101,303) has a > 93, which is consistent with the bound.

## 3. Gaps

### High

None.

### Medium

1. **The all-word result in the crossing note is conditional, and the
   Advances line doesn't say so.** It rests on three inputs:
   - d132's finite-flat theorem, which is conditional on definability.
   - d134's marked algebraicity. d134 still has open gaps: the algebraic
     structure on T, p and q is sketched, and marked EMM rests on one sentence
     in LMW.
   - The note's new classifying-map paragraph, which is also a sketch. It
     doesn't show that its stack-to-coarse map lands in the same algebraic
     structure that d134 uses.

   Label the K-statement, the fiber test and the freezing step "conditional on
   d132/d134".
2. **The freezing reduction moves the problem to d184 slices, but d184 needs
   seeds.** "D184 is effective for each specified fixed-axis slice" requires a
   lit base at the minimal point of each slice and of each exceptional
   sub-slice. d184 Medium 2 shows that L2 can't supply these above area 20.
   The note should state that the seed requirement carries over.

### Low

1. **The st279 specialization violates a stated hypothesis.** With e = −1,
   (i+w)b/(i−e) = 1, not < 1. The proof still holds, for two reasons. First,
   c = i+w, so the outgoing leg never passes under the opening. Second,
   s < 1 gives 2h/s > i+w. Add one sentence. Alternatively, weaken the
   hypothesis to "(i+w−c)⁺·b/(i−e) < 1 ≤ a, and 2h(i−e) > (i+w)b".
2. **The phrase "the route works if and only if"** should say "the
   direct-ascent route class works", to separate it from the floor and
   far-wall routes that the cap note adds.
3. **The cap theorem uses only the +c source image.** This is valid because it
   gives sufficient conditions for lighting, but say so. The ±c images would
   sharpen (1).
4. **The d112 claim for t₂ > 56 is unverified here.** It isn't needed for the
   designated pair.
5. **The separated-scales thresholds weren't traced.** A single named replay
   above the cubic threshold would make the claim checkable.

## 4. What this gives for L1, and what an explicit G(chart) still needs

**What can be assembled now, qualitatively.** Assume the finite-flat theorem
(d132, d134). Fix a chart, and suppose it has dark normalized same-parity
lattice rooms of unbounded area. Then the following holds:

1. Some dark product flat Lx × Ly contains an unbounded subsequence. The
   proof is the freezing step in this note.
2. Freeze one axis. The other axis then carries a dark family with only
   parallel growth. That is d184's setting, and a dark integral ray exists
   (d184 corollary).
3. The flat is dark on all of L ∩ C, so its minimal normalized point is dark.

So "unbounded dark area ⇒ a dark room with gaps ≤ G(chart)" holds with some
G(chart). But this G is only "the largest minimal point over the finitely many
flats". The statement is close to empty unless G is computable. Rows 1–4 add
effective pieces, but they don't make G computable:

- d182: an explicit one-ray threshold, given a seed (X, M, P, q).
- d184: explicit exceptional lines for parallel and disjoint-perpendicular
  growth, given seeds.
- This row-4 work, at two levels:
  - The cap budget gives an explicit residual for one crossing geometry:
    single mouth, fixed end depths, one upper run.
  - The separated-scales transfer covers the two extreme ratios.
  - The comparable-growth diagonal is covered only qualitatively.

**What is missing for an explicit G.** Any one of the following would close
the gap. The first is the cleanest.

1. **A coefficient bound H for dark flats.** d133 names this input. H gives a
   Cramer bound on minimal points, and d133's primitive test handles gcd and
   parity. With H, G is explicit, and rows 1–4 become unnecessary for G. They
   remain useful as certificates.
2. **An effective all-ratio row-4 theorem for general crossings.** It would
   cover k mouths, extra gates on the upper leg, and intermediate swept roofs.
   This is the cap note's own "first open structural case". Its bounds would
   need to be explicit in the fixed gaps only.
3. **A bound on the fixed transverse data.** The freezing step picks the y
   gaps of an arbitrary dark member. Without a bound on which y-datum to
   freeze, d184 gives infinitely many separate decisions. This is the d184
   "fixed gaps" item again, and it reduces to item 1 for the factor Ly.
4. **Seeds and isolated points.** You need a lit base at every minimal base and
   exceptional slice, beyond L2's area ≤ 20. You also need a way to locate
   0-dimensional dark flats. A generic seed doesn't find them, as the note
   says.
5. **Seed constants.** Uniform bounds on X, M, P and q over the chart are
   needed to turn the d182 and d184 thresholds into numbers.

Real and rational marks (L3) are outside all of this, as in d182 and d184.

**Suggested next step.** Extend the cap budget to two mouths on the swept roof,
with explicit dependence on the fixed gaps. This is the smallest case that
tests item 2. It is also the obstruction the cap note names.
