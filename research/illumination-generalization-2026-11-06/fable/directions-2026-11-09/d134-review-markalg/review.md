# D134: review of marked-algebraicity.md (snapshot 2026-11-21 22:30)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/marked-algebraicity.2026-11-21-2230.md`. Context: `d132-review-paramorb/review.md` (gap 1 there), plus the d86 and d116 reviews.

Primary sources: I fetched arXiv 1305.3015v4 (EMM), 1311.2350v3 (Filip), 1407.2975v1 (LMW), 1702.02074v2 (Eskin–Filip–Wright), 1708.03411v3 (Apisa–Wright, "Marked points on translation surfaces"), 2011.08807v2 (Apisa–Wright, "Reconstructing orbit closures from their boundaries") and Stacks tag 0E9C. I extracted text locally with `pdftotext`. No project information left the machine.

Own code: [checks.py](checks.py), log [checks.log](checks.log), under 0.1 CPU-seconds.

## Verdict

**Sound with gaps.** None of the gaps is high. The cover construction exists uniformly, the upstairs stratum is constant, and q is finite onto a closed image. The dimension argument recovers M as a whole irreducible component of an algebraic set. This closes gap 1 of d132 in substance. What remains is the following:

- The algebraic structure on T, p and q is only sketched.
- The marked-point version of EMM rests on a one-sentence remark in LMW.
- The application paragraph claims more than the theorem gives to d132 and d116.

## 1. The cyclic triple cover

**Existence and uniformity.** Covers of X minus the branch set with prescribed local monodromies exist exactly when the local values sum to 0 in ℤ/3. The relation in π₁ is a product of commutators times the puncture loops, and commutators die in an abelian target. The note's assignments are pairs (1, −1) and, for odd n, one triple (1, 1, 1). They sum to 0 and contain a generator, so every such cover is connected. The set of covers is a torsor under H¹(X; ℤ/3) ≅ (ℤ/3)^(2g). Monodromy is topological, so T → A is a finite covering of degree 3^(2g) per assignment, locally constant over A. Every surface in A carries these covers.

- One mark alone can't be the only branch point, because one nonzero value never sums to 0. The note's fix is to branch also at a genuine zero, which exists in genus 2 or more. That fix is correct.
- In genus one with one mark, the stratum is H(0) = GL⁺(2,ℝ)/SL(2,ℤ). The action is transitive, as the note says.
- The line-bundle description also checks. Weights 1 or 2 give a branch divisor of degree divisible by 3, and cube roots of O(D) form a J[3]-torsor. Two remarks:
  - The description isn't needed for existence. A finite topological covering of a quasi-projective variety is algebraic by Riemann existence (SGA 1, XII, Thm 5.1).
  - The universal cyclic cover exists only étale-locally on T, not over T itself. See gap 1.

**Zero orders and Riemann–Hurwitz (checks C3–C5).** Upstairs, each order-a point at a branch point has order 3(a + 1) − 1. A mark gives order 2, and a branched zero gives order 3a + 2. Each unbranched zero of order a gives three zeros of order a. The note doesn't state this last fact. I checked 2g′ − 2 = 3(2g − 2) + 2·#branch on 327 cases with g ≤ 5, all κ and n ≤ 8. All upstairs orders are positive, so B is a genuine-zero stratum, fixed by the assignment. Upstairs genus is always at least 3, so Aut is finite.

**A fact the note should add.** If σ*ω = ω and σ fixes a point of order k with derivative a primitive cube root ζ, then ζ^(k+1) = 1. So k ≡ 2 (mod 3). Fixed points are therefore zeros of B, and the fixed-point profile is a discrete invariant on B. This simplifies the note's transversality paragraph. It also shows how a second structure σ′ arises. In H(2^(3r+n)) the reflex zeros upstairs also have order 2 ≡ 2 (mod 3), so they are admissible fixed points of some other σ′. That is exactly the situation the dimension step must handle, and it does.

**Linearity (check C6).** The σ-invariant part of H¹(Y, Σ_Y; ℂ) has dimension (h¹ + 2)/3 by the Lefschetz formula, because every fixed point lies in Σ_Y. That equals dim_ℂ A = 2g + |Σ_X| − 1 in every case. So q is, locally, a linear immersion in period coordinates. The note doesn't need this, but it confirms that q is an immersion. C7, the hom count 3^(2g), only restates the torsor count and isn't an independent check.

## 2. Upstairs invariance, closedness and applicability of Filip

- The GL⁺ action lifts canonically to T, because the cover is topological and the flat structure pulls back. So p and q are equivariant, and Y = p⁻¹(M) and q(Y) are invariant.
- **Properness of q.** The note's argument is correct. Let Yₙ → Y∞ in B, with deck generators σₙ. The σₙ are flat isometries, so a subsequence converges to σ∞ with σ∞*ω = ω and σ∞³ = 1. σ∞ is not the identity, because the local character at a fixed zero is locally constant. Fixed points stay among the zeros, so the profile persists. The quotient stays in A because orders downstairs are determined and fixed points stay distinct. Quasi-finiteness holds because Aut(Y) is finite. So q is finite onto a closed image, and q(Y) is closed in B.
- q(Y) is a closed invariant set, not necessarily an orbit closure. The note correctly applies EMM Theorem 2.2, not 2.1. Theorem 2.2 gives a finite union of affine invariant submanifolds, and Filip's Theorem 5.4 makes each one quasi-projective. A quasi-projective set closed in the analytic topology is Zariski closed, as Filip notes on p. 4. So q(Y) is closed algebraic in B.

## 3. Descent

- Z = q⁻¹(q(Y)) is algebraic if q is a morphism (gap 1), and dim Z ≤ d because q is finite.
- p is finite, hence Zariski-closed, so p(Z) is closed algebraic, with dim ≤ d, and contains p(Y) = M.
- **Component, not merely containment.** M is analytically irreducible of dimension d. The note's argument works: the connected group fixes each component, and a dense orbit lies in one component. EMM's Definition 1.1 gives the same result more directly, because M is the image of a proper map from a connected manifold. An irreducible variety V has irreducible analytification, so the analytic components of p(Z) are the analytifications of its algebraic components. M lies in one component of dimension at most d. Since dim M = d, M is that component. The note states the needed fact, but it doesn't cite a source (gap 4).
- **Category.** Everything is on coarse quasi-projective spaces. Finite morphisms are closed, and Chevalley isn't needed. Remmert's proper mapping theorem gives analyticity of q(Y) before algebraicity is known. The note uses both correctly.
- **Reduction to orbit closures.** By EMM Definitions 1.1–1.2, each affine invariant submanifold supports an ergodic affine measure, so it is an orbit closure. The note uses this without saying so (gap 5).
- The marked EMM input is load-bearing. Without it, the cover alone doesn't make Y locally linear. q(Y) near q(y) is the union of q(Y ∩ Uⱼ) over the local sheets Uⱼ of q, and those pieces need not be analytic individually.

## 4. Citations

| Citation | Status | Finding |
| --- | --- | --- |
| EMM Thm 2.1, 2.2; Def 1.1–1.2 (1305.3015v4) | Checked | 2.2: "Any closed P-invariant subset of H₁(α) is a finite union of affine invariant submanifolds." Def 1.1(i): proper map from a manifold, local complex-linear sheets over ℝ. EMM never mention marked points. |
| LMW §2.2, Thm 4 (1407.2975v1) | Checked | After Theorem 4: "Note that the results of [EMM] work for strata with marked points, i.e. they allow αᵢ = 0." This is an assertion without proof, and it is the only explicit source for the marked case (gap 3). |
| Filip Thm 5.4 (1311.2350v3) | Checked | "The affine invariant manifold M is a quasi-projective algebraic subvariety of H, defined over Q̄." H is a stratum H(κ) of zeros, so the note correctly uses it only upstairs. |
| Filip Rem 1.7, "Orbifolds" paragraph | Checked | Self-intersections are handled by induction. Proofs run in a finite cover with labelled zeros, and "the results are invariant under passing to finite covers". |
| Filip §4, before Rem 4.1 | Checked | W₀ "coincides with the (reduced) cohomology of the marked points (i.e. zeroes of the 1-form)". The proof uses only H¹(X, Σ). This suggests the theorem holds verbatim with regular marks, but Filip doesn't say so. |
| Stacks 0E9C (Thm 109.25.3) | Checked | M̄_g (g ≥ 2) is DM, proper and smooth. Finite inertia follows: DM gives an unramified diagonal, separated gives a proper one. The note's deduction is correct but indirect. |
| Apisa–Wright 1708.03411v3 | Checked | No theorem stating marked algebraicity. §1 defines n-point markings as affine invariant submanifolds of H*ₙ. The proof before Thm 2.8 applies "[MW17] or [Fil16b]" to a marked locus in the Hodge bundle over M_{g,2}. This is implicit use, not a statement. |
| Apisa–Wright 2011.08807v2 | Checked | The intro cites [Fil16] for algebraicity of orbit closures. §1.3 says "we allow strata to parameterize surfaces with marked points; we treat marked points as zeros of order zero". This is a convention plus citation, not a proof. It is the closest published statement. |
| Eskin–Filip–Wright 1702.02074v2 | Checked | No marked algebraicity statement. It mentions forthcoming work [AW] on "marked points and the illumination and security problems". |

So no source states the marked-point case as a theorem. The note's deduction is needed, and it is a valid one.

## 5. Coverage of d86, d116 and d132

- **d86.** The stratum is H(2^r, 0^(r+4)) plus labels x and y, which is H(2^r, 0^(r+6)) with ordered marks. D is closed and invariant, so the theorem applies directly. The d86 step "D algebraic, forget-y of finite type, fiber count bounded" needs D algebraic in the standard structure on A, and the theorem supplies that (subject to gap 1). Covered.
- **d132.** The stratum H(2^r, 0^(r+6)) is covered, and so is the unfolding variant H(2^r, 0^(r+12)) used in d116. This closes d132 gap 1. It does not close d132 gap 2. That gap asks whether the Schwarz–Christoffel classifying map from parameter cells into A is real-algebraic, and whether E's pullback is semialgebraic. The note's "supplies the algebraicity input" is true, but definability of D still needs that step.
- **d116.** Its main theorem uses only EMM local linearity, and the d116 review says Filip isn't used. Its paragraph on the "marked quadratic stratum" lies outside the note, which treats Abelian strata only. Composing Filip Remark 1.6 (holonomy double cover) with this triple cover would extend it. That extension needs one sentence: poles and regular marks lift to regular points, and those must be marked upstairs.
- Forbidden zeros and endpoint labels are properties of the set, not the stratum, so they need no extra hypothesis. Marks must be distinct from each other and from the zeros, as A requires.

## Gaps

1. **Medium: algebraicity of T, p and q is a sketch.** "Z algebraic" and "p(Z) algebraic" need p and q to be morphisms of quasi-projective coarse spaces. The universal cyclic cover exists only étale-locally on T, because the cube root is chosen locally. The induced map to the moduli stack of B must then descend to coarse spaces. To fix it, take T as the finite étale cover of A given by Riemann existence. Build the cover family on a finite étale refinement, and descend the classifying morphism to coarse spaces. The result is standard, but the note should state it in 3–4 sentences.
2. **Medium: the application paragraph overstates.** State that d132 gap 2 (the semialgebraic classifying map) stays open, and that d116 doesn't need this theorem. Also state that the quadratic stratum in d116 needs the extra Remark 1.6 step.
3. **Low: the marked EMM input is a one-sentence remark.** LMW §2.2 asserts it without proof. Cite the exact sentence. Also cite the Apisa–Wright 2011.08807 §1.3 convention and 1708.03411 as evidence that the field uses it routinely.
4. **Low: irreducibility of analytifications isn't cited.** Cite a standard source for "an irreducible complex variety has connected smooth locus", for example Mumford, *Algebraic Geometry I*, Cor. 4.16, or SGA 1 XII. Also cite Filip p. 4 for Zariski closure = analytic closure of quasi-projective sets.
5. **Low: the reduction to orbit closures is implicit.** Say that each EMM affine invariant submanifold supports an ergodic measure and so is an orbit closure, by Definitions 1.1–1.2. Alternatively, run the argument on each piece of EMM 2.2 directly, using connectedness of N.
6. **Low: zero-order bookkeeping is incomplete.** Add that unbranched zeros give three zeros of the same order. Add that fixed points of an ω-preserving order-3 map are zeros of order ≡ 2 (mod 3). This shortens the transversality paragraph and explains why other quotient structures can occur.
7. **Low: the Stacks citation is indirect.** 0E9C states DM and proper. Finite inertia is a one-line consequence, so state that consequence.

Optional: Filip's proof appears to be marked-agnostic (W₀ is the reduced cohomology of Σ). A sentence noting this would give an independent heuristic check. It isn't a substitute for the cover argument.

## Re-run

```
cd d134-review-markalg && python3 -B checks.py > checks.log
```
