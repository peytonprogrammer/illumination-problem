# General upper full-divisor subsumption, including non-dyadic bottom widths

This supplements upper-subsumption.md without changing that published proof or its pins. It proves a general implication between accepted sufficient criteria; it does not assume or prove that the full-divisor premise holds universally. No new specialized optical family, numerical example, search or engine is introduced. Reciprocal review is requested.

## Quantified arithmetic statement

Let N,K,L,C,G,d be positive integers, F=G+d, and define

    g=gcd(lcm(N,K)*d,L),
    Hprime=gcd(NF,CK,CL),
    Zprime=gcd(NKd,NLG,KLC).

If g divides K, then Zprime divides K*Hprime.

If additionally C,F are even, G,d are odd, and nu2(N)<=nu2(K), then the integer quotient (K*Hprime)/Zprime is even. In particular

    Zprime<=K*Hprime/2<K*Hprime.

The first divisibility statement has NO parity assumption and L need not be dyadic. The second gives strictness throughout the common native UJ01/UJ02 domains. All quantities are original metric/time data, not selected sheet labels.

## Proof of the divisibility, prime by prime

For an arbitrary prime q write n,k,l,c,g0,d0,f for the valuations of N,K,L,C,G,d,F. Then

    Hval=min(n+f,c+k,c+l),
    Zval=min(n+k+d0,n+l+g0,k+l+c).

Case l<=k. The third term gives both Zval<=k+c+l and Zval<=k+c+k. Also

    min(k+d0,l+g0)<=k+min(d0,g0)<=k+f,

because l<=k and the valuation of G+d is at least min(g0,d0), including cancellation. Thus the first two terms give Zval<=k+n+f. Combining these three bounds gives Zval<=k+Hval.

Case l>k. The hypothesis g|K says

    min(max(n,k)+d0,l)<=k.

Since l>k, it forces max(n,k)+d0<=k, hence n<=k and d0=0. The first term now gives Zval<=n+k. This is at most each of k+n+f, k+c+k and k+c+l, so again Zval<=k+Hval.

These are all primes and both order cases. Therefore Zprime|K*Hprime. No inference from a small determinant to box intersection is used.

## Strictness at two, including equality cases of the generic bound

Now n<=k, d0=g0=0 and c,f>=1. If l>k, then

    Zval=n+k,
    Hval=min(n+f,c+k)>=n+1.

Thus nu2(K*Hprime)-nu2(Zprime)>=1.

If l<=k, then

    Zval=n+l,
    Hval=min(n+f,c+l),
    k+Hval-Zval=min(k+f-l,k+c-n)>=1.

Thus the quotient has a factor2 in either case. This strict conclusion includes L odd (l=0), K with arbitrary odd part, and every possible odd-prime cancellation in G+d.

## Exact original-room consequence and coverage consolidation

In GSE03 upper notation, A=Ne,R=Ke,B=Le give H0=e*Hprime,Z0=e^2*Zprime. At the shared native/integral-room domain and upper or strict-mouth source,

    C=2H-h-u, G=h-c, d=c-v, F=h-v.

For h even,c odd and actual even u,v, C,F are even and G,d are odd. Hence g|K and nu2(N)<=nu2(K) imply the accepted GSE03 condition Z0<R*H0 automatically, with a factor2 margin. Its already reviewed joint lattice selection supplies actual S-to-T, strict cap/right passage, positive indices, finite genuine walls, u=h handling, final exact-S roof suffix and first target.

Every shared-native UJ01 upper claim has N odd, so nu2(N)=0<=nu2(K), with its explicit g|K. It is therefore subsumed, INCLUDING its non-dyadic-L branch. UJ02 assumes L dyadic and nu2(N)<=nu2(K), which establishes g|K at its own hypotheses, so it too is subsumed. UC01 and the older upper-depth restrictions are included through these containments. This is a consolidation of their accepted results, not a claim of new optical coverage requiring additional family examples.

Keep separately any broader rational-width or upper-source placement statements beyond GSE03's declared domain. The raw GSE03 source range here is 0<s<a and u>=h; this supplement does not silently enlarge it to every cap abscissa. Also retain all lower-source/equality/real-metric routes and global isometries at their established scopes.

## Precise remaining gap

There is no proof that g|K or nu2(N)<=nu2(K) holds for every residual pair after some permitted representation. Even when either fails, GSE03 may succeed directly, or other accepted routes may apply. Conversely a sufficient flag bound failing does not mean its full affine state lattice is infeasible. Full ordered-spiral availability is still the existential union over exact states/programs, with both actual target images and all physical guards.

The complement audit can now eliminate duplicate UJ01/UJ02/UC01/depth predicates at the SHARED native domain in favor of the single GSE03 predicate. It cannot yet eliminate every lower legacy route or turn the remaining sufficient-hypothesis complement into a darkness condition. All ordered/r3/r<=8 targets remain OPEN.

This is hand algebra only; no new numerical check, discovery, clock, worker, census, fitting, frozen edit or git mutation occurred.
