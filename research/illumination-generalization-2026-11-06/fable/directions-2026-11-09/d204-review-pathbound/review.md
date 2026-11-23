# Review of d204 snapshot: path bounds and per-pattern decidability

## Verdict

The snapshot is correct with gaps: all four mathematical claims hold, and Part 1 breaks the program's step "linear bound implies a Presburger sentence".

Files: `checks.py` (standard library, exact `Fraction` arithmetic) and `checks.log`. CPU time is 2.8 s. The script traces only the two prescribed rays in the named family, for m = 2..30 and u = 1..1000. It runs no other search.

## Per-part verdicts

| Part | Claim | Verdict |
|---|---|---|
| 1 | Zero-reflection obstruction, u > m(m+1) | Correct. The scope statement understates the result; see E1. |
| 2 | Finite witness bound 2N·2^F + 2 | Correct with gaps (attribution, exposition). |
| 3 | Linear witness with at most 2m+4 reflections | Correct. Verified exactly on 31,276 rays. |
| 4 | Phase order at a unit neck | Correct. A definition is missing. |

## 1. The obstruction

**Geometry.** The polygon's cyclic turn word is LLRRLLLLRRLL, a rotation of LLLLRRLLLLRR, so it has 12 walls. All four shoulders are strictly inset: the aperture is [0,2], the left chamber spans [−m−1,3] and the right chamber spans [−1,3]. S = (−u,−m) and T = (m+1,1) are interior. The line ST has ordinate (u − m(m+1))/(u+m+1) at x = 0 and u/(u+m+1) ∈ (0,1) at x = m. Both chambers are convex, so legality depends only on the first mouth.

- Check A, from `checks.log`: in 29,000 (m,u) pairs, an exact trace of S→T agrees with [u > m(m+1)] every time.
- At u = m(m+1), the segment stops at the reflex corner (0,0) in all 29 cases.

**Logic.** The argument is correct. Suppose a Presburger formula P(ℓ, S, T, k) defines "a legal path with at most k reflections exists". Substitute the affine terms in (m,u), set k = 0, and add m ≥ 2, u ≥ 1. The result defines {(m,u) : u > m² + m}. The least-u function m ↦ m² + m + 1 is then Presburger-definable. Two standard facts each exclude it:

- Every unary Presburger function is eventually affine on each residue class of some fixed modulus.
- Every unary Presburger set is ultimately periodic, so an infinite one has bounded gaps. The gaps here are 2m + 2.

**Scope.**

- **What it kills.** The obstruction holds with k fixed at 0. Free k plays no role. So the result is stronger than the snapshot states: legality of even one fixed itinerary isn't Presburger in the lengths and marks. Gate tests compare (affine)·(affine) with (affine)·(affine), which is the variable-times-variable problem d159 already noted. So every encoding of the form "∃ a path of bounded length with these legality constraints" fails. That holds whether the bound is constant, linear, or anything else, and whether or not the linear bound is true. The PROGRAM.md implication "linear bound ⇒ each word's statement is a Presburger sentence" is therefore unsupported.
- **What it doesn't kill.**
  - **Unrestricted predicate.** It says nothing about Lit(ℓ, S, T) or AllLit(ℓ) = ∀S,T Lit. By Part 3, Lit is identically true on this family, so the family gives no evidence either way.
  - **Universal sentence over lengths.** As a closed sentence, "∀ℓ AllLit(ℓ)" is trivially equivalent to ⊤ or ⊥, so "is a Presburger sentence" is vacuous here. The real question is whether some procedure decides it. Written directly, it's a ∀∃ sentence of integer arithmetic with multiplication. No general decision procedure exists for that class, by MRDP. Individual instances can still be provable.
  - **One-parameter rays.** Suppose every length and both marks are affine in one parameter n. Then each fixed-itinerary legality condition is a Boolean combination of polynomial inequalities in n, so it's eventually constant and Presburger-definable. But "all pairs" makes the marks range over a box that grows with n, which brings back products n·x. The witness itinerary also changes with n (Part 3's k and parity choice). So rays don't restore decidability for "all pairs".
  - **Other theories.** Real closed fields (Tarski) are decidable but lose integrality. Part 3 needs integrality, because the target phase −m + rD must be odd. The existential theory of Presburger arithmetic with divisibility (Lipshitz) is decidable, but this sentence is ∀∃.
- **What could still work.** You'd need a structural theorem: AllLit(ℓ), as a set of length vectors, is ultimately periodic in each length. That would make AllLit Presburger-definable and reduce each word to finitely many rooms. Unlike a path bound, this is a statement about the set of lit rooms, not about paths. d152 refutes a uniform tail across words, but a per-word, eventually periodic statement remains open. It's a theorem to prove, not a logical reduction.

## 2. The finite witness bound

**Correct with gaps.** I checked each step:

- **Unfolding.** The four reflected copies form a translation surface tiled by N = 4A unit squares, which covers ℝ²/ℤ² branched over 0. Reflections across integer lines preserve ℤ², so walls, corners, S and T all lift to vertices over 0. Convex corners become regular points, but they're still forbidden. Reflex corners become cone points of angle 6π. So every singular vertex is forbidden.
- **Orbit finiteness.** γ ∈ SL(2,ℤ) preserves ℤ² and fixes 0, so γ·X is again an N-square origami. The marks are carried along. Labelled data number at most (N!)² for the right and top permutations, times 8^(4N) for three flags on 4N corner slots. This overcounts, which is harmless, so the orbit has at most F classes.
- **Shortest walk.** The two unit shears and their inverses generate SL(2,ℤ), so the Schreier graph on the orbit is connected. A shortest walk from [X] to [A·X] has length at most F − 1. An isomorphism over the torus is a translation equivalence, so it preserves horizontal connections between flagged sets.
- **Horizontal bound N.** The eastward flow along bottom edges is injective. A repeated edge forces the trajectory back through the starting S-lift, and the suffix after that return is a shorter connection. So a shortest connection uses at most N edges. The snapshot's "delete the loop" phrasing says the same thing in less detail.
- **Pullback.** For a shear, |x ± y| + |y| ≤ 2(|x| + |y|), so ‖G⁻¹(j,0)‖₁ ≤ N·2^(F−1). Walls lie on integer lines in the developed plane, so the reflection count is at most the total variation plus 2. The stated bound 2N·2^F + 2 holds with slack.

**Literature.**

- Hubert, Schmoll and Troubetzkoy, *Modular fibers and illumination problems*, arXiv:math/0602394. They treat Veech surfaces, including square-tiled ones, through the affine-group orbit of marked periodic points. They show that a point fails to illuminate only finitely many points.
- Lelièvre, Monteil and Weiss, *Everything is illuminated*, arXiv:1407.2975. They extend those results beyond lattice surfaces.
- Wolecki, *Illumination in rational billiards*, arXiv:1905.09358. He shows that non-illuminating pairs form a finite set.

The finite SL(2,ℤ) orbit of a marked origami and the reduction to a horizontal connection are standard; HST is the right citation. I read only the abstracts. None of them states an explicit reflection-count bound, so treat the displayed number as a routine corollary, not a new theorem.

**Value to the program.** The bound depends on the area, not on the word. It gives per-room decidability, which the d8 decider already provides. It gives no information uniform in the lengths.

## 3. The linear witness

**Correct.** Check B traced the slope-r ray from S for every admissible odd target phase in the prescribed interval, with an exact reflecting tracer. That's 31,276 rays in total.

- Every ray reaches T legally, with no corner hits and at most 2m+4 reflections.
- The side conditions 2k ≤ m+3 and, for k > 0, d ≤ w(m+2) hold in every case.
- The observed maximum is 31 reflections, at m = 30, u = 1, r = 61/64. Every ray satisfies refl/(2m+4) ≤ 1/2, so the stated bound has a factor-2 slack.

I checked the hand proof:

- **Existence of r.** rD ranges over an open interval of length 2D/d > 2, so it contains integers of both parities.
- **r < 1.** This follows from r < (m+2)/d and d ≥ m+2.
- **Chamber leg.** Earlier right-wall hits stay below 0 because (m+2)(d−2w) ≤ md ⟺ d ≤ w(m+2). That in turn follows from d < m+2+2w and m(w−1) ≥ 2.
- **Final leg.** The unfolded height at D is an odd integer n. Over the last unit it lies in (n−1, n), so the ray crosses no even line and meets no corner at x = m.

## 4. The phase-order remark

**Correct.** A translation by Lp/q on ℝ/2ℤ has order 2q/gcd(Lp, 2q). For coprime p and q, gcd(Lp, 2q) ≤ 2L, so the order is at least q/L, which is unbounded in q. The snapshot correctly marks this as a group order, not a visit count. Its point about cycle deletion is also correct: only an exact directed state permits deletion, not a wall label or a coarse phase class.

## Errors and fixes

- **E1 (medium, scope).** "Even the uniform predicate 'at most k reflections suffice' … with free … k" understates the result. The failure already occurs at k = 0 for one fixed itinerary. Fix: "Legality of a fixed itinerary is not Presburger in the lengths and marks. So no encoding by bounded paths gives a Presburger sentence, whatever the bound."
- **E2 (medium, program text).** PROGRAM.md's target theorem says "Then each word's … is a Presburger sentence". That inference is invalid. Fix: replace it with the open structural statement in the last bullet of Part 1's scope list, or with the certificate form in the recommendation.
- **E3 (low).** "A different encoding … that eliminates the zero-reflection distinction" is vague. Fix: state that Lit is constant (true) on this family, so the family is silent on Lit and AllLit.
- **E4 (low).** Part 2 has no attribution. Fix: cite HST, arXiv:math/0602394, for the finite modular fiber and horizontal-connection reduction, and present the bound as a corollary.
- **E5 (low).** In Part 4, "unit neck" is undefined. The named family has neck height 2, which gives period 4. Fix: say "neck height 1 (unfolded period 2)", or write modulo 2h for a neck of height h.
- **Not checked.** The D203 claims about moduli 2BⱼD are out of scope.

## Recommendation

Per-pattern decidability through Presburger arithmetic isn't viable as stated. Retire "linear bound ⇒ Presburger sentence" now, without waiting for the 2026-11-26 stopping rule. The failure is logical and independent of any path bound.

Two forms remain logically sound:

1. **Per-word parametric certificates. This is the recommended form; it gives proofs, not a decision procedure.**
   - For each word, split length space into finitely many Presburger-definable regions, using linear inequalities and congruences.
   - Attach to each region an itinerary template like Part 3, with path length linear in ℓ.
   - Prove each template's polynomial legality inequalities by hand or by symbolic algebra.
   - Close the small cases with the existing per-room decider.

   The linear-bound lemma stays useful as a guide for designing templates.
2. **Decidability through a structural theorem.** Prove that AllLit is ultimately periodic in each length for each word with W ≤ 20. Then each word reduces to finitely many rooms. This is a new open theorem, and d152's W = 22 tail failure shows it can't be uniform across words.

Neither form follows from any reflection bound. No estimate change is proposed from this review.
