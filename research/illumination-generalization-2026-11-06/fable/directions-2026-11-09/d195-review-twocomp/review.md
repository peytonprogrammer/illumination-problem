# Review of d195 "Return through the non-target gate (partial)"

Note: `snapshot.md`, sha256 `800033b96b0d…` (prefix 800033b9 confirmed).
Script: `checks.py` → `checks.log`. 8 exact checks, 0 failures, 4.7 CPU-s.
The script uses only parameters the note names. It runs no room, ray, direction, word or size search.

## Verdict

**PASS WITH CORRECTIONS.** Confidence: about 85%.

The local calculation is exact. The return phase is y+Av. The strict clearance test is sufficient and necessary for the stated strip itinerary. The note labels its limits correctly: it claims no dark family and no area bound. The corrections are about stating hypotheses and residuals precisely. None breaks a claim.

## Checks (a)–(d)

### (a) Conditional excursion claim: correct

- **Endpoint equation.** The leftward partial travel j−ℓ, the excursion 2A, the full return j and the target leg B give 2z ≡ e−s−(B+2j−ℓ+2A)v (mod 2Z). Verified on 40,000 exact instances, for both solutions z.
- **Three phases.** The first contact is s+(j−ℓ)v+z = y−Av, with y = (e+s−(B+ℓ)v)/2. The far wall is at y. The return is at y+Av. Verified. The two solutions z differ by Z, so y is fixed modulo Z and has two lifts modulo 2Z. That's the meaning of "two candidate midpoint phases".
- **Strict clearance.** The height is linear in horizontal distance with one slope on both legs. So the path stays strictly inside (l,r) if and only if l+|Av| < y < r−|Av|. Verified on 20,000 instances. Strictness gives an open v-window.
- **Period shifts.** With solid strip walls and kP·A ≡ 0 (mod 2(r−l)) per leg, the shifted ray returns at y+Av with the same vertical sense. Verified on 1,425 instances. A shift without this congruence can change the exit (one explicit example). The note's split at the far-wall turn is needed and correct.
- With the congruence, the excursion adds no new rotation frequency. Only d194's f remains. The note doesn't claim an area bound from this, which is correct.

### (b) Limit-of-method paragraph: correct, correctly labeled

- d192's window fixes a mark and varies the speed. Here the entrance y−Av moves with v, and the same v fixes the return y+Av. So the window doesn't apply as stated. I can't rule out an adapted version, and the note doesn't claim one is impossible.
- Within a fixed approach interval J, the speed is bounded away from 0. So the needed clearance is at least |A|·v_min > 0, and "v near zero" gives no limiting argument. Check 8 confirms the sharp form: a contact approaching a strip end at rate c passes at small v exactly when c > A.
- A finite component count gives no decreasing parameter, because a seam cut can return to the original component. This is correct.
- The paragraph says "neither a dark family nor an area bound … has been proved". It isn't mislabeled as darkness or as a bound.

### (c) Parallel residuals: correct in substance, imprecise in wording

- "A repeated full traversal can cancel the terminal-height divisor." In d194, coefficients −1,+1 give S_b = 0, which makes (2) vacuous. "Cancel" is loose (Low 2).
- "A target already in a grounded cell." d194 excludes targets on the boundary of or inside the closure of the grounded union. The boundary case should be named (Low 2).
- d194 also listed partial terminal widths that involve the free source coordinate. The note omits it (Low 2).

### (d) d194 corrections: four of five folded in

| d194 item | Status |
|---|---|
| Medium 1, q₀ uniform bound | Folded: q₀ ≤ 2(H+b)/(Bη) ≤ 2(H*+b_max)/(B_min η). Check 6 passes. |
| Low 1, K tail target | Folded: tail < 1/2, below the constant term. Check 7 passes. |
| Low 2, b ≥ 1 | Folded. |
| Low 3, connectedness | Folded: each sealed component touches an open mouth. |
| Low 4, open-case ranking | Folded: "first open case for the inside-column row". |
| Low 5, constants cost a power of H* | Not repeated (Low 3). |

## Corrections by severity

### High

None.

### Medium

1. **Headline hypotheses.** The Advances line states only the base-speed strip test. Any use inside d194's k-shift argument also needs the period-shift hypotheses: solid horizontal walls at l and r over the excursion width, and kP·A ≡ 0 (mod 2(r−l)) per leg. Put both in the headline. Otherwise a reader can apply an "unobstructed strip" where the shifted ray leaves it.

### Low

1. **Speed radius.** The excursion raises the mismatch derivative to B+2j−ℓ+2A and the contact rate by A. Restate d194's radius rule r < clearance/(4(2X+j+A+1)), or say that the old rule is replaced.
2. **Residual wording.** Say "(2) is vacuous, S_b = 0" instead of "cancel". Say "on the boundary of or inside the grounded union". List the partial-terminal-width residual.
3. **Constants.** Repeat that the area constant is at least a fixed power of H*.
4. **Representatives.** Say "y is fixed modulo Z; its two lifts modulo 2Z are the candidates". The current sentence attributes the two choices to the wrong modulus.
5. **Notation.** A is the excursion distance and A_aspect the aspect numerator. The rename is fine. Keep it in later notes.

## Scope

- The inside-column pair type of d194, with H < b and both virtual contacts in open gates of another upper component.
- Base speed: one horizontal strip (l,r) in the neighbour, clear over width A, gate open and far wall solid on (l,r).
- Period shifts: additionally solid strip walls and the integrality congruence in a fixed integral decomposition.
- No claim covers contacts within |Av| of a strip end, multi-strip excursions, or the two parallel residuals.

## L1 advance

Small and conditional. The note turns d194's open case into an explicit, checkable gate test with exact phases. It doesn't close any pair type unconditionally. No ledger word moves. The W = 10 word LLLRLLLRLR stays open, and its quoted realization matches d194. The W ≤ 20 estimate doesn't change from this note.

## First open case

Inside-column row, H < b, both contacts in open gates. For the given approach J, every usable v and contact sheet puts y within |Av| of an end of every clear strip through the gate. Equivalently, the contact moves toward a strip end at rate at most A. Closing it needs either a different controlled return (for example multi-strip or through a third component) or a construction showing these placements are dark.

## Convergence of the occupied-crossing line

I read d194's review and this note, not d189–d193 in full. On that evidence, the line is fragmenting into subcases, not converging toward a chart-wide K(C). Each note closes one pair type under added hypotheses: a solid side, H ≥ b, a clear strip with clearance |Av|, solid strip walls, integrality. Each also opens two or three residuals. This note states the core obstruction itself: revisits are unbounded and the finite component count gives no decreasing parameter. A chart-wide K(C) needs a uniform bound on how the itinerary uses the chart, and no note in the line supplies one. Until a global invariant appears, further local gate tests will keep producing conditional returns. The better next step is to test whether the strip-end placement admits a dark family, or to find a parameter that a seam cut provably decreases.
