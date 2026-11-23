# A parity-preserving stretch has no stabilization threshold

**Verdict.** No finite L(20) gives the proposed stabilization of either the marked sheet permutations or individual-direction visibility. The failure already occurs at 12 walls in one fixed combinatorial type, with both endpoint coordinates fixed. It does not decide whether *total darkness* is invariant under sufficiently large stretches, or whether there is a bounded representative for each dark room by some different argument. No census was run.

## One gap, four unchanged canonical types

A length coordinate has to preserve polygon closure. Use DB55 with chambers [0,5]×[0,H] and [8,13]×[0,H] joined by the open passage across [5,8]×[2,3], taking the interior of the union of the three closed rectangles. Increase the common top supporting line from H to H+2. This inserts two rows above the marks into a single gap in the ordered y coordinates. Both caps move, all ordered supporting-line incidences persist, and no corner or mark changes parity. For every odd H≥5 the room is strictly simple and normalized: horizontal wall lengths include 5 and 3, and vertical wall lengths include H and 2. It has r=4 and n=10H+3. Since n>8r and n>4r+4, the known proper-canonical and corner-only bounds put it in BBBB. [Area criteria](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md)

The degree n of the pillowcase map equals its number of cell sheets. At site x write f_x, q_x, r_x for the numbers of convex poles, regular two-cycles and reflex triples. The local degree sum gives n=f_x+2q_x+3r_x. Both corner counts stay fixed in this stretch, so every site permutation acquires ten more two-cycles when H increases by two. Permutation conjugacy, including conjugacy with marked incident sheets, preserves those counts. All four canonical quotients still have degree one. Thus the canonical *types* stabilize immediately and forget exactly the growing data in this example. [Local degree identity](clean-site-cost.md)

## Direction visibility changes above every threshold

Fix S=(2,2), T=(4,4), and primitive direction (1,2j), allowing all launch signs and all traversal counts. At every integer x encountered in the left box the folded height is an integer. The open mouth has no integral height, so the line cannot enter the corridor. Up to its first stop this is reflection in the 5×H box with the two extra stops at the mouth tips.

The bit for reaching T depends only on j modulo H: the vertical phase at each integer abscissa is taken modulo 2H, and changing j by H adds whole periods. There are no corners at nonintegral abscissas; a smooth cap reflection there is harmless. If H divides j, all those lattice heights are two, so the bit is zero. If 2j≡1 modulo H, a rightward, upward launch reaches T on its **first** crossing of x=4: the developed height is 2+4j≡4 modulo 2H. There is no intervening vertical wall. Consequently for every odd prime H≥5 the least period of this physical visibility bit is exactly H: it divides H and is nonconstant. This is an unbounded period of an observable, over and above the unbounded sheet count.

For H=5 and H=7 the following fixed lines already give opposite changes. A direct cell tracer independently checks all four bits. [Replay](stretch-control.py)

| Primitive direction | H=5 | H=7 |
|---|---|---|
| (1,50), j=25 | blocked | lit |
| (1,56), j=28 | lit | blocked |

For any fixed positive j, raising H by 20j preserves this pencil line's verdict. To see it, compare successive visits to the line y=4 in the left chamber. An excursion above it runs to the cap and returns; there is no opening or vertex in the added band except the two corners at the new cap. The extra horizontal travel to the cap is 20j/(2j)=10, one complete signed horizontal period of the width-five box. Cap contact, including whether it is a forbidden corner, and return to y=4 have exactly the old signed horizontal phase. The added vertical sides are smooth. The target lies at y=4 and is encountered on the same crossing, while the source and both mouth corners lie below it. The same argument applies until termination or indefinitely. Thus the two transitions in the table recur *simultaneously* at H=5+28000k and H+2 (28000 is a common multiple of 500 and 560). Both fixed lines change visibility above any proposed threshold. Declaring such phase changes to be “thresholds” would leave infinitely many of them on this one gap.

For this pair every odd H≥5 nevertheless realizes **all three primitive parities**. The direct chord has displacement (2,2). Reflecting the target across x=5 gives displacement (4,2), with a smooth wall contact at (5,7/2), above the mouth. Reflecting it across y=H gives (2,2H−6), whose primitive parity is horizontal because H is odd. That chord stays in 2≤x≤4. These three paths separate pair and class visibility from the changing individual directions.

## The other two controls

| Room | Degree | Canonical degrees relative to S, in a,b,c,d order | Regular two-cycle counts |
|---|---:|---|---|
| DB55 at H=5 | 53 | 1,1,1,1 | 24,24,24,24 |
| Same gap at H=7 | 73 | 1,1,1,1 | 34,34,34,34 |
| Cross b=7 | 96 | 1,1,1,1 | 42,46,48,46 |
| Cross b=9 | 128 | 1,1,1,1 | 58,62,64,62 |
| cov4181 | 28 | 1,1,28,1 | 12,14,0,12 |
| c4181s | 41 | 1,1,1,1 | 18,19,8,19 |

The cross extends four caps at once. Its named pair (6,0),(0,6) retains its legal diagonal even though each site gains 16 regular swaps. For cov4181 the source and target (2,3),(4,3) become (4,3),(6,3) after widening column x=1 by two and row y=4 by three. D144 gives only the horizontal class before stretching; d148 gives all three for every same-parity interior pair after stretching. Here two whole class exclusions disappear. The second insertion is odd and changes some corner colors; the marks preserve parity but this comparison is not a single even gap increment. [Named constructors](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/decomp.py) · [Original pair](dyadic-classes.md) · [Stretched room verdict](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d148-review-delinv/review.md)

## What shortening would still have to prove

For **one direction**, stretching can create or destroy blockage at arbitrarily large lengths. For **one primitive class**, the saved composite cov4181 stretch destroys exclusions; the even DB55 example preserves class illumination despite changing directions. For **total pair darkness**, none of the three controls supplies a creation or destruction example. A finite reduction only needs a one-way implication: from a dark pair in a long room, produce some dark pair in a smaller room, allowing its coordinates and witnessing obstructions to change. Such a descent must also handle marks lying in the removed strip. The growing permutation and period invariants rule out the proposed proof by exact stabilization; they do not refute this weaker descent implication. At present there is no justified cutoff or census size from this route.
