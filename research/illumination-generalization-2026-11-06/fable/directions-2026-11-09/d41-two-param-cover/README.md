# d41: two-parameter covering certificates

Date: 2026-11-13. Idea 2 (Schwartz-style parameter-space covering). Nobody
has reviewed this document. Tags follow d28: **PROVED**, **CHECKED**
(computation, with scope), **OPEN**.

## Answer

- The two-band lemma holds for any two parallel rows (adjacent or not, any
  real heights). For perpendicular bands, it holds only when the band row and
  the band column share no cell of the room. **PROVED** (section 2).
- Every tested pair-line has a two-parameter certificate over all odd
  `(g1, g2)`: 10 of 10 lines in `r20a`, 10 of 10 pairs in `dumb12`.
  **CHECKED.**
- The needed `P` is larger than on one-parameter lines. In `r20a`, rows 2 and
  3 each certify at `P = 9` alone and need `P = 14` jointly. In `dumb12`, pairs
  0 and 2 certify at `P <= 3` per line and need `P = 13` jointly.
- On the hardest lines, the residues that survive longest all lie on
  "slit-shadow" classes in both coordinates: `g_i` shares an odd factor with
  `Q`, so even-`q` directions see `g_i` as the slit `g_i = 0`. Each such class
  was certified at a larger `P`. No class stayed uncovered.

## 1. Method

- Families (task item 1):
  - a. `r20a` (W = 20, the 22-wall room minus cell (5,3); d28 file copied to
    `rooms/`). Its only marked same-parity pair is `(1,3)-(3,5)`.
  - b. Control: `dumb12` (W = 12, two 3 x 3 chambers and a corridor). I first
    tried the 12-wall cross (`rooms/cross12.txt`, one `P = 1` run). Both of its
    same-parity pairs are lit by a straight horizontal or vertical segment at
    every gap, so it can't test anything. `dumb12` has the larger d28
    certificate level (`P = 3`).
- Band choices: two parallel rows `B1 != B2` on one axis, heights `g1`, `g2`
  odd, every other row of height 1 (d28's parity convention). For `r20a`, the
  choices include d28's hardest rows (axis 0 rows 2 and 3, `P = 9`; axis 1
  rows 3 and 4, `P = 7, 8`). Two lines use d28's duplication trick (`dup = 1`)
  so that one total gap is even. This puts the slit `g + 1 = 0` into the odd
  residue grid.
- `band2.c` copies d28's `trace` and adds a second band. For each `p`, it
  fills a table over odd residues `(g1 mod 2 L1 p, g2 mod 2 L2 p)` using every
  normalised direction `0 <= q <= QF p`, every source, and every sign. It then
  lifts the uncovered set `U` from modulus `Q_{P-1}` to `Q_P = 2 L lcm(1..P)` in
  each coordinate and removes the classes that `p = P` covers. When `U` is
  empty, the certificate is complete. `U` is never materialised as a full grid
  (cap 2 x 10^7 entries; never reached, peak `|U|` = 1024).
- Checks (**CHECKED**):
  - At `g2 = 1`, `band2` reproduces `band.c`'s least `p` for `g1 = 1..61` on
    5 lines.
  - Independent check (`xcheck.py`): replicate row `B2` `g2` times as unit
    rows and run d28's `band.c` on row `B1`. This gives 296 (g1, g2, pair)
    comparisons, `g2` in {3, 5, 7, 9}, with 0 mismatches.
  - At the last uncovered residues, the direct tracer finds least `p` = 14
    (`r20a`, `(967967, 679393)`) and 13 (`dumb12`, `(50985, 77217)`), as the
    certificates predict.
  - 80 random odd `(g1, g2) < 2 x 10^6` are all lit, with least `p <= 5`.

## 2. Two-band lemma

**Lemma B2 (PROVED).** Let rows `R1 != R2` be parallel (both horizontal), with
heights `g1, g2 > 0`, and let `L_i` be the lcm of `R_i`'s chord widths. Fix a
primitive direction `(q, p)` with `p >= 1`. Suppose `(g1 - g1') q / p` is in
`2 L1 Z` and `(g2 - g2') q / p` is in `2 L2 Z`. Then `(S, T)` is lit in
`P_{g1,g2}` by a direction-`(+-q, +-p)` path if and only if it is lit in
`P_{g1',g2'}` by one.

*Proof.* Changing `g1` doesn't change any chord width, because chords are
horizontal and lie inside one row. So `L2` and the hypothesis on row 2 are
the same in `P_{g1,g2}` and `P_{g1',g2}`. Apply d28's Lemma B to row 1 with row
2 fixed at `g2`: d28's proof treats each crossing of the open row on its own
and uses only row 1's chord widths. That gives `P_{g1,g2} <-> P_{g1',g2}`.
Then apply Lemma B to row 2 with row 1 fixed at `g1'`. Adjacent rows are
fine: each open row has no vertex, and the strip deleted from a crossing lies
inside one row. QED.

Consequences:

- For each `p`, `Lit_p` is a union of residue classes modulo
  `(2 L1 p, 2 L2 p)`, so the union over `p <= P` is periodic modulo
  `(Q_P(L1), Q_P(L2))`. A cover of every odd residue pair proves the pair lit
  for every odd `(g1, g2)`.
- d28's twist bound `q <= QF p` still holds, because `QF` (the lcm of all chord
  widths) doesn't depend on row heights. Only "no witness with `p <= P`"
  claims depend on this bound.
- The argument extends to `k` parallel rows unchanged.

**Perpendicular bands (row `R`, column `C`).**

- If cell `R ∩ C` is not in the room, no chord of `R` contains a cell of `C`,
  and no vertical chord of `C` contains a cell of `R`. Then `L_R` doesn't
  depend on `v`, and `L_C` doesn't depend on `g`. Lemma B in each direction
  gives periods `(2 L_R p, 2 L_C q)` for a fixed direction **(PROVED)**.
  However, `QF` now depends on `v`, so `q` has no bound. A certificate must
  list finitely many directions with both `p` and `q` bounded. That is still
  sound for "lit" claims. Not computed here.
- If `R ∩ C` is a room cell, the chord of `R` through it has width `w + v - 1`.
  The `g`-period `2 p lcm(widths(v))` then changes with `v`, and the
  `v`-period changes with `g`. The lit set for a fixed direction isn't
  periodic in any fixed lattice. Lemma B gives no joint statement, as d28
  section 6 says.

## 3. Results

d28's one-parameter `P` is listed per band row for comparison.

| Family | Axis, rows (dup) | Pair | Certified (odd g1, g2)? | P (2-band) | d28 P per row | Uncovered set before the last level |
| --- | --- | --- | --- | --- | --- | --- |
| r20a | 0: 2, 3 | (1,3)-(3,5) | yes | 14 | 9, 9 | 8 classes at P = 10..13; all have odd gcd(g_i, Q) > 1 in both coordinates (baseline 0.38); e.g. g1 = 0 mod 1001 = 7·11·13 |
| r20a | 0: 2, 4 | same | yes | 10 | 9, 5 | 12 at P = 9; all slit-shadow in g2 |
| r20a | 0: 3, 5 | same | yes | 9 | 9, 5 | 72 at P = 8; no slit concentration |
| r20a | 0: 0, 2 | same | yes | 11 | 5, 9 | 30 at P = 10; all slit-shadow in g1, 0.80 in both |
| r20a | 0: 1, 3 | same | yes | 10 | 5, 9 | 9 at P = 9, on one g2 value; no slit concentration |
| r20a | 1: 3, 4 | same | yes | 10 | 7, 8 | 396 at P = 9; 0.79 slit-shadow in g1 |
| r20a | 1: 1, 4 | same | yes | 8 | 4, 8 | 48 at P = 7; no slit concentration |
| r20a | 1: 0, 3 | same | yes | 10 | 4, 7 | 96 at P = 9; 0.71 slit-shadow in both |
| r20a | 0: 2, 3 (1, 0) | (1,4)-(3,6) | yes, g1 + 1 even | 9 | 9 (dup) | 128 at P = 8; 4 on the exact slit line g1 + 1 = 0 (about 50 times the share of one line); covered at P = 9 |
| r20a | 1: 3, 4 (0, 1) | (3,1)-(5,3) | yes, g2 + 1 even | 2 | 2 (dup) | trivial |
| dumb12 | 1: 2, 5 | 0 and 2 | yes | 13 | 3, 3 | 192 at P = 12; all have 3 dividing g1 and g2 (L = 3), on 4 lines g1 + g2 = c (mod Q) |
| dumb12 | 1: 2, 5 | 1 and 3 | yes | 3 | 3, 3 | 2 at P = 2 |
| dumb12 | 1: 1, 6 | 0 and 2 | yes | 13 | 2-3, 2-3 | same structure as rows 2, 5 |
| dumb12 | 1: 1, 6 | 1 and 3 | yes | 2 | 2-3, 2-3 | 9 at P = 1 |
| dumb12 | 1: 3, 4 | 0 and 3 | yes | 3 | 3, 3 | 2 to 4 at P = 2 |

Raw output: `runs/*.txt`. Per-pair structure: `runs/analysis.txt`.
`analyze.py` defines "slit-shadow": the odd part of `gcd(g_i + dup_i, Q)`
exceeds 1.

Why slit shadows: for direction `(q, p)`, the period is
`2 L p / gcd(q, 2 L)`. When `2L` divides `q` and `p` is odd, this period is
odd. An odd `g` divisible by it is then equivalent to the slit `g = 0` for
that direction. So residues where `g` shares the odd part of `L p` are
classes on which the slit degeneration acts through even-`q` directions. The
hardest classes in `dumb12` and `r20a` (rows 2, 3) are slit shadows in both
coordinates at once, near the corner `(0, 0)`. This explains the jump in `P`:
the hard set has to avoid two degenerations, and its largest lifts are near
the codimension-2 corner. The reading is a hypothesis; the counts are
**CHECKED**.

## 4. Verdict

- **Yes, qualitatively.** The two-parameter extension behaves like the
  one-parameter case. Every line without a blocking degeneration is
  certified. The residues that resist longest sit on the slit-degenerate
  classes `g_i = 0`, now including their product corner.
- **Quantitatively worse.** The needed `P` rose from 9 to 14 and from 3 to 13.
  Lifting cost follows `|U|`, not the `Q_P^2` grid. Here `|U| <= 1024`, but the
  number of directions per level grows like `QF P^2`.
- **Scaling to all rooms with W <= 20 (honest estimate).** The method can't
  reach a finite proof of 20-wall minimality on its own:
  1. Perpendicular parameters that share a cell have no periodic structure,
     and almost every skeleton row meets every column. A full room has up to
     9 row heights and 9 column widths at W = 20 (vertex grid at most 10 x
     10). Lemma B2 can cover only the parallel parameters of one axis, with
     the other axis's widths fixed. The other axis stays an infinite
     parameter.
  2. Lines that a degeneration blocks (d28's `x0`, total gap 0) need unbounded
     `P`, and these occur at W = 16. With `k` parameters, the degenerate set
     includes every face `g_i = 0` and their intersections.
  3. With `k` parallel rows, the residue grid is `Q_P^k`: at `P = 14`,
     `Q = 2 L x 360360`, about 10^6 per axis and 10^54 for `k = 9`. Lazy
     lifting avoids materialising this only while `|U|` stays small. This
     test (k = 2) says nothing about `|U|` at `k = 9`.
  4. Per (skeleton, row set, pair) at `k = 2`, the run took 0.05 to 2.6 s. The
     number of skeletons with W <= 20 isn't computed here (enumeration was out
     of scope). As an illustration only, 10^5 skeletons times about 50 pair-lines times all row
     subsets is a large cluster job. It would still certify only
     single-axis subfamilies.
- What it can do: certify named single-axis families, for example every
  horizontal stretching of one room's rows with columns fixed, when no face
  blocks the pair. That is a useful lemma generator, not a route to the
  conjecture.

## 5. Resource use

| Item | Use | Cap |
| --- | --- | --- |
| Concurrent processes | at most 3 (`xargs -P 3`); the checks ran one at a time | 3 |
| Computation wall clock | about 2 minutes in total, including checks; certificate runs 5.7 s summed | 60 min |
| Peak memory | 2.2 MB RSS per process | 1 GB |
| Output files | 504 KB for the whole directory, including the binary | 2 MB |

Cap deviation: none. A one-second `P = 1` run on the 12-wall cross was used
only to see that the cross is trivial. Family b is `dumb12`, which the task
allows as "a 12-wall room of your choice from d28's tested rooms".

## 6. Files

- `band2.c`, `band2`: `band2 AXIS B1 B2 PMAX [dup1 dup2 [pairs]] < room`.
  `PT=g1,g2` prints the least `p` per pair. `ULMAX` controls how much of the
  uncovered set is listed.
- `configs.txt`, `run.sh`: the 13 runs. `analyze.py`: uncovered-set
  structure. `xcheck.py`: independent check against d28's `band.c`.
- `rooms/`: copies of `r20a`, `dumb12`, `cross12`. `runs/`: outputs and
  `/usr/bin/time -l` logs.
