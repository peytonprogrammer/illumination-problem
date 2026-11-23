# d13: cylinder certificates for class (iii) rooms

This directory extends Part A (`../d9-census-w22/partA-README.md`) from
one-cylinder directions to every cylinder of every direction. For proofs, see
`theory.md`. This file holds computed facts, interpretation, and commands.

## Answer

- **Lemma A' holds as proposed, with a proof.** If a lift of S lies in an open
  DP cylinder D and a lift of T lies in the closure of D, then S illuminates T.
  The proof covers T on the cylinder boundary, at lattice points, and on
  singular lines (`theory.md`, Section 2). Full cylinders are rare, so the
  working tool is Theorem C. It takes the union of the closed cylinders over
  all directions and all labels of S (`theory.md`, Section 3).
- **X' is computable exactly.** `cover.c` returns the live set X'_Θ (the
  sources S whose certified set doesn't cover the room), the uncovered region
  of each live cell, and the pairs of live points that remain.
- **Validation passed.**
  - Class (i)/(ii) rooms: X' ⊂ X in all 475 rooms with area <= 8.
  - 22-wall room: X' = {(0,0), (2,2)} exactly. The one remaining pair is the
    known dark pair.
  - 12-wall cross: undecided. 12 of its 28 pairs of convex corners never share
    a cylinder (Proposition O).
- **Class (iii) coverage.** 200,675 of the 200,686 normalized class (iii)
  rooms with area <= 14 are fully decided, with no dark pair. The 11 undecided
  rooms all have even area <= 12.
- **Largest A.** The requested form, "W <= 21 and area <= A have no dark pair",
  still holds only for **A = 5**. Both area-6 class (iii) rooms (W = 8) are
  obstructed. By Proposition O, no certificate built from finitely many
  cylinder directions can decide them.
- **Stronger forms that hold** (conditional on the unreviewed lemmas):
  - W <= 22 and area in {1, ..., 5, 7, 9, 11, 13, 14}: no dark pair of
    distinct real interior points.
  - W <= 22 and area <= 14: every pair is lit, with two exceptions. One is
    the known pair of the 22-wall room, which has area 15 and so falls outside
    this range. The other is the 15 rooms listed under "Undecided rooms".
- **No new dark pair.** Every pair that a certificate left open was either
  shot (7,557 pairs, all LIT with two agreeing tracers) or closed by more
  directions.

## Status of each result

| Result | Kind | Where |
| --- | --- | --- |
| Lemma A', Corollary A, Theorem B' | Proved here, unreviewed | `theory.md` §2 |
| Theorem C, pair reduction | Proved here, unreviewed | `theory.md` §3 |
| Exactness of the computation (Q ⇔ U) | Proved here, unreviewed | `theory.md` §4 |
| Propositions O and O' (obstructions) | Proved here, unreviewed | `theory.md` §5 |
| Coverage tables, undecided list, shots | Computed | this file, `runs/` |
| "Near-corner pairs need renormalization" | Interpretation | `theory.md` §5 |

The final statements also use the Part A census for pairs of interior lattice
points and Part A's Lemma A and Theorem B for class (i)/(ii) rooms.

## Method

For each room, `cover.c` does three steps.

1. **Pole test.** For every pair of convex corners, it checks whether some
   direction (p, q), 1 <= p, q <= B, has one DP cylinder at both poles. If a
   pair never shares one, the room is OBST. By Proposition O, no
   certificate from these directions covers that pair's neighbourhood.
2. **Theorem C.** It processes directions by increasing p + q. Each live cell
   of the arrangement of singular lines carries Q, the closed uncovered region.
   A cell dies when Q is empty. The room is DONE when every live cell is a
   point. By default the program stops there. With `COVER_ALLDIRS=1` it keeps
   going through all directions up to B, which kills more points.
3. **Pairs.** For a DONE room, the remaining pairs are pairs (s, t) of live
   points with t in Q(s) and s in Q(t). Lattice pairs are decided by the
   census. The others are shot with `shoot.py`.

A room is RESID when cells of dimension 1 or 2 stay live after B. It's BIG
when the number of live cells passes the cap; BIG rooms are rerun with a larger
cap.

## Computed facts

### Validation

- **Labels.** `check_labels.py` checks the cylinder labels against an
  independent room tracer on 4,128 regular trajectories in 5 rooms. It also
  checks the face rule against sampling.
- **Python and C agree.** `ill.py` and `cover.c` give identical live-cell
  counts and dimensions after each of the 19 directions with p, q <= 5 on the
  area-6 room (0,0)(0,1)(1,1)(0,2)(1,2)(0,3).
- **Class (i)/(ii) rooms.** `validate_x.py 8 8` enumerates every strictly
  simple room with area <= 8 that has a one-cylinder direction with
  1 <= p, q <= 8: 475 rooms. For each one it computes X (points on singular
  lines of both families, intersected over the one-cylinder directions) in
  Python and X' with `cover.c` (`COVER_ALLDIRS=1`, B = 8). Every room is DONE,
  and X' ⊂ X in all 475. In total |X| = 857 and |X'| = 86. X' = X in 346
  rooms.
- **22-wall room** (cells as in `../d3-review/surface.py`, B = 12).
  - With `COVER_ALLDIRS=1`: DONE, X' = {(0,0), (2,2)}. The only remaining pair
    is (0,0)-(2,2), a lattice pair, which is the known dark pair.
  - Default mode: 18 live points, one lattice pair (the same one), and 2
    non-lattice pairs. Both non-lattice pairs are LIT by `shoot.py`.
  - Negative control: `shoot.py` with R = 30 finds no path for (0,0)-(2,2)
    after 2,832 directions.
- **12-wall cross** (cells x = 0..3 with y = 1, 2, plus (1,0), (2,0), (1,3),
  (2,3)). It has no one-cylinder direction with p, q <= 12, so X isn't
  defined. The cross is OBST: 12 of its 28 pairs of convex corners never
  share a cylinder for p, q <= 12. With the test forced off, the run ends RESID
  with 732 live points, 1,464 live edges, and 736 live faces at B = 12. The
  uncovered regions lie within L∞ distance 1/11 of exactly those 12 corner
  pairs.
- **Boundary cases of Lemma A'.** `spotcheck.py 10 30` picks 40 random
  sources in 4 rooms, including the cross and the 22-wall room. For each
  source it takes up to 6 vertices of the closed faces of each cylinder in
  Λ(S): 240 pairs on singular lines, lattice points, and cell edges.
  `shoot.py` lights all 240, and the two tracers never disagree.
- **Room lists.** `enum/` re-lists the class (iii) rooms with the copied Part A
  enumerator in classify-only mode. The area <= 12 list is identical to Part
  A's (12,802 rooms). The counts at areas 13 and 14 (21,523 and 166,361) match
  `partA-coverage.md`. The reduced rooms match too: 4 at area 12 and 2 at area
  14 have class (iii) normal forms.

### Class (iii) coverage, B = 12

Final status per normalized class (iii) room, W <= 22. Lattice pairs left are
decided by the Part A census, where every interior lattice pair is lit in
these rooms. "Other pairs left" counts after the all-directions pass.

| area | class (iii) rooms | DONE | OBST | RESID | lattice pairs left | other pairs left |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 2 | 0 | 2 | 0 | 0 | 0 |
| 7 | 1 | 1 | 0 | 0 | 0 | 0 |
| 8 | 48 | 46 | 2 | 0 | 0 | 0 |
| 9 | 51 | 51 | 0 | 0 | 2 | 0 |
| 10 | 686 | 685 | 1 | 0 | 1 | 0 |
| 11 | 1,090 | 1,090 | 0 | 0 | 18 | 0 |
| 12 | 10,924 | 10,918 | 5 | 1 | 63 | 0 |
| 13 | 21,523 | 21,523 | 0 | 0 | 5,770 | 0 |
| 14 | 166,361 | 166,361 | 0 | 0 | 42,760 | 0 |
| all | 200,686 | 200,675 | 10 | 1 | 48,614 | 0 |

The full table with live-point counts is `runs/table_final.md`.

Default mode left 7,557 non-lattice pairs at areas 8 to 12. `shoot.py` (R = 30,
two tracers) lights all 7,557, needing at most 985 images per pair. The
all-directions pass then closes the same pairs without shooting. At areas 13
and 14, default mode left 200,096 non-lattice pairs in 28,723 rooms. The
all-directions pass closes all of them. 24 rooms first hit the live-cell cap
(BIG): 1 at area 11, 1 at area 13, and 22 at area 14. All 24 are DONE on rerun
with a larger cap.

Run time on 4 workers: 20 s for areas 6 to 12, 67 s for area 13, and 7 min for
area 14.

### Undecided rooms

These 11 normalized rooms, plus 4 reduced rooms, are the only rooms with
W <= 22 and area <= 14 where a dark pair isn't ruled out. Coordinates are
census coordinates. "Pairs" lists the pairs of centres (convex corners or flat
boundary points) whose neighbourhoods hold the uncovered region at B = 12.
"Radius" is the L∞ radius of those neighbourhoods. Every open pair (S, T) has
S and T within that radius of a listed pair. Only Propositions O and O' explain
why these pairs stay open.

| area | W | cells | status | radius | pairs |
| --- | --- | --- | --- | --- | --- |
| 6 | 8 | 0 0, 0 1, 1 1, 0 2, 1 2, 0 3 | OBST | 1/11 | (1,0)-(2,1), (1,4)-(2,3) |
| 6 | 8 | 0 0, 0 1, 1 1, 0 2, 1 2, 1 3 | OBST | 1/11 | (0,0)-(2,1), (0,3)-(2,4) |
| 8 | 12 | 1 0, 1 1, 2 1, 3 1, 0 2, 1 2, 2 2, 2 3 | OBST | 1/9 | (0,3)-(1,0), (0,3)-(3,4), (1,0)-(4,1), (3,4)-(4,1) |
| 8 | 12 | 0 0, 0 1, 1 1, 2 1, 1 2, 2 2, 3 2, 3 3 | OBST | 1/11 | (1,0)-(1,3), (1,0)-(3,1), (1,3)-(3,4), (3,1)-(3,4) |
| 10 | 16 | 0 0, 1 0, 1 1, 2 1, 3 1, 0 2, 1 2, 2 2, 2 3, 3 3 | OBST | 0.6; 2/15 at B = 16 | 12 pairs (see `runs/rinfo_hard_a6to12_B12.txt`) |
| 12 | 12 | 0 0, 0 1, 1 1, 0 2, 1 2, 1 3, 1 4, 0 5, 1 5, 0 6, 1 6, 0 7 | OBST | 1/11 | 6 pairs |
| 12 | 20 | 0 0, 1 0, 3 0, 1 1, 2 1, 3 1, 0 2, 1 2, 2 2, 0 3, 2 3, 3 3 | OBST | 1.09; 1.07 at B = 16 | 94 pairs |
| 12 | 12 | 1 0, 2 0, 0 1, 1 1, 2 1, 3 1, 0 2, 1 2, 2 2, 3 2, 0 3, 3 3 | OBST | 1/10 | 6 pairs |
| 12 | 12 | 0 0, 3 0, 0 1, 1 1, 2 1, 3 1, 0 2, 1 2, 2 2, 3 2, 0 3, 3 3 | RESID | 1/11 | (1,0)-(2,1), (2,1)-(3,0), (1,4)-(2,3), (2,3)-(3,4) |
| 12 | 12 | the cross | OBST | 1/11 | 12 corner pairs |
| 12 | 12 | 0 0, 0 1, 1 1, 0 2, 1 2, 0 3, 0 4, 0 5, 1 5, 0 6, 1 6, 0 7 | OBST | 1/9 | 6 pairs |
| 12 | 8 | 4 reduced rooms: diag(1,2) and diag(2,1) images of the two area-6 rooms | OBST (normal form) | scaled | as for the normal form |

Notes on the table:

- The RESID room passes the pole test but isn't decided. `flatpole.py 16`
  shows that its 4 residual pairs are exactly the pairs (convex corner, flat
  boundary point) that never share a cylinder for p, q <= 16. That is the
  hypothesis of Proposition O'. The flat points (2,1) and (2,3) lie on the
  room's mirror axis. The residue radius is 1/(B - 1) for B = 12, 16, 20.
- The radius column is the L∞ radius at B = 12. The area-10 room localizes
  slowly: radius 0.6 at B = 12 and 2/15 at B = 16, around the same 12 centre
  pairs. The W = 20 room doesn't localize by B = 16: radius 1.07, with
  667,368 live points and 939,472 live faces. Its residue is the least
  understood of the 11.
- Area 14 has 2 reduced rooms with class (iii) normal forms (area 7). Both
  normal forms are DONE, so those rooms are decided.

## What remains and why

- **Pole-obstructed pairs.** By Proposition O, the pairs near
  (c1, c2) in an OBST room can't be decided by any finite set of cylinder
  directions. Shooting can't settle them either: the pair set is a
  4-dimensional open region, not a finite list. Deciding them needs a
  renormalization argument: an argument about the limit of directions whose
  cylinders shrink onto the poles. This directory doesn't attempt one.
- **The corner/flat-point obstruction.** The same applies to the RESID room,
  with a flat boundary point on a mirror axis in place of the second pole.
- **Area 15 and 16.** Not attempted. Part A's list stops at area 12, and the
  re-listing here stops at area 14. The class (iii) counts at areas 15 and 16
  are 364,096 and 2,190,624. At the area-14 rate, area 16 needs roughly 2
  hours of CPU per 166,000 rooms. That exceeds the 40-minute cap for a single
  run, so it would need several runs.
- **Review.** Every lemma in `theory.md` is unreviewed. The coverage claims
  depend on Lemma A', Theorem C, and the exactness argument of Section 4.
  The 7,557 shot pairs don't depend on them.

## Commands

Run from this directory. Build first:

```sh
cc -O2 -o cover cover.c
cc -O2 -o enum/partA-enum enum/partA-enum.c
cc -O2 -o enum/partA-cert enum/partA-cert.c enum/partA-verify_plane.c
```

Checks and validation:

```sh
python3 check_labels.py                 # labels vs room tracer (42 s)
python3 validate_x.py 8 8               # X' within X, class (i)/(ii), area <= 8 (4 min)
python3 spotcheck.py 10 30              # Lemma A' boundary cases by shooting (18 s)
printf 'Q22 15 22 -1 -1 -1 0 0 -2 0 -1 0 0 0 1 1 -3 1 -2 1 1 1 2 2 1 2 2 3 0 3 1 4 0 \n' \
  | COVER_ALLDIRS=1 COVER_LL=1 ./cover 12 0 3000000      # 22-wall room
printf 'X 12 12 0 1 1 1 2 1 3 1 0 2 1 2 2 2 3 2 1 0 2 0 1 3 2 3\n' | ./cover 12 0 400000   # cross
python3 flatpole.py 16 0 0 3 0 0 1 1 1 2 1 3 1 0 2 1 2 2 2 3 2 0 3 3 3
```

Coverage run:

```sh
sh enum/run_enum.sh 14 enum/a14                       # class (iii) lists, 70 s
cat enum/a14/job-*.rf | awk '$1=="C3" && $2<=12' > runs/c3_rooms_a6to12.txt
cat enum/a14/job-*.rf | awk '$1=="C3" && $2==13' > runs/c3_rooms_a13.txt
cat enum/a14/job-*.rf | awk '$1=="C3" && $2==14' > runs/c3_rooms_a14.txt
cat enum/a14/job-*.rf | awk '$1=="RED"' > runs/reduced_a2to14.txt
sh run.sh runs/c3_rooms_a6to12.txt runs/res_a6to12_B12.txt 12 0 100000
sh run.sh runs/c3_rooms_a13.txt runs/res_a13_B12.txt 12 0 100000
sh run.sh runs/c3_rooms_a14.txt runs/res_a14_B12.txt 12 0 100000
# BIG reruns: same command on the BIG rooms with MAXLIVE 2000000 or 3000000
# shooting the default-mode pairs of areas 6 to 12
awk -F'|' '$1 ~ / DONE / { split($1,a," "); if (a[13] > 0) print $2 "|" $3 }' \
  runs/res_a6to12_B12.txt > runs/pairs_a6to12.txt
sh shoot_all.sh runs/pairs_a6to12.txt runs/shoot_a6to12.txt 30
# all-directions pass on rooms with pairs left
awk -F'|' '$1 ~ / DONE / { split($1,a," "); if (a[13] > 0) print "R", a[3], a[4], $2}' \
  runs/res_a13_B12.txt runs/res_a14_B12.txt > runs/withpairs_a13to14.txt
COVER_ALLDIRS=1 sh run.sh runs/withpairs_a13to14.txt runs/res_withpairs_a13to14_alldirs_B12.txt 12 0 100000
gunzip -k runs/*.gz      # stored results are compressed
python3 aggregate.py runs/res_a6to12_B12.txt runs/res_big_rerun_B12.txt \
  runs/res_withpairs_a6to12_alldirs_B12.txt runs/res_a13_B12.txt runs/res_a14_B12.txt \
  runs/res_withpairs_a13to14_alldirs_B12.txt runs/res_big_a13to14_rerun_B12.txt --
python3 reduced.py runs/reduced_a2to14.txt runs/res_a6to12_B12.txt
# residue localization of undecided rooms
COVER_RINFO=1 COVER_ALLDIRS=1 ./cover 12 1 3000000 < runs/hard_a6to12.txt
```

`cover` options: `cover B FORCE MAXLIVE < rooms`. FORCE = 1 skips the pole
test's early exit. The environment variables `COVER_ALLDIRS`, `COVER_LL`
(print lattice pairs), `COVER_PTS` (print live points), `COVER_RINFO`
(residue centres and radius), `COVER_DUMP`, and `COVER_VERBOSE` add output or
change the stopping rule as described above.

## Files

| File | Purpose |
| --- | --- |
| `theory.md` | Proofs: Lemma A', Theorem C, exactness, obstructions |
| `cover.c` | Exact C implementation: pole test, Theorem C, pairs, residue report |
| `run.sh`, `shoot_all.sh` | 4-worker drivers |
| `shoot.py` | Exact pair shooter with two independent tracers |
| `cyl.py` | Python cylinder labels (DP quotient by union-find) |
| `cover.py` | Face rule and full-cylinder test |
| `ill.py` | Python reference implementation of Theorem C |
| `xset.py` | Exact convex geometry used by `ill.py`; its per-direction candidate set is superseded |
| `poles.py`, `flatpole.py` | Pole-pair and corner/flat-point obstruction tests |
| `check_labels.py`, `validate_x.py`, `spotcheck.py` | Validation |
| `aggregate.py`, `reduced.py` | Tables; status of reduced rooms |
| `enum/` | Copied Part A enumerator and classifier with a classify-only mode |
| `runs/table_final.md` | Coverage table by area |
| `runs/rinfo_hard_a6to12_B12.txt` | Undecided rooms: residue centres and radius |
| `runs/res_*.txt.gz`, `runs/shoot_a6to12.txt.gz` | Per-room results and shots, compressed |
| `runs/hard_a6to12.txt`, `runs/reduced_a2to14.txt` | Undecided rooms (plus one BIG room) and reduced rooms |
