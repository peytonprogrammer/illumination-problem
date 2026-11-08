# LC02 hand proof: target-compatible cap run with actual endpoint periods

Independent review pending. Scope is lowerchoice-candidate.md. Dependency:
peer LC01 forward-crossing proof, independently hand accepted in
three-reflex-coprime-extension-forward-review.md/.json. That source stays
frozen and peer-owned. This proof strengthens selection inside its cap run.

## 1. Retain a long block in one cap window, despite backward jumps

Use tau(q)=(A+z-s+2eq)/D. For lower u<h put
n(q)=floor((s+d0*tau(q)+Pe)/(2Pe)) and
z0(q)=s+d0*tau(q)-2Pe*n(q). For u>=h set d0=0,n=0,z0=s;
there is NO source band. In all cases X(q)=z0(q)+C*tau(q) tends
to positive infinity. The source index is nondecreasing (or constant), so

    X(q+1)-X(q)<=2e(d0+C)/D=hstep<2e.

The following is exactly the accepted LC01 cap-run lemma, also valid
with zero source height: choose m>=0 with U=(2m+1)A+Ke>X0+K*hstep,
and let q* be the FIRST index with X(q*)>=U. Then q*>K, and

    U-2Ke < X(q*-j) < U, j=1,...,K.

Firstness gives the upper bound; summing the one-sided forward increment
gives the strict lower bound. No monotonicity of X or lower increment
bound is needed. The K preceding consecutive q all lie in ONE actual
strict cap window with the SAME m. Formal source-corner indices may
be used to locate that window; they are removed before defining a ray.

## 2. Three candidates meet the actual target congruence

The class q=N*m modulo g appears exactly K/g times in a run of K
consecutive integers because g|K. Since K>=3g, choose three consecutive
members q0,q1=q0+g,q2=q0+2g from that class. They are positive and
all have |z1|<Ke, where z1=X(q)-(2m+1)A.

The target seed at any physically strict index has

    E=z+2eJ, J=q-P*n(q)-N*m-K*k(q).

Because g|K|P, selecting q=N*m modulo g guarantees J divisible by g
for ANY eventual actual fold indices n and k. This source-index
independence is essential and is why an unrestricted q choice is not used.
It does not assume target matching from a strict cap interval alone.

## 3. Each actual corner event eliminates at most one candidate

At a lower source the actual first corner event is

    s+d0*tau(q)=Pe modulo2Pe.

If nonempty its exact q period is p_source=P*D/gcd(d0,P*D)>P,
since0<d0<D. It is omitted at u>=h, when actual s is strictly interior
and n=0. Because K|P, P>=K>=3g, so the three candidate differences
are at most2g<K<p_source. Thus this source event kills at most ONE.

The right pre-fold phase is

    Y(q)=z1+g1*tau(q)
        =s+(D-d2)*tau(q)-2Pe*n(q)-(2m+1)A.

K|P makes2Pe*n(q) an integer multiple of2Ke for EVERY varying n(q).
Therefore the ACTUAL right-corner event Y(q)=Ke modulo2Ke is the
single affine event

    s+(D-d2)*tau(q)-(2m+1)A=Ke modulo2Ke.

The common m need not be divisible by K, and K|N is NOT assumed.
The event is empty or has period
p_right=K*D/gcd(D-d2,K*D)>K>2g. It also kills at most ONE
of the three candidates. Two events remove at most two candidates;
at least one survivor has BOTH |z0|<Pe and |z2|<Ke, with cap |z1|<Ke.
Here z2=Y-2Ke*k is the centered full actual right fold.

This is a three-candidate actual-period count, not LC01's four-consecutive
strong-unit count. In particular it permits K3 and nontrivial target g.
A zero residual is a smooth outer-wall reflection, not a true corner.

## 4. Finish the full original target and physical ray

At the survivor J is integral and divisible by g. Since
 g=gcd(Lambda*d2,L), the coefficient Lambda*d2/g is invertible modulo L/g.
Choose0<=p<L/g with J+pLambda*d2=0 modulo L; use p=0 for modulus1.
Increase tau by2eLambda*p and respectively increase actual source/cap/right
indices by Lambda*d0*p/P,Lambda*C*p/N,Lambda*g1*p/K. All are
integers; upper n remains0. Every literal signed residual stays identical.
The final E is z modulo2Le, so the original bottom fold reaches exactly t.
This is one selected ray at one finite positive final slope.

The accepted original CE04 band charts now apply with ALL strict portal
hypotheses satisfied. Original finite wall contacts reflect only the correct
velocity component. Interface positions AND signed derivatives agree;
smooth zero contacts remain actual outer-wall reflections. The true left
and right reflex/ledge corners are excluded by the actual endpoint events.
For lower sources, disjoint ascending/descending h-mouth positions exclude
a roof corner at the FINAL slope. At u=h the same mouth separation applies.
For upper u>h a formal roof endpoint returns to EXACT actual S at
eta*=2H-u; emit its regular descending suffix, traversing no discarded
corner. No endpoint or sheet is replaced, no artificial wall is introduced,
and no different directions are concatenated.
The left ascent stays at x<=a<l<t at any target height. Cap/right heights
exceed v, and descent reaches v only at its final time. Thus the ray ends
at FIRST actual T. Positive widths and finite final slope imply finitely
many ordinary specular reflections, without a reflection-length cutoff.

## 5. Whole native family, arbitrary vertical metrics and even multipliers

Let e>=1 integral,L=2^j,2<=K<L with oddpart(K)>=3,
P=K*t for odd positive integer t,N odd,N>P+L,and ANY ordered integral
0<b<c<h<H with c odd. For every native bottom target v is even, so
d2=c-v is odd. Since t,N are odd, v2(P)=v2(K) and
v2(Lambda)=v2(K). Since K<L, v2(K)<j and therefore

    g=gcd(Lambda*d2,L)=2^v2(K), g|K,
    K/g=oddpart(K)>=3.

Also K|P by construction. Hence EVERY actual native terminal pair
satisfies the theorem, whether below, at or above the cap mouth, with
NO cap-gcd, cap-depth, prime-N or aspect restriction. Source and right
multipliers may both be even. TR01/TR05's exact original-room placement
join covers all other actual pairs; regular ray reversal exchanges labels.
Thus the full stated native family illuminates. It does not settle arbitrary
width patterns, all ordered spirals, other r3 types or r<=8.

## 6. Prescribed hand calibrations and failed alternative

A. e2,P6,K6,L8,N17,b1,c3,h6,H23,S(4,4),T(26,2).
d0=2,C34,g1=3,d2=1,D40,z8,Lambda102,g2.
Before the first source fold, X(q)=(191+18q)/5. With m1, U114,
first crossing q*=22 gives cap run16..21 strictly in(90,114).
Compatible q are17,19,21. Choose19: tau57/20,n0,z0=97/10,
z1=23/5,k1,z2=-217/20,E=-8,J=-4. Target correction p2 gives
tau16377/20,J200,E808=8 modulo32, actual T(26,2).
The old cap gcd is gcd(P*C,N)=17>K6. Weighted/rational target gcd
is2 and z/e4 even, so those earlier uniform sufficient criteria also fail.
But q18 has strict portals and J1 odd, and cannot be corrected by the
102-step target orbit. This demonstrates the need for the selected class.

B. e2,P3,K3,L4,N9,b1,c3,h6,H9,S(2,4),T(14,2):
d0=2,C6,g1=3,d2=1,D12,z4,Lambda9,g=1.
The first crossing of U24 is q*=8, giving run5..7 in(12,24).
Chooseq6: tau11/3,n1,z0=-8/3,z1=4/3,k1,z2=1/3,E4,J0,p0.
The old cap gcd is9>K3 and the four-consecutive K>=4 theorem is
inapplicable; the three actual-period candidates cover this K3 case.

C. SAME B room with source u=h6: q3,tau16/5,z0=2,z1=16/5,
k1,z2=4/5,E4,J0,p0. The source band is absent and its actual mouth
start is regular.
D. SAME B room with source u8: q3,tau4,z0=2,z1=0,z2=0,E4,J0,p0.
Both zero residuals are smooth original outer-wall contacts.

No discovery search/census/engine was used. These hand controls corroborate
the proof and do not establish its quantifiers by sampling. Reciprocal
independent review of this extension remains required.
