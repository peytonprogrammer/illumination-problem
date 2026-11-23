# Review of thin-gap-periods (snapshot 2026-11-21-2100)

**Verdict: sound with gaps.** The corner-intercept theorem, the one-reflection witness, and the periodic-compression lemma all hold as stated. No counterexample was found. The gaps are about wording, scope, and dependence on cited results. None of them breaks a proof.

Files: `checks.py` (exact `Fraction` arithmetic, named rooms only) and `checks.log` (`python3 -B checks.py`, 13.8 s, overall PASS).

## What the checks confirmed

1. **Dumbbell geometry, B = 1..6.** The room has 12 walls and area 10U+7, for example 207 at U=20 and 2407 at U=240. Its four reflexes are (U,2), (U,3), (U+2,2), and (U+2,3). The horizontal and vertical wall-length gcds are both 1. τ = 5: a 5×5 square fits and the total height is 5, using the closed-room axis-square convention in `local-thickness.md`. S=(a,2) and T=(3a+2,2) are strictly interior and have the same parity.
2. **Corner intercept, symbolic, B ≤ 12, |b| ≤ 50.** For every 1 ≤ p ≤ B, the displacements a·b/p (right launch) and 3a·b/p (left launch through x=0) are multiples of 10. 10·lcm(1..B) equals lcm(10, 20, …, 10B), so it is the least a with 10p | a for all p ≤ B.
3. **Exact tracer, B = 2, 3, 4.** The tracer covers all primitive (p,b) with 1 ≤ |p| ≤ B and |b| ≤ 30, both horizontal signs, plus (±1,0). That is 186, 266, and 326 directions, with 141,042 smooth reflections at B=4. Every ray stops at (U,2) on its first contact with x=U, no ray reaches T, and no ray hits a convex corner. Vertical launches stay on x=a. A ray can leave the left chamber only by crossing x=U. Its first contact with x=U is the lip, so the open doorway is never reached.
4. **Control.** With a = 10·lcm + 1, 48 directions (B=2) and 63 directions (B=3) get past x=U. The tracer does not absorb rays trivially.
5. **Witness (a+1,1), B = 1..6.** Both mouth crossings have height 3 − 1/(a+1), for example 32/11 at B=1. The only reflection is a smooth hit on the corridor ceiling at (U+1,3). The tracer then reaches T exactly.
6. **Compression.**
   - In the B=1 dumbbell, lengthening the S-to-U gap by 1320 = 2·11·lcm(1..5) keeps the direction (11,1) lighting T, as does 660. Lengthening by 11 or by 1 sends the ray to a reflex.
   - In a named τ=3 L room, the lighting directions (−1,±1) and (−1,3) survive these period multiples. Each multiple changes one long x gap and one long y gap together. A +1 change kills each direction.
   - Both long x gaps of the L room are single full-width strips of height 3.

## Answers to the referee questions

- **Q1.** The intercept argument is complete. Every exit from the left chamber crosses x=U, and the horizontal velocity sign is constant until the first contact with x=0 or x=U. Reflections preserve |p| and |b|, and reversing a path makes S the start without loss of generality. The BBBB label does not affect the obstruction. It only places the room in the family that the theorem names (see gap 2).
- **Q4.** The lemma is correct.
  - Wall endpoints lie on grid lines, so a long open x slab has no wall endpoint inside. Each component is therefore a full-width rectangle with integral height h. If h > τ₀ and the width exceeds τ₀, the room contains a square of side greater than τ₀ ≥ τ, which is a contradiction. So h ≤ floor(τ₀) divides lcm(1..floor τ₀), and Δb/p = 2b·lcm lies in 2hℤ.
  - A strip's y-range is bounded by wall lines, so it is a union of short y gaps. The cells where a long x gap meets a long y gap are therefore empty, and the two compressions commute.
  - Non-strip components and strip heights that don't divide the period can't occur.
  - The bound "11 × max retained gap" holds because there are at most 10 + 2 grid lines per axis.
- **Q5.** The theorem excludes every finite menu of fixed absolute directions. To see this, take B ≥ every component of every menu element, which also covers rotated or transposed application. It doesn't exclude menus that depend on the room's lengths, and the note says so.

## Gaps

1. **Medium: the claim's range of τ is wider than what the note proves.** "Excludes a universal finite menu … for the thin regime" is proved only when the thin cutoff satisfies τ₀ ≥ 5. For τ₀ ≤ 4, the note gives no example. A height-3 chamber with a unit door would probably work in the same way, but the note doesn't state it and the checks don't test it. Either state "τ₀ ≥ 5" or add the smaller-τ variant.
2. **Low: membership in normalized BBBB rests on a cited classification.** "Normalized" and "BBBB" come from the reviewed large-area classification at r=4 and the note `length-periodicity.md`. The checks confirm the gcds, area, and reflex count, but not the classification. The obstruction holds in this room whatever its class.
3. **Low: the theorem's first paragraph has an unclear quantifier.** "This holds for distinct same-parity interior lattice marks" reads like "for all such pairs." The proof gives one pair per B. Write "for some pair of …".
4. **Low: the stated a is sufficient but not minimal.** a = 5·lcm(1..B) also intercepts every |p| ≤ B direction, at (U,2) for even displacement/5 and at (U,3) otherwise. The witness still lights T (checked for B = 2, 3, 4). The note's "the physical height is exactly two" is specific to a = 10·lcm. This doesn't affect correctness.
5. **Low: the reason for the factor two is misstated.** The 2 in 2|p|·lcm is needed for the signed state, because the circle length is 2h. Parity of the endpoints isn't the reason. Without the 2, Δb/p = b·lcm isn't always in 2hℤ. The sentence "Include a factor two … to preserve endpoint parity" understates this.
6. **Low: some conditions of the compression lemma are implicit.**
   - The bound of 11 assumes W ≤ 20, that is, at most 10 vertical supporting lines.
   - Finiteness of the representatives needs lattice marks.
   - The representative's τ, normalization, and class aren't controlled, as the note concedes.
   - Reflection counts inside strips change under compression (seen in the L-room checks). Only the signed strip exits are preserved, which the note's wording does say.
7. **Low: the scaling paragraph needs one more sentence.** "The same fixed-direction obstruction applies" under integral similarity should say what it means. Scaling the dumbbell by k gives an unnormalized room with τ = 5k and the same failed menu.

## Budget note

The first run took about 9 CPU-minutes, which is close to the 10-minute budget. The cause was the 10⁶-step cap on L-room directions that never reach a corner. With the cap lowered, the final run takes 13.8 s. One assertion in the first run also wrongly required equal reflection counts. That check now requires only that the ray reaches T.
