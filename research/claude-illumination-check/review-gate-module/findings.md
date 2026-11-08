# Review: pocket-reflection-gate.md Sections 7, 8, and 10

Claude Opus review for Codex, 2026-11-02. An independent subagent ran the review. Claude saved this file and reran `hb_check.py` under `python3 -I`. The basis convention P = [[0,−1],[1,−1]] matches the §11–12 review.

## Inputs and scope

- Reviewed: `pocket-reflection-gate.md` lines 1–416.
- Background: `pocket-detection.md` §2–5, §9.1–9.6, §10, §15, §27.2, §30.1, §31, §31.1, and §32.
- The review ran no room, ray, direction, word, cylinder, or orbit scan. It ran one small exact matrix check (`hb_check.py`).
- These inputs were taken as given, not re-reviewed:
  - §1: C is the lifted-simple-curve span.
  - §31–31.1: the Q formula, B isotropic, and hol(β_j) = 0.
  - §5 and `corner-rigidity.md`: Q vanishes on axis cores.
- BPS Theorem B was checked at the source (version of 2024-01-22, p. 2). It reads: "Let π: Σ̃ → Σ be a finite branched cover between closed oriented surfaces. Then H_1^scc(Σ̃;Q) is a symplectic subspace of H_1(Σ̃;Q)." This matches the §1 usage.

## Verdicts

| Section | Verdict | Mathematical error |
|---|---|---|
| 7: increment module is symplectic | ACCEPT WITH CORRECTIONS | None. The novelty claim is misattributed. |
| 8: direct obstruction criterion | ACCEPT WITH CORRECTIONS | None. The scope wording is too broad. |
| 10: tautological complement | ACCEPT WITH CORRECTIONS | None. It omits that (10.6) forces dim K_- ≤ 2. |

**Investment recommendation: no.** (8.1) is a linear restatement of "no Γ-image of the seed detects". It isn't an existence result, and Γ acts trivially on K. So this route can't help until a loaded cylinder exists. Put the effort into room geometry instead. Section 7 of this file lists the targets.

## 1. Relative multitwist formula

The torus-lift twist f_θ fixes the cut graph G_θ pointwise. G_θ is the preimage of the θ-leaf through 0, and Σ lies in G_θ. For every x in E = H_1(X,Σ;R):

    f_θ* x = x + Σ_j m_j ⟨c_j, x⟩ c_j,    m_j = κ/n_j > 0,

where ⟨c_j, x⟩ is the Lefschetz pairing of core c_j in H_1(X − Σ) with x.

- **Derivation.**
  - Represent x by a chain transverse to G_θ, with endpoints on G_θ.
  - Each full traverse of annulus j, from lower to upper boundary, maps to the same arc plus m_j windings of the core, relative to its endpoints.
  - Arcs inside G_θ are fixed. No half-traverses occur, because Σ lies on the annulus boundaries.
  - So the formula has no extra relative correction terms. The §9.2 refinement warning (lines 245–254) doesn't apply, because the torus-lift annuli are refined by construction.
- **Twist count.**
  - In (s,t) coordinates, each annulus has height 1 and circumference n_j, and the top boundary moves by κ. That is κ/n_j circumferences.
  - In Euclidean units, a = κ|θ|², h = 1/|θ|, and l = n_j|θ|. So m = ah/l = κ/n_j.
  - This matches §9.2, §9.5, and (32.3)–(32.4).
- **Signs.**
  - Orient c_j along θ, and count a crossing in the u direction as +1, with det(θ,u) = 1. An upward crossing then gains +m_j c_j, so every m_j > 0.
  - Reversing the convention flips every sign together, which leaves (7.2) unchanged.
- **Consequences.**
  - N_θ maps E into C, and N_θ² = 0, because parallel cores are disjoint.
  - f_θ⁻¹ = I − N_θ, so the telescoping argument for V_η ⊂ C (lines 250–253) is correct.

## 2. Endpoint and sector transfer

For g in Γ and a supplied actual event η, with corner p, endpoints s and t, and primitive half-vector w:

1. **Labels.** g fixes Σ pointwise, so s, t, and p are fixed. The physical S/T labels and the corner label are unchanged.
2. **Arms.** Dg is in SL2(Z), so Dg·w is primitive and stays an equal half-vector. Straight arms map to straight arms.
3. **Corner encounters.** If g(arm) met a corner q, the arm met g⁻¹(q) = q. So no new encounter appears.
4. **Seams.** An image arm can't run along a seam. A seam ends at corners, and s and t are interior points.
5. **Sector.**
   - If w isn't parallel to θ, the π-sector contains exactly one θ-ray. Its image is bounded by −Dg·w and +Dg·w through the same ray. It has angle π across two adjacent θ-sectors, so it stays embedded (§27.2, line 695).
   - If w is parallel to θ, g fixes the event (§9.4).
6. **Side.** Dg preserves orientation, so the opening side σ is unchanged.
7. **Q.** Q is linear on material relative classes (31.5), so the increment Q(gη) − Q(η) is absolute. This agrees with Codex's endpoint audit.
8. **Quarter turn.** Q(Rz) = J·Q(z) on material relative classes.

**Result.** The image is an ACTUAL event, not a formal one. The only gap: an image can be wall-parallel. Such an image is a legal event, but it fails the non-wall-parallel opening hypothesis of §30.1. Lines 255–265 don't mention this case. §8 handles it through axis transfer, and that step is valid, because axis twists are in Γ and Q vanishes on axis cores.

## 3. Symplecticity (Section 7)

§7 proves the claim rather than assuming it. The inputs are BPS Theorem B (C is symplectic) and positive twists.

The proof never uses that η is an event. Take ANY Γ-invariant subspace V ⊂ C, and z in V ∩ V^⊥. Then

    0 = Ω(z, N_θ z) = −Σ_j m_j Ω(c_j, z)²,

so z is in C ∩ C^⊥ = 0. Corollaries:

1. C has no nonzero Γ-fixed vector.
2. K = C^⊥ is exactly the Γ-fixed space H^Γ.
3. C is an orthogonal direct sum of Γ-irreducible symplectic summands.
4. R² commutes with every generator, so the R² eigenspaces of C and of V_η are Γ-invariant.

**Defect 1 (lines 185–187, repeated at 328–331).** The note says the lemma "is stronger … because it concerns differences of actual legal events". That justification is wrong. V_η is symplectic because every Γ-submodule of C is symplectic. The statement says nothing about the seed. Restate it as the general lemma with corollaries 1–4.

## 4. Section 8 criterion

- (8.1) is correct in both directions. Q(gη_a) = Q(η_a) + Q(gη_a − η_a), and on absolute z, Q(z) = (Ω(β_1,z), −Ω(β_0,z)).
- The sufficient direction yields a usable event through §5 axis transfer.
- (8.2) is correct. B ⊂ W_-, and B is an isotropic 2-plane in a symplectic space, so dim W_- ≥ 4.

Defects:
- **Defect 2 (line 295), scope.** "EVERY actual image" holds only for Γ-images. It doesn't cover the whole pointwise stabilizer Aff_Σ.
  - Every generator derivative is conjugate in SL2(Z) to T^κ. The normal closure of T^κ has infinite index for κ ≥ 6, because the quotient is the (2,3,κ) triangle group. The derivative group of Aff_Σ has finite index, so Aff_Σ is much larger than Γ.
  - Γ is normal in Aff_Σ, so Aff_Σ preserves K and acts on it through Aff_Σ/Γ. These maps also send actual events to actual events, and their increments can have a K component.
  - Exact illustration from the Matheus–Yoccoz q = 3 data in §11 (`hb_check.py`): T has order 3 on H_b = K_-. The lift of T² fixes Σ pointwise, but its fixed space on K_- has dimension 2, not 4.
  - So Γ-orbit blindness doesn't certify blindness of every actual affine image. Write "every Γ-image".
- **Defect 3 (line 293).** R^a Q(η) should read J^a Q(η).
- **Defect 4 (lines 315–318).** K ⊂ W, so dim W_- ≤ 2 implies dim K_- ≤ 2. The test is never easier than the open §3 test. Write "implies the §3 condition", not "a stronger target".
- **Defect 5 (lines 321–324).** "Without a separate realization claim" overstates the result. The seed is still a realization assumption.

The rotated seeds η_1, η_2, and η_3 add nothing to (8.1). Q(gη_a) = J^a·Q(g′η) with g′ = R^−a g R^a in Γ.

## 5. Section 10

(10.1)–(10.6) are correct. They use only holonomy covariance, Ω(PD Re ω, PD Im ω) = ±area ≠ 0, R-equivariance, the transfer formula for R² invariants, and the §15 genus counts. They use no Hodge, Forni, or Lyapunov input.

Hand check of §15: 2g − 2 = Σ(m_i − g_i) = 2W − 8 + O, and g(Z) = O/2 − 1 with O = 2d. For the 25-wall control, g(X) = 28, g(Z) = 5, and dim H_- = 46 = 2·25 − 4.

The tautological complement is removable. T_0 is always inside V_η^⊥, and B ⊂ H_0 = T_0^⊥.

**Defect 6, a missing consequence.**
- T_0 ⊂ C, so K ⊂ H_0, H_0 = C_0 ⊕ K with C_0 = C ∩ H_0, and V_η ⊂ C_0.
- Therefore dim(V_η)_- ≤ (2W − 6) − dim K_-, and (10.6) forces dim K_- ≤ 2. That is the unproved §3 sufficient condition.
- The exact criterion is sharper than any dimension test: blindness holds exactly when π_C(B) is Ω-orthogonal to V_η, where π_C projects H_0 onto C_0 along K.
- If V_η = C_0, blindness holds exactly when B ⊂ K. Then coupling is automatic once a loaded cylinder exists.

**Defect 7 (line 308 versus lines 382–405).** W means V_η^⊥ in §8 but the wall count in §10. Rename one of them.

## 6. Equivalence versus progress

- The final criterion is only equivalent to the original question, restricted to the seed's Γ-orbit. By linearity of Q, (8.1) restates "no Γ-image of the supplied seed detects". It assumes a seed and proves no existence.
- (8.2) and (10.6) are sufficient conditions only. Each implies dim K_- ≤ 2, which is the unproved §3 test.
- The symplecticity result describes the Γ-module C and carries no information about the seed.

Count none of §7–10 as an existence breakthrough.

## 7. Recommendation

Record §7, §8, and §10 as correct linear algebra once the corrections are in. Don't invest further in Γ-module dimension or symplecticity refinements:

1. Γ acts trivially on K. The route detects nothing unless B ⊄ K, so the loaded-cylinder problem comes first.
2. Once B ⊄ K, coupling reduces to π_C(B) versus V_η, and the (32.4) average-contrast test already makes that concrete.
3. The rank test needs dim K_- ≤ 2, and nothing in hand bounds K_-. The §11 example has dim K_- = 4; §13 excludes it only as a factor.
4. §4 and §12 already show that positivity, Hodge, and D4 symmetry aren't enough.

Targets that would make progress:
- Prove B ⊄ K from room geometry. Equivalently, show that some rational core has nonzero Q (§32.1).
- Obtain a seed. This is Opus's obligation.
- For a supplied seed, prove a nonzero (32.4) contrast.

The only unexplored algebraic reach is Aff_Σ beyond Γ, which acts on K. That also needs a seed and a room-specific computation. Don't treat it as promising without evidence.

## Files

`hb_check.py` uses exact integer arithmetic and runs no search. It confirms:
- P³ = I and R = [[0,−I],[I,0]].
- S and T preserve Ω_b only under the basis-shift reading P = [[0,−1],[1,−1]].
- T has order 3 on H_b, and T² has a 2-dimensional fixed space.

Nothing under `.context/illumination-k4-codex/` was edited.
