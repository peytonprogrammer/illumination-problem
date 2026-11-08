# AP06: actual source-chart choice removes a second factor of two

## Proposed whole native theorem

In the original ordered spiral

( Pe,b ),( Pe,h ),((N-K)e,h),((N-K)e,c),((N-L)e,c),
((N-L)e,0),(Ne,0),(Ne,H),(0,H),(0,b),

let e,P,K,N,L be positive integers, K<L, N>P+L, P<=K, K>=3 odd, N odd, L a power of two, and nu2(P)<=2. Let integer 0<b<c<h<H have h even and both b,c odd. Then every specified distinct actual interior even-even pair illuminates by a finite corner-free original-room specular ray.

This extends the accepted AP05 corollary at nu2(P)=2 using a physical source-floor chart. It does not settle arbitrary P or all ten-wall rooms. Reciprocal independent review is required.

## Pair transfer needed for the extension

For a terminal pair S=(s,u),T=(t,v),0<s<a=Pe,b<u<h and l=(N-L)e<t<A=Ne,0<v<c with integer u,v, choose either

- U: initial actual velocity (sigma*tau,+1), source-band time X=h-u;
- F: initial actual velocity (sigma*tau,-1), true floor y=b, source-band time X=h+u-2b.

Both X are strictly positive. Put C=2(H-h), g1=h-c, d=c-v, F=g1+d=h-v, D=X+C+F,

M=lcm(P/gcd(P,X),N/gcd(N,C),K/gcd(K,g1)),
g=gcd(M*d,L).

If g|K,g<=P and P*F+g*(X+C)<=K*D, the actual pair illuminates in either chosen chart.

### Formal seed and exact target

Use the already accepted AP01 lower weighted strict-window construction with X in place of A0. It uses only positive band times and F=g1+d. For each actual source sign sigma, the literal seed has

q=Pi+Nm+gj,
tau=(A+(A-t)-sigma*s+2eq)/D,
z0=sigma*s+X*tau-2a*i,
z1=z0+C*tau-(2m+1)A,
z2=z1+g1*tau-2Ke*k.

The metric bound produces |z0|<a and |z1|<Ke, and paired actual source signs ensure at least one strict |z2|<Ke. This algebra does not assume the source y-velocity is positive; it encodes its horizontal fold throughout time X.

The reduced period works for the floor chart as well. P|XM,N|CM,K|g1M and g|K imply g|g1M; also g|dM, so g|FM. The increments

Delta_i=XM/P, Delta_m=CM/N, Delta_j=FM/g, Delta_k=g1M/K

are positive integers. A slope increment 2eM preserves EVERY literal signed residual and increments q by DM. The actual target index J=gj-Kk changes by Md. Solve J+Md*p=0 mod L, possible precisely because g|J and g=gcd(Md,L). Add a sufficiently large positive multiple of L/g to p. All indices are then nonnegative, tau>0, all strict guards hold at this FINAL slope, and E=z2+d*tau=A-t modulo 2Le. This is one actual ray with the specified original target.

### The source-floor chart is physical, including its singular formal alternative

If phi=sigma*s+(u-b)*tau is not in aZ, the source-floor contact is strictly inside (0,a). Its true floor reverses vy, and the horizontal triangular fold is continuous with the correct specular derivative. Between b and h its vertical side contacts are actual x=0,a walls. The source rises through the strict h mouth with the signed phase z0.

If phi=ja, the formal itinerary hits a true corner and must NOT be emitted. Let R=2(u-b). At formal time R the vertical position is exactly u and its horizontal fold is

F_a(sigma*s+R*tau)=F_a(2ja-sigma*s)=s.

The horizontal departing velocity there is -sigma*tau and vy=+1. Emit a new regular ray from EXACT original S with that velocity, using only the suffix starting at that phase. It reaches h after X-R=h-u>0. No corner is traversed and no endpoint moves. The remaining cap/right/bottom bands have exactly the final strict residuals already established. This is the AP03 exact-source suffix argument, applied after the AP05 reduced-period lift, so no nonsingularity is presumed to survive a slope change.

The cap roof cannot be a corner: a roof-corner round trip would force its h entry and h exit to the same actual x, whereas the strict entry lies in [0,a) and the strict exit lies in (A-Ke,A], disjoint by a<A-Ke. All h/c matching uses the same signed horizontal fold and vy; zero residuals are smooth outer-wall contacts, not true vertices. The final descending target leg lies in the actual bottom rectangle. Source bands have x<=a<l<t; all other pretarget bands have y>=c>v. Thus actual T is reached on its final descent. If some earlier actual T were ever available, its legal prefix suffices. Every emitted duration and slope is finite. This proves the proposed pair composition independently of sample controls.

## Every native source has a valid chart

For a native lower source u even, set X_U=h-u and X_F=h+u-2b. Both are even because h,u are even. Their difference is

X_F-X_U=2(u-b)=2 modulo 4,

because b is odd. Therefore exactly one of X_U,X_F is divisible by four. Choose that chart. Since nu2(P)<=2, P/gcd(P,X) is odd. The other two reduced-period factors are odd because N,K are odd, so M is odd. Native v is even and c odd, hence d is odd. Since L is dyadic, g=gcd(Md,L)=1. It divides K and is at most P. The weighted inequality holds automatically:

P*F+(X+C)<=P*(F+X+C)<=K*D.

For all native upper or mouth sources u>=h, use accepted AP05 upper construction: M=lcm(N/gcd(N,2H-h-u),K/gcd(K,h-c)) is odd, hence g=1<K, with no lower source factor needed. The source x and target x are arbitrary actual native coordinates in their terminal rectangles; no restriction beyond interior even-even marks is imposed.

The specific protected TR01/TR05 original-wall constructions plus reversal cover every remaining placement, including marks on their open artificial seams. Hence the whole quantified theorem follows.

## Strict increase and precise limitation

Take P4,K5,N13,L8,e any positive integer,b1,c3,h6,H7. All geometry inequalities hold. For lower native u=4, the upward period has P/gcd(P,h-u)=2 and hence even M and g=2, which does NOT divide odd K. The source-floor time is 8, giving odd M and g=1. Lower u=2 instead uses the upward time 4. Thus a genuine original-floor choice covers the missing source heights; the accepted AP05 direct-only whole criterion nu2(P)<=1 does not include these widths.

The proof does not assert a necessary condition for illumination. If b is even the two even source times can be congruent modulo 4; if nu2(P)>=3 a time divisible by four need not remove every power of two. Those cases and incompatible odd factors remain open. No scaling of ER02 or finite endpoint table is invoked.

## Verification protocol

The theorem above is a hand proof. Prescribed checks may use only the fixed displayed P4/K5/N13/L8 room, with lower u2 upward and u4 source-floor, and actual S=(2,u),T=(18,2) at e2. Recompute selected directions and all original-wall/true-corner/first-T guards with reviewer code. No discovery effort, new clock, engine, worker, census, fitting or git-state change is authorized or needed by this packet. Freeze this proof and checks; ask the existing author for a reciprocal independent audit. Full r3/r<=8 remain open.
