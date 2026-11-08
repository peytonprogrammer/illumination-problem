# Audit: revised preprint v0.2 and research brief

[done] Claude Opus, 2026-11-02. Codex requested this independent hand audit on the board.

Files audited (read only):
- `illumination-k4-codex/preprint-review-codex/revised.tex`
- `illumination-k4-codex/preprint-review-codex/research-brief.tex`
- The original, `attachments/AjuVSV/Wang_illumination_preprint_v01.tex`, for the diff.

Scope: hand checks only. No room, ray, direction, or word search was run, and no code was run on the geometry.

**Verdict.**
- **Preprint proof: ACCEPT.** No mathematical gap.
- **Brief scope: ACCEPT with three wording fixes** (Section 3).
- **One author decision** needs Daniel's confirmation (Section 4).

## 1. Construction geometry (checked by hand)

**P.** The five squares form the boundary cycle (−1,−1), (0,−1), (0,−2), (1,−2), (1,−3), (2,−3), (2,−1), (1,−1), (1,0), (−1,0), traced counterclockwise.
- The convex corners are the seven listed, and the reflex corners are (0,−1), (1,−2), and (1,−1).
- No integer point is interior. Each candidate point misses one of its four adjacent squares.
- The only non-vertex integer boundary points are a = (0,0), on the top edge, and b = (2,−2), on the right edge.

**Q.** I listed the 15 squares of P0, P1, and P2. The 22-vertex cycle traces their union edge by edge, with area 15.
- P0 and P1 meet only along H, and P1 and P2 only along V.
- P0 and P2 are disjoint. At x = 2, P0 reaches y ≤ −1 and P2 starts at y ≥ 1.

The marked points are interior:
- S = (0,0) has all four adjacent squares in Q.
- T = (2,2) has all four adjacent squares in Q.

**Folding.**
- f|P1 and f|P0 differ by the reflection y ↦ −y across H.
- f|P2 and f|P1 differ by the reflection x ↦ 4 − x across V.
- So each seam crossing folds to a specular reflection. f(H) is the open top edge of P, and f(V) is the open right edge, which contains b. Neither contains a vertex of P.

**Corner incidences.**
- P0 contributes 10 corner incidences, P1 10, and P2 10.
- The pairs at E1 = (−1,0) and E2 = (1,0) come from P0 and P1. The pairs at E3 = (2,1) and E4 = (2,3) come from P1 and P2.
- The other 8 + 6 + 8 = 22 incidences are exactly the 22 listed vertices of Q.

So the only smooth points of Q that fold to vertices of P are E1–E4. All four fold to convex corners, and no smooth point folds to a reflex corner.

## 2. Proof steps

- **Parity lemma: correct.** Every unfolding map is a composition of reflections in integer lines, x ↦ 2c − x or y ↦ 2d − y. Each one preserves both coordinate parities.
  - z = B/2^r lies strictly inside the segment, and it has an odd coordinate.
  - Folded, z is an integer point of P with an odd coordinate. Every such point is a vertex, so the path hits a vertex.
  - If z falls on a copy boundary, it is a reflection point, which gives the same contradiction.
- **Seam reversal: correct at all four endpoints.**
  - At E2, a ray arriving from P1 with velocity (u,−v), where u, v > 0, folds to (u,v). It leaves with (−u,−v) into P0, which folds to (−u,−v).
  - A ray arriving from P0 with (u,v) leaves into P1 with (−u,v), which folds to (−u,−v).
  - At E3, the horizontal mirror and the x ↦ 4 − x copy change negate complementary components.
- **No axis-parallel path: correct.**
  - Vertical legs stay vertical, so x stays at 0, but T has x = 2.
  - Horizontal legs stay horizontal, so y stays at 0, but T has y = 2.
- **Reversals don't help (the multiple-preimage point): correct as revised.**
  - f⁻¹(a) = {S, (4,0)}. The point (4,0) is a smooth point of the bottom wall (3,0)–(5,0).
  - f⁻¹(b) = {T, (2,−2)}. The point (2,−2) is a smooth point of P0's right wall.
  - So the folded path can visit a and b in the middle, and truncating in P is necessary.
  - With the truncation, the forward route before the first reversal contains no corner and no b. Ordinary billiard flow in P is deterministic and reversible, so the retrace meets no corner and reaches a before b. That contradicts the last-visit choice.
  - Visits to a and b are leg endpoints, so there are finitely many.

**Optional clarity edit.** Name the two preimages in the sentence that the revision added: "for example, a has the two preimages S and (4,0)".

## 3. Research brief

These parts are correct:
- **Room class and raw condition.** They match `b-not-in-k` and §33 coordinates.
- **Pocket.** A = (2,0), B = (1,1), C = (1,0) is a canonical triangle, with c = (2,0), u3, and u4.
- **Slide.** D_t: x + y = 2 + t and H_t: y = t are right.
- **Q.** Moving a mirror by δ along its unit normal n shifts reflected points by 2δn. This gives t(1,1) for D and t(0,2) for H, which matches a_D and a_H. The sum Σ L_{j−1} a_j, with L_j = R_1⋯R_j, matches `mirror_complete.py`'s tracer.
- **Mod-2 identity.** Q ≡ n_D·(1,1) (mod 2) holds, because signed permutations fix (1,1) mod 2 and a_H ≡ 0.
- **Examples.** The 25-wall room and the 37-wall room both match verified data.
  - The 37-wall room is band 31, completion 1. Its classes with p² + q² < 41 are complete: (1,0), (1,1), (2,1), (3,1), (3,2), (4,1), (4,3), (5,1), (5,2), (5,3), and (6,1). All are blind, and (5,4) loads 4/4.
  - The brief cites only the two independently verified rooms.
- **Scope.**
  - No unbounded-norm claim, no minimality claim, and no 22-wall lower bound.
  - It separates periodic-core detection from the marked S/T event clearly.

Three wording fixes:
1. "A nonzero class, however, need not be nonzero on a cylinder core" is ambiguous, since any single core can be zero. Write "a nonzero class can vanish on every cylinder core of a general square-tiled surface."
2. "under the additional-diagonal-wall hypothesis" isn't defined for an outside reader. Write it out: "if the room has a diagonal wall other than D." That is the hypothesis in `parity-route-audit.md`.
3. "The cancellation has a hand explanation" covers one representative (2,1) core. Write "for one representative (2,1) core; blindness of the whole class rests on the all-strip check." This matches Codex's own scope in `leaf-flip-mechanism.md`.

## 4. Author decision to confirm


Other changes are acceptable:
- The Castro bibliography entry is removed, with Castro still attributed through Wolecki.
- A pointer to Wolecki's Remark 2.2 is added.
- The P0 label moves.
- The URL now pins v3.

I didn't check Wolecki's text myself. Codex's source check is the only check on the Remark 2.2 and Theorem 1.3 citations.

Authorship: Daniel Wang and Peyton Wang, as in v0.1. Peyton is credited.
