# D126: review of the whole-room decomposition note

Date: 2026-11-20. Reviewer: independent referee.

Reviewed file: `whole-room-decomposition.snapshot.md` in this directory (58 lines).

Context read: the d124 review, the d117 review and its cov279 snapshot, the `COV279` cells in `../d69-bbbb/decomp.py`, and the d124 cover code. I didn't evaluate the d125 notes, which are under separate review. No information went to outside services.

Own code: [checks.py](checks.py), log [checks.log](checks.log), under 1 CPU-second. It uses exact integers and `Fraction`. It runs only on the normalized cov279 stretch at the saved parameters q = 12j+4, j = 1..5. The only automaton it reads is the d124 first-hit cover along the fixed slope α = 1/φ². It does no search over rooms, rays, directions or reflection words.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Parallel cuts: at most r cuts, a tree of at most r+1 rectangles, single-door access | Sound. One low wording gap |
| 2 | Deep one-closed-end piece lights every pair in the room; conditional area cutoff | Sound |
| 3 | Deep two-ended piece reduces dark pairs to same-end or near-collar pairs | Sound with fixable gaps (low) |
| 4 | Large area forces neither inequality; cov279 is a decomposition-independent obstruction | Sound with fixable gaps (one medium) |
| 4a | cov279 facts: r = 6, n = 13q+3, normalization, block argument | Sound. Verified exactly at q = 16, 28, 40, 52, 64 |
| 5 | No universal N(r) results from these tools | Sound, as a statement about the method only |
| — | Census arithmetic | Sound |

## 1. The parallel-cut decomposition

The construction is correct. At a reflex vertex, extending the vertical edge enters the open 270° sector. The chord stops at its first boundary contact. A vertical chord can't arrive at a convex vertex through its open sector. If it meets a vertex collinearly, that vertex is reflex, and the chord also resolves it. So the number of cuts is at most r. It is smaller when chords pair two reflexes: cov279 has r = 6 but only 4 vertical cuts and 3 horizontal cuts.

Parallel cuts can't cross. The note says they can't end transversely on an earlier cut. They also can't meet an earlier cut collinearly at its endpoint. That endpoint lies on the original boundary, and a collinear arrival would put interior on both sides of a wall, or along a wall edge. Strict simplicity excludes both. So every cut is a crosscut of the original room, each adds one face, and the dual graph is a tree. Faces have no reflex corners, so they're rectangles.

For a vertical-sweep piece R, the horizontal sides are original walls, since all cuts are vertical. Two doors on one side of R can't share an endpoint. The orthogonal vertex between them must own a vertical edge on that side. Each component of the tree minus R meets R in exactly one crosscut. Closing it gives a sub-polygon bounded by a Jordan curve, so the sealed chamber is strictly simple.

`checks.py` confirms all of this on both canonical decompositions at every saved q. The vertical tree has 5 rectangles and the horizontal tree has 4. Each is a path. Every attachment has exactly one door. Every sealed attachment is hole-free and pinch-free, and its d124 cover is transitive.

## 2. The one-closed-end theorem

**Use of d124.** The note uses only the d124 chamber lemma and its interval, not the d124 corridor gluing. A sealed chamber of area at most B has a four-copy cover of at most 4B squares. So T = 1+F_(3·4B−1) = 1+F_(12B−1), as stated. The interval α ± 1/(4T²) has width δ = 1/(2T²). It excludes every fraction with denominator at most T, so every first-hit word is fixed on it. A larger B only shrinks the interval. The d124 hypotheses needed here are a strictly simple sealed chamber and a lattice door of integral length. Both hold by section 1. The d124 equal-span hypothesis isn't needed. It belongs to the straight corridor, and here the period 2H comes from the receiving rectangle. The note says this correctly.

**Depth threshold Z = 4HT².** The spans check exactly (section E of the log):

- Closed end, two exterior marks: derivative 2L+a+b, span at least 2Lδ = L/T² ≥ 4H > 2H.
- Exterior mark to a target in R at depth x: reflected travel 2L−x ≥ L, span at least 2H.
- Two marks of R on different left doors: the far-wall reflection at the average height lies strictly inside the far wall.

**Corner contact.** A 90° corner reverses the velocity. The unfolded straight continuation is therefore the physical retrace. So a matched path through a far corner returns to the source's own door point with reversed direction. For different components this contradicts the matched arrival, as the note says. For one component, both legs then trace one billiard orbit, so one mark lies on the other's leg. The truncated path is legal. The far corners are convex corners of the room, because the far side and both long sides are walls.

**Area cutoff.** R has at most r attachments, so LH ≥ n − rB. With H ≤ D, the inequality n ≥ rB + 4D²T² gives L ≥ 4DT² ≥ Z. The algebra is correct. The note rightly calls this a test on a class, not a bound on counterexample area.

## 3. The two-ended reduction

The three cases are correct.

- Opposite ends: derivative L+a+b, span at least 2H. The only contacts are the two long walls.
- Exterior mark to a mark at depth x ≥ Z from its access end: span (x+a)δ ≥ 2H.
- Same end: the root of 2Ls + f − g = 2kH puts the far contact at (f+g)/2 + kH. A shift of k by one maps the folded height y to H − y. The door-center test has error at most (w₁+w₂)/4, as stated.

So the residual is a same-end pair failing the far-wall test, or an exterior mark with a near-collar mark. The reduction is a statement about endpoint positions, as the note says.

**Gap 3a (low).** "At exact span 4H use L > Z" is unnecessary. A closed interval of length 4H contains two consecutive multiples of 2H, so both parities occur. Likewise, "exceeds 2H" at L = Z with zero-length legs is "equals 2H". That still suffices on a closed interval. Fix: write "is at least" and drop the caveat.

## 4. The cov279 obstruction

**Room facts.** The stretch has bands (0,2): (0,2q), (2,3): (2q−3,4q), (3,4): (2q,5q), (4,6): (4q,6q). At each saved q the script confirms the following:

- Area 13q+3 and 6 reflex corners, so 16 walls.
- Horizontal wall gcd 1, since q ≡ 1 mod 3. Vertical wall gcd 1.
- Width 6q, height 6, no pinch, no hole.

**Block argument.** Both blocks lie in the room and have area 4q. A rectangle meeting both in positive area contains bottom-height points with abscissa above 2q. All such cells are outside the room. So any central piece misses one block. With at most 7 pieces, one other piece has area at least 2q/3. Then Z_B ≥ 4(1+F_(12⌈2q/3⌉−1))² exceeds 6q at every saved q. It already exceeds 10⁵⁴ at q = 16. This argument is correct and holds for every decomposition into at most r+1 rectangles.

**Both canonical decompositions, piece by piece.** The script lists every piece with its depth L, attachment areas and Z_B. It also computes the first full index k* of every attachment from the d124 cover, and the refined Z* = 4H(1+F_(k*+2))².

| q | Vertical pieces L × H | Largest L | Smallest Z* over pieces | Horizontal pieces: depth | Pieces with L ≥ Z* |
| ---: | --- | ---: | ---: | --- | ---: |
| 16 | 29×2, 3×3, 32×2, 16×3, 16×2 | 32 | 9.6 × 10⁸ | 2, 1, 1, 2 | 0 |
| 28 | 53×2, 3×3, 56×2, 28×3, 28×2 | 56 | 2.0 × 10⁷ | 2, 1, 1, 2 | 0 |
| 40 | 77×2, 3×3, 80×2, 40×3, 40×2 | 80 | 7.8 × 10⁶ | 2, 1, 1, 2 | 0 |
| 52 | 101×2, 3×3, 104×2, 52×3, 52×2 | 104 | 2.0 × 10⁷ | 2, 1, 1, 2 | 0 |
| 64 | 125×2, 3×3, 128×2, 64×3, 64×2 | 128 | 5.3 × 10⁷ | 2, 1, 1, 2 | 0 |

The computed k* ranges over 7–26, and it isn't monotone in q. Every piece in both orientations has a side of at most 3. So the d125-style large-rectangle route also has no piece. No piece meets the one-ended or two-ended inequality, even with the refined T*.

**Gap 4a (medium): the refined T* route isn't addressed.** The note offers T* = 1+F_(k*+2) in section 2. The obstruction paragraph argues only with the area-based Z_B. A reader can ask whether a bound on k* in terms of r rescues the route. It doesn't, by a short argument:

- T* bounds the actual first-hit travel from every square of the cover.
- A vertical-type piece has an attachment of area at least 2q/3 and height at most 6. So it spans at least q/9 columns.
- Some cell center is at least q/18 − 1/2 from the door line. So T* ≥ q/18 − 1.
- Then Z* ≥ 4(q/18 − 1)² > 6q ≥ L for every q ≥ 522.
- A horizontal-type piece has depth at most 6, while Z* ≥ 4(1+F₂)² = 16.

So no first-access bound that dominates the true travel can meet L ≥ 4HT² in cov279 for large q. This holds whenever the common interval has width of order 1/T², as in d124. At the saved q the canonical trees fail by computation. The review didn't check non-canonical trees with at most 7 pieces for q < 522; that would be a search. *Fix:* add this paragraph. Also restate the "next lemma" accordingly. Shrinking T toward the travel can't help in cov279. A useful bound must replace the single 1/T² common interval, for example by the crossing arithmetic the note mentions.

**Gap 4b (low).** "Every inscribed axis-aligned rectangle" in the odd-cross row and "inscribed" here mean "contained". Fix: say "contained in the room".

## 5. What "no universal N(r)" rules out

The conclusion is about the method, and the note states it that way. "The unconditional area cutoff for illumination is undetermined" is correct.

**What it rules out.** cov279 is a family with r = 6 ≤ 8 and area 13q+3 → ∞. In every decomposition into at most 7 rectangles, no piece meets the following:

- The one-ended or two-ended inequality L ≥ 4H(1+F_(12B−1))², with B the largest attachment area.
- The refined L ≥ 4H(1+F_(k*+2))², by computation at the saved q in both canonical trees, and for all q ≥ 522 by gap 4a.
- Both sides growing. Every piece has a side of at most 3.

So no statement "r ≤ 8 and n ≥ N(r) implies one of these certificates applies" can hold. That is all it rules out.

**What it doesn't rule out.** It gives no dark pair and no lower bound on any true cutoff N(r). Other certificates remain possible. The note's own example is the d117 arithmetic for the marked pair.

**Are all pairs lit in the family?** Not established. d117 proved only that the one marked pair S = (q/2,1), T = (3q,3) is lit. It replayed the translate shots for j = 1..5 and the exact-check shots for m = 1..8. d117 also proved this pair needs a reflection count that diverges as t → 0. No source checks the other pairs of the stretched rooms. The note's table says "the specified pair is lit", which is accurate. *Fix (low, gap 5a):* add one sentence: illumination of all pairs in the cov279 family is open, so it obstructs the method, not the conjecture.

**Census.** 3,933,192 / 72.5 s = 54,250.9 per second. Through 10¹¹–10¹² rooms that gives 512–5,120 CPU-hours. This matches "roughly 510–5,100". The phrase "the unconditional threshold for a decomposition into r+1 pieces is N = 1" is correct but reads oddly. It means the decomposition exists at every area.

## Ranked gaps

| Rank | Gap | Fix |
| --- | --- | --- |
| Medium | 4a: The obstruction paragraph doesn't treat the refined T* test. | Add the farthest-cell bound T* ≥ q/18 − 1. It gives failure for q ≥ 522, plus the computed canonical values at the saved q. Retarget the "next lemma" away from shrinking T. |
| Low | 5a: The note doesn't say that all-pair illumination of cov279 is open. | Add one sentence: only the marked pair is proved lit. |
| Low | 3a: The exact-span-4H caveat is unnecessary; "exceeds 2H" can be equality. | Write "is at least", and drop the L > Z caveat. |
| Low | 1: The collinear meeting of a later cut with an earlier cut endpoint is omitted. | Add one sentence: strict simplicity excludes it. |
| Low | 4b: "Inscribed" means "contained". | Reword. |

## Scope

The decomposition, the one-ended theorem and the two-ended reduction are correct as stated. The cov279 obstruction is correct and slightly stronger than the note claims. No universal N(r) follows from these tools. That says nothing about the true cutoff: whether cov279 rooms have every pair lit is unknown.
