# Review of the 44-bounce guard and the orbit-direction extraction

Claude, 2026-11-01. Reviews `illumination-k4-codex/k5-proof-pilot/{orbit-witness.py,inputs/origami_frame.py}` and `cases/I2_1_1-pair0/guard.json` (read-only).

**Verdict: ACCEPT both.**

## 44-bounce guard
- My checker `k5-residual/guard_audit.py` passes both copies of the guard, in `cases/` and in `inputs/pilot/`. Each has 44 bounces, 20 used triangles and 12 absent ones, which matches Codex's claim.

## Orbit-direction extraction
- **Hand derivation.**
  - After T = (R, U R⁻¹), new up is old (−1, 1) and new right is old (1, 0). So B is right-multiplied by [[1,−1],[0,1]].
  - After L = (R U⁻¹, U), new right is old (1, −1). So B is right-multiplied by [[1,0],[−1,1]].
  - Both match Codex. Developed translations commute, so the permutation composition order doesn't affect the vector.
  - `source_frame` is the D4 element g of the copy in which S is a square's lower-left corner, with developed = g·physical. So physical = gᵀ·developed is correct for any g.
- **Replay (`extract_bfs.py`, `bfs.out`).** I rebuilt the matrices from my own derivation and ran a breadth-first orbit search, the order `k5-proof-continuation/run.py` uses. Then I replayed each direction with my own tracer, `folded/exact.py`.
  - Seed 1: 160 of 160 lit. Seed 2: 810 of 810 lit, with |direction| ≤ 34.
  - The samples come from 17,868 generation rooms, plus the 10 pilot packets.
  - Control: reading row 0 of B instead of column 0 gives a wrong direction that fails 711 of 719 times.
- **D4 images (`extract_d4.py`, `d4.out`).** All 8 images of 100 rooms: 800 of 800 lit. Every build returned frame −I, so the transpose is confirmed by reading the code, not by a test.
- **Pilot extractor caveat.** `orbit-witness.direction` searches depth-first (`todo.pop()`). It returns valid but huge directions, such as (−135553594, 3247628349), whose physical paths are very long. The continuation run uses breadth-first search (`popleft`), so its guards are unaffected. Prefer breadth-first search anywhere a path gets replayed.
