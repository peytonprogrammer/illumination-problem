# Independent acceptance: arbitrary U rooms illuminate every interior pair

Verdict: ACCEPT the whole all-interior-pair statement of the historical two-reflex-blocker/all-heights.md, including asymmetric arm widths, unequal heights, arbitrary real dimensions and distinct real interior marks. This closes the old review's unreproduced-L-dependency qualification by using the now independently reconstructed arbitrary-real L theorem. It is not a new construction or a claim of universal eight-wall coverage.

## 1. The finite matching proof is valid over arbitrary real parameters

Use the source's positive a,b,M,c, A=a+M+b and roof heights H_L,H_R>c. For opposite high-arm marks, y_s,y_t>=c and both are strictly below their roofs; S=y_s+y_t>0. The prescribed arm lengths L_n=a-x_s+2na and R_m=x_t+2mb are strictly positive. Taking the first length STRICTLY above each threshold (y_s-c)tau or (y_t-c)tau gives remainders in (0,2a] and (0,2b]. This remains valid at threshold equality, where the next length must be used. If a mark is on y=c, its threshold is constantly zero and its remainder is a fixed number strictly below its period.

Choose tau0>2max(a,b)/c and B=M+2kA>2c*tau0. Since k can be any nonnegative integer, such a finite k exists. The map H(tau)=(L(tau)+R(tau)+B)/S is nondecreasing, H(tau0)>tau0, and H(tau_max)<=tau_max for tau_max=(B+2a+2b)/(2c). Hence its iterates stay in a bounded interval and are nondecreasing. There are finitely many possible arm indices on that interval, so the sequence reaches a fixed value after finitely many steps. No finite-precision convergence or infinite limiting path is used.

At its first stationary value tau_n, n>=1 and tau_n>tau_{n-1}. If either arm-length function jumped at tau_n, that length would have increased by at least its positive period relative to tau_{n-1}; the other length cannot decrease. Thus H(tau_n)>H(tau_{n-1})=tau_n, contradicting stationarity. Both final remainders are therefore STRICTLY below their periods. The proof covers simultaneous jumps and equality-level marks without exception.

## 2. Actual optical matching and all corners

The fixed equation gives u=c-ell_s/tau and v=c-ell_t/tau, each in (0,c). Every earlier inner-wall encounter in the corresponding arm has height at least c+(2a-ell_s)/tau or c+(2b-ell_t)/tau, strictly greater than c. Thus none exits prematurely or hits a reflex corner. Arm heights remain positive and at most the corresponding mark height, below its roof. All outer-wall contacts are smooth.

The lower-strip developed segment (a+d,u-d/tau), 0<=d<=B, is folded horizontally by the period-2A triangular wave and vertically by absolute value. It starts at (a,u) with right/down velocity. It ends at (a+M,v) with right/up velocity because a+B=a+M+2kA lies in the same increasing horizontal-fold branch. These are exactly the forward velocities of the two independently unfolded arm portions. Consequently there is ONE globally matched absolute slope, not independent rays spliced at the portals.

Throughout the lower strip its physical height is strictly below c. The vertical coordinate vanishes exactly once. The developed bottom coordinate is a+M/2+kA+(ell_t-ell_s)/2, strictly between kA+M/2 and kA+A-M/2. This interval avoids every multiple of A. Its physical image, for either parity of k, lies inside (M/2,A-M/2), so the bottom reflection avoids both outer corners. All other lower-strip vertical reflections have nonzero height below c. The finite developed length implies finitely many contacts. The actual right-arm endpoint is the specified x_t because the chosen backward arm length belongs to x_t+2b Z, and the endpoint velocities agree as above.

Thus the opposite-arm construction is a finite ordinary corner-free billiard trajectory. It permits arbitrarily many repeated passage crossings; nothing in the proof caps them uniformly or drops their phase.

## 3. The all-pair corollary now has its full dependency checked

Every interior point is either in a high-arm column (including its internal portal level) or strictly below c. Same-column pairs are directly visible. Pairs below c are directly visible. Pairs in opposite columns with both heights at least c use the preceding construction; this includes both on y=c, where a straight segment along the notch wall would be invalid.

The remaining placement is one high-arm mark and a lower-rectangle mark outside its column. They lie in the corresponding L subroom consisting of the full lower rectangle and that high arm. The independently accepted L theorem produces a vertical-reflection-only path monotonically crossing y=c inside that arm's open portal. Before the crossing it stays strictly below c; after it stays within that high column. It never reflects at an artificial horizontal top wall of the L subroom. Therefore it is also a valid path in the actual U room with the other arm restored. Reflection at x=0 or x=A below c remains reflection at a genuine smooth U wall. Reversal and horizontal reflection cover either high-arm choice and either source order.

The case split is exhaustive and preserves the specified distinct physical endpoints. The all-pair corollary is therefore unconditional given the accepted L dependency.

## 4. Proven scope and verification level

This excludes every U-shaped orthogonal eight-wall canonical45 room from having a distinct dark interior A pair, for arbitrary k, arm dimensions and mark placement. It also proves all-real-geometry/all-real-interior-pair illumination in that U class. It does not establish the other eight-wall staircase or offset shapes, arbitrary blocker removal, higher wall counts or the main W<=21 theorem.

The historical full proof, old tools-disabled Opus review, saved six prescribed-formula controls, and L source were read. The proof above independently checks every real-parameter and physical-path obligation; the old 4,908 wall-incidence checks were not rerun or represented as a new independent computation. The old manifest does not include the later all-heights files, so acceptance pins their current full hashes directly rather than claiming a historical manifest match. No source was edited or peer checker executed.
