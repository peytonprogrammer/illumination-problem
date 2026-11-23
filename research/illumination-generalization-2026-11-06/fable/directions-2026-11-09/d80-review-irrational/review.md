# D80: Referee review of the irrational-endpoint note

Date: 2026-11-20. Target: `.context/qclass-closure/bbbb/high-valency-geometry.md`, including "A stronger conclusion for individual lifts". Context read: d16 `reduction.md` §§2–6.4 and `d16-review/review.md`, `three-sheet.md`, `low-valency.md`, `eight-sheet.md`, `midpoint-necessity.md`, d79's review and `verify.py`. I read the arXiv abstract of 1905.09358 for the theorem statement.

Own code: `verify.py`, log `verify.log`. It reads the cells of four saved rooms (cov3397, cov3608, cov4474, st279). It reuses d79's corner permutations. There's no search over rooms, rays, directions or reflection words. CPU: 0.2 s.

Re-run: `cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d80-review-irrational && python3 -B verify.py > verify.log`

## Verdict

**Sound with fixable gaps.** I found no error that breaks the argument. The gaps are missing justifications and one omission about Wolecki that changes how the result should be read.

## 1. Use of d16

- Coverage. Mixed rational/irrational pairs are lit by Lemma R (Theorem 1, item 1). If both coordinates of one point are irrational, item 2 gives a contradiction. Otherwise item 2 gives S=(x,y) and T=(ρx+c,v), with x irrational and y, v rational. The note starts from this shape, so every case with an irrational coordinate is covered. Points on interior grid lines are interior, are not in L, and need no separate treatment.
- What moves. For each lift pair (s,t_e), the component F°_0 of Lemma F moves. Lemma F needs only that z is irrational, that ab≠0, and that (a,b) is primitive. The rates are |b| for s and |a| for t in the ξ chart. They're well defined up to an overall sign. Theorem 1's identity a_e + e₁b_eρ = 0 gives the same |a|, |b| for all four lifts. Lifting from period Z² to 2Z² is constant on a component. Removing E[2] preimages is the same as removing d16's L.
- DP-darkness of (P₁,P₂). (s',t') ↦ (s',τt') carries F°_0 onto the (a,−b) component through (s,τt). The pair (s,τt) is M-dark by the unfolding lemma, so Lemma F item 4 applies to both. This is correct.

## 2. Unequal rates

- Degrees. F→E_ξ→E has degree Db², so the map F→M has degree Db²/n and P₁ has degree 2Db²/n. In P¹×P¹, the diagonal intersection number is 2D(a²+b²)/n. This is correct.
- Exclusions. Regular points and convex cones (angle π, separation ≤ π/2) are excluded correctly.
- Reflex corners. Near (c,c) the curve is aσ³+bρ³=0. It has three branches ρ=λσ with λ³=−a/b. P₁−P₂=(1−λ²)σ² has order exactly 2 unless λ²=1. That gives ≤ 6 per reflex corner, which is (1). A branch with λ²=1 lies on the diagonal or the τ-graph. The note's phrase "already excluded" should say that such a branch lies on another component. With equal rates the bound is ≤ 4 per reflex corner.
- Group theory. A_m survives restriction to E and pullback by an isogeny. The symmetric difference has size |a²−b²|·|Z| > 0. Joint ⊇ A_m×A_m holds, but the "commutators" sentence is loose. Goursat gives it cleanly: J₁ ⊇ A_m, so [H₁:J₁] ≤ 2, so [H₂:J₂] ≤ 2 and J₂ ⊇ A_m. The sheet-stabilizer step is correct. Connectivity of each pullback from periods 2v is correct and uses normalization. The bound D ≥ nm is correct.
- Where the hypotheses enter. n ≥ 120 gives m ≥ 15 and A_m (through three-sheet, low-valency and d14). r ≤ 8 gives k ≤ 8. The final inequality m(a²+b²) ≥ 75 > 24 ≥ 3r has a wide margin.

## 3. Equal rates

- Placement. c=0 follows for either sign. Comparing the lifts with ±v forces v ∈ Z and y ≡ v (mod 2). Both marks then lie on horizontal grid edges over one non-pole base point. This is correct.
- The four sheets. S±, T± are four distinct points of one regular fibre, so the four sheets are automatically distinct. The note's argument about disjoint incident cells is unnecessary. Its "same physical edge" case is vacuous: u ≡ ±x (mod 2) with x irrational never puts two distinct marks on one unit edge.
- Common block. d ≤ r comes from the midpoint budget, with no regular coincidences. The single external orbit has valency n−k (three-sheet, n ≥ 120), so the graph is internal and k ≥ 4. With r₀ ≤ r−k this gives k ∈ {4,5,6}. The note does not use three-sheet's lattice-mark split (sizes 2, 3, 8) or eight-sheet.md: those concern 8 incident sheets and don't apply to edge marks. Sizes 2 and 3 fail because k ≥ 4. Sizes 7 and 8 fail because k ≤ r−2.
- Boundary argument. It is rigorous; nothing rests on a picture. The maximal partition is unique, so ι descends to N. N has a unique real zero with k real unramified preimages. The fibre over p has ≤ k−4 real points. Real fold points change the real count by ±2, real e=3 points by 0, and nonreal points not at all. So each arc has ≥ 2 simple real ramification points, giving 2k−2 ≥ 4+2r₀. The case k=4 contradicts d ≥ 2. For k=5 and k=6 the graph is 2-regular with 4-cycle components, and 4 ∤ k. All steps check.
- **Gap (low).** Uniqueness of the maximal partition, which ι-invariance needs, depends on the single-external-orbit theorem and therefore on n ≥ 120. The note doesn't say so. The saved data shows the dependence is real: each of the three 8-cell covers has **two** maximal partitions with k=4.

## 4. Stronger conclusion for individual lifts

This section follows. Only (s,t) and (s,τt) are used, so both coordinates of s may be irrational: d16 item 2 needs all four lifts. The note correctly claims only "same image in B", not one irrational coordinate. The valency argument for a single component, d' ≤ r < n−k, is correct.

## 5. Wolecki

The abstract states that a rational polygon has only finitely many non-illuminating pairs. Combined with d16 Theorem 1 item 3 (a continuum of dark pairs), this rules out irrational dark pairs in **every** strictly simple orthogonal lattice room, with no restriction on n or r. The note's implication is therefore correct. **If Wolecki's theorem is accepted, the note's area and reflex restrictions are unnecessary.** However, d16 §6.4 records a gap in Wolecki's Lemma 2.9 exactly for this half-rational family, so the theorem's proof does not cover this case. The note's value is that it gives a proof that avoids the gap for n ≥ 120 and r ≤ 8. The note says only "Wolecki states" and does not mention the gap.

## 6. Saved-data checks (verify.log)

- Riemann–Hurwitz Σ(e−1) = 2k−2 holds for all 16 block systems in the 4 rooms. Every N has genus 0.
- The budget 2d = R+J holds on all 1391 same-parity edge-mark pairs.
- In cov3397, cov3608 and cov4474 (n = 24, 24, 32, below the range), 27 pairs have all four cells in a 4-cell block, with d=2 or 3. Every pair with d ≤ r has J=0 and R=2d > 0. The note's step "no regular coincidences" therefore excludes darkness, as it should. r₀=0 in every system.
- st279: the only proper system has k=2. The four cells never share a proper block, and d > r for all 924 pairs.

## Findings

1. **Medium.** State that Wolecki + d16 implies the result for all n and r, and that d16 §6.4 found a gap in Lemma 2.9 for this family. That gap is why this restricted proof matters.
2. **Low.** Say that ι-invariance uses uniqueness of the maximal partition, which needs n ≥ 120. Saved rooms below 120 have two maximal partitions.
3. **Low.** Replace the "commutators" sentence with the Goursat argument. Say that a λ²=1 branch belongs to another component.
4. **Info.** The four sheets are distinct for free, and the "same edge" case is vacuous. eight-sheet.md plays no role here.
