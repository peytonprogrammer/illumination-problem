# Arc connectivity on a five-sheet pillowcase factor

**Result for review.** Let Q→Y→B be a proper pillowcase factor of a normalized orthogonal BBBB room. Assume Y has outer degree five. Fix two distinct same-class interior marks upstairs, over a, and a primitive class whose first step lands over d. Some arc from a to d has its two marked images in the same component of its full preimage, for some choice of the physical lifts, **unless both marks separately collapse to single points on Y**. In the remaining cases at least one collapsed mark is over a singleton pole and the inner degree is at least four. This concerns connected components with arbitrary vertex continuations allowed. It is not a claim of a legal segment.

**Corrections to the proposed hypotheses.** A regular point over a pillowcase pole is a two-cycle. A fixed letter is a pole, and a (3,2) permutation has no fixed letter. If the outer degree is m, the inner degree k, and Y has z zeros, the general equations are n=mk and r≥kz. The earlier bound n≤4r used m=4 and z≥1. It gives no bound of that form in arbitrary degree. The genus of the underlying Y is already zero; it is its cover degree that remains uncontrolled.

## Cycle types and arc convention

Use U for a transposition on five letters, V for a double transposition, Z for type (3,2). The two possible lists around the four poles are U,U,Z,Z and U,V,V,Z, as follows from the sphere ramification sum of eight and the absolute-period condition. The area bounds are 20 and 40 respectively when r≤8. [Proof of the classification](auxiliary-exclusion.md)

Take peripheral permutations in cyclic order with rightmost-first composition and product identity. For a selected arc joining two poles with local permutations A,D in an adapted basis, the components of its full preimage are the orbits of ⟨A,D⟩. A twist around two adjacent peripheral loops with permutations D,E conjugates both by h=DE (or use the inverse twist); a tail outside the twisting disk stays fixed. Thus powers of the twist replace D by hʲDh⁻ʲ while keeping A and its endpoint labels fixed. These are simple arcs of the same prescribed parity. Cyclic orders below can be chosen when setting up tails, before the argument starts.

## A connected arc whenever one site has type Z

Call that local permutation D, and its two-letter orbit P. If A does not preserve P then ⟨A,D⟩ is transitive. Otherwise use cyclic order A,D,E,F. Neither E nor F preserves P: the product relation would then force the other to preserve it as well, contradicting transitivity of the cover.

If one of the complementary sites is U, take it for E. It swaps one letter of P with one of the other three. Therefore h=DE is a five-cycle, since that transposition joins the two cycles of D. If A preserved every translate hʲP then A would be the identity: the five translates form the edges of a pentagon on five letters, and fixing every edge setwise fixes every vertex. Choose a translate that A does not preserve. The corresponding twisted arc has connected preimage.

The only case here without a complementary U has A of type U and E,F of type V. If A swaps the two letters of P, AD is a three-cycle with fixed set P. Since EF=(AD)⁻¹ and E,F are involutions, each normalizes ⟨AD⟩ and preserves P. This contradicts the preceding paragraph. Otherwise, after relabeling, D=(123)(45), P={4,5}, and A=(12). Now AD=(23)(45). The involutions E,F commute because their product has order two, so both fix the unique fixed letter 1 of AD. On the other four letters they are the two remaining double transpositions. Exchanging labels 4 and 5 if necessary gives E=(24)(35). Then DE sends P to {1,3}, which A does not preserve. One twist suffices. Connectivity is symmetric in the two poles; the proof applies when the Z site is at either end.

## The five-cycle gives connecting arcs for individual marks too

Whenever U and Z are paired, the connected arc just proved has boundary monodromy a five-cycle h: the transposition must bridge the two cycles of Z. Take a narrow closed disk around this arc in the base sphere. Over its boundary the lift is one circle. The complementary disk also has connected preimage, since every component has boundary and there is just one circle. Equivalently its two peripheral permutations have product h⁻¹, already transitive. This settles V,V in U,V,V,Z.

For the remaining pairs of sites choose a disk separating A from D whose boundary has that same five-cycle property. For U,U in U,U,Z,Z put one U and one Z on each side. For U,V in U,V,V,Z put U,Z on one side and V,V on the other. Use the connected U,Z arc for that split. Keep the source side fixed and twist the other disk as a unit. The permutations of the target site now include hʲDh⁻ʲ, j=0,…,4. The source labels stay fixed throughout. This gives five arcs by construction and requires no search.

Index the five letters cyclically along h.

* A U on the U,Z side swaps letters at cyclic distance two, because multiplying the five-cycle by this swap splits it into cycles of lengths two and three. Its translates are the edges of a pentagon (the distance-two pentagon).
* A V on the V,V side is a reflection of that pentagon: it conjugates the product of the two involutions to its inverse. The five translates are all five reflections. Every pair of distinct letters is exchanged by one of them, since in ℤ/5 the reflection sending i to j is x↦i+j−x.

Thus if A=U and D=V, **every** pair of A-images connects in at least one arc. Two ordered cases remain:

| Source and first-step site | Pairs connected by the five arcs | Possible missing pairs |
|---|---|---|
| U,U | Identify the ends of A's own edge in the distance-two pentagon. The other four edges give a four-cycle on the four A-images. | The two opposite pairs of the four-cycle. |
| V,U | Fold the distance-two pentagon by the source reflection A. Its vertex orbits are the fixed vertex and two reflected pairs. Its edges connect these as a path of three vertices, with a loop at the far end. | The fixed vertex paired with the far reflected pair. |

The edges listed are single-arc witnesses: for each one some translated D swaps its endpoint letters. The argument never concatenates edges from different arcs. Other arcs may connect even the pairs listed as possibly missing.

In each row a given A-image has at most one distinct missing partner. Hence separation of two sets of physical images throughout every arc requires each set to be a singleton (coincident images already share a component). Each possibly missing pair contains at least one fixed-letter pole of A: type U has only one regular image, and in the V,U row the fixed vertex itself is a pole. For an interior mark to have both of its distinct Q-lifts at that same pole downstairs consumes at least four sheets of the inner cover: each regular Q-lift has local degree two over the pole. Therefore k≥4. In U,U,Z,Z one also has 2k≤8, so the residue has k=4 and n=20. In U,V,V,Z it has 4≤k≤8 and n∈{20,25,30,35,40}. The area-20 illumination census settles physical existence of some legal shot in its scope. It does not certify a specified primitive class. These are necessary conditions for a five-sheet failure; existence of one has not been shown.

## Reduction ledger

| Link toward the wall theorem | Status and exact scope |
|---|---|
| A physical corner-only parity at W≤20 | Reviewed computer-assisted closure for all areas and all distinct real interior marks in strictly simple orthogonal lattice rooms. [Q-class theorem](../twenty/README.md) · [d102 replay](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d102-qclass-replay/review.md) |
| A proper canonical factor, with same-class interior lattice marks | Reviewed d64 classification and illumination checks. The project separately records a replay for different-parity lattice marks. This link alone does not cover arbitrary real marks. [d67](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d67-review-d64/review.md) · [Scope and further replay](../README.md) |
| BBBB, outer degrees two through four | Excluded by the primitive absolute torus argument in the note submitted for d146 review. Cov4181's four-sheet separator uses a corner-only fiber elsewhere. [d146 submission](exclusion-descent.md) |
| BBBB, outer degree five | Partial and unreviewed here. The two possible collapsed-image cases above remain for the every-class statement. Higher degrees remain open. |
| From a connected arc preimage to a legal path for prescribed physical endpoints | Open in general. Connectivity can use a singular continuation; even a legal downstairs segment induces a specific matching between its endpoint fibers. A connected arc alone supplies neither corner avoidance nor the required matching. [Fiber transport](fiber-transport.md) |
| Primitive sheet monodromy, no proper factor | Open. D140 constructs symmetric examples; it gives no necessity theorem that primitive exclusions require symmetry. D142 rules out one common-quotient midpoint mechanism and does not rule out every primitive exclusion. [d140 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d140-review-halfturn/review.md) · [d142 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d142-review-twoimg/review.md) |

The chain has mathematical gaps even if the new five-sheet result passes review. The narrower target suggested by the calculation is to decide whether both interior marks can collapse to the missing opposite pair **in a physically realizable normalized BBBB factor**, or whether another arc connects that pair. This avoids asking for transitivity where it is impossible: two U permutations on five letters cannot generate a transitive group in any basis. No new room, ray, direction or reflection-word discovery search was run.
