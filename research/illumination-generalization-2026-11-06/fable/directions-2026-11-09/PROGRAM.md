# Illumination program (from 2026-11-22)

## Proof architecture (read first; every brief and review must name its lemma)

Goal: every strictly simple lattice room with W <= 20, orthogonal or with
45-degree walls, lights every pair of interior points.

- **L1, area bound (the open core).** A W <= 20 room with a dark pair has
  area <= 20, or <= N0 for a census-feasible N0. Equivalent forms: one-way
  descent (darkness survives shortening some length; d152 says a uniform
  tail can't work, so descent must use W <= 20), or "every way of being
  large forces lit" (the lighting tails d162, d172, d174 are pieces of this).
- **L2, finite check below the bound.** Done for area <= 20 at W <= 21
  (945 million rooms, d9/d29). Extending N0 needs Daniel's approval.
- **L3, marks.** Real and rational non-lattice marks, wherever the census
  covers lattice marks only.
- **L4, 45-degree rooms.** Same structure; the canonical45 census gap (d138, d139).

Self-enforcement (so Daniel doesn't have to remind us):
- Every Astra note starts with `Advances: L<n> - <one-line statement>`. Notes without it aren't reviewed.
- A daily goal audit runs at 08:53. A fresh Opus subagent reads this file and the last 24 hours of
  coordinator-log.md, STATE.md and the notes dir. It writes audits/YYYY-MM-DD.md: which lemma moved,
  the busy-work fraction, and one recommended change.
- If no lemma moved in 24 hours, the coordinator reports to Daniel with a proposed change.
- Every route carries a dated stopping rule.

Work that doesn't advance L1-L4 is busy work. Certifying single mid-size rooms
is busy work: L2 plus L1 covers them. Ledger bookkeeping is a gauge only.

Daniel approved four changes on 2026-11-22. This file is the source of truth
for how work is delegated; the coordinator tick follows it.

## Approved scope

- **Pattern ledger (approved).** List every orthogonal wall-turn pattern with
  W <= 20 (cyclic L/R words, L - R = 4, up to rotation and reflection). This
  is combinatorial only. It doesn't approve ray, direction, reflection-word or
  room-size searches. A by-area room census still needs separate approval.
- Each pattern gets one status: COVERED (a reviewed theorem lights every pair
  for every length assignment), PARTIAL (only some lengths), or OPEN.
- The estimate comes from the ledger, not from coordinator judgment.

## Roles

- **Astra proves.** She works through the ledger's largest OPEN groups.
- **Reviewer** (Opus subagent) checks each note's proof.
- **Attacker** (Opus subagent, after each new class theorem) builds explicit
  named rooms at the edges of the hypotheses and tests them. No searches.
- **Coordinator** (20-minute ticks) processes reviews, keeps the ledger current and briefs
  Astra only at milestones.

## Every brief ends with

"What is the smallest W <= 20 room your result doesn't cover?"

## Milestones

1. M1 (coordinator, d163): ledger built and reviewed. DONE 2026-11-22 (d165).
2. M2 (Astra): two-sided stacked halls for arbitrary lengths, or an explicit
   obstruction. Then the largest OPEN ledger group.
3. M3 (Astra): every OPEN group either COVERED or reduced to named rooms.
4. M4: the 45-degree gap (d138/d139), after the orthogonal ledger.

## Direction change (2026-11-22, Daniel approved)

Word-by-word closing can't finish (4,574 words). The ledger is a gauge only.
Main question: a word-independent resonance theorem for band chains. Find a
condition that every W <= 20 chain satisfies and R22 fails, under which some
choice of windings (plus cap reversal or the other axis) clears every gate for
every real pair. The W=10 residuals are test cases only (Ferrers U1, U2, U2b,
T1; the pyramid leftovers).
Stopping rule: if the W=10 resonant residuals don't yield to a
word-independent argument within about one day of Astra's time (by
2026-11-23), lower the estimate and report to Daniel.

## Chart-descent route: stopping rule (2026-11-23 audit)

Route: chart descent (d182, d184, d186, d187) plus a height bound H(C), with the
occupied-crossing chain (d189-d195) as its main input. It currently gives
decidability, not a census-feasible N0. By 2026-11-24 20:00, Astra runs chart
descent end to end on LLLRLLLRLR for all lengths, symbolically with no
searches, and reports a numerical N0. If no number comes out, or N0 exceeds
about 40, stop the crossing chain and report to Daniel with a proposed new route.
The 2026-11-22 resonance stopping rule fired on 2026-11-23: the estimate dropped
from 11-13% to 9-11%.

## Shrink-descent route (selected 2026-11-23)
Daniel approved this route after the chart-descent stopping rule fired. The proposal is bbbb/l1-route-shrink-descent.md. Stopping rule: by 2026-11-25 20:00 HST, deliver a symbolic proof for the primitive (n,n+1,n+2,n+3) family in LLLRLLLRLR, uniform in n, or the first precise implication that fails. Stop earlier if the transfer must keep the shortened point on the original line or needs an unbounded factor-height estimate. No searches.
Stopped 2026-11-23 09:40 HST under the early-stop clause (d198): marked transfer needs a slope-denominator bound. Limits: bbbb/l1-shrink-route-limits.md.

## Dark-structure route (2026-11-23): stopped
Stopped on the d199 recommendation: at W ≤ 20 its lemma restates the goal. Route choices no longer need Daniel's approval (Daniel, 2026-11-23). The coordinator picks a route, sets a dated stopping rule and reports the choice.

## Lighting-tail route on the three-chamber family (started 2026-11-23)
L1 in its "every way of being large forces lit" form, for d152's 20-wall family X=Y=3k+1, k ≥ 6. Primitive monodromy holds for most k, so factor certificates can't exist. Target: uniform in k, every interior lattice pair is joined by a legal path. The first open piece is the pair in bbbb/l1-primitive-family-lit.md, whose connection needs a horizontal reversal clearing both corridor apertures. Stopping rule: by 2026-11-26 20:00 HST, a symbolic construction uniform in k for that pair class, or the first failed step. Stop earlier if it needs a slope-denominator bound, a factor-height bound or any search.
