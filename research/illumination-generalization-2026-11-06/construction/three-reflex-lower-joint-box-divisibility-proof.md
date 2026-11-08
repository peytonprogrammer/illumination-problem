# LJ02: an exact sufficient condition for strictness of the lower joint box

Independent review pending. This is a logical extension of LJ01_BOX, preserving every frozen source. It does not claim the divisibility condition is necessary for illumination.

Use the original geometry and variables of LJ01_BOX proof sections1--2,4--5: P=K1,Nodd,Lpower2,positive rational e,integer0<b<c<h<H,h even,c odd,actual rationalhorizontal source0<s<e andtargetl<t<A,even integerheights b<u<h,0<v<c. Letbeta=H-h be ANYpositiveinteger; assume
 beta*s/e is not an integer.

Positivealpha=(h-u)/2 andf=(h-v)/2, and d=alpha+beta+f, are integers. The residual basis and its exact parallelogram bound did not require dyadic e or odd beta. Its determinant remains nonzero; nearest coefficient rounding yields |z0|,|z1|<=e and meets a box boundary ONLY atz0=z1=+e orz0=z1=-e. At either such vertex the exact source/cap equations imply
 beta*s/e + alpha*(2m+1)N = (2i+epsilon)*beta.

Every term except the first is an integer. Thus the vertex would force beta*s/e integral, contrary to the hypothesis. BOTH guards are therefore strict. This is exactly the needed proof step, without the previous sufficient subcondition of odd beta and proper dyadic source. No density or open-window limit is invoked.

The remainder is unchanged and did not use those old subconditions: M=gcd(alpha*N,beta,N*f) gives positive integral nullincrements(alpha*N,beta,N*f)/M, identifies actualnonnegative i,m,q and positive tau. One nullreturn changes the rightphase/fullperiod by g1N/(2M), nonintegral because g1N odd. Selecting a safe right residual and correcting by2eN*p reaches the full actual target using odd Nd2 moduloLpower2. The upward source uses only genuine left walls, the cap has an ordinary roof by disjoint h-mouth symmetry, and every signed passage/corner/first-target guard is exactly as in LJ01_BOX. No floor reflection or corner suffix is added to this itinerary.

For a whole native family, take e>=3 INTEGER withgcd(e,beta)=1 and all other P=K1,Nodd,Lpower2/height hypotheses. Every native terminal source withu<h has positive eveninteger s<e, so e does not divide s. Coprimality implies e does not divide beta*s. Hence the lower lemma applies to EVERY native source and target, not just selected residues. At/aboveh, independently accepted UJ01 covers the same actual source/target withgcd(N*d2,L)=1. ProtectedTR01/TR05 placements and reversal cover the complementary pairs. Therefore EVERYdistinct actual native pair illuminates in the whole stated room family. No cap-depth gcd withN is required; beta can be even.

The earlier dyadic-width/odd-beta family is included because gcd(e,beta)=1 there. The general pairwise lemma also covers some noncoprime(e,beta) cases when its exact source condition holds. It does not cover sources withbeta*s/e integral, arbitraryP/K,evenN,otherparities/normalforms/turntypes orr4..8. Failure of the sufficient condition is not darkness. Fullgoal remains unfinished.

The sole prescribed non-dyadic/even-beta check has e5,beta6,N9. Its sourcebeta*s/e12/5 is nonintegral, yetgcd(beta,N)=3, outsideFR02. The independently derived coefficients and final root are listed in candidate.md; the checker will validate actual source/target domains before any arithmetic. No discovery, engine, new clock, worker or git-state mutation.
