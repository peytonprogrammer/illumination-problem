# d182 review: growth modes and period-one propagation

Date: 2026-11-22. Reviewer: independent referee. Reviewed file:
`d95-review-queue/snapshots/1933/l1-growth-modes.md`. Context read: PROGRAM.md,
d181, d152, and the d112 summary. Linked notes read: length-periodicity,
band-reachability, and the cross-placement and large-rectangle citations in the
table.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.74 CPU seconds, with exact `Fraction` arithmetic. `trace()` is copied
verbatim from d181, which copied it from d175. The only room is DBas, from d110
`geom.ROOMS`. Insertions are made at hand-chosen cuts in DBas only. Every traced
velocity is the one the note's slope formula prescribes from a named base shot.
No room, ray, direction or word search was run. The log has 38 PASS lines, 20
INFO lines for insertions below a proven threshold, and 0 failures.

## Bottom line

| Claim | Verdict |
| --- | --- |
| Chart finiteness, gap count (18, or 22 with lattice marks) | Sound |
| Subsequence and scale-class extraction | Sound. The √t caveat is correct and needed |
| Four-row case table | Sound and exhaustive. It's a partition by which gaps diverge |
| Transfer theorem: slope formula, identity, both bounds | Sound. Verified exactly in 5 configurations |
| Transfer theorem: strict simplicity, itinerary, both senses, mixed heights | Sound |
| DBas named control at t=100 | Reproduced exactly: k=14, s=16/57, 107/57, 18/57, 75/57, 139/57, 3 |
| Consequence for one separating corridor | Sound for the cut-insertion family. Needs one sentence for corridors whose cut meets other parts (Medium 1) |
| Contrapositive: dark at unbounded t on a ray implies dark on the whole ray | Correct. It is a genuine descent along rays, down to the ray's minimal member |
| Conflict with R22 (d152) | None. R22's dilation ray is a full dark ray at W=22, which the theorem allows |
| Note as a whole | **Sound with fixable gaps.** No High gaps. Two Medium gaps |

The note doesn't prove L1. It proves a one-seed, one-ray transfer that is
W-blind and non-uniform. That's what d152 says any W-blind result must be.

## What I verified

### 1. Classification

**Charts are finite.** With maximal walls, W=20 gives 10 vertical and 10
horizontal walls. Each axis then has at most 10 supporting lines and 9 gaps,
so 18 in total. Two lattice marks add at most 2 lines per axis, so 22 in total.
A chart is a cyclic turn word, plus a weak order of each axis's lines, plus the
edge-to-line incidences. Each of these is a finite choice.

**Every positive gap vector is valid.** The intersection and touching relations
of axis-parallel segments depend only on the order of their coordinates. A map
(x,y) ↦ (f(x),g(y)) with f and g increasing preserves that order, ties
included. So it preserves strict simplicity and the occupancy grid. The log
checks one such change of DBas, and the note's W=10 realization
(strictly simple, turn word LLLRLLLRLR).

**Extraction is correct.**

- Integral gaps are either bounded, so eventually constant on a subsequence, or
  diverge on a subsequence.
- Pairwise ratios converge in [0,∞] after finitely many more extractions.
- Positive finite limiting ratio is an equivalence relation among the diverging
  gaps. The classes are totally ordered.
- Area tends to infinity, so some gap diverges.

The note correctly says the bounded values and limiting ratios aren't finite
labels. It also correctly says the sequence needn't lie on a ray. For real
marks the mark gaps converge but don't stabilize. The note restricts the mark
extension to lattice marks, which is the right scope.

**The table is exhaustive.** Its rows are: one diverging gap; several, all on
one axis; both axes with no doubly diverging occupied cell; both axes with
one. This is a partition, up to exchanging axes. I didn't re-verify the cited
tails in the "Available tail" column. They match the reviews I read (d112,
d124, d161, d181).

### 2. Transfer theorem

**Strict simplicity.** A cut in an open x-gap meets no vertex. Inserting a_j t
in every occupied interval of the cut is a stretch of that gap. So it stays in
the chart, and the room stays strictly simple for every t ≥ 0. The new room
doesn't depend on where in the gap the cut sits. The cut position matters only
for which side each mark is retained on, and for avoiding the shot's finitely
many contact abscissas. Both choices are always possible.

**Algebra.** From s(X+Mt) = Xs₀ + MkP:

- X(s−s₀) + M(ts−kP) = 0, so X(s−s₀) + Me = 0.
- s−s₀ = M(kP−ts₀)/(X+Mt), and |kP−ts₀| ≤ P/2. This gives |s−s₀| ≤ MP/[2(X+Mt)].
- e = −X(s−s₀)/M, so |e| ≤ XP/[2(X+Mt)].
- The sufficient condition X+Mt > P·max(M,X)/(2η) makes both bounds less than η.

The log checks the identity and both bounds at every traced t.

**Strip crossings.** The inserted strip at an interval I is the product
[c, c+a_j t] × I. It has no vertical walls, and its corners lie in the
interiors of the lengthened horizontal walls. So a path entering the strip
crosses it with constant horizontal sign. It reflects only on the long walls.
In unfolded coordinates the crossing adds a_j t to horizontal travel and
a_j t s to vertical travel. The part a_j kP is a multiple of 2|I|, because P is
a common multiple of 2|I| over all crossed intervals. So it restores both
height and vertical sign. This holds for a crossing in either horizontal
sense, because the unfolded coordinate doesn't see the sense. The residual
shift is a_j e.

**Itinerary.** In the retained pieces the unfolded error is x(s−s₀) + be. With
e = −X(s−s₀)/M this equals (s−s₀)(x − bX/M). Since 0 ≤ x ≤ X and 0 ≤ b ≤ M,
it is at most X|s−s₀| in absolute value. The base shot has finitely many
transverse contacts and strictly interior gate crossings. These are open
conditions in (s,e), so a neighborhood argument is valid. The error vanishes
at x=X, b=M. So the retained target is reached exactly.

**P with mixed heights.** P must be a common multiple of 2|I| over every
crossed interval, at every cut. That's what the note says, and it's needed.
Case E below has one cut meeting intervals of widths 5 and 4, with P=40. A
control with P=8, a multiple of only one doubled width, misses at all 5 tested
t. P=10 hits at 3 of 5 t. Each hit has kP ≡ 0 or 4 modulo 8. A shift of 4 is
half the doubled width, which mirrors the right chamber about x=11. The target
sits at x=11, so these hits are a coincidence of a centred target.

### 3. Exact traces

**Named control (log §2-3).** DBas at L=4, from (1,3) toward (11,3) with
velocity (7,−2). The base trace touches (8,1) and (13,17/7). At t=100:

| Quantity | Note | Trace |
| --- | --- | --- |
| k, s | 14, 16/57 | 14, 16/57 |
| Entry height at x=5 | 107/57 | 107/57 |
| Signed corridor phase, mod 2 | 18/57 | 18/57 (upward-positive) |
| Exit at x=109 | 75/57, upward | 75/57, upward |
| Cap, target | 139/57, 3 | 139/57 at x=113, then (111,3) |

The trace has 30 contacts. The one vertical contact is the cap. All 29
horizontal contacts are on the corridor's long walls. The fixed slope 2/7
reaches the target at t=98 and misses at t=100, at (111,25/7). That matches
the note's "multiple of 7" remark.

**Thresholds.** The note states no threshold for its control. The uniform
error bound gives one. The itinerary is guaranteed once
XMP/[2(X+Mt)] < μ, where μ is the least transverse gate margin of the base
shot. I assert only above this threshold and log lower t as INFO.

| Case | Configuration | X, M, P, μ | Guaranteed for | Asserted t | Result |
| --- | --- | --- | --- | --- | --- |
| A | Named shot, corridor cut x=6 | 14, 1, 2, 1/7 | t > 84 | 100, 250, 2003/3, 999, 1001 | 5/5 reach target with base itinerary |
| C | Two crossings of one cut, both senses, ceiling and floor bounce | 22, 2, 2, 1/6 | t > 121 | 250, 999, 1001 | 3/3 |
| D1 | Cuts x=6 (height 1) and x=12 (height 6, crossed twice), weights 1,1 | 14, 3, 12, 1/7 | t > 583 | 1001, 5000 | 2/2 |
| D2 | Same cuts, weights 1,3 | 14, 7, 12, 1/7 | t > 586 | 1001, 5000 | 2/2 |
| E | Transposed: cut y=5/2, widths 5 and 4, down then up | 4, 2, 40, 1/2 | t > 158 | 250, 1001, 5000 | 3/3 |

The brief's 1001 is a multiple of 7, so case A at 1001 has s=s₀ exactly. I
added 999 and the non-integral 2003/3, which also pass. The theorem holds for
real t.

**Below threshold.** For case A, a per-gate bound gives t > 14. A full exact
sweep of t=0..60 fails only at t=2, 3, 4 and 10. At t=10, s=1/4 exactly and the
shot hits the corner (5,2). Below their thresholds, D1 and D2 miss at t=100.
C and E at t=37 reach the target by a different itinerary. None of these
contradict the theorem.

**Re-basing (log §4).** I treated t₀=37 as a new base, with s₀=14/51 and
X=51. Inserting 100 and 1001 more both reach the target. This is the step the
contrapositive uses.

### 4. Consequence for one separating corridor

**Eventual constancy is correct.** Suppose a residual placement is lit at some
length L₁ beyond the collar threshold. The theorem with base L₁ lights it at
every L ≥ L₁ + T(L₁). Otherwise it is dark at every length beyond the
threshold. So each placement's status is eventually constant. Finitely many
placements give eventual constancy for the list. The note correctly calls
this qualitative.

**The contrapositive is correct, and stronger than stated.** Take a ray
R(t) = R₀ + t·a in gap space, with integer weights a and a lattice placement on
retained pieces. Any member R(t₀) is itself an integral room, and R(t) is
R(t₀) with insertion (t−t₀)a. So if R(t₀) were lit, R(t) would be lit for all
large t. Hence darkness at unboundedly many t forces darkness at every member
of the ray. That includes members with t₀ < 0, down to the minimal member,
where some gap reaches its least value.

**Row 1 corollary (not stated in the note).** Take lattice marks and the
mark-extended chart. In row 1 every other gap is eventually constant, so the
extracted sequence lies on one ray with a single unit weight. An unbounded
dark sequence in row 1 therefore yields a dark room with that gap at its least
value. That is a one-step area descent. It doesn't bound area, because the
other gaps are only constant along that sequence, not bounded over all
sequences.

**What's missing for arbitrary sequences.**

- **Several gaps at a bounded offset from a ray.** For two cuts take
  (t₁,t₂) = (n, n+c) with c fixed. The itinerary needs |t_j s − k_j P| small
  for both j at one s near s₀. Subtracting gives c·s within about (c+2)η of PZ.
  If c·s₀ is farther than that from PZ, one seed fails for every n. A seed at
  base (0,c) covers this family. So the input is a seed at each base, with η,
  P and X uniform in the base.
- **Drifting ratios.** In general the reach of one seed in (t₁,t₂) is
  given by a simultaneous Diophantine condition. Fixed integral directions from
  the seed always satisfy it, and that is the theorem. Off those rays it can
  fail on whole families, as above. So the reach is not a cone. The note's
  "incompatible phase corrections" sentence is right. This makes it precise.
- **Perpendicular gaps (rows 3 and 4).** A horizontal cut adds t/s to
  horizontal travel. One free slope then has to satisfy two Diophantine
  conditions, one in s and one in 1/s. The same issue arises.
- **Real marks (L3).** Bounded real mark gaps converge without stabilizing.
  The threshold depends on the shot, so the theorem gives no uniformity over a
  convergent family of real marks.
- **Seeds.** The theorem never supplies the first lit length. The note's
  "first open case" says this correctly.

### 5. R22 and d152

There's no conflict.

- **Arm slices.** d152 reports that R22 is dark at arm length 1 and lit at
  length 2 and at large lengths. The theorem propagates lit to lit upward. It
  says nothing about lit at 2 versus dark at 1.
- **Dilation ray.** Dilation is a ray in the mark-extended chart, with weights
  equal to the base gaps. Exact similarity makes R22's dilates dark for every
  dilation factor. So R22 lies on a full dark ray at W=22, and the
  contrapositive just returns R22 as its minimal member.
- **Uniformity.** d152 shows that no W-blind theorem gives a uniform tail
  threshold. The transfer theorem is W-blind and its threshold depends on the
  seed, so it's consistent.

**Where W ≤ 20 must enter.** The dilation ray shows that full dark rays exist
at W=22. So a ray descent alone can't reach a contradiction. W ≤ 20 has to
supply at least one of these:

1. Every ray in a W ≤ 20 chart has a lit member, for each lattice placement.
2. Seeds whose X, P and gate margin μ are bounded uniformly over the bases
   that a drifting sequence visits.
3. A direct whole-room theorem for the multi-gap rows.

The note's last paragraph says the same, in one sentence.

## Gaps

### High

None.

### Medium

1. **The consequence uses a different insertion than the theorem.** The theorem
   inserts length in every occupied interval of the cut. The d110 and d181
   corridor families translate one end chamber along the corridor. These
   agree only when the vertical line through the corridor meets the room in
   the corridor alone. An end chamber that wraps over the corridor breaks
   this. The proof never uses the other intervals. It needs every crossed
   interval stretched and the pieces translated rigidly. So it also applies
   to inserting length only into a separating cross-section, whenever the
   result stays strictly simple. Add that sentence, or restrict the
   consequence to corridors whose cut line meets only the corridor.
2. **No explicit threshold.** The note states the η-box condition but computes
   no η for its control. The box condition is valid but loose. For the
   control it needs η < 2/63, which gives t > 427, so the note's own t=100
   example lies outside it. Add the single-margin form: XMP/[2(X+Mt)] < μ,
   with μ the least transverse gate margin. It gives t > 84 for the control.
   Contacts on horizontal walls need their margin multiplied by s. Any later
   uniformity argument needs this formula, because it names the quantities
   W ≤ 20 must bound: X, M, P and μ. It parallels d181's Medium gap 1.

### Low

1. **State the row 1 corollary and the descent to the minimal member.**
   Section 4 above has the precise form. The note's "first open case"
   paragraph gestures at it without the descent to t₀ < 0.
2. **The parity sentence isn't needed.** The theorem holds for every real t,
   so a seed of either parity lights all large integer lengths.
3. **P can be per cut.** P is sufficient. The weaker requirement is that
   a_j·kP is a multiple of 2|I| at cut j. Integer weights can also be relaxed
   to rationals, by absorbing the denominators into P.
4. **Name the phase convention.** "18/57 modulo 2" is the upward-positive
   signed phase relative to the corridor floor. Say so.
5. **Cite scope of the table's tails.** The "Available tail" column restates
   other reviews. Mark it as cited, not re-proved here.

## What this means for L1

**What the note gives.**

1. A finite, W-dependent classification of growth modes, with at most 22 gaps
   at W ≤ 20 for lattice-marked rooms.
2. A ray descent: if one placement is dark at unboundedly many points of an
   integral growth ray, every member of the ray is dark, down to its minimal
   member.
3. For row 1 with lattice marks, any unbounded dark sequence lies on such a
   ray. So it yields a dark room with the diverging gap at its least value.
4. For a fixed separating corridor, each residual placement has an eventually
   constant status. One lit length per placement suffices for all large
   lengths.

**What it doesn't give.** An area bound. The descent keeps the other gaps,
which aren't bounded across sequences. Rows 2 to 4 need not lie on rays. One
seed's reach in a multi-gap family is a Diophantine set, not a cone. R22's
dilation ray shows that full dark rays exist at W=22. So the descent can only
close L1 together with a W ≤ 20 input.

**Cleanest statement of what remains.** For a lattice-marked room B and a gap
i, let T_i(B) be the least guaranteed threshold XP/(2μ) over lit witnesses
that cross cut i. Set T_i(B) = ∞ if B is dark. The theorem gives this
descent: if R = B + t·e_i is dark and t > T_i(B), then B is dark. Two inputs
would use it.

- **(Seed)** For every W ≤ 20 chart, gap and lattice placement, some member of
  each single-gap ray lights the placement. This is per ray and needs no
  bound. It rules out unbounded dark sequences in row 1, for lattice marks.
- **(Relative threshold)** A bound on T_i(B) in terms of W and B's other
  gaps, strong enough that darkness of R forces every gap of R to be small
  against the rest. A bound in W alone is impossible, because P is at least
  twice the crossed interval height. So the bound must be relative, for
  example T_i(B) ≤ F(W)·h_i(B) with h_i the crossed height. That would bound
  the aspect ratio of dark rooms. Bounded-aspect growth would still need its
  own argument.

d152 shows that a W-blind version of either input fails, because R22 and its
dilates are dark at W=22.

The smallest W ≤ 20 case this note leaves open is the one it names: W=10,
LLLRLLLRLR. For a growth-mode target, the DB55 top-line stretch at L=3 from
d181 is a single-gap ray (row 1). There, (Seed) asks for one lit height H for
each lattice placement. Normalization isn't needed, since the theorem doesn't
use it. That is the natural first test of the descent.
