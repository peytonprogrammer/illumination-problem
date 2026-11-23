## 11. Addendum, 2026-11-18: Q-class closure and later checks

This section records work done after sections 1 to 10 were written. Where it
conflicts with earlier sections, this section takes precedence.

### Q-class closure theorem (Astra)

**Theorem (COMPUTER-ASSISTED; lit side independently sampled).** Let `P` be a
strictly simple orthogonal lattice room. Suppose some parity class has no
interior point and no smooth-wall point in `P`, so all its points are corners.
If `P` has a dark pair of distinct interior lattice points, then `P` has at
least 22 walls. The marks may be in different classes. R22 attains the bound,
so 22 is exact for this class of rooms.

- Finite reduction (PROVED): the d68 counting identity gives area at most
  `(r + 4) + 3r <= 36` for `r <= 8`.
- Computation: 780,565 rooms (261,564 above area 20) and 3,933,192 pairs
  (907,567 same-class, 3,025,625 different-class), all lit. A separate exact
  tracer replays every witness. An independent cell-by-cell census matches the
  room enumeration in all 144 (area, alignment) counts.
- A side run lights all 43,524 lattice pairs in 3,889 d64 covering rooms.
  With d64 and d67, this closes the proper-factor branch for different-class
  pairs too.
- Coordinator check (`d71-check-qclass/`): the audit reproduces the counts.
  d67's tracer, which shares no code with Astra's, lights all 141,882 pairs
  in 20,200 sampled rooms at `max(p, q) <= 20`. R22's dark pair gets no
  witness at `max(p, q) <= 40`. Enumeration completeness was checked by
  reading only.
- Where: `.context/qclass-closure/README.md`, `audit.log`, `compare.log`,
  `reproduce.sh`.

This result supersedes the BBBQ entries in sections 1 and 5. It also closes
gap G1 for every room with a corner-only class.

### Common-cylinder criterion (d72)

**Candidate CC (unproved).** In a BBBB room, some lifts of two distinct
same-class interior marks lie in one open flat cylinder of the doubled
surface, in a rational direction, with no vertex lift inside the cylinder.

- Method (PROVED exact): the test covers the full SL2(Z) orbit of the marked
  origami. It matches direct tracing on 18,446 lifts.
- True BBBB rooms (every `N_x = B`): 747 of 747 pairs in 9 rooms satisfy CC.
- Failures: 11 visible axis-parallel pairs in d64 rooms with a proper factor,
  smallest `cov446` (`W = 18`). The marks lie on a cylinder boundary. A
  closed-cylinder variant covers them. d64 already closes these rooms.
- R22's dark pair fails CC in every direction, as it must.
- No argument links `r <= 8` to cylinder incidence. Agent estimate
  (GUESSED): CC true about 25%, provable about 3%.
- Where: `d72-cylinder-test/README.md`.

### Size of the remaining finite range (d73)

- BBBB rooms with `r <= 8` and area 21 to 36 number about `1e11` to `1e12`
  (GUESSED from d9 growth ratios). Exact: 92,657,242 such rooms at `W <= 12`.
  An exhaustive check would take about 1,000 CPU-hours or more. It wasn't run.
- Corner-only-class rooms (780,565) and proper-factor rooms (2,800) are a
  small fraction. Almost every room in this range is true BBBB, so the open
  case is the generic case.
- Pipeline slice (COMPUTED, not a sample): 31,612 rooms and 1,001,339 pairs,
  all lit, every witness replayed by a second tracer.
- Where: `d73-bbbb-21-36/README.md`, `enum.c`.

### Updated open statement

Same-class and different-class lattice pairs are settled except in BBBB
rooms: rooms where every parity class has an interior or smooth-wall point,
with `r <= 8` and area at least 21. That set is infinite. Computation can't
reach it, and no proof idea has survived. Non-lattice rational marks (G2) and
45-degree rooms also remain open.

### Other Astra notes (2026-11-18, pair-specific)

- `.context/illumination-ninth-corner.md`: replacing one R22 cell with a strip
  of width `w` gives lit widths `w = 4k/7` on both sides of the dark width 1.
- `.context/staircase4991-*.md`: in a 12 by 12 staircase, the pair (1,10) and
  (10,1) is lit for every real middle corner, with explicit routes of at most
  8 bounces. This survives moving each mark up to 1/40.

### Off-grid marks (Astra, 2026-11-19)

- Area-15 theorem (COMPUTER-ASSISTED, one implementation of the continuum
  step): every room of exactly 15 cells with a corner-only parity class and
  fewer than 22 walls lights every pair of distinct interior points, real
  marks included. R22 has 15 cells, so 22 is exact in this family.
- 18-wall rooms with a corner-only class, all areas: 141,885 of 141,887
  cleared for real marks; 2 rooms of 18 cells remain unresolved.
- Doorway lemma: dead-end door pairs are lit when the door width is at least
  half the channel width (one cap) or a quarter (both back walls).
- Where: `.context/qclass-closure/off-grid.md`, `offgrid/`, `offgrid/doorway.md`.
  Audits rerun by the coordinator; the continuum computation itself has no
  independent implementation yet.
- Independent check (d74, 2026-11-19): a separate certifier confirms the
  area-15 theorem on all 6 hard rooms and leaves only R22's known pair in
  R22. Soundness rests on d13's Lemma A' and Theorem C(2), still unreviewed.
- 18-wall closure (Astra, `qclass-closure/two18/`): the last two rooms are
  closed by an endpoint-dependent shear (853 boxes). The coordinator's
  replay reproduces it, but d74's plain cylinder method can't close them, so
  no independent check of the shear step exists yet.

### Long-corridor theorem (Astra, 2026-11-19; reviewed in d75)

- Statement: two fixed orthogonal chambers with doors of equal width `w`,
  joined by an empty straight corridor. Above a length threshold, every
  interior point of one chamber lights every interior point of the other,
  real marks included, with one threshold for all pairs.
- Status: PROVED by hand (Astra), reviewed sound with one minor fixable gap
  (d75). First result that handles unbounded area. DB55: all 496 lattice
  pairs lit at every corridor length of at least 450.
- Open: shrinking doors (d58), turning pairs with no straight corridor
  (cov2929 type), general BBBB rooms.
- Where: `.context/qclass-closure/bbbb/README.md`, `d75-review-corridor/`.

### Corridor follow-ups (Astra, 2026-11-19; reviewed in d76, d77)

- Shrinking doors (`shrinking-door.md`, unreviewed): usable slope width on one
  itinerary is at most w/D; span alone can't close D58's double resonance.
- D58 placement (`placement.md`, reviewed sound in d76): all 8 position types
  of D58's double-resonance builder are lit for every door width 2^-k, k ≥ 2.
  Ten-wall rooms, no dark pair.
- Chain criteria (`chain-criteria.md`, reviewed sound in d77): lattice width
  tests for chains of full rectangular columns. DBw2 dumbbell (5×5 and 5×6
  chambers, width-2 corridor): every interior lattice pair lit for every
  integer corridor length ℓ > 10 (d77 traced all 6,851 pairs at 5 lengths).
- Reversals (`reversal.md`, reviewed sound in d77): turns off vertical walls
  fit the same test. DB55 (1,1)–(9,1) is lit for every corridor length ℓ > 5.
- Limit: these test a named route. They don't show some route works in every
  room.

### Route to the 22-wall bound for large rooms (Astra, 2026-11-20; d78–d80)

- Counting lemma (`midpoint-necessity.md`, reviewed sound in d82 as an
  algebraic lemma): for a same-parity lattice pair with (i) marked valency
  d ≥ 2n/3 and (ii-alg) no regular sheet coincidence at all outside the
  source parity class, r ≥ 9 (from n ≥ 19 with d ≥ ⌈2n/3⌉).
  Equivalently, if r ≤ 8 and d ≥ 2n/3, there are at least
  2⌈2n/3⌉ − 16 − ⌊n/2⌋ such candidates (26 at n = 49).
- Correction (d82): darkness does NOT imply (ii-alg). It only implies that no
  candidate is the midpoint of a real path. Unreached candidates exist (R22's
  source class; cov4181's class d). The route needs an OPEN lemma: in a room
  with r ≤ 8, one of those candidates is reached by a real path.
- Condition (i) from n ≥ 49: d81, reviewed sound with fixable gaps in d82
  (Burness–Guralnick fixed-point-ratio bound, Corollary 2).
- Condition (i), reviewed sound: low-valency.md (d78), three-sheet.md (d78),
  eight-sheet.md (d79). For n ≥ 120 and r ≤ 8, every same-parity interior
  lattice pair is directly visible or has d ≥ n − 8.
- Irrational marks, reviewed sound (d80): `high-valency-geometry.md`. For
  n ≥ 120 and r ≤ 8, any interior pair with an irrational coordinate is lit.
  Wolecki's finiteness theorem plus d16 would give this at every area, but
  d16 §6.4 records a gap in Wolecki's Lemma 2.9 for this case.
- Unreviewed supporting notes: `two-class.md` (cylinder winding changes
  midpoint parity iff one of u, h, C ≢ 0 mod 4), `shortest.md` (one corner
  can block shortest routes in two classes), `fixed-wall.md`, `bottom-step.md`,
  `short-escape.md`, `arithmetic-rigidity.md` (no area bound from corner
  alignments).
- Search plan (`search-plan.md`): no finite reduction exists, so no bounded
  search can prove the W ≤ 20 goal. Census paused.
- Open: condition (ii) for rational pairs at n ≥ 120 (Astra, in progress);
  areas 21–119 (d81, unreviewed: condition (i) holds from n ≥ 49); different-parity pairs; 45-degree rooms.
- Where: `.context/qclass-closure/bbbb/`, `d76`–`d80` review directories.

### Cylinder certificates, shadows and the cover gap (2026-11-20; d83–d86)

- Status note: d81 is now reviewed (d82, sound with fixable gaps), so
  condition (i) holds from n ≥ 49. It stays open for 21 ≤ n ≤ 48.
- Two-cylinder rim test (`adjacent-cylinders.md`, reviewed in d84: sound
  with fixable gaps). If M has exactly two cylinders exchanged by the
  half-turn and the rims pass the interval test, every real pair is lit.
  This closes U2 and all its stretches (areas 46 + 8k). 747/747 saved
  BBBB pairs have off-class midpoints.
- One-cylinder test (`convex-cylinder.md`, reviewed in d84: sound). The
  same conclusion holds when reflex corners occupy at most 2 parity classes.
- Limit (`every-direction.md`, unreviewed). The 12-wall crosses
  [−b,b]×[−2,2] ∪ transpose (odd b ≥ 7, r = 4) fail both whole-room tests
  in every direction, yet are lit. Whole-room cylinder certificates can't
  cover all rooms. `persistent-gaps.md` and `rim-quotient.md` (unreviewed)
  sharpen the rim condition and show that R22's period-10 mechanism
  can't recur at large area.
- Route charging fails (`shared-reflex.md`, unreviewed). One reflex corner
  can block routes with midpoints in all 3 off-classes.
- Blocking set of R22 (`corner-support.md`, unreviewed). Each of the 9
  reflex corners is the sole obstruction of a distinct relaxed route from
  S to T, so all 9 are needed. A filled square of side ≤ 1/12 at any one
  corner lights the pair.
- Lemma stress (d83, unreviewed). The open lemma held in all 11 saved
  single edits of R22 with r ≤ 8. Weak: every room is lit and d = n − 1.
- Shadow kill test (d85, re-run by coordinator). From 2 sources each,
  every point is lit in the crosses b = 7..17 (areas 96–256) and U2
  k = 0..6. R22 control: H(0,0) = {(2,2), (2,−2)}. Short paths are not
  enough: at L = 0.5·diam the unreached count grows from 20 to 60.
- Cover gap (`shadow-budget.md`, reviewed in d86: sound with one fixable
  citation gap; "finite union" needs EMM's theorem on closed invariant
  sets, not the orbit-closure classification). Being lit on Q is
  weaker than reaching the coincidence on the ordered-pair cover U
  (exact cov4181 example). Claimed: a uniform room-level bound B(r) on
  hidden points, from EMM, Filip and Lelièvre–Monteil–Weiss, with no
  explicit constant. Claimed genus bound on U: sum of genera ≥ d − r − 16,
  unbounded at r = 4 (DB55 stretches), so fixed-stratum finiteness can't
  transfer to U.
- Sharpened open target. On U, show the hidden coincidence count is at
  most αn + K with known constants and α < 5/6 (any α < 3/2 for
  n ≥ 120). Reaching one off-class coincidence also suffices for the
  large same-parity cases. d86 notes that for a dark pair this budget
  restates the open lemma numerically; it does not reduce it.
