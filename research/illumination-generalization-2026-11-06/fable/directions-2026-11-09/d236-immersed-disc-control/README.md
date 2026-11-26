# d236: immersed-disc control census (approved by Daniel, 2026-11-25 19:11 HST)

Advances: L1 (route choice: does a proof need planarity?). No lemma is claimed.

Payoff sentence: if a non-embedded immersed disc with W <= 20 has a dark pair, darkness at r <= 8 has a non-fold mechanism, and every planarity-free L1 route is dead. If none exists through area 16, a proof may be stated for immersed discs; that is weak evidence, and the control stops there.

Prior work: d52 (all immersed W-sets at r <= 8, certificates only, 0 fold positives), d55 (lighting on slit and pinched rooms; orbitr.c decides abstract unfoldings), d140 (all-dark genus-9 surface), d205 (embedded census through area 21). Source of the test: d234-route-exploration/outsider.md.

## Class (SPEC, fixed before any code)

An immersed orthogonal disc is a finite complex K of unit squares with a map f to lattice cells of the plane.
- Two cells may be glued along a side only when f places them on the two sides of that lattice edge. Each side is glued to at most one cell.
- Link rule: at every cell corner, the cells reached by turning around the lattice point through glued sides form a path of 1, 2 or 3 cells, or a cycle of exactly 4 cells. A path of 4 (slit tip) and a longer cycle (branch point) are excluded.
- K is connected and F - E + V = 1, where a glued side is one edge and each link is one vertex.
- W = number of links of size 1 or 3. Limits: W <= 20 and F <= 16.
- Unit of enumeration: K up to translation and the 8 lattice symmetries.
- Marks: links that are 4-cycles. Unit of lighting: an unordered pair of distinct marks. Two marks over the same plane point are distinct.
- Billiard rule: reflect at a link of size 2; stop at a link of size 1 or 3.

Buckets: EMBEDDED (f injective on cells, every plane-adjacent pair glued, one link per lattice point: the strictly simple rooms of d205), TOUCHING (f injective on cells, but not embedded), OVERLAP (two cells over one plane cell). The control is TOUCHING plus OVERLAP. EMBEDDED is a validation gate only.

## Gates

- G1: EMBEDDED counts by (area, W) match d205 (validation/PASS.json and the small table) for every area <= 11.
- G2: counts by (area, W, bucket) match an independent enumerator (validator/) for every area <= 10.
- G3: the new unfolding builder reproduces the d205 control (the 22-wall room's pair is DARK, 2592 states).
- G4: pilot at area <= 12 before production. If the forecast for area <= 16 exceeds 60 CPU-min, stop and report to Daniel with the forecast.
- A DARK verdict needs a complete orbit (FULL) and an independent reproduction. CAP or a crash is UNDECIDED, never dark.

## Predictions (written before any run)

- P(a dark pair exists in the control) = 3% (coordinator), 5% (outsider).
- P(production finishes inside 60 CPU-min) = 60%.
- Guess: 10^6 to 10^8 control discs through area 16.

## Stop result

No dark pair: record the counts, and stop the control. A dark pair: reproduce it independently, then report to Daniel before any follow-up.

## Outcome (2026-11-25 20:00 HST)

No dark pair. Through area 16 at W <= 20 the control has 2,446,117 discs (1,858,447 TOUCHING, 587,670 OVERLAP) and 857,156 pairs of marks (752,689 and 104,467). Every pair is lit; 0 dark, 0 undecided. Production: 8.0 CPU-min (astra/README.md), plus 0.9 CPU-min for an abandoned in-memory attempt.

Gates: G1 PASS (57 embedded rows, 22,292 rooms). G2 PASS (69 rows through area 10; the coordinator later ran the validator through area 12: 111 rows, 0 mismatches, 373 pairs all lit by its own decider). G3 PASS (both deciders). G4 PASS.
Coordinator cross-check (crosscheck.py, 3 CPU-s): 297 production discs (65 OVERLAP, areas 10 to 16) decided with the validator's independent unfolding and decider: 478 of 478 pairs lit. My first version of this script misread the decider's return value and reported 297 pairs as not lit; that was a harness bug, fixed.

Predictions scored: no dark pair (I gave a dark pair 3%): held. Inside 60 CPU-min (60%): held. Control size 10^6 to 10^8 discs: held. Smallest OVERLAP at area 9: held; I guessed W = 12 and missed the W = 10 disc.

Status: COMPUTED, cross-checked by a second implementation through area 12 and on a sample above it. Not reviewed.

Reading: the control doesn't separate planarity from the reflection structure in this range. Immersed discs behave like rooms: no dark pair at small area. That is weak evidence that a proof may be stated without embedding. It doesn't move L1. The stop result applies: the control ends here.
