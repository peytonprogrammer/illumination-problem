# d193 review: overlap phase, projective crossing, comparable width bound

| Note | Verdict | Confidence |
| --- | --- | --- |
| `l1-overlap-phase.md` | **PASS WITH CORRECTIONS** | High, about 85% |
| `l1-projective-crossing.md` | **PASS WITH CORRECTIONS** | High, about 90% |
| `l1-comparable-width-bound.md` | **PASS WITH CORRECTIONS** | High, about 80% |

No proof step fails in any of the three notes. The overlap-column route is
legal, the aperture coefficient q is nonzero, the source coordinate drops out
exactly, and the area bound follows with the stated constants. The
corrections are about scope. The main one: the area bound in note 3 covers
rooms that carry a dark pair of one specific type. It doesn't cover every
dark room in the class, because a source inside a template-width column is
still open (Medium 1 on note 3).

Date: 2026-11-23. Reviewer: independent referee. Reviewed files, each
byte-identical to its `qclass-closure/bbbb/` source and matching the brief's
prefix:

- [snapshot-l1-overlap-phase.md](snapshot-l1-overlap-phase.md), sha256
  `0ff49116…b99b36ee2`
- [snapshot-l1-projective-crossing.md](snapshot-l1-projective-crossing.md),
  sha256 `19909ad5…6f9bbd1b`
- [snapshot-l1-comparable-width-bound.md](snapshot-l1-comparable-width-bound.md),
  sha256 `92402b95…a53043b`

Reviewed bases: [d192](../d192-review-shallowroof/review.md),
[d191](../d191-review-fixedratio/review.md),
[d190](../d190-review-scalestep/review.md), and in `bbbb/`:
`l1-gap-hyperplanes.md` (d184 Fourier tail and Presburger test),
`l1-crossing-scale-step.md` (d190 hypotheses), `doorway-word-bound.md`
(two-rectangle theorem), `l1-chart-descent.md` (wall-gcd convention).

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
23 CPU seconds with exact `Fraction` and integer arithmetic. The log has 34
PASS lines, 12 INFO lines and 0 failures. The simplicity and turn helpers are
copied verbatim from d192. The script covers:

- The sheet embedding (lower phase to tall phase adds 0 or 2β) on 456 phases.
- The window constants and their three margin inequalities on 256 parameter
  tuples. The component count N and midpoint clearance on 3,072 cases.
- The mismatch correction on 4,608 synthetic offsets (δ₁, δ₂) with
  |δ| ≤ ρ. No k is searched.
- The Fourier truncation K = 1 + ⌈16/(π²ρ³)⌉.
- Identity (2), consequence (3), the D/u formula, the p = q = 1 cancellation
  and the 2M(M+1) period example.
- The divisor L | Pqw on all 151,090 small tuples that satisfy (1). The
  bounded-mouth bounds on the same tuples.
- The two-generator bound w/u > 1/(BKP) on 31,574 tuples.
- The symbolic family for m = 2 to 79, and a second family where u absorbs L.
- Note 3's reduction L | Pq(jB − iAβ) on 20,621 normalized tuples. The
  explicit bounds and area formula on 17,843 tuples with Δ ≠ 0.
- Vacuity of Δ = 0 when r = 1 and 0 < w < D, on 3,920 cases.
- The complementary and intersection widths, and the source-inside grid step.
- The W=10 ledger realization of LLLRLLLRLR.

No room, ray, direction, slope, reflection-word or room-size search was run.

## Bottom line

**Note 1 (overlap phase).** The construction is correct. In a full-height
overlap column the seam is open, so a monotone flight crosses it any number
of times with only smooth floor and roof contacts. Darkness then forces

    p·Px/(2α) + q·Pε/[2(α+β)] ∈ ℤ,   |p|,|q| ≤ K,   q ≠ 0.

K depends only on the normalized controls, not on ε. The separation step and
its arithmetic limit are correct and correctly labeled.

**Note 2 (projective crossing).** Multiplying (1) by 2umT and reducing modulo
T = m + βn removes the source and the integer j exactly. The result is
L = T/gcd(m,β) divides Pqw. It needs no hypothesis on c/D. The bounded-mouth
theorem follows. The symbolic family is exact and correctly labeled as a limit
of the method, not a dark room.

**Note 3 (comparable width bound).** With gcd(h,t) = gcd(D,u) = 1 and a
template-aligned width rw = iD + ju, the divisor becomes L | Pq(jB − iAβ).
Then Δ ≠ 0 gives h ≤ βS, t ≤ S, D ≤ AβS, u ≤ BS with S = KP|Δ|, and area at
most (Aβ² + VB)S². That's correct. For the d190-type mouth w = ju, Δ = jB is
never zero, so the bound holds however large u grows. The bound is
astronomically large: K is at least a fixed power of d192's H*, which is
roughly a double exponential in 10³⁷ (Low 3).

## Note 1: the overlap-phase lemma

| Claim | Verdict |
| --- | --- |
| Odd number of transverse crossings; any odd number permitted | **Correct.** The seam [D−w, D] × {α} joins the two reflex vertices and separates the room |
| Column legality: floor and roof contacts smooth, entry in (0,α), exit in (α,α+β) | **Correct.** The only vertices on the column boundary are the four corners and the two reflex ends, and the strict gates exclude all of them |
| Lower-to-tall embedding adds 0 or 2β to the unfolded phase | **Correct** on 456 phases |
| Required right-edge phase e − Bσ, invariant under σ → σ + kP | **Correct** as a hypothesis on the upper approach |
| x_min, N, l, m₀, r, ρ positive and independent of ε | **Correct** |
| Longest component midpoint is 4l from its ends; lower phase 4l·x_min from a fold | **Correct** on 3,072 cases |
| Mismatch ≤ 2(2α_max+β)ρ; derivative x + ε + B ≥ B_min; correction ≤ r/4; sheet fixed | **Correct** on 4,608 offsets |
| K = 1 + ⌈16/(π²ρ³)⌉ makes the omitted product mass < 1/4 | **Correct.** d184's tail 2k/(π²Kρ^(k+1)) at k = 2 gives 4/(π²ρ³K), and π²ρ³K > 16 |
| Averaging: q = 0 survivors are nonnegative, so darkness needs a surviving q ≠ 0 mode | **Correct.** It's a necessary condition only, as stated |
| (2) and (3): narrow aperture plus bounded-height z₀ gives α = βp/(q−p), pz₀ ∈ ℤ | **Correct** |
| D/u = 2βnj/[P(q−p)(j−i)], \|n\| ≤ KP(L+1)/(2α_min) | **Correct** |
| p = q = 1 cancellation: z₀ = n + (Pε/2)(1/α − 1/(α+β)) | **Correct** and correctly labeled as a relation among phases |
| Changing upper shape: rational lcm of 2Hᵢ/bᵢ; heights M, M+1 give 2M(M+1), normalized 2(M+1) | **Correct** for M = 2 to 59 |

### Legality of the crossing

The room near the crossing is the octagon formed by the lower box and the
upper wing, with reflex vertices at (D−w, α) and (D, α). The flight is
monotone in x. In the lower wing it meets only the solid floor and roof on
(c, D−w). It enters the column strictly between 0 and α, so it misses the
reflex vertex. Inside the column it meets only the floor y = 0 and the roof
y = α + β at interior abscissas. It leaves strictly between α and α + β, so
it misses (D, α) and (D, 0). Seam crossings inside the column need no test.
The proof uses no claim that three crossings suffice.

### The nonzero aperture coefficient

The first bump is centered at 0, so every q = 0 mode has a nonnegative
coefficient. The constant coefficient is 1, and the truncated tail is below
1/4. If no retained mode with q ≠ 0 survived, the Cesàro average over k would
be at least 3/4. The window construction shows that any k with positive bump
value gives a legal shot, so a dark pair has average 0. Hence a retained mode
with q ≠ 0 survives. The argument would fail if the second bump were also
centered at 0. Centering it at the free target φ is what forces q ≠ 0.

### What ε ≤ 1 is used for

ε enters only the bound x₀ = x + ε ≤ L + 1 in the separation section. The
window constants, the correction and K don't use it. Note 3 relies on this to
allow ε = j ≥ 1. Note 1 should say so (Low 1).

## Note 2: the projective crossing

| Claim | Verdict |
| --- | --- |
| Diagonal (u,t) stretch preserves legality and the normalized slope | **Correct.** Orthogonal reflections are diagonal and commute with the stretch |
| (1) × 2umT gives Pn[p(D−w−c)T + qwm] = 2ujmT | **Correct** |
| gcd(T,n) = 1, gcd(T,m) = gcd(m,β), hence L \| Pqw | **Correct.** gcd(T/g, m/g) = 1 is also needed and holds. The log confirms L \| Pqw on 151,090 tuples |
| Holds for both signs of q and for p = 0; no hypothesis on c/D | **Correct** |
| Bounded mouth: n ≤ KPw₀, m ≤ βKPw₀ | **Correct** |
| κ = A/B listed: D/u = Am/(Bn) with the stated height bounds | **Correct** |
| Anchored ordinates and wall gcd one force h = m, t = n | **Correct** under the stated "if" |
| For each prime of w some wall gap is nonzero modulo it | **Correct.** The gcd of the gaps divides w |
| Presburger slice test is possible under d184's domain conditions | **Correctly labeled.** It's not a run, and it's not a horizontal area bound |
| Symbolic family: (p,q) = (2,1) gives (N−1)/N + 1/N = 1, L = w | **Correct** for every m from 2 to 79. "Odd m ≥ 5" is unnecessary (Low 2) |
| Two-generator presentation: gcd(D,u) = 1, u ≤ Bn, w/u > 1/(BKP) | **Correct** on 31,574 tuples |
| Rational P: L \| P_num·q·w | **Correct** |
| 2s+1 example: lcm(2, (2s+1)/s) = 2(2s+1) absorbs L = 2s+1 | **Correct** for s = 1 to 199 |
| First open case: a second relation with a different wall difference | **Correct** |

### Source elimination

The reduction is exact. Both c and j sit in terms that are multiples of T
after clearing denominators. What's left is T | P·n·q·w·m. Coprimality with n
and the split gcd(T, m) = gcd(m, β) give L | Pqw. The elimination needs c to
be an integer in the same unit as D, u and w. That matches the project's
convention of primitive lattice rooms with lattice marks (see
`l1-chart-descent.md`). The note states this proviso.

### The arithmetic obstruction

The family is exact. With the note's own m, the theorem's numerator and
denominator are m+1 and m, so T = 2m + 1 = w. Then c = m² + m + 1 lies in
(0, D−w), gcd(D,u,w) = 1 and gcd(D,u) = N. The note labels it correctly as a
test of the available equations, not a dark room. The label "limit of
method" is the right one. The family needs the width to carry a factor that
isn't a fixed combination of D and u. The note's remark that a genuine
two-generator presentation forces w/u ≥ 1/(BKP) is correct and isolates
exactly that.

## Note 3: the comparable width bound

| Claim | Verdict |
| --- | --- |
| Wall abscissas in x₀ + Dℤ + uℤ and wall gcd one give gcd(D,u) = 1; likewise gcd(h,t) = 1 | **Correct** |
| D = Am/g, u = Bn/g with g = gcd(Am, Bn) | **Correct** |
| L \| Pqw ⇒ L \| Pq(iAm + jBn) ⇒ L \| Pq(jB − iAβ) | **Correct** on 20,621 tuples. It uses m ≡ −βn (mod L) and gcd(L,n) = 1 |
| h ≤ βS, t ≤ S, D ≤ AβS, u ≤ BS; area ≤ (Aβ² + VB)S² | **Correct** on 17,843 tuples |
| w = ju: Δ = jB ≠ 0; w = D − ku: Δ = −kB − Aβ ≠ 0 | **Correct.** For k = 0, w = D and no lower-wing source exists (Low 2) |
| Intersection widths have one of the two forms | **Correct** |
| Independent rows cannot both have Δ = 0 | **Correct** |
| Δ = 0 means the width is proportional to m/n + β in template units | **Correct.** With r = 1 it can't occur at all for 0 < w < D (Low 1) |
| ε ≤ E in place of 1 | **Correct.** See note 1 above |
| Source inside the column: grid spacing ≤ ℓP; (ℓ + B)η > ℓP suffices | **Correct.** It covers ε < Bη/P, not a template-width column (Medium 1) |
| Independent offset: u can contain factors of L, even for κ = 1 | **Correct**, but not by the cited family (Low 5) |
| Scope: "the stated intersection, not all W ≤ 20 charts" | **Honest**, but the theorem statement needs the pair restriction (Medium 1) |

### When the two-generator hypothesis holds and fails

It holds when the template is anchored at a wall line of the lower box. In
note 1's orientation the column is [D − ju, D], and every template wall sits
at D − ju + u·(template integer). Ordinates are 0, h and h + t·(template
integer). Then every wall displacement lies in gcd(D,u)ℤ or gcd(h,t)ℤ, and
wall gcd one forces both gcds to be one.

It fails when the template carries an independent offset o. Normalization
then gives only gcd(D, u, o) = 1. The log has an explicit case with a
template-aligned mouth: H = (m+1)/m, β = 1, P = 2, u = m(2m+1),
D = (m+1)(2m+1), w = u and c = m. Then (p,q) = (1,2) satisfies (1) for every
m, κ = 1, and gcd(D,u) = L = 2m+1. An offset that restores gcd one on the x
axis defeats note 3 here, even though the mouth is template-aligned. This is
an arithmetic identity, not a dark room.

### Δ = 0 is vacuous when r = 1

Under the stated hypothesis w is an integral combination of D and u, so
r = 1. An integral (i,j) parallel to (B, Aβ) is (B, Aβ)·k/G with
G = gcd(B, Aβ) and k a nonzero integer. Then w ≤ 0 or w ≥ (B/G)D + (Aβ/G)u
> D. A lower-wing source needs 0 < w < D, so Δ ≠ 0 always. The "exceptional
width" paragraph only matters for r > 1, that is, for templates with
fractional coordinates. The log confirms this on 3,920 cases. This makes the
theorem stronger, and the note should say so (Low 1).

### The area bound and its constants

The chain is: dark pair of the covered type → note 1's (1) with |q| ≤ K →
note 2's L | Pqw → L | PqΔ → L ≤ KP|Δ| = S. Every step is exact. K is uniform
because d192 confines dark placements to α ∈ (Bη/P, H*], x ≤ κ_max·H*, and θ
on a finite list. All of note 1's controls are then normalized quantities,
independent of u and t.

The size: ρ ≤ m₀/(8α_max) with α_max up to H*, and K ≥ 16/(π²ρ³). So K is at
least of order H*³/m₀³, and the area bound is at least of order K². At st279
constants H* is roughly a double exponential in 10³⁷ (d192 review). The bound
is explicit but has no practical numerical value.

## Is this the first explicit area bound in a growing-template class?

**Within the occupied-crossing chain, yes, conditionally.** d190 bounds a
ratio. d191 and d192 bound dark placements only at a fixed template (u and t
fixed). Note 3 is the first in this chain to bound u and t together, so the
stretch factor itself can't grow on a dark pair of the covered type. It
depends on note 1's transverse-approach hypotheses and on d192.

**Two qualifications.**

- If the upper template is a rectangle, the room is a two-rectangle union.
  `doorway-word-bound.md` and the eight-wall theorem light every pair there,
  with at most 6HD + 5 reflections. The bound adds content only for
  non-rectangular upper templates (Low 4).
- I didn't audit all 227 `bbbb/` notes for priority. A grep for area bounds
  found `parametric-orbits.md` (a conditional numerical estimate in another
  setting) and `l1-dbas55-top-phase.md` (which lights an unbounded-area family
  outright). Neither is an area bound on dark rooms in a stretched-template
  class. "First" is fair for this chain. I can't certify it for the whole
  project.

## Mandatory corrections

### High

None.

### Medium

1. **Note 3: state the bound per pair type, not per room.** The bound applies
   to rooms carrying a dark pair whose source lies in the lower wing,
   0 < c < D − w, and whose target has the transverse approach. For the
   d190-type mouth w = ju, ε = j ≥ 1. The source-inside paragraph needs
   ε < Bη/P, about 5 × 10⁻⁶ at st279. So in a template-width column it covers
   only sources within ℓ < Bη/(P − η) of the target-side edge. Sources inside
   the column, targets in the column cap and targets whose first side hit
   lies elsewhere are not covered. Put this restriction in the Advances line
   and the theorem statement, not only in "First case still open".
2. **Note 3: state the solid lower wing.** Note 1's window treats the lower
   wing as a strip with period 2α. d190 and d192 allow several roof openings
   in [0, uR] and other attached components. Add the hypothesis that the
   lower roof is solid between the column and every covered source. That
   holds, for example, when the column is the only roof opening on the
   source's side.

### Low

1. **Note 1:** say that ε ≤ 1 is used only for x₀ ≤ L + 1, so the window and
   K hold for ε ≤ E. **Note 3:** add that under its own hypothesis r = 1 and
   Δ = 0 forces w ∉ (0, D), so every lower-wing column has Δ ≠ 0. Keep the
   exceptional-width paragraph for r > 1 only.
2. **Note 3:** k = 0 gives w = D, where no lower-wing source exists. Write
   k ≥ 1 for the lower-wing bound, or route w = D to the source-inside
   paragraph. **Note 2:** "odd m ≥ 5" can be "m ≥ 2". The identities hold for
   every m from 2 to 79.
3. **Note 3: give the scale.** K ≥ 16/(π²ρ³) with ρ ≤ m₀/(8α_max), and
   α_max reaches d192's H*. The area bound is at least a fixed power of H*,
   a double exponential in about 10³⁷ at st279.
4. **Note 3:** add that rectangular upper templates are already lit by the
   two-rectangle theorem (`doorway-word-bound.md`), so the result is new only
   for non-rectangular templates.
5. **Note 3:** "u can contain factors of L, even for κ = 1, and the symbolic
   arithmetic obstruction applies" cites the wrong mechanism. In note 2's
   family gcd(u, L) = 1 and L = w. A family where u absorbs L is w = u,
   u = m(2m+1), D = (m+1)(2m+1), c = m, (p,q) = (1,2). Cite both, or reword
   to "gcd(D,u) or w can absorb L".
6. **Symbol reuse across the three notes.**
   - m is the θ margin in note 1, the numerator of h/t in notes 2 and 3, and
     a family index in note 2, where the theorem's numerator is m + 1.
   - L is the x bound in note 1 and T/gcd(m,β) in notes 2 and 3.
   - B is the upper travel and the denominator of κ. Note 3 writes B_travel
     in places but not in "x + ε + B".
   - S is the source and KP|Δ|. N is the component count and 2m + 3. T is
     d124's first-hit bound and m + βn.

   Rename, for example m_θ, L_x, B_tr, S_Δ.

## Scope

All three notes concern one geometry:

- a lower box with a full-height overlap column;
- strict side gates and an upper wing reached through the column's far
  vertical edge;
- a uniform upper approach with integer period P and integral cap height β.

Note 3 also requires d192's comparable region (which in turn needs d190's
horizontal-mouth approach), anchored template coordinates and wall gcd one
with lattice marks. Within that intersection, and for dark pairs with a
lower-wing source, area is bounded explicitly.

The scope sentence "for the stated intersection, not for all W ≤ 20 charts"
is honest. The intersection is nonempty: an anchored template overhanging
the lower box's side with mouth [0, ju] satisfies both d190's span condition
and the overlap geometry. Nothing here gives a chart-wide G(C), a census
ceiling or a ledger change. The notes say so.

## What it advances on L1

L1 is the area bound for W ≤ 20 strictly simple lattice rooms. These notes
advance the occupied-crossing row in three ways:

- Note 1 supplies a transverse gate relation whose aperture coefficient can't
  vanish.
- Note 2 removes the source coordinate from it exactly, with no hypothesis on
  c/D.
- Note 3 turns this into the first bound in the chain on the stretch factors
  u and t, inside the anchored overlap class.

The comparable-scale product that d192 left open is closed for lower-wing
sources in that class. The constants are astronomically large, the class is
narrow, and no ledger word changes status. I see no basis to move the W ≤ 20
estimate.

## First open case

The notes' list is correct: a usable transverse approach for every residual
source and target, an independent horizontal offset, and a changing upper
shape. In order of proximity:

1. **Source inside a template-width column.** Same rooms as the bound, with
   ε = j ≥ 1. The source-inside argument covers only ℓ < Bη/(P − η). This is
   the smallest gap, because it sits in exactly the rooms where note 3 applies.
2. **Target in the column cap, or an upper first hit outside the portal.**
   This needs another approach theorem.
3. **Independent horizontal offset.** gcd(D,u) or w can absorb L, as both
   families in the log show. A second crossing relation with a different wall
   difference is the natural target, as note 2 says.
4. **Changing upper shape.** This needs a uniform K and control of the primes
   that P shares with L. d182 scale classes supply neither.

LLLRLLLRLR (W = 10) remains open as an all-length statement. Its ledger
realization is correct: strictly simple, 10 walls, area 8.
