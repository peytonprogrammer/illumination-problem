# CE06 hand proof: rational period lattice, actual target and native coverage

Scope is rational-candidate.md. Independent review pending. Only the final
target-selection condition of CE04 is changed. The source/cap/right guarded
prefix uses its accepted two-event noncover and strict delta<K construction.
The original room and actual S,T are never scaled, replaced or projected.

## 1. Exact rational period group

Write the three exact signed residuals as in WP01:
z0=s+d0*tau-2Pe*n,z1=z0+C*tau-(2m+1)Ne,
z2=z1+g1*tau-2Ke*k. For an upper source d0=0,n=0.
A slope increment2eQ preserves all literal residuals iff

    Q*d0/P, Q*C/N, Q*g1/K are integers.

Reduce each fraction height_i/width_i=B_i/A_i, with coprime positive
A_i,B_i for a positive height. For the zero source height use1,0 and
omit it from positive-fraction requirements. Put Z=lcm(A_i) and
gamma=gcd(B_i). Any prime dividing gamma divides every active B_i,
and hence no corresponding A_i; the absent source factor is1. Therefore

    gcd(Z,gamma)=1.

For Q=Z/gamma all ratios Q*B_i/A_i=(Z/A_i)*(B_i/gamma) are integers,
including the zero source ratio. Conversely, write Q=x/y>0 in lowest
terms. The condition x*B_i/(y*A_i) integral implies A_i divides x,
because gcd(A_i,B_i)=1; it implies y divides B_i, because gcd(x,y)=1.
Thus Z divides x and y divides gamma. Consequently Q/(Z/gamma)=
(x/Z)*(gamma/y) is a positive integer. This proves that the full rational
preserving group is precisely (Z/gamma)*Z, not merely the integer-Q
subgroup derived in WP01. No global affine transport is asserted.

## 2. Preserve the phase and match the ENTIRE bottom target

The preliminary prefix gives E=z2+d2*tau=z+2eJ with J an integer.
Let d=gcd(gamma,d2) and Q0=Z/d. Since d divides gamma, Q0 is a
positive integer multiple gamma/d of eta=Z/gamma. Its fold-index changes

    Delta_n=Q0*d0/P, Delta_m=Q0*C/N, Delta_k=Q0*g1/K

are therefore integers. Upper n stays0. All signed residuals are identical
and their physical fold indices remain correct. The bottom index changes by

    A_target=Q0*d2=Z*(d2/d), an INTEGER.

Under gcd(A_target,L)=1 choose0<=p<L with J+p*A_target=0 modulo L.
Increment the slope by2eQ0*p. Now E'=z+2Le*j and the original bottom
fold F_(Le)(E') equals exactly z=A-t. This is actual target attainment.
The slope remains positive finite. The q grid does not become inconsistent:
Q0*D is integral because Q0*d0,Q0*C,Q0*g1 and Q0*d2 are integers.
More importantly, literal residual equality directly retains actual guards.

For completeness, this Q0 is the least positive rational preserving
coefficient with an INTEGER J increment. Indeed write Q=eta*m. Since
Zd2/gamma has reduced denominator gamma/d (gcd(Z,gamma)=1),
Q*d2 is integral iff gamma/d divides m. Thus Q is a multiple of Q0.
This is a fixed-prefix period statement only; another prefix could behave
differently, and no global nonillumination criterion follows from failure.

If gcd(A_target,L)=2 and r=z/e is an odd integer, the same two target
images used in CE02/WP01 also work: choose desired residue0 or-r matching
J modulo2, then solve the divided congruence modulo L/2. That optional
branch is not used for the whole family below.

## 3. Original finite walls, signed velocities and first T

The CE04 four bands use exactly the original F_(Pe),F_(Ne),F_(Ke),F_(Le)
folds. Because z0,z1,z2 are LITERALLY unchanged, every centered strict
portal residual and its signed absolute-value germ are unchanged. A zero
residual still means a smooth original outer-wall contact. No projected
endpoint or changed sign is substituted at a seam. Vertical hits reverse
only vx; a smooth roof reverses only vy. All portions share the FINAL
selected absolute velocity ratio tau.

Lower-source roof corners remain impossible by the disjoint h-mouth
symmetry. For upper sources the FINAL slope is treated anew: if its roof
phase is jA, its curve returns at eta*=2H-u to EXACT actual S with a regular
descending departing velocity. Emit only that suffix; it never traverses
the discarded corner. A fractional preserving increment changes none of
this identity. It neither splices different directions nor adds a wall.

The left ascent cannot hit T because x<=Pe<l<t at any relevant target
height. Cap/right heights exceed v, and the descending height reaches v
only at its final time. The same argument applies to a retained suffix
from u>h>v. Therefore the endpoint is first actual T. Finite widths and
finite slope give finitely many ordinary reflections. Every true corner,
first-hit guard and actual endpoint condition is inherited through exact
signed residual equality, not through numerical evidence.

## 4. New entire native family without a horizontal target parity restriction

Take integral e>=1,odd P,K,3<=K<L=2^j,prime N>P+L,
0<b<c=4<h,H=h+epsilon with all heights integral,h EVEN,
epsilon>0 and2epsilon<N. For native terminal sources, u is even.
For u<=h,d0=h-u is even and C=2epsilon is even.
For u>h,d0=0 and C=2H-h-u is again even. In all cases g1=h-4 is
even and d2=4-v=2, since a native bottom ordinate has only v=2.
Every positive developed height is even; every P,N,K is odd. Hence the
reduced numerators A_i are odd, so Z is odd; all active denominators B_i
are even, so gamma is even. Thus d=gcd(gamma,2)=2 and

    A_target=Z, which is coprime to L.

The cap flight satisfies0<C<N and0<P<N. Primality of N gives
 delta=gcd(PC,N)=1<K, so the accepted prefix exists for EVERY actual
native terminal pair, including all sources within the cap. No condition
on z/e is used: t and s need only be their actual even native coordinates;
they need not be multiples of e. In particular arbitrary integral e is
allowed. The original TR01/TR05 join covers exactly all other placements
for these arbitrary source/right widths, and regular reversal exchanges
labels. Therefore EVERY distinct actual interior even-even pair illuminates
throughout the quantified family. No room size or reflection cutoff is used.

These rooms with c4 and an arbitrary e are not justified by the previous
odd-c native corollary. The new cancellation of a genuine shared height
factor changes the actual target step; it is not a relabelled integer-Z
identity or a claim from one calibrated room.

## 5. Two prescribed hand controls

Use e2,P3,K3,L4,N11,b1,c4,h6,H9,A22,a6,R6,B8,l14,w16.
For S(2,4),T(18,2): d0=2,C6,g1=2,d2=2,D12,z4.
The reduced numerators(3,11,3) give Z33; denominators(2,6,2) give
gamma2,Q0=33/2,A_target33. q1 gives tau7/3,n1,z0=-16/3.
The cap inverse selects M2, giving tau79/3,n5,m3,z1=-4/3,k4,z2=10/3.
E56=z4+4J,J13. Its z/e2 is even; WP01's gcd2/odd-r sufficient
criterion is unavailable. The rational correction p3 adds198 to tau and99
to J: tau673/3,J112,E452=4 mod16, actual T(18,2).
Index increments per step are(11,9,11), all integers.

For upper source S(2,8) and SAME target: d0=0,C4,g1=2,d2=2,D8.
Reduced numerators(1,11,3),denominators(0,4,2) again give Z33,gamma2.
q2 gives tau4; M1 gives tau16,n0,m1,z1=0,k3,z2=-4,
E28=z4+4J,J6. p2 gives tau148,J72,E292=4 mod16.
Its indices change by(0,6,11) per step. The zero cap residual is smooth.
No discovery search or numerical room census was used for these controls.

Whole spiral/W10/r3 and r<=8 remain open. The result is a quantified
positive family, not completion of the native full objective.
