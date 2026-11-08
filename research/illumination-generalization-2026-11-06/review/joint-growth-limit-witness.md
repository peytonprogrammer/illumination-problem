# Joint-growth witnesses and an effective finite-prefix criterion

R26 positive hand theorem, pending independent review. This transfers a limiting witness to finite rooms while BOTH coordinate directions and chamber shapes change. It supplies no claim that arbitrary W<=21 parameter directions satisfy its hypotheses.

## 1. Data and the full limiting boundary trace

Let P_L, L>=L_geom>0, be strictly simple orthogonal polygonal disks with a fixed cyclic list of W genuine maximal walls. Suppose every vertex and the ACTUAL marks are affine functions of L:

    v_i(L)=L*v_i^0+v_i^1,
    S(L)=L*S0+S1, T(L)=L*T0+T1.

Assume the actual marks are distinct interior points for the stated family. Directions of nonzero indexed walls are fixed horizontal/vertical. Put epsilon=1/L and divide all coordinates by L. The normalized data are v_i^0+epsilon*v_i^1, S0+epsilon*S1, T0+epsilon*T1. This is a global similarity at each L, so it preserves ordinary specular paths exactly.

Let K be the union of EVERY closed limiting indexed segment [v_i^0,v_(i+1)^0], including zero-length segments and any coincident, backtracking or internal slit segments. Do NOT discard a segment merely because it disappears from the boundary of a proposed limiting filled polygon. Index data matter at intended contacts.

Suppose a known strictly simple limiting room P0 has an actual finite corner-avoiding S0-to-T0 witness gamma0 with reflection word i1,...,ik, and satisfies ALL these additional strict trace guards:

1. S0,T0 are distinct interior points, outside K.
2. Every open straight leg of gamma0 is disjoint from K except its designated reflection endpoints. In particular no interior ghost slit is crossed or followed.
3. Each reflection point belongs to the relative interior of the nondegenerate indexed limiting wall E_ij, is different from EVERY limiting vertex v_i^0, and has positive distance from every other indexed limiting segment. Its local mirror and interior side agree with P0. There is therefore one actual persistent mirror at that contact, rather than two collapsing mirrors or a disappearing cap.

These guards can be checked against a supplied finite path. Ordinary illumination of P0 alone does not imply them: a path may hit an extra limiting subdivision point or an internal slit. The stronger limiting certificate is the premise.

## 2. Actual finite-room tail theorem

**Theorem.** Under section1, there exists L_* such that EVERY real L>L_* has a finite legal path from its actual S(L) to its actual T(L), with the SAME reflection word. If all coefficient data are rational, a rational/integer L_* can be computed by finitely many exact polynomial operations and sign checks. No witness in any finite P_L is required as a premise.

**Proof of existence.** In normalized coordinates reflect the actual target successively in the indexed moving mirror lines for the fixed word. Each axial mirror reflection has a constant linear matrix and a translation affine in epsilon. Their finite composition therefore gives one actual unfolded target image U(epsilon), affine in epsilon. The straight segment from the actual normalized source to U(epsilon) is continuous at epsilon=0 and has nonzero displacement there.

Unfold each intended wall through its preceding prefix of reflections. At epsilon=0 the reference line hits each intended mirror transversely, in the prescribed strictly increasing times, and inside its indexed finite aperture. Its relevant line/axis intersection denominator is nonzero. The collision times and folded collision points therefore vary continuously for sufficiently small epsilon. Their order, strict aperture guards and reflection signs persist. Folding produces exactly the recorded finite word and the actual target, because U(epsilon) was built from that target and those physical mirrors.

For legality between contacts, take small disjoint neighborhoods of the finitely many reference contacts. Trace guard3 makes each such neighborhood contain only its intended mirror, with the correct local side. Trim the adjacent legs within these neighborhoods. The remaining finitely many compact leg pieces have positive distance from K by guard2. Every normalized indexed wall converges to its corresponding segment of K, so these trimmed legs avoid every actual boundary for small epsilon. The source remains interior by hypothesis, and near each transverse mirror the specular normal sign places the reflected leg on the same interior side. Induction along the legs proves that the whole folded path is inside the ACTUAL room, with no extra boundary hit, corner contact or glide. Possible earlier actual target arrival only supplies a shorter valid connection. Multiplying by L gives the stated actual path.

This proof does not cap an unused mouth, remove a created mirror, retain a target only modulo a period, or assume fixed chamber geometry. All actual indexed walls enter the trace guards, and every reflection is on a persistent actual wall.

## 3. Effective cutoff and finite-prefix certificate

For rational coefficient data, every unfolded mirror line and U(epsilon) is affine with rational coefficients. Each intended collision time and contact is a rational function in epsilon; its denominator is nonzero at0. All required checks have finite exact algebraic descriptions: positive ordered collision times, contact in its indexed wall interior, no unintended segment-wall intersection, proper reflection sign, interior source/target, and an interior sample for each leg. Segment intersection and polygon winding can be decided by coordinate comparisons and orientation determinants, using exact rational arithmetic after clearing denominators with their known signs. Parallel/collinear cases are kept as cases; they are not discarded by a generic-position assumption.

Thus a finite Boolean formula in polynomial sign/equality predicates determines validity of the prescribed word. No universal degree2 claim is needed after rational contacts and intermediate samples are substituted. Identically zero polynomials are evaluated as such. For each nonzero polynomial p(epsilon), remove any initial factor epsilon^j, leaving c0+c1*epsilon+... with c0!=0. Set

    eta_p = 1, if all higher coefficients vanish;
    eta_p = min(1, |c0|/(2*sum_(i>=1)|ci|)), otherwise.

For 0<epsilon<eta_p, the constant term strictly dominates all remaining terms, so the sign is fixed. Include every nonzero denominator polynomial. Let eta be the minimum of the resulting finitely many positive rational bounds. All predicates have constant truth values throughout0<epsilon<eta. The existence proof in section2 establishes that this common truth value is VALID. Therefore any integer

    N > max(L_geom, 1/eta)

is a certified cutoff: every real L>N has the actual witness. An exact sample in this tail may independently verify the Boolean formula. This is a finite algorithm once the strict limiting witness and indexed trace are supplied, not a bounded direction search or darkness test.

For a canonical integer-parameter ray L=L0+q*n, q>0, the cutoff leaves finitely many n>=0 with L<=N. Certificates for ALL those actual prefix members, combined with the tail, prove the ENTIRE marked ray. Prefix certificates may come from the accepted k<=6 theorem or an applicable closed low-wall theorem when THEIR hypotheses hold, or from independently validated finite paths. The proof does not assume every prefix member has such a certificate and does not infer it from a tail witness. R25 disproves W-independent monotone transfer as a substitute.

## 4. Uniform joint cones from a compact set of certified limits

The same stability proof works for any finite-dimensional continuous rational coordinate parameters, not just epsilon. For a strip-generator family write its coordinates as affine functions of n in N^d. Put L=sum(n_j) when nonzero, p=n/L in the compact standard simplex, and normalize coordinates by L. The leading boundary and actual marks depend linearly on p, with the fixed base coordinates contributing order1/L.

Let C be a compact subset of this direction simplex. Suppose EVERY p in C has a limiting witness satisfying the COMPLETE trace guards, with actual distinct interior limiting marks. For each p, stability supplies an open direction neighborhood U_p, a positive epsilon tolerance and one finite reflection word. Compactness gives a finite subcover. Taking the minimum tolerance gives a uniform L_C such that ALL integer generator vectors n with n/sum(n) in C and sum(n)>L_C illuminate their actual pair. This allows perpendicular coordinates and chamber shapes to vary simultaneously.

The finite-word count here is a conclusion of compactness under the stated ALL-directions premise. It is not a claim that rational directions alone cover C, that each limiting room is k<=6, or that arbitrary ratios have already been checked. For an effective global finite-prefix certificate one must supply a finite cover by certified neighborhoods with exact guards and a verified coverage proof. Then the finitely many integer vectors with sum(n)<=L_C are the remaining prefix. A single accepted k<=6 or applicable L/U/T template provides a local open cone only when its chosen witness satisfies the trace guards; no all-family coverage is inferred.

Boundary directions may collapse S and T, put a mark on a boundary, create a slit, or lack a strict known limiting witness. Such directions are explicitly OUTSIDE this theorem until separately resolved, possibly with a different normalization or another method. Thin notches are not removed by a Hausdorff argument about filled rooms.

## 5. Prescribed exact control

The companion checker uses the ten-wall family, lambda>2,

    (0,0),(4lambda,0),(4lambda,lambda/2),
    (4lambda-1,lambda/2),(4lambda-1,3lambda/2),
    (4lambda,3lambda/2),(4lambda,2lambda-1),
    (2lambda-1,2lambda-1),(2lambda-1,4lambda),(0,4lambda),

with actual S=(3lambda,lambda),T=(lambda,3lambda). Its normalized limit is the L room [0,4]x[0,2] union [0,2]x[0,4]. The limiting path

    (3,1)->(2,0)->(0,2)->(1,3)

has two genuine reflections and avoids the extra limiting vertex images (4,1/2),(4,3/2). Every other limiting wall is away from its open legs and contacts. Its scaled two-reflection version is legal in the actual ten-wall room for lambda>2. Both coordinate directions and multiple shape dimensions change, and the width1 notch persists at finite lambda. At lambda=4n, n>=1, all vertices are integral and the actual marks are A. This is a control of the stated transfer, not a census or universal all-pair theorem for ten-wall rooms.

The checker validates selected prescribed instances and rational polynomial sign bounds without searching for a direction or word. The hand theorem, not those instances, provides the continuous tail and uniform compact-cone implication.

## Coverage and remaining objective

This supplies an actual positive joint-growth and effective finite-prefix TRANSFER theorem under checkable limit-trace premises, including known illuminated limiting bases. It does not supply witnesses on arbitrary collapsed directions or verify a finite cover of any full W21 rank family. The universal canonical45 W<=21 target remains OPEN, including diagonal rooms. The next central obligation is to exhibit certified direction covers or resolve their uncovered endpoint-collapse/slit strata; it cannot be replaced by another one-witness eventuality claim.

Dependencies: elementary unfolding, rational segment-intersection predicates and compactness are proved/used directly; accepted strip-generators.md supplies the affine parameterization. Historical k<=6 and closed low-wall results enter only when separately invoked for a supplied limiting/prefix certificate. No new external theorem or literature result is imported.
