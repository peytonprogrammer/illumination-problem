# Semantic necessity of the kmax6 encoder clauses

[done] Claude Opus, 2026-11-02. This is task A of Codex's `lower-bound-proof-audit/dependency-review.txt`, claimed on the board.

Scope: hand proof plus source reading only. No solving, replay, or discovery was run. The source is the frozen `illumination-k4-codex/k5-proof-pilot/inputs/encode.py`, `geometry(case, wmax=21, kmax=6)`, with the helpers in the same folder's `illumination_geometry.py`. This is the call that `claude-illumination-check/k6-run/run.py` makes.

**Verdict: ACCEPT.** Take any eligible room in a case whose full set F is exactly the room's interior A points. The room's triangle assignment extends to an assignment that satisfies every base clause family. The proof had one library assumption (Section 4), which `../arithmetic-review/` has since closed for this packet. I found no missing hypothesis and no over-strong clause.

## 1. Hypotheses (H)

The room R is a finite union of canonical triangles. Each triangle has one A (even, even), one B (odd, odd), and one C (mixed) vertex.
- **H1.** R is a closed disk with a strictly simple boundary and no slits. It is a triangulated disk with a connected dual graph, and each occupied vertex has one angular sector or a full ring.
- **H2.** F is exactly the set of interior A points, and I = |F|. The case lists F; translation and D4 normalization belong to the census, obligation 1.
- **H3.** W ≤ 21, where W is the number of genuine corners and equals the number of maximal walls.
- **H4.** k = J + s_N ≤ 6, where J counts interior B/C points and s_N counts smooth boundary B/C points.

Specialization: N cap = ⌊4(21 − 2 + 12)/3⌋ = 41, triangle depth = 41 − 8 = 33, and cap = ⌊(33 − 4I)/2⌋ = 12, 10, or 8 for I = 2, 3, or 4.

## 2. Counting facts used

- **(C1)** N = 2(I + J) + B − 2, where B = W + s_A + s_N. This is Euler's formula for a triangulated disk.
- **(C2)** N = 8I + Q + s_A, where Q = 3s_A + Σ_{A corners} m. Every triangle has exactly one A vertex.
- **(C3)** From C1 and C2, W = 2 + 6I + Q − 2J − s_N. Since 3s_A ≤ Q, N = 2I + s_A + (W − 2 + 2J + s_N) ≤ (4/3)(W − 2 + 2J + s_N) ≤ (4/3)(W − 2 + 2k).
- **(C4) The P + m bound**, re-derived for general k.
  - Let P count the partial occupied A cells. Let m count the empty cells among the b cells of R_F − F, where R_F = F ∪ 4-neighbors.
  - The cell graph joins occupied cells whose triangles share a BC edge on the common cell side. H1 makes it connected.
  - A full cell has degree ≤ 4 minus its empty neighbors, so Σ_full deg ≤ 4I − m.
  - A partial cell's degree is at most the number of cell sides its contiguous fan touches. Slots pair up as (7,0) right, (1,2) top, (3,4) left, and (5,6) bottom. So m = 1…7 triangles touch at most 1, 2, 2, 3, 3, 4, and 4 sides. These are ≤ the Q charges 1, 2, 3, 3 (the half-star), 5, 6, and 7. So Σ_partial deg ≤ Q.
  - Connectivity gives 2(I + P − 1) ≤ 4I − m + Q.
  - Each empty neighbor c′ of a full cell c makes the side midpoint (c + c′)/2 a smooth C point, since it carries exactly the two triangles of c's star. Distinct c′ give distinct midpoints, so m ≤ s_N.
  - Substituting C3: 2P + m ≤ W − 4I + 2J + s_N. So 2(P + m) ≤ W − 4I + 2J + s_N + m ≤ W − 4I + 2k, and P + m ≤ cap.
- **(C5)** Occupied cells outside R_F number P − (b − m) = P + m − b ≤ cap − b. A shortest cell-graph path from such a cell to R_F passes only distinct occupied outside cells, so its Manhattan length is ≤ cap − b.

## 3. Witness assignment and clause families

Set x_t = [t ∈ R]. By C5, the universe `ts` contains every triangle of R. `ts` is the eight-triangle stars of all cells within Manhattan radius cap − b of R_F. The case's diamond only feeds an `assert allowed <= case['allowed']`, so no coordinate cutoff removes any room.

| Family (encode.py) | Witness | Why it holds |
|---|---|---|
| Unit `[x_t]` for t at a full A point | — | Interior points carry their full star (H1, H2). |
| `A-used` ⇔ OR of x at p | occupied(p) | Definition. The incident universe triangles of an A point are its whole star. |
| `[−bit, w]`, `[−w] + bits`, `[−w] + x(r)` | w_p = p is a genuine corner; bits = corner angle in 45° units, else 0 | A corner angle is in 1–7 and isn't 4, so it's nonzero. A corner is occupied. |
| C-point `[−b0]`, `b1 ⇔ w` | — | C corners are 90° or 270°, which encode as 010 or 110. |
| `e` clauses: `[−e,−w]`, `e → occ`, `occ → e ∨ w` | e_p = p is interior or smooth (non-A) | Under H1, an occupied vertex is exactly one of interior, smooth, or corner. |
| Fan rows: at least one selector; selector → its values | Select R's actual mask at p | R's fan lies inside r = inc[p], because R ⊂ ts. It is empty, one contiguous sector, or full (H1). `local_sectors` counts shared spokes as open, so R's fan is a legal row with matching w, e, A-used, and angle. For A points, full ⇔ p ∈ F (H2). |
| Support clauses `[∓var] + selectors` | Same | Exactly one selector is true, and it carries var's true value. |
| atmost(x, 41) | — | C3 with H3 and H4. |
| atmost(walls, 21) | — | H3. Every corner is a lattice vertex in `inc`. |
| atmost(exceptions, 6) | — | Σe = J + s_N = k (H4). |
| atmost(outside A-used, cap − b), or `[]` if cap < b | — | C4 and C5. P ≥ b − m, so cap < b leaves no room. |
| A-cell reach, depth I + cap − 1 | reach(s,p) = [axis distance from root ≤ s among occupied cells] | Occupied cells number I + P ≤ I + cap, and cell-graph edges are axis steps. |
| Triangle reach, depth 33 | tri-reach(s,t) = [dual distance from the origin star ≤ s within R] | A shortest dual path has distinct triangles outside the 8-star, so its length is ≤ N − 8 ≤ 33. Every R edge is a universe edge. |
| Gauss–Bonnet PB: Σ 4w + Σ wt·¬bit = 8 + Σ wt | — | It is equivalent to Σ_corners (4 − θ) = 8 in 45° units, the exterior-angle sum of a simple polygon. Non-corners have bits = 0. |

## 4. Library assumption and minor notes

- **Assumption.** The necessity direction also needs pysat's `CardEnc.atmost` (seqcounter) and `PBEnc.equals` (adder) to be complete. That means every input assignment that meets the arithmetic constraint must extend to their auxiliary variables. Installed PySAT 1.9.dev17 implements `PBEnc` with Pindakaas 0.6.1, not PBLib (Codex's correction).
  - For Sinz's sequential counter, setting s_{i,j} = [count of first i ≥ j] satisfies every clause. This covers the abstract construction only, not the emitted implementation.
  - **Correction (Codex, 2026-11-02):** small-n exhaustive tests are useful controls, but they can't establish completeness for the larger encodings actually emitted. Closing this assumption needs a construction-level proof bound to the emitted clauses. Codex's `lower-bound-proof-audit/arithmetic/` supplies that proof, and my review in `../arithmetic-review/findings.md` accepts it. **This assumption is closed for the frozen packet.**
- **Fragile but harmless.** `exceptions=[];angle_lits=[];angle_weights=[]` sits inside the `if` on the forced-triangle line, so it resets on every forced triangle. Nothing has been appended yet at that point, so this is harmless. It would raise an error only if F were empty, and F is never empty.
- **Out of scope (other obligations).**
  - Obligation 1: the census completeness, I ≤ 4, and the F/pair normalization. The proof is in `k6-support-census/findings.md`; it isn't re-proved here.
  - Obligations 4–5: guard validity and guard-to-clause provenance, which is task B, Codex's.
  - Obligation 6: DRAT replay.
- **Relaxation direction.** The CNF also admits disconnected or spurious assignments. That's acceptable, because UNSAT of a necessary relaxation still excludes every eligible room.
