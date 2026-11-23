# Arc reconnection on the four proper factors of the seven-unit cross

The seven-unit cross has 69 interior lattice points. All **574 same-parity pairs are physically lit in all three primitive classes**, and all 1,772 mixed-parity pairs are lit, accounting for all 2,346 unordered pairs. Projecting the same legal shots connects the marked images in **1,722/1,722 pair-and-class cases on each of the four proper factors**. The table below measures how much of this result comes from the prescribed twist pencils. [d147 independent calculation, checks 3–6](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d147-review-crossarcs/review.md)

## A simultaneous congruence test for any factor

Write A for the source permutation and D for the permutation at the other end of the reference arc. Twist a disk containing D and an adjacent non-source branch site E, using the boundary permutation h (the product in cyclic order). A and its marked vertices stay fixed. As the twist power j varies, the D-vertices incident to a given source vertex U are the D-cycles C meeting h^j U, up to reversing the sign convention for every j. Here U is one A-cycle. This follows from conjugating the two peripheral loops inside the disk. [Arc and twist dictionary](five-sheet-arcs.md)

Label the edge from U to C by the set of residues j modulo ord(h) for which that intersection is nonempty. Explicitly, in each h-cycle of length l, for every x in U and y in C in that cycle, include the residue pos(y)−pos(x) modulo l. Take their union. Label a walk by the intersection of its edge labels, and take the union over walks between marked vertices. The result is exactly the set of powers giving a connection. Indeed, fixing a single residue in advance gives the ordinary bipartite incidence graph of that one twisted arc. Connectivity commutes with taking this residue slice. One can therefore use ordinary finite transitive closure, replacing Boolean OR and AND by set union and intersection. This allows arbitrarily many intermediate A-vertices while enforcing the same twist power at every contact. No full cycle of h, universal connected component, or independent choice of twist for each contact is required.

## Exact named control

Use the standard tail order a,b,c,d with a at the common mark parity. For each requested target tail use each adjacent non-source partner in that order. The first sheet is the lower-left cell (−7,−2). Its companion cells in the four partitions identify the factors. The first numeric column uses the reference arc. The second adds cases where one twisted D-cycle meets both marked sheet sets. The third adds cases requiring full connected-component closure in this test.

On the identity cover, the primitive vectors for twist power j are (1,2j) in class b and (2j,1) in class d, up to lift reflections. The two class-c pencils give (1,σ+2εj) and its transpose, where σ=±1 selects the reference diagonal and ε=±1 selects the twist orientation. D147 checked the origin-dependent signs and the physical reachability of every slice over the full period 28. [d147, check 3](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d147-review-crossarcs/review.md)

| Factor and companion cells | Reference | Added by one contact | Added by closure | Remaining |
|---|---:|---:|---:|---:|
| 24, all three companions below | 1,014 | 416 | 292 | 0 |
| 48, (6,1) | 998 | 432 | 292 | 0 |
| 48, (−7,1) | 876 | 411 | 431 | 4 |
| 48, (6,−2) | 876 | 411 | 431 | 4 |
| 96, identity control | 722 | 370 | 614 | 16 |

On the (−7,1) factor the four residuals are marks at (x,0), in the vertical primitive parity, with x-pairs (−5,1), (−5,5), (−3,3), (−1,5). Transposing coordinates gives the other factor's four. D147 supplies legal paths in the specified classes for all 16 residual identity rows. For example, (−5,0) reaches (1,0) in the vertical parity class along primitive direction (−2,5). This one physical witness also settles the corresponding row on every quotient. [Independent residual witnesses](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d147-review-crossarcs/review.md) · [Original pencil checker](cross-factor-arcs.py)

On the identity cover the checker also deletes all incidences at cycles of length other than two before computing components. The surviving graph has maximum degree two. At each interior vertex there is exactly one forward continuation after arrival, so a simple path in it develops to a legal straight segment. The restricted calculation still covers **1,706/1,722 classes and 574/574 physical pairs**. Since the unrestricted calculation covers exactly 1,706, every positive identity-cover row in these pencils has a corner-free witness. The equality concerns existence of a power within a row. In 668 rows, forbidding corner continuation strictly reduces the set of successful powers. Those rows exhibit the legal-lifting issue at a specific slope even though another power succeeds. [d147, check 6](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d147-review-crossarcs/review.md)

## Component bound from Euler’s V − E

Let f_i and z_i be the counts of fixed letters and three-cycles at site i of a sphere factor of degree m. Regular points give the two-cycles. The ramification index sum at i is (m+z_i−f_i)/2. Hence the preimage of an arc between i,j, with m edges and one vertex per endpoint cycle, has at least (f_i+f_j−z_i−z_j)/2 components by Euler's graph inequality. On the degree-24 factor the sites (0,1),(1,0) each have two fixed letters and no triples, so **every** arc between them has at least two components. Pairwise reconnection above holds even across this split. The universal canonical relations guarantee a two-cycle over each site on a proper factor. They supply no mechanism in this count to assign the two marked vertices to the same component. Also, the earlier inequality n≤4r assumes the four-sheet cov4181 portrait. For a general proper factor of outer degree m and inner degree k, the zero charge is k times the number of quotient zeros ≤r, and n=km. Substituting 4 for m would discard the cross itself.

## Status of the proposed proof chain

1. **Reviewed, with scope.** The orthogonal corner-only branch covers real interior endpoints below 22 walls. The proper canonical branch is closed for interior lattice pairs by d64/d67 and the saved replay. The remaining normalized orthogonal lattice-mark problem is BBBB. [Scope and certificates](../README.md)
2. **Reviewed.** d146 excludes proper factors of degrees 2–4 in BBBB. Its arc exclusion on cov4181 needs the distinct singleton images and a corner-only site on the factor. [Corrected statement](exclusion-descent.md)
3. **Open.** Pairwise reconnection on every larger factor remains unproved. D147 verifies the four named factors and gives no general degree bound.
4. **Open independently.** Even a connected quotient arc can lift to a walk meeting a forbidden corner or ending at the wrong physical lift. A primitive sheet action also has no proper intermediate factor to test. The genus-two examples in d140 exhibit one mechanism for separation. They do not classify mechanisms. d142 excludes a common two-image midpoint explanation under its hypotheses. It does not prove lift reachability. [Primitive examples](half-turn-fibers.md) · [Midpoint theorem](two-image-midpoints.md)

The general chain remains open after independent verification of the table. The next theorem worth targeting is simultaneous: in BBBB, if two primitive classes fail for a physical pair, prove that some single arc in the third connects physical lifts with all intermediate vertices regular. That formulation keeps the endpoint and stopping conditions and allows an entire class to fail on pairs already joined in another.
