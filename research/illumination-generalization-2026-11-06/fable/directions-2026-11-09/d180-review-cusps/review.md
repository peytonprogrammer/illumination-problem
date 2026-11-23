# d180: review of l1-swap-cylinders.md and l1-marked-cusp-frequency.md

Notes: `../d95-review-queue/snapshots/1906/l1-swap-cylinders.md` and `l1-marked-cusp-frequency.md`. Context: `l1-swap-pole-averaging.md` in the same snapshot.
Checks: `checks.py`, log in `checks.log` (`python3 -B checks.py`, 0.05 CPU-seconds, 0 failures). The script loads d146's `Double` model the same way d178 and d179 do. It copies the exact Fraction tracer `trace()` from `../d175-review-windinglimits/checks.py`. It uses 2 named rooms (DB55 stretch at p = 53, and U2 from d69 and adjacent-cylinders.md) and 7 named mark pairs. It runs no room, ray, direction or word search. Sources: arXiv math/0602394 (Hubert–Schmoll–Troubetzkoy) pages 1–5 and §8, and arXiv 1208.0131 (Fisher–Schmidt) pages 1–3.

## Bottom line

**Both notes are correct. Neither advances L1. The cusp-frequency note restates the reachability lemma, and the equal-depth criterion is a special case of a formula already in adjacent-cylinders.md.**

- Every computational claim in the swap-cylinders note checks exactly at p = 53. The 6 horizontal pair annuli all have circumference 26 and height 1 and are maximal. Offsets j = 1..5 have no swap pole on either rim, and j = 6 has 2 on each rim, at x = 6 and x = 7. The folding argument and the CRT claim are correct.
- The Hubert–Schmoll–Troubetzkoy description is accurate.
- In the cusp-frequency note, the finite-index group H exists as claimed. The Moeckel–Nakanishi theorem is applied correctly to convergents of almost every slope, and the triangle-area step is right. But the formula's numerator is positive exactly when the pair is lit, which the note says itself. So the frequency statement is a reformulation of "some direction passes E", with no positivity and no computable index.
- The equal-depth criterion is right, and 2l > gcd(C₁,C₂) suffices. Exact traces confirm it on 3 same-parity and 4 other named pairs. The unequal-depth generalization is (h₁+h₂)u ≡ h₁(x₂−o₂) + h₂(x₁−o₁) mod gcd(h₁C₂, h₂C₁). adjacent-cylinders.md already states it in equation form and used it to certify 20 of the 23 outstanding saved pairs in that note.

## Verified items

### Swap-cylinders note

1. **The pair annuli at p = 53, D = 13 (check item 1).** The band 2 < y < 3 on Q is one horizontal cylinder of circumference 26. The script confirms that unit steps in u are the tau crossings of the d146 model. For each j = 1..6, the following hold:
   - Both coordinates of {(u,t),(u+2j,t)} lie over the same base point.
   - The Y-orbit has circumference 26. Because D is odd, 4j ≢ 0 mod 26, so no half-period exchange shortens it.
   - Each rim contains a Y cone point of angle 6π, which is a 2-cycle letter paired with a 3-cycle letter. So no horizontal cylinder extends past either rim, and the annulus is maximal of height exactly 1.
   - Offsets 2j and 26 − 2j give the same annulus, and the 6 annuli are distinct. So j = 1..6 is the full list of even offsets, and (p−41)/2 = 6.
2. **Swap-pole incidence.** For j = 1..5 there is no swap pole on either rim. For j = 6 there are swap poles at (6,2), (7,2), (6,3) and (7,3), so both rims have them. This matches the note.
3. **Folding argument.** The script lists every rim lattice position where the two coordinates sit at the same physical point. For each j these are exactly x = j and x = D − j. They're swap poles only when both positions are on the smooth corridor walls 5 < x < 8, which happens only at j = 6. The argument is correct for every odd D: u + (u+2j) ≡ 0 mod 2D gives x = D − j or x = j. Front and back copies agree only on a smooth wall. x = 5 and x = D − 5 are reflex corners, and chamber-interior points have distinct front and back Q-points.
4. **The compatible start on the pole-free rim.** The front lifts of S = (1,2) and T = (3,2) are the Q-points {2,6} and {12,16}. Their Y-point {2,12} lies on the y = 2 rim of the j = 1 annulus and is regular, with cone angle 2π. The pair has the same parity (both odd), and the exact tracer shows that S sees T directly. So the example correctly shows that a pole-free annulus doesn't mean a dark pair.
5. **CRT claim (check item 1b).** A k with gcd(d+kC, h) = 1 exists if and only if gcd(d,C,h) = 1. The script checks this exhaustively for |d| ≤ 30 and 1 ≤ C, h ≤ 30. The note's proof is also correct as written. For a prime dividing h but not C, exactly one residue of k is bad. For a prime dividing both, d+kC ≡ d is nonzero. Height-one chords are primitive for any k.
6. **Hubert–Schmoll–Troubetzkoy (math/0602394).** The description is accurate.
   - Theorem 2: on a Veech surface, for every p the set of points not illuminable from p is finite.
   - §8, arithmetic case with a periodic p: "p illumines every point q except a finite number". The note's "can leave finitely many exceptional targets" is right.
   - Theorem 5: for an arithmetic surface there are infinitely many invariant subspaces of each even dimension. Only the non-arithmetic case has finitely many. The note places the finite conclusion on the non-arithmetic side, which is correct.
   - Neither result says anything about which kind of pole a specified start reaches. The note's closing point also holds. A finite exceptional set can contain the entire finite swap-pole set.

### Cusp-frequency note

7. **H exists.** Every A ∈ SL₂(ℤ) is the derivative of an affine map of the base pillowcase ℝ²/((2ℤ)² ⋊ ±1). Such a map permutes the 4 corners. There are finitely many degree-n covers branched over the 4 corners, so the stabilizer of the class of Q has finite index. For a transitive G ⊇ A_n the centralizer is trivial, so the lift to Q is unique. Y, the stop set and the swap poles are functorial in Q. The marks and lift choices form a finite set over the lattice sites, so fixing them costs only finite index. The derivative image H therefore has finite index in PSL₂(ℤ). E and R are constant on H-orbits of directions, because a marking-preserving affine map carries clean segments, cylinders, rims, starts and swap poles to objects of the same kind.
8. **Moeckel–Nakanishi.** Fisher–Schmidt's Theorem 1 states the following. Let H ⊂ SL(2,ℤ) have finite index. Then for almost every real x, the frequency of regular continued-fraction approximants p_n/q_n in a cusp κ (an H̄-orbit in ℚ ∪ {∞}) is w(κ)/[Γ : H̄]. Congruence isn't required, and Fisher–Schmidt note that Nakanishi removed Moeckel's restriction. The note applies it correctly:
   - It concerns convergents of almost every slope.
   - It conjugates by the coordinate exchange to pass from vectors (q,p) to Möbius action on p/q.
   - It sums over the finitely many cusps that pass F.
9. **Triangle step (check item 3).** The doubled area of the triangle 0, (q,qx), (q,p) is |det((q,p),(q,qx))| = q|qx − p|. For a convergent, |x − p/q| < 1/(qq′), so q|qx−p| < q/q′ ≤ 1, using q_{n+1} ≥ q_n for n ≥ 1. The d179 straightening proof uses only |det(v, y−v)| < 1 and primitivity of v, so it applies. The script confirms the inequality and primitivity for 40 convergents each of √2, the golden ratio, e and √7 − 2. The maximum doubled area is 0.72.
10. **The equal-depth criterion (check item 4).** The derivation is correct. The two legs have equal transverse travel h, so they have equal horizontal travel, o₁+u−x₁+iC₁ = x₂−o₂−u+jC₂. Bézout gives the congruence modulo gcd(C₁,C₂). An open interval (0,2l) of length greater than g meets every class modulo g, so 2l > g suffices. At 2l = g, the class 0 is missed, as the note says. Both open legs lie in clean cylinders, and the seam point is a regular point of the open edge, so the chord is a legal billiard path. Equal depth makes the seam point the midpoint. Exact traces confirm the following:

    | Room, cylinders | Pair | Parity | gcd, 2l | Result |
    |---|---|---|---|---|
    | DB55, vertical left-chamber cylinder (C = 10), wall edge x = 5, 3 < y < 5 | (4,1), (4,3) | same | 10, 4 | Front lift of T: u = 1, midpoint (5,4), traced to T. Back lift: no solution. |
    | same | (4,1), (4,4) | different | 10, 4 | Front lift: midpoint (5,7/2) on the upper wall, and (5,3/2) on the lower wall with the other side assignment, both traced. Back lift: no solution on either wall edge in either side assignment. |
    | same | (4,1), (4,2) | different | 10, 4 | Front lift traced. Back lift: no solution. |
    | U2, bar (C = 18) below, left arm (C = 4) above, edge through (0,2), l = 4 | (7,1), (1,3) | same | 2, 8 | All 4 lift combinations solvable, as the bound predicts. Midpoints (1,2) and (0,2), all traced to T. |
    | same | (5,1), (1,3) | same | 2, 8 | Same: all 8 instances traced. |

    In the same-parity cases every solution has a lattice midpoint, as midpoint-necessity.md requires. Horizontal circumferences on Q are even, so g is even and u is an integer.
11. **Unequal depths.** With depths h₁, h₂ the condition is t₁/h₁ = t₂/h₂. This gives (h₁+h₂)u ≡ h₁(x₂−o₂) + h₂(x₁−o₁) mod gcd(h₁C₂, h₂C₁), with sufficient condition (h₁+h₂)l > gcd(h₁C₂, h₂C₁). It's the equation hu = a(z−f+Dj) − b(e−x+Ci) of adjacent-cylinders.md, which adds parity constraints there to force an off-class midpoint. Exact traces confirm it on U2 with S = (5,1) at depth 1 and T = (1,4) at depth 2: 3u ≡ −23 mod 4, with 8 traced instances. On DB55 with S = (4,1) and T = (3,4), 3u ≡ −1 or −3 mod 10 has no solution in (0,2), for either lift.

## Gaps

### High

None.

### Medium

1. **The frequency formula restates the reachability lemma.** The numerator is the total width of the E-cusps. It's positive exactly when some direction passes E, and that's when the pair is lit (d178 with midpoint-necessity.md). So the theorem turns "does some direction pass E" into "does some cusp pass E", which is the same finite question. The index [PSL₂(ℤ):H] is the orbit size of the marked cover among degree-n covers. The note gives no bound for it, so the formula doesn't yield a search bound or an N₀ either. The straightening paragraph adds only that the approximants of a generic ray sample the same cusp types. That's d179's Medium 1 in different words. The header "Determines the exact frequency" is accurate, but it doesn't mark progress on L1.
2. **The equal-depth criterion isn't new, and the note understates what exists.** adjacent-cylinders.md already has the general-depth equation and its arithmetic-progression solution. It applied that equation to certify 20 of the 23 outstanding saved pairs there. The note calls its criterion an "equal-depth specialization", which is accurate. It should instead give the general form in item 11, because unequal depths are the common case for lattice marks.
3. **The 2l > gcd test seldom applies in the long-corridor rooms that matter.** For lattice marks, an integral depth h ≥ 1 needs both cylinders to have height at least 2 around the edge. In DB55's two axis directions, the only usable edges are self-glued chamber walls with l = 2 and gcd = 10. The sufficient bound fails there, and the exact congruence decides each lift separately (item 10). The note shouldn't imply that the sufficient condition is generic.

### Low

4. **Self-glued edges have two side assignments.** On Q a wall edge has the same cylinder on both sides, and the paired occurrence uses the reversed coordinate. A test must try both assignments of S's side. In DB55 the (4,1), (4,4) front lift misses on the lower wall in one assignment and hits in the other. The note's "common developed orientation" covers this implicitly but doesn't say it.
5. **The shear remark is close to a tautology.** A shear fixing the seam preserves x₁ + x₂, so it can't change the criterion. Any affine map that preserves this cylinder pair preserves the criterion too. Only a change of cusp gives new chances, which is the frequency note's own point.
6. **R covers interior and opposite-rim starts only.** A start on the same rim as the pole needs the rim-crossing analysis of adjacent-cylinders.md. The note's wording is accurate, but R is narrower than "incidence".
7. **The count claim is weak evidence.** Y has genus growing with n, so an unbounded number of cylinders at r = 4 is expected. The useful content is the j = 1 versus j = 6 contrast: same modulus, opposite incidence.
8. **Headers overstate.** Both say "Advances: L1". One is a correct negative example and the other is a reformulation, as in d178 and d179.

## What this means for L1

- The natural-action BBBB branch is unchanged. A same-parity lattice pair is lit if and only if some clean segment from one of the 8 starts reaches a swap pole. Equivalently, some cusp of a finite-index H passes E.
- Cylinder dimensions don't decide incidence. DB55 at p = 53 has annuli of identical circumference 26 and height 1, with no poles (j ≤ 5) or poles on both rims (j = 6). So no modulus or count argument can produce a swap pole.
- The cusp frequency is exact but uninformative until someone shows a positive numerator, and that's the open lemma. A real step would bound [PSL₂(ℤ):H], or a cusp representative set, in terms of r. It would then show that one representative direction places a start in, or opposite, a swap-incident clean cylinder. The equal-depth and unequal-depth congruences give an exact test for each such cusp.
- No ledger word moves, and no area bound or N₀ changes. The first open L1 case is still the marked primitive natural-action BBBB branch beyond the area-20 census.
