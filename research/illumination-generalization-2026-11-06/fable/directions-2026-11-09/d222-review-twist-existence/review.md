# d222 referee review: two-pole twist existence

Note: `note-snapshot.md`. Checks: `checks.py`, log in `checks.log`. The run takes 0.7 s of CPU at nice 10 and ends with 0 failures. It uses only cov4181 (d66 cell rows) and a combinatorial self-test on permutation pairs. It runs no room enumeration and no ray, direction, word, or room-size search. The only rays are the note's own b-twist family from S = (2,3): velocities (±1, ±2j) for j = 0..5, two lattice steps each. It makes no network calls.

## Summary

| # | Claim | Verdict |
|---|---|---|
| 1 | Two-pole orbits as planar bipartite maps; genus 0; F = 2 + (B−L)/2; faces = k-cycles; B ≤ 8, F ≤ 6 at n = 22 | CORRECT WITH GAPS (minor) |
| 2 | H² is the boundary Dehn twist; realized by (x,y) ↦ (x+2y, y) | CORRECT WITH GAPS (sign, scaling) |
| 3 | D(I,J) test exact (both orders, I = J); path formula X(i) = c−i; odd-path sufficiency; alternating cycles | CORRECT |
| 4 | Pigeonhole \|Sᵢ\|+\|Tⱼ\| > g | CORRECT |
| 5 | Tree of disk components; distance-two filter | CORRECT |
| 6 | Residual graph test; mₐ ≤ 5 | CORRECT (tautological as stated) |
| 7 | cov4181 tuple, k = BC table, orbits, faces, j = 0 and j = 3 witnesses | CORRECT (exact, plus geometric trace) |

Overclaim: none found. The note says plainly that it doesn't force a populated face-offset entry at area 22.

## 1. Planar maps: CORRECT WITH GAPS

Self-test (`checks.log`, Part A): all 4,721 pairs with cycles ≤ 3 on degree ≤ 5, plus 6,000 random pairs on degree 6..12. That gives 18,760 components.

- Components equal ⟨X,Y⟩ orbits, and Σ(face lengths) = E, in every case.
- All 17,968 genus-0 components satisfy F = 2 + (B−L)/2 and F ≤ 2 + B/2.
- 792 components have positive genus and satisfy F = 2 − 2g + (B−L)/2 instead. So genus zero is a property of the room, not of the two permutations. The note's argument for it is right: Q = DP is the double of a disk, so it's a sphere, and any subsurface has genus 0.
- B = 0: all 7,217 paths have one E-cycle, and all 894 alternating cycles have two h-cycles.
- cov4181: every component for all four adjacent pole pairs has genus 0. The total number of 3-cycles is 8 = r.

The n = 22 bounds follow. B counts the 3-cycles of X and Y only, and all four poles together have r ≤ 8. Then F ≤ 2 + 8/2 = 6.

Gaps (minor):

- State once that genus zero uses Q ≅ S². The phrase "subsurface of a sphere" carries it, but the reader has to know that DP is a sphere.
- The converse ("every such bipartite planar map gives a two-permutation orbit") is standard hypermap theory. The note correctly doesn't claim that it completes to a four-pole room.

## 2. Full twist: CORRECT WITH GAPS

- H(X,Y) = (Y, Y⁻¹XY) gives H² = (k⁻¹Xk, k⁻¹Yk) with the product kept. This was checked exactly on (B,C).
- The shear (x,y) ↦ (x+2y, y) commutes with −1. With exact rationals it fixes the four poles and both rims y = 0 and y = 1/2 pointwise. Its x-displacement runs from 0 to 1 across the band, so it's one Dehn twist about the core. The unit shear moves the pole (0, 1/2), so the factor 2 is needed.
- **Dictionary check (new).** For the b,c pair the curve is vertical. The full twist sends the horizontal a→b arc to slope (1, 2j) in room coordinates. An exact billiard trace from S = (2,3) along (±1, ±2j), two lattice steps, reaches T = (4,3) through a regular class-b point exactly for j ≡ 0, 3 (mod 6). The twist test predicts exactly j ≡ 0, 3. Both agree on all six residues of ord k = 6.

Gaps:

- The sign of the shear relative to H² isn't fixed. This is harmless, because the family is indexed by all j ∈ ℤ, and the note says so.
- The "unit torus coordinates" are the room's lattice scaled by 1/2. The poles are then the half-periods. The note doesn't state this scaling.

## 3. D(I,J) test: CORRECT

- On 545,684 ordered (s,t), the D test equals brute force over every j < ord k. 129,430 of them are positive. This includes I = J and X with 3-cycles.
- Random changes of face origin never change the verdict.
- Both orders are needed. A table with one order per transposition disagrees with brute force on 57,210 (s,t).
- On I = J, a nonzero offset is forced, so s ≠ t is automatic.
- Path components: pos(X(i)) + pos(i) is constant. "Some j solves 2j ≡ c − pos s − pos t (mod E)" equals brute force, and it's always soluble for odd E.
- Alternating cycles: X exchanges the two faces and reverses the index. The equation 2j ≡ −pos s − pos t (mod h) is exact. No same-face pair ever has a witness.

The proof in the note (two congruences, consistent iff offsets agree mod gcd) is complete.

## 4. Pigeonhole: CORRECT

In 9,141 random cases, D(I,J) was nonempty and |Sᵢ| + |Tⱼ| > g. Every case had a witness. The argument is one line: |Sᵢ + δ| = |Sᵢ| in ℤ/g. The note's restriction on what "Sᵢ" means for lift compatibility is stated correctly.

## 5. Tree filter: CORRECT

- On cov4181, for all four adjacent pairs, the components of both disks plus the k-cycles form a tree, with no repeated edges. The complementary product equals k⁻¹ (AB·CD = 1 and so on), which matches "reverse boundary orientation".
- In every two-traversal witness from the families B|BC and D|CD over all class-a lift pairs, the filter holds. The lifts are either at distance two through the shared x,y-component, or in one complementary component with both sheets on one face. There were 26 witnessed lift pairs and 0 violations.

The proof is sound: each boundary circle separates the sphere, so every edge is a bridge, and Q is connected. The filter is necessary, not sufficient. The note treats it that way.

## 6. Residual graph: CORRECT

"Failing pairs = missing edges" is a restatement of claim 3 over a finite family list. The bound tₐ ≤ ⌊22/2⌋ = 11 with two A-transpositions per interior mark gives mₐ ≤ 5 and at most 10 pairs.

cov4181 illustration (new): mₐ = 4 regular interior class-a marks, (2,3), (4,1), (4,3), and (4,5), with tₐ = 12. The union over B|BC, C|BC, C|CD, and D|CD has 5 of 6 edges. The pair (4,1)–(4,5) is missing. It's lit by the direct vertical chord through (4,3), which has a class-a midpoint. So a missing edge isn't darkness, and the note is right that longer or same-class routes stay available.

## 7. cov4181: CORRECT

All of the following were recomputed exactly:

- ABCD = 1.
- Against the d220 note's convention ("Vᵢ followed by Hⱼ", i.e. HⱼVᵢ right-to-left): A = a⁻¹ and C = c⁻¹. Here a and c have 1 and 7 three-cycles, so these aren't equalities. Also B = b and D = d (both involutions). This matches the note.
- k = BC = H₁H₀. The column cycle table matches row for row. B(i) = H₁(V₁(i)).
- The ⟨B,C⟩ orbits are the column pairs, sizes 8, 8, 8, 4. The face lengths are (6,2), (2,6), (6,2), (1,3), each with F = 2 and genus 0.
- s = (2,2) at S and t = (3,3) at T. B has the 2-cycles (s t) and (u v), with u = (2,3) and v = (3,2). The offsets are 1 mod 2 and 3 mod 6. k³ sends s, t to u, v, and k⁻³Bk³ exchanges s, t. For this pair exactly j ≡ 0, 3 (mod 6) work.
- Under the note's tuple, class b passes 2 of 16 incidence pairs and class d passes 0. This matches d221's numbers in its tuple.
- **Geometric trace of j = 3.** From (2,3), the velocities (1, 6) and (1, −6) reach the regular class-b point (3,3) after one step and T = (4,3) after two. gcd(1,6) = 1, so no grid vertex is hit at fractional times. This is an exact two-traversal billiard witness. It's a different path from the j = 0 horizontal chord but uses the same class-b point (3,3).

## Lemma advanced and first open case

The note advances **L1** as a decision procedure. For a fixed marked room and fixed adapted bases, two-traversal existence over all twist exponents reduces to a finite face-offset table, and every step is exact. It doesn't advance any area-22 closure. cov4181 is area 28 and imprimitive.

The first open case is the note's own: in the primitive, positive, normalized eight-reflex BBBB chart at area 22, take a nondirect same-parity pair. Nothing forces even one adapted family to put compatible incidences in a populated face-offset entry. The cov4181 residual pair (4,1)–(4,5) shows that the families can miss a pair that is lit some other way. So a proof must either show coverage or fall back to longer walks.
