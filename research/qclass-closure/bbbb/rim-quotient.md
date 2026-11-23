# Where R22's period ten comes from

**Result.** The five-square staircase fold induces the same degree-three translation cover in both manuscript charts. Reduction modulo ten on either thirty-unit contour is its restriction to that contour. In cov4181 the unique proper quotient also separates the endpoint lifts, but regular far-class pairs can project to distinct sheets there. Separation alone does not explain darkness. There is an area obstruction to reconstructing R22's particular congruence mechanism in the large-area problem.

## The two charts are images of one cover

Use the manuscript coordinates and the three copies of the staircase. On signed unfolding squares fold the cell into the staircase and multiply its sheet signs by the two diagonal entries of the derivative of its copywise folding isometry. The resulting map F from 60 squares to 20 commutes with both right and up neighbors. This follows across each seam because the physical copy reflection exactly compensates the change of sheet downstairs; the checker verifies all 120 identities, including the exterior identifications. Every target square has three preimages. The map also commutes with simultaneous sign reversal. Away from vertices this is a translation cover; it extends unbranched on the translation unfoldings, since every staircase reflex has only reflex preimages of the same cone angle and all other preimages are regular. Branching can occur on the half-turn quotients.

Integral straightening of either saved direction changes the neighbor permutations by the same words on both surfaces, so F still intertwines them. In each direction the two ten-unit staircase rows lift to thirty-unit rows, with the ten individual square labels repeating three times. Both completed contours of the chosen cylinder project by the circle map with period ten. A change of contour origin translates the residues together.

| Direction | Residues of S | Residues of T | Regular physical far-rim midpoint sites |
|---|---|---|---|
| (4,7) | 1,3 | 7,9 | (−1,0), (1,0) |
| (7,4) | 0,8 | 4,6 | (2,1), (2,3) |

All four far-rim sites are smooth seam endpoints that fold to convex staircase corners. A convex point is a leaf on the downstairs rim tree and has only one contour representative. The two upstairs representatives of each regular site therefore coincide modulo ten. In the first direction the paired positions are 3 and 23, and 5 and 15. In the second they are 5 and 25, and 13 and 23. Their oriented differences give exactly 10 and 20 modulo 30. By the rim equation a two-traversal connection would need the same difference between source and target representatives. Their residues are disjoint in both charts. This derives the missing matches from the fold; the two charts alone would not prove all-direction darkness. [Exact verifier](rim-quotient.py) · [Full output](rim-quotient.txt) · [Rim equation](adjacent-cylinders.md)

## Why the same congruence explanation stops at large area

Suppose a normalized room of area n has two geometric cylinders exchanged by the half-turn. Its quotient cylinder has height one and circumference 2n, as proved in the rim note. Fix one far rim with t reflex corners. Suppose some divisor m>2 of 2n forces *every regular integral far-rim pairing* to have contour difference zero modulo m. Then

    n ≤ 4t+2.

Indeed the metric tree has 2t+1 unoriented edges and total length n, because its contour traverses each edge twice. Edge lengths are positive integers in the straightened chart. On an edge occurrence beginning at i paired to m₀, an interior lattice site at offset u has difference i−m₀+2u. If the edge has length at least three, offsets 1 and 2 are both regular sites, and their differences differ by exactly two. They cannot both vanish modulo m. Every edge therefore has length at most two. Summing proves the bound.

In particular at r≤8 and n≥35 **neither rim in any such chart** can trap all its regular integral pairings in a single zero-residue congruence of modulus greater than two. At n≥49 this obstruction applies throughout d81’s range whenever the specified chart exists. This does not force a match for a given pair: its required differences can still lie in gaps even when the available differences generate the full even subgroup. The result concerns a congruence on the entire far rim, and says nothing about rooms lacking these charts.

## cov4181 distinguishes separation from control of the far rim

In the saved labeling the unique proper pillowcase block system has four blocks of seven sheets. Both lifts of S project to the fixed block 3 at the source pole, and both lifts of T to the fixed block 2. Yet at target class d seven regular transpositions exchange sheets across blocks 1 and 2. Those regular sites project to a degree-two point in the quotient, where two different sheets meet. Thus the quotient separates the marks but does not collapse every admissible d-midpoint pairing to one sheet, as the staircase contour quotient did. This computation does not identify a cause that excludes every d-path. That exclusion comes from d66's complete orbit. At b the regular swaps include seven across blocks 2 and 3, and the actual horizontal segment connects the marks through (3,3). [D66 verdict](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/README.md)

The next structural question is how the specific set of differences required by the four source and four target representatives can stay inside the uncovered intervals as the chart changes. A proof based only on the subgroup generated by all far-rim differences loses precisely that information.
