# D154: review of r22-arm-descent.md (snapshot 2026-11-22 03:35)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/r22-arm-descent.2026-11-22-0335.md`.
Context: `qclass-closure/bbbb/` notes `clean-site-cost.md`, `dyadic-classes.md`,
`exclusion-descent.md` and `parity-shortening.md`, plus the d114, d124, d145,
d146 and d152 reviews.

Code: [checks.py](checks.py), log [checks.log](checks.log). It runs in under
1 CPU-second, including the d8 orbit decider in early-stop mode. It uses named
rooms only: R22, cov4181, the 3-cell L-room, the R22-L1-027 junction, d152's
three-chamber room, the three R22 arm slices for L = 1..10, and the V-notch B.
It runs no room, direction or witness search, and makes no network calls.

## Verdict

**Sound with gaps.** Both gap lemmas are correct as stated for normalized
orthogonal rooms. The R22 arm check is correct, and its lit verdicts hold
after re-tracing. The consequence in item 4 is valid only in a narrow sense.
For normalized orthogonal rooms, the known structural certificates bound every
gap, which bounds the room to a box of side at most 270. But at W ≤ 20 those
certificate types are already closed, so the finite set is empty. The finiteness
says nothing about the open BBBB case. It also fails once 45° walls are in scope.

## 1. Gap lemma A (corner-only fiber forces G ≤ 2)

**The proof is correct.** Let a < b be consecutive distinct abscissas of
vertical walls, taken over the whole room. The following steps hold:

- No vertical wall has abscissa in (a, b). Every horizontal-wall endpoint is a
  vertex, and vertices lie on vertical-wall abscissas. So every horizontal wall
  that meets the open slab spans it, and the vertical cross-section is constant
  on the slab.
- The interior meets the slab, because the room is connected and spans
  [min x, max x]. The cross-section is a union of intervals with integer
  endpoints, so it contains a unit row [y, y+1] across the full slab.
- At an intermediate integer abscissa c, the points (c, y) and (c, y+1) each
  touch two row cells and aren't vertices. So each is an interior point or a
  smooth wall point.
- For G ≥ 3 there are two consecutive intermediate abscissas. With y and y+1,
  they cover all four parities. Each class gets at least floor((G−1)/2) points.

**Edge cases.**

- *Thin rooms.* A unit-height row is all the argument needs. The
  three-chamber room has unit corridors, and its gaps 3 and 4 each give a full
  row with regular ends in all four classes.
- *Perpendicular walls inside the slab.* They span the slab, by the
  constant-section step, so they can't block the row. The check confirms
  constant sections on every gap ≥ 3 tested.
- *Whole-room versus local gaps.* The note sorts supporting-line coordinates
  over the whole room, which is the right choice. A local gap, inside one
  component of a slab, is at least the whole-room gap. So the local version is
  also true, but it's weaker than needed for the box bound. The note's usage is
  consistent.

**Tests.** Every room with a corner-only class has max gap ≤ 2. In every room,
each class has at least floor((G−1)/2) regular points.

| Room | W | Max gap | Corner-only classes |
|---|---:|---:|---|
| R22 | 22 | 1 | (1,1): 0 regular, 9 corners |
| cov4181 | 20 | 2 | (1,0): 0 regular, 14 corners |
| L-room (3 cells) | 6 | 1 | (0,0) and (1,1) |
| R22-L1-027 (junction J) | 20 | 1 | (1,1) |
| three-chamber X = Y = 4 | 20 | 4 | none (10 regular per class) |

Cov4181 is the sharpest test: gaps of exactly 2 coexist with a clean class.
That shows the bound G ≤ 2 can't be lowered to 1.

## 2. Gap lemma B (proper clean quotient forces G ≤ 4r − 2)

**The budget argument is correct.** Q is the room's pillowcase double, a sphere.
N is an intermediate sphere, and Q → N has inner degree k. At a site x clean on
N, every N-point is a pole or a zero. A regular Q-point over x can't lie over a
zero: it would be unramified there with cone angle 3π, which makes it a reflex.
So it lies over a pole with local degree 2, and costs one unit of Riemann–Hurwitz
ramification. The total budget for Q → N is 2k − 2. Physical regular points
inject into the regular Q-points, so Lemma A's count gives
|J|·floor((G−1)/2) ≤ 2k − 2. The check confirms that the largest such G equals
2·floor((2k−2)/|J|) + 2 for k ≤ 8 and |J| ≤ 4. With |J| = 1 and k = r = 8, the
bound is G ≤ 30.

**The step k ≤ r needs a zero on N, and the note should say why one exists.**
A zero of N has k unramified preimages, and each is a distinct physical reflex.
The note writes "with a downstairs zero" as a hypothesis. The zero is in fact
automatic for a normalized proper factor. A zero-free N is a four-pole sphere,
which would give an unramified isogeny. `exclusion-descent.md` rules that out
using the absolute periods 2ℤ². The word "proper" is load-bearing: N = B is clean
at all four sites and has k = n (gap 4).

**Named cases.**

- *R22 staircase.* k = 3, and J is the three off-source classes, with
  Σq = 2 + 2 + 0 = 4 = 2k − 2. The bound gives G ≤ 4. The actual max gap is 1.
- *Cov4181 four-sheet quotient.* n = 28 = 4k, so k = 7 ≤ r = 8. With J = {c},
  the bound gives G ≤ 26. The actual max gap is 2.

The lemma also covers the different-site mechanism of `exclusion-descent.md`,
because J may be any clean site on N.

## 3. R22 arms

**Confirmed.** For each arm, `checks.py` builds R22 with arm length L = 1..10.
At L = 2 the rooms equal d8's named R22-L1-007, R22-L1-025 and R22-L1-012. Every
room has W = 22, r = 9, both axis gcds equal to 1, and is strictly simple. Each
named vertex is convex, with one incident cell, at L = 1. For every L from 2 to 10
it's a smooth wall point with two cells. At every L ≥ 2 no parity class is
corner-only.

**Lit at length 2.** I ran d8's orbit decider with all pairs wanted. All three
runs returned EARLY, which means every unordered pair was lit.

| Room | Regular points | Pairs | States | Unlit |
|---|---:|---:|---:|---:|
| R22-L1-007 (bottom) | 10 | 45 | 940 | 0 |
| R22-L1-025 (right) | 10 | 45 | 1,038 | 0 |
| R22-L1-012 (top) | 11 | 55 | 864 | 0 |

The control is R22-base, which gave DONE after 5,184 states. Its 4 dark pairs
include (0,0)–(2,2).

I re-traced every witness with d8's Fraction tracer, which d152 didn't do. One
witness fails: R22-L1-025's pair (4,0)–(5,0) has the decider witness D = (1,0).
That's a segment that runs along the wall y = 0, and the tracer rejects it. The
single bounce D = (1,2) off the arm's top wall re-traces correctly. So the
verdict holds (gap 6).

**Precision of "fails exactly there".** The top arm has two odd–odd cap corners,
(1,3) and (3,3). Both become smooth at L = 2. The bottom and right arms each have
one odd–odd cap corner. Lemma A gives a stronger statement than the note's
incidence argument. At arm length L the max gap is L. So for L ≥ 3, Lemma A
alone shows that no physical fiber is clean, and L = 2 is a direct check. For
fold certificates, Lemma B with r = 9 only rules out L ≥ 35 (gap 5).

## 4. Consequence: is the set of known-certificate dark rooms finite?

**The arithmetic is valid.** A normalized orthogonal room has W/2 = r + 2
vertical walls, so it has at most r + 2 distinct abscissas and r + 1 gaps. The
same holds for ordinates. If every gap is ≤ C, the room fits in a box of side at
most (r+1)·C. For r ≤ 8 and C = 30 that's 270. There are finitely many
strictly simple lattice rooms in such a box up to translation. So both
ingredients are present: a bound on each gap, and a bound on how many gaps
exist.

**It covers only what the hypotheses cover.**

- *The set is empty, by existing results.* Physical corner-only rooms below 22
  walls are closed by the all-area theorem. The proper-canonical-factor branch is
  closed for interior lattice pairs by d64. So at W ≤ 20 there are no
  known-certificate dark rooms. Finiteness is true but adds nothing. The open
  problem is a BBBB room whose darkness has no such certificate (gap 1).
- *What's missing is certificate completeness, not the gap bound.* The note's
  "decisive lemma" is the missing step: total darkness forces a clean physical
  fiber or a proper clean quotient. Without it, the finite set doesn't constrain
  the actual dark rooms.
- *"Known certificate type" needs a definition.* The d8 orbit scans and d66's
  cov4181 exclusion of class (0,1) are certificates. d66's exclusion has no
  recognized parity certificate, and neither kind yields a gap bound (gap 3).
- *Normalization.* The bound holds for gcd-one rooms. Dilates mR are infinite in
  number. A dark lattice pair of 2·R22, such as (0,0)–(4,4), is certified only
  through R22 at rational marks (gap 4).
- *45° walls.* The project target includes them, and the lemmas don't transfer
  (gap 2).

So the claim "known-certificate dark rooms with W ≤ 20 form a finite set" holds
for normalized orthogonal rooms with structural certificates. Both certificate
completeness and the 45° extension are missing. Completeness is the substantive
gap.

## 5. Scope

The note keeps its scope accurate in most places. It says R22 supplies no value
of C, that the descent conjecture excludes mixed-wall rooms and real marks, and
that the arm check rejects certificates without proving completeness. Two
statements overreach slightly:

- "The certificate fails exactly there" doesn't mention the second odd–odd top
  corner.
- "All 10 pairwise lit" rests on one wall-grazing decider witness. A legal
  alternative exists.

The mixed-wall control shows the orthogonal framework is genuinely narrower. The
V-notch B has r = 1 and an axis gap of 4, which exceeds 4r − 2 = 2. It also has
four clean sites on its degree-three torus quotient X/C₃, which
`clean-site-cost.md` records. A normalized orthogonal room can't have a clean
torus quotient, because its absolute lattice is 2ℤ². Mixed rooms can. So a gap
lemma for 45° rooms needs a new proof.

## Gaps

1. **High.** The finiteness consequence is vacuous at W ≤ 20. Existing theorems
   already show that no room with a known structural certificate is dark there.
   The missing step is certificate completeness, the note's decisive lemma. The
   gap lemmas don't approach it.
2. **High (relative to the project target).** The gap lemmas and the
   (r+1)·C box are orthogonal-only. The V-notch B is a mixed room with clean
   torus-quotient sites and axis gap 4 > 4r − 2. "Every known certificate type
   forces gaps ≤ 30" is false once 45° walls are in scope.
3. **Medium.** "Known certificate type" is undefined. Computational
   certificates, such as d8 DONE scans and d66's orbit exclusion, give no gap
   bound. The finiteness claim needs an explicit list: physical clean fiber,
   proper clean pillowcase factor at any site, and the R22 staircase fold.
4. **Medium.** Lemma B silently relies on two facts from
   `exclusion-descent.md`. A normalized proper factor has a zero, via the
   isogeny exclusion, and "proper" excludes N = B. Finiteness also holds only
   for normalized rooms. Dilates are infinite and carry certificates only
   through rational marks.
5. **Low.** On the arms, the note proves only that the physical odd–odd fiber
   becomes dirty. Lemma A gives a cleaner all-fiber statement for L ≥ 3. Fold
   certificates are excluded only for L ≥ 35, since G ≤ 4·9 − 2 = 34. The top
   arm has two odd–odd cap corners, not one.
6. **Low.** The d8 decider accepts a wall-grazing segment as a LIT witness:
   R22-L1-025, (4,0)–(5,0), D = (1,0). The verdict survives with D = (1,2).
   Project-wide, DONE-scan DARK verdicts are unaffected. LIT verdicts that d152
   and others didn't re-trace could rest on grazing segments.
