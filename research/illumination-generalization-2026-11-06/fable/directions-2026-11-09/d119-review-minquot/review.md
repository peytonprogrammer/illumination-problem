# D119: review of the minimal-quotient rigidity note

Date: 2026-11-20. Reviewer: independent referee.

Reviewed file: `minimal-quotient-rigidity.snapshot.md` in this directory. SHA-256 `ece2791b…bd8ce`. The live `qclass-closure/bbbb/minimal-quotient-rigidity.md` is byte-identical.

Context read: `generic-line.md`, `dark-locus.md`, `accumulation.md` and `fold-converse.md` in `qclass-closure/bbbb/`; reviews d89, d105, d115, d116, d118 and d19–23; d20 `periodic.md`; d22 `README.md`; RESULTS §11; d108 and d109 room definitions.

Primary sources: I fetched arXiv 1708.03411 (Apisa–Wright, marked points), arXiv 2110.07540 (Apisa, genus zero) and `highrank.pdf` (Apisa–Wright, high rank). I extracted their text locally with `pdftotext` and then deleted the downloads. No project information went to outside services.

Own code: `checks.py`, log `checks.log`, 0.06 CPU-seconds. Named rooms only: the 12-wall cross, the DB55 stretch at ℓ = 3 + t and the DBas family at ℓ = 4 + t. No search over rooms, rays, directions or reflection words.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Every rational affine mark motion is a fixed rational combination of three absolute periods, so the line test can't contradict periodicity | Sound |
| 2a | Setup at an irrational parameter: non-torus cover, 2 ≤ h < (r+3)/2, individual periodicity of every lift, finite blocking | Sound with fixable gaps (low) |
| 2b | Riemann–Hurwitz count: Y is a sphere in Q(1^z, −1^(z+4)), r = kz + c₃, c₂ + 2c₃ = 2k − 2, z ≥ 1 | Sound |
| 2c | z ≤ 2 is excluded (Apisa 1.5, minimality, AW 1.4, then the full-family exclusion) | Sound with fixable gaps (medium) |
| 2d | Hence z ≥ 3, k ∈ {1, 2}, and k = 2 only at r = 6 or 8 | Sound, given 2c |
| 3a | Degree one: both marks give regular, non-J-fixed periodic lifts on a proper rational primitive locus | Sound (restates d89 with z = r ≥ 3) |
| 3b | Degree two: at least one regular periodic point survives on Y; downstairs rank 2 (z = 3) or 2–3 (z = 4) | Sound with fixable gaps (low) |
| 3c | Smallest unresolved case: proper rank-two locus on a quadratic sphere with three simple zeros | Correctly identified, with one clarification |
| 4 | Overclaiming and conditional status | Not overclaimed; dependency list incomplete (medium) |

## 1. Mark motion and the three periods

**Claim.** Take two doubled horizontal wall periods 2(eᵢ + tuᵢ) with e₁u₂ − e₂u₁ ≠ 0 and one vertical period 2ib. Then any displacement a + vt + ic with rational a, v, c equals xP₁ + yP₂ + zV with rational x, y, z, identically in t.

**Why the periods are absolute.** For a wall γ between two corners, γ − Jγ is closed, because every corner has one lift on X. Its period is twice the wall vector. Cylinder core curves also give absolute periods directly. `checks.py` uses the core curves, which avoids this step.

**Exact check (Part A of `checks.log`).**

| Line | P₁, P₂ (horizontal cores) | V | Minor | Sample decomposition |
| --- | --- | --- | --- | --- |
| Cross, b = 7 + t | 8, 28 + 4t | 8i | 32 | Center O from corner (−7−t, −2): (7 + t) + 2i = ¼P₂ + ¼V |
| DB55, ℓ = 3 + t | 10, 26 + 2t | 10i | 20 | Right mark (9 + t, 1) = −⅖P₁ + ½P₂ + ⅒V |
| DBas, ℓ = 4 + t | 8, 26 + 2t | 8i | 16 | Mark (11 + t, 3) = −¼P₁ + ½P₂ + ⅜V |

Every listed mark decomposes identically in t. The identity also holds at t = 3/11, −2/9 and 1/1000.

**Vacuity control.** On each line, 1,000 random rational motions (a + vt, c) were all fitted, with 0 failures. That includes motions with rates no actual mark has. So a fixed-functional fit along the line can't reject any proposed mark motion. The note's conclusion is correct: this test has no power. Real periodicity requires the functional to hold on the whole 2h-dimensional tangent space of M, and the note says so.

**Cross center.** The center's horizontal offset 7 + t is exactly a quarter of the long horizontal core period 28 + 4t. This agrees with the half-turn argument: twice the corner-to-center period is a corner-to-corner period.

No gap. One optional addition: state the γ − Jγ reason for "twice the lengths give absolute periods".

## 2. The reduction

### 2a. Hypotheses at an irrational parameter

- **Non-torus cover.** If (e₁ + tu₁)/(e₂ + tu₂) = q ∈ ℚ, then (e₁ − qe₂) + t(u₁ − qu₂) = 0. This forces t rational unless the vectors are proportional. Two parallel real absolute periods with irrational ratio can't lie in a lattice. Correct. This supplies AW Assumption 3.2 and hence Lemma 3.3 and Theorem 3.6.
- **Rank.** The lower bound h ≥ 2 comes from three independent absolute vectors x₀, v, y. Part A confirms rank 2 of the horizontal affine span on all three lines. The upper bound comes from d89, because M_t lies in the projection of N. Correct.
- **Individual periodicity.** The argument in `generic-line.md` holds. The projection is linear on a linear chart, so injectivity at the smooth seed gives injectivity along the smooth branch. The marked orbit closure through X_t then has the unmarked dimension.
- **Finite blocking.** I checked AW's definition against the source. Lemma 3.7 counts a segment as unblocked only if it meets neither B′ nor the zeros. So B = ∅ is a valid blocking set when no zero-avoiding segment exists, which d118 §1 supplies. The convex-corner lifts would also do as B (d116 already says so). So d118 is convenient but not needed.

**Gaps (low).**

- The note uses h both for d89's ambient rank and for rank(M_t). Write rank(M_t) ≤ h and use one symbol.
- d116 reviewed only the twist theorem of `generic-line.md`. The paragraph "Why individual periodicity does hold conditionally" was not in its scope. The note should cite d89 directly for periodicity, or flag that paragraph as unreviewed.
- Say that d118 is optional, since B can be the convex lifts.

### 2b. Riemann–Hurwitz count

The local rule is order e(a + 2) − 2 upstairs. Upstairs orders lie in {−1, 0, 1}. Part B lists the allowed pairs (a, e): (−1, 1), (−1, 2), (−1, 3), (0, 1) and (1, 1). So Y has only simple zeros and poles, and its regular points carry no branching. Genus zero forces z + 4 poles, and Riemann–Hurwitz on spheres gives c₂ + 2c₃ = 2k − 2. Counting zeros gives r = kz + c₃. The pole count r + 4 = c₁ is then automatic. Part B confirms it on every feasible row.

z = 0 means Y is a pillowcase. Its orientation cover is a torus, and X would cover it. Excluded at irrational t. Correct.

The feasible (z, k ≥ 2) support for r ≤ 8 is exactly d22's finite list: z = 1 with k ≤ 8, z = 2 with k ≤ 4, and z = 3, 4 with k = 2. Part B checks this.

### 2c. Exclusion of z ≤ 2

**Steps checked against the sources.**

1. *Apisa, Theorem 1.5* (checked): "In genus zero strata of quadratic differentials with two or fewer zeros, the only GL(2, R) orbit closures of rank at least two are full loci of covers of genus zero strata." Downstairs Y has no marked points and z ≤ 2 zeros. Rank h ≥ 2 holds downstairs because pullback is injective on absolute periods and the Hurwitz incidence is finite.
2. *Minimality.* A further cover Y → Z can't branch over regular points of Z, because Y has no points of order ≥ 2. A cover of degree > 1 would contradict Lemma 3.3. So M_Y = Q(1^z, −1^(z+4)).
3. *AW, Theorem 1.4* (checked): the exceptions are Q(−1⁴), Q(2, −1²) and Q(2²). z ≥ 1 avoids them. AW Remark 4.6 shows that Q(−1⁴) is the only genus-zero stratum in which every surface has an involution, so these strata are not hyperelliptic. The note's Möbius-symmetry argument reaches the same conclusion. Citing Remark 4.6 is shorter and exact.
4. *Descent* (d20 Lemma 3): a periodic point over a regular point of Y gives a periodic point of M_Y. So every regular periodic lift on Q lies at an e = 2 point over a pole.
5. *Full-family exclusion.* See below.

**Which earlier result is the "full-family exclusion".** It is the final section of the d19–23 review, "What the chain establishes about rooms". Suppose (D(P); S, T) is dark with at least one interior point. Then its orbit closure is not a full P1, P2 or P3 family over Q(1^z, −1^(z+4)), z ≥ 1. P1 means both points are 2-cycles over one pole, P2 means 2-cycles over different poles, and P3 means a free fold. Its inputs:

- the d21 and d22 censuses (unreviewed code);
- d22 Lemma A, a hand argument by one author;
- the d21 arc proof;
- d23 Lemma 2, the equivariance f∘ρ = σ∘f;
- the d19–23 reviewer's unreviewed hand addition for wall points.

**Its review status.** The d19–23 review was one offline reader, and nobody has reviewed that review. It replayed the z = 1, k = 4 slice in full (665 covers, 420 P1 and 3,990 P3 nodes). It reproduced the cover and node counts for z = 2, 3 and 4. It did not re-run the verdicts for z = 1 at degrees 5–8 or for any z ≥ 2. The note's summary ("replayed a slice and checked some further counts, not every verdict") is accurate.

**Gap 2c-1 (medium): the exclusion is not a pure census result.** d22 found three abstract dark families:

- P1 at k = 4 with group A₄;
- P1 at k = 5 with group A₅;
- P2 at k = 5 with group S₅.

These families are excluded for interior marks only through d23 Lemma 2 and the interior filter. The note should name d21, d22 Lemma A and d23 Lemma 2 explicitly, not only "the archived census". It should also say that the identification "orbit closure of (Q; s₊, t₊) = the full family" uses irreducibility of the orbit closure. The cover locus over the full base is finite, so the orbit closure is one connected Hurwitz component, which is d22's braid orbit. The note states this. It should add that d22's families are exactly these components.

**Gap 2c-2 (low): the census is needed only for k ≥ 3.** The four lifts s±, t± are distinct regular periodic points on Q. In the z ≤ 2 case all four must be e = 2 points, so c₂ ≥ 4. For k = 2, c₂ = 2, so counting alone closes z = 1, 2. Part B lists where the census is genuinely needed: (k, z) ∈ {(3,1), (3,2), (4,1), (4,2), (5,1), (6,1), (7,1), (8,1)}. Say this. It shrinks the census dependence, and degree two never uses it.

### 2d. Conclusion z ≥ 3

With z ≥ 3, r ≥ kz ≥ 3k, so k ≤ 2. For k = 2, e ≤ k forces c₃ = 0 and c₂ = 2, hence r = 2z ∈ {6, 8}. For k = 1, z = r. Part B asserts all three facts.

## 3. Residual claims

### 3a. Degree one

Q is its own minimal quotient. Every regular point of Q has two lifts exchanged by J, so periodic lifts of interior marks are never J-fixed. Properness and 2 ≤ h < (r + 3)/2 are d89's. Rationality is d89's. Correct. This row adds only z = r ≥ 3.

### 3b. Degree two

- The four distinct regular points s±, t± can't map to zeros, because the preimages of zeros are zeros. They can't map to poles with e = 1 either, because those preimages are poles. At most c₂ = 2 of them lie at e = 2 points. So at least two map to regular points of Y, possibly the same point. By descent, that point is periodic for M_Y, and its lifts to Ỹ are not J_Y-fixed. Correct.
- The genus of Ỹ is z + 1. The high-rank threshold is (z + 1)/2 + 1. A stratum component fails by dimension, since 2z + 2 < 3z + 1 for z ≥ 2 (Part C). A holonomy-double locus with an involution I ≠ J_Y gives the nontrivial translation automorphism I·J_Y. Ỹ = X_min, and the proof of AW Lemma 3.3 states that X_min has at most one involution negating ω_min. So I = J_Y, M_Y is the full stratum, and AW 1.4 forbids the regular periodic point. Hence downstairs rank is 2 for z = 3 and 2 or 3 for z = 4 (Part C).

**Gaps (low).**

- Cite the explicit sentence in AW's proof of Lemma 3.3 for uniqueness of the negating involution, instead of the informal "further translation quotient".
- The k = 2 table row omits "defined over ℚ", but the "Next theorem" assumes it. It does hold. M_Y is the preimage of M under the injective ℚ-linear pullback in period coordinates, so it is cut out by rational equations. Add that sentence.
- Note that the downstairs rank equals rank(M_t). For r = 6, this already forces rank(M_t) = 2, sharper than d89's range of 2–4.

### 3c. The smallest unresolved case

The phrase "proper rank-two locus on a quadratic sphere with three simple zeros" is correct. The note itself phrases it as "3–8 simple zeros", and "three or four" in degree two. One clarification: the case Q(1³, −1⁷) with rank 2 first arises at **r = 3 in degree one**, where d89 already forces h = 2 (Part C). It arises again at r = 6 in degree two. Both lead to the same downstairs problem: a proper, rational, rel-zero, primitive rank-two locus in Q(1³, −1⁷) with a regular periodic point. So one theorem for Q(1³, −1⁷) closes r = 3 and the degree-two r = 6 row together. The note should say this.

This is also d20 Theorem P case (B) at r = 3, 4. d20 records it as OPEN, and the introduction of Apisa 2110.07540 says the conclusion "may hold for arbitrary genus zero strata" without proving it.

## 4. Overclaiming and status

The note does not overclaim. It says that no dark component is known or excluded, and that an exclusion of all rows would give only a qualitative area bound. It also credits d20 for the degree split. In fact, the table is d20 §5.2 cases (B) and (C), specialized to the d89/d116 setting. The new content is the specialization, plus the removal of case (A) by the census route.

**Gap 4-1 (medium): the conditional chain is not stated in one place.** The result is conditional on all of the following:

- d80 and its inputs: corrected d16, low-valency, three-sheet, and partition uniqueness at n ≥ 120;
- d89, which reviewed as sound with fixable gaps;
- d115 and d116, both reviewed;
- the d21/d22 censuses and d23 Lemma 2, with the review status in 2c;
- literature statements, two of which I could not check at source (see the audit below).

The opening verdict says "with the dependencies below". It should list them, as the d89 and d115 reviews asked of their notes.

## Ranked gaps and fixes

| Rank | Gap | Fix |
| --- | --- | --- |
| Medium | 2c-1: the full-family exclusion is described as a census result | Name d21, d22 Lemma A, d23 Lemma 2 and the reviewer's addition. State that three abstract dark families exist and are excluded only by equivariance. Give the review scope from 2c. |
| Medium | 4-1: the conditional chain is scattered | Add a dependency line to the opening verdict: d80 → d89 → d115/d116, the census and d23, and the literature. |
| Low | 2c-2: census use is broader than needed | Say that k = 2 closes by counting (c₂ = 2 < 4), so the census is used only for k ≥ 3 at z ≤ 2. |
| Low | 3c: the r = 3 instance is not named | Say that Q(1³, −1⁷) with rank 2 arises at r = 3 (k = 1) and r = 6 (k = 2). |
| Low | 3b: the k = 2 row omits rationality | Add the pullback argument for ℚ-definition of M_Y. |
| Low | 3b: the involution uniqueness is argued informally | Cite AW's proof of Lemma 3.3 (at most one involution negating ω_min). |
| Low | 2c step 3: Möbius-symmetry argument | Replace it with AW Remark 4.6. |
| Low | 2a: notation h and an unreviewed paragraph | Distinguish rank(M_t) from d89's h. Cite d89 for periodicity, or flag the `generic-line.md` periodicity paragraph as outside d116's scope. |
| Low | 2a: d118 is presented as needed | Note that the convex lifts also form a finite blocking set (d116). |

## Literature audit

| Statement | How checked |
| --- | --- |
| AW 1708.03411: definitions of n-point marking and M-periodic point; Theorem 1.2 (credited to EFW) | Against the source. EFW itself was not checked. |
| AW Theorem 1.3 (irreducible n-point markings, n > 1) | Against the source. The note uses it correctly, only to say it doesn't apply. |
| AW Theorem 1.4 and the three exceptions | Against the source |
| AW Remark 4.6 and §5 (genus-zero strata other than Q(−1⁴) are not hyperelliptic) | Against the source |
| AW Assumption 3.2, Lemma 3.3 and its proof (uniqueness of the negating involution on X_min) | Against the source |
| AW Theorem 3.6, and Lemma 3.7's definition of blocking (segments avoiding B and the zeros) | Against the source |
| Apisa 2110.07540, Theorem 1.5, and the remark that zero count is used only in §4 | Against the source |
| Apisa's definition of "full locus of covers" | Not stated in 2110.07540. It is defined in earlier Apisa–Wright papers, which I didn't fetch. I used the standard meaning (half-translation covers), as d20 did. |
| Apisa–Wright high rank, Theorem 1.1, the no-marked-points remark, and Lemma 2.1 | Against the source (`highrank.pdf`) |
| Möller's minimal translation quotient (cited inside AW) | Only as quoted in AW |
| d20 Lemma 3 (descent of periodic points) | Read in the project file. The proof is a two-line sketch, and d19–23 confirmed d20 with corrections that don't touch it. |

## Re-run

```
cd d119-review-minquot && python3 -B checks.py > checks.log
```
