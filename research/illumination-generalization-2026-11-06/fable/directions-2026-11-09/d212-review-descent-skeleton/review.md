# D212: review of the insertion-descent skeleton

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: [note-snapshot.md](note-snapshot.md).
Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
9.4 CPU-seconds, single process, under `nice -n 10`, and reports 0 FAIL.

To rerun it, use `nice -n 10 python3 -B checks.py`.

The tracer is the d210 exact integer-scaled grid tracer, extended to record
the x-direction before and after each lattice event. That makes the base chart
exact at bounces that happen on an integer level. Only named rooms were used,
all built from rectangles in `checks.py`:

| Room | Shape | Area | r | Stretched row | Components (widths) |
| --- | --- | ---: | ---: | --- | --- |
| U21 | base x[0,6); arms x[0,2), x[3,6), y[1,4) | 21 | 2 | y ∈ [1,2] | [0,2], [3,6] (2, 3) |
| H26 | bars x[0,2), x[3,6), y[0,5); crossbar y[2,3) | 26 | 4 | y ∈ [3,4] | [0,2], [3,6] (2, 3) |
| U29 | base x[0,8); arms x[0,2), x[3,8), y[1,4) | 29 | 2 | y ∈ [1,2] | [0,2], [3,8] (2, 5) |
| Staircase | nine rows, widths 9..1, scaled by t = 1..4 | 45t² | 8 | none | none |

The only direction search is a bounded first-hit seed search inside each of
the three named parents (|p|+|q| ≤ 13). It supplies actual parent seeds. No
room enumeration or room-size search was run.

In all three rooms the stretched unit row sits inside a thicker slab, cut at
a mark level. These are refined gaps in the sense of the marked version. The
transfer proof uses only a unit row with constant section, so it applies
unchanged to whole-band compression.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Band pigeonhole, thresholds 81 and 121, k ≤ 5 | CORRECT |
| 2 | Band compression gives a strictly simple lattice parent; area drop; mark counts | CORRECT |
| 3 | Parallel retained transfer for k ≥ 1, common N, lcm period, threshold | CORRECT WITH GAPS (presentation only) |
| 4 | Marked version and the minimal-counterexample implication | CORRECT WITH GAPS (scope) |
| 5 | Nine-row staircase | CORRECT |
| 6 | Axis-scaling reduction and perturbation neighborhood | CORRECT WITH GAPS |
| | **Overall** | **CORRECT WITH GAPS** |

No mathematical error was found. The note labels every open item as open.

## Claim 1: band pigeonhole

An orthogonal polygon has r+4 convex vertices, so W = 2r+4. Edges alternate,
so each orientation has r+2 ≤ 10 walls. That gives at most r+2 distinct levels
and at most r+1 ≤ 9 bands per axis. If every band is at most h₀−1 thick, both
spans are at most 9(h₀−1), so area ≤ 81(h₀−1)². The contrapositive is the
claim. The quantitative form follows from area ≤ ((r+1)·h_max)².

A section with k intervals meets 2k distinct vertical edges. So
2k ≤ r+2 and k ≤ 5.

Adding two mark coordinates gives at most r+4 levels and r+3 ≤ 11 gaps. Both
mark coordinates lie inside the box, so the span is still the sum of the gaps.
The threshold 121(h₀−1)² follows.

The log confirms the counts, k ≤ ⌊(r+2)/2⌋, and constant sections within
bands on the three rooms.

## Claim 2: compression

The map y ↦ y (below a), a + (y−a)/h (inside), y − E (above) is an increasing
piecewise-linear homeomorphism. It maps the boundary to a simple lattice
polygon with the same vertices and turns, so strict simplicity holds.
The area drops by E·Σwᵢ.

Each parent mark corresponds to exactly one child mark, because the band
section is constant. The marks strictly inside the stretched band are the
interior lattice points of E·k open rectangles, which gives E·Σ(wᵢ−1).
Two new marks in one component lie in one open rectangle, so a direct segment
lights them.

**Measured.** For E = 1, 2, 5, 9 on all three rooms the log confirms:

- the area increase E·Σwᵢ
- identical reflex, convex and pinch counts
- the retained-mark bijection
- new marks = E·Σ(wᵢ−1), all strictly inside the band
- removing the E inserted rows returns the parent

## Claim 3: parallel retained transfer

**Algebra.** From s(D+mE) = Ds₀ + 2QmN you get Es − 2QN = −(D/m)δ. So the
selected-step increment is (1+E)s − s₀ − 2QN = δ + Es − 2QN = (1 − D/m)δ.
Summing m selected and D−m ordinary increments gives Dδ − Dδ = 0, so e(D) = 0.
The log checks both identities exactly on 13,860 grid cases.

**Period on each visited circle.** Within component i the band is the open
rectangle [cᵢ, cᵢ+wᵢ] × (a, a+h). Its sides are full height and it contains no
corner. The unfolding of that strip reflects in the lines cᵢ + jwᵢ. Two
reflections compose to translation by 2wᵢ, so translation by any multiple of
2wᵢ is a symmetry of the strip's unfolded chart. The developed chart at the
strip is the local chart composed with an affine map of slope ±1, so the
offset cᵢ and the orientation don't matter. Since wᵢ | Q, 2QN = 2wᵢ·(Q/wᵢ)·N
is a whole period on every visited circle.

**Gate induction with alternation.** The induction is per unit step and
needs no memory of which component was visited before. Suppose the child
agrees with the base chart through old level t−1 at developed coordinate
X₀(t−1) + e(t−1). Two cases follow.

- **Ordinary step.** The vertical walls crossed strictly inside the row are
  the integers strictly between the endpoints. Those are the same for base and
  child when both endpoints satisfy the strict gate.
- **Selected step.** The exit circle state is the entry state plus (1+E)s,
  reduced modulo 2wᵢ. Subtracting 2QN leaves it unchanged, whatever i is.

Either way the next coordinate is X₀(t) + e(t). The gate at level t then fixes
the next row's component, even when it differs from the previous one.

**Measured.** The search found 6 seeds per room that traverse both components.
Each alternates components several times, in both vertical directions. Some
examples:

- U21: (4,3)→(5,2), s₀ = 7/3, D = 33, m = 8. The components visited are
  R, L, L, R, R, L, L, R, with traversal directions down, up, alternating.
  Q = 6, M = 4, threshold E > 543/8.
- H26: (4,2)→(4,4), s₀ = 5/6, D = 24, m = 7, Q = 6, threshold E > 1020/7.
- U29: (1,2)→(7,2), s₀ = 10/3, D = 54, m = 14, widths 2 and 5, Q = 10,
  threshold E > 753/7.

Each seed was re-aimed at every E from 1 to min(260, threshold + 25). The
review used the nearest N and both neighbors, then traced exactly.

| Room | Gate-passing re-aims | Illegal among them | Old-level states checked | Mismatches | Cases with E > threshold, nearest N | Failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| U21 | 545 | 0 | 12,870 | 0 | 150 | 0 |
| H26 | 973 | 0 | 21,319 | 0 | 150 | 0 |
| U29 | 561 | 0 | 28,311 | 0 | 150 | 0 |

At each old level t the state check compares the child's physical crossing
(x, direction) with the base chart evaluated at X₀(t) + e(t). Where the base
bounces exactly on the level, the check also accepts the mirrored pre-bounce
chart. The check is sensitive: it rejects the uncorrected prediction tδ in
every case with δ ≠ 0 (513, 931 and 454 cases).

**Below the threshold.** At the nearest N, 328 of 369 (U21), 913 of 1,081
(H26) and 547 of 617 (U29) re-aims are still legal. That's consistent with
the claim that the threshold is sufficient, not necessary. The signed gate
test fails in many legal cases: 577, 1,335 and 1,031. That's consistent with
the test being sufficient only.

**Why the lcm is needed.** Replace 2QN with 2w₁N, where 2w₁N isn't a
multiple of 2w₂. Of 5,801 such traces, 837 reach the target. Among those that
pass the same signed gate, only 8 of 26 are legal. The single-width formula
from d210 doesn't transfer to two widths, and the lcm is the needed change.

**Gaps.**

1. Low. The ordinary-step part of the induction ("the next gate and
   component persist") relies on d210's argument without restating it: the
   integers strictly between consecutive endpoints are the same for base and
   child. Name it or cite d210 Claim 2.
2. Low. The note cites d210 for D ≤ (4·area − 2r)v. The d210 review states
   D ≤ 4·area·v. Pick's theorem gives exactly 4A − 4r − 4 nonsingular lattice
   states (4 per interior point, 2 per wall-interior point), so the stated
   bound holds with slack. The log confirms 72, 84 and 104 states on the three
   rooms. Every chosen first-hit seed satisfies D ≤ (4A − 2r)v.
3. Low. Q ≤ B⁵ is valid but loose. Σwᵢ ≤ B gives Q ≤ ∏wᵢ ≤ (B/k)ᵏ.

## Claim 4: marked version and the implication

**Preservation.** Mark coordinates are cut levels, so neither mark is strictly
inside a refined gap. A mark on the bottom interface keeps its four cells,
because the gap's section is constant. After compression both interfaces are
one unit apart, and both marks stay interior lattice points. The parent pair
is a retained pair, so Claim 3 lifts any passing parent seed.

**Minimal-counterexample logic.** Assume three things:

- (i) Every strictly simple orthogonal lattice room with r ≤ 8 and area ≤ 121
  is lattice-lit.
- (ii) The parallel transfer from Claim 3 holds.
- (iii) Marked selection: if every smaller room in the class is lit, some
  refined gap of thickness ≥ 2 has a passing parent seed for the given pair
  at E = h−1.

Suppose a dark lattice pair exists. Areas are positive integers, so take a
room of least area A among rooms with a dark pair. By (i), A > 121, so some
refined gap has thickness ≥ 2. Its compressed parent has the same r, stays in
the class, and has smaller area, so it is fully lit. By (iii) a passing seed
exists, and by (ii) it lights the pair. That contradicts darkness. The
implication is valid. The room-level version (census through 81, selection
for one band, collars) has the same structure and is also valid.

**Gaps.**

1. Medium, scope. L1 in PROGRAM covers W ≤ 20 rooms with 45-degree walls
   too. This skeleton is orthogonal only, so it advances the orthogonal part
   of L1. L4 remains separate.
2. Medium, honesty of the base. The conditional N₀ is 121 (or 81). The
   reviewed census reaches area 21, and PROGRAM says extending N₀ needs
   Daniel's approval. The note states this as a proof dependency. A summary
   should not describe the skeleton as giving L1 with any census-feasible N₀.
   The staircase in Claim 5 shows that N₀ < 45 is impossible for this move
   alone.

## Claim 5: staircase

For t = 1..4 the log confirms each of these:

- r = 8 and 12 convex vertices
- area 45t²
- every wall gap equals t on both axes
- compressing any one band leaves at least 36t² + 9t ≥ 36t²

At t = 1 every gap is 1 on both axes, so no band compression applies. Marked
refinement only splits gaps, so it doesn't help.

The coarse threshold comparison fails as stated: Q·(4·area(parent) − 2r)·F²
≥ 144t² − 16 > t − 1. The note correctly calls this a failure of the
estimate, not a dark pair.

## Claim 6: axis scaling and perturbation

**Scaling.** If all marked gaps on one axis share a factor g > 1, every
coordinate on that axis is congruent to the minimum modulo g. Translate, then
divide. Independent axis scalings map straight segments to straight segments,
commute with reflections in axis-parallel walls, and map corners to corners.
The log lifts all 6 H26 seeds through scalings (2,1), (1,3), (2,3) and (5,2).
All 24 lifts are legal and end exactly at the scaled target. The remark about
arbitrary marks is right.

**Perturbation.** A legal seed between interior marks has transverse hits in
relative edge interiors. Its legs touch the boundary only at their endpoints.
A leg can't run along an edge without passing a vertex. The unfolded target
is an affine function of the levels, and every strict condition is open, so
the lemma holds.

The log tests it on the U21 marked chart for the pair (1,3)→(4,3). The
template seed has direction (−3,2), 5 steps, and 8 wall hits. Perturbed rooms
use gaps tu + c with |c| ≤ 1 on 5 x-gaps and 3 y-gap patterns, 729 rooms per
t:

| t | Relative error ≤ | Legal | Same itinerary |
| ---: | ---: | ---: | ---: |
| 6 | 1/6 | 702 | 701 |
| 7 | 1/7 | 720 | 720 |
| 9 | 1/9 | 729 | 729 |
| 12 | 1/12 | 729 | 729 |

Failures at t = 6, 7 show that the radius is finite and depends on the
template.

**Gaps.**

1. Low. Divide after translating to the minimum. As written, "divide by that
   divisor" leaves this step implicit.
2. Low. The effective-radius procedure terminates because natural interval
   extensions of rational functions converge as the box shrinks, with nonzero
   denominators at the template. That convergence, not compactness of the
   segments, is the operative fact. State it.
3. The note states the open quantifier correctly: covering all marked gap
   ratios by certified neighborhoods doesn't follow from openness.

## First case still open

The marked selection lemma at h₀ = 2 is the first open step. Here is a
concrete form: take a strictly simple orthogonal room with area > 121, a dark
lattice pair, and every refined gap of thickness ≥ 2. For each gap, every
parent seed must fail the signed gate test at E = h−1. The staircase family at
t ≥ 2 is the model case. Every refined gap has thickness t. After
compressing one gap, the other eight comparable gaps still drive D, M and v,
and nothing bounds QvM by t − 1.

In the room-level version, item 2 has the same open quantifier. Item 3 also
needs collars for mixed pairs and for new/new pairs across components. The
review found no proof of either in the note or in d209–d211.

## Lemma advanced

The skeleton advances the orthogonal part of **L1**. Parallel retained
transfer for k ≥ 1 (Claim 3) is now proved and tested on bands with two
widths. Together with Claim 4 it reduces L1 (orthogonal, r ≤ 8) to two
inputs. The first is marked selection (or the weaker template-neighborhood
form). The second is a lattice census through area 121. Neither input exists
yet, so the note gives no unconditional area bound, and it doesn't claim one.
