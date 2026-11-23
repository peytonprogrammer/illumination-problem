# d178: review of l1-natural-four-sites.md and l1-natural-marked-poles.md

Notes: `../d95-review-queue/snapshots/1632/l1-natural-four-sites.md` and `l1-natural-marked-poles.md`.
Checks: `checks.py`, log in `checks.log` (`python3 -B checks.py`, under 1 CPU-second). The script loads d146's `Double`, `closure`, `counts`, `wall_gcds`, `stretch` and `cov4181` definitions by executing only the definitions section of `../d146-review-exdescent/checks.py`. It builds 5 named rooms and runs no room, ray, direction or word search.

## Bottom line

**Both notes are sound. Neither moves the L1 area bound.**

- **Four sites.** Every computational claim checks exactly. The refutation is valid: the four-site product, Riemann–Hurwitz and r ≤ 8 don't force a corner-only class or a proper block in the natural action, even for real normalized strictly simple rooms. The Jordan step is valid. The refutation concerns the unmarked implication only. It says nothing about an implication that uses darkness of a marked pair, and the note says so.
- **Marked poles.** The pole counts and the Riemann–Hurwitz identity are correct. binom(r+4,2) is a valid upper bound for Σ binom(f_x,2). The midpoint step has no gap: a clean segment from a start to a swap pole yields an S-to-T billiard path. With midpoint-necessity.md it's in fact an equivalence. The "more than Σ binom(f_x,2) poles" criterion is correctly stated as sufficient only. It's a reformulation of the open reachability lemma, not progress on it.

## Verified items

### Note 1 (four sites)

1. **DB55 stretch rooms.** Rooms are [0,5]×[0,5] ∪ [5,5+ℓ]×[2,3] ∪ [5+ℓ,10+ℓ]×[0,5] with ℓ = p − 50. The p = 53 cell set equals d146's DB55.

   | p | ℓ | n | W | r | Strictly simple | gcd(h), gcd(v) | Type at each of 4 sites | Sign | G |
   |---:|---:|---:|---:|---:|---|---|---|---|---|
   | 53 | 3 | 53 | 12 | 4 | yes | 1, 1 | 1² 2²⁴ 3 | even | A₅₃ |
   | 59 | 9 | 59 | 12 | 4 | yes | 1, 1 | 1² 2²⁷ 3 | odd | S₅₉ |
   | 61 | 11 | 61 | 12 | 4 | yes | 1, 1 | 1² 2²⁸ 3 | even | A₆₁ |

   - The relation g00·g10⁻¹·g11·g01⁻¹ = id holds in all three rooms. This is the note's LB·BR·RT·TL product.
   - Each room is transitive. Each is primitive: for every j, the finest invariant equivalence joining sheets 0 and j is universal. Prime degree gives this anyway.
   - At every site the square of the generator is a single 3-cycle. All four canonical relations B_x are universal.
   - Each 5×5 chamber has 2 interior lattice points of each parity, 8 per parity in total.
   - The general-p argument is also correct. Since ℓ is odd, the four mouth reflexes (5,2), (5,3), (5+ℓ,2), (5+ℓ,3) fall in four different classes. The 8 convex corners fall two per class. gcd(5,ℓ) = 1 because p is a prime other than 5. The sign is (−1)^((p−5)/2).
2. **Ferrers grid widths 5,3,2,1¹¹.** n = 21, W = 10, r = 3, strictly simple, normalized. The four types match the note's table exactly: 00 is 1² 2⁸ 3, 10 is 1³ 2⁹, 11 is 1 2⁷ 3², 01 is 1 2¹⁰. The product is the identity. The (0,j)-closure is universal for all 20 values of j, so the group is primitive. The 00 square is a single 3-cycle and the 10 generator is odd, so G = S₂₁. Interior lattice points are (1,1), (2,1), (1,2), in three different classes. So this room has no same-parity marked pair, as the note says.
3. **c4181s control.** The geometry is defined in d146 as `stretch(stretch(cov4181, 0, 1, 2), 1, 4, 3)`. It's strictly simple, n = 41, W = 20, r = 8, normalized. Types in the order 00, 10, 11, 01 are 1³2¹⁹, 1⁴2⁸3⁷, 1³2¹⁹, 1²2¹⁸3, matching the note. It's primitive, the 01 square is a single 3-cycle, and 00 is odd, so G = S₄₁. It has same-parity interior pairs: 4, 6 and 4 interior points in classes 00, 01, 11.
4. **Logical claim.** The implication "four-site product plus r ≤ 8 forces a corner-only class or a proper block" is false in the natural action. Each room above has a 2-cycle at every site, so no class is corner-only, and it's primitive, so it has no proper block. One room is enough. d146's table already contained such rooms (DB55, DBas, U2 and c4181s are all BBBB with a single block system). The note adds the unbounded prime family and the exact group.
5. **Jordan step.** It's valid. A transitive group of prime degree is primitive. A primitive group containing a 3-cycle contains A_n (Jordan; d81 cites Wielandt 13.3). The squared generator of type 1^a 2^b 3¹ is a single 3-cycle. The four local permutations generate G, so G = A_p if all four are even and S_p otherwise.

### Note 2 (marked poles)

6. **Pole counts, by orbit enumeration on unordered pairs.** The script enumerates every 2-set orbit of every site generator. A 2-set is fixed exactly when the generator swaps its letters (q_x of these) or fixes both (binom(f_x,2)). A 3-cycle fixes no 2-set.

   | Room | n | r | f_x (00,10,11,01) | Σ(q_x+2z_x) = 2n−2 | Swap poles = 2n−2−2r | Σ binom(f_x,2) | binom(r+4,2) | Σ f_x q_x |
   |---|---:|---:|---|---|---:|---:|---:|---:|
   | DB55 p=53 | 53 | 4 | 2,2,2,2 | 104 ✓ | 96 | 4 | 28 | 192 = 4(n−5) |
   | DB55 p=59 | 59 | 4 | 2,2,2,2 | 116 ✓ | 108 | 4 | 28 | 216 = 4(n−5) |
   | DB55 p=61 | 61 | 4 | 2,2,2,2 | 120 ✓ | 112 | 4 | 28 | 224 = 4(n−5) |
   | Ferrers21 | 21 | 3 | 2,3,1,1 | 40 ✓ | 34 | 4 | 21 | 60 |
   | c4181s | 41 | 8 | 3,4,3,2 | 80 ✓ | 64 | 13 | 66 | 182 |

   Σ f_x = r+4 holds in every room. The count of regular Y-points with one convex-corner leg is exactly Σ f_x q_x, as the note says. The value 96 matches the archived R = 96 in shadow-budget.md and midpoint-necessity.md.
7. **The bound binom(r+4,2).** This is the point the brief asked about. f_x is split over four sites, and Σ_x binom(f_x,2) ≤ binom(Σ f_x,2) = binom(r+4,2) by superadditivity. Equality holds only when all r+4 convex corners lie in one class. So the inequality runs in the right direction. The script confirms that binom(r+4,2) is the exact maximum over all 4-part compositions of r+4 for each r ≤ 8. It reaches 66 at r = 8. The named rooms sit far below it: 4, 4 and 13. Swap poles exceed 66 exactly when 2n−2−2r > 66, so n ≥ 43 at r = 8, with 68 swap poles there. That matches the note.
8. **The midpoint step.** It's correct. A swap pole is a 2-cycle (a b) of g_x, so both legs end at one regular Q-point P. In the 2π chart at P the two sheets of the cycle are the rays u and −u, so the legs arrive from opposite sides. Following leg 1 forward and leg 2 backward passes straight through P in Q. That's a straight crossing at an interior point or a legal bounce at a smooth wall point. The legs' open interiors avoid corners by hypothesis. The result is a legal S-to-T path.
   - The start points are all regular on Y. A start is the orbit {a,b}, {a′,b′} of size 2, so no compatibility condition beyond choosing one of the 8 starts is needed.
   - The converse also holds, by midpoint-necessity.md. For same-parity lattice marks the unfolded midpoint (S+T̃)/2 is a lattice point, and a legal path's midpoint is regular. So **the pair is lit if and only if some swap pole is reachable by a clean segment from one of the 8 starts.**
9. **Sufficient criterion.** Reaching more than Σ binom(f_x,2) distinct poles forces at least one swap pole by pigeonhole. The note calls this sufficient and says it doesn't prove L1. That's accurate. Its warning about the Σ f_x q_x regular forbidden points is also accurate (item 6).

## Gaps

### High

None.

### Medium

1. **Note 2's criterion has no traction yet.** Reaching more than Σ binom(f_x,2) poles takes at least that many separate clean segments. That's no easier than reaching one swap pole, which by item 8 is equivalent to lighting. So the 66 bound only helps if some argument produces many clean terminal poles at once, and none is given. The ordered-cover form of the same count is already in midpoint-necessity.md (R = 2d − J and the open reachability lemma). The new content is the bound on non-swap poles, plus the observation that the obstacle set is not bounded by 66.
2. **Scope of note 2.** The construction needs S and T in one pillowcase fiber, so it covers same-parity lattice marks only. That's the BBBB residual named in deletion-invariance.md. It does not cover different-parity pairs or real marks, which are L3. The note should state this restriction next to the criterion.
3. **Note 1 doesn't cite the implication it refutes.** The note never says where "corner-only or proper block" was proposed, or whether that version assumed a dark marked pair. The refutation covers the unmarked statement only. A reader can't check whether a live proof step depended on it.

### Low

4. **Unused hypotheses in note 2.** The criterion doesn't use G ⊇ A_n, n ≥ 21 or the connectedness of Y. The pole counts and the midpoint step hold for any monodromy group. The natural-action framing is harmless, but the criterion is more general than stated.
5. **The bound 66 is arithmetic, not geometric.** Equality needs all convex corners in one class. Normalization forces an odd edge on each axis, which likely spreads corners over at least two classes. A tighter bound was not derived and isn't needed.
6. **The Σ f_x q_x warning undercounts the obstacles.** Other forbidden Y-points over sites have a reflex leg: fixed×3-cycle, 2-cycle×3-cycle and 3-cycle×3-cycle pairs. These are cone points of angle 3π or 6π, and q_x z_x also grows with n. The note's "ordinary forbidden points" wording is accurate, but the full obstacle set is larger than it suggests.
7. **The headers overstate the advance.** Both lines read "Advances: L1". Note 1 is an obstruction to one proof route, and note 2 is a reformulation. Neither gives an area bound. The "Gauge" line in note 1, with the word LLLRLLLRLR, is unrelated to the result, as in d176.
8. **Unchecked side claims.** The claim that "the Ferrers lighting theorem covers this realization" (note 1) was not checked here. The general-p claim for every prime p ≥ 53 was checked by argument (item 1) and computed only at 53, 59 and 61.

## What this means for L1

- The natural-action branch (G ⊇ A_n) can't be closed by cycle-type or block arguments. Real rooms with W = 12, r = 4 realize A_p and S_p at every prime p ≥ 53, with 2-cycles at every site and no blocks. Any L1 argument in this branch has to use the dark pair itself. In practice that means how a clean straight segment transports the marked lifts.
- Note 2 states that requirement exactly. A same-parity lattice pair is lit if and only if one of the 2n−2−2r swap poles on Y is reachable from one of the 8 starts by a clean segment. Only Σ binom(f_x,2) ≤ 66 poles can be false terminal targets. But no mechanism yet makes any pole reachable. So the open reachability lemma of midpoint-necessity.md is unchanged.
- No ledger word moves and no area bound changes. The imprimitive follow-on stays blocked behind the natural branch, as note 1 says.
