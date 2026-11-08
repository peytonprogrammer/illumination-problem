# A short reduction for the folded-parity 22-wall minimum

Computer-assisted theorem in the stated normalized class. The new Lemmas1–4 and minimum reduction are accepted by a separate tools-disabled Opus review, conditional on the previously audited inputs1–3. The equality corollary added afterward awaits independent peer review. This does not establish a global minimum among mirror rooms.

## Scope and remaining finite inputs

Fix the canonical tiling by area1/2 right-isosceles triangles with vertices of three kinds: A=2Z^2, mixed parity, and odd-odd. Each triangle has one vertex of each kind and its angles there are pi/4,pi/2,pi/4, respectively. The tiling diagonals lie on x+y even and x-y even. Edge lines through A points are axial or have slope±1; reflection in such lines preserves the tiling and the A parity class. Diagonal reflections may exchange the two mixed-parity cosets; preservation of each of those cosets is neither asserted nor needed. A parity base P is a closed simple polygon made of these triangles, with every non-A lattice point in P an actual boundary corner. Its distinct marks a,b are noncorner A points; they may be smooth boundary points or interior points.

A folded room Q is a closed simple polygon equal to the union of m congruent copies g_i(P) with disjoint interiors. The copy maps agree as a continuous fold f:Q->P, restricting to g_i^(-1) on the i-th copy. Along each common positive-length boundary segment, adjacent copies are mirror images pointwise across its supporting line. Interior physical marks S,T satisfy f(S)=a, f(T)=b. No holes, slits, point contacts in the exterior boundary, or overlaps are permitted.

We use three previously verified inputs:

1. The wall identity

       W_Q = m(W_P-4)+4+E+2b45+4i45 >= m(W_P-4)+4,

   with nonnegative terms as derived in findings.md§2. It permits arbitrary copy-adjacency cycles and shared seam endpoints.
2. No parity room with two interior A marks has W<=21 (the m=1 case, already independently audited).
3. Among parity bases with two distinct noncorner A marks, none has W_P<=8. At W_P=9 there is one base shape, given below, up to a grid isometry. This small classification is computer-assisted: a fresh run of frozen reviewed enum_base.c through W12 has eight W9 listings and no smaller listing. The eight W9 geometries and marks normalize to the stated representative. No fold enumeration is needed in this input.

The prior positive22-wall construction attains the resulting lower bound and is dark by the separately reviewed parity/folding/retracing proof.

## Lemma 1: an interior A mark and another noncorner A mark need at least14 base walls

Let N be the number of canonical triangles and E_A the sum of angles at actual A corners in units of pi/4. Every mixed-parity and odd-odd vertex in P is a genuine corner. Summing triangle angles of these two kinds, then adding A-corner angles, gives

    4(W_P-2)=3N+E_A,     E_A>=0.

Suppose a is interior. Its eight-triangle star is contained in P. At each of its four axial mixed-parity neighbors, the star contains exactly two of the four available pi/2-angle sectors, giving angle pi. Every such vertex must be an actual corner. It cannot have just those two sectors (smooth), or all four (interior); it must have exactly three contiguous sectors. Thus P needs one extra triangle at each of four distinct mixed-parity vertices.

If b is interior, its eight triangles are disjoint from a's eight because a canonical triangle has only one A vertex. Hence N>=16.

If b is smooth boundary, its four-triangle half-star is disjoint from a's star. The half-star is contiguous. For a mixed neighbor v of a, either possible extra triangle there has A vertex2v-a. The four values2v-a=a±2e_i are distinct, so b's half-star can fulfill a requirement at at most one of the four neighbors. It cannot contribute two extra triangles at that neighbor, because that would fill all four sectors and make a forbidden non-A interior point. At least three additional triangles lie outside both stars. Therefore N>=8+4+3=15.

In either case, 4(W_P-2)>=45, so integer W_P>=14. In particular, a base with W_P<=12 and two noncorner A marks has both marks on its boundary.

## Lemma 2: an interiorizable smooth mark must lie on a supporting wall

Normalize its copy to P, and suppose a smooth mark p on wall line l becomes interior in Q. Its incident copy contributes angle pi at p. Every other incident copy maps p to that same base point, hence also contributes angle pi. The finite set of closed copies not containing the lift lies at positive distance from it. A neighborhood is therefore covered by incident copy half-disks only, so exactly one further copy is required and possible, occupying the opposite half-neighborhood. Coherence and mirror gluing force that entire copy to be R_l(P), where R_l reflects pointwise in l.

If l met int(P) anywhere, take a small disk centered at that intersection and contained in int(P). Reflection in l preserves the disk, so it lies in both int(P) and int(R_l(P)), contradicting disjoint copy interiors. Thus l avoids int(P). The interior of a simple polygon is connected, so it lies entirely on one side of l. Accordingly l supports the entire base.

This is a necessary condition only. A supporting wall need not be sufficient for a larger valid assembly.

## Lemma 3: two copies cannot give W_Q<=21

The wall identity forces W_P<=12. Lemma1 therefore puts a,b on the base boundary. Normalize one copy to P. Since both marks need interior lifts, the second copy must be reflection across the line of a's wall and also across the line of b's wall. The coherent fold determines the copy transformation, so these reflection lines agree; call the line l. Lemma2 puts P in one closed half-plane and R_l(P) in the opposite one. Hence their intersection K equals P intersect l: one inclusion follows from the opposite half-planes, and the other because reflection fixes every point of l.

The compact set K is a finite union of closed intervals and possibly isolated points. Each connected component is contractible. Reflection in the wall line preserves the canonical tiling, so the sets form subcomplexes of a common finite subdivision. Euler inclusion-exclusion gives

    1 = chi(Q) = chi(P)+chi(R_l(P))-chi(K) = 2-c,

where c is the number of components of K. Thus c=1, and K is one interval containing both a and b.

Because l avoids int(P), K lies in the boundary of P. The simple Jordan boundary contains the whole interval [a,b]; locally at a point strictly between a and b, its boundary arc is exactly that straight line. Since P lies on one side, the boundary angle there is pi. But the segment between two distinct A lattice points on an axis or diagonal lattice line contains a non-A lattice point. That point would be smooth, contradicting the parity-base condition. Therefore two copies are impossible below22.

This proof also rules out disconnected multiple seams and isolated supplementary contacts; no assumption of a tree is needed.

## Lemma 4: the sole9-wall base cannot interiorize both marks, for any number of copies

A representative boundary is

    (0,0),(1,1),(2,1),(2,3),(1,3),(1,2),(-1,2),(-1,1),(0,1).

Its only noncorner lattice points are a=(0,2) and b=(2,2). The maximal wall containing a is on y=2, but this line meets the polygon interior at (3/2,2). Indeed, the full rectangle [1,2]x[1,3] belongs to P and is symmetric about y=2. The reflection across a's wall overlaps P on an open rectangle. By Lemma2, a cannot acquire an interior lift in any allowed assembly. Isometries transfer this obstruction to every listed9-wall base.

## Conclusion

If W_Q<=21, input3 gives W_P>=9, so the wall inequality forces m<=3.

- m=1 is excluded by input2.
- m=2 is excluded by Lemma3.
- m=3 forces W_P=9 and is excluded by Lemma4.

Therefore every room in this normalized folded-parity class has at least22 walls. The known22-wall room attains the bound. The proof retains a finite base classification through9 and the earlier m=1 exclusion, but replaces all412-base/fold checks in the exclusion step. The independent larger replay remains a cross-check.

## Equality corollary: cycles and shared seam endpoints cannot improve a22-wall minimizer

The same argument gives a structural restriction on equality, without classifying all10-wall bases. No base of8 or fewer walls exists, and the9-wall base cannot interiorize both marks at any copy count. Thus an eligible assembly with at least2 copies has W_P>=10.

Two copies always require at least24 walls: if W_P<=13, Lemma1 puts both marks on the boundary and Lemma3's topological contradiction applies independently of the numerical threshold. Therefore an eligible two-copy assembly needs W_P>=14, so W_Q>=2(14-4)+4=24. With at least4 copies, W_P>=10 gives W_Q>=28.

A22-wall folded-parity room therefore has exactly3 copies: the1-copy case is excluded by the earlier W<=22 parity audit, and the other counts were just excluded. Its base must have W_P=10, and the wall identity forces E=b45=i45=0. With at most3 copies at any point there can also be no interior lift of a90-degree base corner (that needs4 copies). Thus there are no interior seam vertices, and Euler gives exactly2 seam edges. Their connected copy-adjacency graph is a tree. Every seam endpoint is a smooth lift of a90-degree base corner involving exactly2 copies; its seam degree is1, so the four endpoints are distinct.

Consequently any22-wall minimizer in the broader folding class returns to a three-copy tree with distinct convex-right-angle seam endpoints. Both base marks are boundary marks by Lemma1. The two seam walls are distinct, with one mark on each, because one maximal base wall cannot contain two noncorner A marks. Diagonal exterior walls are not excluded by this argument alone. Uniqueness of the attained unmarked22-wall shape remains a finite classification/replay statement, not a consequence of this equality corollary alone.

## Universal two-copy corollary for the next, non-parity class

The same supporting-line/Euler argument does not require parity. In any two-copy coherent reflected double that is a simple polygon, two distinct smooth boundary base marks with interior lifts must lie on the same connected seam interval. Every point of their joining segment has one incident half-disk from each copy and is therefore interior in Q. The straight segment connects the two interior marks with zero reflections.

Thus no such two-copy double can make that pair dark. Any dark two-copy extension of the proposed non-parity-base class must have at least one mark already interior in its base. Ordinary base darkness by itself does not license ignoring trajectories that project to a segment along a base wall. This corollary does not supply an actual non-parity dark-base counterexample; it is a direct geometric restriction on any candidate. It is not included in the first Opus review prompt and awaits live peer review.
