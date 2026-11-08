# Exact rational-direction propagation across mixed rectangular necks

A25 hand candidate. Same original deadline as mixed-neck-residue-effort.json. Not a universal illumination theorem.

Let a finite tree of fixed orthogonal chambers be joined by rectangular necks of fixed positive widths w_e, each horizontal or vertical. Chamber positions change only by translations prescribed by neck lengths; all members considered remain strictly simple disks with disjoint piece interiors and smooth relative mouth interiors. Keep actual S,T in fixed chamber coordinates. Suppose a finite legal actual path is supplied with velocity component magnitudes (p,q), p,q>0.

After placing fixed collars inside the chambers, all reference mouth crossings can be made transverse and strictly between the sidewalls. Each neck visit is a full traversal: longitudinal velocity cannot change sign inside its rectangle. Chamber blocks may return through the same mouth or revisit an edge.

For a horizontal neck, the transverse position and velocity sign are obtained by folding u+epsilon*(q/p)*L with period 2w_e. Increasing L by delta>=0 with (q/p)*delta in 2w_e*Z therefore preserves BOTH exit coordinate and exit sign. It inserts a finite even number of sidewall reflections and cannot create a corner hit since the two end coordinates are strict and every added bounce is longitudinally interior. For a vertical neck the condition is (p/q)*delta in 2w_e*Z.

Induct through the supplied physical itinerary: every chamber block is the identical rigidly translated path, every neck has the identical entry/exit local phase and velocity, and the final block ends at the actual translated T. Earlier actual target arrival only supplies a shorter legal connection. This proves exact simultaneous propagation, even across perpendicular necks and repeated visits. No reference endpoint lift is silently replaced.

For integer parameters L_e=L_e^0+ell_e*n_e with rational positive w_e,ell_e and rational p/q, let P_e be the positive denominator in lowest terms of ell_e*q/(2p*w_e) for horizontal e, or ell_e*p/(2q*w_e) for vertical e. A witness at n^j illuminates every n in n^j+diag(P_e)*Z_nonnegative^E. This is an arithmetic orthant, not monotonicity for arbitrary increases.

A finite exact certificate list yields a FINITE criterion for full integer-orthant coverage. Set B_e=max_j n_e^j and M_e=lcm_j P_e^j. Membership in the union is constant on the cells obtained by fixing a coordinate below B_e, or fixing its residue modulo M_e above B_e. Each cell has a representative in 0<=n_e<B_e+M_e. Consequently covering that finite box by the supplied witness orthants proves coverage of ALL nonnegative integer parameters. This is a condition on an actual finite certificate pack; no claim such a pack always exists is made.

Widths and chamber shapes are FIXED. Intersecting coordinate-strip generators may change neck widths or chamber geometry and are not automatically represented by this model. This proof does not fill the universal atlas, lower k for arbitrary dark rooms, or resolve the finite prefixes without certificates. The perpendicular-neck-joint-proof.md companion tests a different ALL-jointly-large construction under the SAME original A25 effort deadline.
