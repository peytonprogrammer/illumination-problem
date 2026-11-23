# D6: Hurwitz census of genus-0 pillowcase covers

This directory holds an exact, exhaustive census of abstract genus-0 pillowcase covers
with cycle lengths at most 3, for degrees n = 3 to 10. It tests the parity-factor
conjecture for the LIT/DARK verdict on pairs of regular points over corner `a`.

## Result

- Validation passes. The 22-wall room is DARK for all four S/T lifts. All 31 k7
  controls and all 8 triangle-screen controls are LIT. Castro-24, Tokarsky-26 and the
  34-wall room are DARK.
- The largest degree completed exhaustively is n = 10 (654 s with 13 workers). At
  n = 9 it was 49 s, so n = 11 would take well over the 40-minute limit.
- The conjecture fails in the "only if" direction. DARK pairs with no separating parity
  factor: 3, 12, 87 and 36 orbit pairs at n = 7, 8, 9 and 10.
- The "if" direction is a theorem (see [Facts that are proved](#facts-that-are-proved)).
  No LIT pair has a separating parity factor at any n.
- Four generalisations, G1, G5, G6 and G7, account for every counterexample through
  n = 10. G1, G5 and G6 are tested on every pair of the census and never predict DARK
  for a LIT pair. G7 covers one family of 3 orbit pairs at n = 10. It's checked by hand
  from computed hypotheses.
- A Nielsen class doesn't determine the verdict. From n = 8 on, some classes split into
  pure-braid orbits with different numbers of DARK pairs. In every such class the orbits
  also differ in |G|.
- Involution flag: one counterexample family (G1, n = 10) is the double of a 10-square
  staircase polyomino in 3 bases of its orbit. Both marked points lie on the walls.

## Conventions

- A permutation is a tuple `p` with `p[i]` the image of sheet `i`. Products act on the
  right: `mul(p, q)` applies `p` first, then `q`. This matches `d4_monodromy.mul`.
- A cover is a tuple `t = (t0, t1, t2, t3) = (g_a, g_b, g_c, g_d)` with
  `t0 t1 t2 t3 = 1`. It's the corner monodromy of a geometric basis: disjoint tails
  from one base point, in cyclic order.
- The census keeps tuples that generate a transitive group, have every cycle length at
  most 3, and satisfy `sum over x of (n - #cycles(g_x)) = 2n - 2` (genus 0). Tuples are
  counted up to simultaneous conjugation. The identity is allowed at a corner.
- A cycle of length 1, 2 or 3 is a point of Q with cone angle pi, 2 pi or 3 pi: a pole,
  a regular point or a zero.
- Hurwitz moves:
  - `s_i` maps `(t_i, t_{i+1})` to `(t_i t_{i+1} t_i^-1, t_i)`.
  - `s_i^-1` maps `(t_i, t_{i+1})` to `(t_{i+1}, t_{i+1}^-1 t_i t_{i+1})`.
- Points over `a` keep fixed IDs through moves. When `a` moves and its new monodromy is
  `k^-1 g k`, the labels transform as `pt' = pt o k^-1`.
- The pure-braid group acts through `s0^2`, `s1^2` and their inverses. Adding `s2^2`
  never changes an orbit. This is checked on every orbit at n <= 7 and on the 22-wall
  room.
- Light rule. Along the tail arc from `a` to corner `x`, build the bipartite graph with
  one vertex per cycle of `g_a` and of `g_x`, and one edge per sheet. Light passes only
  through regular points. Marked regular points sigma and tau over `a` are connected if
  they lie in one component of the subgraph induced on 2-cycle vertices.
- A pair (sigma, tau) is LIT if it's connected along some tail arc in some basis of the
  marked pure-braid orbit. Otherwise it's DARK. The tail arcs over the whole orbit cover
  every isotopy class of simple arc from `a`, because the level-2 group acts
  transitively on each slope parity class.
- In the marked orbit only regular points over `a` carry IDs. Poles and zeros over `a`
  share the label -1, because they never carry light or marks.
- `k` is the number of 2-cycles in `g_b`, `g_c` and `g_d` together.
- A factor is N = Q / Pi for a block system Pi other than the one-block system.
  N = Q (the singleton system) counts.
- Parity property of N: the induced `g_b`, `g_c`, `g_d` have no 2-cycles.
- Separation: sigma and tau map to distinct points of N over `a`.
- Degenerate cover: one of `g_b`, `g_c`, `g_d` is the identity. Q is then branched over
  only 3 of the 4 corners, although every point over the fourth corner is a pole of the
  flat metric.
- An orbit pair is one pair (sigma, tau) on one pure-braid orbit. A tuple pair weights
  each orbit pair by the number of tuples in its orbit.

## Validation

All rows below come from `validate_rooms.py` with the current code
(`validate_rooms.log`, `validate_rooms.json`).

| Input | Framework | Degree | Verdict | Basis |
| --- | --- | --- | --- | --- |
| 22-wall room, all 4 S/T lifts | Square | 15 | DARK | Full marked orbit, 3,456 states |
| 22-wall room | Triangle pull-back | 30 | DARK | Two components, 3,456 states each |
| 30 k7 models and the W18 control | Square | 14 to 18 | 31 of 31 LIT | Stops at the first lit target |
| First 8 screen records with W <= 21 | Triangle pull-back | 26 to 27 | 8 of 8 LIT | Stops at the first lit target |
| 34-wall room | Square | 19 | DARK | k = 0 |
| Castro-24 | Triangle pull-back | 27 | DARK | k = 0 |
| Tokarsky-26 | Triangle pull-back | 29 | DARK | k = 0 |

- The square framework tuple is `(g_A, g_C1^-1, g_B, g_C2^-1)` from the d4 generators
  at `(0,0)`, `(1,0)`, `(1,1)`, `(0,1)`.
- The triangle framework pulls back to the pillowcase branched at A and B. With
  `u = g_A`, `v = g_C^-1`, `w = g_B^-1` and `u v w = 1`, the tuple is
  `(u^2, v, w v w^-1, w^2)`.
- In the 22-wall room, the lit A-point classes are {0, 1, 7} and {4, 5, 6}. Its plain
  pure-braid orbit has 48 tuples. Each pull-back component lies in the full B_4 orbit
  (1,152 labelled tuples) of the square tuple, with corner orders (A, C1, C2, B) and
  (A, C2, C1, B).
- An earlier run labelled every point over `a` and found 20,736 marked states for the
  22-wall room. The 10,368-state certificate in d4 counts cylinder states, a different
  object. The three numbers are 6, 3 and 1 times 3,456.
- The Castro-24, Tokarsky-26 and 34-wall checks are weak. With k = 0, no basis has a
  regular point over `b`, `c` or `d`, so every pair is DARK without an orbit search.
  The orbit search for these rooms stops at 200,000 states.

## Census

| n | Tuples | Nonempty Nielsen classes | Split classes | Braid orbits | Orbit pairs | DARK orbit pairs | Tuple pairs | DARK tuple pairs | Seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 22 | 19 | 0 | 19 | 0 | 0 | 0 | 0 | 0.0 |
| 4 | 104 | 44 | 0 | 44 | 12 | 3 | 21 | 3 | 0.2 |
| 5 | 573 | 94 | 0 | 94 | 23 | 1 | 153 | 12 | 0.1 |
| 6 | 3,882 | 294 | 28 | 342 | 216 | 6 | 1,596 | 33 | 0.2 |
| 7 | 25,904 | 432 | 27 | 463 | 357 | 12 | 15,111 | 159 | 0.5 |
| 8 | 185,976 | 928 | 158 | 1,148 | 1,606 | 84 | 144,588 | 1,185 | 4.6 |
| 9 | 1,376,056 | 1,745 | 193 | 2,015 | 2,941 | 175 | 1,363,602 | 5,673 | 49.1 |
| 10 | 10,491,858 | 2,726 | 406 | 3,352 | 7,709 | 158 | 12,998,667 | 26,784 | 653.9 |

- `Seconds` is wall time with 13 worker processes.
- `check_enumeration.py` checks the enumeration against brute force and the mass
  formula at n = 3 to 6. At n = 6 there are 3,882 classes and 2,723,760 labelled
  tuples.
- `census.py` asserts that every orbit stays inside its enumerated Nielsen class and
  that the orbits partition the class.
- `check_orbit_invariance.py` reruns the decider from every tuple at n = 6 (1,128
  tuples) and n = 7 (9,407 tuples). All orbit-mates agree and `s2^2` is redundant. A
  full-B_4 scheme that uses every tail arc gives the same lit set.
- No pair is LIT when k = 0, at any n.

### Conjecture verdict

Each cell counts orbit pairs that are DARK without a separating parity factor. Each pair
is listed under the first test that explains it, in the order G1, G5, G6, G7.

| n | Total (tuple pairs) | G1 | G5 | G6, N = Q (degenerate) | G6, proper N | G7 | LIT with parity factor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 to 6 | 0 (0) | 0 | 0 | 0 | 0 | 0 | 0 |
| 7 | 3 (3) | 0 | 0 | 3 | 0 | 0 | 0 |
| 8 | 12 (15) | 6 | 0 | 6 | 0 | 0 | 0 |
| 9 | 87 (195) | 0 | 75 | 12 | 0 | 0 | 0 |
| 10 | 36 (117) | 3 | 0 | 18 | 12 | 3 | 0 |

`rigid_factor.py` runs G6 on every pair at every n. It never predicts DARK for a LIT
pair. After G1, G5 and G6, the only DARK pairs left are the 3 G7 pairs at n = 10.

## Generalised tests

- G1 (parity over a pillowcase quotient). Let Pi be a block system whose induced tuple
  has all cycle lengths at most 2 and exactly 4 fixed points, so P' = Q / Pi is a
  pillowcase. Suppose sigma and tau lie over one P'-corner c0. Let Pi' refine Pi, with
  N = Q / Pi', such that N has no regular point over any P'-corner other than c0 and N
  separates sigma and tau. Then the pair is DARK.
- G5 (per corner). For each corner x in {b, c, d}, some factor N satisfies one of:
  - Parity route: N separates sigma and tau, and N has no regular point over x.
  - Cut route: sigma and tau have the same image in N. Every regular point of Q over
    `a` and over x maps to a regular point of N. The monodromy of N at one of the other
    two corners is a single cycle.
- G6 (rigid factor). Some factor N has the identity as induced monodromy at a corner y.
  Over each other corner x, build the graph on N-points over `a` and x, with one edge
  per sheet whose Q-points over `a` and x are both regular. sigma and tau map to
  different components of the union of these graphs.
- G7 (rigid over a pillowcase quotient). P' = Q / Pi is a pillowcase as in G1, and sigma
  and tau lie over two different P'-corners A0 and A1. Q -> P' is unbranched over a
  third P'-corner. sigma and tau are the only regular points of Q over P'-corners. The
  census computes the pair as DARK, and the hypotheses are checked from the block
  structure. G7 isn't coded as a test.

### Proof sketches (interpretation, not machine-checked)

- G1 and G5 parity route: the parity argument below, applied over P' or one corner at a
  time. The corner of an arc is braid invariant, so corners can be blocked separately.
- G5 cut route: the preimage in N of the arc between the other two corners is connected
  and holds their branch points. Branch points over `a` or x are leaves of the light
  graph, joined to it through cylinders. The union misses every closed light walk and
  has simply connected complementary pieces. So every closed walk in N lifts to a
  closed walk in Q, and tau is never reached.
- G6: N -> B is unbranched over y, so N covers the sphere minus the other three
  corners. In a 3-punctured sphere all simple arcs from `a` to x are isotopic, so N
  has one lift pattern per corner, the one in the given basis. A light walk in Q
  projects to a walk in that fixed graph. Over y, every N-point is a single fixed block,
  so passing a regular Q-point over y doesn't change the N-point over `a`.
- G7: a light walk from sigma can turn only at regular points, and the only regular
  points over P'-corners are sigma and tau. So a walk to tau is one straight segment in
  P' from A0 to A1. A saddle connection between two corners of a pillowcase is simple.
  Q -> P' is unbranched over the third corner, so all such segments are isotopic in the
  sphere minus the three branched corners and lift the same way.

## Facts that are proved

- If some factor N has the parity property and separates sigma and tau, the pair is
  DARK. Proof: along any arc, a light walk alternates between regular points over `a`
  and regular points over x. A regular point of Q over x maps to a point of N whose
  cycle length divides 2. N has no regular point over x, so that image is one fixed
  block, and both `a`-points joined through it lie over the same N-point. Block
  systems are invariant under moves, so the walk never leaves the N-point of sigma,
  and tau lies over a different one.
- The census confirms this: 0 LIT pairs with a parity factor at every n.

## Counterexample classes

Each representative gives `rep = [g_a, g_b, g_c, g_d]` and the sheets of sigma and tau.
`summary.json` holds every family with its corner orders and block systems.

### A. Degenerate covers (G6 with N = Q)

- n = 7, cycle types a [3,2,2], b [1^7], c [3,2,2], d [3,2,2]. One orbit pair per
  corner order.
  - `rep = [[1,2,0,4,3,6,5], [0,1,2,3,4,5,6], [3,4,6,0,5,1,2], [4,6,5,2,0,3,1]]`
  - sigma = sheets [3, 4], tau = sheets [5, 6].
  - G = A_7 (order 2,520), primitive, k = 4, trivial deck group. Plain and marked
    orbits have 1 element.
- n = 8: a [3,2,2,1], b [1^8], c [3,3,2], d [3,3,2]; G = S_8, k = 2.
- n = 9: a [3,2,2,2], b [1^9], c [3,3,2,1], d [3,3,3]; G = S_9, k = 1.
- n = 10: a [3,3,2,2], b [1^10], c [3,3,2,2], d [3,3,2,2] or [3,3,3,1].
- These break "G primitive and k >= 1 implies LIT". Every primitive DARK pair with
  k >= 1 through n = 10 is in this class.
- These covers aren't rooms. In a square-tiled room, `g_b = 1` makes every b-lattice
  point a convex corner, which only one square satisfies.

### B. Parity over a proper pillowcase quotient (G1), n = 8 and 10

- n = 8: a [2,2,1^4], b [2^4], c [2^4], d [3,3,1,1].
  - `rep = [[1,0,3,2,4,5,6,7], [4,5,6,7,0,1,2,3], [5,7,6,4,3,0,2,1], [0,2,3,1,7,4,6,5]]`
  - sigma = [0, 1], tau = [2, 3].
  - |G| = 96, imprimitive with one 2-block system of block size 4. Its induced types
    are a [1,1], b [2], c [2], d [1,1]. So P' is the double of B branched over `b` and
    `c`.
  - Deck group trivial. Plain orbit 1, marked orbit 2. The other orbits of this Nielsen
    class (|G| = 48) have no DARK pair.
- n = 8: a [3,2,2,1], b [2^4], c [2^4], d [3,1^5]; |G| = 288, the same P'.
- n = 10: a [3,2,2,1^3], b [2^5], c [2^5], d [3,3,1^4]; |G| = 7,200, plain orbit 12.
  This family is the one flagged as a polyomino (see [Involution flag](#involution-flag)).

### C. Per-corner blocking (G5), n = 9

- Parity route at every corner:
  - Types a [2^4,1], b [2^3,1^3], c [2^3,1^3], d [3,3,3]. |G| = 36, k = 6.
  - `rep = [[1,0,3,2,5,4,7,6,8], [0,2,1,4,3,5,6,8,7], [0,7,8,3,4,6,5,1,2], [1,8,6,5,2,7,4,3,0]]`
  - sigma = [2, 3], tau = [6, 7].
  - Two 3-block systems separate sigma and tau. One has no regular point over `c`; the
    other has none over `b`. Q itself has none over `d`. No single factor works at all
    three corners.
- Cut route at one corner, Z/3 deck group:
  - Types a [2^3,1^3], b [2^3,1^3], c [3,3,1^3], d [3,3,3]. |G| = 54, k = 3.
  - `rep = [[1,0,3,2,5,4,6,7,8], [0,6,2,7,4,8,1,3,5], [0,5,2,1,4,3,7,8,6], [1,7,3,8,5,6,4,0,2]]`
  - sigma = [0, 1], tau = [2, 3]. Plain orbit 3, marked orbit 6.
  - The deck group permutes the three regular points over `a` cyclically.
  - The 3-block system `[[0,2,4],[1,3,5],[6,7,8]]` has induced types a [2,1], b [2,1],
    c [1,1,1], d [3]. sigma and tau have the same image. Every regular point of Q over
    `a` and `b` maps to a regular point of N, and `g_d` induces one 3-cycle, so `b` is
    blocked by the cut route. Q has no regular point over `c` or `d`.
  - Three more families share this shape, all with |G| = 162. One of them is degenerate
    (b [1^9]).

### D. Rigid proper factor (G6), n = 10

- Types a [2^5], b [2,1^8], c [3,3,2,2], d [3,3,2,2]. One pair per corner order, 4
  orbit pairs each.
- `rep = [[1,0,3,2,5,4,7,6,9,8], [0,1,2,3,4,5,6,7,9,8], [2,3,0,8,6,7,4,9,1,5], [3,8,1,0,7,9,5,4,2,6]]`
- sigma = [0, 1], tau = [8, 9].
- |G| = 3,840, k = 5, deck group of order 2 that doesn't map sigma to tau. Plain orbit
  5, marked orbit 10.
- One block system of block size 2. N has degree 5 with induced types a [2,2,1],
  b [1^5], c [3,2], d [3,2], so N is degenerate while Q isn't. It separates sigma and
  tau.

### E. Rigid over a pillowcase quotient (G7), n = 10

- Types a [3,3,2,2], b [2^5], c [2^5], d [3,1^7]. One orbit pair per corner order.
- `rep = [[1,2,0,4,5,3,7,6,9,8], [3,6,7,0,8,9,1,2,4,5], [6,7,3,2,9,8,0,1,5,4], [0,1,2,6,4,3,5,7,8,9]]`
- sigma = [6, 7], tau = [8, 9].
- |G| = 14,400, k = 10, trivial deck group. Plain orbit 1, marked orbit 2.
- Block system `[[0,1,2,8,9], [3,4,5,6,7]]`: P' is the double of B branched over `b`
  and `c`, with corners A0, A1 over `a` and D0, D1 over `d`.
- Over A0, Q has a 3-cycle and tau. Over A1, it has a 3-cycle and sigma. Over D0, g_d
  restricts to the identity, so Q -> P' is unbranched there. Over D1, it has a 3-cycle
  and two poles.

## Nielsen classes and braid orbits

| n | Split classes | Split classes with a pair | Orbits differ in |G| | Orbits differ in primitivity | Orbits differ in DARK count | Same |G|, different DARK count |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 28 of 294 | 6 | 3 | 3 | 0 | 0 |
| 7 | 27 of 432 | 13 | 3 | 0 | 0 | 0 |
| 8 | 158 of 928 | 77 | 61 | 52 | 6 | 0 |
| 9 | 193 of 1,745 | 105 | 88 | 84 | 21 | 0 |
| 10 | 406 of 2,726 | 266 | 227 | 182 | 15 | 0 |

- Every nonempty Nielsen class is a single pure-braid orbit for n <= 5.
- The verdict depends on the orbit, not only on the class. In every class where orbits
  differ in DARK count, they also differ in |G|.
- Example (n = 8): the class a [2,2,1^4], b [2^4], c [2^4], d [3,3,1,1] has orbits of
  sizes 3, 3 and 1 with |G| in {48, 96}. Only the |G| = 96 orbit has a DARK pair.
- The marked orbit is larger than the plain orbit for 1,807 of 2,017 orbits with a pair
  at n = 10. Moves often return the same tuple with the points over `a` permuted.

## Involution flag

`involution_flag.py` tests the seam reflection of the pillowcase, which fixes all four
corners, on every tuple of every counterexample orbit. It looks for a lift iota whose
quotient Q / iota is a disk that develops injectively into the square grid.

- Sanity check: the 22-wall room's square tuple develops to its own 15-square shape, up
  to symmetry.
- 41 of the 44 reflection lifts found have an interior cone point or an overlap. Some
  degenerate families have no lift.
- Flag: the n = 10 G1 family (a [3,2,2,1^3], b [2^5], c [2^5], d [3,3,1^4]) is the
  double of a 10-square polyomino in 3 of its 12 bases. One of them is this staircase,
  with rows from bottom to top: x = 0 to 3, x = 2 to 5, and x = 4 to 5.

  ```text
  .....##.
  ...####.
  .####...
  ```

  - The tuple is `[[0,2,1,3,6,5,7,4,9,8], [1,0,3,2,5,4,8,9,6,7], [1,0,4,5,2,3,9,8,7,6], [0,2,5,7,3,1,6,4,8,9]]`
    with `phi = [0,1,2,3,4,5,7,6,9,8]`.
  - The cover has exactly two regular points over `a`, so sigma and tau are those two.
    They're the wall points (2, 0) and (6, 2), not interior points, and iota fixes
    both.
- Reflections that swap corners (rhombic pillowcases) aren't tested.

## Interpretation

These points are interpretation, not computed facts.

- The conjecture's single-factor condition is too strong in two ways. Different corners
  can be blocked by different factors (G5). Parity can hold relative to an intermediate
  pillowcase rather than B (G1).
- Separately, rigidity creates DARK pairs: a degenerate factor or a degenerate
  cover over an intermediate pillowcase leaves one arc class per corner (G6, G7). No
  parity condition sees this.
- For interior points of rooms, the relevant counterexamples are the nondegenerate
  ones. None of them is a room with interior marks through n = 10 under the seam
  reflection.

## Reproduce

Run these commands from this directory with Python 3 and no extra packages:

```sh
python3 -B -u validate_rooms.py > validate_rooms.log       # about 7 minutes
python3 -B check_enumeration.py 6                          # enumeration versus brute force
for n in 3 4 5 6 7 8 9 10; do python3 -B -u census.py $n 13; done   # n = 10 takes about 11 minutes
python3 -B check_orbit_invariance.py 6 > check_orbit_invariance_n6.log
python3 -B check_orbit_invariance.py 7 > check_orbit_invariance_n7.log
python3 -B rigid_factor.py                                 # writes rigid_factor.json
python3 -B summarize.py                                    # writes summary.json
python3 -B involution_flag.py                              # reads summary.json, writes involution_flag.json
```

`census.py N W` uses W worker processes and writes `census_nN.json` and `census_nN.log`.

## Files

- `d4_monodromy.py`: verbatim copy of `d4-monodromy-blocks/monodromy.py` (SHA-256
  `d60460beba7c9a18965e113d0ebc88b7517a9d697a8e93812a488b6f2c288d17`). It provides
  block systems, induced actions, Schreier-Sims and the room builders.
- `hurwitz.py`: permutations, Hurwitz moves, canonical forms, the light rule and the
  marked and plain pure-braid orbits.
- `enumerate_tuples.py`: meet-in-the-middle enumeration of each Nielsen class up to
  conjugation.
- `check_enumeration.py`: brute-force and mass-formula checks of the enumeration.
- `validate_rooms.py`: validation on the d4 rooms and controls.
- `census.py`: the census, factor analysis, the G1 and G5 tests and the counterexample
  records.
- `check_orbit_invariance.py`: per-tuple invariance, `s2^2` and full-B_4 cross-checks.
- `rigid_factor.py`: the G6 test on every census pair, with a soundness count.
- `summarize.py`: aggregates `census_n*.json` into `summary.json` and labels each
  counterexample with its mechanism.
- `involution_flag.py`: the optional reflection flag.
- Outputs: `census_n3.json` to `census_n10.json` with their logs, `summary.json`,
  `rigid_factor.json`, `involution_flag.json`, `validate_rooms.json` and `.log`,
  `check_enumeration_n6.log`, `check_orbit_invariance_n6.log` and
  `check_orbit_invariance_n7.log`.
