# d50: referee report on d49 (even-index pillowcase bases)

Referee: Opus 5.5, 2026-11-14. Memo under review: `../d49-even-index/memo.md`.
Theory, plus read-only checks on two named rooms (`check_d50.py`,
`check_d50.log`, 0.03 CPU-s, one process) and a rerun of
`../d49-even-index/check_even.py` (output matches `check_even.log` except
the CPU line). Arithmetic on stored census tables
(`../d9-census-w22/partA-totals.json`), no enumeration.

Tags: **PROVED** (argued here), **CITED** (from the named file, not
rechecked), **GUESSED** (estimate). Notation follows d47, d48, d49.
`Lambda'' ` is the lattice of a zero-free factor `N = P_{Lambda''}`, with
`Z^2 <= Lambda'' <= Lambda` and `d = [Lambda : Lambda'']`.

## Verdicts

| Item | Verdict | Confidence |
| --- | --- | --- |
| 1a. m = 2 bound (`n_R <= 2r`) | CORRECT WITH FIX: claim true, cited proof doesn't cover Par | 90% |
| 1b. m >= 4 step | CORRECT WITH FIX: zero-free Cut omitted, bound unchanged | 85% |
| 1c. Non-dyadic step | CORRECT WITH FIX: `Lambda'` must contain `rho M_0` | 85% |
| 2. Lemma R0 and consequences | CORRECT | 90% |
| 3. Lemma Z, Z', shape list | CORRECT WITH FIX: "Cut forces d = 3" is false as worded | 90% |
| 4. Witness lemma | CORRECT WITH FIX: "classes" must mean mod `2 Z^2`; Cut isn't lattice-only | 85% |
| 5. Closure for lattice marks | CORRECT WITH FIX: citations mislabelled, logic sound | 85% |
| 6. r = 9 | CORRECT: the argument stops where it should | 90% |
| 7. Finite check | Room set is 2.2x too large; (b) is already closed; spec below | 75% |

Errors found, by location in `memo.md`:

- Line 114-115: "sections 3-4" don't prove the non-V claim for Par (item 1).
- Line 33: `Lambda' = Lambda_(2) + M_0` can miss `rho S` (item 1c).
- Line 49: "Cut forces d = 3" holds only with a zero; zero-free Cut has
  `d = 2` (item 3).
- Line 52: the vertex-only class is the target `x`, not the cut class
  (item 3).
- Line 120: "lattice marks are excluded" plays no role; `m >= 6` comes
  from the 2-part (>= 2) times the odd part (>= 3).
- Lines 151-153: "10 <= W <= 20 ... Count 2,052,226" includes the 234
  W = 8 rooms; the 10-20 count is 2,051,992. Both ignore the memo's own
  bound `n_R <= 2r` (item 7).
- Line 128-129: Part A's "class (i)/(ii)" is the one-cylinder classification,
  not a corner-class count (item 5).

## 1. Section 5 bounds

### 1a. m = 2: CORRECT WITH FIX

Section 3 gives no zero-free Rig at `m = 2` (R0) and no zero-free Cut at a
non-V target. For Par, section 3 says only that zero-free Par is lattice
data, and section 4 is whole-pair. Neither excludes zero-free Par at a
non-V target. Section 4's own counterexample shows lattice-data Par can
certify a single target. So the cited proof has a gap.

**Repair (PROVED).** A zero-free `N` is `P_{Lambda''}` with
`Z^2 <= Lambda'' <= Lambda` (d47 Prop 1.1, d48 item 4), so `d` divides `m`.
At `m = 2`, `d` is 1 or 2.

- `d = 1`, `N = P_Lambda`. Par fails: `c_s = c_t` gives
  `phi(sigma) = phi(tau)`. Rig fails: the graph is one edge, and both ends
  are live through `sigma` and `tau`. Cut fails: `sigma` maps to a pole.
- `d = 2`, `N = P_{Z^2} = B_R`. Its four corners are the classes of `Z^2`,
  which map into `V`. Over a non-V corner `x`, `N` has one regular point,
  so Par(x) fails. Cut(x) at `d = 2` needs every `Q`-point over `x` to be
  a vertex, but no vertex lies over a non-V class. Rig fails by R0
  (`d != 4`).

So at `m = 2` every certificate at a non-V target has a zero, and Lemma Z'
gives `n <= 4r`. For `c_s != c_t` with `c_t` in `V`, only Rig applies, and
R0 forces a zero; Rig with a zero has `n <= 4r` at any target (item 3).
Hence `n_R <= 2r <= 16`. PROVED.

**The restriction to m = 2 is essential (PROVED).** At `m = 4` zero-free
Par can certify a non-V target. Take `Lambda = (1/2) Z^2`, so `V = {0}`,
and `Lambda'' = (1/2) Z x Z`. The corners `0, (1/2,0), (0,1), (1/2,1)` of
`P_{Lambda''}` lie over classes `0, x, 0, x` with `x = (1/2, 0)`. So
`N` has 2 poles and no regular point over the non-V corner `x`. With
`T = S + (0, 1)`, `S` and `T` agree mod `2 Lambda = Z^2` and differ mod
`<2 Lambda'', -1>`, so Par(x) holds in every room. That is why `m >= 4`
needs the witness lemma.

**Run check.** Section 4's counterexample on the cross, `S = (1,2)`,
`T = (2,2)`, `Lambda = (1/2) Z x Z`: Par at the V target `d`
(`d = 2`, `z = 0`) separates all four lift pairs; targets `b` and `c` have
nothing (`check_d50.log`). This matches the repair.

### 1b. m >= 4: CORRECT WITH FIX

The witness lemma transfers zero-free Par and zero-free Rig, which are
lattice data (item 4). It doesn't transfer zero-free Cut, which needs a
vertex-only target class. So the conclusion is "some target has a
certificate with a zero, or a zero-free Cut". The second case has
`n <= 4r + 4 <= 8r` (Lemma Z), so `n_R <= 8r/m <= 2r` stands. PROVED.

### 1c. Non-dyadic marks: CORRECT WITH FIX

- The reduction needs all four lifts in `Lambda'` (d48 item 1). With
  `Lambda' = Lambda_(2) + M_0` this can fail. Example: `S = (1/3, 1/3)`,
  `T = S + (1, 0)`, `Lambda = (1/3) Z^2 + (1/2) Z x Z`. Then
  `rho S = (1/3, -1/3)` is not in `Z^2 + Z S`. Fix: put
  `Lambda' = Lambda_(2) + M_0 + rho M_0`. `[Lambda : Lambda']` is still
  odd, because `Lambda' >= Lambda_(2)`. PROVED.
- Per lift pair, use `M = Z^2 + Z sigma~ + Z tau~` with
  `sigma~ in {S, rho S}`, `tau~ in {T, rho T}`. Lemma 3.2 needs only the
  two lifts in play.
- `m' = [Lambda' : Z^2]` is `2^k` (k >= 1, since `m` is even) times the odd
  part of `[M : Z^2]`, which is at least 3 for non-dyadic marks. So
  `m' >= 6`. Lemma Z and item 1b give `m' n_R <= 8r`, so
  `n_R <= floor(8r/6) <= 10`. "Lattice marks are excluded" plays no role.
  PROVED.

## 2. Lemma R0: CORRECT

Full argument (PROVED). Zero-free Rig(x) with identity at `y`: `p_y = d`,
`p = 4`, so `d <= 4`.

- `d = 1`: no separation (item 1a).
- `d = 3`: every class has odd `p_j >= 1`, so `p >= 3 + 3 = 6 > 4`.
  Impossible.
- `d = 2`: `p_y = 2`, and one other class has 2 poles. In each of the three
  placements, `Gamma_alpha` is a 2-cycle or a path pole-regular-pole. Every
  vertex is live (poles over `c_s`, `c_t` carry `sigma`, `tau` with
  `e = 2`). The graph is connected, so nothing separates.
- `d = 4`: `p_y = 4`, and all other fibres are two regular points. All four
  corners of `P_{Lambda''}` lie over `y`. The corner `0` of `Lambda''` lies
  over class 0, so `y = 0` and `Lambda'' <= 2 Lambda`. Index 4 forces
  `Lambda'' = 2 Lambda`. `Lambda'' >= Z^2` gives `Lambda >= (1/2) Z^2`, so
  `4 | m` and `V = {0}`.

Consequences: `m = 2` has no zero-free Rig (`4` doesn't divide 2). Lattice
marks have `c_s = 0 = y`, which Rig forbids. Every vertex of `Gamma_alpha`
is regular, so liveness is room-independent. PROVED.

## 3. Lemma Z and Z': CORRECT WITH FIX

- `w_j = p_j + 3 z_j`, so `sum w_j = p + 3z = (z + 4) + 3z = 4z + 4`.
  Correct. Par: `d = w_x <= 4z + 4 <= 8z`, and `delta z <= r` gives
  `n <= 8r`. Rig: `d = p_y <= z + 4 <= 5z`, `n <= 5r`. PROVED.
- **Cut wording.** A single cycle at `w` has length at most 3 (Fact L), so
  `d <= 3`. `d = 1` fails (`sigma` over a pole). `d = 3` puts a 3-cycle,
  that is, a zero, at `w`. `d = 2` is zero-free: `w` has one regular point,
  `c_s` has no pole (else `sigma` maps to one), so `x` and the fourth class
  carry the 4 poles. Then no regular point of `Q` lies over `x`. So "Cut
  forces d = 3" is true only with a zero, and the vertex-only class is the
  target `x`. The bounds `3r` and `4r + 4` stand. PROVED.
- **Lemma Z'.** At a non-V target, `z_x = 0`, so Par has `d = p_x <= z + 4`.
  Rig has `d = p_y <= z + 4` at any target. So `n <= delta (z + 4) <= r +
  4r/z`. At `z = 1`, `d = 5` puts all 5 poles at one class. The zero class
  has `w = 3`, and the other two have `w = 0`, which is even against odd
  `d`. Dead. `d = 4` gives `n = 4 delta <= 4r`. `z >= 2` gives `n <= 3r`.
  Cut with a zero gives `3r`. So `n <= 4r`. PROVED, and the Rig half needs
  neither `c_s != c_t` nor a V target.
- `shapes_exact.py` scans `n <= 5r`. That range suffices only because of
  the `d <= z + 4` bound above, which the memo doesn't state. Its output
  (max `n = 32` at `(delta, d, z) = (8, 4, 1)`) agrees with the hand
  argument. PROVED (arithmetic).

## 4. Witness lemma: CORRECT WITH FIX

- **Lattice data (PROVED).** For a room with a vertex at the origin, the
  map `Q -> P_{Lambda''}` is the identity chart on the front face and `rho`
  on the back (d48 item 3), up to a deck translation by `2 lambda`,
  `lambda` in `Lambda`, which doesn't change separation. So zero-free Par
  and zero-free Rig depend on `Lambda`, `Lambda''`, the lift pair, and
  `S`, `T` **mod `2 Z^2`**. Classes in `Lambda / 2 Lambda` are not enough.
  Fix the wording at memo lines 78-80 and 93.
- **Witness (PROVED).** `[-2K, 2K+1]^2` minus the unit notch, translated by
  `(2K, 2K)`, has integer vertices and a vertex at the origin. Place
  `S' = S + 2a`, `T' = T + 2b` in `[-2K+1, 2K-1]^2`, distinct. Any residue
  mod `2 Z^2` fits there, so no mark is forced near the notch. Front-front
  and back-back pairs use the straight segment inside the convex square.
  Front-back pairs use one bounce off `y = -2K`, which hits the wall
  strictly between its end vertices. Admissibility (`S, rho S, T, rho T` in
  `Lambda`) is unchanged by `2 Z^2` shifts.
- **Scope.** Zero-free Cut needs a vertex-only target class, which is room
  data. It isn't covered, and item 1b handles it.

## 5. Closure for lattice marks: CORRECT WITH FIX

What the cited documents say (CITED):

| Input | Source | Coverage |
| --- | --- | --- |
| Same-class interior lattice pairs | `../d9-census-w22/README.md` lines 9-21 | W <= 22, area <= 20, 945,070,200 rooms; one dark pair, the 22-wall room (W = 22). Paths double-traced |
| Different-class interior lattice pairs | `../d9-census-w22/partA-README.md` lines 10-15 | W <= 22, area <= 16, 12,786,778 rooms, 6,258,116 pairs, all lit, `verify_plane` checked |
| "Class (i)/(ii)" | `partA-README.md` lines 16-27, 43-51 | One-cylinder classification: (i) a certified one-cylinder direction with `X = Z^2`; (ii) with `X` larger, all `|X / Z^2| = 2`. Not about corner classes |
| W <= 8 | `../d15-small-r/theorems.md` lines 5-9 | r <= 2: every real interior pair lit, proved |

- "All real pairs lit" for class (i)/(ii) is a proof plus a computation:
  Lemma A and Theorem B (d3 audit, accepted in `d3-review`) reduce it to
  the shooting of the `X`-pairs, which `verify_plane` checked. CITED.
- Rooms with at most 2 corner classes are never normalized (d47 Lemma 1.3).
  Part A lists them as the 1,060 "reduced" rooms and skips them. Residue E
  works with the normal form `R` and an even `Lambda`, so that input isn't
  needed.
- **Logic (PROVED from CITED).** Lattice marks give `M_0 = rho M_0 = Z^2`,
  so the reduction yields `m' = 2^k`, and item 1 gives `n_R <= 2r <= 16`.
  Both censuses then show the pair lit. One lit lift pair can't carry a
  full Theorem U certificate. So not all four lift pairs are certified.
  W = 20 rooms of area 17 to 20 never arise, because `n_R <= 16`. The d15
  input is redundant here.
- The same argument works per lift pair, each choosing its own even base.
  With odd bases mixed in, d48's per-lift-pair statement covers the rest,
  except D20 when every lift pair uses `Z^2`.

## 6. r = 9: CORRECT (nothing proves too much)

- The bounds give `n_R <= 2r = 18` at r = 9. The 22-wall room
  (`n_R = 15`) passes them. The closure then needs the census, and the
  census reports this pair dark (W = 22). The argument stops there.
- Its certificate is over `Z^2` (m = 1, odd), outside Residue E.
- The room scaled by 2 has normal form `R` and unit base
  `(1/2) Z^2` (m = 4). Its darkness comes from the coarser odd base `Z^2`
  (d47 section 8), which d49 doesn't touch.
- Run (`check_even.log`, reproduced): at m = 2 only the V target is
  certified (Par, `z = 3`, `d = 10`, `delta = 3`). A non-V Par with
  `z = 3` would need `p_x = 10 > p = 7`, so this is consistent with Lemma
  Z'. At m = 4 nothing is certified. Zero violations of Z, Z', R0.

## 7. The finite check

### Corrections to d49 section 8

- The memo proves `n_R <= 2r` for every even `m`, but its room set uses
  `n_R <= 16` for every W. With the r-dependent bound, the class (iii)
  normalized rooms are (arithmetic on `partA-totals.json`, PROVED):

  | W | r | area range | rooms | max even m |
  | --- | --- | --- | --- | --- |
  | 10 | 3 | <= 6 | 0 | - |
  | 12 | 4 | <= 8 | 22 | 4 |
  | 14 | 5 | <= 10 | 287 | 4 |
  | 16 | 6 | <= 12 | 3,875 | 4 (one area-8 room: 6) |
  | 18 | 7 | <= 14 | 59,893 | 4 |
  | 20 | 8 | <= 16 | 881,807 | 4 |
  | total | | | 945,884 | |

  Non-dyadic marks need `n_R <= floor(8r/6)`. That leaves one room
  (W = 16, area 8) and only index-6 bases.
- Part A already shot every (1/2)-grid pair in the 200,686 class (iii)
  rooms of area <= 14 (81,894,589 pairs, all lit; CITED). That covers
  every index-2 base and `(1/2) Z^2` for 108,037 of the 945,884 rooms.

### Residue (b) is already closed (PROVED from CITED)

Odd `m >= 3`, per lift pair, marks outside `Lambda_r`:

- Zero-free certificates don't exist (`d | m` is odd; Par needs `d` in
  {2, 4}, Rig needs 4, Cut needs 2).
- All four classes lie in `V`, so d36's colour argument applies verbatim.
  It uses only that vertex images occupy at least 3 classes
  (`../d36-amalgamation/astra.md` lines 82-96). Par gives `n <= 5r`, Rig
  and Cut less.
- `m >= 5` needs `n_R <= r`. No class (iii) room with `W >= 10` is that
  small (the smallest have area 8 at W = 10).
- `m = 3` needs `n_R <= floor(5r/3) <= 13`: 3,801 class (iii) rooms, all
  of area <= 14. Every index-3 lattice lies in `(1/3) Z^2`, and Part A lit
  every (1/3)-grid pair in those rooms (706,262,468 pairs, CITED).
- W = 8 is d15; classes (i) and (ii) are Part A Task 2.

So (b) drops out of the job. Keep a 1% sample in the job as a
regression test.

### Merged job specification

**Rooms.**

- Set A (D20): strictly simple, W = 20, area 20; 169,672,127 rooms up to
  symmetry (CITED). All are normalized (d48 item 2).
- Set E: normalized class (iii) rooms with `12 <= W <= 20`,
  `n_R <= 2r`; 945,884 rooms. List: Part A class (iii) output, or re-run
  `partA-enum` plus the one-cylinder classifier for areas <= 16.

**Bases and marks** (origin at a vertex; `sigma~ in {S, rho S}`,
`tau~ in {T, rho T}`).

- Set A: `Lambda = Z^2` only. Marks: interior lattice points `S`, `T` with
  `T - S` not in `2 Z^2`.
- Set E: all `Lambda >= Z^2` with `[Lambda : Z^2]` in {2, 4}: 3 of index 2,
  `(1/2) Z^2`, and 6 cyclic of index 4, so 10 lattices. Add the index-6
  lattices for the one W = 16, area-8 room. Marks: distinct interior
  points `S`, `T`, not both in `Z^2`, with `sigma~, tau~` in `Lambda` for
  some lift pair. Skip pairs inside `(1/2) Z^2` when `n_R <= 14`.

**Per-item test.**

- Primary (illumination): shoot each `(room, S, T)` as Part A does
  (room scaled by the mark denominator, `p + q <= 40`, then 120), and
  re-check every path with `verify_plane`. A lit pair ends the item: by
  Theorem U soundness no certificate system covers it.
- Fallback (certificate), on survivors and on a 1% random sample of all
  items:
  - Build `Q -> P_Lambda` as a block system on the refined sheets
    (`../d48-review-d47/check_transfer.py`).
  - Per `(room, Lambda)`, compute `B_x` and `R_y` for all four corners
    (d10 R3). Per lift pair and target, test Par, then Rig with the live
    graph (d48 item 2 steps 3-5).
  - Test Cut only where Lemma Z allows: `n <= 3r`, or `n <= 4r + 4` with a
    vertex-only target class. Enumerate degree-2 and degree-3 factors
    (`unified_test.cut`).
  - Flag a lift pair when every target is certified, and a pair when all
    four lift pairs are flagged.
  - Lemma tripwires: a separating zero-free Rig with `d != 4` or
    `Lambda` not containing `(1/2) Z^2`; a non-V certificate with a zero
    and `n > 4r`; a D20 separation with `(delta, d, z) != (4, 5, 2)`.

**What a positive means.**

- A flagged pair is a certified dark pair in a room with `W <= 20`. That
  contradicts the 22-wall-minimum target. Re-decide it with `orbitc`
  before believing it.
- A tripwire hit refutes a d47, d48, or d49 lemma.
- A pair that survives shooting at bound 120 but isn't flagged is
  unresolved, not dark. Send it to the orbit decider.
- Expected: 0 positives, 0 tripwires, few or no survivors (GUESSED).

**Size (GUESSED, basis given).**

| Part | Items | Basis | CPU |
| --- | --- | --- | --- |
| A, enumerate | 2.3e10 fixed polyominoes of area 20 | d9 did area <= 20 in two batches of about 14 min wall (`README.md` line 213) | 3-8 CPU-h |
| A, shoot | 1.5e8 to 5e8 different-class pairs | Part A ratio of diff/same pairs at W = 20, area 15-16 is 9.6-12; same-class at area 20 is 51,360,364 | under 1 CPU-h at about 2 us per pair |
| E, shoot | about 1.3e10 pairs (1.4e4 per area-16 room, fewer below) | point counts in `(1/4) Z^2` lattices; Part A grid run shot about 7.9e8 pairs in 1,115 CPU-s | 7-20 CPU-h at 2-5 us per pair |
| E, certificate on everything instead | 1e7 `(room, Lambda)` precomputes, then 5e10 lift-pair lookups | d46 check cost 1.57 us per room at n <= 40; lookups about 0.05 us | 1-4 CPU-h |
| Total, primary design | | | about 12-30 CPU-h |

**Illumination versus certificate.** The certificate check on all of set E
is about 5x cheaper, because partitions are shared across marks. On set A
the costs are equal: enumeration dominates both. The illumination check is
stronger:

- A lit verdict needs only Theorem U soundness.
- The certificate check also relies on R3 canonicity, the live-graph rule,
  and the Cut enumeration being complete.
- A lit verdict decides the pair outright, which the darkness question
  needs.

Recommendation: shoot first, and run certificates on survivors plus a 1%
validation sample.

## The statement I would sign

**Theorem (computer-assisted).** Let `R` be a normalized, strictly simple
orthogonal lattice polygon with `W <= 20`, a vertex at the origin. Let
`S != T` be interior points of `R`, and let `Lambda >= Z^2` have even index
and contain `S`, `T`, `rho S`, `rho T`.

1. If `S` and `T` are lattice points, the four lift pairs of `(S, T)` are
   not all certified by Par, Rig, or Cut over `P_Lambda`. This also holds
   when each lift pair chooses its own even-index base. PROVED from CITED
   d10 (Theorem U, Fact L, R3), d47 Prop 1.1 and Lemma 3.2 with the d48
   fix, d9 phase 1, and d9 Part A Task 1.
2. If `S` or `T` is not a lattice point and all four lift pairs are
   certified, then `n_R <= 2r` and the index of the reduced base
   `Lambda_(2) + M_0 + rho M_0` is 2 or 4 (6 for a single W = 16 room).
   `R` is one of the 945,884 class (iii) rooms in the table above. Rooms in
   classes (i) and (ii) and `W <= 8` are excluded by CITED Part A Task 2
   and d15.

Not claimed: anything at `W >= 22`, and non-lattice marks before the job
runs.

## What I ran and what I reasoned

- Ran `check_d50.py` (0.03 CPU-s): the section 4 counterexample on the
  cross over `(1/2) Z x Z`, and the interior test for 22-wall candidates
  (none of `(1,2)`, `(2,0)`, `(2,1)` is interior, so no 22-wall run).
- Reran `check_even.py`: identical to `check_even.log` except CPU time.
- Read `partA-totals.json` for per-(W, area) class (iii) counts
  (arithmetic only).
- My first run wrote `d10-mechanisms/__pycache__/unified_test.cpython-315.pyc`.
  I deleted it and reran with bytecode writing off. The file was not
  present before.
- Reasoned: everything else, including the m = 4 non-V Par example, the
  witness geometry, closure of residue (b), and all size estimates.
