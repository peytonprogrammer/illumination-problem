# D81: Lowering the area threshold for d ≥ 2n/3

Date: 2026-11-20. Setting: a normalized strictly simple orthogonal lattice room with r ≤ 8 reflex corners and area n. S and T are distinct same-parity interior lattice marks. d is the marked valency of [midpoint-necessity.md](../../../../qclass-closure/bbbb/midpoint-necessity.md).

**Result.** For n ≥ 49, every such pair is directly visible or has d ≥ 2n/3. The proof uses the same dependencies as the reviewed notes plus Jordan's 3-cycle theorem. It doesn't reach N = 21. The gap is 21 ≤ n ≤ 48, in the explicit (k, m, zero-pattern) cases of section 6. The saved data contain no obstruction: among 9,851 pairs in 2,145 saved rooms with 21 ≤ n ≤ 40 and r ≤ 8, three pairs have 3d < 2n, and all three are directly visible.

## Threshold table

k is the block size of a maximal block system, m = n/k, and z is the least positive number of quotient zeros over one pole. "Proved" means d ≥ 2n/3 or direct visibility for every pair in that case.

| Case | Reviewed threshold | Proved here | Step that limits it |
| --- | ---: | ---: | --- |
| Primitive | n > 64 | n ≥ 49; n ≥ 25 if reflex corners lie in ≥ 2 classes | Burness–Guralnick fpr ≤ 1/2 gives n ≤ 6z_x, and z_x = 8 when all 8 reflex corners share a class |
| k = 2 | n > 48 | n ≥ 50 (z = 4), 38 (z = 3), 26 (z = 2), 12 (z = 1) | Theorem G(a) on the block action, m ≤ max(6z, z²) |
| k = 3 | n > 36 | n ≥ 27 if z = 1; n ≥ 39 if z = 2 | z = 1: transversal alternative at m = 7, 8. z = 2: Theorem G(a), m ≤ 12 |
| k = 4 | n ≥ 52 | n ≥ 32 if z = 1; n ≥ 52 if z = 2 | z = 1: transversal alternative at m = 7. z = 2: Theorem G(a), m ≤ 12 |
| k = 5 | n ≥ 50 | n ≥ 40 (n ≥ 35 if z_x ≤ 7) | spare blocks for g_x² at m = 7 |
| k = 6 | n ≥ 72 | n ≥ 42 | simplicity of A_(m−2), m ≥ 7 |
| k = 7 | n ≥ 98 | n ≥ 49 | simplicity of A_(m−2), m ≥ 7 |
| k = 8 | n ≥ 120 | n ≥ 56, or visible | simplicity of A_(m−2), m ≥ 7 |

No k = 4 room has 49 ≤ n ≤ 51 and no k = 8 room has 49 ≤ n ≤ 55, so every row holds for all n ≥ 49. **Overall N = 49.**

## Dependencies

Dictionary D0, corrected Proposition R1 (gcd 1 per axis), and d10 Fact L. D14 Theorem G and the Burness–Guralnick Corollary 2 it rests on (CFSG). Jordan's theorem: a primitive group containing a 3-cycle contains the alternating group (Wielandt, Theorem 13.3). The matching lemma of [low-valency.md](../../../../qclass-closure/bbbb/low-valency.md). The spare-block lemma of [three-sheet.md](../../../../qclass-closure/bbbb/three-sheet.md). The [eight-sheet lemma](../../../../qclass-closure/bbbb/eight-sheet.md). Reviews: [d78](../d78-review-valency/review.md), [d79](../d79-review-eight-sheet/review.md).

## 1. Where 48, 36 and 120 come from

Three facts drive every threshold.

- **Cycle types and Riemann–Hurwitz.** Each branch permutation g_x has cycles of length 1 (convex corners of class x), 2 (regular points) and 3 (reflex corners of class x). Genus 0 gives Σ_x (k_x + 2z_x) = 2n − 2, where k_x and z_x count 2- and 3-cycles. With 4n = Σ_x (f_x + 2k_x + 3z_x), this gives Σ_x f_x = r + 4. Every proper quotient N of degree m has genus 0, the same cycle lengths, and Σ fixed points = Z_N + 4, where Z_N counts its zeros.
- **Class-size budget.** R1 gives every proper nontrivial quotient at least one zero. Over a zero (local degree 3) the inner cover can't ramify further, so each zero has exactly b reflex preimages, where b is the block size. Hence b·Z ≤ r ≤ 8. So k ≤ 8, Z_N ≤ ⌊8/k⌋, and every block system has block size ≤ 8.
- **Theorem G(a).** A primitive group with an order-3 element having z 3-cycles contains A_m or has m ≤ max(6z, z²). For the block action, h_x² has z 3-cycles, one per quotient zero at pole x.

The old numbers follow.

- **48 (k = 2).** Z_N ≤ 4, so z ≤ 4 and m ≤ max(24, 16) = 24. The matching lemma needs H ⊇ A_m, so n = 2m > 48.
- **36 (k = 3).** Z_N ≤ 2, so m ≤ 12 and n = 3m > 36.
- **120 (uniform).** The spare-block lemma needed (m − 2)!/2 > (k!)² to make pointwise block stabilizers transitive. That gives m ≥ 7, 7, 9, 10, 12, 14, 15 for k = 2 to 8. The class budget needs m > 8. Theorem G needs m ≥ 25 for k = 2 and m ≥ 13 for k = 3, 4. The binding case is k = 8, m = 15.
- **64 (primitive).** Theorem G with z = 8 gives max(48, 64) = 64. The 64 is the product-action bound z²; the generic bound is 6z = 48.

Under the weak target, an external orbit equal to all pairs in distinct blocks gives d ≥ n − k = n(1 − 1/m). This is ≥ 2n/3 exactly when m ≥ 3, and m ≥ 3 always holds: a degree-2 quotient has no zero. So the weaker target never relaxes "all external pairs form one orbit". All the gain below comes from sharper proofs of that statement and of the primitive bound. The saved room cov2493 (n = 21, k = 7, m = 3) has d = 14 = 2n/3 exactly, so the m = 3 margin is tight.

## 2. Primitive case

**Proposition P.** Let 1 ≤ r ≤ 8, n ≥ 21, G primitive. Then G ⊇ A_n, so d = n − 1, or n ≤ 6z_x for every class x with z_x ≥ 1. In particular, n ≥ 49 forces G ⊇ A_n. So does n ≥ 25 when reflex corners occur in two or more classes.

*Proof.* Fix x with z_x ≥ 1 and set u = g_x², an element of order 3 with z_x 3-cycles. If G isn't in the Burness–Guralnick family, fpr(u) ≤ 1/2, so n ≤ 6z_x. Otherwise G ≤ S_μ wr S_κ in product action on λ-subsets, with A_μ^κ ≤ G and n = C(μ,λ)^κ. The case λ = κ = 1 is the natural action, where G ⊇ A_n. Write u = (u_1, …, u_κ)π.

- If π ≠ 1, d14 step 3 gives n ≤ 4z_x ≤ 6z_x.
- If π = 1, d14 step 4 gives z_x ≥ C(μ,λ)^(κ−1) C(μ−2, λ−1). With z_x ≤ 8 and n ≥ 21, this rules out κ ≥ 3 (z ≥ 9), κ = 2 with λ ≥ 2 (z ≥ 30), and κ = 1 with λ ≥ 3 (μ ≥ 7, z ≥ 10). Two cases remain.

*κ = 1, λ = 2 (S_μ on pairs, μ ≥ 7).* A permutation of the μ points acts on pairs with cycle lengths in {1, 2, 3} only if its own cycles have length ≤ 3 and it doesn't mix 2- and 3-cycles. A pair across a 2-cycle and a 3-cycle has length 6. A class y with z_y ≥ 1 is therefore of type 1^α 3^γ on points, with α ≤ μ − 3. It fixes C(α, 2) pairs and has z_y = (C(μ,2) − C(α,2))/3 ≥ μ − 2. The budget C(α, 2) = f_y ≤ 12 forces α ≤ 5, and z_y ≤ 8 then forces C(μ,2) ≤ 34, so μ ∈ {7, 8}. Thus n = C(μ,2) ≤ 28 ≤ 6(μ − 2) ≤ 6z_y for every reflex class y, which is the second alternative. (Fixed-point counting alone doesn't exclude it. For μ = 7, the point types 3²1, 2³1, 2³1, 2²1³ give 21 pairs with r = 7, 11 fixed pairs and genus 0 by Riemann–Hurwitz. Whether such a tuple exists wasn't checked. It lies in the n ≤ 6z_x residual.)

*κ = 2, λ = 1 (sheets = [μ]², μ ≥ 5).* Each g_p is (a,b): (i,j) ↦ (a i, b j), or swap type (i,j) ↦ (a j, b i).

- Generators of swap type exist, since G isn't in the base group, which preserves rows. Their number is even by the product relation. check.py confirms that a product relation holds in all 2,145 rooms.
- A swap-type g with cycle lengths in {1, 2, 3} has g³ a swap-type involution. Write g³ = (a′, b′)τ with a′b′ = 1. Its fixed points are the μ pairs (i, b′ i). They are exactly the sheets in 1- and 3-cycles of g, so f_g + 3z_g = μ.
- Every reflex class y has z_y ≥ μ. If g_y is non-swap, d14 step 4 applies. If it is swap type, g_y² = (ab, ba) with ab conjugate to ba, so z_y ≥ 2μ − 3. Two reflex classes would need r ≥ 10, so only class x has reflex corners. g_x can't be swap type, since f + 3z = μ would give z_x ≤ μ/3.
- So g_x = (a, b). Suppose u = (3-cycle, 1). Then a has one 3-cycle, and b = 1, because a 2-cycle of b would meet a's 3-cycle in a 6-cycle. So r = z_x = μ. The two swap-type generators have z = 0, so each fixes μ sheets. Then 2μ ≤ r + 4 = μ + 4 gives μ ≤ 4, a contradiction.
- Otherwise both u_1 and u_2 are nontrivial. Then z_x ≥ 2μ − 3, so μ = 5 and z_x = 7, and a, b are each one 3-cycle plus 2 fixed points. Then f_x = 4, and total fixed ≥ 10 + 4 > r + 4 = 11.

So the family occurs for n ≥ 21 only in the natural action or with n ≤ 6z_x. For n ≥ 49, z_x ≤ 8 makes n ≤ 6z_x impossible. If reflex corners occur in two or more classes, the least positive z_x is ≤ 4, so n ≤ 24. ∎

## 3. Imprimitive case: making external pairs one orbit

Fix a maximal block system with block size k, m blocks, and primitive block action H. Let π: G → H, write G_{D,E} for the setwise stabilizer of blocks D and E, and K_{D,E} for the subgroup fixing every sheet of D ∪ E. The spare-block argument of three-sheet.md uses its order inequality only to get condition (T).

**(T)** H ⊇ A_m, m ≥ 7, and π(K_D) and π(K_{D,E}) contain the alternating group on the blocks other than D (resp. D, E), for all D and E.

Given (T), that note's proof gives the following. Either all ordered external pairs form one orbit, or a G-invariant partition into q classes exists, with 2 ≤ q ≤ k and every class meeting every block. It uses only m ≥ 4, transitivity of K_{B_s,B_t} on spare blocks, and transitivity of K_D on blocks ≠ D.

**Lemma T1 (sections).** If H ⊇ A_m and m − 2 > max(k, 4), then (T) holds.

*Proof.* π(K_{D,E}) is normal in π(G_{D,E}) ⊇ A_(m−2). Its intersection with A_(m−2) is all of A_(m−2) or trivial. If trivial, A_(m−2) is a section of G_{D,E}/K_{D,E} ≤ S_k × S_k. Then it is a composition factor of a subgroup of S_k, so (m−2)!/2 ≤ k!, false for m − 2 > k ≥ 2. The single-block case is the same with A_(m−1). ∎

This replaces (m−2)!/2 > (k!)² by m ≥ max(7, k + 3).

**Lemma T2 (the element g_x²).** Suppose pole x carries exactly one quotient zero, and m ≥ max(7, 5 + z_x − k). Then (T) holds.

*Proof.* h_x² is a 3-cycle, so Jordan's theorem gives H ⊇ A_m. Let y = g_x². It fixes every sheet outside class-x 3-cycles. The k reflex corners over the zero fill its three blocks. Any other class-x 3-cycle maps to a fixed block, so it lies inside one block. So the support of y meets at most 3 + (z_x − k) blocks, and two blocks D, E avoid it. Then y ∈ K_{D,E}, and π(y) is a 3-cycle in the alternating group on the remaining blocks. π(K_{D,E}) is normal in π(G_{D,E}) ⊇ A_(m−2), which is simple for m − 2 ≥ 5, so π(K_{D,E}) ⊇ A_(m−2). H is 2-transitive, so K_{D′,E′} is conjugate to K_{D,E} for every ordered pair. K_D ⊇ K_{D,E} for every E ≠ D gives transitivity on blocks ≠ D. ∎

For k ≥ 5, Z_N = 1 and z_x ≤ 8. So T2 applies at m ≥ 7 for k ≥ 6, at m ≥ 8 for k = 5, and at m = 7 for k = 5 when z_x ≤ 7.

**Lemma B (classes).** In the second alternative with m ≥ 7, the classes have exactly m sheets and meet each block once. This alternative is possible only if (k, m) ∈ {(3, 7), (3, 8), (4, 7)}, with r ≥ 7.

*Proof.* For a sheet s, B(s) ∩ C(s) is a block, and s ↦ B(s) ∩ C(s) is G-equivariant. So its size e is constant, and every class has e·m sheets. The classes form a proper nontrivial block system, so e·m ≤ 8 by the class-size budget. Hence e = 1, and sheets are identified G-equivariantly with (block, class) pairs. The class quotient has one zero (m·Z′ ≤ 8), say at pole y, and g_p = (h_p, l_p) acts coordinatewise.

- A 3-cycle of l_y forbids 2-cycles in h_y (6-cycles), so the 3m sheets over it form m reflex corners of class y.
- A quotient zero at a pole x ≠ y would add k more, so r ≥ m + k ≥ 9. So all quotient zeros lie at y, h_y has z(h_y) ≥ 1 3-cycles, and l_y has no 2-cycles: one 3-cycle and k − 3 fixed points.
- Counting class-y 3-cycles gives r ≥ m + z(h_y)(k − 3), so z(h_y)(k − 3) ≤ 8 − m. ∎

**Per-k conclusion.** If an external marked pair exists and (T) holds, then all external pairs form one orbit when m ≥ 9 or (k, m) is outside Lemma B. Then d ≥ n − k ≥ 2n/3. For k = 2, the matching lemma needs only H ⊇ A_m and m ≥ 6, since its alternative is a degree-2 pillowcase quotient that R1 excludes. An external marked pair exists unless all 8 marked sheets share one block. That forces k = 8, and the eight-sheet lemma gives direct visibility. With the H ⊇ A_m conditions from Theorem G or Jordan, this gives the table.

| k | Zero pattern | Conditions | Threshold |
| --- | --- | --- | --- |
| 2 | z = 1 / 2 / 3 / 4 | m ≥ 6 and m > max(6z, z²) | m ≥ 6 / 13 / 19 / 25 |
| 3 | z = 1 | T1 (m ≥ 7), not Lemma B → m ≥ 9 | n ≥ 27 |
| 3 | z = 2 (both zeros at one pole) | m ≥ 13 | n ≥ 39 |
| 4 | z = 1 | T1 (m ≥ 7), Lemma B excludes m = 8 | n ≥ 32 |
| 4 | z = 2 | m ≥ 13 | n ≥ 52 |
| 5 | Z_N = 1 | T1 or T2 at m ≥ 8 | n ≥ 40 |
| 6, 7, 8 | Z_N = 1 | T2 at m ≥ 7 | n ≥ 42, 49, 56 |

For n ≥ 49, each (k, m) with km = n satisfies its row. k = 7 at m = 7, 8, 9 and k = 8 at m = 7 to 10 use T2, the cases T1 can't reach. Lemma B excludes the class alternative for k ≥ 5 at m = 7, 8.

## 4. Theorem

For a normalized strictly simple orthogonal lattice room with r ≤ 8 and area n ≥ 49, every distinct same-parity interior lattice pair is directly visible or has d ≥ 2n/3. Corrected after review (d82): with midpoint-necessity.md, a dark pair with r ≤ 8 and n ≥ 49 satisfies (i), so it must have at least 2⌈2n/3⌉ − 16 − ⌊n/2⌋ regular coincidences outside the source class (26 at n = 49), none of them the midpoint of a real path. Darkness does not exclude such candidates; the lemma that one of them is reached is open.

## 5. What a weaker target can't buy

The weak target gains nothing once external pairs form one orbit (section 1). The remaining gap is where no proof of a single external orbit is known. The weak target would help only through a different argument that bounds the marked union without that statement. No such argument is given here.

## 6. Remaining gap, 21 ≤ n ≤ 48

These are the only (n, k, structure) cases where neither d ≥ 2n/3 nor visibility is proved.

| Case | Residual | Areas |
| --- | --- | --- |
| Primitive, G ⊉ A_n | n ≤ 6z_x for every reflex class x. For n ≥ 25, all reflex corners lie in one class and r ≥ ⌈n/6⌉ | 21–48 |
| k = 2, H ⊉ A_m | z ≥ 2 and m ≤ max(6z, z²) | z = 2: 22, 24. z = 3: 22–36. z = 4: 22–48 |
| k = 3 | z = 2 with m = 7–12; z = 1 with m = 7, 8 (Lemma B, r ≥ 7) | 21–36 |
| k = 4 | z = 2 (all 8 reflex corners in one class) with m = 6–12; z = 1 with m = 6, 7 | 24–48 |
| k = 5 | m = 5, 6; m = 7 with z_x = 8 | 25, 30, 35 |
| k = 6 | m = 4, 5, 6 | 24, 30, 36 |
| k = 7 | m = 3, 4, 5, 6 | 21, 28, 35, 42 |
| k = 8, not the eight-sheet case | m = 3, 4, 5, 6 | 24, 32, 40, 48 |

The limiting steps are as follows.

- Theorem G at z = 2 to 4 (k = 2, 3, 4, and primitive with all reflex corners in one class).
- Lemma B's transversal configurations.
- m ≤ 6 for k ≥ 5, where A_(m−2) isn't simple and no spare blocks exist.

The genus-0 cycle-type constraints, as used in section 2, are the natural tool for the first two. Closing them needs small primitive groups of degree ≤ 48 with these generator types, and that list isn't available offline.

## 7. Saved-data check

[check.py](check.py) reads only cell sets: `cyl.rooms()` (the named rooms plus the normalized rooms of `d64-finite-case/data/covers.json`) and the D72 BBBB names. For each room with n ≥ 21 and r ≤ 8 it does the following.

- It rebuilds g_x with d78's code and asserts genus 0, Σ z_x = r, a product relation, and k·Z_N ≤ r.
- It finds the maximal block system and computes d for every same-parity interior pair.
- It runs an exact rational test of direct visibility on every pair with 3d < 2n. The test was checked to return false on the R22 dark pair.

[Log](check.log). CPU 3.7 s.

- **Coverage.** 2,145 rooms (21 ≤ n ≤ 40) and 9,851 pairs. This includes 8 of the 9 BBBB rooms. dumb12 has n = 20 and d = 19 (d78). Seven BBBB rooms are primitive and 2-transitive. st279 has k = 2, m = 28.
- **Low pairs.** Exactly 3 pairs have 3d < 2n: cov3397 and cov3608 (n = 24, d = 6) and cov4474 (n = 32, d = 6). All are d79's eight-sheet pairs, and all are directly visible. **There is no saved obstruction.**
- **Minimum outside the eight-sheet case.** d/n = 2/3 exactly, at cov2493 (n = 21, r = 7, k = 7, m = 3, d = 14).
- **Residual cases in the data.** The saved rooms reach many residual rows of section 6. They include k = 2 with m = 11–17 and z = 3, 4; k = 3, m = 7, 9; k = 4, m = 6–9; k = 5, m = 5; k = 6, m = 4, 5; k = 7, m = 3–5; and k = 8, m = 3–5. All satisfy d ≥ 2n/3 or the eight-sheet case. No saved primitive room fails 2-transitivity.

The saved list isn't claimed complete, and the data stop at n = 40.

Re-run: `cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d81-lower-threshold && python3 -B check.py > check.log`

No search over rooms, rays, directions or reflection words was run.
