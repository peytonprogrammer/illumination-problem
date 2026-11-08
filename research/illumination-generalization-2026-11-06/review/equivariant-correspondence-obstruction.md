# A clean intrinsic-reversal quotient cannot explain an entire physical dark pair

R24 hand candidate, pending independent review. This is an obstruction to a precisely specified higher-degree correspondence. It does NOT classify all multivalued correspondences or prove W<=21 illumination.

## Hypotheses

Let M be a connected reflection unfolding, Sigma all actual corner lifts, and rho its intrinsic physical half-turn. The accepted half-turn theorem gives Fix(rho)=Sigma. Let A,B be two disjoint free physical interior lift fibers. Each is rho-invariant, disjoint from Sigma, and has q=4or8 points. Thus rho has no fixed point on A or B.

Let Y be a translation surface with a finite forbidden set Z containing its singularities. Let tau:Y->Y be a globally defined derivative -I involution with Fix(tau) subset Z. Let f:M->Y be a finite translation cover with the following TWO explicit conditions:

    (C) f^-1(Z) subset Sigma;
    (E) f*rho = tau*f.

Condition C means a legal source trajectory never projects through a target forbidden point. It is stronger than saying source corners map to target corners. Condition E identifies the quotient reverser with the induced intrinsic physical half-turn. Neither condition follows from physical darkness or an arbitrary translation quotient.

Define the relation

    R_f = {(x,y) in (M minus Sigma)^2 : f(y)=tau(f(x))}.

It can have many possible y values for one x; no degree bound or regularity of the cover is assumed. The argument below also works for any map satisfying C and E, independent of covering theory.

## 1. Why this is a valid sufficient surface-dark relation

If (x,y) belongs to R_f, then f(x),f(y) avoid Z by C. They are distinct, since otherwise f(x) is tau-fixed and hence in Z. A legal straight geodesic in M from x to y would project to a straight geodesic in Y from u to tau(u), avoiding Z. Apply tau to the time reversal of that segment. It starts at u with the same velocity. Unique regular straight continuation forces equality with the original segment and a tau-fixed midpoint. That midpoint belongs to Z, contradiction.

This is only a sufficient nonillumination mechanism on M. The explicit inverse-forbidden-set condition is essential for this proof; regular preimages of a forbidden target point invalidate the projection argument.

## 2. Exact obstruction for physical fibers

Fix x outside Sigma and y outside Sigma. If BOTH (x,y) and (rho(x),y) belonged to R_f, then

    f(y)=tau(f(x)),
    f(y)=tau(f(rho(x)))=tau(tau(f(x)))=f(x).

Thus f(x)=tau(f(x)) is in Z. Condition C would put x in Sigma, contradiction. Therefore R_f cannot contain BOTH source points in an intrinsic half-turn pair for one target. The same argument prohibits both targets y,rho(y) for one source.

In particular A x B is NOT a subset of R_f: it contains (a,b) and (rho(a),b) for every a in A,b in B. A SINGLE common quotient with C and E cannot account for the full surface-dark rectangle required by an actual physical dark pair. This obstruction applies to orthogonal AND diagonal canonical rooms, at every W and at every covering degree. It does not require a global inverse map of f, a deck group, or a bound on primitive degree.

## 3. Finite unions and the precise escape routes

Relation R_f is invariant under (x,y)->(rho(x),rho(y)) because of E. Partition A and B into their half-turn pairs. In each 2by2 block it contains either no entries or two matched diagonal entries; it cannot contain two entries in a row or column. Consequently

    |R_f intersect (A x B)| <= q^2/2.

A union of such relations covering A x B would therefore need AT LEAST TWO relations. Two is a necessary lower bound only; it is not asserted sufficient or realizable, and no upper bound is proved. Different pairs may require different maps. Nothing here rules out that possibility.

Other escape routes include failure of C (regular lifts of forbidden target points), failure of E (the relevant quotient reversing involution is NOT the induced physical rho), or correspondences not defined by one reversing quotient at all. A proof must state which mechanism it uses and establish its actual endpoint/corner behavior. It cannot replace C by f(Sigma) subset Z or infer E from derivative -I alone.

In particular a strict physical parity fold is a piecewise map into a polygon. The earlier proofs explicitly repair regular preimages of certain base corners by local retracing. They do not establish C and E for a corresponding global translation cover. This result must not be cited as excluding those accepted folds or the known22 dark room. If a translation-surface realization of that fold is constructed, any use of the present sufficient-darkness argument requires a separate check of both conditions.

## Consequence and verification boundary

The fixed-point argument makes a naive upgrade from global maps to ONE clean intrinsic-reversal quotient fail, even at arbitrarily large degree. A useful quotient/correspondence theorem must handle at least one of the precise escape routes. This is a structural constraint, not a construction of the required common base or a threshold-specific W<=21 theorem.

Dependencies: review/half-turn-quotient.md for Fix(rho)=Sigma and the free actual physical fibers; the optical reversal uniqueness proof is rederived here. All algebra, finite-union coverage and forbidden-set guards are proved in this packet. No new external theorem, computation, room, ray, direction, word, cylinder or orbit search was used.
