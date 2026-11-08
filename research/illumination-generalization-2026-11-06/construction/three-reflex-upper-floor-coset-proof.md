# UP03 hand proof: finite initial-entry block contains a usable cap coset

Independent review pending. Unlike UP01/UP02 this theorem permits upper depths not divisible by2N. It proves a new quantitative availability inequality, not merely a preserving-period identity.

## 1. Quantified original-room data

Take a=Pe,A=Ne,R=e,B=Le with odd positive integersP,N,N>P+L,Lpower2,integer e>=1,K1. Let integer0<b<c<h<H,h even,codd,epsilon=H-h, gcd(P*epsilon,N)=1. The actual native sourceS=(s,u) satisfies0<s<a,h<u<H; actual native bottomT=(t,v) hasl<t<A,0<v<c. Put
 dp=u-h even>0, dl=2(h-b),C=2epsilon,g1=h-c odd,d2=c-v odd,
 T1=dp+dl,T2=T1+C,D=T2+g1+d2 even,z=A-t,
 deltaN=N/gcd(N,dp/2), aP=P/gcd(P,h-b), a0=aP*deltaN.
Assume P>=deltaN+4. All these coefficients are odd. Sincegcd(P,N)=1, the source and initial-cap preserving factors aP anddeltaN are coprime. Also gcd(epsilon*aP,N)=1.

Use the genuine five physical bands: initial cap descent of durationdp with widthA; left loop fromh tob toh of durationdl with widtha; roof cap of durationC with widthA; right arm durationg1 with widthe; bottom durationd2 with widthLe. No source-width mirror exists aboveh.

## 2. A finite initial-entry block with large NET cap growth

Set tau_q=(A+z-s+2eq)/D>0 for integerq>=0. The initial endpoint Y(q)=s+dp*tau_q increases unboundedly. Choose an even cap center2A*npre sufficiently far along that its strict left-entry interval
 2A*npre-a < Y(q) < 2A*npre+a
contains only positive grid indices. Let qstart andqend be its first and last integer indices. The corresponding slope interval has length2a/dp, while the grid spacing is2e/D. Therefore
 tau_end-tau_start >= 2a/dp-4e/D.
The interval has many indices becauseC>2dp (u<H), henceD>3dp and its q length P*D/dp>3P.

For EVERY q in this finite block the actual initial cap index is the SAME npre. Define
 zpre=s+dp*tau_q-2A*npre in(-a,a),
 nleft=floor((zpre+dl*tau_q+a)/(2a)),
 z0=zpre+dl*tau_q-2a*nleft in[-a,a),
 X=z0+C*tau_q.
Algebraically bad left-loop endpoints remain defined for locating a crossing but never become retained rays.

Because the centered source difference is strictly greater than-2a,
 Xend-Xstart > C*(2a/dp-4e/D)-2a > 2a-4e.
The last strict inequality uses C>2dp andC<D. This NET growth allows arbitrary backward source-fold jumps. For consecutive q, nleft is nondecreasing and
 X(q+1)-X(q)<=rho=2e*T2/D<2e.

## 3. Select a strict cap-coset point AND a safe left-loop endpoint

Desired cap-coset upper thresholds have spacing2e*deltaN:
 U=A+e+2e*deltaN*j, j integer.
SinceP>=deltaN+4,
 Xend-Xstart>2a-4e>=2e*deltaN+4e>2e*deltaN+2rho.
Thus some threshold U lies in(Xstart+2rho,Xend]. Let qcross be the FIRST q in the finite initial-entry block withX(q)>=U. Thenqcross>qstart+2. Putq=qcross-1. Firstness and the upper step bound give
 U-2e < U-rho <= X(q) < U.
This is a strict cap-coset window with centerA+2e*deltaN*j.

The selected left-loop endpoint cannot be a true source corner. If it were, z0(q)=-a, and its preceding step would have exactly one source reset (the uncentered increment is2e*T1/D<2e<=2a). Hence
 X(q-1)=X(q)-rho+2a>=U-2rho+2a>U,
contradicting firstness. The predecessorq-1 is still inside the initial-entry block becauseqcross>qstart+2. Therefore both |zpre|<a and|z0|<a hold, as well as a strict needed cap-coset phase. This handles the jumps rather than assuming monotonicity or simply counting new controls.

## 4. Preserve both entries and rotate within the SELECTED coset

Increase slope by e*a0*M. Its initial-cap fold-index increment is
 dp*a0*M/(2N), an integer by deltaN=N/gcd(N,dp/2).
The literal zpre is unchanged. Its left-loop index changes by(h-b)*a0*M/P, also integral by the definition ofaP. Thus literal z0 is unchanged too.

The cap phase changes by2e*epsilon*a0*M. Its orbit modulo2A has coset spacing2e*deltaN because
 gcd(epsilon*a0,N)=deltaN.
At the selected seed X=A+2e*deltaN*j+z1 with|z1|<e. Solve
 j+epsilon*aP*M=0 moduloN/deltaN,
which has a solution0<=M0<N/deltaN becausegcd(epsilon*aP,N)=1. At that slope the actual cap endpoint is an odd-A center plus the SAME literal z1, strictly in the original right opening. The seed's cap-coset requirement was proved, not assumed.

Replacing M0 byM0+N/deltaN preserves zpre,z0,z1, changes the cap index byepsilon*aP and changes the right pre-fold phase by
 g1*e*a0*N/deltaN = e*g1*aP*N,
an odd multiple ofe. At most one of the two alternatives equals the actual corner classe modulo2e. Choose its safe alternative; the centered right residual |z2|<e is then strict. All FOUR original passage guards hold simultaneously.

## 5. Entire actual target and source identity

The seed target index is integral becauseD is even:
 E=z+2eJ,
 J=q+D*a0*M/2-N*npre-P*nleft-N*m-k,
using actual fold indices AFTER the M shift. The final slope increase2e*aP*N*p changes initial-cap/left-loop/roof-cap/right indices by
 dp*aP*p, 2(h-b)*aP*N*p/P, 2epsilon*aP*p, g1*aP*N*p.
These are integers and preserve ALL literal passage residuals. The target index increases by aP*N*d2*p, odd and a unit modulo Lpower2. A finite0<=p<L therefore reaches the full original target t.

The actual physical charts and signed seams are the five original bands described in section1. They require only the strict passage inequalities just proved, not upper-depth divisibility. At a formal floor corner the left phase after the loop becomes-zpre. At cap ascent time dp it is-zpre+tau*dp=-s+2A*npre, folding to EXACT actual S at heightu before the roof because dp<epsilon. Discard the entire corner prefix and emit only that regular ascending suffix; retain the whole itinerary if the floor is ordinary. The FINAL slope decides which case applies. No physical path traverses a corner.

Disjoint ascending left and descending right h mouths exclude a roof corner. All source-cap heights exceedv; left-loop x<=a<l<t rules out earlier T at any target height; right/cap heights exceedv and the bottom reachesv only at its final time. Every retained contact is a finite original-wall specular reflection at the common final slope, with correct signed velocity. This is a positive actual S-to-T theorem, not a projected sheet path.

## 6. Scope and prescribed control

The quantitative conditionP>=deltaN+4 is real. When deltaN=N it cannot hold becauseP<N; no general upper-depth result follows in that case. UP02 still supplies the special deltaN1 family without a width bound. Their union does not settle arbitrary ordered spirals, all r3 or r<=8.

One prescribed control before execution: e2,P7,K1,L4,N15,b1c3h4H15,S4,14,T26,2. Here dp10 is NOT a multiple2N30,deltaN3,aP7,a021. Initial npre1 gives strict q block35..62. Xstart211/2,Xend1521/10,rho19/5. Choose cap threshold116; its first crossing isq46, selectq45. Then tau21/4,zpre-7/2,z0=0,X231/2,desiredcapresidual3/2. CapM4 solves modulusN/deltaN5 and gives693/4,rightz2-5/4,E172,J42. Finalp2 gives4053/4,E1012,J252,actualT26,2. Finalindices npre169,nleft217,m371,k254. The source reset atq37 lies inside the block and does not invalidate the later first crossing. This explicitly tests the new NET-growth argument with a backward jump.

No discovery search, new clock, engine, census, fitting, worker or git mutation. Independent review of both the new availability argument and actual physical transfer is required; this is not full goal completion.
