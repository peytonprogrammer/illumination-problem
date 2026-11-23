# Census part A: all real interior pairs, W <= 22, area <= 16

Part A extends the phase 1 census (`README.md`) from same-class lattice pairs to
all pairs of real interior points. It covers every strictly simple orthogonal
lattice room with W <= 22 and area <= 16, up to the 8 lattice symmetries:
12,786,778 rooms.

## Answer

- **Task 1, different-class lattice pairs (area <= 16).** The census holds
  6,258,116 different-class pairs. All of them are lit. Each has a shooting
  certificate that `verify_plane` re-checks. Same-class pairs were re-run as a
  control: 792,133 pairs, 792,132 lit, which matches phase 1 exactly. The only
  survivor is the known pair of the 22-wall room. `orbitc` decides it DARK
  (2,592 states, complete).
- **Task 2, one-cylinder certificates (area <= 16).** Every room was
  classified with directions max(p, q) <= 15. Class (ii) rooms with
  |X / Z^2| > 2 got directions up to 25 inline, then up to 40 in a retry.
  - 1,060 rooms are reduced: they're diag(gx, gy) images of a smaller
    normalized room.
  - Class (i), X = Z^2: 5,384,089 rooms.
  - Class (ii), X strictly larger than Z^2: 4,646,223 rooms. After the retry,
    every one has |X / Z^2| = 2. The extra points are one coset of half-integer
    points: (1/2, 1/2), (1/2, 0), or (0, 1/2) mod Z^2. All 391,921,919 pairs
    of interior points of X with an endpoint outside Z^2 are lit, with verified
    certificates. That's 391,880,927 pairs inline and 40,992 in the follow-up
    runs.
  - Class (iii), no one-cylinder direction: 2,755,406 normalized rooms, 21.5%
    of the census.
- **Task 3, coverage.** 10,031,276 rooms are fully covered. 2,755,502 rooms are
  partial: the 2,755,406 class (iii) rooms plus 96 reduced rooms whose normal
  form is in class (iii). For the table by W and by area, see
  `partA-coverage.md`.
- **Dark pairs found.** One: the known pair of the 22-wall room, at census
  coordinates (1,3), (3,5). No other dark pair appeared in any task.

## Theorem supported by the data

The statement uses Lemma A and Theorem B
(`d3-two-mechanisms/audit.md`, accepted in `d3-review/review.md`). It also
uses Theorem A, the phase 1 census, and the computations in this directory.

**Statement.** Let P be a strictly simple orthogonal lattice room with
W <= 22 and area <= 16. Suppose that the normal form of P is in class (i) or
(ii): it has a certified one-cylinder direction (p, q) with p, q >= 1. That
holds for 10,031,276 of the 12,786,778 rooms. Then every pair of distinct
real interior points of P is lit, with one exception: the pair (0,0), (2,2) of
the 22-wall room.

Class (iii) means "no one-cylinder direction with max(p, q) <= 15". It
doesn't mean that no one-cylinder direction exists.

**Corollaries.**

- Every room with area <= 5 (21 rooms) has no dark pair of real interior
  points.
- Every room with W <= 6 and area <= 16 (189 rooms) has no dark pair of real
  interior points.
- Among the 2,623,533 fully covered W = 22 rooms, the 22-wall room is the only
  one with a dark pair.
- Among the 7,407,743 fully covered rooms with W <= 20, none has a dark pair.

**What the statement doesn't give.** The form "every room with W <= 21 and
area <= A has no dark pair" holds through this method only for A = 5. Area 6
already has two class (iii) rooms, both with W = 8:

- cells (0,0) (0,1) (0,2) (0,3) (1,1) (1,2), which has a mirror axis;
- cells (0,0) (0,1) (0,2) (1,1) (1,2) (1,3), which is symmetric under a
  half-turn.

The smallest asymmetric class (iii) room has area 7: cells (0,0) (1,0) (0,1)
(0,2) (1,2) (0,3) (1,3). It has no one-cylinder direction with
max(p, q) <= 31.

## Partial results for class (iii) rooms

These hold for all 2,755,502 partial rooms:

- Every pair of distinct interior lattice points, in all classes, is lit.
  This comes from Task 1 and phase 1, and the 22-wall room isn't in class
  (iii).
- Every pair with one rational and one irrational endpoint is lit, by
  Theorem A.

These hold for the 200,686 normalized class (iii) rooms with area <= 14:

- Every pair of distinct interior points of the (1/2)-grid is lit:
  81,894,589 pairs.
- Every pair of distinct interior points of the (1/3)-grid is lit:
  706,262,468 pairs. Of these, 6,429 needed shooting bound 120.

The grid runs check the (1/2)-grid and the (1/3)-grid separately. Pairs with
one endpoint in each grid aren't checked.

Two kinds of pair stay open in class (iii) rooms:

- rational pairs outside those grids;
- pairs with two irrational endpoints.

## Computed facts about class (iii)

- **Symmetry.** 2,753,559 of the 2,755,406 normalized class (iii) rooms have
  no lattice symmetry (99.93%). Only 5 have two mirror axes like the cross of
  Proposition X: 4 with exactly two axes and 1 with all 8 symmetries.
  Symmetry doesn't explain the class. Conversely, 101 rooms with two mirror
  axes are in class (i). For the full table, see `partA-totals.md`.
- **Parity.** In 2,096,524 class (iii) rooms, every tested direction gives a
  number of strips on M divisible by 4. So DP never splits into an odd number
  of strips. Every such room has even area. No odd-area class (iii) room has
  this property. The other 658,882 class (iii) rooms have some direction with
  an odd number of DP strips but still no one-cylinder direction.
- **Single strips.** Each of the 86,371,834 certified one-cylinder directions in
  the main run has exactly 2 strips on M. So each such cylinder of DP is a
  single strip, and the union-find step never ran.
- **Larger bounds.** Directions with max(p, q) <= 25 rescued 1 of the 12,802
  class (iii) rooms with area <= 12, and that room only reached class (ii).

## Interpretation (not proved here)

- The parity count suggests an obstruction for even area: the strip
  permutation of DP may have a sign that depends only on (p mod 2, q mod 2).
  At area <= 10, the parity of the DP strip count depends only on
  (p mod 2, q mod 2) in 6,169 of 6,193 normalized rooms. No proof is written.
- Lemma A' (same proof as Lemma A, not separately reviewed) works with any
  cylinder. It's the natural tool for class (iii) rooms, through pairwise
  cylinder-sharing tests in two-cylinder directions. Part A doesn't use it.
- The audit mentions a W <= 8 theorem in the record that may cover the small
  W = 8 class (iii) rooms. Part A doesn't rely on it.
- Self-pairs (S = T) aren't covered.

## Method

1. `partA-enum` is `enum_rooms.c` with an `all` flag. It writes every kept room,
   not only the eligible ones. Counts per (W, area) match phase 1.
2. `partA-cert` runs on each room.
   - **Task 1.** It shoots every pair of interior lattice points, as
     `shoot.c` does, with p+q <= 40. `partA-verify_plane.c` re-checks each
     certificate. It's `verify_plane.c` with a bitmap cell lookup and a larger
     size limit.
   - **Normalization.** If gx > 1 or gy > 1, the room is reduced and
     skipped. `partA-reduced.py` maps the 1,060 reduced rooms to their normal
     forms. Its count matches the census count.
   - **Cylinder count.** For each coprime (p, q), one permutation on slots
     (square, j) moves both the strips and the integer-leaf points. A leaf
     cycle is regular when none of its offset-0 slots is a corner lift.
     Union-find merges strips across regular leaves. One cylinder on DP means
     2 components on M.
   - **The lattice X.** Lambda is the span of (q, p) and (q, -p), kept in
     Hermite normal form [[a, b], [0, c]]. X is the dual of Lambda, so
     |X / Z^2| = a * c.
   - **Class (ii).** The room is scaled by the exponent e of X / Z^2. Each
     pair of interior points of X with an endpoint off Z^2 is shot in the
     scaled room.
   - **Class (iii).** The (1/2)-grid and (1/3)-grid checks run on scaled
     rooms.
3. Rescue mode (`partA-cert 120 ...` on survivor lines) re-shoots each survivor
   with p+q <= 120 and verifies it.

## Validation

- **22-wall room.** In list mode with max(p, q) <= 14, the one-cylinder
  directions are (4,7), (7,4), (4,9), (9,4), (8,11), (11,8), (8,13), (13,8).
  This matches the audit. The room is in class (i), and X is closed by (4,7)
  and (7,4).
- **Cross.** The 12-cell cross gives 62 directions with 6 cylinders on M and
  29 with 8, for 1 <= p, q <= 12. On DP that's {3: 124, 4: 58} with both signs,
  which matches `cylcount.py`. It has no one-cylinder direction.
- **Plus pentomino.** (1,1) and (1,2) are one-cylinder directions, and
  X = Z^2. This matches the audit.
- **L-tromino.** One cylinder exactly when p and q are odd. X / Z^2 is
  {0, (1/2,1/2)}.
- **Independent counter.** `partA-crosscheck_cyl.py` compares against
  `d3-review/surface.py` `cylinders()`, which traces leaves with exact
  fractions. It found 0 mismatches:
  - every 40th room of area <= 12 for p, q <= 6: 2,028 rooms, 46,644
    directions (`partA-crosscheck_cyl_all12.log`);
  - every 40th class (iii) room of area <= 12 for p, q <= 8: 321 rooms,
    13,803 directions (`partA-crosscheck_cyl_c3.log`).
- **Reproducibility.** The area-14 grid run repeats Task 1 and the class counts
  for area <= 14. Its counts match the main run. Class (ii) pair counts differ
  only because the grid run used a larger size limit, which fit more rooms
  inline.
- **Verification.** `verify_plane` rejected 0 certificates in all runs.
- **34-wall room.** It's in class (iii), with no one-cylinder direction for
  max(p, q) <= 15. It isn't parity-obstructed.

## Files

- `partA-enum.c`, `partA-cert.c`, `partA-verify_plane.c`, `partA-run.sh`:
  the pipeline.
- `partA-aggregate.py`, `partA-totals.md`, `partA-totals.json`: main run
  totals per (W, area), area <= 16.
- `partA-totals-g14.md`, `partA-totals-g14.json`: the area <= 14 run with grid
  checks.
- `partA-coverage.md`, `partA-final.py`: coverage per W and per area.
- `partA-reduced.py`, `runs/partA/post/reduced16.txt`: reduced rooms by
  normal-form class.
- `partA-aut.py`: translation automorphisms of (M, Sigma). This is an
  exploratory check. Most class (iii) rooms at area <= 10 have only the
  identity.
- `partA-orbitc-task1.log`: the orbit decider on the Task 1 survivor.
- `runs/partA/a16`, `runs/partA/g14`: job outputs, survivor lines, and class
  (iii) room lists for area <= 12.
- `runs/partA/post`: rescue runs and the C2BIG retry.

## Run cost

- **Main run (area <= 16).** 4 workers, 5,944 s CPU, 42.7 min wall on a
  shared machine with a load average near 100.
- **Grid run (area <= 14).** 4 workers, 1,115 s CPU, 5.5 min wall.

Area 17 would cost about 3 times the main run. It wasn't run.
