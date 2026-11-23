# d97: review of Q03, the counting identity and the corner-only area bound

Date: 2026-11-20. Reviewer: independent agent. Sources: `D/d68-one-target/README.md` §1 and
§3, `qclass-closure/README.md` "Why a finite computation suffices", Q03 brief in
`D/d95-review-queue/review-queue.md`. Files here: `count.py` (run with `python3 -B`) and
`count.log`. CPU: 0.8 s.

## Verdict

**Sound.** The identity holds for every orthogonal lattice room, with one extra term for
pinches. The bound `n <= 4r + 4 <= 36` holds for strictly simple rooms with `r <= 8`. The
Q-class closure states that hypothesis and its census removes pinches, so it applies the
bound correctly. Q03 can be marked reviewed.

## 1. The identity (PROVED here)

Definitions. Let `P` be a closed orthogonal polygon with integer vertices, and let its
cells be the `n` unit squares inside it. Fix a class `y` in `(Z/2)^2`. For a lattice point
`p`, let `k(p)` be the number of the four unit cells around `p` that lie in `P`.

| `k(p)` | Cell pattern | Name | Notes |
| --- | --- | --- | --- |
| 0 | none | outside | Contributes 0. A boundary point always has `k >= 1`, because walls lie on grid lines. |
| 1 | one cell | convex corner | The boundary turns 90 degrees around the cell. |
| 2, edge-adjacent | two cells sharing an edge | smooth wall point | The point is in the relative interior of a straight wall. |
| 2, diagonal | two cells sharing only `p` | pinch | Impossible in a strictly simple room. |
| 3 | three cells | reflex corner | Interior angle 270 degrees. |
| 4 | four cells | interior point | No slit can run between them, since a slit makes the boundary non-Jordan. |

The patterns are exhaustive, and `k = 1` and `k = 3` are exactly the polygon's true
corners. Collinear listed vertices have `k = 2` and count as smooth points.

Double count. Each cell `[i, i+1] x [j, j+1]` has four corners, one in each parity class.
So the number of pairs (cell, class-`y` corner) is `n`. Counted by point, each class-`y`
point contributes `k(p)`. That gives, for any orthogonal lattice polygon:

`n = cvx_y + 2 smooth_y + 2 pinch_y + 3 rfx_y + 4 int_y`

In a strictly simple room `pinch_y = 0`, which is d68's Lemma A. d68's proof step 4 says
the same thing.

## 2. The bound step

- `cvx_y <= v` and `rfx_y <= r` hold trivially, because class-`y` corners are a subset of
  all corners.
- `v = r + 4` holds for a strictly simple orthogonal polygon, because the turning number is
  1. So `W = v + r = 2r + 4`.
- A corner-only class has `smooth_y = int_y = 0` by definition. With no pinches,
  `n = 3 rfx_y + cvx_y <= 3r + r + 4 = 4r + 4`.
- `W <= 20` gives `r <= 8`, so `n <= 36`. Equality needs all 8 reflex and all 12 convex
  corners in class `y`. `count.py` finds such a room (census R780546, class `(0, 0)`).

**Pinches.** The bound needs strict simplicity or an explicit pinch convention. The control
in `count.log` is two 2 x 2 squares touching at one point. Its pinch is in class `(0, 0)`,
and that class has no smooth or interior points.

- If a pinch isn't a corner, then `v - r = 6`, not 4. The bound reads `n <= 4r + 4 = 4`,
  but `n = 8`. It fails.
- If the pinch counts as two reflex turns, then `v - r = 4`, but the identity term is
  `2 pinch_y`, not `3 rfx_y`. Then `n <= 4r + 4 = 12` still holds, by a different count.

Neither case affects the Q-class closure. Its hypothesis is "strictly simple". Its census
drops pinches and holes at completion ("outward minus inward must be four").

## 3. Computation (COMPUTED)

`count.py` computes each term for all four classes and checks both sides. It also counts
the class-`y` corner of every cell directly. All 14 rooms and 56 (room, class) checks pass.
Every room has `v - r = 4` and no pinch.

| Room | n | r | W | Corner-only classes (`3 rfx + cvx`) |
| --- | --- | --- | --- | --- |
| R22 (`rooms.json` first, `R22-base`) | 15 | 9 | 22 | (1,1): 3·3 + 6 = 15 |
| Cross `P_7` | 96 | 4 | 12 | none |
| Cross `P_9` | 128 | 4 | 12 | none |
| U2 (`indep.py`, k = 0) | 46 | 3 | 10 | none |
| Census R1 | 10 | 3 | 10 | (1,0): 10 <= 16 |
| Census R1205 | 13 | 3 | 10 | (1,1): 13 <= 16 |
| Census R40597 | 16 | 4 | 12 | (1,0): 16 <= 20 |
| Census R284965 | 19 | 5 | 14 | (1,1): 19 <= 24 |
| Census R518983 | 21 | 5 | 14 | (1,1): 21 <= 24 |
| Census R725636 | 24 | 6 | 16 | (1,0): 24 <= 28 |
| Census R774722 | 27 | 7 | 18 | (1,0): 27 <= 32 |
| Census R780206 | 30 | 8 | 20 | (0,0): 30 <= 36 |
| Census R780542 | 33 | 8 | 20 | (1,1): 33 <= 36 |
| Census R780546 | 36 | 8 | 20 | (0,0): 36 = 36 |

Census rooms are the first room at each of areas 10, 13, ..., 36 in
`qclass-closure/witnesses.txt.gz`. R22 has `r = 9`, so its bound is `4r + 4 = 40`. It sits
outside the `r <= 8` range, as expected for the 22-wall room.

## 4. Use in `qclass-closure/README.md`

The README applies the bound correctly.

- Its hypotheses are a strictly simple room, integer vertices, and one corner-only class
  on the same grid. These are exactly the hypotheses of the bound.
- `W = 2r + 4 < 22` gives `r <= 8`. Each class-`y` cell corner is a convex corner (1) or
  a reflex corner (3), so `n <= (r + 4) + 3r <= 36`.
- The census prunes at area 36 and drops pinched or holed shapes. So it covers the whole
  class.

d68 §3 states the same bound for BBBQ rooms and reports area 36 attained in `covers.json`.
Census R780546 independently confirms that 36 is attained.
