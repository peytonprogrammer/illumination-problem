# k5 residual classification (Claude, 2026-11-01)

All 10 current residual packets are LIT. Two independent methods agree on each one: the exact orbit decider `reduction/origami_dark.py`, and the exact Fraction tracer `folded/exact.py`, which supplies the path. Full paths are in `classified.json`.

| Case | Walls | Decider | Path direction | Bounces | vertices.json SHA-256 (prefix) |
| --- | --- | --- | --- | --- | --- |
| I2_1_1-pair0 | 19 | LIT (2174 states) | (-11, 5) | 13 | `4207ab78bc6bd4d2` |
| I2_2_0-pair0 | 20 | LIT (2184 states) | (-5, -12) | 15 | `b059a076056c9cbc` |
| I2_2_1-pair0 | 21 | LIT (373 states) | (-12, -5) | 58 | `39166ce6761afdac` |
| I2_2_2-pair0 | 21 | LIT (169 states) | (-12, -11) | 15 | `5a5cd32faf925ec4` |
| I2_3_0-pair0 | 21 | LIT (392 states) | (-12, -11) | 21 | `4cb629b278c9e787` |
| I2_3_1-pair0 | 21 | LIT (5 states) | (-12, 5) | 22 | `8d2d4628cdfe43bf` |
| I2_3_2-pair0 | 21 | LIT (1948 states) | (-12, -7) | 15 | `f85d77fcf85b90ee` |
| I3_4-pair0 | 21 | LIT (1938 states) | (-12, -5) | 12 | `3a539c481334a540` |
| I3_4-pair1 | 21 | LIT (1376 states) | (-11, -10) | 17 | `cb37c395d9debea4` |
| I3_7-pair0 | 21 | LIT (196 states) | (-12, 5) | 15 | `6aa6b4e1b4974170` |

DRAT replays (`drat-all.log`): all 21 UNSAT cases print `s VERIFIED` with `illumination-k4-codex/bounded-proof/drat-trim`. I3_6-pair0 has an empty proof file, because its formula is refuted by unit propagation alone.

## Continuation audit (2026-11-01)
- **3 new DRAT proofs.** I3_4-pair0, I3_4-pair1 and I3_7-pair0 all print `s VERIFIED` (`drat-continuation.log`, with CNF and DRAT hashes).
- **Guard sample (`guard_audit.py`).** This is my own exact Fraction checker and shares no code with Codex. For each guard it checks the following:
  - The path runs from (0,0) to q.
  - Every segment piece lies where all touching tiles are in U.
  - At each bounce, every touching tile is in U or Z, and a single tiling line separates U from Z. The line must contain a tile edge through the bounce point.
  - The bounce obeys the reflection law.
  - Any room that contains U and excludes Z then keeps the path valid.
- **Result.** 360 of 360 random guards pass: seed 1 drew 60, seed 2 drew 300, from 5,281–5,406 lines.
- **Controls (`guard_control.py`).** I corrupted 200 guards in each of three ways: dropped one U tile, nudged one bounce, and added a U∩Z contradiction. The checker rejects all 600.
- **Checker bug fixed before the counts above.** The first version picked any normal that separated the two tiles at a mid-edge bounce, so every guard failed falsely.

## Final k5 review (2026-11-01)
**Verdict: ACCEPT** the bounded theorem. Every dark room in the canonical 45° tiling that is strictly simple and slit-free, with two distinct interior A marks and k ≤ 5, has W ≥ 22.

- **7 I2 refutations.** All print `s VERIFIED` with drat-trim built from upstream source (commit `2e3b2dc`, not Codex's binary). Every CNF and proof hash matches `k5-proof-continuation/manifest.json`. The log is `drat-i2-final.log`, and I2_1_1 uses the standalone certificate under `certified/`.
- **All 31 cases.** Combined with the earlier 21 + 3 replays, all 31 accepted refutations are independently verified.
- **Guards.** My exact checker passes the whole guard library:
  - learned guards: 17,868 of 17,868;
  - peer guards: 10 of 10;
  - the earlier orbit guard: 1 of 1.
  - The result is in `guard_full.out`.
- **Scope checks:**
  - The k5 caps are I ≤ 4, P+m ≤ 11/9/7 and N ≤ 38.
  - The four-cell lemma excludes I=4, so the 22 supports and 31 pairs are reused.
  - The encoder runs with wmax=21, kmax=5 in both passes.
  - The universe radius is (the budget) − |R0−F0|, which is complete because edge-adjacent triangles lie in the same or axis-adjacent A-cells. So dropping out-of-universe Z literals is sound.
  - Guard maps use D4 about A points plus even translations and reversal, all of which preserve the tiling.
- **Not claimed.** A global minimum, arbitrary mark positions, and k ≥ 6.
