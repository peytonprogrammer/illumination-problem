## 11. Addendum, 2026-11-18 to 2026-11-20: current status

This section records work done after sections 1 to 10 were written. Where it
conflicts with earlier sections, this section takes precedence. Paths under
`qclass-closure/` are relative to `.context/`.

### Current status

Target: 22 walls is minimal for a dark pair among strictly simple
square-lattice rooms. Working goal: every pair is lit in every such room with
W ≤ 20. Rooms with a corner-only parity class are closed for lattice pairs,
and for real marks at 15 cells. Lattice pairs of either class are settled
except in BBBB rooms: every parity class has an interior or smooth-wall
point, r ≤ 8, area ≥ 21. That set is infinite, and computation can't reach
it. Reviewed large-area results: condition (i) from n ≥ 49, irrational marks
from n ≥ 120. The core is one open lemma: some off-class candidate is reached
by a real path. G2, different-parity pairs and 45-degree rooms remain open.

### Proved and reviewed

- **Q-class closure** (COMPUTER-ASSISTED; lit side independently sampled in
  `d71-check-qclass/`). Let `P` be a strictly simple orthogonal lattice room
  with a parity class whose points are all corners. If `P` has a dark pair of
  distinct interior lattice points, in any classes, then `P` has at least 22
  walls. R22 attains the bound, so 22 is exact for this class.
  - Finite reduction (PROVED): the d68 counting identity gives area at most
    `(r + 4) + 3r <= 36` for `r <= 8`.
  - Computation: 780,565 rooms (261,564 above area 20) and 3,933,192 pairs
    (907,567 same-class, 3,025,625 different-class), all lit. A separate exact
    tracer replays every witness. An independent cell-by-cell census matches
    the enumeration in all 144 (area, alignment) counts.
  - A side run lights all 43,524 lattice pairs in 3,889 d64 covering rooms,
    which (with d64, d67) closes the proper-factor branch for both classes.
  - d71 reproduces the audit counts. d67's tracer (no shared code) lights all 141,882 pairs in 20,200 sampled rooms at
    `max(p, q) <= 20`. R22's dark pair gets no witness at `max(p, q) <= 40`.
    Enumeration completeness was checked by reading only.
  - This supersedes the BBBQ entries in sections 1 and 5, and closes gap G1
    for every room with a corner-only class. Where: `qclass-closure/README.md`,
    `audit.log`, `compare.log`, `reproduce.sh`.
- **Area-15 off-grid theorem** (COMPUTER-ASSISTED; independent check d74).
  Every 15-cell room with a corner-only class and fewer than 22 walls lights
  every pair of distinct interior points, real marks included. R22 has 15
  cells, so 22 is exact in this family. The coordinator reran Astra's audits.
  d74's separate certifier confirms all 6 hard rooms and leaves only R22's
  known pair in R22. Caveat: d74's soundness rests on d13's Lemma A' and
  Theorem C(2), still unreviewed. Where: `qclass-closure/off-grid.md`,
  `offgrid/`, `d74-continuum-check/`.
- **Long-corridor theorem** (PROVED by hand by Astra; d75: sound, one minor
  fixable gap). Two fixed orthogonal chambers have doors of equal width `w`,
  joined by an empty straight corridor. Above a length threshold, every
  interior point of one chamber lights every interior point of the other.
  Real marks are included, with one threshold for all pairs. First result for
  unbounded area. DB55: all 496 lattice pairs are lit at
  every corridor length of at least 450. Where: `qclass-closure/bbbb/README.md`.
- **D58 placement** (`placement.md`; d76: sound). All 8 position types of
  D58's double-resonance builder are lit for every door width 2^-k, k ≥ 2.
  These are ten-wall rooms with no dark pair.
- **Chain criteria and reversals** (`chain-criteria.md`, `reversal.md`; d77:
  both sound). Lattice width tests cover chains of full rectangular columns;
  turns off vertical walls fit the same test. In the DBw2 dumbbell (5×5 and 5×6
  chambers, width-2 corridor), every interior lattice pair is lit for every
  integer corridor length ℓ > 10. d77 traced all 6,851 pairs at 5 lengths.
  DB55 (1,1)–(9,1) is lit for every corridor length ℓ > 5.
- **Condition (i)** (d ≥ 2n/3 unless directly visible). For n ≥ 120 and
  r ≤ 8, every same-parity interior lattice pair is directly visible or has
  d ≥ n − 8 (`low-valency.md`, `three-sheet.md`: d78; `eight-sheet.md`: d79).
  d81 extends (i) to n ≥ 49 (d82: sound with fixable gaps), using the
  Burness–Guralnick fixed-point-ratio bound, Corollary 2.
- **Counting lemma** (`midpoint-necessity.md`; d82: sound as an algebraic
  lemma). Take a same-parity lattice pair with (i) d ≥ 2n/3 and (ii-alg) no
  regular sheet coincidence at all outside the source parity class. Then
  r ≥ 9 (from n ≥ 19 with d ≥ ⌈2n/3⌉). Equivalently, if r ≤ 8 and d ≥ 2n/3,
  there are at least 2⌈2n/3⌉ − 16 − ⌊n/2⌋ such candidates (26 at n = 49).
  Darkness doesn't imply (ii-alg); see "Open core".
- **Irrational marks** (`high-valency-geometry.md`; d80: sound). For n ≥ 120
  and r ≤ 8, any interior pair with an irrational coordinate is lit.
  Wolecki's finiteness theorem plus d16 would give this at every area. But
  d16 §6.4 records a gap in Wolecki's Lemma 2.9 for this case.
- **Cylinder tests** (d84). Two-cylinder rim test (`adjacent-cylinders.md`,
  sound with fixable gaps): suppose M has exactly two cylinders exchanged by
  the half-turn. If the rims pass the interval test, every real pair is lit. This
  closes U2 and all its stretches (areas 46 + 8k). One-cylinder test
  (`convex-cylinder.md`, sound): the same holds when reflex corners occupy at
  most 2 parity classes. All 747 saved BBBB pairs have off-class midpoints.
- **Cover gap** (`shadow-budget.md`; d86: sound, one fixable citation gap).
  Being lit on Q is weaker than reaching the coincidence on the ordered-pair
  cover U (exact cov4181 example). A uniform room-level bound B(r) on hidden
  points follows from EMM, Filip and Lelièvre–Monteil–Weiss, with no explicit
  constant. "Finite union" needs EMM's theorem on closed invariant sets, not
  the orbit-closure classification. On U, the sum of genera is at least
  d − r − 16, unbounded at r = 4 (DB55 stretches).

### Proved, not yet reviewed

- **18-wall Q-class closure** (`qclass-closure/off-grid.md`, `two18/`). Every
  18-wall room with a corner-only class, all areas, lights every pair of
  distinct interior points, real marks included. 141,885 of 141,887 rooms
  clear by cylinders. The last two (18 cells each) close by an
  endpoint-dependent shear (853 boxes). The coordinator's replay reproduces
  it. d74's plain cylinder method can't close those two rooms, so the shear
  step has no independent check.
- **Doorway lemma** (`offgrid/doorway.md`). Dead-end door pairs are lit at
  door width ≥ 1/2 the channel width (one cap) or ≥ 1/4 (both back walls).
- **Shrinking doors** (`shrinking-door.md`). Slope width on one itinerary ≤ w/D.
- **Every-direction limit** (`every-direction.md`; d87 in progress). The
  12-wall crosses [−b,b]×[−2,2] ∪ transpose (odd b ≥ 7, r = 4) fail both
  whole-room cylinder tests in every direction, yet are lit.
- **Blocking set of R22** (`corner-support.md`; d87 in progress). Each of the
  9 reflex corners is the sole obstruction of a distinct relaxed route from S
  to T, so all 9 are needed. A filled square of side ≤ 1/12 at any one corner
  lights the pair.
- **Bounded denominators** (`dark-locus.md`; d89 in progress). For each
  r ≤ 8 there is an integer D(r), with no explicit value, such that in every
  room with n ≥ 120, dark-pair coordinates have denominators dividing D(r).
  An unbounded counterexample sequence must lie in a proper rank 2–5 family
  with four periodic marks. No gain for same-parity lattice pairs.
- **Perpendicular bridges** (`perpendicular-bridges.md`). Two long
  perpendicular corridors force every pair lit; a 2-parameter family of
  20-wall rooms.
- **20-wall Q-class run.** All 913,622 rooms cleared for real marks (912,728
  whole-room, 894 tile-level; 620 shear boxes). Single implementation plus
  Astra's audit; the shear step has no independent check.
- **Rim refinements** (`persistent-gaps.md`, `rim-quotient.md`). Sharper rim
  condition; R22's period-10 mechanism can't recur at large area.
- **Supporting notes** in `qclass-closure/bbbb/` (home of the notes above): `two-class.md` (cylinder
  winding changes midpoint parity iff one of u, h, C ≢ 0 mod 4);
  `shortest.md` (one corner can block shortest routes in two classes);
  `fixed-wall.md`; `bottom-step.md`; `short-escape.md`; `denominator.md`.
- **Pair-specific notes** (Astra, 2026-11-18).
  `illumination-ninth-corner.md`: replacing one R22 cell with a strip of width
  `w` gives lit widths `w = 4k/7` on both sides of the dark width 1.
  `staircase4991-*.md`: in a 12 by 12 staircase, the pair (1,10) and (10,1) is
  lit for every real middle corner, by explicit routes of at most 8 bounces.
  This survives moving each mark up to 1/40.

### Computed evidence

- **Common-cylinder test** (d72; method PROVED exact). It covers the full
  SL2(Z) orbit of the marked origami and matches direct tracing on 18,446
  lifts. In the 9 true BBBB rooms (every `N_x = B`), 747 of 747 pairs satisfy
  CC. Its only failures are 11 visible axis-parallel pairs in d64 rooms with a
  proper factor, smallest `cov446` (`W = 18`). The marks lie on a cylinder
  boundary; a closed-cylinder variant covers them, and d64 closes these rooms. R22's dark pair fails CC in every direction, as it must.
  Where: `d72-cylinder-test/README.md`.
- **BBBB range, area 21 to 36** (d73; `d73-bbbb-21-36/README.md`, `enum.c`).
  It holds about `1e11` to `1e12` rooms with `r <= 8` (GUESSED from d9 growth
  ratios); exactly 92,657,242 at `W <= 12`. Corner-only-class rooms (780,565)
  and proper-factor rooms (2,800) are a small fraction. So the open case is
  the generic case. Pipeline slice (COMPUTED, not a sample): 31,612 rooms and
  1,001,339 pairs, all lit, every witness replayed by a second tracer.
- **Lemma stress** (d83; coordinator re-ran). The open lemma held in all 11
  saved single R22 edits with r ≤ 8. Weak: every room is lit and d = n − 1.
- **Shadow kill test** (d85; coordinator re-ran). From 2 sources each, every
  point is lit in the crosses b = 7..17 (areas 96–256) and U2 k = 0..6. R22
  control: H(0,0) = {(2,2), (2,−2)}.

### Open core

- **Open lemma.** In a room with r ≤ 8 and d ≥ 2n/3, one of the
  2⌈2n/3⌉ − 16 − ⌊n/2⌋ off-class candidates is reached by a real path.
  Unreached candidates exist (R22's source class; cov4181's class d). This is
  the current form of condition (ii) for rational pairs.
- **Numeric form.** On U, show the hidden coincidence count is at most
  αn + K, with known constants. It needs α < 5/6, or any α < 3/2 for n ≥ 120.
  Reaching one off-class coincidence also suffices for the large same-parity
  cases. d86: for a dark pair this budget restates the open lemma
  numerically; it doesn't reduce it.
- **Condition (i) for 21 ≤ n ≤ 48.**
- **Candidate CC** (d72). In a BBBB room, some lifts of two distinct
  same-class interior marks lie in one open flat cylinder of the doubled
  surface. The cylinder has a rational direction and no vertex lift inside. No argument
  links `r <= 8` to cylinder incidence. Agent estimate (GUESSED): CC true
  about 25%, provable about 3%.
- **Other gaps.** General BBBB rooms; shrinking doors (d58); turning pairs
  with no straight corridor (cov2929 type); different-parity pairs;
  non-lattice rational marks (G2); 45-degree rooms.

### Dead ends

- **Bounded search** (`search-plan.md`): no finite reduction exists, so none
  can prove the W ≤ 20 goal. Census paused.
- **Exhaustive area 21–36 run** (d73): 1,000 CPU-hours or more; not run.
  A single slice is proposed in `search-plan.md`: area 21, W = 10, 34,501
  rooms, cap 2 CPU-hours. It awaits Daniel's decision.
- **Span alone for D58's double resonance** (`shrinking-door.md`): the w/D
  bound on slope width rules it out.
- **Named-route tests** (d76, d77): they don't show some route works in every room.
- **Whole-room cylinder certificates** (`every-direction.md`): the 12-wall
  crosses defeat them in every direction.
- **Per-corner route charging** (`shared-reflex.md`, unreviewed): one reflex
  corner can block routes with midpoints in all 3 off-classes.
- **Bounded-length shadows** (d85): at L = 0.5·diam the unreached count grows
  from 20 to 60, so short paths aren't enough.
- **Fixed-stratum finiteness on U** (d86): the genus of U is unbounded.
- **Shortest-path clearance** (`midpoint-clearance.md`, unreviewed): it can
  succeed only for directly visible pairs. A lit area-501 room has ≥ 228
  candidates per class, and every one fails the test.
- **Area bound from corner alignments** (`arithmetic-rigidity.md`): none exists.

### Corrections log

- **Darkness and (ii-alg)** (d82). Earlier text implied darkness gives
  (ii-alg). It only gives that no candidate is the midpoint of a real path.
- **d81 status** (d82). Earlier text listed areas 21–119 open with d81
  unreviewed. The open range for condition (i) is now 21 ≤ n ≤ 48.
- **Area-15 independence** (d74). Earlier text said the continuum step had no
  independent implementation. d74 now confirms it, modulo d13's lemmas.
- **Two 18-cell rooms** (Astra `two18/`). Earlier text called them
  unresolved. The shear closes them, with replay but no independent check.
- **Shadow-budget claims** (d86). Earlier text marked B(r) and the genus
  bound "Claimed". d86 found them sound, with one citation fix.
- **"No proof idea has survived"** (2026-11-18). d75–d84 now cover named
  families, but no proof covers all BBBB rooms.
