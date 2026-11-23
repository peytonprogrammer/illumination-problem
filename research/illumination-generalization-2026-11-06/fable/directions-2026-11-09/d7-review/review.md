# Review of d7: wall bounds for Wolecki-triangle rooms

Reviewer: independent Opus agent, 2026-11-09. Scope: `d7-wolecki-triangles/theorem.md`.
I re-derived every step by hand and wrote my own exact code. I imported
nothing from d7.

## Verdict

Every claim survives. I found no error and no counterexample. Two statements
need a scope note, and one proof step needs a one-line completion. I also
close the non-clean gap for the 22.5-45-112.5 triangle: every room from that
triangle with two interior A points has at least 32 walls, clean or not, so
32 is the exact minimum for dark rooms from that triangle.

For right triangles with `n >= 8`, I prove `W >= 2n` for every room whose
interior A pair is dark. Every room from the (1,3,4) triangle with at most 6
extra tiles is lit (1,044,045 rooms, exact paths or Proposition R2).

## Verdict per claim

| Claim | Verdict | Note |
| --- | --- | --- |
| Values of `E`, class list (seven cases cover all triangles) | ACCEPT | Re-derived; `checks.py` C3 confirms for `n <= 60`. |
| Theorem 1 (clean room: no path joins interior A points) | ACCEPT WITH COMPLETION | See [Theorem 1](#theorem-1). |
| `q` odd never obstructs; `q` even, `p > 1` is always a corner | ACCEPT | Step 3 and L1 item 3. |
| L1 (edge-to-edge tiling, fans, turning sum) | ACCEPT | Uses strict simplicity to exclude pinch points. |
| L0 (hypothesis H) | ACCEPT | |
| L2 (stars share no tile, edge, C-tip) | ACCEPT WITH SCOPE NOTE | Needs H. Without H it fails: two regular octagons of the (1,3,4) triangle that share a side form a valid 14-wall room. That room isn't clean, so Theorem 2 is unaffected. |
| L3, L4, L5, exit-tile count | ACCEPT | Checked line by line; see [Exit-tile count](#exit-tile-count). |
| L6 (at most one shared B-tip; `T = 2P - S`) | ACCEPT WITH SCOPE NOTE | Items 1 to 3 need H only. Item 4 ("six or seven tiles at `P`") needs a clean room. |
| L7 (two non-tip corners if `x = 0`, `n >= 6`) | ACCEPT | |
| Case 1, `3c >= 2n`: no room at all | ACCEPT | Hand proof re-derived; C1 checks every attachment for `n <= 24`. |
| Case 2, right `n >= 8`: no clean room | ACCEPT | Forced tiles and overlaps re-derived; C2 checks them exactly for `n = 8, ..., 24`. |
| Case 3, 30-60-90: `W >= 26` | ACCEPT | The B-tip closure argument holds. |
| Case 4, 45-45-90: `W >= 22`; `W >= 23` if no shared B-tip | ACCEPT | `delta <= 1` holds: `2R = 2r sqrt 2`, not `4r`. |
| Case 5, (1,2,5): `W >= 32`, exact | ACCEPT, and STRENGTHENED | The bound holds for all rooms, not only clean ones. See [Theorem R1](#theorem-r1). |
| Case 6, generic obtuse: `W >= 4n + 2` | ACCEPT | Every room is clean here, because `E` is empty. |
| Case 7, `3b = n`, `n >= 12`: `W >= 4n` | ACCEPT | |
| Corollary: `n >= 6` clean rooms need 26; non-30-60-90 need 32 | ACCEPT | |
| Turning-sum-only bounds | ACCEPT | |

## Theorem 1

The proof is correct. I checked these points:

- **Fixed points of `tau`.** A point of side `i` on sheet `h` is glued to
  sheet `h s_i`. `tau` fixes it only if `-I = s_i`, which never holds. A
  vertex lift is the coset `hH`, with `H` dihedral of order `2q`. `tau` fixes
  it exactly when `-I` is in `H`, that is, when `q` is even.
- **Lift through flat wall points.** A non-corner tile vertex has `p = 1`.
  Its `2q` interior tiles, or its `q` flat tiles plus their mirror images,
  develop onto the `2q` sheets around a regular point. The reflected path
  develops to the straight continuation.
- **First-return symmetry.** Both `G(t)` and `tau(G(T1 - t))` start at `O`
  with the same direction. Both avoid true cone points, because `g` avoids
  corners and `tau` maps regular points to regular points. Uniqueness of
  geodesics gives equality on `[0, T1]`.
- **Fold map.** The proof uses only the room's own fold. It needs no tiling
  of the plane, so it holds for non-tiling triangles.

Completion: the first return `G(T1) = O` can occur at a flat boundary A
point, not only at `S` or `T`. The argument is unchanged. It also proves a
stronger statement: in a clean room, no billiard path joins an interior A
point to any non-corner A point. Theorem R1 doesn't need this extension.

## Exit-tile count

This is the author's weakest step, and it holds. Let `e = (M, B0, C0)` be an
exit tile.

1. `C0` carries two star tiles and `e`. H allows at most three tiles, so the
   fan at `C0` is exactly `e`, then two star tiles. The edge `M C0` has no
   tile beyond it, so it's a wall, and `e` is an end tile of the fan at `M`.
2. An inner C-tip of `M` carries two tiles with A vertex `M`. If it were a
   star C-tip, or an inner C-tip of another centre, it would carry four
   tiles, and H excludes that. So the sets `N(M)` are disjoint and contain
   no tips.
3. A centre with two exit tiles and `m = 2` has both tiles on one B vertex.
   That vertex is a B-tip of two different stars, by the perpendicular
   bisector argument of L5.

Each step uses only H, L1, and L2.

## Theorem R1

**Theorem R1.** Let `Q` be a room built from the (1,2,5) triangle with
`n = 8`. Let `Q` have two distinct interior A points. Then `W >= 32`. `Q`
need not be clean.

Proof. The triangle is obtuse with `3c = 15 < 16`, so H holds in every room
(L0). L2, L3, L4, L5, L6 items 1 to 3, and L7 use only H. So they hold in
`Q`.

- The 16 C-tips are distinct corners.
- At most one B-tip is shared (`x <= 1`), so there are `16 - x` distinct
  B-tips.
- Let `Y` be the set of B-tips that aren't corners. A B point that isn't a
  corner has 4 or 8 tiles.

Choose exit tiles as follows. For each `P` in `Y`, the fan at `P` has more
than the two star tiles and is edge-connected. So a tile shares an outer
star edge at `P`. That tile is an exit tile with B vertex `P`; choose it.
Distinct tips give distinct tiles. Two chosen tiles with one centre have
different B vertices. So `m >= 4` at that centre, and `|N(M)| >= 2`. The
exit-tile count then gives at least `|Y|` non-tip corners.

- **Case `x = 0`.** L7 also gives two non-tip corners. So
  `W >= 16 + (16 - |Y|) + max(|Y|, 2) >= 32`.
- **Case `x = 1`, shared tip `P` a corner.** `T = 2P - S`. One gap at `P`
  holds two exit tiles with a common centre `M0`. `M0` has no other exit
  tile (L3 item 5), so no chosen tile has centre `M0`. `N(M0)` adds one more
  corner, and `W >= 16 + (15 - |Y|) + |Y| + 1 = 32`.
- **Case `x = 1`, `P` not a corner.** Four tiles would put a star tile of
  `S` next to one of `T`, which L2 excludes. So `P` has eight tiles, and both
  gaps hold two exit tiles, with centres `M1 != M2`. Choose the exit tile at
  `P` from the first gap. Then `N(M2)` is extra, and `W >= 32` again.

Theorem 1 makes the 34-tile clean room with 32 walls dark. So 32 is the
exact minimum over all rooms from this triangle in which an interior A pair
is dark. No fold-type room does better.

## Right triangles with n >= 8

**Proposition R2.** Let the triangle be right with `n >= 8`. Let `Q` be a
room with interior A points `S != T`, and suppose no billiard path joins
`S` and `T`. Then:

1. `St(S)` and `St(T)` share no C-tip. If they shared a C-tip `X`, the four
   tiles at `X` would form the rhombus `S B T B'`. That rhombus is convex,
   and the open segment `ST` meets only the interior point `X`. So `S` sees
   `T`.
2. The stars share no edge. A shared spoke forces `S = T`. A shared `BC`
   edge has a shared C endpoint.
3. The stars share no B-tip. A shared tip would carry two star pairs that
   aren't adjacent in its fan, so at least six tiles. Then `6b = 3n - 6 > 2n`.
4. Every B point is a corner, because `b = n/2 - 1` doesn't divide `n`.

So the `2n` B-tips are distinct corners, and `W >= 2n`, which is 16 for
`n = 8`. PROVED.

Without the darkness hypothesis, the bound is `2n - 2`. Two octagons that
share a side reach 14, and that room is lit by a direct segment.

I can't prove a sharper bound for right triangles. Item 1 shows that
darkness needs the two stars apart. The Case 2 argument then fails, because
the C points on the corridor may carry two or four tiles.

## Independent enumeration

Code: `geom.py` (exact `Z[zeta_2n]`, certified signs), `enum_rooms.py`,
`shoot.py`, `lit_scan.py`, `deep_shoot.py`, `checks.py`.

Exact bound of every run: rooms `Q = St(S) u St(T) u K` with `|K| <= k`
extra tiles. `S` is at the origin. `T` is every A vertex of a tile within
reflection distance `k + 1` of `St(S)`, up to the `2n` symmetries of the
star. `K` covers every tile set that joins the two stars through edges
(Redelmeier enumeration with distance pruning). A room is valid when four
checks hold: labels agree at every vertex; there are no T-junctions; tile
interiors are disjoint; and the boundary is one simple cycle with every
vertex of degree 2. Two implementations, a brute-force version and a pruned
version, agree on valid counts and the `W` histogram for (8,2) with
`k <= 5`.

| Triangle | `k` | Valid rooms | Min `W`, all rooms | Min `W`, clean | Claimed |
| --- | --- | ---: | --- | --- | --- |
| (1,2,5), `n = 8` | 8 | 558,473 | 32 | 32 | 32 exact (clean) |
| (1,3,4), `n = 8` | 6 | 1,044,045 | 14 (lit) | none | no clean room |
| (1,3,6), `n = 10` | 7 | 11,042 | 42 | 42 | `>= 42` |
| (1,1,4), 30-30-120 | 4 | 0 | none | none | no room |
| (1,1,2), 45-45-90 | 11 | 12,086,492 | 4 (lit, convex) | 24 (48 rooms, all with `k = 11`) | `>= 22`; author's best is 24 |

Notes:

- (1,3,6) is the smallest generic obtuse triangle. No generic obtuse
  triangle exists with `n = 6` or `n = 8`: the only candidates are
  closed-star, right, or (1,2,5).
- 30-30-120: no tile can attach to a star (C1, all closed-star triangles
  with `n <= 24`). The enumeration finds no room with two interior A points.
- 45-45-90: no clean room has 10 or fewer extra tiles. With at most 11,
  the clean minimum is 24, which matches the author's construction. The
  enumeration also finds 24 clean rooms with 25 walls. No clean room with 22
  or 23 walls has 11 or fewer extra tiles. Larger rooms aren't searched, so
  22 and 23 stay open.

## Non-clean rooms

**(1,2,5).** Theorem R1 settles the minimum. Within `k <= 8`, three
non-clean rooms have 32 walls, and I found an exact path in each:

- 36 tiles, `P` interior with 8 tiles. `S` sees `T` directly through `P`.
- Two rooms with 36 tiles and two flat B points each. Each has a path with
  7 reflections, found from images of depth 4 (`deep-8-2-W32.json`).

In the same runs, the 2 clean 32-wall rooms show no path up to depth 5 (7,567
images each). That result agrees with Theorem 1. I didn't
scan non-clean (1,2,5) rooms with more than 32 walls. Theorem R1 makes them
irrelevant to the minimum.

**(1,3,4), right `n = 8`.** Every room is non-clean. With `k <= 5`
(196,114 rooms, `W` from 14 to 24), I found an exact path in every room:

- 196,062 rooms at depth 0 or 2.
- Every remaining room at depth 3 or 4: two rooms with `W = 19` and 50 rooms
  with `W = 21`.

With `k <= 6` (1,044,045 rooms), every room is lit:

- Rooms whose stars share a C-tip are lit by Proposition R2 item 1, with no
  search needed.
- The other 915 rooms have `W` from 17 to 23. Each has an exact path.
  `deep_scan.py` finds most at image depth 4 or less. It finds the
  `W = 23` paths by a midpoint-targeted search (`shoot.find_path_mid`). That
  search aims at `T' = 2 g(X) - S` for images `g(X)` of transparent C
  points, which is the shape that the proof of Theorem 1 forces on every
  path.
- One 20-wall room, with 38 tiles, needed that search. It has a path with
  12 reflections whose midpoint is a flat C point
  (`logs/mid-8-3-W20.log`).

The smallest rooms whose stars share no C-tip have 17 walls, and they're
lit.

So the search finds no dark room for the (1,3,4) triangle. The proved
bound is `W >= 16`. No dark room was found among rooms with 6 or fewer extra
tiles, up to 23 walls. The search covers all whole-copy fold rooms in this
size range, because every fold room is a room. Beyond that size, the
question is open.

## Theorem I sign

Setting: `n` is even, and the triangle has angles `(1, b, c) * pi/n` with
`b + c = n - 1` and `b < c`. A room is a strictly simple polygon that is a
finite union of isometric copies of the triangle. It has a continuous fold
onto the triangle that is an isometry on each copy. A billiard path stops at
a corner. `W` is the number of corners.

1. In a clean room, no billiard path joins two interior A points (Theorem 1).
2. If `3c >= 2n`, no room has two interior A points.
3. For right triangles with `n >= 8`, no clean room has two interior A
   points. Every dark room with two interior A points has `W >= 2n`.
4. For 30-60-90, clean rooms have `W >= 26`.
5. For 45-45-90, clean rooms have `W >= 22`, and `W >= 23` unless the stars
   share a B-tip.
6. For (1,2,5), every room with two interior A points has `W >= 32`, clean
   or not. A dark 32-wall room exists, so 32 is the exact minimum for dark
   rooms.
7. For generic obtuse triangles, every room with two interior A points is
   dark and has `W >= 4n + 2`. For `3b = n` with `n >= 12`, it's dark and
   has `W >= 4n`.

Consequence: take any allowed triangle with `n >= 6`, other than 30-60-90
and the right triangles with `n >= 8`. Every room from it with two interior
A points has at least 32 walls, clean or not. For right triangles with
`n >= 8`, a dark interior A pair needs `W >= 2n`.

## What remains unverified

- Rooms whose dark pair isn't a pair of interior A points. Theorem 2 and R1
  say nothing about them.
- For right triangles with `n >= 8`, the gap between `W >= 2n` and the
  smallest dark room. The enumeration covers only `n = 8` with `k <= 6`
  extra tiles. No dark room exists there.
- The 45-45-90 minimum for clean rooms (22, 23, or 24).
- 30-60-90 non-clean rooms, which belong to another agent.
- The hand proofs here are AI-reviewed only. Float sign evaluation in
  `geom.py` is certified by a norm bound and falls back to 90-digit Decimal
  arithmetic.

## Files and commands

Run each command from this directory. Python 3 standard library only.

| File | Purpose |
| --- | --- |
| `geom.py` | `Z[zeta_2n]` arithmetic, certified signs, tiles, room validator |
| `shoot.py` | Exact billiard tracer, image search, midpoint-targeted search |
| `enum_rooms.py` | Two stars plus at most `k` tiles; writes `enum-<n>-<b>-k<k>.json` |
| `lit_scan.py` | Path search on every enumerated room up to `W`; writes `lit-*.json` |
| `deep_scan.py` | Rooms whose stars share no C-tip, deeper search; writes `deep-scan-*.json` |
| `deep_shoot.py`, `one_room.py`, `one_room_mid.py` | Single-room inspection and deep search |
| `checks.py` | C1 closed star, C2 case-2 overlaps, C3 classification; writes `checks.json` |

```
python3 checks.py
python3 enum_rooms.py 8 2 8          # about 7 minutes
python3 enum_rooms.py 4 1 11         # about 37 minutes
python3 lit_scan.py 8 3 5 40 2
python3 deep_scan.py 8 3 6 0 20 4
python3 one_room_mid.py deep-scan-8-3-k6-W0-20.json 0 5
```
