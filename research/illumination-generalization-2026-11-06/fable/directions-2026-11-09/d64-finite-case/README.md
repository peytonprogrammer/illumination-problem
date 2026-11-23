# d64: the finite case of the realization lemma (RL-fin)

Date: 2026-11-18. Approved enumeration: quotients `K_x`, their covers, and a per-row test.
Tags: **PROVED** (argument here), **COMPUTED** (script and log here), **CITED** (file),
**GUESSED**.

## Answer

- **RL-fin is false as stated (COMPUTED).** Take the 2,800 normalized strictly simple rooms
  with `W <= 20` and some `1 < deg N_x < n`. They have 81,924 rows, and 830 are x-dark.
  None of the 830 has a Rig or Cut certificate, so all 830 are counterexamples to d63's RL.
- **It also fails for distinct interior marks, at point level.** 37 pairs `S != T` of
  interior points are x-dark on all four lift pairs, with no certificate at `x`. The
  smallest has 12 walls and 20 cells (room 1843, section 5).
- **The target consequence holds in this range (COMPUTED).** All 6,680 distinct same-class
  interior pairs in the 2,800 rooms are lit. So no room with `W <= 20` and some
  `N_x != B` (with `delta_x >= 2`) has a dark pair. This closes the finite half directly,
  without RL.
- **The proof chain must change (PROVED from the above).** d61 and d63 use RL one target at
  a time. That per-target statement is false. Every counterexample pair is lit through
  another target or another lift pair. The usable statement works at pair level: a dark
  pair has a certificate at every target (d10 D2). RL-B (`N_x = B`) probably needs the same
  restatement (GUESSED).

## 1. Scope

- Rooms: strictly simple orthogonal lattice rooms, normalized, with `r <= 8` (`W <= 20`).
  45-degree walls are out of scope.
- Rows follow d63 `realize.py`. For each corner class `a` and target `x` with
  `1 < deg N_x < n`, a row is an unordered pair of distinct regular `a`-points of `DP`
  with one image in `N_x`. Regular points include lifts of interior points and smooth wall
  points. Rows with `N_x = B` are RL-B and aren't tested. With `delta_x = 1`, `B_x` is
  discrete, so no row exists.
- Certificates (d62 G3 quantifiers):
  - `rigRy` is Rig(x) over `DP / R_y` for both `y` outside `{a, x}`.
  - `rig` and `cut` are Rig(x) and Cut(x) over every proper factor (d10 Theorem U code).
  - Par(x) is asserted absent on every dark row (R3).
- A counterexample is an x-dark row with none of `rigRy`, `rig`, or `cut`. Its orbit must
  be complete.

## 2. Completeness argument (PROVED; written before the run)

Let `P` be in scope and let `x` have a row. Translate so `x = (0, 0)`. A unit translation
permutes the classes, so this loses nothing (d54 item 1).

1. `B_x` is W-invariant (R3.3). So `K = P / B_x` is a transitive W-set with `d` cells, and
   `P -> K` has fibres of size `delta >= 2` (d54 item 2).
2. `K` has these properties:
   - Orbit types are cvx, smooth, rfx, cone, or int (d52 C9: Fact L, zeros on the seam).
   - Class `x` has no smooth or int orbit (R3.1).
   - It has at most one cone (C4), and genus 0 (C1).
3. **`z >= 1`.** If `z = 0`, then `N_x` is a pillowcase, so `N_x = B` by R1, and the row is
   out of scope. Also `delta * z <= r <= 8` (C5), so `z <= 4`.
4. **At least 3 singular classes (PROVED here).** Normalized means some horizontal and some
   vertical edge have odd length. Their end points give two classes that differ in `x`
   parity, plus two that differ in `y` parity. Together that's at least 3 classes. Fact L
   maps corners of `P` to singular points of `K`.
5. **`d <= 4z + 2` (PROVED here).** Each cell has one `x`-star, so
   `d = cvx_x + 3 rfx_x + 2 cone_x`. With `p = z + 4`, this equals
   `4z + 4 - (cvx' + 2 cone' + 3 rfx')`, where primes count orbits outside class `x`.
   Two non-`x` classes are singular by step 4, so the subtracted term is at least 2.
   So `d <= 18`.
6. **The quotient search finds every such `K`.** `enum_K.c` is a line-for-line C port of
   d52 `enum_K.py`. d54 item 1 checked that search as complete. Run here with `zmax = 4`
   and `dmax = 18`.
7. **The cover search finds every `P`.** `enum_P.covers` (d52, unchanged) enumerates every
   degree-`delta` W-set cover of `K` with room-local types and `r <= 8`. The model is
   proved in d54 item 2 for every `delta`, including `delta = 2`.
8. The filters `fold.is_room` and normalization (edge-length gcd 1 in each direction, as in
   R1) then give every in-scope room. The covers are a superset: `B_x` is recomputed on `P`.

The same chain applies to the target statement in section 4. That check uses the same rooms.

**Validation (COMPUTED).**

| Check | Result |
| --- | --- |
| C port against d52 lists | `zmax 2, dmax 12`: 127 = 127 shapes. `zmax 3, dmax 16`: 677 = 677. Node counts are identical. |
| Admissible shapes | 4,290 of 4,420. d52's 106 shapes are all included. The largest `d` is 17. |
| Arc model against d52's model-free enumerator, `delta = 2` | All 4,290 cases: 9,548 = 9,548 covers. 0 missing, 0 extra. d54 already checked `delta >= 3` (the same 185 cases). |
| Brute force: every fixed polyomino with `n <= 14` (9,800,041) | 229 in-scope rooms. All 229 are in the cover list. |
| Named rooms | cross12 is in the list. dumb12 (`N_x = B`), R22 (`r = 9`), and P6 (`r = 12`) correctly aren't. |

## 3. Counts (COMPUTED)

| Stage | Count |
| --- | --- |
| Genus-0 shapes, `z <= 4`, `d <= 18` | 4,420 (54 CPU-s, 114,149,700 nodes) |
| Admissible shapes / (K, delta) cases | 4,290 / 4,475 (3,663 of them `z = 4`, `delta = 2`) |
| Cover tuples / genus-0 discs with `r <= 8` | 59,653 / 14,458 |
| Strictly simple rooms (up to isometry) / normalized | 4,776 / 4,581 (area 6 to 40) |
| Rooms with some `1 < deg N_x < n` | 2,800 |
| (room, a, x) cases | 8,529 (`delta` 2: 5,481; 3: 243; 4: 480; 5: 342; 6: 963; 7: 831; 8: 189) |
| Rows / x-lit / x-dark | 81,924 / 81,094 / 830 |
| Dark rows certified (rigRy, rig, cut) | 0, 0, 0 |
| Counterexamples / unresolved orbits | 830 / 0 |
| Soundness violations (lit with rigRy) | 0 |
| Largest orbit / deepest witness | 4,608 states / depth 7 |

The 830 dark rows break down as follows:

- By kind: 535 smooth-smooth, 170 distinct interior, 46 interior-smooth, and 79 lift pairs
  of one point.
- By room: they lie in 55 rooms. 29 of those rooms have a distinct-interior dark row.
- By `(delta, deg N_x, z(N_x))`: `(2, 8, 4)` has 4 rows and `(4, *, 1 or 2)` has 206.
  `(6, 3 to 5, 1)` has 337, and `(8, 4 to 5, 1)` has 283. Every case has `delta` even.

**Point level (`pointlevel.py`).** On the 29 rooms, 200 (a, x, S, T) groups have
distinct interior points:

- 37 are x-dark on every lift pair, and all 37 are uncertified.
- 43 are mixed: some lift pairs are lit and some are dark.

The 37 uncertified groups lie in 10 rooms.

**Ground truth.** `verify_billiard.py` compared the orbit verdicts with exact integer
billiards (d62 `billiard.shoot`) on all 55 dark rooms: 2,794 (S, T, x) groups.

- At `H = 30`: 17 mismatches. Every one was an orbit-lit group with no billiard witness yet.
- At `H = 120`, on the 7 rooms involved: 0 mismatches.

No billiard path contradicts a dark verdict.

**Target check (`dark_pairs.py`).** On the 2,800 rooms, 6,680 distinct same-class interior
pairs were tested. All are lit, and the largest orbit walked had 74 states.

## 4. What this means for the proof

- **RL-fin isn't true, so it can't be proved (COMPUTED).** The counterexamples need no
  exotic structure. Rig fails because each `R_y` is the one-block system. Cut fails in two
  ways:
  - No factor of degree at most 3 exists.
  - The only one (the tromino double) sends a regular `a`- or `x`-point to a pole (R4).
- **The finite half of the target is closed anyway (COMPUTED).** Let `P` be a normalized
  strictly simple room with `W <= 20` and some `delta_x >= 2` with `N_x != B`. Then every
  same-class interior pair of `P` is lit. This rests on the completeness argument
  (section 2) and on the pure-braid orbit model of light. d62 checked that model against
  billiards, and this check repeats it on 55 rooms.
- **What's left for `W <= 20` same-class pairs.** Rooms where every class has `N_x = B` or
  `delta_x = 1`. This is RL-B territory. The statement to prove there is pair-level, as in
  d10 D2: a dark pair is certified at every target. Per-target RL-B may fail like RL-fin.
  That's GUESSED and untested here.
- Different-class pairs (G1) and rational pairs (G2) are unchanged.

## 5. Counterexamples with full data

Rooms are cell lists; cell `(i, j)` is `[i, i+1] x [j, j+1]`. Sheets follow
`roomtools.room_tuple(cells, origin)`.

**Room 1843: the smallest point-level counterexample.** It has 20 cells, `r = 4`, and
`W = 12`.

```
y=5 .##.
y=4 ####
y=3 ####
y=2 ####
y=1 ####
y=0 #..#
```

- Cells: `(0,0) (0,1) (0,2) (0,3) (0,4) (1,1) (1,2) (1,3) (1,4) (1,5) (2,1) (2,2) (2,3)
  (2,4) (2,5) (3,0) (3,1) (3,2) (3,3) (3,4)`.
- Class `a` is the class of `(1, 0)`. Target `x = d`, the class of `(1, 1)`.
  `S = (1, 2)` and `T = (3, 2)` are interior. The same holds for `(1, 4)` and `(3, 4)`.
- Cycle types of `(g_a, g_b, g_c, g_d)`: `[2^8, 1^4]`, `[2^9, 1^2]`, `[2^9, 1^2]`,
  `[3^4, 2^4]`.
- `N_d` has degree 5 and `delta = 4`. Its types are `[2,2,1]`, `[2,2,1]`, `[2,2,1]`,
  `[3,1,1]`. The blocks are `{0,9,14,15} {1,8,13,16} {2,7,12,17} {3,6,11,18} {4,5,10,19}`.
- Lifts are `S~ in {(1,6), (2,5)}` and `T~ in {(10,17), (11,16)}`. Two lift pairs share
  an `N_d` image: `(1,6)-(11,16)` and `(2,5)-(10,17)`. Both are d-dark, with a complete
  orbit of 36 states. The other two lift pairs are d-dark by Par. Billiards agree.
- No certificate:
  - `R_b` and `R_c` are the one-block system, so Rig fails.
  - The proper factors have degree 10 and 5, so no Cut is possible.
- The pair is lit. All four lift pairs are b-lit at depth 0, along the straight segment
  through `(2, 2)`.

**Room 1490: the smallest distinct-interior row (lift level).** It has 18 cells, `r = 8`,
and `W = 20`.

```
y=7 .#..
y=6 ##..
y=5 ####
y=4 .##.
y=3 .##.
y=2 ####
y=1 ##..
y=0 .#..
```

- Class `a` is the class of `(0, 1)`. `S = (2, 3)` and `T = (2, 5)`, target `x = d`.
- `N_d` is the tromino double (degree 3, `delta = 6`), with types `[2,1]`, `[3]`, `[2,1]`,
  `[1,1,1]`.
- Rows `(6,13)-(9,14)` and `(7,12)-(8,15)` are d-dark, with 27 orbit states. The lift pair
  `(6,13)-(8,15)` is d-lit.
- No certificate:
  - `R_b` and `R_c` are the one-block system.
  - The degree-3 factor sends a regular `a`- or `x`-point to a pole, so Cut fails.
- The pair is c-lit.

**Room 453: the smallest row overall.** It has 16 cells and `W = 12`. The marks are smooth
wall points `(0, 2)` and `(0, 10)`, with `x = c`.

Full row data for all 830 rows: `data/rl_*.json` (`special_rows`). The 1843 and 1490 dumps
are in `logs/example_1843.log` and `logs/example_1490.log`.

## Files

| File | Role |
| --- | --- |
| `enum_K.c`, `kload.py` | C port of d52 quotient search (`cc -O2 -o enum_K enum_K.c`; `./enum_K 4 18`) |
| `shapes.py` | Admissibility filter (`delta >= 2`) |
| `covers.py` | d52 arc-model covers, room and normalization filter, isometry dedupe |
| `validate.py` | Brute-force polyominoes and generic-versus-arc check |
| `rl_test.py`, `summarize.py` | RL rows, certificates, aggregate (`logs/summary.log`) |
| `dark_pairs.py` | Direct darkness test of interior pairs |
| `pointlevel.py`, `example.py`, `verify_billiard.py` | Point-level form, example dumps, billiard ground truth |
| `data/`, `logs/` | Outputs (5.2 MB in total) |

Reused unchanged: d52 `fold.py`, `enum_P.py`, and `validate_generic.generic_covers`;
d63 `realize.orbit_lit`; d61 `dp_joined`; d10 `unified_test` and `roomtools`; d62
`billiard.shoot`. `fh_star`'s 540-s import-time CPU limit is bypassed in `rl_test.py`.
Each script sets its own limit.

## CPU

All measured with `time` or `process_time`, except item 2.

| Item | CPU-s |
| --- | --- |
| Quotient search (5 runs, including validation slices) | 83 |
| Shapes (estimated) and covers | about 40 |
| Validation (brute force `n <= 14`, generic checks) | 441 |
| RL rows (7 runs, including slices) | 597 |
| Billiards (2 rounds of `H = 30` and `H = 120`) | about 402 |
| Point level, dark pairs, examples | about 70 |
| **Total** | **about 1,630 (27 CPU-minutes); cap 120** |

At most 5 processes ran at once. Temporary files went to `/tmp` and were deleted. Nothing
was written outside this directory.
