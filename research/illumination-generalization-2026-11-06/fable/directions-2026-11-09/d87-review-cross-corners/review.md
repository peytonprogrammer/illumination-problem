# D87: review of every-direction.md and corner-support.md

Date: 2026-11-20. Reviewer: independent referee. Files under review are the frozen
snapshots in this directory. The live originals in `qclass-closure/bbbb/` currently
have the same SHA-256.

| File | SHA-256 prefix |
|---|---|
| every-direction.snapshot.md | `ad1cbb4b` |
| corner-support.snapshot.md | `08d8031b` |

The brief had these two prefixes swapped. The contents match the live files.

## Verdicts

- **every-direction.md: sound.** The parity lemma is correct and covers every
  rational direction. The cross count (−4, 4, 4, 0) rules out both whole-room tests.
  The one claimed witness path is legal for every odd b ≥ 7. The note claims one lit
  pair, not all pairs.
- **corner-support.md: sound with one fixable gap.** All nine rows replay exactly.
  "Exactly nine" is correct, given that the R22 pair is dark. The disjointness and the
  ε ≤ 1/12 repair hold. The gap is in the cov4181 paragraph, which equates D66's
  algebraic "class d dark" with the direction-class route family.

## every-direction.md

### The lemma

For a primitive direction v = (p, q), the transverse coordinate in an integral chart
is det(v, z) + const. Sheet reflections keep coordinates mod 2, so its parity is
L = qx − py mod 2 on lifts of physical lattice points. That part is correct.

- **One cylinder.** convex-cylinder.md gives H = 2. Reflex corners are singular, so
  they're on the rim at even height. Convex corners in the open cylinder are τ-fixed.
  There are exactly two, at height 1. Each physical corner has exactly one point on
  M, so these are two distinct physical convex corners. The odd level sums to 2, and
  the even level sums to 4 − 2 = 2.
- **Two exchanged cylinders.** adjacent-cylinders.md gives H = 1. Exchanged
  cylinders hold no convex lift, because a cylinder that holds one is τ-preserved.
  So every corner is on one of the two rim trees. The trees are disjoint and sit at
  opposite transverse parities. A tree with t trivalent vertices has t + 2 leaves, so
  each level sums to 2.

Both cases inherit the normalization hypotheses (axis wall gcds of 1, r ≥ 1). D84
already accepted them.

### Coverage of all directions

Every primitive (p, q) reduces mod 2 to (1,0), (0,1) or (1,1). That gives
L = y, x or x + y. All rational directions in a lattice room are periodic, so this
list is exhaustive. It includes the axial directions. For the cross, the six level
sums are:

| L | Sums (L = 0, L = 1) |
|---|---|
| y | (0, 4) |
| x | (0, 4) |
| x + y | (−4, 8) |

None of these is 2. So both whole-room tests fail in every direction. The argument
uses no sampling.

The count holds for every odd b ≥ 3, because gcd(4, b − 2) = 1. The note needs
b ≥ 7 only so that S = (6, 0) is interior.

### Replays (`replay_cross.py`, `replay_cross.log`, 4.5 s)

- **μ counts.** The script recomputes μ from the cells. For the cross at
  b = 3, 5, 7, 9, 11, 21, μ = (−4, 4, 4, 0). The cross has 12 walls and r = 4.
- **Lemma controls.** In each passing direction, the lemma's level sums are (2, 2):
  - R22 in (4, 7), level L = x.
  - R22 in (7, 4), level L = y.
  - DBas in (−4, 1), level L = x.
  - U2 in (−1, 1), level L = x + y.
- **Leaf census.** I wrote a separate census on M. Either whole-room hypothesis forces
  exactly two closed half-offset leaves, swapped by τ.
  - All four controls give (N, swapped, fixed) = (2, 1, 0).
  - For the cross at b = 7, 128 directions give N ≥ 4. Those are 1 ≤ p ≤ 10 and
    |q| ≤ 10, plus the vertical axis.
  - For the cross at b = 9, 88 directions also give N ≥ 4.
  - This census is a sanity check. The proof doesn't depend on it.
- **Witness path.** The path (6,0) → (4,−2) → (−2,4) → (0,6) is legal for every odd
  b from 7 to 39. Its only wall contacts are (4, −2) and (−2, 4). Its midpoint is
  (1, 1), which is interior and in class (1, 1). The point (3, 3) is outside the room.

### "Lit" compared with d85

The note claims illumination for one specified pair only. d85 shows that
H_L(S) = ∅ for two sources per cross, at b = 7 to 17. Neither source claims that all
pairs are lit. The brief's phrase "yet all its pairs are lit" is stronger than both.

I ran a further finite check in `allpairs_b7.py` and `allpairs_b7.log`. It traces
every nonaxial even displacement with |D| ≤ 2·diam from every interior lattice point:

| b | Same-parity interior lattice pairs | All lit |
|---|---|---|
| 7 | 574 | Yes |
| 9 | 1066 | Yes |
| 11 | 1710 | Yes |

This is evidence for three values of b only. It isn't a proof for all b or for real
points.

### Smaller points

- The phrase "normalized BBBB" relies on cited results. Area 16b − 16 > 8r = 32 puts
  the cross in R* by the d63 corollary. A regular point of each parity excludes Q. I
  didn't re-derive these.
- The R22 paragraph checks out:
  - The reflex splits are 3/6 by x parity and 3/6 by y parity.
  - The trees have 7 and 13 edges.
  - The 15 and 33 uncovered differences match d84.
- The along-leaf equivalence is correct. As the note says, it's tautological and
  supplies no shot.

## corner-support.md

### Independent replay (`replay_corners.py`, `replay_corners.log`, 0.1 s)

I wrote my own tracer, `billiard.py`, which imports no D8 or D85 code. I typed R22
from the cell picture and matched it to the d8 archive. It has 22 walls, 9 reflex
corners and 13 convex corners. For each row, I ran both legs past the stated step
count. The results are as follows.

- **Legs.** Each leg first stops at C, at exactly t = 1 (or t = 3 for row 1's T leg).
  C has incidence 3. No earlier contact is forbidden.
- **Straight join.** The arriving velocities are exact negatives. The cells behind
  and ahead of C are both room cells, so the straight join is valid.
- **Intermediate sites.**
  - Row (0, −1) visits (0, −1), (2, −2) and (2, 1). The last two are smooth wall
    points.
  - The other eight rows each visit only C.
  - The nine site sets are pairwise disjoint. None contains S or T.
- **Corner as midpoint.** C is the midpoint in eight rows. In row (0, −1) it isn't.
- **Direction classes.** In every row, the direction class (p, q) mod 2 equals C's
  parity class. That matches h_x(∅) = 3 for each of the three classes.
- **Provenance.** All nine slopes match the archived D8 witness directions.

### "Exactly nine"

The lower bound holds because nine routes have singleton supports at nine distinct
corners. The upper bound holds because R22 has exactly nine reflex corners and the
pair is dark. So every relaxed route has a nonempty support among them. The note
states this dependence on darkness. The stronger lattice-blocker bound of 9 follows
from the disjoint site sets.

### ε repair

The gap argument is correct. A primitive line from a lattice point meets x = k at
ordinates in Z + (q/p)Z. A non-lattice contact is therefore at least 1/|p| from an
integer, and folding preserves that distance. The same holds for horizontal walls
with 1/|q|.

The largest component is 11, so 1/11 > 1/12 ≥ ε. Contacts can't reach the removed
wall pieces or the two new vertices at C ± ε along the walls. The new walls lie in
the former exterior, which the routes never enter.

My replay fills the missing cell at scale N. At N = 11, 12, 13 and 24, all 9 routes
are legal from S to T. The actual nearest wall contact on C's lines is at least 2/9,
in row (3, 2). So 1/12 is conservative.

The authors' checker traces only the full route from S at scale 12. That covers the
claim, because a legal route of length i + j from S that ends at T is the whole route.

### The fixable gap: cov4181

The support statement is correct by the parity lemma. Routes of direction class
(0, 0) from a source of class (0, 1) can meet only reflexes of classes (0, 1) and
(0, 0). The only such reflex is (6, 3).

The gap is the phrase "this failed class." D66's "class d dark on all four lift
pairs" is a per-target algebraic notion. The note's classes are first-step parity
classes, which the note itself separates from midpoint classes. The paragraph should
say that it bounds the direction-class-d route family. It shouldn't identify that
family with D66's dark class without an argument.

The counting identity min_A(|A| + Σ h_x(A)) is correct. It holds because a class-x
route's support lies in classes a ∪ x.

## Re-run

From this directory, run:

```
python3 -B replay_corners.py
python3 -B replay_cross.py
python3 -B allpairs_b7.py 7 30
python3 -B allpairs_b7.py 9 38
python3 -B allpairs_b7.py 11 46
```

Total CPU is about 60 s.
