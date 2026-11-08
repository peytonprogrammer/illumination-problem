# LC01R: all right widths K>=2 by first crossing and true source guards

Hand refinement of frozen LC01; not a new discovery effort. Reciprocal review required. Preserve LC01 proofs/checks/receipt unchanged.

Same original ordered spiral, integer P>=1,2<=K<L,N>P+L, positive rational e, integer0<b<c<h<H. Rational actual S=(s,u),T=(t,v),0<s<Pe,b<u<h,(N-L)e<t<Ne,0<v<c,integeru,v. Set d0=h-u,C=2(H-h),g1=h-c,d2=c-v,D=2H-u-v,z=Ne-t,Lambda=lcm(P,N,K). Assume gcd(Lambda*d2,L)=1.

Claim: actual S illuminates actual T with no cap-gcd, prime-N or cap-depth condition. Use LC01 first-crossing X(q), but avoid the TRUE source endpoint event modulo2Pe rather than its stronger surrogate modulo2e. Its period pS=PD/gcd(d0,PD)>P. The right strong event retains period pR=D/gcd(D-d2,D)>=2. At the first cap upper-threshold crossing q*>4, a legal index exists among q*-1,...,q*-4:
- pR2 forces hstep<e, so four prior indices lie in the same cap window and the old four-block lemma applies.
- pS2 forces P1,d0=D/2. q* is source-good since a source-endpoint reset decreases X. The same-source-phase indices q*-2,q*-4 lie in the window, and pR>2 cannot reject both.
- pS,pR>=3: if last two are both bad they have one source event and one right event. The source reset makes q*-3 lie in the window despite the crude forward bound, and its distance1or2 from the bad indices avoids both.

Full native corollary using accepted CE08/TR01/TR05: integral e, odd P,N,K with K>=3,K<L=2^j,N>P+L,integer0<b<c<h<H,codd; ALL distinct actual interior even-even pairs illuminate for arbitrary H-h and composite N. This is an ordered-spiral family, not all r3/r<=8.

Prescribed deterministic controls: all three frozen LC01 fixed rays; existing CE07 e4/P1/K2/L3/N8,b1c4h6H7,S2,4,T26,2; existing CE04 e1/P2/K2/L3/N7,b1c4h5H6,S1,4,T5,2. Two hand-fixed resonance controls: e4/P1/K2/L3/N8,b1c5h6H7,S2,2,T26,4 has pS2; same widths b1c7h8H9,S2,6,T26,2 has pR2. These seven constructor replays are prescribed before execution, not room/ray discovery or a census.
