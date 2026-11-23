# D157 review: doorway word bound and terminal-cap placement

Snapshots reviewed: `doorway-word-bound.2026-11-22-0405.md` and `terminal-cap-placement.2026-11-22-0405.md`.
Checks: `checks.py` (exact integer tracer, own polygon builder), output in `checks.log`, 0.6 CPU seconds.
Every polygon vertex is a stopping corner. No room search was run. Direction enumerations are over shots inside fixed named rooms.

## Verdict

**Sound with gaps.** The two-rectangle theorem is correct as stated, and its construction works shot by shot on four explicit rooms. The terminal-cap lemma is correct as a conditional statement. The DB55 and R22 calculations reproduce exactly. The gaps concern scope: neither note supplies the prefix slope interval that the cap lemma and the chain lemma both assume, and the notes say so.

## 1. Two-rectangle theorem

### Exact hypotheses

- Two closed lattice rectangles share a side segment of positive length, which is automatically an integer of at least one. Their interiors lie on opposite sides. The room is the interior of the union, with no mirror on the door.
- Coordinates are rotated so the door is horizontal. **D** is the bounding-box span along the door. **H** is the span perpendicular to it, which equals the sum of the two rectangle heights.
- The pairs are **all** distinct interior lattice marks. There is no parity condition. The brief's "parity-compatible" is stronger than what the note claims or needs.
- Lattice positions matter. The proof uses d, e, w ≥ 1 to bound slopes by 2H and 6H. For non-lattice marks the bound would degrade like 1/d.

### Proof check

- **Case split.** I checked that pairs in the same rectangle are mutually visible, and so are pairs in the closed overlap strip. Pairs with an endpoint on an overlap boundary line are covered too, because such an interior mark lies within the adjacent wing's height range. `checks.py` asserts that every pair not classified as one-wing or opposite-wings is direct. No assertion fired.
- **One wing and overlap.** The crossing formula c = (z+(e/d)u)/(1+e/d) is correct. Images ±v+2mB have gaps 2v and 2B−2v, both under 2B. So the closed interval of radius B about −(e/d)u contains an image. If the only image is the center, a neighbor within B exists. Hence 0<|c|<B: the shot avoids the reflex corner at height B, and c=0 would be a smooth contact on the common outer wall. The wide leg runs between u∈(0,H) and c∈(−B,B), so it folds at most once at height 0 and never reaches height H. The slope bound |c−u|/d ≤ (H+B)/d ≤ 2H is correct.
- **Opposite wings.** n ≥ 1 and |θ−K/w| ≤ B/d hold. On I the first-seam coordinate is d(s−θ)∈(−B,B). The exit image interval has center within wB/d of K and radius B+wB/d, so it covers (K−E,K+E) because E ≤ B. On that preimage the terminal range has length 2E(d+w+e)/(d+w) > 2E, so it contains a target image. Seam smoothness is right. Height 0 at the left seam lies on rect 1's straight bottom wall. Height H at the right seam lies on rect 2's straight top wall. The convex corners (w,0) and (0,H) are never contact candidates. The bound |s| ≤ 4B+2H ≤ 6H is correct.
- **Counting.** The path is monotone in x, so no vertical wall is touched, and the total transverse travel is at most 6H·D. The bound "contacts ≤ travel/h + 1 per strip, plus two interface contacts" is valid but loose. Each straight leg crosses the door at most once, which gives the 12HD+11 events bound.

### Exhaustive test on named rooms

Each nondirect pair was given the slope computed by the note's formulas: the one-wing image z, or K, n, θ and the first target image in the terminal window. That slope was then traced exactly.

| Room | W | H | D | Bound | Pairs (direct / one-wing / opposite) | Failures | Max reflections used |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L: [0,5]×[0,2] + [0,2]×[2,6], door 2 | 6 | 6 | 5 | 185 | 22 / 6 / 0 | 0 | 6 |
| T: [0,7]×[0,3] + [2,5]×[3,7], door 3 | 8 | 7 | 7 | 299 | 176 / 14 / 0 | 0 | 3 |
| Z1: [0,3]×[0,2] + [2,6]×[2,7], door 1, B<E | 8 | 7 | 6 | 257 | 78 / 7 / 6 | 0 | 16 |
| Z2: [0,6]×[0,3] + [4,10]×[3,6], door 2, B=E | 8 | 6 | 10 | 365 | 160 / 36 / 14 | 0 | 15 |

Z1 exercises the 180-degree normalization and a width-1 door. Z2 exercises the B=E tie. Every in-code assertion of the note's intermediate inequalities held. An independent short-shot check found every pair in all four rooms lit with at most 6 reflections, using |p|,|q| ≤ 6. All 539 pairs are lit, of every parity.

## 2. Terminal-cap lemma

- 2C/B = (2A+2L)/(A+2L−t) lies in (1,2) exactly when A+t>0 and t<L. So adjacent cap heights differ by 2HC/B, which lies strictly between H and 2H, and at most one of any two adjacent candidates hits Hℤ. The residue-class remark is correct, with n/gcd(n,2) ≥ 2 forced by the same inequality.
- If B·|I| > 4H, the image of I contains two consecutive members of σu+2Hℤ, so the conclusion follows.
- The legality test is complete for the stated geometry. The outbound leg passes the mouth inside I's window. Lateral contacts in the last rectangle are smooth except at depth L, which is the cap test. The return stops at depth t ≥ 0 before reaching the mouth side, and at the open mouth if t=0.
- **The hypothesis carries the weight.** "An open interval I on which one fixed developed chart clears every earlier window, including the mouth, with the required sheet" is assumed, not produced. The lemma is a placement test after such an interval exists. In DB55 the uniform criterion fails by a factor of about 9: B·|I| = 16/7 against 4H = 20. Only the indexed test rescues it, and nothing guarantees the indexed test in general. The clause "provided it includes their wall guards" for turned prefixes is not made precise.

## 3. DB55 slope −37/8

The traced shot from S=(1,1) in direction (8,−37) reaches T=(9,1) after 27 reflections: 4 in the left chamber, 14 in the corridor, the cap at (13, 1/2), and 8 more in the right chamber. Its only vertical-wall contact is the cap. The mouth heights are 5/2 at x=5 and 21/8 at x=8, matching 5/2+4δ and 21/8+7δ at five traced δ values. At δ=−5/56 the shot stops at the corner (8,2), and at δ=3/56 at (8,3). Points just inside both ends pass both mouths. The interval I contains only k=−4 for σ=+ and no k for σ=−. (19+15k)/2 is never 0 mod 5. No rightward-monotone shot with |dx|,|dy| ≤ 40 lights the pair. The same holds for the ×2 dilation from (2,2) to (18,2), with ≤ 30.

## 4. R22 top cap

R22 is rebuilt from the d8 `R22-base` cells: 22 walls, S=(0,0) and T=(2,2) both interior. The door at y=1 is 0<x<1 and both of its ends are reflex. The top mouth is 1<x<3 and the cap is at y=3. The halfway argument is exact. The developed T abscissa x′ is even, so the outward y=2 crossing is at x′/2, an integer, and 2 is the only integer in (1,3). No upward-monotone shot with |dx|,|dy| ≤ 40 reaches T. All 40 top-cap candidates (x′,4), for even x′ in [−40,40] except 0, stop at a corner before T, mostly at (1,2), (0,1), (1,1) or (−1,1). So the claim "forces an earlier visit to T, which is excluded" is verified. The chords from S and T to (1/2,1) are clear, as stated.

## 5. Scope

**What's proved in general:**

- The two-rectangle theorem, for all pairs, with no parity condition and any door width.
- Its localization to a slab with the same strip profile.
- The chain lemma under its explicit interval inequalities.
- The cap lemma, conditional on a prefix interval.
- The monotone and top-cap exclusions for the named R22 and DB55 pairs.

**Chain obligation.** For W ≤ 20 BBBB, you'd need a route-selection theorem. For every pair it must produce a word with these properties:

- It may include turns, revisits and returns through intermediate doors.
- One fixed chart with an open slope interval clears every door and lateral guard.
- That interval either satisfies the chain inequalities A_i w_{i−1}/A_{i−1} ≥ P_i+w_i, ending with > P_last, or passes the exact indexed cap test at its final reversal.
- It never treats an unused branch mouth as a mirror.

The halfway obstruction already appears at W=12 in DB55, so it can't separate R22 by wall count.

## Gaps

1. **High.** Neither note constructs the prefix interval I for general BBBB rooms. The cap lemma and the chain lemma are conditional on it. DB55 misses the uniform cap criterion by a factor of about 9 (16/7 against 20). The W ≤ 20 implication therefore remains open, as the notes concede.
2. **Medium.** Localization requires the whole open slab between the mark abscissas to have exactly the one-, two- or three-strip profile, with solid lateral walls. In a BBBB room this rarely holds for distant pairs, so the two-rectangle theorem gives no chain composition by itself. The note should say this explicitly rather than calling it "one way to reuse the theorem along a chamber graph".
3. **Medium.** The cap lemma's turned-prefix clause ("provided it includes their wall guards") is undefined. For a prefix that reverses at a vertical wall, the legal set within one chart must also exclude that wall's end corners. The lemma should state this as a hypothesis on I.
4. **Low.** The 6HD+5 count is loose. The construction used at most 16 reflections against bounds of 185 to 365, and the shortest found paths used at most 6. The per-strip "+1" and interface "+2" terms are valid but could be stated as one inequality.
5. **Low.** The hypotheses are implicit. Lattice marks are needed for d, e, w ≥ 1. The theorem covers all pairs; no parity condition is needed. Door width is any positive integer. The R22 top-cap exclusion covers one turned word only, which is correctly scoped in the note.
