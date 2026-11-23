# Review: ferrers-terminal-strip.md (snapshot 2026-11-22 0813)

**Verdict: sound with gaps.** The construction and both tests are correct as stated. Condition (1) and its transpose are empty on every lattice room, so only the denominator test reaches the target class. It covers a thin but infinite lattice region. Checks: `checks.py`, `checks.log` (37 PASS, 0 FAIL, under 1 CPU-second).

## 1. The lattice issue

- In a lattice room, d/(2u), e/(2v), and h/W are positive rationals. The Q-span of one nonzero rational is Q, so h/W is in the span and (1) fails. The same holds for any room whose lengths are commensurable. Confirmed on all 6 named rooms.
- The transpose has w'=h, u'=e+h, v'=d+e+h, W'=c+d+e+h, d'=v−u, e'=u−w, h'=w. These are rationals too, so the transposed condition fails the same way.
- (1) has no content for the target class. Its region is the non-commensurable real rooms.
- **Denominator test, exact lattice region.** Let P0 = lcm(den d/(2u), den e/(2v)). This is the best choice, because every valid P is a multiple of P0. Let Q = floor(W/w). The room is covered iff W/gcd(W, P0·h) > Q². The transposed test applies by symmetry; the note doesn't state it.
- **Necessary condition:** Q² < W. So w=1 never passes, and W ≤ w²+w−1. For w=2 only W=5 passes. For w=3 only W ∈ {6,7,8,10,11} passes.
- **Covered (explicit):**
  - Family F: widths (2,3,4,5), any c,d,e ≥ 1, and 5∤h. P0 divides 24, so den(P0h/5)=5 > 4.
  - Widths (3,u,v,7) with 7∤h.
  - Named: R1 = (2,3,4,5; heights 1,1,1,1), R2 = (2,3,4,5; 2,6,8,2), R3 = (3,4,5,7; 1,2,1,3), and R4 = (3,5,6,8; 1,2,4,1). Heights are listed top to bottom. R3 is also covered transposed.
- **Not covered:**
  - The ledger realization N1 = (1,2,3,4; 1,1,1,1) fails in both orientations.
  - The d17 chain N2 = (3,4,9,12; 3,4,2,3) fails in both orientations.
  - (2,3,4,5; 1,1,1,5) and every room with w=1.

## 2. Reduction via d15

The `cert_r3.json` entry for `#.../##../###./####` (mask 4991) has exactly one uncovered pair, (1,7)–(7,1). That pair is the open top cell against the open bottom-right cell [v,W]×[0,h]. So the reduction is exactly right. The note handles 0<z<W, which is a harmless superset. The source of the reduction is d15 **Theorem 3 (partial, r=3)**, not Theorem S. Theorem S covers only r ≤ 2, and this word has r=3.

## 3. Proof

- **Strip:** |L(t)| ≤ w − (t/D)(w−|Z|) is correct. Every joint opening is at least w. The left wall is straight, so folding at 0 is smooth. Corners at x=w,u,v at the joints are avoided because |L|<w.
- **Slope M:** Exact multiples make the middle bands invisible. The terminal condition Z+MB ≡ ±z (mod 2W) is correct.
- **Floor:** The switch shift is ΔX(h−b)/D. Since (h−b)/D < 1/2 and 0<|ΔX| ≤ 2w, the shift is nonzero and below w ≤ W. At most one X gives a floor corner, and Z+MB doesn't depend on X. This step is correct.
- **Q² bound:** Spacing 2W/q < 2w iff q > W/w. The two rotations sum to Ph/W, and lcm(q1,q2) ≤ Q². This step is correct and gives only a sufficient condition, as the note says.
- **Kronecker step:** The basis rescaling and continuous Kronecker theorem are applied correctly. At least one of b/(2W) and (2h−b)/(2W) leaves the span. The limit and correction argument holds because the margin aw/D stays fixed. This step is sound, but only for non-commensurable rooms.

## 4. Exact tests

- **Covered rooms:** The note's construction uses the smallest |k| and is replayed with the d167 tracer.
  - R1: 10 of 10 pairs hit T exactly.
  - R2: 16 of 16 pairs.
  - R3: 26 of 26 pairs.
  - R4: 14 of 14 pairs.
  - The pairs are half-lattice pairs plus 8 random rational pairs per room. Both routes occur, with at most 52 reflections.
- **Note control:** (163,−9) in N2 reaches (10,1) with 31 vertical reflections, as claimed.
- **Uncovered rooms:**
  - N2: all 8 named pairs are lit by the note's construction itself, because resonance blocks only special targets.
  - N1: 3 of 4 pairs are lit by the construction. (8/13,44/13)–(23/6,1/3) has both rotations integral, so the construction fails. Direction (−11,−2) lights that pair, with 8 reflections and an independent retrace.

## Gaps

1. **High (scope).** The title and headline condition (1) are empty on the lattice target class, and so is its transpose. Only the denominator test applies, and it needs Q² < W. That excludes w=1 and the ledger's own realization. The note should say this up front.
2. **Medium.** The reduction rests on d15 Theorem 3, the r=3 certificate table. The d15 review scoped that table out ("r = 3 and r = 4 are out of scope"), so it is unreviewed for this word. It isn't Theorem S.
3. **Medium.** The note doesn't state the transposed denominator test, or that P0 (the minimal P) is optimal. The covered region should be written as W/gcd(W,P0h) > floor(W/w)², or the same for the transpose.
4. **Low.** The "sharper test" should say it is sufficient only. b ranges over (0,h), not over all residues, so the exact failure set is smaller.

## 5. Ledger effect

LLLLLRLRLR can become **PARTIAL for lattice rooms** if this note and the d15 r=3 staircase entry are accepted. The region is integer w<u<v<W and c,d,e,h ≥ 1 with W/gcd(W, P0·h) > floor(W/w)², or the transposed inequality. Family F is an explicit infinite part of it. Nothing becomes COVERED. Today the word stays OPEN in the word-specific split.
