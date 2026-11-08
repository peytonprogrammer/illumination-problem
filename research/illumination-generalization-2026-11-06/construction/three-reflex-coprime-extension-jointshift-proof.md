# CE07 hand proof: source and target-grid compatibility during cap selection

Scope: jointshift-candidate.md, independent review pending. The original
geometry has source widthPe,cap widthNe,right widthKe,bottom widthLe,
with0<Pe<(N-L)e<(N-K)e<Ne. Source and target are actual interior
terminal marks. All source/target ordinates and room heights are integral.

## 1. Choose a strict initial source/right grid

Take tau_q=(A+z-s+2e*q)/D with q>=0. As in accepted CE04,
exclude source endpoint Pe modulo2e at time d0 only when u<h,
and exclude the strong right endpoint Ke modulo2e at time
 t3=D-d2=d0+C+g1.
Their distinct nonzero times in(0,D) imply at most two nonempty classes
with periods>=2 that cannot both be2. Thus there exists q in0..D-1
avoiding them. At u=h and u>h omit the source event and set n=0,z0=s.
Otherwise fold using the full source period2Pe, giving |z0|<Pe.
The cap flight is C>0; no final target-gcd or cap-gcd hypothesis was
used in this initial selection.

## 2. The fractional shift retains ALL needed conditions

Let F=gcd(d0,P*D,P*d2)>0 and Qsrc=P/F. Then

    Qsrc*d0/P=d0/F is an integer,
    Qsrc*D=P*D/F is an integer,
    Qsrc*d2=P*d2/F is an integer,
    Qsrc*t3=Qsrc*(D-d2) is an integer.

Consequently a slope change2e*Qsrc*M, M integral, leaves the source
signed residual z0 identical: the lower-source index changes by d0*M/F.
For an upper source d0=0 and n remains0. It also advances the ORIGINAL
q grid by Qsrc*D*M, an INTEGER, preserving the initial endpoint phase
compatibility. The strong right endpoint event modulo2e is unchanged
because Qsrc*t3*M is integral. The source event stays strict through
literal z0 equality (and also Qsrc*d0 is integral).

It is NOT necessary that the cap or right residual already be preserved;
cap selection is precisely the step still being made. Keeping only the
source while losing the target grid/right guard would not prove this lemma.

## 3. Strict cap access with the finer phase orbit

Let X0=z0+C*tau_q. The new cap phases are

    X0+(2e/F)*P*C*M modulo (2e/F)*N*F.

Put gcap=gcd(P*C,N*F). This is one coset of spacing2e*gcap/F,
with N*F/gcap points. Choose an integer r nearest to
(A-X0)/(2e*gcap/F), and let Y=X0+(2e*gcap/F)*r.
Then |Y-A|<=e*gcap/F<Ke by the stated strict hypothesis.
A nearest-point tie is harmless. The reduced inverse solves

    (P*C/gcap)*M=r modulo N*F/gcap

with0<=M<N*F/gcap, making X=X0+(2e/F)*P*C*M differ from Y by
an integer multiple2Ne. Thus X=(2m+1)Ne+z1 with |z1|<Ke.

The right pre-phase z1+g1*tau differs modulo2e from the same original
expression s+t3*tau-A: removed source/cap periods are2e times the
integers P*n and N*m. The strong right event was preserved in section2.
Therefore this pre-phase is not Ke modulo2e and hence not Ke modulo2Ke.
The actual right fold has |z2|<Ke, as required.

Because the updated q is integral, the terminal phase still has
 E=z2+d2*tau=z+2eJ with J an integer. No rational J or missing actual
target image has been hidden by cap refinement.

## 4. Correct the actual target, then apply the original physical charts

Let Lambda=lcm(P,N,K). The accepted slope increment2e*Lambda
keeps the now strict source/cap/right residuals IDENTICAL and increments
J by Lambda*d2. The assumed gcd gives p in0..L-1 with
J+pLambda*d2=0 modulo L. The final bottom phase equals z modulo2Le
and folds to actual x=A-z=t. All slopes remain finite positive.

The original CE04 four-band charts, at source widthPe,cap widthNe,
right widthKe,bottom widthLe, now have exactly their proved strict
portal hypotheses. They agree in position AND signed velocity at each
interface; a zero residual is a smooth outer-wall reflection. Each
open-band contact is on an original finite wall; no ledge, reflex corner,
artificial cut or projected sheet substitutes for the actual geometry.
Lower-source roof corners contradict the disjoint h-mouth symmetry.
For an upper source, evaluate the FINAL slope: if the formal roof is
singular it returns at eta*=2H-u to EXACT actual S; emit its regular
descending suffix only, traversing no corner. The construction is one
ray with one final absolute slope. Initial ascent cannot hit T because
x<=Pe<l<t, cap/right heights exceed v, and descent reaches v only at
its final time. Thus the target is first actual T; positive widths and
finite slope give finite ordinary specular reflections.

## 5. Entire new native family with composite cap width

Take e>=1 integral,odd P,odd L>=3,gcd(P,L)=1,K2,N=2^m>P+L,
integer0<b<c4<h,h even,H=h+1. Native u is even and there is no
integral source level strictly inside the height-one cap, so u<=h.
Hence d0=h-u is even,C2,d2=2 and D=2H-u-2 is even.
Since F=gcd(d0,P*D,2P) is even and divides2P, write F=2d with d|P.
Now

    gcap=gcd(2P,N*2d)=2*gcd(P,N*d)=2d,

because P is odd,N is a power of two and d divides P. Therefore
 gcap/F=1<K2.
The finer cap orbit works for EVERY native terminal source and target.
Lambda=P*N, since P is odd and N is a power of two. L is odd and
coprime to P,N, so gcd(Lambda*d2,L)=gcd(2PN,L)=1 for every pair.
Thus the terminal theorem covers the entire remaining left-terminal /
bottom placement. Original TR01/TR05 cover all other actual pairs,
with reversal for opposite labels. No size/support/reflection cap is used.
The old integer-source-shift cap gcd is gcd(PC,N)=gcd(2P,N)=2=K,
and K does not divide odd P, so this family is outside CE04/CE05's
sufficient cap selection hypotheses. The new joint refinement supplies
actual coverage, rather than only a rewritten root formula.

## 6. Prescribed exact native control

Use e4,P1,K2,L3,N8,b1,c4,h6,H7,S(2,4),T(26,2).
Then A32,a4,R8,B12,l20,w24,d0=C=g1=d2=2,D8,z6,F2,Qsrc1/2.
Choose q1,tau11/2. The source index n2 gives z0=-3, and X0=8.
Under the older source-preserving step2Pe=8 the cap orbit has phases
8,24,40,56 modulo64: NO point lies in the strict window(24,40).
Under the NEW step2eQsrc=4, M3 gives tau35/2 and X32 exactly,
with n5,m0,z1=0,k2,z2=3. Then E38=z6+8J,J4.
Lambda8,d2=2,p2 supplies tau291/2,J36,E294=6 mod24.
The final actual target is (26,2). The zero cap residual is a smooth
outer-wall hit, and all strict portal residuals remain unchanged.
This is a prescribed evaluation of the hand formula, not a discovery
search or proof from a single example.

Whole spiral/r3/r<=8 remains open; other cap/target classes are not
excluded by failure of these sufficient hypotheses. No discovery clock
was opened, renewed or renamed.
