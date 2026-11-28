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

## Step 1 result (2026-11-27 23:05 HST): pyramid not closed, one new sufficient lemma, no counterexample

Astra's note: bbbb/t10-pyramid.md (unreviewed). She stopped on the method, not on a counterexample.
- Lemma (later-image, vertical): with g = gcd(dV, ub), eta = gcd(wg, auV)/g, L = d + b, D = a + L, the pair is lit when g/L + b*eta/D < u. A perpendicular variant needs g'/L' + b'*eta'/D' < u'/2.
- Open region: all three of min(ub, dV) + wb > u(d+b), g/L + b*eta/D >= u, g'/L' + b'*eta'/D' >= u'/2. Named example: w=4, u=5, V=60, (q,h,d,f)=(8,4,1,2), (x,z,a,b)=(1,15,1,3), area 285.
- Lattice marks don't remove the old obstruction: at widths (200, V, 400, 200) with V = 38400 and 57600 the vertical list misses and the horizontal list hits.

Coordinator checks, onepass.py (complete one-pass list per axis over one full period, exact integers):
- Controls: reproduces Astra's three named tests (vertical 0 hits of 2,688,000 and 4,032,000; her named displacements hit).
- Gap room at V = 60, 120, 180, 240, 300: vertical hits at 22 and 32 (mod 10V/3), horizontal 132 hits per 1,680 at every V. Prediction held (80% for one axis at all five; 50% for both at V = 60). The gap is in the estimate, not in the lists.
- Lemma at V = 193, 577, 1001, 4097, 20001 (third-test family): 276 vertical hits per period each. Prediction held (95%).
- Observation, by geometry: the horizontal list from T never sees x > z, so it doesn't depend on V.

Review deferred: the lemma covers part of one word, and no decision depends on it until the open region has a route.
Next: brief 2 to Astra asks for the exact hit criterion per list and either an incompatibility proof or a hand-built both-miss room (at most 5 candidates, tested with onepass.py).
Question for Daniel: a bounded search for a room where both one-pass lists miss needs his approval.
