# d208 review: condition (i) below area 49

Advances: L1 (review). The review closes n = 22, which the note leaves open, and the twisted p = 23 case.

**Overall verdict: CORRECT WITH GAPS.** I found no false mathematical claim that the note relies on. The prime-degree theorem is right. Its affine exclusion is complete, so I have no obstruction to report. The main defect runs the other way: the note calls n = 22 "the first open case", but a short group-theory argument closes it. It also lists a residual (z = 4 at n = 22) that can't occur. The note makes no overclaim of condition (i).

Checks: [checks.py](checks.py), output in [checks.log](checks.log), 0.13 CPU-seconds. It uses plain Python on M11, PSL(2,11), M23 and AGL(1,p), plus a cycle-type enumeration at degree 11. It doesn't use rooms, rays, directions or words.

| Claim | Verdict |
|---|---|
| 1. Where 49 enters d81 | CORRECT (two minor omissions) |
| 2. Prime areas: d = p − 1 | CORRECT |
| 3. Twisted degree ≥ p − 1 at 29–47 | CORRECT (p = 23 also closes; see below) |
| 4. Uniform d ≥ 4; residual at n = 22 | CORRECT WITH GAPS (z = 4 residual is impossible; n = 22 is closable) |
| 5. Overclaim | NONE. The note underclaims at n = 22 |

## 1. Where 49 enters: CORRECT

Each statement matches d81 §§1–3 and the d82 review.

- Primitive case. Prop P gives G ⊇ A_n or n ≤ 6z_x for every reflex class. The fpr ≤ 1/2 bound is applied to g_x², which moves 3z_x sheets. With z_x ≤ 8, n = 49 > 48. Two reflex classes give a least z_x ≤ 4, so n ≥ 25 suffices.
- Equality cases at 48: (k, m) = (2, 24) with z = 4 fails m > max(24, 16) at equality. (4, 12) with z = 2 fails m > 12 at equality. (8, 6) fails T2's m ≥ 7.
- Divisibility: k = 4 needs n ≥ 52 and no multiple of 4 lies in 49–51. k = 8 needs n ≥ 56 and no multiple of 8 lies in 49–55. Both are correct.

Minor omissions, which don't affect correctness:

- The k = 2 row's threshold is 50 (z = 4), not 49. It holds at 49 only because 49 is odd. The divisibility sentence lists only k = 4 and k = 8.
- The k = 7 row (T2 at m ≥ 7) has threshold exactly 49. So 49 is also a k = 7 cutoff: 42 = 7·6 fails.

## 2. Prime areas: CORRECT

Steps checked:

1. G is transitive because the double is connected. Burnside's theorem (1906) states that a transitive group of prime degree p is 2-transitive or is permutation-isomorphic to a subgroup of AGL(1, p). The statement in the note is accurate, and this step needs no CFSG.
2. A normalized room with n ≥ 2 isn't a rectangle, so r ≥ 1 and some z_x ≥ 1. Then g_x² has order 3 and fixes p − 3z_x sheets.
3. In AGL(1, p), a nonidentity element fixes at most one point. checks.py confirms this exhaustively at p = 29. 3 doesn't divide 23·22 = 506, so no order-3 element exists at p = 23. For p ≥ 29, g_x² fixes p − 3z_x ≥ p − 24 ≥ 5 points. The affine case is excluded at every listed prime. At p = 23 the fixed-point argument also works: 3z_x ≤ 23 forces z_x ≤ 7, so g_x² fixes at least 2 points.
4. With G 2-transitive, the orbitals are the diagonal and its complement. S and T are distinct and of the same parity, so they share no incident cell. The marked pairs are off-diagonal, so U is the complement and d = p − 1. This doesn't use the nondirect hypothesis.

You asked for an obstruction if the affine case survived. It doesn't survive, so there is none.

The H bound is right: H ≥ 2(p − 1) − 16 − ⌊p/2⌋ = 2p − 18 − ⌊p/2⌋ = 17 at p = 23. This is the counting lemma with d = p − 1. The note correctly says it's algebraic only.

## 3. Twisted degree: CORRECT

- Claim 1 (unpaired reflex support). This step is correct. If z_{x+e} = 0, the peripheral square is (g_x², 1). L ∩ (G₁ × 1) then projects to a nontrivial normal subgroup of a primitive group, which is transitive. Surjectivity onto G₂ gives transitivity on all n² pairs, so d_e = n.
- Claim 2 (natural A_n or S_n, n ≥ 7). This step is correct. A nontrivial kernel gives d_e = n. Otherwise L is the graph of an automorphism. For n ≠ 6 that automorphism is conjugation by some σ ∈ S_n. The orbits are then the matching {(s, σs)} and its complement. A 4×4 marked set doesn't fit in a matching, so d_e ≥ n − 1.
- At p ≥ 29, Prop P gives G ⊇ A_p or a single reflex class (two classes would force p ≤ 24). So claim 1 or claim 2 applies. The conclusion d_e ≥ p − 1 holds at all six primes.
- H_e = 2d_e is the twisted intersection count. d207 has since reviewed it as CORRECT WITH GAPS (minor), so the "pending" tag can become "reviewed".
- The p = 23 Cauchy–Davenport bound d_e ≥ 7 is correct as stated.

**Improvement: p = 23 closes.** The nonaffine 2-transitive groups of degree 23 are M23, A23 and S23. If G = M23, every order-3 element has at least six 3-cycles. checks.py verifies this: M23 is 4-transitive (basic orbits 23, 22, 21, 20). Its 4-point stabilizer has order 48, and no nonidentity element there fixes more than 7 points. So an order-3 element fixes at most 7 points and has z ≥ 6. A random sample of 4,488 order-3 elements gave type 3⁶1⁵ every time. With r ≤ 8, only one class has reflex corners, so claim 1 gives d_e = 23. If G ⊇ A23, claim 2 gives d_e ≥ 22. The residual "two classes of four, exchanged by e" can't occur. The twisted bound d_e ≥ p − 1 holds at all seven primes.

## 4. Uniform bound and n = 22: CORRECT WITH GAPS

These parts are correct:

- All 16 incident-sheet pairs lie in U, so d ≥ 4.
- If d = 4, every source sheet's four targets form a K_{4,4} component. G-translates of that component partition the first coordinate, so 4 | n. When 4 ∤ n, d ≥ 5. The same argument applies to the twisted curve, using transitivity of the L-projection.
- At n = 22, the only possible block size is k = 2: block size 11 gives a degree-2 quotient with no zero, which R1 excludes. The block action H on 11 blocks is 2-transitive because 3 doesn't divide 110. The index-2 normality argument and the "10 or 5" orbit split are correct but weak.

**Error (minor): the z = 4 residual at n = 22 is impossible.** z counts 3-cycles of h_x on m = 11 blocks, so z ≤ 3. d81 §6 has the same slip: its k = 2, z = 4 row starts at 22.

**Gap: n = 22 is closable, and the note misses it.** The argument uses two standard lists:

- The transitive groups of degree 11 (Butler–McKay): C11, D11, 11:5, AGL(1,11), PSL(2,11), M11, A11, S11.
- The primitive groups of degree 22 (Sims; Dixon–Mortimer, Appendix B): M22, M22:2, A22, S22.

*Imprimitive case (k = 2, m = 11).* H contains an order-3 element, so it isn't solvable. Therefore H is PSL(2,11), M11, or contains A11. checks.py does the following:

- Builds M11 (order 7920) and finds a transitive PSL(2,11) of order 660 inside it.
- Lists M11's cycle types. Those with all cycle lengths in {1, 2, 3} are only 1¹¹, 2⁴1³ and 3³1².
- Enumerates all 247 genus-0 type multisets at degree 11 with Z ≥ 1. It uses Σ(k_x + 2z_x) = 20 and Σf_x = Z + 4.

Exactly one multiset uses only M11 types: {2⁴1³, 2⁴1³, 3³1², 3³1²}. It has Z = 6. The class budget kZ ≤ r ≤ 8 gives Z ≤ 4, which excludes it. So H ⊇ A11. The matching lemma (`low-valency.md`; it needs H ⊇ A_m and m ≥ 6) then applies with its R1 exclusion. All external pairs form one orbit. A marked external pair exists because a block of size 2 can't hold 8 sheets. So d ≥ n − 2 = 20 ≥ 15.

*Primitive case.* M22 and M22:2 are 3-transitive, and A22 and S22 are at least 20-transitive. So every primitive G at n = 22 is 2-transitive, and d = 21.

So condition (i) holds at n = 22 for every distinct same-class interior lattice pair, without the nondirect hypothesis. The dependencies are R1, Fact L (the class budget), the matching lemma and the two group lists. The degree-22 list rests on CFSG, as d81 already does through Burness–Guralnick.

## 5. Overclaim: NONE

- The note claims condition (i) only at the seven primes, and those proofs are complete.
- The H and H_e bounds are labeled algebraic, with no claim about legal midpoints.
- The twisted transfer gaps (n = 22, p = 23) are stated as gaps.
- Wording to fix: the opening sentence "condition (i) for normalized rooms below area 49" reads broader than the result. It should name the areas.
- Wording to fix: "First open case. … n = 22" is wrong after §4 above. In the 22–48 range, the first open area is now 24. Area 21, from d81's 21–48 range, is also still open.

## Exact surviving statement

For a normalized strictly simple orthogonal lattice room with r ≤ 8, let S ≠ T be same-parity interior lattice marks.

1. If n ∈ {23, 29, 31, 37, 41, 43, 47}, then G is 2-transitive and d = n − 1.
2. If n = 22, then d ≥ 20. G is primitive and 2-transitive with d = 21, or k = 2 with H ⊇ A11 and d ≥ 20. *(This review; it adds the degree-11 and degree-22 group lists to d81's dependencies.)*
3. For every n, d ≥ 4. If 4 ∤ n, then d ≥ 5.
4. For different-parity marks at n ∈ {23, 29, …, 47}, d_e ≥ n − 1. Then H_e = 2d_e ≥ 2n − 2 when the pair is dark. *(p = 23 by this review, using M23's order-3 cycle type.)*

Together with d81, condition (i) holds at n = 22, n = 23, the primes 29–47, and n ≥ 49. It stays open at the composite areas 24–48 and at n = 21.
