# D177: shear-box residual for the rooms d107 left undone

## Bottom line

> **Update from the 2-300 follow-up (see the last section):** with no piece cap, cert2 skips 0 directions on all 16 saved tile pairs of 2-300. Every residual product, 1,550,080 in total, lies inside a saved box. The largest displacement is 2/17, inside the saved radius of 1/8. **The 2-300 FAIL below came from the cap, so it isn't a gap in the corner-only closure.** 2-300 still isn't fully confirmed: 273 of its 512 tile pairs that have no box weren't re-run.

- **6 of the 13 rooms are now confirmed:** 1-244, 5-252, 6-213, 6-219, 7-234 and 8-220. Each room's open tile pairs equal its saved boxes' tile pairs. Every residual product lies in a saved box. No direction was skipped.
- **FAIL under the brief's rule, in room 2-300.** cert2 timed out after 9 of the 16 open tile pairs. In 3 of those 9 pairs, 78,408 residual products lie outside every saved box. These are pairs 7–15 (39,648 of 39,648), 8–15 (20,010 of 39,828) and 8–19 (18,750 of 39,716).
- **The 2-300 FAIL is probably a cert2 artifact, but this run doesn't prove that.** In every 2-300 pair, cert2 hit its 20,000-piece cap and skipped 41 to 73 directions, 506 in total. Skipping keeps extra pieces alive, so cert2's residual is a superset of the true one. The uncovered products sit at the saved box's own corner pair. They reach 1/7 or 2/15 against a saved radius of 1/8. 2-300 isn't confirmed, and the FAIL stays open until a run with fewer skips settles it.
- Not run: 8-239, 8-240, 9-240, 7-241 and 4-244 ran out of budget. 4-49 was skipped by the brief.
- **Budget overrun.** The cert2 and compare runs used 556 CPU-s, logged in `cpu.log`. The 2-300 partial-pair checks added about 35 to 245 CPU-s that I didn't measure, most of it from a quadratic `awk`. The total is about 590 to 800 CPU-s, so it may exceed the 600 CPU-s cap. `run.sh` now uses a linear `head` instead of that `awk`.

## Method

The procedure is d107's task 1, unchanged. `cert2.cpp` and `compare.py` are byte copies from `../d107-twenty-residual/`. cert2 is built with `c++ -std=c++17 -O2` and run as `cert2 room 0 18 20000` (B = 18, cap 20,000). `compare.py` checks three things in exact arithmetic:

- The open tile pairs equal the boxes' tile pairs.
- Every product lies in its closed tiles.
- Some box covers every product, at max-norm radius r/65536 from its corner pair.

Rooms run in order of saved box count, fewest first, with ties broken by name. Each cert2 run is wrapped in `ulimit -t` and `timeout`, with a cap of min(200, remaining budget − 15) CPU-s.

I added two things for the timed-out room, and neither one searches anything new:

- The partial check cuts cert2's output after its last complete `PAIR` line, then compares only the finished pairs. cert2 prints each pair's `PROD` lines before its `PAIR` line, so every finished pair is complete.
- `nearest.py` reads the first 3,000 products of each finished pair. It reports the nearest corner pair and the largest exact displacement.

## Per-room results

| Room | Saved boxes | Open (live) pairs | Residual products | Outside every box | Skipped dirs | cert2 CPU-s | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| 2-300 | 16 | 9 of 16 finished | 354,270 (partial) | **78,408** | 506 | 200.1 (timeout) | **FAIL (partial, likely cap artifact)** |
| 1-244 | 32 | 32 | 85,744 | 0 | 0 | 28.4 | PASS |
| 5-252 | 32 | 32 | 144,702 | 0 | 0 | 71.0 | PASS |
| 6-213 | 32 | 32 | 99,860 | 0 | 0 | 62.0 | PASS |
| 6-219 | 32 | 32 | 116,404 | 0 | 0 | 66.2 | PASS |
| 7-234 | 32 | 32 | 77,792 | 0 | 0 | 40.2 | PASS |
| 8-220 | 32 | 32 | 109,868 | 0 | 0 | 76.3 | PASS |
| 8-239 | 32 | — | — | — | — | — | not run (budget) |
| 8-240 | 32 | — | — | — | — | — | not run (budget) |
| 9-240 | 32 | — | — | — | — | — | not run (budget) |
| 7-241 | 40 | — | — | — | — | — | not run (budget) |
| 4-244 | 48 | — | — | — | — | — | not run (budget) |
| 4-49 | 2 | — | — | — | — | — | skipped (brief) |

The compare steps took 1.3 to 2.4 CPU-s per room. In all 6 passing rooms, every saved box is needed. Every radius is 3856, which equals ceil(65536 × reached displacement), and the reached displacement is 1/17.

### Room 2-300 in detail

The saved boxes have r = 8192 (1/8), except 0–8 and 20–28, which have r = 7711. cert2 reached these displacements at each box's corner pair (`nearest.log`):

| Pair | Products | Uncovered | Skipped dirs | Reached | Saved r |
|---|---:|---:|---:|---|---|
| 0–7 | 39,796 | 0 | 55 | 1/8 | 1/8 |
| 0–8 | 39,924 | 0 | 62 | 2/17 | 7711 |
| 0–20 | 38,412 | 0 | 41 | 1/8 | 1/8 |
| 0–27 | 39,702 | 0 | 53 | 2/17 | 1/8 |
| 7–15 | 39,648 | **39,648** | 73 | **1/7** | 1/8 |
| 7–19 | 37,542 | 0 | 51 | 2/17 | 1/8 |
| 7–28 | 39,702 | 0 | 53 | 1/8 | 1/8 |
| 8–15 | 39,828 | **20,010** | 60 | **2/15** | 1/8 |
| 8–19 | 39,716 | **18,750** | 58 | **1/7** | 1/8 |

Pairs 8–28, 15–20, 15–27, 19–20, 19–27, 20–28 and 27–28 didn't finish. Every finished pair skipped directions and ended with about 20,000 live pieces per side, at the cap. In d107, room 2-269 also skipped directions, but its residual still fit. Here it doesn't.

## Side finding: a latent bug in d107's compare.py

Line 88 of `compare.py` reads `unused = [k for ... if ... not in reach]`, and `k` is undefined. The line crashes only if some box is never reached. That happens after the uncovered count prints and before the `RESULT` line. A passing room never hits this line, so the PASS results in d107 and here are unaffected. d107's negative control 1 also hits it, so that control finishes on an error instead of printing `RESULT ... FAIL`. I didn't fix the copy, because the brief says to reuse d107's code. `run.sh` tolerates the crash with `|| true` on the partial step only.

## What remains

1. **Settle 2-300.** Rerun cert2 on the 16 saved tile pairs with a larger piece cap, so fewer directions are skipped. Or compare against the census's own 2-300 residual and the cap it used. If products still reach 1/7 with no skips, the saved 1/8 boxes don't cover the residual, and the corner-only closure has a real gap in 2-300. A complete run may need well over 200 CPU-s.
2. **Run the 5 unrun rooms:** 8-239, 8-240 and 9-240 have 32 boxes each, 7-241 has 40 and 4-244 has 48. The 32-box rooms took 28 to 76 CPU-s each here, so these 5 need about 5 to 8 CPU-minutes.
3. **4-49** is still open, as in d107.

## Files

- `run.sh` reproduces the whole run: checksums, extraction, build, the per-room loop, and the partial step for timed-out rooms. It writes only here. `KEEP=1` keeps `work/`. A clean run needs about 10 to 11 CPU-minutes.
- `cert2.cpp` and `compare.py` are d107's copies.
- `nearest.py` is new. It reports the nearest corner pair and the largest displacement for one tile pair.
- `cert2.log` holds every room's PAIR and DONE lines. `compare.log` holds the full-room comparisons. `cpu.log` holds per-room CPU and status. `partial.log` and `nearest.log` hold the 2-300 partial check.

## 2-300 follow-up

**Answer:** none of 2-300's products lies outside every saved box once no direction is skipped. I re-ran all 16 saved tile pairs, and the uncovered products disappear in every one. The 78,408 uncovered products in the main run came from cert2's 20,000-piece cap.

### Census parameters

The census ran `tile 18 1 6000` with `COVER_ALLDIRS=1`, per `qclass-closure/twenty/tiles.py`. That's B = 18 and FORCE = 1. MAXLIVE = 6000 counts both sides together. The `tile` program comes from d13's `cover.c` through `offgrid/build_skip.py` and `build_pairskip.py`. It also skips directions on its own:

- It skips a direction if the new live count exceeds 2 × MAXLIVE.
- It skips a direction if the count after pruning exceeds MAXLIVE.
- It skips a direction if the count was over 300 and more than triples.

The census's 6,000 cap is lower than cert2's 20,000, so I removed the cap instead: cap = 10^9. The census's own residual for these pairs was about 1,400 to 1,550 live pieces (`ROOM ... RESID` lines in `hard/2-300/tiles`).

### Method

`cert2pair.cpp` is `cert2.cpp` with 2 added lines. Two optional arguments, `A B`, restrict the run to one tile pair. Pairs are independent in cert2, so the per-pair output is unchanged.

As a control, the patched binary at cap 20,000 on pair 7–15 reproduces the main run's line exactly: `live 19894 19754 prods 39648 dirs_used 128 skipped 73`. It also reproduces the 39,648 uncovered products.

Each run used `ulimit -t` and `timeout`, with a 600 CPU-s follow-up budget. Then `compare.py` and `nearest.py` read every product.

### Results, cap 10^9

| Pair | Live pieces | Products | Skipped dirs | Outside every box | Max displacement | Saved r | cert2 CPU-s |
|---|---:|---:|---:|---:|---|---|---:|
| **7–15** | 43,252 + 52,474 | 95,726 | 0 | 0 (was 39,648) | 2/17 | 1/8 | 23.0 |
| **8–15** | 44,842 + 51,426 | 96,268 | 0 | 0 (was 20,010) | 2/17 | 1/8 | 33.5 |
| **8–19** | 45,182 + 57,836 | 103,018 | 0 | 0 (was 18,750) | 2/17 | 1/8 | 40.9 |
| 0–7 | | 98,016 | 0 | 0 | 2/17 | 1/8 | 22.5 |
| 0–8 | | 95,380 | 0 | 0 | 2/17 | 7711 | 42.5 |
| 0–20 | | 92,696 | 0 | 0 | 2/17 | 1/8 | 20.3 |
| 0–27 | | 97,514 | 0 | 0 | 2/17 | 1/8 | 29.7 |
| 7–19 | | 96,422 | 0 | 0 | 2/17 | 1/8 | 24.5 |
| 7–28 | | 97,514 | 0 | 0 | 2/17 | 1/8 | 22.4 |
| 8–28 | | 92,696 | 0 | 0 | 2/17 | 1/8 | 23.2 |
| 15–20 | | 103,018 | 0 | 0 | 2/17 | 1/8 | 24.2 |
| 15–27 | | 96,422 | 0 | 0 | 2/17 | 1/8 | 37.5 |
| 19–20 | | 96,268 | 0 | 0 | 2/17 | 1/8 | 24.3 |
| 19–27 | | 95,726 | 0 | 0 | 2/17 | 1/8 | 33.1 |
| 20–28 | | 95,380 | 0 | 0 | 2/17 | 7711 | 22.8 |
| 27–28 | | 98,016 | 0 | 0 | 2/17 | 1/8 | 30.9 |

`followup-cert2.log` and `followup2-cert2.log` hold the live counts for the other 13 pairs. Every product sits at the saved box's own corner pair. 2/17 is 7710.1/65536, so a radius of 7711 is tight, and the 1/8 boxes have slack.

All 7 pairs the main run didn't finish are in this table: 8–28, 15–20, 15–27, 19–20, 19–27, 20–28 and 27–28. The capped residual was larger than the uncapped one. In 7–15 the capped run reached 2/13 over all 39,648 products. The earlier 3,000-product sample in `nearest.log` reported 1/7.

### What this does and doesn't confirm

- **Confirmed:** each of 2-300's 16 saved boxes covers cert2's full B = 18 residual for its tile pair, with zero skipped directions.
- **Not confirmed:** that the other 512 tile pairs close with no residual. The main run reached pair 8–27 and checked 248 of the 528 pairs. Every non-box pair among them closed. That's sound even with the cap, because skipping only keeps more alive. The remaining 273 non-box pairs, from 8–29 to 31–31, weren't re-run. A run over all pairs at cap 10^9 would need roughly 16 × 30 CPU-s for the box pairs, plus the closed pairs, so about 9 to 10 CPU-minutes.
- The closure's soundness doesn't depend on cert2 alone. The census's residual is its own sound superset of the dark pairs, and the boxes enclose it. cert2 is an independent re-derivation, and it now agrees on all 16 boxes.

### CPU

The follow-up used 503 CPU-s, timed by `/usr/bin/time`: 121 s in `followup-cpu.log` and 382 s in `followup2-cpu.log`. The `nearest.py` runs over about 1.5 million products and three archive extractions weren't timed. I estimate they add 30 to 50 CPU-s, so the total is about 540 to 560 CPU-s, under the 600 CPU-s cap.

Files: `cert2pair.cpp`, `followup.sh` (control and the 3 failing pairs), `followup2.sh` (the other 13 pairs), `followup*-cert2.log`, `followup*-compare.log`, `followup*-cpu.log` and `followup*-run.out`.
