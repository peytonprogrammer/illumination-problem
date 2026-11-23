# d102: Q02 review — Q-class closure completeness and full witness replay

Referee for review-queue row Q02. Sources: `qclass-closure/README.md` steps 1–4,
`qclass-closure/enumerate.cpp`, `D/d71-check-qclass/`, and `D/d67-review-d64/indep.py`.

## Verdicts

- **Completeness (steps 1–2): sound.** No missing case found.
- **Lit side: all 3,933,192 saved witnesses replay.** Zero failures across 780,565 rooms.

## 1. Completeness read

The claim: anchoring the lowest-row, leftmost cell over four alignments, with 2×2 class blocks of
one or three cells, reaches every strictly simple room with a corner-only class and n ≤ 36.

I checked each link against `enumerate.cpp`.

1. **Class condition equals block masks.** Each unit cell has exactly one vertex of a given parity
   class, so the class blocks partition the cell grid. At a class point, 0 cells means outside,
   1 or 3 means a corner, 2 adjacent cells means a smooth wall point, and 4 means interior.
   The diagonal masks 6 and 9 are pinches, which strict simplicity excludes. So "every class point
   in the closed room is a corner" is equivalent to "every class block has 0, 1 or 3 cells".
   The code offers exactly masks {1, 2, 4, 8, 7, 11, 13, 14}, and every 3-cell mask is an L.
2. **Alignments.** `base` puts the block's lower-left cell at parity (px, py). The four phases
   cover all four class positions relative to the anchor.
3. **Anchor.** `forbidden` excludes cells below the anchor row and cells left of the anchor in
   that row. Any room translates so its lowest-leftmost cell is the anchor. Forbidden cells are
   only blocked from being present; a block that contains one can still be placed with it absent.
4. **Branch completeness.** The walk queries every edge neighbor of every placed cell in order.
   Each query branches on "absent" or "present via a block mask containing it". For a target room
   P, the branch that follows P's own blocks is always consistent, and P's connectivity means
   every cell of P gets queried. New cells join the set through z or an L, so the set stays
   connected. Every block holding a present cell is fully decided by an allowed mask. A later
   conflicting assignment is rejected by `state[c] != v`.
5. **Pruning is sound.** `invalid` fires only when no completion of a vertex star avoids masks
   6 and 9. "Inevitable reflex" and "inevitable convex" fire only when every legal completion is
   reflex or convex. Forbidden cells are never recorded as absent, so the star tests see a
   superset of the true completions. That weakens pruning but never cuts a real room. The caps
   r ≤ 8, convex ≤ 12 and n ≤ 36 follow from 2r + 4 ≤ 20 and the D68 bound n ≤ 3r + (r + 4).
6. **Emit filter.** Pinch rejection, `v − r = 4` (a pinch-free connected polyomino has
   v − r = 4 − 4·holes), and ≥ 2 interior points are exact. Symmetry reduction keeps the
   lex-least orientation. That orientation is itself a qualifying room with some corner-only
   class, so some phase emits it. `sort -u` removes rooms emitted by two phases.
7. **Array bounds.** n ≤ 36 at node entry, plus at most 3 cells per block, stays below
   `filled[42]`. Coordinates stay inside the 100×100 grid.

The README text is terse, but every step it states matches the code, and the code covers every
case. I found no gap.

### Independent spot check

`brute.py` enumerates fixed polyominoes directly (Redelmeier). It filters by connectivity,
pinches, the Euler characteristic, ≤ 20 walls, ≥ 2 interior points and a corner-only class, then
reduces by the 8 symmetries. It shares no code with `enumerate.cpp`, `independent.c` or
`polyo.c`. Per-area counts match the room list in `witnesses.txt.gz` for every area 1–13
(3, 16, 63, 234, 907, 3,262 at areas 8–13). Log: `brute13.log`, 23.7 CPU s.

## 2. Full witness replay

`replay.py` uses d67's integer billiard (`indep.shoot`) with two changes. It stops at the target,
and it counts lattice-point events so it can compare the saved step count m. It imports nothing
from `qclass-closure` or `d9`. Per room it also checks, with d67's helpers, strict simplicity,
≤ 20 walls, a corner-only class, and that the saved pairs are exactly all unordered pairs of
interior lattice points. Each first-pass `U` record is looked up in `witnesses-retry.txt.gz`.

Sizing: a 2,000-room sample took 0.2 CPU s above the 2.4 s parse cost, which projected about
80 CPU s in total. That's under the 6-minute threshold, so I ran the full replay.

Full result (`full.log`, 72.5 CPU s):

| Check | Count |
| --- | --- |
| Rooms | 780,565 |
| Hypothesis failures | 0 |
| Witnesses replayed | 3,933,192 |
| Replay failures | 0 |
| Lit, but at a step count other than m | 0 |
| First-pass `U` records | 4,655, all resolved by the retry file |
| Missing, extra or duplicate pairs | 0 |

Negative control (`control.log`, 2,000 rooms): the tracer rejected all 9,587 wrong-target
corruptions and all 4,877 off-by-one step counts. It accepted 28 of 10,268 sign flips. Those 28
are expected: a mirror-symmetric room maps a path to its reflection, so a flipped direction can
also reach T at the same step.

This replaces d71's sampled search with a replay of every saved witness. Only saved rooms and
witnesses were used; no new rooms, rays or directions were searched.

## Scope notes

- This review covers integer marks in rooms with integer side lengths, as the README states.
  The off-grid and real-endpoint extension in `qclass-closure/twenty/` is out of scope here.
- The upper bound (the 22-wall dark pair) rests on the manuscript, not on this census.

## Re-run

```
cd illumination-generalization-2026-11-06/fable/directions-2026-11-09/d102-qclass-replay
python3 -B replay.py 1 2000 > sample2000.log   # timing sample
python3 -B replay.py 0 0 > full.log            # full replay, about 75 CPU s
python3 -B control.py 2 2000 > control.log     # negative control
python3 -B brute.py 13 > brute13.log           # completeness spot check, about 25 CPU s
```

Total CPU used by this review: about 105 s.
