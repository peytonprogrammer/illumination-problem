# D132: review of parametric-orbits.md (snapshot 2026-11-21 22:00)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/parametric-orbits.2026-11-21-2200.md`, SHA-256 prefix `815164423d09d3e7`. Context read: `shadow-budget.md`, `generic-line.md`, `thin-room.md`, `stabilizer-orbits.md`, `convex-cylinder.md`, `corner-support.md`, and the d86 and d116 reviews.

Primary sources: I fetched arXiv 1305.3015 (EMM), 1311.2350 (Filip, Annals), 1307.7314 (Filip, Inventiones), 0911.4373 (Cluckers–Miller), 1708.03411 (Apisa–Wright), the Annals landing page and the Driscoll–Trefethen excerpt. I extracted text locally with `pdftotext`. No project information left the machine.

Own code: [checks.py](checks.py), log [checks.log](checks.log), 0.3 CPU-seconds.

## Verdict

**Sound with gaps.** The logical skeleton of the main theorem is correct, and it is a genuinely new argument. Finiteness on all of C, including near ∂C, comes from o-minimality, not from local linearity. That step is valid once D is known to be definable. Definability rests on one load-bearing citation that doesn't cover the case used: Filip proves algebraicity in strata H(κ) of zeros, and the note needs strata with regular marked points. I expect this to be fixable, but until it is, the theorem is conditional. Everything downstream (Presburger, the conditional bound, the cov279 and st279 directional examples) checks. The theorem gives no effective handle on W ≤ 20.

## 1. Main theorem: is D a finite union of C ∩ L?

The argument has four links. I checked each one.

**E is a finite union of affine invariant submanifolds.** E is closed in the marked stratum: a legal segment keeps positive clearance from the finite forbidden set and persists under small changes of periods and endpoints. E is GL⁺-invariant. EMM Theorem 2.2 states: "Any closed P-invariant subset of H₁(α) is a finite union of affine invariant submanifolds." It applies to any closed invariant set, not just one orbit closure. Apply it to E ∩ H₁ and take the cone. The marked-point extension is LMW §2.2 ("they allow αᵢ = 0"), checked in d116. Forbidden convex lifts are a property of the set E, not of the stratum, so they need no extra hypothesis. This link holds. The note names the theorem only as "EMM's closed-invariant-set theorem" and should cite Theorem 2.2 and LMW §2.2 directly.

**Local structure.** EMM Definition 1.1(i): each point has a neighborhood on which the cone is "a complex linear subspace defined over R in the period coordinates", and the map is proper. So near any point E is a finite union of linear sheets through that point. The sheets are defined over R (by Wright, over a number field), not over Q.

**Local linearity on C.** This is correct. The weak-order cell fixes the combinatorics of the room, the marks and the grid triangulation. C is convex, so one topological marking serves all of C. Each relative period is a signed sum of edge holonomies, which are integral linear forms in the coordinates. Forgetting unused endpoint lifts is a coordinate projection. So each pullback Φᵢⱼ⁻¹(E) is, near each x in C, a finite union of affine flats through x. The finite intersection D has the same property. As the note says, this bounds nothing globally: lifts of one sheet to Teichmüller space are infinitely many, and Φ(C) is not relatively compact.

**Global finiteness (section 3).** Given that D is definable in an o-minimal structure, the argument is correct:

- The extension lemma holds. The set of points of L ∩ C with an L-neighborhood in D is open. At a limit point, finitely many flats cover an open patch of L, so one contains L. L ∩ C is convex, hence connected.
- Every point of D lies in a maximal flat, since dimensions are bounded.
- Countability holds. Cover C by countably many balls with finite local descriptions. A maximal flat meeting a ball is contained in a local flat, which extends throughout C by the lemma, so maximality gives equality.
- The set of maximal flats is first-order definable over C and D in the affine Grassmannian. A countable definable set in an o-minimal structure is finite.

The argument only quantifies over points of C, so thin and pinched rooms near ∂C need no special treatment. This answers the question of where finiteness near ∂C comes from: it comes entirely from definability of D.

**Definability of D (section 2).** This is where the gaps are.

- The Schwarz–Christoffel exponents check (check 3). For r reflexes there are 2r + 4 prevertices, the exponent sum is −2, and the curve v² = ∏(z − aᵢ) has genus r + 1. ω has order 0 at convex prevertices and order 2 at reflex prevertices, total 2r = 2g − 2. On a sheet over H, ω = c·∏(z − a)^(εᵢ/2) dz = f′ dz, so the developing map is the physical room. The orientation cover of the doubled sphere is the four-copy unfolding.
- The integrands on the segments from i to aₖ are semialgebraic jointly in t and the parameters, with the closed-upper-half-plane square root. The only singularity is (1 − t)^(−1/2), which is integrable. Cluckers–Miller Theorem 1.3 states: "Let f be in C(X × Rᵐ) for some subanalytic set X. Then I_X(f) is in C(X)." Here "subanalytic" means globally subanalytic, which includes semialgebraic sets on unbounded domains. Constructible functions are definable in ℝ_an,exp. This link holds.
- The converse direction (matching vertex images imply the conformal map onto the room) uses the argument principle. That is standard and correct. The edge through ∞ is straight because arg f′ is the same on both real rays (the total turn is −2π).
- **Algebraicity of E: the main gap.** Filip's Theorem 5.4 (arXiv 1311.2350v3; Theorem 1.1 in the introduction) states: "The affine invariant manifold M is a quasi-projective algebraic subvariety of H, defined over Q̄." In Filip, H = H(κ) is a stratum where κ lists the orders of the zeros. Remark 5.6(ii) builds it from the divisor map to Sym^(2g−2). Order-zero marked points don't appear. The note needs algebraicity in H(2^r, 0^(r+6)) with r + 4 forbidden convex labels and two endpoint labels. Apisa–Wright use Filip's torsion results for periodic points, but they don't state algebraicity of affine invariant submanifolds of marked strata. I found no statement covering the case.
- **The classifying map is sketched in three sentences.** The note doesn't specify the algebraic structure on the labelled marked stratum, check that the family over the root-choice cover gives an algebraic morphism into it, or check that it agrees with the structure in which E is algebraic. "Or work with its moduli stack and then take the coarse image" is a direction, not an argument.

**Conclusion for item 1.** The deduction "E algebraic ⇒ D definable ⇒ D a finite union of C ∩ L" is correct. "E algebraic" is not established by the cited theorem.

## 2. Darkness as an intersection over lifts

This is exact physical darkness under the project's convention. The project forbids convex-corner contacts ("Convex corners are regular on M but remain forbidden billiard contacts", convex-cylinder.md; corner-support.md).

- Reflex corners are the order-2 zeros, so segments can't pass through them.
- Convex corners are regular points of the unfolding. The note keeps them as forbidden labels, which matches the convention. If a convex hit were instead allowed to retroreflect, D would be a superset of physical darkness. The note should state the convention.
- Early hits are harmless. A segment that meets y early can be truncated at the first hit, and one that revisits x can start at the last visit. So E's treatment of x and y in segment interiors doesn't matter.
- Unused lifts of S and T are forgotten, so segments may pass through them. A physical ray through T at another sheet is caught by the corresponding lift pair.
- The four-copy unfolding is a translation surface for axis-parallel walls, so legal billiard paths and legal segments correspond. With all 16 lift pairs intersected, labelling conventions on the algebraic side don't matter.

## 3. Presburger consequence and rationality of L

Correct. Rationality of L is not needed and is not claimed. If L ∩ ℤᵏ is nonempty, it is x₀ + (dir(L) ∩ ℤᵏ), and that subgroup has a finite integral basis whatever field defines L. C is cut out by rational strict inequalities and equalities, and the parity test is a congruence. So integral darkness on each cell is a finite union of sets "∃ n ∈ ℤᵐ: x = x₀ + Σ nᵢbᵢ, x ∈ C, parity", which is Presburger. There are finitely many cyclic types and cells at fixed W.

The scaling step also holds. In gap coordinates each cell is a full open orthant, because simplicity and interiority are determined by the weak order. D is scale-invariant, and λ ↦ λL is a continuous path through a finite set, so every maximal flat is a linear subspace. The sheets can still be irrational. V = span_ℝ(L ∩ ℤᵈ) has the same lattice points as L, as stated.

## 4. cov279 and st279 directional replays

I replayed both with an exact integer billiard on the named rooms only, scanning directions (p, 1) over all four launch signs (checks 1–2). Rays stop at any corner. Each launch runs until its lattice-level state repeats, with a cap of 200,000 rows that no launch reached.

- **cov279**, q = 4u for u = 4, 7, 10, 13 (q = 16, 28, 40, 52), S = (4,1), T = (12,1), p = 8v, v = 1 … 2u + 3. Lit if and only if gcd(u, v) = 1, with no mismatches. No launch hit a corner or left the bottom rectangle. Each room has area 13q + 3, 6 reflexes, 10 convex corners and no pinches.
- At q = 16, v = 3 is lit at time 2 with launches (+,+) and (+,−). The developed abscissa 52 folds to 12. v = 4 is periodic with folded abscissa 4 at every height-one return.
- **st279**, m = 32 and 48, S = (2,1), T = (6,1), p ∈ 4ℤ up to 4m. Lit if and only if p ≡ ±4 (mod m), with no mismatches. At m = 32, p = 36 is lit at time 2 with launch (−,−), as stated, and p = 40 is dark on all four launches.
- **Non-Presburger argument (check 4).** u = 3P + 1 gives gcd(u, P) = 1, so v ∈ uℤ is dark and v + P is lit. In st279, 1 + P is never ±1 modulo M > 2P + 4. Both shift arguments hold.

The section proves that the directional relation is not Presburger. As the note says, both marked pairs are lit with all directions allowed, so this says nothing about darkness.

## 5. Scope and W ≤ 20

**Proved, conditional on gap 1:** the existence of a finite-union-of-flats description and of a Presburger formula per cell, the one-parameter dichotomy, and that the maximal flats are linear in gap coordinates.

**Proved outright:** the directional relation is not Presburger on the two named slices, and the extension and finiteness lemma of section 3 for any definable, locally flat D.

**Not proved:** anything effective. There is no f, no equations, no lattice bases, no emptiness decision.

The conditional bound gives no practical finite check. Its Cramer/Hadamard step checks on 1,189 random vertices (worst denominator/Δ = 0.33). With d = 22, even H = 1 gives Δ ≈ 5.8 × 10¹⁴, box sides ≤ 5.7 × 10¹⁷ and area ≤ 3.2 × 10³⁵. H = 2 gives area ≤ 5.6 × 10⁴⁸. The note's "precise coefficient-height target" is accurate, but no census reaches these sizes. The bound also needs H uniformly over all cells, and it produces non-primitive (even) witnesses. The theorem doesn't change the W ≤ 20 estimate.

## Gaps

1. **High: Filip's theorem doesn't cover marked strata.** Theorem 5.4 is stated for H(κ) of zeros. The note needs algebraicity of affine invariant submanifolds of H(2^r, 0^(r+6)). The d86 and d116 reviews checked Filip only from memory, so "reviewed inputs" overstates this. To fix it, cite an explicit statement for regular marked points. Alternatively, check that Filip's proof uses only the mixed Hodge structure on H¹(X, Σ) for an arbitrary finite labelled Σ. A third option is to reduce to unmarked strata through a branched double cover at the marks, which is algebraic and linear on periods. I expect this to be true, but it is load-bearing and currently unsupported.
2. **Medium: the real-algebraic classifying map is a sketch.** Specify the quasi-projective structure on the labelled marked stratum, the family over the root-choice cover and its morphism, and the agreement with the structure from gap 1. Also show that pulling back E to the real parameter locus with w = z̄ gives a semialgebraic set.
3. **Low: the convex-corner convention isn't stated.** "Exactly physical darkness" holds because the project forbids convex contacts. Say so, and note that retroreflection at convex corners would change D.
4. **Low: EMM and LMW are cited by description only.** Cite EMM Theorem 2.2, EMM Definitions 1.1–1.2 for the local sheets, and LMW §2.2 for αᵢ = 0. Also note that the sheets are defined over R, not Q. The note's Presburger argument already handles this.
5. **Low: the Driscoll–Trefethen citation is loose.** Their Theorem 1.1 is the forward direction with f(∞) = wₙ, a vertex. The edge-interior normalization needs a Möbius change, and the converse is the note's own argument-principle step. Both are fine, but the citation says more than the theorem does.
6. **Low: the conditional bound needs its size stated.** Even H = 1 gives area 3.2 × 10³⁵ at d = 22. Say that the bound is a target for structure, not a census plan.

## Citation status

| Citation | Status | Finding |
| --- | --- | --- |
| EMM Theorem 2.2 (arXiv 1305.3015) | Checked | Closed P-invariant subset of H₁(α) is a finite union. Exactly the needed finiteness. Not numbered in the note. |
| EMM Definitions 1.1–1.2 | Checked | Proper immersion, local complex-linear sheets defined over R. |
| LMW §2.2, marked points | Checked in d116, not re-fetched | EMM allow αᵢ = 0. |
| Filip, Annals 183(2) 2016, pp. 681–713, Theorem 5.4 | Checked (arXiv 1311.2350v3) | Matches for H(κ). Doesn't state the marked-point case (gap 1). The Annals link resolves to the correct paper. |
| Filip arXiv 1307.7314 | Wrong ID in the review request | That paper is "Semisimplicity and rigidity of the Kontsevich–Zorich cocycle" (Inventiones). It has no algebraicity theorem. The note's link is correct. |
| Cluckers–Miller Theorem 1.3 (arXiv 0911.4373) | Checked | Stability under integration for constructible functions on globally subanalytic X. Applies as used. |
| Driscoll–Trefethen Theorem 1.1 | Checked | Forward SC formula with ∞ at a vertex (gap 5). |
| van den Dries–Macintyre–Marker, o-minimality of ℝ_an,exp | From memory | Standard. The linked lecture notes weren't fetched. |
| Apisa–Wright (arXiv 1708.03411) | Checked for gap 1 | Uses Filip's torsion results for periodic points. No general algebraicity statement for marked strata. |

## Re-run

```
cd d132-review-paramorb && python3 -B checks.py > checks.log
```
