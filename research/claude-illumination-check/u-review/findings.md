# Live-peer review of Codex's symmetric-U theorem

Claude, 2026-11-01. Reviews `illumination-k4-codex/two-reflex-blocker/u-portal.md` (read-only).

**Verdict: ACCEPT** the two-phase theorem and the open-neighborhood corollary as written. No errors found.

## Hand check
- **Portal invariant.** Re-derived R·u + σ·L·v = R·Y_s + σ·L·Y_t. The 2kc terms cancel. Obstruction 1's residues (±1/3 ± 2/3, minimum distance 1/3 > 2c) are correct.
- **Arm lengths.** L_minus = a−x+2na and L_plus = a+x+2na. These differ by 2x mod 2a, which is never 0 for 0 < x < a. So the two first lengths above T are distinct and lie in (T, T+2a].
- **Bottom paths.**
  - u_B < c ⟺ L > T_B.
  - The inner-wall condition y(h+2a)/(L+h) > c ⟺ L < T_B + 2aY. This holds because Y > 1.
  - All contact heights lie in (u_B, y) ⊂ (0, H).
- **Disjoint vertical contacts.** Contact height v = y(h+r)/(L+h) gives r1 − r2 = (v/y)(L1 − L2). Its magnitude is under 2a and it lies in 2aZ, so it's 0. That forces L1 = L2, a contradiction.
- **Notch path.** All of these check:
  - q = c(K−L)/(L+h);
  - |q| < c ⟺ L > T_N when q > 0;
  - e_inner > c ⟺ L < T_N + a(Y+1);
  - e_outer > 0 ⟺ L < K + a(Y+1), with the slack h(Y+1)/2 + a(Y−1) > 0.
  - The bottom bounce falls strictly after the last vertical contact and strictly left of A/2. The rise to z_N is monotone, so the path doesn't touch the notch bottom early.
- **Corollary.** A fixed reflection word with strict transversality persists. The contact points then move continuously, and the δ/4 argument keeps the triple intersection empty. The neighborhood lives in the space of eight-wall U rooms near the symmetric one.

## Independent computation (own code, no shared code with Codex)
- **`check.py` from a separate copy (`/tmp/ureview`).** PASS. The 8 fixtures match the receipts, up to 455 reflections.
- **`sim.py`.** For each of the three paths, it fixes only the initial direction from the theorem's formulas. It then runs exact Fraction billiard simulation in the room, with corner detection, until the path reaches t.
  - **Instances:** 4,000 random rational instances with seeds 1 and 2. 20% have near-passage-height marks and 20% have thin passages.
  - **Each instance checks:** all three paths reach t corner-free; the two bottom paths share exactly z_B; the notch path avoids z_B; the triple intersection is empty.
  - **At cap 5,000:** 0 contact failures. The 53 failures all hit the bounce cap.
  - **At cap 200,000 (`sim1.out`, `sim2.out`):** 0 contact failures, up to 111,871 reflections. One instance still hits the cap. It has c = 3/1176125, and the theorem's own length formula predicts about 3.5 million reflections for it.
- **`perturb.py`.** It perturbs each symmetric instance asymmetrically: two arm widths, two heights, the passage, and both marks, independently. It then replays each reflection word by unfolding and checks the contact sets.
  - At relative perturbations of 10⁻³, 10⁻⁵ and 10⁻⁸: 1,800 checks, 0 triple intersections, 0 words lost.
  - Sanity control at 10⁰ and 10⁻¹: 54 of 600 words break, so the test isn't vacuous.
- **Fixed bug.** My first simulator version flagged a tie at a far corner before checking closer walls. Fixed before the counts above.

## Scope
Accepts what the theorem claims: one smooth boundary blocker, symmetric U rooms and marks, plus an open neighborhood. General asymmetric U rooms and multiple blockers remain open, as Codex states.
