# D206 · Referee review of the d205 area-21 census

Independent referee, 2026-11-23. Scope: [d205-census-a21](../d205-census-a21/) and the parity backfill in its `parity-gap/` folder.

## Verdict

**CORRECT WITH GAPS.** The two stated claims hold as computed:

- At exact area 21, W ≤ 20, all 1,604,242,406 unordered pairs of distinct interior lattice points in 538,025,823 canonical rooms are lit.
- At exact areas 17–20, all 726,251,893 different-parity pairs are lit.

I found no bug. The gaps are about how much the evidence proves, not about wrong numbers:

1. The per-shard EXPECT = SHOT reconciliation is weaker than the status note implies (see check 3).
2. Room-count completeness at area 21 has no external reference count. It rests on indirect evidence.
3. The combined figure of 2,471,412,511 pairs through area 21 reuses d9 same-parity and Part A results, which this review didn't re-examine.

## Check 1 · Lit criterion

**Result: sound.** A pair is marked lit only when `verify_plane.c` accepts a certificate. A rejected certificate calls `abort()`, which fails the shard.

Code reading of `verify_plane.c`:

- It requires the source to be an interior lattice point, meaning all four cells are present.
- Within one lattice step of a primitive direction (p, q), all grid-line crossings fall at non-lattice points, because gcd(p, q) = 1. A crossing into an absent cell reflects one velocity component, which is a reflection off a wall interior.
- At every lattice point it reaches, it rejects corners (1 or 3 cells), pinches and empty points. It passes straight through interior points (4 cells). It reflects at flat wall points (2 adjacent cells), which are smooth boundary points.
- For axis directions, it allows only perpendicular bounces off a flat wall. It rejects grazing.
- The path stays inside closed cells, and both convex and reflex vertices are excluded.

In `shoot.c`, the pair (a, b) leaves `pending` only after `verify_plane` returns 1. Any pair left in `pending` is written to `.sv` as a survivor. All 84 `.sv` files and `.err` files are empty, and `survivors = 0` in every shard.

Differential test (`fuzz_verify.py`): I compared production `verify_plane.c` with my tracer on random strictly simple rooms of area 6–11 and on the 22-wall control. Each test uses a random interior source, a primitive direction with p + q ≤ 8, a random step count m and every interior target.

| Run | Rays | Rays hitting a corner | Queries | Accepted | Mismatches |
|---|---:|---:|---:|---:|---:|
| m ≤ 6 | 20,000 | 15,756 | 23,759 | 840 | 0 |
| m ≤ 30 | 6,000 | 5,365 | 7,108 | 128 | 0 |

Hand-made near-dark cases (`adversarial.py`, `adversarial.json`). Both implementations agree on all six:

- In a 4×4 L-room, the straight segment (3,1)→(1,3) passes through the reflex corner (2,2). Both directions are rejected.
- In a 3×3 square, diagonals that run into a convex corner and fold back onto a mark are rejected.
- A legitimate one-step diagonal and a perpendicular axis bounce off a flat wall are accepted.

Control: the 22-wall, area-15 room has cells (0,2) (0,3) (1,1) (1,2) (1,3) (1,4) (2,0) (2,1) (2,4) (2,5) (3,4) (3,5) (4,3) (4,4) (5,3). My code confirms the following:

- The room has 22 walls, no hole and no pinch.
- Its only interior lattice points are (1,3) and (3,5). The pair is therefore the room's only pair, and it matches d29's recorded DARK pair.
- `verify_plane` rejects all 235,200 queries over every primitive direction with p + q ≤ 40 (1,960 signed directions), both orientations and m = 1–60.
- My tracer reaches neither endpoint from the other before a corner along any of those 3,920 rays, out to time 60.
- `validate.py` previously showed that the production shooter leaves exactly this pair as a survivor, and that both orbit implementations exhaust 2,592 states and return DARK.

The control is the real dark pair, and it isn't lit.

## Check 2 · Independence

**Witness replay: 3,985 of 3,985 pass.**

- I rebuilt the census from the d205 sources with my own `cc -O2` build. The only change was a side channel that writes about 1 in 16,384 lit certificates to a file (`shoot_witness.c`; the diff touches nothing else).
- I reran shards 17, 83 and 42, which took 25.0, 26.8 and 25.4 user-seconds. All three `.counts` files are byte-identical to the sealed SHA-256 values in `done.json`.
- `tracer.py` shares no code or method with the production path. It turns the room into maximal wall segments and moves a ray with Fraction position and integer velocity from wall hit to wall hit. Any contact with a wall endpoint ends the path, and every leg is checked to stay in the closed room.

Every one of the 3,985 sampled certificates satisfies all of the following:

- My tracer reaches the target at time exactly m, the first arrival, with no corner contact.
- Both endpoints are interior lattice points.
- The room has area 21 and no hole or pinch under my own filters.
- The room has W ≤ 20 under my own wall count.
- The room is minimal under an independent implementation of d205's 8-symmetry key (3,981 distinct rooms).

The sample has 1,301, 1,471 and 1,213 certificates per shard. It includes 1,849 axis-direction paths, a maximum p + q of 18 and a maximum m of 11.

**Small-area room counts: exact match.** `rooms.py` grows free polyominoes by set extension, not Redelmeier. It detects holes by flood fill and counts walls as maximal collinear runs of boundary edges, not by corner parity.

- Free polyomino counts for areas 1–10 match A000105.
- Through area 11, all 57 (area, W) buckets match d205 `validation/optimized.counts` and d9 Part A: 22,292 rooms, 225 same-parity pairs and 3,483 different-parity pairs. The match covers room counts, EXPECT and SHOT (`compare_small.py`).

## Check 3 · Completeness

**Enumerator filters (code reading): correct.**

- **Vertex masks.** Bit 8 is the cell up and right of a lattice point, 4 up and left, 2 down and right, and 1 down and left. Pinch masks 6 and 9 are exactly the two diagonal pairs.
- **Corners and walls.** Odd popcount (1 or 3 cells) marks a corner. With no pinch, W equals the number of corners, which equals the number of maximal edges.
- **Euler increment.** The update is new vertices − 3 + shared sides. A connected, pinch-free union is a disc exactly when χ = 1.
- **Marks.** Only mask 15 counts as a mark. Points on smooth walls (two adjacent cells) and reflex vertices are not marks.
- **Canonical key.** The key orders (w, h, rows). The early exit `row[0] > row[ymax]` is the t = 2 comparison, and transposes are tested only when w = h. My minimality check on 3,981 sampled rooms found no non-minimal key.
- **Traversal coverage.** The per-size fixed-node totals for 1–21 equal A001168 exactly, including 88,983,512,783 at area 21. Only shard 0 counts nodes of size 10 or less. Larger nodes are split disjointly by their size-11 ancestor.
- **Area 20 cross-check.** At area 20, the incremental-mask code reproduces d9's archived counts, which d9 computed from full masks, in all nine W buckets (247,523,973 rooms).

**Reconciliation in `report.py` and `batch.py`: valid but weaker than described.**

- EXPECT is C(marks, 2) from the enumerator's vertex masks.
- SHOT same + different counts every pair in the shooter's double loop, not lit pairs. Its mark set is rebuilt from row masks, and `shoot_room` aborts if the two mark counts differ.
- Equality therefore proves two things: every eligible room reached the shooter, and the two mark definitions agree. That second point is a real cross-check.
- Equality does not count lit pairs independently. The "all lit" conclusion follows from the code structure: a verified hit or a survivor line for every pair, and zero survivors.

I re-aggregated all 84 sealed shards from scratch (`checks.py`, `checks.json`). The results are 538,025,823 rooms, 271,308,782 same-parity pairs, 1,332,933,624 different-parity pairs, a total of 1,604,242,406 pairs, and 0 survivors. These agree with `totals.json`. Each shard's counts hash, its per-W EXPECT = SHOT, and its eligible = SHOT room count all hold.

## Check 4 · Parity backfill

**Result: confirmed.** `parity-gap` differs from the production code only in two places. Its enumerator emits a room only when it has a cross-class pair, and its shooter queues only different-parity pairs. The plane verifier is identical.

| Area | Shards | Rooms (= d9 archive per W) | Different-parity pairs lit | Survivors |
|---:|---:|---:|---:|---:|
| 17 | 7 | 17,411,314 | 15,736,503 | 0 |
| 18 | 14 | 44,765,205 | 53,457,288 | 0 |
| 19 | 21 | 108,242,515 | 167,782,890 | 0 |
| 20 | 42 | 247,523,973 | 489,275,212 | 0 |
| **Total** | | | **726,251,893** | 0 |

- At area 20, d9 same-parity (93,566,285) plus backfill different-parity (489,275,212) equals the all-pair EXPECT from validation (582,841,497) in every W bucket.
- I rebuilt the parity-gap binary from source and reran all 7 area-17 shards and area-20 shard 7. All 8 counts files are byte-identical to the sealed hashes.

## Check 5 · Scope

The census covers the following:

- **Rooms.** Strictly simple polyomino rooms: connected, no holes, no pinch points, closed region, walls are maximal boundary edges. Rooms are taken up to translation and the 8 lattice symmetries.
- **Walls.** W ≤ 20.
- **Areas.** Exact area 21 for all pairs. Exact areas 17–20 for different-parity pairs only.
- **Points.** Pairs of distinct interior lattice points only, meaning all four surrounding cells are in the room. "Same parity" means both coordinates have the same parity.
- **Paths.** Billiard paths that avoid every vertex, both convex and reflex. Reflections at lattice points on flat walls are allowed.

The census doesn't cover the following:

- Lattice points on smooth walls or at reflex corners.
- Non-lattice points.
- Rooms with W ≥ 22 at any area.
- Exact area 22 or larger.
- 45-degree walls, pinched rooms and rooms with holes.
- Same-parity pairs at areas 17–20. Those rely on d9's phase-one shooting (`lit_by_shooting = pairs`), which this review didn't audit.
- Different-parity pairs through area 16. Those rely on d9 Part A, also not audited here.

The combined 2,471,412,511 figure is correct arithmetic over those sources. Only its area-21 and different-parity 17–20 components were reviewed here.

## Compute and files

I used about 3 CPU-minutes, all single-process at nice 10. Shard reruns took 77 seconds, parity reruns about 37 seconds, and the Python checks about 20 seconds.

| File | Purpose |
|---|---|
| `rooms.py` | Independent small-area room enumerator. |
| `compare_small.py` | Compares `rooms.py` output with the run's small-area counts and d9 Part A. |
| `tracer.py` | Exact Fraction tracer. |
| `replay.py` | Replays sampled witnesses with `tracer.py`. |
| `fuzz_verify.py`, `vp_harness.c` | Differential test of `verify_plane.c` against `tracer.py`. |
| `adversarial.py` | Hand-made near-dark cases and the 22-wall control. |
| `checks.py` | Re-aggregates the sealed shard outputs. |
| `shoot_witness.c` | Witness side-channel copy of `shoot.c`. |
| `rerun/`, `rerun-pg/` | Regenerated shard outputs and witness samples. |
| `*.json` | Recorded outputs of the scripts above. |

I deleted the compiled binaries. To rerun the checks, rebuild them first:

- `cc -O2 -o vp_harness vp_harness.c verify_plane.c`
- `cc -O2 -o census_w enum_rooms.c shoot_witness.c verify_plane.c`
