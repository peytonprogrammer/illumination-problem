# D234: route exploration round (2026-11-25)

Advances: L1 (route choice only; no lemma claimed).
Trigger: Daniel asked to resume research after the gate-box route closed. Run under the `research-conduct` skill.

## Blocker (same for every closed route)

Produce one legal chord for a specified pinned lattice pair in a growing chart.
Equivalent forms: an explicit height bound H(C) for rigid dark flats (d187), or
"dark implies a known certificate" on torus covers (d154).

## Payoff sentence

If this round succeeds, it changes the decision between "open a theory route"
and "report that no theory route has a payoff", by producing at most one route
with named new leverage that survives a cheap test.

## Prior work

Closest earlier attempt: d230 (coordinator's solo fresh angles, 2026-11-24),
which gave the gate-box route, closed in one day. Also l1-route-assessment.md
(Astra, P = 5%) and the 2026-11-18 strategy step-back. Difference here:
independent ideators who don't see the coordinator's candidates, a fixed
candidate format with a pre-registered cheap test, and a surprise review of
the logs (surprises were logged only as bad news before).

## Coordinator's own ideas, checked against the notes before the round

All five are known ground, so none is offered as a candidate:
- diagonal-scaling invariance and rigid dark points: d137, d145;
- affine-orbit action on lattice pairs: d176 to d180, l1-large-monodromy.md;
- leaf-sharing criterion per primitive direction: d149, d151;
- degeneration of positive-dimensional flats: l1-flat-collapse.md, d186, d187;
- literature for torus covers: HST, AW, Wolecki, LMW are all read at source.

One candidate held back from the ideators to avoid anchoring: W = 10 (r = 3)
is still open for all areas (0 COVERED, 4 PARTIAL, 4 OPEN). A stronger
hypothesis (r = 3 only) with the tools reviewed since 2026-11-23 (d200, d212
to d215, d228, d229, d231) is a bounded test of whether any all-area method
exists. Astra assesses it after she gives her own candidate.

## Predictions (written before launch)

- P(at least one candidate passes the filter and gets a funded test) = 35%.
- P(that candidate then moves L1) = 5%.
- Most likely outcome: every candidate reaches the two-gate aiming blocker
  with new vocabulary only.

## Filter for a candidate

1. Names leverage that no closed route had: a stronger hypothesis, a
   counterexample, or a cheap distinguishing test.
2. Cites the closest earlier dNN and says what differs.
3. Has a test costing at most 10 CPU-minutes on named rooms, or a hand check,
   with a prediction written first.
4. States the result that stops it.

## Stop result for the round

One round only. If no candidate passes, report to Daniel that no theory route
has a payoff, with a recommendation among the census options and stopping.
No searches and no census in this round.

## Outcome (2026-11-25 08:00 HST)

| Ideator | Candidates | Their estimate |
| --- | --- | --- |
| Astra (`bbbb/l1-route-candidates.md`) | none; r = 3 has no all-area proof | 5% for the current methods |
| Surprise review (`surprises.md`) | one-pass two-list theorem | 3% |
| Outsider (`outsider.md`) | immersed-disc control (a census, needs approval) | 1%; 2% for any theory route |

Finding that changes a decision: the residual on which the gate-box route
closed is lit by the x-monotone list at m = 2, 3, 4, 5, 6 (exact scan plus an
independent tracer; coordinator re-ran both and added m = 5, 6). The route's
early-stop clause fired on a gap in a sufficient test, not on a hollow region.

Decision: reopen the last step of the gate-box route (two-list union on the
six-reflex two-gate chart) under its original deadline, 2026-11-26 20:00 HST.
New leverage, per the same-blocker rule:
1. an exact list scan costs 0.1 CPU-seconds per parameter point, so every
   subregion gets a prediction and a test before a proof attempt;
2. a one-pass list revisits no slab, so every dual relation is arithmetic and
   d231's flatness criterion applies in full (the surprise review's point).

Stop result: a named unbounded family in the vertical lock region V where the
exact x-monotone list is also hollow (verified by scan), or no proof of an
explicit exceptional set by the deadline. Either one closes the route for good.

Not chosen:
- r = 3 all-area test: Astra and pyramid-sweep-obstruction.md show it has the
  same two-list blocker, so it adds no leverage beyond the reopened step.
- Immersed-disc control: informative (it tests whether planarity carries the
  goal), but it is a census. Recommended to Daniel; not launched.

Predictions scored: "at least one candidate gets a funded test" (35%) came
true. "Every candidate reaches the two-gate blocker with new vocabulary only"
was wrong for the surprise review, which found a missed test, and right for
the rest. Coordinator's slope prediction for m = 5, 6 (within 5% above 1) held
at m = 5 (2437/2401) and failed at m = 6 (4328/3457).

Route-close record for the first closure: avoidable expense = closing without
the 0.1-second scan; surprise worth pursuing = hard-case witnesses reverse at
most twice on one axis.
