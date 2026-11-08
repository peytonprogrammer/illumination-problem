# Next distinct extension: arbitrary commensurate source-arm width

Hand derivation offered to the existing author for construction/challenge; not independently accepted. No discovery run is proposed. This concerns a new P parameter, not another cap-gcd cutoff.

Replace the original source-arm width a by P*a0, retaining total width N*a0, right arm K*a0 and bottom arm L*a0. Require positive rational a0, positive integers P,K,L,N with2<=K<L and P<N-L (hence the source and bottom arms are strictly disjoint). Heights/actual ordinates remain integral and strictly ordered as in CE03. Actual terminal marks satisfy0<s<P*a0,b<u<H,(N-L)*a0<t<N*a0,0<v<c.

Let d0,C,g1,d2,D be CE03's developed heights and z=N*a0-t. The same initial grid

    tau_q=(N*a0+z-s+2*a0*q)/D

enforces final phase compatibility modulo2a0. Exclude source endpoint P*a0 modulo2a0 (only if u<h) and right endpoint K*a0 modulo2a0. These remain at two distinct times, so their integer q classes cannot cover; zero-duration source cases are empty/omitted. The exclusions are stronger than physical endpoints modulo2P*a0 and2K*a0, respectively, and hence suffice.

After source folding z0=s+d0*tau-2P*a0*n, preserve it by shifting tau by2P*a0*M. The cap orbit step is2*a0*P*C modulo2N*a0. Its spacing is2*a0*gcd(P*C,N). Therefore the new strict sufficient cap-access condition is

    gcd(P*C,N)<K.

The old condition gcd(C,N)<K cannot silently be reused. Nearest-coset selection then gives |z1|<K*a0, with the right endpoint exclusion preserved as before. The phase identity becomes

    E=z+2*a0*J, J=q-P*n-N*m-K*k

(with the q index updated when the slope is shifted).

Let Lambda=lcm(P,N,K). A final shift2*a0*Lambda preserves ALL residuals: source index increments Lambda*d0/P, cap index Lambda*C/N, right index Lambda*g1/K, all integers. The actual target index increments Lambda*d2. Thus the candidate sufficient target condition is

    gcd(Lambda*d2,L)=1.

The K=1 three-event source-offset argument is deliberately excluded: for P>1,0<s<P*a0 does not imply0<s/a0<1, so CE01's equal-block obstruction repair cannot be copied. For K>=2 the two-event noncover avoids that retired premise entirely.

Physical guards should carry over with |z0|<P*a0<N*a0, |z1|<K*a0, |z2|<K*a0<L*a0, and source/bottom separation P<N-L. Lower-source roof symmetry uses disjoint mouths[0,P*a0) and((N-K)*a0,N*a0]. Upper-source singular roof uses the SAME exact-source suffix since0<s<P*a0<N*a0, independent of P. First-target ascent exclusion uses s(t)<P*a0<(N-L)*a0<t. These require a complete author proof and independent review, not just these phase identities.

A potential whole-native family uses integral a0, odd P,K,N; K>=3; L a power of two with K<L; N prime>L+P; c odd and positive integral cap depth epsilon with2epsilon<N. Then gcd(P*C,N)=1<K for every native left source, and Lambda*d2 is odd, hence coprime to L. TR01/TR05 supply the other pair placements. This would remove the equal-left-width normalization from a restricted family and is strictly wider than CE03's P=1 geometry. No universal r3 conclusion follows.
