# d42: thickening the slit in Monteil's slit room

## Verdict

No thickening is dark. Every strictly simple thickening with `W <= 22` that
was built (872 thick-wall variants, k = 1 to 12; 1,373 further resolutions,
k = 1 to 8) has every pair of interior lattice points lit. Each lit verdict
comes from an explicit billiard path. There's no counterexample to the
22-wall conjecture here.

The slit room itself is dark for its marked pair. The fold (Tokarsky)
argument proves it, and two tracers agree to their bounds. The scaled slit
rooms (k = 1 to 12) each have exactly one unlit lattice pair: the scaled
marks.

## The slit room

Read from the vector data of Monteil, *Transparent blocking*, page 5
(`monteil_p5.trace`, `mutool draw -F trace`). The PDF uses 8 units per
lattice unit. The coordinates below flip the PDF's y axis so that y points
up.

Outer polygon, counter-clockwise (17 corners):

`(0,2) (1,2) (1,1) (2,0) (2,1) (4,1) (4,0) (5,1) (5,2) (6,2) (5,3) (4,3) (4,4) (3,3) (2,4) (2,3) (1,3)`

- Slit: `(3,1)–(3,2)`. The foot `(3,1)` is a flat point of the bottom wall
  `(2,1)–(4,1)`; the tip `(3,2)` is inside the room.
- Marks: red `S = (2,2)`, green `T = (4,2)`.
- Area 11, so 22 tiles of the canonical45 tiling. All diagonal walls lie on
  lines with `x ± y` even.

```
4         o       o
          | \   / |
3     o---o   o   o---o
    /                   \
2 o---o   S   +   T   o---o
      |       |       |
1     o   o---+---o   o
        \ |       | /
0         o       o
  0   1   2   3   4   5   6
```

`+` marks the slit tip `(3,2)` and the slit foot `(3,1)`.

Side count:

| Convention | Count |
|---|---:|
| Corners (17 outer corners, plus the slit foot and tip) | 19 |
| Sides, slit as 1 side (the foot splits the bottom wall: 18 outer segments + 1) | 19 |
| Sides, slit as 2 sides | 20 |

This matches Monteil's "19 or 20 sides". Without the slit the room has 17
walls and all 3 interior lattice points are lit (direction `(1,0)`, 2 steps).

Sanity checks (`verify_slit.py`, log `work/verify_slit.log`):

- The room is a union of 22 canonical45 tiles, so it's a union of reflected
  45-45-90 triangles. The marks are A points (`(even, even)`, angle π/4), the
  images of an acute vertex.
- Tokarsky's condition holds. Every B point (`(odd, odd)`) and every C point
  (mixed parity) of the closed room is a polygon corner, the slit foot, or
  the slit tip. The only interior lattice points are the two marks.

## Darkness of the slit room

| Method | Result |
|---|---|
| Fold argument | Proof. Folding the room onto the 45-45-90 triangle maps a billiard path from S to T to a path from the π/4 vertex A back to A. Every B and C point of the room is a corner, so the folded path can't pass through B or C. Tokarsky's lemma says no billiard path in that triangle returns from A to A. So no path joins S and T. |
| Origami shooter (`shootall`, slit edges glued as walls) | No witness among 48,679 primitive directions with `p + q <= 400` (all 8 lifts of S). |
| Independent plane tracer (`slit45.trace` logic, Fractions) | All 1,112 primitive directions with `\|dx\| + \|dy\| <= 30` from S die at a corner within 300 reflections; none reaches T. The same tracer without the slit reaches T in direction `(1,0)`. |
| `orbit45` (exact orbit decider, 88 squares) | UNDECIDED at the 3,000,000-state cap. This is the same behaviour as Castro's and Tokarsky's clean rooms in d11. |

## Thickenings

Scale the room by k: polygon `k · P`, slit from `(3k, k)` to `(3k, 2k)`, marks
`(2k, 2k)` and `(4k, 2k)`. Replace the slit by a convex obstacle that stands on
the bottom wall `y = k`:

- Box `[xl, xr] × [k, top]`, width `w = xr − xl >= 1`, with `xl <= 3k <= xr`.
  `place` is `left` (`xr = 3k`), `right` (`xl = 3k`), `centred`, or `offset`.
- End shapes: `flat`; `up` (one 45° face rising to the right); `down` (one
  45° face falling to the right); `roof` (two 45° faces, w even). When the
  45° face is longer than the wall height, the obstacle becomes a triangle.
- `thick`: `top = 2k`, so the tip stays at the slit tip. Every obstacle
  contains the slit segment and doesn't contain the marks.
- Other resolutions (`other-top-1`, `other-top+1`): the same shapes with
  `top = 2k − 1` (shortened) or `top = 2k + 1` (lengthened). The obstacle may
  reach past the bottom wall and merge with the side walls of the two spikes
  (`xl <= 2k` or `xr >= 4k`). That covers the "notch that reaches the
  boundary differently" case.
- Coordinates stay integer. If a 45° face lies on a line with `x ± y` odd,
  the room is doubled internally to fit the canonical45 tiling (`c = 2` in
  `results.tsv`). Only points of the room's own integer lattice are paired.

The run keeps a variant only if the room is a strictly simple lattice
polygon: connected, one boundary cycle, no pinch (d11's `rooms45.boundary`
plus a connectivity check). Both marks must be interior, and `W <= 22`.
Duplicates of the same obstacle are removed.

## Method

1. `slit45.build` builds the 8-fold unfolding as an origami of `4N` unit
   squares, porting d11's `shoot45` construction. Slit edges are glued as
   walls. A sector analysis types the lattice points. An interior point has
   no wall through it. A flat point is one run of angle π. Every other wall
   point is a corner where paths die, including the slit tip (one run of 2π)
   and the slit foot.
2. `shootall` (C) runs, for every primitive `(p, q)` with `p, q >= 0` and
   `p + q <= BOUND`, the one-step map F (Christoffel word). It cuts each
   cycle of F at corner squares. Any two lattice points on one corner-free
   segment are joined by a billiard path. The lit relation over all interior
   integer points (all parity classes) is accumulated as bitsets.
3. For the scaled marks, `shootall` also records the first witness (smallest
   `p + q`) and the shortest one (minimum Euclidean length). Both are replayed
   by the independent plane tracer `slit45.trace`, which also counts
   reflections and records which walls the path hits.
4. Bounds: 40 for k <= 8, 60 for k = 9 to 12 (thick only). Rooms with an
   unlit pair were rerun at 150 (k = 6, 8) or 200 (k = 9 to 12).
5. No thickening needed an exact decider: after the reruns every pair was
   lit with a path. `orbit45` was used only on the k = 1 slit room. The other
   origamis exceed its 255-square limit, or were already fully lit.

## Results

Every count covers all pairs of interior integer points in all parity
classes. That's a superset of the pairs in the marks' class, and it includes
the marks and their neighbours. `max p+q` is the largest direction bound
needed before the last pair in a variant was lit.

| k | kind | variants | W <= 21 | min W | pairs tested | dark or unlit pairs | max p+q | method |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | slit | 1 | 1 | 19 | 1 | 1 (marks, dark) | - | fold proof; shooting 400 |
| 1 | thick | 3 | 3 | 18 | 3 | 0 | 10 | lit certificates |
| 2 | thick | 9 | 8 | 18 | 2,326 | 0 | 19 | lit certificates |
| 3 | thick | 17 | 15 | 18 | 35,360 | 0 | 29 | lit certificates |
| 4 | thick | 27 | 24 | 18 | 216,194 | 0 | 36 | lit certificates |
| 5 | thick | 39 | 35 | 18 | 850,033 | 0 | 35 | lit certificates |
| 6 | thick | 53 | 48 | 18 | 2,565,676 | 0 | 65 | lit certificates |
| 7 | thick | 69 | 63 | 18 | 6,487,054 | 0 | 37 | lit certificates |
| 8 | thick | 87 | 80 | 18 | 14,440,828 | 0 | 46 | lit certificates |
| 9 | thick | 107 | 99 | 18 | 29,200,047 | 0 | 41 | lit certificates |
| 10 | thick | 129 | 120 | 18 | 54,763,866 | 0 | 72 | lit certificates |
| 11 | thick | 153 | 143 | 18 | 96,673,324 | 0 | 41 | lit certificates |
| 12 | thick | 179 | 168 | 18 | 162,363,182 | 0 | 79 | lit certificates |
| 2–8 | other-top−1 | 889 | 868 | 17 | 63,982,723 | 0 | 28 | lit certificates |
| 2–8 | other-top+1 | 484 | 402 | 18 | 36,109,339 | 0 | 36 | lit certificates |
| 2–12 | slit (scaled) | 11 | 11 | 19 | 3,039,399 | 1 each (the scaled marks) | - | dark by similarity; all other pairs lit |

Wall counts of the thick variants: 770 with `W = 21`, 24 with `W = 19`, 12
with `W = 18`, and 66 with `W = 22`. The `W = 18` and `W = 19` rooms are the
triangle and roof ends (for example, `up` with `w = k` is the triangle
`(2k,k) (3k,k) (3k,2k)` with `W = 19`). The `other-top−1` rooms are lit
trivially along `y = 2k`, because the obstacle stays below the marks.
Per-variant rows are in `results.tsv`.

At bound 40 or 60, some pairs were still unlit at k = 6, 8, 10 and 12: up to
73 pairs in the k = 6 slit room and up to 38 in its thickenings. All of them
were lit at bound 150 or 200, except the scaled marks in the slit rooms
(`work/rerun150.jsonl`, `work/rerun200.jsonl`). A low bound isn't enough at
large k; the needed `p + q` grows roughly like k.

## Witness complexity for the scaled marks

Every shortest witness reflects off the thick wall: in all 872 thick
variants, the path touches a face of the obstacle. Across the variants, the
shortest witness has length 7.62k to 21.6k and 4 to 14 reflections (median 4
to 7 for each k). Columns: direction in room coordinates (doubled when
`c = 2`), steps m, reflections r, and the face sequence (`E` end face, `S`
side face, `o` other wall).

| Family | Shortest witness, by k | Behaviour |
|---|---|---|
| `left`, `flat`, w = 2 | k = 4 to 12: direction `(2k − 1, −k)`, 4 reflections, `Sooo` | First reflection on the side face facing S. Fixed reflection count; `p + q = 3k − 1` grows linearly. |
| `left`, `flat`, w = 1 | k = 2 to 6, 9, 10: `(4k − 1, −2k)`, 4 reflections, `Sooo`; k = 7, 8, 11, 12: 6 or 8 reflections, side face | Direction complexity ≈ `6k / w`. The slope tends to −1/2 as `w / k → 0`. |
| `centred`, `flat`, w = 2 | k = 3 to 12: direction `(1, 4)`, 7 reflections, `oooEooo` | The path reflects at `(3k, 2k)`, the old slit tip, now a flat point of the end face. In the slit room that point is a corner, and the same path dies there. |
| `left`/`centred`, w = k/2 or w = k, flat | `(7, −4)`, 4 reflections, `Sooo`, for every even k | Similar rooms (fixed `w / k`) give the same path, scaled. |
| `left`, `up`, w = k (triangle, W = 19); `centred`, `roof`, w = 2k (W = 18) | `(3, −7)`, 4 reflections, `Eooo`, every k | First reflection on the 45° end face. |

So two mechanisms light the marks:

- The end face turns the slit tip into a mirror. The fixed-direction path
  through the old tip then survives, and its complexity doesn't depend on k.
- A narrow wall away from the tip gives a side-face reflection. That path
  has 4 reflections, and its direction complexity grows like `k / w`.

Complexity stays bounded only in the first case and for fixed `w / k`. Under
the shortest-length criterion, no family needed more than 14 reflections.

## Validation

- Known dark rooms through the same pipeline: the 22-wall room, Castro's
  room, and Tokarsky's room each have their marked pair unlit at bound 40.
- Witness replay: for 280 sampled lit pairs (`validate42.py`, k = 1 to 8),
  both witnesses were replayed by the independent plane tracer: 560 of 560
  accepted. Negative tests (target moved to another point, or direction
  rotated 90°) were rejected 1,119 of 1,120 times. The one accepted negative
  case is a rotated direction that is also a legal path, which d11 also saw.
  Logs: `work/validate_k1-4.log`, `work/validate_k5-8.log`.
- Every shortest and first witness for the scaled marks, in every variant,
  replayed in the plane tracer (`replay` column in `results.tsv`).
- Each scaled slit room has exactly one unlit pair, which matches the
  similarity argument.

## Not verified

- The lit verdicts for pairs other than the scaled marks rely on
  `shootall`'s segment logic. Only 280 sampled pairs were replayed in the
  plane.
- Only points of the room's integer lattice were tested. Other rational
  points of the thickened rooms (for example, half-integer points of the
  doubled rooms) weren't tested.
- Darkness of the slit room rests on the fold argument and on bounded
  tracing. `orbit45` didn't finish (3,000,000 states).
- Scope: k <= 12 for thick walls, k <= 8 for the `top ± 1` resolutions. Only
  the end shapes listed above were built: flat, one 45° face, or two 45°
  faces. Partial chamfers have more walls and weren't built. Rooms with
  `W > 22` were discarded.

## Resource use

| Item | Use |
|---|---|
| Compute | About 1,150 CPU seconds. Runs between 12:39 and 12:57 (about 18 minutes of wall clock), well under 60 minutes. |
| Concurrency | At most 3 CPU-busy processes. The OS process count was higher: the idle `multiprocessing` parent, and Python workers blocked while their `shootall` child ran. |
| Memory | Not measured. The largest origami has 22,528 squares; each process stayed well under 1 GB. |
| Output | Largest file 1.5 MB (`work/k6-8.jsonl`); directory total 4.8 MB. |

Runs: `k4` 7 s, `k5` 10 s, `k6-8` 93 s, `rerun150` 34 s, `k9-12` 155 s,
`rerun200` 243 s, validation 330 s, `orbit45` 28 s, `verify_slit` 3 s.

## Files

| File | Contents |
|---|---|
| `slit45.py` | Origami with slit walls, sector typing, `orbit45` line, independent plane tracer |
| `rooms42.py` | The room, scaling, obstacles, `analyse` |
| `shootall.c` | All-pairs shooter with witnesses for the marked pair |
| `run42.py`, `rerun42.py` | Variant enumeration and runs; reruns at a larger bound |
| `verify_slit.py` | Darkness checks for the k = 1 slit room |
| `validate42.py` | Sampled witness replay and negative tests |
| `report42.py`, `results.tsv` | Per-variant table and aggregates |
| `rooms45.py`, `orbit45.c` | Copied from d11 unchanged |
| `monteil_p5.trace` | Vector trace of the slide |
| `work/` | JSONL results and logs per run, origami files, `orbit45` input |

## Reproduce

```sh
clang -O3 -march=native -o shootall shootall.c
clang -O3 -o orbit45 orbit45.c
python3 -B verify_slit.py 400 30 300 > work/verify_slit.log
./orbit45 3000000 < work/slit_k1.orbit
python3 -B run42.py 4 40 work/k4.jsonl 2
KMIN=5 python3 -B run42.py 5 40 work/k5.jsonl 2
KMIN=6 python3 -B run42.py 8 40 work/k6-8.jsonl 2
KMIN=9 KINDS=thick python3 -B run42.py 12 60 work/k9-12.jsonl 2
python3 -B rerun42.py 150 work/rerun150.jsonl work/k6-8.jsonl
python3 -B rerun42.py 200 work/rerun200.jsonl work/k9-12.jsonl
python3 -B validate42.py 3 20 4 40 work/k4.jsonl > work/validate_k1-4.log
python3 -B validate42.py 7 40 5 150 work/k6-8.jsonl work/k5.jsonl > work/validate_k5-8.log
python3 -B report42.py results.tsv work/rerun200.jsonl work/rerun150.jsonl work/k4.jsonl work/k5.jsonl work/k6-8.jsonl work/k9-12.jsonl
```
