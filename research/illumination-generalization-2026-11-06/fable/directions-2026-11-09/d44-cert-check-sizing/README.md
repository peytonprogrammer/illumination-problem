# d44: design and sizing of the certificate check for 5 <= r <= 8

Opus 5.5 subagent, 2026-11-14. Sizing only. The full check was not run. No
illumination, ray, or direction search was run.

## Summary

- **Chosen design: room-side enumeration with proved structural pruning.**
  Rooms are enumerated as compressed shapes plus widths and heights. A proved
  filter (F\*, below) acts on reflex-corner parity classes and area before any
  room is materialised. The exact class-partition check then runs only on
  survivors.
- **The plain room-side check is infeasible on one laptop.** The range holds
  about 1.9 x 10^13 free rooms, almost all at W = 20. At 5 us per room that
  is about 2.6 x 10^4 CPU-hours.
- **The pruned check is feasible.** About 1.5 to 2.1 x 10^10 free rooms
  survive F\*. The estimate is about 60 CPU-hours, with a range of 25 to 180.
  On 8 cores that's 3 to 23 hours of wall clock.
- **Before the full run,** a referee should sign off F\* (a short corollary,
  see "Proved and new claims"). Run a W <= 18 pilot first to recalibrate.

## What the check decides

From `../d43-review-d39/review.md`: take a strictly simple room with
`5 <= r <= 8`, `21 <= n <= 5r`, and corners in at least 3 parity classes. The
check must show that no same-class pair of interior lattice marks S, T has all
four endpoint lift pairs separated by each of `B_b`, `B_c`, `B_d`. A room and
pair with that property is a **positive**.

The check enumerates cell sets, not normalized shapes. So it covers
non-normalized rooms with at least 3 corner classes, as d43 item 1 requires.
Rooms with at most 2 corner classes are counted and skipped (d43 item 3).

## Designs compared

| Design | Objects | Proof status | Cost |
| --- | --- | --- | --- |
| a1. Redelmeier polyominoes to area 40, as in d9 | about 10^22 fixed polyominoes | complete | impossible |
| a2. Compressed shapes x weights, every room checked | 1.9 x 10^13 free rooms | complete, uses only d36.4's range | about 2.6 x 10^4 CPU-h |
| a2 + d36 area filter | 9.9 x 10^12 free rooms | proved (d36.4) | about 1.4 x 10^4 CPU-h |
| **a2 + F\* (chosen)** | 8.9 x 10^9 fixed shapes, then about 2 x 10^10 free rooms | F\* is a short corollary of reviewed results; needs a referee line | about 60 CPU-h (25 to 180) |
| b. Pure target-side: small targets N, degree-delta covers, rebuild rooms | 26,640 target tuples, then an unsized cover count | needs a realizability procedure or a new tiling lemma | not sized; model guess 0.01 to 10 CPU-h |

**Why a2 and not a1.** Every room is a unique compressed shape (no two adjacent
rows or columns equal) with positive column widths and row heights. Stretching
keeps corners, strict simplicity, and simple connectivity, so W depends on the
shape only. The area is `sum_j h_j * sum_{i in row j} w_i`. W <= 20 forces at
most 9 rows and 9 columns. This replaces a hopeless area-40 polyomino search
with a shape search bounded by the corner budget.

**Why not pure b.** Design b needs a way to turn a cover tuple back into a
room. That needs either the seam involution data or a new lemma that the room
is a reflection tiling by delta copies of the target disc. Neither exists yet.
Design b's structure is still the source of the F\* pruning.

## Proved and new claims

**Proved in reviewed write-ups (used):**

- d36.4 (d38: CORRECT): a non-unit class quotient has `n = delta * d`,
  `d <= 4z + 1` (`d <= 4z` if d is even), `z >= 1`, `delta * z <= r`, so
  `n <= 5r`. Each zero of N has delta unramified zero preimages.
- d36.3 (d38: CORRECT): if all three `phi_x` are Galois, the join separates.
- d2, as cited by d43 item 1: a common separating parity factor needs `r >= 9`.
- A degree-1 or degree-2 cover is Galois.

**F\* (new, short corollary; needs one referee pass).** Suppose a room with
`r <= 8` has a positive pair. If every `phi_x` were Galois, d36.3 and d2 would
give a contradiction. So some class x has a non-Galois quotient, hence
`delta >= 3`. By d36.4 its z zeros each have delta reflex preimages, all in
the parity class of that zero's corner. Write `rho_y` for the number of reflex
corners in parity class y. Then some factorisation `n = delta * d` with
`delta >= 3` has

```
sum_y floor(rho_y / delta) >= z_min(d),  z_min(d) = ceil((d-1)/4) (d odd), ceil(d/4) (d even),
z_min(d) * delta <= r.
```

At `r <= 8` this forces `z <= 2` and `d <= 9`. Consequences:

- Allowed areas: r = 5: {25}. r = 6: {21, 24, 25, 27, 30}. r = 7: {21, 24, 25,
  27, 28, 30, 35}. r = 8: {21, 24, 25, 27, 28, 30, 32, 35, 36, 40}.
- Example: n = 40 at r = 8 needs all 8 reflex corners in one parity class
  (delta = 8, d = 5, z = 1).

The referee should check two points. First, that d2's statement covers the
join quotient of d36.3. Second, that "zero preimages lie in the zero's parity
class" follows from the factorisation `DP -> N -> PC`. Both look immediate.

`rho_y` depends only on the shape and the parities of the widths and heights.
So F\* can run once per (shape, parity pattern) before any room is built.

**New claims considered and not used:**

- Stretch monotonicity (B_x one block stays one block when a width grows by
  2). Unproved. It would cut only by about 30x anyway: rooms with all widths
  and heights in {1, 2} still number 4.7 x 10^12 fixed at W = 20.
- delta = 2 forces a lattice symmetry of P (from d36.1). This is true but F\*
  already removes delta <= 2.
- Reflection-tiling structure for delta >= 3 (needed for pure design b).
- delta = 1 rooms (no transparent x point) are impossible at n >= 21. This is
  plausible, but not needed.

## Counts

All counts are fixed rooms (all 8 orientations) unless marked free. Free is
about fixed / 8.

**Exact (`count_rooms` mode 0 and 1).**

- Free counts for every (W, area) with W <= 20 and area <= 12 match the d9
  census: 66 of 66 cells (`val_a12.log`, `compare_census.py`).
- W = 14, areas 21 to 25: 434,437,036 fixed rooms (`cnt_14_25.log`). At
  area 20 this run gives 21,348,116 fixed, and the census gives 2,668,579
  free.
- An exact W = 16, area <= 30 run hit the 60 s cap and was dropped.

**Estimated (Knuth probes, mode 2).** Importance sampling picks child rows with
probability proportional to `4^(corner budget left) * 1.15^(cells left)`. On
W = 14 it gave 4.5 to 5.5 x 10^8 against an exact 4.86 x 10^8. At area 20 it
is 8 to 15% below 8 x census. So treat each estimate as +-25% with a slight
low bias.

| W | r | Areas | Fixed rooms in range | Fixed shapes (base area <= 5r) | F\* survivors (free) |
| --- | --- | --- | --- | --- | --- |
| 14 | 5 | 21..25 | 4.34 x 10^8 (exact) | 2.36 x 10^5 (exact) | 2.8 x 10^4 |
| 16 | 6 | 21..30 | 2.9 x 10^10 | 6.5 x 10^6 | 1.4 x 10^7 |
| 18 | 7 | 21..35 | 2.0 x 10^12 | 2.4 x 10^8 | 4.2 to 5.3 x 10^8 |
| 20 | 8 | 21..40 | 1.5 x 10^14 | 8.6 x 10^9 | 1.4 to 2.1 x 10^10 |
| Total | | | 1.5 x 10^14 (1.9 x 10^13 free) | 8.9 x 10^9 | 1.5 to 2.1 x 10^10 |

Survivors are the estimated count per (W, area) times the F\* pass rate on
80,000 sample rooms (`filter_rate.log`). The samples aren't uniform: shapes
come from probes and weights are geometric. Treat the survivor numbers as
uncertain by a factor of 3. Pass rates run from 0 of 3,224 samples (r = 8,
n = 40) to 34% (r = 8, n = 21).

**Design b sizing input.** The d6 Hurwitz census holds 26,640 genus-0 target
tuples with d <= 9, z in {1, 2}, the d36.4 degree bound, and singular points
in at least 3 corners (`targets.log`).

## Timings

| Item | Measured |
| --- | --- |
| Per-room check, C prototype (`check_rooms.c`), 2,000 sample rooms per W | 6.0, 6.8, 7.9, 9.4 us per room at W = 14, 16, 18, 20, including text parsing |
| Shape DFS, W <= 14, base area <= 25 (no weight counting) | 1.5 s for 2.36 x 10^5 W = 14 shapes, about 6.4 us per shape |
| Shape DFS, W <= 16, base area <= 21 | 12.7 s |
| Named rooms (`validate_named.py`) | 26 us per room; up to 108 cells |

None of the 8,000 timing samples had a non-trivial `B_b`. The C check stops at
the first one-block partition.

## CPU estimate for the chosen design

| Stage | Work | CPU-hours |
| --- | --- | --- |
| 1. Shape DFS, W = 14..20, base area <= 5r | 8.9 x 10^9 fixed shapes at 5 to 20 us | 12 to 50 |
| 2. F\* per canonical shape and parity pattern | at most 5.8 x 10^11 patterns at 0.02 to 0.2 us | 3 to 30 |
| 3. Materialise survivors, run the B_x check | 1.5 to 2.1 x 10^10 free rooms at 3 to 10 us, x3 rate uncertainty | 10 to 100 |
| Total | | about 60 (25 to 180) |

The plain a2 design without F\* would cost about 2.6 x 10^4 CPU-hours.

## Validation plan

1. **Named rooms, done here** (`validate_named.log`). The C check agrees with
   `roomtools` block counts on every class. It reports:
   - 22-wall room (r = 9, area 15): POSITIVE at S = (0,0), T = (2,2), blocks
     5, 15, 5.
   - P6 (r = 12, area 20): POSITIVE at S = (1,0), T = (3,-2), blocks 5, 5, 5.
   - 12-wall cross: negative (`B_c` is one block).
   - Cross scaled by 2 and by 3: negative.
   F\* passes all three named rooms (`fstar_named.log`), so the filter doesn't
   discard the known positives.
2. **Pipeline, widened range.** Run the full pipeline (shape DFS, F\* with
   general r, check) for W <= 22 and area <= 20. By the d9 census it must
   output exactly one positive, the 22-wall room's pair, and nothing at
   W <= 20. Run P6's compressed shape alone at W = 28 and confirm it is
   reported. A full W = 28 run is not sized.
3. **Counts.** Per-(W, area) room totals must match the d9 census for
   area <= 20, and the exact W = 14 counts here.
4. **Filter cross-check.** Run r = 5 (5.4 x 10^7 free rooms, about 5 CPU-min)
   and r = 6 at F\* areas (1.9 x 10^9 free, about 3 CPU-h) with and without
   F\*. Both must give the same positives.
5. **Two implementations.** Recheck every positive and a random 10^5 survivors
   with `roomtools` in Python.

## Recommended caps for the full run

- **Processes:** 8 (leave 2 cores free), jobs split by the first two shape
  rows into about 500 resumable jobs.
- **Wall clock:** 24 hours for the full run, after a W <= 18 pilot capped at
  2 hours. Stop if the pilot's survivor count is more than 5x the estimate.
- **Memory:** 1 GB total. Each process needs well under 100 MB.
- **Disk:** 1 GB. Write per-job counts, survivor counts, and positives only.
  Don't store rooms.
- **Feasibility:** feasible on one laptop overnight, given F\* sign-off.
  Without F\*, it isn't.

## Open risks

- Counts are sampling estimates (+-25%, slight low bias). Survivor rates come
  from non-uniform samples (factor 3).
- Stage 1 cost at W = 20 is extrapolated from W <= 16 timings.
- F\* depends on d2's `r >= 9` statement applying to the d36.3 join. If it
  doesn't, the fallback is a2 with the d36 area filter, at about
  1.4 x 10^4 CPU-hours.
- Stage 2 still needs code: shape-level canonical form under the 8 symmetries
  and a parity-pattern loop. Symmetric shapes need deduplication.
- The check covers ordinary certificates over the unit pillowcase B. Relative
  certificates (d43 item 2), rooms with at most 2 corner classes (item 3),
  rational marks, and different-class marks stay out of scope.
- The d9 census reported a heavily loaded machine (load 100 to 170). Wall
  clock could double.

## Resource use of this sizing job

About 3 to 4 CPU minutes in total, at most 2 concurrent processes, and about
120 KB of files in this directory, including sources. One run hit its 60 s cap (exact W = 16 count) and was
dropped.

## Files

- `count_rooms.c`: compressed-shape counter. Mode 0 gives exact fixed counts,
  mode 1 free counts, mode 2 Knuth estimates, and mode 3 random sample rooms.
- `check_rooms.c`: C prototype of the per-room check (B_b, B_c, B_d,
  separation of all four lift pairs).
- `validate_named.py` and `validate_named.log`: named rooms, C against
  `roomtools`.
- `compare_census.py` and `val_a12.log`: count validation against d9.
- `cnt_14_25.log`: exact counts, W <= 14.
- `est_W16.log`, `est_W18.log`, `est_W20.log`: estimates.
- `tally.py` and `tally.log`: range totals and the d36 area filter.
- `filter_rate.py`, `filter_rate.log`, `survivors_est.py`, and
  `survivors_est.log`: F\* pass rates and survivors.
- `fstar_named.log`: F\* on the named rooms.
- `targets.py` and `targets.log`: design b target count.

To rebuild, run `clang -O3 -march=native -o count_rooms count_rooms.c -lm` and
`clang -O3 -march=native -o check_rooms check_rooms.c`.
