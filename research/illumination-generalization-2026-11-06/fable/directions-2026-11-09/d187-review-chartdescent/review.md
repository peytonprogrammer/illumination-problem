# d187 review: chart descent and the seed-normal bound

Date: 2026-11-22. Reviewer: independent referee. Reviewed files:
`d95-review-queue/snapshots/2052/l1-chart-descent.md` and
`d95-review-queue/snapshots/2052/l1-seed-normal-bound.md`. Both are identical
to the live copies in `.context/qclass-closure/bbbb/`. Reviewed base:
[d182](../d182-review-growthmodes/review.md),
[d184](../d184-review-gaphyper/review.md) and
[d186](../d186-review-crossing/review.md). Context read: the
[d132](../d132-review-paramorb/review.md),
[d133](../d133-review-primflats/review.md) and
[d134](../d134-review-markalg/review.md) reviews, `primitive-dark-flats.md`,
`dark-locus.md` and `l1-gap-hyperplanes.md`.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.08 CPU seconds with exact `Fraction` arithmetic. `trace()` is copied verbatim
from d184. The log has 45 PASS lines and 0 failures. The named rooms are DBas,
its axis rescalings, DBas with insertions at the d184 cuts, and the W=10 ledger
room. Every traced velocity is the DBas seed, its rescaled image, a ray aimed at
a named reflex corner, or the note's corrected slope. The trial slope u comes
from a closed nearest-integer formula, not a search. No room, ray, direction or
word search was run.

## Bottom line

Both notes are **sound, with one inherited Medium gap and no High gaps.** Every
step I checked is correct. Neither note makes G(C) explicit, and both say so.

| Claim | Verdict |
| --- | --- |
| (1a) Axis rescalings preserve paths, the order cell and each maximal flat | **Correct.** 6 exact traces map event for event under 3 rescalings |
| (1b) Product splitting via (2x,y) − (x,y) | **Correct** once each flat is linear and fixed |
| (1c) m(U), G(C), area ≤ kₓkᵧ m(U)m(V) ≤ 81 G² | **Correct.** m is attained whenever finite. 81 = 9·9 is right at W ≤ 20 |
| (1d) Two-replacement descent; x₃ = x₁ + x₂ model | **Correct.** The replacement order is irrelevant (Low 1) |
| (1e) Isolated dark rooms are covered | **Correct.** No dark room is isolated in the real dark set. "Isolated" means a rank-one factor, and m covers it |
| (2a) Slope correction, 2E₀ ≤ 1/(4q) | **Correct.** 2 constructed DBas instances trace exactly to the target with the seed itinerary |
| (2b) Fourier argument | **Correct.** It can be sharpened to h·b ≠ 0 (Low 3) |
| (2c) Hyperplane cover gives one h | **Correct** |
| (2d) Iterative full-equation bound | **Correct as stated.** It gives existence of seeds, not bounds on them |
| (2e) Doubly proper product model | **Correct** for every m > 1 |
| L1 consequence | No explicit G(C). The single missing estimate is a factor-height bound H(C) (section 4) |

The new content is real. Chart descent turns d186's qualitative "G is the
largest minimal point" into a closed formula in two one-axis minima. The
seed-normal bound is the first explicit coefficient bound on a dark factor. It
needs no finite-flat input and no onset estimate in λ. On DBas its constant is
K ≈ 7.5·10¹⁰ for the two-gap family and K ≈ 4.5·10²² on the full x space.

## 1. l1-chart-descent.md

### 1a. Axis rescalings

diag(a,b) with a,b > 0 commutes with both axis reflections. It maps lines to
lines and corners to corners of the same type. d133 verified this; I re-checked
it on DBas. Under diag(3,2), diag(1,5) and diag(7/2,1/3), both the seed and a
ray aimed at the reflex corner (5,2) map event for event (log §1). The turn
word is unchanged, and each axis's gap vector scales by its own factor. So the
real order cell is preserved.

The connectedness argument is correct. The group (ℝ₊)² is connected and acts
continuously on the finite set of maximal flats, so each orbit is one point.
The finite-flat input is essential: the toy flat {x = y} moves under
diag(2,1) (log §1).

The note says rescalings preserve "the chart". Its chart includes endpoint
parities, which real rescalings don't preserve (Low 2). The argument only needs
the real cell and the real dark set, so nothing breaks.

### 1b. Product splitting

Common dilation makes each flat L linear. For (x,y) ∈ L, the point (2x,y) is
in L, so (x,0) ∈ L. Thus L = Lₓ × Lᵧ. This needs the d132 extension lemma
that D ∩ C is a union of **full** sets L ∩ C, which d186 confirmed. Then every
positive (x′,y′) ∈ Lₓ × Lᵧ is dark. The order cell is a product of positive
orthants (d132 review), so the concatenation stays in C. Parity and wall gcd
are per axis, so they survive. Log §2 checks the identity on a hand-built
product.

### 1c. m(U), G(C) and the area bound

- **m is well defined.** Each fine gap is a summand of exactly one wall gap,
  because the extremal levels are walls. So ‖Az‖∞ ≤ n bounds z in a finite box.
  The values are positive integers, so the minimum is attained when the set is
  nonempty.
- **G is a valid cutoff.** A dark target room lies on some retained product.
  Its own x and y parts are feasible, so both minima are finite and at most its
  own wall gaps. The minimizer pair is dark, in C, normalized and of the
  required parity.
- **Area.** Area ≤ (Σ x wall gaps)(Σ y wall gaps) ≤ kₓ m(U) · kᵧ m(V). At
  W ≤ 20 there are at most 10 vertical edges, so kₓ, kᵧ ≤ 9 and 81 G² is
  correct. Log §3 checks the chain on DBas (48 ≤ 78 ≤ 150) and the ledger room
  (8 ≤ 16 ≤ 16).
- **Toys.** The rank-one DBas factor has m = 5 at its own gap vector. The
  (1,M) kernel has m = M for M = 2, 5, 9. A factor whose mark-gap sum is odd on
  every primitive multiple has m = ∞ and is discarded.
- **Saturation.** The box rule needs a ℤ-basis of U ∩ ℤᵏ. With the generator
  (2,8,8,4,4) for the DBas line, the box over its multiples finds nothing
  (log §3). d133's integer linear algebra supplies the saturated basis, but the
  note says only "rational spans" (Low 4).

G(C) is a maximum over retained products. A census only needs one dark room
per chart, so the minimum over products would also suffice. A uniform estimate
naturally bounds the maximum, so the note's choice is reasonable.

### 1d. Descent order and the x₃ = x₁ + x₂ model

The two replacements are correct. Each replaces a whole axis by its minimizer,
and the product property keeps the pair dark. The "fastest gap first" order
plays no role. Any order gives the same pair (z*ₓ, z*ᵧ). The descent is just the
two independent minimizations (Low 1).

The model is correct. On x₃ = x₁ + x₂, keeping x₂ = j forces x₃ ≥ j + 1. So you
can't bound both fast coordinates while keeping the slow one (log §5). This
shows why freezing slow coordinates fails and why the note minimizes whole
factors before any constants are fixed.

### 1e. Isolated dark rooms

Covered. d132 shows every point of D lies on a maximal flat. Each flat is
linear and contains the two-parameter rescaling orbit of each of its points. So
it has dimension at least 2, and no dark room is isolated in the real dark set.
"Isolated" can only mean a factor with finitely many primitive target points:
a rank-one image in d133's test. m(U) is a minimum over the factor, so it
covers that case. The rank-one DBas toy is an example.

This also clarifies d186 §4, item 4. Zero-dimensional dark flats can't occur.
The hard case is a rank-one factor, which a generic seed still doesn't locate.

### Other sections

- **Computable given a list.** Correct. Given saturated factor bases, d133
  decides feasibility, and the box rule terminates on feasible factors.
- **L3, real marks.** Correct. Wall norms are positive integers, so a minimum
  is attained. The two real lifts are independent. The note correctly claims no
  denominator bound.
- **Ledger room.** The vertices realize LLLRLLLRLR. The room is strictly
  simple, with area 8 and wall gcds 1 and 1 (log §4).

## 2. l1-seed-normal-bound.md

### 2a. Slope correction and the displacement bound

The derivation checks. Write D = X + Σtⱼ. Then D(s − u) = (Y − Xu) +
Σ(Kⱼ − tⱼu), so D|s − u| ≤ E₀. At retained abscissa x ≤ X, the error is
x(s − s₀) + Σ(tⱼs − Kⱼ) over crossings so far. Splitting s − s₀ through u
bounds it by D|s − u| + X|u − s₀| + Σ|tⱼu − Kⱼ| ≤ 2E₀.

With X|u − s₀| < 1/(16q) and Mε = 1/(16q), E₀ < 1/(8q), so 2E₀ < 1/(4q). That
is strictly inside d184's margin 1/(2q). The bump radius gives phases within
ρP = 1/(32qM), half of ε, so there is extra slack. The condition u > s₀/2 is
implied by the J radius (Low 5). The wall-hit caveat from d184 Low 3 needs
s > s₀/2, which holds because |s − u| < 1/(8qX).

**DBas replay (log §6).** Family (t₁,t₂), k = 2, M = 2, common P = 8, q = 7,
so ρP = 1/448.

| (t₁,t₂) | u | Phase errors | s | Max displacement | 2E₀ (actual / note) | Trace |
| --- | --- | --- | --- | --- | --- | --- |
| (5711, 28) | 2/7 + 1/20000 | 1.6·10⁻⁴, 1.4·10⁻³ | 1644/5753 | 1.97·10⁻³ | 4.5·10⁻³ / 0.019 | Target, 418 reflections, seed itinerary and sheets |
| (8569, 56) | 2/7 − 1/30000 | 8.1·10⁻⁵, 1.9·10⁻³ | 2468/8639 | 2.24·10⁻³ | 4.8·10⁻³ / 0.019 | Target, 630 reflections, seed itinerary and sheets |

Both are below 1/(4q) ≈ 0.036. The endpoint error is exactly 0 in both.

### 2b. Fourier argument

- **Coefficients.** The product of triangular bumps has coefficients
  Π sinc²(πρhⱼ) ≥ 0 and constant term 1. The 1-D sums equal 1/ρ (log §7).
- **Tail.** The bound 2k/(π²Kρ^(k+1)) is d184's, which d184 verified.
  K > 8k/(π²ρ^(k+1)) makes it less than 1/4. At ρ = 1/4 and 1/5 with k = 2,
  the actual tails are 0.127 and 0.130, below bounds of 0.247 and 0.248.
- **Characters.** The frequency of h is (h·t)/P with h·t = λ h·z − h·b. There
  are three cases (log §8):
  - h·z ≠ 0: the frequency grows with λ, and the normalized integral is at most
    P/(π|h·t||J|) → 0.
  - h·z = 0 and h·b = 0: then h·t = 0, and the term contributes c_h ≥ 0.
  - h·z = 0 and h·b ≠ 0: the frequency is a nonzero constant, and the sign is
    uncontrolled. Only this case can block positivity.
- **Positivity.** If no retained h is in the third case, the average is at
  least 1 − 1/4 − o(1) > 0. Some u then puts every phase within ρP of Pℤ, and
  2a gives a legal shot at λz.

The note's hypothesis, "annihilates z ⇒ annihilates E", is stronger than
needed. The proof gives h·z = 0 and h·b ≠ 0. That implies h|E ≠ 0 because
b ∈ E. The sharper form shows E enters only through b (Low 3).

### 2c. One h for all of U

Correct. For each positive integral z ∈ U there is an h in a finite set with
h·z = 0 and h|E ≠ 0. Positive rational points of U scale to integral ones with
the same h. So the finitely many sets ker h ∩ U cover a dense subset of the
relatively open positive part of U. That union is closed, so it covers the
positive part. A finite union of proper subspaces has empty interior, so some
ker h contains U. The argument uses only rays through 0, so no onset bound in λ
is needed, as the note says.

The core estimate uses no finite-flat input, as the note says. It needs a
rational U whose positive integral points are all dark at y₀. The finite-flat
theorem is needed only to know that dark factors have this form.

### 2d. Iterative full-equation bound

Correct as stated. Each new seed bᵢ lies in Eᵢ = ∩ ker hⱼ, so the previous rows
vanish on bᵢ, but hᵢ·bᵢ ≠ 0. So the rows are independent, and after codim(U)
steps they cut out U with height at most max Kᵢ. A primitive normal of a
hypersurface divides h, so its entries are at most K.

The seed-existence step is correct, given finite flats. If all positive
integral points of E ⊋ U were dark at y₀, E would lie in one slice flat, which
contradicts maximality of U. The note correctly says this gives existence only.

Masking: U is maximal on the slice for all y₀ ∈ V outside finitely many proper
subspaces. Otherwise V would lie in the finite union of the masking Vⱼ, and the
product would not be maximal. So a generic probe works, but no explicit probe
follows (Low 6).

### 2e. Doubly proper products

Correct. With seed ((1,1),(1,1)) and U: x₂ = m x₁, V: y₂ = m y₁, the horizontal
slice meets U × V only if (1,1) ∈ V, and the vertical slice only if (1,1) ∈ U.
Both fail for every m > 1. The product has positive lattice points
(1,m) × (1,m), and its primitive normals (−m,1) have height m (log §9). The
note correctly calls this a model of the information, not a dark family.

The full-chart hypersurface remark is correct. If Lᵧ is the whole y space,
every y₀ lies in it. The seed's own slice then meets the flat, and 2a–2c apply.

## 3. Gaps

### High

None.

### Medium

1. **Inherited conditionality.** Chart descent, the seed-existence step in 2d,
   and every application to "dark factors" need the d132 finite-flat theorem
   and d134 marked algebraicity. Both notes label this. Chart descent says the
   classifying-map completion was "submitted to d186". d186 judged it a sketch
   (d186 Medium 1). Say "reviewed in d186 as a sketch" instead.

### Low

1. **Descent order.** "Replace first the entire axis containing a fastest gap"
   suggests the order matters. It doesn't: the result is (z*ₓ, z*ᵧ) in either
   order. State the descent as two independent minimizations.
2. **"Preserve the chart."** Real rescalings preserve the real order cell and
   the dark set, not integrality, parity or wall gcd. Those are imposed after
   the flat is fixed.
3. **Sharper Fourier conclusion.** State the result as h|U = 0 and h·b ≠ 0.
   It implies the current form and shows that E matters only through b ∈ E.
4. **Saturated bases.** m(U) and the box rule need a ℤ-basis of U ∩ ℤᵏ, not
   just its rational span. d133 supplies it; say so.
5. **Constants.** u > s₀/2 is implied by the J radius. ρP = ε/2, so the stated
   E₀ has a factor-2 slack. Both are harmless.
6. **Probe genericity.** Add that U is maximal on the slice for y₀ ∈ V off
   finitely many proper subspaces. This is the precise form of the masking
   remark.
7. **Target scope.** m handles either specified parity on each axis, and the L3
   section handles real interior marks. Boundary and corner targets remain
   outside both notes (d133 gap 1).

## 4. What L1 needs for an explicit G(C)

**What is now in place, conditional on d132 and d134:**

- G(C) = max over retained products of max(m(U), m(V)) is a valid wall-gap
  cutoff. The census ceiling is 81 G(C)² at W ≤ 20.
- m(U) is explicit in the saturated rows defining U: Cramer bounds on a
  positive point, then d133's Smith progression for primitivity and parity.
- The seed-normal bound turns one lit seed on a slice through V into an
  explicit row for U: ‖h‖∞ ≤ K = 1 + ⌈8k/(π²ρ^(k+1))⌉ with ρ = 1/(32qMP).

**The single missing estimate is a factor-height bound H(C).** State it as
follows:

> For every retained dark product U × V in C, the saturated lattices
> U ∩ ℤ^kₓ and V ∩ ℤ^kᵧ are cut out by integer rows with entries at most an
> explicit H(C).

This is d133's H, and d186 §4 item 1. With H(C), m(U) and m(V) are explicit,
so G(C) and the ceiling 81 G² are explicit. Nothing else is needed for G.

Through the seed-normal note, H(C) would follow from one seed estimate. There
must be an explicit Q(C) such that every retained product, on each axis, has an
integral probe y₀ ∈ V with the following property. Every rational E ⊋ U cut out
by rows of height at most K(Q) contains a lit nonaxial lattice seed at y₀ with
qMP ≤ Q(C). Then ρ ≥ 1/(32Q), so H(C) ≤ 1 + ⌈8·11·(32Q)¹²/π²⌉ with k ≤ 11.

Neither note supplies this, for three reasons:

- **The probe.** The doubly proper model shows a fixed seed can miss both
  slices of U × V. So the probe must come from V itself, which is unknown.
- **Seed size.** Finite flats give lit seeds in each E, but no bound on q, M
  or P. L2 can't supply them, because the relevant slices have area above 20
  (d184 Medium 2).
- **Circularity.** A proof that locates the probe needs V, and locating a probe
  for V needs U. One axis has to be controlled by an independent argument.

The smallest test of the seed route is a product of two proper factors, each a
line in two gaps of its axis, so codimension 2 overall.
Rational full-chart hypersurfaces are already handled: the seed's own slice
meets them.

No ledger word changes status. LLLRLLLRLR remains open as an all-length
statement.
