# d189 review: an upper chamber replaces the upper run

**Verdict: PASS WITH CORRECTIONS.** Confidence: high (about 85%) that the
theorem is correct as scoped. The corrections are about labeling and scope,
not proof steps.

Date: 2026-11-22. Reviewer: independent referee. Reviewed file:
[snapshot.md](snapshot.md), sha256 `5a2e76a1…9082675`. Reviewed bases:
`l1-cross-cap-budget.md` and `l1-crossing-gap-transfer.md` (reviewed in
[d186](../d186-review-crossing/review.md)), `l1-mixed-seed-normals.md`
(reviewed in [d188](../d188-review-mixedseed/review.md)) and
`l1-gap-hyperplanes.md`. The stable first-hit argument is in
`qclass-closure/bbbb/README.md`, which the note links.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.04 CPU seconds with exact `Fraction` arithmetic. `trace()`, `shoot()`,
`st()` and the simplicity helpers are copied verbatim from d188. The log has
134 PASS lines, several INFO lines and 0 failures.

The only room family is the st279 (m=5) crossing slice `st(a,D)` that the
note names. It appears on the d188 ray a = 7+2n, D = 3a at d188's 8 named n,
and on the note's family D = a(a+2) at a = 9 and a = 101. Here a = 9 is the
least odd a meeting the note's own condition Dδ > 4h, solved in closed form.
Every traced velocity comes from a closed-form gate or root formula. No room,
ray, direction, slope, word or room-size search was run.

## Bottom line

The note generalizes d186's cap budget in two directions. Several roof mouths
are now allowed, if they lie in a fixed span [0,R]. The single upper run is
replaced by any fixed lattice end chamber, with arbitrarily many upper gates.
The key new step is a periodicity lemma for one stable upper path. It is
correct, and the log confirms it exactly at st279. The explicit box is correct
and reduces to d186's constants when B = 1.

| Claim | Verdict |
| --- | --- |
| (a) Stable first hit in the sealed chamber; nonintegral level abscissas | **Correct.** Lattice T plus irrational slope gives no lattice hits. Stability is the README argument |
| (a) Periodicity: v₀ + kP keeps the same seam z, intercept e + BkP | **Correct.** Only runs that the path visits enter. See Low 1 on the definition of P |
| (b) Route switching through arbitrarily many upper gates | **Correct.** One open path interval carries every gate, so no per-gate clearance is needed |
| Gate (A+B)v₀ ∈ e−c+g_Aℤ, g_A = gcd(2D,AP) | **Correct.** Exact elimination of k |
| Floor-corner count and threshold aη > 2dP(2d+1) | **Correct** |
| (1) (a+B)(a+2d+B)η² ≤ 4dPD | **Correct.** gcd divides 2dP and lcm divides 2D, checked at 5 named pairs |
| Bounded modulus on affine rays, Δ_j constant, subsequence stabilization | **Correct.** At d188's ray, Δ₀ = 0 and Δ₂ = −12. The floor modulus is 6, and 6 divides 144 |
| Far-wall return guards every mouth in [0,R] | **Correct.** Traced at a = 9 and 101 |
| (c) Box a ≤ max{d, 2dP(2d+1)/η, 32dP/(δη²)}, D ≤ 4(a+d)/δ | **Correct.** At B = 1 the constants equal d186's. See Low 3 on a factor of 2 |
| (d) Scope: fixed d, mouths in [0,R], fixed upper chamber | **Matches the proof.** Two implicit hypotheses should be stated (Low 4) |
| st279 family D = a(a+2): both short-route moduli ≥ 2a | **Correct.** g_a = 2a·gcd(a+2,3) and g_(a+2) = 2(a+2)·gcd(a,3) |
| D = 3a floor spacing gcd(6a,6(a+2)) = 6, whole ray lit | **Correct.** All 8 named n traced |
| (e) Relation to d188: ≥ 1 normal per seed, k ≤ 22 | **Correct and correctly conditional** |
| First open case | **Correctly named but incomplete** (Medium 1) |

## 1. The periodic upper approach

**First hit.** T is a lattice point. A backward ray of irrational slope from T
meets no other lattice point. So it avoids every developed vertex and mouth
endpoint. The square-tiled unfolding has no saddle connections in irrational
directions, so the flow is minimal. The README argument then gives a finite
first mouth crossing and an open stability interval of slopes. At every
integer level the elapsed vertical travel is an integer. The abscissa is
therefore an integer plus an irrational, so it is nonintegral. On nearby
slopes the finite list of strict level events persists.

**Parameterization.** With unit vertical speed and seam speed v, the unfolded
target abscissa is z + Bv. B counts all vertical travel, including reversals
at horizontal walls, and it is an integer. e is an integer because T is a
lattice point and every wall is integral. So z = e − Bv on a stable interval J.

**Periodicity.** Between consecutive integer levels the chamber's cross
section is constant. The path stays in one run of integral width W, whose
sides are smooth walls on that open band. A change of kP in horizontal speed
moves the unfolded unit-step exit by kP, a multiple of 2W. The folded exit
point is unchanged. The number of lateral reflections changes by kP/W, which
is even. So the exit direction keeps its sign relative to the original, and the
signed speed differs by ±kP again. Whether the path passes a level or reflects
there depends only on the folded point, which is nonintegral. Induction over
the B unit steps proves the claim. The upper path also never recrosses the
mouths, because its events are the same as before.

The log confirms this exactly in st279. Three seam points z = 1/4, 1/2 and 3/4
are each traced at k = −10, −3, −2, −1, 0, 1, 2, 3 and 10. Every path reaches
T = (6,6) with no horizontal contact and exactly 2|k| lateral reflections.
At k = 1 the speed changes sign, as the note allows.

**(b) Many upper gates.** Every gate on the upper path is part of one stable
path, so J already certifies all of them at once. This removes d186's second
open item, "a second gate on the upper leg".

## 2. The two short routes

**Gate.** The positive-sheet condition is c + A(v₀+kP) ≡ e − Bv₀ (mod 2D).
As k ranges over ℤ, this is (A+B)v₀ ∈ e − c + gcd(2D, AP)ℤ. That is exact.
The direct ascent touches the roof only at z and never reaches y = 0. So it
meets no corner, and every solution is legal.

**Floor corners.** Changing k by 2D/g_A keeps the gate. If g_A > 2dP, the
floor phase moves by 2dP/g_A ∈ (0,1), so two consecutive choices aren't both
corners. If g_A ≤ 2dP, a corner fixes v = (jD−c)/d. Then
z ≡ c + (a+2d)(jD−c)/d (mod 2D) depends only on j mod 2d. Since z lies in
(0,R) ⊂ (0,D), at most 2d values of v₀ are bad. An open window of length
(A+B)η > (2d+1)g_A holds at least 2d+1 gate points. So aη > 2dP(2d+1)
forces a legal floor shot whenever g_A ≤ 2dP.

**(1).** On failure, (A+B)η ≤ g_A for both A = a and A = a+2d. The gcd of the
two moduli divides gcd(aP, (a+2d)P), which divides 2dP. Their lcm divides 2D.
So g_a·g_(a+2d) ≤ 4dPD, which gives (1). The log checks the gcd and lcm steps
at 5 named pairs. At st279, with d = 1, B = 1, P = 6 and η = 1, (1) reads
(a+1)(a+3) ≤ 24D. That's d186's reviewed inequality.

**The d188 ray in v-form.** On a = 7+2n, D = 3a the direct modulus is 6a.
No direct v-gate solution exists, matching d188. The floor modulus is 6 for
every odd a. The log solves the floor gate in closed form at all 8 named n and
traces each shot. Every trace reaches T, and its only horizontal contact is
the floor. At n = 0 the seam speed is 23/5, which equals d188's floor velocity.
Other n use a different representative k, so the speeds differ from d188's
table. The route class is the same.

**Bounded modulus on affine rays.** qD − p(a+j) = qD₀ − p(a₀+j) = Δ_j is
constant. The combination 2D·qP − (a+j)P·2p = 2PΔ_j gives g_(a+j) | 2P|Δ_j|.
The Δ values differ by 2dp ≠ 0. When R₀ = 2P|Δ_j| divides n, both inputs
agree with their base values mod R₀. So g_(a+j) equals its base value. On
d188's ray, Δ₀ = 0 and Δ₂ = −12. The direct modulus is unbounded, and the
floor modulus is 6, which divides 144. At n = 144, 288 and 1008 it equals its
n = 0 value. All of this is correct. Low 2 notes that (1) already implies
eventual lighting on these rays.

## 3. The far-wall return

Translating J by kP with k ≪ 0 is legal by section 1. It makes v < 0, e′ < 0
and Rs < 1. With horizontal time, the arrival equation
d + s(2D−c−e′) − B = (2j+1)h is the upward positive-sheet roof condition at
z = e′ + B/s.

- **Outward leg.** Any point with x ≤ R lies within horizontal travel R of S,
  so it has risen less than Rs < 1 ≤ a. So it can't reach a mouth.
- **Return leg.** Roof visits are 2h/s > R apart horizontally. Only the last
  lies in [0,R], so no other mouth intercepts the shot. Intermediate roof hits
  are at x > R, so they aren't at mouth endpoints either.
- **Corners.** The only reachable corners are at x = D. The far-wall height
  step is 2h(D−c)/(2D−c−e′). It lies in (0,h) because e′ < 0 < c. So two
  consecutive roots can't both be corners.
- **Two roots.** (2D−c−e′)δ > 4h gives two roots, and 2D−c−e′ > D.

The log traces both consecutive roots at a = 9 and a = 101 on D = a(a+2).
Every shot reaches T with one lower lateral reflection, at x = 5−D. All roof
contacts are at z > R = 1, and the seam point is in the mouth. At these two
rooms the closed-form direct and floor gates have no solution (INFO lines).
So the far-wall route is the one that lights them, as the note says.

**(c) The box.** On failure, D ≤ 4(a+d)/δ. Combined with (1), this gives
a²η² ≤ 16dP(a+d)/δ ≤ 32dPa/δ for a ≥ d. Both stated bounds follow. Every
constant depends only on d, R and the upper data (J, B, P and the chosen k).
At B = 1, P = 2W and η = w the constants equal d186's: 4dW(2d+1)/w and
64dW/(w²δ). For B > 1 they are weaker by a factor of B, which is harmless.
The st279 instance gives a ≤ 384 and D ≤ 8(a+1). That's weaker than d186's
a ≤ 93, D ≤ 4(a+1), which uses the open-unit-door corner argument and the
2D coefficient. The note doesn't claim the st279 numbers.

## 4. The st279 counterexample to raw moduli

For odd a and D = a(a+2), gcd(2D, 6a) = 2a·gcd(a+2, 3) and
gcd(2D, 6(a+2)) = 2(a+2)·gcd(a, 3). Both are at least 2a, against windows of
length a+1 and a+3. The log checks this at 7 named odd a. It also holds with
P = 30 (Low 1). So no bound on the raw short-route moduli holds over the
two-gap cone, as the note says. The far-wall route lights the wide end, because
D grows quadratically while the far-wall threshold is linear in a.

## 5. Relation to d188

The d188 lemma needs the phase implication only along λ → ∞ at each positive
rational point. So a subsequence of dilations is enough, as the note says. A
uniform radius ρ gives K with k ≤ 22, matching d188 Low 5. "At least one
normal per seed" matches d188's best-possible conclusion. The note labels the
menu statement "would suffice" and states the residue caveat. That's correct.

**Does it address the d188 open case?** Partly. d188 asked for one of two
inputs: a fixed-period transfer at occupied crossings, or a lemma that accepts
gate congruences with modulus bounded on E × F.

- The note gives bounded moduli only along affine rays, not on E × F.
- It replaces FPT on its own slice with something stronger: every placement
  outside an explicit box is lit, uniformly in c.
- d188's smallest test had two mouths, so that the cap budget wouldn't apply.
  Two mouths in [0,R] are now covered.
- d188's test also asked for each factor to be a line in **two** gaps per
  axis. The note varies one gap per axis (a and D), so that test stays open.

So the note settles the geometric side of one occupied crossing with one gap
per axis. It doesn't supply FPT, so H(C) isn't bounded.

## 6. Mandatory corrections

### High

None.

### Medium

1. **First open case is incomplete.** Add two cases to the "First open case"
   paragraph. First, the source depth d can grow; every constant is polynomial
   in d, so d is a real hypothesis. Second, d188's smallest test, with two
   gaps per axis at one occupied crossing, isn't covered, since the note varies
   one gap per axis. The growing upper run is a correct open case. It
   shouldn't be presented as the only one.

### Low

1. **Definition of P.** The note defines P from "all horizontal unit-height
   runs in the fixed upper chamber". The st279 example uses P = 6, but that
   rule gives lcm(6, 6, 10) = 30 there. The proof uses only the runs that the
   upper path visits. Either define P that way or use P = 30 in the example.
   With P = 30 the conclusions still hold. The moduli stay at least 2a, and
   the D = 3a floor modulus is 6·gcd(a,5) ≤ 30.
2. **The bounded-modulus paragraph isn't needed for lighting.** On any ray
   with p, q > 0, D is linear in a, so (1) already fails for large a. Say that
   the paragraph's value is exact gcd stabilization for a phase-window
   argument, not eventual lighting.
3. **Far-wall factor.** The box uses Dδ > 4h. The proof allows
   (2D−c−e′)δ > 4h, which is about twice as strong; d186 used it at st279.
   This is optional.
4. **Implicit hypotheses.** State R ≤ D, so that the mouths lie in the roof,
   and h, D integral. Also state that only positive-sheet routes are used.
   The box is a necessary condition for darkness, not a census.
5. **Advances line.** Add "for these mark placements, one gap per axis", so
   that later citations don't read it as covering d188's two-gap factors.

## 7. Scope

The result holds for this setup:

- a solid-sided lower rectangle [0,D] × [0,h];
- every roof opening inside a fixed span [0,R] from the near side;
- a fixed lattice end chamber above the roof, with a fixed lattice target;
- a source at fixed depth d, with any abscissa 0 < c < D.

For one upper first-hit interval J, the note proves an explicit finite box for
dark (a, D). No chart-wide K(C), G(C) or H(C) follows, and the note says so.
The finite-flat application still depends on d132 and d134.

## 8. What it advances

**L1 (area bound), occupied-crossing row.** The note extends d186's effective
residual from one mouth and one upper run to several mouths in a bounded span
and any fixed upper chamber. It closes both items of d186's "first open
structural case" when the extra opening lies in [0,R]. It doesn't give a
chart-wide bound, and no ledger word changes status. The advance is a
hypothesis removal inside one geometry class. I see no basis to move the
W ≤ 20 estimate.

## 9. First open case

The first open case is an occupied crossing whose upper approach also crosses
a growing run, so that P, B and η depend on the ray. This is the note's case.
Two cases have equal standing:

- a growing source depth d;
- d188's codimension-2 product with two gaps per axis at one occupied
  crossing.

A roof opening outside [0,R] is also open. LLLRLLLRLR (W = 10) remains open as
an all-length statement.
