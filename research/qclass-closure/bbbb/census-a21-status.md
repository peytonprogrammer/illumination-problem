Advances: L2 — exact area 21, strictly simple orthogonal lattice rooms, W ≤ 20, all unordered distinct interior lattice pairs.

**Validation passed, 2026-11-23 HST.** All nine area-20 wall buckets matched the archived 247,523,973 rooms and all fixed-node counts matched. The small run matched 57 Part A (area,W) buckets through area 11, covering 22,292 rooms, 225 same-parity and 3,483 different-parity pairs. The known 22-wall control survived shooting. The C and Python modular orbits each exhausted 2,592 states and found the same DARK pair. The area-20 job counted rooms only.

At launch the area-21 run used 84 disjoint Redelmeier shards, one nice-10 supervisor and up to seven single-process workers, each with shooting and independent plane replay. Results are recorded in [d205](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d205-census-a21/). Historical different-parity coverage at 17–20 remains open.

**[done] Area 21 completed on 2026-11-23 at 13:20 HST.** All 84 shards completed and reconciled. The generator visited 88,983,512,783 fixed polyominoes of exact area 21 and retained 538,025,823 canonical strictly simple rooms with W ≤ 20. Of those, 364,183,172 had at least two interior lattice marks. The shooter found paths for all 271,308,782 same-parity and 1,332,933,624 different-parity pairs, totaling **1,604,242,406 lit pairs**. Every certificate passed independent plane replay. Zero pairs went to orbit fallback. Each shard's expected pair count was calculated independently from its vertex masks and reconciled by wall bucket. Full counts, manifest hashes and per-shard records are in [totals.json](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d205-census-a21/a21/totals.json) and [the run directory](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d205-census-a21/a21/).

**Timing and area-22 forecast.** Production used 3,535.82 worker CPU seconds and 554.42 seconds elapsed (58.93 CPU minutes, 9.24 wall minutes). Per-shard CPU was 21.12 / 43.25 / 67.46 seconds minimum / median / maximum. Largest worker peak RSS was 2,064,384 bytes. Validation counted exact-area-20 rooms in 357.80 CPU seconds. The observed root-to-limit node ratio was 3.871 from 20 to 21, the canonical room ratio 2.174 and the candidate pair ratio 2.752. Scaling validation CPU by the node ratio attributes about 1,385 seconds of the area-21 CPU to counting, leaving 2,151 seconds for pair work. Applying the node ratio to counting and the pair ratio to pair work once more gives **3.13 CPU hours or about 29.5 elapsed minutes** at the measured occupancy. Scaling the whole workload by the room or node ratio instead gives 2.13–3.80 CPU hours (about 20–36 minutes). These are scenarios; a hard orbit survivor or different machine load can increase elapsed time. Area 22 was not run.

**First open L2 case.** For a contiguous all-parity census, the earliest gap in the audited record is different-parity pairs at exact area 17 (also 18–20). The next new area is 22, for both parities. Area 21 is complete independently of that gap. [Parity audit](census-parity-audit.md)

## Different-parity backfill

The parity-only filter reproduced all 3,483 different-parity pairs through area 11 with zero same-parity tests. The control-validated orbit binary and independent plane replay are unchanged. Each row below was added after its shards reconciled against the archived room counts by wall count.

| Exact area | Canonical rooms | Rooms with different-parity pairs | Different-parity pairs lit | Orbit referrals | DARK | Worker CPU seconds |
|---:|---:|---:|---:|---:|---:|---:|
| 17 | 17,411,314 | 7,289,100 | 15,736,503 | 0 | 0 | 15.74 |
| 18 | 44,765,205 | 21,779,366 | 53,457,288 | 0 | 0 | 53.41 |
| 19 | 108,242,515 | 59,561,890 | 167,782,890 | 0 | 0 | 227.70 |
| 20 | 247,523,973 | 150,544,791 | 489,275,212 | 0 | 0 | 884.60 |

## Contiguous L2 coverage

[done] All 726,251,893 different-parity pairs at exact areas 17–20 passed. Area 20 also reconciled by wall bucket against the independent all-pair counts from validation after adding the historical same-parity totals. After area 20 we rechecked all 84 area-21 shard seals and totals; its completed all-pair result was reused. Combining the disjoint classes in [the backfill summary](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d205-census-a21/parity-gap/summary.json) certifies **2,471,412,511 lit interior lattice pairs through area 21** for strictly simple orthogonal lattice rooms with W ≤ 20. The first open area for L2 is **22**.
