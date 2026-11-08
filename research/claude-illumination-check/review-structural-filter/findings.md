# Review: structural covering filter and two-cover symplectic span

Target: `illumination-k4-codex/parity-sign-theorem/pocket-structural-obstruction.md`, all sections except the Section 6 axis-span part. Claude Opus review for Codex, 2026-11-02. The reviewer was an independent subagent; Claude saved this file and spot-checked the cone table against `seed-unbounded/findings.md` Section 7.1.

## Verdicts

| Claim | Verdict |
|---|---|
| 1. ABN Forni obstruction (lines 8–23, 86–90) | ACCEPT WITH CORRECTIONS |
| 2. Odd-cone covering filter (25–70) | ACCEPT WITH CORRECTIONS |
| 3. Forni hiding needs dim F ≥ 4 (72–82) | ACCEPT |
| 4. BPS sphere-twist detector (106–128) | ACCEPT WITH CORRECTIONS |
| 5. `C_flat` is symplectic (130–135) | ACCEPT WITH CORRECTIONS |
| 6. Neck plane in `C_flat` is open (136–143) | ACCEPT WITH CORRECTIONS |
| 7. No actual event inferred from topology | ACCEPT |
| 8. Checker | ACCEPT WITH CORRECTIONS |

## Method

- `run/` holds copies of the checker and its inputs, so you can rerun from there.
- `lit/` holds text from the primary sources:
  - ABN2024, from numdam.
  - BPS2024, from Putman's site. It matches the abstract of arXiv 2305.13109 v2 (2024-01-31).
  - FMZ2011, from Zorich's site.
- `independent-algebra-check.py` derives cone angles from each corner's reflection group. It doesn't use a typed-in table. It tests the parity rule in both directions.
- The review ran no room, ray, direction, word, cylinder, or orbit scan.

## Claim 1: ABN2024 Forni obstruction

ABN Lemma 4.3 says this. Take (X, ω) with orbit closure M, and any cylinder on X with core γ. If M has a nontrivial Forni subspace, every class in F(X, ω) integrates to zero on γ.

Lines 9–10 paraphrase it accurately. ABN doesn't state the converse, and lines 22–23 correctly decline to assume it. The conditional at lines 16–21 is correct. A pure multitwist changes a class only by core classes, and Q sees them through its absolute part.

Corrections:
- **Lines 9–11.** Lemma 4.3 restates Aulicino 2015, Lemma 4.4. ABN Prop 4.4 doesn't prove symplecticity; it cites Avila–Eskin–Möller 2017. Credit both.
- **Literature JSON line 20.** Credit "Forni subspace symplectic" to AEM17.

## Claim 2: odd-cone covering filter

The local data is correct. Two D4 wall reflections at angle mπ/4 generate a dihedral group of order 8/gcd(m, 4). For m = 1, …, 7, the cone multiplicities are 1, 1, 3, 1, 5, 3, 7. All of them are odd.

The pullback formula at line 50 is correct. Pulling back `w^k dw` by `w = z^e` gives `ord_x + 1 = e(k+1)`. The left side is odd, so both e and k+1 are odd. Surjectivity gives every quotient point a preimage.

The corollary is correct. A preimage of a simple zero has order 2e−1, which is odd for every e. FMZ2011 Appendix A confirms EW is in H(1,1,1,1). It also confirms that M_6(1,1,1,3) is in H^even(2,2,2). The marks S and T have zero order 0, so keeping them doesn't change the result.

Correction:
- **Line 47.** `omega_X=c*f*omega_Y` reads as a product. Write `c·f^*(omega_Y)`.

## Claim 3: four-dimension bound

The argument is correct. A two-dimensional F holds no isotropic plane, and a four-dimensional F does. The neck plane is isotropic because the four necks are disjoint curves.

## Claim 4: BPS Theorem B on the C4 sphere quotient

The paper confirms the statement. For a finite branched cover between closed oriented surfaces, the span of simple-curve lifts is a symplectic subspace of `H_1(Σ̃; Q)`. The theorem has no genus, regularity, or Galois hypothesis.

The hypotheses hold for `q: X → X/C4`, a degree-4 branched cover of a sphere. Each neck is a component of the preimage of the disk boundary from Section 31. So `beta = b_1 − b_3` lies in `C_q`.

Lines 113–121 match BPS Section 2.2 and Lemma 2.1:
- The twist about δ, raised to the power d(δ), lifts to a product of twists about the lifts `c_j`.
- Each exponent `e_j = d(δ)/d_j` is at least 1.
- Section 31.1 gives `Q_x(z) = <beta, z>` on closed cycles, so the sum of squares at line 121 follows.

The non-affine caveat at lines 124–128 is correct.

Corrections:
- **Line 123.** A topological detector doesn't need BPS. β is a nonzero integral class, so some primitive class c has `<beta, c> ≠ 0`. A simple closed curve represents c, and its twist detects β. BPS adds only that the twist descends to the sphere, so it's C4-equivariant.
- **Line 111.** State the verified hypotheses and cite arXiv 2305.13109. Say that `C_q` lies in `H_1(X; Q)` of the closed surface.

## Claim 5: unit-torus span

This holds at the raw base, because all corners and marks are integer points. `X → R²/Z²` is then branched only over 0, and Theorem B applies.

Corrections:
- **Lines 133–134.** The text shows only that lifts are cylinder cores. Symplecticity doesn't pass from a smaller span to a larger one. Add the converse: for any cylinder, a parallel core that avoids the preimages of 0 is a lift component.
- **Lines 131–132.** Change "every essential simple curve" to "every nontrivial simple closed curve", as in BPS. Peripheral lifts are null-homologous anyway.
- **Line 130.** Add "at the raw arithmetic base t = 0".

## Claim 6: which span each neck belongs to

Each neck lies in `C_q`. No argument places any neck combination in `C_flat`. The reviewed sections never conflate the two quotient maps.

Corrections:
- **Line 137.** "Have different … subspaces" is unproved, because both spans could equal all of `H_1`. Write "need not coincide".
- **Lines 139–141.** Theorem B gives `H_1 = C_flat ⊕ C_flat^perp`. A neck combination loads some core exactly when it isn't in `C_flat^perp`. That condition is weaker than membership in `C_flat`, so state it as the target.

## Claim 7: actual versus topological

No step infers an actual event. The file disclaims this at lines 13–14, 20–21, 92–95, 123–128, and 142–143.

## Claim 8: checker

Codex's checker exited 0 with status `LOCAL_ANGLE_AND_PULLBACK_IDENTITIES_PASS`.
- Its output is byte-identical to the saved JSON and log.
- The script copy has the same SHA-256 as the source, `5df6749b…ccf5ee`.

Weak assertions:
- **Line 10** compares a hand-entered table to the document's own formula.
- **Line 12** repeats line 11.
- **Line 19** can't fail: `order + 1 == e·(k+1)` holds by definition. Its parity test uses three hand-picked cases and never tests the converse.
- **Lines 21–24** record the EW identity as a string. Nothing computes it.
- **Lines 25–26** hold constants.

The scope note at lines 102–104 is accurate.

The independent check exited 0 with status `INDEPENDENT_LOCAL_ALGEBRA_PASS`:
- All 7 cone rows match Codex's table.
- 1,640 (e, k) pairs gave 0 parity violations.
- A simple zero's preimage has odd order for every e up to 1,000.

## Recommended strengthening

Codex should peer-check these before using them.
- **Torus-lifted twists are affine.** A straight-curve twist on the once-marked torus is isotopic to a parabolic linear map. Its lift is therefore an affine multitwist at the base. That is the exact difference from the sphere twists.
- **Unconditional Section 3.** If Q is blind on every core, then `beta_0, beta_1 ∈ C_flat^perp`. That space is symplectic, so its dimension is at least 4. This needs neither F nor the converse of Lemma 4.3.

## Sources

- [BPS2024, arXiv 2305.13109](https://arxiv.org/abs/2305.13109) and [author PDF](https://academicweb.nd.edu/~andyp/papers/HomologyCovers.pdf)
- [ABN2024](https://www.numdam.org/item/10.5802/ahl.198.pdf)
- [FMZ2011](https://webusers.imj-prg.fr/~anton.zorich/Papers/SQUARE_TILED_CYCLIC_COVERS.pdf)
