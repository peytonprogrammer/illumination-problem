# d184 review: effective descent and finite exceptional slices

Date: 2026-11-22. Reviewer: independent referee. Reviewed file:
`d95-review-queue/snapshots/1952/l1-gap-hyperplanes.md`. Base:
`l1-growth-modes.md` in the same snapshot, reviewed in
[d182](../d182-review-growthmodes/review.md).

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.43 CPU seconds with exact `Fraction` arithmetic. `trace()` is copied
verbatim from d182. The only room is DBas, with insertions at hand-chosen
cross-sections of DBas. The log has 39 PASS lines, 4 INFO lines and 0
failures. Every traced velocity is either the note's formula slope or an
endpoint slope of the named seed word. The second kind is traced at 3 named
points only, to validate the hand-derived gate list. No room, ray, direction
or word search was run.

## Bottom line

| Claim | Verdict |
| --- | --- |
| (1) Lattice threshold t > XPq − X/M, margin 1/(2q) | Sound. Reproduced 84 and 182 on DBas, and 1171.3 on the d182 two-cut ray |
| (2) Exact fixed-word test | Sound. A hand derivation for DBas agrees with exact traces on all 39 endpoint slopes at 3 points |
| (2) One seed fails only on finitely many affine slices, parallel gaps | Sound. On DBas the failure set is 95 explicit lines in 9 directions |
| (2) Reviewer offsets (n, n+c) | The d182 heuristic was wrong. c=1 is lit by the seed; the failing offsets are c = −4, −5, −6 |
| (3) Perpendicular insertions with disjoint strips | Sound. Note's control reproduced exactly: s=564/1975, (1412,83), 528 reflections |
| Fourier proof of finiteness | Sound. Constants are valid, and two of them are conservative |
| (4) Recursion over exceptional slices | Terminates. The semilinearity claim is correct |
| (4) L2 as seed source | The note's caveat is right but understated. The tested family has area ≥ 48, so L2 holds none of it |
| Note as a whole | **Sound with fixable gaps.** No High gaps. Two Medium gaps |

The note proves a real structural result for L1. For a fixed chart and lattice
marks on retained pieces, the lit set of a parallel or disjoint-perpendicular
gap family is semilinear. It doesn't prove L1. Row 4, the unbounded values of
the fixed gaps, real marks and the seed supply all remain open.

## What I verified

### 1. Explicit lattice threshold

**Margin.** Take a seed between lattice marks with reduced slope p/q. In the
unfolding its line passes through lattice points. At an integer abscissa its
height is a multiple of 1/q. At a cut placed at integer ± 1/(2p), its height is
an odd multiple of 1/(2q). The log checks this at three DBas cuts: x=13/4
(height 33/14), x=25/4 (21/14), and x=49/4, crossed twice (31/14 and 37/14).

- Lattice vertices clear by at least 1/q.
- Cut endpoints sit at integer heights, so they clear by at least 1/(2q).
- So μ = 1/(2q) is a valid common margin.

The horizontal-wall case needs one extra line. A vertical error δ moves a wall
hit by δ/s, with the perturbed s, not s₀. Its clearance 1/p becomes
s/p > 1/(2q) when s > s₀/2. Under the threshold, |s − s₀| < 1/(2Xq) ≤ s₀/2.
So the claim holds (Low 3).

**Bound.** The d182 error at retained abscissa x after weight b is
(x − bX/M)(s − s₀). Its magnitude is at most X|s − s₀| ≤ XMP/[2(X+Mt)].
Requiring this to be less than 1/(2q) gives t > XPq − X/M. The formula is right.

| Ray | X, M, P, q | Threshold | Asserted t | Result |
| --- | --- | --- | --- | --- |
| Corridor, μ=1/7 measured | 14, 1, 2, 7 | t > 84 | (d182) | (d182: 5/5) |
| Corridor, μ=1/(2q) | 14, 1, 2, 7 | t > 182 | 183, 185, 200, 500 | 4/4, seed itinerary kept |
| d182 D1: corridor + right box | 14, 3, 12, 7 | t > 3514/3 ≈ 1171.3 | 1172, 1500 | 2/2 |

The threshold needs lattice marks. The d182 case C seed starts at (1, 3/2),
so the formula doesn't apply to it (Low 4).

### 2. Exact condition for two parallel gaps

**Family.** R(t₁,t₂) is DBas with t₁ added to the left box x-gap and t₂ added
to the corridor. The cuts are x = 13/4 (box height 4, period 8) and x = 25/4
(height 1, period 2). Both follow the note's rule integer + 1/(2p). The seed is
(1,3) → (11,3) with velocity (7,−2). The target moves to (11+t₁+t₂, 3).

**Derivation.** Write D(x) = 3 − y in the positive development, and
N = 14 + t₁ + t₂. The seed's chart gates, in retained x, are these.

| Gate | Condition |
| --- | --- |
| Cut c₁, both banks | D ∈ (−1, 3) |
| Left mouth x=5 | 4s + e₁ ∈ (1, 2) |
| Cut c₂, both banks | 21s/4 + e₁ ∈ (1, 2), and the same plus e₂ |
| Right mouth x=9 | 8s + e₁ + e₂ ∈ (2, 3) |
| Cap x=13 | 12s + e₁ + e₂ ∈ (0, 6) |
| Endpoint | 14s + e₁ + e₂ = 4 |

Here e₁ = t₁s − 8k₁ and e₂ = t₂s − 2k₂. The endpoint gives the note's formula,
s = (4 + 8k₁ + 2k₂)/N. Eliminating e₂ leaves one condition:

> The seed's chart itinerary is realizable at (t₁,t₂) if and only if some even
> m has s = m/N in (8/35, 1/3) and t₁s mod 8 in (1 − 4s, 2 − 21s/4).

The log validates this at (37,61), (45,40) and (120,133). There I traced every
even-m endpoint slope with s in (1/6, 1/3), 39 slopes in all. A slope keeps the
seed's outside contacts and its sheets at all four cut banks exactly when the
condition says so. The first comparison used contacts only, and it disagreed.
A sheet change can hide inside a strip, so the sheet signature is necessary.

**Line criterion.** On the line βt₁ − αt₂ = a, with g = α+β and m = 2j, one
identity holds exactly:

    t₁s = 2αj/g − κs,     κ = (14α − a)/g.

The residues 2αj/g mod 8 form ΔZ, with Δ = gcd(2α, 8g)/g. So the seed fails on
the whole line if and only if no s in the window and no ρ ∈ ΔZ satisfy
1 + (κ−4)s < ρ < 2 + (κ − 21/4)s. If such a pair exists, the seed succeeds for
all large points of the line. The window has length at least 5/7 near
s = 8/35. So directions with Δ < 5/7 never fail. That leaves finitely many
directions, and finitely many offsets in each, since the window sweeps a full
period once |κ| is large.

**Exceptional lines of this seed.** The criterion gives 95 lines.

| Direction (α,β) | Δ | Failing a |
| --- | --- | --- |
| (0,1), line t₁ = a | 8 | 4–23, 39–47 |
| (1,1), line t₂ = t₁ − a | 1 | 4, 5, 6 |
| (2,1) | 4/3 | 7–11, 21–25 |
| (2,3) | 4/5 | 11 |
| (4,1) | 8/5 | 12–22, 39–51, 74, 75 |
| (4,3) | 8/7 | 14–23, 46–49 |
| (4,5) | 8/9 | 18–23 |
| (8,1) | 8/9 | 74–79 |
| (1,0), (4,7), (8,3) | 2, 8/11, 8/11 | none |

This confirms the theorem's structure on DBas. It is a finite union of affine
lines, in more directions than the (n, n+c) offsets.

**Named traces (log §2c).** 14 named points, all consistent:

| Point | Prediction | Exact test | Trace |
| --- | --- | --- | --- |
| (500,495), (1000,995) | line t₂ = t₁−5 | no slope | note slope misses |
| (1000,996) | line t₂ = t₁−4 | no slope | note slope misses |
| (10,500), (10,1001) | line t₁ = 10 | no slope | note slope ends on the corridor floor, short of the target |
| (821,400), (1641,400) | lines (2,1) a=21, (4,1) a=41 | no slope | note slope misses |
| (500,501), (1000,1001) | off all lines (c=1) | 3 and 7 slopes | reaches target with the seed itinerary |
| (1000,1007), (2000,1999) | off all lines | 10 and 26 slopes | reaches target with the seed itinerary |
| (777,1234), (1500,400), (1234,2345) | off all lines | 8, 10, 15 slopes | reaches target with the seed itinerary |

"Note slope" means the formula at trial slope u = s₀. It's a control, not the
note's construction, which chooses u. It succeeds only at (2000,1999).

**The reviewer offsets (n, n+c).** d182 claimed that if c·s₀ is far from PZ,
one seed fails for every n. That's wrong, and the error is in d182, not this
note. The η-box is a sufficient radius, not the true gate window. Inside the
window, s can move up to about 0.1 from s₀, and e₁, e₂ need not be small.

- c = 1 has c·s₀ = 2/7, far from 2Z, yet the seed lights (500,501) and (1000,1001).
- c = −6 has the same distance 2/7 from 2Z, and it fails on the whole line.

The note's sentence, "Offsets (n,n+c) then require cs close to Pℤ when the two
errors must both be small", is true under its hypothesis. That hypothesis isn't
the exact test (Low 1).

**The chart test is stricter than the word.** The cut endpoints sit on smooth
walls. Drop the recorded-sheet requirement at the cuts and treat each strip as
a smooth band. The condition becomes s in (1/6, 1/3) and t₁s mod 8 in
(1 − 4s, 2 − 4s). This band test has 24 exceptional lines, against 95 for the
chart test. At (1000,995) a band slope, s = 580/2009, reaches the target. It
has an extra floor bounce before cut c₂. Line t₁ = 10 fails under both tests
(Medium 1).

**Common P is stronger than needed.** At (1000,1007) the exact test has 10
slopes, but none with m ≡ 4 mod 8. The note's smaller test with common P = 8
fails there. This only enlarges the exceptional cover, so the theorem still
holds (Low 2).

### 3. Perpendicular insertions with disjoint strips

**Formula.** In the retained development, an x-strip leaves a vertical error
e = ts − K. A y-strip leaves a horizontal error f = t/s − B. The retained
displacement must equal the seed's (X, Y):

- X = X_r + Σ_y f
- Y = sX_r + Σ_x e

Eliminating X_r gives the note's s = (Y + Σ_x K + Σ_y t)/(X + Σ_x t + Σ_y B).
The total horizontal travel is the denominator. The log checks the identity
exactly.

**Estimates.** D ≥ X/2 + Σ_x t + Σ_y t/(2s₀), D|s − u| ≤ E, |s − u| ≤ 2E/X.
The x-error is at most ε + E and the y-error at most ε + 16E/s₀. I re-derived
each from |K − ut| ≤ ε, |t − uB| ≤ uε, t ≤ D and t/D ≤ 2s₀. All are correct.

**Hypothesis.** The x-strip of column i meets the y-strip of row j exactly
when cell (i,j) is occupied. So "no occupied cell with both gaps varied" gives
disjoint strips and fixed crossed widths together. After extraction, row 3 of
the growth table satisfies it for the diverging gaps. "Uncrossed gaps are
harmless" needs this hypothesis on every varied gap, crossed or not (Low 6).

**Traces.**

| (t_x, t_y) | K, B | s | Errors e, f | Result |
| --- | --- | --- | --- | --- |
| (1401, 80), the note's control | 400, 280 | 564/1975 | 0.083, 0.142 | (1412,83), 528 reflections. Matches the note |
| (2801, 160) | 800, 560 | 1124/3935 | 0.082, 0.142 | (2812,163), 1054 reflections |
| (4201,241), (2000,123), (700,35), (999,400) | — | — | at least one ≥ 1/2 | INFO: u = s₀ isn't a valid trial slope |

The four INFO points don't contradict the theorem. The theorem chooses u
inside J, and points like t_y = 35 sit near slices where the 1/u phase barely
moves across J.

### 4. Fourier finiteness proof

I checked each step.

- **Bump.** The periodic triangle of half-width ρ has coefficients sinc²(πρh).
  They sum to 1/ρ.
- **Tail.** The product tail is at most k · 2/(π²ρ²K) · ρ^(−(k−1)), which is
  the note's 2k/[π²Kρ^(k+1)].
- **First derivative.** If |A| ≥ 2|B|/min(J)², then |φ′| ≥ π|A|/P and φ′ is
  monotone, since φ″ has fixed sign for u > 0. The sharp bound is 2P/(π|A|).
  The note's 4P/(π|A|) is valid.
- **Second derivative.** Otherwise |φ″| ≥ λ = 4π|B|/[P max(J)³]. The bound
  6/√λ suffices. The note's 10/√λ is valid (Low 5).
- **Positivity.** The average is at least 1 − ρ^(−k) · ρ^k/4 − 1/4 = 1/2.
- **Exceptions.** A form nonzero on the slice that takes one of 2C+1 values
  lies in a proper affine slice. There are finitely many h with |h|∞ ≤ K.

The 95 DBas lines are the concrete form of this cover. Their directions are
the small-denominator resonances Δ ≥ 5/7. The Fourier C is far larger, as the
note says.

### 5. Recursion and semilinearity

**Termination.** Each step does the following.

- Pick the minimal lit points of the current slice inside its orthant. Dickson
  gives finitely many.
- Apply the slice theorem at each one. This leaves finitely many proper
  subslices.
- Recurse on those subslices.

The dimension drops by one at each step, and each level branches finitely. The
tree is finite. Each lit point x is covered: it dominates a minimal base, and
either lies off that base's slices or recurses into a smaller slice containing
it.

**Semilinearity.** Each covered piece is an orthant minus finitely many
hyperplanes, intersected with a slice. That's semilinear, and the lit set is a
finite union of such pieces. Presburger sets are closed under complement, so
the dark set is semilinear too.

**Corollary, not stated in the note.** An infinite semilinear set contains a
ray b + nv with v ≠ 0. So unbounded darkness in such a family gives a full dark
integral ray. The d182 descent then makes that ray dark back to its minimal
member. Within one valid family, L1 reduces to: every integral ray in a valid
direction has a lit member.

**Universality test.** The Presburger procedure terminates for the same
reasons. It relies on the cited fixed-instance decision, which I didn't
re-verify. It needs no L2 input.

**What it needs from L2.** It needs a lit witness at every minimal lit base of
the cone and of every exceptional slice. L2 supplies only rooms of area ≤ 20.

- The two-gap DBas family has area 48 + 4t₁ + t₂, which is never ≤ 20 (log §4).
  L2 holds none of its members. The seed here came from a named shot.
- The W=20 staircase chart has 45 unit cells, so none of its members has
  area ≤ 20 (log §4).
- On DBas, 29 of the 95 exceptional lines have the form t₁ = a. Each needs its
  own lit base, and none is in L2.

So L2 is not a seed source for most families. The universality test, or direct
lighting theorems, must supply the bases (Medium 2).

## Gaps

### High

None.

### Medium

1. **The exact test is chart-dependent and stricter than the word.** Requiring
   recorded sheets at cut banks creates exceptions that the band word doesn't
   have. On DBas that's 95 lines against 24. Cut endpoints lie on smooth
   walls, which matches the note's own threshold-section remark. State the test
   modulo smooth reflections inside each strip's band. Otherwise the recursion
   has to find seeds on 71 avoidable lines.
2. **L2's reach as a seed source is overstated by omission.** "In two parallel
   gaps an L2 seed covers the complement of finitely many explicit lines" is
   true only for families with members of area ≤ 20. Many families have none,
   including this note's own DBas control family and every chart with more than
   20 occupied cells. Say so, and point to the universality test as the
   L2-free route.

### Low

1. **Replace the (n,n+c) sentence with the exact line criterion.** The
   condition isn't "cs near PZ". On DBas, c=1 is lit and c=−4, −5, −6 fail.
   This also corrects d182's "fails for every n" claim.
2. **Per-gap periods.** The common-P test can fail where per-gap periods
   succeed, for example at (1000,1007). Say that per-gap P gives a smaller
   exceptional set.
3. **Wall-hit clearance uses the perturbed slope.** Add that the threshold
   keeps s > s₀/2.
4. **Scope of the lattice margin.** It needs lattice marks. Rational marks
   change q, and real marks have no q.
5. **Oscillatory constants.** 2P/(π|A|) and 6/√λ suffice. The stated
   constants are valid.
6. **Uncrossed gaps.** They are harmless only under the global disjointness
   hypothesis on all varied gaps.
7. **State the dark-ray corollary.** It is the cleanest form of the result for
   L1.

## What this gives for L1

**What it gives.**

1. An explicit one-ray threshold t > XPq − X/M for lattice seeds. It names the
   seed quantities X, M, P and q that a uniform argument must bound.
2. For a fixed chart, lattice marks on retained pieces, and a parallel or
   disjoint-perpendicular family:
   - One seed covers its orthant except finitely many computable slices.
   - The lit set and the dark set are semilinear.
   - Finitely many seeds suffice.
   - Universal illumination is decidable on any Presburger domain, given the
     cited fixed-instance decision.
3. Unbounded darkness in such a family forces a full dark integral ray.

**What remains.**

- **Row 4: perpendicular strips that meet.** The intersection rectangle grows,
  the crossed periods grow, and the phase equations no longer apply.
- **Fixed gaps.** A row 2 or row 3 sequence lies in a cone whose fixed gaps
  take values that are unbounded across sequences. Each value is a separate
  family, so a finite list of decisions doesn't cover a chart.
- **Real marks (L3).** The margin and threshold depend on q. Real marks
  converge without stabilizing and have no lattice margin.
- **Missing seeds.** L2 can't seed families above area 20, as shown above. The
  universality test or a structural lighting theorem must supply the bases.
- **No N₀.** No bound on X, P, q or slice offsets follows from W ≤ 20.

**Natural next test.** Pick one exceptional DBas line, for example t₁ = 10.
Decide it with the universality test, or light one base on it by a named
theorem. That is the first real use of the recursion.
