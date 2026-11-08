# GSE04Q: an explicit all-native lower-source cap return bound

## Statement

Let integers0<s<a<w<A, beta>=1, X>=0 and sigma in{+1,-1} be fixed. At any tau>0 with strict actual source-mouth phase z0=center_(2a)(sigma*s+X*tau) in(-a,a), define

 x_q=F_A(z0+2q beta tau).

Set

 mu=a/(1+2A beta),
 N=floor(2A/mu)+1=floor(2A(1+2A beta)/a)+1,
 Q=max(A X,N).

Then SOME integer1<=q<=Q has x_q<a. In particular a genuine first-right-exit programme with all earlier contacts in(a,w) has exit index at mostQ. All widths/source data are the original integers; no finite direction/reflection cutoff is assumed. The valueQ grows with full geometry and is not bounded by the ten-wall count.

## 1. Entry safely away from the source corner

Put eta=a-|z0|>0. If eta>=mu, let theta=2beta tau. Partition the circle[0,2A) into N equal half-open intervals and consider N+1 points0,theta,...,Ntheta modulo2A. Two are in one interval; their difference gives a q with1<=q<=N and a representative rho of qtheta modulo2A satisfying

 |rho|<2A/N<mu<=eta.

Thus z0+rho lies STRICTLY in(-a,a) and x_q=F_A(z0+rho)=|z0+rho|<a. This is the standard finite pigeonhole argument, with a STRICT interior margin; no target recurrence claim is involved.

## 2. Entry close to a source corner

Suppose eta<mu. Since0<a<A and beta>=1, mu<1. If X=0 then z0=sigma*s is an integer and eta=a-s>=1, a contradiction. Hence X>=1.

If z0=a-eta, the adjacent source-corner parameter is

 tau0=tau+eta/X.

Its source phase is a modulo2a. If instead z0=-a+eta, use

 tau0=tau-eta/X;

its source phase is -a modulo2a. In BOTH cases X*tau0 is an integer because sigma*s, a and the source branch2ai are integers.

Choose the explicit positive integer q=A*X. At tau0,

 2q beta tau0=2A beta*(X tau0) in2A Z.

There is no unproved denominator estimate; q is an exact cap-rotation period at the comparison parameter. The comparison tau0 need not itself be a legal ray or a positive physical direction. It is only an algebraic reference phase.

For the +a side tau=tau0-eta/X, so the qth phase modulo2A is

 a-(1+2q beta/X)*eta
 = a-(1+2A beta)*eta in(0,a).

For the -a side tau=tau0+eta/X it is

 -a+(1+2A beta)*eta in(-a,0).

Both are strict because eta<mu. Their F_A folds are less thana. This handles BOTH sides of the source-centering jump and preserves the actual slope throughout the conclusion. Therefore q<=Q is the desired LEFT contact.

The two cases exhaust every admissible tau and prove the theorem.

## 3. Actual-room and whole native lower-source scope

In an ordered room let beta=H-h. For a native actual lower source (s,u), b<u<h, use X=h-u for its actual upward source or X=h+u-2b for its genuine source-floor programme. Mouth sources u=h have X=0 or X=2(h-b). Source/target floor repairs and finite actual walls remain exactly those already independently accepted; no new mirror is introduced. Every true first-right-exit programme must either exit earlier or contradict the LEFT hit guaranteed by the theorem. True-corner termination earlier is a failed programme, not a bypass.

For ALL native lower/mouth source marks in ONE fixed room, X<=2(h-b). Hence the SAME finite room-dependent value

 Q_room=max(2A(h-b), floor(2A(1+2A(H-h))/a)+1)

bounds every cap exit index for both declared source choices and both horizontal signs. The bound is independent of the actual bottom target, whose direct or floor programme starts only after the cap exit. It says nothing about arbitrary trajectories that leave the cap into the left arm and return later, or about upper sources. GSE04 proves that upper sources can instead have arbitrarily long finite regular first-R cap programmes.

Combining Q_room with the already proved full phase period2*lcm(a,A,R,B) yields a FINITE exact branch arrangement for the COMPLETE stated lower-source first-right-exit class at any fixed integral input. No cap-contact cutoff was assumed or fitted. Every target image equation and original guard can be retained. This is a proof of finite completeness for that restricted mechanism, NOT a proof of a nonempty actual-target branch, a general algorithm implementation, or all-word completeness.

## Validation and frontier

This is a direct all-integer hand proof, stronger/effective at native marks than the compactness lemma GSE04. No sample, numerical search, engine, census, worker, new clock or git change was used. Its original candidate was published before this proof. Existing infinite-square/unbounded-reflection controls are respected: Q depends on metricA,beta,h-b and does not limit vertical-wall bounces as slope grows.

Independent review should verify the source branch comparison, q=A X exactly closing the reference rotation, strict pigeonhole margin, and the original-room scope. The universal actual-target existence lemma remains OPEN, as do all ordered spirals, allr3 andr<=8. Finite completeness of one mechanism cannot substitute for proving some legal branch exists.
