# D116: review of the generic-line theorem

Date: 2026-11-20. Reviewer: independent referee.

Reviewed files, both snapshots in this directory:

- `generic-line.snapshot.md`, section "Every irrational parameter tests the same physical component" (main claim).
- `accumulation.snapshot.md`, the "Continuation through the physical component" paragraph and the d80 dependency-chain paragraph.

Context read: d115 review, d89 review, RESULTS §11 entries "Irrational marks", "Bounded denominators" and "Accumulation".

Primary sources: I fetched arXiv 1305.3015 (EMM), 1407.2975 (LMW) and 1708.03411 (Apisa–Wright). I extracted their text locally with `pdftotext`. No other information went to outside services. The citation table below separates checked statements from statements I recall from memory.

Own code: `checks.py`, log `checks.log`, 23 CPU-seconds.

- Check 1 lists the vertical slab rectangles of the named four-reflex cross for t = 0, 1/3, −1/5 and k/7. The circumferences stay (8, 28, 8) and the widths are affine in t.
- Check 2 runs 200 synthetic cases with random rational aⱼ, bⱼ, cⱼ and t₀ = √2 at 60 digits. With s = Kn and frac(n t₀) near η/K, every twist s·dⱼ(t₀) mod cⱼ matches η bⱼ mod cⱼ. The error is within K|bⱼ| times the rotation error (worst normalized error 3.1e−6).
- Check 3 is a control. At rational t₀ = 3/7 the twists take only 35 values, so the arc isn't reached. Irrationality is needed.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Steps 1–2: twist coordinates and the arc z(t₀)+iηv | Sound |
| 2. Passage from iv to v, and continuation over the whole I | Sound |
| 3. Darkness transfer along the orbit closure | Sound with fixable gaps |
| 4. Dark parameters form a locally finite set of rationals | Sound with fixable gaps |
| 5. Literature hypotheses and theorem numbers | Sound with fixable gaps (one misnumbered definition, one paraphrase) |
| 6. Scope and the remaining crux | Sound. One internal inconsistency elsewhere in the note. |
| 7. accumulation.md continuation paragraph | Sound |
| 8. accumulation.md dependency-chain paragraph | Sound with fixable gaps |

## 1. Steps 1–2: the twist argument

**Cylinders.** Inside an open slab between consecutive cut abscissas, the room is a union of rectangles. Each rectangle has a genuine horizontal wall at its top and bottom, because every vertex abscissa is a cut. A vertical ray in copy (εx, +) reflects into copy (εx, −). So each rectangle gives two vertical cylinders on the translation unfolding, one per εx. Each has circumference cⱼ = 2hⱼ, where hⱼ is a difference of fixed rational ordinates. Each has width dⱼ(t) = x_{k+1}(t) − x_k(t) = aⱼ + bⱼt with rational aⱼ, bⱼ. Check 1 confirms this on the cross.

The vertical direction is completely periodic for every t. All vertex lifts, all convex-corner lifts and all eight mark lifts lie on the cuts. At irrational t₀, two distinct rational affine abscissas can't coincide, so the cut order is locally constant.

**Shear and twist.** The shear (x, y) ↦ (x, y + sx) sends a crossing vector (dⱼ, 0) to (dⱼ, s dⱼ). Vertical rim vectors don't change. So the sheared marked surface equals the original cylinders with twist τⱼ = s dⱼ mod cⱼ. Independent twists of individual subcylinders always give valid surfaces. A full twist by cⱼ is a translation isomorphism that fixes both rims pointwise, so it fixes every labeled point. The twist torus ∏ ℝ/cⱼℤ therefore maps continuously into the marked stratum.

**Arithmetic.** K makes Kaⱼ/cⱼ and Kbⱼ/cⱼ integers. Then Kn aⱼ ≡ 0 mod cⱼ and Kn bⱼ t₀ ≡ cⱼ(Kbⱼ/cⱼ)·frac(n t₀) mod cⱼ. If frac(n t₀) → η/K, the twist tends to η bⱼ mod cⱼ. This holds for every small real η, by density of n t₀ mod 1. Check 2 reproduces it numerically.

**Periods.** Write any relative cycle as signed crossings of subcylinders plus vertical pieces along cuts. A twist by η bⱼ adds iη bⱼ to each rightward crossing. A parameter change h adds h bⱼ to the same crossing. Vertical pieces don't change in either case, because ordinates are fixed. So the twisted surface has period z(t₀) + iηv, with v = dz/dt. This includes periods that end at a mark.

**Minor fix (low).** Mark ordinates need to be fixed, not rational. Only wall ordinates enter cⱼ. The hypothesis is harmless but stronger than needed.

## 2. From iv to v, and continuation

EMM Definition 1.1(i) states that each point of N has a neighborhood U whose cone Rf(U) is "a complex linear subspace defined over R in the period coordinates". The map f is proper. So near X_{t₀} the closure is a finite union of complex-linear sheets. One sheet contains z(t₀) + iη_k v for a sequence η_k → 0. That sheet then contains iv, hence v, hence z(t₀) + hv for small real h. The point z(t₀) + hv is the marked unfolding at t₀ + h, because z is affine in a fixed chart. This step is correct.

**Continuation.** Let J = {t ∈ I : X_t ∈ M}. J is closed in I, because M is closed and t ↦ X_t is continuous into the fixed marked stratum. At a boundary point t₁ of a subinterval of J, one sheet through X_{t₁} contains infinitely many line points. An affine function that satisfies a linear equation at infinitely many parameters satisfies it identically. So J contains a neighborhood of t₁. The component of J through t₀ is open and closed in I, so it equals I. The stratum doesn't change across I, because the turn type, strict simplicity, positive lengths and distinct interior marks persist. Cut-order changes at rational parameters don't matter here, because step 3 uses only the period chart.

Applying this from t₀ to t₁ and back gives equal orbit closures for any two irrational parameters. This is correct.

**Minor fix (low).** Finiteness of the sheets near a point uses local injectivity of f together with properness. EMM say "immersed submanifold". State that this gives finitely many preimages and hence finitely many local sheets.

## 3. Darkness transfer

The argument is correct once the stratum is pinned down. The translation unfolding X_t has genus g = r + 1. Each reflex corner gives one zero of order 2 (cone angle 6π). Each convex corner gives one regular point of angle 2π. Label all r + 4 convex-corner lifts and all eight mark lifts. The stratum is H(2^r, 0^(r+12)) with labeled points, and labels remove the orbifold issue.

Define D as the set of surfaces where no saddle-free segment joins any source lift to any target lift while avoiding zeros and convex-corner labels. Then:

- **Lit is open.** A legal segment has an embedded strip free of forbidden points. The strip persists under small changes of period coordinates. So D is closed in the stratum.
- **D is GL⁺-invariant.** GL⁺ maps segments to segments and preserves labels.
- **Physical restriction.** On a physical X_t the Klein group acts by affine automorphisms preserving the forbidden set. So "all lift pairs dark" is equivalent to "the lift in copy (+,+) is dark to every target lift". That is exactly billiard darkness.

If an irrational X_{t₀} lies in D, its orbit closure lies in D, so every X_t with t ∈ I lies in D. If any parameter in I is lit, no irrational parameter can be dark. All four conclusions follow.

**Gap 3a (medium).** The note defines D in one sentence and doesn't name the stratum, the labels or the openness argument. Add the stratum H(2^r, 0^(r+12)), the strip argument for openness, and the Klein-symmetry equivalence. D89's D₄ lives on the quadratic double, while this D lives on the translation unfolding. Say explicitly that this theorem doesn't use D₄.

## 4. Locally finite set of rationals

EMM Theorem 2.2 reads: "Any closed P-invariant subset of H₁(α) is a finite union of affine invariant submanifolds." D ∩ H₁ is closed and P-invariant, so D is the cone over a finite union. Near each point of I, D is a finite union of linear sheets. The affine line meets each sheet in either a local segment or at most one point. A local segment forces the whole of I into D by section 2. Otherwise the dark set is finite on compact subintervals. Irrational points are lit, so the dark points are rational. Accumulation at the open ends of I remains possible, as the note says.

**Gap 4a (low).** EMM state Theorem 2.2 for unmarked strata H₁(α). The marked extension comes from LMW §2.2: "the results of [EMM] work for strata with marked points, i.e. they allow αᵢ = 0." Cite that sentence next to Theorem 2.2. The note's citation of LMW Theorem 2 isn't needed for this step.

## 5. Literature audit

| Citation in the note | Status | Finding |
| --- | --- | --- |
| EMM Theorem 2.1 | Checked | P-orbit closure equals the SL(2,ℝ) orbit closure and is an affine invariant submanifold of H₁(α). Matches. |
| EMM Theorem 2.2 | Checked | Closed P-invariant set is a finite union. Matches. |
| EMM "Definition 1.1 gives the proper immersion and linear charts" | Checked, misnumbered | Definition 1.1 defines an *affine measure*. Its clause (i) contains the proper map and linear charts. Definition 1.2 names the support an affine invariant submanifold. Cite "Definitions 1.1–1.2". |
| LMW §§2.1–2.2 marked points | Checked | §2.1 sets up the marked covers H′, H″. §2.2 states that EMM allow αᵢ = 0. LMW restate EMM's orbit-closure theorem as their Theorem 4. |
| LMW Theorem 2 | Checked | For any x the set of non-illuminated y is finite. The pair set is a finite set plus finitely many covering surfaces. Matches. |
| Apisa–Wright Theorems 1.2, 1.3, 1.4 | Checked | Statements and hypotheses match the table, including n > 1 in Theorem 1.3 and the three excluded strata in Theorem 1.4. |
| Apisa–Wright Theorem 3.6 | Checked | "Either they are both M-periodic points or zeros … or π_Qmin(x₁) = π_Qmin(x₂)." Matches. |
| Wright, cylinder paper, Theorem 1.9 | Checked only through LMW's quotation | LMW quote it for "any completely periodic surface … and any cylinder decomposition", giving k ⊂ ℚ(cᵢ/cⱼ). The note says "a direction containing cylinders". Use the cylinder-decomposition wording. The vertical direction here is completely periodic, so the application stands. |
| Wright, field of definition, Theorem 1.1 | From memory | Used only in the earlier field lemma, not in the new theorem. |
| Filip, Theorem 5.4 | From memory | Not used in the new theorem. |
| Apisa–Wright, high-rank, Theorem 1.1 | From memory | Not used in the new theorem. |

The new theorem uses only EMM Definitions 1.1–1.2, EMM Theorems 2.1–2.2, the LMW marked-point remark and irrational rotation. All of these are checked.

## 6. Scope and the crux

The theorem doesn't overclaim. It doesn't produce a dark room, an area bound or a lighting theorem.

The stated crux is correct. On a d89 line, d115's continuation argument already makes the whole component I dark under the counterexample hypothesis. So one certified lit parameter anywhere in I, rational or irrational, contradicts the hypothesis. The witness must lie in I itself. A witness in a pinched or self-contacting endpoint room doesn't count, and the note says so.

The new theorem isn't needed for that crux. Its added content applies to lines with no known dark interval. On such a line, one dark irrational parameter already darkens the whole component, and lit lines can have only isolated rational dark parameters.

**Gap 6a (medium).** The "Decision" section says that on an arbitrary line "relative closedness alone allows isolated algebraic dark parameters". For lines of this form, the new theorem excludes isolated irrational algebraic dark parameters. Replace "algebraic" with "rational" and point to the new theorem. The opening "Verdict for review" and the field lemma treat only transcendental t. Add a sentence that the new theorem supersedes them for all irrational t.

## 7. accumulation.md: continuation paragraph

The paragraph is correct. N is closed in the marked quadratic stratum. Near any point it is a finite union of linear sheets. An accumulating sequence from the known dark interval forces the affine line into one sheet. The quadratic stratum doesn't change when abscissas cross, so "harmless changes of coordinate order" is right. The paragraph also correctly declines to say anything at an invalid endpoint. It matches the argument d115 suggested.

## 8. accumulation.md: dependency-chain paragraph

The paragraph now names the d80 chain that d115 asked for: corrected d16, low-valency, three-sheet, and partition uniqueness at n ≥ 120. It states correctly that d89 and d115 didn't check the literature.

**Gap 8a (low).** It says the generic-line audit "distinguishes the theorems actually checked". The audit table doesn't mark which statements were checked against primary sources. Add a "checked" column using the table in section 5 of this review.

## Ranked gaps and fixes

| Rank | Gap | Fix |
| --- | --- | --- |
| Medium | 3a: D is defined only informally. | Name the stratum H(2^r, 0^(r+12)) with labels. Add the strip argument for openness and the Klein-symmetry equivalence with billiard darkness. |
| Medium | 6a: The "Decision" section contradicts the new theorem on algebraic parameters. | Change "isolated algebraic dark parameters" to "isolated rational dark parameters" for lines of this form. Note that the new theorem supersedes the transcendental-only arguments. |
| Low | 5: The EMM definition is misnumbered. | Cite EMM Definitions 1.1–1.2. |
| Low | 5: Wright Theorem 1.9 is paraphrased loosely. | Use "cylinder decomposition of a completely periodic surface". |
| Low | 4a: The marked extension of EMM Theorem 2.2 lacks a citation. | Cite the LMW §2.2 sentence on αᵢ = 0. |
| Low | 2: Local finiteness of sheets is left implicit. | Derive it from properness and local injectivity. |
| Low | 1: Mark ordinates are assumed rational. | Assume only that they're fixed. |
| Low | 8a: The checked and from-memory citations aren't separated. | Add a "checked" column to the audit table. |

## Re-run

```
cd d116-review-generic-line && python3 -B checks.py > checks.log
```
