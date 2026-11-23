# d29: rigidity test (dark rooms with a run)

Opus 5.5 subagent, 2026-11-10. Daniel approved this small test. Nobody has
reviewed it.

## Question

Rigidity conjecture: a same-class pair (S, T) is lit whenever the room has a
*run*. A run is two adjacent identical cell rows (or columns). The lattice
line between them then has no vertex, and that line must not be the row
(column) of S or T. This test looks for a dark room that has a run.

## Result

No counterexample. Every dark room found has no run, and every dark room
found has a vertex on every interior lattice line outside the rows and
columns of S and T.

| Family | Scope | Dark rooms | With a run | Vertex on every line |
| --- | --- | --- | --- | --- |
| Orthogonal | strictly simple, W <= 24, area <= 19 | 1 (the 22-wall room, area 15) | 0 | 1 of 1 |
| 45-degree | the 12 clean 24-wall rooms of d11 | 12 | 0 | 12 of 12 |

Because no dark room has a run, step 3 (stretch the run to g = 2..5) had
nothing to act on.

## Orthogonal census (CHECKED)

- Pipeline: d9's `enum_rooms 19 24 1 0 | shoot 40 0`, read in place. Every
  pair that the shooter lights has a certificate replayed by
  `verify_plane.c` (`verify_fail 0`).
- 545,201,856 rooms, 60,524,192 eligible rooms, 70,665,634 same-class pairs.
  Exactly 1 pair survives shooting. orbitc decides it DARK (2,592 states). It
  is the 22-wall room's pair, (1,3)-(3,5) (`ortho_a19.log`).
- W = 24: 193,043,132 rooms, 10,930,380 eligible, 11,321,897 pairs, all lit.

| Area (W = 24) | 14 | 15 | 16 | 17 | 18 | 19 |
| --- | --- | --- | --- | --- | --- | --- |
| Eligible rooms | 5 | 298 | 10,243 | 143,483 | 1,345,503 | 9,430,848 |
| Pairs | 5 | 298 | 10,259 | 144,151 | 1,367,800 | 9,799,384 |
| Dark | 0 | 0 | 0 | 0 | 0 | 0 |

- Cross-check: the W <= 22 rows reproduce d9's eligible counts (area 18, W 22:
  2,611,743; area 19, W 22: 13,341,095). `lit_but_separated` is 0, so
  "dark iff N_min separates" still holds.
- Control: the 22-wall room comes out DARK with no run (`control22.log`).

## Diagonal rooms (CHECKED)

`diag45.py` reads the 12 polygons from `../d11-census-45/README.md`, with
S = (0, 2) and T = (0, 6). Box 4 x 8. Lines tested: y = 1, 3, 4, 5, 7 and
x = -1, 1. Each line holds a polygon vertex in all 12 rooms, so no run exists
(`diag45.log`). Their darkness rests on d11's clean-parity lemma (k = 0), not
on a finished orbit.

## Run tests

- Orthogonal (`ortho.py`): a line is a run line when no lattice point on it
  has 1 or 3 cells around it.
- Polygon (`runs_poly.py`): no vertex on the line, and every edge that crosses
  it is vertical. A diagonal edge that crosses a vertex-free line therefore
  blocks a run.
- Controls (`runs_poly_controls.log`): the 22-wall room has none; a 3 x 5
  rectangle and a capped pentagon give the expected lines. `ortho.stretch`
  equals d28's `stretch.py` on all 36 control cases tried.

## Not covered

- Orthogonal rooms with area >= 20 at W = 24, and area >= 21 at W <= 22. A
  room with a run is a stretch of a room with smaller area. So this census
  covers only runs whose contracted room has area <= 18.
- 45-degree rooms beyond d11's 12 clean rooms (d11 found no other dark room
  at W = 24 within N <= 32 tiles), and C pairs.
- W = 23 orthogonal rooms don't exist (W = 2r + 4).

## Files and compute

- `ortho.py`, `runs_poly.py`, `diag45.py`: scripts.
- `runs/a18.*`, `runs/a19.*`: census outputs (the a19 run includes a18).
- `ortho_a18.log`, `ortho_a19.log`, `control22.log`, `diag45.log`.
- Compute: about 36 minutes wall-clock, one census pipeline (2 processes) at
  a time, under 1 MB. A first launch with 3 parallel pipelines was stopped
  after 1 minute because it used about 6 processes.
