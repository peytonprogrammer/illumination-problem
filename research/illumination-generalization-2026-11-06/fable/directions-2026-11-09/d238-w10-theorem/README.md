# d238: the ten-wall theorem (target changed by Daniel, 2026-11-27 22:55 HST)

Target T10: every strictly simple orthogonal lattice room with at most 10 walls lights every pair of distinct interior lattice points, at every size.

Daniel chose this over the W <= 20 goal as the outcome worth the cost. The W <= 20 goal stays stated and isn't worked (estimate 2-4%).

## Where T10 stands (from the notes, checked before any brief)

- W <= 8 is done: d15 Theorem S, reviewed. Every pair of distinct real interior points is lit, for any real side lengths, r <= 2.
- W = 10 has 8 turn words, 0 COVERED (d163 ledger, STATUS.md):
  - LLLLLRLRLR, staircase (Ferrers): PARTIAL (d168, d170, d174). Named residuals: V1 = (2,3,5,9; 3,1,1,3), V2 = (1,2,3,6; 3,2,1,4), family (2,3,5,90m; 40n-5,1,1,3).
  - LLLLRLLRLR, pyramid: PARTIAL (d172: lit when wb <= ud). Open outside that inequality. One winding family can miss while the perpendicular sweep lights the pair (bbbb/pyramid-sweep-obstruction.md).
  - LLLRLLRLLR, orthoconvex with 3 or 4 corners: PARTIAL (3 certified order types, d169).
  - LLLLLLLRRR, spiral: PARTIAL (d84: U2 and its stretches).
  - LLLLLLRLRR, LLLLLRLLRR (one-bank stacked halls), LLLLRLLLRR (two-bank), LLLRLLLRLR (staircase band): tall-hall members only (d162).
- Small sizes are done by census: every W <= 20 room of area <= 21 (d9, d205).
- Earlier W = 10 work (d57, d58, 2026-11-18 to 11-22) aimed at all real sizes and real pairs and stopped at thin corridors: no finite set of lighting paths works there. T10 asks for lattice rooms and lattice pairs only.

## Same-blocker check

Astra's view on 2026-11-25 (bbbb/l1-route-candidates.md): no all-area proof at ten walls with the methods of that date; first obligation is the pyramid word outside wb <= ud; a hand proof that selects a winding for every lattice placement there would be real progress. The blocker is the one that closed the gate-box route: produce one chord for a pinned lattice pair as the lengths grow.

New leverage since then:
1. Later-image selection (d235, reviewed): an explicit chord with a free winding count, proved for an unbounded family. It postdates all W = 10 work.
2. At r = 3 every gate has one reflex end and one wall end. The six-reflex chart that defeated the method had two corner ends per gate.
3. Exact tools decide any named room in under a second (scan_classes.py, the d236 enumerator with the complete decider), so each proof step gets a prediction-first test.

## Route and stop result

First step: the pyramid word, all lattice placements outside wb <= ud, both aperture widths free. It is the test Astra named, and it fails fast.
Stop result: a family of pyramid placements where every one-pass list in both axes misses, or no proof for the pyramid by 2026-11-30 20:00 HST. Then report to Daniel with what a W = 10 theorem would need.
If the pyramid closes: review it (it is a closure), then order the other seven words by the same method.

## Predictions (written before the brief)

- P(the pyramid word closes for all lattice placements by the deadline) = 25%.
- P(T10 complete within two weeks) = 10%.
