# d11: exact census of dark pairs in strictly simple canonical45 rooms

## Bounds completed

| Census | Rooms covered | Pairs checked | Result |
|---|---|---|---|
| A/B pairs | every strictly simple room with `N ≤ 32` tiles, `W ≤ 24` and an A/B pair: 734,609,564 rooms up to G | 736,957,663 | 736,957,650 lit, 1 dark, 12 undecided by `orbit45` (all 12 dark by clean parity) |
| C pairs | every strictly simple room with `N ≤ 24` and a C pair (no room in this range has `W > 22`): 129,200,974 rooms | 178,695,704 | all lit |
| C pairs, extra | C pairs inside the A/B-census rooms (`N ≤ 32`, `W ≤ 24`) | 1,162,254,602 | all lit |

The A/B bound is `N_max = 32`. It covers Wolecki's tile count (24),
Castro's (27), Tokarsky's (29) and the known 22-wall room (30). The C bound is
`N_max = 24`. It doesn't reach the C-pair copy of the 22-wall room: that room
shifted by `(1, 0)` has 30 tiles and only 2 interior points, both C points.

Every lit verdict has an explicit legal path that `verify45` replayed
(`verify_fail = 0` in every chunk; the longest certificate is 28 lattice
steps).

## Answers

These are computed facts within the bounds above, followed by interpretation
where marked.

**(a) Is there a dark or undecided strictly simple room with `W ≤ 21`?**
No. All 616,380,295 A/B pairs with `W ≤ 21` and `N ≤ 32` are lit, each with
a replayed certificate. All C pairs (`N ≤ 24`, and inside A/B rooms up to
`N ≤ 32`) are lit. Nothing at `W ≤ 21` needed the distrust protocol.

**(b) Is the known orthogonal room the only strictly simple dark room at
`W = 22`?** Within `N ≤ 32` (A/B pairs) and `N ≤ 24` (C pairs), yes. Exactly
one pair at `W = 22` survives shooting: a B pair in a 30-tile room that is the
22-wall room translated by `(1, 1)`. `orbit45` decides it DARK (2,592 states),
and d6 decides it DARK by exhausting both orbit components (3,456 states each).
There's no dark or undecided pair at `W = 23`.

**(c) Smallest `W` of a strictly simple dark room, and of a clean one?**
Within the bounds, the smallest `W` of a dark room is 22 (the known room, 30
tiles). The smallest `W` of a clean room (`k = 0`) is 24: the 12 rooms with 27
tiles that d4 listed as `parity-W24-0` … `parity-W24-11` (Castro's room is
`parity-W24-5`). No pair with `W ≤ 23` and `N ≤ 32` has `k = 0`.

**(d) Does "dark iff a parity factor separates" hold for every decided
pair?**

- A/B pairs: yes. None of the 736,957,650 lit A/B pairs has a separating
  N_min, and all 13 surviving pairs (1 dark, 12 clean) are separated. Every
  lit A/B pair has `k ≥ 1`; the only `k = 0` A/B pairs are the 12 clean
  rooms.
- C pairs: no. The triangle-framework N_min separates 159,403 lit C pairs in
  the A/B census and 14,770,425 lit C pairs in the C census. The smallest
  example has `N = 10`, `W = 7`:
  tiles `(1,0,1) (2,0,0) (2,0,1) (3,0,0) (3,0,1) (4,0,1) (1,1,0) (2,1,0) (3,1,0) (4,1,0)`,
  pair `(2,1)`, `(4,1)`, `k = 0`. It's
  lit by direction `(1, −1)` in 2 steps, reflecting at the flat boundary C
  point `(3, 0)`.

  *Interpretation.* The parity proof rotates the developed segment by π about
  its midpoint, and it needs that rotation to act trivially on N_min. For a C
  pair, N_min kills π-rotations only about A and B points. A developed C-to-C
  segment can have its midpoint at a C point or at the centre of a unit
  square, where the argument says nothing. `cmid45.py` confirms this: in the
  rooms of `star 24 (1,0)`, all 124 separated lit C pairs have a midpoint of
  class C (4) or a square centre (120), never A or B. The same reason means
  `k = 0` doesn't imply dark for C pairs: a path in a direction `(p, q)` with
  `p` and `q` both odd never meets an A or B point. So N_min separation and
  `k = 0` are dark certificates only for A/B pairs.

## Dark and undecided pairs

Coordinates are those written by `enum45` (canonical form under G). The
polygons are the boundary corners in order.

| Chunk (`census/star-32/`) | Class | N | W | S | T | k | N_min blocks | sep | `orbit45` | d6 | Same as |
|---|---|---:|---:|---|---|---:|---:|---:|---|---|---|
| `1_1-02` | B | 30 | 22 | (−1, 3) | (1, 5) | 4 | 10 | 1 | DARK, 2,592 states | DARK, full orbit (3,456 + 3,456) | 22-wall room, translated by (1, 1) |
| `2_0-15`, `2_0-20`, `2_0-28` (12 rooms) | A | 27 | 24 | (0, 2) | (0, 6) | 0 | 27 | 1 | UNDECIDED at 3,000,000 states | DARK, basis `k = 0` (orbit not finished at 200,000) | d4 `parity-W24-0` … `-11`; Castro = `-5` |

The 22-wall room in census coordinates is
`(0,0) (1,0) (1,2) (0,2) (0,4) (2,4) (2,3) (4,3) (4,4) (3,4) (3,5) (2,5) (2,6) (0,6) (0,5) (-1,5) (-1,4) (-2,4) (-2,2) (-1,2) (-1,1) (0,1)`.
d4's block analysis of it (degree 30, group order 466,560, imprimitive) finds
block systems of sizes 1, 2, 3, 6, 15 and 30. The size-3 system is a parity
system that separates S and T.

The 12 clean rooms are all strictly simple, and the Python boundary walk
confirms `W = 24`. Their monodromy groups are primitive of degree 27, so d4
finds no nontrivial block system. They're dark by the clean-parity lemma
(`k = 0`, A pair), not by a finished orbit. Their tiles are in
`census/star-32/survivors.txt`. Each has S = (0, 2) and T = (0, 6):

| Chunk | Same as | Polygon |
|---|---|---|
| `2_0-28` | `parity-W24-0` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (0,3) (0,5) (1,5) (2,6) (1,6) (1,7) (0,8) (0,7) (-1,7) (-1,6) (-2,6) (-1,5) (-1,4) (-2,4) (-1,3) (-1,2) (-2,2) (-1,1)` |
| `2_0-28` | `parity-W24-1` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (0,3) (0,5) (1,5) (2,6) (1,6) (1,7) (0,7) (0,8) (-1,7) (-1,6) (-2,6) (-1,5) (-1,4) (-2,4) (-1,3) (-1,2) (-2,2) (-1,1)` |
| `2_0-28` | `parity-W24-2` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (0,3) (0,5) (1,5) (1,6) (2,6) (1,7) (0,7) (0,8) (-1,7) (-1,6) (-2,6) (-1,5) (-1,4) (-2,4) (-1,3) (-1,2) (-2,2) (-1,1)` |
| `2_0-15` | `parity-W24-3` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (2,4) (1,4) (1,5) (2,6) (1,6) (1,7) (0,7) (0,8) (-1,7) (-1,6) (-2,6) (-1,5) (0,5) (0,3) (-1,3) (-1,2) (-2,2) (-1,1)` |
| `2_0-15` | `parity-W24-4` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (2,4) (1,4) (1,5) (2,6) (1,6) (1,7) (0,8) (0,7) (-1,7) (-1,6) (-2,6) (-1,5) (0,5) (0,3) (-1,3) (-1,2) (-2,2) (-1,1)` |
| `2_0-15` | `parity-W24-5 (Castro)` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (1,4) (2,4) (1,5) (2,6) (1,6) (1,7) (0,8) (0,7) (-1,7) (-2,6) (-1,6) (-1,5) (0,5) (0,3) (-1,3) (-1,2) (-2,2) (-1,1)` |
| `2_0-15` | `parity-W24-6` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (0,3) (0,5) (1,5) (2,6) (1,6) (1,7) (0,7) (0,8) (-1,7) (-1,6) (-2,6) (-1,5) (-2,4) (-1,4) (-1,3) (-2,2) (-1,2) (-1,1)` |
| `2_0-15` | `parity-W24-7` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (1,4) (2,4) (1,5) (2,6) (1,6) (1,7) (0,8) (0,7) (-1,7) (-1,6) (-2,6) (-1,5) (0,5) (0,3) (-1,3) (-2,2) (-1,2) (-1,1)` |
| `2_0-20` | `parity-W24-8` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (1,4) (2,4) (1,5) (2,6) (1,6) (1,7) (0,8) (0,7) (-1,7) (-1,6) (-2,6) (-1,5) (0,5) (0,3) (-1,3) (-1,2) (-2,2) (-1,1)` |
| `2_0-28` | `parity-W24-9` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (0,3) (0,5) (1,5) (2,6) (1,6) (1,7) (0,8) (0,7) (-1,7) (-1,6) (-2,6) (-1,5) (-1,4) (-2,4) (-1,3) (-2,2) (-1,2) (-1,1)` |
| `2_0-28` | `parity-W24-10` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (0,3) (0,5) (1,5) (2,6) (1,6) (1,7) (0,7) (0,8) (-1,7) (-1,6) (-2,6) (-1,5) (-1,4) (-2,4) (-1,3) (-2,2) (-1,2) (-1,1)` |
| `2_0-20` | `parity-W24-11` | `(0,1) (0,0) (1,1) (1,2) (2,2) (1,3) (1,4) (2,4) (1,5) (2,6) (1,6) (1,7) (0,7) (0,8) (-1,7) (-1,6) (-2,6) (-1,5) (0,5) (0,3) (-1,3) (-1,2) (-2,2) (-1,1)` |


Both deciders and the independent simplicity and `W` routine
(`rooms45.boundary`) agree on every row; see `decide_star32.log` and
`census/star-32/decide45.json`.

## Totals

`census/star-32/table_WN.tsv` and `census/cstar-24/table_WN.tsv` hold the full
per-`(W, N)` tables. `totals.tsv` adds per-class rows and the N_min separation
counts, and `khist.tsv` the distribution of `k`. Star growth doesn't enumerate rooms
without a pair. Counts of all rooms per `(n, W)` are in `e12.counts`
(`n ≤ 12`) and `xcheck/p20_*.counts` (`16 ≤ n ≤ 20`, `W ≤ 22`, summed over the
3 jobs).

"Dark" means a finished `orbit45` orbit. "Undecided" means `orbit45` hit its
3,000,000-state cap.

### A/B pairs, `N ≤ 32`, by W

| W | rooms with a pair | pairs | lit | dark | undecided by orbit (of which k = 0) |
|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 1 | 1 | 0 | 0 (0) |
| 4 | 29 | 57 | 57 | 0 | 0 (0) |
| 5 | 125 | 175 | 175 | 0 | 0 (0) |
| 6 | 1246 | 1626 | 1626 | 0 | 0 (0) |
| 7 | 6751 | 7917 | 7917 | 0 | 0 (0) |
| 8 | 38106 | 43080 | 43080 | 0 | 0 (0) |
| 9 | 155713 | 168035 | 168035 | 0 | 0 (0) |
| 10 | 588983 | 623902 | 623902 | 0 | 0 (0) |
| 11 | 1784780 | 1853587 | 1853587 | 0 | 0 (0) |
| 12 | 4853721 | 4987917 | 4987917 | 0 | 0 (0) |
| 13 | 11039807 | 11239617 | 11239617 | 0 | 0 (0) |
| 14 | 22463728 | 22750229 | 22750229 | 0 | 0 (0) |
| 15 | 39197098 | 39531954 | 39531954 | 0 | 0 (0) |
| 16 | 61136457 | 61499247 | 61499247 | 0 | 0 (0) |
| 17 | 82949221 | 83260929 | 83260929 | 0 | 0 (0) |
| 18 | 100218764 | 100471206 | 100471206 | 0 | 0 (0) |
| 19 | 106085751 | 106255770 | 106255770 | 0 | 0 (0) |
| 20 | 100395276 | 100493405 | 100493405 | 0 | 0 (0) |
| 21 | 83143969 | 83191641 | 83191641 | 0 | 0 (0) |
| 22 | 60570939 | 60589696 | 60589695 | 1 | 0 (0) |
| 23 | 38450967 | 38456641 | 38456641 | 0 | 0 (0) |
| 24 | 21528132 | 21531031 | 21531019 | 0 | 12 (12) |
| all | 734609564 | 736957663 | 736957650 | 1 | 12 (12) |

### A/B pairs, `N ≤ 32`, by N

| N | rooms with a pair | pairs | lit | dark | undecided by orbit (of which k = 0) |
|---:|---:|---:|---:|---:|---:|
| 16 | 1 | 1 | 1 | 0 | 0 (0) |
| 17 | 3 | 3 | 3 | 0 | 0 (0) |
| 18 | 25 | 25 | 25 | 0 | 0 (0) |
| 19 | 101 | 101 | 101 | 0 | 0 (0) |
| 20 | 453 | 453 | 453 | 0 | 0 (0) |
| 21 | 1670 | 1670 | 1670 | 0 | 0 (0) |
| 22 | 6042 | 6042 | 6042 | 0 | 0 (0) |
| 23 | 20393 | 20393 | 20393 | 0 | 0 (0) |
| 24 | 67414 | 67419 | 67419 | 0 | 0 (0) |
| 25 | 215890 | 215916 | 215916 | 0 | 0 (0) |
| 26 | 679195 | 679434 | 679434 | 0 | 0 (0) |
| 27 | 2096286 | 2097605 | 2097593 | 0 | 12 (12) |
| 28 | 6383512 | 6390296 | 6390296 | 0 | 0 (0) |
| 29 | 19176089 | 19205930 | 19205930 | 0 | 0 (0) |
| 30 | 56959094 | 57081631 | 57081630 | 1 | 0 (0) |
| 31 | 166871395 | 167340404 | 167340404 | 0 | 0 (0) |
| 32 | 482132001 | 483850340 | 483850340 | 0 | 0 (0) |
| all | 734609564 | 736957663 | 736957650 | 1 | 12 (12) |

### C pairs, `N ≤ 24`, by W

| W | rooms with a pair | pairs | lit | dark | undecided by orbit (of which k = 0) |
|---:|---:|---:|---:|---:|---:|
| 3 | 2 | 4 | 4 | 0 | 0 (0) |
| 4 | 43 | 187 | 187 | 0 | 0 (0) |
| 5 | 201 | 647 | 647 | 0 | 0 (0) |
| 6 | 1414 | 4527 | 4527 | 0 | 0 (0) |
| 7 | 7664 | 22486 | 22486 | 0 | 0 (0) |
| 8 | 36090 | 99292 | 99292 | 0 | 0 (0) |
| 9 | 143738 | 364801 | 364801 | 0 | 0 (0) |
| 10 | 490782 | 1157375 | 1157375 | 0 | 0 (0) |
| 11 | 1422166 | 3098286 | 3098286 | 0 | 0 (0) |
| 12 | 3510227 | 7034552 | 7034552 | 0 | 0 (0) |
| 13 | 7360265 | 13482668 | 13482668 | 0 | 0 (0) |
| 14 | 13013807 | 21692650 | 21692650 | 0 | 0 (0) |
| 15 | 19285185 | 29174000 | 29174000 | 0 | 0 (0) |
| 16 | 23720269 | 32577192 | 32577192 | 0 | 0 (0) |
| 17 | 23711913 | 29698039 | 29698039 | 0 | 0 (0) |
| 18 | 18718343 | 21557051 | 21557051 | 0 | 0 (0) |
| 19 | 11321452 | 12141390 | 12141390 | 0 | 0 (0) |
| 20 | 4909946 | 5043090 | 5043090 | 0 | 0 (0) |
| 21 | 1385398 | 1385398 | 1385398 | 0 | 0 (0) |
| 22 | 162069 | 162069 | 162069 | 0 | 0 (0) |
| all | 129200974 | 178695704 | 178695704 | 0 | 0 (0) |

### C pairs, `N ≤ 24`, by N

| N | rooms with a pair | pairs | lit | dark | undecided by orbit (of which k = 0) |
|---:|---:|---:|---:|---:|---:|
| 8 | 1 | 1 | 1 | 0 | 0 (0) |
| 9 | 2 | 2 | 2 | 0 | 0 (0) |
| 10 | 10 | 10 | 10 | 0 | 0 (0) |
| 11 | 34 | 34 | 34 | 0 | 0 (0) |
| 12 | 134 | 138 | 138 | 0 | 0 (0) |
| 13 | 447 | 461 | 461 | 0 | 0 (0) |
| 14 | 1538 | 1616 | 1616 | 0 | 0 (0) |
| 15 | 4935 | 5281 | 5281 | 0 | 0 (0) |
| 16 | 15663 | 17196 | 17196 | 0 | 0 (0) |
| 17 | 48042 | 54087 | 54087 | 0 | 0 (0) |
| 18 | 145187 | 168306 | 168306 | 0 | 0 (0) |
| 19 | 430243 | 513817 | 513817 | 0 | 0 (0) |
| 20 | 1260089 | 1553120 | 1553120 | 0 | 0 (0) |
| 21 | 3643329 | 4637752 | 4637752 | 0 | 0 (0) |
| 22 | 10436932 | 13734086 | 13734086 | 0 | 0 (0) |
| 23 | 29638154 | 40332972 | 40332972 | 0 | 0 (0) |
| 24 | 83576234 | 117676825 | 117676825 | 0 | 0 (0) |
| all | 129200974 | 178695704 | 178695704 | 0 | 0 (0) |


## Open doubts

- **Bounded, not general.** Every answer holds only for `N ≤ 32` (A/B) and
  `N ≤ 24` (C). Rooms with `W ≤ 22` exist at every size, so these bounds don't
  settle (a) or (b) in general.
- **C pairs from 25 to 30 tiles.** The C census stops at 24 tiles. A dark
  C pair at `N = 25 … 30` and `W ≤ 22` that isn't a C copy of the known room
  isn't excluded. The C copy of the 22-wall room (30 tiles) is dark but lies
  outside the bound.
- **`W = 25, 26`.** The census keeps `W ≤ 24`, so Tokarsky's room (`W = 26`)
  isn't a census positive control; the validation covers it.
- **Undecided orbits.** `orbit45` didn't finish the 12 clean rooms at
  3,000,000 states. Their darkness rests on the clean-parity lemma.
- **Shared assumptions.** Star growth and plain enumeration share the room
  test (Euler characteristic plus vertex runs) and `canon_free`. The Python
  brute force checks the room test independently only up to `n = 12`; the
  Python boundary walk rechecks every survivor.
- **OEIS.** The free tetrakis animal counts weren't checked against OEIS (no
  network); they rest on the independent brute force.

## Validation

| Item | Result |
|---|---|
| Castro 24 | 27 tiles, strictly simple, `W = 24`; shooting survivor, `k = 0`, separated; `orbit45` UNDECIDED at 3,000,000; d6 DARK by `k = 0` |
| Tokarsky 26 | 29 tiles, strictly simple, `W = 26`; survivor, `k = 0`, separated; `orbit45` UNDECIDED at 3,000,000; d6 DARK by `k = 0` |
| 22-wall room as triangles | 30 tiles, strictly simple, `W = 22`; survivor, `k = 4`, separated; `orbit45` DARK (2,592 states); d6 DARK, full orbit (3,456 + 3,456) |
| Wolecki's pinched room | 24 tiles, not strictly simple (2 boundary cycles, `W = 22` with multiplicity, 21 corner points); survivor, `k = 0`, separated; `orbit45` UNDECIDED at 3,000,000; d6 DARK by `k = 0` |
| d4 census rooms, `W = 24 … 26` | all 327 marked pairs survive shooting and are separated; 3 sent to `orbit45`, all UNDECIDED at 3,000,000 (`k = 0`) |
| Lit controls | 520 (13 from `transparent-simple-two-symmetric-screen.json`, 307 from `two-global-*.json`, the first 200 of `learned.jsonl`): all lit with replayed certificates, none separated; 49 sent to `orbit45`, all LIT |
| Tracer negative test | 747 certificates replayed 747; with the target replaced by S, 747 of 747 rejected; with the direction rotated by 90°, 741 of 747 rejected (the other 6 rotated paths are also legal) |
| Boundary-walk `W` against record `W` | equal for all 851 validation rooms |

`orbit45` agrees with the expected verdict on 50 of 56 decided pairs; the
other 6 hit the cap and are all `k = 0`. Logs: `validate45.log`,
`validate45.json`, `validation/`.

## Tiling and room definition

The tiling is d4's `canonical45` tiling. Its lines are `x ∈ Z`, `y ∈ Z`,
`x + y ∈ 2Z` and `x − y ∈ 2Z`. Square `[i, i+1] × [j, j+1]` is cut along its
A–B diagonal: `/` if `i + j` is even, `\` if odd. A tile is written `(i, j, h)`:

- `/`: `h = 0` is `(i,j)(i+1,j)(i+1,j+1)`; `h = 1` is `(i,j)(i,j+1)(i+1,j+1)`.
- `\`: `h = 0` is `(i,j)(i+1,j)(i,j+1)`; `h = 1` is `(i+1,j)(i+1,j+1)(i,j+1)`.

Lattice point classes:

- A = (even, even) and B = (odd, odd): 8 tiles meet, each with angle π/4.
- C = mixed parity: 4 tiles meet, each with angle π/2. Diagonal walls never
  pass through C points.

The symmetry group G of the tiling is the translations `(a, b)` with `a + b`
even, together with the 8 linear maps of D4. Translation by `(1, 1)` swaps A
and B. Rooms are counted up to G. Castro's, Tokarsky's, Wolecki's and the
22-wall orthogonal room are unions of tiles of this tiling with marks on A
points. Every polyomino at every integer position is also a union of tiles.

A room is a finite edge-connected set of tiles that is strictly simple:

- The tiles around every vertex form one cyclic run, so there's no pinch.
- `V − E + F = 1`, so there are no holes.
- A union of tiles can't contain a slit, because every interior edge has
  room on both sides.

`W` is the number of corners: boundary vertices whose run isn't a straight
angle (run length ≠ 4 at A/B points, ≠ 2 at C points). For a strictly simple
room, `W` is the number of polygon vertices, so odd `W` is possible. `N` is the
number of tiles.

A pair is two distinct interior points of the same class. Eligible rooms
have at least one pair. The census treats A/B pairs (8-tile points) and C
pairs (4-tile points) separately.

## Pipeline

| Step | Program | What it does |
|---|---|---|
| Enumerate | `enum45.c` | Star-growth enumeration of rooms with a pair (modes `star`, `cstar`), and plain enumeration of all rooms (mode `plain`). |
| Filter | `shoot45.c` | Builds the 8-fold unfolding as an origami of `4N` unit squares. Shoots every primitive `(p, q)`, `p + q ≤ 40` (491 directions), from all 8 lifts of S. Computes `k` and the N_min separation. |
| Re-check lit | `verify45.c` | Independent exact tracer in the room plane. It replays every LIT certificate `(S, direction, m steps, T)`. |
| Decide | `orbit45.c` | Complete SL(2, Z)-orbit decider for a marked origami (port of d9's `orbitc.c`). |
| Second decider | d6's `validate_rooms.decide_room` | Pure-braid Hurwitz decider on the triangle pull-back, read in place. |
| Describe | d4's `monodromy.analyse_room` | Block systems, read in place. |

Every step uses integer arithmetic. The tracer scales positions by
`M = lcm(|dx|, |dy|, |dx + dy|, |dx − dy|)` and stops at the first lattice point
on a corner, so a lit verdict is an explicit legal billiard path. A dark verdict
needs a finished orbit (`orbit45` DARK, or d6 "full orbit exhausted").

### Unfolding details

Face `(t, g)` of the unfolding develops to `g(t)`. Across an interior edge,
`(t, g)` is glued to `(t', g)`; across a wall `e`, to `(t, g ρ_e)`. Pairing faces
across the hypotenuse gives unit squares. Each square is labelled with the
room point at its bottom-left corner. `shoot45` asserts that `h` and `v` are
permutations, that labels agree, and that every interior point has exactly 8
lifts.

Rooms with only axis-parallel walls (polyominoes) generate only a Klein
four-group of reflections. Their unfolding has two mirror-image components, so
`orbit45` keeps the component of the first lift of S.

### N_min and k

`k` is the number of transparent (interior or flat boundary) lattice points
of the two classes other than the pair's class.

N_min is the triangle-framework parity factor: sheets are tiles, and
`g_A = κ_AC κ_AB`, `g_B = κ_BC κ_AB`, `g_C = κ_AC κ_BC`. Forced unions kill every
regular point over the two other classes (a 4-cycle over A or B gives
`x ~ g²x`; a 2-cycle over C gives `x ~ g x`). The unions are closed under the
generators and iterated to a fixed point; each round collects its unions on
the closed partition before applying them. The pair is separated if no
induced `g_X` cycle contains images of both S and T.

## Completeness of the enumeration

### A/B pairs (`enum45 star`)

Take a strictly simple room with `N ≤ NMAX` tiles and an A/B pair.

1. **Canonical embedding.** Over all ordered same-class A/B pairs `(S', T')`
   and all `g ∈ D4` with `g(T' − S') = (2a, 2b)`, `a ≥ 1`, `0 ≤ b ≤ a`, take the
   lexicographic minimum of `((a, b), sorted tile ids of the image with S' at
   the origin)`. The map `x ↦ g(x − S')` is in G for A and B points alike. It
   places the room with `S = (0, 0)` and `T = (2a, 2b)` both interior A points.
   So the placed room contains `star(S) ∪ star(T)`, which are disjoint.
2. **Growth.** Redelmeier's algorithm rooted at the 8 tiles of `star(S)`
   lists every connected tile set that contains `star(S)` exactly once.
3. **Pruning.** A subtree is cut only when no set in it can qualify:
   - A tile of `star(T)` was already rejected in this branch.
   - Or `|R| + (8 − |star(T) ∩ R|) + max(0, δ − 1) > NMAX`. Here `δ` is the
     minimum breadth-first tile distance from the current set `R` to
     `star(T)`. Any completion must add the missing `star(T)` tiles and at
     least one tile at each distance `1 … δ − 1`; those tiles aren't in `R`,
     because every tile of `R` has distance at least `δ`.
4. **Vectors.** `enum45 dlist NMAX` lists every `(a, b)` whose two stars fit
   in `NMAX` tiles (`16 + δ0 − 1 ≤ NMAX`). The census runs all of them.
5. **Acceptance.** A room is written only if no embedding beats the current
   one. The minimum key fixes the tile set, so each room is written exactly
   once over all vectors.

`enum45 dlist 32` gives 13 vectors: (1,0) 16, (1,1) 18, (2,0) 20, (2,1) 21,
(2,2) 24, (3,0) 24, (3,1) 25, (3,2) 27, (3,3) 30, (4,0) 28, (4,1) 29, (4,2) 31,
(5,0) 32 (the number is the minimum room size). `enum45 cdlist 24` gives 21
C vectors.

### C pairs (`enum45 cstar`)

The argument is the same, with `S = (1, 0)`, `T = (1 + U, V)`, `U ≥ 1`,
`0 ≤ V ≤ U`, `U + V` even, and 4-tile stars. Every tile has exactly one
right-angle vertex, so distinct C stars are disjoint. G acts transitively on
C points, and the stabiliser of a C point is all of D4.

### Cross-checks

| Check | Result | Log |
|---|---|---|
| Plain enumeration (`enum45 plain`) against an independent Python brute force (mirror-image growth, boundary-cycle walk), `n ≤ 12`: fixed, free, rooms per `(n, W)`, eligible per `(n, W)` | all match | `check_enum_small_12.log` |
| Free tetrakis animals, `n = 1 … 12` | 1, 2, 2, 6, 8, 22, 42, 112, 252, 650, 1584, 4091 | same |
| Strictly simple rooms, `n = 1 … 12` | 1, 2, 2, 6, 8, 22, 42, 112, 251, 641, 1542, 3921 | same |
| Star growth (`star`, `cstar`) against plain enumeration, `8 ≤ N ≤ 20`, `W ≤ 22`, identical canonical room lines | match (583 A/B rooms, 1,906,325 C rooms) | `xcheck/` |
| 3-way job split against 1 job, `N ≤ 12` | identical rooms (md5) | — |
| Rooms written by `enum45` equal rooms read by `shoot45`, per `(N, W)` | equal in every chunk | `agg45.py` asserts |
| `star-30` (16 chunks per vector) against the `N ≤ 30` part of `star-32` (32 chunks per vector) | identical `totals.tsv` rows | — |

The plain enumeration shares no growth or pruning code with star growth: it
uses 4 roots modulo the translation lattice and full canonical forms.

## Reproduce

Build (Apple clang, no other dependencies):

```sh
clang -O3 -march=native -o enum45 enum45.c -lm
clang -O3 -march=native -o shoot45 shoot45.c verify45.c -lm
clang -O3 -march=native -o orbit45 orbit45.c
clang -O3 -march=native -o negtest45 negtest45.c verify45.c
```

Enumeration checks (run in bash; zsh doesn't split `$v`):

```sh
./enum45 plain 12 99 1 1 1 0 0 /tmp/e12.txt e12.counts
python3 -B check_enum_small.py 12 e12.counts > check_enum_small_12.log
./enum45 plain 15 22 8 0 1 0 0 /tmp/p15.txt /tmp/p15.counts
for j in 0 1 2; do ./enum45 plain 20 22 16 0 3 $j 6 /tmp/p20_$j.txt xcheck/p20_$j.counts; done
for v in "1 0" "1 1" "2 0"; do set -- $v; ./enum45 star 20 22 $1 $2 1 0 0 /tmp/xs_$1_$2.txt /dev/null; done
./enum45 cdlist 20 | while read u v n; do ./enum45 cstar 20 22 $u $v 1 0 0 /tmp/xc_${u}_$v.txt /dev/null; done
python3 -B xcheck45.py 8 15 /tmp/p15.txt -- /tmp/xs_*.txt -- /tmp/xc_*.txt > xcheck/xcheck_8_15.log
python3 -B xcheck45.py 16 20 /tmp/p20_*.txt -- /tmp/xs_*.txt -- /tmp/xc_*.txt > xcheck/xcheck_16_20.log
```

Validation (about 9 minutes; `orbit45` cap 3,000,000 states):

```sh
python3 -B validate45.py > validate45.log
```

Census (checkpointed: rerunning skips finished chunks), aggregation, and
decision of every survivor:

```sh
python3 -B census45.py run star 32 24 4 32 > census_star32.log     # 1,893 s wall after resuming, 4 workers
python3 -B census45.py run cstar 24 24 2 16 > census_cstar24.log   # 913 s wall after resuming, 2 workers
python3 -B census45.py run star 30 24 2 16 > census_star30.log     # optional: 1,036 s, consistency run
python3 -B agg45.py census/star-32 > agg_star32.log
python3 -B agg45.py census/cstar-24 > agg_cstar24.log
python3 -B decide45.py 3000000 24 census/star-32/survivors.txt > decide_star32.log
python3 -B tables45.py census/star-32 census/cstar-24
```

Each census command pipes `enum45` into `shoot45`, so room lines never reach
the disk. A chunk takes at most about 5 minutes. To pause, stop the driver;
to resume, rerun the same command.

C-pair midpoint tally (question d):

```sh
./enum45 star 24 24 1 0 1 0 0 /dev/stdout /dev/null | ./shoot45 40 99 - /tmp/cm.out /dev/null
python3 -B cmid45.py /tmp/cm.out > cmid/cmid_star24_T10.txt
```

## Files

| File | Contents |
|---|---|
| `enum45.c` | Enumeration: `plain`, `star` (A/B), `cstar` (C), `dlist`, `cdlist` |
| `shoot45.c`, `verify45.c` | Origami, exact shooting, `k`, N_min; independent plane tracer |
| `orbit45.c` | Complete orbit decider (keeps one component of a disconnected unfolding) |
| `negtest45.c` | Tracer negative test |
| `rooms45.py` | Tile helpers, Python boundary walk, record rooms, wrappers for d6 and d4 |
| `check_enum_small.py`, `check_enum_small_12.log`, `e12.counts` | Brute-force check of `plain`, `n ≤ 12` |
| `xcheck45.py`, `xcheck/` | Star growth against plain enumeration, `N ≤ 20` |
| `validate45.py`, `validate45.log`, `validate45.err`, `validate45.json`, `validation/` | Validation |
| `census45.py`, `census_*.log` | Census driver and run logs (`*.part1.log`: runs stopped and resumed from checkpoints) |
| `census/star-32/`, `census/star-30/`, `census/cstar-24/` | Per-chunk counts and shooter statistics, `totals.tsv`, `rooms.tsv`, `khist.tsv`, `table_WN.tsv`, `survivors.txt`, `decide45.json` |
| `agg45.py`, `agg_*.log` | Aggregation and its checks |
| `decide45.py`, `decide_star30.log`, `decide_star32.log` | Survivor decisions and descriptions |
| `tables45.py` | Per-`(W, N)` tables |
| `cmid45.py`, `cmid/` | Midpoint classes of lit certificates |

`census/star-30` is the first completed run (`N ≤ 30`, 16 chunks per
vector). Its totals equal the `N ≤ 30` part of `census/star-32`, which used
32 chunks per vector.
