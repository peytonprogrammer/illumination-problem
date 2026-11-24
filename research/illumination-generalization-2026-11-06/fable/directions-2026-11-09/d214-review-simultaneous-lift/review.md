# D214: review of simultaneous lift and two-scale selection

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: [note-snapshot.md](note-snapshot.md).
Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
1.9 CPU-seconds under `nice -n 10` and reports 30 PASS, 0 FAIL.

To rerun it, use `nice -n 10 python3 -B checks.py`.

`checks.py` imports the d212 exact tracer and the d213 staircase helpers
(`stair_room`, `run_order`, `interval_Ns`, `lu`, `first_ns`) unchanged. Every
traced ray is a direct chord, the template seed, or a re-aim at an explicit
winding. No room class, direction, word, or room size was searched. F was not
enumerated. The rooms used are the named staircase (and its height variants
for the cone test), the tiers room, and four hand-built rooms for Claim 9.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Positive lower density 1/64 + 1/882; window bound 2(D+y)/(bH) | CORRECT |
| 2 | Direct-chord simultaneous lift; t=15 numbers | CORRECT |
| 3 | Convex-cone ratio region | CORRECT (minor scope gaps) |
| 4 | Multi-band lemma | CORRECT WITH GAPS (proof read only) |
| 5 | Transparent collapsing band | CORRECT WITH GAPS (proof read only) |
| 6 | Two-scale theorem | CORRECT (threshold x ≥ 9 is not sharp) |
| 7 | Finite base F and minimal-counterexample logic | CORRECT WITH GAPS |
| 8 | Bound 867,415,174,096,573,784 | CORRECT |
| 9 | Room-first Burnside / inclusion–exclusion count | CORRECT |
| | **Overall** | **CORRECT WITH GAPS** |

No mathematical error was found. The main finding for the program is in
Claim 2: the √2 staircase pair is directly visible for every t, so item 3 of
F already discharges it. The note's simultaneous lift is correct, but it is
the direct chord, not a new lighting mechanism.

## Claim 1: positive lower density

**Window bound.** l and u are the nearest fractions with denominator ≤ H
strictly below and above s. Each differs from s = a/b by at least 1/(bH), so
u − l ≥ 2/(bH). The log confirms this on all 4,118 (t, order, n) cases with
t ≤ 200. The remark that (D+y)/H² isn't a uniform window size is right.

**Mod-8 class.** s = 3/4 needs n = x/8, and exact replay in a width-3 band
needs 3E/4 ≡ 0 (mod 6), so E ≡ 0 (mod 8). For t ≤ 200 the class is
{40, 136, 176}. All three pass the interval test in both orders. Exact traces
show δ = 0 at both stages, the gate passes, and the ray reaches T.

**Mod-42 class.** This is d213's reviewed theorem. t = 731 and 1319 pass the
interval test, and both gains are odd. t ≡ 17 (mod 42) is odd, so the class is
disjoint from the mod-8 class.

**Density.** For t = mk + r, ⌊√2t⌋ mod m is ⌊m{k√2 + r√2/m}⌋, a window of
length 1/m. Weyl equidistribution gives 1/64 and 2/42² = 1/882. Up to t = 10⁶
the counts are 15,625 and 1,134, which match exactly to rounding. The density
exists, so the lower density is at least 1/64 + 1/882 = 473/28224.

The note's own caveat stands: this is about the strict certificate, not
lighting. Positive-density failure is not addressed.

## Claim 2: direct-chord simultaneous lift

The chord from S = (2, 1) to T = (5, 5+x+y) has displacement (3, D*) with
D* = 4+x+y. At ordinate Y the abscissa is 2 + 3(Y−1)/D*. The interfaces at
Y = 2, 3+x, 4+x+y give the stated values. The middle crossing lies in (3, 4)
if and only if D* < 3(2+x) < 2D*, which is y < 2x+2 and x < 2y+2.

The log checks the following:

- The formulas and the "if and only if" hold for all 0 ≤ x, y < 40, exactly.
- Exact traces agree with the two inequalities on the full 26 × 26 grid
  0 ≤ x, y ≤ 25. There are no mismatches.
- For y = ⌊√2t⌋, the chord is legal for every t = 0..200. The proof for all t
  is one line: 2y + 2 > 2(√2t − 1) + 2 ≥ t, and y ≤ √2t < 2t + 2.
- The t = 15 numbers are right. D* = 40, gcd(3, 40) = 1, the crossings are
  83/40, 131/40, 197/40, the clearance is 11/40 (at the middle crossing,
  distance to 3), and the area is 126. The chord is legal by exact trace.
- The limit abscissa 2 + 3/(1+√2) ≈ 3.243 is inside (3, 4).

**Finding.** The exact segment test in the log shows the open segment S–T
lies inside the room interior for every t = 0..200. The inequalities prove
this for all t. So every √2 staircase pair is directly visible. Item 3 of the
finite-base section discharges it, and it was never an L1 obligation. The note
says "this room requires no new base check", which is consistent. The note
should also say that the pair is directly visible. The d213 "open case" at
t = 15 was a gap in the certificate only, as d213 already said.

## Claim 3: convex-cone ratio region

The inequalities are the chord equation at each interface multiplied by
H > 0. They are homogeneous and strict, so the region is an open convex cone
in the positive orthant. Necessity holds because a crossing outside the open
overlap hits a wall or a corner. Sufficiency holds because each segment joins
relative-interior points of opposite edges of a rectangle tier.

Exact traces agree with the cone test on 576 staircase height variants (374
inside) and on 150 tiers rooms with S = (1, 1), T = (5, top−1). The t = 15
deformation from (0, 0) to (15, 21) stays inside, since both inequalities are
linear in λ and hold at both ends.

**Gaps (low).**

1. State that the tiers are stacked along one axis with every interface a
   single open overlap, and that h₁ and h_last are positive (marks interior to
   the end tiers).
2. The face remark is only continuity of strict inequalities. The note says
   equality needs a separate argument.

## Claim 4: multi-band lemma

The argument is the standard open-condition stability of a regular unfolded
itinerary. It is correct. Independent positive scaling of the two axes
commutes with reflections in axis-parallel walls, so normalizing each axis
separately is legitimate for orthogonal rooms. Marks sit on cut levels and
move piecewise linearly with the gaps. This review checked the proof by
reading only. The direct-chord and cone checks are consistent special cases.

**Gaps.**

1. Medium. The neighborhood is not quantified. Without a radius or a
   compactness argument over the closed ratio simplex, no finite cover
   follows. The note says this.
2. Low. Define "regular": no corner hits, no tangency to a wall, marks off
   the walls, and strict order of transverse hits. The proof uses all four.
3. Low. State the axis-scaling invariance explicitly. The proof uses it.

## Claim 5: transparent collapsing band

The proof is correct under its hypotheses. A transverse crossing has bounded
slope, so the drift across a band of normalized thickness ε is O(ε). The
crossing stays inside the common column of both adjacent pieces and of the
inserted component, so it meets none of the new short vertical walls. Away
from the collapsed level, ordinary stability applies. The listed exclusions
are the right ones: corner hit, missing overlap, reflection inside the layer,
and a mark on the layer. This review checked it by reading only. No
collapsing-band room was built, because that would need a new room family.

**Gaps.**

1. Medium. The limit object is not a room in the class. "Ordinary itinerary
   stability" outside the neighborhoods must be stated for this degenerate
   limit: the other gaps converge to positive values while ε → 0.
2. Low. The lemma assumes the x-ratios converge too. Say so.
3. As stated in the note: iteration across several vanishing scales needs
   compatible crossings at each scale. That isn't proved.

## Claim 6: two-scale theorem

The proof is correct.

- d213 reviewed that the first-stage gate set is (1/2, 1) in both orders.
- For D ≥ 10, the interval (D/2, D) contains an integer ≡ 3 (mod 6). This
  holds for every x ≥ 6. The note's x ≥ 9 (length > 6) is sufficient but not
  sharp. The log lists x = 0..11.
- The reduced denominator b of s is ≤ D, and H = x + 2 < D. So the window
  width is at least 2(D+y)/(bH) > 2(D+y)/D². This exceeds 6 when
  y > 3D² − D. An open interval longer than 6 contains every residue
  mod 6.
- The interval test equals the signed gate (d213), and gate-passing lifts
  are legal (d212/d213).

The log checks x in {9, 10, 11, 15, 20, 40, 100}, each with four y at or above
the threshold. Every first-stage n has width > 6 and a passing N. Full
two-stage lifts were traced exactly for x = 9, 10, 20 at y = 3D² − D + 1,
with the smaller gain on either band. All six pass the gate and reach T. At
x = 9, y = 495 the direct chord is illegal, so the theorem covers rooms the
direct chord misses. The theorem doesn't use the √2 relation.

**Gaps (low).**

1. The phrase "M ≤ D in the reviewed level-error bound" isn't needed. The
   Farey bound above suffices. Replace it with the one-line computation.
2. x ≥ 6 suffices.

## Claim 7: finite base F

**Characterization.** The wall set on each axis contains 0 and B. So
X ∪ {Sₓ, Tₓ} = {0, …, Bₓ} holds exactly when every refined gap is a unit gap,
which is when no gap can shrink. The rank map is an increasing piecewise-linear
homeomorphism on each axis, so it preserves strict simplicity, incidence,
turns, and interior lattice marks. The equalities therefore characterize
irreducible marked charts exactly, for the one-gap shrink move. The staircase
template satisfies both equalities (area 18, census side). The t = 15 room
fails the Y equality.

**Size limits.** There are at most W/2 ≤ 10 distinct wall levels per axis, plus
two marks. So B ≤ 11, at most two levels are missing per axis, and the area is
at most 121.

**Minimal-counterexample logic.** The logic is valid. Take a dark pair of
least area. Each of the following discharges it:

- Area at most 21: the census.
- W ≤ 8: Theorem S.
- Direct visibility.
- An irreducible chart: it lies in F.

Otherwise, shrink one gap of width ≥ 2 by one. This keeps W, strict
simplicity and the marks, and lowers the area. That parent's pairs are lit by
minimality, and the lift hypothesis lights the child. Selection is therefore
needed at reducible areas 22 through 121. The correction is right.

**Gaps.**

1. High, scope. The lift hypothesis is the whole inductive content. "Every
   reducible marked room of area > 21 admits a passing lift or another
   lighting proof" is L1 for reducible rooms. F shrinks the base, not the
   step. The note states this ("Lighting F alone proves neither selection nor
   ratio coverage").
2. Low. The scope is lattice marks in orthogonal rooms. 45° walls and real
   marks are outside it, as in d212.
3. Low. Item 3's "area > 21" relies on d206's census for all W ≤ 20 rooms
   through area 21. d206 notes that the through-21 total reuses unaudited d9
   same-parity data.

## Claim 8: numerical bound

The recomputation in exact rationals gives
ceil(½ Σ) = **867,415,174,096,573,784**, which matches.

The justification is sound:

- A rectilinear polygon with W = 2m maximal walls has 2m vertices. Strict
  simplicity makes them distinct lattice points, one per 0-1 matrix entry.
  Every used level has positive even degree.
- Stub matching: each simple matrix arises from exactly ∏dᵢ!∏eⱼ! labeled
  matchings, so the count is at most (2m)!/(∏d!∏e!). The log confirms this
  against exact 0-1 counts on six margin pairs.
- (2m)![zᵐ]fᵏ sums the multinomials over ordered even-degree sequences on k
  levels. Squaring the per-axis sum combines independent row and column
  data.
- P(k) matches a direct order-type count of two ordered interior coordinates
  on k levels, for k = 2..10.
- Ordered pairs include coincident marks. Unordered distinct pairs number at
  most half the ordered count, so the factor ½ is valid.

The bound ignores item 2's "at most two missing levels" constraint, so it is
very loose. That is not an error.

## Claim 9: room-first count

The identity is correct. For a fixed g, Σ_J (−1)^|J| C(g, J) counts g-fixed
pairs that touch every tagged missing level, by inclusion–exclusion. The
covering condition and direct visibility are G-invariant, so Burnside's lemma
counts orbits. The log compares it with a brute-force orbit count on four
hand-built rooms, each with two predicates (nondirect, all pairs):

| Room | G | Missing levels | Formula = orbits |
| --- | ---: | --- | --- |
| L-shape 4×4, arm width 2 | 2 (diagonal) | x 1,3; y 1,3 | 1 = 1 (both predicates) |
| Symmetric U 5×4 | 2 (mirror) | x 1,4; y 1,3 | 1 = 1 (both) |
| Plus 4×4 | 8 | x 2; y 2 | 0 = 0 nondirect; 2 = 2 all |
| Plus 6×6 (3 missing per axis) | 8 | x 1,3,5; y 1,3,5 | 0 = 0 (both) |

The covering pairs in the two-missing-per-axis rooms are diagonals of the
missing-level rectangle, as the note says. The rejection rule (more than two
missing levels on an axis) follows from |X| ≤ 10 and B ≤ 11. The formula still
requires a list of unmarked rooms with B ≤ 11, which is a room enumeration
that wasn't run.

## Lemma advanced

The note advances **L1** (orthogonal, lattice marks), in its marked-selection
and base parts:

- It closes the d213 √2 staircase as a selection question. The pair is
  directly visible for every t. The cone region certifies the whole
  simultaneous deformation.
- It proves strict selection on the staircase whenever the smaller gain is at
  least 6 and y > 3(4+x)² − (4+x).
- It replaces the 121-area census with an exactly characterized irreducible
  base F, with an exact orbit-count formula and a proved upper bound. It also
  corrects the induction: selection is needed from area 22, not only above
  121.

It does not prove the lift hypothesis for general reducible rooms, which is
still the theorem-level step.

## First case still open

On the named staircase, the gap between the two proved regimes is
2x + 2 ≤ y ≤ 3(4+x)² − (4+x), outside the arithmetic classes. The note's
sample regime is y = ⌊x^{3/2}⌋. Here the direct chord is illegal, so
these pairs need an actual lift.

Arithmetic samples in the log show the strict test is not uniformly failing
there. With the smaller gain first it passes at x = 9, 16, 36, 49, 100. At
x = 25 (y = 125) it fails with the smaller gain first but passes with the
larger gain first. So the regime is a proof gap, not an observed failure.

In general rooms, the first open item is the lift hypothesis at reducible
areas 22 through 121. No reviewed result covers those rooms.
