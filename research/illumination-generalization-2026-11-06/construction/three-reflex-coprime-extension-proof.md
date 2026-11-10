# CE01: coprime bottom multipliers, including even displacement

Author proof pending independent review. This is an extension of the
coordinator's COORD-COPRIME-01 selection, whose source packet is preserved.
The reviewer separately owns that packet's audit. No independent acceptance is made for this extension.

## 1. Quantified geometry and target

Let integers L>=2,N>=L+2 and positive rational a satisfy

    A=Na, w=(N-1)a, l=(N-L)a.

Let integers 0<b<c<h<H satisfy gcd(2(H-h),N)=1. Thus
0<a<l<w<A and R=A-w=a, B=A-l=La. The original polygon has the
ten vertices in candidate.md, with strict simple ordered geometry.
Let actual rational S=(s,u), 0<s<a,b<u<=h, u integral, and actual
rational T=(t,v), l<t<A,0<v<c, v integral. Define

    d0=h-u>=0, G=2(H-h)>0, g1=h-c>0, d2=c-v>0,
    D=d0+G+g1+d2=2H-u-v, z=A-t in (0,La).

Assume gcd(N*d2,L)=1. No parity of d2 and no nonresonance of these
four developed heights is required. We construct a finite actual
one-roof path, corner-free with exact target T.

## 2. The finite initial grid and three forbidden events

Set

    tau_q=(A+z-s+2a*q)/D, q in Z.

For every q>=0 this slope is positive. Define t1=d0,t2=d0+G,
t3=d0+G+g1=D-d2. Exclude the following congruences modulo2a:

    s+t1*tau_q = a,
    s+t2*tau_q-A = a,
    s+t3*tau_q-A = a.

When t1=0, its event is empty since 0<s<a. For nonzero t_i,
0<t_i<D. Each event on integer q is either empty or exactly one
class modulo m_i=D/gcd(t_i,D)>=2. Indeed, subtracting two solutions
gives D dividing t_i times their difference; conversely translation
by m_i changes the left phase by an integral multiple of2a. This
argument remains valid for rational s,z,a. All moduli divide D.

We show these events cannot cover Z. Three classes with moduli>=2
can cover only if two moduli are2, all three are3, or the multiset is
(2,4,4). Here is a direct density justification. If the least modulus
is>=4 their summed density is<=3/4. If it is3, density forces all3.
If it is2 and the second is>=5, summed density is<1; if the second
is4, density forces the third to be4. If the second is3, the first
two overlap with density1/6 and cover2/3. A third modulus>=4 cannot
finish the cover. A second modulus3 as the third class yields at most
5/6, since each modulus3 class intersects the modulus2 class with
density1/6, and the two distinct modulus3 classes are disjoint (equal
classes only reduce the union). This proves the listed alternatives.

Two moduli2 are impossible: each corresponding time would equal D/2,
but the nonzero times t1<t2<t3 are distinct. Three moduli3 are also
impossible: their only possible times are D/3,2D/3. Fewer than three
nonempty classes cannot cover, since two classes would need to be the
two modulus2 classes, again impossible.

## 3. NEW: the (2,4,4) resonance is incompatible with actual source offset

The only remaining dangerous modulus multiset forces, in time order,

    t1=D/4, t2=D/2, t3=3D/4.

Consequently d0=G=g1=d2=lambda=D/4>0. We do NOT exclude this metric.
Suppose the cap event, the middle time, has an integer solution q_c.
Substitute tau_q into its left side:

    s+2lambda*tau_q-A = (s+z-A)/2 + a*q.

For this to be a modulo2a endpoint a, necessarily

    s+z-A=2a*r for some integer r.

For ANY integer q the source-event phase then becomes

    s+lambda*tau_q
       =(3s+A+z+2a*q)/4
       =(s+A+a*(r+q))/2.

If this were a modulo2a endpoint a, it would imply

    s/a + N + r + q = 2 + 4p

for an integer p. This is impossible because 0<s/a<1 while all
other terms are integers. Thus whenever the cap event is nonempty,
the source event is empty. If the cap event is empty, there are also
at most two classes. The dangerous three-class cover never occurs.

This is the new phase-offset fact: equal developed heights do not
force exclusion. It also explains why an odd d2 was not needed for
this covering step. Choose some q in {0,...,D-1} avoiding all events;
existence follows from the noncover proof and their D-periodicity.
Put tau0=tau_q.

## 4. Strict cap placement by the coprime N-orbit

Let

    n=floor((s+d0*tau0+a)/(2a)),
    z0=s+d0*tau0-2n*a, so |z0|<a.

Replace tau0 by tau0+2a*M. Since d0 is integral, z0 is unchanged
and n increases by d0*M. The cap phase X=z0+G*tau modulo2A
visits all N points of one lattice coset with step2a as
M ranges0,...,N-1, because gcd(G,N)=1. The cap's open return window
is A+(-a,a) modulo2A, length2a. The second forbidden-event exclusion
ensures the coset does not meet its endpoints: X=A+a modulo2a would
be that event, and shifts by2a*M preserve it. Hence precisely one
orbit point is strictly inside the window. Choose that M and an
integer m with

    z1=z0+G*tau-(2m+1)A, |z1|<a.

Next put

    k=floor((z1+g1*tau+a)/(2a)),
    z2=z1+g1*tau-2k*a.

Its residue is s+t3*tau-A modulo2a. The third event remains excluded
under the shift because t3 is integral, so |z2|<a strictly.

## 5. NEW: full actual-target correction modulo L

At this slope the terminal developed phase is

    E=z2+d2*tau
     =s+D*tau-2n*a-(2m+1)A-2k*a
     =z+2a*J,

with an integer J. The B=La fold reaches actual T if E=z modulo2La,
so it suffices to make J=0 modulo L. This is stronger than congruence
modulo2a; no target projection is substituted.

Increasing tau by2a*N preserves ALL portal residuals exactly. Its
source index changes by N*d0, cap index by G, and right index by
N*g1. Therefore E increases by2a*N*d2 and J increases by N*d2.
By gcd(N*d2,L)=1 there is a unique p in{0,...,L-1} with

    J+p*N*d2=0 modulo L.

Choose it (equivalently use the modular inverse of N*d2). Replace tau
by tau+2a*N*p and update n,m,k by p times those increments. All
three strict residuals are unchanged. Now E=z+2La*j for an integer j,
and F_(La)(E)=z. Here F_W(x)=distance(x,2W*Z). This is exact matching
to actual t=A-z, using its positive image sign. Target sign choices
and a monotone fixed-point iteration are unnecessary.

## 6. Physical path and all guards

Use one increasing developed height eta from u to2H-v. Its actual
height is eta up to H and 2H-eta afterward. On the four bands set

    u..h:             F_a(s+tau*(eta-u)),
    h..2H-h:          F_A(z0+tau*(eta-h)),
    2H-h..2H-c:       A-F_a(z1+tau*(eta-(2H-h))),
    2H-c..2H-v:       A-F_(La)(z2+tau*(eta-(2H-c))).

The first band has zero duration when u=h; then z0=s and the source
is the same exact actual interior mark. At the other portals, the
formulas agree locally in both position and signed velocity by the
even2a periods or the odd A center. A zero residual gives one smooth
outer-wall reflection, represented by the same local absolute value on
both sides. The strict a-bounds exclude all three actual reflex corners
and the convex ledge endpoints. Since B=La>a, the final portal has
the same local fold as the preceding a-band. No artificial wall is used.

The genuine vertical mirrors are x=0,a below h and above u>b;
x=0,A in the cap; x=w,A between c,h; and x=l,A below c. The sole
horizontal reflection is at y=H. A roof cusp would make the physical
x-coordinates at the two h-crossings identical by triangular-wave
symmetry. They instead lie in [0,a) and (w,A], disjoint. Thus no
roof corner occurs. Positive widths and finite tau give finitely many
wall contacts. Each ordinary fold reverses exactly its normal velocity.

The endpoint has actual height v and x=A-F_(La)(E)=A-z=t. During
source ascent, any visit to height v lies at x<a<t (since l>=2a).
The cap has height>=h>v; the descending path reaches v only at its
end. Thus this is first actual T. Reflections, period shifts and the
final congruence all belong to ONE straight unfolded ray, not a
concatenation of separately chosen directions.

## 7. Whole native family with EVEN bottom displacement

Take integer a>=1, odd integers L>=3,N>=L+2 with gcd(N,L)=1,
integers b in{1,2,3}, h>4, and c=4,H=h+1. Then G=2 is coprime
to N. Every actual even-even lowest-chamber point has v=2, so d2=2
and gcd(N*d2,L)=1. Every actual even-even source in the left terminal
has integral u<=h, since no integer level lies strictly inside the
cap h<y<h+1. Therefore the lemma applies to ALL residual terminal
pairs, including h=6,u=4, the equal-four-heights resonance.

All other native pairs are supplied by the independently accepted
TR01 protected U/L coverage. Its unhandled upper-cap placements are
absent at integer heights; its seam u=h is included by this lemma.
Reversing a finite regular ray treats label reversal. This is the author's
whole quantified native claim, pending independent audit. Its quantifiers
follow from the hand construction, not from the prescribed controls.

A second whole-native corollary, also suggested by the existing reviewer,
is L=2^r for any integer r>=1, N>=L+2 odd, c odd, H=h+1, with all
other integer strict orders as above. Then every native d2=c-v is odd,
so gcd(N*d2,L)=1 automatically. The same terminal construction and
protected coverage prove every native pair in this entire family. This
includes the coordinator's L=2 case and adds all larger power-of-two
bottom multipliers; it does not remove arbitrary coprimality conditions.

For example a=4,L=3,N=5,b=1,c=4,h=5,H=6 gives geometry (a,l,w,A;b,c,h,H)=(4,8,16,20;1,4,5,6). Both old TR04 sufficient bounds fail (required H>=404, required A>=484). Its eight native marks and28 pairs are a prescribed verification fixture, not the quantified proof. This family neither closes all (1,1,8), all W10/r3, nor r<=8. No actual dark pair or external refereeing is supplied.
