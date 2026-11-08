# CE02: actual-target signs cover both gcd-two cosets

Pending independent review. Geometry and hypotheses are exactly
two-sign-candidate.md, using the frozen CE01 proof sections1-4 for
the three-class noncover and coprime cap selection. Those steps do
not use gcd(N*d2,L)=1; it enters CE01 only in its final target step.

At their selected slope there are strict actual portal residuals
z0,z1,z2 in(-a,a), and the developed terminal phase is

    E=z2+d2*tau=z+2aJ, z=A-t, J integral.

Every slope shift2aN leaves all three residuals EXACTLY unchanged
and increases J by Nd2. Put g=gcd(Nd2,L). Within this invariant
period orbit, actual positive-image matching requires

    J+p*Nd2=0 mod L,

while actual negative-image matching requires

    J+p*Nd2=-r mod L, r=z/a.

The second condition is relevant here because r is an integer. Indeed
E=-z modulo2La is equivalent to J+r=0 modulo L. Both are images
of the SAME actual target under F_(La); no endpoint is substituted.

Now g=2 and r is odd. If J is even choose desired residue C=0
and target sign positive. If J is odd choose C=-r and target sign
negative. In either case C-J is even, and the congruence reduces to

    p*(Nd2/2)=(C-J)/2 mod (L/2).

Since gcd(Nd2/2,L/2)=1, a solution exists in0,...,L/2-1. For
L=2 the reduced modulus is1, so p=0 suffices. Otherwise use its
modular inverse. Replace tau by tau+2aN*p and change source, cap
and right indices by p times Nd0,G,Ng1. This preserves all three
strict residuals and every cap-return guard. The slope remains
positive and finite. Let J'=J+pNd2.

If C=0, E'=z+2La*j with j=J'/L. If C=-r,

    E'=z+2aJ'=-z+2La*j,
    j=(J'+r)/L integral.

Hence F_(La)(E')=z in BOTH cases, because0<z<La. The four-band
path in CE01 section6 reaches EXACT actual T=(A-z,v). In the
negative-image case its last horizontal velocity is +tau instead
of -tau. That is a legitimate arrival direction at an interior
target. The entire path still uses one common developed slope;
the signed portal identities are unchanged, and the fold in the
actual bottom width supplies that changed velocity without a splice.

All original finite walls, reflex/ledge exclusions, source u=h,
zero-residual smooth contacts and the roof-corner contradiction
remain exactly as in CE01. Nothing in those checks depends on
which target image was used. On ascent the path is in x<a<t
whenever its height might equal v; descending height reaches v
only at its end. Therefore first actual T is retained. Finiteness
follows from a finite shift and finitely many fold crossings.

For L=2, the only odd integer r in(0,L) is1, equivalently t=A-a=w.
Since N is odd, gcd(Nd2,2) is1 for odd d2 (CE01) and2 for even
d2 (CE02). Thus EVERY positive integral d2 is covered for this
centered bottom target, not just odd displacements. In the thin-cap
integral family H=h+1, all native terminal sources have u<=h and
all native targets have integral v. Protected TR01 covers the
other actual native source placements, as in the frozen family
join. This proves the stated all-source-to-bottom-center-column
corollary for ANY integral c, pending independent audit.

Limits: when g>2 two target residues need not meet every period
orbit. When r is nonintegral, the negative target-image condition
is not even in the same modulo2a phase coset, so this argument
cannot silently cover off-grid targets. These are limits of this
invariant orbit, not dark-room claims. Full r3/r<=8 remains open.
