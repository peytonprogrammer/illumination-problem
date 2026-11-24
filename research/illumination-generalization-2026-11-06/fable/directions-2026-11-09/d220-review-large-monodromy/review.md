# d220 referee review: large monodromy at area 22

Note: `note-snapshot.md`. Checks: `checks.py`, log in `checks.log`. The run takes 2.5 s of CPU at nice 10 and ends with 0 failures. It uses no rooms beyond the named cov4181 cells. It runs no ray, direction, word, or room-size search, and it makes no network calls.

## Summary

| # | Claim | Verdict |
|---|---|---|
| 1 | Component ↔ orbital G·(i,j); projection monodromy = Gᵢ on Δ | CORRECT |
| 2 | n=22, r=8 primitive: M22 and M22:2 excluded, so G ∈ {A22, S22}, stabilizer A21/S21 | CORRECT WITH GAPS (imported inputs only) |
| 3 | Imprimitive branch: the 20-sheet external projection is imprimitive | CORRECT (conditional on d208 §4) |
| 4 | Hurwitz formulas, functoriality, shear reduction, U∘V vs V∘U | CORRECT; the darkness equivalence is conditional on the FC criterion |
| 5 | cov4181: blocks, table, a², G = (S7 wr S4) ∩ A28, external orbit S7 wr S3 | CORRECT (computed exactly) |

Overclaim: none found. The note states its open obligations accurately.

## 1. Orbital/projection correspondence: CORRECT

Over the punctured base, components of the fiber product Q ×_B Q correspond to G-orbits on Ω×Ω. The first projection of the component through (i,j) has fiber Gᵢ·j over the sheet i. The image of π₁(Q, i) in G is exactly Gᵢ, because a loop lifts closed at i iff it fixes i. So the projection monodromy is Gᵢ acting on Δ, and the degree is |Δ|. Normalization changes nothing over the unramified locus. The remark that a marked union of several orbitals has no transitive degree-d action is also correct.

## 2. Primitive branch at n=22, r=8: CORRECT WITH GAPS

`checks.py` builds M24 from Conway's four generators on PG(1,23) and gets order 244,823,040. M22 is the pointwise stabilizer of ∞ and 0, with order 443,520. Enumerating all its elements in the natural degree-22 action gives these results:

- The only order-3 cycle type is 3⁶1⁴, with 12,320 elements (= 443,520/36, matching the ATLAS 3A centralizer order 36).
- Every M22 element whose cycle lengths lie in {1,2,3} has z ∈ {0,6}.
- M22:2 has order 887,040. Its outer-coset elements with cycle lengths in {1,2,3} are the types 2¹¹ and 2⁷1⁸. Neither contains a 3-cycle.
- Four values in {0,6} never sum to 8, but 6+0+0+0 survives at r=6. This matches the note's caveat.

So the exclusion is correct, and G ∈ {A22, S22}. The point stabilizer acts on 21 points as A21 or S21, which is primitive and contains 3-cycles.

Gaps:

- **Imported inputs.** The argument uses Σzₓ = r and the fact that branch cycles have length 1, 2, or 3. Both come from the reviewed pillowcase accounting, not from this note. The degree-22 primitive list (M22, M22:2, A22, S22) rests on CFSG, as in d208.
- **Simplification, not an error.** The odd-order remark about M22:2 is unnecessary. gₓ² is a square, and every square in M22:2 lies in M22.
- **Link not fetched.** The ATLAS URL was not opened. The class structure was computed directly instead.

The Jordan paragraph is correct. A primitive group of degree 21 containing a 3-cycle with 18 fixed points contains A21. Jones (arXiv:1209.5169) is an appropriate citation. The paragraph is illustrative only and the main proof does not depend on it.

## 3. Imprimitive branch: CORRECT (conditional on d208 §4)

d208 gives blocks of size 2, a block action containing A11, and one external orbital. Fix i. Δ is the 20 sheets outside i's block. Gᵢ preserves G's block system, so the ten pairs in Δ form a Gᵢ-invariant partition with 10 blocks of size 2. That partition is nontrivial, so the action is imprimitive. Gᵢ also fixes i's partner, which gives the extra degree-one component. The note's refusal to discard case (iii) is appropriate.

## 4. Hurwitz action, functoriality, and shears: CORRECT

- **σ and σ².** σ:(g,h) ↦ (h, h⁻¹gh) gives σ²(g,h) = (k⁻¹gk, k⁻¹hk) with k = gh, and gh is preserved. This holds on 2,000 random pairs in S9 under both composition conventions.
- **Relabeling.** Under g ↦ kgk⁻¹, the cycle through s is k applied to the old cycle through k⁻¹(s). So the cycle labels transform as m∘k⁻¹, as stated.
- **Functoriality.** The argument for geometric marked states is correct. It needs only path lifting and the order of composition, not the availability of arbitrary conjugators. The note correctly says that σ² prescribes its conjugator and that arbitrary loops can turn or hit corners.
- **Shears.** U and V are ≡ I mod 2, so they descend to the pillowcase and fix each pole. The stated reduction reaches the base slope of the same parity for all 8,816 primitive (p,q) with |p|,|q| ≤ 60, with at most 59 steps. The maximum decreases strictly at every step. A tie |p′| = |q| occurs only at |q| = 1 (116 cases), and the final U-step plus overall sign gives (1,1).
- **Order.** On (1,0), U∘V gives (5,2) and V∘U gives (1,2). The point that a single-letter match cannot fix the word-to-slope convention stands.

Gap: the equivalence "dark iff separated in every regular graph for every geometric state and off-class" also depends on the reviewed single-arc FC criterion (d61). It was not re-checked here. The ≥13 and ≥15 candidate counts were not in scope.

## 5. cov4181: CORRECT (exact computation)

`checks.py` builds the 28 d66 cells. Vᵢ exchanges across vertical lines x = L with L ≡ i (mod 2), and Hⱼ does the same on horizontal lines. The generators are a, b, c, d = VᵢHⱼ.

- B0..B3 partition the cells, 7 each.
- All four rows of the table match exactly: block maps (01), (01)(23), (123), (12) and bits 0010, 0011, 0000, 0001. Each generator is even.
- a² moves exactly (5,2), (5,3), (6,2), and abab fixes every block with bits 0011.
- Schreier–Sims gives |G| = 7,742,895,390,720,000 = (7!)⁴·24/2. The generators preserve the blocks and are even, so G = (S7 wr S4) ∩ A28.
- Adding HⱼVᵢ, V0V1, and H0H1 doesn't enlarge G, which confirms the basis independence.
- The stabilizer of (0,0) has orbits of sizes 1, 6, and 21. The 21-orbit is the union of the other three blocks. The induced group has order (7!)³·6 = |S7 wr S3| and contains odd permutations.
- These numbers match `midpoint-orbits.txt` (valencies 21 and 6).

The hand argument is also sound. The image of the B3 stabilizer on B3 is primitive (prime degree), so it contains A7 by Jordan. The conjugates of a² are supported in B3, and 3-cycles form one A7-class, so A7 is supported on B3 alone. The sign bookkeeping and the span of the weight-two vectors are right.

Gap (minor): this review takes the identification of the VᵢHⱼ products with the pole branch permutations from the d64/d66 conventions. It wasn't re-derived from the pillowcase.

## Lemma advanced and first open case

**Lemma advanced: L1.** On the primitive branch at n=22 and r=8, the marked degree-21 projection is now A21 or S21, which removes the group-list uncertainty. On the imprimitive branch, the degree-20 external projection is imprimitive. Neither branch closes L1. A giant group doesn't place compatible endpoint lifts in one regular component for a legal Hurwitz translate.

**First open case.** Take a nondirect same-parity interior lattice pair in a positive normalized eight-reflex BBBB chart at area 22 on the primitive branch (G ∈ {A22, S22}). The open step is single-state reachability: show that one geometric state has compatible lifts of both marks in a common regular component. The stronger midpoint target also needs walk length 2 mod 4. The imprimitive degree-20 branch is a separate open obligation.
