# GSE05: actual target matching bounds the final cap episode

## Exact quantified theorem

Fix positive integral widths/heights with0<R<A, beta=H-h>=1, G=h-c>=1, B=A-l>R. Let actual bottom target T=(t,v) have integral horizontal coordinate, z=A-t in Z and0<z<B. Fix one of its physical direct/floor tails d=c-v or c+v, a positive integer, and put F=G+d.

Consider ANY single cap episode: consecutive descending h contacts are separated by vertical travel2beta and share one positive unfolded horizontal speed tau. Its qth descending contact is its FIRST exit through the actual right mouth (w,A], w=A-R; all preceding positive-index h contacts are strict genuine notch reflections. Its final signed cap residual is z1 in(-R,R), so the exit phase is (2m+1)A+z1. Require the genuine right/bottom tail at the SAME tau to attain actual T. Thus for actual integer fold indices k,j and one actual target-image sign epsilon,

 z1+F*tau-2Rk=I, I=epsilon*z+2Bj in Z.

Set

 mu=R/(1+2A beta),
 N=floor(2A/mu)+1=floor(2A(1+2A beta)/R)+1,
 Q_T=max(A F,N).

Then q<=Q_T. The source location, cap-entry phase and initial vertical sign are not used in this implication. In particular it applies to actual upper sources, whose UNMATCHED first-right-exit programmes can have unbounded cap residence as GSE04 proves. It also applies to either genuine lower-source entry. This is a consequence of fixed actual target matching; no assumed direction/reflection cutoff is present.

## 1. A backward cap return safely inside the right mouth

Let eta=R-|z1|>0 and theta=2beta*tau. If eta>=mu, the N+1 rotation points0,theta,...,Ntheta modulo2A give, by pigeonhole into N equal half-open intervals, an integer1<=p<=N with a representative rho of ptheta satisfying

 |rho|<2A/N<mu<=eta.

Therefore z1-rho in(-R,R). The cap contact p cycles BEFORE the nominated exit has phase, modulo2A,

 A+z1-ptheta = A+z1-rho.

Its folded physical coordinate is A-|z1-rho|>w: it is already in the actual right mouth, including a possible smooth outer-wall point. If q>Q_T then q-p>=1, so this is an earlier h contact of the same cap episode, contradicting the stipulated first exit.

This is a backward return to an OPEN right interval of positive margin. It is not recurrence to the point target, nor concatenation of trajectories. The exact target is already imposed in the equation.

## 2. A backward cap return close to either right-mouth corner

Suppose eta<mu and write z1=sigma*(R-eta), sigma in{+1,-1}. The exact ACTUAL target relation gives the reference parameter

 tau_b=(I+2Rk-sigma*R)/F,
 F*tau_b in Z,
 tau-tau_b=sigma*eta/F.

Do NOT replace I by one projected image, omit its sign, or assume tau_b is a legal ray. Integrality holds for BOTH actual target images and every full2B target period because z and widths are integral.

Choose the explicit positive integer p=A*F. Its cap rotation at the comparison parameter closes EXACTLY:

 2p beta tau_b=2A beta*(F tau_b) in2A Z.

Hence the p-cycles-earlier cap phase, centered at the same odd-A right band and computed modulo2A, equals

 z1-2p beta tau
 =sigma*[R-(1+2A beta)*eta].

Because eta<mu, this centered value is strictly between-R and R (indeed its signed magnitude is between0 andR). Thus that earlier contact is RIGHT. Again q>Q_T implies q-p>=1 and contradicts first exit.

Both boundary signs are essential. For sigma=+ the target equation places tau ABOVE its comparison parameter and the BACKWARD rotation moves inward from+R; for sigma=- it places tau BELOW and moves inward from-R. This is the reverse-target counterpart of the positive source coupling in GSE04Q. No unproved optical continuation through the comparison corner is used.

The two margin cases exhaust all strict exit states, proving q<=Q_T.

## 3. Physical scope, actual target and first-hit guards

The recurrence relation concerns the SAME cap rectangle and consecutive h contacts of ONE physical episode. Subtracting p cycles is legitimate only when q-p>=1; this is why the proof assumes q>Q_T before deriving its contradiction. Earlier right-mouth membership is incompatible with the original finite-wall first-exit requirement. No later formal rectangle continuation is treated as part of an emitted physical ray.

At the final exit, right and bottom signed phases are those of accepted GSE01: z2=z1+Gtau-2Rk, |z2|<R, then E=z2+dtau=I. Both actual images E=+z or-z modulo2B are retained in I. The proof does not weaken the strict c/reflex guards, roof guards, source/target exact-point repairs or finite original mirrors. It derives a NECESSARY bound for every fully guarded matched programme. A true corner that kills a programme earlier is not an exception. Accepted upper exact-S suffix deletion does not add ghost contacts; apply the same theorem to the actual retained cap episode.

The result allows arbitrary source horizontal positions, since only the actual integer TARGET offset is used. It covers upper upward or downward cap starts whenever they remain in this one episode until their first right exit, and lower upward/source-floor entries. It does not include a ray that leaves through the LEFT mouth and returns later without explicitly starting a new episode.

It also does not silently include arbitrary right/bottom scattering words. The declared tail is the genuine right descent followed by the direct or true-bottom-floor target segment. Further genuine bottom-top returns would add unbounded positive vertical duration to F and require separate availability reasoning; the present theorem does not remove them by monotonicity.

## 4. Finite completeness without excluding upper periodic orbits

GSE04 constructs upper sources with regular periodic cap rays and arbitrarily long finite first-right prefixes. The present theorem does not contradict that result. Those prefixes cannot ALL remain exact hits of ONE fixed integer actual target with a fixed tail F. If they did, q would exceed the proved Q_T. This is a genuine use of the point-target condition, which recurrence/open-prefix arguments alone could not provide.

For every fixed integral room, direct/floor bottom marks have F=h-v orh+v<h+c. Thus the room-dependent value

 Q_room_target=max(A*(h+c), floor(2A(1+2A(H-h))/R)+1)

bounds cap exit counts for EVERY target-matched programme of this class and every actual source, including upper sources. This does not depend on source depth or a. There is no bound depending only on wall count.

For actual native marks and integer vertical durations, reduce tau modulo2*lcm(a,A,R,B) for lower entries, or2*lcm(A,R,B) for a direct upper start, preserving complete actual phases and BOTH target-image tests. With q bounded by Q_T, every branch's phases range over bounded intervals and its target equation has positive coefficient equal to its total vertical travel. Consequently the entire declared target-matched first-cap/direct-or-floor-tail union has a FINITE complete exact representation at each fixed input. No new engine, search, census, fitted cutoff or finite reflection assumption is used.

A finite complete representation is NOT a proof of nonempty target matching. It supplies neither a universal ten-wall illumination theorem nor an actual dark pair. Its purpose is to remove the apparent infinite-cap-detour obstacle for this point-target class; the next REQUIRED global step is NONEMPTINESS, not further finiteness lemmas.

## Review and frontier

Candidate published before proof. Independent hand review must check the backward-cycle identification, integer reference period p=A F, BOTH actual target images, strict margin and signed boundary cases, and limits on genuine left reentry/bottom-tail words. Existing roof and actual-endpoint optical lemmas remain frozen. No numerical run/search, new clock, worker, engine, census, fitting or git-state change occurred. Full ordered/r3/r<=8 goals remain OPEN.
