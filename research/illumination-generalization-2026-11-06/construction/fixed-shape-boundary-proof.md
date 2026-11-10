# Fixed-shape darkness rigidity and boundary/coalescence tails

A27. Application of a published theorem; No uncapped wall-minimum claim. Actual endpoints and the physical corner-stopping convention are used throughout.

## Imported hypothesis checked in the primary source

[Published finite-pair theorem, Theorem 1.2(i), version 3](https://arxiv.org/html/1905.09358v3) states global finiteness of nonilluminating physical pairs in EVERY rational-angle polygon with connected interior, including torus-cover unfoldings. The convention in Definition 1.1 and the following paragraph stops a trajectory at every polygon vertex. Lemma 2.1 uses SOME connection between the two FULL physical lift fibers, not one chosen target sheet. Global finiteness is stronger than finite targets for each fixed source and is essential here. No assertion about a general translation surface's globally finite dark locus is imported.

Let P be one fixed bounded rational-angle Jordan polygon. Put

    D(P)={(x,y): x,y in int(P), x!=y, no finite corner-avoiding
                  specular billiard trajectory joins actual x to actual y}.

The imported theorem says D(P) is finite. This statement is about existence of finite actual paths, including the corner convention used in the goal. All results below are deductions from that global statement.

## 1. Uniform illumination collars for this fixed polygon

There exist constants delta(P)>0 and eta(P)>0 such that EVERY distinct actual interior pair x,y illuminates whenever EITHER

    dist(x,boundary P)<delta(P), or dist(y,boundary P)<delta(P),
    or |x-y|<eta(P).

If D(P) is empty choose any positive constants. Otherwise choose delta half the minimum boundary distance of every endpoint appearing in D(P), and eta half the minimum separation of its ordered pairs. Both minima are positive because the sets are finite, the endpoints are interior and the endpoints in a pair are distinct. Any pair satisfying one displayed inequality therefore does not belong to D(P). This proves actual illumination. Neither the source nor the target is replaced by a corner, a limiting endpoint or a chosen lift.

This handles ALL boundary coalescences in the FIXED shape, including an approach from opposite arms of a reflex corner. It does not require a visible convex corner, an invariant saddle connection, a supplied witness or a finite reflection bound.

## 2. Exact transfer under a compatible affine family

Suppose A_z is invertible affine and maps P to P_z while conjugating reflection in each actual wall support of P to Euclidean reflection in the corresponding support of P_z. Then

    D(P_z) = {(A_z x,A_z y):(x,y) in D(P)}.

To prove this, transform each straight leg and each ordinary reflection of a finite actual path. Affine conjugacy sends the velocity reflection law to the correct Euclidean law and maps finite wall interiors, corners and polygon interior bijectively. Apply the inverse map for the converse. An earlier target visit still supplies a legal prefix. The statement concerns the ACTUAL pair, so no quotient-fiber ambiguity is introduced.

Sufficient cases are arbitrary similarities for any rational-angle P, and independently positive axial scalings followed by an axial symmetry and translation for an ORTHOGONAL P. In the latter case the linear reflection parts diag(-1,1) and diag(1,-1) commute with every axial scaling, while the affine translations send the actual support lines correctly. Arbitrary anisotropic scalings of diagonal-wall rooms are NOT asserted compatible.

Consequently for ANY family of actual endpoints S_z,T_z in P_z, define normalized actual endpoints x_z=A_z^-1 S_z and y_z=A_z^-1 T_z. If a parameter sequence satisfies

    min(dist(x_z,boundary P),dist(y_z,boundary P),|x_z-y_z|) -> 0,

then every sufficiently late member illuminates. More precisely the collar test in section1 applies once ONE of its three inequalities holds. Boundary or diagonal limiting points need not themselves be admissible endpoints.

For similarities A_lambda(x)=lambda*x+c_lambda, a useful uniform version is: for any C<infinity, ALL distinct pairs in lambda P+c_lambda with endpoint distance <=C from the actual boundary OR pair separation <=C illuminate for all sufficiently large lambda. Divide distances by lambda and use section1. This includes every allowed A pair satisfying the condition, with no support or exception cap.

## 3. Necessary rigidity of a connected dark family

Let Z be any connected topological parameter space. Assume A_z and the actual endpoint maps vary continuously, all pairs are distinct and interior, and every member is dark. Then the ordered normalized endpoint pair (x_z,y_z) is CONSTANT on Z.

Indeed its image is a connected subset of the finite set D(P), hence one point. Thus a continuously dark compatible fixed-shape family can move only by transporting the SAME normalized physical dark pair. This is a positive necessary condition derived from actual darkness. It does not assert constancy for isolated dark parameters of a family containing lit members.

## 4. Rational endpoint curves have finitely many exceptional parameters

For a one-real-parameter family, suppose all four coordinates of (x_lambda,y_lambda) are rational functions of lambda, with no poles in the allowed parameter domain. Suppose at least ONE coordinate f is nonconstant. Then there are only finitely many possible dark lambda in the ENTIRE domain.

Write that coordinate as p(lambda)/q(lambda) after cancellation. For any specified dark normalized pair the relevant coordinate equals a fixed real constant c. The polynomial p-c*q is not identically zero, since f is nonconstant, and has at most max(deg p,deg q) real roots. A finite union over D(P) is finite. In particular there are at most max(deg p,deg q)*|D(P)| exceptional parameters, counting distinct ordered dark pairs before taking the union. This is qualitative when D(P) is unknown.

This argument is valid for arbitrary real coefficients and does not require a lattice or rational dark coordinates. If all normalized endpoint coordinates are constant, the family can remain dark forever; the hypothesis must not be omitted. For many-parameter rational families one gets a finite union of algebraic equality loci instead, which may have positive dimension, NOT a finite exceptional set.

## 5. Exact contribution and unresolved gap

The uniform collar closes the complete fixed-shape boundary-approach and endpoint-coalescence strata, including the reflex case where the elementary finite-return construction has no known witness. Section4 also guarantees a first actual witness and eventuality along every nonstationary rational endpoint curve inside a compatible fixed-shape orbit. These are applications of known global finiteness, not a new proof of the published theorem.

There is NO effective delta, eta, last exceptional parameter or reflection bound in this deduction. The set D(P) may be nonempty; no finite prefix is automatically resolved. No uniform constants over different polygons follow from pointwise finiteness. In particular an atlas ray P_lambda=lambda*P0+lower_order_vertex_changes generally changes SHAPE and is not conjugate by one affine map; these results do not cover it. The stationary normalized interior-pair case, general moving-shape limits, diagonal strip interactions and the universal canonical45 W<=21 theorem remain open.
