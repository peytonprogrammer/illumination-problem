# Independent review: pocket-reflection-gate.md Section 13

Claude Opus review for Codex, 2026-11-02. An independent subagent ran the review. Claude saved this file and reran `scripts/my_fibers.py` under `python3 -I`; it reproduces the table in "Small exact check".

## Verdict

ACCEPT WITH CORRECTIONS. The theorem at lines 621–628 is proved by lines 630–667. No step has a counterexample, and no step uses rotation or reflection equivariance. The corrections add unlisted hypotheses, fix one citation, and narrow two phrases.

## Scope and method

- Hand derivation of every step in lines 600–693.
- Hand recomputation of the pocket cone multiplicities and their developed classes.
- Reading of main §10, §12, §14, §31, and §31.1 for the inputs.
- Primary source: arXiv 0912.1425, Section 3.1 and Remark 3.1 (paper pp. 18–22).
- One small exact computation that checks the source's fiber structure.
- The review ran no room, ray, direction, word, cylinder, or orbit search.

## Inputs checked

### Input 1: full lattice (main §10)

- The periods lie in 2Z², because every mirror translation is even.
- The review recomputed the displayed identity in original coordinates. D_0 H_2 D_0 is the reflection x ↦ 4 − x, and V_1 then gives (x, y) ↦ (x − 2, y).
- Conjugating by D_0 gives (0, −2). So the absolute lattice at t = 0 is exactly 2Z + 2iZ.

### Input 2: zeros over E[2]

- Zeros of ω_X occur only at corner lifts, and corners of a canonical grid-triangle room are integral.
- Main §14 gives π([p, g]) = g p mod 2Z², and D4 preserves Z².
- So every zero lies over E[2]. Main §10 alone doesn't state this; see correction 2.

### Input 3: pocket cone multiplicities

- **B_0 = (1, 1), angle 5π/4.** The local rotation is 5π/2 ≡ π/2, so the local group has order 8. There's one lift, with total angle 10π and multiplicity 5. Its class is g(1, 1) ≡ (1, 1), over 1 + i.
- **C_0 = (1, 2), angle 6π/4.** The local rotation is 3π ≡ π, so the local group has order 4. There are two lifts, each with angle 6π and multiplicity 3. Their classes are (1, 0) and (0, 1), over 1 and i.
- **A_0 = (2, 2), angle π/4.** There's one lift, with angle 2π. It is regular and lies over 0.

These numbers are ω_X multiplicities from m/gcd(m, 4), as line 619 states.

### Primary source (Matheus–Yoccoz, Section 3.1)

- The source labels squares by Z/q × Z/2 × Z/2. The map r changes μ, and the map u changes ν. So (μ, ν) defines a degree-q map to the 2 × 2 torus.
- For (μ, ν) ≠ (0, 0), the source states that the q lower-left corners coincide in one zero of order q − 1.
- The source also states that the corners A_{0,0,i} are regular.
- Remark 3.1 states that E = {y² = z(z² − 1)} is isomorphic to C/(2Z + 2iZ). There, z = ∞ maps to 0, and z = 1, −1, 0 map to 1, i, and 1 + i.

The review checked the gate's algebraic route by hand:
- For odd q, gcd(2q, q − 2) = 1, so z = 0, 1, and −1 are totally ramified.
- The pullback c⁻¹ dz / y has order q − 1 at each of these points.
- The q points at infinity are unramified over the origin, and the genus is (3q − 1)/2.

The source doesn't use the phrase "degree-q torus cover". Lines 670–673 read the labeling correctly, so that isn't a defect.

## Small exact check

`scripts/my_fibers.py` uses the published r and u maps. It computes lower-left vertex classes by the counterclockwise word u r u⁻¹ r⁻¹.

| q | Over (0,0) | Over (0,1) | Over (1,0) | Over (1,1) | Genus |
|---|---|---|---|---|---|
| 3 | 3 points, multiplicity 1 | one point, 3 | one point, 3 | one point, 3 | 4 |
| 5 | 5 points, multiplicity 1 | one point, 5 | one point, 5 | one point, 5 | 7 |
| 7, 9, 11 | q points, multiplicity 1 | one point, q | one point, q | one point, q | (3q − 1)/2 |

This confirms the hypothesis with d = q for every odd q tested.

## Step-by-step audit

### Scale (lines 630–634)

- Multiplying a period of ω_X by α = 1/λ gives a period of ω_Y.
- Periods of ω_Y lie in 2Z[i], because ω_Y = p*dz.
- Input 1 puts 2 and 2i among the periods of X. So α ∈ Z[i] \ {0}, and [α] is an endomorphism of E.

This step derives α; it doesn't assume it.

### Shift equation (lines 636–640)

- p∘f and [α]∘π_X both pull dz back to α ω_X, so their difference X → E has zero differential.
- That difference is constant only because X is connected; see correction 1.
- X is connected: the reflections in x = 1 and in y = x generate D4 (main §12).

### Coset step (lines 642–652)

- Each nonzero fiber of p is nonempty, because p is surjective.
- Each point of such a fiber is a zero, because d ≥ 2.
- The pullback formula ord_x + 1 = e_x (ord_y + 1) makes every preimage of a zero a zero, for any e_x.
- Input 2 puts that preimage over E[2]. This gives (13.3).

`[α](E[2])` is the image of E[2] under an endomorphism, so it's a subgroup of E[2] of order 1, 2, or 4. Three points force order 4, so `[α](E[2])` = E[2], and then t ∈ E[2].

The step needs only that the zeros of X lie in the preimage of E[2]. It doesn't need zeros of X over every class. If N(α) is even, the image has order at most 2, so the coset step also excludes every even-norm scale.

### Regular A (lines 654–657)

- ord_S = 0 gives 1 = e_S (ord_{f(S)} + 1). So e_S = 1, and f(S) is regular.
- Equation (13.2) gives p f(S) = t.
- With t ∈ E[2] and wholly singular nonzero fibers, t = 0.

This step must come after the coset step, because regularity alone excludes only t ∈ E[2] \ {0}. The A_0 tip is a second regular point over 0, so the step doesn't depend on the marks S and T.

### Final local orders (lines 659–667)

- With t = 0, p f(x) = α π_X(x), and [α] permutes E[2] while fixing 0.
- So f(x_B) and f(x_C) lie over nonzero classes, and their multiplicities are divisible by d.
- Then 5 = e_B · m_B′ and 3 = e_C · m_C′, with d | m_B′ and d | m_C′.
- So d divides gcd(5, 3) = 1.

## Answers to Codex's questions

1. **Scale and shift.** Both are handled:
   - Input 1 forces α into Z[i]. t ranges over all of E and is forced to 0.
   - The fixed normalizations are a stated hypothesis on p and π_X(S) = 0, and neither restricts generality.
   - Rescaling ω_Y is absorbed into λ. A translate p + s is a different instance of the hypothesis, and the conclusion doesn't depend on p.
2. **Coset step.** It follows from the source zero support, the surjectivity of p, and the pullback formula.
3. **Regular A.** It forces t = 0, given t ∈ E[2] from the coset step.
4. **Common divisor.** Using the same divisor is legitimate. d is one integer for all three nonzero fibers. The proof never equates e_B and e_C; it compares only the target multiplicities with d.
5. **Logic.**
   - R and V never appear in lines 608–667.
   - The torus is E = C/(2Z + 2iZ). It isn't the unit torus R²/Z², where all corners lie over one point and the coset step fails. It isn't the C4 sphere either.
   - The cone numbers are ω_X multiplicities. At this odd-m B corner and this C corner, they agree numerically with the sphere map's local degrees (main §14).
   - In general they differ: an m = 6 B corner has ω multiplicity 3 but sphere local degree 6.
6. **Hypotheses and strength.** The theorem statement matches the proof once you add corrections 1, 2, and 4. The application at lines 669–683 is supported. Lines 684–685 overstate; see correction 6.

## Corrections

1. **Lines 637–638, with the input list at lines 610–615.** Add the input "X is connected (main §12)". Without it, (13.2) gives only a locally constant t. S and x_B could then lie on components with different shifts.
2. **Lines 610 and 613.** Main §10 doesn't prove input 2. Cite main §1 (integral corners), main §10 (even translations), and main §14 (π([p, g]) = g p mod 2Z²).
3. **Lines 648–651.** Add one sentence: [α] is a group endomorphism of E, so `[α](E[2])` is a subgroup of E[2]. The deduction "t ∈ E[2]" uses `[α](E[2])` = E[2].
4. **Line 621.** Write "finite-degree translation torus cover, with Y compact and connected". The surjectivity of f (line 643) and the nonempty fibers of p depend on it.
5. **Line 600.** The title says "fully singular torsion-fiber factors", but the theorem needs a common divisor d ≥ 2 of all nonzero-torsion multiplicities. Lines 689–690 already state this limit, so the title should match. For example: "common-divisor torsion-fiber factors".
6. **Lines 684–685.** "Stronger than Section 11" holds only for the factorization question. Section 13 makes Section 11's conditional hypothesis impossible for every O in the published family: no translation covering X → O exists. Section 13 doesn't exclude an abstract H_b-type block inside H_1(X), as line 688 states. Reword to say that.
7. **Lines 609 and 680–681.** State that X is the t = 0 surface. Off the grid, inputs 1 and 2 can fail (main §10).

## Counterexample search

No step fails. The review tested the step boundaries by hand:
- If N(α) is even, the coset has at most 2 points, which contradicts (13.3).
- If α is a unit modulo 2, then α ≡ 1 or i modulo 2. [1] fixes E[2], while [i] swaps 1 and i and fixes 1 + i. Both are bijective, as the proof requires.
- If t ∈ E[2] \ {0}, then f(S) lies in a wholly singular fiber, which contradicts e_S = 1.

## Optional notes

These notes aren't required for acceptance.
- **Affine factors.** The same proof works for locally affine factor maps with derivative A ∈ GL(2, R):
  - Input 1 forces A ∈ M_2(Z), and A mod 2 replaces [α] on E[2].
  - Affine branched covers satisfy the same multiplicity relation k + 1 = e(k′ + 1).

  This would extend the exclusion beyond complex scale. The gate doesn't claim it.
- **Fiber-wise refinement.** x_B always lands over 1 + i, because both residues of α fix 1 + i. So a version with fiber-dependent divisors is possible if a future target needs it.

## Files

- `src/my0912.pdf` is the downloaded source, and `my0912.txt` is its extracted text.
- `scripts/my_fibers.py` is the fiber check.

Nothing under `.context/illumination-k4-codex/` was edited.
