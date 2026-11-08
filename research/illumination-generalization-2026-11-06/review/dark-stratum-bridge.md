# A precise sufficient bridge through rational affine dark strata

This is a proved CONDITIONAL reduction with an explicit unproved hypothesis. It does not establish that hypothesis, remove k<=6, or decide the existence of any dark pair.

## 1. Parameter space with actual marks retained

Fix a cyclic list of m<=21 oriented wall directions u_i from

    {(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)}.

Adjacent directions are not parallel, as the walls are maximal. Put v_0=0 and v_j=sum_{i<j} ell_i u_i, where ell_i>0 are COORDINATE increments, not Euclidean side lengths. The closure equations sum ell_i u_i=0 have integer coefficients. Append four real coordinates for two designated marks S,T.

Let H be the resulting rational linear parameter space and U the subset whose boundary is a finite strictly simple polygon with this direction sequence and whose two marks are distinct and strictly interior. U is relatively open in H. To see this, a given valid polygon has positive separation between its finitely many nonadjacent closed wall segments. Adjacent nonparallel segments meet only at their shared vertex and retain that property locally; each fixed positive ell_i stays positive. Small closure-preserving perturbations therefore retain simplicity and maximal wall count. The marks have positive distance to the boundary and to each other, and remain interior by continuity of the Jordan polygon. No degenerating polygon or boundary mark is used.

Let D be the subset of U whose ACTUAL designated pair fails to illuminate under finite corner-avoiding ordinary billiards. No regularity, definability, or finite presentation of D is assumed.

## 2. Rational-affine germ criterion

Suppose x is an element of D. Assume there exists an affine subspace L of H defined by finitely many rational linear equations with rational constant terms, containing x, and a relative neighborhood V of x in H such that

    L intersect V intersect U is contained in D.

Then D contains a rational parameter vector arbitrarily close to x. Consequently D contains a rational-coordinate polygon with the same m maximal walls and a distinct rational interior dark pair.

Proof. A consistent rational affine system has a rational particular solution and a basis of rational direction vectors, by Gaussian elimination over Q. Rational coefficient combinations of that basis are dense in L. The set V intersect U is open around x in H, so there is a rational y in L intersect V intersect U. The assumed inclusion makes its actual marked pair dark. Rational wall increments give rational vertices, and the four mark coordinates are rational by construction. This proof also covers dimension-zero L: its unique solution is then rational already. There is no need to perturb a physical trajectory or pass an infinite limiting sequence of trajectories to a limit.

## 3. Exact consequence if the criterion holds for every dark configuration

Hypothesis R: for every eligible fixed direction list and every x in its dark locus, the rational-affine germ criterion in section 2 holds.

Under R, illumination of ALL rational-coordinate four-direction polygons and rational interior pairs with W<=21 implies illumination of ALL real-coordinate four-direction polygons and ALL distinct real interior pairs with W<=21. Indeed, a real dark configuration would give a rational dark configuration in the same valid parameter domain by section 2. The accepted common even-denominator similarity would then give a canonical45 W<=21 disk with a dark interior A pair.

Thus R, TOGETHER WITH a proof of the uncapped canonical theorem, would supply the missing arbitrary-real-wall octilinear bridge. Neither premise has been established here. The accepted k<=6 baseline cannot substitute: rationalization and denominator clearing need not keep k<=6.

This is darkness-preserving parameter deformation of the entire marked polygon. It need not be a global affine map of one room to another, so the accepted affine mirror obstructions do not refute R. It also does not infer a dark or illuminated limiting pair from illumination of nearby rational points. Its rational approximants must already be dark by the explicit local inclusion.

## 4. Hostile tests of the premise

A merely real-affine local description is insufficient. The set {(x,y): y=sqrt(2)x, x>0} is a real affine line intersected with an open domain and contains no point of Q^2. Even rational POLYNOMIAL equations are insufficient: x^2=2, x>0 has a real solution but no rational solution. These examples are logical tests of the proposed sufficient hypothesis, not billiard dark loci or counterexamples to R.

Finiteness of the dark pairs for each FIXED room is insufficient to establish R for the family of rooms. It only constrains fibers over the wall parameters. Even a finite fiber can move on a graph with irrational coefficients or an algebraic irrational relation. The independently accepted endpoint-rationality theorem establishes rationality when the walls themselves are rational; it does not establish the required family-wise rational-affine inclusion near irrational wall data.

The imported LMW decomposition supplies finite affine correspondences on a FIXED translation surface with real coefficients. It does not, in the cited form, assert rational coefficients or a rational affine description of the total physical dark locus as the surface and designated marks vary. Unfolding an irrational-wall room need not yield an arithmetic torus cover, so the shear argument from dark-endpoint-rationality.md cannot silently be reused. A new moduli-space argument would have to prove the rational-affine germ property or another explicit rational-point-preserving property of the dark locus.

The fixed-direction hypothesis is essential for the rational linear closure parameterization. This lemma supplies no bridge to arbitrary wall directions or irrational angles. It supplies no global theorem forcing an S-to-T edge in the weighted skeleton.

## 5. Review targets and next mathematical question

Independently challenge relative openness with strict simplicity and all marks retained; rational density in the exact closure space; whether the criterion uses containment in the correct direction; the actual-A embedding; and whether any cited theorem has been overstated.

The next substantive question is R itself, or a materially weaker local rational-point property sufficient for the same argument. An affirmative proof would be useful; a counterexample to R would retire this particular deformation mechanism. Neither finite-pair theorems, genericity, approximation, nor the current conditional lemma settles R.
