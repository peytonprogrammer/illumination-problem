# k=6, I=4 equality branch: closed by geometry

Claude, 2026-11-01. Approved by Daniel (cheap part of k=6 only). Fixed finite cases; no ray or room search.

**Result.** For W ≤ 21 and k = 6, no simple canonical-45° room has exactly 4 full A stars. The I=4 branch of k=6 is empty before any optical guard.

## Argument
1. At k=6 the partial-or-missing budget for I=4 is floor((21 − 16 + 12)/2) = 8. Four cells have at least 8 external axis neighbors (four-cell lemma), so equality holds.
2. Equality holds for exactly 9 translation-normalized 4-sets: the 2×2 square O, 4 T orientations and 4 S/Z orientations (`../reduction` four-cell data; recomputed here). In each, the universe is exactly the 4 full cells plus their 8 neighbors, with radius 0.
3. Codex's frozen necessary-geometry encoder (`k5-proof-pilot/inputs/encode.py`, audited earlier) is UNSAT at wmax=21, kmax=6 for all 9 (`all9.py`).
4. **Certificates.** For the 3 shapes up to symmetry, my own drat-trim (built from upstream) prints `s VERIFIED` on O, T and S (`cert.py`, `{O,T,S}.cnf/.drat/.drat.log`).

## Controls and margins
- The same encoder is SAT at k=8 for all three shapes (`sanity.py`), so the UNSAT isn't an artifact.
- **Thresholds at W ≤ 21.** O becomes feasible at k = 7. T and S are still infeasible at k = 7.
- **Minimum W at k = 6.** O needs W ≥ 22; T and S need W ≥ 24.
- The union of the four full patches already forces interior non-A points: 5 for O, 3 for T and S. Making every boundary lattice point a corner then costs walls, which is the intuition behind the cap.

## Optical side (not needed, recorded for later)
- Direct interior segments light all 6 O pairs and 4 of the 6 pairs in each of T and S.
- The 2 diagonal pairs in T and S pass through an odd-odd patch corner whose fourth quadrant lies in a neighbor cell.
- That only matters if a later branch (k ≥ 7, for O) becomes geometrically feasible.

## Dependence
The exclusion relies on the encoder's clauses being necessary conditions, as already accepted for k5. The k6 I=2,3 supports are with Codex.
