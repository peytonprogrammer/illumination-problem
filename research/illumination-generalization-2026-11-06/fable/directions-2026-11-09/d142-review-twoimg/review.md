# D142: review of two-image-midpoints (snapshot 2026-11-22 01:00)

Date: 2026-11-21. Reviewer: adversarial referee. Reviewed file: `../d95-review-queue/snapshots/two-image-midpoints.2026-11-22-0100.md`, SHA-256 prefix `25f27255d673afa7`. It is identical to `qclass-closure/bbbb/two-image-midpoints.md`. Context: `quotient-midpoint.md`, `free-half-turns.md`, and the d140 and d141 reviews.

Files: [checks.py](checks.py), [checks.log](checks.log). Re-run: `python3 -B checks.py > checks.log`, 0.35 CPU-seconds. The script uses exact Fraction arithmetic and builds named rooms only: R22, its staircase P, and d141's rooms H, B, O, M, imported from `../d141-review-freeht/checks.py`. It runs no room search and no direction search.

## Verdict

**Sound with gaps.** Every step of the proof checks, and no replay contradicts it. Across 61 quotient–pair cases, no quotient blocks more than 8 of 64 lift pairs. No gap is high. The wall bound is conservative: the same argument, plus 2 short cases, proves the result for W ≤ 23. It first breaks at W = 24. R22 doesn't test the inequality at all, because the orthogonal case is excluded at every W.

## 1. The reduction to degrees 1 and 2

The step is Riemann–Hurwitz for the **refinement** u: X → Z, not for f. The arbitrary map f = v∘u enters only through Z. So deg f, the base torus, and any intermediate room quotient don't matter. v can have any degree.

- Freeness of ε needs u(A) ∩ u(B) = ∅. That follows from the all-pairs hypothesis: a coincident pair's involution would fix a regular image.
- With ε free, Z has a zero, and H = Z/⟨τ⟩ carries a free involution. So genus(H) is odd. The note doesn't say why: H → H/ε̄ is an unramified double cover (gap 4).
- 2 genus(Z) + 6 = 3m + 2b₂ with m = 2 genus(H) + 2 and b₂ ≥ 2. So genus(Z) ≥ 5 for elliptic H and genus(Z) ≥ 11 otherwise.
- genus(X) − 1 ≥ deg u · (genus(Z) − 1). Against genus(X) − 1 ≤ 26, this gives deg u ≤ 2 when genus(H) ≥ 3. In the elliptic case, a singleton gives deg u ≥ 8 and needs 32.

I checked the corner formula for genus(X) against the square-tiled genus on all 6 rooms. Results: R22 10, P 4, H 5, B 3, O 9, M 5 (log §2).

**The refinement step, tested (log §3–4).** For every quotient tested, the script computes Z as the meet of the 2 or 4 R-conjugate block systems. There were 43 cases with disjoint images, and 4 of them are nonvacuous. In all 43, every pair blocked on Y for all R-rotations is blocked on Z by a **free** −I involution, as the note claims. The implication fails in exactly 4 cases, and each has coincident images. These are H/Γ₂ and B/C₃, so the disjointness lemma is load-bearing.

**Hidden translations (coordinator's question).** The reduction covers them. It never classifies symmetries. Its only inputs are genus, branch counts, and the disjointness lemma. Degree 1 uses free-half-turns on X itself, where d141 found that every hidden −I map either has non-forbidden fixed points or isn't an involution. The replays agree:

| Quotient | deg, genus | Pairs blocked | Why it can't block all pairs |
|---|---|---|---|
| B, X/C₃ (hidden), ψ = [τ] | 3, 1 | 8/64, 1 per source | f(B) meets f(A) in 8 coincidences. The blocked targets are hidden translates of τ(S), so the disjointness lemma applies. |
| O, X/⟨central⟩, quarter-turn | 2, 5 | 8/64, 1 per source | Free and disjoint. genus(Z) = 5 forces m = 4 and b₂ = 2, so H is elliptic. Then \|u(A)\| = 8 > 3. |
| H, X itself, y = 1 lift | 1, 5 | 8/64 | free-half-turns: 1 partner per source |
| H, X/Γ₂ | 2, 3 | 8/64 | coincident images (8) |

All 6 subgroups of B's Trans(X) ≅ S₃ and all 10 of O's were tested, together with every block system of size 2 and 3. Coverage never exceeded 1 partner per source. In these small rooms the hypothesis also fails earlier: genus(X) ≤ 9 < 11, so the degree-2 count is never reached. The note should name the B and O mechanisms and say which branch excludes each (gap 3).

## 2. The degree-2 count

- **Sphere.** Z/⟨r⟩ is the image of the sphere X/⟨R⟩ under the map induced by uR = ru. A holomorphic image of a sphere is a sphere. This checks.
- **Branch data.** With 11 ≤ genus(Z) ≤ 14 and genus(Z) odd, the only solutions are m = 8 and b₂ = genus(Z) − 9 ∈ {2, 4}. Each ε commutes with r, so its sphere involution preserves stabilizer orders. It fixes exactly 2 order-2 values: four-point fibres and singleton fibres are excluded, as the note argues. The map from ε to sphere involutions is injective. Lifts differ by r^j, and only j = 0 keeps derivative −I.
- **Exact count (log §1).** I enumerated the Möbius maps of a b₂-set and counted the involutions that fix exactly 2 of its points. With b₂ = 4: generic, 0; harmonic {0, ∞, ±1}, 2; equianharmonic, 0. That matches the finite-subgroup picture (V₄, D₄, A₄ in S₄), and D₄ contains exactly 2 transpositions, both disjoint. So the bound of 2 is attained and sharp. With b₂ = 2, there's at most 1.
- **Hyperelliptic double cover.** H has genus 3 and m = 8 = 2g + 2. For y² = q(x²) with deg q = 4, the lift (x, y) ↦ (−x, −y) is free. So the free lifts the note needs exist in principle, and 2 can't be lowered to 1 by this route.
- **Targets.** If deg u = 2, the 8 target lifts have at least 4 images. 4 > 2, so the case closes.

## 3. Where W ≤ 20 enters

The inequality is genus(X) − 1 ≤ ⌊(3W − 8)/2⌋. Here is where each case opens (log §0):

| W | Bound | Elliptic singleton (needs 32) | Max deg u, genus(H) ≥ 3 | deg-2 genus(Z) options (b₂) | deg 3 |
|---|---|---|---|---|---|
| 20 | 26 | closed | 2 | 11, 13 (2, 4) | — |
| 21 | 27 | closed | 2 | 11, 13 | — |
| 22 | 29 | closed | 2 | 11, 13, **15 (b₂ = 6)** | — |
| 23 | 30 | closed | **3** | 11, 13, 15 | genus(Z) = 11, b₂ = 2 |
| 24 | 32 | **open** | 3 | up to 17 | open |

- **W = 22.** The count needs a bound for b₂ = 6. A finite Möbius group preserving 6 points is cyclic, dihedral, A₄, or S₄; A₅ has no orbit of size ≤ 6. Each has at most 3 involutions fixing exactly 2 of the 6 points. The octahedron and the hexagon both reach 3 (log §1). 3 < 4 targets, so W = 22 is excluded.
- **W = 23.** deg u = 3 forces genus(Z) = 11, u unramified, m = 8, and b₂ = 2. There's at most 1 eligible ε against at least 3 target images, so W = 23 is excluded.
- **W = 24.** The elliptic singleton case (deg 8, genus(Z) = 5) is open. This matches the 24-wall threshold of quotient-midpoint.

So the proof doesn't fail at W = 22, and it can't be checked against R22. R22 is orthogonal, and the orthogonal branch (H a sphere) excludes a common quotient at every W. Its consistency with R22 is the statement "R22 has no such witness", and the replay confirms it (§4). The note's R22 paragraph is correct but doesn't state this (gap 2).

## 4. Replays

- **R22 (W = 22, orthogonal).** M has 60 squares and genus 10. Trans(M) is trivial. The only half-turn is τ, which blocks 0 of the 16 pairs. M has exactly one block system of size 3. It is the staircase fold M → M_P, a degree-3 translation map onto P's 20-square, genus-4 unfolding. It **violates the full-fibre rule**: 4 forbidden P corners, (−1, 0), (1, 0), (2, −1), (2, −3), have regular seam-endpoint points of Q in their fibres. So it has 0 admissible half-turns. Under the fold, the 4 S lifts and the 4 T lifts each collapse to 2 points, all at lattice offset 0.

  What R22 uses instead is a 2-adic descent. First, a degree-3 fold onto a room where the marks are smooth wall points. Next, both marks develop into 2ℤ², so they coincide on R²/2ℤ². Then the first lattice point B/2^r with an odd coordinate along the particular developed segment folds to a vertex. Last, a separate reversal lemma handles the seam endpoints. The obstruction point depends on the path and isn't a fixed point of any global involution.
- **H (small mixed room, W = 6).** X has the free lift of y = 1 and τ as admissible maps. Each source has 1 partner, 8 of 64, as free-half-turns predicts. Its 3 degree-2 quotients and its degree-4 quotient give at most 8 of 64.
- **B, O, M.** See the table in §1. M has only τ and blocks nothing.

## 5. Scope

Closing the common-quotient midpoint route means this: in a mixed room with W ≤ 20 (provably W ≤ 23), no single translation quotient carries midpoint witnesses for all 64 relative lift choices at once. The orthogonal result holds at every W. Darkness needs every lift pair blocked, so a darkness proof by common-quotient midpoints is impossible in this range.

For the W ≤ 20 goal, this narrows which mechanism a counterexample could use. It isn't an illumination proof: no theorem says darkness forces such a witness. R22 shows that implication is false in general, because it is dark with no witness at all. A W ≤ 20 dark pair, if one exists, would need a path-dependent obstruction, such as a different quotient for each lift pair or a parity descent like R22's. The note says this correctly. I see no basis for moving the goal estimate on this result.

## Gaps

1. **Low. The wall bound is conservative.** The proof gives W ≤ 23 with 2 additions. At W = 22, add the 6-point Möbius bound (at most 3 eligible involutions). At W = 23, add the degree-3 case (genus(Z) = 11, b₂ = 2, at most 1 eligible). W = 24 is the first open case, matching quotient-midpoint. State the threshold, or say that 20 is chosen for the goal rather than forced.
2. **Medium. The R22 consistency statement is missing.** The W-inequality concerns mixed rooms only. R22 is orthogonal and is excluded at every W by the sphere step, so R22 gives no check of the inequality. The note should say so. It should also record that R22's fold is a degree-3 translation map that breaks the full-fibre rule at the 4 seam endpoints, and that M has no admissible half-turn except τ.
3. **Low. Hidden-translation and quarter-turn quotients aren't named.** The proof covers them; nothing in it uses symmetry. d141 raised them as open for free-half-turns. Add one line: B's X/C₃ mechanism always creates coincident images, so the disjointness lemma excludes it. O's quarter-turn quotient lands in the elliptic branch.
4. **Low. Oddness of genus(H) isn't justified.** "Thus H has positive odd genus" needs the reason: a free involution gives an unramified double cover H → H/ε̄, so genus(H) = 2g′ − 1.
5. **Low. Stale dependency note.** "(d141 review pending)" is out of date. d141 found free-half-turns sound with gaps, and its degree-1 count of 1 partner per source on X is what this note uses.
