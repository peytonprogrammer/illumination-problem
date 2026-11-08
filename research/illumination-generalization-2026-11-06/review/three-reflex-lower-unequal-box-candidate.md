# UB01: a target-compatible unequal-arm half-open box

Reviewer-owned quantified candidate, written before prescribed verification.
Author LJ03's equal-arm construction remains author-owned and frozen.

Use ordered spiral a=Pe,R=Ke,A=Ne,B=Le with positive integers
1<=P<=K<L, N>P+L, N odd, L a power of two>=2. Let
g=gcd(lcm(P,N,K),L); impose BOTH g<=P and g|K. The latter condition is
essential and must not be inferred from g<=P alone. Equivalently
nu2(P)<=nu2(K) and 2^nu2(K)<=P. Take rational e>0, integer
0<b<c<h<H with h even,c odd. Actual horizontal marks are rational,
0<s<Pe, b<u<h, (N-L)e<t<Ne, 0<v<c; u,v are even integers.

Claim: every such lower pair illuminates. For alpha=(h-u)/2,
beta=H-h, f=(h-v)/2, d=alpha+beta+f, use q=Pi+Nm+gj.
Residual generators are

    vi=(2eP/d)(-(beta+f),-f),
    vj=(2eg/d)(alpha,alpha+beta).

Uniform half-up rounding gives each component STRICTLY smaller in absolute
value than its half absolute sum. The source bound is <=Pe because g<=P;
the cap bound is <=Pe<=Ke. Positive kernel with
H0=gcd(Ng*alpha,Pg*beta,PN*f) preserves both residuals; nu2(H0)>=nu2(P)
implies its right-return ratio g1PN/[2(K/g)H0] is noninteger.
J=gj-Kk is divisible by g and the full period 2e*lcm(P,N,K) solves actual T.

Whole native corollary: e any positive integer, all remaining room hypotheses
as stated. UJ01 covers terminal source at/above h, and TR01/TR05 plus reversal
covers complementary placements. Thus every distinct native pair illuminates
in this unequal-arm family, with arbitrary vertical metrics at the stated
parities. No cap gcd, size or reflection cap is imposed.

Three prescribed exact inputs, no discovery:

1. e2,P3,K6,L8,N13,b1,c3,h6,H12,S(2,4),T(14,2).
   Rounded i1,m0,j0,q3 yields tau8/3,z0=-14/3,z1=4/3,z2=28/3,J0.
2. SAME first widths/b,c,h,S but H24,T(12,2). Initial i0,m0,j=-1,q=-2
   requires the positive null shift; this checks actual index restoration.
3. e2,P2,K6,L8,N11,b1,c3,h6,H12,S(2,4),T(10,2).
   Rounded i1,m0,j=-1,q0 gives tau16/9,J=-2. Full-target correction p1
   has Lambda66, so final tau2392/9. This tests even P and a nonzero correction.

Strongest objections: retain g|K explicitly, prove nu2(H0)>=nu2(P) rather
than odd-P reasoning, identify actual source/cap/right indices, and check
original roof/seams/first target. The algebra is a finite exact construction,
not a new engine or search. Independent author review required. Full r3/r<=8
and mixed canonical45 remain open; no clock is opened.
