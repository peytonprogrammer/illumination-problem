Advances: L1 — confirms the exact coset test on a rational dark flat, the conditional tie lemma, and a length-independent coefficient bound for one itinerary. It corrects the false-hit warning: closing one endpoint is always safe. A false hit needs two simultaneous closed endpoints.

# D232 review: dark-flat exactness (`snapshot-l1-dark-flat-exactness.md`)

This is an adversarial referee review. The snapshot is identical to the live note `qclass-closure/bbbb/l1-dark-flat-exactness.md` (no diff). Arithmetic is exact (`fractions`). The only room used is the named six-reflex point (a,t,B)=(1,1,1). The review ran no searches.

## Verdicts

| # | Claim | Verdict |
|---|-------|---------|
| 1 | Elimination z=v+Ak, character formula, inverse, relation, offset ℓ·v=−Σnⱼbⱼ/Pⱼ | CORRECT |
| 2 | Closure = persistent congruences; generic open-box miss persists to every positive point; generic characters = condition D | CORRECT (direction checked); minor wording gap |
| 3 | Boundary-face test; "false hit" warning | Test: CORRECT and exact. Warning: CORRECT WITH GAPS. It is false for one closed endpoint and true only for faces of codimension ≥ 2. |
| 4 | Six-reflex calibration at (1,1,1) | CORRECT (recomputed exactly; both chords trace as legal S→T paths) |
| 5 | Real kernel of A is ℝ(aⱼ/Pⱼ); winding group rank m or m−1 | CORRECT |
| 6 | Extreme-ray argument | CORRECT (extremality is not needed) |
| 7 | Conditional tie lemma | CORRECT WITH GAPS. "Regularly" and the visit-M parity choice are left implicit. Under the hypotheses, x* is in J and the τA_M step is valid. |
| 8 | Coefficient bound B_E, \|nⱼ\| ≤ Pⱼ√g B_E, independent of longitudinal lengths | CORRECT. F* can be replaced by an explicit constant, g (Banaszczyk). r_E cannot degenerate. |
| 9 | Geometric scope bullets and closing scope | Mostly CORRECT. Bullet 1's second sentence and bullet 4's sweep claim need more than the note gives. The closing scope statement is accurate. |

## Claim 1: elimination and characters

**Derivation.** Sum the m passage equations. Because z₀=z_m=0, H s = Σb + ΣPₖkₖ. Then zᵢ = Σ_{j<i}(aⱼs−bⱼ−Pⱼkⱼ) = Yᵢ s − Σ_{j<i}bⱼ − Σ_{j<i}Pⱼkⱼ. Substituting s gives vᵢ and Aᵢⱼ = Pⱼ(Yᵢ/H − [j<i]) exactly.

Put tⱼ = Σ_{i>j}ℓᵢ and L = ΣℓᵢYᵢ/H. Then ℓ·Aeⱼ = Pⱼ(L−tⱼ) = −nⱼ, so the sign is opposite to the note's but integrality is unchanged. The inverse is ℓᵢ = t_{i−1}−tᵢ = n_{i−1}/P_{i−1} − nᵢ/Pᵢ. Abel summation gives Σtⱼaⱼ = ΣℓᵢYᵢ = LH, so Σnⱼaⱼ/Pⱼ = 0. The map n ↦ ℓ is injective: ℓ=0 forces nⱼ/Pⱼ = c, and the relation then gives cH=0.

**Offset.** ℓ·v = LΣb − Σⱼbⱼtⱼ = Σⱼbⱼ(L−tⱼ) = −Σnⱼbⱼ/Pⱼ. This holds for every ℓ, not only for characters. ℓ(n) depends on n and P only. So for a fixed persistent n, the character vector and its level are independent of x.

**Condition D.** Write x = Σc_rβ_r with β_r a rational basis of L_x. Then Σnⱼaⱼ/Pⱼ = d(n)·x = Σc_r(d·β_r), with rational d·β_r. Linear independence of the c_r over ℚ forces d ⊥ L_x. That is condition D.

**Check.** `algebra.py` checks the elimination, ℓ·Aeⱼ = −nⱼ, the inverse, the relation, the offset identity and the kernel over 400 random exact instances with m = 2..7. Failures: 0.

## Claim 2: closure and persistence

The closed-subgroup theorem gives the closure of v+Λ as {z : ℓ·z ≡ ℓ·v mod 1 for all ℓ ∈ Λ*}. Write C(x) for this set at the point x.

- **At a generic point x_g,** Λ*(x_g) is exactly {ℓ(n) : n satisfies D}, and the levels are −Σnb/P. So C_gen depends only on L_x, the itinerary and y. It is the same at every generic point.
- **At any positive point x_s ∈ L_x,** Λ*(x_s) contains every persistent character, with the same levels. Then coset(x_s) ⊆ C(x_s) ⊆ C_gen.

So J ∩ C_gen = ∅ implies J ∩ coset(x_s) = ∅. The direction is right: extra relations at special points add congruences and shrink the closure, and a generic miss implies a special miss. The converse fails, as it should. The positive orthant of gap coordinates is one order chart, so J, P and b are constant on it.

**Supporting fact used later.** Λ∩V is dense in V, where V is the connected part of Λ̄. Points of Λ near p ∈ V lie in Λ̄ = V + (a discrete set), so near p they lie in V. So the coset is dense in **every** component of its closure, not only in the closure as a whole.

**Wording gap.** "A generic miss therefore persists at every positive point" refers to the open part. Face hits can appear at special points, because an integer system that is insoluble at generic points can become soluble. The note says this at the end of the face paragraph, but the persistence sentence reads as if it applied to the whole itinerary.

## Claim 3: boundary faces

**The test is exact.** On the face span Rz=c, the coset points are v+Ak with RAk = c−Rv, that is z₀+Γ with Γ = A·ker_ℤ(RA) ⊂ ker R. The relative-open face is open in z₀+ker R, and z₀+Γ is dense in z₀+Γ̄. So the face is hit iff it meets z₀+Γ̄, and the projected test along the connected part of Γ̄ decides that. A zero-dimensional face reduces to integer solvability. I agree with the note.

**The false-hit warning is wrong for a single endpoint.** Suppose the open box misses the closure C, and C meets the relative interior of a codimension-1 face F = {zᵢ = cᵢ}. Let p be a point of C ∩ relint F, and W = p+V its closure component.

- If some w ∈ V had wᵢ pointing into the box, then p+εw ∈ J ∩ C for small ε. That contradicts the miss.
- So V ⊂ eᵢ^⊥ and W lies in the face hyperplane.
- W ∩ relint F is relatively open and nonempty in W. The coset is dense in W (claim 2), so the coset hits relint F.

So closing **one** endpoint and testing the closure never gives a false hit. A false hit needs a face of codimension ≥ 2, meaning two events at closed smooth endpoints at once. Example in ℝ²: J = (0,1)², Λ = ℤ(1,−1) + ℤ(√2,−√2) + ℤ(2,0), and v = (√3,−√3).

- Λ̄ = {x+y ∈ 2ℤ}, which misses the open box but contains the corner (1,1).
- (1,1)−v ∉ Λ, because 1+√3 ∉ ℚ+ℚ√2.

The face test remains correct for all faces and is required only at codimension ≥ 2. At rational points the closure is the coset itself, so false hits occur only at irrational points.

**Calibration check.** At (1,1,1), the smooth endpoint z₃ = 16 (wall x=16 continuing through y=3) has no coset point with the other three events open, in any of the 32 parity cosets (`claim4.out`).

## Claim 4: six-reflex calibration at (1,1,1)

I recomputed it with `claim4.py`, using the room built exactly as in `gatebox.py`'s `__main__`: 16 walls, 6 reflexes, area 73, S=(7,0), T=(20,3).

- Travels (1,1,1,3,3), widths (8,10,8,9,9), and box (7,8), (16,17), (16,24), (16,25) at y = 1, 2, 3, 6 (R): confirmed.
- **Every** lattice point of every coset was enumerated. Exactly 2 of 32 cosets meet the open box, each in exactly one event vector:
  - 00000: (68/9, 145/9, 50/3, 55/3)
  - 11001: (64/9, 151/9, 56/3, 73/3)
- Both match the note.
- Each event vector carries a family of chords. Winding vectors differ by the integer kernel vector (15,12,15,40,40), which changes the slope by 240/1 in dx/dy units. With |k₀| ≤ 40 there are five per vector.
- I traced the three smallest-|slope| chords of each vector with the exact polygon tracer.
  - 00000: slopes dx/dy = 437/9, −1723/9, 2597/9.
  - 11001: slopes 449/9, −1711/9, 2609/9.
  - All six are legal S→T billiard paths. Each follows the itinerary T@1, T@2, T@3, R@6, has no on-boundary event, and ends exactly at (20,3).
- Example: slope 437/9 with k = (3,2,3,8,8).

The statement that 5/8 decides none of the memberships is right: the minimum width 5/8 < Flt(4).

## Claim 5: rank

Ak = 0 gives Σ_{j<i}Pⱼkⱼ = YᵢK/H for every i, where K = ΣPⱼkⱼ. Hence Pⱼkⱼ = aⱼK/H, so the kernel is ℝ(aⱼ/Pⱼ). A has rank m−1 = g, which is full row rank (checked in `algebra.py`). Aℤ^m has rank m exactly when this line has no nonzero integer point, and rank m−1 otherwise. The one-gap example is correct.

## Claim 6: extreme ray

The section P = L_x ∩ ℝ^g_{≥0} ∩ {Σe=1} is a compact rational polytope of dimension dim L_x − 1 ≥ 1. Suppose e ∈ P were strictly positive. Then e ± εw ∈ P for any nonzero w ∈ L_x ∩ {Σ=0}, so e would not be extreme. The ray x₀+te stays positive. A persistent d satisfies d ⊥ L_x, so d·x₀ = d·e = 0. Nonnegativity of e then gives the opposite-sign second growing gap. A repeated visit to one slab gives d ≡ 0. All correct.

Extremality is used only to make "growing" a proper subset. The sign argument works for any e ≥ 0 in L_x.

## Claim 7: conditional tie lemma

**The key step holds.** Elimination is linear and valid for real k. Allow the visit-M winding to be real: P_Mτ := a_Ms − (z_{M+1}−z_M) − b_M. Then x* = v + Ak + τA_M with k_M = 0. `algebra.py` checks this exactly with non-integer τ.

**x* ∈ J.** x* = (z₁..z_M from the source leg, z_{M+1}..z_{m−1} from the reversed target leg). The mouths of visit M are events M and M+1. So x* ∈ J iff every leg event, including both mouths, is strictly inside its interval. "Regularly reach" has to mean exactly that, and the note never defines it.

**The middle release joins two parallel developments.** For a fixed parity of visit M, the developments of visit M differ by translations P_M·ℤ plus a constant. A real τ absorbs any transverse offset, so phases need not match. Slopes must match as signed slopes. Choose the visit-M parity ε_M so that the reversed target leg's developed slope equals s; this choice is always available. The note leaves this choice implicit.

**The contradiction holds.** ℓ(n)·A_M = −n_M. If every persistent n has n_M = 0, then x* satisfies every congruence, so x* ∈ C_gen ∩ J, the coset meets J, and the pair is lit. That contradicts darkness. With γ visited only once, d_γ = n_M/P_M ≠ 0.

**Remaining gaps.**
- The existence of common-slope legs is the hypothesis, and it carries all the geometry.
- If visit M spans several refined subgaps, d_γ = n_M/P_M still holds for each subgap that no other visit touches.

## Claim 8: coefficient bound

**Lift.** The section lattice L_E = L ∩ E₀/V is the intersection of a lattice with a subspace, so it is saturated. Any saturated sublattice is a direct summand, and restriction L* → L_E* is onto. This holds even without primitivity. Primitivity of each cut on the preceding dual makes the kernel of the restriction exactly ℤℓ₁ + … + ℤℓ_{k−1}, which the size reduction needs.

**Size reduction.** The component of ℓ_r orthogonal to ℓ₁..ℓ_{r−1} is its section-character vector at node r, with norm ≤ F*/(2r_U). Nearest-plane reduction in reverse order bounds each of these components by half that norm. This gives the B_E² formula.

**Potential bound.** The values uⱼ = nⱼ/Pⱼ have positive aⱼ-weighted mean zero. So |uⱼ| ≤ max u − min u ≤ Σ|ℓᵢ| ≤ √g|ℓ|. Checked in `algebra.py`.

**Section claims.** p = x* − τA_M lies in E, because the cut characters annihilate A_M. The section group spans E₀. A ball anywhere in J∩E works, because only the next cut must pass through x*. The lift detects A_M independently of the lift chosen, since A_M ∈ E₀. Correct.

**Independence of the longitudinal lengths, and r_E.**
- ℓ(n) and its level −Σnb/P do not depend on x. The cut through x* is ℓ·z = level + k with k ∈ ℤ, because ℓ·x* ≡ ℓ·v.
- Every node of the recursion is therefore a node of a finite tree. Its depth is ≤ g, and its branching is bounded by the n-bounds and the finitely many integer levels meeting the bounded slice.
- The tree is determined by J, P, b (fixed by y and the signed itinerary).
- Each non-empty node has inradius > 0, so min r_E > 0 over the tree.
- **r_E cannot tend to 0 along the flat or along the ray.** The bound is independent of the longitudinal lengths, as claimed.

**What the bound needs from flatness.** It uses flatness only for Euclidean balls. An open ball of radius r missing a coset of a rank-d lattice L forces μ(L) ≥ r. Banaszczyk's transference theorem (Math. Ann. 1993) gives λ₁(L*)μ(L) ≤ d/2. So there is a dual vector with |ℓ| ≤ d/(2r) ≤ g/(2r). Replace F* by g. This is explicit for every g, and the unknown Flt(i) for i ≥ 3 is irrelevant.

I confirmed the constant from secondary sources only, not the original paper:
- [Aggarwal–Stephens-Davidowitz, arXiv:1907.09020](https://arxiv.org/abs/1907.09020)
- [Regev's lecture notes](https://cs.nyu.edu/~regev/teaching/lattices_fall_2004/ln/transference.pdf)

Hurkens' Flt(2) is for general convex bodies and is not needed.

## Claim 9: geometric scope

- **Bullet 1, first sentence:** matches the long-corridor theorem (`bbbb/README.md`). Its hypotheses are fixed chambers, sealable doors of the corridor's width, and an empty rectangle. Correct as a citation.
- **Bullet 1, second sentence:** "the conditional tie applies … if the end legs avoid every other visit to γ" omits the hypothesis that does the work, namely regular legs at a **common slope**. The README's pointwise construction supplies them (a common direction and first regular door hits, at any one geometry). The note should cite that step rather than imply the tie is automatic.
- **Bullet 2:** correct and correctly hedged (d_γe_γ = −d_ηe_η fixes a ratio only).
- **Bullet 3:** correct. With equal P the +1/−1 entries cancel in d_γ.
- **Bullet 4:** "sweeping the long middle gives a matching signed phase with fixed ends" is stated as fact and isn't proved here. It is a large-length statement in the corridor theorem's style, not a pointwise statement on the flat. "Opposite open mouths are directly visible" is correct, since the open rectangle is convex.
- **Closing scope** ("no relation locking every itinerary, no eight-reflex exclusion, no N₀"): accurate. So is the stated first unproved implication.

## Scripts and output

| File | Checks | CPU |
|---|---|---|
| `claim4.py` → `claim4.out` | Six-reflex (1,1,1) roof itinerary: itinerary data, all lattice points in all 32 parity cosets (open box and face z₃=16), and exact traces of three chords per hit | 0.46 s |
| `algebra.py` → `algebra.out` | 400 random exact instances: elimination, τA_M identity, character, inverse, relation, offset, kernel, rank, potential bound | 0.09 s |

Total CPU is about 0.6 s. The scripts import `../d231-review-gate-box/gatebox.py` read-only. I did not run the B=18 roof itinerary or (1,2,3).

## Which lemma does this advance, and what is the first case still open?

It advances **L1**. On a rational dark flat, the open-box obstruction for a fixed itinerary is exactly a persistent-congruence miss. A once-visited growing gap with common-slope regular end legs lies in a persistent relation with another growing gap. That relation's coefficients have a bound that depends only on (J, P, b, g), with F* replaceable by g.

**First open case.** Take a growing gap that every candidate itinerary visits at least twice. Examples are two strip components at the same gap, or an excursion. Here the pushed coefficient d_γ can cancel (equal P, entries +1 and −1), so the tie lemma gives nothing. Close behind it is the existence of common-slope regular legs when no separating sealable rectangle exists. The tie lemma assumes those legs; nothing in the note produces them.
