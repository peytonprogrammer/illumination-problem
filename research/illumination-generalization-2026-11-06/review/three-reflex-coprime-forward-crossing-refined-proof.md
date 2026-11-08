# LC01R full hand proof: the first cap threshold forces a legal grid index

Reviewer-originated claim awaiting independent reciprocal review. Frozen LC01 remains correct as a weaker sufficient proof.

Use LC01R candidate notation. For every integerq>=0 set

    tau(q)=(A+z-s+2eq)/D,
    n(q)=floor((s+d0*tau(q)+a)/(2a)),
    z0(q)=s+d0*tau(q)-2a*n(q),
    X(q)=z0(q)+C*tau(q), hstep=2e(d0+C)/D.

Here a=Pe,A=Ne. For ALL q, including algebraically bad indices, -a<=z0<a and n is nondecreasing. Hence X tends to infinity and X(q+1)-X(q)<=hstep<2e. The actual source corner event Sbad is s+d0*tau(q)=a modulo2a. Its integer solution set is empty or one class modulo

    pS=PD/gcd(d0,PD)>P>=1.

The right sufficient strong corner event Rbad is s+(D-d2)*tau(q)-A=Ke modulo2e. Its solution set is empty or one class modulo

    pR=D/gcd(D-d2,D)>=2.

These are consequences of subtracting two solutions, valid also for rational offsets. The source condition now uses its actual period2a; there is no requirement to avoid extra regular source phases.

Choose m>=0 sufficiently large that U=(2m+1)A+Ke > X(0)+4*hstep. Let q* be the FIRST q with X(q*)>=U. It exists and q*>4. For any j>=1 with q*-j>=0, firstness gives X(q*-j)<U and the upper increment bound gives X(q*-j)>=U-j*hstep. The physical cap window is (U-2Ke,U), of width at least4e.

At any source-bad integerq>=1, z0(q)=-a. The source increment before folding is 2e*d0/D, strictly between0 and2e<=2a. Therefore n(q)=n(q-1)+1 exactly, and

    X(q)-X(q-1)=hstep-2a<0.

In particular q* CANNOT be source-bad, since its predecessor is belowU. This reset identity is material, not an optional observation about labels.

## Case 1: pR=2

Then D-d2=D/2, so d0+C<D/2 (becauseg1>0). Thus hstep<e and all FOUR indices q*-1,...,q*-4 lie strictly inside the same cap window: 4*hstep<4e<=2Ke. Also pS cannot equal2. Indeed pS2 would force P1,d0=D/2, contradicting d0<D-d2=D/2.

One class of period2 and one of period>=3 cannot cover four consecutive integers. The period2 class leaves two indices a distance2 apart; a class of period>=3 cannot contain both. Therefore some cap index avoids both events.

## Case 2: pS=2

From PD/2=gcd(d0,PD)<=d0<D follows P1. Since 0<d0<D, gcd(d0,D)=D/2 forces d0=D/2. Consequently C<D/2, pR>2, and the source phase has exact two-step period:

    tau(q+2)-tau(q)=4e/D,
    n(q+2)-n(q)=1,
    z0(q+2)=z0(q),
    X(q+2)-X(q)=4e*C/D in(0,2e).

The already proved source-good q* therefore has source-good predecessors q*-2 and q*-4. Both are strictly belowU by firstness and strictly above U-4e by the two-step increment, hence inside the cap window. Their separation is2, so a right-bad class of periodpR>2 cannot contain both. Select the surviving index. The argument also holds when either event is empty; the phase identity follows from dimensions regardless of offsets.

## Case 3: pS,pR>=3

Both q*-1 and q*-2 are cap-interior since2*hstep<4e<=2Ke. If either avoids both events, select it. Otherwise the two distinct bad indices must have one Sbad and one Rbad: neither event class can contain adjacent indices, and an overlap of both events at one would leave the other clear.

The source-bad index among those two causes at least one increment of n between q*-3 and q*. Thus telescoping the EXACT phase formula gives

    X(q*-3)=X(q*)-3*hstep+2a*(n(q*)-n(q*-3))
            >= U-3*hstep+2a > U-4e >= U-2Ke.

Firstness gives its strict upper bound. Its distances from the two bad indices are1and2, less than BOTH periods. Therefore q*-3 is neither source-bad nor right-bad, and is a legal cap-interior choice.

These three cases exhaust all periods. Each selected q is positive, has strict actual source residual |z0|<a and strict cap residual |z1|<Ke at the SAME odd center m. The strong right condition gives strict |z2|<Ke after the actual right fold. No source-direction concatenation is used.

## Exact target and genuine walls

As in LC01/CE04, the seeded identity gives E=z+2eJ with integer J=q-Pn-Nm-Kk. Choose0<=p<L solving J+Lambda*d2*p=0 moduloL. This exists by the stated gcd. Add2eLambda*p to tau and integral increments Lambda*d0*p/P, Lambda*C*p/N, Lambda*g1*p/K to n,m,k. ALL three literal signed residuals remain unchanged. Thus the physical original source/cap/right/bottom charts join in both position and signed velocity and reach the specified actual target, with E=z modulo2Le. Every wall is original, all true reflex corners are excluded, zero residuals are smooth outer-wall contacts, and ascending/descending h mouths are disjoint, excluding a lower-source roof corner. The source band stays aboveb, the bottom band above0; target heightv can occur on ascent only withx<a<l<t, and on descent only at the final time. The final ray has one positive finite slope, finitely many ordinary reflections, and first actual T.

## Entire native family and unresolved scope

For integral e and odd P,N,K>=3 with K<L=2^j,N>P+L,codd, every native bottomv is even, so d2odd and Lambdaodd give targetgcd1. LC01R covers every below-h terminal source; accepted CE08 covers at/above-h sources with its cap Lambdaodd/g1 and KD/C>K>=3. Accepted TR01/TR05 and reversal cover all other pairs in this ordered original geometry. There is NO remaining cap-gcd, prime-N or cap-depth requirement in THIS family. This corollary requires independent LC01R acceptance and does not prove arbitrary target arithmetic, all ordered spirals, other r3 forms/types or the native r<=8 target. No darkness is inferred for any omitted metric.
