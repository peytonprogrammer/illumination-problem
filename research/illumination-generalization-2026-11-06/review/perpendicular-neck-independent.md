# Independent A25 review: jointly long perpendicular necks

Verdict: ACCEPT the complete stated joint-tail theorem and finite LATTICE remainder corollary in frozen perpendicular-neck-joint-proof.md. The extra half-plane/separation hypotheses in the latter are mandatory. This is an independent hand reconstruction; no trajectory search, numerical oscillatory experiment or peer program execution was used.

## Exact itinerary and actual target

I independently reconstructed the cumulative shifts rather than assuming that residue matching reaches the target. Orient the unfolded reference velocity with both components positive. A full horizontal traversal contributes its positive developed length in x; increasing that length by A and its winding by n full periods therefore changes the next copy by (A,2u*n). A full vertical traversal analogously changes it by (2v*m,B). This remains true on backward physical traversals: unfolding reverses the corresponding physical axis, leaving the developed component positive. The traversal counts are total completed visits, not signed net visits. Orthogonal mirrors never exchange the two axes.

Induction over every complete neck visit and every fixed chamber block gives Z_i=(a_i*A+2v*b_i*m,b_i*B+2u*a_i*n), including repeated edges, returns and branches of the recorded word. Each fixed chamber block has the same counts at its ends. Collars make every cut crossing strictly interior/transverse, so finite open margins exist. No unused mouth is capped. Small vertical line residual controls a vertical mouth directly and a horizontal mouth after division by tau, which stays uniformly away from zero.

Let alpha=tau*A-2u*n and beta=B/tau-2v*m. Direct substitution gives every cut residual (tau-tau0)*X_i+a_i*alpha-b_i*tau*beta. At the target this is F=(tau-tau0)*D+a*alpha-b*tau*beta. The proposed target image is a consequence of the copy induction, not a separate freely chosen modulo image. Both a,b are positive for the three-chamber outer-mark model. Added winding integers will be nonnegative, preserving the reference fold signs and avoiding deletion of a reference bounce.

## Uniform curvature and exact endpoint correction

For a fixed nontrivial character (h,k) and a fixed positive compact interval J, write its phase as c*h*A*tau+d*k*B/tau. If k=0, the integral is bounded by a constant/(|h|A). If k!=0, its second derivative has constant sign and magnitude at least cJ*|k|B. Hence the near-stationary set |phi'|<=R has length <=2R/(cJ*|k|B). On each of at most two remaining intervals, phi' is monotone, and integration by parts bounds the integral by C/R. Choose R=sqrt(|k|B). The estimate tends to zero uniformly in A. This proves the needed finite-character convergence whenever BOTH A and B exceed sufficiently large independent thresholds, including arbitrarily imbalanced ratios.

A nonnegative continuous torus bump supported in the chosen open phase box has positive mean. A fixed finite trigonometric approximation with uniform error less than one quarter of that mean, together with the finitely many estimates, makes its integral positive. Thus a tau1 and integers n,m enter the box for every sufficiently large A,B. The Fourier approximation and slope interval are chosen BEFORE the length thresholds; neither depends on their ratio. This is enough for existence and does not assert an effective numerical threshold in the frozen theorem.

Choose the fixed interval J sufficiently close to tau0 to make D*|tau1-tau0|<=epsilon. Then |F(tau1)|<=C*epsilon. HOLD n,m fixed. Expanding F gives

    F(tau)=tau*(D+a*A+2v*b*m) - (tau0*D+b*B+2u*a*n).

It is genuinely affine, with positive derivative. Since 2v*m=B/tau1+O(epsilon), that derivative is >=c*(A+B) for all sufficiently large A,B. Its exact root moves tau by at most C'*epsilon/(A+B). The horizontal phase error changes by A times that amount, and the vertical phase error changes by at most C''*B times that amount on the positive compact slope window. Both are O(epsilon), uniformly in aspect ratio. Shrinking epsilon once preserves all finite strict chamber/cut margins, as well as the original chosen period parities. There is no re-rounding after taking the root.

At this root every realized chamber block and neck splice is legal and the endpoint equality is EXACT. All neck lengths are finite at each member and winding integers finite, so the path has finitely many smooth specular reflections. Every genuine corner is avoided, all actual walls are retained, and an earlier actual target visit only shortens a valid path.

## Witness existence and the finite integer remainder

For each fixed horizontal length the extra hypotheses make the vertical neck a valid opposing-half-plane single-neck decomposition, with the union of C0, C1 and the horizontal neck as one fixed chamber. Both groups are strict disks with the actual marks interior. The accepted long-neck theorem therefore supplies an actual witness at some K0. It necessarily has both velocity components nonzero because it traverses both perpendicular necks. This provides the joint-tail reference witness without assuming illumination of every member.

After obtaining thresholds L*,K*, only finitely many lattice L-values lie below L*. For each, the same one-neck theorem supplies a K-tail; take their finite maximum. Do the symmetric operation for the finitely many lattice K-values below K*. The joint tail and these finitely many fiber tails leave a FINITE lattice rectangle. This uses no uniform-in-W threshold and no unsupported compactness for continuous families. I accept the separate real-parameter compactness remark only with its explicitly stated nondegenerate local-uniformity hypotheses; it is unnecessary for the lattice result.

## Coverage and exclusions

Reviewed every section of the frozen joint proof and the named parallel-tree/long-neck dependencies, including backward visits, signs, both mouth orientations, arbitrarily imbalanced growth, phase-cell tolerance, exact target arrival, finite reflections, validity of whole glued rooms and the extra separation cuts. All frozen request pins were verified.

This is positive eventual witness EXISTENCE and a finite reduction for the stated fixed three-chamber two-neck model. It does NOT verify the finite remainder, give a wall-count threshold, cover arbitrary intersecting strip generators or changing chambers, or prove W<=21. Those obligations remain open. No claim is made about independent coefficients for three or more growing neck lengths. No general all-darkness classification is inferred.
