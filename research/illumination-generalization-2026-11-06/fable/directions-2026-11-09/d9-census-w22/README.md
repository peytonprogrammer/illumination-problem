# D9: exhaustive census of dark pairs, W <= 22

Opus 5.5 subagent, 2026-11-09. Daniel approved this room census today.
All arithmetic is exact integer arithmetic, plus Fractions in the
third-party tracer. No human has reviewed it.

## Result

- **Bound completed: A_max = 20.** The census covers every strictly simple
  polyomino room with area at most 20 and at most 22 walls, up to the 8
  lattice symmetries: 945,070,200 rooms. 173,270,477 of them have two
  interior lattice points of one parity class. They hold 217,900,349
  same-class pairs, with all four classes counted.
- **One dark pair.** 217,900,348 pairs are lit by an explicit path. A
  second, independent tracer re-checked every one of those paths. The one
  remaining pair is (0,0),(2,2) in the known 22-wall room. Three complete
  deciders call it dark.
- **(a)** No dark same-class pair exists in any room with W <= 21 and area
  <= 20.
- **(b)** At W = 22 and area <= 20, the known room is the only dark room up
  to symmetry, and its pair is the only dark pair.
- **(c)** "Dark if and only if N_min separates" holds for all 217,900,349
  pairs. No lit pair is separated, so the proved lemma is not contradicted.
  The one dark pair is separated.
- **(d)** The largest k among lit pairs is 26. Of the rooms with W <= 20,
  100,538,916 have a lit pair with k >= 7. In total, 173,183,153 rooms have
  one.
- **Not covered:** rooms with area 21 or more. That includes long, thin rooms
  with W <= 22, of which there are infinitely many. Their area has no bound,
  so no finite census reaches them all.

## Scope and definitions

- **Room.** A finite union of closed unit lattice squares. Its interior is
  connected, it has no holes, and it has no pinch point (a lattice point
  with exactly two diagonally opposite cells). Its boundary is then one
  simple closed curve.
- **W.** The number of maximal straight walls, which equals the number of
  corners, meaning lattice points with 1 or 3 cells around them. `r` counts
  the reflex corners, and `W = 2r + 4`.
- **Pairs.** Every unordered pair of distinct interior lattice points, with
  4 cells around each, in the same parity class. All four classes count.
  The census includes a room when some class has two interior points.
  Symmetric rooms are counted once. Their pairs are not merged under the
  room's symmetry.
- **Lit.** A billiard path joins the points. It may reflect at flat
  boundary lattice points and pass through interior lattice points. It may
  not meet a corner.
- **k for a pair.** The number of transparent lattice points of the other
  three classes. Transparent means interior or flat boundary. This
  definition gives k = 7 on all 30 k7 models in the record.
- **N_min, through B_min.** Label the cells of the room. B_min is the finest
  partition of cells that meets two conditions. First, it contains the
  2-cycles at transparent points of the other three classes: both diagonal
  pairs at an interior point, and the two cells at a flat point. Second,
  the four edge-crossing involutions of the pillowcase fold preserve it,
  with the class origin at the pair. N_min separates S and T when no cell
  at S shares a B_min block with a cell at T. The d2 audit (section 3.1)
  shows this is the G-congruence it defines. The cross-checks below confirm
  that both constructions agree on 721,884 rooms.

## Method

1. **Enumeration (`enum_rooms.c`).** Redelmeier's method lists every fixed
   polyomino up to area 20. Each polyomino gets these checks:
   - a 4-bit cell mask at each lattice point;
   - rejection of pinch points;
   - rejection of holes, by testing V - E + F = 1;
   - W <= 22;
   - the canonical representative among the 8 symmetric images.

   The search tree splits at polyomino size 11 into 26 jobs.
2. **Cheap exact filter (`shoot.c`).** The filter builds the 4-fold
   unfolding as an origami. Each square is a pair (cell, sheet), and each
   square carries the room point at its bottom-left corner. From every copy
   of each source, it follows every primitive direction (p, q) with p, q >= 0
   and p + q <= 40 (491 directions). It moves one lattice step at a time
   until the ray returns to its start or meets a corner. The first hit
   joining each pair becomes the pair's certificate: source, initial room
   direction, and number of lattice steps.
3. **Second tracer (`verify_plane.c`).** This code shares nothing with
   step 2. It replays every certificate in the room plane with integer event
   times and the reflection law. It confirms that the path ends at T and
   meets no corner. It ran inside every census job. It rejected 0 of
   217,900,348 certificates.
4. **N_min and k** come from `shoot.c` for every pair.
5. **Complete decider for survivors.** Survivors are pairs that the filter
   didn't light.
   - `orbitc.c` (C) and `orbit.py` (Python) are two implementations of the
     SL(2,Z) orbit of the marked unfolding. The moves are the two shears and
     their inverses: `h' = h, v' = v o h^-1` and `h' = h o v^-1, v' = v`.
     Every move keeps each square's bottom-left corner, so labels never
     change.
   - States are canonical up to relabellings that keep the labels: source
     index, corner, or free.
   - Each state's horizontal rays from source squares cover one direction
     class. The whole orbit covers every primitive direction, so a full
     orbit with no hit is a complete DARK decision.
   - Every DARK verdict also needs `room_model.illumination` from the d2
     audit, written by another agent.
6. **Dark-room analysis (`process_survivors.py`)** gives:
   - vertices, by the d3 reviewer's boundary walk;
   - W, r, area, and k;
   - the monodromy group order and block systems, from room_model;
   - B_min and N_min separation, from room_model's own closure;
   - equivalence to the known room, by canonical form.

## Validation

| Check | Result |
| --- | --- |
| Fixed polyomino counts per area, 1 to 20 | Equal to OEIS A001168, including 22,964,779,660 at area 20 |
| Free room counts per (area, W) and eligible rooms, area <= 12, against an independent brute force (`check_enum_small.py`: set growth plus a boundary-cycle walk) | Identical (`check_enum_small_12.log`) |
| Parallel split, area 14: 1 job against 5 jobs | Identical room lists and counts (`check_split.log`) |
| 22-wall room, own deciders | DARK. orbitc and orbit.py each reach 2,592 states, the same number room_model reports. The full matrix over regular A points matches room_model, including the smooth points (4,0) and (2,-2). |
| Five-square staircase | DARK, 24 states, matching room_model |
| 56 lit controls through orbitc, with no shooting: 30 k7 models, the W18 k7 control, and the 25 census pairs with the longest certificates | 56 of 56 LIT. orbit.py agrees on the first 12 with identical state counts (`validate_controls.log`). |
| Record rooms inside the census (`check_known_in_census.log`) | Known room found, one pair, unresolved and separated. All 23 k7 rooms with area <= 16 found, every pair lit. |
| Every room with area <= 16 (721,884 rooms, 792,133 pairs; `crosscheck_full.log`) | 0 mismatches. W and strict simplicity by boundary walk; r and k recounted; B_min block count and separation from room_model's G-closure; all 792,132 certificates replayed by the d3 reviewer's `Surface.segment` (Fractions), or by a grid-line walk for axis directions |
| 34-wall orthogonal room, area 19, pair (2,0)-(6,0) | Not completed. Shooting finds no path with p + q <= 40. N_min = DP (k = 0) separates the pair, so the proved lemma makes it dark. orbitc was stopped at about 12 million states because the machine was swapping (`validate34_orbitc.log`). This room has W = 34, so the census excludes it anyway. |

One bug was found and fixed during validation. A first build printed the
class label of the `K` line in shifted internal coordinates. The cross-check
caught it. All census outputs come from the fixed build.

## The dark pair

`dark_rooms.json`, `survivors.log`. In census coordinates:

- Cells: (0,2) (0,3) (1,1) (1,2) (1,3) (1,4) (2,0) (2,1) (2,4) (2,5) (3,4)
  (3,5) (4,3) (4,4) (5,3).
- Vertices: (0,2) (0,4) (1,4) (1,5) (2,5) (2,6) (4,6) (4,5) (5,5) (5,4)
  (6,4) (6,3) (4,3) (4,4) (2,4) (2,2) (3,2) (3,0) (2,0) (2,1) (1,1) (1,2).
- Pair: S = (1,3), T = (3,5). This is (0,0),(2,2) of the manuscript room
  after the shift (x+1, y+3).
- W = 22, r = 9, area 15, k = 4.
- Monodromy group order 233,280. The only proper block system has block
  size 3.
- B_min has 5 blocks of size 3. N_min separates S and T.
- Equivalent to the known 22-wall room: yes.
- Deciders: orbitc DARK (2,592 states, complete), orbit.py DARK (2,592
  states), room_model DARK.

## Totals by W

The full table per (W, area) is in `census_totals.md` and
`census_totals.json`. Every row has 0 dark pairs except (22, 15).

| W | Rooms | Rooms with eligible pairs | Pairs | Dark | Rooms with a lit pair, k >= 7 | Max k (lit) |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 35 | 12 | 86 | 0 | 12 | 24 |
| 6 | 303 | 157 | 736 | 0 | 157 | 26 |
| 8 | 7,076 | 3,780 | 13,838 | 0 | 3,780 | 25 |
| 10 | 96,990 | 50,659 | 144,422 | 0 | 50,658 | 25 |
| 12 | 950,210 | 455,084 | 1,047,177 | 0 | 455,072 | 24 |
| 14 | 6,445,422 | 2,700,230 | 5,112,233 | 0 | 2,700,109 | 22 |
| 16 | 31,283,242 | 10,884,324 | 17,399,895 | 0 | 10,883,551 | 21 |
| 18 | 109,535,695 | 29,960,973 | 41,552,091 | 0 | 29,957,484 | 19 |
| 20 | 279,084,099 | 56,504,029 | 69,966,386 | 0 | 56,488,093 | 18 |
| 22 | 517,667,128 | 72,711,229 | 82,663,485 | 1 | 72,644,237 | 16 |

Rows by area at W = 22:

| Area | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rooms | 11,707 | 93,477 | 556,286 | 2,664,253 | 10,776,173 | 38,043,674 | 120,133,065 | 345,387,503 |
| Eligible rooms | 2 | 104 | 3,785 | 46,896 | 406,503 | 2,611,743 | 13,341,095 | 56,301,101 |
| Pairs | 2 | 104 | 3,789 | 47,065 | 413,398 | 2,715,921 | 14,492,879 | 64,990,327 |
| Dark pairs | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

## Computed facts and interpretation

**Computed facts.**

- The counts above.
- The shooting filter left one survivor in the whole census. Every other
  pair is lit through a direction with p + q <= 40.
- At W <= 20, only 20,332 eligible rooms have every pair with k <= 6.
- The largest k at W = 22 among lit pairs is 16. The dark pair has k = 4.

**Interpretation.**

- Within area 20, the census supports the main conjecture: W <= 21 has no
  dark pair. It also supports the same-fibre conjecture with no exception.
  On the lit side the support is broad, with about 2 x 10^8 pairs, most
  with k >= 7.
- On the dark side the evidence stays thin. The census finds only one dark
  pair. So "separated implies dark" is tested once, where it is already
  proved. The content of the converse lies in the lit pairs.
- The k <= 6 theorem covers few rooms. In this census, k >= 7 is the
  common case at every W <= 20.

## Open doubts

- **Area > 20 is not covered.** In particular, the census says nothing about
  rooms with W <= 22 and area >= 21.
- **The orbit deciders are validated only on rooms in the record.** They
  produce a full DARK decision on just two rooms: the staircase and the
  22-wall room. For the 34-wall room the orbit did not finish. Every census
  lit verdict comes from explicit paths checked by two or three tracers, so
  this limit affects only the one DARK verdict. Three deciders, one by
  another agent, agree on that verdict, and the proved lemma confirms it.
- **Path convention.** A path through a flat boundary lattice point
  reflects there, and a path along an edge of the unfolding is legal. From an interior start, an axis path
  never runs along a wall, and `verify_plane.c` rejects such a path if it
  occurs. It never occurred.
- **Certificates are not all on disk.** The machine had 0.4 to 3 GB of free
  disk. So per-pair certificates are stored only for area <= 16
  (`runs/a20/job-*.out.gz`). For larger areas, rerun the pipeline, which is
  deterministic. Every certificate was re-checked when it was produced.
- **Restarts.** The machine's load average was 100 to 170 during the runs.
  Batch 1 was restarted twice: once for the label bug, and once to add the
  per-W k counters. Final batches took 14.5 and 13 minutes.

## Reproduce

Run from this directory. Paths to `../d2-factor-audit` and `../d3-review`
are read in place and never modified.

```sh
clang -O3 -march=native -o enum_rooms enum_rooms.c
clang -O3 -march=native -o shoot shoot.c verify_plane.c
clang -O3 -march=native -o orbitc orbitc.c
./run_census.sh 20 26 40 16 runs/a20 0 12      # about 15 min under load
./run_census.sh 20 26 40 16 runs/a20 13 25     # about 13 min
python3 process_survivors.py runs/a20 > survivors.log
python3 aggregate.py runs/a20 26 > census_totals.md
python3 check_known_in_census.py runs/a20 26 > check_known_in_census.log
python3 crosscheck.py runs/a20/job-0.out 1     # one job; loop over 0..25 for all
python3 validate_controls.py runs/area15_check.out > validate_controls.log
```

To repeat the enumeration check: the logged run wrote the room list and the
counts to one file and passed that file. Run
`./enum_rooms 12 22 1 0 e12.txt e12.counts; cat e12.counts >> e12.txt;`
then `python3 check_enum_small.py 12 e12.txt`.

`runs/area15_check.out.gz` is a separate area <= 15 run with bound 30.
`validate_controls.py` reads it to choose census controls. The room ids in
`validate_controls.log` refer to that file.

## Files

- `enum_rooms.c`: enumerator.
- `shoot.c`: filter, N_min, k, and counters.
- `verify_plane.c`: second tracer.
- `orbitc.c` and `orbit.py`: complete deciders.
- `run_census.sh`: batch runner.
- `check_enum_small.py`: brute-force enumeration check.
- `crosscheck.py`: cross-checks against room_model and the d3 tracer.
- `validate_controls.py`: lit controls.
- `check_known_in_census.py`: finds record rooms in the census.
- `process_survivors.py`: survivor decisions and dark-room analysis.
- `aggregate.py`: totals.
- `room34.py`: 34-wall room loader.
- `census_totals.md` and `census_totals.json`: totals.
- `survivors.json`, `survivors.log`, and `dark_rooms.json`: survivors and
  the dark room.
- Logs: `check_enum_small_12.log`, `check_split.log`,
  `validate_controls.log`, `check_known_in_census.log`,
  `crosscheck_batch1.log`, `crosscheck_batch2.log`, `crosscheck_full.log`,
  `validate34_shoot.log`, `validate34_orbitc.log`,
  `runs_a20_batch1.log`, and `runs_a20_batch2.log`.
- `runs/a20/job-*.counts`, `job-*.sv`, `job-*.err`: per-job enumerator
  counts, survivors, and errors (all `.err` files are empty).
- `runs/a20/job-*.out.gz`: shooter summaries, plus certificates for
  area <= 16.
- `inputs/`: copies of the 34-wall room, the k7 models, and the k7 controls.
