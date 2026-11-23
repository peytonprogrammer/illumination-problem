# d62: referee review of d61 Lemma FC (equal-images branch)

Date: 2026-11-18. Target: `d61-fold-converse/README.md` (lines cited below) and
`fold_converse.py`. Named rooms only (R22, P6, cross12, dumb12). Exact
permutation and integer arithmetic. No d61 file was edited.

## Verdict

**Sound with fixable gaps.** The lit direction of Lemma FC is correct, and so
is the iff "x-lit iff some state's `D_alpha` joins `S~` to `T~`". The reduction
to `N_x` via R3 is correct, and so is `deg N_x <= r + 4 + 3 r_x <= 4r + 4`. No
finding is fatal. One finding is about the statement (the domain of the
`tau`). The other gap is about how much the d61 computation actually tests.

## 1. Line-by-line check of Lemma FC

**Every billiard path is accounted for.** A light path from `S~` to `T~` (both
over `a`) projects to `B` as a geodesic from `a` to `a`. With a primitive
rational slope `(p, q)`, the first lattice point after `a` is `a + (p, q)`,
of class `x != a`, and the segment meets no other corner. So the path runs
back and forth along one saddle connection `alpha: a -> x`. It is a walk in
`Gamma_alpha(Q)`. Regular points are interior lattice points and smooth wall
points (cone angle 2 pi in DP). Poles and zeros are convex and reflex corners.
"Interior vertices regular" is exactly corner avoidance, and passing a regular
vertex is `s -> g s` (straight continuation, which includes wall reflection).
Every isotopy class of arc `a -> x` is a tail arc in some state, because the
pure braid group acts on slopes through Gamma(2), which is transitive on each
parity class. d61 inherits this from d60 without restating it. It's true.

**Part 1 (path or cycle): correct.** Live vertices have degree 1 (live pole)
or 2 (N-regular) in `Gamma_alpha(N)`. Zeros are never live. Double edges are
possible: an N-regular `a`-vertex `{beta, beta'}` with `g_x` swapping the same
two blocks gives a 2-vertex cycle. The lemma's statement covers this case.
The code's shape label doesn't (finding C1).

**Proof step 3 (pass straight / reverse): correct.** Over an N-regular vertex,
Fact L gives `e = 1`, so the two sheets of the `Q`-point are in the two
distinct blocks, and the image passes through. Over a live pole `p` (a block
fixed by the induced `g`), only an `e = 2` point continues, and both of its
sheets lie in the one block, so the image reverses. Each excursion from `F_u`
bounces at most once (path case) or wraps once (cycle case). The lemma says
this, and `check_fc.py` asserts it.

**Part 3 (path case): correct in substance, misstated in the pole case.** See
finding G1. For `u` N-regular, `F_u` is in bijection with the sheets in
`beta` (and with those in `beta'`). `tau_{p_1}` acts on the `beta` side and
`tau_{p_2}` on the `beta'` side. Both are fixed-point-free partial
involutions, because transport is a bijection and only 2-cycles of `L_p` are
kept. The alternating-word verdict is then exact.

**Part 2 (cycle case): correct.** Every vertex is N-regular, so every visited
`Q`-point is regular, and the walk leaves `beta` and returns on `beta'`. That
is `mu`, and the reverse direction gives `mu^{-1}`.

**Part 4 ("never meets a point over an N-zero"): correct.** By Fact L, only
zeros lie over an N-zero, and light paths visit only regular points.

**Part 5 (wraps enclose branching): correct.** `K` is a whole component of
`Gamma_alpha(N)` with all vertices of degree 2, so it's a simple closed curve
on the sphere `N`. If one closed disc holds no branch value, the restricted
cover is trivial, and `mu = id`. The branch values that count may lie over
the other two corners. An early version of my check counted only poles over
`a` and `x`, and that version failed on dumb12. The lemma says "a pole of N",
which is right.

**Part 6 (corner avoidance): correct.** Fixed points of `L_p` give
self-loops. 3-cycles are `Q`-zeros with `e = 3`, which are reflex corners.

**The iff.** "Lit along alpha" implies "same orbit" through parts 2 to 4.
The converse holds because each generator is a realized excursion. The
union over states gives "x-lit iff some `D_alpha` joins". Both directions
are complete.

## 2. Reduction to `N_x` and the degree bound

- **R3 reduction: correct.** A factor with no regular point over `x` must
  merge each 2-cycle of `g_x`, because `len(p) = 2 / e` must be 1. So the
  factor is coarser than `B_x`. In `N_x`, `K` is `u` plus at most two
  `x`-poles. So "x-lit" is literally the realization lemma's connectivity
  statement. The equivalence "x-dark implies a certificate at x" iff "the
  realization lemma" is a correct restatement. It is also close to a
  tautology, and d61 says so.
- **Degree bound: correct.** Points of `N_x` over `x` have length 1 or 3, so
  `deg = P_x + 3 Z_x`. For a genus-0 cover with cone angles `k pi`,
  Gauss-Bonnet gives `sum (2 - k) = 4`, so `P - Z = 4`. Fact L gives
  `Z(N_x) <= Z(Q) = r` and `Z_x <= r_x`. With `W = 2r + 4 <= 20`, `r <= 8`,
  and `4r + 4 <= 36`.
- **COMPUTED** (`deg_bound.py`, own union-find for `B_x`). On all 12
  (room, x) cases: no regular `x`-point, `P - Z = 4`, `Z <= r`, and the bound
  holds. The tightest case is cross12 at `b`: `B_x` is discrete, so
  `N_x = Q` with degree 12, against a bound of 20.

## 3. Does `fold_converse.py` compute what the lemma says?

- **Ground truth (`dp_joined`) is independent of the lemma.** It uses only
  `g_a`, `g_x`, and cycle lengths, never `N`. It is not independent of the
  `Gamma_alpha` model. I checked that separately (below).
- **The "FC verdict" (`h_graph`) is not built the way README section 4
  (lines 166-167) says.** It doesn't compute `L_p`, transport it, or use the
  path/cycle shape. It re-simulates the same `Q`-walk step by step and cuts it
  at visits to `F_u`. So FC-versus-truth agreement is nearly automatic. What
  it actually tests is Fact L (asserted on every step) and containment in `K`
  (Lemma 1). The 992,988-instance count overstates the evidence for the
  lemma's algebraic form (finding G2).
- The code works on sheets, not points. That's the right domain (see G1).

### Independent checks (this directory)

| Script | What it does | Result |
| --- | --- | --- |
| `check_fc.py` | Implements FC as stated. Finds the ends of `K` from N-data only. Uses `tau_p` = `L_p` at the end, restricted to 2-cycles, conjugated by transport. Takes `<tau_1, tau_2>` orbits on points of `F_u` (u N-regular), `<tau_u, tau_p>` on sheets (u a pole), or `<mu>` (multigraph cycle). Tests every pair of regular a-points with equal image, every factor, every corner class as `a`. Asserts fixed-point-free involutions, one bounce per excursion, Fact L, and part 5 in weak form (`mu != id` implies at least 2 branched poles). Ground truth is its own walk. | 969,372 instances on R22, P6, cross12, dumb12 (capped BFS of the pure-braid orbit). 0 disagreements. All three mechanisms occur, including 2-vertex cycles (dumb12) and pole `u`. |
| `billiard.py` | Exact integer billiards in the cell room: no permutations, no orbit walk. Covers all primitive directions with `max(p, q) <= H`, reflects at walls, and stops at corners. Records the lift by reflection parity. Compares the number of lit lift pairs per (pair, x) with d61's rows at `N = B`. | R22 with wall marks (24 pair-x cells, H = 40), P6 (H = 40), cross12 with wall marks (H = 40), dumb12 (H = 30): 0 mismatches. Every x-lit row has a billiard witness. No x-dark row gets one. |
| `deg_bound.py` | Checks the section 6 bound. | Holds in all 12 cases. |

I also checked d61's own JSON. At `N = B`, the OR of `lit_x` over lift pairs
and `x` equals the O9 pair verdict for all 28 pairs. Factor-level `lit_x`
equals B-level `lit_x` for every row. The certificate counts (202 lit,
147 Par, 56 Cut) reproduce. `fold_converse.py` doesn't assert the first two
facts.

## 4. Findings

### Fatal

None.

### Fixable gaps

- **G1. Domain of `tau` when `u` is an N-pole.** Lines 10-17 (Answer) and
  61-69 (part 3) call `tau_p` and `tau_u` partial involutions of `F_u`,
  the fibre of points. When `u` is a pole, both sheets of each regular point
  lie in the one block. So `tau_u` (`g_a` restricted to 2-cycles) fixes every
  point, and `tau_p` doesn't descend to a map on points. The two sheets of a
  point can return to different points. The correct domain is the sheets in
  the block of `u`, with `S~ ~ T~` when some sheet of `S~` reaches some sheet
  of `T~`. Proof step 3 ("determined by its starting sheet") and the code
  already work this way. The fix is to restate part 3 and the Answer on
  sheets. "Partial dihedral action on `F_u`" is accurate only for `u`
  N-regular.
- **G2. Evidence weight of the d61 computation.** Lines 18-20, 162-174, and
  205: the "FC verdict" is a segmented re-simulation of the ground-truth walk.
  It isn't a computation from `L_p`, transport, and `mu`. The 0-disagreement
  result confirms Fact L and Lemma 1, not the algebraic form. The fix is to
  reword section 4, or to cite `d62-review-d61/check_fc.py`, which tests the
  stated form. Also add the `truth_pair` consistency assertion.
- **G3. Quantifiers in the realization lemma.** Lines 270-275: "neither
  Rig(x) ... nor Cut(x) holds" should read "Rig(x) fails for `DP / R_y` for
  both `y` outside `{a, x}`, and Cut(x) holds for no factor". Line 320:
  "When Par(x) fails, `N_x` has no regular point over x" is true
  unconditionally (R3 part 1). The condition is misleading.

### Cosmetic

- **C1.** `fold_converse.py` lines 105-106: `shape` uses neighbour sets, so a
  2-vertex cycle (double edge) is labelled `path`. Such cycles occur on dumb12
  (589 to 670 per 1,000 states in my sample). Only the `shapes` field in the
  JSON is affected. Verdicts are not.
- **C2.** Lines 104-110: proof items "4." and "5." prove parts 5 and 6.
  Renumber them.
- **C3.** Lines 192-195: the tower rows use `N6`'s own corner rule as
  "light". That isn't room light, and `truth_pair` is `n/a`. Say so in the
  table.
- **C4.** Section 6 (lines 307-317): "the whole remaining content of the lit
  side" holds for the orthogonal `W <= 20` target only. The chain also cites
  d46, d52, and d56 for "no pair certified dark", where the certifying factor
  may change with the corner and the lift pair. I did not re-verify that those
  checks allow this mixing.

## Files and CPU

| File | Content |
| --- | --- |
| `check_fc.py`, `log_check_fc.txt` | Algebraic FC versus direct walk |
| `billiard.py`, `log_billiard.txt` | Exact billiard ground truth versus d61 rows |
| `deg_bound.py`, `log_deg_bound.txt` | Degree bound on `N_x` |

Run with `python3 -B <script> [args]`. `check_fc.py ROOM CAP`;
`billiard.py H ROOM JSON`.

CPU: final logged runs about 27 s. Debugging runs, including one failed
assertion run and two repeats, took about 45 s. The total is about
72 s (1.2 CPU-minutes).
