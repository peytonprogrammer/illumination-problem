# From ordinary corner rank to signed spanning by cylinder mixing

[done] Conditional rank-to-positive-span theorem accepted in independent tools-disabled Opus core and focused optical reviews. Integrality, fixed-direction gauge, component, local-sector and physical-sign clarifications incorporated.
[done] Exact mixing-matrix checks on 34 frozen surfaces and four prescribed controls.
[waiting on Claude] Independent live proof challenge and copied-script replay.

## Result and what remains open

Suppose P is a compact strictly simple polygonal disk which is a finite union of canonical A-B-C grid triangles and has no interior B/C lattice points. Fix two distinct interior marks S,T in the even-even lattice. This is precisely the raw parity-room hypothesis needed here (allowing additional smooth boundary lattice points for the alignment part). The independently reviewed axis-alignment theorem in `axis-alignment.md` therefore applies. Fix all physical wall directions in the original horizontal/vertical/diagonal frame and vary only their supporting offsets and the marks, with constant cyclic wall order and strictly simple geometry. Suppose finitely many admissible one-corner midpoint event rows from the chosen source-lift component span the FULL PHYSICAL ROOM deformation quotient dual in the ordinary linear sense. The quotient removes only actual family symmetries: translations and uniform scaling in the D4 case, or the additional compatible axis scaling in orthogonal families. Global rotation and wall-angle variation are not allowed. Then their images under the two axis multitwists contain a finite positively spanning family.

Thus, in this room class, **ordinary rank is sufficient for signed spanning after enlarging to affine orbits**. The proof does not assume the original rows positively span, nor that their individual twist slopes already have full rank. No theorem here says ordinary rank holds for every parity room. That becomes the remaining rigidity premise.

The argument below uses only finite-dimensional relative homology and the elementary maximum principle for a connected stochastic matrix. It does not use a growth estimate or Lyapunov-exponent theorem.

## 1. Setup

Choose the connected square-tiled unfolding component X containing the source lift. If the formal eight-copy unfolding is disconnected, all seed paths from that lift stay in this component; the construction and argument are componentwise. Let Z be the finite marked set consisting of every lifted physical polygon vertex and every endpoint lift of the seed events. Z is distinct notation from lattice parity class A and the chord vector A used locally below. Every physical polygon vertex is an integer grid point, and the two marks are even-even integer points by the stated hypothesis. Their lifts are therefore vertices of the unit-square cellulation. Thus every point of Z lies on both row- and column-annulus boundaries, and the integral shears fix Z pointwise; no endpoint lies in an annulus interior. There are no half-grid endpoints or partial annulus crossing terms here. Use the unit-height horizontal row annuli and unit-width vertical column annuli of the square cellulation; including artificial boundaries at regular grid vertices is allowed. Denote their oriented cores by

    h_i, i=1,...,H, oriented rightward,
    v_j, j=1,...,V, oriented upward.

Let E_ij count squares at the intersection of row i and column j. The horizontal widths and vertical lengths are

    l_i=sum_j E_ij > 0,    m_j=sum_i E_ij > 0.

Choose positive integers a,b divisible by all l_i,m_j respectively. The row and column shear maps fix grid vertices and have derivatives

    P_h=Id+L_h,  L_h(x,y)=(a y,0),
    P_v=Id+L_v,  L_v(x,y)=(0,b x).

Their actions on M=H1(X,Z;R) are Id+N_h and Id+N_v, with

    N_h z = sum_i (a/l_i) int_h(z,h_i) h_i,
    N_v z = sum_j (b/m_j) int_v(z,v_j) v_j.

Here int_h counts upward crossings of the rightward h_i core; int_v counts rightward crossings of the upward v_j core. Both agree with the positive shear convention. If algebraic intersection is defined in the order (path,core), int_h is its negative for a rightward horizontal core, while int_v has its usual sign for an upward vertical core. The formulas below use the explicitly defined crossing counts, not an implicit common intersection sign. In particular,

    N_h v_j = sum_i (a/l_i) E_ij h_i,
    N_v h_k = sum_j (b/m_j) E_kj v_j.

Since each twist fixes its own cores, N_h^2=N_v^2=0. Absolute holonomy satisfies hol N_h=L_h hol and hol N_v=L_v hol, on relative as well as absolute classes.

Let M0=ker(hol:M->R^2). It is invariant under both N operators. Fix an allowed polygon deformation delta and write

    Q(z)=delta hol_delta(z),    Q_x,Q_y its components.

Smooth boundary lattice points introduced by the cellulation are subdivisions of maximal physical walls, not independent polygon vertices or wall-offset parameters. Both subedges inherit the same supporting line and offset; moving them independently is not allowed. They may optionally be marked, at the cost of also requiring the seed interiors to avoid those extra marked points. No such enlargement is necessary here.

The fixed-wall-direction family has translation-surface unfoldings with constant topological gluing and fixed linear reflection parts. Its Gauss-Manin period differential Q is consequently a linear map on the same relative-homology space M; moving marked points does not alter derivatives of absolute periods. Each unit row core is an absolute class, homologous to its containing maximal-cylinder core. The exact period identity in `axis-alignment.md` Section 4, applied to each unit row/column core on the chosen connected component, therefore gives

    Q_y N_h=0,    Q_x N_v=0                  (A)

on all M, because the twist increments are sums of the corresponding axis cores.

## 2. Nonnegative orbit rows force intertwining on their class span

For each seed event, gamma1 and gamma2 have equal nonzero developed displacement w=(p,q), and eta=gamma2-gamma1 belongs to M0. Form all its images under the group generated by the two orientation-preserving shears. They remain straight midpoint events with the same labeled endpoints and intrinsic admissible side. Omit image directions parallel to physical walls when interpreting event inequalities. There is no length or minimality bound.

Let K be the real span of all these orbit classes eta, including algebraic images at any omitted wall-parallel directions. It is finite-dimensional, is contained in M0, and is invariant under N_h,N_v and both shear maps.

Suppose that **every admissible orbit-event row is nonnegative on delta**. For any orbit event with q!=0, its horizontal powers have rows

    g_h,n(delta)=g_0(delta)+n sigma q[Q_x(N_h eta)-a Q_y(eta)].

Only finitely many integer powers can be wall-parallel, and arbitrarily large powers of either sign remain admissible. Nonnegativity in both directions forces

    Q_x(N_h eta)=a Q_y(eta).                 (H)

If q=0, then p!=0. Apply vertical powers to the event. For every nonzero integer k except finitely many excluded powers, its half-displacement has q_k=k b p!=0, and its class is eta+k N_v eta. Equation(H) holds on each of these classes. Its left side minus its right side is linear in k, so vanishing for infinitely many k implies vanishing of the constant term too. Thus(H) also holds on eta.

The same argument, exchanging the roles, gives

    Q_y(N_v eta)=b Q_x(eta).                 (V)

on every orbit generator, and hence throughout K. Together with(A), these are exactly

    Q N_h=L_h Q,    Q N_v=L_v Q on K.        (I)

This step avoids assuming a physical wall-sector label is fixed. The side is intrinsic angular sidedness on the unfolded surface. Orientation-preserving affine derivatives preserve it. At omitted directions only the algebraic class is retained, and the identities are recovered from nonparallel powers as above.

## 3. The cylinder product has a unique top mode

Let C:R^H->M send the ith standard basis vector to h_i. The operator N_h N_v factors through the horizontal core span, and

    N_h N_v C = C T,
    T = D_h E D_v E^T,
    D_h=diag(a/l_i), D_v=diag(b/m_j).

Divide by ab and write

    B=T/(ab)=diag(1/l_i) E diag(1/m_j) E^T.

B has nonnegative entries, row sums1, and positive diagonal entries. Its graph is connected: the bipartite graph of rows and columns, with one incidence per square, is connected whenever the origami is connected. Moving to the right stays in the same horizontal row and moving up stays in the same vertical column, so a disconnected incidence graph would disconnect the entire square adjacency graph. Two horizontal rows are adjacent in B whenever they share a vertical column. Thus B is irreducible.

The equation Bx=x has only constant solutions. For a real solution choose a maximum entry. A convex average can equal that maximum only if all its neighbors attain the same maximum. Connectivity propagates equality to all entries. The complex case follows by real and imaginary parts. The same eigenvalue has no nontrivial Jordan block: every B^n is row stochastic with operator norm at most1 in the sup norm, whereas a generalized eigenvector at eigenvalue1 would grow polynomially. Therefore1 is algebraically simple.

Consequently T has a single algebraically simple eigenvalue ab, with eigenvector(1,...,1).

Relations among the h_i do not spoil this conclusion. Ker C is T-invariant, so T induces the operator N_h N_v on im C. The positive core sum

    c_plus=sum_i h_i

is nonzero because hol_x(c_plus)=sum_i l_i, the number of squares, is positive. The unique ab eigenmode therefore survives the quotient by ker C, and it remains algebraically simple there. Since N_h N_v maps all M into im C, every nonzero generalized eigenmode already lies in im C. Hence the ab eigenvalue on M is algebraically simple too, with eigenspace R c_plus.

Crucially, c_plus is not in M0. The restriction of N_h N_v to M0 therefore has **no eigenvalue ab**. This remains true on its invariant subspace K.

## 4. Intertwining kills all zero-period event drift

From(I), on K,

    Q_x N_h N_v = ab Q_x.

The operator N_h N_v-ab Id is invertible on K, by Section 3. Thus Q_x=0 on K. Equation(H), and invariance of K under N_h, then imply Q_y=0 on K as well.

Therefore Q(eta)=0 for every seed event. Its base signed row

    g_e(delta)=-sigma det(w,Q(eta))

vanishes. If the seed rows have ordinary full quotient rank, delta is a symmetry direction.

Taking the contrapositive, every nonsymmetry deformation has a negative admissible orbit-event row. Compactness of the unit sphere in a fixed deformation gauge extracts finitely many orbit rows with that property. Their positive hull is the full quotient dual, equivalently0 lies in the interior of their convex hull. They therefore admit a full-rank positive stress; strictly positive weights on every selected row can be obtained by averaging zero balances containing each row.

This proves the claimed ordinary-rank-to-positive-span reduction, using the independently reviewed alignment theorem and the explicit admissibility proposition below. The compactness gauge is the same fixed-direction chart used for alignment. Its actual symmetry directions act on all periods by one common linear map (translations act trivially), so every zero-period event row vanishes on them.

## Full orbit-module rigidity corollary

The strongest sufficient rank condition in this proof concerns K itself, not just the original seed classes. Section 2 defines K as the FULL two-shear orbit span, including the algebraic wall-parallel images. Its identities are recovered using arbitrarily large nonparallel powers and, for an axis exception, vertical-then-horizontal or horizontal-then-vertical powers. Section 4 therefore proves Q(K)=0 from nonnegativity of all admissible orbit rows, before invoking any original-seed rank premise.

It is consequently sufficient that the map delta -> Q_delta restricted to K have kernel equal to the family symmetries. This is weaker than requiring the original seed vector defects alone to have full quotient rank. K can contain additional independent core-period relations generated by the twists. `corner-rigidity.md` and `seed-module.py` give a fixed nine-seed example where the original vector rank is18 but the orbit-module vector rank is26. The existence of a finite positive-spanning orbit family then follows from the same contrapositive/compactness proof.

## Immediate vector-relation corollary

The ordinary scalar-row rank hypothesis is sufficient but stronger than needed. It is enough that the vector-valued seed defects detect every nonsymmetry variation:

    Q_delta(eta_i)=0 for all selected i  ==>  delta is a family symmetry.

Indeed, the proof of Section 4 already makes both components of Q vanish on every seed class, so this weaker injectivity premise gives the same contradiction. In coordinates it asks for full quotient rank of the matrix formed from the two component derivatives of every seed defect, rather than just the one signed determinant row per event. Ordinary full scalar-row rank implies this vector injectivity; the converse need not hold.

This is an immediate consequence of the proof, not a new optical assumption. It connects the remaining task to the earlier zero-period-relation rigidity theorem: one must show that actual admissible corner-event defects detect every nonsimilarity period/mark drift. That geometric realization step is still open.

## What this changes

The earlier fixed-room calculation checked full rank of a specific finite set of twist slopes. This theorem would replace the universal version of that difficult slope-rank target by ordinary full rank of admissible seed rows. The seed family need not already have a positive balance, and no particular eight-corner-plus-one-diagonal pattern is assumed.

Still open: proving ordinary full quotient rank for **every** raw parity room, constructing enough admissible one-corner seed events with their physical endpoint labels, and the non-parity/degeneration parts of the unrestricted minimum problem. The conclusion does not claim those steps are complete.


## 5. Admissible intrinsic corner events and the physical inequality

This section supplies the optical hypothesis used above. It is local and places no bound on the event length or word.

**Definition.** A one-corner midpoint event is a concatenation alpha*beta on the unfolded surface X with the following properties:

1. Alpha runs from a chosen lift s to a lift c of a forbidden polygon vertex; beta runs from c to a lift t of the physical target. Their interiors avoid every lift of every polygon vertex, and the endpoint marks s,t are distinct regular points. No other condition on an embedded or immersed region is used.
2. Both segments are straight in their translation charts, with the same developed displacement w!=0. Thus c is the midpoint of the developed chord.
3. In a sufficiently small cone neighborhood of c, the incoming backward ray and outgoing ray bound an embedded sector of total angle pi on the selected intrinsic side sigma. This is the side into which an infinitesimal angular rotation w+epsilon sigma Jw approaches and bypasses the corner. It is not a physical incident-wall-side label.
4. The developed direction is not parallel to any of the finitely many physical wall directions in any unfolding copy, so all noncorner wall contacts are isolated transverse wall-interior hits.

These are exactly the regularity and selected-side conditions needed for the previous infinitesimal event construction. The paths may intersect themselves or revisit physical points away from forbidden vertices. Such intersections do not invalidate a billiard path. If an endpoint mark occurs earlier along a connection, that already illuminates the pair; forbidding earlier mark visits is not needed for the implication below.

**Local opening proposition.** In the fixed-direction family, develop the two event halves along their labeled copy chain. Write A=T_image-S_image and C=C_image-S_image, so at the base A=2 w and C=w. Put

    f(delta)=sigma det(A(delta),C(delta)).

For sufficiently small variations, f<0 implies a legal physical source-to-target billiard connection near the event. In particular, f'(0)<0 along a deformation ray implies illumination for sufficiently small positive parameters.

**Proof.** First freeze the base geometry, put the developed corner at0, and the two endpoints at-w and+w. For an oriented chord in direction w, det(A,C) measures twice the signed displacement of the corner to the chord's left, up to a positive scale. Multiplication by sigma selects the intrinsic angular side. Thus f<0 says that the chord passes on side sigma of the corner.

The selected sector is an ordinary embedded Euclidean pi-wedge at the base, even if the cone's full angle is larger than 2 pi. Under a small variation, put a=T_image-C_image=A-C and b=S_image-C_image=-C. The corresponding selected angular interval is near pi and satisfies sigma det(a,b)=-f. Thus f<0 makes its angle strictly less than pi. That sector is convex, and the chord joining its two boundary rays stays inside it and misses the apex. This gives a unique near-straight bypass on the selected side. The other complementary cone sector can have a larger angle and is not being asserted admissible. This local bypass is a straight geodesic and misses c. Choose its cone-disk radius smaller than all adjacent physical wall lengths and the distance to every other forbidden vertex lift. Inside the selected sector it can cross radial fold lines emanating from c. Those crossings project to ordinary wall-interior reflections close to c; they remain transverse because wall-parallel directions were excluded.

Away from a small neighborhood of c, the two finite event halves are compact and avoid all forbidden vertices. Cover their parameter intervals by finitely many flat chart disks, in path order. The resulting ordered developed strip is allowed to overlap itself on X; no global injectivity or embedded swept region is required. Under sufficiently small fixed-direction deformations, these charts and their transition translations vary continuously, and the near-straight chord stays in this strip away from its corner bypass. The finitely many transverse wall contacts remain in wall interiors. Consequently the entire bypassed path is a legal geodesic on the deformed unfolding, and its physical projection is an ordinary reflected path from S to T. If it reaches the physical T earlier, the earlier subpath already suffices. This proves the implication.

Development around c has trivial linear holonomy because its cone angle is an integral multiple of2 pi, and a shrinking loop has zero translation period. The consistent labeled developments of S,C,T therefore agree on either near-corner continuation. In the fixed-direction supporting-line chart those developed points are affine functions of the offsets and endpoint marks, so f is an exact quadratic polynomial.

The sign can also be checked directly: a velocity perturbation w+epsilon sigma Jw shifts the approaching line to side sigma of c. In that arrangement the corner lies on the opposite side of the line, so sigma det(A,C)<0. There is no physical-sector-dependent sign change.

At the midpoint relation, differentiation gives

    f'(0)=-sigma det(w,Q(beta-alpha)),

since the base zero-period defect is hol(beta-alpha)=0. This is the signed row used throughout the reduction.

**Affine invariance.** Let F be either shear or a composition, fixing Z pointwise. It maps the two halves to straight segments with common displacement Pw, fixes their endpoint labels, and preserves avoidance of all forbidden vertices. On the tangent cone its lifted angular map satisfies phi(theta+pi)=phi(theta)+pi, so it maps the selected pi-sector to another embedded pi-sector and preserves its orientation. Equivalently,

    det(Pw,P Jw)=det(P)|w|^2>0,

so the angular side sigma is unchanged; the possible parallel component of P Jw changes speed only. Hence the same physical opening proposition applies to every nonparallel image, even as the approach passes between different physical wall sectors. Only powers whose developed directions are parallel to a wall are discarded. For the one-shear sequences with nonzero transverse component there are only finitely many such powers, exactly as used in Section 2.

This verifies the load-bearing optical transfer for arbitrary finite powers. The 52 prescribed image replays in the earlier packet are a separate implementation check of the same sign and label conventions, rather than a substitute for this local argument.


## 6. Conditional local isolation

The finite positive-spanning orbit family supplies a uniform first-order margin. Fix a linear local gauge transverse to the actual family symmetries, and use a norm on that quotient. Compactness gives kappa>0 such that every unit variation v has some selected event row g_i(v)<=-kappa. The finite exact quadratic functions f_i have a common quadratic remainder bound. Their finite path-regularity neighborhoods also have a common positive radius. For sufficiently small positive t, some event satisfies

    f_i(t v)<=-kappa t+C t^2<0,

uniformly over unit v. The local opening proposition gives illumination. Hence, under the stated seed-rigidity/rank premise, the dark base configuration is locally isolated modulo the actual fixed-direction family symmetries.

This is conditional local isolation, not a classification of all dark polygons or an unrestricted wall-count bound.
