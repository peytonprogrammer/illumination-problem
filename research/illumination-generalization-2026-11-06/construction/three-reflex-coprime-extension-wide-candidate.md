# CE03: wider right arms and sources inside a thick cap

Positive candidate before prescribed checks. Existing CE01/CE02 packets
remain frozen. This is not an all-r3 claim.

Let integers 1<=K<L, N>=L+2, a>0 rational, and

    A=Na, w=(N-K)a, l=(N-L)a, R=Ka, B=La.

Let 0<b<c<h<H be integers. Take actual rational S=(s,u),T=(t,v)
with 0<s<a,b<u<H,l<t<A,0<v<c and integral u,v. Put

    d0=max(h-u,0),
    C=2(H-h) if u<=h, else C=2H-h-u,
    g1=h-c, d2=c-v, D=d0+C+g1+d2=2H-u-v.

Assume gcd(N*K*d2,L)=1 and either

    K=1 and gcd(C,N)=1, OR
    K>=2 and gcd(C,N)<K.

Claim: a finite ordinary corner-free actual S-to-T path exists. It uses
one smooth roof hit, or a zero-roof legal suffix starting again at SAME
actual S when an upper-cap formula has a singular roof prefix.

Missing implications to prove:

1. For K>=2, a spacing2a*gcd(C,N) cap orbit has a point strictly in
   its window of radiusKa; the strict inequality on the gcd guarantees
   it even if the old endpoint exclusion fails. Only source and right
   congruence exclusions are needed, and two distinct-time residue
   classes cannot cover the initial q grid.
2. For K=1 and u>h, only cap/right exclusions remain; two classes again
   cannot cover. K=1,u<=h is the already accepted CE01 selection step.
3. Shift2aNK preserves the RIGHT residual of widthKa as well as source
   and cap residuals. It increments target index J by NK*d2; its
   coprimality with L gives actual target matching in bottom widthLa.
4. Upper-left cap sources need the exact actual-S return argument when
   the roof is singular. No corner traversal belongs to the retained ray.

Whole native families proposed: integral a, prime N>=L+2, positive
integer epsilon=H-h with2epsilon<N, integral0<b<c<h. Either

    c=4, L>=3 odd, gcd(K,L)=1,
    OR c odd, L=2^r (r>=1), K odd.

Then EVERY distinct actual interior even-even pair illuminates. The
thin-cap restriction is removed; all original cap-source placements
are handled using this lemma and accepted TR01/TR05 coverage.

Strongest objection: an admissible phase orbit does not by itself give
legal original walls, and deleting a singular roof prefix is valid only
if the retained start is exactly actual S with a legal departing velocity.
Success requires those proofs and full target-period matching.

Prescribed whole-room control, declared here before checks:
(a,l,w,A;b,c,h,H)=(4,8,12,20;1,4,5,7), K=2,L=3,N=5.
It has19 native marks/171 pairs, including15 terminal and25 additional
upper-cap TR05 pairs. Singular-roof control S=(2,6),T=(10,2) uses
q=4,M=1,tau=18; its formal roof corner is discarded by restarting
at SAME S at developed eta=8. These controls are corroboration, not
the quantified proof. No discovery effort or new clock is proposed.
