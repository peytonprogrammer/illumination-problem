# GSE04: lower-source cap residence has a finite complete bound

## Precise statement and scope

Fix integers 0<a<w<A, beta>0, X>=0, a real horizontal source mark0<s<a, and sigma in{+1,-1}. For any tau>0 admitting the strict source-mouth state

 z0(tau)=center_(2a)(sigma*s+X*tau) in(-a,a),

write the successive descending cap contacts

 x_q(tau)=F_A(z0(tau)+2q*beta*tau), q=1,2,... .

There exists a FINITE Q, depending on this complete fixed data, such that for every such tau some q<=Q has x_q<a. In particular no actual first-right-exit programme can have Q or more preceding strict notch contacts in(a,w). A right exit or true corner can stop it earlier; neither supplies an exception to this upper bound.

This is NOT a room-independent/reflex-count/direction/reflection cutoff. It allows unbounded vertical-wall reflections as tau grows. For actual lower sources X=h-u or the genuine source-floor duration h+u-2b, its hypothesis is the actual source-to-mouth phase, with one common direction. Mouth sources X=0 are included. Upper interior sources are explicitly excluded and have the obstruction in section4.

## 1. Compactness of the coupled phase parameter

Take L=2*lcm(a,A). Because X,beta are integers,

 z0(tau+L)=z0(tau),
 2q*beta*(tau+L)=2q*beta*tau modulo2A

for every integer q. Hence all source-mouth states and cap contact positions are L-periodic in tau. It suffices to consider the compact circle R/LZ. At its parameter endpoints use local real lifts; periodicity makes that harmless.

Suppose no such Q exists. Choose tau_n (mod L) with x_q(tau_n)>=a for every1<=q<=n and all strict mouth states. This is stronger than needed for strict-notch programmes, since right-mouth contacts are not excluded in this contradiction. Pass to a subsequence with tau_n converging to tau_* in a local real lift and z0(tau_n) converging to z_* in[-a,a]. Every fixed q contact then converges to

 x_q^*=F_A(z_*+2q*beta*tau_*).

Continuity of the fold in its argument is sufficient; continuity of the centered source phase ACROSS its jumps is not assumed.

## 2. Interior mouth limit: rational or irrational recurrence

If |z_*|<a, consider rotation by theta=2beta*tau_* on the circle of length2A. If theta/(2A) is rational, some positive q has qtheta=0 modulo2A, and x_q^*=F_A(z_*)=|z_*|<a. If it is irrational, its forward orbit is dense on that circle, so some positive q has folded coordinate<a. This uses density only to hit a genuinely OPEN left interval, not to claim intersection with a point target.

For that fixed q, continuity gives x_q(tau_n)<a for all sufficiently large n, a contradiction. The recurrence statement here can also be obtained from the elementary irrational circle-rotation theorem. No trajectory is concatenated and no target matching is inferred.

## 3. Source-corner limit: the sign is decisive

It remains to handle z_*=+a or-a. This cannot happen when X=0 because z0 is the fixed strict mark sigma*s. Thus X>0. The limiting source phase is a modulo2a. Near tau_*, choose its fixed source branch on each side and write epsilon_n=tau_n-tau_*.

For z_*=+a the strict centered branch is

 z0(tau_n)=a+X*epsilon_n, epsilon_n<0.

For z_*=-a the strict centered branch is

 z0(tau_n)=-a+X*epsilon_n, epsilon_n>0.

These are the TWO sides of the actual source-fold jump; neither is omitted. An irrational limiting rotation again has a fixed positive q landing in the OPEN left interval, giving the previous contradiction.

For a rational limiting rotation choose any positive period q with2q beta tau_* in2A Z. Then, on the +a branch,

 x_q(tau_n)=F_A(a+(X+2q beta)*epsilon_n)<a

for all sufficiently small negative epsilon_n. The perturbed phase is just below+a and inside(-a,a). On the -a branch the same formula is

 x_q(tau_n)=F_A(-a+(X+2q beta)*epsilon_n)<a

for all sufficiently small positive epsilon_n. Here too the phase lies inside(-a,a). The coefficient X+2q beta is positive in BOTH cases. Thus the qth contact enters the LEFT mouth on every sufficiently close admissible branch, a contradiction.

This is precisely what generic recurrence alone would miss: a rational boundary orbit is dealt with by the sign of the coupled source and cap phase, not by perturbing the actual target or assuming an open source family.

All accumulation possibilities are exhausted. Therefore the finite uniform Q exists. No bound is claimed to depend only on wall count, and no asymptotic cutoff was tested.

## 4. Why the same conclusion is false for upper sources

Let actual upper S=(s,u),h<u<H, beta=H-h, C=2H-h-u. Its first descending h contact occurs at phase s+Ctau, with later contacts adding2beta tau. Suppose for an integer n>=1,

 tau0=nA/beta,
 x_*=F_A(s+Ctau0) in(a,w).

Then2beta tau0=2nA, so EVERY descending h contact is the same strictly interior notch point x_*. Every corresponding roof contact is ordinary: its phase differs from a bottom phase by nA, whose fold is x_* or A-x_*, both strictly between0 and A. Hence this is a genuine regular periodic cap ray, never leaving through either mouth.

For every finite N, choose a sufficiently small perturbation epsilon: at the qth descending contact the phase changes by (C+2(q-1)beta)*epsilon. The fold is1-Lipschitz; if

 |epsilon| < dist(x_*,{a,w}) / (C+2(N-1)beta),

all first N h contacts remain in(a,w). Shrink this bound further using the finitely many ordinary roof-contact margins to keep every intervening roof reflection corner-free. Thus arbitrary long genuine notch prefixes exist; no uniform finite bound over all upper-source slopes is available.

In fact finite FIRST-RIGHT-exit programmes themselves have unbounded length here. Choose a phase lift p with F_A(p)=x_* and local fold derivative eta=±1. Take epsilon with eta*epsilon>0. Until the first crossing of w the qth physical coordinate is EXACTLY

 x_q=x_*+eta*(C+2(q-1)beta)*epsilon.

Choose epsilon sufficiently small and avoid the countable equalities x_q=w. Then the first q with x_q>w exists, all preceding contacts lie in(a,w), and its overshoot is less than2beta*|epsilon|<A-w. Its count tends to infinity as epsilon tends to0. At each intervening roof the phase differs from the nearby h phase, modulo A, by at most beta*|epsilon|; because all h coordinates stay between x_* and w+2beta*|epsilon|, a further smallness bound keeps every roof strictly away from0,A. Thus these are genuine finite regular cap prefixes with first RIGHT exit and unbounded contact count, not merely a limit with no exit.

This is NOT darkness and is compatible with a different illuminating ray from the same source.

On the ALREADY accepted swapped countercontrol, A=5,a=3,w=4,beta=2K,C=2K+2,s=2 and K>=33. The open interval(K/5,2K/5) has lengthK/5>6, hence contains a positive even integer n. At tau0=5n/(2K),

 s+Ctau0=2+5n+5n/K,
 F_5(s+Ctau0)=2+5n/K in(3,4)

because n is even. Thus the obstruction applies to the exact frozen actual source, without choosing a new room. GSE02 already supplies a different actual source-to-target trajectory for every one of these rooms. The cap-periodic ray is an obstruction to a UNIFORM RETURN BOUND, not an optical counterexample.

## 5. Consequence for the lower first-right-exit proof programme

For a FIXED integral room and fixed actual lower/mouth source, choose L'=2*lcm(a,A,R,B). It is also a valid common slope period for every finite declared source/cap/right/direct-target programme: source/contact phases at the integral vertical durations change by full physical periods, and target phase changes by dL' in2B Z. The same holds for genuine source/target floors when their separately accepted repairs are retained. This does not assert completeness over rays that reenter the left arm after leaving the cap.

Combine the finite Q with0<=tau<L'. For each1<=q<=Q, every source branch, cap fold and right fold lies in a bounded phase range. Its boundary/first-hit equations are affine in tau, so there are finitely many branch intervals and isolated boundary phases. Strict source/notch/right guards and exact actual target E in{+z,-z}+2B Z can in principle be decided on this FINITE arrangement. Each branch's unfurled E has positive slope X+2q beta+G+d, so it cannot identically equal one nominated target image on an open interval.

This yields a finite complete representation for this entire lower-source first-right-exit class without ASSUMING a return cutoff, despite arbitrarily many allowed original reflections. Smooth outer-wall seam contacts are kept; original true corners remain forbidden. Endpoint and signed-velocity guards still come from the accepted GSE01 physical theorem.

No new engine or arrangement implementation is requested or performed. A finite representation is NOT a proof that any target-compatible cell/root exists. The remaining global question is still actual-endpoint existence in every ordered spiral, potentially including repeated genuine left-arm visits. The upper-source obstruction also forbids silently extending this compactness conclusion to all source programmes.

## Evidence and ownership

Hand argument only, no new discovery search, room census, fitting, engine, worker, clock or git change. The only explicit control is the exact already accepted GSE02 swap of the peer's frozen countercontrol. Independent review must challenge the source-jump signs, rotation recurrence's limited use, actual periodic upper orbit, and the scope of the finite-arrangement consequence. Full ordered-spiral, r3 and r<=8 targets remain OPEN.
