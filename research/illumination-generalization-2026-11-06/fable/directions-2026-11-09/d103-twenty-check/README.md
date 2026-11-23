# D103: independent check of the 20-wall and below-18 Q-class real-mark runs

**Verdict: confirmed with gaps.** Every one of the 3,652 shear trees at 20 walls holds under D103's own root boxes and cylinder model, and every sampled whole-room room re-certifies with independent code. The gaps are in what this check couldn't re-derive: the three pixel-finished rooms, the tile-level residual boxes, and part of the tile-level sample.

Brief: row Q06 in `../d95-review-queue/review-queue.md`. Sources: `qclass-closure/twenty/README.md`, `method.md`, and the saved archives in `twenty/data/` (SHA-256 sums match).

## Re-run

```
bash run.sh > run.log 2>&1
```

It needs about 7 CPU-minutes, most of it in step 5. It re-extracts the archives into `work/`, which you can delete afterwards.

## Files

| File | Role |
|---|---|
| `sample.py` | Reconciles each archive shard stage by stage, then draws fixed-seed samples (seed 103). |
| `shear_check.py` | Derives each tree's root box from the method, replays every bisection, checks `E` leaves, and emits `W` leaves. Never reads the author's root boxes or `END` status. |
| `leafchk.cpp` | D103's exact leaf checker. It has its own square-tiled surface, leaf-following criticality, union-find cylinders and half-turn orbits, with int128 interval arithmetic. d90's `surface.py` was the template. |
| `tracer.py` | D103's exact rational billiard tracer and image search. |
| `whole.py` | Runs the d74 certifier (`../d74-continuum-check/cert.cpp`, not the author's `cover.c`) at B = 6, 10, 14, 18, then traces each leftover point pair with `tracer.py`. |
| `control.py` | Negative control on the 22-wall room. |
| `shear.log`, `whole-lower.log`, `whole-twenty.log`, `control.log` | Logs. `shear.log` is transcribed from the run. |

## Results

| Check | Claim | D103 |
|---|---|---|
| Stage counts at 20 walls | a 619,223, b 269,168, c 22,401, d 1,936, tile-level 894 | Same, from the archive |
| Stage counts below 18 | 26,706 rooms, 19 tile-level | Same |
| Shear trees, 20 walls | 620 boxes, 3,652 trees, 246,639 leaves | 3,652 trees and 246,639 `W` leaves pass, 0 fail. They cover 458 boxes in 24 rooms. The other 162 boxes are in 3 pixel-finished rooms. |
| Shear trees, below 18 | 194 boxes, 122,865 leaves | 122,865 leaves pass, 0 fail |
| Mutation control (j → j+1) | none | 232,884 of 246,639 leaves rejected |
| Whole-room sample, 20 walls | 912,728 clear | 300 of 300 clear (210 a, 81 b, 8 c, 1 d); 613 leftover point pairs traced, 0 without a path |
| Below-18 sample | 26,706 clear | 200 of 200 clear; 113 point pairs traced, 0 without a path |
| Tile-level sample, 20 walls | 894 clear | 46 of 100 clear outright. 13 hit the 15-s cap (undecided, not failed). 4 have boxes and were skipped. 37 weren't reached before the CPU cap. |
| R22 control | dark pair kept | d74 leaves exactly (1,3)–(3,5); the tracer finds no path at image radius 6 |

## Method read

- **Shear coverage is sound.** D103 re-derived the label formula. In the fixed-phase mode (K = 1), the transverse coefficient is p + jqL; otherwise it's p, plus a phase term qj. Variable mode with K = max(1, ⌈1/(8LA)⌉) covers A ≤ min(r, ⌈U/(8L)⌉)/U. Fixed mode covers A ≥ ⌊U/(8L)⌋/U, so the two ranges overlap. When r is below that cap, there's no fixed tree, and variable mode with K = 1 covers the rest, because the phase top is max(1/4, L·r). `method.md` doesn't say this last case explicitly.
- **Half-turn (the d90 gap 1).** `method.md` now says that labels live on the quotient and that the shear commutes with the half-turn. D103 compares half-turn orbits, which is sound.
- **Single-axis boxes.** Three boxes use one axis only. Each has a wall through a center perpendicular to that axis, so A_t > 0. D103 checked this itself.
- **Lattice case.** No box has two distinct regular interior centers, so no shear box needs a census path.

## Gaps

1. **Three rooms aren't covered by the trees.** The pinwheel (`hard/5-0`) and the two 24-square rooms (`hard/2-266`, `hard/7-230`) hold 162 of the 620 boxes. They're finished by `pixel_finish.py` bin-pair certificates: explicit reflected paths and rational-height shears. D103 didn't check these. The claim's breakdown ("620 boxes and 3,652 trees") doesn't show this.
2. **The residual boxes aren't re-derived.** The boxes come from the author's `tile.c`. The d74 certifier doesn't localize the residue: for `hard/7-242`, B = 18 leaves 209,900 pieces after 67 CPU-s. This is d90's gap 2 at 20 walls.
3. **The tile-level sample is incomplete.** Only 46 of 100 rooms were independently cleared.
4. **No concrete paths through shear leaves.** The fixed-phase mode, which is new since d90, has no traced end-to-end path.
5. **Shared theory.** The author's solver and d74 both rest on d13's Lemma A′ and Theorem C(2), which are unreviewed.
6. **Lattice residuals.** The author matches lattice residuals to the earlier census (`witnesses.txt.gz`). D103 instead traced the 726 sampled point pairs directly, so this check covers the sample only.

## CPU

About 9.7 CPU-minutes (≈580 s), estimated from per-command `time` output: about 395 s in the twenty-sample run (168 s in d74 on finished rooms, 13 × 15 s timeouts, about 31 s Python), about 150 s probing d74 on box rooms, about 20 s on shear trees and controls, and about 15 s on sampling, builds and the lower sample. The twenty-sample run was stopped at the cap.
