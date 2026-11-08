# CE03: source-cap selection with a right arm of width K*a

Author proof pending independent review. Scope is wide-candidate.md.
Earlier proofs/receipts remain frozen. All geometry is the ORIGINAL
ten-wall room with A=Na,w=(N-K)a,l=(N-L)a. N>=L+2 and1<=K<L
give 0<a<l<w<A and a<R<B when K>1 (R=a when K=1).

## 1. One initial grid, with the source in its actual band

Use d0,C,g1,d2,D of the candidate. All are integers, d0>=0 and
C,g1,d2>0, and D=2H-u-v. Let z=A-t in(0,La), and

    tau_q=(A+z-s+2a*q)/D, q in Z.

All q>=0 give positive slopes. The integer grid enforces initial
target compatibility modulo2a. If u<=h, the source has a narrow-arm
band of developed height d0 and then a cap band of height C=2(H-h).
If u>h, its actual starting band is the cap, of developed height
C=2H-h-u; there is NO fictitious source-arm segment. Write

    t3=d0+C+g1=D-d2 in(0,D).

An affine phase endpoint event at nonzero integer time t in(0,D)
is empty or one q-class modulo D/gcd(t,D)>=2, by subtracting any
existing solution. This fact uses rational offsets correctly and is
the same elementary residue argument as accepted CE01.

## 2. Initial selection when K>=2

Exclude

    s+d0*tau_q = a mod2a             (only if u<h),
    s+t3*tau_q-A = K*a mod2a.

The first event is empty at u=h because0<s<a, and is omitted for
u>h. If both nonempty events occur, their distinct nonzero times
d0<t3<D prevent both moduli from equaling2. Two residue classes
of moduli>=2 can cover Z only when both have modulus2: otherwise
their summed densities are <=1/2+1/3<1. Thus they do not cover.
With only one event the assertion is immediate. Every bad period
divides D, so choose q in{0,...,D-1} avoiding these events.

For u<=h put n=floor((s+d0*tau_q+a)/(2a)) and
z0=s+d0*tau_q-2na, hence |z0|<a. For u>h put n=0,z0=s.
No source reflection is added in that case.

## 3. Strict cap selection, including noncoprime cap rotations

Let delta=gcd(C,N). In this case delta<K. The initial cap phase
is X0=z0+C*tau_q. Increasing tau by2aM leaves z0 unchanged;
for a lower source n increases by d0M, and for an upper source
n stays0. Modulo2A=2Na, the cap orbit has N/delta points forming
one coset of the lattice of spacing2a*delta.

Choose an integer r nearest to (A-X0)/(2a*delta). Then

    Y=X0+2a*delta*r,
    |Y-A|<=a*delta<K*a.

This remains strict at a rounding tie. Solve

    (C/delta)M=r mod (N/delta)

with M in{0,...,N/delta-1}; it exists because the two coefficients
are coprime. The cap phase X=X0+2aCM differs from Y by a multiple
of2A. Thus for some m it equals(2m+1)A+z1, with

    z1=Y-A in(-Ka,Ka).

This is an actual strict cap-return window, not a torus projection
with an unguarded boundary. No cap-endpoint congruence needs to be
excluded when delta<K. In particular coprimality C,N is unnecessary
for sufficiently wider right arms.

Let k=floor((z1+g1*tau+Ka)/(2Ka)) and
z2=z1+g1*tau-2kKa. Modulo2a this pre-fold phase is
s+t3*tau-A. The second exclusion from section2 is preserved under
tau->tau+2aM because t3 is integral. Therefore it is NOT equal to
Ka modulo2a, and in particular not equal to Ka modulo2Ka.
Hence |z2|<Ka strictly. This exclusion is stronger than necessary,
but its noncover proof gives it without extra assumptions.

## 4. K=1: a narrow right arm, also allowing upper-cap sources

If K=1 and u<=h, use the already accepted CE01 three-class noncover
and cap selection, which has no d2-parity or equal-block restriction.
It only requires gcd(C,N)=1 at this stage. Its source/right/cap
residuals lie strictly in(-a,a).

If K=1 and u>h, omit the source event and exclude only

    s+C*tau_q-A=a mod2a,
    s+(C+g1)*tau_q-A=a mod2a.

Their nonzero integer times are distinct and strictly in(0,D), so
the two classes cannot cover as in section2. Set z0=s. Under shifts
2aM the cap orbit has N points at spacing2a because gcd(C,N)=1.
The first exclusion ensures that coset misses the endpoints of the
open cap window of length2a. Exactly one of its points is inside;
choose its M and odd-A index m. The second exclusion ensures the
right residual is strict. Thus |z1|,|z2|<a also in this new upper
source case. Both K cases now supply the same three actual guards.

## 5. Correct period for the ACTUAL bottom target

The developed terminal phase has, in both source cases,

    E=z2+d2*tau
     =s+D*tau-2na-(2m+1)A-2kKa
     =z+2aJ, J integral.

For an upper source n=0; for a lower source it is its true source
period. This identity follows from the original q grid, not from
changing endpoints. Increase tau by2aNK. All residuals stay exactly
unchanged: lower-source n increases by NK*d0 (upper n remains0),
cap m by K*C, and right k by N*g1. Indeed the right pre-phase
increases by2aNK*g1=2Ka*(N*g1), its full actual period.

The target index J changes by NK*d2. Under gcd(NK*d2,L)=1,
choose p in{0,...,L-1} solving J+pNK*d2=0 modulo L. The finite
slope shift2aNK*p preserves every strict residual. Now

    E=z+2La*j,

so F_(La)(E)=z and the final actual abscissa is t=A-z. This is
matching the entire bottom width La, not only the narrow-arm residue.

## 6. Original physical trajectory

For a lower source use increasing developed eta from u to2H-v:

    u..h:             F_a(s+tau*(eta-u)),
    h..2H-h:          F_A(z0+tau*(eta-h)),
    2H-h..2H-c:       A-F_(Ka)(z1+tau*(eta-(2H-h))),
    2H-c..2H-v:       A-F_(La)(z2+tau*(eta-(2H-c))).

For an upper source start the cap formula instead at eta=u, with

    x(eta)=F_A(s+tau*(eta-u)), u<=eta<=2H-h.

Use the same right and bottom formulas afterward. Actual height is
eta before H, then2H-eta. Adjacent formulas agree locally in
position and SIGNED velocity: at a lower source portal |z0|<a<A;
at the cap exit |z1|<Ka<A and the odd-A identity gives A-|z1|;
at the last portal |z2|<Ka<La and both formulas give the same
local A-absolute-value. A zero residual is one smooth outer-wall
reflection. The u=h source seam has no fictitious positive-length band.

Strict portals avoid (a,h),(w,h),(w,c) and the ledge endpoints.
Actual open-band mirrors are exactly0/a between b,h;0/A in the
cap;w/A between c,h; l/A below c. All finite-wall intervals are
original walls. Every vertical reflection reverses only vx; at a
smooth roof the sole horizontal reflection reverses only vy.
Finite times, positive widths and finite tau give finitely many hits.

For u<=h a singular roof is impossible. Its triangular-wave symmetry
would equate the h-level mouth coordinates in [0,a) and(w,A],
which are disjoint. The argument includes u=h.

For u>h a formal singular roof MAY occur. Put B0=s+tau(H-u).
If B0 is a multiple of A, symmetry gives

    F_A(s+2tau(H-u))=F_A(s)=s.

Thus at eta*=2H-u the formal cap curve is exactly actual S=(s,u).
It satisfies H<eta*<2H-h. DISCARD the entire prefix through the
singular roof and use the suffix starting at eta*. Every remaining
cap point has h<=y<=u<H; its vertical-wall contacts avoid all roof
corners. All later portals and finite walls already satisfy the
proved strict guards. This suffix is a legal independently emitted
actual S-to-T ray; it never traverses the discarded corner, and no
singular continuation is postulated. This is the same actual-S
return device independently accepted in TR03, with exact formula here.

For a lower source, ascending points at target height lie at x<a<t;
cap heights are >v. After H, or throughout an upper-source suffix,
height decreases and meets v only at the end. For an upper source
even its initial height exceeds h>v. Hence every retained path
ends at FIRST actual T, with one common ray and no endpoint change.

## 7. Two whole native families with thick caps and unequal arms

Let a>=1 integral, 1<=K<L, prime N>=L+2, positive integral
epsilon=H-h with2epsilon<N, and integral0<b<c<h. Either choose

    (A) c=4, L>=3 odd, gcd(K,L)=1,
    OR (B) c odd, L=2^r for r>=1, K odd.

Then every distinct actual interior even-even pair illuminates.

For every native left-terminal source u<=h, C=2epsilon<N. For
every native source u>h, C lies between epsilon+1 and2epsilon-1,
also strictly between0,N. Prime N therefore makes gcd(C,N)=1.
This supplies K=1's requirement or K>=2's strict1<K requirement.
In family A each native bottom mark has v=2,d2=2; L odd and
gcd(K,L)=1, with prime N>L, give gcd(NK*d2,L)=1. In family B
each d2 is odd and N,K are odd, so it is coprime to the power2 L.
Every left-terminal/bottom pair satisfies the new lemma, including
all actual marks INSIDE the thick cap.

Accepted TR01 and TR05 protected coverage supplies every other pair
at all metrics. Their exact remaining placement after the join is
left terminal(0,a)x(b,H) versus bottom(l,A)x(0,c), precisely this
lemma. No native cap level is omitted. Label reversal is legal.
This is a quantified family proof, pending independent audit, not a
conclusion drawn from a single room or arithmetic sample.

It does not cover arbitrary ratios R/a,B/a,A/a, arbitrary cap gcds,
all endpoint heights, all ten-wall turn types, or r<=8. No failed
hypothesis establishes a dark pair. No discovery/clock renewal is used.
