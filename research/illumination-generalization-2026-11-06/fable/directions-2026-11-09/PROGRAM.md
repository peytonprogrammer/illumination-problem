# Illumination program (from 2026-11-22)

## Proof architecture (read first; every brief and review must name its lemma)

Goal: every strictly simple lattice room with W <= 20, orthogonal or with
45-degree walls, lights every pair of interior points.

- **L1, area bound (the open core).** A W <= 20 room with a dark pair has
  area <= 20, or <= N0 for a census-feasible N0. Equivalent forms: one-way
  descent (darkness survives shortening some length; d152 says a uniform
  tail can't work, so descent must use W <= 20), or "every way of being
  large forces lit" (the lighting tails d162, d172, d174 are pieces of this).
- **L2, finite check below the bound.** CORRECTION 2026-11-23 (census-parity-audit): different-parity pairs are verified only through area 16; areas 17–20 cover same-parity pairs only. Gap filled and area 21 done in d205 (reviewed d206, correct with gaps); L2 now complete through exact area 21. Originally recorded as done for area <= 20 at W <= 21
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

## Long-neck route (2026-11-23): stopped
Stopped at its early-stop clause: no 8-versus-9 mechanism. A 6-reflex long-neck room has no pocket. Route tally for 2026-11-23: chart descent, shrink descent, shear counting (not run), dark structure and long neck all lack an 8-versus-9 step. Lighting tails (d200–d202) are per-family.

## Per-pattern decidability route (started 2026-11-23)
Replaces the search for an 8-versus-9 mechanism. Target theorem: for each wall-turn word with W ≤ 20, if lattice marks are joined at all, they're joined by a path with at most a·|ℓ| + b reflections (a, b depend on the word). Then each word's "all pairs lit for all lengths" is a Presburger sentence, and computation decides the 8-versus-9 question. Decision runs and any census extension need Daniel's approval. First test: one-neck word LLLLRRLLLLRR. Stopping rule: 2026-11-26 20:00 HST, or a family whose shortest paths need superlinearly many reflections.
Correction (d204, 2026-11-23): a linear reflection bound does NOT yield a Presburger sentence, because gate conditions are quadratic in the lengths (u > m(m+1) on the one-neck word). The surviving decidability form is an eventual-periodicity theorem: per word, the set of fully lit length vectors repeats periodically for large lengths. That's an open theorem. Per-word parametric certificates remain valid proofs but aren't a decision procedure.

## L2 extension: area 21 (approved by Daniel 2026-11-23)
Approved: the census at exact area 21, W ≤ 20, all interior lattice pairs across parities, plus a log audit of different-parity coverage through area 20. Plan: bbbb/census-extension-plan.md. Run dir: d205-census-a21. Limits: nice 10, ≤ 8 processes. Validate against the area-20 counts and the W=22 dark control first. A confirmed dark pair stops the run. Areas above 21 still need approval.

## Seed-profile route (selected 2026-11-23 14:12)
Theory routes today (area-bound counting d207/d208, corner charging, direction density, common cylinders) all reduce to the seed: one straight legal chord for each pair. CC in a variable direction is equivalent to lighting (l1-common-cylinder.md). New route: rerun the approved area-21 slice recording each pair's first-witness direction height, reflection count and r; extract the hardest pairs; state a seed-type conjecture; attempt a proof for its family. Stopping rule: if by 2026-11-25 20:00 no seed type covers all area-21 pairs with a uniform description, stop and report.

## Insertion-descent route (2026-11-23 16:25)
Reviewed pieces: width-w replay + flat-cap collar (d209), all-residue re-aim for retained pairs (d210). A descent proof of L1 needs (a) a collar lemma for arbitrary terminal ends and for bridges, and (b) a polynomial bound on the seed denominator v per pair for r ≤ 8. Then every room with a long single-interval slice reduces to a shorter lit room plus a threshold that the census must cover. Stopping rule: if neither (a) nor (b) has a reviewed general case by 2026-11-26 20:00, stop and report.

## Affine-transfer route: stopping rule (2026-11-23 21:30 audit)

Audit finding: d212–d224 gave 13 correct reformulations of L1 case (iii) at area 22 and no closures. Area 22 alone doesn't prove L1 (d212 needs the lift step at areas 22–121). Daniel approved the following (2026-11-23):
- The symmetric-only area-22 check is dropped (it would close one branch at one area).
- The single live theory bet is the affine-transfer lemma (bbbb/l1-affine-transfer.md): corner-fixing band multi-twists carry a short direct chord onto any target, uniform in area. Stopping rule: by 2026-11-25 20:00 HST, a reviewed general lemma, or at most two notes, whichever comes first. Then stop the L1 theory chain and report (pause vs. costed computation).
- Opus reviews only for notes that claim a closure or a general (area-uniform) lemma. Reductions and reformulations are logged without review.
- Estimate re-based to 5–8% until a case closes.

## Pinned-pair route (2026-11-23 22:00; replaces affine transfer)

Affine transfer stopped after one note: l1-affine-transfer.md proves that the corner-fixing band twists preserve displacement gcd and parity, and fix pinned sites. Daniel asked for the key blocker to a general proof.

Key blocker: the descent (d212–d215) is the only mechanism that creates straight chords in rooms above the census. It lifts a parent witness when a gap grows, but it needs growth commensurate with the witness direction, or a slack window of directions (d214 claims 1 and 6). Ratio compactness (d215) supplies slack everywhere except at a specified pair **pinned to supporting-line intersections**. The affine twists also fix exactly these sites. Pinned pairs are therefore the single residual of the descent.

Target lemma (L1): for a nondegenerate chart with r ≤ 8 and a pinned pair, darkness forces some refined gap ≤ B(r) for an explicit B. One-gap shrink (d214 F) then lands it in a lower chart or the census. Proposed mechanism: two-scale blow-up at each pin. The local geometry at a pin is one of finitely many crossing types, so the micro problem is finite and independent of area. Test bed: d215's x=1 staircase open strip (near b=c; and 2a+2b ≤ c with α ≥ 1/4).

Stopping rule: by 2026-11-25 20:00 HST, a reviewed general pinned-pair lemma or a sharp obstruction (a pinned dark family with every gap unbounded). Otherwise stop the L1 theory chain and report. No searches: at most 5 hand-picked parameter points per family, as exact traces.

Correction (2026-11-23 21:35, l1-pinned-pairs.md): the target "darkness forces a gap ≤ B(r)" was ill-posed. Dilation preserves darkness, so an absolute bound is equivalent to having no pinned dark pair. Interior pins are locally free, so the blocker is global aim (an itinerary whose developed target image clears every gate), not a local crossing type. End bounces realize only the sign patterns 0, +, −, (+,−). Current step: interior-bounce sign patterns (l1-interior-bounce.md). The deadline is unchanged.

## PAUSED (2026-11-23 23:10, Daniel)

The L1 theory chain is stopped. Pinned-pair route outcome: reviewed tools d228 (sign-cone theorem) and d229 (bounded templates, one-gap tails); closures d225/d226 and the parabola family. The residual is the seed problem: produce one legal chord for a specified pinned pair in a growing chart (l1-route-assessment.md, Astra's P = 5%). Coordinator and daily-audit crons are cancelled; Astra is on standby. To resume, either:
- start a new theory route with a dated stopping rule; or
- run the area-22 census as a falsification test (≈1.17B rooms, 3.1 CPU-h; needs Daniel's approval). A dark pair would refute the goal; all-lit closes only area 22.
Estimate at pause: 5–8%.

## Gate-box route (2026-11-24, Daniel approved; pause lifted)

Single live route. Source: d230-fresh-angles/README.md.
- Lemma 1: for a vertical itinerary, legal chords are the points of a lattice coset in the box of gate intervals. The dual lattice is the set of integer relations among the slab moduli h/2w.
- Lemma 2: no chord of that type forces a relation that is short against the gate widths (flatness theorem).
- Target for L1: for r ≤ 8, a finite chart-only family of itineraries can't all be resonant unless the primitive room is small. This supplies the height bound H(C) that d187 isolated.

Roles: Opus reviews Lemmas 1–2 (d231). Astra runs the exact tests (R22, six-reflex locked gate) and attacks the persistence step.
Stopping rule: stop if the R22 test doesn't produce short relations, or if the persistence step has no proof for the two-gate family by 2026-11-26 20:00 HST. Then report.
No searches. The resonance-guided census (d230, Angle 2) needs Daniel's approval and isn't approved.
Estimate stays 5–8% until d231 returns.

Update 2026-11-24 22:45 HST (d231): Lemma 1 holds. Lemma 2 is necessary for darkness only and is silent on itineraries that revisit a slab, so it can't supply the area bound. Astra's notes refute itinerary decoupling. Live step, same stopping rule: exclude positive-dimensional dark flats with the exact projection criterion on a flat (bbbb/l1-dark-flat-exactness.md). Estimate 4–7%.

Update 2026-11-24 23:15 HST: d232 reviewed (exact test on a flat, conditional tie lemma, coefficient bound; 0 wrong, no closure). Live step: collapse lemma (bbbb/l1-flat-collapse.md), which takes the seed from a collapsed boundary room of the flat. Known limit: excluding dark flats of dimension ≥ 2 gives finiteness, not an explicit N₀. Same stopping rule. Estimate 3–6%.

Update 2026-11-24 23:20 HST: dark-flat line stopped (overlaps d186/d187; no explicit N₀). Live step is the stopping-rule test itself: an explicit H(C) for the six-reflex two-gate chart with all gaps free, by exact coset tests on a fixed itinerary family (bbbb/l1-two-gate-chart.md), or a named unbounded subfamily where the family is hollow. Estimate 3–6%.
