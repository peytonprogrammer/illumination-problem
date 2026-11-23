# D115: review of accumulation.md

Date: 2026-11-20. Reviewer: independent referee. Reviewed file: `qclass-closure/bbbb/accumulation.md` (live, 55 lines).

Context read: `dark-locus.md` (live), d89 review, RESULTS §11, d69 §1, the normalization definition in RESULTS §2 (per-axis gcd 1), and the d80 note header. Literature statements (EMM, Filip, Apisa–Wright, LMW) aren't checked here. d89 already recorded that they come from memory.

Own code: `checks.py`, log `checks.log`, 16 CPU-seconds.

- Check 1 tests the step-3 minor argument on 3,480 random integer cases. It finds no failure of primitivity, mark parity or coordinate parity. A control with `p` not a multiple of `D` gives gcd 2, so the hypothesis `D | p` is needed.
- Check 2 tests the strip placement matrix `G` on a four-run chain. It confirms the kernel `(d_j/P_j)`, full row rank 3, and the translate form `c = c₀ + Gn` exactly on 531,441 integer vectors. Both vectors that land in the open overlaps replay as legal positive-sheet paths under direct folding.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Fixed-height theorem | Sound, conditional on d89 and through it on d80. Two wording fixes. |
| 2. Deformation line and limits | Sound as stated (small \|t\|). The note doesn't claim the whole line is dark. That stronger statement is true for the physical component, by an argument the note omits. |
| 3. Strip exclusion | Sound. |
| 4. Scope statements | Accurate. |

## 1. Fixed-height theorem

**What d89 supplies.** Restrict to the subcollection of same-parity interior lattice pairs with n ≥ 120. The least-dimension choice of N is then made for this subcollection, and every d89 step goes through unchanged:

- σ-stability and discarding the singular locus use only minimality and the presence of unbounded n.
- K = 0 uses d80 in the seed room. The seed is strictly simple and normalized, with r ≤ 8 and n ≥ 120, so d80 applies.
- Rationality uses GL⁺(2,Q) density of the selected rational examples.
- k ≥ 2 uses only unbounded n.

The note uses exactly these four outputs. It doesn't use D(r) or the rank upper bound. So the d89 fixes on N_reg connectivity and the Möbius sentence don't affect it.

**Step 1 (real branch).** Physical rooms give 2r + 2 edge parameters plus 4 mark coordinates. The labeled stratum Q(1^r, −1^(r+4)) with four regular labels has complex dimension 2r + 6, so its σ-fixed germ has real dimension 2r + 6. Physical tuples are σ-fixed, and the period map is real linear, rational and injective. So it is a local diffeomorphism onto the fixed germ.

N is smooth and σ-stable at the seed, so its fixed part has real dimension 2k. Its physical preimage is an open piece of a real linear plane E. E is rational because N has rational equations and the physical map is rational. All of N lies in the four-pair dark set D₄. So every physical room near the seed in E is dark. This is correct.

**Step 2 (one-axis vector).** diag(a, 1) ∈ GL⁺ preserves N and acts on physical coordinates as a horizontal stretch. Differentiating at an open set of points gives the projection of E onto horizontal coordinates. So E = E_H ⊕ E_V. Both parts are rational, and each contains its radial stretch. dim E_H + dim E_V = 2k ≥ 4, so one part has dimension at least 2.

A vector in that part whose wall component is proportional to e differs from a radial multiple by a mark-only tangent. K = 0 forbids that tangent. This also rules out u = 0, so some 2 × 2 minor M is nonzero. This is correct.

**Step 3 (primitive lattice rooms).** Take a prime ℓ dividing every entry of qe + pu. Then ℓ divides qM and pM. Because gcd(p, q) = 1, ℓ divides M, hence D and p, but not q. So ℓ divides every e_k, which contradicts gcd(e) = 1. Check 1 reproduces this.

Per RESULTS §2, "normalized" means per-axis gcd 1, so gcd(e) = 1 holds for the seed. The marks are integral because v was cleared of denominators. q is odd because q ∤ D and D is even. p is even. So every horizontal coordinate keeps its parity mod 2, which is stronger than the note's claim about the mark difference. All parity classes are unchanged.

Strict simplicity, interiority, distinctness, and r all persist for small |t|. Positive diagonal maps preserve both legality and strict simplicity. The area is about q · area(z(t)), so it is unbounded. The height Y equals the seed's height. BBBB follows at area > 64 from d69 §1. The theorem holds as stated.

**Fixes.**

- (Low) "shrink to |t| < 1/2" should read: restrict to |t| < min(ε, 1/2), where ε is the dark radius after clearing denominators. Scaling v down would break integrality. The bound 1/2 only serves 0 < |p| < q, and so gcd(p, q) = 1.
- (Medium) "its d80 inputs" should name the chain that d89 Finding 1 lists. That chain is d16 with corrections, three-sheet, low-valency, and partition uniqueness at n ≥ 120. It should also note that EMM finite union, Filip algebraicity and the marked-stratum conventions were checked only from memory.
- (Info) The "iff" is accurate. The reverse direction is unconditional. It needs a normalized r ≤ 8 strictly simple seed, darkness at the rationals p/q near 0 with D | p, and n large enough for BBBB.

## 2. The deformation line

The line z(t) = z₀ + tv exists and is dark for |t| < ε, as the note asserts. Its rational limit is correct: with p = D and q → ∞, the normalized rooms tend to the seed. Its non-torus limit is correct: for irrational t, (e_i + tu_i)/(e_j + tu_j) is irrational because M ≠ 0.

The cycle γ − ιγ for a wall γ is closed, because the endpoints are odd-order singularities with one lift each. Its period is twice the wall vector. Two real periods with irrational ratio can't both lie in a rank-two lattice. Every t in the dark interval is a persistent limit, because suitable primes q and multiples p of D approximate t.

On "the whole line is dark": the note claims darkness only for small |t|. The lighting test also works only on a subinterval, so the note is consistent with what it proves. A stronger statement holds, but the note doesn't use it. Let I be the component of {t : z(t) is strictly simple with distinct interior marks} that contains 0. Then all of z(I) lies in N:

- The set {t ∈ I : z(t) ∈ N} is closed because N is closed in the stratum.
- The set is open. Near any of its points, N is a finite union of linear sheets. One sheet contains infinitely many points of the line, so it contains the line locally.

So the whole physical segment is dark. Add this only if a later argument needs it.

## 3. Strip exclusion

I re-derived and checked each step.

- `c_i = x_s + sA_i − Σ_{j≤i} n_j P_j`, with s fixed by the endpoint. This gives G_ij = (A_i/X − 1_{j≤i})P_j exactly. Check 2 confirms this against direct folding.
- A crossing vector in the open overlap product is a legal path. Reflections happen strictly inside run height ranges, where the walls are actual walls, so the path avoids corners.
- Consecutive row differences are (d_i/X)P − P_i e_i, which are independent. So G has rank m − 1, and its kernel is spanned by (d_j/P_j).
- The character criterion and image(Gᵀ) = ker(G)^⊥ give the density test: GZ^m is dense exactly when Σ k_j d_j/P_j(t) = 0 has no nonzero integer solution k.
- Pairwise nonproportional affine functions P_j have distinct roots, and at most one of them is constant. So the 1/P_j are linearly independent. The cleared relation is a nonzero rational polynomial, which has no transcendental root. For m = 2 the polynomial has degree at most 1, so every irrational t works.

The listed exclusions are honest: same-height endpoints, turning routes, and proportional width classes.

## 4. Scope

**Proved (conditional on d89 → d80 and the cited literature):**

- Unbounded dark same-parity lattice area at r ≤ 8 gives a normalized seed inside a d89 locus.
- The seed has a rational, nonradial, one-axis dark interval with every ordinate fixed and integral.
- That interval yields primitive BBBB dark rooms of fixed height and unbounded area. Their limits include the rational seed and non-torus rooms.

**Unconditional:** the reverse implication, and the strip-lighting lemma.

**Not proved:** any dark room, any area bound (effective or not), or the case W ≤ 20.

**Crux:** show that every nonradial one-axis interval with fixed integer ordinates, inside a d89 locus, contains a lit parameter. The strip test does this only for monotone chains of full runs with pairwise nonproportional widths.

## Re-run

```
cd d115-review-accum && python3 -B checks.py > checks.log
```
