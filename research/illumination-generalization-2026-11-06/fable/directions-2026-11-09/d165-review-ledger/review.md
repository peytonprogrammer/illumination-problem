# d165 review: d163 pattern ledger

Target: `d163-pattern-ledger/` (ledger.md, ledger.py, ledger.json, ledger.log).
Checks: [checks.py](checks.py), output in [checks.log](checks.log). The run takes 2.7 CPU
seconds and shares no code with ledger.py. It's combinatorial only: no rays, directions or
room searches. The d162 constructions build one explicit member per word and check its
word, strict simplicity and metric hypothesis. They don't trace any shot.

## Verdict

**Sound with gaps.** The enumeration, realizations, family rules, dent lemma, named-room
words and the d15 COVERED rows are all correct. The status column is out of date: d162 is
now reviewed, and its main theorem gives an all-pairs metric member to all 266 histogram
words. The ledger still files them OPEN. M2 is also framed too narrowly to close
target 1, and the cov279 PARTIAL rests on a lattice-only result.

## 1. Counts and mirror convention

- A bitmask orbit enumeration over rotations and reversals gives 1, 1, 4, 8, 29, 79, 280,
  912, 3,260. The word sets equal the ledger's at every W.
- **Reversal is the right equivalence.** L and R mean convex and reflex, which are
  intrinsic. Reflect a CCW polygon and traverse it CCW again, and you get the reversed word
  with the same letters. This holds for all 4,574 realizations. Reversal combined with an
  L/R swap gives #L − #R = −4 on every word, so it's not an equivalence on CCW words.
- 4,212 of the 4,574 classes are chiral. Necklaces (rotation only) would number 6,310 at
  W = 20. Merging mirror images is correct, because illumination is invariant under
  isometry.

## 2. Realizations

The spot sample covers all 43 words with W ≤ 12 plus 200 random words with W ≥ 14. All
243 pass every test:

- integer coordinates
- axis-parallel edges with nonzero lengths
- exact turn word, with vertex i carrying w[i]
- CCW orientation and strict simplicity, using an orientation-based segment test of my own
- raster area equal to the shoelace area
- a left-hand boundary walk with no pinch and one component

All 4,574 realizations also pass every test.

## 3. Statuses

- **d15 (COVERED, W ≤ 8): justified.** Theorem S covers strictly simple orthogonal rooms
  with real vertex coordinates and r ≤ 2, for every pair of distinct interior points. Its
  type list is over coordinate order types, including coincident coordinates, so every
  real length assignment of every r ≤ 2 word falls in some type. The boundary walk maps
  the d15 type files onto the words: r = 2 gives 8 types and 4 words, r = 3 gives 70
  types and 8 words. Both are exactly the ledger's word sets. The scope is interior points
  only, which matches the goal.
- **Plus (d161): justified.** A hall with four full-side arms is a proper metric subfamily
  of (LLR)⁴, and d161 covers all real pairs in it.
- **DB55 word (d112): justified.** Rectangular dumbbells with L > 4d cover all real pairs.
  Every realization of (L⁴R²)² is a dumbbell, but the chamber sides beside the mouth need
  not be collinear. So d112 covers a proper subfamily. d108 and d77 are lattice-only
  extras.
- **U2 (d84): justified.** The rim test lights every real pair in U2 and its stretches.
- **cov279 (d127): weak.** d127 lights same-parity lattice pairs only. No length
  assignment of this word has every pair proved lit, so this row should be tagged
  PARTIAL-lattice. See gap 3.
- **d162: should move words.** The one-sided stacked-hall theorem holds for every pair of
  distinct real interior marks. Its hypotheses are a hall [0,A]×[0,c], nested roof
  rectangles that may be flush, and 8Ah ≤ cu. Every histogram word L⁴P has such a
  member: use unit steps, A = k+1 and c = 8A·H. checks.py builds that member for all 266
  histogram words with W ≥ 10, with 0 failures. They are 245 one-bank words, 15 pyramids,
  6 Ferrers words and 3 three- or four-corner orthoconvex words. All 266 are OPEN in the
  ledger.
- **d162 second step.** This class has two-sided halls with both banks strictly inside
  [A/4, A/3] and 16Ah ≤ cu. Its words have the form LL P₁ LL P₂, with P₁ and P₂
  balanced and nonnegative. There are 10 such words: the plus and 9 OPEN words at
  W = 16 and 20, including **cov4269**. The d162 reviewer read this proof and found it
  correct, but tested only one member. Treat these 9 as provisional.
- **d157: moves nothing.** Two-rectangle rooms have W ≤ 8, and the theorem covers lattice
  marks only. The slab localization works per pair, not per room.
- **Crosses: move nothing.** The odd crosses already sit in d161's plus subfamily.
  d87 and d147 each cover one named room.
- **d76: moves nothing.** It covers specific pairs only.
- **Corrected split.** With d162's main theorem only, the split is 6 COVERED, 270
  PARTIAL and 4,298 OPEN. With the second step as well, it's 6, 279 and 4,289.

## 4. Families

- **Rules: confirmed.** My own heading-based rules reproduce every subfamily with 0
  mismatches:
  - A histogram is an edge class with exactly one edge whose heading opposes all the
    others.
  - Corner vectors come from reflex counts by incoming heading.
- **Dent lemma: confirmed.** Rows are intervals if and only if the room has no horizontal
  dent. This is the standard characterization, and the raster check finds 0 mismatches.
  An edge with two reflex ends is the right word-level notion for convexity in one
  direction. It doesn't measure pocket depth, so it says nothing about how hard a word
  is.
- **1,020: confirmed,** but it includes the 85 dent-free orthoconvex words. 935 words
  have at least one dent.
- **944: confirmed.** It's the OPEN words only. U2 makes 945 in total.
- **Named rooms: correct.** The covN indices follow d72's (n, cells) sort. cov4181 matches
  the cells in d66, and room 1843 matches the d64 log. All 12 rooms walk to the words,
  families and statuses in the table.

## Gaps

1. **High: stale statuses.** d162 is reviewed, so 266 histogram words have an all-pairs
   metric member and are PARTIAL by the ledger's own rule. RESULTS §11 already says "now
   PARTIAL", but ledger.json and ledger.md still say OPEN or pending. Add the 9
   two-sided words, including cov4269, as provisional.
2. **Medium: M2 doesn't close target 1.** A "two-sided stacked hall" needs a full-width
   hall band. In 296 of the 935 dented one-direction-convex OPEN words, the ledger's own
   realization has no such band. The smallest is LLLRLLLRLLRR at W = 12. So M2 for
   arbitrary lengths still leaves those words PARTIAL. State target 1 as "convex in one
   direction, every length".
3. **Medium: cov279 PARTIAL is lattice-only.** d127 doesn't light all pairs at any
   length. Tag each PARTIAL with its pair scope, either "real" or "lattice".
4. **Medium: PARTIAL definition.** PROGRAM.md defines PARTIAL as "only some lengths". The
   ledger replaces that with "word-specific". Its strict-reading example, d80, lights
   irrational marks only. d126 lights every pair whenever one piece with a closed end is
   deep enough, which plausibly puts every word in PARTIAL with all pairs. The ledger
   doesn't check this, and either way PARTIAL carries little information.
5. **Low: labels.** "Dents in one direction only (1,020)" includes 85 words with no
   dents. "One dent per direction (944)" counts OPEN words only.
6. **Low: Ferrers pending note.** The terrace-induction entry is redundant, because d162
   already gives every Ferrers word a member.
7. **Low: Turtlegons citation.** I couldn't check the citation without network access.
   The per-word constructions make it unnecessary.
8. **Low: d84 one-cylinder theorem.** It covers DBas and a 58-cell bay room. Whether bay
   insertion defines a family that would add PARTIAL words is unchecked.

## Usefulness

The ledger is a sound map of the word space and a reasonable way to rank structural
targets. As a progress or probability measure, it's weak.

The biggest blind spot is metric. Each word is a cone of length assignments with W − 2
dimensions, and statuses are per word while proofs cover metric regions. Only d15
handles every length. A word-level ledger can't show progress until a theorem covers
whole cones, and PARTIAL hides how much of each cone is covered.

The second blind spot is the "other" family: 3,539 words (77%) with dents in both
directions, which the ledger gives no structure. Concretely, it should track the covered
region per word, such as "tall hall" or "L > 4d", and its pair scope.
