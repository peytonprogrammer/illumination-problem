# d63: the realization lemma

Date: 2026-11-18. Theory plus exact checks on named rooms and on abstract double covers
of their canonical factors. No room, ray, direction, or word search. Tags: **PROVED**
(argument here), **COMPUTED** (exact check here), **CITED** (proved or checked elsewhere),
**GUESSED** (judgment). The d61 proof (Lemma FC) is under separate review; nothing here
depends on it.

## Answer

- **Status: partial.** The lemma isn't proved. It splits into a finite part and an
  infinite part (PROVED). The infinite part is the case `N_x = B`. That case contains
  a per-class form of d14's Lemma H, which is on the dead-end list.
- **It's false as an abstract cover statement.** Two examples from the record break the
  literal d61 wording: d39's cross scaled by 3 (CITED), and d14's six n = 10
  non-transitive relations with no identity corner (derived here from d14's checked
  data, not recomputed). Any proof must use room hypotheses.
- **It doesn't close the whole target, even if proved.** It covers same-class lattice
  marks in normalized rooms. Different-class pairs and non-lattice rational pairs need
  two more lemmas (section 1.3).
- **No counterexample on named rooms (COMPUTED).** There are 530 rows on normalized
  covers: the rooms and their factors. There are 192 more rows on 168 abstract double
  covers of the rooms' `N_x`. Every x-dark row has a Cut certificate, and all of them
  come from cross12. Rig never appears. Total CPU is under 1 s.

## 1. The statement

### 1.1 Exact restatement

Setting: `Q -> B` is a connected genus-0 pillowcase cover with cycle lengths 1, 2, 3.
`G = <g_a, g_b, g_c, g_d>`. Fix a target corner `x != a`.

- `B_x` is the finest `G`-block system that merges every 2-cycle of `g_x`.
  `N_x = Q / B_x` has no regular point over `x` (d10 R3).
- `S~ != T~` are regular points of `Q` over `a`, with one image `u` in `N_x`.
- `U` is the set of sheets in the blocks of `u`. That's one block `beta` if `u` is
  an `N_x`-pole, and two blocks `beta` and `g_a beta` if `u` is `N_x`-regular.

**Realization lemma (RL).** Suppose there's no Rig(x) certificate (via `R_y` with
`y` not in `{a, x}`, which is equivalent by R3) and no Cut(x) certificate (over any
factor). Then some state of the pure-braid orbit has `S~` and `T~` in one component of
the graph on `U` with these edges:

- `{s, g_a s}` for each 2-cycle of `g_a`;
- `{s, g_x s}` for each 2-cycle of `g_x`.

**Lemma 1 (PROVED, independent of FC).** With equal images in `N_x`, the pair is x-lit
exactly when the RL conclusion holds. So RL is "x-dark implies a certificate at x" for
same-class pairs.

Proof. A light path along an arc `a -> x` alternates two moves. From sheet `s` it
crosses the `x`-point of `s` to `g_x s`, which needs a 2-cycle. Then it crosses the
`a`-point to `g_a s'`, which needs a 2-cycle unless that point is `T~`. Each sheet has
at most one edge of each kind, so the components are alternating paths and cycles. The
light path is the walk along one of them.

Now let `s` be in a block `beta` of `U`, and let `p` be the `N_x`-point over `x` that
contains `beta`. Then `p` is a pole or a zero.

- If `p` is a zero, Fact L makes the `Q`-point of `s` a 3-cycle, so the walk stops.
- If `p` is a pole, `g_x` fixes `beta`, so `g_x s` is in `beta`.
- `g_a` maps the blocks of `u` to themselves.

So the walk never leaves `U`. Conversely, every edge inside `U` is a legal step.

### 1.2 Hypotheses the lemma can't drop

- **A room hypothesis.** d61 states RL for any `Q -> N_x -> B` of this kind. That
  wording is false.
  - **(a) Cross scaled by 3 (CITED: d39 claim 1, confirmed by the d43 referee).** `n` is
    108, and every `B_x` and `R_y` is the one-block system (`d43-review-d39/check_cross.log`).
    At the original cross's Cut class, the pair is x-dark. Directions keep their class
    under scaling by 3, so the scaling preserves the darkness. No Par, Rig, or Cut
    certificate exists over the fine `B`. The certificate is a relative Cut over the
    coarse pillowcase. So RL needs `B` to be the coarsest base with `S~` and `T~` over
    corners. For lattice marks in a normalized room, d10 R1 gives that.
  - **(b) The d14 n = 10 relations (derived from CITED data; GUESSED until recomputed).**
    d14 section 4.3 has 18 corner relations where x-lit isn't transitive. The setup:
    - `N` has degree 5 and blocks of size 2.
    - `u_1` and `u_2` are joined by a live path through an `N`-regular `x`-point.
    - The pair `s_1`, `s_2` is x-dark, and `s_1 ~ s_3 ~ s_2` (CHECKED in d14).

    That forces `B_x` to be the one-block system:
    - `N` has a regular `x`-point, so `B_x` isn't the system of `N`.
    - `s_1` and `s_3` are x-lit and distinct, so `B_x` isn't discrete.
    - `N` is the only proper system.

    In the 6 relations where `N` has no identity corner, nothing certifies the pair:
    - Rig can come only from a factor with identity at `y`, and none exists.
    - Cut needs a factor of degree at most 3, and none exists.
    - Par fails, because `B_x` doesn't separate.

    So these are abstract RL counterexamples with `N_x = B`. Recomputing them means a
    lookup in the n = 10 census, which needs Daniel's approval under d61's scope note.
    It wasn't run. These covers are not known to be rooms.

So RL is only plausible with room structure. Section 2 states the room form.

### 1.3 Does RL close the gap left by d61? Only for one pair type

d61 section 6 says RL plus d46, d52, d56, and d16 gives the W <= 20 orthogonal target.
Lemma 1 confirms the step for one pair type: same-class interior lattice marks in a
normalized room over `B`. The argument:

1. A dark pair makes all four lift pairs x-dark for each of `b`, `c`, `d`.
2. Lemma 1, RL, and R3 give a certificate per lift pair and target.
3. d46, d52, and d56 exclude that.

Two pair types fall outside RL (PROVED by inspection of the statements):

- **(G1) Different-class lattice pairs.** `T` lies over `x != a`. Only Rig can
  certify (Theorem U), and RL says nothing here. The missing statement is "x-dark
  implies Rig(x)", with `x` the class of `T`. The certificate side is done (d47
  Prop. 4.1 and d56 Set A). The lit side has only the census through area 16.
- **(G2) Non-lattice rational pairs.** Over `B` these marks aren't over corners. The
  certificate side works over `P_Lambda` with `Lambda >= Z^2 + ZS + ZT` (d47 to d50).
  `DP` over `P_Lambda` has the intermediate pillowcase `B`. So the needed lit-side
  statement is RL over `P_Lambda0`, `Lambda0 = Z^2 + ZS + ZT`. That's the coarsest base
  with both marks at corners, and by the R1 argument it's the only one. Example (a)
  shows the minimality is essential. The coordinator-log plan "rational points are
  lattice points of mP" doesn't work: `mP` isn't normalized, and RL fails on
  non-normalized presentations.

d16 (real to rational) is unaffected.

## 2. Proof attempt

### 2.1 Finite / infinite split (PROVED)

Let `delta` be the block size of `B_x`, and let `z` be the number of zeros of `N_x`.

- **Zeros.** Fact L puts `delta` zeros of `Q` over each zero of `N_x`. So
  `delta * z <= r` (also d52 C5).
- **Pillowcase case.** If `z = 0`, then `N_x` is a pillowcase, so `N_x = B` by R1.
- **Degree.** If `z >= 1`, then `deg N_x <= p_x + 3 z_x <= 4z + 4` (also d52 C10).
  So `n = delta * deg N_x <= 4r + 4 delta <= 8r`.

Corollary: a normalized room with area greater than `8r` has `N_x = B` for every `x`.
At W <= 20 (`r <= 8`), RL has two parts:

- **RL-fin (`N_x != B`).** This is finite: area at most 64, `delta * z <= 8`. A
  d52-style enumeration of the targets `K_x` with `delta >= 2`, followed by the
  per-cover test in `realize.py`, would decide it. d52 enumerated `delta >= 3`,
  `z <= 2` only (1,113 rooms), so the `delta = 2` targets would be new. Not run: it's an
  enumeration and needs approval.
- **RL-B (`N_x = B`).** Here `U` is all sheets, `u` is the one pole of `B`, and
  `S~`, `T~` are any two regular `a`-points. This part is infinite.

### 2.2 What is proved about RL-B

- **Primitive `G` (PROVED reduction).** x-lit is invariant under `M_t`, d14's
  label group. Pure braids fix corner labels, and `M_t` acts within one marked
  orbit. So two inputs give every pair x-lit:
  - Lemma H: `M_t` is 2-homogeneous on the regular `a`-points.
  - E_x: some pair is x-lit.

  With `G` primitive and `n > 3`, Rig needs `g_y = 1`, and Cut is impossible. So
  primitive RL-B is exactly H plus E_x. That's d14's open Lemma H, and "Lemma H via
  monodromy groups" is on the dead-end list. d14 shows that cusp (twist) elements can
  act trivially. So local twist arguments, approach (iii) induction on degree
  included, don't reach it.
- **Imprimitive `G` with `B_x` one block.** Example (b) has this shape, and RL fails
  there abstractly. A room proof must use something (b) lacks. Candidate: d10 R6
  (size-2 systems come from symmetries of `P`) and the reflection `iota`. GUESSED.

### 2.3 Approaches from the brief

- **(i) Split forces a Par-type partition.** This fails as a closure argument
  (PROVED). Let `C` be the union over states of the component relations. Its `G`-closure
  contains every 2-cycle of `g_x`, which is an edge. So the closure is `B_x`, whatever
  the single-state components are. No coarser or finer factor is produced, which
  confirms d61's remark. Example (b) shows a split that no certificate detects.
- **(ii) Connectedness or transitivity of `Q -> B`.** This gives "same `N_x`-image",
  which is already the hypothesis. It doesn't reach a single state.
- **(iii) Induction on `deg(Q -> N_x)`.**
  - **Degree 2 (PROVED, from d14 D3).** RL is equivalent to this: some state puts a
    branch `x`-pole of `Q -> N_x` next to `u`, along `beta` or `g_a beta`. Whether such
    a state exists is a pure-braid question on `N_x` with marked poles. It isn't
    automatic.
  - **Galois case (PROVED).** Let `Q -> N_x` be Galois with group `D`. Both surfaces
    are spheres, and point stabilizers have order at most 3. `B_x` minimal makes `D`
    the normal closure of the `x`-pole involutions. So `D` is `C_2`, `V_4`, or `S_3`.
    For `u` regular, a state lights the pair exactly when `T~` is in
    `<d_1, d_2> S~`. Here `d_1` and `d_2` are the deck involutions at the `x`-poles
    next to `u`. Two distinct involutions light the whole fibre.

### 2.4 Minimal unproved sub-claims

1. **RL-B for rooms (needs a global argument).** Let `P` be a normalized, strictly
   simple orthogonal lattice room with `B_x` the one-block system. Then any two regular
   class-`a` points of `DP` are x-lit, unless Rig(x) or Cut(x) holds. For primitive `G`
   this is Lemma H plus E_x. In general it needs room geometry, because (b) shows the
   abstract form is false. The argument has to act on the pure-braid orbit as a whole:
   for example, the Hurwitz-curve genus in d14 H2, a classification of `M_t`, or a
   room-level visibility argument such as one-cylinder directions per class (d10
   section 4, step 4). Lemma 1 rules out local arguments inside `U`.
2. **RL-fin.** A finite computation (section 2.1).
3. **(G1) and (G2).** These are needed for the full target even with 1 and 2 done.

## 3. Tests (COMPUTED)

`realize.py`: for each named room, each of the 4 corner classes as `a`, and each
level `M` (`DP` and every proper factor `DP/Pi`, each as its own cover of `B`), the
script does the following:

- It computes `B_x(M)`.
- It takes **every** pair of regular `a`-points with one `N_x` image. That includes
  smooth wall points.
- It runs the exact x-lit test over the pure-braid orbit with two marks.
- It checks Rig and Cut over all factors of `M` and asserts that Par is absent (R3).

`double_covers.py`: for each canonical factor `N_x` of cross12, dumb12, R22, and P6 with
`B_x` non-discrete, it builds every genus-0 double cover branched over two poles by
solving a cocycle system over GF(2). It asserts the product relation, then runs the same
test.

| Covers | Rows (equal `N_x` image) | x-lit | x-dark, Cut | x-dark, Rig | Counterexamples | Soundness violations |
| --- | --- | --- | --- | --- | --- | --- |
| cross12 `DP` / factors | 54 / 18 | 42 / 12 | 12 / 6 | 0 | 0 | 0 |
| dumb12 `DP` / N10 | 306 / 54 | all | 0 | 0 | 0 | 0 |
| R22 `DP` | 14 | 14 | 0 | 0 | 0 | 0 |
| P6, P6 (found.json) `DP` | 42 + 42 | all | 0 | 0 | 0 | 0 |
| **Normalized total** | **530** | **512** | **18** | **0** | **0** | **0** |
| of which `N_x = B` | 424 | 406 | 18 | 0 | 0 | 0 |
| of which `N_x != B` | 106 | 106 | 0 | 0 | 0 | 0 |
| L-room (non-normalized; RL not claimed) | 115 | 115 | 0 | 0 | 0 | 0 |
| Double covers of `N_x` (168 built, 32 with rows; N3 of cross12, N5 of R22 and P6) | 192 | 186 | 6 | 0 | 0 | 0 |

Notes:

- The `N_x` that occur are `B` (cross12, dumb12, some R22 and P6 classes), the tromino
  double N3 (cross12), and N5 (R22, P6).
- `delta * z = r` holds with equality in every room where `N_x != B`: R22 (3, 3, 9),
  P6 (4, 3, 12), and cross12 (4, 1, 4). So every zero of `Q` lies over a zero of `N_x`.
- x-lit is transitive on every `N_x`-fibre tested: 0 failures. The named rooms are too
  small to show the d14 phenomenon. The witness depth in the orbit BFS is at most 5.
- Every x-dark row is cross12's Cut through N3 with `N_x = B` (R4).
- The test is weak evidence. The named rooms have small orbits (at most 131 states per
  marked pair), and only 106 rows have `N_x != B`.

## Files and CPU

| File | Content |
| --- | --- |
| `realize.py` | Room and factor test. `python3 -B realize.py [room ...]`. |
| `double_covers.py` | Abstract double covers of the rooms' `N_x`. |
| `realize_*.json`, `log_*.txt` | Rows and per-(level, a, x) summaries. |
| `double_covers.json`, `log_double_covers.txt` | Per-cover summaries. |

Reused: d60 `fh_star.py` (orbit walk, canonical form), `fh_tower.quotient`, d61
`dp_joined` (ground truth), d10 `unified_test` (certificates), and `roomtools`. CPU,
measured with `time`: 0.07 + 0.14 + 0.15 + 0.12 s for the four runs, plus about 0.5 s of
sanity checks. That's under 1 CPU-second in total, run as one process at a time.
