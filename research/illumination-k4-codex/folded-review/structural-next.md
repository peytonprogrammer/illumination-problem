# Next structural target

Fixed-base census (not new geometry search):

- W=9, noncorner A marks=2, interior A marks=0: 8 listings.
- W=10, noncorner A marks=2, interior A marks=0: 52 listings.
- W=11, noncorner A marks=2, interior A marks=0: 128 listings.
- W=12, noncorner A marks=2, interior A marks=0: 208 listings.
- W=12, noncorner A marks=3, interior A marks=0: 16 listings.

Unmarked base shapes under D4 and arbitrary translations: {12: 28, 10: 7, 11: 16, 9: 1}. These are geometric shapes, not parity-preserving marked equivalence classes.

A possible computation-free replacement would exclude the two-copy case by proving that a low-wall base cannot provide an interior mark plus a distinct mark on the gluing wall; if both marks must be boundary points, a single maximal base wall cannot contain two A marks. Multiple disconnected seams between two disk copies create a hole and are excluded by simplicity. For three copies below22, the wall formula forces W_P=9, leaving the small9-wall base classification. This is a research target, not a proved general reduction beyond the verified finite census.

## A shorter reduction, for independent peer review

### Lemma A: low-wall two-mark bases have no interior mark

Use canonical triangles of area1/2, each with exactly one even-even A vertex, one mixed-parity vertex and one odd-odd vertex. Suppose a parity base has an interior A mark a and another distinct noncorner A mark b.

The full star at a contains8 triangles. Its four axial mixed-parity neighbors a+(1,0), a+(-1,0), a+(0,1), a+(0,-1) each already have two incident triangles, forming angle pi. They cannot remain smooth or become interior, because every non-A lattice point must be a true boundary corner. Thus each must receive exactly one more triangle, making angle3pi/2. Each additional triangle has exactly one mixed-parity vertex, so these are four distinct requirements.

If b is interior its8-triangle star is disjoint from a's star (every triangle has a unique A vertex), so N>=16. If b is smooth boundary, its star contains4 triangles, again disjoint from a's. Distinct even-even vertices have at most one common axial mixed-parity neighbor: a common neighbor would force b-a to be one of (±2,0),(0,±2). Even at that shared neighbor b's star can satisfy at most one required extra triangle; satisfying two would make that non-A vertex interior. Therefore at least3 of the four requirements remain outside both stars, and N>=8+4+3=15.

For a parity base the angle ledger gives3N+E_A=4(W_P-2), with E_A>=0, exactly as in the earlier parity-area proof. Hence W_P>=ceil(2+45/4)=14. In particular, every two-mark parity base with W_P<=12 has both marks on the boundary. The fixed-base census independently agrees, but is not needed for this lemma.

### Lemma B: an interiorizable smooth mark needs a supporting wall

Let a smooth base mark lie inside a maximal wall on line l. To make its lift an interior point in a coherent nonoverlapping reflected-copy assembly, two pi-angle sectors must meet there. The other copy is the reflection in l of the original copy. If l crossed the interior of P anywhere else, a small disk centered at such a crossing would lie in both P and its reflection, contradicting disjoint interiors. Since P is connected, this is equivalent to P lying entirely on one side of l. Thus l must be a supporting line of the whole base.

### Two copies cannot suffice below22

The wall bound gives W_P<=12, hence both marks are boundary marks by Lemma A. A union of two disk copies that is itself a disk can glue along only one connected wall interval: two disjoint seam intervals create a hole (Euler), and a coherent reflection cannot turn onto a second noncollinear seam line. Both marks would need to lie on that same maximal wall. A maximal parity-base wall contains at most one noncorner A point: between two such points there is a non-A lattice point, which must instead be a true corner. Contradiction.

### Three copies: the9-wall base cannot work

The already verified base classification gives W_P>=9, and the wall bound at W_Q<=21 forces W_P=9 for three copies. The8 saved listings have one unmarked base shape under D4 and integer translations. A representative boundary is

    (0,0),(1,1),(2,1),(2,3),(1,3),(1,2),(-1,2),(-1,1),(0,1).

Its only noncorner lattice points are a=(0,2), b=(2,2). The line y=2 of a's wall crosses the interior of P at (3/2,2), inside the rectangular arm[1,2]x[1,3]. Lemma B says a cannot be interiorized by any coherent nonoverlapping copy assembly. Thus no three-copy room with both marked lifts exists, independently of the fold enumeration.

### Remaining finite input

This short route needs only the already rebuilt base classification through W9 (none atW<=8, one shape atW9), plus the earlier accepted m=1 parity exclusion. It no longer needs the412-base census through W12 or2,096-assembly replay for the exclusion. Those remain independent controls. Lemmas A and B and the two-copy topology argument await independent Opus review; do not report this shortened proof as peer-accepted yet.

## Completed write-up

The precise proof, including Euler inclusion-exclusion for two copies, is now `short-proof.md`. A separate Opus reviewer accepted Lemmas1–4 conditional on the previously audited inputs; clarity fixes are incorporated. The equality structure and universal two-copy corollaries were added afterward and await peer review. The reviewer incorrectly said diagonal reflections preserve every parity coset; the final text correctly asserts preservation of A only.
