# Mixed-axis neck trees with rational-affine growth

A25 positive scope extension, SAME original aggregate deadline. Read with the frozen perpendicular-neck-joint-proof.md. Independent review is required for this new statement; acceptance of the two-neck proof alone is not asserted to accept it.

## Quantifiers

Let a finite tree of fixed orthogonal chambers be joined by horizontal and vertical rectangular necks of fixed widths. Actual distinct S,T lie in fixed chamber coordinates. Chamber positions change by translations only. For all parameters considered the full union remains a strictly simple polygonal disk with no additional piece contacts affecting the recorded paths. Relative mouth interiors are smooth; fixed collars can be absorbed.

Within each orientation the widths are commensurate. Choose U>0 with U/u_e a positive integer for every horizontal width, and V>0 with V/v_e a positive integer for every vertical width. Empty orientation classes can be omitted.

Horizontal lengths are L_e(x)=p_e*x+c_e, p_e nonnegative integers; vertical lengths are K_e(y)=q_e*y+d_e, q_e nonnegative integers. Finite rational coefficients can be made integral by rescaling the corresponding parameter. Assume a finite actual legal witness is supplied at (x0,y0).

If that witness traverses at least one growing neck of EACH orientation, it gives actual illumination for EVERY valid member with x and y independently sufficiently large. No balance or rational ratio restriction applies. Chamber branching, same-mouth returns, and repeated or backward passages are permitted.

On a ONE rational-affine growth ray x=y=lambda, a supplied actual witness consequently gives actual illumination for EVERY sufficiently large lambda, irrespective of which growing orientations it uses. The no-growth and one-orientation cases are treated separately below. This extends the provided-witness ray theorem beyond parallel necks; it does not supply a witness on every ray or settle finite prefixes.

## Weighted-copy derivation

Cut collars away from all reference bounce locations. Unfold the supplied witness with initial velocity (1,tau0), tau0>0 whenever both growing orientations are visited. Let A=x-x0, B=y-y0. At a reference cut i let

    r_i=sum p_e over preceding horizontal traversals,
    s_i=sum q_e over preceding vertical traversals.

These are TOTAL weighted visit counts, not signed net traversals. Across a fixed chamber word they do not change. A repeated physical backward traversal still has positive developed longitudinal travel, as independently checked in the two-neck proof.

For integers n,m insert U*p_e*n/u_e full transverse periods on each horizontal traversal, and V*q_e*m/v_e on each vertical traversal. They are integers. If a coefficient is zero no additional winding is inserted. The downstream unfolded chamber-image shift is EXACTLY

    Z_i=(r_i*A+2*V*s_i*m, s_i*B+2*U*r_i*n).            (1)

Proof by finite induction: across a horizontal neck e the increment is (p_e*A,2*U*p_e*n); across a vertical neck it is (2*V*q_e*m,q_e*B). Across a fixed chamber block the same shift translates its entire reference copy. Finite chamber shapes, words and mouth locations remain unchanged. This proves (1) for any tree itinerary, not only a serial chain.

Let X_i,Y_i=tau0*X_i be reference cut coordinates, and (D,tau0*D) the reference target. Put r=r_target and s=s_target. Define

    alpha=tau*A-2*U*n,  beta=B/tau-2*V*m.

Every cut residual is

    (tau-tau0)*X_i+r_i*alpha-s_i*tau*beta,

and the EXACT actual-target condition is

    F(tau)=(tau-tau0)*D+r*alpha-s*tau*beta=0.          (2)

If r,s>0, the curvature proof applies to the TWO phases (A*tau/(2U), B/(2V*tau)). It does not introduce one independent phase per neck. The rational-affine coefficient and width premises are precisely what make all parallel necks share the two integer winding variables. Arbitrary independent length vectors do NOT satisfy this reduction automatically.

All finite guard tolerances may depend on max_i r_i,s_i and the reference word. With n,m fixed,

    F'=D+r*A+2*V*s*m >= c*(A+B)

at sufficiently large A,B and near-reference positive slopes. The two-neck Fourier-box argument and affine-root correction therefore preserve all chamber/neck guards and hit the actual target image dictated by (1), exactly. Each growing neck gets nonnegative extra full periods; fixed necks retain their reference winding and only small entry/slope perturbations. This proves the independent two-parameter joint tail when r,s>0.

## The remaining one-ray cases

Set x=y=lambda. If no traversed neck has a positive coefficient, every edge of the connected visited subnetwork has fixed length. The tree forces its relative chamber positions to remain fixed. The entire actual witnessed path therefore moves rigidly with that subnetwork; unused growing branches do not affect it because all members remain disjoint valid disks.

If just one growing orientation is used, say horizontal, absorb all fixed-length necks of the visited connected subnetwork into its chambers. These components are fixed orthogonal disks, translated as rigid pieces. Every remaining traversed growing neck is horizontal and has a width dividing U. The accepted parallel-tree provided-witness propagation theorem applies to those finite blocks, with weighted cumulative horizontal coefficient r_i. Unvisited growing necks contribute no traversal and no term to the copy induction; no reflection on an artificial cap is inserted. Equivalently use the accepted parallel proof directly on the recorded blocks, retaining every unused-mouth avoidance guard. Its q=0 exception is the preceding no-growth case. The vertical-only case follows by exchanging the axes.

An axis-parallel reference path can only use necks parallel to that axis. Its visited chamber/reflection geometry lies in that one-orientation subnetwork; it is covered by the same fixed/parallel cases. It cannot be a reference for the r,s>0 proof. Thus no nonzero-component hypothesis is silently imposed on the full one-ray conclusion.

## Limits

This is a provided-witness eventuality theorem on a FIXED mixed-axis neck tree, or a joint tail with two orientation-locked growth parameters. It covers more than the earlier parallel-tree statement and permits arbitrary finite repeated itineraries. It does NOT prove that every geometric strip atlas has such a fixed-chamber representation, cover independently varying lengths within one orientation without the rational-affine locking, generate witnesses, or finish finite prefixes. The first-witness/finite-lattice argument for the special two-neck separating chain remains in the main proof and is not automatically extended to this larger tree.

The entire calculation uses actual physical chamber and neck states and a target image forced by that itinerary. It neither substitutes a selected target lift nor infers darkness from failed search. No computation or new literature theorem is used.
