# CE05 hand proof: equality spacing still permits a strict cap return

Scope: equality-candidate.md. Independent acceptance pending. Reuse CE04's
actual geometry, developed heights d0,C,g1,d2,D and z=A-t. This proof
supplies a different guarded initial selection; it does not require the
CE04 sufficient inequality delta<K. CE04's sourcewide proof remains frozen.

## 1. Count genuine endpoint events, not the narrow-unit surrogate

Use tau_q=(A+z-s+2e*q)/D. For lower u<h exclude

    s+d0*tau_q=Pe modulo2Pe.                     (source)

Omit this event at u=h and above, since the actual source is strictly
interior and the source-arm band has zero duration. Also exclude

    s+(d0+C)*tau_q-A=Ke modulo2Ke,               (cap)
    s+(d0+C+g1)*tau_q-A=Ke modulo2Ke.            (right)

Each event is empty or exactly one q residue class. The source period
is DP/gcd(d0,DP); cap/right periods are DK/gcd(t,DK), with respective
times t=d0+C and d0+C+g1. All times are positive and strictly less
than D. Thus the source period is strictly greater than P>=K>=2,
and cap/right periods are strictly greater than K>=2.
If K>=3, their density sum is at most3/4. If K=2, every period is
at least3. The cap and right periods cannot both equal3: because
0<t<D, period3 would force t=DK/3=2D/3, but their times differ by
g1>0. Therefore, with three events, at least one period is at least4
and the sum is at most1/3+1/3+1/4=11/12. With only two events it
is at most2/3. In all cases, the union fails to cover Z.
Each period divides DP, since K|P. A good q exists in0..DP-1.
All nonempty offsets may be rational; subtracting solutions proves the
period assertion without assuming an integral offset.

## 2. Why these are the actual folded cap/right guards

Fold the lower source using its full period2Pe as in CE04, giving
z0=s+d0*tau-2Pe*n with |z0|<Pe. At u=h or u>h use z0=s,n=0.
Since K|P, subtracting the source period changes no cap/right residue
modulo2Ke. Since delta=gcd(PC,N)=K, K divides N as well. Subtracting
an odd-A center then changes no right residue beyond the displayed
subtraction of A. Hence the cap and right events are exactly sufficient
for the corresponding physical fold endpoints. This divisibility check
is required; without K|P the linear cap event need not remain its folded
counterpart.

## 3. Select a strict cap point at equality

Shift tau by2Pe*M. Source residuals remain identical; all three selected
exclusions are preserved, since K|P and all developed times are integers.
Cap phases X0+2Pe*C*M modulo2Ne form a coset of spacing2e*delta=2Ke.
The cap exclusion says that X0-A is NOT Ke modulo2Ke. Thus the coset
misses both endpoints of the radiusKe open interval centered at A.
Exactly one representative lies inside that interval. Equivalently the
nearest lattice choice Y=X0+2Ke*r satisfies |Y-A|<Ke strictly; a tie
would be precisely the excluded cap event.
Solve (PC/K)M=r modulo N/K; the inverse exists because delta=K.
Take0<=M<N/K. Then X=(2m+1)A+z1 with z1=Y-A and |z1|<Ke.
The right event, preserved through the source/cap subtractions and slope
shift, gives |z2|<Ke on the next full right fold. Every needed actual
portal is strict.

## 4. Actual target and optical guards

All equations in CE04 section3 hold unchanged: E=z+2eJ,
Lambda=lcm(P,N,K), and tau->tau+2eLambda keeps all three residuals
identical and adds Lambda*d2 to J. The assumed gcd supplies p in0..L-1
with J+pLambda*d2=0 modL. Thus the complete bottom fold reaches actual
T, not merely its residue modulo2e.

The four original-room fold charts are exactly CE04 section4 with source
widthPe, cap widthNe, right widthKe and bottom widthLe. Every strict
portal now comes from sections1-3. Local fold germs match POSITION AND
SIGNED VELOCITY; each contact lies on its actual finite wall and avoids
all three reflex corners. Lower-source roof symmetry uses disjoint
mouths[0,Pe) and((N-K)e,Ne]. Upper-source singular prefixes return to
EXACT actual S at eta*=2H-u and can be discarded, retaining only the
ordinary descending suffix. The retained path never traverses a roof
corner. Original height monotonicity gives first actual T, and finite
positive widths/slope give finitely many specular contacts. No new
optical transfer or artificial-wall premise is introduced.

## 5. Two full native composite-width families

Take P=K=q with2<=q<L,N=qM,Mprime>L,integral e>=1 and
0<b<c<h,H=h+epsilon,epsilon positive integer,2epsilon<M.
The geometry inequality P<N-L follows from q(M-1)>L, which holds
because M>L and q>=2. For every native terminal source, C is an integer
in(0,M), so gcd(PC,N)=gcd(qC,qM)=q=K. Lambda=qM.
If c=4,Lodd,gcd(q,L)=1, every native bottom v=2 gives d2=2 and
 gcd(Lambda*d2,L)=gcd(2qM,L)=1.
If codd,Lpower2,qodd, M is odd and d2 is odd, so the same gcd is1.
TR01/TR05's exact original-room placement join supplies all other actual
pairs. Hence BOTH whole native families illuminate, including all upper
cap levels. These rooms fail CE04's strict delta<K criterion identically;
the new equality-window guard is doing necessary proof work here.

## 6. Three fixed hand calibrations

A: e2,P2,K2,L3,N10,b1,c4,h5,H6,S(2,4),T(18,2).
d0=1,C=2,g1=1,d2=2,D6,z2. q0 gives tau10/3,z0=-8/3.
Nearest-cap r2 selects M1; tau34/3,n2,m0,z1=0,k1,z2=10/3.
E26=z2+4J,J6, already0 mod3; p0. delta2=K, never<K.
This is an actual native terminal pair in the whole composite family.

B: e1,P3,K3,L4,N15,b1,c3,h5,H7,S(2,4),T(13,2).
d0=1,C4,g1=2,d2=1,D8,z2. q0 gives tau15/8,z0=-17/8.
Nearest-cap r2 selects M3; tau159/8,n4,m2,z1=19/8,k7,z2=1/8.
E20=z2+2J,J9. Lambda15,p1 gives tau399/8,J24,E50, actualT13,2.

C: e1,P2,K2,L3,N10,b1,c4,h5,H7,S(1,6),T(9,2).
This upper-cap source has C3,D6. q0 gives tau5/3,z0=1; M2 gives
tau29/3,z1=0,z2=5/3,E21,J10. Lambda10,p1 yields tau89/3,J30,
E61 and actualT9,2. The formal roof phase92/3 is nonsingular.
All three use delta=K. They are prescribed identities, not discovered
rays or a room census. Quantifiers rely on the argument, not these checks.

Full r3 and r<=8 remain open. No failure of an arithmetic sufficient
condition is a dark counterexample. No discovery clock was opened.

Calibration correction before freeze: the first attempted N6/P2/K2/L3
fixture has gcd(Lambda*d2,L)=3, so it is outside the quantified lemma
even though its hand-selected J matches the target. The prescribed
assertion correctly rejected it before checking a ray. It is withdrawn
as a scoped control and replaced by N10. No theorem hypothesis changed.
