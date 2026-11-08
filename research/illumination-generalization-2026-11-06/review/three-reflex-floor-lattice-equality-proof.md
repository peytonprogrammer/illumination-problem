# FE01: two source columns remove the exact fiber corner obstruction

Use exactly candidate.md's hypotheses and notation. The original actual
floor-loop source/cap/root lattice is already independently accepted in
LJ01_LATTICE. Its generators in integer coordinates are

    v0=(-P(n+f),-Pf), v1=(Nr,-Nf), v2=(gr,g(r+n)),

with physical scale 2e/d and offset (C0,C1)/d from that proof. Their pair
minors have gcd dH0. The constructive Bezout proof supplies an actual lattice
vector w=(Hx,Y) and the vertical generator v=(0,Fy), Fy=dH0/Hx, with
integer preimages in (source index,cap index,j). Every original generator
has form (vi_x/Hx)*w + (0,m_i*Fy), m_i integral; conversely w,v are
integer combinations of the generators. Thus they form a full basis of
the exact source/cap lattice, not a larger auxiliary image lattice.

The gcd of the y components of all original generators therefore equals

    Hy=gcd(Pf,Nf,g(r+n))=gcd(Y,Fy).

This follows in both directions from the integer basis relations. The new
hypothesis Hy<Fy is equivalent to Y NOT being a multiple of Fy. Hence
adjacent source columns differ in cap phase by (2e/d)Y, which is NOT an
integer multiple of its fiber mesh (2e/d)Fy.

At equality H0=K*Hx the fiber mesh is exactly2Ke, the full cap-mouth
window width. In each fixed source column, choosing the nearest vertical
fiber gives |z1|<=Ke; failure of strictness occurs at exactly the single
class Ke modulo2Ke. Two adjacent columns cannot BOTH have that class,
since their difference is a noninteger multiple of the full mesh.

It remains to place both adjacent columns strictly within the ACTUAL source
window. Its lattice column spacing is Delta_x=2eHx/d. Choose the nearest
column to center0, with source residual x0 satisfying |x0|<=Delta_x/2.
Choose its adjacent column toward zero (if x0=0, choose either side).
That column's residual has absolute value <=Delta_x. Since P*d>2Hx,
Delta_x<Pe, so BOTH columns lie strictly inside the source window.
They are distinct consecutive columns, represented by two actual integer
triples. Center each cap fiber independently. At least one column has
strict |z1|<Ke. Choosing that one proves simultaneous STRICT source/cap
entry in the nominated complete target-compatible lattice at EVERY offset.
This is a two-column covering argument, not a covolume conclusion.

All remaining optical steps are exactly those independently established
in LJ01_LATTICE, with no use of its now-replaced strict covering inequality.
In detail the positive kernel

    (Delta_source,Delta_cap,Delta_j)=(rNg,nPg,fPN)/H0

has positive integral entries, preserves both literal residuals, and changes
q by PNgd/H0 and slope by ePNg/H0. Finite ceilings make source/cap/q
nonnegative, so the selected residuals identify actual folds at positive
slope. One more kernel step cannot preserve the true right-corner class:
its right phase/full-period ratio (h-c)PN/[2(K/g)H0] is nonintegral by
odd numerator/even denominator. Thus strict |z2|<Ke is also available.

At actual right index k, J=gj-Kk is divisible by g. The final common slope
period2eLambda preserves every signed residual with integral fold increments
and changes J by Lambda(c-v). Its quotient by g is a unit modulo L/g,
so finite p gives E=+z modulo2Le, reaching actual t=A-z. All selections
occur before one final common slope is emitted; no path concatenation.

Only true left-floor/left-wall/cap/roof/right/bottom contacts are used.
At the FINAL slope a formal left-floor corner is removed by exact fold
symmetry: at elapsed2(u-b) the path is again at actual S with velocity
(-tau,+1). Since h-u>=0, the remaining suffix begins before or at the
regular ascending h entry, also when u=h. Emit only that suffix; it never
traverses the discarded corner. Otherwise the real left-floor reflection
is ordinary. The strict h positions are in disjoint original left/right
mouths, so a true roof corner is impossible. Signed position/velocity match
at every seam, including zero residual as one smooth outer-wall reflection.
Source x<=a<l<t prevents early T, cap/right heights exceed v, and the
bottom first reaches v at its last time. Finite widths/time/slope give
a finite legal actual S-to-T path with no artificial mirror or true corner.

## Whole native thin-cap family

Take integral e,P,N odd coprime,K2,L power of two>=4,N>P+L,
b1,c3,h6,H7. Then g=2,n=1,f=2 for all native bottom targets v2.
The exact terminal source levels are u2,u4,u6, giving r3,r4,r5 and d=r+3.
For these levels

    H0=2*gcd(P,r), Hy=2*gcd(P,N,r+1)=2.

At r3, Hx=gcd(3P,3N,6)=3. If 3 does not divide P, H0=2<2Hx,
so the already accepted strict theorem applies. If 3 divides P, H0=6=2Hx,
Fy12>Hy2 and Pd=6P>6=2Hx because P>=3; FE01 applies.

At r4, Hx=gcd(3P,4N,8)=1 and H0=2. This is equality, with Fy14>Hy2
and Pd=7P>2Hx; FE01 applies for every odd P.

At r5, Hx=5 if5|P and1 otherwise, while H0=10 or2 respectively.
Thus H0=2Hx always, Fy16>Hy2 and Pd=8P>2Hx (if5|P, P>=5).
FE01 again applies, including the actual mouth u=h6.

There is no native level strictly between h6 and H7. Therefore every
residual actual terminal pair is covered by strict LJ01_LATTICE or FE01.
TR01/TR05 protected original-wall constructions and reversal cover every
complementary pair. Every distinct native pair illuminates in this whole
family, including arbitrarily large odd P>K2 and arbitrary integral e.
No cap coprimality, size or reflection bound is added. Other metrics,
parities, forms and all r3/r<=8 remain open. Independent review is pending.
