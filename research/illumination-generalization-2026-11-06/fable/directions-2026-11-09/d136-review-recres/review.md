# D136: Referee review of reciprocal-resonance.md

Date: 2026-11-21. Target: `d95-review-queue/snapshots/reciprocal-resonance.2026-11-21-2230.md`. Context read: `flat-resonance.md`, `primitive-dark-flats.md`, `parametric-orbits.md`, `length-periodicity.md` (all in `qclass-closure/bbbb/`), the d132 and d133 reviews, and the d130 checks for the room data. I assumed the finite-flat theorem and the product splitting from d132 and d133. I didn't re-review them.

Code: `checks.py`, log `checks.log`. Run it with `python3 -B checks.py > checks.log`. It uses exact `Fraction` arithmetic and takes 3.1 CPU seconds. It builds only the named rooms: the cov279 slice and stretch, the st279 slice and end-square stretch, and the U/U+1 dumbbell. Part A enumerates abstract coefficient tuples, which aren't rooms. The directional replay caps each launch at 200,000 row steps. No network access was used.

## Verdict

**Sound with gaps.** Every algebraic step I checked is correct, and the note labels both main results as conditional. The rank test, however, is weaker than the note suggests:

- It's sufficient but not necessary.
- It's equivalent to K = Vₓ⊗Vᵧ, which needs ab − jₓjᵧ independent identities.
- The note's routes can't supply that many identities for the low-dimensional flats where H matters.

So "dimension recovery" isn't only unproved. As set up, it's out of reach.

## 1. The height bound and what it's conditional on

**Pencil section.** The bound 4J² holds if all of the following are true:

- Both factors are lines in specified two-dimensional spaces with integral bases.
- A two-term resonance holds in each orientation.
- Both elimination determinants are nonzero polynomials.

The 4J² bound is in the chosen bases. Converting it to gap coordinates also needs the heights of the bases, as the note says.

- The determinant coefficients are bounded by 2J², 4J² and 2J². The rational-root step is correct. The 4J² case is needed when the constant term vanishes and you divide by X: the middle coefficient then becomes the constant term.
- Exhaustive check (log §A): J=1 gives 5,856 systems with a maximum height of 3, against the bound 4. J=2 gives 383,456 systems with a maximum of 11, against 16. The bound holds and isn't tight.
- **J = 4ME² is twice what's needed.** The x_i y_j coefficient of n₁d₁u₂ + n₂d₂u₁ is at most 2ME². 2,000 random cases reach exactly 2.00·ME².
- The redundancy test is correct. The two relations give one graph exactly when g∘f is scalar. The reciprocal example is exact: the transposed form is −1 times the original. (N, N+1) solves it with height N+1.

**Gap-coordinate section.** The bound H = ⌈(√j Δ)^j⌉ with Δ = ⌈(2M√t)^t⌉ is conditional on three things:

- (a) a uniform bound M on the resonance weights;
- (b) the dimension equalities dim X = dim Vₓ and dim Y = dim Vᵧ, which require the true dimensions to be known;
- (c) the upstream finite-flat theorem and the product splitting (d132, d133).

The steps hold:

- **Entry bound.** Width and travel forms have 0/1 coefficients, so the entries of Cᵢ are at most 2M. In the named rooms, max|C| = max|n| (log §D).
- **Cramer and Hadamard.** In 150 random systems the pivot-minor vectors are integral and span K, and their entries are at most Δ. At t=1 the bound is attained. The defining-row bound ⌈(√j Δ)^j⌉ also holds (log §B).
- **Smith form.** The note doesn't use a Smith form or a lattice basis. It produces rational defining rows, which is what the d133 enumeration consumes. d133 then does its own Smith step. No lattice-index issue arises.
- **Alternatives.** Siegel or Bombieri–Vaaler would improve the exponents. At the scales in item 4 that doesn't matter.

## 2. Is the rank test exact?

No. It's sufficient but not necessary, and its premise is much stronger than it reads.

- **Equivalence (log §C1, 53 instances).** dim X = dim Vₓ and dim Y = dim Vᵧ hold exactly when K = Vₓ⊗Vᵧ. In that case every M in K has its columns in Vₓ and its rows in Vᵧ. The note treats K = Vₓ⊗Vᵧ as a special case ("in particular"), but it's the whole condition. It needs t = ab − jₓjᵧ independent identities.
- **Not necessary (log §C2).** Take the identities x₂y₂ = 0 and x₁y₂ − x₂y₁ = 0. They pin the factors to (e₁, e₁), with height 1. Still, K = span(E₁₁, E₁₂+E₂₁) and X = Y = ℚ². Exact identifiability is the rank-one (Segre) locus in P(K), which is not a rank condition. The reciprocal example is the other failure mode: it has a continuum of solutions and X is full.
- **"Precisely which directions … fails to constrain" overclaims.** X^⊥ is the set of forms e such that e⊗ℝᵇ ⊂ span(Cᵢ). Those are the constraints you can derive linearly. The directions that leave every identity unchanged form a separate space F. In the st279 square-centre pair, F = 0 but X = ℚ⁷.
- **Named rooms (log §D).** For each room the table gives the identities found, the rank t and dim X. Identities lists the rectangle pairs and resonance vectors n.

  | Room and pair | Identities | t | Needed | dim X vs jₓ |
  |---|---|---|---|---|
  | cov279 slice, S=(4,1), T=(12,1) | none (direct chord) | 0 | 33 | 7 vs 2 |
  | st279 slice, S=(2,1), T=(6,1) | none (direct chord) | 0 | 31 | 7 vs 2 |
  | cov279 stretch, d130 pair | none two-term; one three-term relation (−2/3, −1, 1) | 0 | 33 | 7 vs 2 |
  | cov279 stretch, S=(q/2,1), T=(9q/2,5) | horizontal (0,2), (0,3), (2,3); vertical (2,3), n=(−1,6) | 4 | 40 | 7 vs 2 |
  | st279 stretch, square centres | α₀=α₃ and α₁=α₂ in each orientation | 4 | 38 | 7 vs 2 |
  | dumbbell, length-periodicity marks | none | 0 | 17 | 5 vs 3 |

  Every case reports "not recovered." That is consistent with the known results, because none of these rooms is dark on its family span.
- **Comparison with the directional criteria.** The criteria "cov279 lit iff gcd(u,v)=1" and "st279 lit iff p ≡ ±4 (mod m)" replay with 0 mismatches (log §E). They are statements about fixed directions. Both pairs share the bottom band, so the all-direction route is a direct chord and the rank test gets empty input. The directional dark points (u,v) span ℚ², so no finite union of rational subspaces describes them. This is consistent with parametric-orbits §4: the flat machinery applies only to the all-direction dark locus.

## 3. What a free gap direction implies

A free direction of the test, meaning X ⊋ Vₓ or F ≠ 0, implies nothing about darkness. The identities are only necessary conditions, and lit rooms pass them:

- The cov279 stretch is lit for every pair (d127, 3∤q), yet it carries 3 horizontal identities.
- In the dumbbell all 5 x-directions, including the corridor gap L, are fully free. Opposite-chamber pairs there are lit for every L ≥ K.

A free direction *of a true dark flat* is different. If it changes the walls and the factor's wall image has rank at least 2, the d133 progression gives primitive dark rooms of unbounded area at fixed W. By the d133 area-≥120 lemma, such a direction must move walls, not only marks. No reviewed result rules this out, since bounding dark area at fixed W is the open goal. No reviewed result exhibits it either. Every named family with a free stretch direction is lit, so the note is consistent with the reviewed results. It doesn't claim "free ⇒ dark."

## 4. Scope: an explicit H and a finite census

**The resonance-coefficient bound is well defined per flat, not uniformly.** At a point and a placement, flat-resonance's M(ε) exists, because (2M+1)^k·exp(−4Mε²) → 0. The intrinsic quantity M* = min max|n| over relations that hold identically on the flat is well defined, and M* ≤ M(ε) at every point of the flat. M* can be 1 while the height is unbounded, as the reciprocal example shows, so M alone doesn't give H. M(ε) is very large:

- In the cov279 cross route, ε ≤ 1/(64q), so M ≥ 1.8×10⁷ at q=16 and M ≥ 1.1×10¹¹ at q=1000.
- On the same flat, offsets that widen the door give M ≈ 5.1×10⁵ for every q.

So the dependence on clearance can be handled within one flat. Uniformity across flats is the open input.

**Remaining inputs for an explicit H:**

- (i) the finite-flat theorem, still conditional on the semialgebraic-map gap from d132;
- (ii) a uniform M*;
- (iii) an exact identifiability mechanism to replace dimension recovery;
- (iv) relations with three or more terms;
- (v) the cases outside the primitive subproblem: non-primitive normalizations, irrational marks below area 120, and boundary marks (d133 gap 1).

**Census size, even with every hypothesis granted.** Take M=1 and a=b=11. Then log₁₀Δ ≈ 161 and log₁₀H ≈ 1775. The d133 enumeration then needs about 10^(4.3×10⁵) witness pairs per order cell. The d132 area cutoff is about 10^(7.8×10⁴). That is a definability statement, not a census you can run.

## Gaps

1. **High: dimension recovery is structurally out of reach, not only unproved.** The test needs t = ab − jₓjᵧ independent identities. Each tree route gives at most C(k,2) two-term identities. At W≤20 a route has at most r+1 = 9 rectangles (d126), so two orientations give at most 72. At a=b=11 that forces jₓjᵧ ≥ 49, so flats of dimension 6 or less in each axis can never pass. In the named rooms, t = 4 against 38–40 needed. Fix: either name a source of about ab independent identities, such as non-tree itineraries, or replace the test with exact identifiability. That means the rank-one locus of P(K) plus an arithmetic-Bézout height bound for isolated rational points.
2. **Medium: the test is presented as more exact than it is.** It's sufficient only (§C2 counterexample). "In particular K = Vₓ⊗Vᵧ" is in fact the equivalent condition. The final sentence ("precisely which directions") conflates the linear hull X with the free-direction space F; in st279, F = 0 while X is full. Fix: restate the test as "K = Vₓ⊗Vᵧ" and drop "precisely."
3. **Medium: the two-term restriction misses relations that occur in named rooms.** In the d130 pair, the vertical route's only relation on the flat has three terms, (−2/3, −1, 1), and the bilinear flattening doesn't see it. Flat-resonance guarantees only a relation inside one proportionality class. Fix: say how classes of size s ≥ 3 enter, for example through a degree-(s−1) multilinear flattening, or restrict the claim explicitly.
4. **Medium: M is not room-uniform even along one named family.** The clearance-derived M grows with q in cov279. Fix: define M* intrinsically, as the least resonance height that holds identically. State that the hypothesis is a uniform bound on M*, together with item 1, not on M(ε).
5. **Low: J is twice what's needed.** J = 2ME² suffices. The 4J² pencil bound holds but isn't tight (maximum 11 against 16 at J=2).
6. **Low: the transposition redundancy is narrower than "rotating the test."** In the cov279 cross pair, the vertical route gives an identity, n=(−1,6), that is independent of the horizontal ones. The literal loss of an equation occurs when one rectangle carries both roles with swapped width and travel. Fix: state that condition.
7. **Low: the finite census is a definability statement.** The constants in item 4 should appear next to "explicit height bound," so readers don't read it as a runnable cutoff.
