# d151 referee review: local-global.md (snapshot 2026-11-22-0250)

**Verdict: sound with gaps.** The density theorem is correct as stated, including the lower-density claim and the noncongruence case. The DB55 row checks exactly. The citation supports the claim. The fixed-chain remark is correct but mostly tautological. No gap is fatal. The largest issue is that the note never says which legality notion the theorem uses, and the DB55 refutation is narrower than its wording.

Checks: `checks.py` (named room DB55 only, no searches), output in `checks.log`, 0.3 CPU-seconds.

## 1. Density theorem

The argument holds.

- **Finite index.** SL₂(ℤ) acts on the finite set of labelled n-square origamis. Corner stops and endpoint lifts sit at square vertices, so their labels go along with the action. The stabilizer of the labelled surface has finite index. Fixing the labels pointwise means taking the kernel of a homomorphism to a finite symmetric group, so that subgroup also has finite index. An affine lift is unique up to the finite group of translation automorphisms, so it doesn't matter which lift you pick. The note's one-line justification is thin but correct.
- **Blockage under affine maps.** Suppose an affine map has derivative h and fixes every corner stop and both endpoint lifts. It maps a corner-free straight segment from s̃ to t̃, with holonomy w, to a corner-free straight segment from s̃ to t̃ with holonomy hw. Its inverse does the same in reverse. Vector-level legality means "some lift pair is legal." H fixes every lift, so vector-level legality is also H-invariant. Convex corners are regular points of the 4-copy unfolding, so the corner stops must be marked; the definition of H does mark them.
- **Counting.** Write SL₂(ℤ) = ⋃ gᵢH, with d cosets. Every content-m vector v has the form gᵢ h (mp). The map v ↦ (i, gᵢ⁻¹v) is injective, so #{content m in B_R} ≤ d · #(H·mp ∩ B_{CR}). The left side is at least c R²/m² for every large R. That gives a lower bound for every R, so the liminf is positive and **lower density** follows, not only upper density.
- **Noncongruence.** The argument uses only finite index. It holds for noncongruence H.

Empirical illustration (§5 of the log): among primitive directions in a ball of radius R, the lit fraction for DB55 with S=(2,2), T=(4,4) is 0.833, 0.771, 0.729, 0.725, 0.722 for R = 5, 10, 20, 30, 40. This is consistent with the theorem, but it doesn't prove anything.

## 2. DB55 pencil

**Verified exactly.** A direct billiard trace (reflect at flat walls, stop at every convex or reflex corner, all four sign choices, any traversal count) runs over all 121 directions (1, 2j) with |j| ≤ 60. It gives lit if and only if 5 ∤ j, with 0 mismatches. For 5 | j, every lattice point the ray visits has y = 2, and every ray stops at a corner.

**Refutation.** For every N ≤ 60 coprime to 5, p₀ = (1,0) is dark and p_N = (1,2N) is lit, and the two agree modulo 2N (48 of 48 cases). So the direction observable for this pair factors through no modulus coprime to 5. That includes every 2^k, and is stronger than the note's claim. It does not rule out a test modulo 10. It also says nothing about class darkness, because this class is lit. The note says this itself.

**Structural reason for the 5.** In a direction (1, q), the ray crosses every vertical grid line at a lattice point. The corridor opening is the open segment from (5,2) to (5,3), and it contains no lattice point. So the ray never enters the corridor. The log confirms that the maximum visited x is 5 and that no cell with x ≥ 5 is ever entered. The dynamics are therefore those of the closed left 5×5 square, with corner stops at (0,0), (0,5), (5,0), (5,5), (5,2), and (5,3). The 5×5 square unfolds to a 10×10 torus. At time t the ray sits at the fold of (2+t, 2+qt) mod 10.

When q = 2j and 5 | j, qt ≡ 0 mod 10 for every integer t. The ray then sees only lattice points with y = 2, so it never reaches T = (4,4). It eventually stops at (5,2) or (0,0). When 5 ∤ j, the congruence jt ≡ 1 or 2 mod 5 has a solution with x folding to 4, and T is reached before any stop.

This closed-box model matches the billiard on all 241 directions (1,q) with |q| ≤ 120. It also reproduces "lit iff 5 ∤ j" for |j| ≤ 500. So the modulus 5 is the side length of the left square, or half the 10-period of its horizontal and vertical cylinders.

## 3. Schmithüsen citation

arXiv 0704.0416 is G. Schmithüsen, *Origamis with non congruence Veech groups* (2007). The abstract gives two explicit genus-2 origamis with noncongruence Veech groups, and one noncongruence example in every genus g > 1. That supports "square-tiled Veech groups need not contain a principal congruence subgroup." A noncongruence subgroup contains no Γ(N) by definition. Marking points only passes to a subgroup, which still contains no Γ(N). The note's inference is correct. Only the abstract was fetched; no project information was sent.

## 4. Fixed-chain answer

The answer is correct. In a fixed development with both endpoint images fixed, exactly one straight path joins them. Any other path with the same endpoints is not straight, so it bends. That part is a tautology.

The DB55 witness checks out. Between its endpoints, the segment from (2,2) to (10,2) meets (5,2) reflex, (6,2) smooth, (7,2) smooth, and (8,2) reflex. The segment runs along a wall, not only through two reflex tips. Direction (3,2) does light (2,2) → (10,2), at step 16 forward and step 6 backward.

The answer is complete only in its own terms. The real alternatives are a different endpoint image, lift, or seam itinerary. The note names these and correctly leaves their existence open.

## 5. Scope

**Proved:**

- H-invariance of legality.
- Positive lower density of an H-orbit, given a legal seed.
- The DB55 row and its failure modulo every N coprime to 5.
- Existence of noncongruence square-tiled Veech groups in general (cited).

**Not proved:**

- That any legal seed exists.
- Any odd-prime or congruence characterization of dark classes.
- Whether any BBBB room double has a noncongruence marked group.

**Precise open existence statement.** Take a strictly simple square-lattice room, a same-parity pair (S,T), and a parity class not excluded by a known obstruction (the R22 fold parity or the cov4181 sheet separation). Is there a content m and an H-orbit of content-m developed vectors containing a corner-free straight segment from a lift of S to a lift of T? Equivalently, in fixed-chain language: is there an alternative endpoint image with the required primitive parity whose seam crossings are strictly interior?

For one named room, the question is finite for each m. d149 found legality constant on cusps, so in principle a cusp table of H ∩ Γ(2) decides the room. The general statement has no bound on m and no uniform mechanism.

## Gaps

1. **Medium. The theorem's legality notion is not pinned down.** §1 of the note defines exact, relaxed (all corner continuations), and formal-image legality, and says these give different sets. The invariance proof covers only the exact notion, a corner-free straight segment. Invariance of the relaxed notion would need the corner continuation rules to commute with affine maps, and the note doesn't show that. State that the theorem is about exact legality.
2. **Medium. The DB55 refutation is narrower than its wording.** It refutes only per-direction tests that are functions of p mod N, for one pair, in a lit class. It doesn't touch tests that use fold or seam geometry, which is how R22 works. It also doesn't touch a test modulo 10. The note half-says this, but the Result line reads more broadly.
3. **Low. Finite index of H is asserted in one line.** Give the kernel-of-a-finite-permutation-action argument, and say that the choice of affine lift is immaterial.
4. **Low. The normal core K and the intersection with Γ(2) are unnecessary for density.** Left cosets of H suffice. Γ(2) matters only for the parity bookkeeping.
5. **Low. The structural reason for the 5 is missing.** The note says "Five explains this particular pencil" without saying why. The reason is that the corridor opening contains no lattice point, so the left 5×5 square acts as a closed box with a 10-periodic unfolding (§2 above).
6. **Low. Wording.** The claim "p₀ and p_(2^k) agree modulo 2^k" undersells the result: they agree modulo 2^(k+1). "Residue zero is the horizontal line at y = 2" means the ray visits only lattice points on y = 2, not that the ray is horizontal. The fixed-chain section changes T from (4,4) to (10,2) without saying so. "Original construction" for Schmithüsen is a priority claim the review did not check. Hubert–Lelièvre's H(2) work is roughly contemporary.
7. **Low. The pencil mask.** The review did not replay mask 30 from `pencil_components`. The direct billiard row agrees with it.
