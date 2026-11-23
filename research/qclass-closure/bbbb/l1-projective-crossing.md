Advances: L1 — For a transverse overlap crossing, integrality eliminates the free source coordinate. A bounded physical mouth bounds the reduced vertical ratio, and with a bounded-height coupled aspect also the horizontal ratio. The result applies in the overlap geometry, independently of the source's horizontal denominator.

# Comparable dimensions: a divisor read off at the overlap

**Geometric inputs.** Use the full vertical overlap column, side portals, normalized upper approach and compact parameter bounds of [l1-overlap-phase](l1-overlap-phase.md). It is a new proof input awaiting independent review. Let w≥1 be the physical integer width of the overlap, with D,c,u integers as in that note. The upper cap of the overlap has height βt, β a positive template integer. Set H=h/t=m/n in lowest terms. Where the coupled aspect κ=(D/u)/H is used below, assume an independent bounded-height certificate for it, such as d191/d192 **when their distinct geometric hypotheses hold**. A bound on κ in magnitude alone is insufficient. An upper chamber opening on a roof need not have this full transverse overlap. No implication between the two geometric hypotheses is assumed.

## Why stretching the entire chart does not produce the seed

With the normalized marked shape fixed, (u,t) rescale the horizontal and vertical coordinates separately. The specular reflection matrices in orthogonal walls are diagonal and commute with this map. Segment legality, smooth-wall contacts and every corner hit are preserved in both directions. Even the normalized slope is unchanged. Thus a lit seed ON this two-scale orbit already proves its entire orbit lit; varying u,t does not bring a seed from another normalized shape into it. If, for instance, w is held fixed as u grows, w/u changes, so this motion is no longer that orbit. D184 then requires the actual fixed transverse periods of its cuts, and d188 requires its mixed transfer hypothesis. In an occupied cell one period can grow with the perpendicular insertion. [D186 crossing and its exact failure](l1-crossing-gap-transfer.md) · [D188 mixed seed](l1-mixed-seed-normals.md)

## Source elimination by divisibility

The overlap argument gives a necessary condition for darkness with |p|,|q|≤K, q≠0, and an integer j:

    P p (D−w−c)/(2uH) + P q w/[2u(H+β)] = j.                    (1)

Its uniform K comes from the upper-wing interval and the normalized vertical gate clearances. The first term alone could be adjusted by choosing the source abscissa. Put T=m+βn and multiply (1) by 2umT:

    P n [p(D−w−c)T + qwm] = 2ujmT.

Reducing modulo T kills the source term AND the integer j. Since gcd(T,n)=1 and gcd(T,m)=gcd(m,β), one obtains the exact necessary condition

    L=T/gcd(m,β) divides Pqw.                                    (2)

In particular L/gcd(L,Pw)≤K. This holds for both signs of q, includes p=0, and requires no hypothesis about the height of c/D. If all horizontal lengths including c share a lattice unit, (1) can first be expressed in that unit using their corresponding integer representatives.

**Bounded-mouth theorem.** For w≤w₀ and integer P, (2) implies

    n ≤ KP w₀,          m ≤ βKP w₀.

If κ=A/B in reduced form is known from a finite list then D/u=Am/(Bn), with reduced numerator ≤AβKP w₀ and denominator ≤BKP w₀. These are separate height bounds in this subclass; the Fourier coefficient K is not itself a bound on every flat equation. The same test works for unbounded w whenever the part of L coprime after cancellation with Pw is too large: the precise test is L/gcd(L,Pw)>K.

**Consequence for checking rooms.** If every wall ordinate is a translate of an integral combination of h and t, vertical wall gcd one forces gcd(h,t)=1. Thus h=m and t=n, and the bounded-mouth theorem bounds actual vertical wall levels for a fixed upper template. With bounded w and the overlap endpoints on wall lines, horizontal normalization also has a finite congruence test: any common divisor of the wall gaps divides w, so for each prime dividing w at least one wall gap must be nonzero modulo that prime. Split into w=1,…,w₀ first. On a fixed vertical slice the horizontal domain can therefore use d184's Presburger universality procedure whenever its other chart restrictions are Presburger (fixed-template linear equations and integral-mark parity are). Alternatively one can test the larger order chart with the same bounded-width and normalization restrictions; success would cover its subdomain. This is a possible terminating slice test under d184's stated domain conditions, not a run or a numerical horizontal area bound. A free horizontal scale and a width-one offset can coexist with horizontal wall gcd one. Bounds on the two ratios by themselves do not bound every marked gap of such a chart. [Fixed-transverse decision and its normalization proviso](l1-gap-hyperplanes.md)

## Exact surviving arithmetic for a drifting aperture

Small w/u does not imply small w. The following symbolic identity tests the available equations, without constructing or asserting a dark room. Take odd m≥5, N=2m+3, t=m, h=m+1, u=mN and D=(m+1)N. Here m is a family index; H=(m+1)/m. Set β=1, P=2, w=2m+1 and D−w−c=(m+1)(N−1)/2. Then the horizontal lengths are integral with 0<c<D−w, gcd(D,u,w)=gcd(N,2m+1)=1, and gcd(h,t)=1. The coupled κ equals 1, the aperture fraction tends to zero, and the two axis ratios have unbounded reduced denominator. Yet the left side of (1) for (p,q)=(2,1) equals (N−1)/N+1/N=1. The divisor in (2) is exactly w. Thus scale invariance, primitive wall-length arithmetic, the coupled aspect and this source-independent necessary condition still allow the large denominator to live in the mouth width. This does not refute illumination, nor the existence of additional independent trajectory relations. On a genuinely two-generator horizontal presentation with D,u generating *all* wall levels integrally, normalization instead forces gcd(D,u)=1. In that case u, the reduced denominator of D/u, is ≤Bn and (2) gives w/u≥1/(BKP). Such a chart cannot support a dark sequence with w/u→0 under these uniform controls. The additional primitive offset in the displayed identity is essential.

## Follow-on: let the upper wing change shape

At a particular upper shape with rational return period P=P_num/P_den in lowest terms, the identical calculation after clearing P_den yields L | P_num q w. This permits a sharper test than requiring every upper period to remain small. If the normalized upper windows and travel bounds still give a uniform K, it suffices to bound gcd(L,P_num w) to bound L. A large period supported on primes absent from L cannot mask the lower denominator. This formulation assumes an integral β in the chosen common vertical unit; changing the unit requires recomputing all these integers.

The scale labels do not give the needed gcd estimate. For example two normalized unit-travel runs of heights 1 and (2s+1)/(2s) have common exit-preserving slope period 2(2s+1). At the comparable lower ratio (s+1)/s with β=1 the divisor 2s+1 is absorbed entirely. This arithmetic example only tests the period estimate. Independent upper gap variations can also narrow the approach window used for K. Recursing on scale classes would need a uniform gate window AND control of the common prime powers, or an additional itinerary giving a divisor with different prime support. A count of the growth scales supplies neither.

**First open case.** An unbounded physical aperture with w/u→0 can absorb the reduced height divisor even with a fixed overlap return period; without the transverse overlap geometry one does not yet have (1). The clean next target is a second crossing relation whose aperture coefficient multiplies a different wall difference with controlled gcd with w. If it gives L | P' q' w' as well, then L divides gcd(Pq w,P' q' w'), explicitly removing any shared-width ambiguity when that gcd is bounded. No chart-wide G(C), numerical census ceiling or ledger change follows.

**What is the smallest W ≤ 20 room this result doesn't cover?** The W=10 word LLLRLLLRLR, realized by (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2), remains open as an all-length statement. No discovery search was run.
