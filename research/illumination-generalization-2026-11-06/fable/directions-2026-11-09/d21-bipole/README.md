# d21: bi-pole families over Q(1, -1^5), degrees 5 to 8

Date: 2026-11-10. Exact permutation arithmetic only. Nobody has reviewed this.

## Answer

**Yes, one entirely dark bi-pole family exists.** It has degree 5 and `r = 8`.
Degrees 6, 7, and 8 have none. This refutes the CONJ in d20 `periodic.md`,
Section 5.4.

The dark family, in the conventions of `bipole.py`:

- Tuple `(1, 1, (0 1)(2 3 4), (0 1 2)(3 4), (0 4 2))`, product 1, group `S_5`.
- `S` is the 2-cycle `{0,1}` over pole 3. `T` is the 2-cycle `{3,4}` over pole 4.
- `X` lies in `Q(1^8, -1^12)`: `t = 3` three-cycles, `s = 2` two-cycles.
- The family has 30 members over a fixed base (30 covers, one pair each).

Structure:

- The cover branches over three poles only. It's a rigid three-point cover.
- Degree 5 is prime and the group is `S_5`, so no intermediate cover exists.
  The family isn't fold type.
- Proof of darkness (hand proof, unreviewed). A segment from `S` to `T`
  projects to a simple arc from `b_S` to `b_T` that avoids the third branch
  pole. In the sphere minus three points that arc is unique up to isotopy. Both
  of its lifts that start at `S` end at the 3-cycle `(0 1 2)`, a zero of `X`.
- No room double lies in the family (hand argument, unverified; it uses d18
  Theorem C). Two unbranched poles force four tile sides to be walls, and the
  remaining two reflections can't join five tiles.

## Counts

A cover is a 5-tuple up to simultaneous conjugation, one permutation per
labelled pole. Constraints: product 1, transitive, cycle lengths at most 3,
index sum `2d - 2`, three-cycles `t <= 8 - d`. So `t <= 3, 2, 1, 0` for
`d = 5, 6, 7, 8`. A node is a cover with an unordered bi-pole pair. A family is
a `B_5`-orbit of nodes.

| `d` | covers | `B_5` cover orbits | nodes | families | dark families |
| --- | --- | --- | --- | --- | --- |
| 2 | 10 | 1 | 10 | 1 | 0 |
| 3 | 60 | 3 | 150 | 2 | 0 |
| 4 | 665 | 8 | 3,630 | 10 | 0 |
| 5 | 8,510 | 16 | 68,150 | 35 | 1 |
| 6 | 75,168 | 32 | 1,259,340 | 106 | 0 |
| 7 | 153,440 | 13 | 6,112,620 | 47 | 0 |
| 8 | 62,100 | 14 | 4,800,960 | 76 | 0 |

Degrees 2 to 4 run without the `t` cap. They reproduce d20 Lemma 5.

## Method

1. **Enumeration.** For each multiset of five cycle types, `bipole.py` fixes
   `h_1`, takes `h_2` up to the centralizer of `h_1`, and brute-forces `h_3`,
   `h_4`. It then closes the seeds under the braid generators `s_0..s_3`. That
   yields every ordering. A mass check (`sum d!/|Aut|` against the raw tuple
   count) passes for every seed ordering, and for all orderings at `d <= 5`.
2. **Base.** `L(A,B) = [0,A]x[0,1] u [0,1]x[0,B]`, poles in boundary order.
   `X` is `d` copies of the double of `L`, cut along the boundary path through
   the five poles. `L(2,2)` is the tromino.
3. **Families (stage 1).** A node is lit if a chain of lifts of a boundary
   edge of `L` joins `S` to `T` through regular points. That's a straight
   segment on the square-tiled member. A family is lit if one node is lit.
   One witness per lit family also goes through `hurwitz.marked_orbit` on
   `L(2,2)`, `L(3,2)`, `L(3,4)`: all 263 witnesses at `d = 5..8` return LIT.
4. **Every cover (stage 2, no point tracking).** For every cover of the
   tromino double and every pair over poles 3 and 4, the script runs the edge
   test, then the composed degree-`3d` pillowcase decider. Every family has
   such a node, so this is exhaustive.

| `d` | pairs over poles 3, 4 | lit on `L(2,2)` | dark on `L(2,2)` | of those, lit on `L(3,2)` |
| --- | --- | --- | --- | --- |
| 4 | 363 | 362 | 1 | 1 |
| 5 | 6,815 | 6,812 | 3 | 0 (the dark family) |
| 6 | 125,934 | 125,902 | 32 | 32 |
| 7 | 611,262 | 611,262 | 0 | n/a |
| 8 | 480,096 | 479,436 | 660 | 660 |

The same tuple on `L(3,2)` is the same family, because the boundary-path basis
deforms continuously with `A`, `B`.

## Checks (`checks.py`, `checks.json`)

- Composition: the composed tuple equals `d0lib.room_tuple` for four rooms.
- The 22-wall room: `marked_orbit` completes at 3,456 states; all four `S`,
  `T` lift pairs are DARK.
- An independent ray tracer on the square complex agrees with the decider on
  363 pairs at `d = 4` and 1,357 at `d = 5`: no disagreement.
- The dark family: the decider returns DARK, with complete orbits, for every
  member whose two poles share a pillowcase corner, on `L(2,2)`, `L(3,2)`,
  `L(3,4)`, `L(2,4)` (largest orbit 1,382,400 states). The ray tracer finds no
  ray with `p + q <= 30` for all 30 members on all four bases.

## Not covered

- `r > 8` (for example `d = 6` with three or more 3-cycles), and `d > 8`.
- Bases other than `L(A,B)` with arms of width 1.
- Whether the dark family meets d19's exact definition of type a-per.

## Weakest steps

- Darkness for *every* `Y` rests on the hand proof above. The computation
  shows darkness on four square-tiled bases only.
- Family grouping uses the point-tracking rule of `hurwitz.py`. Stage 2
  doesn't use it, and the two agree.
- For `d >= 6`, the mass check covers seed orderings only.

## Files

- `bipole.py DEGREE [stage2_seconds]`: census, families, both stages.
- `checks.py`: sanity checks, ray tracer, candidate analysis.
- `result_d*.json`, `log_d*.txt`, `checks.json`, `darknodes_d4_d5.json`.

Compute: about 20 CPU minutes in total, at most 3 processes.
