# D127: review of the thin-room lighting theorem

Date: 2026-11-21. Reviewer: independent referee.

Reviewed file: `thin-room.snapshot.md` (identical to `qclass-closure/bbbb/thin-room.md`). Replay: `thin-room-replay.snapshot.py` (identical to `thin-room-replay.py`).

Context read: the d126 review (cov279 room facts), `general-gluing.md` (odd crosses), and RESULTS.md §11. No information went to outside services.

Own code: [checks.py](checks.py), log [checks.log](checks.log). It took about 15 CPU-seconds. It uses `int` and `Fraction` only and imports nothing from the author. It builds the room from its 16 vertices and derives the slabs from the edges. The tracer folds inside each open slab, where both side walls are full-height edges. At every slab level it classifies the point exactly as a vertex (illegal), horizontal-wall interior (reflect) or interior (cross). A second, edge-by-edge tracer with no slab shortcut matches it on 80 sampled certificates. Certificates come from the note's formulas. Nothing searches over directions or reflection words. Section E samples slopes only to test the two negative claims.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Every same-parity interior lattice pair is lit for q = 12j+4, j ≥ 1 | Sound |
| 1a | Four-band crossing, steps 1 to 4, for heights (1,5) | Sound. One low exposition gap (parity of F) |
| 1b | Matching criterion: shift s+kP works iff F ∈ gcd(dP,2u)ℤ | Sound |
| 1c | Two-band Bézout cases (1,3), (2,4), (3,5), and the special pair (3q,3)–(5q,5) | Sound |
| 1d | Vertical travel ≤ 6, horizontal travel O(q²), primitive vertical component ≤ 3 | Sound with fixable gaps (low wording) |
| 2 | Replay counts 2,182 and 6,922 at q = 16 and 28, with 481 and 1,513 four-band pairs | Sound. Reproduced independently |
| 3a | Height alone doesn't give the modulus: least first-door period 4q | Sound |
| 3b | Monotone upward passage fails for X = 2q−1, Y = 6q−1 | Sound |
| 3c | Odd crosses defeat the fat-regime piece geometry | Sound |
| 4 | Generalization to even q ≥ 4 coprime to 3 | Sound, and stated too narrowly: odd q also works |
| — | DBas and DB55 controls | Not checked |

## 1. The proof for all q

**Room.** The builder confirms 16 walls, 6 reflex corners and area 13q+3 at q = 16, 28, 76 and 100. The slabs are (0,2q) for 0<y<2, (2q−3,4q) for 2<y<3, (2q,5q) for 3<y<4 and (4q,6q) for 4<y<6. Interior rows are y = 1: (0,2q); y = 2: {2q−2, 2q−1}; y = 3: (2q,4q); y = 4: (4q,5q); y = 5: (4q,6q). Each row is one open interval.

**Case split.** The same-parity height pairs are (1,1), (3,3), (4,4), (5,5), (1,3), (2,4), (3,5) and (1,5). Height 2 has no same-parity pair, because its two points differ by one. Equal heights have a direct chord in one open interval. That leaves exactly the four cases the note treats. Marks on the interface heights 2, 3 and 4 appear in (1,3), (2,4) and (3,5), so the split is complete.

**Step 1.** X + 3s = c + 4qi, and both choices of c fold to 2q−1 inside the opening (2q−3,2q). Two values of 3Y+2X−2c differ by 4, so both vanish mod 2q only if q ≤ 2. The bottom contact is X+s = (odd)/3, never a multiple of 2q. Every other contact in band 0 is a side wall at 0<y<2, which is wall interior.

**Step 2.** The three phases of Y−4q−s mod 4q are spaced 4q/3, so one is within 2q/3 of zero. Zero would need 3Y+X−c ≡ 0 mod 4q, which is odd. So 4q < x₄ ≤ 4q+2q/3 < 5q.

**Step 3.** A shift by 4q preserves both outer legs, since 3·4q and 4q are multiples of 4q. The three phases mod 6q are spaced 2q, so one is within q of zero. Mod 2q the phase is Y−2s. Its vanishing forces 3Y+2X−2c ≡ 0 mod 2q, which step 1 excluded. So 2q < x₃ ≤ 3q.

**Step 4.** P = 12q preserves all three placed legs. In band 1, gcd(12q, 4q+6) = 2·gcd(6q, 2q+3) = 2·gcd(9, 2q+3) = 2 when 3 ∤ q. The criterion then needs F even.

**Gap 1a (low): the parity of F.** The note's sentence on outer folds is correct but terse. A direct argument: every other leg acts on the horizontal coordinate as x ↦ ±x + 2m. So F ≡ ±Y − X − 6s mod 2. Here 6s = 2(c−X+4qi) is an even integer and X ≡ Y mod 2, so F is even. The script confirms F even for every four-band pair at every tested q. *Fix:* replace the sentence with this two-line computation.

**Legality.** The only horizontal contact is the bottom. All seam crossings are strictly inside the open overlaps (2q−3,2q), (2q,4q) and (4q,5q). Every side wall of every slab is a full-height edge, so side contacts strictly inside a slab are smooth. The final reduction modulo 12q(2q+3) preserves everything, since 12q(2q+3) = 6q(4q+6).

**Two-band cases.** The crossing set (U+V)/2 + gcd(u,v)ℤ is correct. The gcds are 1, 1 and q when 3 ∤ q. The (3,5) flip argument is correct. Only (3q,3)–(5q,5) fails both flips. Its special shot s = 3q/2 crosses y = 4 at 9q/2. It meets the right wall at (6q,5), which is wall interior. It reflects on the top at physical 9q/2 and arrives at (5q,5). My tracer confirms this at every tested q.

**Gap 1d (low): the nonhorizontal clause.** "A nonhorizontal certificate can be chosen with primitive vertical component at most three" doesn't hold as written for equal-height pairs. The note lights those by a horizontal chord and gives no nonhorizontal one. *Fix:* restrict the clause to pairs at different heights. The measured bounds are otherwise correct. Slope denominators are at most 3. Vertical travel is 6, 4 or 2. The maximum horizontal travel over q² is 156, 151, 147 and 146 at q = 16, 28, 76 and 100. The bound 72q(2q+3)/q² is 157.5 at q = 16.

## 2. Independent replay

| q | Pairs | Four-band pairs | Failures | Brute-tracer cross-checks |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 2,182 | 481 | 0 | 40 |
| 28 | 6,922 | 1,513 | 0 | 40 |
| 76 | 52,522 | 11,401 | 0 | — |
| 100 | 91,306 | 19,801 | 0 | — |

These are all same-parity pairs, not a sample. Every certificate ends exactly at its target with no corner contact. The author's script, run once, prints the same counts at q = 16 and 28: 2,182/481 and 6,922/1,513. It also prints 14,326, 24,394 and 37,126 at q = 40, 52 and 64, matching the note.

## 3. The negative claims

**Least period 4q (sound).** With direction (a,1) from (X,1), the exact tracer accepts the first door at y = 2 exactly when X+a mod 4q lies in {2q−2, 2q−1, 2q+1, 2q+2}. The least period in a is 4q at q = 16 and 28, for X = 1, q and 2q−1. The gap argument 1, 2, 1, 4q−4 is correct.

**Monotone obstruction (sound).** For X = 2q−1, every sampled slope with a legal first door lies within 4 of 0 mod 4q. The sample uses step 1/7 over [−4q, 4q). The backward point at y = 4 from Y = 6q−1 then lies within 4.86 of 6q, so it misses (4q,5q). The analytic bound "within five" holds for q ≥ 5.

**Odd crosses (sound).** At b = 7, 9 and 11 the largest contained lattice rectangle has shorter side 4, while the bounding box is 2b. The first-hit argument repeats the d126 farthest-cell bound: an arm piece's attachment spans order b horizontally, so T* grows like b. Then 4HT² grows like b² and exceeds the depth b−2. I checked that argument by reading only.

## 4. Scope

The theorem as stated, q = 12j+4, is proved. The proof uses only 3 ∤ q and q > 2, which together mean q ≥ 4. Step 1 fails at q = 2. Evenness of q is never used. The prescribed certificates succeed for every same-parity pair at q = 4, 5, 7, 8, 10, 11, 13, 14, 17, 20 and 22.

When 3 | q, the construction breaks in two places. In step 4 the gcd is 6 or 18. In (1,3) and (2,4) the Bézout gcd is 3. The failure counts are 62 of 267 pairs at q = 6, and 2,128 of 7,971 at q = 30. That shows only that this method fails for those q. It doesn't show any pair is dark. Lighting for 3 | q remains open.

## Ranked gaps

| Rank | Gap | Fix |
| --- | --- | --- |
| Low | 4: "even q ≥ 4 coprime to 3" is narrower than the proof. | State "every q ≥ 4 coprime to 3", odd q included. Say that 3 \| q is open for this method. |
| Low | 1a: the parity of F is argued tersely. | Use F ≡ ±Y − X − 6s ≡ 0 mod 2, with 6s an even integer. |
| Low | 1d: the nonhorizontal, vertical-component-3 clause fails for equal-height pairs. | Restrict it to pairs at different heights. |
| Low | The DBas and DB55 controls weren't refereed here. | Treat them as unreviewed until a separate check. |
