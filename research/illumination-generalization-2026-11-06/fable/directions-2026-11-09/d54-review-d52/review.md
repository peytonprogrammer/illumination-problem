# d54: referee report on d52 (fold enumeration, a second proof at r <= 8)

Opus 5.5 referee subagent, 2026-11-15. Adversarial review of
`../d52-fold-enumeration/memo.md` and its scripts. No room enumeration by
shape, ray, direction, or reflection-word search was run. Every run is a
permutation or cover enumeration, or a check on d52's own covers.

Tags: **PROVED** (argument here), **CITED** (file and line), **COMPUTED**
(script and log in this directory), **GUESSED**.

## Verdicts

| # | Item | Verdict | Confidence |
| --- | --- | --- | --- |
| 1 | Completeness of the reduction to the 106 quotient shapes | CORRECT WITH FIX (wording) | high |
| 2 | The arc and slit cover model, and `enum_P.py` | CORRECT WITH FIX (two proof steps unstated) | high |
| 3 | The separation test | CORRECT | high |
| 4 | Validation | CORRECT; cross-check now complete, 185 of 185 | high |
| 5 | The r = 9 claim | CORRECT WITH FIX (hypothesis must name a target class) | high |
| 6 | Independence | CORRECT as stated; one shared input removable, done here | medium-high |
| 7 | Agreement with d44, d45, d46 | CORRECT, no disagreement | high |

No error changes d52's conclusion. Two statements are worded more broadly
than the code supports (items 1 and 5). Two proof steps of the cover model
are used but not written down (item 2).

## 1. Completeness of the reduction: CORRECT WITH FIX

**Reading of F\*.** CORRECT. d44 (`README.md:67-71`) and d45
(`review.md:64-73`) say: if all three of `phi_b`, `phi_c`, `phi_d` were
Galois, d36.3 and d2 claim 4 give a contradiction, so some *target* class
`x != a` has `delta_x >= 3`, and its `B_x` separates (`d >= 2`). d52 reads
this as "one class with delta >= 3" (memo lines 16-17, C6 at line 51). The
code encodes `x != a` through filter K4 (`analyze_K.py:26`, mark class in
`10, 01, 11` while `x = 00`). **Fix:** C6 and the theorem should say "some
target class `x != a`". At r <= 8 this is only wording. At r = 9 it matters
(item 5).

**F\* holds at every area.** CITED: d45 `review.md:150-152` says d36.3 and
d2 hold with no area limit. So d52 may apply C6 at n <= 20 and at r <= 4,
which d46 never needed. Correct.

**Bounds.** PROVED, each re-derived here:

- `z <= 2`: from C5 (`delta z <= r`, CITED d45 `review.md:79-95`) with
  `delta >= 3`, `r <= 8`. Derived, not assumed.
- `d <= 12` search bound (C10): every cell of K lies in exactly one class-x
  star, and those stars are cvx (1 cell), rfx (3), or cone (2). So
  `d = cvx_x + 3 rfx_x + 2 cone_x <= p + 3z = 4z + 4`, using genus 0
  (`p = z + 4`). Correct. The search reached `d = 12` and found nothing
  above 9, so "d <= 9" is a computed output, not an input.
- `z >= 1`: the code's K3 rejects `z = 0` outright (`analyze_K.py:24`), but
  each of the 6 `z = 0` shapes also fails K2 or K4
  (`logs/analyze_K_r8.log:2`: unit square fails K4, the other five fail K2).
  So the memo's line 76 is right: no citation needed.
- One cone (C4): the d39 argument (`d39-mixed-class/astra.md:69`) uses only
  that off-seam poles have regular preimages with `e = 2` and
  Riemann-Hurwitz (`2 delta - 2`). It applies verbatim to `B_x`. Correct.
- Orbit types (C9): a dihedral orbit is a path of L cells (one g-cycle of
  length L) or a cycle of 2k cells (two g-cycles of length k). C1 gives
  `L, k <= 3`. `k = 3` is an off-seam zero pair, which C3 excludes, because
  a zero's preimages are reflex corners, which are iota-fixed. Correct.

**The search itself.** I read `enum_K.py` line by line. It's a standard
coset-table (low-index) search: slots filled in cell-major order, each slot
is a wall, a gluing to a later cell with a free slot, or a new cell. Every
transitive W-set with `d <= dmax` is reached. Pruning is monotone:
completed orbits stay completed, so `z`, `cone`, `cvx` only grow, and
`partial_ok` only rejects orbits that can't complete to an allowed type.
Mirror images: all 106 shapes are enumerated and searched, so the 56
"modulo mirror" count is only a report. The choice of x: translation by a
unit vector swaps `V0 <-> V1` or `H0 <-> H1` and moves class x to `(0,0)`,
so fixing `x = (0,0)` loses nothing (PROVED).

**Is any admissible shape missing?** None found. COMPUTED
(`checks.py`, `logs/checks.log`): over all 4,275 distinct in-scope covers
from the r <= 8 run, every class y with `delta_y >= 3` and `d_y >= 2` was
normalised to `(0,0)`. All 4,018 such quotients `K_y` are in d52's
127-shape genus-0 list, and all 4,018 are admissible. These quotients were
not built from the list, since only the class x quotient was. This is a
partial, not a full, test of the list's completeness.

## 2. The cover model: CORRECT WITH FIX

**Setting (PROVED).** `B_x` is a W-invariant partition of P's cells (R3.3,
CITED `d10-mechanisms/theory.md:332-334`). P is transitive, so all blocks
have the same size `delta`. So `P -> K = P / B_x` is a W-set map with
fibres of size delta, and K is literally the quotient W-set. No geometric
fold argument is needed.

**Parametrisation (PROVED here, with the two steps d52 leaves out).**
Label cells `(u, k)`. A cover is one bijection per interior edge of K and
one involution per wall slot. Up to relabelling each fibre:

- The cell-adjacency graph of K, with the interior vertices of K as faces,
  is a disc. Its cycle space is spanned by the faces: Euler gives cycle rank
  `E - V + 1 = F`. Cutting the slit (cone to a reflex vertex, through int
  vertices) leaves a connected graph whose cycles are spanned by the faces
  off the slit. So the connection can be made trivial off the slit if and
  only if the holonomy is trivial at every int vertex off the slit.
- **Unstated step 1.** An int vertex of K lifts to dihedral cycles of length
  `4 * (cycle length of its holonomy)`. P allows only 4. So the holonomy is
  trivial. The memo states "trivial elsewhere" (line 123) without this
  reason.
- At an int vertex on the slit, the holonomy is `s_in s_out^{-1}`, so all
  slit edges carry one permutation c. At the cone the lift has length
  `2 * (cycle length of c)`. Only `int` (4) is allowed, so c is a
  fixed-point-free involution. Correct as stated.
- **Unstated step 2.** At a smooth vertex of K the two wall involutions
  `rho_1`, `rho_2` must be equal. Otherwise some `<rho_1, rho_2>`-orbit gives
  a path of 4 or more cells, or a cycle of 6 or more. That's why arcs pass
  through smooth points (memo line 114 states it without proof). At a K
  reflex vertex, both involutions are the identity, since only 3-cell paths
  are allowed. The memo's 3-pi argument covers this case.
- At a convex corner the `<rho_A, rho_B>`-orbits must be cvx, smooth, rfx,
  or int. `corners_ok` imposes this with `P_TYPES`, which excludes `cone`.

**Code.** `enum_P.covers` enumerates every tuple (free rho's, c) whose group
acts transitively on the sheets, up to simultaneous conjugation
(`canon_perms`). Transitivity on sheets is equivalent to P being connected.
So dropping non-transitive tuples discards exactly the disconnected covers,
which is correct. Non-disc results (genus > 0) are discarded after
building (`not_disc`). The `rfx_extra` prune is valid: P's reflex corners
are the `delta z` over K's zeros plus the 3-paths over K's convex corners.
`ngen == 0` returns nothing, which is right for `delta >= 3` (the cover is
disconnected). The slit always reaches a reflex vertex in practice (the
`assert` never fired), and the endpoint choice is harmless because rho = id
there. COMPUTED: the `bad_local` counter is 0 in every case, so the corner
filter fully captures the local constraints.

**True-room test.** `fold.is_room` requires an injective, consistent
developing map, walls exactly where the neighbour cell is absent (no
slits), and no pinch vertex. Genus 0 and transitivity have already been
checked, which excludes holes. That's correct for "strictly simple".
**Note:** the r <= 8 result doesn't depend on this test. Positivity is
tested on every in-scope cover, embedded or not. The test only affects
counts and the r = 9 identification, and there all 3 positives are true
rooms identified with the named 22-wall room by full canonical form.

## 3. The separation test: CORRECT

`fold.positives` tests, for every class a with at least 2 interior points,
every pair `s < t`, and every `y != a`, that the sets of `B_y`-images of the
two lifts are disjoint. That's exactly "all four lift pairs separated"
(Par(y), CITED `d10-mechanisms/theory.md:187-189`). Lifts are taken as
`cells[0]`, `cells[1]` of the 4-cell star, which sit in different
`g_a`-2-cycles. The image of a lift is its `g_a`-cycle on blocks.

Two independent checks, COMPUTED (`checks.py`, `logs/checks.log`):

- `B_y` closed under all of W (d52) equals the d10 definition (closed under
  the rotations `g_x` only), as partitions, for all 4 classes of all 4,420
  covers: 0 mismatches. That's R3.3 confirmed in practice.
- A separate implementation (own union-find over `g_x` only, interior points
  found as pairs of `g_a`-2-cycles swapped by `V_i`, images as orbits on
  blocks) agrees with `positives` on all 4,275 in-scope covers: 0 positives
  from both.

## 4. Validation: CORRECT; cross-check completed

**The 10 unchecked cases (COMPUTED, `run_generic.py`).**

| Case | Generic covers | Arc model | Missing / extra | Positives | Generic CPU-s | Log |
| --- | --- | --- | --- | --- | --- | --- |
| K22 delta 6 | 4 | 4 | 0 / 0 | 0 | 0.4 | `logs/generic_rest_a.log` |
| K22 delta 8 | 7 | 7 | 0 / 0 | 0 | 3.9 | same |
| K41 delta 6 | 4 | 4 | 0 / 0 | 0 | 0.5 | same |
| K41 delta 8 | 7 | 7 | 0 / 0 | 0 | 4.7 | same |
| K44 delta 6 | 4 | 4 | 0 / 0 | 0 | 0.7 | same |
| K44 delta 8 | 7 | 7 | 0 / 0 | 0 | 6.7 | same |
| K29 delta 5 | 70 | 70 | 0 / 0 | 0 | 3.0 | same |
| K29 delta 6 | 232 | 232 | 0 / 0 | 0 | 26.5 | same |
| K29 delta 7 | 270 | 270 | 0 / 0 | 0 | 178.0 | `logs/generic_29_7.log` |
| K29 delta 8 | 115 | 115 | 0 / 0 | 0 | 885.0 | `logs/generic_29_8.log` |

All 185 of 185 (K, delta) cases now agree between the model-free
enumerator and the arc model, with 0 positives from either. The 10 cases
cost about 1,110 CPU-s in total.

**The brute-force check at n <= 9 is weak.** With `delta >= 3` and
`n <= 9`, only `d <= 3` can occur. All 24 incidences are `d = 3`,
`delta = 3`, on the 6 tromino shapes (`logs/validate_brute_n9.log`). It
tests nothing with `z = 2`, `d >= 4`, a cone at `delta >= 4`, or extra
reflex corners over convex corners. It is a valid smoke test and nothing
more. The real validation of the cover model is the generic enumerator,
now complete. The quotient list is validated only partially (item 1).

## 5. The r = 9 claim: CORRECT WITH FIX

**What d52's computation proves (COMPUTED, conditional on Fact L, R3, C4,
and C5, none of which needs r <= 8).** Take an immersed disc W-set with
room-local types, `r <= 9`, and corners in at least 3 classes. Suppose
**some target class `y != a`** has `delta_y >= 3`, and some interior
same-class pair has all four lift pairs separated by each of
`B_b, B_c, B_d`. Then it's the 22-wall room up to lattice isometry, with its
one pair. This holds at any area.

**Fix.** The memo's lines 209-211 say "some class has delta >= 3". If only
the marks' class a has `delta_a >= 3`, the case isn't covered. K4 excludes
`x = a`, and C8 doesn't apply. So the hypothesis must name a target class.
For the 22-wall room itself, `delta_a = 15` (`logs/sanity.log`, `d = 1`),
which shows that `delta_a` can be large and still useless.

**Closing the other branch at r = 9 (new, COMPUTED).** The case in which
all targets have `delta <= 2` is Galois, so d36.3 applies. It uses no
reflex bound (CITED `d36-amalgamation/astra.md:66`). Section 6's enumeration
at `RMAX = 9` (`logs/case_b_r9.log`, 68 CPU-s) gives 519 shapes K_\*, 76 in-scope degree-1 room W-sets, 23 in-scope degree-2 covers, and **0 positives**. None has two interior class-a points. Bounds at r = 9: `delta_* = 1`, `z <= 9`, `d <= 13`; `delta_* = 2`, `z <= 4`, `d <= 6`. With that, the delta hypothesis can be dropped
at r = 9 within pure Par.

**What stays unproved at r = 9.**

- Essential Rig: d39's area bound (`astra.md:81-118`) is for r <= 8, so a
  room certified partly by Rig at r = 9 isn't excluded.
- Cut is fine: d39 claim 2 uses no reflex bound.
- Rooms with at most 2 corner classes, relative certificates, rational or
  different-class marks: out of scope, as at r <= 8.
- Darkness without certificates (U\* is a conjecture).

So "the 22-wall room is the only certified-dark room with 22 walls" is
**not** proved. It is proved for pure-Par certification.

## 6. Independence

**Shared with d46 (both proofs rely on these):**

1. Theorem U soundness and Prop. R3 (d10): the meaning of "positive" and
   the canonical `B_y`.
2. Fact L (d10).
3. C7: the d39/d43 reduction of a full certificate triple to pure Par. This
   includes R4 (patched), d39 claims 2-3, and the **d9 census (area <= 20)**
   for essential Rig.
4. C6/F\*: **d36.3** (Galois implies a chain) and **d2 claim 4**, which rests
   on Theorem 1.1 of `preprints/restricted-minimum-k6` (CITED
   `d2-review/review.md:20-27`). That's the computer-assisted `k <= 6`
   theorem.
5. The zero-fibre count `delta z <= r` (d36.4 / d45 item 3). d46 uses it
   inside F\*. d52 uses it in K3.
6. Scope: strictly simple, at least 3 corner classes, same-class interior
   lattice marks, ordinary certificates over B.

**Independent:** all code (`fold.py` and the rest share nothing with
d44/d46). The enumeration method: quotient side, not room side. d36.4's
`d <= 4z + 1` bound (re-derived as an output). F\*'s area list and its `rho`
filter. The d44 shape DFS and weights. The d9 census for the Par branch at
`n <= 20`. The no-positive part also holds for immersed, slit, and pinched
discs.

**Removing input 4 (sketch PROVED, run COMPUTED, `case_b.py`).** d52 doesn't
need F\* at all if the Galois branch is closed directly:

- Case A: some target has `delta >= 3`. That's d52's enumeration.
- Case B: all three targets have `delta <= 2`. Each `phi_y` is then Galois,
  d36.3 makes `B_b, B_c, B_d` a chain, and the coarsest, `B_*`, separates,
  has `delta_* <= 2`, and has no regular point over any target (a coarser
  quotient of a quotient without regular points has none, by Fact L).
- In `K_* = P / B_*`, put `a = (1,1)`. Summing
  `d = cvx_j + 3 rfx_j + 2 cone_j` over the three target classes gives
  `3d <= 4z + 4`. With `delta_* z <= r <= 8`: either `delta_* = 1`,
  `z <= 8`, `d <= 12` (P = K_*), or `delta_* = 2`, `z <= 4`, `d <= 6`. So
  `n <= 12`.
- COMPUTED (`logs/case_b.log`, 21 CPU-s): 190 shapes K_\*. 43
  degree-1 room W-sets with at least 3 corner classes, and 23 in-scope
  degree-2 covers. **0 positives** by both separation codes. In fact none of
  them has two interior points in class a.

This replaces d2 claim 4 and its computer-assisted `k <= 6` theorem with
d36.3 (a hand proof, d38: CORRECT) and a 21-second enumeration. The shared
inputs then drop to items 1, 2, 3, 5, 6, plus d36.3.

**Possible next step (GUESSED, not run).** Input 3's use of the d9 census
could also be removed. d39 reduces essential Rig to `R_y`-quotients with
`delta = 2, z <= 4` or `delta = 4, z = 2, d <= 5`. The same quotient-cover
enumeration, with the Rig test in place of Par, would cover them.

## 7. Agreement with d44, d45, d46: CORRECT

COMPUTED (`logs/checks.log`):

- Every in-scope cover with `5 <= r <= 8`, `n >= 21` has a `delta >= 3`
  class with `d >= 2`, and passes F\* (re-typed from
  `d44-cert-check-sizing/filter_rate.py:12-30`): 2,845 of 2,845. A
  rejection would have meant an error in F\* or in d52. None occurred.
- On every `delta >= 3`, `d >= 2` quotient (4,018): d36.4's
  `d <= 4z + 1` (`4z` if even), `delta z <= r`, and the fibre count
  `sum floor(rho / delta) >= z` all hold.
- Areas seen at `5 <= r <= 8`, `n >= 21`: r = 5 {25}; r = 6 {21, 24, 25,
  27, 30}; r = 7 {21, 24, 25, 27, 28, 30, 35}; r = 8 {21, 24, 25, 28, 30,
  32, 35, 36, 40}. Every one is in F\*'s list. Only area 27 at r = 8 is
  allowed but not realised. That's consistent, since F\* is a necessary
  condition.
- Rooms outside F\*'s areas: all have `n <= 20` or `r <= 4`. That's outside
  d44/d46's range (d46 relies on d9 there) but inside d52's. So no conflict:
  d52 covers a strict superset of d46's range for the Par step.
- Counting note: the memo's 4,710 / 4,541 count covers per (K, delta) case,
  with repeats across cases. Distinct W-sets number 4,420 / 4,275. The memo
  then reports 1,744 up to isometry. Not an error, but "4,710 covers" isn't
  a count of distinct rooms.

## The statement I would sign

**r <= 8.** Let P be a strictly simple orthogonal lattice room with
`r <= 8` whose corners lie in at least 3 parity classes. Assume Theorem U,
R3, Fact L (d10), d36.3, and the d39/d43 reduction (which uses the d9
census for essential Rig). Then no two distinct interior lattice points of
one class are dark by Par, Cut, or Rig certificates over the unit
pillowcase. The proof is d52's quotient-cover enumeration (Case A) plus
this report's Case B enumeration, at every area. It doesn't need d2
claim 4, F\*, or d46. With d2 claim 4 in place of Case B, it's d52's proof
as written, and it agrees with d46 on d46's range.

**r = 9.** Under the same inputs except the d39/d43 Rig reduction, the
following holds. Any strictly simple room with `r = 9`, corners in at least
3 classes, and a same-class interior pair certified dark by three Par
certificates is the 22-wall room, up to lattice isometry, with its one
pair. The proof is d52's r = 9 enumeration for a target class with delta >= 3, plus this report's Case B run at r = 9 (d36.3) for the rest. It uses neither d2 nor F\*. Rooms certified with essential Rig at r = 9 are not
covered.

## Compute and files

| Run | CPU-s |
| --- | --- |
| `checks.py` (items 1, 3, 7) | 15 |
| `case_b.py 8` | 21 |
| `case_b.py 9` | 68 |
| `run_generic.py`: 8 small cases plus one timing probe | 51 |
| `run_generic.py 29:7` | 179 |
| `run_generic.py 29:8` | 891 |
| Failed starts (setrlimit errors) | under 1 |
| Total | about 1,225 (20.4 min) of the 30-minute cap |

Processes: at most 2 at once. Peak RSS 28 MB. Output in this directory: 208 KB. Files in
this directory only.

| File | Role |
| --- | --- |
| `fold.py`, `enum_K.py`, `enum_P.py`, `analyze_K.py`, `validate_generic.py`, `validate_brute.py`, `named.py` | Copies of d52's scripts. Only change: CPU limits set soft-only, so modules can be imported together. |
| `checks.py` | Items 1, 3, 7: B definitions, independent separation test, K_y membership, d36.4 and F\* on every cover |
| `run_generic.py` | Item 4: the 10 remaining model-free cross-checks |
| `case_b.py` | Item 6: the Galois branch without d2 (`RMAX` 8 and 9) |
| `logs/*` | Every run quoted here |
