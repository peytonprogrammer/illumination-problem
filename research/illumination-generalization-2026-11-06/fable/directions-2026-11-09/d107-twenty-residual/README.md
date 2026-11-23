# D107: residual boxes and bin-pair certificates at 20 walls

**Verdict: confirmed with gaps.** Gaps 1 and 2 of [d103](../d103-twenty-check/README.md) are closed or narrowed:

- **Bin-pair rooms:** all three are checked in full. That's 295,323 bin-pair receipts with 0 failures.
- **Shear-box rooms:** 11 of the 24 have an independently re-derived residual. Each matches the saved boxes, and every residual product lies inside a box.

Task 3 wasn't attempted: the CPU cap ran out first.

Brief: row Q50 in `../d95-review-queue/review-queue.md`. Sources are `qclass-closure/twenty/method.md` and the saved archive `twenty/data/twenty-wall.tar.gz` (SHA-256 checked by `run.sh`).

## Re-run

```
bash run.sh
```

It needs about 4 CPU-minutes and leaves `compare.log`, `pixchk.log` and `control.log`. `KEEP=1` keeps `work/`. `cert2.log` is a transcript of the original run: per-room CPU, open tile pairs, and pairs that skipped directions at the piece cap.

## Files

| File | Role |
|---|---|
| `cert2.cpp` | Copy of [d100](../d100-check-residual/README.md)'s tile-pair certifier: d74 core plus d100's two-sided driver, B = 18, cap 20,000. |
| `compare.py` | Compares one room's cert2 residual with its saved `boxes`, in exact arithmetic. |
| `pixchk.py` | Independently replays one bin-pair room's receipts. It writes label queries for `labchk` and a synthetic directory for d103's `shear_check.py`. |
| `labchk.cpp` | d103 `leafchk.cpp`'s surface model verbatim (cylinders, criticality, half-turn orbits), with a new `main()` that checks exact strip intervals. |
| `bincov.py` | Checks that cert2's residual for a bin-pair room lies in the saved bin-pair list. |

## Task 1: residual boxes

**Method.** This is d100's method, unchanged. cert2 runs over every unordered tile pair with directions up to 18. It doesn't read census code or census output. `compare.py` then reads the saved `boxes` only as the object under test. It checks three things:

- The open tile pairs equal the boxes' tile pairs.
- Every product f × W lies in its closed tiles.
- Some box covers every product. All vertices at each end must lie within r/65536, in the max norm, of that box's corner. Corner k is (x + (k & 1), y + (k >> 1)), as in d103.

| Room | Boxes | Open pairs equal | Products | Uncovered | cert2 CPU-s |
|---|---:|---|---:|---:|---:|
| 0-10 | 16 | yes | 167,932 | 0 | 61.5 |
| 6-12 | 16 | yes | 152,316 | 0 | 26.4 |
| 7-15 | 16 | yes | 29,504 | 0 | 23.8 |
| 0-32 | 2 | yes | 30,464 | 0 | 9.5 |
| 1-170 | 2 | yes | 5,664 | 0 | 4.8 |
| 1-47 | 2 | yes | 26,296 | 0 | 9.6 |
| 2-269 | 2 | yes | 42,600 | 0 | 18.2 |
| 7-242 | 2 | yes | 41,956 | 0 | 19.8 |
| 7-244 | 2 | yes | 3,856 | 0 | 2.4 |
| 8-243 | 2 | yes | 7,464 | 0 | 2.8 |
| 9-41 | 2 | yes | 8,392 | 0 | 7.3 |

These 11 rooms hold 64 of the 458 shear boxes. Every saved box is needed by some product.

In 9 rooms the reached displacement rounds up to exactly the saved radius, for example 1/17 → 3856 and 1/15 → 4370. In 2-269 the saved radius is 8739, about 2/15, but cert2 reaches only 2/17, so the box has slack. In 2-269 and 7-242 cert2 skipped 61 and 86 directions at the piece cap. Skipping is sound, and the residual still fits.

**Not done (13 rooms, 394 boxes):** 1-244, 2-300, 4-244, 4-49, 5-252, 6-213, 6-219, 7-234, 7-241, 8-220, 8-239, 8-240, 9-240. Room 4-49 was started and stopped by hand after about 295 CPU-s, during tile pair 11–16. Its tile pair 4–16 alone took 244 s and skipped 61 directions. It also has many 1 × 1 live pairs, which are interior lattice points. cert2 can't resolve lattice points, and the census sends them to the lattice path census. Most of the other 12 rooms have 32 or more boxes. At the observed 2–4 CPU-s per open pair, they'd need roughly 15–25 CPU-minutes.

## Task 2: bin-pair rooms

The bin-pair rooms are `hard/5-0` (the pinwheel, 99 boxes), `hard/2-266` (54 boxes) and `hard/7-230` (9 boxes), 162 boxes in total. d103's `shear.log` lists them as pixel-finished.

**What method.md claims.** Each surviving tile pair is cut into 16 × 16 bins per tile, and the bins are treated as closed. Every reciprocal bin pair is closed by one of four leaf types:

- A fixed cylinder direction pulled back through a shear.
- An explicit reflected path that holds on the whole box.
- A shear about rational reference heights, with a phase rectangle tree. The leaf must also show that A > 0.
- A corner neighborhood of radius 1/64, handed to the corner shear trees.

**Method.** `pixchk.py` was written from method.md and the receipt grammar. It doesn't run or import census code. It does these steps itself:

- It replays every split.
- It recomputes the period, the shear multiple M = L · lcm(denominators), and the A > 0 test.
- It derives which sign and dominance cases are possible.
- It sets the phase root rectangle, [U/8, max(U/4, M·A_max)] × [0, same].
- It computes each leaf's four strip intervals exactly.

d103's independent surface model, in `labchk`, then checks the labels. Explicit paths are checked over the whole box with D107's own crossing-order search. That search evaluates the multilinear orientation determinant at the 16 box vertices. At ties it branches and requires a physical vertex that isn't a corner. Every branch must end at the target sheet. The 4 corner neighborhoods go through d103's `shear_check.py` and `leafchk`.

| Room | Bin pairs (= grid PIX set) | Label queries (L + K) | Failed | Explicit paths | Failed | Corner trees |
|---|---:|---:|---:|---:|---:|---|
| 7-230 | 9,396 | 11,681 | 0 | 0 | 0 | none |
| 2-266 | 104,769 | 105,913 | 0 | 100 | 0 | none |
| 5-0 | 181,158 | 612,868 | 0 | 15,106 | 0 | 4 boxes, 32 trees, 6,452 leaves, 0 failed |

The record counts for 5-0 equal those in `pinwheel-audit.txt`, and the counts at the end of method.md: 15,106 explicit paths, 10,094 rational-shear calls, 32 trees and 6,452 leaves. The I keys are distinct, and each room's set equals its grid's PIX set. The corner neighborhoods equal `near/boxes`.

**Bin coverage.** For 7-230 alone, cert2 also re-derived which bin pairs need certificates. It leaves **no** open tile pair at B = 18, because tile pair 14–20 empties after 69 directions. The census kept 9,396 bin pairs, so the saved certificates are more than needed. A likely cause is the census grid run's lower piece cap (6,000 against 20,000), but this check didn't confirm that. 5-0 and 2-266 weren't re-derived. For those two rooms, the bin-pair list itself still comes from the census `grid` run.

## Negative controls

See `control.log`. All three fail as intended.

1. **Residual:** room 0-32 with its boxes shrunk from 4370 to 3856. 3,800 of 30,464 products are uncovered.
2. **Labels:** 7-230 receipts with j → j + 1 in every L and K leaf. 11,606 of 11,681 queries fail.
3. **Corner trees:** 5-0 corner trees with j → j + 1. 5,086 of 6,452 leaves fail.

## Task 3: tile-level sample rooms

Not attempted. The CPU cap ran out after task 1 and task 2. The timed-out rooms in `../d103-twenty-check/whole-twenty.log` remain undecided.

## Gaps

1. 13 shear-box rooms, with 394 boxes, have no independent residual. Room 4-49 is the costly one.
2. For 5-0 and 2-266, the bin-pair list isn't re-derived. The certificates for every listed pair are checked.
3. The label model is d103's, reused here. Its own controls validated it, but it isn't a third derivation. The soundness of cert2 and the shear lemma rests on d13's Lemma A′, as in d100.
4. pixchk's receipt parser must follow the census's tree order to read the receipts. The logic it checks is reimplemented.

## CPU

About 530 CPU-s, or 8.8 CPU-minutes, in total:

- cert2: 489 s, including 295 s on the abandoned 4-49 run.
- Receipt replay and label checks: about 15 s.
- Comparisons: about 20 s.
- Builds: about 6 s.

A clean `run.sh` skips 4-49 and needs about 4 CPU-minutes.
