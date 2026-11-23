# d191 review: fixed-ratio corner and lower-period coupling

| Note | Verdict | Confidence |
| --- | --- | --- |
| `l1-fixed-ratio-corner.md` (primary) | **PASS WITH CORRECTIONS** | High, about 85% |
| `l1-lower-period-coupling.md` (secondary) | **PASS WITH CORRECTIONS** | High, about 85% |
| `l1-crossing-scale-step.md` v2 | d190 Medium 1 **partly applied** | High |

No proof step fails in either note. The corrections are about scope and
labels. The main one is that the fixed-ratio threshold isn't uniform in the
depth ratio, and neither note says what that leaves open.

Date: 2026-11-23. Reviewer: independent referee. Reviewed files:

- [snapshot-fixed-ratio-corner.md](snapshot-fixed-ratio-corner.md), sha256
  `36ba40d2…d766f2`
- [snapshot-lower-period-coupling.md](snapshot-lower-period-coupling.md),
  sha256 `7346a98d…bc6846`
- [snapshot-scale-step-v2.md](snapshot-scale-step-v2.md), sha256
  `a9dc5b09…a177ff`

All three are byte-identical to their `qclass-closure/bbbb/` sources. Reviewed
bases: [d190](../d190-review-scalestep/review.md) (scale step v1),
[d189](../d189-review-gateresultants/review.md) (gate resultants),
[d188](../d188-review-mixedseed/review.md) (mixed seeds) and
`doorway-word-bound.md` (the two-rectangle theorem).

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
2.3 CPU seconds with exact `Fraction` and integer arithmetic. The log has 38
PASS lines, several INFO lines and 0 failures. The simplicity and turn helpers
are copied verbatim from d190.

What the script covers:

- Residue and coprimality claims for N at all 277 reduced ratios r/s with
  s ≤ 30 and k ≤ 3. This includes θ = 1/3, the note's a = 2d case.
- The corner-targeting lemma, checked exhaustively. For each small admissible
  N up to 512, it covers every reduced p/q with q ≤ N, three j windows and
  every earlier level.
- The clearance μ, the joining equation, the correction and the displacement
  bound, on fixed grids.
- The aspect reduction κ ∈ [κ₋, κ₊] on about 115,000 grid tuples.
- The explicit k, N and threshold at the d190 constants: n = 1, T = 90,
  P = 6 for st279, R = 1.
- The comparable-region arithmetic and the (m+1)/m example.
- The coupling note's gcd and resultant steps on synthetic grids. The note's
  junction at even n = 2 to 10, and its congruence obstruction.
- Text checks on scale-step v2 against the d190 corrections.
- The W=10 ledger realization of LLLRLLLRLR.

Nothing is traced. No room, ray, direction, slope, reflection-word or
room-size search was run.

## Bottom line

**Fixed-ratio corner.** The theorem is correct with its stated constants. At
a fixed depth ratio θ = d/h = r/s, if both d190 routes fail, then
κ = (D/u)/(h/t) lies in [κ₋, κ₊]. Then the corner-target route lights the pair
once

    Y = h/t ≥ 1   and   κ₋Y > 8RN³.

The bound is uniform in ξ, D and u, as claimed. The key step is
number-theoretic: an auxiliary corner target at vertical travel H = N/s. N is
a power of M = 3s−r chosen so that N ≡ s−r (mod 2s). A CRT choice of the
column j keeps every earlier level 1/(4N³) away from a lattice corner. The
proof is complete. The checks confirm it exhaustively at small N.

**What it closes.** For a fixed template, every fixed ratio has only finitely
many dark placements. That closes d190's named open case "a = 2d with the
template fixed". It doesn't close the regime where h/t stays bounded, and it
isn't uniform in θ. The threshold blows up as θ → 1. So bounded a/gcd(a,2d)
with d/a → ∞ survives both d190 and this note, even at a fixed template
(Medium 1).

**Lower-period coupling.** The proposition is correct: a wholly dark product
forces D ∝ u, or both a ∝ t and d ∝ t. The gcd-divides-determinant step and
the resultant step are exact. The junction example is correct. It sits
outside the fixed-template hypothesis, and the body says so. One phase example
has D < u, which clips a lattice mouth (Low 1).

## Note 1: the fixed-ratio corner theorem

| Claim | Verdict |
| --- | --- |
| Hypotheses inherited from d190: span, no extra openings, positive sheet, z₀ ∈ (0,R), B ≥ 1, signed J | **Stated and used correctly.** The wording differs slightly from v2 (Low 3) |
| θ = r/s, H = N/s, l = (N−s+r)/(2s) a nonnegative integer, 1+2l−θ = H | **Correct.** Holds for 1108 (r/s, k) cases |
| N = M^(1+kφ(2s)) ≡ s−r (mod 2s), gcd(N,s) = 1, same primes as M | **Correct**, including the even-M case, where s is odd |
| v₀ = κ(2j−ξ)/H; j window of length Hη/(4κ) > Q | **Correct** |
| CRT restrictions give gcd(2jq−p, N) ≤ 2, so no corner at p/q for 1 ≤ l′ < N/s | **Correct.** Exhaustive at N = 5, 7, 8, 9, 11, 13, 125 and 512 |
| Clearance μ = 1/(4N³) via 1/N² Farey separation and slope s·l′/N ≥ 1/N | **Correct.** Minimum observed: 1/128 at N = 8 |
| Joining equation, correction v−v₀ = κ(e−Bv₀)/(HX+κB), displacement < R/X | **Correct.** Exact on 972 grid cases |
| X > 4κ₊R/(Hη) keeps v ∈ J; X > 2R/μ keeps earlier contacts off corners and mouths | **Correct** |
| Aspect reduction: direct failure gives κ ≥ κ₋; far-wall failure and Y ≥ 1 give κ ≤ κ₊ | **Correct.** Holds on 53,856 and 61,560 failing tuples |
| Explicit k makes Hη/(4κ₊) > Q | **Correct.** At the d190 constants, k = 16; the least admissible k is 8 |
| (1) is uniform in ξ, D and u; covers h/t → ∞ even when u and t diverge | **Correct** |
| Uniform in θ | **Not claimed, and false** (Medium 1) |
| Comparable region: q ≤ P/η, κ = (1−θ)Pp/(2q), t/a ≤ P/(Bη), Y ≥ Bη/(P(1−θ)) | **Correct.** Holds on 18,804 tuples |
| Finitely many κ; κ constant on a dark product; D/u and h/t separately constant | **Correct**, with θ fixed on the product (Low 2) |
| (m+1)/m example labeled as a limit of method, not a dark room | **Correctly labeled** |

### The corner-targeting lemma

In unit box coordinates, the target (2j, 1+2l) is an image of the roof corner
(0,h) next to the mouths. At vertical distance l′ below the final level, the
abscissa is 2j − (2j−ξ)s·l′/N. A corner occurs exactly when this is an
integer. Then ξ is rational with denominator at most s·l′ < N, and such
rationals are at least 1/N² apart.

Suppose ξ is within 1/(4N²) of a reduced p/q. Then p/q is critical for column
j at level l′ only if qN divides (2jq−p)s·l′. Since gcd(2jq−p, q) = 1, this
forces q | s·l′. Then N/gcd(N, 2jq−p) divides s·l′, and so divides l′,
because gcd(N,s) = 1.

The CRT choice of j makes gcd(2jq−p, N) ≤ 2:

- Each odd prime of M excludes at most one residue of j.
- If M is even, p is even and q is odd, j is chosen so that jq − p/2 is odd.

Then N/2 ≤ N/gcd < l′ is impossible, because l′ < N/s ≤ N/2. Every other
critical ξ is at least 3/(4N²) away. The affine slope s·l′/N ≥ 1/N gives
μ = 1/(4N³). The log confirms all of this exhaustively. It also shows that the
restriction matters: at N = 8, an unrestricted j in 0..3 puts a corner on an
earlier level for 4 (p/q, j) pairs.

### Moving off the corner

The real seam endpoint is 2j + (e−Bv)/X on the positive sheet. The correction
formula solves the joining equation exactly. With |e−Bv₀| < R,
|v−v₀| < κR/(HX), and every earlier-level displacement is below R/X. Mouths
unfold to within R/X of even integers, because every roof opening is in
[0,uR]. So X > 8RN³ keeps every earlier roof contact off every mouth and
corner. This step uses the d190 span hypothesis.

The far-wall bound κ ≤ κ₊ also needs that hypothesis. The positive-sheet
choice matches the forward template speed and the upward sense at an odd
level. Signed J is handled, because j may be negative.

### Aspect reduction

- **Lower bound.** Direct failure gives u(a+tB)η ≤ gcd(2Dt, auP) ≤ 2Dt. So
  X ≥ ηa/(2t) = (1−θ)ηY/2.
- **Upper bound.** Far-wall failure gives Dδ ≤ 4h with
  δ ≥ tη/[uC²(1+t/L)²]. So κ ≤ 4C²(1+t/L)²/η. With Y ≥ 1, t ≤ h ≤ L, which
  gives κ ≤ 16C²/η.

Both bounds are exact.

### Size of the constants

At n = 1 (T = 90, η = 1/32400), P = 6, R = 1 and θ = 1/3, the note's formula
gives k = 16 and N = 8³³. The threshold is Y > 2.0 × 10⁹⁵. The second term in
(1) is always below R/Q, so it's redundant (Low 4). The theorem is a
qualitative tail, which is how the note uses it.

### Medium 1: the threshold isn't uniform in θ

The constants depend on θ through s, M, N and κ₋ = (1−θ)η/2. As θ → 1,
s → ∞ and κ₋ → 0, so the threshold grows faster than h.

Take a = 1 and d → ∞. Then a/gcd(a,2d) = 1, so d190 gives nothing. Here
κ₋ = η/(2(d+1)), and even N ≥ M = 2d+3 forces Y > 8RM³/κ₋, which is about
4 × 10⁶·d⁴ for large d. But Y ≤ d+1. The log shows this at d = 2, 5 and 20.

So after d190 and this note, the remaining growing-depth placements at a fixed
template have:

- a/gcd(a,2d) ≤ K, the d190 bound, and
- d/a unbounded.

A tall narrow box with the source near the roof is the basic example. The
Scope paragraph should say that constants depend on θ and give no uniform
bound as θ → 1. The scale-step v2 open-case sentence, "For a fixed rational
depth ratio and h/t large…", should name this residual as well.

### The comparable region

Every displayed identity and inequality is correct. The argument for "κ is
constant on a wholly dark product" fixes θ. On a product, θ is fixed because
d190's cone argument forces a fixed a:2d on a wholly dark family. The note
doesn't cite this (Low 2).

The (m+1)/m example is correct arithmetic, and the note labels it correctly.
It isn't a dark room. It's the limit of using the aspect equation factor by
factor. One detail: d190 needs uR ≤ D, so X ≥ R. Then X = (m+1)/m needs
R ≤ 1+1/m. Scaling to R(m+1)/m removes this, and it doesn't affect the point.

### Does it close d190's "growth in a fixed ratio"?

**Yes, for a fixed template.** With u and t fixed and θ fixed, a dark
placement has bounded Y. If Y < 1, it also has a lower bound on Y, and
κ ≤ 4C²(1+P/(Bη))²/η. So it has bounded X, and h and D are bounded. Only
finitely many placements are dark. This is a direct corollary. The note
states the tail but not the finiteness. Adding the finiteness is optional.

**No, when t grows with h.** If h/t stays below the threshold, for example
t ∝ h, the note proves only the arithmetic restrictions. The note correctly
names this comparable regime as remaining.

**No, uniformly in θ** (Medium 1).

## Note 2: lower-period coupling

| Claim | Verdict |
| --- | --- |
| gcd(a,2d) divides 2\|p·d₀ − q·a₀\| on affine rays; zero determinant gives a constant ratio | **Correct.** Holds on 49,000 ray points. The p = 0 ray (a fixed) has bounded a/γ and isn't covered |
| Phase shift AuP/(2Dt) mod 1, order 2Dt/g_A, window u(A+tB)η | **Correct**, from d190 |
| The direct and floor routes need no span bound and tolerate extra roof openings | **Correct.** Both meet the roof first at the seam |
| Proposition: a dark product forces D ∝ u, or a ∝ t and d ∝ t | **Correct** |
| Root-crossing argument: one of k = 1, 2, 3 gives coprime f, g | **Correct.** Holds on 3,584 synthetic form pairs |
| gcd(f(n), g(n)) divides the Bézout constant, or Res(f,g) | **Correct.** Holds on 107,520 evaluations |
| "Needs unrestricted integral multiples before room gcd one" | **Correctly disclosed** |
| Junction: 8 walls, wall gcds (1,1), same-parity interior marks, a/gcd = 2n+1 | **Correct** at n = 2, 4, 6, 8 and 10 |
| Phase orbits of order one; bounded A/(2D) | **Correct** |
| Congruence (A+b)z ≡ ±bD/2 + Ae (mod 2D); impossible when 3A+b ≤ D/2 | **Correct.** Checked for b ≤ 7 and every admissible A at D = 96 |
| Junction lit by the two-rectangle theorem; outside the scaled-template hypothesis | **Correct.** It's two lattice rectangles with full overlap [0,1] |
| Doubly proper: the first proportionality is automatic for homogeneous rank-one forms | **Correct** |
| (D,u) = (m,m+1), (A,t) = (m,m+1): Au = Dt, normals of height m+1 | **Correct algebra.** It's geometrically inconsistent with unclipped mouths (Low 1) |

### The proposition

The proof is complete. Choose x₀ and x₁ with D(x₀)u(x₁) ≠ D(x₁)u(x₀), and y₀
and y₁ separating A/t. Then D(kn) and u(kn) have distinct roots r_D/k and
r_u/k, and t and A have distinct fixed roots. The only possible common roots
of f and g are cross pairs, and each cross pair rules out at most one k. So
one of k = 1, 2, 3 works.

For coprime integer quadratics, gcd(f(n), g(n)) divides Res(f,g) at every
integer n. So g_A stays bounded while the window grows quadratically. The
floor route also clears, using the d190 coset lemma with 2g_L. The
contrapositive is right: if both a and L are proportional to t, so is d.

The note correctly limits this to a whole dark product, not to a failing
sequence. The resultant depends on the chosen vectors, so it gives no bound
on surviving coefficients.

### The junction

All checks pass. The rooms are the eight-vertex junctions lower
[0,D] × [0,h] and upper [1−D,1] × [h,h+2], with D = 16(a+1). In each:

- D/2 > 3L+1.
- Both marks are interior with coordinates (even, even).
- Speed shifts of 2D move the lower phase by the integer A.

The congruence derivation is exact. Fix the identity column at z on both
sides. Then the source image is z − Aw ∈ ±D/2 + 2Dℤ, and the target image is
z + bw ∈ {0,2} + 2Dℤ. Eliminating w gives the stated congruence modulo 2D.
For odd b, its right side is at least D/2 − 2A from 2Dℤ, while
0 < (A+b)z < A+b.

The note's label is right: this shows the detector fails, not that the room
is dark. The two-rectangle theorem in `doorway-word-bound.md` covers these
rooms, because the rectangles share the full side interval [0,1].

The Advances sentence "The lower side-wall period alone gives no
equidistribution" is true as a statement about that method. But the example
lies outside the fixed-template setting, because the door stays at width one
while the upper width grows. The body says so. The Advances line doesn't
(Low 2, which mirrors d190 Medium 1).

### The doubly proper example

Au = Dt holds identically, and with even P, g_A = 2Dt, so the phase has order
one. But D/u = m/(m+1) < 1. Any lattice mouth in the template has a right
endpoint at least 1 in template units. It would then reach past the lower
width D, so the mouth is clipped. Use (D,u) = (m+1,m) and (A,t) = (m+1,m).
The same identity holds with D ≥ u. The note already labels the example as a
test of the phase identity, so this is Low.

## Scale-step v2: d190 corrections

| d190 item | Status in v2 |
| --- | --- |
| Medium 1, Advances line | **Applied.** It now conditions on mouth width divided by target depth tending to 0 |
| Medium 1, section opening and "junction is outside the hypotheses" | **Not applied.** The opening paragraph is byte-identical to v1. No sentence places the junction outside the theorem |
| Low 1, T and W symbol clashes | Not applied |
| Low 2, outside-span opening in the open cases | **Applied** |
| Low 3, template has no openings beyond the labelled mouths | **Applied** |
| Low 4, "offset by one" wording | Not applied |
| Low 5, unused 1 in Q (optional) | Not applied |

v2 also adds a sentence linking the fixed-ratio tail. It's accurate, but see
Medium 1 above. **d190 Medium 1 is half done.** The headline is fixed. The
body still reads as a general obstruction, and it should state that the
junction lies outside the theorem's hypotheses.

## Mandatory corrections

### High

None.

### Medium

1. **Fixed-ratio note: say that the constants aren't uniform in θ, and name
   the θ → 1 residual.** Add to the Scope paragraph: "The constants depend on
   θ = r/s through M, N and κ₋. They give no bound as θ → 1. Bounded
   a/gcd(a,2d) with d/a → ∞, for example a = 1 and d → ∞, isn't covered by
   this note or by d190." Add the same residual to scale-step v2's
   first-open-cases paragraph, next to the new fixed-ratio sentence.
2. **Scale-step v2: finish d190 Medium 1.** In the opening of "Why the
   requested physical-window induction fails", state the condition w/b → 0.
   Add that under the theorem's exact stretch, the physical window is
   (u/t)η. Say that the junction example lies outside the theorem's
   hypotheses.

### Low

1. **Coupling note:** replace (D,u) = (m,m+1), (A,t) = (m,m+1) with
   (m+1,m), (m+1,m). The current example clips a lattice mouth, because
   D < u.
2. **Coupling note:** in the Advances line, scope the equidistribution
   failure to rooms outside the fixed scaled-template hypothesis, as the body
   does. **Fixed-ratio note:** in the product paragraph, cite d190's cone
   argument for why θ is constant on a wholly dark product.
3. **Fixed-ratio note:** use v2's wording for the inherited hypothesis: "the
   upper template has no openings other than the labelled mouths". "No extra
   openings on the sealed upper itinerary" is weaker than what d190 v2 now
   assumes.
4. **Fixed-ratio note:** the term 4κ₊R/(Hη) in (1) is below R/Q < 8RN³, so
   drop it. Optionally, state the fixed-template finiteness corollary. Also
   optionally, give the size of the threshold, which is about 10⁹⁵ at st279
   constants.
5. **Scale-step v2:** carry over d190 Lows 1 and 4, the symbol clashes and
   the "offset by one" wording.

## Scope

**Fixed-ratio corner.** The setting is:

- a solid-sided rectangular lower box;
- a fixed sealed lattice template stretched by (u,t);
- every roof opening in the near-side span [0,uR];
- a fixed depth ratio θ.

In this setting, failure of both d190 routes plus Y above an explicit
threshold forces lighting. There's no chart-wide H(C), G(C) or census
ceiling.

**Coupling.** The setting is the same stretched template, without the span
bound. The conclusion is a restriction on whole dark products only. The
product-flat application is conditional on d132 and d134, as the note says.

## What it advances on L1

L1 is the area bound for W ≤ 20 strictly simple lattice rooms. These notes
advance its occupied-crossing row.

The fixed-ratio note:

- removes the a/gcd(a,2d) divergence requirement at every fixed ratio;
- makes fixed-template, fixed-ratio darkness finite;
- confines dark comparable placements to finitely many κ values.

The coupling note shows that a dark product locks either D/u or both depth
ratios. Together they remove one more dimension from the d188 two-gap product
at this crossing.

Neither note supplies the fixed-period transfer or a uniform constant in θ.
H(C) stays unbounded, and no ledger word changes status. The advance is real
but stays inside one geometry class. I see no basis to move the W ≤ 20
estimate.

## First open case after both notes

The smallest open case uses a fixed template. The depth ratio drifts to 1
while a/gcd(a,2d) stays bounded, for example a = 1 and d → ∞. That's a tall
lower box with the source one unit below the roof, and D/u at most κ₊·h/t.
None of these routes applies:

- d190 gives nothing, because a/γ ≤ a.
- The corner threshold grows faster than h.
- The far-wall route fails while κ ≤ κ₊.

The next case is a fixed ratio with h/t bounded, so t grows with h. Here the
notes prove only the finite-κ restriction. Two cases from the notes remain at
equal standing:

- the coupling note's locked-D/u product;
- the doubly proper rank-one product with high-height coefficients.

LLLRLLLRLR (W = 10) remains open as an all-length statement. Its ledger
realization is correct: strictly simple, 10 walls, area 8.
