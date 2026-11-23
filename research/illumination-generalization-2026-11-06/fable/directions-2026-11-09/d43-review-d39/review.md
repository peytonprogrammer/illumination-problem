# Referee report on d39 (`../d39-mixed-class/astra.md`)

Independent referee, 2026-11-14. I formed the verdicts below from d39, the
d38 review, d36, d10 `theory.md` (sections 0 to 3), and the d10-d12 review
(R4 patch). I did not use the STATE.md summary of d39.

Computation: `check_cross.py` and `check_cross.log` in this directory. It
computes `B_x`, `R_y`, induced cycle types, joins, and separation of the four
endpoint lift pairs for the 12-wall cross scaled by 1, 2, and 3. It runs no
ray, direction, or reflection-word search and no decider. Total CPU time is
about 0.005 seconds.

## Verdict table

| Claim | Verdict |
| --- | --- |
| 1. Fixed-unit per-class necessity fails at r = 4 (cross scaled by 3) | CORRECT |
| 2. Genuine ordinary Cut forces the 12-wall cross, so never in a full triple | CORRECT (two trivial omissions) |
| 3. Essential Rig, r <= 8, corners in >= 3 classes, forces area <= 20 | CORRECT WITH GAP (two unproved assertions; both fixable, fixed below) |
| 4. A full triple in scope reduces to three Par certificates | CORRECT for ordinary certificates (P' = B) only; rests on the cited d9 census |
| 5. Named-room table | CORRECT (cross rows reproduced; 22-wall and P6 rows agree with d38) |

## Most serious problem

**"Fully certified" silently means "certified over the unit pillowcase B".**
d39's own Claim 1 shows that, outside normalized presentations, darkness can
be certified only relative to a coarser pillowcase. The three-corner-class
scope of Claims 3 and 4 contains such presentations. Example: the 22-wall room
scaled by 3 has corners in 4 classes, `r = 9`, and `n = 135 > 5r`. By d36 every
`B_x` and `R_y` is one block. By the Claim 1 pole-fibre count, ordinary Cut is
impossible. Yet the pair is dark, certified by relative Par over the coarse
pillowcase. So Claim 4 says nothing about relative full triples. The scope is
"ordinary certificates", or equivalently "normalized presentations (gcd 1 per
axis)", where R1 gives `P' = B`. STATE.md's wording "within scope, certified
dark pairs reduce to three per-class Par certificates" overstates d39 in the
same way. At `r <= 8` no example is known, so this is a scope error, not a
false theorem.

## Claim 1: CORRECT

- Scaling: `3P` has `n = 108`, `r = 4`, and corners in classes a, c, d
  (confirmed: a and c hold 4 convex corners each, d holds the 4 reflex
  corners, b holds none). A primitive direction `(p, q)` from `S'` meets the
  next lattice point at offset `(p, q) mod 2` in both lattices, so class `c`
  means the same set of directions before and after scaling. c-darkness
  transfers.
- No ordinary Par or Rig: d36's argument needs only `N_x != PC` (so `d >= 2`),
  not separation. With two off-x corner classes it forces `n <= 5r = 20`. So
  `B_b`, `B_c`, `B_d` are one block, and each `R_y` (coarser) is too. The log
  confirms all six partitions are one block.
- No ordinary Cut: a single cycle has length at most 3 (Fact L), so `d <= 3`.
  `d = 1` has no regular A point. At `d = 2`, A must be `(2)`, and the convex A
  corners (poles) have nowhere to go. At `d = 3`, A is `(2,1)`. Cut sends
  every regular A point to the regular point. The pole's fibre is then the 4
  convex A corners, each with `e = 1` (there are no reflex A corners), so
  `delta = 4 != 36`. Correct.
- Relative Cut: `DP' -> D([0,3]^2)` is literally the original `DP -> B`, and
  coarse classes equal fine classes for primitive directions. Correct.

## Claim 2: CORRECT

- No transparent x point: `g_x` has no 2-cycles, `B_x` is discrete, and Par
  separates any `sigma != tau`. Correct.
- `d = 1` is omitted; it fails because B has no regular A point.
- `d = 2`: Cut needs regular points over A and x, so both are `(2)`. The
  single-cycle corner is a third `(2)`. The product forces a fourth
  transposition. Riemann-Hurwitz gives genus 1, which a quotient of a sphere
  can't have. Correct. This replaces R4 step 1's use of R1, which was the only
  normalization dependence in R4.
- `d = 3`: profiles `(2,1)`, `(2,1)`, `(3)`, `(1^3)` follow from Riemann-Hurwitz
  (total ramification 4). Correct.
- R4 steps 2 to 5 and the step 3c patch: I re-read them. Step 2 (iota
  invariance via the orbit of size 3, 6, or 9), step 3a (uniqueness of the
  `S_3` triple), step 3b and steps 4 to 5 (four long-side copies, the cross),
  and step 3c (Z-hexomino copies, short mirrors forbidden) use strict
  simplicity and interior marks, not normalization. The patch still has a
  single author plus one review; I found no error.
- Full triple exclusion: R4 says the pair is the cross pair, which is lit, so
  no full triple can contain genuine Cut. Correct for interior marks. R4 is
  false for wall marks (Z-hexomino), which are out of scope.
- The log agrees: in the cross, `B_b = R_b` is the degree-3 tromino factor
  with types `(2,1)`, `(1^3)`, `(2,1)`, `(3)`, which is the Cut target at c.

## Claim 3: CORRECT WITH GAP

Checked step by step.

- **Seam compatibility.** `R_y` is iota-invariant (R3 part 3, confirmed). A
  zero of N has only zero preimages (Fact L), and zeros of Q lie on the seam,
  so zeros of N are seam-fixed. The fixed set of `iota_N` is nonempty (it
  contains the seam image), so `N / iota_N` is a disc. Correct.
- **At most one conjugate pair of off-seam poles.** Poles and zeros of Q lie
  on the seam, so an off-seam pole of N has only regular preimages with
  `e = 2`. So `delta` is even and each such pole contributes `delta / 2`. Two
  pairs give `2 delta > 2 delta - 2`. Correct.
- **No off-seam poles, "one star".** Every y-point of N is a pole on the
  seam, so a convex corner of `K`. Each cell has one y-corner with walls on
  both edges, so neighbours share the opposite vertex `o`. `o` has 1 to 4
  cells (seam angles `pi/2, pi, 3pi/2`; an interior point is regular). So `K`
  is a cell, domino, L-tromino, or 2 x 2 square. Correct.
  - Gap: d39 disposes of the domino and square in one sentence. I checked
    them. Domino: if A is a flat class, there is one A point. If A is the
    non-y convex class, both A poles are joined through the single regular
    x point. 2 x 2 square: the arc graph is a 4-cycle through regular
    points. The L-tromino needs Lemma F (strict simplicity), as in R5. The
    claim holds without R1.
- **z = 1.** `d = p_y <= z + 4 = 5`, and a zero needs `d >= 3`.
  - `d = 3`: profiles `(1^3)`, `(3)`, `(2,1)`, `(2,1)` are forced. If x is
    `(3)`, N has no regular point over x, so Rig implies Par. Otherwise A and
    x are the `(2,1)` corners (S is regular, so A is not `(3)`). Arc lifts
    correspond to sheets, so components are orbits of `<g_a, g_x>`. The
    relation `g_a g_x = g_w^{-1}` with `g_w` a 3-cycle forces `g_a != g_x`,
    so the graph is the path `p_x - r_a - r_x - p_a`, all live. Correct, and
    planarity is not used.
  - `d = 4`: the extra pole and the zero must share a corner `(3,1)`. The
    rest are `(2,2)`, in `V_4`, which can't produce a 3-cycle. Correct.
  - `d = 5`: no poles off y. Each odd-degree fibre with cycle lengths 2 and 3
    needs an odd number of 3-cycles. One zero can't serve three corners.
    Correct.
- **Area bound.** `z = 0` is excluded by d36's colour argument with `w_y = d`
  (identity at y), given 3 corner classes. `delta z <= r` (each zero of N has
  `delta` distinct zero preimages) and `d <= z + 4` hold. With `delta` even
  and `z >= 2`, only `(delta, z) = (2, <=4)` (`n <= 16`) and `(4, 2)`,
  `r = 8`, `d <= 6` remain. Correct.
- **d = 6.** All 6 poles over y. Zeros split as `(3,3)`, `(2,2,2)`,
  `(2,2,2)`, and Riemann-Hurwitz (4 + 3 + 3 = 10) checks.
  - Gap: "This is the regular `S_3` cover" is asserted. Fix: the cover is an
    unramified orbifold cover of the `(3,2,2)` sphere, whose orbifold group
    is `D_3`, order 6. A connected degree-6 cover is the universal one, so it
    is regular with deck group `S_3`.
  - Point stabilizers over the `(3,3)` corner are `A_3`, which is normal, so
    the one order-3 subgroup fixes both zeros. y is unbranched, so the 6
    poles form a free orbit and split into two `A_3` orbits of size 3.
  - With the zeros at `0` and `infinity`, the seam is a line through 0. It
    contains at most one of `p, wp, w^2 p`, since 120 and 240 degrees are not
    0 or 180. So at least 4 poles are off the seam, giving two pairs, which
    contradicts the bound. Correct.

Conclusion: `n <= 20` for essential Rig, within the stated scope. The scope is
needed: `z = 0` targets with unbounded `delta` occur with fewer corner classes
(cross scaled by 2: every `B_x = R_x` is a degree-2 pillowcase with `z = 0`).

## Claim 4: CORRECT, ordinary certificates only

A full ordinary triple makes the pair dark (Theorem U, `P' = B`). Genuine Cut
is excluded (Claim 2). Essential Rig forces `n <= 20` and `W <= 20`. The d9
census covers all rooms with area at most 20 and `W <= 21`, every same-class
interior pair, with lit verdicts by explicit path. It finds no dark pair. It
was not rerun here or in d39. So every class of every lift pair is certified
by Par, which means each `B_x` separates all four lift pairs. See "Most
serious problem" for the scope.

## Claim 5: CORRECT

`check_cross.log`:

| Presentation | `N_b` | `N_c` | `N_d` | `N_*` | Separates |
| --- | ---: | ---: | ---: | ---: | --- |
| Cross | 3 | 1 | 12 (discrete) | 1 | only `B_d`, all 4 lift pairs |
| Cross scaled by 2 | 2 | 2 | 2 | 1 | none; `R_y = B_y` for all y |
| Cross scaled by 3 | 1 | 1 | 1 | 1 | none |

For the cross scaled by 2, all corners are in A, with types `(3^4, 2^14, 1^8)`.
So a degree-3 Cut target needs a pole fibre of `8 + 3*4 = 20 != 16`, as d39
says. d39 omits `d = 2` there; it fails as in Claim 1. The 22-wall and P6
rows match `../d38-review/check_named.log` (degrees 5, 15, 5, 5 and
5, 5, 5, 5).

## What is established at r <= 8

Assume D0, Theorem U, R3, and R4 (patched), the d36 bound, and the d9 census.
Let P be a strictly simple orthogonal lattice room with `r <= 8` (`W <= 20`)
whose corners occupy at least three parity classes. Let `S != T` be interior
lattice points of one class. Suppose every lift pair has, at each of b, c, d,
a Par, Cut, or Rig certificate over the unit pillowcase B. Then:

- `B_b`, `B_c`, and `B_d` each separate all four lift pairs, and
- `5 <= r <= 8` and `21 <= area <= 5r <= 40`.

For normalized presentations (gcd 1 per axis), R1 makes B the only
pillowcase factor. There, "over B" can be dropped, and the statement covers
every Theorem U certificate.

## What would complete "no room with W <= 20 is dark by any certificate"

1. **Normalized, same-class interior lattice marks.** Either:
   - run a finite canonical-partition check (no ray search) over strictly
     simple rooms with `5 <= r <= 8` and `21 <= n <= 5r`, showing that no
     same-class interior pair has all three `B_x` separating all four lift
     pairs; or
   - prove amalgamation in that range, then cite d2's `r >= 9` for a common
     separating parity factor.

   To also cover non-normalized rooms with at least 3 corner classes, the
   check must enumerate cell sets, not normalized shapes.
2. **Relative certificates (`P' != B`, non-normalized only).** By the R1
   proof, `P'` corresponds to a lattice `Lambda'` containing `gZ x g'Z`. If
   `Lambda'` is rectangular, a relative triple is an ordinary triple of the
   coarser presentation, with the same `r` and area `n / [Z^2 : Lambda']`, so
   you can recurse. A non-rectangular `Lambda'` (G1 type, as in even
   refinements) and coarse presentations with at most 2 corner classes need
   a separate argument.
3. **At most 2 corner classes** (even refinements, rational marks with even
   denominators). The d36 bound and d39's `z = 0` step both fail here (cross
   scaled by 2). You need a lemma that every `z = 0` Par or Rig target is a
   pillowcase factor, with a push-down to the maximal pillowcase via Lemma 0.
   The marks may then be non-lattice points of the coarse lattice, which is
   d16 territory.
4. **Rational marks.** Refining to make marks lattice points puts odd
   denominators in item 1 or 2. The area grows by `k^2`, so for `k^2 n > 40`
   only relative certificates can certify. Even denominators go to item 3.
   So rational marks reduce entirely to items 2 and 3, which are untreated.
5. **Different-class marks** are outside the d35 to d39 programme.

All of this is "dark by certificate". Darkness without a certificate (U\*)
remains open.
