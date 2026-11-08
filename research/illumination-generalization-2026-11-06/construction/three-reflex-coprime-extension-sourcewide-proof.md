# CE04 proof: arbitrary commensurate source-arm width

Author hand proof; independent acceptance pending. Geometry and quantified
hypotheses are in sourcewide-candidate.md. Every room is original and
strictly simple with boundary
(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b).
The inequalities P<N-L and K<L give0<a<l<w<A. No artificial wall is used.
Let F_b(x)=dist(x,2b*Z), the triangular fold with range[0,b].

## 1. Initial compatible grid and two strict exclusions

Put z=A-t in(0,L*e), d0=max(h-u,0), g1=h-c, d2=c-v;
C=2(H-h) when u<=h, and C=2H-h-u when u>h.
Then d0>=0,C,g1,d2>0 are integers and D=d0+C+g1+d2=2H-u-v.
Take

    tau_q=(A+z-s+2e*q)/D, q>=0 integral.

The numerator is positive since A-s>0. When u<h exclude

    s+d0*tau_q=P*e modulo2e.

At u=h OMIT that exclusion: there is no positive-length source band and
0<s<P*e is the exact actual guard. Also omit it for u>h.
In every case exclude

    s+(D-d2)*tau_q-A=K*e modulo2e.

An event at time t in(0,D) is empty or one residue class modulo
D/gcd(t,D)>=2: subtract two solutions of the affine congruence.
The two event times, when present, are distinct. Their periods cannot
both be2, since that would force both times to equal D/2. Two classes
of periods>=2 cannot cover Z unless both periods are2: otherwise their
densities sum to at most1/2+1/3. All periods divide D, so some
q in0..D-1 avoids both. This proof permits rational e,s,t and offsets.
It does not copy the invalid P>1 three-class equal-block shortcut.

For a lower source put

    n=floor((s+d0*tau_q+P*e)/(2P*e)),
    z0=s+d0*tau_q-2P*e*n.

When u<h, the strong exclusion modulo2e rules out either actual endpoint
modulo2Pe, so |z0|<Pe. When u=h,n=0,z0=s already has this property.
For an upper-cap source u>h put n=0,z0=s and do not invent a source band.

## 2. Cap orbit with the correct source period

Increase tau by2Pe*M, M>=0 integral. For a lower source n increases
by d0*M, leaving z0 identical; for an upper source n remains0.
Every initial exclusion is preserved because all its times are integers.
The cap phase X0=z0+C*tau_q has shifts2Pe*C*M modulo2A=2Ne.
Let delta=gcd(P*C,N). These phases form a coset of spacing2e*delta.
Choose an integer r nearest to(A-X0)/(2e*delta). Then

    Y=X0+2e*delta*r, |Y-A|<=e*delta<K*e.

Ties are harmless because the last inequality is strict. Solve

    (P*C/delta)M=r modulo N/delta

with0<=M<N/delta. The inverse exists by the definition of delta.
After this slope shift X=z0+C*tau differs from Y by a multiple2A.
Thus X=(2m+1)A+z1 for an integer m and z1=Y-A in(-Ke,Ke).
This is an actual strict cap-exit window.

Put

    k=floor((z1+g1*tau+K*e)/(2K*e)),
    z2=z1+g1*tau-2K*e*k.

Modulo2e the pre-fold phase is s+(D-d2)*tau-A, because the removed
source and cap periods are integer multiples2e. The second exclusion
still holds. Consequently this phase is not Ke modulo2Ke, and |z2|<Ke.
The full actual source period was2Pe, not2e; the latter was used only
as a sufficient stronger guard and as an initial endpoint-compatibility grid.

## 3. Match the entire actual bottom period

The developed bottom phase is

    E=z2+d2*tau
     =s+D*tau-2Pe*n-(2m+1)Ne-2Ke*k
     =z+2e*J

for an integer J. Under the initial grid, J=q-P*n-N*m-K*k;
q is increased by P*D*M during the preceding slope shift.
Let Lambda=lcm(P,N,K). The next slope shift tau->tau+2e*Lambda
preserves all three residuals, since the index changes are

    n += Lambda*d0/P  (lower source; upper n stays0),
    m += Lambda*C/N,
    k += Lambda*g1/K.

These are integers and give identical z0,z1,z2. Thus J increases by
Lambda*d2. By gcd(Lambda*d2,L)=1, choose0<=p<L with
J+p*Lambda*d2=0 modulo L. Make that single final shift2e*Lambda*p.
Now E=z modulo2Le and F_(Le)(E)=z, so the actual endpoint is
x=A-z=t. All slope choices are finite and positive. They define one
ray after selection; no concatenation of different directions is used.

## 4. Actual bands, signed velocities and corners

For lower u<=h, let eta increase from u to2H-v and set actual y=eta
up to H and y=2H-eta afterward. The actual abscissa is

    u..h:        F_(Pe)(s+tau*(eta-u)),
    h..2H-h:     F_A(z0+tau*(eta-h)),
    2H-h..2H-c:  A-F_(Ke)(z1+tau*(eta-(2H-h))),
    2H-c..2H-v:  A-F_(Le)(z2+tau*(eta-(2H-c))).

For upper u>h start instead with F_A(s+tau*(eta-u)) on u..2H-h.
The source band is absent. Every open-band mirror is an original wall:
0/a below the left mouth,0/A inside the cap,w/A inside the right arm,
and l/A inside the bottom. The selected heights stay above b on the
left and above0 on the bottom. Each band lies in the actual room.

At the first seam the centered residual z0 has |z0|<Pe<A.
Both folds equal |z0| locally, with the same signed derivative.
At the cap exit X=(2m+1)A+z1 and |z1|<Ke<A, so both adjacent
expressions equal A-|z1| locally, again including their signed derivative.
At the right/bottom seam |z2|<Ke<Le, so both expressions also equal
A-|z2|. A zero residual represents a smooth reflection on a continuous
outer wall, not a missing seam guard. The excluded endpoint residuals
avoid every reflex corner (a,h),(w,h),(w,c). Seam outer endpoints at
x=0 orA are smooth original wall points. Source u=h is interior and
starts with the cap chart. Vertical-wall hits reverse only vx;
a legal roof hit reverses only vy. All legs have the common absolute
velocity ratio |vx/vy|=tau. Positive widths and finite tau give finite hits.

The only remaining possible corner is a roof endpoint. For a lower
source, triangular-wave symmetry at a roof corner would equate the
ascending and descending h-level abscissas. The former lies in[0,a),
the latter in(w,A]. They are disjoint since a<l<w. Hence no lower
source ray hits a roof corner, including u=h.

For upper u>h, a formal roof corner can occur when
s+tau*(H-u) is a multiple of A. Its exact fold symmetry gives

    F_A(s+2tau*(H-u))=F_A(s)=s.

At eta*=2H-u in(H,2H-h), the formal curve therefore returns to EXACT
actual S. Delete the whole prefix through the roof corner and emit the
remaining suffix from S with its descending signed velocity. The suffix
stays belowH, has no roof contact, and satisfies every later guard already
proved. No optical continuation through the discarded corner is claimed.

On the initial ascent, x<=a<l<t whenever the target height occurs.
The cap and right arm have heights>v. On the retained descending part,
y reaches v only at its final time. Thus this is a finite corner-free
specular path to FIRST actual T. Its endpoints never change sheets or
physical identity.

## 5. Whole native family with P>1

Take integral e>=1, odd P,K,3<=K<L=2^j, prime N>L+P,
ordered integral0<b<c<h, c odd, and positive integral epsilon=H-h
with2epsilon<N. For every native left-terminal source, C is a positive
integer<=2epsilon<N. Since P<N and N is prime, gcd(P*C,N)=1<K.
Also Lambda=lcm(P,N,K) is odd and d2=c-v is odd for native even v.
Their product is coprime to L, so the terminal theorem applies to ALL
native left-terminal/bottom pairs. The accepted exact TR01/TR05 placement
join supplies every other pair for this same ordered spiral geometry;
those proofs are metric-independent and allow arbitrary source/right widths.
Reversal covers either label ordering. Therefore every distinct native
interior even-even pair illuminates in this family, without a room-size
or reflection bound.

This removes the equal source-width premise for a quantified family; it
still imposes commensurate widths and arithmetic cap/target conditions.
General spiral metrics, other W10 types and r<=8 remain OPEN.

## 6. Two prescribed hand calibrations (not discovery)

A: e2,P3,K3,L4,N11,b1,c3,h5,H7,S(2,4),T(18,2).
Here(d0,C,g1,d2,D)=(1,4,2,1,8),z4,delta1,Lambda33.
Take q0,tau3,n0,z0=5; nearest-cap r1 gives M1 and tau15.
Then n1,z0=5,m1,z1=-1,k2,z2=5,E20=z4+2e*J with J4.
Already J=0 mod4, so p0. This is a native-terminal witness in a whole
family with both source and right arms of width6, rather than2.

B: e1,P2,K2,L3,N7,b1,c4,h5,H6,S(1,4),T(5,2).
Here(d0,C,g1,d2,D)=(1,2,1,2,6),z2,delta1,Lambda14.
Take q0,tau4/3,n1,z0=-5/3; nearest-cap r3 gives M6 and tau76/3.
Then n7,m3,z1=0,k6,z2=4/3,E52=z2+2*J with J25.
The final correction p2 yields tau244/3,J81, still all residuals
identical; E164=2 mod6 folds to z2. The zero cap residual is a smooth
outer-wall reflection. This also tests even P/K and a rational slope;
it is a terminal theorem control, not a member of the whole native corollary.

No discovery search or new clock was used. Independent review must check
both the exact argument and reuse scopes, rather than infer quantifiers
from these two examples.
