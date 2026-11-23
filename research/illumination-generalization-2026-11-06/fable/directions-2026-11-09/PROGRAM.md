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
