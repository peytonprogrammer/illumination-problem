# d192 review: shallow roof return

| Note | Verdict | Confidence |
| --- | --- | --- |
| `l1-shallow-roof-return.md` (primary) | **PASS WITH CORRECTIONS** | High, about 85% |
| `l1-fixed-ratio-corner.md` v2 | d191 Medium 1 **applied in this note**, not in scale-step | High |

No proof step fails. The roof-return route is legal, the bounded winding
period follows from the two d190 failures, and the finite combination with
d190 and d191 is sound. The corrections are about stating what the result
gives at a fixed template, the size of H*, symbol reuse, and one stale
open-case list in the scale-step note.

Date: 2026-11-23. Reviewer: independent referee. Reviewed files:

- [snapshot.md](snapshot.md), sha256 `ac833ca2…ab57ded8`. It's byte-identical
  to `qclass-closure/bbbb/l1-shallow-roof-return.md`.
- [snapshot-fixed-ratio-corner-v2.md](snapshot-fixed-ratio-corner-v2.md),
  sha256 `59f00ced…ad179a`. It's byte-identical to
  `qclass-closure/bbbb/l1-fixed-ratio-corner.md`.

The brief gave the prefix `59f00ced` for snapshot.md. That prefix belongs to
the fixed-ratio v2 snapshot, not to the shallow-roof note. Both files match
their sources, so this is a labeling slip in the brief only.

Reviewed bases: [d191](../d191-review-fixedratio/review.md) (fixed-ratio
corner v1), [d190](../d190-review-scalestep/review.md) (scale step) and
[d189](../d189-review-gateresultants/review.md) (gate resultants). The current
`l1-crossing-scale-step.md` (sha256 `f4bfa23c…`) was read for item (e).

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.29 CPU seconds with exact `Fraction` and integer arithmetic. The log has 23
PASS lines, 28 INFO lines and 0 failures. The simplicity and turn helpers are
copied verbatim from d191.

What the script covers:

- Constants at the st279 values from d190 and d191: n = 1, T = 90,
  η = 1/32400, R = 1, P = 6 and P = 30.
- The period identity (1) on 10,752 integer tuples.
- The floor-failure consequences on 18,661 failing tuples, and the far-wall
  bound q ≤ Q on 945 rational cases.
- The reduction to (2), the r* formula, the rounding and both correction
  bounds, on 2,592 rational cases.
- The interval-clearance lemma on 960 placements, including the tight case.
- The floor-corner exclusion r ≡ −z on 378 cases.
- The constructed route on 162 synthetic closed-form instances that meet the
  note's explicit hypotheses. The three horizontal-level contacts are computed
  in closed form. Nothing is traced.
- The depth-ratio conversion on 3,481 pairs (a,d).
- a = 1, t = 1 at d = 2, 5, 20, 10¹⁹, 10²⁰, 10²¹ and 10³⁰.
- Direct failure implies A ≥ Bη/P, on 7,846 tuples.
- Text checks on fixed-ratio v2 and scale-step against d191's corrections.
- The W=10 ledger realization of LLLRLLLRLR.

No room, ray, direction, slope, reflection-word or room-size search was run.

## Bottom line

**The uniform tail is correct.** In the d190 geometry, with template units
H = h/t and A = a/t, there is an explicit H* such that H > H* lights the pair
at every source depth. The bound is uniform in D, c, u and t. The proof has
two parts:

1. **Shallow sources.** If A/H ≤ ε and H > H₁, the roof–floor–roof route
   lights the pair whenever the d190 floor and far-wall routes fail. Here
   ε = η/(32QP) and H₁ = 64(R+1)/η.
2. **Deeper sources.** If A/H > ε, d190 and ε together put the reduced depth
   ratio θ on a finite list fixed by the template. d191's fixed-ratio
   threshold then applies to each listed ratio. H* is the maximum of these
   thresholds and H₁.

This closes d191's flagged escape, a = 1 with d → ∞, at a fixed template.
With t = 1 and P = 6, the shallow route alone covers every d with
d + 1 > max(H₁, 1/ε), about 4 × 10¹⁹. The log confirms the crossover between
d = 10¹⁹ and d = 10²¹.

**What it doesn't give.** H* is explicit but enormous. The listed ratios reach
denominators near 2K₀/ε, about 10³⁷ at P = 6. d191's exponent there is about
φ(2s), so log₁₀ log₁₀ H* is roughly 37 or more. The residual H ≤ H* is
bounded, not small. Nothing here bounds area for W ≤ 20.

| Claim | Verdict |
| --- | --- |
| Template-unit reduction: lower box [0,X] × [0,H], lower slope equals template speed v + kP | **Correct.** Diagonal scaling divides both axes, and d190's physical speed u(v+kP)/t becomes v + kP |
| One-slab remark: floor window grows with h at fixed a, D and upper data | **Correct**, and correctly labeled as D-dependent |
| (1): (2H−A)qP ∈ 2Xℤ with q = 2Dt/g | **Correct.** It holds for every placement. Failure only bounds q |
| Floor failure gives X ≥ (2H−A+B)η/4 and q ≤ 4X/((2H−A+B)η) | **Correct** on 18,661 failing tuples |
| Far-wall failure and H ≥ 1 give X ≤ 16HC²/η, so q ≤ 64C²/η² ≤ Q | **Correct.** It uses 2H − A > H ≥ 1 |
| Reduction of the exact terminal equation to (2) on the positive sheet | **Correct.** The rounded solution meets the unreduced equation exactly |
| First roof r farther than R from Xℤ is solid and corner-free | **Correct.** Every roof opening is within R of 2Xℤ after unfolding, by the d190 span hypothesis |
| Floor corner would force r ≡ −z (mod 2X) | **Correct.** The floor contact is the unfolded midpoint |
| r* = (e + c₀ − (2H−A+B)v₀)/2; its range over the middle half has length ≥ Hη/4 | **Correct** |
| An interval of length ≥ Hη/4 with X ≥ Hη/4 has a point at distance ≥ Hη/16 from Xℤ | **Correct.** The tight case gives exactly Hη/8 |
| Rounding: \|v − v₀\| ≤ AqP/(L+B), \|r − r*\| ≤ AqP/2 | **Correct.** The r shift is AqP(j−j*)[1 − 2A/(L+B)] |
| A/H ≤ ε and H > H₁ give v ∈ J and first-roof clearance > R | **Correct.** The margins are η/64 < η/4 and 3Hη/64 > 3(R+1) |
| Uniform in c₀ and X; negative j allowed; covers a/h → 0 with h/t → ∞ | **Correct** |
| a/h > ε gives b ≤ 2K₀/ε; θ = b/(2p+b), reduced before use | **Correct.** 178 small coprime pairs need reduction by 2, and the note says so |
| H* = max(H₁, max H₂) is a finite formula in template data | **Correct.** The list is fixed by K₀ and ε, not by the room |
| Comparable residual: A ≥ Bη/P, H ≤ H*, finite θ and κ lists | **Correct** on 7,846 direct-failure tuples |
| "No absolute area cutoff for L1 follows" | **Correct** |
| Fixed-template finiteness | **True but not stated** (Low 1) |
| First open case | **Correct and complete within this geometry** (Low 2) |

## (a) Legality of the roof-return route

The route launches upward from S. It reflects once on the roof after vertical
travel A, once on the floor after a further H, and arrives in the mouth after
a final H. So L = 2H + A. Side-wall windings are free, and the lower sides are
solid by hypothesis. Only the three horizontal-level contacts can meet a
vertex or an opening.

- **First roof contact.** It lies at unfolded abscissa r = c₀ + Aw, with
  w = v + qjP. Every roof opening is in [0,R], so its unfolded images are
  within R of 2Xℤ. The far roof corner unfolds to X + 2Xℤ. A point farther
  than R from Xℤ is therefore solid roof, away from both corners. X > 2R is
  needed for such points to exist. It follows from X ≥ Hη/4 and H > H₁.
- **Floor contact.** It's at c₀ + (A+H)w, the average of r and the final
  abscissa z + 2Xl. A floor corner would give r + z ∈ 2Xℤ. Since z ∈ (0,R)
  and r is more than R from Xℤ, this is impossible.
- **Final contact.** On the positive sheet the final unfolded abscissa is
  congruent to z modulo 2X. The folded horizontal sense then matches the
  unfolded sense, which is the upper path's forward speed w. The vertical
  sense is upward after the floor. The speed shift v → v + qjP keeps every
  upper contact and the seam z = e − Bv, by d190's unit-band periodicity.
  With v in the open stable interval J, z is strictly inside the mouth.

The exact terminal equation is c₀ + L(v + qjP) ≡ e − Bv (mod 2X). Since
LqPj = (2H−A)qPj + 2AqPj and the first term lies in 2Xℤ, this is (2). The log
confirms on 2,592 cases that the rounded pair (j, v) satisfies the unreduced
equation, not only (2).

On 162 synthetic instances that meet every explicit hypothesis (A/H ≤ ε,
H > H₁, q ≤ Q, X ≥ Hη/4), the closed-form construction passes all five
legality tests. The least first-roof clearance divided by H is about 0.080.
The note's guaranteed margin is 3η/64 ≈ 0.012. With A/H near 1/2, outside the
hypotheses, the construction fails on 13 of 16 instances. That's expected. It
shows the ε condition is doing real work, not that the theorem is wrong.

## (b) Failure gives a bounded winding period

The implication is correct, and the wording "a missed route supplies an exact
period" is slightly loose. Identity (1) holds for every placement, by the
definition q = 2Dt/g. What failure supplies is the bound q ≤ Q:

- The floor route fails, so u(2h−a+tB)η ≤ 2g. Then q ≤ 4X/((2H−A+B)η), and
  q ≥ 1 gives X ≥ (2H−A+B)η/4.
- The far-wall route fails, so D ≤ 4huC²(1+t/L)²/(tη) with L = 2h − a. In
  template units X ≤ 4HC²(1 + 1/(2H−A))²/η. With H ≥ 1, 2H − A > H ≥ 1, so
  X ≤ 16HC²/η.
- Combining, q ≤ 64C²/η² ≤ Q.

Only these two d190 routes are used. The direct route isn't needed here. The
bound q ≤ Q is what makes ε independent of the room, so the step carries the
uniformity.

## (c) H* and its uniformity

**Explicit.** At P = 6, R = 1 and T = 90:

| Constant | Value |
| --- | --- |
| C | 10 + 1/32400 |
| Q | 6,718,505,472,064 (about 10¹²·⁸) |
| ε | about 10⁻¹⁹·⁶ |
| H₁ | 4,147,200 |
| K₀ | about 10¹⁷·⁵ |
| 2K₀/ε | about 10³⁷·⁴ |

At P = 30, 1/ε is about 10²¹·⁴ and 2K₀/ε is about 10⁴¹. H₂(θ) needs d191's
N = M^(1+kφ(2s)) at denominators s up to about 2K₀/ε. So H* is roughly a
double exponential in 10³⁷. It's a closed formula in n, W, P and R, as the
note says. Computing it requires no trajectory or room enumeration.

**Uniform as a/d → 0.** This is the case d191 flagged. Take a = 1 and t = 1,
so A = 1, H = d + 1, p = 1 and b = 2d. d191 alone fails at every d in the log.
Its threshold is about 10¹⁰⁰ at d = 2, 10¹⁹⁷ at d = 5 and 10⁶⁰⁰ at d = 20,
while Y = d + 1. The shallow route covers d + 1 > max(H₁, 1/ε) directly. The
conditions A/H ≤ ε and H > H₁ don't mention D, c, u or t. More generally, any
sequence with a/h → 0 and h/t → ∞ is covered, as the note says.

**Between the two regimes.** For a = 1, t = 1 and d + 1 < 1/ε, the ratio
θ = d/(d+1) is on the finite list. But H₂(θ) is far above d + 1, so these
placements sit in the residual H ≤ H*. The combination proves nothing new
there. At a fixed template, the shallow theorem itself still bounds dark
placements with a = 1: d + 1 ≤ max(H₁, 1/ε), about 4 × 10¹⁹ at P = 6.

## (d) The combination with d190 and d191

**Legitimate.** Assume the placement is dark and H > H*. All three d190
routes fail, so:

- part 1 forces A/H > ε;
- d190 forces p = a/gcd(a,2d) ≤ K₀;
- a/h = 2p/(2p+b) > ε gives b < 2p/ε ≤ 2K₀/ε.

The reduced θ is then one of finitely many ratios, and that list depends only
on template data. H > H₂(θ) satisfies d191's condition (1), including Y ≥ 1,
and d191 lights the pair. That's a contradiction. A maximum over a finite list
fixed in advance by template constants is uniform. The "1 +" in H₂ handles
d191's strict inequality correctly.

**The regime H ≤ H*.** The note doesn't claim it, and it states the residual
correctly:

- Direct failure gives A ≥ Bη/(P − η) > Bη/P, so a/h ≥ Bη/(PH*). The log
  confirms this on 7,846 tuples.
- d190 then bounds p, and the lower bound on a/h bounds b. So θ is on a
  finite list even inside the residual box.
- d191's finite κ list applies for each θ, including H < 1 through
  t/a ≤ P/(Bη).

The residual box is H ∈ (Bη/P, H*], X ≤ κ_max·H, with finitely many θ and κ.

## (e) d191's Medium 1 in fixed-ratio v2 and the scale step

| d191 item | Status |
| --- | --- |
| Medium 1, fixed-ratio Scope: not uniform in θ, diverges as θ → 1 | **Applied.** The Scope says so and links the shallow return. It says "can diverge"; d191 showed it does |
| Medium 1, fixed-ratio Scope: name the residual, bounded a/gcd(a,2d) with d/a → ∞, for example a = 1 | **Not named.** The link to the shallow return now covers it in substance |
| Medium 1, scale-step first-open-cases paragraph: add the θ → 1 residual | **Not applied.** The paragraph still says growing d survives when a/gcd(a,2d) stays bounded, and cites only the fixed-ratio tail |
| Medium 2, scale-step: w/b → 0 and junction outside the hypotheses | **Applied.** Both sentences are now in the scale-step note |
| Low 2, fixed-ratio: cite d190's cone argument for constant θ | Not applied |
| Low 3, fixed-ratio: "no openings other than the labelled mouths" | Not applied |
| Low 4, fixed-ratio: drop the redundant term 4κ₊R/(Hη) | Not applied |

The fixed-ratio note is done for Medium 1. The scale-step note still lists
bounded a/gcd(a,2d) as a surviving case without saying that the fixed-ratio
and shallow notes now cover it above h/t = H*. That's now stale (Medium 1
below).

## (f) First open case

The note's first open case is the comparable-scale product: X and H in
bounded positive intervals, a free source, and possibly high-denominator axis
ratios. This is **correct and complete within the d190 geometry**:

- Above H*, every depth is lit.
- Below H*, θ and κ lie on finite lists, so only the individual rational
  heights of X and H are unbounded.
- The out-of-geometry cases are named: an internally changing template, a
  shrinking aperture and mouths outside the span.

Two clarifications would sharpen it (Low 1 and Low 2):

- **At a fixed template the residual is finite.** With u and t fixed,
  h ≤ tH*, D ≤ u·κ_max·H* and 0 < c < D. So the first open case needs u or t
  to grow, with D/u and h/t bounded. That's a lower box growing in step with
  the template.
- **"Comparable" is in a qualitative sense.** H* is about a double exponential
  in 10³⁷. The note should give the scale so readers don't take the residual
  for a small box.

## Mandatory corrections

### High

None.

### Medium

1. **Scale-step open-case list is stale.** In `l1-crossing-scale-step.md`,
   "First open cases for L1", replace "Growing d survives when a/gcd(a,2d)
   stays bounded, including comparable depths in a fixed rational ratio" with
   the current status. Above h/t = H*, the fixed-ratio and shallow-roof notes
   light every depth. Below it, the surviving case is the comparable-scale
   product. Link the shallow-roof note. This finishes d191 Medium 1, part b.

### Low

1. **State the fixed-template finiteness.** Add one sentence: with u and t
   fixed, a dark placement has h ≤ tH* and D ≤ u·κ_max·H*, so only finitely
   many placements are dark. Also note that a = 1, t = 1 needs only the
   shallow theorem: dark forces d + 1 ≤ max(H₁, 1/ε).
2. **Give the size of H*.** At st279 constants, ε is about 10⁻¹⁹·⁶, H₁ is
   4,147,200 and the ratio list reaches denominators near 10³⁷. So H* is
   roughly a double exponential in 10³⁷. "Comparable" in the open case means
   bounded, not small.
3. **Symbol reuse.** H = h/t here, but d191 uses H = N/s, and H₂ refers to
   d191's (1), which contains d191's H. Q here is ⌈64C²/η²⌉, while d190 uses
   Q = max(1, …) and d191 uses Q = 2rad(M). p and b here are reduced depth
   coefficients, while d191 uses p/q for rationals and d190 uses b for target
   depth. Rename, for example H_d191, Q_w, and (p_θ, b_θ).
4. **Wording in the winding-period section.** "Thus a missed route supplies
   an exact period" should read "identity (1) holds for every placement;
   failure of the floor and far-wall routes bounds q by Q". Also,
   min(1/2, …) in ε is never active, and ⌈K₀⌉ can be ⌊K₀⌋. Both are optional.
5. **Fixed-ratio v2 carry-overs.** Apply d191 Lows 2, 3 and 4. Optionally
   change "can diverge" to "diverges" and name a = 1, d → ∞ as the example.

## Scope

The theorem covers the d190 setting:

- a solid-sided rectangular lower box [0,D] × [0,h] with source S = (c,d);
- one fixed sealed lattice template stretched by integer (u,t), with no
  openings other than its labelled mouths;
- every lower roof opening in [0,uR], with uR ≤ D;
- a stable positive-sheet upper approach with B ≥ 1.

In this setting, h/t > H* forces illumination at every source depth,
uniformly in D, c, u and t. The constants depend only on n, W (through P) and
R. There's no chart-wide H(C), G(C) or census ceiling. The d188 two-gap
product, outside-span openings and drifting marks remain outside, as the note
says.

## What it advances on L1

L1 is the area bound for W ≤ 20 strictly simple lattice rooms. This note
advances the occupied-crossing row.

- It removes the fixed-ratio hypothesis from d191's tail. Large h/t now lights
  every depth, which closes d191's first open case (θ → 1 at a fixed
  template).
- Combined with d190 and d191, a fixed template has only finitely many dark
  placements in this geometry. The note implies this but doesn't state it.
- What remains is one structural case: the lower box grows in step with the
  template, with bounded but high-height aspect ratios.

The constants are astronomically large, and no ledger word changes status. No
area cutoff for W ≤ 20 follows. The advance is a real narrowing inside one
geometry class. I see no basis to move the W ≤ 20 estimate.

## First open case after this note

The smallest open case in this geometry is the comparable-scale product:

- u or t grows without bound;
- X = D/u and H = h/t stay in a bounded box, with H in (Bη/P, H*];
- θ and κ are on finite template-determined lists;
- the source abscissa is free;
- the reduced denominators of X and H are unbounded.

At equal standing outside this geometry are three cases: d188's two-gap
product with a varying template interior, a mouth that shrinks relative to the
template, and a roof opening outside [0,uR] beyond d190's resolved regime.

LLLRLLLRLR (W = 10) remains open as an all-length statement. Its ledger
realization is correct: strictly simple, 10 walls, area 8.
