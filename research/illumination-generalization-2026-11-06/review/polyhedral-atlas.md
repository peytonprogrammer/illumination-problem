# Global geometric atlas with unbounded integer deformation parameters

Candidate structural reduction for independent review. It covers the FULL canonical45 geometry and marked-pair quantifiers at W<=21, without k, support, surplus, diameter or interior-A-count bounds. It does not prove illumination on those parameters. The finite structural conclusion and the remaining optical obligation must not be conflated.

## 1. Exact parameters for every marked room

Translate the actual interior A mark S to(0,0); this is an even-even translation and preserves the canonical tiling. Write T=(2u,2v), u,v integers, not both zero. Choose a starting boundary vertex p0=(x0,y0) and the cyclic list of maximal directed walls e_i, 0<=i<W. Each e_i belongs to

    {(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)}.

There are finitely many such lists for3<=W<=21. Require consecutive directions, including the last/first pair, to be noncollinear. Same-direction neighbors would not be maximal; opposite-direction neighbors would retrace and violate strict simplicity. Let positive integer lambda_i be the component length along e_i. Then

    p_i=p0+sum_{j<i} lambda_j e_j,
    sum_i lambda_i e_i=0.

These are two closure equations in W+4 integer variables (x0,y0,lambda_0,...,lambda_{W-1},u,v). Directions in any nonempty valid list span the plane, so closure has rank2. The real parameter dimension is therefore at most W+2<=23. We do not bound any variable or enumerate its values.

Diagonal walls require the extra congruence p_i.x+p_i.y=0 mod2 at their start. The end has the same parity automatically. Integer axial walls are always tiling-edge unions; the even-intercept diagonal condition is exactly the diagonal tiling condition. Thus these finitely many linear mod2 congruences retain the canonical45 presentation, rather than merely its geometric directions.

## 2. A finite rational-linear sign arrangement captures ALL geometry

For each fixed direction list, include the signs of these homogeneous integer-linear forms:

1. p_i.x-p_j.x and p_i.y-p_j.y, for all ordered vertex pairs i,j.
2. det(e_i,p_j-p_i), for all ordered pairs i,j.
3. p_i.x-Q.x, p_i.y-Q.y and det(e_i,Q-p_i), for every vertex i and each Q in {S,T}.
4. Every lambda_i and u,v.

There are at most3W^2+7W+2 forms, or1472 atW21. Some are zero or redundant; overcounting is harmless. A sign assignment is in {-1,0,+1} for EVERY form. Zero signs are retained as equations; no general-position hypothesis is imposed. Closure is kept separately as two equations.

Each nonempty sign cell is a relatively open rational polyhedral cone. On it the following predicates are CONSTANT:

* Strict polygon simplicity. For any two nonadjacent segments, the four orientation signs come from item2, since multiplying a directed primitive edge by its positive length does not change a sign. Proper crossing is determined by those four signs. A collinear endpoint lies on the finite other segment exactly when its two coordinate differences lie in the corresponding closed intervals, decided by item1. This also detects parallel overlap, nonadjacent vertex touching and repeated vertices. Adjacent edges cannot overlap because their fixed directions are noncollinear. Therefore the boundary is a Jordan polygon exactly in the selected simple cells. Such a closed polygon bounds a disk, with no separate hidden hole or slit.
* Actual mark membership. Boundary membership uses item3 orientation zeros and its coordinate comparisons with both endpoints. If the mark is not on any boundary segment, its winding number follows from upward/downward ray crossing: p_i.y<=Q.y<p_{i+1}.y with positive orientation contributes+1, and the reversed half-open condition with negative orientation contributes-1. All comparisons are sign data. The half-open convention includes marks aligned with a corner's horizontal line without double counting. Nonzero winding gives the actual interior of a simple polygon.
* Mark distinctness and wall maximality. Distinctness is u,v not both zero, recorded in item4; wall lengths stay positive and their noncollinear directions fixed.

Discard exactly the cells failing any required predicate. Each remaining cone together with the integer variables and diagonal parity congruences is EXACTLY a family of eligible marked canonical45 disks. The finitely many direction lists and retained cells cover EVERY such input and both orientations; choosing one of many possible starting vertices merely duplicates representations.

Conversely a lattice point in a retained cell gives the required polygon, not just necessary conditions. Its boundary lies on the canonical triangulation's edges. Each triangle's open interior is wholly inside or outside that boundary, so the closed disk is the finite union of its inside triangles. Interior even-even marks are actual interior A stars. Thus neither tile realizability nor actual endpoint membership is delegated to an optical assumption.

## 3. Finite bases and finitely many integer growth directions

The integer geometry in each cell admits a further finite affine-monoid representation, still with UNBOUNDED coefficients. For each integer-linear strict positive form f, replace f>0 by f>=1; for a negative form use f<=-1, and preserve zero forms as equations. This changes no integer point. Split into the finitely many mod2 residue vectors compatible with the diagonal congruences, then substitute the parameter vector x=r+2z, z integral. The remaining condition is a closed rational polyhedron P_r in z.

The standard rational-polyhedron representation of integer points applies; see [Kaibel, Basic Polyhedral Theory, Theorems8,10,20](https://arxiv.org/pdf/1001.2161). In particular there are finite integer sets B,R with

    P_r intersect Z^d = union_{b in B} { b+sum_j n_j r_j : n_j>=0 integer }.

For completeness, existence also follows directly from the rational Weyl–Minkowski form. Write P_r=conv(V)+cone(R), choosing each ray integer by positive scaling and including both signs of lineality generators if needed. For any integer x=v+sum_j theta_j r_j, subtract sum_j floor(theta_j)r_j. Its residual b is integer, remains in P_r, and lies in the bounded set conv(V)+sum_j[0,1]r_j. Only finitely many integer residuals occur. Conversely every such b plus nonnegative integer ray increments stays in P_r because all rays are recession directions. This proves the claimed finite-module structure without assuming the cone itself is pointed. Restoring x=r+2z preserves every congruence and the exact geometry predicates.

Consequently ALL eligible canonical45 marked rooms atW<=21 have a finite list of base parameter vectors and finite lists of integer geometric growth directions. A growth direction itself may represent a degenerate polygon; its asserted property is that adding it to any associated base representation preserves the selected strict geometry cell. It is not asserted to be a corridor stretch or an optical equivalence. T can move according to its recorded parameter coordinates; S stays fixed. Every resulting mark is an actual interior mark of its resulting room, but there is NO automatic trajectory transfer between different parameter values.

The finite atlas and its bases/generators have not been enumerated here, and their possible size is enormous. No practical small case list, bound on k, lattice diameter or reflection count follows. The coefficients n_j remain arbitrary nonnegative integers. The structural theorem is an application of standard polyhedral theory.

## 4. Compact primitive arithmetic escape defeats a geometric-only reduction

For every even integer n>=2 take the six-wall L polygon with cycle

    (0,0),(4n+1,0),(4n+1,2n),(2n,2n),(2n,4n),(0,4n),
    S=(n,n), T=(n,3n).

It is canonical45, strictly simple and contains both distinct even-even marks in its interior. The coordinate-span gcd is gcd(4n+1,2n)=1, so it is not a redundant integer dilation of a smaller integer presentation in this frame. All straight-wall lengths are at least2n.

The number of closed-region integer points is(2n+1)(6n+2), from two closed rectangles and their overlap. The closed-region A count is(n+1)(3n+1). Exactly two genuine corners are non-A, so

    k=(2n+1)(6n+2)-(n+1)(3n+1)-2=9n^2+6n-1.

Divide geometry and marks by n. The polygons converge to the strictly simple L with widths4,2 and heights2,4; every limiting wall is positive. Marks stay EXACTLY at(1,1),(1,3), with normalized distance at least1 from the boundary and distance2 from each other. Aspect ratios, perimeter and all nonadjacent-wall clearances remain nondegenerate. Yet k tends to infinity and the original integer presentations are primitive.

These rooms illuminate by the accepted L6 theorem. They refute the STRUCTURAL inference that unbounded primitive k must produce a long neck, shrinking mouth, endpoint collision or degenerating normalized geometry. A global proof based on geometric degeneration alone would omit this valid source of unbounded arithmetic complexity. The accepted long-neck theorem is not contradicted.

## 5. Geometry cells do not fix optical words

One fixed cell already contains changes in a prescribed reflection word. Take the rectangle [-4,8]x[-4,4], S=(0,0), and T_X=(X,-2), X=2,4,6. All three are genuine A pairs in the SAME direction/sign cell of the atlas: only the magnitude of a strictly positive target x coordinate changes.

For the word floor-then-right, unfold T_X to(16-X,-6). The floor hit has x=(2/3)(16-X). At X=6 the legal physical path is

    (0,0)->(20/3,-4)->(8,-16/5)->(6,-2).

At X=4 the same prescribed word hits the actual corner(8,-4); at X=2 the right wall is reached first, changing the word. All three pairs illuminate directly in the convex rectangle. This is an exact warning about word uniformity, not a dark-pair construction.

The own prescribed checker verifies sign-cell equality, the corner equality, the legal two-reflection path, parallel-overlap and bow-tie rejection, an interior mark on a ledge's LINE EXTENSION, and exact k counts at n=2,4,10. These controls support the hand proof and do not enumerate the global atlas or prove illumination by sampling.

## 6. Exact remaining optical implication

The full goal is now still equivalent to illumination for every allowed integer parameter vector in these finitely many geometric families. To turn this structural atlas into a general proof one needs an additional proved optical statement, for example a darkness-preserving descent along enough generators plus independently resolved bases, or a universal actual-pair connection construction on every family. Neither is established here. Finite geometric generators are not automatically finite optical generators. Existing affine/containment obstructions and the same-cell word example prohibit treating that transfer as automatic.

The atlas is more global than the existing special-case neck theorems, but it does NOT remove their remaining arithmetic phase or coupled-growth obligations. Diagonal walls and every interior A count are covered geometrically; their actual illumination remains OPEN. Arbitrary real polygons with other directions, arbitrary real-wall rationalization and universal22minimality are not supplied by this arithmetic atlas.
