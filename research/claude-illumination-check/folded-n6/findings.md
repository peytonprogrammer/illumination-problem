# Folded parity rooms in the 30-60-90 tiling (n = 6): theory

Claude, 2026-11-01. Approved by Daniel. This is theory, plus a re-analysis of the saved n = 6 closure search. No new room search.

## Setup
- **Tiling.** This is the kaleidoscope of the triangle with A = 30°, B = 60°, C = 90°.
  - A points are 6-fold centers, with 12 tiles.
  - B points are 3-fold centers, with 6 tiles.
  - C points are 2-fold centers, with 4 tiles.
- **Mirror lines.** Each mirror line has vertex pattern A–C–A–C… or A–B–C–B–A…. So any segment between two A points on a mirror line contains a B or C point. (Fact M)
- **Parity base.** An n = 6 parity base P is a simple tile union in which every B and C point is a corner. Its marks a ≠ b are non-corner A points, interior or smooth boundary.
- **Folded room.** A folded room Q is m mirror-glued copies with a coherent fold f: Q -> P and interior marks over a and b. One extra condition applies: no transparent lift of a 60° base corner.

## 1. Seam transport (darkness)
- A transparent lift is k copies around a base corner of angle θ, with kθ = π (smooth) or 2π (interior). It retraces exactly when π ∈ 2θZ.
  - That holds for θ = 30° (k = 6 or 12) and θ = 90° (k = 2 or 4).
  - It fails for θ = 60° (k = 3 or 6), where F(t+π) = θ − F(t). This is Codex's §2, checked by Claude for both lift types.
  - **Case list.** Corner angles are multiples of 30° at A, 60° at B and 90° at C. Arithmetic allows θ ∈ {30, 60, 90} and also θ = 120°, k = 3 (interior).
  - **Orientation parity (Codex's repair).** Adjacent copies differ by a reflection, so copy-map orientation alternates around an interior fan. A closed interior fan needs an even k. That excludes θ = 120°, k = 3, and also θ = 60°, k = 3.
- With 60° lifts excluded, projected paths in P are ordinary or reverse at convex 30° or 90° corners.
  - Every B and C point is a P corner.
  - Wolecki's Lemma 3.1 with n = 6 rules out an ordinary path between A images in P, through the fold P -> triangle.
  - Lemma retrace, with a ≠ b, rules out reversals.
- **Tangent case.** It works as in the 45° proof (Codex `folded-review` §1). Two marks on one base wall are impossible by Fact M.

## 2. Wall identity
Corner incidence plus Euler, as in `folded-review` §2, gives seam weights s = k−1 on the boundary and s = k in the interior. With the 90° and 30° transparent lifts, this yields

  W_Q = m(W_P − 4) + 4 + E + 4 b30 + 8 i30  >=  m(W_P − 4) + 4.

Derivation: 2(m−1) = b90 + 5 b30 + 2 i90 + 10 i30 + E, then eliminate b90 and i90.

## 3. Bases
- **Lemma A (interior mark).** If a base has an interior A mark, it has no second mark.
  - The saved closure search (`tokarsky-n/claude_n6_enumerate.py`, reproduced today: 5,975 nodes, 416 leaves) lists every tile set containing a full A star that satisfies the local rules.
  - All 416 are simple single-cycle polygons with 18–24 walls (`leaf_census.py`).
  - None contains a second full A star, and none has a smooth boundary A point.
- **Lemma B (area).** Every B and C point is a corner, and each tile puts 60° at B and 90° at C. So 180(W_P − 2) = 150N + E_A.
  - A smooth boundary mark needs its 6-tile half-star.
  - Each tile has exactly one A vertex, so two marks give disjoint half-stars and N >= 12.
  - Therefore W_P >= 12.

## 4. Conclusion
- m = 1: no base has two interior marks (Lemma A).
- m = 2: both marks are on the boundary (Lemma A).
  - The Lemma 3 argument of `short-proof.md` then applies: a supporting seam line, then Euler, then one interval [a, b] on ∂P.
  - Fact M puts a smooth B or C point inside that interval, which contradicts the base condition.
- m >= 3: W_Q >= 3(12 − 4) + 4 = 28.

**Every n = 6 folded parity room has at least 28 walls, if one exists.** This family can't beat 22.

## Caveats
- Lemma A rests on my earlier closure search. Codex read its code and receipt but hasn't independently audited it.
- The 60° exclusion is part of the class definition. Rooms that use 60° lifts would need a different darkness argument.
- No existence claim: no n = 6 folded room has been constructed.

## Review status (2026-11-01)
- Codex ACCEPTS W >= 28 for this class, after the 120° orientation-parity repair (now in the case list above).
- Codex's independent replay found 416 leaves with the histogram 18:2, 19:12, 20:54, 21:136, 22:150, 23:60, 24:2. `leaf_census.py` on my rerun gives the same histogram. Node counts differ (5,111 vs 5,975) because of tie-break order.
