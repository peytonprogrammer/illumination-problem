# d207 review: area bound for a BBBB dark pair

Advances: L1 (review only; no new bound).

**Overall verdict: CORRECT WITH GAPS.** I found no arithmetic or logical error. Every identity, inequality and table entry recomputes exactly. The gaps are about what the two conditional bounds are worth. The bound of 48 assumes a hypothesis that, at n ≥ 49, is equivalent to its own conclusion. The area-25 condition depends only on the room, not on the marks, and is equivalent to n + ⌊v_out,min/2⌋ ≤ 25. The note admits most of this, but the opening paragraph and one section heading present both as more than restatements. The note claims no unconditional bound, which is correct.

Checks: `checks.py` in this directory, about 0.1 CPU-seconds. It runs cell-incidence arithmetic on R22, cov4181 and cov2929 only, plus closed-form integer checks. It doesn't search rooms, rays, directions or words.

| Claim | Verdict |
|---|---|
| 1. Per-class identities | CORRECT |
| 2. Conditional bound H ≥ …, area ≤ 48 | CORRECT WITH GAPS (restatement, not reduction) |
| 3. Two-class estimate, exact loss, control table | CORRECT WITH GAPS (framing of the "area-25 condition") |
| 4. Twisted-curve count for different-parity marks | CORRECT WITH GAPS (minor; no error) |
| 5. Scope | CORRECT WITH GAPS (two framing overstatements; no unconditional claim) |

## 1. Per-class identities: CORRECT

Proof: each unit cell has exactly one corner of each parity class. Count (cell, class-y corner) incidences by corner. Convex corners have 1 incident cell, smooth wall points 2, reflex corners 3 and interior points 4. So n = v_y + 2s_y + 3r_y + 4i_y = c_y + 2m_y. This is d68 Lemma A. Summing c_y over the four classes gives (r+4) + 3r = 4r+4. Then Σm_y = (4n − 4r − 4)/2 = 2(n−r−1). Riemann–Hurwitz agrees: Σ(e−1) = 2r + Σm_y = 2n − 2.

The reading of m_y as the number of degree-two points of the doubled room DP over pole y is also correct. An interior point has two lifts in DP and a smooth wall point has one.

Computed on the three controls (`checks.py`): all four identities hold in every class, v = r+4 holds, and no room has a pinch.

| Room | n, r | m (00,01,10,11) | c (00,01,10,11) | Q class |
|---|---|---|---|---|
| R22 | 15, 9 | 0, 2, 2, 6 | 15, 11, 11, 3 | 00 |
| cov4181 | 28, 8 | 12, 12, 0, 14 | 4, 4, 28, 0 | 10 |
| cov2929 | 22, 8 | 0, 8, 10, 8 | 22, 6, 2, 6 | 00 |

These m values match the note. The statement "All three controls have a Q class" is confirmed.

## 2. Conditional bound: CORRECT WITH GAPS

**The inequality is right.** The counting lemma gives 2d = R_a + R_other + J with J ≤ 2r. A regular degree-two point of DP carries one off-diagonal germ (y = −x), so it contributes at most one branch to any union, and R_a ≤ m_a = (n − c_a)/2. This refines the lemma's ⌊n/2⌋. For a dark pair every off-class regular coincidence is unrealized, so H ≥ R_other ≥ 2d − 2r − (n−c_a)/2. This holds whether or not H also counts off-class reflex branches; the note's wording leaves that open.

**The arithmetic is right.** Since (n−c_a)/2 ≤ ⌊n/2⌋, r ≤ 8 and d is an integer, H ≥ f(n) := 2⌈2n/3⌉ − 16 − ⌊n/2⌋. `checks.py` confirms that f(n+6) = f(n)+5 for all n, min f on 49–54 is 26, f(25) = 6 and f(26) = f(27) = 7. The minimum over n ≥ 26 is 7.

**The direction is right.** A dark pair isn't directly visible. d81 then gives d ≥ ⌈2n/3⌉ for a normalized room at n ≥ 49, so H ≥ 26. Contrapositive: if every dark pair has H ≤ 25, no dark pair has n ≥ 49. A bound on H gives an area bound only through this contrapositive, and that is how the note uses it.

**Gap A: the conditional is a restatement.** At n ≥ 49 every dark pair has H ≥ 26. So the hypothesis "every dark pair has H ≤ 25", restricted to n ≥ 49, is logically equivalent to "no dark pair has n ≥ 49". Below 49 the hypothesis adds nothing, because d81 doesn't apply there. d86 reached the same verdict on the αn + K budget in RESULTS §11 "Open core": it restates the open lemma; it doesn't reduce it. The note says the hypothesis is open and gives no upper bound on H. It should also say that the hypothesis carries no information beyond the conclusion.

**Gap B: inherited scope.** The bound holds only for normalized rooms and same-parity lattice marks. It inherits d81's status, which d82 rated "sound with fixable gaps". The "Result" paragraph says "normalized", which is correct. The reduction from arbitrary rooms to normalized ones is project bookkeeping (R1) and isn't re-argued here.

**The 25 target is correct.** With condition (i) extended to n ≥ 26, H ≤ 6 contradicts H ≥ f(n) ≥ 7 for every n ≥ 26, so the area is at most 25. The constant 6 is the largest one this estimate allows at n = 26, because f(26) = 7. The claim that reaching one candidate would suffice is also correct wherever f(n) ≥ 1, which is n ≥ 19 (f(19) = 1, f(18) = −1). Both extensions remain unproved, as the note says.

## 3. Two-class estimate: CORRECT WITH GAPS

**The algebra is right.** For a pair of classes I with complement out, Σ_{y∈I} c_y = (r+4 − v_out) + 3(r − t). Adding the two identities gives 2n = 4r+4 − v_out − 3t + 2M, so n = 2r+2+M − (3t+v_out)/2. Each c_y ≡ n (mod 2), so c_out = 3t + v_out is even. Then (3t+v_out)/2 is an integer at least 3t/2, which gives U(I) := 2r+2+M − ⌈3t/2⌉ ≥ n.

**The exact loss is right.** U(I) − n = (3t+v_out)/2 − ⌈3t/2⌉. If t is even, v_out is even and the loss is v_out/2. If t is odd, v_out is odd and the loss is (v_out−1)/2. In both cases it is ⌊v_out/2⌋. The optimal I leaves out the two classes with the smallest convex counts. Their sum is at most ⌊(r+4)/2⌋ = 6 at r = 8, so n ≤ min U ≤ n+3. `checks.py` asserts U − n = ⌊v_out/2⌋ for all six choices of I in each control.

**The control table is right.** I recomputed all six choices of I per room:

| Room | min U | Minimizing I | M, t | U − n | ≤ 25 |
|---|---:|---|---|---:|---|
| R22 | 17 | 00,01 (ties: 00,10 and 00,11) | 2, 3 | 2 | yes |
| cov4181 | 28 | 00,10 (unique) | 12, 1 | 0 | no |
| cov2929 | 22 | 00,10 (unique) | 10, 4 | 0 | yes |

These match the note's 17/28/22 against areas 15/28/22. For R22 the threshold is 23 − 2r = 5 at r = 9, and M − ⌈3t/2⌉ = 0 passes.

**Gap C: the "area-25 condition" is a property of the room, nearly equivalent to n ≤ 25.** By the exact-loss identity, min_I U(I) ≤ 25 is equivalent to n + ⌊v_out,min/2⌋ ≤ 25. It holds whenever n ≤ 22 and fails whenever n ≥ 26. It never refers to the marks, so "works for different-parity marks" holds only trivially. The continuation section says this ("Optimizing over classes cannot discover a small-area dark representative"). However, the opening paragraph still calls it "a separate, directly checkable condition giving area at most 25 for either parity type", and the section heading repeats that framing. Both should say it is a restatement of the area bound with a loss of at most 3.

The one-neck family is right as described. Chambers of widths 5 and 10 with a 3 × 1 neck have r = 4 for every h ≥ 1. Horizontal edge lengths {5, 3, 10, 18} and vertical edge lengths {2h+1, h} each have gcd 1. Every class gains interior points as h grows, so every M is unbounded while t ≤ 4. This shows that the estimate depends on shape alone. I checked it by hand, not with code, to stay within the three named rooms.

## 4. Twisted-curve count: CORRECT WITH GAPS (minor)

Each step checks out.

- **τ descends.** −(u+e) = −u − e ≡ −u + e (mod 2), since 2e ∈ 2Z². So translation by e commutes with ±1. It is holomorphic, it is an involution, and it maps pole S to pole S+e = T.
- **Two regular fixed points.** u+e ≡ u is impossible. u+e ≡ −u gives 2u ≡ e, so u ∈ e/2 + Z² mod 2Z², which has four solutions. None of them is fixed by −1, because 2u ≡ e ≠ 0. So they form two sign orbits, and neither is a pole. `checks.py` lists them for each e. For e = (1,0) they are (1/2,0) and (1/2,1).
- **Equal degrees.** On each component, f∘p₁ = τ∘f∘p₂. Since deg τ = 1, n·deg p₁ = n·deg p₂. This holds component by component, so it also holds on any union.
- **No diagonal component.** A diagonal component would need f = τ∘f on an open set, but τ has only two fixed points.
- **Count 2d_e and transversality.** The bidegree-(1,1) pullback argument applies verbatim. At a coincidence x = y, f(x) ∈ Fix τ is a regular base point, so f is unramified at x. Near (x,x) the curve is the graph y' ↦ f⁻¹τf(y'), with derivative dτ = −1. A holomorphic involution with an isolated fixed point has derivative −1 there. So the curve has one smooth branch at (x,x), transverse to the diagonal. The 2d_e intersections are therefore distinct points of DP over the two τ-fixed base points, and none lies at a corner. This is a real advantage over the untwisted count, where up to 2r branches can sit at reflex corners.
- **The midpoint of a legal path is a candidate.** The developments are S+vt and T*−vt, with T* = ±T + 2k ≡ T (mod 2). I verified −T* + e ≡ S (mod 2) for all parity pairs and all T* ≡ T. In B, [T* − vt + e] = [−(S + vt)] = [S + vt], so f(x(t)) = τ(f(y(t))). The arc starts at a marked lift pair, so it lies in the chosen union. At t = L/2 it meets the diagonal.

  Earlier passes through regular lattice points are harmless. Those points have cone angle 2π, so the geodesic is analytic there, and an analytic arc stays in one branch of the normalization. The midpoint can lie on a wall. A smooth wall point at a half-integer position is still unramified, so this case is covered.

Minor gaps:

- **Gap D.** The note doesn't say that the union also has to include the branches at every lift pair (S_i, T_j), four in all. Its parenthetical "include all allowed endpoint lifts" covers this, but tersely. The (S_i, T_j) are singular points of the curve, since both coordinates are ramified. The note's "f is locally onto" gives nonemptiness, but the two local branches s = ±c·t should be named.
- **Gap E.** "A nondirect different-parity pair there already has regular algebraic midpoint candidates" is true, but the only lower bound is 2d_e ≥ 2. The note gives no lower bound on d_e and says so. The word "nondirect" plays no role in that sentence.

Neither gap affects correctness. As the note states, the identity yields a necessary condition (darkness implies that all 2d_e candidates are hidden) and no visibility statement.

## 5. Scope: CORRECT WITH GAPS

- The note claims no unconditional area bound, in the Result paragraph and again in the Conclusion. This is correct.
- "First uncovered exact area is 22" agrees with the census through area 21. The L2 provenance paragraph correctly states that d206 didn't re-audit d9's earlier tables.
- The claims about the controls are scoped correctly. R22 is dark at r = 9. The cov4181 and cov2929 pairs are lit, and all three rooms have a Q class, so none of them tests the BBBB implication. The statement about seven inaccessible branches in class d of cov4181 matches midpoint-necessity.md.
- Overstatements: (i) the opening's "directly checkable condition giving area at most 25 for either parity type" (Gap C); (ii) "This proves the conditional bound 48" without saying that the hypothesis is equivalent to the conclusion at n ≥ 49 (Gap A).

## Statement that survives

1. **(Identities.)** For every strictly simple lattice room and parity class y, n = c_y + 2m_y, Σc_y = 4r+4 and Σm_y = 2(n−r−1).
2. **(Hidden-branch lower bound.)** For a normalized room with r ≤ 8 and a dark same-parity interior lattice pair of class a, H ≥ R_other ≥ 2d − 2r − m_a. If n ≥ 49, d81 then gives H ≥ f(n) ≥ 26. So "H ≤ 25 for every dark pair" is equivalent to "no dark pair at n ≥ 49". This is a restatement, not a reduction. Extending condition (i) to n ≥ 26 and proving H ≤ 6 would give n ≤ 25.
3. **(Two-class identity.)** For every room and pair of classes I, n = U(I) − ⌊v_out/2⌋. So min_I U(I) = n + ⌊v_out,min/2⌋ ∈ [n, n+3] for r ≤ 8. The "area-25 condition" is equivalent to n + ⌊v_out,min/2⌋ ≤ 25 and says nothing about marks or darkness.
4. **(Twisted count.)** For different-parity interior lattice marks with e = T − S mod 2, the marked union of components of f(x) = τ(f(y)) has equal projection degrees d_e ≥ 1. It meets the diagonal in exactly 2d_e distinct points of DP, transversely, all over the two τ-fixed half-integral base points, and none at a corner. The midpoint of every legal S–T path is one of them. For a dark pair, all of them are unrealized. No reachability or lower bound on d_e beyond 1 follows.
5. No unconditional finite area bound for a BBBB dark pair with r ≤ 8 follows from the note. The first uncovered exact area is 22.
