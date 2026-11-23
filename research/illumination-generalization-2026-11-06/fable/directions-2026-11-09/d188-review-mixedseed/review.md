# d188 review: mixed seeds and the occupied crossing

Date: 2026-11-22. Reviewer: independent referee. Reviewed file:
`d95-review-queue/snapshots/2114/l1-mixed-seed-normals.md`. Reviewed bases:
[d184](../d184-review-gaphyper/review.md) (fixed-period transfer, Fourier
tail), [d186](../d186-review-crossing/review.md) (st279 crossing, gate
congruence, cap budget) and [d187](../d187-review-chartdescent/review.md)
(seed-normal bound, H(C) reduction).

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.73 CPU seconds. `trace()`, `shoot()`, `st()`, `gate()`, `direct()` and
`trace_direct()` are copied verbatim from d186. The log has 42 PASS lines,
2 INFO lines and 0 failures. The only rooms are st(7,5) and st(a,3a) at
a = 7+2n for n = 0, 1, 5, 20, 31, 44, 47 and 100. Each traced velocity comes
from a gate formula: the note's v = 57/2, or d186's floor gate with A = a+2.
Oscillatory averages use fixed quadrature. No room, ray, direction, slope or
word search was run.

## Bottom line

**The note is sound. It has no High gaps and one Medium gap, which the note
itself names.** The fixed-period lemma is correct, and "at least one" is the
best possible conclusion. The st279 counterexample is exact. It refutes the
fixed-period transfer at an occupied crossing, not illumination: the whole
ray is lit by d186's floor route.

| Claim | Verdict |
| --- | --- |
| (1) Oscillatory step: φ'' = 2β/u³, O(λ^(−1/2)), and O(1/λ) when β = 0 | **Correct.** The λ^(−1/2) rate is attained at a stationary point (log §1b) |
| (1) Modes annihilating E × F contribute ≥ 0 | **Correct.** It can be sharpened to (h·b, g·d) ≠ (0,0) (Low 1) |
| (1) Finite kernel cover, then one (h,g) for all of U × V | **Correct** |
| (1) "At least one of h\|E, g\|F nonzero" is best possible | **Yes.** The (1,2), (2,−1) example is right, if ρ < 1/6 (Low 2) |
| (2) U = V = span(1,m) excluded for m > K | **Correct.** Unequal slopes give only min(m₁,m₂) ≤ K |
| (3) Seed (7,5), c = 1, e = −1, v = 57/2: both seam coordinates 1/2 | **Correct.** The exact trace crosses y = 5 once, at z = 1/2, with 50 lateral reflections |
| (3) Every direct ascent fails on a = 7+2n, D = 3a | **Correct for every n.** No primality is needed. Checked at 6 named n |
| (3) Fixed-period phases still match for large n | **Correct.** The bump average is 0.92 at n = 20 and 1.05 at n = 100 |
| (3) d186 lights the pair for a > 93 | **Correct, but understated.** The d186 floor route lights every n ≥ 0 (Low 3) |
| (4) Depth ≤ codim U + codim V ≤ 20; branching 2(2K*+1)^11 | **Correct.** Both are conditional bounds, as the note says |
| (5) Missing input for H(C) | A fixed-period mixed transfer at occupied crossings, with explicit seed constants (section 5) |

The real advance is that a mixed seed needs no slice through the product.
This removes d187's probe obstruction and its circularity: one seed anywhere in
the ambient E × F yields a bounded row on at least one axis. The price is one
row per seed, and the recursion pays it in at most 20 steps. What remains is
geometric. The lemma's hypothesis fails exactly where crossings are occupied.

## 1. The fixed-period lemma

**Setup.** Pick positive integral (z,ζ) ∈ U × V and set (t,τ) = λ(z,ζ) − (b,d).
Every placement λ(z,ζ) is dark, because U × V is a linear dark set. The
argument scales by a common λ only. "Independent integral scaling" is more
than the proof uses (Low 4).

**Oscillatory step.** The mode (h,g) gives the average over J of
e(λφ(u))·A(u), where φ(u) = αu + β/u, α = h·z/P and β = g·ζ/P′. The amplitude
A(u) = e(−(h·b)u/P − (g·d)/(uP′)) is fixed and smooth.

- φ'' = 2β/u³. The log confirms the exact second-difference identity at three
  named points (log §1a).
- If β ≠ 0, φ' is monotone on J. So {|φ'| < δ} is one interval of length at
  most 2δ/min|φ''|. Integration by parts on the rest gives O(1/(λδ)), because
  1/φ' is monotone on each piece. Taking δ = λ^(−1/2) gives O(λ^(−1/2)).
- If β = 0 and α ≠ 0, the phase is linear and the average is O(1/λ).

| Case on J = [1/2, 2] | λ = 30 | λ = 300 | λ = 3000 | Rate |
| --- | --- | --- | --- | --- |
| α = β = 1 (stationary at u = 1) | 0.449 | 0.464 | 0.469 | √λ·\|avg\| constant: λ^(−1/2), attained |
| α = 0, β = 1 | 0.398 | 0.398 | 0.398 | λ·\|avg\| constant: no stationary point |
| α = 1, β = 0 | 0 | 0 | 0 | Closed form \|e(2λ) − e(λ/2)\|/(2πλ\|J\|) = O(1/λ); it is 0 at even λ |

So a stationary point gives no persistent term, as the note says.

**Nonnegative modes.** A mode with α = β = 0 and h·b = g·d = 0 has amplitude
exactly 1. It contributes its coefficient, which is nonnegative. Modes that
annihilate E and F are a special case, because b ∈ E and d ∈ F. Only modes
with α = β = 0 and (h·b, g·d) ≠ (0,0) can block positivity. Without them, the
average is at least 1 − 1/4 − o(1). Some u ∈ J then matches every phase, and
the transfer lights a dark placement. So each positive integral point carries
a retained (h,g) with h·z = 0, g·ζ = 0 and (h·b, g·d) ≠ (0,0). That implies
(h|E, g|F) ≠ (0,0). The K formula is d184's, re-verified by d187. The log
recomputes K = 105 and the tail 0.2470 < 1/4 at k = 2, ρ = 1/4.

**Finite kernel cover.** The characters come from a finite set. Each gives a
product kernel (ker h ∩ U) × (ker g ∩ V), not a hyperplane, because α and β
must vanish separately. The note says "product kernels", which is right.
Rational points are dense in the positive part of U × V, and scaling preserves
the character. So finitely many closed subspaces cover a nonempty open subset.
One of them is all of U × V. That (h,g) annihilates U and V, and is nonzero
on E × F.

**"At least one" is best possible.** Take b = (1,1), z = (1,2) and
h = (2,−1). Then h·z = 0, and h·t = −1 for every λ (log §1d, four named λ).
If both x phases t₁u/P and t₂u/P are within ρ of ℤ, then
2t₁u/P − t₂u/P = −u/P is within 3ρ of ℤ. On a J with dist(u/P, ℤ) > 3ρ the
transfer never fires, whatever the y data. The log checks this exactly at
u = 2/5, 1/2 and 3/5 with P = 1 and ρ = 1/10.

Under a phase-level model where "lit" means "some u matches", U × F is dark
for U = span(1,2). So U × V is dark for every V, including span(1,m) with
m > K. No bounded g annihilates that V. The lemma therefore can't promise both
rows. The example needs ρ < 1/6, because dist(u/P, ℤ) ≤ 1/2 (Low 2).

## 2. The model U = V = span(1,m)

The primitive annihilator of span(1,m) is (m, −1), with height m. With full
ambient factors, a nonzero h or g must be a multiple of (m, −1). For m > K
both must vanish, which contradicts the lemma. So a genuine fixed-period mixed
transfer excludes this product, though neither seed slice meets it. For
slopes m₁ ≠ m₂ the lemma gives only min(m₁, m₂) ≤ K. Both statements are
correct.

## 3. The st279 occupied crossing

**Seed.** st(7,5) is strictly simple, with wall gcds (1,1). S = (4,−2) and
T = (6,6) have the same parity. The area is 71.

- (1 + 7v) mod 10 = 1/2 and (−1 − v) mod 6 = 1/2 at v = 57/2.
- The gate spacing is gcd(10, 42) = 2. The (c,e) = (1,−1) gate values are
  z = 1/4, 1/2 and 3/4, so z = 1/2 is the window midpoint. The gate is
  strictly cleared.
- With v = −3/2 + 6l, the lower leg forces l ∈ 5ℤ. So v = 57/2 is the least
  positive solution. (l = 0 gives the rightward launch v = −3/2.)
- The exact trace of (−57/2, 1) from S reaches T. It makes 50 reflections, all
  on lateral walls: 40 in the lower box and 10 in the (5,6) band. It crosses
  y = 5 exactly once, at x = 9/2, that is z = 1/2.

"Traverses the lower box sideways several times" means 40 crossings of a
width-5 box. That is accurate, if modest.

**The ray a = 7+2n, D = 3a.** The increments from the seed are
(D − 5, a − 7) = (16 + 6n, 2n). The spacing gcd(2D, 6a) = gcd(6a, 6a) = 6a for
every a. The residues ±1 − a and ±1 − 3a reduce to 5a ± 1 and 3a ± 1. All
exceed a + 1 once a > 1. So no primality is needed, as the note says. The log
confirms this, and that `direct()` returns no solution, at n = 1, 5, 20, 44, 47
and 100. Each room is strictly simple with wall gcds (1,1).

**Phases still match.** Each nonconstant mode has (α, β) = (6h/P, 2g/P′) ≠ 0,
so the lemma's averaging applies along the ray. With the seed periods P = 10,
P′ = 6, ρ = 1/4 and J = [1,2], the two-bump average is 0.9221 at n = 20 and
1.0498 at n = 100. So some u matches both phases, yet no direct ascent exists.

**Why the transfer fails.** The true vertical-travel phase is
a/(2Du) = 1/(6u) on the ray, against 7/(10u) at the seed. It is homogeneous
of degree 0 in the growing gaps, so it doesn't oscillate in n. No fixed P′
reproduces it. The note's diagnosis is correct.

**The cap route.** d186 lights every placement outside its residual box. On
this ray, D = 3a lies in the box only for a ≤ 67. At a = 67 the lower bound is
595/3 ≤ 201; at a = 69 it is 210 > 207. So the cap theorem alone lights
n ≥ 31, not only a > 93.

The floor route does better. Its spacing is gcd(2D, 6(a+2)) = 6·gcd(a, 2) = 6
for odd a, below the window a + 3. Floor corners are impossible at st279
(d186). So d186's own argument lights every n ≥ 0. The log traces the floor
velocity from `gate(a+2, D, 1, −1)` at 8 named n. Every trace reaches T, and
its only horizontal contact is the floor.

| n | (a, D) | Floor v | Reflections | In d186 residual box |
| ---: | --- | --- | ---: | --- |
| 0 | (7, 21) | 23/5 | 5 | yes |
| 1 | (9, 27) | 29/6 | 5 | yes |
| 5 | (17, 51) | 107/10 | 9 | yes |
| 20 | (47, 141) | 4172/25 | 115 | yes |
| 31 | (69, 207) | 1259/36 | 25 | no |
| 44 | (95, 285) | 16412/49 | 227 | no |
| 47 | (101, 303) | 2753/52 | 37 | no |
| 100 | (207, 621) | 76124/105 | 487 | no |

At n = 20, 44 and 100 one far-wall reflection precedes the floor contact. The
route class is unchanged.

So the counterexample is exactly what the note claims. The seed itinerary does
not transfer, and the pair stays lit by another route.

## 4. The seed-count recursion

**Depth.** Each successful seed gives a row that is nonzero on the current
ambient factor and vanishes on the dark factor. Restricting to its kernel drops
that factor's dimension by 1 and keeps U × V inside. Both factors contain a
positive point, so dim U, dim V ≥ 1. With at most 11 marked gaps per axis,
codim U + codim V ≤ 10 + 10 = 20. The final rows have height at most
K* = max Kᵢ and cut out U and V rationally. U ∩ ℤ^k is then saturated
automatically, so H(C) ≤ K*.

**Branching.** One axis (2 choices) and one row in [−K*, K*]^11 give
2(2K*+1)^11 children. This overcounts: it includes the zero row and sign
duplicates. Branching on one nonzero row per step is enough. A tree of depth 20
has at most (2(2K*+1)^11)^20 leaves.

**Conditions.** Each step needs a lit seed in the current ambient product with
a valid fixed-period transfer. A wholly dark ambient product ends the branch,
which is correct. The constant K at each step uses k up to 22 crossed
coordinates in both factors, not 11 as in d187 (Low 5). The note states
these conditions.

## 5. Gaps

### High

None.

### Medium

1. **The transfer hypothesis is proved only for disjoint insertions.** d184
   gives it when no occupied cell has both gaps varied. The st279 ray shows it
   fails at an occupied crossing. So the lemma, the U = V model and the
   recursion currently apply only to products whose crossed gaps are pairwise
   disjoint. The note says this in its "First open case" paragraph. The
   Advances line should name the restriction too.

### Low

1. **Sharper conclusion.** State the result as h|U = 0, g|V = 0 and
   (h·b, g·d) ≠ (0,0). This matches d187 Low 3 and shows that E × F enters
   only through the seed.
2. **Sharpness needs ρ < 1/6.** dist(u/P, ℤ) ≤ 1/2, so a J with
   dist > 3ρ exists only if ρ < 1/6. Add the condition.
3. **Cap route understated.** d186's cap theorem lights the ray for n ≥ 31,
   and the floor gate (spacing 6) lights every n ≥ 0. Say "the whole ray is
   lit by the floor route".
4. **Scaling.** The proof uses common integral scaling only. Replace
   "independent integral scaling" with "integral dilation".
5. **k in K.** In the recursion, k counts crossed coordinates in both factors,
   up to 22. State K* with that k.
6. **Conditionality.** The room application depends on d132 and d134, and the
   note labels it. Keep that label in any later citation of the H(C) bound.

## 6. The missing geometric implication for H(C)

The lemma turns one geometric input into H(C). Here is that input.

> **Fixed-period mixed transfer (FPT).** For each chart C there are explicit
> Q(C) and ρ(C) > 0 with this property. Let U × V be a retained dark product.
> Let E × F ⊋ U × V be rational and cut out by rows of height at most K. Then
> E × F contains a lit integral seed (b,d), with a compact slope window J,
> periods P, P′ ≤ Q(C) and radius ρ ≥ ρ(C). For all large nonnegative
> integral (t,τ) ∈ E × F, if the crossed phases tu/P and τ/(uP′) are within ρ
> of ℤ for some u ∈ J, then (b+t, d+τ) is lit.

Given FPT, every step uses K ≤ K* = 1 + ⌈8k/(π²ρ(C)^(k+1))⌉ with k ≤ 22.
Then H(C) ≤ K*, and d187 makes m(U), m(V), G(C) and 81 G(C)² explicit. No
onset bound in λ is needed.

FPT has two parts, and both are open.

- **Fixed periods at occupied crossings.** P and P′ must not depend on (t,τ).
  At an occupied crossing the exit phase is a ratio of growing gaps, such as
  a/(2Du). It is degree-0 homogeneous and doesn't oscillate along rays. No
  fixed-period hypothesis holds for the seed itinerary. Itinerary switching
  repairs st279, but by a gcd argument (d186's floor gate), not a phase
  condition. So the needed result is either a fixed-period transfer for some
  route, chosen per arithmetic class, or a version of the lemma that accepts
  gate congruences whose modulus is bounded on E × F. The st279 floor gate
  has constant modulus 6, so it is of the second kind.
- **Seed constants.** Even where FPT's form holds, no current result bounds
  the seed's q, M and P on each intermediate E × F. Finite flats give
  existence only. L2 doesn't reach the relevant areas (d184 Medium 2).

The smallest test is a doubly proper codimension-2 product at one occupied
crossing. Each factor should be a line in two gaps of its axis, and the
crossing should have two mouths, so the d186 cap budget doesn't apply.

No ledger word changes status. LLLRLLLRLR remains open as an all-length
statement.
