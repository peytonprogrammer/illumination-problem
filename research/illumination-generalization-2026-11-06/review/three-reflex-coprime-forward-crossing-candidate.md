# LC01 predeclared lower-source first-crossing candidate

Reviewer hand candidate; reciprocal independent review required. No discovery run.

Use ordered original spiral a=Pe,l=(N-L)e,w=(N-K)e,A=Ne, positive integer P,K,L,N, 4<=K<L,N>P+L, positive rational e, integer 0<b<c<h<H. Actual rational S=(s,u),T=(t,v), 0<s<a,b<u<h,l<t<A,0<v<c, integer u,v. Let d0=h-u,C=2(H-h),g1=h-c,d2=c-v,D=2H-u-v,z=A-t,Lambda=lcm(P,N,K). Require gcd(Lambda*d2,L)=1.

Claim: original actual S illuminates original actual T, with NO cap-gcd condition. In initial target grid tau(q)=(A+z-s+2eq)/D set n(q)=floor((s+d0*tau(q)+Pe)/(2Pe)), z0(q)=s+d0*tau(q)-2Pe*n(q), X(q)=z0(q)+C*tau(q). Although X has backward jumps, its forward increments are at most hstep=2e(d0+C)/D<2e, and X tends to positive infinity. At the first crossing of a sufficiently distant cap-window upper endpoint U=(2m+1)A+Ke, the previous K consecutive indices lie STRICTLY inside (U-2Ke,U). Among four consecutive integers at least one avoids the two initial strong endpoint classes; their periods are >=2 and cannot both be2. Use that index and the existing exact Lambda target correction and physical band guards.

Proposed whole native corollary, using CE08 cap-source lemma and TR01/TR05: integral e>=1, odd positive P,N,K with K>=5,K<L=2^j,N>P+L, integer0<b<c<h<H,c odd, arbitrary H-h. Every distinct actual interior even-even pair illuminates. No prime N or cap-depth/gcd restriction.

Predeclared exact constructor checks (no census or coefficient fitting):
- Existing CE03 noncoprime room e4/P1/K4/L5/N9,b1/c4/h8/H11,S2,6,T18,2.
- Explicit cap-gcd-failing calibration e4/P1/K4/L7/N17,b1/c3/h4/H21,S2,2,T48,2; gcd(PC,N)=17>=K; target gcd(lcm(1,17,4),7)=1. Geometry is fixed before verification.
- Whole-family native calibration e4/P1/K5/L8/N15,b1/c3/h4/H19,S2,2,T40,2; gcd(PC,N)=15>=K, target gcd(lcm(1,15,5),8)=1. Composite N and deep cap violate earlier sufficient conditions. No claim of all-pair numeric enumeration.
