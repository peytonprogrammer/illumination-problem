# d53: resolving the pinch in Monteil's 22-sided room

## Verdict

No resolution is dark. Every strictly simple resolution of the pinch that was
built (5,867 rooms, k = 1 to 12) has every pair of interior lattice points
lit, and each lit verdict comes from an explicit billiard path. Of these, 500
rooms have `W <= 21` and 666 have `W = 22`. There's no counterexample to the
22-wall conjecture and no second minimal example here.

The pinched room itself is dark for its marked pair under both treatments of
the touching point. The convention doesn't matter: the fold argument shows that
no billiard path from either mark ever reaches the touching point.

## The room

Read from the vector data of Monteil, *Transparent blocking*, page 4
(`monteil_p4.trace`, `mutool draw -F trace`). The room is a single stroked
path with transform `3 0 0 3`, so y already points up. Lattice coordinates are
`((x − 0.977) / 8, (y − 0.965) / 8)`. The marks are filled discs drawn with a
flipped transform; their centres map to the lattice points below.

Boundary walk, clockwise, 22 vertices (the pinch `Q = (4,4)` appears twice):

`(1,4) (1,5) (2,6) (2,5) (3,5) (4,4) (3,4) (3,3) (4,3) (4,4) (5,3) (5,2) (6,2) (5,1) (4,1) (4,0) (3,1) (3,2) (2,2) (2,3) (1,3) (0,4)`

- Marks: red `S = (2,4)`, green `T = (4,2)`. Both are A points (even, even).
- Pinch: `Q = (4,4)`, also an A point. The unit square `[3,4] × [3,4]` is
  not part of the room. Its corner touches the straight diagonal wall
  `(3,5)–(5,3)` at its midpoint `Q`. The room is an annulus around this square
  hole, closed off at `Q`.
- Two 45° wedges of the room meet at `Q`: R1 (triangle `(3,4) (4,4) (3,5)`,
  above the hole) and R2 (triangle `(4,3) (4,4) (5,3)`, right of the hole).
- Area 12, so 24 canonical45 tiles. Every diagonal wall lies on a line with
  `x ± y` even. The room is symmetric in `y = x`, which swaps S and T.

```
6           o
          / |
5       o   o---o
        |         \
4   o---o   S   o---Q
      \         | # | \
3       o---o   o---o   o
            |           |
2           o---o   T   o---o
                |         /
1               o   o---o
                  \ |
0                   o
    0   1   2   3   4   5   6
```

`#` is the square hole. `Q` is the touching point.

Side count:

| Convention | Count |
|---|---:|
| Sides of the closed boundary walk, with `Q` visited twice (Monteil's count) | 22 |
| Distinct corner points (`Q` once) | 21 |
| d11's boundary-cycle count: outer cycle (the wall `(3,5)–(5,3)` is straight through `Q`) plus the hole cycle, 17 + 4 | 21 |

No two consecutive sides of the walk are collinear, so the 22 sides are 22
walls. At `Q`, the walk turns twice: once at the tip of R1 and once at the tip
of R2.

## Darkness of the pinched room

Two treatments of `Q`:

- **die**: `Q` is a vertex, and a path that reaches it stops. This is the
  standard rule and the origami's sector analysis (two separate runs of tiles
  at `Q`).
- **reflect**: `Q` is a flat point of the straight wall `x + y = 8`, which the
  hole's corner only touches. A path that reaches `Q` reflects in that wall
  and passes from one wedge into the other. A straight continuation through
  `Q` would leave the room, so there's no third option.

| Method | Result |
|---|---|
| Fold argument (both conventions) | Proof. The room is a union of 24 canonical45 tiles. Every B point (odd, odd) and every C point (mixed parity) of the closed room is a corner (`verify_pinch.log`, check 1), and the only interior lattice points are S and T. Folding onto the 45-45-90 triangle sends S, T and `Q` to the same π/4 vertex A. Take any path from S, and stop it at the first A point it reaches. That prefix avoids every B and C point, so it folds to a billiard path from A back to A, which Tokarsky's lemma rules out. So no path from S reaches T, and none reaches `Q` either. Since the reflect rule only acts at `Q`, both conventions have the same paths from S, and the pair is dark in both. |
| `orbit45` (exact orbit decider, 96 squares, die convention) | DARK, 48 states (`work/orbit_k1.log`). |
| Origami shooter (`shootall`, die convention) | No witness among 48,679 primitive directions with `p + q <= 400`. |
| Independent plane tracer, both conventions | From S and from T, all 1,112 primitive directions with `\|dx\| + \|dy\| <= 30`: every path dies at a corner within 300 reflections. None reaches the other mark, and none visits `Q`, under either convention. A control ray from `(3, 9/2)` in direction `(2, −1)` does reach `Q`: it stops under die and reflects into R2 under reflect. |
| Scaled pinched rooms, k = 2 to 12 | Exactly one unlit pair each (the scaled marks), after reruns at bound 150. Dark by similarity. |

The darkness of the pinched room for S and T is proved for both conventions.
The `orbit45` decision covers only the die convention.

## Resolutions

### What a strictly simple resolution must do

Near `Q`, four sectors meet: R1 (135° to 180°), the hole (180° to 270°), R2
(270° to 315°), and the exterior (315° to 135°). There are two ways to stop
the boundary from touching itself:

- Join R1 and R2 (open a doorway between the wedges, or pull the hole away
  from the wall). Then the hole becomes a real hole, and the room is no longer
  simply connected. None of these is strictly simple. The `door(w)` family and
  the shifts that move the hole away from the wall check this. Every one of
  them was rejected as not simple.
- Put wall material between the wedge tips, so the hole joins the exterior at
  `Q`. The hole then becomes a notch cut into the room from the diagonal wall.
  Every strictly simple resolution is of this kind.

### Families built

Scale k: room `k · P`, `Q = (4k, 4k)`, hole `[3k, 4k]²`, marks `(2k, 4k)`
and `(4k, 2k)`. One-sided shapes are cut from R1. The R2 versions are mirror
images in `y = x` with S and T swapped, so they have the same verdicts and
weren't rerun. All coordinates are integers, and all diagonals lie on even
lines, so every room is a union of canonical45 tiles at scale 1.

| Family | Definition | k |
|---|---|---|
| `V(w)` | Vertical cut `x = 4k − w` across R1, `1 <= w <= k`. `V(k)` removes all of R1 and equals `T(k)`. | 1–12 |
| `D(a)` | 45° chamfer of R1 along `x − y = −2a`, from the wall point `(4k − a, 4k + a)` to the hole top `(4k − 2a, 4k)`, `1 <= 2a <= k`. | 2–12 |
| `T(s)` | Hole's top wall raised to `y = 4k + s` inside R1 (a shifted wall), `1 <= s <= k`. | 1–12 |
| two-sided `A\|B` | Shape A on R1 and shape B on R2, both tips cut. Unordered up to the mirror. `D(a)\|D(a)` is a symmetric doorway along `(1, 1)` that joins the hole to the exterior. | 1–12 |
| `shift(s1, s2)` | Hole translated by `(s1, s2)`, `−1 <= s1 <= s2 <= k − 1`. Shifts that cross the wall merge the hole with the exterior. Shifts away from the wall give an annulus. | 1–12 |
| `door(w)` | Exterior tiles within `w` of `Q` added, joining R1 and R2. | 1–3 |
| `plug1` | Every subset of R1's `k²` tiles that contains the tip tile and leaves a strictly simple room. | 2–4 |
| `plug2` | Every pair of `plug1` cuts, one on each wedge. | 2–3 |
| `win1` | k = 1: all 255 nonempty toggles (add or remove) of the 8 tiles in `[3,5]²`. | 1 |

Duplicate rooms are removed: a room keeps the first name that produced it, so
`plug1` and `plug2` list only the shapes that aren't `V`, `D` or `T`.

### Method

1. `rooms53.check`: connected, one boundary cycle with no pinch (d11's
   `rooms45.boundary`), and both marks interior. `W` is the corner count of
   the cleaned boundary cycle.
2. `slit45.build` (from d42) builds the 8-fold unfolding as an origami.
   `shootall` (from d42) lights all pairs of interior integer points in all
   parity classes, and records the first and the shortest witness for the
   marks.
3. Both witnesses for the marks are replayed by the independent plane tracer
   (`slit45.trace`, Fractions). The face string marks each reflection as `N`
   (a wall made by the resolution) or `o` (an original wall). `dQ2` is the
   squared minimum distance from the path to `Q`.
4. Bounds: 40 for k <= 4, 60 for k = 5 to 12. Every room with an unlit pair
   was rerun with no designated pair, at 150 (k <= 8), 120 (k = 10) or 200
   (k = 12), until every pair was lit. For this I patched my copy of
   `shootall.c` to stop as soon as every pair is lit when no pair is
   designated. The `need_pq` column is the largest `p + q` that was needed.

## Results

Each count covers all pairs of interior integer points in all parity
classes, including the marks.

| Family | k | Strictly simple variants | Rejected (not simple / disconnected) | W range | W <= 21 | W = 22 | Pairs tested | Unlit pairs | Max p+q needed |
|---|---|---:|---|---|---:|---:|---:|---:|---:|
| one-sided (`V`, `D`, `T`) | 1–12 | 180 | 0 | 20–23 | 12 | 72 | 86,850,494 | 0 | 112 |
| two-sided | 1–12 | 1,993 | 0 | 18–24 | 282 | 328 | 1,161,773,094 | 0 | 98 |
| `shift` | 1–12 | 408 | 34 not simple | 15–22 | 162 | 246 | 272,988,339 | 0 | 58 |
| `door` | 1–3 | 0 | 6 not simple | – | – | – | – | – | – |
| `plug1` | 2–4 | 1,178 | 0 | 22–31 | 0 | 2 | 11,759,375 | 0 | 48 |
| `plug2` | 2–3 | 2,071 | 0 | 20–32 | 7 | 18 | 5,180,858 | 0 | 27 |
| `win1` | 1 | 37 | 47 not simple, 168 disconnected | 16–20 | 37 | 0 | 199 | 0 | 13 |
| total | | 5,867 | | 15–32 | 500 | 666 | 1,538,552,359 | 0 | 112 |
| pinched (reference) | 1–12 | 12 | – | 22 | – | – | 3,610,828 | 1 each (the marks) | – |

Per-`k` rows are in `work/report.log`, and per-variant rows are in
`results.tsv`. The family rows above are sums over those rows.

The `W` floor comes from `V(k)` on one or both wedges (`W = 20` and `18`):
removing a whole wedge turns two corners into collinear points. The single
`W = 15` room is `shift(−1, −1)` at k = 1. At that scale the hole moves onto
the corner `(2,2)` and fills the old hole, so it isn't a local resolution.

## Witness structure for the scaled marks

Every shortest witness in a cut family (`V`, `D`, `T`, two-sided, `plug`)
reflects off a wall made by the resolution: 5,421 of 5,421. No witness passes
through the old pinch, which is wall material now. The minimum distance from
a shortest witness to `Q` has median 0.91k, and ranges from 0.017k to 1.11k.

| Family | Shortest (or first) witness | Behaviour |
|---|---|---|
| `V(k)` = `T(k)`, one or both wedges (`W = 20`, `18`) | Direction `(−4, −3)`, m = 2k, 6 reflections, `ooNooo`. The third reflection is at `(3k, 4k)`, the hole's old top-left corner. | That corner is now a flat point of the extended wall `x = 3k`. The same path dies there in the pinched room. Bounded: the path is the same at every k. |
| `T(s)`, any `1 <= s <= k` (`W = 22`) | The first witness is `(−4, −3)` in all 66 one-sided `T` rooms, m = 2k, 6 reflections, through the same flat point `(3k, 4k)`. The shortest is sometimes `(3k − 1, 4k − 1)`, m = 2, also 6 reflections. | Bounded uniform witness for every s and k. Raising the hole's top wall by even one unit makes `(3k, 4k)` a mirror. |
| `D(k/2)`, one or both wedges (`W = 22`) | `(5, 7)` (one-sided) or `(5, −7)` (two-sided), m = k, 4 reflections, one on the chamfer face. | Bounded. The chamfer ends at `(3k, 4k)`. |
| `V(w)` with `w / k` fixed | For example `V(k/2)`: `(−6, 11)`, m = k, 6 reflections. | Similar rooms give the same path, scaled. |
| `V(w)` with w fixed | `V(1)`: `(−3k, 6k − 1)`, m = 2, 6 reflections (`oNoooo`), for k = 2 to 6. `V(2)` at k equals `V(1)` at k/2. | Direction complexity `p + q ≈ 9k / w`. For `V(1)` at k >= 7, that direction exceeds the bound 60. The shortest witness found within the bound then has 10 to 592 reflections. |
| `D(a)` with a fixed | `D(1)`: `(−(6k − 1), 3k − 1)`, m = 2, 8 reflections, for k = 4 to 6. Longer at larger k. | Complexity grows like k/a. |
| symmetric doorway `D(a)\|D(a)`, a fixed | `D(1)\|D(1)` grows with k, as one-sided `D(1)` does. | Unlike d42's centred thick wall, the symmetric resolution of fixed width has no bounded witness. |
| `shift` | For all 407 rooms with k >= 2: direction `(1, −1)`, 0 reflections, the straight segment from S to T. | The segment ST passes through the hole's other corner `(3k, 3k)`. Any translation of the hole moves that corner off the segment. These rooms are lit trivially, and they show that the pinched room's darkness also uses the corner `(3k, 3k)`. |

Across the cut-family variants, the median reflection count of the shortest
witness is 6 at every k except k = 3 (5). Longer witnesses appear only when the
short direction exceeds the first-run bound.

Comparison with d42: the pinch behaves the same way, with one difference.

- A bounded, k-independent witness exists when the resolution turns an old
  corner into a mirror, as with d42's centred end face. Here that corner is
  the hole's corner `(3k, 4k)`, not the pinch `Q` itself. `Q` can't carry a
  witness, because no path from S ever reaches it.
- A narrow cut of fixed width next to `Q` gives a witness with a fixed
  reflection count whose direction complexity grows like k/w, as in d42.
- The symmetric case differs. d42's centred thick wall gave a bounded
  witness, but the symmetric doorway `D(a)|D(a)` of fixed width doesn't.

## What's inside the d11 census

d11 covers strictly simple rooms with `N <= 32` tiles and `W <= 24`. All 40
strictly simple k = 1 variants are inside that range: `V1|-` (W = 20),
`V1|V1` (18), `shift(−1, −1)` (15) and 37 `win1` rooms (16 to 20). They
have 22 to 30 tiles. d11 already found them lit, and this run agrees. Every
variant with k >= 2 has at least 88 tiles, so it's outside the census and
new. Rooms with `W > 24` (part of `plug1` and `plug2`) are outside the census
at any size. The `in_d11` column of `results.tsv` flags the 40 rooms.

## Validation

- Witness replay for the marks: in all 5,866 variants where the first run lit
  the marks, both witnesses replayed in the plane tracer (the `best_replay`
  and `first_replay` columns). In the remaining variant (`plug1-508`, k = 4,
  W = 28), the marks were unlit at bound 40. At bound 150, the first witness
  `(−17, 26)` (30 reflections) and the shortest `(−21, −26)` (16 reflections)
  both replayed (`work/validate.log`).
- Sampled pairs (`validate53.py`, 41 rooms with k <= 8, 4 random pairs each):
  328 of 328 witnesses replayed. In the negative tests (target moved, or
  direction rotated 90°), 655 of 656 were rejected. The one accepted case is
  a rotated direction that is also a legal path to the same target, which
  d42 and d11 also saw.
- Each scaled pinched room has exactly one unlit pair, which matches the
  similarity argument.

## Not verified

- Lit verdicts for pairs other than the marks rest on `shootall`'s segment
  logic. Only 164 sampled pairs were replayed in the plane.
- Only points of the integer lattice were tested. Half-integer and other
  rational points weren't.
- The reflect convention has no exact decider. Its darkness rests on the fold
  argument and on the plane tracer (1,112 directions, 300 reflections).
- Scope:
  - Exhaustive cuts are limited to the two wedge triangles: both wedges for
    k <= 3, one wedge for k = 4. For larger k, only the `V`, `D`, `T` and
    shift families were built.
  - Cuts along diagonals on odd lines (`x ± y` odd) weren't built. They need
    the doubled lattice that d42 used.
  - Partial chamfers (a vertical cut that ends in a 45° face) weren't built
    as a family. Those up to k = 4 are among the `plug1` and `plug2` subsets.
  - Resolutions that change the room away from the two wedges, other than
    hole translations, weren't built.

## Resource use

| Item | Use |
|---|---|
| CPU | 929 s recorded by `/usr/bin/time` (`work/*.time`). Unrecorded work: a first k = 1 to 3 run and a first `verify_pinch` run, about 54 s, and candidate counting and checks, about 25 s. One failed rerun also ran for 605 s of wall clock with up to 3 busy workers, at most about 1,800 CPU s. **Total at most about 2,800 CPU s (47 minutes), under the 60-minute cap.** |
| Failed rerun | My first `rerun53.py` lacked a `__main__` guard. On macOS, `multiprocessing` uses spawn, so each worker re-ran the module, regenerated the k = 4 candidates (about 17 s) and failed to start a nested pool. The pool kept replacing them for 10 minutes until I stopped it. It wrote no results. The fixed script is the one in this directory. |
| Concurrency | At most 3 busy worker processes plus 1 idle parent. The failed rerun started about 99 short-lived workers in sequence, never more than 3 at once. |
| Memory | Not measured. The largest origami (k = 12) has 13,824 squares, and each process stayed far under 1 GB. |
| Output | 1.7 MB in total. JSONL results are gzipped: the uncompressed files came to 4.9 MB, which would have exceeded the cap together with `results.tsv`. |

## Files

| File | Contents |
|---|---|
| `rooms53.py` | Room, scaling, wedges, strict-simplicity check, `analyse` (shoot, replay, face string, distance to `Q`) |
| `run53.py` | Variant families and the parallel run |
| `rerun53.py` | Reruns of rooms with unlit pairs at a larger bound, stopping early |
| `verify_pinch.py` | Fold condition, shooting, plane tracer under both conventions, `orbit45` input |
| `validate53.py` | Sampled witness replay and negative tests, extra witness for `plug1-508` |
| `report53.py`, `results.tsv` | Per-variant table (26 columns) and per-`k` aggregates (`work/report.log`) |
| `shootall.c` | From d42, with one change: early stop when no pair is designated |
| `slit45.py`, `rooms45.py`, `orbit45.c` | Copied from d42 unchanged |
| `monteil_p4.trace` | Vector trace of the slide |
| `work/` | Gzipped JSONL results, logs, `*.time`, `orbit45` input and output |

## Reproduce

```sh
clang -O3 -march=native -o shootall shootall.c
clang -O3 -o orbit45 orbit45.c
python3 -B verify_pinch.py 400 30 300 > work/verify_pinch.log
./orbit45 3000000 < work/pinch_k1.orbit
KEX1=3 KEX2=3 python3 -B run53.py 3 40 work/k1-3.jsonl 3
KMIN=4 KEX1=4 python3 -B run53.py 4 40 work/k4.jsonl 3
KMIN=5 python3 -B run53.py 8 60 work/k5-8.jsonl 3
KMIN=9 python3 -B run53.py 12 60 work/k9-12.jsonl 3
python3 -B rerun53.py 150 work/rerun150.jsonl work/k4.jsonl work/k5-8.jsonl
# The next three inputs are the rows of work/k9-12.jsonl with unlit > 0:
# resolved rooms with k = 10, resolved rooms with k = 12, and pinched rooms.
python3 -B rerun53.py 120 work/rerun120_k10.jsonl k10u.jsonl
python3 -B rerun53.py 200 work/rerun200_k12.jsonl k12u.jsonl
python3 -B rerun53.py 150 work/rerun150_pin.jsonl pinu.jsonl
EXTRA=4:plug1-508:150 python3 -B validate53.py 1 40 4 60 work/k1-3.jsonl work/k4.jsonl work/k5-8.jsonl > work/validate.log
python3 -B report53.py results.tsv work/k1-3.jsonl work/k4.jsonl work/k5-8.jsonl work/k9-12.jsonl \
  -- work/rerun150.jsonl work/rerun120_k10.jsonl work/rerun200_k12.jsonl work/rerun150_pin.jsonl > work/report.log
```

Run `gunzip work/*.jsonl.gz` before rerunning `report53.py` on the stored
results.
