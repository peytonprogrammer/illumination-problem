# Referee review: period ratios for two triple collisions

Date: 2026-11-20. Reviewed file: `three-zero-monodromy.snapshot.md` in this directory. It is byte-identical to `qclass-closure/bbbb/three-zero-monodromy.md`. Checks: `checks.py`, output in `checks.log` (1.4 CPU-seconds, `python3 -B`). No search over rooms, rays, directions, or reflection words was run.

## Verdict

| # | Claim | Verdict |
|---|-------|---------|
| 1 | Monodromy dichotomy: weights (1,1,1) in both triples, or additive in both | Sound with fixable gaps |
| 1′ | Additive case puts a zero and a pole with equal image in A in each matching | Sound |
| 1″ | The additive example C = I+R, a = (1,1,−2), b = (−1,2,−1) | Sound as linear algebra; geometrically realizable only for one hexagon parity (gap G1) |
| 2 | Explicit sphere family in Q(1³,−1⁷) with exact ratios 1:1:2 and positive-area limit | Sound |
| 3 | A rank-h locus in unmarked Q(1^s,−1^(s+4)) has dimension 2h, so a proper boundary has rank ≤ h−1 | Sound for these strata; false for the broader "all genus-zero strata" wording |
| 4 | Citations | One link is wrong (G2); others correct |
| 5 | Stated next move | Well posed; one half can be sharpened (see "Next move") |

The dichotomy proof is correct. The main new finding is that the hexagon geometry fixes the normal form of C. The note treats I+R and I−R as both available.

## Gaps, ranked, with fixes

**G1. The normal form of C is fixed by a parity (substantive refinement).** In an explicit hyperelliptic model, I computed the six doubled-arc intersection signs by analytic continuation of √f. The cycle sign depends only on the parity of k, the number of the four remaining poles inside the hexagon (`checks.log` §2):

| Poles inside | Normal form | det C |
|---|---|---|
| 0, 2, 4 | I−R | 0 |
| 1, 3 | I+R | ±2 |

A nonconvex hexagon gives the same pattern. For k = 0 or 4 this matches a chain relation: the two lifts of the boundary circle give Σ±uᵢ = ±Σ±vⱼ, so C is singular.

The consequences for the additive case (exhaustive over primitive integer weights with |entries| ≤ 12, `checks.log` §1b):

- **Odd k (I+R).** b is a signed cyclic permutation of a. Both triples carry the same weight multiset, for example 1:1:2 in both. The note's example lives here.
- **Even k (I−R).** b ∝ (a₁−a₃, a₂−a₁, a₃−a₂). Nonzero entries of b force pairwise distinct |aᵢ|. Thus 1:1:2 is excluded, and the smallest additive pair is (1,2,3) with (1,4,5).

Fix: add the parity lemma and state both additive sub-cases. Say that the example in "The additive alternative" requires an odd number of poles inside the hexagon. For k = 0 or 4 the chain relation also gives 3P = ±3Q in the constant case, so P = ±Q. I verified the singularity of C, not the chain relation itself, at the homology level.

**G2. Wrong citation link.** `arxiv.org/abs/1303.3603` is Iwaki's paper on Voros coefficients of Painlevé III. Wright's "Cylinder deformations in orbit closures of translation surfaces" is arXiv:1302.4108. Fix: replace the link.

**G3. Equal vanishing order needs one more sentence.** "All three separations in a triple have the same order e" does not follow from "period = s × unit" alone. It follows because M is cut out by homogeneous linear equations. Proportionality on the whole tangent therefore makes Per(uᵢ) = aᵢ·Per(P̃) identically along the disk, with constant ratios. Fix: state this step.

**G4. Scope of the dimension statement.** The note correctly restricts to Q(1^s,−1^(s+4)). There every zero is odd, so it is J-fixed and the anti-invariant relative part vanishes. The broader wording "in unmarked genus-zero quadratic strata" is false. Q(2,−1⁶) has dimension 5 and absolute anti-invariant dimension 4, so rel = 1 (`checks.log` §4). The rank drop needs only rel = 0 for the **parent**. The inequality 2·rank(M′) ≤ dim M′ < dim M = 2h holds whatever the boundary's rel is. Fix: phrase the obstruction as "parent rel = 0" so it also covers zero–zero collisions.

**G5. Hypotheses carried, not derived.** The dichotomy assumes four things:

- The field of definition is Q, so a saturated lattice quotient exists.
- Each triple is proportional on the full absolute tangent.
- Both degenerations are transported to one fiber.
- The transported arcs form an embedded hexagon.

The note labels these hypotheses correctly. The Verdict paragraph should repeat that the dichotomy is conditional on all four.

**G6. Minor points.**

- In the additive case exactly one weight per triple is even. That arc's endpoints coincide in A. All three pairs coincide if P ∈ 2Λ_A. The note's "contains a zero and a pole" is correct.
- The deck-sign remark is unnecessary. The local monodromy is supported in disjoint annuli around the three pairs, so no J factor arises.

## Claim 1: monodromy dichotomy

I reproduced every step.

- **Local braid.** Positions extend holomorphically over the puncture. The monodromy is e full twists of each colliding pair in disjoint disks. Birman–Hilden lifts each full twist to T²_{uᵢ}, which gives Tᵤ(x) = x + 2e Σ⟨x,uᵢ⟩uᵢ.
- **Descent.** The loop lies in M, so it preserves TM and its annihilator ker j. Comparing j(Tᵤvⱼ − vⱼ) upstairs and downstairs gives (Cᵀa)ⱼ·2eP = bⱼ·W. Since every bⱼ ≠ 0 and P ≠ 0, this gives Cᵀa = λb, including λ = 0.
- **Normal form.** All 64 sign arrays on the six-cycle support reduce to I±R under row and column signs. The product of the six entries decides which (32 arrays each).
- **Spectra.** CCᵀ = CᵀC takes the values 4 and 1 for I+R, and 0 and 3 for I−R, on the constant line and on the sum-zero plane.
- **Exhaustive check.** All integer solutions with |entries| ≤ 12 fall into the two cases: 4 + 540 for I+R and 4 + 240 for I−R.
- **Parity.** Every additive triple has exactly two odd entries.
- **A[2] identity.** J fixes Z and Pole and acts by −1 on H⁰(Ω), so ∫_{γ−Jγ} = 2∫_γ. Then j(Z) − j(Pole) = (aᵢ/2)P mod Λ_A, which vanishes when aᵢ is even.

## Claim 2: explicit family

Reconstruction: c = (0, 3, 3i), p = (10, −10, 10i, −7−9i). Then q_s = Π(x−cᵢ−sᵢ)/(x−cᵢ) · dx²/Π(x−pⱼ). The 10 points are distinct, checked exactly with Gaussian rationals. That gives 3 simple zeros and 7 simple poles. Since deg(den) − deg(num) = 4, q is regular and nonzero at ∞. The limit is Q(−1⁴), with estimated area 0.068 on [−60,60]², which is finite and positive.

I computed the periods with the substitution x = cᵢ + sᵢ sin²θ, which makes the integrand smooth, and 200-point Gauss–Legendre quadrature. The leading derivatives ∂Perᵢ/∂sᵢ at s = 0 are 0.0294, 0.0278, and 0.0305, all nonzero. Newton's method solves Per(s) = (t, t, 2t) for t = 10⁻², 10⁻³, and 10⁻⁴(1+i). The ratios hold to 10⁻¹⁵, and s scales linearly in t.

"Exact" here means exact by the inverse function theorem. Numerics confirm it to double precision; no symbolic certificate is possible without sympy, which is absent. The family is one-parameter and tests only the local residue and area argument, as the note says. By G1 its 1:1:2 ratio cannot be a full-tangent additive triple in an even-parity hexagon.

## Claim 3: dimension and rank

For Q(1^s,−1^(s+4)) the orientation double is hyperelliptic of genus s+1. Then dim Q = 2s+2 = dim H¹₋, and rel = 0 because J fixes all zeros. Rank is half the dimension of the projection of TM to absolute H¹₋, so dim M = 2·rank. Marked points add only relative directions and never rank. The note's conclusion h′ ≤ h−1 is correct.

## Literature

| Source | How checked | Finding |
|---|---|---|
| Mirzakhani–Wright, arXiv:1508.01446 | At source (PDF §1, deleted after reading) | Theorem 1.1: boundary tangent = TM ∩ tangent of the boundary stratum. Corollary 1.2: smaller dimension, rank ≤ rank M, same field of definition. Multicomponent case is in §2. Stated for abelian differentials; the note applies it through the orientation double, which is standard. |
| Wright, cylinder deformations | At source (abstract pages) | Correct paper is arXiv:1302.4108. The note's link 1303.3603 is an unrelated paper. |
| Apisa, arXiv:2110.07540 | At source (abstract only) | "Billiards in right triangles and orbit closures in genus zero strata." The title fits the citation. I did not check the cited sections. |
| Margalit–Winarski, doi:10.1112/blms.12456 | From memory (publisher returned HTTP 403) | Recalled as the Birman–Hilden survey in Bull. LMS 2021. The half-twist lift to a Dehn twist is standard. |

## Overclaims

None are material. "A parity criterion" and "a dimension obstruction at every z" are accurate. The sentence about recognition-result minimality excluding a further cover relies on BBBB/d105 and the predecessor note. That note is under separate review in d122, and I did not check it.

## Next move

The proposed next theorem is well posed. I suggest one sharpening.

- **"Distinct images in one matching kill the additive case."** This is correct and is the right target. Each additive triple has exactly one even weight, so one coincidence j(Z) = j(Pole) per matching is forced.
- **"Minimal locus admits two clean hexagonal degenerations."** This is well posed but carries all four G5 hypotheses. Full-tangent proportionality and the transport are the hard parts.
- **Split by parity.** Split the additive alternative by the parity in G1. For even k, the additive case needs three pairwise distinct weights, and the chain relation adds a homology constraint. That may be easier to exclude geometrically than the odd-k case.
