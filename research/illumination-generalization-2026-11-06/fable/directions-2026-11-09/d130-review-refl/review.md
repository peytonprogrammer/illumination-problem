# D130: review of the reflection-complexity note

Date: 2026-11-21. Reviewer: independent referee.

Reviewed file: `../d95-review-queue/snapshots/reflection-complexity.2026-11-21-2110.md`. It's identical to `qclass-closure/bbbb/reflection-complexity.md`.

Context read: `component-ends.md` (cov279 control and its lower bound), `thin-room.md`, `local-thickness.md` (definition of τ), `stabilizer-orbits.md` (st279 rows), the d117 review, and the coordinator-log entry that defines the target R(τ₀, r). No network access was used.

Own code: [checks.py](checks.py), log [checks.log](checks.log), 72 CPU-seconds. It's an exact `Fraction` slab tracer that imports nothing from the author. It builds only the two named band rooms. Witnesses come from the note's formulas (thin: the two-band CRT; fat: the note's rounding rule). The only search is check C: it enumerates every developed image of T under at most L wall reflections in the named room. That enumeration is complete for paths with at most L reflections.

## Verdict

**Sound with gaps.** Both lower bounds are correct, and both witness families are lit. The gaps are about definitions, explicit constants and the framing of the next move. None of them affects the two theorems.

## 1. Thin claim (cov279)

**Lighting.** The scaled marks are (q/2, 1) and (3q, 3), both even-odd. Check B builds the two-band CRT shots for q = 16, 28, 40, 580 and 3604. Every shot replays legally from S to T. Each crosses the door at x = 2q−2 or 2q−1 and uses exactly two band passages.

**Lower bound.** I rederived the d117 inequality 1 ≤ 6(R+1)(8R+2)t ≤ 48(R+1)²t.

- Every S-to-T path must cross y = 2 through the door (2q−3, 2q), because the bottom band has no other exit.
- At t = 0 every wall lies on X = 2x/q ∈ {0, 4, 8, 10, 12} or y ∈ {0, 2, 3, 4, 6}. Reflections preserve both parities. The parity classes of S, p and T are (1,1), (0,0) and (0,1), so the determinant is odd for every word.
- Only the wall x = 2q−3 moves. Ordinates are exact, so the determinant error is bilinear in the abscissa errors and the developed ordinates.

With t = 3/q this gives R+1 ≥ √q/12. The argument uses only the formal word, so it covers every slope, every route and repeated door visits. Check B confirms det = 0 at the actual t and an odd formal determinant (1, 5, 13, 17, −87, …) on all 62 replayed shots.

**Dependence on d117.** D117 rated the cov279 control "Sound" after a line-by-line check of this bound. Its tracer checked only j = 1..5, but the argument holds for any t > 0 and any legal shot. So the note's use for all q = 12j+4 is within the reviewed argument. D117 also observed that the bound is vacuous at the parameters it replayed. The note's quantifier ("choose q > 144(R+1)²") handles this correctly.

**Completeness check.** Check C finds no path with at most 8 reflections at q = 580, where the bound requires R ≥ 2. It finds none with at most 10 reflections at q = 3604, where the bound requires R ≥ 5. At q = 16 and 28 the minimum is 4 reflections, which is consistent because the bound is vacuous there.

## 2. Fat claim (st279)

**Room.** For k = 1, 2, 4, 16, 128 and 320 (m = 144k²), the builder confirms r = 6 and gcd 1 for both wall-length lists. The largest inscribed square has side τ = m.

**Lighting.** The arithmetic is correct. m/2 and m/4 are multiples of 4, so a ≡ b ≡ 1 (mod 4). Also 2s = 12k+3 ≡ 3 (mod 4). Both unfolded abscissas are even integers and both ordinates are odd. Check D replays the shot for every k listed above:

- The seam crossings are exactly m−½, m+1 and m+5/2.
- The marks are (even, odd).
- The shot uses four band passages.
- The depth is at least 0.25m for both marks.
- The extra travels a − m/2 and b − m/4 stay below 2m/s + 5.

The witness uses R ≈ 0.71√m reflections, so Ω(√m) is sharp up to the constant.

**Determinant.** In coordinates 4/m every limiting mirror lies on 0, 4 or 8. A reflection acts as X ↦ −X (mod 8), so it preserves "0 mod 4" and parity. Then A₀ ≡ (2,2) (mod 4) and B₀ ≡ (even, odd), so det ≡ 2 (mod 4). That gives |det| ≥ 1/8 in scaled units. Check D evaluates this determinant on each witness word and gets −2 or 6. The mirror shift (≤ 3/m), the per-reflection error (≤ 6/m), the box bound (≤ 3 per segment) and the inequality 1/8 ≤ 12(R+1)δ + 2δ² are all correct.

**Access claim.** The claim is correct. The proof uses only the limit T₀ and the first crossing of the lower mouth. Any landing point within K/m of T has the same limit.

## 3. Scope

- The negation of R(τ₀, r) holds in the natural reading: for each lit pair, some witness has at most R reflections. Cov279 has τ = 3, so the note actually refutes R(3, 6), which is stronger than R(6, 6).
- The fat claim correctly rules out a bound that depends only on r for rooms with τ ≥ τ₀. The note correctly leaves open a bound that grows with m.
- "No union of words of bounded length covers this family" follows directly. The paragraph about semialgebraic tests is heuristic (gap 5).
- Band passages: both witnesses use bounded passage counts (2 and 4, confirmed). The note claims no more than that.

## Gaps

1. **Medium. R(τ₀, r) is never defined in the note.** The headline "R(6,6) does not exist" depends on quantifiers that appear only in the coordinator brief: which rooms, which pairs, and whether R bounds some witness or every witness. Fix: state the definition. Also note that τ = 3 for cov279, so the result refutes R(τ₀, 6) for every τ₀ ≥ 3.
2. **Medium (next move). Bounded band passages don't give Presburger statements.** In the proposed K(r) reduction, each band transit still imposes a congruence modulo a parameter-dependent width, such as gcd(dP, 2u) in thin-room.md. Divisibility between two variables isn't Presburger-definable. Also, bounded passages are known only for the named st279 pairs. For cov279, thin-room.md bounds them for all pairs with 3 ∤ q. Fix: state that K(r) finiteness alone doesn't make the arithmetic linear, and that st279 passage counts for general pairs are open.
3. **Low. The fat constant is not explicit, and "k ≥ 16" has no visible role.** With the actual endpoint errors (eS·√m ≈ 3.5, eT·√m ≈ 0.9), the note's inequality forces nothing until k ≈ 128. There it forces R ≥ 3, and at k = 320 it forces R ≥ 9, which is roughly R+1 ≥ √m/384. The construction also works at k = 1. Fix: say that the bound is asymptotic, or give the explicit constant. Drop k ≥ 16 or explain it.
4. **Low. The thin bound is far from the observed counts.** The shortest CRT witness uses about q/3 reflections (192 at q = 580, 1,200 at q = 3604) against √q/12 (about 2 and 5). This doesn't affect correctness. D117's suggested sharpening, which counts only moving-wall bounces, may improve the exponent.
5. **Low. The semialgebraic remark is inaccurate for this pencil.** In cov279 only abscissas scale and ordinates are fixed. For a fixed word, the collinearity and crossing conditions are therefore linear in q. The nonlinearity comes from unbounded winding counts multiplying widths, not from the determinants. Fix: reword the remark or delete it. The lower bound alone carries the conclusion.
6. **Low. The thin target lies on the artificial cut y = 3.** It's interior, and d117 noted this. Say so in the note, because the band-passage count depends on the cut convention.

## What the checks confirmed

- Every named witness is legal and reaches its target. That's 62 thin shots across 5 values of q, and 6 fat shots with k up to 320.
- The determinant identities hold on every witness: det = 0 at the actual parameter, odd at t = 0 for cov279, and ≡ 2 (mod 4) at the limit for st279.
- No path with at most 8 or 10 reflections exists at q = 580 and q = 3604, or at k = 1, 128 and 320. The k = 1 witness uses 10 reflections, so 10 is the true minimum there.
- The witnesses use 2 band passages (thin) and 4 (fat).
