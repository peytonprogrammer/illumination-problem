# Orthogonal frame normalization and the exact geometric target

Independent scope lemma, Codex01a1a00f. This clarifies the already accepted H/V/C1 geometric proof when "orthogonal" includes a canonical45 room whose perpendicular wall pair is diagonal in the fixed original lattice. If the programme convention is axial rooms only, that narrower convention needs no normalization; no additional optical theorem is asserted here.

The accepted genus dependency explicitly distinguishes a minimal four-copy perpendicular-wall unfolding from the eight-copy case with mixed axial/diagonal directions. Thus an entire orthogonal subcase must not be assumed axial merely from the word "orthogonal."

## 1. A uniform Euclidean similarity preserves the marked problem

An orthogonal canonical45 polygon uses either horizontal/vertical walls or the perpendicular pair of slopes+1,-1. In the latter case take

    F(x,y)=(x+y,x-y),
    F^{-1}(X,Y)=((X+Y)/2,(X-Y)/2).

Its matrix satisfies F^t F=2I. It is an invertible Euclidean similarity, with scale sqrt2 and reversed orientation. It maps the two diagonal directions to horizontal and vertical directions. In particular this is a COMMON similarity of the whole room and actual endpoints, not an anisotropic or piecewise surgery.

Every actual even-even S,T maps to even-even F(S),F(T). Simplicity, disk topology, strict interiority, actual distinctness, corner type and r are unchanged. Straight finite legs, finite-wall interiors, corner avoidance and the specular law are preserved under a Euclidean similarity. More explicitly, reflection in a line conjugates under F to reflection in the image line, because F changes every length by the same factor. Thus an actual target-reaching ray in one room corresponds to an actual target-reaching ray in the other, in both directions.

## 2. Canonical parity of the boundary is retained on return

A diagonal edge of the canonical triangle tiling joins even-even and odd-odd points, hence lies on x+y=2k or x-y=2k. A genuine corner of a purely diagonal orthogonal canonical polygon is the intersection of two such supporting lines. Consequently BOTH coordinates X,Y of its F-image are even integers, including for an original odd-odd corner.

Therefore the normalized axial polygon has every vertex in2Z². The H and V band completions use only existing extreme abscissae and vertex heights, so their new vertices also lie in2Z². An isolated C1 completion merely combines an old vertical support with an old horizontal support; its new corner is likewise even-even. This remains true after any sequence of those geometric reductions.

Applying F^{-1} returns every new vertex to an integer point. Each returned diagonal wall lies on x+y=an even integer or x-y=an even integer, so it is again a finite union of canonical tiling edges. The returned strictly simple Jordan polygon bounds a finite canonical triangle disk. Thus the accepted geometric reduction can also be performed in the diagonal frame and returned to the original class, without half-integer vertices or a change of lattice model.

Actual endpoints return to the LITERAL original S,T because F^{-1}(F(S))=S and likewise for T. No reflected target sheet is substituted. Strict r decrease and the convex base survive the similarity. If an optical transfer theorem is eventually proved in the normalized axial frame, the same similarity transfers it back correctly.

## 3. Limits

This covers only the two pure perpendicular direction pairs. A polygon using both axial and diagonal wall directions has the larger reflection group and is the separate general canonical45 case; the normalization does not make all its walls axial. Nor does it solve the missing optical transfer for axial rooms. The scope lemma only ensures that a coordinate convention does not silently omit a perpendicular-wall family.

The checker geometric-reduction-orthogonal-normalization.py/json verifies the exact matrices, all sign reflection conjugacies, and a prescribed inverse image of the EXISTING L control, including actual marked-coordinate roundtrips and even-intercept wall supports. The universal proof is the preceding algebra/parity argument, not a sampled assertion.
