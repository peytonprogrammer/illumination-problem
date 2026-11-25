# Coordinator log, directions 2026-11-09

Fable coordinator. Each entry records a subagent result and the decision
taken. Subagent claims are computed facts unless marked as interpretation.

## Literature check (done)

See `lit-tokarsky/findings.md`. Decisions: the target is strictly simple
rooms (Daniel, 2026-11-09). Wolecki's Lemma 3.1 widens the room class to
every triangle with angle pi/n, n even.

Coordinator hand check: for the 30-30-120 triangle, the 12 tiles around an
interior source point form a six-pointed star. Each boundary edge borders
the third tile at a 120 degree vertex, and adding it destroys a consistent
fold. So that triangle gives no strictly simple dark room. Unreviewed.

## Monodromy block systems (done)

Files: `d4-monodromy-blocks/`. Computed facts:

- 22-wall room, unit-pillow framework: degree 15,
  G = (S3 wr A5) intersect A15, order 233,280. Exactly one proper block
  system, block size 3. Its factor is the double of the five-square
  staircase, has the parity property, and separates S from T. The
  prediction of direction 2 holds.
- Every dark room in the record with no transparent point (Tokarsky 26,
  Castro 24, the 34-wall orthogonal room, all 327 census rooms) has
  primitive G equal to S_n or A_n.
- 18,219 lit controls: no lit room has a proper factor with the parity
  property that separates S from T. The 11 imprimitive lit rooms each have
  one size-2 block system from a symmetry that swaps S and T.
- Saved 10,368-state certificate: no one-cylinder state. Cylinder counts are
  2, 6, 7, 9, 10, or 12.
- If a factor has the parity property, each transparent point ramifies with
  index 2 over a pole, so k <= 2 * degree - 2. The 22-wall room has
  equality (k = 4, degree 3).

Decisions:

- Direction 4 as written is false. "G primitive implies lit" fails for every
  dark room with no transparent point.
- Corrected dichotomy, which fits all data: a pair is dark if and only if
  DP or a proper factor has the parity property and separates S from T.
  For primitive G this reads: at least one transparent point implies lit.
- The record holds only one dark room with transparent points. The
  conjecture is therefore weakly tested on the dark side.
- New experiment started: `d6-hurwitz-census/`. It tests the corrected
  dichotomy on all abstract genus-0 pillowcase covers of small degree, as
  permutation 4-tuples under the pure braid action. It is not a room search.
  If the dichotomy holds abstractly, the proof target becomes a statement
  about Hurwitz orbits and needs no polygon geometry.

## Two-mechanism audit (done; one background run for denominator 12 pending)

Files: `d3-two-mechanisms/audit.md`. Author-proved, not yet reviewed:

- The coordinator's Claim 1 is false as stated. Counterexample: the 12-wall
  cross with S = (1,2), T = (3,2). Corrected lemma: every candidate passes a
  corner-class lattice point if and only if S and T are lattice points of
  the same class and the corner classes include the other three classes.
  The sieve sketch in the memo is invalid.
- Gap in the record, already acknowledged in `review/bridge.md`: outside
  the family theorems, rational non-A pairs are unproved for
  9 <= W <= 21. The `W <= 21`, `k <= 6` theorem covers interior A pairs
  only.
- Lemma A: in a one-cylinder direction of DP, a point on a regular leaf
  illuminates every other interior point.
- Theorem B: one-cylinder directions (p_i, q_i) confine both endpoints of
  every dark pair to X = {s : q_i s1 +- p_i s2 in Z}.
- Theorem Q22: directions (4,7) and (7,4) are one-cylinder on the 22-wall
  room and give X = Z^2. So (0,0),(2,2) is the room's only dark pair among
  all real interior pairs.
- The 12-wall cross has no one-cylinder direction, so the method does not
  start on rooms with two mirror axes.

Decisions:

- Direction 3's lemma is replaced by the corrected lemma. Direction 5 is
  upgraded: Lemma A and Theorem B are the rigorous form of the cylinder
  idea, and they close the non-lattice part of the non-A gap room by room.
- Independent review started: `d3-review/` (own checker, own lit-path
  certificates for all other lattice pairs of the 22-wall room).
- Open lemma for a universal statement: every strictly simple lattice room
  without two mirror axes has one-cylinder directions with X = Z^2.

## Relaxed 30-60-90 search, phase 1 (done)

Files: `d1-306090-relaxed/`. Computed and hand-proved by the subagent:

- The coordinator's midpoint claim holds (8,816 primitive vectors, 0
  failures). The parity argument is sound with B points transparent.
- Exact minimum for C-clean strictly simple rooms: 27 walls. CP-SAT returns
  OPTIMAL 27 at hex radius 4, 5, and 6. A hand argument shows hex radius 6
  contains every room with W <= 26.
- Hand bound: two interior A points force at least 12 three-tile C corners,
  and the turning sum then gives W >= 22 with no computer.
- Regression: with B forced to be corners, the model is infeasible, which
  matches the old strict result.
- Trusted without proof log: CP-SAT statuses.

Decisions:

- The C-clean 30-60-90 class cannot beat 22. Direction 1's refutation
  attempt fails for this class.
- Not yet covered: rooms dark despite transparent C points. The 22-wall
  square room is of this type (three copies of a 10-wall base; the dark
  points sit on flat walls of the base). Phase 2 started in the same
  directory: fold-family enumeration plus a counterexample-guided search
  with transparent C points, W <= 21.
- The turning-sum count is a hand technique. `d7-wolecki-triangles/`
  started: generalize it to every triangle in Wolecki's lemma, target
  "every clean room has at least 22 walls".

## Parity-factor audit (done)

Files: `d2-factor-audit/audit.md`. Author-proved in one session, not yet
reviewed by a second party:

- Both Riemann-Hurwitz formulas in direction 2 are correct, with added
  side conditions. The case list for r <= 8 is correct.
- The conjecture as written in the memo is vacuous: it omits
  phi(S) != phi(T), and "midpoint class" must include B.
- No finite check remains for r <= 8 in orthogonal rooms. Any parity
  factor gives k <= 2 * delta - 2 <= 6, so the existing W <= 21, k <= 6
  theorem covers every case. A separate hand case analysis reaches the
  same conclusion.
- A unique finest parity factor N_min exists. It is the quotient by the
  smallest monodromy-invariant equivalence that identifies the two sheets
  at each transparent non-A point.
- Exact form of the conjecture: a pair is dark if and only if N_min
  separates S from T. "Separated implies dark" is proved. "Same fibre
  implies lit" is open, and it is a lit-side statement.
- At W <= 21 the conjecture is equivalent to the target theorem. Its
  content is W-independent: it is falsifiable at W >= 22.
- The formulas assume orthogonal rooms. Rooms with diagonal walls need
  separate bookkeeping.

Decisions:

- The whole universal problem for orthogonal lattice rooms now rests on
  one statement: two interior A points in the same N_min fibre are lit.
  Call it the same-fibre conjecture.
- Tests of the same-fibre conjecture on rooms (W = 22 dark census;
  one-defect perturbations of known dark rooms) are room and ray searches.
  They wait for Daniel's approval. The abstract census in
  `d6-hurwitz-census/` tests the permutation form without rooms.

## Review of the one-cylinder theorems (done)

Files: `d3-review/review.md`. An independent Opus reviewer with its own
checker accepted every claim and found no counterexample:

- Lemma A, Theorem B, corrected Lemma 1, Theorem A, Proposition X: accept.
  One correction: Theorem B gives rationality only for a direction with
  p * q != 0.
- Theorem Q22, accepted with two completions (self-pairs; the room has
  only two interior lattice points). Signed statement: in the manuscript's
  22-wall room, two distinct interior points are joined by no billiard path
  if and only if they are (0,0) and (2,2). Every interior point joins
  itself.
- The manuscript's darkness proof is complete.
- Certificates: two independent programs certify that (4,7) and (7,4) are
  one-cylinder directions. Explicit lit paths cover all pairs on the 1/2,
  1/3, and 1/4 grids (22,228 pairs, one unjoined).
- Not verified by the reviewer: literature theorem numbers, the record's
  family theorems, existence of one-cylinder directions in general.

Decision: Theorem Q22 is AI-reviewed with reciprocal exact checks. It is
not formally verified and has no external referee.

## Abstract cover census (done through degree 10)

Files: `d6-hurwitz-census/`. Computed facts (decider validated on the
22-wall room, three k = 0 dark rooms, and 39 lit controls):

- Exhaustive for degree n <= 10 (10,491,858 tuples at n = 10).
- "A separating parity factor implies dark" holds everywhere: 0 lit pairs
  have one.
- The converse FAILS for abstract covers: 3, 12, 87, 36 dark orbit pairs at
  n = 7, 8, 9, 10 have no separating parity factor.
- Four further mechanisms explain every counterexample: degenerate covers
  (a corner with identity monodromy), parity over an intermediate
  pillowcase (G1), different factors blocking different corners (G5), and
  rigid factors (G6, G7). G1, G5, G6 never mispredict on the census. G7
  was checked by hand only.
- Nielsen classes split into several pure-braid orbits from n = 6. Where
  orbits of one class differ in dark count, they also differ in |G|.
- Almost no counterexample is the double of a planar polygon. The one
  flagged case has marked points on walls.

Coordinator hand notes (unreviewed):

- The flagged case has corners in only two parity classes. Its cycle types
  match the five-square staircase stretched by 2 along one axis. It is the
  known base in an un-normalized lattice, not a new room.
- G1 needs two classes with no corner, which the normalization forbids.
- The degenerate mechanism needs a class whose points are all convex
  corners, which an interior marked point forbids.

Decisions:

- The same-fibre conjecture is false for abstract covers. For rooms it is
  still open; the planar hypotheses may exclude every extra mechanism.
- `d10-mechanisms/` started (Fable, high): unify the mechanisms, prove the
  "if" directions, decide which survive for normalized planar rooms, and
  derive reflex-corner bounds for those.
- Daniel approved the W <= 22 census (`d9-census-w22/`) and the
  perturbation test (`d8-perturbation-test/`); both are running.

## Perturbation test (done)

Files: `d8-perturbation-test/`. Computed facts (orthogonal rooms only;
decider validated on the 22-wall room over all 5,184 orbit states and on
31 lit controls):

- 1,027 rooms, exhaustive: all single and double local modifications of
  the 22-wall room (29 + 445) and of the 34-wall k = 0 room (31 + 520).
- 1,464 same-class interior pairs. N_min separates 3 pairs, and all 3 are
  dark. N_min does not separate 1,461 pairs, and all 1,461 are lit, each
  with a path checked by two independent tracers.
- No counterexample in either direction. Every perturbed room with at
  least one transparent point is lit. No dark room has W <= 21.
- Limits: the dark side is weakly tested; the orbit decider cannot finish
  primitive rooms (over 40 million states); perturbations are local;
  diagonal-wall rooms were not tested.

Decision: the same-fibre conjecture survives for rooms on this test. The
census in `d9-census-w22/` and the theory in `d10-mechanisms/` are the
next evidence.

## Other-triangle lower bound (done; review started)

Files: `d7-wolecki-triangles/theorem.md`. Author hand proofs, unreviewed:

- Obstruction classes: a vertex class obstructs if and only if its angle
  is pi/q with q even. A room is clean when every point of an obstruction
  class is a genuine corner. Clean implies every pair of interior A points
  is dark.
- For most allowed triangles no class obstructs, so every room with two
  interior A points is dark, and such rooms need W >= 4n or more.
- Clean-room bounds: isosceles with n >= 6 admit no room with two interior
  A points; right triangles with n >= 8 admit no clean room; 30-60-90 needs
  W >= 26 by hand (27 exact from d1); the 22.5-45-112.5 triangle needs
  W >= 32; generic obtuse needs W >= 4n + 2.
- Only 45-45-90 leaves 22 open: the count gives W >= 22, with equality
  only if the two stars share a corner.
- Author's weakest step: the exit-tile count (lemmas L3 to L5).

Decisions:

- Clean rooms from every non-square triangle need at least 26 walls, if
  the proofs survive review. Review started in `d7-review/` with an
  independent enumeration.
- Remaining gap outside squares: rooms dark despite transparent
  obstruction points, for 30-60-90 (d1 phase 2), right triangles with
  n >= 8, and 22.5-45-112.5 (assigned to the reviewer).

## Orthogonal dark-pair census (done through area 20)

Files: `d9-census-w22/` (README.md, census_totals.md, dark_rooms.json).
Computed facts:

- 945,070,200 strictly simple orthogonal rooms with W <= 22 and area
  <= 20, up to symmetry. 217,900,349 same-class pairs of interior lattice
  points, over all four parity classes.
- Exactly one dark pair: the known 22-wall room's (0,0),(2,2). No dark
  pair exists at W <= 21 within the bound. The known room is the only
  W = 22 room with a dark pair within the bound.
- Every lit pair has an explicit path, replayed by a second tracer with 0
  rejections. The one dark pair is decided by three complete deciders.
- "Dark if and only if N_min separates" holds for all 217,900,349 pairs.
- 100,538,916 rooms with W <= 20 have a lit pair with k >= 7. Only 20,332
  eligible rooms with W <= 20 have every pair at k <= 6, so the existing
  k <= 6 theorem covers few rooms.
- Validation: polyomino counts match OEIS A001168 through area 20.
- Not covered: area >= 21 (including long thin rooms), different-class
  lattice pairs, non-lattice pairs, rooms with diagonal walls.

Decisions:

- Part A started with the same agent (`partA-*` files): different-class
  lattice pairs, and one-cylinder certificates (Theorem B) to extend the
  result to all real pairs room by room.
- `d11-census-45/` started: the same census for rooms with diagonal walls.
- Machine note: under 3 GB of free disk. Agents are told to keep outputs
  small and use at most 6 workers.

## Mechanism classification (done)

Files: `d10-mechanisms/theory.md`. Author proofs from one session,
unreviewed:

- Coordinator notes (i) to (iii) hold, with corrected reasons: R1 (the
  double of a normalized room has no pillowcase factor other than B) and
  R2 (a class of only convex corners forces the 2 x 2 block).
- Theorem U ("if"): certificates of three kinds (Par, Rig, Cut) at every
  target corner imply dark. Parity factors and all four census mechanisms
  are special cases.
- Conjecture U* ("only if"): on the degree <= 10 census, all 439 dark
  pairs are certified and 0 of 12,425 lit pairs are.
- For normalized rooms with an interior pair, every extra mechanism is
  excluded by proof except two open cases: Rig with a non-embedded target,
  and Par with different factors per class.
- Revised room conjecture: D1 (proved) all three classes certified implies
  dark; D2 (open, lit side) dark implies certified; D3 (open, algebraic)
  certified implies B_min separates. Same-fibre is equivalent to D2 + D3.

Coordinator deduction: within the d9 census range (W <= 22, area <= 20),
D3 has no failure. A D3 failure is a pair dark by D1 without a separating
parity factor, and the census found one dark pair, which B_min separates.
This uses D1, which is unreviewed.

Decision: `d12-lit-side/` started (Fable, high): witness complexity on the
census, orbit structure for primitive groups, and proof attempts for the
lit side (Conjecture U* and its primitive special case).

## Paused by Daniel (2026-11-09)

Daniel paused the run to free disk space. Five agents were stopped
mid-task, and three leftover `phase2_cegar.py` solver runs were ended.
Resume each with SendMessage to the same agent, or restart from its
directory's README:

- `d1-306090-relaxed/` phase 2: fold-family enumeration and the
  counterexample-guided search with transparent C points were in progress
  (K = 4 runs interrupted). No result reported yet.
- `d7-review/`: review of the triangle lower bounds. No report yet.
- `d9-census-w22/` part A: different-class pairs and one-cylinder
  certificates. Stopped while reading; nothing computed.
- `d11-census-45/`: diagonal-wall census. Stopped while reading; nothing
  computed.
- `d12-lit-side/`: lit-side proof attempt. No report yet.

## Resumed (2026-11-09)

Daniel said to continue after freeing disk (31 GB free). All five paused
agents were resumed with their original briefs and a worker cap.

## Census part A (done through area 16)

Files: `d9-census-w22/partA-README.md`, `partA-coverage.md`. Computed:

- Different-class lattice pairs: all 6,258,116 pairs in the 12,786,778
  rooms with area <= 16 are lit.
- One-cylinder certificates on normalized rooms: 5,384,089 rooms have
  X = Z^2; 4,646,223 rooms have |X/Z^2| = 2, and all 391,921,919 extra
  pairs are lit; 2,755,406 rooms (21.5%) have no one-cylinder direction up
  to max(p,q) = 15. Of those, 99.93% have no symmetry, and 2,096,524 show
  a strip count divisible by 4 in every tested direction (all even area).
- For the 200,686 uncertified rooms with area <= 14, all 1/2-grid and
  1/3-grid pairs are lit (788 million pairs).
- Supported statement: in 10,031,276 of the 12,786,778 rooms (W <= 22,
  area <= 16), every pair of distinct real interior points is lit except
  the known pair. "No dark pair of real points at W <= 21" is fully
  established only for area <= 5.
- The earlier guess that only rooms with two mirror axes lack one-cylinder
  directions is false.

Decision: `d13-cylinder-cover/` started. It proves and applies a
generalized certificate (any cylinder whose closure projects onto the
whole room) to the uncertified rooms.

## Lit-side proof attempt (done; not proved)

Files: `d12-lit-side/notes.md`. Neither Conjecture U* nor its primitive
case PRIM is proved. Findings on the degree <= 10 census:

- Under the PRIM hypotheses all 9,118 pairs are lit, each through one
  transparent point. Longer chains are needed only for imprimitive G.
- Distance from a state to a witness state grows with degree (0, 2, 4, 5,
  5, 7, 8 for n = 4 to 10), so bounded local search is not a proof route.
- Braid orbits do not fill Nielsen classes even for G containing A_n.
  No published connectedness theorem covers these cycle types for n >= 7.
- The point monodromy M_t on regular a-points is 2-homogeneous in all
  2,885 orbits with G containing A_n under PRIM. It can fail for other
  primitive groups (|G| = 1,344, 336, 60).
- Proved (one session, unreviewed): arc-tree lemma, face certificate,
  twist lemma (a pinch state gives a transposition in M_t), abstract
  cylinder lemma, and Proposition R (M_t 2-homogeneous plus one lit pair
  gives all pairs lit).
- Refuted: any corner-by-corner proof (explicit S_8 counterexample at
  n = 8), degree induction by sheet removal (verdicts are not monotone),
  and cylinders alone (765 of 7,551 lit pairs at n = 10 have no cylinder
  witness). The corner-by-corner gloss on D2 in `d10-mechanisms/theory.md`
  is wrong; U* itself is unaffected.

Coordinator architecture for orthogonal rooms with W <= 21 (conditional):

1. Primitive G with a 3-cycle-bearing corner and large area contains A_n
   (minimal-degree bounds; r <= 8 bounds the support of g_x^2 by 24).
2. Lemma H: for G containing A_n under PRIM, M_t is 2-homogeneous.
3. One lit pair exists; Proposition R then lights every pair.
4. Imprimitive G and small area are separate cases.

Decision: `d14-lemma-h/` started (Fable, high) on items 1 to 4.

## Second-reader reviews started

- `d2-review/`: adversarial review of the Riemann-Hurwitz factor audit
  (claims 1 to 4, including the "no finite check remains at r <= 8" chain).
- `d10-d12-review/`: adversarial review of Theorem U, the room
  propositions, and the d12 lemmas that `d14-lemma-h/` builds on.

## Review of the Riemann-Hurwitz factor audit (done)

Files: `d2-review/review.md`. No mathematical error found. Claims 1 to 3
confirmed; claim 4 confirmed with a wording correction and a scope gap.

- Corrected claim 4: for r <= 8, every parity factor other than the unit
  pillowcase PC has delta <= 4 and k <= 6, so no single parity factor
  separates two distinct interior A points. "Any parity factor" was wrong:
  PC is a parity factor of every room with delta = n.
- The k <= 6 theorem is Theorem 1.1 of
  `preprints/restricted-minimum-k6/manuscript.tex`, not the 22-wall
  manuscript. It is computer-assisted and its 8.75 GB of certificates
  were not replayed.
- Scope: claim 4 excludes one darkness mechanism only. Rooms with k >= 7
  are outside the theorem (100,538,916 such rooms at W <= 20 in the d9
  census). "Par with different factors per class" and "Rig in general"
  stay open; the Z' bookkeeping needs one factor for all three classes.
- "Interior" is essential: the staircase (r = 3, W = 10) has a dark pair
  of smooth boundary A points.
- Tests: 3,747 polyominoes of area <= 8 plus 19 hand rooms, 30,868
  factors, 0 failures. Only 38 parity factors differ from PC, so claims
  2 and 3 are thinly tested by computation; the hand proofs carry them.
- Script defects, none affecting a claim: `all_block_systems` misses 76
  block systems in 44 cases; the "formulas hold" check in
  `enum_targets.py` is vacuous.

## Review of the triangle lower bounds (done)

Files: `d7-review/review.md`. Independent re-derivation; nothing imported
from d7. Every d7 claim accepted; no error or counterexample.

- Theorem 1 accepted with a completion: the first return may land at a
  flat boundary A point; the argument is unchanged.
- L2 and L6 item 4 carry scope notes (L2 needs hypothesis H; without H two
  (1,3,4) octagons sharing a side give a non-clean 14-wall room).
- New Theorem R1: for the (1,2,5) triangle every room with two interior A
  points has W >= 32, clean or not, so 32 is exact for that triangle.
- New Proposition R2: right triangles with n >= 8, a dark interior A pair
  forces W >= 2n. For (1,3,4), all 1,044,045 rooms with at most 6 extra
  tiles (up to 23 walls) are lit by exact paths.
- Enumeration (two stars plus k extra tiles) matches every claimed bound.
  45-45-90: no clean room with 10 or fewer extra tiles; with 11 the clean
  minimum is 24.
- Consequence: for n >= 6, excluding 30-60-90 and right triangles with
  n >= 8, every fold-type room with two interior A points has W >= 32.
- Open: dark pairs that are not interior A pairs; right triangles with
  n >= 8 between 16 walls and the smallest dark room; whether the
  45-45-90 clean minimum is 22, 23, or 24; non-clean 30-60-90 rooms (d1
  phase 2). AI review only; float signs certified by a norm bound.

Coordinator note: the enumeration of (1,3,4) and other fold rooms was run
by the reviewer as a check of the claimed bounds, bounded at k <= 11.

## Diagonal-wall (45-45-90 tile) census (done)

Files: `d11-census-45/README.md`. Integer arithmetic; every lit verdict
has a path replayed by a second tracer.

- A/B pairs: every strictly simple room of at most 32 triangle tiles with
  W <= 24: 734,609,564 rooms, 736,957,663 pairs. All 616,380,295 pairs
  with W <= 21 are lit. At W = 22 the only dark pair is the known room
  (30 tiles, k = 4). Nothing dark or undecided at W = 23.
- At W = 24 there are 12 clean rooms (27 tiles, k = 0, primitive
  monodromy of degree 27), dark by the k = 0 lemma; Castro's room is one.
  The orbit decider did not finish on them (3M-state cap).
- C pairs: all 1,162,254,602 C pairs inside those rooms are lit, and all
  178,695,704 C pairs in rooms of at most 24 tiles are lit.
- Same-fibre test: holds for A/B pairs (no lit pair separated; all 13
  survivors separated). The agent's extension of N_min to C pairs fails
  (14,770,425 separated lit C pairs; smallest has 10 tiles, W = 7). The
  parity proof needs an A or B midpoint, so neither separation nor k = 0
  proves a C pair dark. The conjecture must stay restricted to A/B pairs.
- With d7-review: the clean 45-45-90 minimum is 24 within 32 tiles.
- Limits: bounded by tile count (rooms with W <= 22 exist at every size);
  C pairs from 25 to 30 tiles are not covered, including the C-pair
  translate of the 22-wall room; enumerator and star growth share the
  room test (independent brute force only to n = 12).

## Review of the mechanism and lit-side proofs (done)

Files: `d10-d12-review/review.md`. No named statement is false. All
recomputed counts match (3,882 orbits with q >= 2; 12,864 pairs).

- Theorem U confirmed (0 of 12,425 lit pairs fully certified; 439 of 439
  dark pairs certified). Lemma 0 is a sketch resting on dictionary D0,
  which was not checked.
- R1 corrected: "normalized" must mean gcd 1 of horizontal edge lengths
  and gcd 1 of vertical edge lengths. Under "corners occupy three parity
  classes" R1 fails (L-tromino stretched by 3, degree 9). The earlier log
  paraphrase of normalization was wrong on this point.
- R4 had a gap in step 3: the degree-3 Cut target is planar only when the
  two [2,1] classes are diagonal. In the adjacent case the target is a
  3-cell disc K2 with an interior cone point (the Z-hexomino folds onto
  it). The reviewer's patch closes the case for interior marks; the patch
  has no second reader. For wall marks R4's conclusion is false.
- D1 is fully proved for rooms given D0; its cited dependencies were
  wrong (it needs only Theorem U with P' = B and R3).
- Proposition R corrected: M must be defined as the ID permutations pi
  with (t, pi L) in the marked orbit of (t, L); then M is a group and
  state independent. Vacuous at q = 2.
- d12 Lemma 1, F, T, T1, T2, C, G, Proposition N confirmed.
- Lemma H evidence is thinner than reported: 1,242 of the 2,885
  supporting orbits have q = 2, where the lemma is vacuous.
- D3 open cases, exactly two: O1 (two incomparable parity factors whose
  join fails to separate; needs n >= 9, r >= 3, not both block size 2)
  and O2 (Rig holds on DP / R_y where P / R_y overlaps itself or has an
  interior cone point). D3 holds when every class is Par-certified and
  the B_x are pairwise comparable.
- Most serious structural issue: room-side arguments treat fold targets
  as planar polygons. Non-planar targets are the open case of R5 and D3.
- Not checked: dictionary D0, literature citations, the imprimitive n = 8
  sketches, the d10 saved-room scripts.

Decision: review corrections forwarded to the `d14-lemma-h/` agent.
`d0-dictionary/` started (Fable, high) to prove or break dictionary D0,
the unchecked room-to-tuple correspondence under Theorem U, D1, and the
lit-side lemmas.

## Relaxed 30-60-90 search, phase 2 (done; K = 4 open)

Files: `d1-306090-relaxed/README.md` (phase 2 section), `phase2-*.json`.
No dark room with W <= 23 found.

- Fold family, hand proof (unreviewed): three copies need W >= 25 (24 if
  all three meet at one point); two copies need W >= 28; four copies need
  W >= 28. So no fold room has W <= 23.
- Direct three-copy search: minimum found is a 43-wall dark room, S =
  (0,0), T = (-12,12), base 17 walls, 4 transparent C points (the seam
  endpoints). Darkness proved by the adapted fold proof and a shooter at
  bound 40. The search window is not proved sufficient, so W from 25 to
  42 is unsettled in the fold family.
- CEGAR over simple rooms, W <= 21, A pairs, at most K transparent C
  points: K = 2 INFEASIBLE (4 T values); K = 3 INFEASIBLE (7 T values);
  K = 4 open (4 of 10 T values ran, all UNKNOWN at 1,700 s; 6 not run).
- Doubts: CP-SAT verdicts carry no proof logs; cut soundness rests on a
  written argument plus 124 sampled paths; fold-proof adaptation
  unreviewed.

Decision: no further K = 4 compute. The run does not converge at this
budget, and K has no a priori bound, so the search cannot close the
30-60-90 case. That case needs the structural route (the analogue of the
same-fibre conjecture for the (2,3,6) orbifold), same as k >= 7 for
orthogonal rooms.

## Marked-point monodromy lemma (done; not proved, plan refuted)

Files: `d14-lemma-h/proof.md`. Lemma H stays conjectural.

- Step (i) of the plan is false. In 72 PRIM orbits with G containing A_n
  every cusp loop acts trivially on the regular a-points (first: n = 5,
  G = A_5, q = 2; first with q >= 3: n = 7, G = S_7, q = 3, genus-7
  Hurwitz curve). M_t then comes only from handle loops, which no local
  computation reaches.
- Honest evidence for H (q >= 3): 1,643 orbits, all 2-homogeneous;
  M_t = S_q in 1,640 (3 exceptions with C_3 at n = 6).
- Proved: twist lemma H1; H2 (M_t modulo cusp group and deck maps is a
  quotient of the surface group of the Hurwitz curve); H3 (genus 0, no
  deck map: M_t = cusp group).
- One lit pair: equivalent to a state with a link. Holds in all 2,932
  PRIM orbits; each PRIM hypothesis is needed. For rooms, given D0, a
  link exists if r <= 5 or n > 52r + 68.
- Theorem G (from Burness-Guralnick 2022, Corollary 2, verified from the
  source; depends on CFSG): primitive G with an order-3 element having z
  3-cycles contains A_n or n <= max(6z, z^2). For rooms N_0 = 64 at
  r <= 8, sharp for group theory alone (S_8 wr S_2).
- Imprimitive G: lemmas I1', I2, I3, D2, D3 proved; the induction needs
  fibre homogeneity FH*, at least as hard as H; FH fails in 69 of 588
  rigid incidences.
- Conditional Theorem R assembled (rooms, primitive G, n > N_0, assuming
  H, D0, and E in the range 6 <= r <= 8, n <= 52r + 68).

Coordinator assessment: the abstract route is the wrong level. One-mirror
lit-ness asks whether lifts along simple arcs of the four-punctured
sphere reach every pair that lifts along arbitrary paths reach. Braid
orbits split Nielsen classes for unexplained reasons, and H2 ties M_t to
handle loops of the Hurwitz curve, so a general proof would amount to an
orbit classification for genus-0 pillowcase covers. No further agents on
abstract U*, PRIM, or H.

Clean remaining target for orthogonal rooms (from d2 and d2-review): a
parity factor other than the pillowcase forces k <= 6, so the same-fibre
conjecture at W <= 20 is equivalent to T7: every room with k >= 7 has
all interior same-class lattice pairs lit. T7 is a statement about rooms
with unbounded area and at most 8 reflex corners.

Decision: `d15-small-r/` started (Fable, high): all-area theorems L(r)
for small r by parametric path families, using room geometry (few
rectangles, direct visibility, collinearity conditions) and not the
abstract model.

## Dictionary D0 (done; proved both ways, one author)

Files: `d0-dictionary/dictionary.md`. No gap found. Not second-read; two
classical facts are quoted from memory (Hurwitz move = monodromy of the
twisted basis; simple arcs between corners are isotopic to straight arcs).

- Precise statement: the room pair is lit iff at least one of the four
  lift pairs is LIT; by reflection symmetry (S+, T+) and (S+, T-)
  suffice. A chain stays at one corner in one state. Pure braids reach
  every coprime direction because the decider reads all three arcs per
  state.
- Tests: 30 interior pairs in polyominoes of area <= 9, all lit on three
  deciders; 22-wall room dark on both sides for all four lift pairs;
  4,164 wall-mark pairs agree (4,144 lit, 20 dark); 5.4M state-level
  comparisons, 0 mismatches. Negative controls fail visibly.
- Evidence limits: the interior family has no dark pair; no test room
  separates the two lift kinds; slopes with |p| + |q| > 400 skipped.
- Wall marks: the tuple model and d8 `orbit.c` accept a segment sliding
  along a wall; d8 `tracer.py` rejects it. Interior marks unaffected.
- Corrections to earlier records: the 22-wall factor has degree 5 (block
  size 3), not degree 3; d8 README V1 should say six of the 8 regular
  points are flat and two interior; class names differ between d4/d8
  (A, C1, B, C2) and d6/d10/d12 (a, b, c, d).
- Dependency map: Theorem U for rooms and D1 need "room lit implies
  LIT"; D2 and the lit half of the same-fibre conjecture need the
  converse.

## Approval: capped tests on larger rooms (2026-11-09)

Daniel approved testing the room-level lemmas on rooms larger than area
20. Cap: rooms with at most 8 walls in a 12x12 box, exhaustive; at most
100,000 sampled rooms with 10 or 12 walls in a 16x16 box; 3 workers,
2 hours wall-clock, under 100 MB. Forwarded to the `d15-small-r/` agent.
Any dark or undecided pair gets a second decider before it is reported.

## Decision: square-lattice target (2026-11-09)

Daniel accepted the target "22 walls is the minimum among strictly simple
rooms on the square lattice, including 45-degree walls". Triangle bounds
are companion results; general polygons are an open problem, not pursued.
Recorded in GOALS.md and memory.

What the target needs, by pair type and room type:

1. Orthogonal rooms, interior same-class lattice pairs: T7 (rooms with
   k >= 7 are lit), all areas. In progress: `d15-small-r/`.
2. Orthogonal rooms, different-class lattice pairs: lit through area 16
   by census; needs an all-area proof (one-cylinder directions of the
   right parity, or a room-level argument).
3. Orthogonal rooms, non-lattice points: Theorems A and B plus
   `d13-cylinder-cover/`; needs all areas.
4. Rooms with 45-degree walls: A/B pairs, C pairs, and non-lattice
   points, all sizes. Census clean through 32 tiles only.
5. Odd wall counts occur only with diagonal walls (item 4).

## Generalized cylinder certificates (done; 11 rooms open)

Files: `d13-cylinder-cover/README.md`, `theory.md`. Unreviewed.

- Lemma A' proved: if a lift of S lies in an open cylinder of DP and a
  lift of T in its closure, S illuminates T. Full cylinders are too rare
  (0 of 102 class (iii) rooms with area <= 9), so the working tool is
  Theorem C: the union of closed cylinders over all directions; dark
  pairs have both points in the live set X'. `cover.c` computes X'.
- Validation: X' inside X on 475 class (i)/(ii) rooms; on the 22-wall
  room X' = {(0,0), (2,2)} exactly.
- Class (iii), area <= 14, directions up to 12: 200,675 of 200,686 rooms
  fully decided lit. No new dark pair.
- Open: 11 normalized rooms (areas 6, 8, 10, 12) plus 4 reduced copies.
  Ten are pole-obstructed (Proposition O): two convex corners never share
  a cylinder, and an open 4-dimensional set of pairs near them cannot be
  certified by finitely many cylinder directions. One pairs a convex
  corner with a flat point (Proposition O'). The 12-wall cross is among
  the undecided rooms.
- Unconditional statement stays: no dark real pair at W <= 21 for area
  <= 5 only. Areas 15 and 16 not run.

Coordinator plan for non-lattice points (all areas):

1. Rational points of P are lattice points of the scaled room mP, which
   has the same wall count. So all-area lattice theorems (same class and
   different class) cover every rational pair.
2. Being lit is an open condition, so the dark set is closed and
   invariant under the affine group of DP. If closed invariant subsets of
   DP x DP are finite unions of periodic pairs and graphs of affine
   correspondences (Ratner-type results for branched covers of Veech
   surfaces), every component of the dark set contains rational pairs.
   Then "all rational pairs lit" gives "all real pairs lit".
3. Near pole pairs, parabolic elements (multi-twists in the horizontal
   and vertical directions) move S out of the uncertified neighbourhood,
   which should close the 11 open rooms directly.

Decision: `d16-real-to-rational/` started (Fable, high) on items 2 and 3.

## Room-level all-area theorems (done for r <= 2; partial for r = 3, 4)

Files: `d15-small-r/theorems.md`, `cert_r3.json`, `cert_r4.json`,
`lemmas.py`. Unreviewed.

- Theorem (r <= 2): in every strictly simple orthogonal room with at most
  2 reflex corners (at most 8 walls), a billiard path joins every two
  distinct real interior points. No parity and no integrality used: edge
  lengths may be any reals. Certificates: 1, 15, 543 position-type pairs
  over 1, 1, 8 order types.
- Consequence: an orthogonal room with a dark interior pair has at least
  10 walls. First all-area lower bound in this project.
- r = 3: 13,030 of 13,608 position-type pairs certified (578 open; 3 of
  70 order types complete). r = 4: 503,328 of 564,629 (61,301 open; the
  cross is complete).
- Open pairs are of three kinds: collinear pairs with a reflex vertex
  between them; half-period doors (a door with two reflex ends); chains
  through doors that do not share a rectangular hub.
- Lemmas proved for real points: A, A2, B, B', B2, C, D.
- Refuted: bounded reflections. L-shaped room [0,60]x[0,2] with
  [0,1]x[0,100]: every path from (50,1) to (1/2,99) reflects more than
  95 times. So no finite candidate list exists per order type.
- Mechanical method at r = 8 is infeasible as designed: about 10^9 order
  types; validity conditions are bilinear; parity-free certificates must
  fail somewhere by r = 9.
- Capped tests (approved by Daniel): all 290,060 rooms with at most 8
  walls in a 12x12 box, 356,724,940 pairs, 0 failures; 100,000 sampled
  rooms with 10 or 12 walls in a 16x16 box, 417,791,881 pairs, all lit
  (28,996,621 by shooting only), none dark or undecided. About 8 minutes
  of the 2-hour cap, 58 MB.
- Deviations reported by the agent: a first check ran before the claims
  were written; Lemma D was added after sample run 1; four processes ran
  at once for under a minute.
- Weakest step: `lemmas.py` must encode the lemma hypotheses faithfully;
  only 14 of the r = 2 certificates were read against the shapes.

Decisions: `d15-review/` (second reader for the r <= 2 theorem) and
`d17-r3/` (close r = 3 with collinear, half-period door, and chain
lemmas) started, both Fable, high.

## Exploration: incommensurable rooms (2026-11-10)

Daniel asked for an exploratory agent on rooms with right-angle or
45-degree corners and incommensurable side lengths. `d18-incommensurable/`
started (Fable, high): theory and literature only, no room searches.
Route: such rooms are not torus covers, so Apisa-Wright Theorem 3.6
confines blocked pairs to periodic points, zeros, and Q_min-identified
pairs; the work is to compute that exceptional set. Outside the accepted
square-lattice target; exploration only.

## Exploration: incommensurable rooms (done; unreviewed)

Files: `d18-incommensurable/exploration.md`. Rests on Apisa-Wright
1708.03411 (read from source) plus Wright's field-of-definition theorem
and others cited from memory.

- Unfolding of an orthogonal room: X(P) in H(2^r), genus r + 1,
  hyperelliptic. Torus cover iff the horizontal lengths span Q-dimension
  a = 1 and the vertical lengths b = 1.
- Theorem B (generic lengths, any r): every two distinct non-vertex
  points are lit. Holds for almost every room of each combinatorial type.
- Theorem L (r = 1): every incommensurable L-shaped room is fully lit.
- Theorem C (every incommensurable room): dark interior pairs lie in
  E x E for a finite set E of points with periodic lifts, or on fold
  lines of a smaller room that P covers by reflections; the fold-line
  case is empty when a + b >= r + 3.
- Remaining for r >= 2 with special lengths: classify orbit closures in
  the hyperelliptic locus containing a room surface; find periodic
  points; decide fold-line pairs.
- pi/4 rooms: finite exceptional set for every non-Gaussian room; generic
  closure only sketched. Irrational angles untouched. No limiting
  argument reaches lattice rooms.

## Reduction from real pairs to rational pairs (done; unreviewed)

Files: `d16-real-to-rational/reduction.md`. Elementary proof; no Ratner
or orbit-closure theorem used.

- Corollary 1: in a strictly simple orthogonal lattice room, if every
  pair of distinct rational interior points is lit, every pair of
  distinct interior points is lit.
- Theorem 1: a dark pair with S irrational has, after exchanging axes,
  S = (x, y), T = (rho x + c, v) with y, v, c, rho rational, and the
  pair stays dark as x varies, so rational dark pairs lie arbitrarily
  close. No limit of room pairs is taken.
- Ingredients proved there: openness on the unfolding M (Prop 1), twist
  invariance on M and DP (Prop 2), Lemmas D, R, G, F. Unfolding lemma
  cited from Wolecki Lemma 2.1 (stated there without proof).
- Open: whether a one-parameter dark family exists in some orthogonal
  lattice room. Excluded for rooms with an open set of universal
  illuminators (Prop U) and for lattice rooms with both an axis-parallel
  and a 45-degree wall (Theorem 2: every dark pair rational).
- Corrections to the coordinator brief: twists do not act on room pairs
  (reflections conjugate a twist to its inverse), so certificates must be
  tracked on DP by lift class.
- Agent's reading: Wolecki Theorem 1.2(i) has a gap for orthogonal
  polygons (Lemma 2.9 asserts rank 2 where the hypothesis gives rank at
  most 3; the rank-3 case is the one-parameter family). Not a published
  erratum; unverified.
- The 11 open rooms from d13 all close: Lemma T' confines dark pairs to a
  grid (1/D) Z^2; every candidate pair is lit (W = 20 room: 405,450
  pairs). Control: the 22-wall room leaves exactly the known pair.
  Depends on `dpcover.c`, a patched copy of unreviewed `cover.c`,
  validated by sampling (17M triples, 0 failures).
- Defect found in d13 `shoot.py`: `m_hits` misses a corner on a path
  along a lattice line; wrappers skip those directions.

Consequence for the target: with Corollary 1, the orthogonal part reduces
to lattice pairs (same class and different class) in rooms of all sizes.

Decision: `d16-review/` started (Fable, high, narrow): Lemmas D, G, F,
Theorem 1, Corollary 1 only.

## Review of the real-to-rational reduction (done; Corollary 1 stands)

Files: `d16-review/review.md`, `slidecheck.py`.

- Propositions 1, 2, Lemmas R, G (including case B), Theorem 1, and
  Corollary 1 confirmed.
- Lemma D: statement holds; one proof step is false (an affine map fixing
  the end vertices need not fix the edge; counterexample on the 8-square
  quaternion surface). Repair: pass to a power H^k, Vt^k that fixes each
  horizontal edge. Lemma F item 3 needs the same extra power.
- Theorem 1's "small delta" made explicit; the rational pairs produced
  are distinct, interior, and off the excluded lines.
- Residual: the chain rests on the unfolding lemma (cited as standard,
  no proof in the source); Corollary 1 gives no denominator bound.

Status: the reduction is AI-reviewed. The orthogonal part of the
square-lattice target is now exactly: all lattice pairs lit in every
strictly simple orthogonal lattice room with at most 20 walls, all sizes
(rational points being lattice points of scaled rooms).

## The 10-wall case (done; not proved)

Files: `d17-r3/r3.md`. Theorem 3 is not proved. All 578 open
position-type pairs at r = 3 still lack a metric-free certificate.

- New lemmas, proved for any r: H (door seen through a channel; lit
  unless L h / (w D) is a positive integer and D > h, with an exact
  residue condition) and C+ (two doors on a hub with a cut corner). No
  collinear lemma.
- They certify 3.2% of open instances at r = 3 and 2.7% at r = 4. Chains
  are 96% of the open pairs.
- Tests (approved range, about 17 minutes): 22,045 ten-wall rooms,
  2,452,103 open-type rational pairs, all lit; 60,389,695 Lemma H paths
  and 4,478,424 C+ sign pairs, 0 failures after one bug fix in the
  agent's corridor scan (run 1 stopped on 94 invalid paths). No dark or
  undecided pair.
- Assessment by the agent: lemmas of this kind do not avoid enumerating
  order types. Path families fail only on resonance sets and then only
  for bad residues; a proof for r <= 8 must show bad residues of all
  families cannot coexist. That is where parity enters.

## State of the programme (2026-11-10)

Target: 22 walls is minimal among strictly simple square-lattice rooms.

Proved here (AI-reviewed unless marked):
- 8 walls or fewer, orthogonal, any real lengths: fully lit (review of
  this theorem in progress).
- Theorem Q22: exactly one dark real pair in the 22-wall room.
- Real pairs reduce to rational pairs in orthogonal lattice rooms.
- Theorem U (certificates imply dark); dictionary D0 (one author).
- Parity factor other than the pillowcase forces k <= 6 at r <= 8.
- Triangle lower bounds (d7, reviewed).
Exhaustive evidence: orthogonal census (area <= 20), diagonal census
(32 tiles), abstract census (degree <= 10), samples to 12 walls in 16x16.
Open, with no route in hand:
- Lattice pairs lit in all orthogonal rooms with 10 to 20 walls, all
  sizes. Abstract route: equivalent in difficulty to an orbit
  classification. Room-level route: stalls at 10 walls on chains and
  resonances.
- Diagonal-wall rooms of all sizes.
Coordinator conclusion: the target stays a conjecture. Further agents on
the two closed routes are not justified without a new idea.

## Review of the 8-wall theorem (done; theorem stands)

Files: `d15-review/review.md`. No gap and no counterexample.

- Theorems 0, 1, 2 confirmed with one correction to the setting: vertex
  coordinates are real (the text said integer; no proof uses it).
- Lemmas A, A2, B, B', B2, C (par, perp), D confirmed. Lemma C (same
  form) is false as written when one corridor serves as both arms;
  corrected hypothesis: the two doors belong to two different corridors.
  Theorem 2 is unaffected (0 such certificates at r = 2; also 0 of 200 at
  r = 3 and 0 of 8,227 at r = 4). `lemma_C` in `lemmas.py` does not
  exclude that reading.
- Independent enumeration: 1, 1, 8 types and 559 position-type pairs,
  matching; all certificates reproduced by separate code; 60 hand-checked.
- Exact tests in Q(sqrt 2), Q(sqrt 5), Q(sqrt 3): 2,160 two-reflex rooms,
  148,031 pairs, 0 failures. Limit: 169 Lemma B paths exceed 200,000
  reflections and were checked by exact window count only.
- Statement to record: a strictly simple orthogonal room with a dark pair
  of interior points has at least 10 walls. Lower bound only; boundary
  points excluded (10-wall staircase).

All agents are finished. No agent is running.

## New idea: finiteness of dark families (2026-11-10)

Coordinator idea, approved by Daniel for one agent (cap about 150k
tokens). The dark locus D_r in the marked stratum Q(1^r, -1^{r+4}, 0, 0)
is closed (lit is open) and GL(2, R)-invariant, so by
Eskin-Mirzakhani-Mohammadi it should be a finite union of affine
invariant submanifolds. Each dark lattice configuration is a closed
orbit, so all but finitely many lie in positive-dimensional dark
families, where Apisa-Wright forces a fold structure (already bounded by
the k <= 6 count). Expected limits: ineffective; families made only of
torus covers need separate treatment. `d19-finiteness/` started (Fable,
high) to check each step against the sources.

## Finiteness of dark families (done; decomposition proved, conclusion not)

Files: `d19-finiteness/finiteness.md`. One author; several inputs cited
from memory (Masur-Smillie compactness, Smillie, Gutkin, Monteil).

- Theorem: for r >= 1 the dark locus D_r in Q(1^r, -1^{r+4}, 0, 0) is
  closed and GL(2, R)-invariant and equals a finite union of affine
  invariant submanifolds, each entirely dark. Closedness is Apisa-Wright
  Lemma 3.7; finiteness is EMM Theorem 2.2 plus the marked-point
  extension asserted in Lelievre-Monteil-Weiss and a properness argument
  for the quadratic case. Ineffective: no bound on the number of pieces.
- Types of pieces: sporadic (closed orbit; finitely many); a-fold (every
  member has a half-translation cover f with f(S) = f(T), degree between
  2 and r, target with at least 5 poles); a-per (S, T periodic points of
  a non-torus-cover family; no fold forced); b (torus-cover families of
  dimension at least 3).
- Correction to the coordinator's step 3: one closed orbit contains
  infinitely many lattice rooms (diag(1, n) P). Finiteness of sporadic
  rooms holds up to independent scaling of the two axes.
- Not proved: "all non-sporadic dark rooms have fold structure". Types
  a-per and b escape it. Type b includes the half-rational one-parameter
  families left open in d16.
- Novelty: a direct corollary of published theorems; no statement of it
  found after a light search. Treat as likely new, not certain.
- A dark family meets the room locus only in the diagonal orbit; the
  fold structure still holds on the lattice room itself.

Decision (Daniel approved, cap about 150k tokens): `d20-periodic/`
started (Fable, high) on the a-per type: can periodic-type dark families
have regular marked points, and if so with what structure.

## Periodic-type dark families (done; open for r >= 3)

Files: `d20-periodic/periodic.md`. Two key citations (Apisa 2110.07540
Thm 1.5; Apisa-Wright High rank Thm 1.1) read through a page summary,
not the source.

- Full stratum: every periodic point is a cone point (Apisa-Wright
  1708.03411 Thm 1.4), so a-per with regular points cannot occur there.
- Proper N: rank 1 means a closed orbit (zero rel), so never a-per. No
  proper N has rank at least (r + 3)/2. a-per is empty for r <= 2.
- r >= 3, three possibilities: (A) full locus of covers over a smaller
  stratum, where regular periodic points are exactly the order-2
  ramification points over poles; (B) primitive N of rank at least 2
  (existence open); (C) covers of a primitive locus (needs r >= 6).
- New structure to add to the classification: "bi-pole" pairs in case
  (A), with S and T over two different poles of the base and no fold.
  Proved lit for degree at most 4. For r <= 8 a dark one needs base
  Q(1, -1^5), degree 5 to 8, and r >= 5: a room tiled by 5 to 8
  reflected L-shaped rooms with S, T at different tile-corner types. No
  example known. The d2 bound does not cover this case.
- Open: (1) the degree 5 to 8 monodromy question, finite and decidable by
  a Hurwitz-orbit script; (2) primitive rank >= 2 loci in genus-0 strata
  with three or more zeros; (3) non-arithmetic Teichmuller curves in
  these loci (none known).

Decision (Daniel: "run the finite check"): `d21-bipole/` started (Fable,
high; cap about 100k tokens, 3 workers, 1 hour): enumerate degree 5 to 8
covers of Q(1, -1^5) with r <= 8 and decide every bi-pole pair on
square-tiled members with the validated decider.

## Finite check of bi-pole pairs (done; one dark family found)

Files: `d21-bipole/README.md`. About 20 CPU minutes.

- Enumerated covers of Q(1, -1^5) of degree 5 to 8 with r <= 8: 8,510 /
  75,168 / 153,440 / 62,100 tuples; 35 / 106 / 47 / 76 families;
  12.2 million bi-pole pairs.
- One entirely dark family, degree 5, r = 8: tuple
  (1, 1, (0 1)(2 3 4), (0 1 2)(3 4), (0 4 2)), S = {0,1}, T = {3,4}.
  Monodromy S_5, prime degree, so no intermediate cover and not fold
  type. It branches over three poles only; the arc from b_S to b_T is
  unique in the thrice-punctured sphere and both lifts from S end at a
  zero. Darkness for every base is a short hand proof (unreviewed);
  computation confirms it on four square-tiled bases (orbits up to
  1,382,400 states). Degrees 6, 7, 8: none.
- This refutes the conjecture in `d20-periodic/periodic.md` section 5.4
  and adds a mechanism to the abstract classification: a rigid
  three-point cover over a non-pillowcase base. Whether Theorem U's
  certificates (stated over pillowcase factors) cover it is unchecked.
- Sanity: degrees 2 to 4 all lit; the 22-wall room reports DARK;
  independent ray tracer agrees on 1,720 pairs.

Coordinator deduction (simple, not yet second-read): this family cannot
give a room with an interior dark pair. In the double of a room tiled by
copies of the base, an interior point where four tiles meet gives two
2-cycles at its pole (the two lifts); a single 2-cycle is a flat wall
point. Here the pole under S has cycle type (2,3) and the pole under T
has type (3,2): one 2-cycle each. So in any room realization S and T are
wall points. That agrees with the census (no dark interior pair at 20
walls, area <= 20) and with the known 10-wall staircase, whose dark pair
is also on the boundary. For rooms with at most 20 walls and interior
pairs, the bi-pole mechanism over the L-shaped base is therefore
excluded at degrees 5 to 8, and at degree <= 4 by the d20 proof.

Decision (Daniel approved option 1): `d22-structured/` started (Fable,
high; cap about 150k tokens, 3 workers, 1 hour): enumerate every cover
structure over bases Q(1^z, -1^{z+4}) with delta * z <= 8, decide
same-pole, bi-pole, and free fold pairs, apply the interior filter, and
check the coordinator's wall-point deduction and d21's hand proof.

## Structured-mechanism enumeration (done; no counterexample)

Files: `d22-structured/README.md`. About 35 CPU minutes. Unreviewed.

- Bound r = delta * z + t confirmed: z = 1 with delta <= 8; z = 2 with
  delta <= 4; z = 3, 4 with delta = 2. Covers enumerated: z = 1: 10 / 60
  / 665 / 8,510 / 75,168 / 153,440 / 62,100 (delta 2 to 8); z = 2: 15 /
  135 / 680; z = 3: 21; z = 4: 28.
- Dark families: three in total, all over Q(1, -1^5). P2: the d21
  family (delta 5, r = 8). P1 (same pole), new: delta 4, r = 6, tuple
  (1, 1, (123), (012), (01)(23)), group A_4; and delta 5, r = 8, tuple
  (1, (234), (123), (012), (01)(34)), group A_5. Both primitive, dark
  for every base by a hand lemma (Lemma A, one author). P3 (free fold
  pairs): none. z >= 2: every node lit.
- Interior filter: none of the three passes. d21 family: S, T are wall
  points. P1 families: S, T are two wall points or the two lifts of one
  interior point (not a pair of distinct room points). No room built.
- Coordinator's wall-point deduction: correct for rooms tiled by
  reflected copies of a base, with two corrections: the partner 2-cycle
  can sit over a different pole when the base reflection moves the pole;
  and equivariance of the cover under the room reflection is an
  assumption, not a consequence.
- d21 hand proof holds after adding two steps (no bounce at a third
  pole; the projected saddle connection is a simple arc).
- Theorem (unreviewed): for a strictly simple room with at most 20 walls
  and a reflection-equivariant cover of degree >= 2 onto a base with at
  least 5 poles, no pair of distinct interior points is a dark P1, P2,
  or P3 pair.
- Not covered: non-equivariant covers; torus-cover families over the
  pillowcase; primitive loci; sporadic rooms; mixed ramified/free pairs.
- Weakest: the equivariance hypothesis; P3 at z = 1 for degrees 2, 3, 6,
  7, 8 relies on family grouping.

Decision (Daniel: "ok go"): `d23-equivariance/` started (Fable, high;
cap about 100k tokens): remove the equivariance hypothesis from the d22
theorem, by showing the cover descends under the room reflection or by
counting that the forced dark pairs never contain the four-lift pattern
an interior room pair needs; also treat mixed ramified/free pairs.

## Equivariance gap (done; hypothesis removed, unreviewed)

Files: `d23-equivariance/README.md`. Hand proofs by one author; about
19 CPU minutes of cross-checks. Rests on the d22 census (not re-verified).

- Theorem: for a strictly simple orthogonal room P with at most 20
  walls, any side lengths, and a half-translation cover f: D(P) -> Y of
  degree >= 2 onto a base with at least 5 poles, no two distinct points
  of P, at least one interior, have a lift pair that is a P1 or P2 pair
  of a dark family. No P3 family is dark.
- Route 1: two covers with 2-transitive monodromy sharing a ramification
  point have the same fibres; the reflection fixes every corner and each
  family has a 3-cycle at a reflex corner, so f rho = sigma f. Route 2:
  family pairs of different covers are equal or disjoint, so the
  four-lift pattern cannot occur.
- Cross-check on all 300 family members over L(2,2): groups A_4, A_5,
  S_5; zero interior-interior and wall-interior patterns under all 142
  disc-quotient reflections; none of the 300 is a room double. A_5
  family: 38,834 cross-corner pairs undecided, counted as possibly dark.
  12 dark pairs on 6 A_4 members are not family pairs (same-fibre pairs
  over a wall midpoint).
- Mixed pairs: no dark family with one ramified and one free point off
  torus-cover loci (given Apisa-Wright Theorem 3.6).
- Open: wall-point pairs in the three families; sporadic dark pairs;
  torus-cover loci; r > 8.

Summary of the structured part (d19 to d23): a dark pair of distinct
interior points in an orthogonal room with at most 20 walls cannot come
from a parity factor over the pillowcase with k >= 7 (d2), nor from any
cover structure over a base with at least 5 poles (d22, d23). What
remains is sporadic rooms, torus-cover families, and exotic primitive
loci whose existence is open.

Decision (Daniel: "yes go" to both follow-ups): `d19-23-review/`
(second reader for the structured-mechanism chain) and
`d24-one-parameter/` (existence of one-parameter dark families from d16
Theorem 1) started, both Fable, high, capped at about 150k tokens.

### d19-23-review (done 2026-11-10; second reader, 144k tokens, no network)

Verdicts: d19, d20, d21, d23 CONFIRMED WITH CORRECTION; d22 CONFIRMED.
The final d23 theorem stands. Corrections:
- d23 Lemma 1 needs "cone angle p*pi with p prime at Z" (true on room
  doubles). Route 2 proves less than item 2; item 2 rests on Lemma 2.
- d22 Lemma A: lift through the orientation cover of X. Independent
  re-run of z = 1, delta = 4 matches all counts and verdicts; node counts
  for z = 2, 3, 4 match; verdicts there and degrees 5 to 8 not re-run.
- d21: "two reflections can't join five tiles" holds only for the listed
  pole ordering; the reviewer's count covers all orderings.
- d20 Section 6 is wrong for r >= 2: covers of L-shaped Veech doubles give
  non-arithmetic closed orbits that contain room doubles.
- d19: type (b2) is empty by d20 Lemma 1 (zero rel).
- Reviewer's addition (unreviewed; coordinator checked the side count by
  hand and found no error): no room double lies in any of the three dark
  families, so the wall-point case closes too.

Coordinator correction: earlier summaries said "structured mechanisms
excluded at <= 20 walls". The chain excludes only full P1/P2/P3 families
over a full base stratum. Not covered: closed orbits (lattice rooms with
rational points, rooms tiled by a Veech L-table), type (b1), fold or
periodic pairs over a proper sublocus of the base stratum, primitive loci.
The chain is no evidence for 22-wall minimality in lattice rooms.
Citations still not re-read at source: Apisa 2110.07540 Thm 1.5 and the
high-rank theorem (summary only), Apisa-Wright Thm 1.4 (earlier session),
EMM Thm 2.2 with marked points (LMW remark).

### d24-one-parameter (done 2026-11-10; OPEN, narrowed; 171k tokens)

Answer: open. No family found, none excluded in general.
- Theorem X (proved by the agent; coordinator read Steps 1 to 3 and found
  no error; no second reader): an M-dark pair with pi(s) irrational and
  primitive relation a pi(s) + b pi(t) = c0 has c0 = 0. Corollary: a
  family is S = (x, y0), T = ((k - a x)/b, v0) with k, a y0 + b v0,
  a y0 - b v0 integers.
- The twist attack fails: v k_e = k_e v^-1, so the twisted lift pairs
  belong to two room pairs and Theorem 1 doesn't apply.
- A family is a common line of four dark surfaces in M x M; two of the
  four must be dark by monodromy alone (no blocking point).
- No abstract obstruction: the 27-square Heisenberg-mod-3 surface has the
  blocker-free dark family (s, c s), c the central commutator.
  Coordinator checked: exponent 3 and primitive classes make g^k != c.
- Computation (exact tracer, checked on three hand paths only): 13,384
  polyominoes of area 2 to 9 and 256 plus-tree rooms at slopes rho = +-1,
  90 polyominoes of area 2 to 5 at 12 other slopes; about 3.2 million
  samples; all lit.
- Deviation: the brief allowed computation on one fixed explicit room for
  a candidate family. The agent instead enumerated small rooms. This is a
  room-and-ray test outside the approved caps; small (under 30 minutes,
  204 KB). Reported to Daniel.
- Open question, exact form: does a room unfolding have a real line on
  which two components of {a pi(s) + b pi(t) = 0} and two of
  {a pi(s) - b pi(t) = 0} are all dark? Unused hypothesis: M/K is a disc.

### d25-astra (done 2026-11-10; idea exchange with Codex on GPT-6-Astra)

Requested by Daniel ("collaborate with Codex Astra"). Two rounds, read-only
Codex session 01a1c80d, theory only. Files: `d25-astra/brief-round1.md`,
`astra-round1.md`, `brief-round2.md`, `astra-round2.md`.

Outcome: no idea that either side would fund at more than a few percent.
- Astra's verdicts on the coordinator's ideas: A (word-family cover)
  salvageable with multi-winding templates, its best bet at 10% in round 1;
  B (twist expansion) is the orbit classification again; C (vertex
  counting) dead as stated because of wrong-lift endings (d24); D
  (surgery) needs door position and direction as the inductive object.
- Astra's idea I (rank([H,V] - I) = 2r as an obstruction): killed by
  Astra in round 2. Holes in midpoint relations are unbounded at r = 0
  ([0,6m]^2, X = (1,1), S = (6i+2, 6j+2), T = S + (2,2): d = 3 mod 12m).
- Astra's idea II (four dark correspondences can't share an arc): side
  issue; d16 already reduces to rational pairs.
- Reformulation (coordinator, round 2; checked by both): on the unfolding
  M, for a primitive direction d the lattice leaves (saddle connections
  and closed lattice geodesics) partition the regular lattice lifts. A
  lattice pair is lit iff for some primitive d a lift pair lies on one
  leaf. Midpoint-only (g = 2) is not enough: L room
  [0,8]x[0,4] U [0,4]x[0,8], S = (2,2), T = (6,2) needs a 4-step chain.
- Uniform incidence bound (Astra, proof read by coordinator): for each
  primitive d the continuation-by-2d graph on regular A-lifts has at most
  b_0 + b_delta <= 4r + 4 path components, plus z_d cycles. The pair
  count sum n_i^2 >= a_0^2 / (4r + 4 + z_d). It bounds aggregate losses
  only; z_d is unbounded at r = 0 and directions overlap.
- Astra's final line: fund only a capped attempt at a cross-direction
  component-intersection inequality; 3% to close the orthogonal case.
- Coordinator's reading: cross-direction control of leaf partitions is
  the SL(2,Z)-orbit of (M; s, t), i.e. the orbit classification (dead
  end 2). Heuristic only: a pair is dark iff it avoids a common
  horizontal leaf on every surface of a finite orbit, which is why dark
  pairs are rare without a structural reason.

### Decision 2026-11-10: unconventional ideas 1 and 3

Daniel: "ok go, do 1 & 3 together". Approval recorded for idea 1, an
adversarial optimization search for dark rooms with W <= 20 (orthogonal,
large rooms), capped at 3 workers, 2 hours compute, 300 MB. Started:
`d26-adversarial/` (Fable, high) and `d27-free-group-lit/` (Opus,
literature on Nielsen equivalence, Markoff connectivity, origami orbits,
positive primitive words). Ideas 2 (compactness cover) and 4 (planarity)
not started.

### d27-free-group-lit (done 2026-11-10; Opus, 77k tokens)

No published theorem settles r <= 8 or classifies SL(2,Z)-orbits of
origamis with two marked points. Closest analogue: Duryev (arXiv
1905.09312, Geom. Topol. 2024), vertex illumination on genus-2
square-tiled surfaces via SL(2,Z)-orbit classification plus cylinder
arguments; proved for d <= 5 only. Apisa-Wright Thm 1.3 has the shape of
the same-fibre conjecture but excludes torus covers. Free-group/Markoff
line (Chen, Eddy et al., Zmiaikou): analogy only.
Coordinator review: the suggested first lemma (s on the bottom and t on the
top boundary of one cylinder => connected) is the cylinder certificate
already used in d13 (Lemma A', Theorem C); not new. Duryev's d <= 5
method is a template for small cases, not a route to r <= 8.

### d26-adversarial (done 2026-11-10; Fable, 128k tokens, 72 min, 2.1 MB)

No dark room with W <= 20 found. About 892,000 rooms, areas 12 to 900,
boxes up to 64x64, seven annealing runs; seeds include every one-rectangle
edit of the 22-wall room and its 2x scaling. Only about 12,000 rooms above
area 300. Tools validated: known pair unlit to length 440 and DARK in
orbitc; independent Python tracer matched 608 shortest lengths.
Near-darkness: no C(r) x diameter bound (two DxD chambers joined by a 1x1
corridor, r = 2, grow without bound in rho). Longest shortest lighting
path / area <= 1.42 in every room tried at r <= 8 (max at area 21; falls
with area). Agent's conjecture: path length <= 1.5 x area for r <= 8.
Closest rooms: fat chambers joined by width-1 corridors.
Coordinator review: evidence only. A per-room length bound gives a finite
check per room, not across rooms, so it is not a proof route by itself.
Caveat: orbitc handles area <= 40 only, so large candidates had no
complete decider (none arose). No README written in d26.

### New route 2026-11-10: band stabilization (Daniel: "do better")

Coordinator's idea, `d28-band-stabilization/idea.md`: inserting a
vertex-free horizontal band of height D into a room preserves a lit
witness whenever D is a multiple of 2 lcm(chord widths) lcm(crossing
numerators p). It relates darkness on different square-tiled surfaces,
which nothing earlier does. If lit/dark status is eventually periodic in
each gap of a finite set of skeletons (W <= 20), the conjecture becomes a
finite computation. Started: d28 agent (Fable, high; prove, measure
witness periods, find the obstruction; 45 min compute from the remainder
of today's approved search cap) and Astra round 3 (same idea, adversarial).

Astra round 3 (done; 241k cumulative session tokens): band lemma PROVED
(all segments share |q|, |p| in an orthogonal room, so the period is
2 lcm(w_i) |p|). Skeleton-uniform numerator bound FALSE: rectangle
[0,6]x[0,3D], S = (2,D), T = (4,2D), D = 2^j forces |p| >= D/2
(coordinator checked the 2-adic count). Three gaps vary together there, so
one-gap periodicity is not refuted. Propagation alone can't give
periodicity (composite-number analogy). Restricted stabilization proved
for Lemma H's channel: lit once D > L h / w. Astra's reframing: what is
needed is a compression theorem (a dark room with a gap > B yields a
smaller dark room); a gap bound is an area bound (area <= 121 B^2).
Astra: 5% that a stabilization-type reduction is provable for W <= 20.

### d28-band-stabilization (done 2026-11-10; Fable, 130k tokens, 12 min compute)

Full reduction fails. Band lemma PROVED (any cell row; one p per path;
M = 2Lp/gcd(q,2L); iff per direction). Lit_p periodic mod 2Lp from g = 1.
A dark room on a line forces unbounded p on its residue classes. Several
rows: about Q^k residue vectors (> 10^37 at k = 10); vertical stretches
change every horizontal modulus.
New facts (CHECKED, tracer band.c validated against orbitc):
- The 22-wall dark pair is destroyed by duplicating any row: dark only at
  g = 1 on all 6 rows; lit at every odd g to 801 (row 0 to 1,441,445);
  72 stretched rooms (g = 2..7) have no dark pair at all (orbitc).
- Covering certificates prove infinite one-parameter families lit: all 63
  pair-lines of the 20-wall neighbour of the dark room (P <= 10) and 452
  of 452 in three other rooms. 4 pair-lines of a W = 16 room uncertified
  at P = 8 (class gap = 0 mod 10080; slit-degeneration hypothesis).
Coordinator synthesis: "rigidity conjecture" - in a room with W <= 20 a
pair is lit whenever some run of >= 2 identical cell rows or columns
avoids the rows and columns of S and T. Rigidity would confine any
counterexample to a box of side r + 3 = 11 (special lines <= r + 4 per
axis), a finite census. Rigidity is still universal over the rest of the
room, so it is not easier in kind; unproved.

Decision 2026-11-10 (Daniel: "nice idea, go"): rigidity programme.
Started `d29-rigidity-test/` (Opus; search for dark rooms at W = 24
orthogonal and the 12 diagonal 24-wall dark rooms, check for runs;
caps 3 workers, 1 hour, 200 MB, set by the coordinator under Daniel's
approval of "a small test") and `d30-rigidity-proof/` (Fable, high;
theory only).

### d30-rigidity-proof (Fable hit its usage limit at the end; rigidity.md complete)

- Rigidity is FALSE without the wall bound: P6, four reflected copies of
  the 5-cell staircase Q (the 22-wall room's factor), W = 28, r = 12,
  k = 6, a height-2 run (width-1 corridor), dark pair S = (1,0),
  T = (3,-2) by the fold-back lemma (degree-4 parity factor onto DQ).
  Coordinator re-ran mirror_check.py: no witness to |q|,|p| <= 30; lit at
  run heights 0, 1, 3, 4, 5, 6. Darkness is isolated at g = 2.
- Theorem R (PROVED, unreviewed; check the zip argument in case (E)):
  a run of height >= 3 admits no parity factor other than PC, any W.
- For r <= 8, rigidity = same-fibre conjecture (lit side) restricted to
  rooms with a run. A proof must use r <= 8 in a way that fails at r = 12.
- Open: a dark room with a run at 22 <= W <= 26.
Future agents: Fable usage limit reached; use Opus.

### d29-rigidity-test (done 2026-11-11; Opus, 121k tokens, 36 min, < 1 MB)

No counterexample to rigidity. Orthogonal census W <= 24, area <= 19:
545,201,856 rooms, 70,665,634 pairs; only dark pair is the known 22-wall
room (no run; vertex on every interior line). No W = 24 room is dark at
area <= 19 (11,321,897 pairs lit, re-checked). W <= 22 counts match d9.
The 12 diagonal 24-wall dark rooms have no run. Deviation: about 6
processes for 1 minute on the first launch (cap 3); stopped and rerun.
Verdict on the rigidity route: consistent with every dark room known
below 28 walls, false at 28 (d30 P6). Its proof at W <= 20 is the
same-fibre lit side restricted to rooms with a run, so the route
reduces the target to that core plus an 11x11 census, not to something
easier in kind.

Decision 2026-11-11 (Daniel: "ok go"): `d31-run-dark-min/` (Opus) - smallest W of a dark room with a run, by mirrored copies of parity-property bases; 2 processes, 20 min.

### d31-run-dark-min (done 2026-11-11; Opus, 103k tokens, 5 min)

Within the glued-copy class (29 parity-property bases of area <= 10,
d = 2..9, trees and cycles, 38,902 rooms), the smallest dark room with a
run has W = 28 and is unique up to symmetry: d30's P6. Next: W = 34 (3
rooms), W = 36 (7). All 11 rooms with W <= 36 verified by orbitc (complete)
and by the d30 tracer; both agree. Only the staircase Q yields a pair the
fold separates. Wall formula W(P) = d (W(R) - 4) + 4 + 2 n3 (hand proof,
unreviewed; held on all 38,902 rooms). Outside the class: factors that
are not whole copies of one base, and dark rooms with no separating
factor; W = 24, 26 remain open in general.
Coordinator reading: rigidity has a margin of 8 walls inside the only
known darkness mechanism. Its W <= 20 proof is still the same-fibre lit
side for rooms with a run.

Paused 2026-11-11 (Daniel agreed). State page: `STATE.md`. GOALS.md entry marked [blocked] and pointed to it.

Tokarsky note (2000-08-07) received 2026-11-11: fold-back mechanism for vertex pairs in a plus room; filed in `lit-tokarsky/`. No change to the open core.

### Decision 2026-11-12: fold-darkness minimum for all polygons

Daniel: "ok go, use codex astra to help you". This reopens general
rational polygons for one question: the fewest sides of a strictly simple
polygon made dark by folding (branched covers of doubled polygons;
Riemann-Hurwitz + Gauss-Bonnet). Started in `d32-fold-minimum/`: Astra
(GPT-6-Astra, read-only, theory: fold inequality, parity condition,
minimum, scope of Apisa-Wright) and an Opus literature check of
Apisa-Wright / Moeller / Wolecki at the source. A capped enumeration of
triangle and kite bases waits for Astra's framework.

d32 literature (Opus, 86k tokens; all four papers read at arXiv): the
middle-row claim holds with corrections. AW Thm 3.6: finitely blocked
x1, x2 on (X, w) are both M-periodic (or zeros) or have the same image
under the half-translation cover to Q_min. A dark polygon pair lifts to a
finitely blocked pair (Wolecki Lemma 2.1), so the classification applies
to non-torus-cover unfoldings. Periodic points are finite (Eskin-Filip-
Wright) but not classified in general (AW Problem 1.5). AW Thm 3.10: an
angle not a multiple of pi/2 gives finitely many finitely blocked pairs,
and its proof excludes option (a) except over points fixed by powers of
the rotation. Square-lattice rooms (rectangle-tiled or Gaussian) are torus
covers: no constraint. Wolecki gives finiteness only; the agent's own
reading supports the suspected Lemma 2.9 gap for orthogonal polygons
(rank 3 case).

d32 Astra round 1 (74k tokens): PROVED wall formula for any rational base:
n = 2 + d (k - 2) - sum over vertices with p_i = 1 of c_{i, q_i}
(regular points counted on the double); recovers the orthogonal formula.
Local fold-back works over any vertex of angle pi/(2h), not only right
angles. Triangle mechanism (f(S) = f(T) = A, midpoint fixed by the
half-turn) is a second fold mechanism. Covering identities alone can't
give a lower bound (two squares make a lit rectangle). Apisa-Wright gives
a necessary reduction, not a characterization, and gives no wall bound.
The concrete gap: non-clean (1,3,4) pi/8 rooms, reviewed bound only 16.
Astra: 40% that fold-darkness needs >= 22 sides and is provable.
Started: Astra round 2 (corner-charge bound for (1,3,4)) and
`d33-134-rooms/` (Opus; extend the d7 enumeration to k = 7, 8 at
W <= 21; 2 processes, 1 hour, 200 MB; approved enumeration).

d32 Astra round 2 (cumulative 177k tokens): (1,3,4) pi/8 bound raised
from 16 to W >= 17 (PROVED by Astra; unreviewed). Exact charge table;
16 distinct mandatory B corners; W = 16 impossible by 3F = 112. Two
17-wall profiles survive: 38 tiles (excluded by the reviewed k <= 6
search) and 40 tiles (k = 8). Concrete 40-tile candidate: half-octagon
with two reflected octagons attached across x = 1 and y = 1, pair at
their centres; Astra guesses lit. Correction to round 1: darkness doesn't
require every C preimage to be a corner. Extension: right triangles
(1, h-1, h) pi/(2h) need W >= 2N + 1: 25 for pi/12, 21 for pi/10.
So two weak spots remain below 22: (1,3,4) pi/8 (17..21) and
(1,4,5) pi/10 (W = 21). Candidate forwarded to the d33 enumeration.

d33-134-rooms (part 1, Opus, 88k tokens, 18 CPU min): no dark (1,3,4) pi/8
room with k <= 8 and W <= 21 (3,734 rooms with no shared C-tip; the rest
lit by Prop R2.1). Astra's 17-wall candidate is lit by a 2-reflection
path. Validation at k <= 6 matches d7-review exactly. Hardest: 40-tile,
21-wall rooms needing 13 to 14 reflections. Not covered: k >= 9. Asked
the agent to run (1,4,5) pi/10 at W = 21 in the remaining cap.

d33 part 2: (1,4,5) pi/10 has no dark room with W <= 21 and k <= 10.
Only two 21-wall rooms exist in that range (46 tiles, k = 6), both lit by
3-reflection paths. 3,513,725 rooms with no shared C-tip at k <= 10.
Validation at k <= 2 and k <= 6 consistent. Not covered: k >= 11. Total
29 CPU minutes, 172 KB, 2 processes.
Status of the general-polygon question: no fold-dark strictly simple
polygon below 22 walls known; the two weak right-triangle families are
clear to k = 8 (pi/8) and k = 10 (pi/10). Proved bounds there: 17 and 21.

Decision 2026-11-12 (Daniel: "ok go"): close (1,3,4) pi/8 at 22. Step 1: Astra round 3 (finiteness check, corner profiles W = 18..21, search plan). Search waits for profile counts.

d32 Astra round 3 (cumulative 315k tokens): finiteness CONFIRMED and
sharpened. Identity K + p + 3m + 12I + 6f = 2W - 4 forces I in {2,3},
f <= 2 at W <= 21. Max tiles F: 40, 42, 44, 48, 50 at W = 17..21 (extras
8, 10, 12, 16, 18). With d33 (k <= 8), W = 17 is closed. Profile counts
(arithmetic, two independent enumerations, no rooms): 10, 54, 240, 1,005,
3,324 at W = 17..21; with F > 40: 0, 27, 219, 975, 3,255. W = 18 has 3
families. Search plan: second star placed by reflection words of length
<= 19; exact Q(sqrt 2) coordinates; prune by completion profiles; don't
prune on intermediate walls. Naive size at 18 extras ~1e14 (extrapolated).

Decision 2026-11-12 (Daniel: "ok go stage 1"): `d34-134-stage1/` (Opus) - extend the (1,3,4) scan to k = 10 (closes W = 18) and k = 12 if it fits (W = 19); profile cross-check; 2 processes, 2 hours, 500 MB.

d34-134-stage1 (done 2026-11-12; Opus, 112k tokens, 16 CPU min, 61 MB):
W = 18 and W = 19 CLOSED for the (1,3,4) pi/8 triangle (no dark interior
A pair). With d33 (W = 17): no dark (1,3,4) room with W <= 19. Counts at
W = 18, 19 stop growing at k = 10, 12, as the ceilings predict; 2,015
rooms at W <= 19, every pair lit by an exact path (max 8 reflections).
New prune (B points + frozen A/C corners > W) matches unpruned runs
through k = 8. Profile cross-check: no violation in 97,984 rooms; the
ceilings F = 40, 42, 44 are attained. Projection: W = 20 (k <= 16)
0.5 to 1 CPU hour; W = 21 (k <= 18) 2 to 5 CPU hours enumeration plus 4
to 25 CPU hours of path search, needs streaming. Unreviewed: scan34.py.

Decision 2026-11-12 (Daniel: "let's do 3"): `d35-aw-torus/` - Astra (d32 session) on where the Apisa-Wright proof uses "not a torus cover" and whether a finite-action analogue survives at r <= 8. Tokarsky email: Daniel's call, not sent by us. Branch (1,3,4) W = 20, 21 parked.

Entries before 2026-11-21 are in [coordinator-log-archive-1.md](coordinator-log-archive-1.md).

## 2026-11-21 09:10 — ticks stalled overnight; thin-room.md (Q72)
- Cron 31c40a68 still registered, but no ticks fired between 19:04 (Nov 20) and 09:08 (Nov 21); the Mac stayed awake (caffeinate). Cause unknown (harness side). Astra idle ~14 h after delivering thin-room.md at 19:10.
- thin-room.md: all same-parity pairs lit in every cov279 stretch q = 12j+4; 84,950 certificates replayed. Claim d127; Opus referee with independent tracer launched. Brief: general thin-room theorem via band graph + absorption gcd; follow-on: fat regime by max band height.

## 2026-11-21 09:16 — band-absorption.md (Q73)
- Prescribed-route absorption false; exact absorption test + CRT placement; cov279 all pairs at q = 8, 10, 14, 20; odd crosses defeat band-height fat regime. Claim d128 (2 reviews running). Brief: dichotomy by local thickness τ (largest contained square); thin-regime theorem with free route/band/crossing choice; follow-on: fat regime via a τ₀ square.

## 2026-11-21 11:55 — network outage
- No ticks 09:16–11:54; d127 and d128 reviews both failed with ENOTFOUND (network). Network back; resumed both agents from transcripts. Astra resumed at 11:51 on the thin-regime (local thickness) brief.

## 2026-11-21 12:30 — d127 processed (Q72)
- Re-ran checks.py: SAME except wall time (54.6 s under load vs 1.7 s). thin-room.md sound; scope widens to all q ≥ 4 with 3 ∤ q; 3 | q open. Estimate 9–11% → 10–12% (first infinite W ≤ 20 open-core family closed for all lattice pairs; the 16-wall family that defeated every metric method).

## 2026-11-21 12:55 — d128 processed (Q73); Q74 queued
- band-absorption.md sound (low gaps). Absorption test and CRT placement are reviewed tools for the thin regime. resonant-cov279.md queued at P2 (case work). Astra redirected from cov279 case work to the general thin-regime theorem. Estimate unchanged 10–12%.

## 2026-11-21 21:00 — thin-gap-periods.md queued (Q75) and in review (d129)
- Astra's corner-intercept theorem: no thickness/reflex bound on the lighting direction's primitive component, so fixed-menu proofs of the thin theorem fail. Brief sent: bounded route complexity R(τ₀, r) with width-dependent slope; follow-on fat-regime access. Estimate unchanged 10–12%.

## 2026-11-21 21:10 — reflection-complexity.md queued (Q76), in review (d130)
- Astra: no reflection bound R(τ₀, r) (cov279 needs R+1 ≥ √q/12; st279 fat pairs need Ω(√m)). Brief sent: band-passage finiteness theorem K(r) plus reduction to finitely many Presburger-type statements; follow-on checkability. Two reviews running (d129, d130). Estimate unchanged 10–12%.

## 2026-11-21 21:30 — d129 processed (Q75 DONE)
- thin-gap-periods.md sound with gaps; main gap: menu exclusion proved only for τ₀ ≥ 5. Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-21 21:25 — passage-complexity.md queued (Q77), in review (d131)
- Astra: no band-passage bound K(6) (st279 end-square stretches). Route-length finiteness is ruled out at three levels (menu, reflections, passages). Brief sent: parametric definability of the dark relation (Presburger via a uniform interval-exchange / AHT acceleration); follow-on bound the formula or period sizes. Reviews running: d130, d131. Estimate unchanged 10–12%.

## 2026-11-21 21:40 — d130 processed (Q76 DONE)
- reflection-complexity.md sound with gaps (R undefined; actually refutes R(3,6); fat constant implicit). Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-21 21:55 — d131 processed (Q77 DONE)
- passage-complexity.md sound with gaps. Correction to the 21:25 entry: route-length finiteness is ruled out only for the fixed horizontal decomposition; vertical/mixed passages are open. Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-21 22:00 — parametric-orbits.md (Q78, P0) and primitive-dark-flats.md (Q79) in review (d132, d133)
- Astra's candidate finite-flat theorem: on each cell, darkness is a finite union of affine flats, so integral darkness is Presburger definable (existence only, non-effective). primitive-dark-flats reduces primitive normalization to a coefficient bound H. Astra is now on the height of a single axis factor's equations. Estimate unchanged 10–12% pending review.

## 2026-11-21 22:15 — d133 processed (Q79 DONE)
- primitive-dark-flats.md sound with gaps. Scope flag: the axis-stretching step fails for 45° walls, which the target includes; the axis-parallel program does not yet cover them. Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-21 22:20 — d132 processed (Q78 DONE)
- parametric-orbits.md: logic sound (o-minimal finiteness; Presburger without rational flats). HIGH gap: Filip 5.4 is for unmarked strata; the marked-point case is unsourced, and the d86/d116 reviews checked Filip from memory. Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-21 22:30 — three new notes: Q80 (d134), Q81 (d135), Q82 queued
- marked-algebraicity.md (cyclic triple cover makes marks zeros, Filip upstairs, finite descent) is in review as P0 because it closes the d132 HIGH gap. The 45° extension of the finite-flat theorem is in review as d135. reciprocal-resonance.md (conditional H, rank test) is queued. Brief sent: rigidity theorem (full gap rank on dark flats, via long-strip tools) with follow-on uniform resonance bound. Estimate unchanged 10–12%.

## 2026-11-21 22:40 — d134 processed (Q80 DONE)
- marked-algebraicity.md sound with medium gaps (algebraic morphisms only sketched; application overstated). Closes d132 gap 1. Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-21 22:50 — d135 processed (Q81 DONE)
- The 45° extension of the finite-flat theorem is sound with gaps, none high; the 45° scope flag from d133 is resolved for the finite-flat theorem (not for axis stretching). Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-21 23:05 — d136 processed (Q82 DONE); corner-orbit-rigidity.md queued (Q83, d137)
- reciprocal-resonance: algebra sound, but the rank test is unattainable (4 vs 38–40 identities), M is not uniform, and the census is about 10^(4.3e5) per cell, so the explicit-H census route is dead. New target for Astra: rigid dark rooms ⇒ area ≤ 20 (censused), non-rigid flats lit by long-strip tools. Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-21 23:30 — rigidity-area.md queued (Q84, d138)
- Correction to my 23:05 brief: d39's area-20 bound applies to essential-Rig certificates only, not to d137 rigidity, so the dichotomy plan's step (b) has no ready-made bound. Astra reduced it to a degree bound d ≤ 160 (area = cd/8) and is now trying to bound d using all-lift darkness. Estimate unchanged 10–12%.

## 2026-11-21 23:40 — Astra idle (since 22:28); briefed
- Brief: cylinder-avoidance theorem. All-lift darkness implies no target lift is interior to a source lift's marked cylinder in any rational direction; prove this bounds d ≤ f(g, n), and test it on the 22-wall dark room. Follow-on: explicit f against d ≤ 160/80. Reviews running: d137, d138. Estimate unchanged 10–12%.
- Sync note: coordinator-log.md passed the 200 KB rsync cap after Nov 20 15:30, so it stopped syncing. I split the entries before Nov 21 into coordinator-log-archive-1.md.

## 2026-11-21 23:55 — d137 processed (Q83 DONE)
- corner-orbit-rigidity.md: algebra sound on 4 named rooms; HIGH scope gap: rigidity is generic, including at lit seeds, so part (a) of the dichotomy carries no area content. Cylinder avoidance (current brief) is the remaining route. Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-22 00:00 — d138 processed (Q84 DONE)
- rigidity-area.md sound with gaps. The reviewer found a census coverage gap: canonical45 (d11) misses mixed rooms with different diagonal-intercept parities at every N (room M, area 27/2). Recorded in STATE.md. A census run to close it needs Daniel's approval. Re-run SAME. Estimate unchanged 10–12%.

## 2026-11-22 00:00 — d138 processed (Q84 DONE); d137 records repaired
- rigidity-area.md sound with gaps. The reviewer found a census coverage gap: canonical45 (d11) misses mixed rooms with different diagonal-intercept parities at every N (room M, area 27/2). Recorded in STATE.md. A census run to close it needs Daniel's approval. d138 re-run SAME; d137 re-run differed only in timings, and that timing diff had blocked its RESULTS, queue, STATE and board updates, which are written now. Estimate unchanged 10–12%.

## 2026-11-22 00:10 — diagonal-periods.md queued (Q85, d139)
- Mixed-parity diagonal rooms map to canonical45 by a 45° similarity that doubles area; d11 covers that class only through original area 8. Brief sent: general cylinder-avoidance bound via monodromy (separation in every direction ⇒ block structure or factorization ⇒ d ≤ f(g, n)), tested on R22; follow-on area bound against census coverage. Estimate unchanged 10–12%.

## 2026-11-22 00:20 — half-turn-fibers.md queued (Q86, d140)
- No general d ≤ f(g, n): half-turn symmetric square-tiled surfaces give dark pairs at unbounded degree with S_p monodromy. Brief sent: the 'darkness is symmetry' theorem (separation of complete physical lift orbits ⇒ a −I involution exchanging the orbits, with every fixed point forbidden); follow-on classify such rooms at W ≤ 20. Reviews running: d139, d140. Estimate unchanged 10–12%.

## 2026-11-22 00:35 — d139 processed (Q85 DONE)
- diagonal-periods.md sound with gaps, none high. The census residual for mixed-parity diagonal rooms at area ≤ 20 is A/B pairs at N = 34–80, plus A–B pairs at every N. That needs Daniel's approval. Estimate unchanged 10–12%.

## 2026-11-22 00:45 — free-half-turns.md queued (Q87, d141)
- On the full unfolding, the midpoint mechanism blocks at most 1 of 8 target lifts, so darkness must come from a quotient. Brief sent: quotient version (separation ⇒ blocks ⇒ intermediate Y with a −I involution and forbidden midpoints), tying in the old parity-factor program; follow-on list the possible quotients Y at W ≤ 20 against R22's staircase fold. Reviews running: d140, d141. Estimate unchanged 10–12%.

## 2026-11-22 00:55 — d140 processed (Q86 DONE)
- half-turn-fibers.md sound with gaps for abstract surfaces. The examples are not room unfoldings (2 marks fold to an interior non-corner point), so in rooms the mechanism needs a hidden symmetry, which is consistent with the quotient brief. Estimate unchanged 10–12%.

## 2026-11-22 01:00 — two-image-midpoints.md queued (Q88, d142)
- Astra closes the common-quotient midpoint route at W ≤ 20, pending review. Brief sent: torus-cover analogue of Apisa–Wright 3.6 (dark ⇒ per-class fold certificate at r ≤ 8); follow-on per-class certificates impossible at W ≤ 20 (extending d2), with R22 extremal. Reviews running: d141, d142. Estimate unchanged 10–12%.

## 2026-11-22 01:15 — d141 processed (Q87 DONE)
- free-half-turns.md sound with gaps on X. Quotients by hidden translations carry free half-turns (V-notch, octagon), which is directly relevant to d142's quotient claim; I forwarded this to the d142 reviewer and to Astra. Estimate unchanged 10–12%.

## 2026-11-22 01:25 — per-class-relay.md queued (Q89, d143)
- Two-site per-class blocking lemma, refining d142 for the V-notch and octagon quotients. Brief sent: reachability lemma (a regular fixed preimage over p is reachable ⇒ darkness forces two-site separation) plus R22's seam-reversal signature; follow-on: no per-class factor at W ≤ 20. Reviews running: d142, d143. Estimate unchanged 10–12%.

## 2026-11-22 01:35 — d142 processed (Q88 DONE)
- two-image-midpoints.md sound with gaps; the proof holds through W ≤ 23 and covers the d141 hidden-translation quotients. R22 is dark by a path-dependent 2-adic parity argument, so the midpoint route is closed and the 2-adic mechanism is what remains. Estimate unchanged 10–12%.

## 2026-11-22 01:45 — dyadic-classes.md queued (Q90, d144)
- Astra refuted my 'each 2-adic class is realized' lemma (cov4181, W = 20: only 1 of 3 classes realized). Brief sent: a wall-budget theorem (blocking all three primitive classes costs ≥ 22 walls net of overlap; R22 tight); follow-on check it on R22, the parity-W24 rooms, Castro's room and cov4181. Reviews running: d143, d144. Estimate unchanged 10–12%.

## 2026-11-22 01:55 — d144 processed (Q90 DONE)
- dyadic-classes.md sound, low gaps; cov4181 blocks 2 of 3 classes at W = 20 (independent full-orbit replay). Estimate unchanged 10–12%.

## 2026-11-22 02:05 — d143 processed (Q89 DONE)
- per-class-relay.md sound with gaps; one site per class suffices. It independently confirms that R22's darkness is not a midpoint phenomenon (also d142), so the wall-budget brief is the live route. Estimate unchanged 10–12%.

## 2026-11-22 02:15 — clean-site-cost.md queued (Q91, d145)
- R22's exact budget is 9 reflexes (one corner-only site plus 6 indispensable stops), W = 22. A corner-only site costs a full fiber. BBBB rooms have no corner-only fiber. Brief sent: structure theorem (every developed-path exclusion factors through a corner-only quotient ⇒ BBBB pairs lit), tested at once on cov4181 class (0,1); follow-on: the full reviewed chain W ≤ 20 ⇒ lit. Estimate unchanged 10–12%.

## 2026-11-22 02:30 — d145 processed (Q91 DONE)
- clean-site-cost.md sound with gaps (R22-specific; 6 routes certify only 4 of 12 residual cells). The open item is unchanged: the cost of an obstruction with no clean fiber and no corner-only factor. Estimate unchanged 10–12%.

- 2026-11-22: d146 exclusion-descent reviewed sound with gaps; checks re-run SAME. Medium gap: BBBB lemma needs universal B_x. Degree >= 5 open. Estimate 10-12% unchanged.

- 2026-11-22 00:40: Astra refuted my proposed per-pencil deletion-invariance theorem (DB55 counterexample, unreviewed). d148 review launched. New observation: 272/272 pairs lit in >=2 classes on 4 named rooms.
- 2026-11-22: d147 cross-factor-arcs sound with gaps; re-run SAME. Cross lit at all 2,346 interior pairs. Estimate 10-12% unchanged (named room, no general bound).
- 2026-11-22: d148 sound with gaps; re-run SAME. My deletion conjecture is refuted only in its pencil form; class form open. 272/272 pairs lit in all 3 classes. My q-parity brief predicted an odd number of failing classes, which the 0-failure data contradicts; corrected with Astra. Estimate 10-12%.
- 2026-11-22 02:50: Astra's local-global.md refutes my dyadic-sieve brief: DB55 (2,2)->(4,4) along (1,2j) is lit iff 5 does not divide j, so no per-direction 2-adic test exists. My claim that square-tiled Veech groups contain a level-N congruence subgroup was wrong (Schmithuesen, arXiv 0704.0416). Her positive result: one legal shot gives positive density in its affine orbit. Q97 queued; two reviewers (d149, d150) are still running.
- 2026-11-22 03:00: d149 cyclic-separation sound with gaps. The re-run's coverage depends on timing: 1,960 vs 720 slopes, the same conclusion (0 mixed cusps). Saved as checks.rerun.log. Q97 review launched as d151.
- 2026-11-22: d150 and d151 sound with gaps; both re-runs SAME (explicit diff check). Estimate 10-12% unchanged. Asked Daniel whether to approve a bounded BBBB census or reduce the tick cadence; awaiting an answer.
- 2026-11-22 03:05: My stretch-reduction brief repeated length-periodicity.md (d110, sound, tail only). I corrected it with Astra and redirected her to the open frontier: a uniform K(W) for arbitrary skeletons, via corridor induction.

- 2026-11-22 03:20: Astra's parity-shortening.md refutes my brief's two claims (unreviewed): shortening by 2 doesn't preserve the sheet permutations, and it can create a legal shot ((2,1) in the three-chamber room at 28 vs 26). Fourth wrong brief this stretch. d153 launched.
- 2026-11-22: d152 sound with gaps; re-run SAME. Uniform K is refuted at W=22 by R22's arm-length behavior. My brief's question (a) was answered by existing reviewed results (d114/d124) I should have cited.
- 2026-11-22: d153 sound with gaps; re-run SAME. My brief's two claims are confirmed false; darkness descent is open.
- 2026-11-22: d154 sound with gaps; re-run SAME. My wide-gap/census framing was wrong: known certificates are already excluded below 22 walls, so the finite set is empty, and the wide-gap theorem I briefed is itself certificate completeness. Corrected with Astra.
- 2026-11-22: d155 sound with gaps; re-run SAME. The 45-degree bound is correct but doesn't reduce the census gap. Completeness is still the open core.
- 2026-11-22 03:55: Astra's multitwist-first-shot.md refutes my multitwist brief (unreviewed): the dumbbell witness is outside the pencil, and no horizontal stabilizer map works. Fifth wrong brief this stretch. My d155 relay also misread (a+1,1) as a (kc,1)-type direction. d156 launched.
- 2026-11-22: d156 sound with gaps; re-run SAME. The vertical-seed multitwist method is dead; doorway visibility is the active route.
- 2026-11-22 04:20: Astra's simultaneous-door-fractions.md refutes my door-fraction brief (unreviewed): large denominators don't give simultaneous clearance, and R22's obstruction is a relation between visits, not a halfway door. Sixth wrong brief this stretch. From now on I'll brief from Astra's own stated next question, plus framing. d158 launched.
- 2026-11-22: d157 sound with gaps; re-run SAME. First reviewed constructive general lemma (two rectangles). Estimate 10-12%; the chain obligation is open.
- 2026-11-22: d158 sound with gaps; re-run SAME. Joint obstruction = time-reversal pairing of visits t <-> D-t.
- 2026-11-22 04:35: Astra's time-pairing.md refutes the t<->D-t characterization I forwarded from d158 (unreviewed). Positive: an exact joint-interval criterion per itinerary. d159 launched.
- 2026-11-22: d159 sound with gaps; re-run SAME. My brief called the joint-interval criterion 'the real gain'; it's unfolding legality restated. The Presburger route stands on the itinerary-length bound alone.
- 2026-11-22 04:55: Astra's skeleton-decidability.md refutes my Presburger brief (unreviewed): legality is bilinear in slope and length, and one-reflection lighting on a 6-wall L is zy<3x, which is quadratic. Again my framework brief was wrong. Going forward I'll endorse Astra's own next moves rather than propose frameworks. d160 launched.
- 2026-11-22: d160 sound with gaps; re-run SAME. The Presburger route is dead; d132's all-word definability is unaffected.

## 2026-11-22 d161 processed
Verdict sound with gaps (re-run SAME). Class collapses to 4/6/8/12-wall rooms; Astra's follow-on (induction by adding features) is the right next step. Forwarded.

## 2026-11-22 program change (Daniel approved)
Daniel approved all four changes: (1) wall-turn pattern ledger for W<=20 (combinatorial only; by-area room census still needs approval), (2) every brief ends with the smallest uncovered room, (3) attacker subagent per new class theorem, (4) milestone-only briefs and hourly ticks. See PROGRAM.md. d163 builds the ledger.

## 2026-11-22 d162 processed
Sound with gaps (re-run SAME). Key gap: DB55 is a two-sided stacked hall. Forwarded with M2 emphasis. Attacker d164 launched on the stacked-hall class.

## 2026-11-22 d163 processed
Ledger re-run SAME (json identical). Ledger reviewer d165 launched. Astra briefed on M3 target 1 (one-direction dents; merges with M2).

## 2026-11-22 d164 processed
Re-run SAME. Forwarded to Astra as input to M3 target 1.

## 2026-11-22 d165 processed
Re-run SAME. M1 complete. STATUS.md holds the live split. Forwarded the 296 no-hall words to Astra.

## 2026-11-22 08:00 idle gap
Astra sat idle from 06:03 to 07:57 UTC with three unreviewed notes; the hourly tick did not fire in that window. Switched to 20-minute ticks that check session state and the notes dir, not only ListSessionMessages. Milestone set: close W=10, then W=12.

## 2026-11-22 d167 processed
Re-run SAME. Forwarded to Astra.

## 2026-11-22 d166, d168 processed
d166 re-run differs only by the --extra supplement; d168 SAME. First W=10 word moves (provisional). d169 launched to review d15 Theorem 3 r=3 table, load-bearing for the W=10 milestone.

## 2026-11-22 d169 processed
Re-run SAME. Work list forwarded; Astra targets Ferrers' 1 pair (resonant lattice) then pyramid 7, 3-4 corners 21.

## 2026-11-22 d170 processed
Re-run SAME. Forwarded residual rooms to Astra.

## 2026-11-22 04:10 stalls
d171 and d172 reviewers stalled for ~1h before reading any file (no CPU, empty dirs). Stopped and resumed both. Astra shows running with no activity since 02:35 local; check again next tick and flag to Daniel if still silent.

## 2026-11-22 d172 processed
Re-run SAME. Two W=10 words move to PARTIAL. d171 still running (resumed).

## 2026-11-22 d171 processed
Re-run SAME. Ferrers not COVERED; residual named. Forwarded.

## 2026-11-22 direction change
Daniel approved: stop word-by-word; target a resonance theorem for band chains. Stopping rule by 2026-11-23. Astra briefed.

## 2026-11-22 d174 processed
Re-run SAME. Ferrers residual persists after nine tests; this is the resonance core the d173 line targets. Forwarded.

## 2026-11-22 d173 processed
Re-run SAME. R22 at rank-one equality is the first structural link between the lit tools and the dark room. Forwarded with per-gate windows + delta bound as the next step.

## 2026-11-22 refocus (Daniel: avoid busy work)
Added the L1-L4 proof architecture to PROGRAM.md. L1 (area bound / descent) is the open core. Reviews and briefs must name the lemma they advance; single-room certificates and per-word bookkeeping stop.
- 2026-11-22 17:15 Processed d175 (re-run SAME). Read winding-assessment, l1-primitive-subset-action (Advances L1), certificate-local-data (certificate design limit). Stopping rule applied: no word-independent L1 argument from winding; estimate lowered to 7-9%. Launched d176.
- 2026-11-22 16:20 Processed d176 (re-run SAME). L1 branch moved. Forwarded to Astra.
- 2026-11-22 16:32 Astra notes l1-natural-four-sites (L1, negative: algebra alone can't close the natural branch) and l1-natural-marked-poles (L1, pole criterion). Launched d178.
- 2026-11-22 16:50 Processed d177 (spot re-run 1-244 SAME). Resumed agent on 2-300 with a larger piece cap.
- 2026-11-22 16:58 Processed d178 (re-run SAME). Forwarded to Astra.
- 2026-11-22 16:50 Astra note l1-swap-pole-averaging (L1: averaging fails at marked starts; straightening lemma). Launched d179.
- 2026-11-22 17:20 Processed d177 follow-up (spot re-run SAME). No wrong claim.
- 2026-11-22 17:00 Processed d179 (re-run SAME). Forwarded to Astra.
- 2026-11-22 19:06 Ticks missed 17:00-19:05; Astra idle ~2h. Two L1 notes (cylinders, cusp frequency). Launched d180. Redirected Astra from obstruction-mapping to a positive area-bound attempt on Q.
- 2026-11-22 19:12 Astra l1-four-band-directions (L1, negative): adjacent-cylinder failure in four directions is compatible with unbounded prime area and full illumination (stretched DB55, lit by d112 L>4d). Logged, not reviewed: counterexample family is covered by a reviewed theorem. Briefed: generalize d112 to general end chambers.
- 2026-11-22 19:20 Processed d180 (re-run SAME). Forwarded to Astra.
- 2026-11-22 19:21 Astra: two positive L1 gluing lemmas (open collar, remote-wall return); also reports W<=20 does not force scale separation (odd crosses, DB55 top-line stretch). Launched d181.
- 2026-11-22 19:35 Processed d181 (re-run SAME). Forwarded to Astra.
- 2026-11-22 19:33 Astra l1-growth-modes (L1): growth classification + ray transfer theorem (contrapositive: eventual darkness along a ray descends to every base). Launched d182.
- 2026-11-22 19:50 Processed d182 (re-run SAME). Estimate 7-9% -> 8-10%. Forwarded to Astra.
- 2026-11-22 19:52 Astra: l1-dbas55-top-phase (L1, closes d181's first no-corridor case) and l1-gap-hyperplanes (L1, effective descent). Launched d183, d184.
- 2026-11-22 20:08 Processed d183 (re-run SAME). Forwarded to Astra.
- 2026-11-22 20:25 Processed d184 (re-run SAME). Estimate +1. d182 review offset sentence corrected. Forwarded.
- 2026-11-22 20:12 Astra l1-db55-odd-lengths (L1 row-1 family extension). Launched d185 (P2). Astra already briefed on row 4.
- 2026-11-22 20:25 Processed d185 (re-run SAME). Forwarded. Not redirecting Astra to DB55 even lengths: single-family closing; row 4 is the structural gap.
- 2026-11-22 20:32 Astra row-4 notes (crossing-gap transfer, cross-cap budget). Launched d186. Briefed: assemble full descent to bounded gaps G(chart).
- 2026-11-22 20:50 Processed d186 (re-run SAME). Forwarded.
- 2026-11-22 20:53 Astra: l1-chart-descent + l1-seed-normal-bound (L1 assembly). Launched d187. Briefed mixed-seed (u, 1/u) equidistribution idea for doubly proper products.
- 2026-11-22 21:08 Processed d187 (re-run SAME). Estimate +2: L1 now a precise two-input reduction. Forwarded.
- 2026-11-22 21:12 Network down: GitHub push and Slack post failed. Unpushed: 7a8c9f6. Pending Slack: estimate 11-13% + d187 reduction. Retry next tick.
- 2026-11-22 21:14 Network recovered, pushed 5a262df, Slack posted. Astra l1-mixed-seed-normals (L1 H(C)): mixed seed bounds one axis equation; occupied crossing breaks fixed period. Launched d188.
- 2026-11-22 21:30 Processed d188 (re-run SAME). Forwarded. Push verification added to tick routine.
- 2026-11-22 21:34 — New Astra note l1-crossing-gate-resultants.md (L1, occupied-crossing route switching) → d189 Opus review launched, claimed. Astra briefed: scale-separated upper approach (remove given first-hit interval hypothesis). Estimate 11–13% unchanged.
- 2026-11-22 21:45 — d189 done: PASS WITH CORRECTIONS (134 checks re-run, 0 fail). Claim released, verdict forwarded. Estimate 11–13% unchanged.
- 2026-11-22 21:54 — New Astra note l1-crossing-scale-step.md (L1: bound on a/gcd(a,2d); uniform first-hit interval impossible) → d190 Opus review launched, claimed. Astra briefed: unbounded a/gcd(a,2d) case via lower side-wall period. Estimate 11–13% unchanged.
- 2026-11-22 22:05 — d190 done: PASS WITH CORRECTIONS (48 checks re-run, 0 fail). Claim released. Corrected my 21:54 brief: the open case is bounded a/gcd(a,2d) (fixed ratio), not unbounded. Estimate 11–13%.
- 2026-11-22 22:18 — New Astra notes l1-fixed-ratio-corner.md (L1: fixed-ratio tail, closes d190 open case if sound) and l1-lower-period-coupling.md (L1: ratio locking) → joint d191 Opus review launched, claimed. scale-step v2 snapshotted for correction check. Astra briefed: two-gate itinerary sensing D and u separately (locked D/u, drifting aperture). Estimate 11–13% pending d191.
- 2026-11-22 22:35 — d191 done: both notes PASS WITH CORRECTIONS (38 checks re-run, 0 fail). Claim released, verdict forwarded. Estimate 11–13%.
- 2026-11-22 22:54 — New Astra note l1-shallow-roof-return.md (L1: h/t>H* lights every source depth; covers d191 open case a=1, d→∞) → d192 Opus review launched, claimed. Corrections folded into corner/coupling/scale-step. Astra briefed: comparable dimensions as one d182 chart with growth ray (u,t). Estimate 11–13% pending d192.
- 2026-11-22 23:05 — d192 done: PASS WITH CORRECTIONS (23 checks re-run, 0 fail). d189–d192 together close the fixed-template occupied crossing (finitely many dark placements). Claim released, verdict forwarded, Slack posted. Estimate 11–13%.
- 2026-11-22 23:15 — New Astra notes l1-overlap-phase.md, l1-projective-crossing.md, l1-comparable-width-bound.md (L1: comparable-scale crossing; explicit area bound in anchored-template class) → joint d193 Opus review launched, claimed. d192 corrections folded in. Astra briefed: transverse-approach dichotomy, induct on vertical components. Estimate 11–13% pending d193.
- 2026-11-22 23:30 — d193 done: 3 notes PASS WITH CORRECTIONS (34 checks re-run, 0 fail). Claim released, verdict forwarded. Estimate 11–13%.
- 2026-11-22 23:38 — New Astra note l1-grounded-component-transfer.md (L1: first entry, inside-column source bound when opposite side solid or H≥b; d193 corrections folded) → d194 Opus review launched, claimed. Astra briefed: H<b two-component return via d192 mechanism. Estimate 11–13% pending d194.
- 2026-11-22 23:41 — Publish push failed (exit 128, transient); manual retry pushed cb0f22e4f, HEAD = origin/main. Note: manifests/files.jsonl is 60.7 MB (GitHub warns above 50 MB, hard limit 100 MB); it was already 62.5 MB before today's syncs.
- 2026-11-23 00:56 — d194 reviewer stalled (output dir empty 75 min, no python); stopped and resumed. Astra running (no new note in 25 min). Estimate 11–13%.
- 2026-11-23 01:22 — d194 resume made no progress (transcript unchanged since 00:55); stopped and relaunched fresh with write-early brief. Astra running ~58 min since brief with no visible output; check next tick, flag as stuck if unchanged. Estimate 11–13%.
- 2026-11-23 05:23 — Sync at 02:41 hung on push under load (~14), but 7660b8862 is on origin/main. Astra ran ~5h on one brief with no note: told her to write the partial result to l1-two-component-return.md and end her turn. d194 v2 stalled after a skeleton review.md; stopped and resumed. Slack posted (Astra stuck). Estimate 11–13%.
- 2026-11-23 05:38 — d194 done: PASS WITH CORRECTIONS (12 checks re-run, 0 fail). Claim released, verdict forwarded. Estimate 11–13%.
- 2026-11-23 06:18 — Astra wrote partial l1-two-component-return.md (L1 conditional strip return + limit of method) → d195 Opus review launched, claimed, with a convergence question. Crossing chain d189–d195 is fragmenting into subcases; Astra redirected to a word-independent crossing reduction theorem (chart → d184 / bounded crossing / explicit residual set R) with a decreasing invariant. Estimate 11–13%.
- 2026-11-23 07:05 — d195 done: PASS WITH CORRECTIONS (8 checks re-run, 0 fail). Reviewer independently confirms the fragmentation; matches the 06:18 redirect. Claim released, verdict forwarded.
- 2026-11-23 07:12 — Push failed again (exit 128); manual retry pushed d5935ffd5 (= origin/main). Added one automatic push retry to publish-illumination.py.
- 2026-11-23 07:25 — Two sync runs failed on git fetch (exit 128, intermittent; manual fetch fine). publish-illumination.py now retries fetch/push once after 15s and prints git's stderr on final failure. Pushed 335e476b4. Astra running on crossing reduction theorem.
- 2026-11-23 07:25 — Daily audit done (audits/2026-11-23.md). Applied its change: dated stopping rule for the chart-descent route in PROGRAM.md (N0 for LLLRLLLRLR by 2026-11-24 20:00, else stop the crossing chain). Resonance stopping rule fired: estimate 11–13% → 9–11%. Briefed Astra, Slack posted.
- 2026-11-23 07:58 — Astra in a compaction loop: since 17:00Z she has re-run near-identical head/ls/rg reads of chart-descent, grounded-component and board ~30 times without writing. The session is 20,600 events old (since 11-09). Reported to Daniel; recommended a fresh session with a compact handoff.
- 2026-11-23 08:15 — GitHub unreachable (port 443, 75 s timeouts); 1 commit pending locally. publish-illumination.py now pushes a pending commit when there's nothing new to copy, and no longer refuses to run when ahead of origin. Astra idle after the compaction loop, with no note. Waiting for Daniel's yes on a fresh session. Slack posted.
- 2026-11-23 08:40 — Daniel closed the old Astra session (e380bb94) and started a new one: 49fa6670-83db-4258-af09-a722a6cb0e5f. Sent a compact handoff brief (PROGRAM, d182–d195 one-liners, crossing reduction theorem, N0 stopping rule). Tick cron now targets the new session and detects compaction loops.
- 2026-11-23 08:45 — New Astra finished in 4 min: l1-crossing-reduction.md. Stopping test: NO numerical N0 for LLLRLLLRLR (d187 sharpens to 16·G(C)², G(C) unbounded). Per PROGRAM the crossing chain stops; Astra proposes a new route (small actual-area witness per dark chart family). d196 review launched, claimed. Reported to Daniel.
- 2026-11-23 08:55 — d196 done: PASS WITH CORRECTIONS (27 checks re-run, 0 fail). No N0, so the crossing chain stops. Estimate 9–11% → 8–10%. Claim released. Astra asked for a 1-page route proposal (shrink descent) while Daniel decides. Slack posted.

## 2026-11-23 08:50 — shrink-descent proposal received
- Astra wrote bbbb/l1-route-shrink-descent.md, a 1-page L1 route proposal. It isn't a lemma result, so it gets no review subagent.
- The conjecture: every dark room with W ≤ 20 and area > 20 has a 1- or 2-unit gap shrink that keeps the room normalized, strictly simple and dark. The area loss is the invariant.
- First test: the primitive rank-one factor (n,n+1,n+2,n+3) in LLLRLLLRLR. Stop by 2026-11-25 20:00.
- Daniel's route decision is pending. Astra started the first test provisionally (symbolic only, no searches) so she isn't idle.

## 2026-11-23 — Daniel approved the shrink-descent route
- Daniel answered "yes": the shrink-descent route (bbbb/l1-route-shrink-descent.md) is the selected L1 route. Its stopping rule is 2026-11-25 20:00 HST.

## 2026-11-23 09:12 — primitive shrink test received
- bbbb/l1-shrink-primitive-test.md (L1). Moves exist. The same-product fallback is blocked. Terminal-rectangle transfer works iff s·r ∈ hZ. A parity obstruction (4 | h, odd mark difference) blocks same-exit transfer. The implication from all shrinks being lit remains open.
- Launched an Opus review, d197-review-shrinkprimitive, and claimed it on the board.
- Briefed Astra on forward darkness transfer: P dark ⇒ some shrink dark. Output goes to bbbb/l1-shrink-dark-transfer.md.
- Sync pushed f6295d75a.

## 2026-11-23 09:15 — dark-transfer note received
- bbbb/l1-shrink-dark-transfer.md (L1). Forward darkness transfer fails locally: one cap excursion already moves the exit phase. Exact one-visit gluing criterion: (A_d + 2dr) ∩ B_T ≠ ∅. Added it to the d197 review scope instead of launching a second subagent.
- Briefed Astra on exterior induction: with the mouth closed, the exterior is a room with fewer walls. Output goes to bbbb/l1-shrink-exterior-induction.md.

## 2026-11-23 09:25 — d197 verdict
- CORRECT WITH MINOR GAPS for both notes. Re-ran checks.py: 28 PASS, 0 FAIL. It needs sympy, so I ran it under `uv run --with sympy`.
- It's an L1 method limit, and the estimate stays at 8–10%. RESULTS §11 and STATE are updated, and the claim is released. The verdict went to Astra, with the reviewer's stop condition: a slope-denominator bound counts as an early stop.

## 2026-11-23 09:32 — exterior-induction note received
- bbbb/l1-shrink-exterior-induction.md (L1, method limit). Closing the cap gives an 8-wall exterior. A lit family breaks the fixed-slope one-visit implication. The number of cap visits needed at a fixed slope is unbounded (q = 2mL), so finite-return induction needs a denominator bound. Astra stopped at that bound, per the d197 stop condition.
- Launched Opus review d198-review-exterior and claimed it on the board. Next brief: one cap-avoidance test, per the d197 reviewer.
- Sync pushed b6eb50c22.

## 2026-11-23 09:40 — d198 verdict; shrink route stopped
- d198 CORRECT WITH MINOR GAPS. Re-ran checks.py: 25 PASS. The reviewer recommends stopping the route, and its early-stop clause applies. The claim is released.
- Astra's last allowed test, bbbb/l1-shrink-cap-avoidance.md, is logged without review. It's partial (adjacent columns only), and the route is stopped. Her route-limits summary is in bbbb/l1-shrink-route-limits.md.
- Estimate 8–10% → 7–9%: the second L1 descent route failed its first test. Reported to Daniel on Slack. Astra is drafting a 1-page proposal for a new route, with no long proof until Daniel picks.

## 2026-11-23 09:50 — new route proposal
- bbbb/l1-route-next.md proposes shear-orbit counting: sum over the SL2(Z) shear orbit of the decorated 4-copy unfolding, and prove Σ C > Σ B. Proposed stopping rule: 2026-11-26 20:00. Sent to Daniel for a decision; no review subagent.
- Coordinator concern: dark 22-wall rooms must violate the inequality, so it has to be sharp at 8 versus 9 reflex corners. Asked Astra for a 1-page sharpness check (bbbb/l1-route-next-sharpness.md) before Daniel decides.
- Sync pushed c170957d3.

## 2026-11-23 10:07 — sharpness check
- bbbb/l1-route-next-sharpness.md: Astra found no mechanism separating 8 reflex corners from 9. The corner budget enters only as the number of blocker terms, not their sizes. Added as objection 3 in l1-route-next.md. Astra has been idle since 09:50, waiting on Daniel's route decision.

## 2026-11-23 10:09 — idle brief
- Astra was idle, and the counting route is on hold for Daniel. Briefed a 1-page dark-structure route proposal (bbbb/l1-route-dark-structure.md): darkness forces a structure that needs ≥ 9 reflex corners. It starts from d154. No proof before Daniel decides.

## 2026-11-23 10:30 — dark-structure proposal
- bbbb/l1-route-dark-structure.md proposes that a dark pair forces Q → B to factor through N with degree ≥ 3 and three 3π points, so r ≥ 3d ≥ 9. It's the first proposal with a sharp 8-versus-9 mechanism, and it starts from d154's R22 factor. The open part is the converse, darkness ⇒ invariant block partition.
- Recommended it to Daniel. Astra started the first test provisionally (d152 family X = Y = 3k+1, k ≥ 6); output goes to bbbb/l1-dark-structure-test.md.
- Sync pushed 711a8e3e7.

## 2026-11-23 10:40 — dark-structure test; route approval
- bbbb/l1-dark-structure-test.md stopped early. Sheet count N = 29+6k, and block size d ≤ 8 gives d ∈ {5,7}. Monodromy is primitive for k = 35j without any darkness hypothesis. No property of darkness forces a block. Launched Opus review d199-review-darkstructure and claimed it on the board.
- Daniel asked why routes needed his approval. They don't: the stopping rule only required reporting the route. Route choices now proceed without approval. Astra is briefed on the primitive subfamily k = 35j (prove all pairs lit); output goes to bbbb/l1-primitive-family-lit.md, stopping 2026-11-26 20:00.

## 2026-11-23 10:45 — d199 verdict; dark-structure route stopped
- d199 CORRECT WITH GAPS. Re-ran checks.py: all pass. The route restates the goal at W ≤ 20 and is stopped early. The claim is released and the verdict sent to Astra.
- New route (coordinator's choice under the new rule): lighting tail on the three-chamber family, uniform in k, starting from the reversal problem. Stopping 2026-11-26 20:00. Estimate unchanged at 7–9%.

## 2026-11-23 10:50 — three-chamber family lit (claimed)
- bbbb/l1-three-chamber-lit.md (L1, lighting tail). Claims every interior lattice pair is lit in d152's three-chamber family, for all k ≥ 6. The equal-offset outer pair needs two reversals, through an upper-pocket excursion of slope 1/(D−1/2). The note uses no W ≤ 20 inequality. Launched Opus review d200-review-threechamber and claimed it on the board.
- Briefed Astra on a general pocket lemma, with unequal corridor lengths as the first test.

## 2026-11-23 11:00 — d200 verdict: three-chamber family lit
- CORRECT. Re-ran checks.py: 0 failures. RESULTS §11 and STATE are updated, the claim is released, and the verdict is sent to Astra. The L1 lighting tail moved, so I posted to Slack. Estimate unchanged.

## 2026-11-23 11:04 — pocket lemma
- bbbb/l1-pocket-lemma.md (L1, lighting tail). Claims:
  - a pocket return map, with an exact matching criterion (congruence plus interval);
  - every aligned three-chamber room of 3×3 chambers with unit corridors and any lengths D₁, D₂ ≥ 4 is fully lit;
  - an R22 control: the dark base room has no full integral pocket.
- Launched Opus review d201-review-pocket and claimed it on the board. Briefed Astra on displaced apertures and general chamber sizes.

## 2026-11-23 11:08 — pocket-general note
- bbbb/l1-pocket-general.md (L1): the ledger-word dictionary F L^j F L^(4−j), and a sufficient condition for displaced apertures. The opposite-side word isn't certified; the residual is disjoint unit mouths with long necks. Added to the d201 review scope.
- Briefed Astra on a neck phase map (bouncing legs) combined with the pocket return. Output goes to bbbb/l1-neck-phase.md.

## 2026-11-23 11:15 — d201 verdict
- CORRECT. Re-ran checks.py and checks2.py: 0 failures. Ledger STATUS.md updated: 6/274/4,294, d152 word PARTIAL. This corrects my d200 note, which called the word already PARTIAL. Its ledger status was OPEN.
- Estimate 7–9% → 8–10%. Claim released, verdict sent to Astra, Slack posted.

## 2026-11-23 11:20 — neck-phase note
- bbbb/l1-neck-phase.md (L1). Coupled neck and pocket phase tests for displaced mouths. Claims all lengths are lit in the aligned 3×4 middle-chamber family, plus a gcd sufficient condition for arbitrary chamber heights. Launched Opus review d202-review-neckphase and claimed it on the board.
- Briefed Astra toward a general (w, h) theorem, not case-by-case chambers.

## 2026-11-23 11:35 — d202 verdict
- CORRECT WITH GAPS. Re-ran checks.py: 0 failures. The status claim "first open area 32" was wrong (it's 21), and I repeated it from d201 in my report and Slack. Fixed in RESULTS. Claim released, verdict sent to Astra.

## 2026-11-23 11:50 — chamber-general note
- bbbb/l1-chamber-general.md (L1). A group-ring arithmetic test for prescribed strip transits, exact for its constructions. Dimension-only lighting under gcd(P, lcm(w)) = 1. Width-2 and width-1 tests. The aligned layout isn't closed. Ledger follow-on: two OPEN two-neck words. Launched Opus review d203-review-chambergeneral and claimed it on the board.
- Briefed Astra on two-pocket coverage of the complement, with a follow-on long-neck lemma for general W ≤ 20 rooms.

## 2026-11-23 11:58 — busy-work check (Daniel's reminder)
- Assessment: the aligned three-chamber work (d200–d203) had drifted into per-word closing. That's four notes on one ledger word, which PROGRAM classes as busy work beyond the first reusable mechanism (the pocket lemma).
- Stopped the two-pocket task. Astra's main task is now the long-neck lemma for general W ≤ 20 rooms, which is L1's "large ⇒ lit" form. It must locate the 8-versus-9 step or stop. d203 finishes as the last review on this word; no more per-word reviews.

## 2026-11-23 12:08 — long-neck lemma stopped
- bbbb/l1-long-neck.md: there's no absolute C. Pocket absence doesn't separate R22 (6-reflex counterexample), and dilation makes the unnormalized statement equivalent to the full goal. The early-stop clause applies. Not reviewed: it's a stop note, and its counterexample is explicit and simple.
- Estimate 8–10% → 6–8%. Asked Daniel the strategy question. Astra is held until he answers, rather than given another local route.

## 2026-11-23 12:10 — route switch
- Daniel asked whether L1 is the only path. I recommended per-pattern decidability (d159's Presburger idea) plus a bounded census extension; both computations need his approval. Switched Astra to the path-length theorem (theory only). Output goes to bbbb/decide-path-bound.md. Recorded in PROGRAM.md.
- d203 is still running: checks are done, review.md not yet filled in.

## 2026-11-23 12:32 — path-bound note
- bbbb/decide-path-bound.md. Claims:
  - the Presburger reduction fails even with a linear bound: the zero-reflection predicate on the one-neck word defines u > m(m+1);
  - a finite (huge) witness bound for all rooms via the SL2(Z) orbit;
  - a linear witness on the quadratic family.
- This undercuts the premise of the route I recommended to Daniel. Launched Opus review d204-review-pathbound and claimed it on the board. Asked Astra for a 1-page assessment of whether any decidable encoding exists.

## 2026-11-23 12:45 — d204 verdict
- CORRECT WITH GAPS. Re-ran checks.py. The Presburger premise I recommended to Daniel is false; PROGRAM.md is corrected. The claim is released, the verdict is forwarded to Astra, and Slack is posted (wrong claim).
- 12:50 bbbb/decide-encoding.md: no uniform decision procedure. The surviving route is a per-word least-dark-area bound, which is L1 per word. Briefed Astra on a one-neck word COVER test (stopping 2026-11-25 20:00) to see whether the lighting-tail tools scale.

## 2026-11-23 12:55 — one-neck cover test
- Stopped at the first uncovered region (u=6, v=12, L=6, deep unequal marks). The tools don't scale to whole words. Estimate 6–8% → 5–7%. Astra is briefed on a design-only census-extension plan (bbbb/census-extension-plan.md); nothing runs without Daniel's approval.
- d203 has been running ~1 hour; told it to wrap up.
- 13:00 d203 verdict recorded, CORRECT WITH GAPS. Not re-run by the coordinator because the reviewer's final run of its 42 KB script is still going. Claim released. Not forwarded as a task, since that line is stopped.
- 13:10 d203 final run: all checks pass (269 CPU-s). RESULTS updated.

## 2026-11-23 13:10 — area-21 census approved
- Daniel: "yes go, don't always wait for me." Approved the area-21 census slice and the parity-coverage audit. Astra is implementing it in d205-census-a21 (validate, then run in the background, ≤ 8 processes). Recorded in PROGRAM.md.
- 13:12 Parity audit: L2 gap at areas 17–20 (different-parity pairs untested). PROGRAM L2 line corrected. Gap fill added to d205, ordered before area 21, under Daniel's census approval. Slack posted (wrong claim).
- 13:32 d205 done: area 21 + 17–20 parity backfill all lit (author). d206 review claimed and launched. Astra briefed: L1 BBBB area bound via d68 counting identity, write bbbb/l1-bbbb-area-bound.md. Area 22 awaits Daniel.
- 13:45 d206 verdict CORRECT WITH GAPS; re-ran checks (note: replay.py needs witness args). RESULTS §11 + PROGRAM L2 updated. Claim released. Verdict forwarded to Astra. Estimate 6–8%.
- 13:52 Astra note l1-bbbb-area-bound (L1, partial). d207 review claimed/launched. Astra briefed on condition (i) low range.
- 14:00 d207 verdict recorded, checks re-run, claim released, forwarded to Astra.
- 14:00 d208 claimed/launched; charge route logged stopped; Astra briefed on direction density.
- 14:03 direction-density stopped; Astra on CC seed lemma.
- 14:10 d208 recorded, checks re-run, claim released, forwarded.
- 14:12 CC stopped; seed-profile route selected (PROGRAM.md); Astra briefed; Slack posted.
- 15:31 seed profile logged; Astra on width-w insertion.
- 15:52 d209 claimed/launched; Astra on re-aim threshold.
- 16:05 d209 recorded, checks re-run, claim released, forwarded.
- 16:10 d210 claimed/launched; Astra on general collar, then seed-denominator bound.
- 16:25 d210 recorded, checks re-run, claim released, forwarded, Slack posted. Estimate 7–9%.
- 16:32 d211 claimed/launched; Astra on descent skeleton.
- 16:50 d211 recorded, checks re-run, claim released, forwarded.

## 2026-11-23 16:55
- Read bbbb/l1-descent-skeleton.md (L1). It claims a parallel retained transfer for k≥1, which extends d210. Marked descent: transfer + marked band selection + census through 121 imply L1. Axis-gcd scaling and a perturbation-neighborhood lemma. Staircase example: coarse estimate fails.
- Launched d212-review-descent-skeleton (Opus, named rooms only, 10 CPU-min); board claim added.
- Briefed Astra: marked band selection lemma (routes a–c), bbbb/l1-marked-selection.md.
- Estimate 7–9% unchanged pending d212.

## 2026-11-23 17:10
- d212 verdict CORRECT WITH GAPS. Re-ran checks.py: 54 PASS, 0 fail, 9.4 CPU-s, identical to the agent's log. RESULTS §11 updated; claim released; verdict forwarded to Astra.
- Estimate 7–9% → 8–10%: L1 now has a reviewed, complete conditional reduction with one named open lemma (marked selection). The census through 121 is a dependency only; any run beyond area 21 needs Daniel's approval.

## 2026-11-23 17:32
- New Astra note bbbb/l1-marked-selection.md (L1). It proves marked selection for exact-replay, U=1 and determinant-test classes, plus a mod-42 non-replay class on the offset √2 staircase. It shows that an arbitrary successful first lift can fail. It names the offset staircase as the open selection test.
- Launched d213-review-marked-selection (Opus, named rooms only, 10 CPU-min); claim added.
- Briefed Astra: bbbb/l1-selection-obstruction.md. Decide whether single-band selection fails on the √2 staircase; if so, use a multi-band lift lemma via perturbation in ratio coordinates; degenerate ratios next.
- Estimate 8–10% unchanged pending d213.

## 2026-11-23 17:45
- Daniel approved the recommendation (17:45): drop the pending area-22 census. Next, a theorem that pins down the base the descent needs; a scoped base computation will go to Daniel for approval with a cost estimate. No search is approved.

## 2026-11-23 17:55
- d213 verdict CORRECT WITH GAPS. Re-ran checks.py: 33 PASS, 0 fail, identical to the agent's log except for CPU time. RESULTS §11 updated; claim released; verdict forwarded to Astra.
- Key data: single-band gate selection passes for only 65/200 values of t on the √2 staircase. This supports the multi-band lift redirect. First open case: t=15. Estimate unchanged at 8–10%: the result is partial, with a concrete obstruction.

## 2026-11-23 17:55 (tick)
- Astra idle. New note bbbb/l1-selection-obstruction.md (L1). It resolves the t=15 case by a simultaneous direct-chord lift and adds a convex-cone ratio region, a multi-band lemma, one vanishing scale and a two-scale theorem. It also defines the exact finite base F. F's bound is 8.7e17, an upper bound only, not computable as proposed. The reduction is corrected: selection is also needed at reducible areas 22–121. l1-marked-selection.md was edited with the d213 corrections.
- Launched d214-review-simultaneous-lift (Opus, named rooms, 10 CPU-min, no F enumeration); claim added.
- Briefed Astra: bbbb/l1-ratio-compactness.md. Chart-wise compactness over ratio space using LMW/Wolecki finiteness; faces by induction on codimension; staircase chart as the test case.
- Note: the tick text's LLLRLLLRLR stopping rule is stale. PROGRAM's current rules are the shrink-descent rule (2026-11-25) and insertion descent (2026-11-26 20:00).

## 2026-11-23 18:05
- d214 verdict CORRECT WITH GAPS. Re-ran checks.py: 30 PASS, identical. RESULTS §11 updated; claim released; verdict forwarded to Astra. The finite base F is far too large to compute (8.7e17 upper bound); the lift hypothesis is the whole open step. Estimate unchanged at 8–10%.

## 2026-11-23 18:12 (tick)
- Astra idle. New note bbbb/l1-ratio-compactness.md (L1). It states chart-wise compactness, the face induction by codimension and an explicit effective radius. It covers the whole ratio triangle for one staircase pair, and adds an open certificate for a nondirect pair at (15,21) and the √2 face. Key admission: the interior exceptional specified pair is the real gap.
- Launched d215-review-ratio-compactness (Opus, named staircase only, 10 CPU-min); claim added.
- Briefed Astra: bbbb/l1-periodic-obstruction.md. Dark lattice pairs as periodic-point/symmetry coincidences (HST, Apisa–Wright, Tokarsky), plus a reflex-count lemma aiming at r ≥ 9; test against the 22-wall dark room.

## 2026-11-23 18:25
- d215 verdict CORRECT WITH GAPS. Re-ran checks.py: 22 PASS, identical. RESULTS §11 updated; claim released; verdict forwarded. The core is now the exceptional pinned pair, which Astra's periodic-obstruction brief targets. Estimate unchanged at 8–10%.

## 2026-11-23 18:33 (tick)
- Astra idle. New note bbbb/l1-periodic-obstruction.md (L1). Lattice marks are always periodic, so periodicity and symmetry cost zero reflexes. Count r ≥ kz for a pillowcase factor; R22 accounts for k=z=3. Pinned eight-reflex controls show that symmetry and periodicity don't decide darkness.
- Launched d216-review-periodic-obstruction (Opus, named rooms, 10 CPU-min); claim added.
- Briefed Astra: bbbb/l1-dark-implies-fold.md. Converse via Lemma FC: darkness gives a block system, hence a factor, hence r ≥ kz; check on R22 and P6.

## 2026-11-23 18:45
- d216 verdict CORRECT WITH GAPS (scoping). Re-ran checks.py: 37 PASS, identical. RESULTS §11 updated; claim released; verdict forwarded. Both pinned controls are lit. Estimate unchanged at 8–10%.

## 2026-11-23 18:55 (tick)
- Astra idle. New note bbbb/l1-dark-implies-fold.md (L1). R34 (degree 19, prime) refutes fold-only necessity. Corner-only off-classes force r ≥ 9 (local count). A midpoint witness ⇔ a single-state walk of length 2 mod 4. Hand check on R22/P6 gives kz = r.
- Launched d217-review-dark-implies-fold (Opus, R22/P6/R34 only, 10 CPU-min); claim added.
- Briefed Astra: bbbb/l1-relay-lemma.md. For r ≤ 8 the local count gives a regular off-class site; the Relay lemma would then light every same-parity pair. Test the hypothesis against every reviewed dark room.

## 2026-11-23 19:05
- d217: 4 CORRECT, 2 CORRECT WITH GAPS. Re-ran checks.py: 24 PASS, identical. RESULTS §11 updated; claim released.
- **My Relay brief was wrong.** R22 and P6 have regular off-class sites upstairs, so "regular off-class site ⇒ lit" is false. I sent Astra a steer with the corrected lemma, which adds "no separating parity factor", and the three-way split. Estimate unchanged at 8–10%.

## 2026-11-23 19:14 (tick)
- Astra idle. New note bbbb/l1-relay-lemma.md (L1 case iii). It has the corrected three-way split, a different-parity analogue, and a dark-room control table (R22 and P6 in (ii), R34 in (i)). It adds an exact single-state test: components are paths or cycles, with D ≡ 2 mod 4 or gcd(C,4) | 2−D.
- Launched d218-review-relay-lemma (Opus, named rooms, 10 CPU-min); claim added.
- Briefed Astra: bbbb/l1-mod4-cocycle.md. Darkness in (iii) as a Z/2 cocycle; invariance gives a double cover and hence a separating factor; cov4181 sanity check.

## 2026-11-23 19:25
- d218: 4 CORRECT, 2 CORRECT WITH GAPS (scoping). Re-ran checks.py; see the PASS count above. RESULTS §11 updated; claim released; verdict forwarded. Estimate unchanged at 8–10%.

## 2026-11-23 19:34 (tick)
- Astra idle. New note bbbb/l1-mod4-cocycle.md (L1 case iii). It refutes my cocycle → double-cover brief: darkness separates the lifts into different components, so there is no cycle-parity constraint. Dilated R22 has a C=10 cycle. A triangle obstruction rules out any global cocycle. cov4181 shows a class-b parity flip across states. A character gives a cover above, not a factor.
- Launched d219-review-mod4-cocycle (Opus, named rooms, 10 CPU-min); claim added.
- Briefed Astra: bbbb/l1-large-monodromy.md. At n=22, d ≥ 20, use Jordan's theorem for giant monodromy; relate the state action; test on cov4181.
- Assessment: the last 7 notes (d212–d219) are reviewed scoping with no closure. L1 case (iii) at n=22 is the frontier. The estimate holds at 8–10%. The insertion-descent stopping rule is 2026-11-26 20:00.

## 2026-11-23 19:45
- d219: 6 CORRECT, 1 CORRECT WITH GAPS. Re-ran checks.py; see above. RESULTS §11 updated; claim released; verdict forwarded. The cocycle route is closed. Estimate 8–10%.

## 2026-11-23 19:55 (tick)
- Astra idle. New note bbbb/l1-large-monodromy.md (L1 case iii). At n=22, r=8, the primitive branch excludes M22 (order-3 elements have six 3-cycles, forcing z_x ∈ {0,6}, while Σz = 8), giving A21/S21. The imprimitive branch has 20 external sheets. Shear functoriality is proved geometrically. cov4181's G = (S7 wr S4) ∩ A28. The realization lemma is still missing.
- Launched d220-review-large-monodromy (Opus, cov4181 only, 10 CPU-min); claim added.
- Briefed Astra: bbbb/l1-cylinder-levels.md. Origami orbit criterion (S, T on a common interior integer level of a tall cylinder) plus a counting attack at n=22, r=8.

## 2026-11-23 20:05
- d220: all claims hold (4 CORRECT, 1 WITH GAPS). Re-ran checks.py; see above. RESULTS §11 updated; claim released; verdict forwarded. Estimate 8–10%.

## 2026-11-23 20:14 (tick)
- Astra idle. New note bbbb/l1-cylinder-levels.md (L1 case iii). Exact orbit criterion: (I) a common interior cylinder level or (II) a common open saddle connection; interior-only is false (cov446). Exact incidence counts at n=22 (52 regular sites). A cov4181 type-(I) witness. At the primitive branch, R=26 and off-class ≥15. A CRT test for two-traversal witnesses in pure-twist families.
- Launched d221-review-cylinder-levels (Opus, named rooms, 10 CPU-min); claim added.
- Briefed Astra: bbbb/l1-twist-existence.md. Prove the CRT test passes for some twist family at n=22 primitive, or reduce to an explicit finite list of failing tuples.
- Assessment: d212–d220 are reviewed scoping, and case (iii) at n=22 remains open. If the twist-existence note doesn't close or finitize the primitive branch, I'll report to Daniel with a route decision (theory continuation vs. an approved finite check).

## 2026-11-23 20:25
- d221: no wrong claims (3 CORRECT, 3 WITH GAPS). Re-ran checks.py; see above. RESULTS §11 updated; claim released; verdict forwarded.
- **Sync failed** at 20:12 and 20:22. GitHub port 443 timed out (network). Local commit 9e3b4a3cd isn't pushed; origin/main is 4d09ed3a3. Will retry next tick.

## 2026-11-23 20:40 tick
- Astra note l1-twist-existence.md (L1 case iii, primitive branch): exact D(I,J) residue test for two-traversal twist witnesses, planar-map classification, tree filter, cov4181 j=3 witness. Reduction only; no closure or finitization at area 22. d222 Opus review launched (claim on board).
- Astra briefed: imprimitive degree-20 branch at n=22 via the 11-block intermediate cover N (case ii vs. deck-involution witness); follow-on: general block-size-2 lemma.
- Route decision due (condition from 20:14 met): reported to Daniel.
- Sync: still no outbound internet (GitHub/Google time out). Local 9e3b4a3cd unpushed; origin/main 4d09ed3a3.
- Estimate 8–10% (unchanged). Ledger 6/274/4,294.
- Slack self-DM post failed (ECONNREFUSED); status reported in chat only. Re-post when the connection returns.
- d222 done: 5 CORRECT, 2 CORRECT WITH GAPS (minor), 0 wrong. Exact decision procedure; no area-22 closure. Re-run identical (0 failures). RESULTS §11 updated, claim released, verdict forwarded to Astra.
- Network back. Sync pushed 565ed6da6 (HEAD = origin/main verified). Slack status posted. Note: sync blocked d71-check-qclass/sample_check.py and bbbb/l1-pocket-lemma.md for private data (pre-existing filter, not published).

## 2026-11-23 20:50 tick
- Astra note l1-imprimitive-22.md (L1 case iii, imprimitive branch): quotient N is a degree-11 sphere, z=4; BBBB ⇔ qₓ≥1; (2,11) row excluded from case (ii); exact double-cover graph test; axial half-room H (11 cells) + census ⇒ S lights T or σT. No closure. d223 Opus review launched (claim on board).
- Astra briefed: seam-parity lemma (both seam-contact parities via odd-crossing cylinder), follow-on half-turn subcase.
- Stopping rule from tick text (N0 for LLLRLLLRLR by 11-24 20:00) is superseded by PROGRAM.md deadlines (11-25/11-26).
- Estimate 8–10% (unchanged).
- Sync pushed 16fd9e29a (HEAD = origin/main verified); two earlier runs timed out at 150–170 s before pushing.
- d223 done: 6 CORRECT, 2 CORRECT WITH GAPS, 0 wrong. The imprimitive branch is exactly the area-22 rooms with a parity-preserving mirror or half-turn symmetry. First open case: a half-turn with two distinct off-center orbits. The reviewer suggests a symmetric-only area-22 run built from 11-cell halves; it's a NEW SEARCH, so it needs Daniel's approval and nothing was launched. Re-run identical. Claim released, verdict forwarded.

## 2026-11-23 21:10 tick
- Astra note l1-seam-parity.md (L1 iii, axial branch): exact attainable-parity set; band multi-twist shear swaps target sides under gcd(Lₛdₜ,2Wₜ) | Wₜ; half-turn quotient has 2 branch values. Sufficient test, no closure. d224 Opus review launched (claim on board).
- Astra briefed: affine transfer lemma on the primitive branch (corner-fixing multi-twist group A_S; orbit of a short neighbor must reach T, or an invariant partition gives case ii); follow-on: test on cov4181 class d.
- Route proposal to Daniel: the imprimitive branch at area 22 = symmetric rooms; a symmetric-only area-22 check from 11-cell halves is small, but it's a new search and needs approval.
- 21:15 sync failed (git fetch: cannot reach github.com:443); Slack also ECONNREFUSED. Last verified push 16fd9e29a; 21:10 notes pending.

## 2026-11-23 21:30 — route audit (Daniel approved)
- Busy-work audit: d212–d224 = 13 correct reformulations, 0 closures. Dropped the symmetric a22 check request. Affine transfer is the single live bet (deadline 11-25 20:00 or 2 notes). Review only closures/general lemmas. Estimate re-based 8–10% → 5–8%. PROGRAM.md updated; Astra told.

## 2026-11-23 22:00 — key-blocker attack (Daniel: "attack that")
- Astra's l1-affine-transfer.md (21:04) refutes my affine-transfer idea: SL₂ derivative preserves displacement gcd/parity; band twists fix pinned sites; on cov4181 the twist group acts trivially. Logged, not reviewed (an obstruction to my proposal; no closure). Affine route stopped.
- Blocker identified: pinned pairs are the single residual of descent (d214 slack window, d215 ratio compactness, affine note). New route in PROGRAM.md, deadline 11-25 20:00. Astra briefed on the general lemma (two-scale blow-up, finitely many local pin types); Opus attack agent d225 on the d215 staircase pinned strip as the worked instance.
- d224 done: 2 CORRECT, 4 CORRECT WITH GAPS, 0 wrong; sufficient test only (fails when every band has height 1). Re-run identical. Claim released; verdict logged for Astra (no redirect: she's on pinned pairs).

## 2026-11-23 21:12 tick
- Astra note l1-affine-transfer-obstruction.md (21:07, written before the pinned-pair brief): an area-uniform family (prime areas p ≥ 37) where the band twists fix a nondirect pair pointwise, though one floor reflection lights it. Second affine note; the route was already stopped. It obstructs a proposal, not illumination: logged, not reviewed. It confirms that pinned sites are the residual.
- Astra is running on the pinned-pair brief (since 21:08). d225 is running (dir empty, launched 21:10). Estimate 5–8%.
- 21:15 sync failed (git fetch: github.com:443 unreachable); Slack post ECONNREFUSED. Last verified push 16fd9e29a.
- d225 attack done: claims the d215 x=1 staircase open strip is closed for x+y>8 (the strip near b=c, and 2a+2b ≤ c with α ≥ 1/4). Two pins block the lines α=1/2 and α=1/3, and one floor bounce fixes both. Five crossing types (P0, P+, P−, R, S). Open: lattice rooms (0,2) and (0,3) (areas 24, 27), and pins with sign order (−,+). Re-run identical, 45 PASS, 0 failures. A closure claim, so independent review d226 launched. Claim d225 released.
- d226 done: the d225 closure HOLDS for x+y > 8 across the whole sector (2 CORRECT, 2 CORRECT WITH GAPS, 0 wrong; 62 checks, 0 failures; re-run identical). This is the first closure on the pinned-pair route. The crossing-type principle needs tightening: unfolded μ, two-sided approach (counterexample ray at (12,26)), and shifts at the non-pinned interfaces. Open: lattice rooms of areas 24 and 27. The estimate stays at 5–8%: one family is closed, and the general lemma isn't proved yet. Claim released, verdict forwarded.
- Sync pushed 50cd80b8c (20 files; HEAD = origin/main verified). Slack status posted.

## 2026-11-23 21:35 tick
- Astra note l1-pinned-pairs.md (L1). Key findings:
  - (a) Interior pins are locally free, so there is no local obstruction type.
  - (b) WRONG CLAIM (mine): the lemma "darkness forces a gap ≤ B(r)" is ill-posed. Dilation preserves darkness, so the bound is equivalent to having no pinned dark pair. R22 (r=9) is pinned and dark at every dilation.
  - (c) The graze determinant test.
  - (d) Sign-pattern theorem: end bounces give only 0, +, −, or (+ then −); (−,+) is impossible at every scale.
  - (e) A six-reflex room realizes the (−,+) order for a fixed chord, with arbitrary gaps. This obstructs the move, not illumination.
  - (f) R22 has the multiple-gate type.
- The blocker is global aim (an itinerary that hits the target image), not local. General lemma, so d227 review launched.
- Astra redirected: interior-bounce sign patterns (a kink in q).
- d227 done: 7 CORRECT, 1 CORRECT WITH GAPS; the six-reflex pair is LIT by an interior roof–floor double bounce, which realizes (−,+). Open: (−,+) with no double-bounce wall; mixed demands like (−,+,−). Re-run identical. Claim released, verdict forwarded.

## 2026-11-23 21:52 tick
- Astra note l1-interior-bounce.md (L1, general): exact visit displacement q = s − Hα; an interval-chain iff criterion for a fixed chain; a sign-cone theorem in which three cut rules settle every strict demand vector; an exact simultaneous-clearance condition. R22: its demand IS in the sign cone, but the turn hits corner (1,2) at zero clearance, so the cone doesn't characterize darkness. The residual is again aim/clearance, now as a linear feasibility problem over integer counts per winding. General lemma, so d228 review launched.
- Astra briefed: completeness of slab-excursion normal form + arithmetic (zero-clearance) lemma.
- d228 done: 5 CORRECT, 1 CORRECT WITH GAPS; sign-cone theorem confirmed. R22 fails by parity (needs 4<H<6, H even), which supports the arithmetic-clearance conjecture (B). Re-run identical. Claim released, verdict forwarded.

## 2026-11-23 22:10 tick
- Astra note l1-excursion-normal-form.md (L1). WRONG CLAIMS (both mine) refuted:
  - (A) Presburger encoding: one fixed itinerary of a pinned pair in a five-reflex chart is legal exactly when u > m², which is non-semilinear.
  - (B) Parity gap ⇒ fold: a seven-reflex family has R22's exact missed window 4<H<6 yet is lit by one side reflection, velocity (−5c,1). Coordinator verified this by hand: hit at x=−c, y=1/5; crossing at y=1 at x=3c ∈ (0,4c); arrives at (8c,2) inside (4c,10c).
- Also:
  - A finite tier graph (≤ 4(r+3)² states) describes all legal words exactly.
  - A fixed excursion template can fail with strictly negative clearance while the pair is lit by another path.
  - The LLLRLLLRLR stress chart has no interior pinned mark, so there is no N0.
- Not reviewed: these are counterexamples to coordinator proposals, and the key one was hand-verified.
- Next: witness selection (bounded templates), the first open step of (A).

## 2026-11-23 22:30 tick
- Astra note l1-witness-selection.md (L1):
  - The five-reflex parabola pinned family is lit for ALL m≥3, u≥m+2 (gate lemma + winding choice; one simple cycle). The seven-reflex family is lit by a bounded walk.
  - General: bounded-template membership reduces to finitely many polynomial tests (extreme occurrences). One-gap tails are affine (ag+b>0).
  - Open: interleaved cycles in a branched recurrent component, and joint (diagonal) regimes.
- Closure + general lemma, so d229 review launched.
- Astra briefed: commuting cycle translations ⇒ target image depends only on counts; witness order = cutting sequence; branched component ⇒ Λ-periodic slit corridor (square-tiled), apply the cylinder criterion I/II.
- d229 done: 6 CORRECT, 1 CORRECT WITH GAPS, 0 wrong. Parabola family closed; template and tail tests confirmed. Re-run identical. Claim released, verdict forwarded.

## 2026-11-23 22:50 tick
- Astra note l1-periodic-corridor.md (L1). WRONG CLAIM (mine) refuted: the "Λ-periodic corridor" reformulation loses the terminal sheet. In the 7-cell pinned room ([0,3]² minus two corners, S=(1,2), T=(2,1)), (1,−7) reaches T but (13,−7) in the same cycle-lattice coset ends at the corner (0,1); likewise for all +84j.
  - Coordinator spot check: (1,−7) traced exactly to (2,1). My quick tracer for (13,−7) was buggy; this point is unverified by me.
- Positive: fixed-H residue test (K mod HM, finite), and the smallest pinned room (area 7, minimal).
- Remaining step, in her words: "produce some H and a residue whose ray reaches a compatible T". That is the seed problem the route started from. Not reviewed (it refutes a coordinator proposal; it's not a closure).
- Assessment: the pinned-pair route has produced reviewed general tools (sign-cone d228, templates d229) but has circled back to the seed problem. Asked Astra for a route assessment; reported to Daniel with a stop recommendation.
- 23:07 Astra route assessment (l1-route-assessment.md): no seed-producing argument in sight beyond one-gate nearest winding; area-22 census ≈1.17B rooms, 3.1 CPU-h (2.1–3.8); areas 22–25 ≈170 CPU-h, decisive only with a proved cutoff; her P(theory closes L1) = 5%. Astra idle by instruction. Awaiting Daniel's route decision.
- 23:10 PAUSED by Daniel. Cancelled crons 2a4e66f3 (tick) and e1d1ec9d (daily audit). Astra told to stand by.
- 2026-11-24 Coordinator (Fable): d230-fresh-angles/README.md written at Daniel's request. Angle 1: gate-box lattice + flatness criterion (dual lattice = integer relations among slab moduli); unreviewed. Oblique-twist check on the 20-wall obstruction family: marks fixed in 21/21 cases. No searches, no sync. Program stays paused pending Daniel.
- 2026-11-24 Daniel approved the gate-box route; pause lifted. d231 Opus review launched (claim on board). Astra briefed: tests on R22 and the locked-gate family, then the persistence step.
- 2026-11-24 Tick cron dfb9f162 created (every 20 min, gate-box route). Daily audit cron not recreated.
- 2026-11-24 22:20 Astra: l1-gate-box-tests.md (R22 short blockers found: arithmetic relation (1,−2), width 1/2; locked gate reproduced by relation (1,0,−1); 20-wall control unblocked) and l1-total-resonance.md (WRONG COORDINATOR CLAIM: itinerary-level decoupling refuted; a long middle visit is absent from every short relation yet the box misses via an end-to-end relation; per-excursion reflex charging fails at six reflexes). Logged without review (tests and a refutation). Astra briefed: room-level decoupling by independent end excursions (l1-room-decoupling.md). d231 still running. Estimate unchanged 5–8%.

## 2026-11-24 22:45 tick
- Astra note l1-room-decoupling.md (L1). WRONG COORDINATOR CLAIM (second on this route): "cross relations fail for all but finitely many (k0,k2)" is false. Cross relations give whole lines, such as k0 = k2. Weaker count in an aggregated model only: at most P(N+1) pairs on cross lines, P = prod over j != M of (2b_j+1).
  - New, general, conditional on the d230 model: clearance-weighted lemma. With a common-slope realization x of both end legs and rho_i = dist(x_i, boundary of J_i), a missed coset gives a dual vector with n_M != 0 and (sum rho_i^2 l_i^2)^(1/2) <= C_g. No lcm, but it needs the clearance of a realization, which is the seed problem again.
  - First stall: the six-reflex two-gate chart's monotone itinerary has disjoint end-slope sets, so there is no common x.
  - Not sent to review: the lemma is conditional and d231 was still open.
- Astra briefed: exclusion of positive-dimensional dark flats by the exact (projection) criterion on a flat, then growth rays and a tie lemma (l1-dark-flat-exactness.md).
- d231 done (Opus, about 12 CPU-min against a 10-minute budget; two runs timed out). Verdicts: Lemma 1 CORRECT; coset parametrization, Lemma 2 and the g=1 formula CORRECT WITH GAPS; two WRONG CLAIMS of mine in d230:
  - "Universal relations need thin boxes" is false. A slab visited twice at full height gives a relation of width <= 2 < Flt(2), so Lemma 2 never certifies an itinerary with a repeated full-height visit. Hand-checked: four gate terms, each |J| <= w, coefficient 1/(2w).
  - The parabola hand check is false. For even m with m | U <= 7m (U = u - m) the monotone itinerary has a relation of width u/(4m), which is 3/4 at (10,30). Hand-checked with n = (-U/m, m/2, (m+2)/2). The pairs are lit (d229); the criterion is silent.
  - Also: "explicit in general" is overstated (Flt(g) is unknown for g >= 3), and rational independence is vacuous for lattice rooms.
- Re-run of light2.py (300 s cap): the five parabola rows and the six-reflex rows match review.md; it times out at the same B=18 roof itinerary. gatebox.py and light.py not re-run in full (they exceed the budget).
- Consequence: flatness is a necessary condition for darkness on non-repeating itineraries only, and it can't bound the area on the parabola subfamily. The route needs the exact coset or one-direction projection test, family-wide. The new Astra brief already uses the exact form.
- Board claim d231 released. Verdict forwarded to Astra. Estimate 5-8% -> 4-7%.

## 2026-11-24 22:55 tick
- Astra note l1-dark-flat-exactness.md (L1), idle after it. Claims: on a dark flat the open-box obstruction for a fixed itinerary is exactly a quotient-coset miss, and the affine levels of the persistent characters don't depend on x; a boundary-face test; six-reflex roof calibration (lit cosets 00000 and 11001 of 32); a conditional tie lemma (a growing gap crossed once with compatible end legs has n_M != 0, so it is tied to a second growing gap); a coefficient bound for a fixed itinerary that is independent of the longitudinal lengths. Her own scope statement: no relation locking every itinerary, no eight-reflex exclusion, no N0.
- The coefficient bound is a length-uniform lemma, so d232 review launched (Opus, claim on board, snapshot in d232-review-dark-flat-exactness/).
- Astra briefed: minimal-support ray lemma (l1-minimal-ray.md). Single-gap rays by k = 0, 1, >= 2 separating components; two-gap rays, target "tie => fold symmetry", with a calibration on a known dark family with a free length at r >= 9.
- Estimate unchanged, 4-7%, until d232 returns.
