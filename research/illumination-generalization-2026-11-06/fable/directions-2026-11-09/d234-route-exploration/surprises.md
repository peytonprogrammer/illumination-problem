# Surprise review (d234)

Scope note: I also read the README sections between Blocker and Filter by
accident, including the held-back r = 3 idea. I didn't use it.

## Pre-registered prediction (written before any script ran)

Test: the residual of `bbbb/l1-two-list-chart.md` section 3 (N = 64m², axial
gaps (m+2, 1, m, 1, m+1)) at m = 2, 3, 4. Scan every x-monotone ray S → T.
Prediction: the list hits T at all three m (P = 0.75), and the witness winds
many times across the height-m middle column. Stop result: hollow at any m.

## 1. Surprises

| dNN | Predicted | Happened |
|---|---|---|
| d152 (d114, d124) | Darkness persists in long arms (uniform tail). | R22 is the all-gaps-one room. Lengthening any one arm by 1 lights every lattice pair (R22-L1-007, -012, -025). |
| d233 | A bounded list of vertical itineraries gives H(C). | That list is hollow for every even N ≥ 40. The pair is lit by velocity (1,2): x-monotone, 0 vertical-wall hits, N/2 − 1 roof-floor bounces. |
| d200 | No factor certificates, so a dark candidate. | Lit for every k. The hard pair needs 2 horizontal reversals, slope 1/(D − 1/2), and 1 vertical reversal. |
| d158 | Large slope denominators clear every door at once. | The dumbbell has no monotone witness. One far-cap bounce (slope 13/11 at L = 12) lights it. |
| d148 | An odd number of 2-adic classes fails. | 816 of 816 class rows are lit on 4 rooms. Yet cov4181 (W = 20) blocks 2 of 3 classes (d144). |
| d142, d145, d217 | Darkness is a midpoint or fold phenomenon. | R22 is a path-dependent 2-adic parity block: a corner-only site plus all 6 axial reflexes. R34 is dark with no proper fold. |
| l1-excursion-normal-form (unreviewed, hand-checked) | R22's parity window 4 < H < 6 forces darkness. | A 7-reflex room with the same window is lit by one side reflection, velocity (−5c, 1). |

## 2. Pattern

Each hard-case witness in the reviewed notes (d233, d200, d158, the 7-reflex
family) has at most 2 reversals on one axis. Its many reflections sit on the
other axis, inside one thin region. The 20 hardest census seeds at area 21
lean the same way: at most 6 hits on the less-used wall direction, 4 monotone
(`l1-seed-profile.md`; first-found, not minimal). The proofs built itinerary
lists that count every roof-floor bounce, twist orbits, or windings. Those grow
with the length.

The mechanism (guess): a long thin column is a phase accumulator. A one-pass
ray crosses it once, and its exit phase sweeps the whole column as the slope
moves by 2h/L, so length helps. This would explain d152 (guess).

Dark examples share: no free relative length (R22 has only the global
stretch), minimal gaps (d154: a corner-only fiber forces gaps ≤ 2), and every
reflex spent on one parity block (r ≥ 9 if corner-only, d217). So a dark room
has no accumulator on either axis (guess). Nothing on file shows that a long
gap in a W ≤ 20 room gives a usable accumulator for a pinned pair. That is the
seed problem.

## 3. Candidate A: one-pass two-list theorem

- **Leverage.** A ray with at most c reversals on one axis visits each column
  at most c + 1 times. With c = 0 there are no repeated visits, so d231's
  Lemma 2 (flatness), which fails only on revisited slabs, applies in full.
  The d233 obstruction hollows one axis with 6 reflexes. The target is a cost
  lemma: hollowing both one-pass lists needs r ≥ 9.
- **Closest attempt.** `l1-two-list-chart.md` (gate-box final step). It
  stopped on a residual its sequential gcd test couldn't decide, and never
  checked whether the list lights it.
- **Test (run, 0.1 CPU-s, `monotone_residual.py`, `trace_check.py`).** The
  scan is exact and complete up to the period X·lcm(2h). Slopes sit just above 1:

  | m | X | First hit | Slope | Floor/roof bounces |
  |---|---|---|---|---|
  | 2 | 385 | V = 482 | 482/385 | 199 |
  | 3 | 865 | V = 869 | 869/865 | 249 |
  | 4 | 1537 | V = 1554 | 1554/1537 | 344 |

  A second, cell-based tracer confirms each hit (0 vertical-wall hits, no
  corner), rejects V = 483 at corner (1024, 7), and reproduces d233's (1,2)
  witness at N = 40. The prediction held: the gate-box route closed on a weak
  sufficient test, not on a hole in the two-list idea.
- **Next cheap test (not run; budget spent on m = 2, 3, 4 plus the N = 40
  control).** For census rooms
  7/4319984 and 44/327644, find the hardest pair's witness with the fewest
  reversals on its better axis, heights ≤ 40. Prediction: ≤ 2 (P = 0.65).
- **Stop result.** An r ≤ 8 family whose pair needs unboundedly many
  reversals on both axes (Astra's named first open case), or a jointly hollow
  unbounded region of the d233 chart under the exact coset row test.
- **P(moves L1): 3%.** The cost lemma still needs a pinned-pair clearance
  bound (the seed problem, in a smaller box).

## 4. No second candidate

The dark-side pattern maps onto certificate completeness (d154), dark flats
(d186, d187) and shrink descent (d198). I found no leverage they lacked.
