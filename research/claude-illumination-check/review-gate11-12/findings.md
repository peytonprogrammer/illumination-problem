# Review: pocket-reflection-gate.md Sections 11 and 12

Claude Opus review for Codex, 2026-11-02. An independent subagent ran the review. Claude saved this file and reran `independent-check.py` under `python3 -I`: exit 0, 41/41 PASS.

## Verdicts

| Section | Verdict | Basis |
|---|---|---|
| §11 | ACCEPT WITH CORRECTIONS | The math holds. Two unstated steps need a sentence each, and the scope wording overstates what is proved. |
| §12 | ACCEPT | The convention, norm identity, cancellation, and lattice disclaimer are correct. Two sharpenings are optional. |

## Reproduction

- **Copied checker.** `pocket-reflection-gate-check.py` is byte-identical to the original (SHA-256 `61da26b9…`).
- **Command.** Running `python3 -B pocket-reflection-gate-check.py` in this directory exits 0 with status PASS and 47 checks.
- **Output.** The generated JSON is byte-identical (`cmp`) to Codex's JSON.
- **Independent check.** `independent-check.py` rebuilds every matrix from the paper's index formulas, without the checker's typed blocks. It passes 41/41.
- **Source.** `https://arxiv.org/pdf/0912.1425` resolves to v2 (2010-10-06). The PDF has SHA-256 `5962546f…`.
- **Scope.** The review used exact rational arithmetic only. It ran no room, ray, direction, word, cylinder, or orbit scan.

## 1. Transcription against the primary source

Source sections: §3.3 (p. 24), §3.5 (p. 25), and §3.7 (pp. 26–28).

- **S table (§3.7).** S̃σ̆_i = σ̆_i + ζ̆_{i−1}, and S̃ζ̆_i = ζ̆_{i+1}.
- **T table (§3.7).** T̃σ̆_i = σ̆_{i−1}, and T̃ζ̆_i = ζ̆_i + σ̆_{i+1}.
- **Agreement with §3.3.** Both tables also follow from the §3.3 a_i/b_i table, using σ̆_i = a_i + a′_{i−1} and ζ̆_i = b′_i + b_{i−1}.
- **Matrices.**
  - The basis is (σ̆_0, σ̆_1, ζ̆_0, ζ̆_1), with σ̆_2 = −σ̆_0 − σ̆_1.
  - With P = [[0,−1],[1,−1]], the paper gives S = [[I,0],[P²,P]] and T = [[P²,P],[0,I]].
  - Both match the checker exactly.
- **Intersection form (proof of Lemma 3.4, p. 28).**
  - The values are (σ̆_i,σ̆_{i+1}) = (ζ̆_i,ζ̆_{i+1}) = 6, (σ̆_i,ζ̆_i) = −4, and (σ̆_i,ζ̆_{i±1}) = 2.
  - The review rederived all four from the paper's γ/δ table.
- **Reduction to four coordinates.** The 6×6 Gram matrix kills Σσ̆_i and Σζ̆_i, so the reduction is consistent. It matches Ω_b at lines 467–470.
- **Convention.**
  - The tables give the push-forward action, with images as columns.
  - On H1st, S̃σ = σ + ζ matches S = [[1,0],[1,1]] acting on hol(σ) = (6,0).
- **Composition.**
  - R = T⁻¹ST⁻¹ has derivative J, the counterclockwise quarter turn.
  - The word is a palindrome, so composition order can't matter.
  - A row reading of the tables would give R⁻¹, which only flips the sign of G.
- **Extra consistency checks** (not in Codex's checker):
  - The braid relation ST⁻¹S = T⁻¹ST⁻¹ holds.
  - R⁴ = I and (ST⁻¹)³ = R².
  - The deck action diag(P,P) preserves Ω_b.
  - R = −I on H_τ and R = J on T_0.
  - The fixed spaces of R and R² have dimensions 0 and 2, which confirms genus 0 and genus 1 at line 446.
- **Riemann–Hurwitz cross-check of line 446.**
  - R fixes A_0, A_1, A_2, and the zero over 1+i, and it swaps the zeros over 1 and i. Then χ(M) = −6 = 4·2 − (4·3 + 2), so the quotient is a sphere.
  - R² has 6 fixed points. Then −6 = 2·0 − 6, so that quotient is a torus.
- **Paper-side facts at lines 429–431 are confirmed.**
  - Aff^(1) fixes every regular A_i (§3.1, p. 21).
  - For q = 3, Aff permutes Σ through the full S_3 (§3.4).
  - H_τ is acted on through Z/2q = Z/6 (§3.5).
- **Transcription mismatches:** none.

### The result depends only on S and T

- The S,T-invariant antisymmetric forms on Q⁴ form a one-dimensional space. Exact rank computation confirms it.
- This follows because H̆(ρ) is irreducible and H̆(ρ) ≇ H̆(ρ̄).
- So the checker's two symplecticity checks fix Ω_b up to a rational scalar, and anisotropy is scale-invariant.
- Therefore the §11 conclusion depends only on the S and T tables. It would survive an error in the paper's intersection numbers.

## 2. Cylinder annihilator (lines 452–463)

The argument covers every cylinder, not only the generators' cylinders:

1. In each rational direction, the §7 construction gives an affine multitwist whose annuli exhaust that direction. All square corners lie over 0, so the construction applies to M.
2. The multitwist is unipotent, with N² = 0, because parallel cores are disjoint.
3. The affine group acts on H_0 through a finite group: Z/6 on H_τ, and Z/3 × SL(2,Z/3) on H̆ (Lemma 3.3).
4. A unipotent map of finite order is the identity, so N_θ = 0 on H_0.
5. The sum-of-squares identity then forces every core to be orthogonal to H_0. Hence C ⊂ H_0^⊥ = T_0.
6. Horizontal and vertical cores have independent periods, which gives equality. This step doesn't need §1's symplecticity.
7. R² acts as +I on H_τ and −I on H̆. So K_- = H̆ holds, with no separate H_τ ⊥ H̆ input.

**Gap D2 (lines 453–455).** "Finite order by the source input" requires the multitwist to be an element of Aff(M,ω), and the text never says so. Add one sentence citing §7 or Thurston–Veech.

For M, K = H_0. So any zero-period class is cylinder-blind automatically, and the "if both lay in K" hypothesis at line 496 always holds.

## 3. Rational norm descent (lines 476–493)

- **Identity.** Set A = 2a−b+3d, B = 2c−d−3b, C = b, and D = d. Then −vᵀGv = A² + B² − 6C² − 6D². Both scripts confirm this.
- **Change of variables.** det N = −4, which is invertible over Q and prime to 3.
- **Descent.** The step is correct:
  - Mod 3, A² + B² ≡ 0 forces 3 | A and 3 | B.
  - Then 3(A₁² + B₁²) = 2(C² + D²) forces 3 | C and 3 | D.
  - Homogeneity finishes the argument.
- **Wording D5 (line 490).** "ALL FOUR original variables" could mean (A,B,C,D) or (a,b,c,d). Both readings work, because 3 ∤ det N.
- **Independent confirmation.**
  - −G diagonalizes over Q to ⟨4, 3, −8, −6⟩, and det G = 576 = 24².
  - By the Hasse invariant, −G is anisotropic over Q_2 and Q_3, and isotropic over Q_5 and Q_7.
  - So −G is the norm form of the quaternion algebra (−1,6)_Q, which is ramified at {2,3}.
- **Shorter equivalent proof (optional).** 6 isn't a sum of two rational squares, because 3 is inert in Z[i] and divides 6 once.
- **Real signature.** G has signature (2,2). The values −4 and 4 at line 474 are correct.

## 4. Lift choice and finite-cover transfer

### Lift (lines 441–442 and 515–517)

The choice is justified:
- Aff^(1) ≅ SL(2,Z) (§3.1), so R has order 4.
- Aff is the direct product Z/3 × SL(2,Z). Every other lift with derivative J is D^a·R, whose fourth power is D^a. So only a = 0 gives order 4.
- A clockwise identification gives R⁻¹. That changes G to −G on K_-, which preserves isotropy.

### Transfer (lines 502–513)

The transfer is valid under these hypotheses:
1. f: X → O is finite of degree n, with ω_X = c·f*ω_O.
2. f∘R_X = R_O∘f.
3. B ⊂ f^!H_1(O;Q).
4. hol(β_j) = 0, from §31.
5. R_X β_0 = β_1, R_X β_1 = −β_0, Ω(β_0,β_1) = 0, and β_0 ≠ 0.

It uses four standard facts:
- hol_X(f^!a) = c·n·hol_O(a).
- Ω_X(f^!a, f^!b) = n·Ω_O(a,b).
- f^! is injective over Q.
- f^!R_O = R_X f^!.

Corrections:
- **Gap D3.** The text doesn't show that R_O is the order-4 lift R. Add: R_O has derivative J and R_O⁴ = 1, so line 515 forces R_O = R.
- **Stronger than claimed.** The transfer never uses cylinder blindness on X. It excludes B from f^!H_1(O;Q) entirely. Separately, f^!H_0(O) ⊂ K_X, because f_* sends cores to multiples of cores. State both.
- **D6.** §13 (line 684) excludes M as a translation quotient of any literal-pocket room. If §13 holds, the transfer at line 502 has no room instance. Add a forward pointer.

## 5. Scope defects in §11

- **D1 (lines 417 and 495–500).** M lies in H(2,2,2). It has no cone-multiplicity-5 zero, so it carries no literal pocket (§13 input 3; pocket-detection §31, m = 5).
  - "THIS surface's full cylinder annihilator cannot hide the specified … neck plane" is therefore counterfactual.
  - Restate it as: "H_0(M)_- = H_b contains no nonzero rational v with Ω(v,Rv) = 0."
  - That statement is both stronger and exact.
- **D4 (line 446 versus line 503).** At line 446, X names the Matheus–Yoccoz surface. At line 503, X is the cover and O is that surface. Elsewhere, X is the room. Use M for the example, as the paper does.

## 6. Section 12

### Reflection convention (lines 538–545), checked against §31.1

- The annuli carry coset labels R^j{I,V}. Left multiplication gives V·R^j{I,V} = R^{−j}{I,V}, so A_j maps to A_{−j}.
- V reverses orientation and preserves U, so V b_j = −b_{−j}. Then V β_0 = −β_0 and V β_1 = β_1.
- These signs agree with §4's covariance Q V = A Q, where A = diag(−1,1). The derivative of left multiplication by V is V.

### Algebra

All of these check out:
- L implements i → −i.
- V_b is an involution, it's antisymplectic, and V_b R V_b = R⁻¹.
- The V_b-negative eigenspace is (a, 2a, c, 0).
- On that space, the restricted Gram matrix is [[−12,12],[12,−4]], which equals −4((c−3a)² − 6a²). That is (12.1).
- The block values 20, −4, and −16 sum to 0.
- R_3 b matches the display at line 563.
- V_3 b = −b and V_3 R_3 b = R_3 b.
- Rows 4 and 6 give [[0,−1],[1,0]], with determinant 1.

### Coordinate lattice versus surface

The distinction is explicit at lines 572–575 and 584–586.

### Optional sharpenings

- **S1. Three copies is the exact threshold for block-diagonal V.**
  - Two V-negative copies give q ⊕ q ≅ G, which is anisotropic; the script confirms this at Q_3.
  - Without the V constraint, two copies already work, for example e_0 ⊕ (e_0 − e_3).
- **S2. The conclusion holds for every blockwise compatible V,** not only V_b; other examples are V_b·g^k and V_b·R^k.
  - V_- is Lagrangian, and R maps V_- isometrically onto V_+.
  - So G ≅ q_V ⊕ q_V, and q_V has signature (1,1).
  - Three copies then give an indefinite rational form in 6 variables, which is isotropic by Hasse–Minkowski.
- **S3 (line 577).** Replace "an integral generating pair" with "a pair spanning a saturated sublattice of the coordinate lattice". This keeps the disclaimer visible in the summary sentence.

## 7. Checker audit

All 47 checks are fixed-matrix equalities, with no geometry and no search. The scope string is accurate.

- **Self-referential checks.**
  - Line 136 defines `triple_beta1 = R_3·beta0`. So the first column of "Triple neck quarterturn" holds by construction, and the second follows from line 115.
  - Lines 91–92 read a and b from `pairing`, so 2 of the 4 compared entries are self-equal.
- **Checks that echo inputs.** Line 109 (P³ = I) and line 110 (the typed inverse of T).
- **Consequences of other checks.**
  - Line 114 (R symplectic) and line 115 (R² = −I) follow from lines 111–113.
  - Line 116 (G symmetric) follows from lines 114 and 115.
- **Independent content.** Only 4 of the 9 source checks are independent: lines 111, 112, 113, and 120.
- **Count assertion.** `assert len(checks) == 47` at line 161 counts checks; it doesn't measure their independent content.
- **Not tested by the checker:**
  - R on H_τ and on T_0, which the genus claims at line 446 need.
  - The braid relation.
  - Deck invariance.
  - Anisotropy itself.
  - Transcription against the paper.

  `independent-check.py` covers all of these except transcription. Section 1 checks transcription by hand.
- **Strength.** Lines 112–113 aren't tautological. Because the invariant space is one-dimensional, they fix Ω_b up to scale.

## 8. Not verified

- The lecture-notes claims at lines 429–431 (§8.6 of the notes). The notes weren't supplied, and nothing in §11 depends on them.
- The citation `pp19--28` in `sources.json`. In v2, §3.1 begins on p. 18. Cite v2 explicitly.

## Files

- `pocket-reflection-gate-check.py` and its JSON: the copied checker and its replay output. `review-run-checker.log` is the run log.
- `codex-original-outputs/`: the original checker JSON and log, kept for comparison.
- `independent-check.py`, with its `.json` and `.log`: the 41-check independent rebuild.
- `source-0912.1425/`: the primary source, arXiv v2, as PDF and extracted text.

Nothing under `.context/illumination-k4-codex/` was edited.
