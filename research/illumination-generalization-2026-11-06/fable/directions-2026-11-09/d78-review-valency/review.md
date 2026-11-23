# D78: Referee review of the low-valency and three-sheet notes

Date: 2026-11-19. Targets: `.context/qclass-closure/bbbb/low-valency.md` (with `low-valency.py`,
`low-valency.txt`) and `three-sheet.md`. Context read: `midpoint-necessity.md`, d70 `RESULTS.md`
sections 2 and 11, d10 `theory.md` (Fact L, R1), `d10-d12-review/review.md` (R1 correction), d14
`proof.md` sections 3.2 and 3.3.

Own code: `verify.py`, log `verify.log`. It reads only the cell sets (through `cyl.rooms()`) and
the saved pair list `d72-cylinder-test/cyl_H40.json`. It rebuilds the four branch permutations
from cells with its own rule and doesn't call `pair_level` or the `cyl` tuple code. There's no search
over rooms, rays, directions, or reflection words. CPU: about 3 s per run.

Re-run: `cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d78-review-valency && python3 -B verify.py > verify.log`

## Verdict

- **low-valency.md: sound, with minor fixable gaps.** The matching lemma, the degree-2 exclusion,
  and the n > 48 threshold are correct. The defects are wording and stale scope.
- **three-sheet.md: sound, with minor fixable gaps.** The permutation lemma, the reflex-corner
  charging, the thresholds 36 and 120, and the residual 8-sheet case are correct. Both notes depend
  on d14 Theorem G (CFSG, through Burness and Guralnick) and on dictionary D0, and should say so.

No fatal finding.

## 1. Definitions

- **d is well defined.** The marked union is the set of orbits of the full monodromy group
  G = ⟨g_a, g_b, g_c, g_d⟩ on ordered off-diagonal sheet pairs that meet sheets(S) × sheets(T).
  Each mark contributes its four incident cells (two 2-cycles of g_a). d is the sum of the
  distinct orbits' valencies (orbit size / n). It doesn't depend on sheet labels.
- **Match with midpoint-necessity.md.** That note uses "the union containing every pair of
  incident sheets at the two marked fibers (four choices at each physical mark)", ordered S then
  T, with each projection of degree d. This is the same object. `low-valency.py` computes
  exactly that: each orbit is counted once, and closure under generators equals the group orbit.
- **Use.** d ≥ n − 8 gives d ≥ 2n/3 for n ≥ 24, so every regime claimed here feeds the
  r ≥ 5n/12 inequality. The other hypothesis (no regular non-source coincidence) is untouched.

## 2. The size-2 lemma (low-valency.md)

- **Stabilizer step.** G_s has index ≤ 2 in G_B. Its image on the other m − 1 blocks has index
  ≤ 2 in a group containing A_(m−1), and A_(m−1) has no index-2 subgroup. So G_s is transitive on
  the other blocks. Correct.
- **All four pairs or a matching.** Row sums of the 2 × 2 incidence matrix are constant across
  sheets (G transitive) and across target blocks (G_s transitive). Column sums are constant
  similarly, and equal row sums by counting. O is an orbit of the full G, so block swaps by the
  pair stabilizer cause no trouble: the argument never uses that stabilizer. Correct.
- **2-colouring.** f_CB ∘ f_BC and f_DB ∘ f_CD ∘ f_BC are conjugation-invariant up to identity
  versus swap. A_m is 3-transitive for m ≥ 5, so b and t are constants. A triangle plus its
  reversal gives 3b = 2t = 0, so b = 0. Complements of equivariant matchings are equivariant. The
  transported labels define a G-invariant equivalence with two classes of size m. Correct.
- **Degree-2 factor.** A two-part G-invariant partition is a block system. The quotient has
  cycles of length ≤ 2 over every pole, so no zero. It is genus 0 because Q dominates it. A flat
  sphere with only π cone points is a pillowcase. **R1 excludes every intermediate pillowcase of
  every degree**, not only certain ones. The proof uses gcd 1 of edge lengths per axis. That's the
  corrected definition in `d10-d12-review/review.md`, and it matches RESULTS §2.1.
- **Where n > 48 enters.** Each zero of the block quotient N has 2 reflex preimages (Fact L), so
  N has ≤ 4 zeros and the squared pole permutation has 1 ≤ z ≤ 4 three-cycles. Theorem G(a)
  gives A_m or m ≤ max(6z, z²) ≤ 24. So n = 2m > 48. Correct.

## 3. The spare-block lemma (three-sheet.md)

- **Spare-block independence needs no 2-transitivity of G.** It needs the pointwise stabilizer
  of the one or two blocks holding s, t to be transitive on the remaining blocks. The note proves
  it contains A_(m−1) or A_(m−2): the kernel has index ≤ (k!)² and A_(m−2) is simple with order
  greater than (k!)². Correct.
- **Classes.** The relation is G-invariant, transitive (common spare block, m ≥ 4), and every
  class meets every block, so 2 ≤ q ≤ k. The q ≥ 2 step is correct: X = N_D(s) is nonempty and
  G_D-invariant, so X = D, which contradicts properness.
- **Factor or contradiction.** The classes form a block system with q parts of size n/q ≥ m. The
  degree-q quotient is not B, so R1 gives it a zero. By Fact L that zero has n/q distinct reflex
  preimages, so n/q ≤ r ≤ 8. With m > 8 this is a contradiction. The charging is rigorous: zeros
  of Q are exactly the reflex corners, each a single point of the double.
- **Thresholds.** Size 3: z ≤ 2, m ≤ 12, so n > 36 gives m ≥ 13 and (11)!/2 > 36. Uniform:
  per-k minimum n is 50, 39, 52, 50, 72, 98, 120 for k = 2..8. The binding case is k = 8 with m ≥
  15. **n > 120 is correct and conservative by one; n ≥ 120 already works.**
- **Residual.** An external marked pair exists unless all 8 incident sheets share one block, so
  k = 8. Then each quotient zero has 8 reflex preimages, so r = 8 with one zero, and all reflex
  corners lie over one pole. Correct. That pole need not be the marks' class a; the note doesn't
  claim it is.

## 4. Coverage of the case split

Every transitive imprimitive group has a maximal proper block system, and the action on its
blocks is primitive. The argument applies to any such system, so several block systems cause no
gap. A non-maximal size-2 system isn't covered by low-valency.md, but the uniform statement in
three-sheet.md covers it above 120. Gaps remain only at finite areas: n ≤ 64 primitive, n ≤ 120
imprimitive with k ≥ 4, and the residual k = 8 case. three-sheet.md states this.

## 5. Computation

- `low-valency.py` re-run: output identical to `low-valency.txt`.
- `verify.py` rebuilds g_x as two 90° steps about each cell's class-x corner. The steps are
  counterclockwise on the front face and clockwise on the back. It checks that every cycle is a
  lattice-point star of length 1, 2, 3, or 2 per interior half. It also checks genus 0 by
  Riemann–Hurwitz, transitivity, interior marks, same parity, and normalization by wall gcd.
- Results agree with `low-valency.txt` for all 9 rooms and all 747 pairs. For **st279** (n = 56,
  r = 6), the orbital valencies are [1, 54] and d is 54 for 104 pairs and 55 for 16. The unique
  proper block system has k = 2 and m = 28, with 3 quotient zeros (= r/2). The block action is
  2- and 3-transitive. For **dumb12** (n = 20, r = 4), the valencies are [1, 18] and d = 19 for
  all 4 pairs. Its blocks have k = 2, m = 10, and 2 quotient zeros. For **c4181s** (r = 8) and
  DB55, the group is primitive with valency n − 1. No pair has all 8 sheets in one block.

## Findings

1. **Low.** low-valency.md says "the other 743 meet the area restriction". Under n > 48 only 566
   pairs (CR34, DB55, DBw2, st279) qualify. The 743 is correct only for the n ≥ 21 restriction
   of midpoint-necessity.md. Name the restriction.
2. **Low.** The last paragraph of low-valency.md says the unbounded branch is confined to
   k = 3..8 and that k ≥ 3 is not handled. three-sheet.md now handles it above area 120. Add a
   forward link.
3. **Low.** Neither note lists its dependencies. Theorem G(a) rests on Burness–Guralnick
   Corollary 2 (CFSG). The room-to-tuple step rests on D0. The primitive branch's n > 64 also
   comes from d14 "for rooms", which is tagged `[PROVED given D0]`.
4. **Low.** Both notes cite R1 through d10 `theory.md`, which never defines "normalized". Cite
   the corrected statement in `d10-d12-review/review.md` (gcd 1 per axis), since R1 is false
   under the parity-class reading.
5. **Info.** In three-sheet.md, n > 120 can be n ≥ 120. The per-k thresholds in section 3 above
   give finer finite ranges if they matter later.
