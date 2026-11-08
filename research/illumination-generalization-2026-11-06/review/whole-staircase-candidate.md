# Candidate closure of every real orthogonal eight-wall room

UNREVIEWED CANDIDATE. The other authorized chat has reached its native budget limit. This note has no independent acceptance, and is NOT a resolution of the W<=21 goal. It proposes a complete all-real staircase theorem; U/T/offset eight-wall types are already independently accepted.

## A. The corner obstruction can be removed more directly

The accepted cone-only/full-fiber dependency already proves that a folded connection can be purified of removable convex90corner contacts. For the present roof chart an explicit identity is simpler and avoids any sheet or continuation issue.

Use the partial-overlap roof construction of staircase-roof-proof.md, retaining its STRICT guards at the two reflex corners, but choose only ONE actual target image. Its upper coordinate is

    x(eta)=F_a(w+tau*(eta-d)),
    y(eta)=d+F_h(eta-d),
    d<=eta<=2H-yt,

where h=H-d and d<=yt<H. Before the roof eta=H, physical height equals eta. The terminal developed height2H-yt has actual height yt. Suppose its roof coordinate is B=w+tau*h in a*Z, a true convex roof corner. Then triangular-wave symmetry at every multiple of a gives

    x(yt)=F_a(B-tau*(H-yt))
         =F_a(B+tau*(H-yt))
         =x(2H-yt)=xt.

Thus the actual target was already reached on the upward leg at eta=yt, BEFORE the singular roof contact. Truncate there. If yt=d, truncate at the first upper portal instead. This prefix is corner-free: the two reflex corners and all other step corners were excluded by strict portals; the only newly questioned corner was the still-unreached roof corner.

If B is not in a*Z, the entire upper roof excursion is an ordinary specular path, or it can be truncated at an earlier actual target as before. Consequently ANY single genuine target image inside the roof chart's strict slope window gives an actual ordinary corner-free connection. No two-image roof-corner avoidance or off-resonance exception is needed. This does not claim arbitrary corner continuation is legal; it constructs a prefix that never reaches that corner.

## B. A stronger whole-room overlap criterion

Let 0<a<b<A and 0<c<d<H, g=d-c, and

    P=([0,A]x[0,c]) union([0,b]x[c,d]) union([0,a]x[d,H]).

For a cross-placement b<=xs<A,0<ys<c,0<xt<a,d<=yt<H, write Hs=c-ys, T0=Hs+g=d-ys, h=H-d, Ht=yt-d, v=2h-Ht>h and D=T0+v.

The independently accepted partial-window construction, with n=1 and K nearest to g*(2A-xs)/Hs among even multiples of b, gives strict portals and an overlap of length

    ell >= min(2a, a+b*g/Hs).

It uses no assumption on H or target depth. Its final actual-target coordinate has image interval length L=ell*D/T0. Set

    Qv=min(2, 1+b*(d-c)/(a*c)).

Since Hs<c, T0<d and v>h,

    ell >= a*Qv,
    L=ell*(1+v/T0) > a*Qv*(1+h/d)=a*Qv*H/d.

Therefore the whole geometric condition

    (H/d)*Qv >=2                              (Rv)

gives L>2a. The true target images +/-xt+2ma have gaps strictly below2a, so at least one lies strictly inside. Its inverse slope lies strictly within BOTH portal windows. Section A handles a possible convex roof-corner candidate by actual earlier arrival, and otherwise the already audited roof path is ordinary. All corner, velocity, finite-length and actual-target guards are inherited explicitly from that construction; its earlier v>=2T0 premise was used ONLY to give a stronger image-span bound, and is replaced here by L>2a.

The orientation-avoiding Qlow/Qup L arguments cover all other placements exactly as in the accepted staircase-window theorem. No boundary endpoint is substituted for an actual interior mark: xs=b and yt=d are included in the cross chart. Transposing x,y gives the other whole condition

    (A/b)*Qh >=2,
    Qh=min(2, 1+d*(b-a)/(c*a)).                (Rh)

This proves the candidate Rv/Rh sufficient whole-room criteria using arbitrary real parameters.

## C. Combine with the already accepted floor criteria

The independently accepted source-floor theorem covers the entire room under either

    (A-b)(d-c)<=c(b-a),                       (F)
    (H-d)(b-a)<=a(d-c).                       (Ft)

I claim that EVERY positive-real staircase metric satisfies at least one of F,Ft,Rv,Rh. Here is a dimensionless proof independent of optics.

Put

    alpha=a/b, beta=c/d, p=alpha*beta,
    lambda=A/b, mu=H/d, s=alpha+beta.

All alpha,beta,p lie strictly between0 and1; lambda,mu>1. If 1-beta>=p, Qv=2 and mu*Qv>2, so Rv holds. If 1-alpha>=p, Rh similarly holds. Otherwise

    Qv=(p+1-beta)/p, Qh=(p+1-alpha)/p.

Assume both F and Ft fail. Their strict negations are

    lambda>(1-p)/(1-beta),
    mu>(1-p)/(1-alpha).

Define

    E_lambda=(1-p)(p+1-alpha)-2p(1-beta),
    E_mu=(1-p)(p+1-beta)-2p(1-alpha).

If E_lambda>=0, the lower bound for lambda is at least2p/(p+1-alpha), hence lambda*Qh>2 and Rh holds. If E_mu>=0, Rv holds in the same way. At least one is positive because

    E_lambda+E_mu=2-s+p*(3s-4)-2p² >0.          (*)

To verify the last strict inequality, use 2sqrt(p)<=s<=1+p. If p>=1/3, the displayed expression is nondecreasing in s, and at s=2sqrt(p), with x=sqrt(p), it equals

    2(1-x)²(1+x-x²)>0.

If p<=1/3, it is nonincreasing in s, and at s=1+p it equals

    (1-p)²>0.

All factors are strict because0<p<1. Thus (*) holds and the four sufficient criteria exhaust every metric. Equality in either F or Ft is already covered by the accepted floor theorem; no limiting or genericity argument is used.

## D. Claimed consequence and verification boundary

Sections A--C would prove every real staircase8/all distinct actual interior pairs. With the independently accepted complete eight-wall metric classification and existing L/U/T/offset theorems, this would prove every strictly simple ORTHOGONAL polygon with at most eight maximal walls illuminates every distinct real interior pair, without a k bound.

It says nothing about diagonal-wall eight-wall shapes or orthogonal10--20wall shapes, and does not resolve the full canonical45 W<=21 target or universal22minimality.

The decisive NEW facts requiring independent review are the earlier-target identity at a bad convex roof corner, removal of the old roof-pair amplification premise once a single image suffices, and the dimensionless exhaustive geometry argument. All source dependencies are pinned in the request. Exact prescribed algebra/fold checks are supporting controls only; they do not replace that review. Until it is obtained, the WHOLE staircase/eight-wall consequence remains an UNREVIEWED CANDIDATE.
