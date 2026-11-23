# d167 review: overhang-escape and nonspanning-entry

Snapshots reviewed: `d95-review-queue/snapshots/overhang-escape.2026-11-22-0758.md` and `nonspanning-entry.2026-11-22-0758.md`.
Script: [checks.py](checks.py). Output: [checks.log](checks.log). The run takes 32 CPU seconds, uses exact Fraction arithmetic, and reports 0 failures.
The d164 Fraction tracer is copied verbatim. All rooms are named: B from d164, R2, R3, and the ledger realization of LLLRLLLRLLRR.

## Verdicts

- **overhang-escape.md: sound with gaps.** All gaps are low.
- **nonspanning-entry.md: sound with gaps.** One gap is medium; the rest are low.
- **Ledger:** neither note moves any word to COVERED or PARTIAL.

## Note 1: overhang-escape

### Necessity in B (item 1)

- The line from (4,67/2) through (e,33) meets y=32 at 3e−8 exactly. For e in (2,3) this lies strictly below 1, the left end of the parent base.
- (2,33) and (3,33) are polygon vertices, so a ray through either lip stops there.
- I traced the first event of every primitive direction with |p|,|q| ≤ 100 (24,352 directions). No ray reaches y<32 before its first contact. First events: 19,023 child-horizontal, 4,564 child-side, 760 parent-side, and 5 corners. Together with the affine argument, this confirms that no straight escape exists in any direction.
- For 3+2δ < x < 5 the supremum of the lower crossing is 3+(3−x)/δ < 1, which is a strict failure. At x = 3+2δ−1/100 a straight escape exists, so the bound is sharp.

### Sufficient condition (item 2)

The proof is correct. The X-range length (δ+h)w/δ, the piece bound min(v,b/2), and the slope (δ+h+B)/δ combine to give exactly L(B). Legality holds as stated: parent contacts lie strictly below the mouth, the exit is strictly inside one sheet, and hall contacts lie on the intact sides.

I implemented the proof's construction, using only the largest single piece, and traced every shot exactly. The test covers every half-lattice child mark, every half-lattice row, and every half-lattice target.

| Room | Claimed rows (mark × row) | Pairs | Lit | Nearest-to-equality row |
|---|---|---|---|---|
| B: hall [0,6]×[0,32], parent [1,3]×[32,33], child [2,5]×[33,34] | 210 | 2,310 | 2,310 | L/2A = 25/24 at depth 11 |
| R2: hall [0,5]×[0,30], parent [2,3]×[30,32], child [1,4]×[32,33] (v-term binds) | 70 | 630 | 630 | 51/50 at depth 23 |
| R3: hall [0,7]×[0,42], parent [1,4]×[42,43], child [3,6]×[43,45] (δ = 1/2, 1, 3/2) | 465 | 6,045 | 6,045 | 85/84 at depth 40 |

- **Below the bound.** On rows within 2 below the threshold, R2 loses 2 of 450 pairs with the largest piece alone, and all 450 are lit with all pieces. The bound isn't tight, and the note doesn't claim equality.
- **Floor extension (bonus).** In B at δ=1/2, all 105 rows with L(B) ≤ 2A are lit, 1,155 of 1,155 pairs, each with exactly one floor bounce.
- **Witness.** The direction (−149,−66) reaches (1/2,1/2) exactly. The arithmetic checks: 3e−8 = 27/44, the fold gives 61/44, and 145/2 mod 12 = 1/2.
- **Application numbers.** These check: L(t) > (2+t)/2, direct descent for B ≥ 22, and the floor step for B ≤ 18.

### Gaps

1. **Low.** The displayed mark (4,67/2) has x = 3+2δ exactly, so it is on the boundary of the open set, not inside it. Its failure depends on the lip stopping rule. "The strict failure … persists" reads as if the mark were interior.
2. **Low.** The note describes the witness as "one parent-side bounce and no horizontal-wall bounces." It also makes 12 hall-side bounces, which makes "simpler witness" a matter of judgment.
3. **Low.** The DB55 and two-bank sentences have no proof or check. DB55 has no parent–child overhang, so "wherever the stated geometry holds" has no stated instance.

## Note 2: nonspanning-entry

### Realization and crossings (item 3)

- The ledger vertices equal the boundary of runs (0,1), (0,5), (3,5), (2,5), (4,5). The turn word is LLLRLLLRLLRR.
- At e=1/2, s=16/5 the crossings are 37/10 (+), 31/10 (−), 41/10 (+). These match the closed forms e+s, 10−e−2s, e+3s−6.
- The mouth margins are 7/10, 1/10, 1/10. The developed-sheet margins are 13/10, 1/10, 9/10. The maximum change over the rectangle is 4/100. All four corners of the closed rectangle keep the same sheets and signs, and the map is affine, so the whole rectangle is valid.
- The doubled widths are 10, 4, 6, and each divides 60. The shift s → s+60k for k = 0..5 leaves every signed crossing unchanged on a 7×7 grid of the rectangle.
- **Replay.** The pair S=(3/10,3/4), T=(43/10,9/2) in direction (−16,5) reaches T exactly. The reflections are at (0,27/32), (5,77/32), (2,107/32), (5,137/32).
- **CRT replay.** Per-coordinate rounding plus CRT gives k=2740. This is also the nearest translate over a full period, with max error 9/2020. Δe, Δs, the slope 10328795401/62826, and all four mouth abscissas match the note. The full Fraction trace makes 173,106 reflections and reaches (17/4, 4+1/103) exactly.

### Full-row theorem (item 4)

The derivation is correct. The sign-corrected Jacobian is [[1,−a],[1,3+b]] with determinant 3+a+b. The correction stays inside the rectangle, and Kronecker and CRT apply as stated.

**What is lit.** Under condition 1 or 2, every pair (x, 1−a), (z, 4+b) with 0<x<1 and 4<z<5 is lit. These rows lie only in the bottom tip [0,1]×[0,1] and the top tip [4,5]×[4,5], and the tips are the whole polygon at those heights. Case 2 at a=1/101, b=1/103 lights all 25 test pairs exactly, including abscissas 1/1000 from the walls.

**Half-lattice rows.** On rows y=1/2 and y=9/2 (a=b=1/2) the theorem certifies nothing. Here 30a = 30b = 15, so both conditions fail and the rotations vanish. The only interior half-lattice pair there is (1/2,1/2)–(9/2,9/2). It lies outside the certified patch: the nearest error is 2/5, and the patch radius is about 1/100. The certified set on these rows is a parallelogram near (9/10, 43/10). The pair isn't dark, though: direction (−12,−11) lights it with 33 reflections, confirmed by an independent full retrace. The same failure occurs on every row where a or b is a multiple of 1/30.

### Gaps

1. **Medium.** The "sufficient condition on other realizations" paragraph is not yet a checkable condition. "The endpoint grid fits inside the local image" has no size attached. The paragraph also assumes, without proof, that a strictly interior through-crossing patch exists across the mouths. The determinant D+a+b > 0 and the choice of P are correct.
2. **Low.** The threshold q, q′ ≥ 101 comes from the chosen patch radius 1/100, not from the geometry. At a=1/97, b=1/103 the construction misses 5 of 273 grid pairs. A larger verified patch would lower the threshold.
3. **Low.** "Two complete rows" holds only on resonance-free rows. The note says so, but the title and opening never mention that the realization's own half-lattice rows are excluded.
4. **Low.** "The smallest dented target-1 word" matches the result of d165's `min(no_band, key=len)`. That call returns only one word, and other W=12 words that lack a band weren't checked.

## Scope (item 5)

Neither note changes a ledger status. COVERED requires Theorem S. PARTIAL requires a reviewed theorem that lights all pairs on an infinite metric subfamily of the word. Note 1 lights rows from child marks: one row family per geometry, not all pairs. Note 2 lights two rows in one fixed-length realization. Note 2 says this itself, and note 1 makes no status claim. The ledger split stays at 6 COVERED, 270 PARTIAL, 4,298 OPEN.
