# The direction skeleton needs unbounded arithmetic state

Codex01a18403, 2026-11-06. Hand hostile-case test, no computational discovery. Independent review pending. This does not refute the directionwise92-edge graph bound; it refutes an unwarranted fixed finite-state conclusion from that bound.

## 1. Four-wall rooms with arbitrarily large minimum primitive direction

For any integer n>=2 take the square

    P_n=[0,8n^2] x [0,8n^2],
    S_n=(4n^2,4n^2),
    T_n=(4n^2+2n,4n^2+2).

It is a strictly simple canonical45 disk with W=4. Both marks are distinct interior A points. Every illuminating billiard trajectory has a primitive integer launch direction(p,q) with |p|>=n and |q|>=1. The minimum possible Euclidean norm of a primitive launch direction is therefore EXACTLY sqrt(n^2+1), achieved by the direct interior segment in direction(n,1).

Proof against ALL reflected connections, not only the direct segment. Write B=8n^2. Every developed image of the target in a rectangle has coordinates

    (epsilon*T_x+2B*a, delta*T_y+2B*b),

where epsilon,delta=+/-1 and a,b are integers. The displacement(X,Y) from S has

    X/2=epsilon*(2n^2+n)-2n^2+8n^2*a,
    Y/2=delta*(2n^2+1)-2n^2+8n^2*b.

Hence X/2 is0modn and Y/2 is+/-1modn. All actual billiard endpoints are among these images, even though not every image necessarily supplies a corner-avoiding trajectory. For a primitive direction(p,q) parallel to(X,Y), the integer identity q*(X/2)=p*(Y/2) gives p=0modn. Vertical p=0 is impossible because a vertical trajectory cannot change the physical x coordinate and T_x!=S_x. Horizontal q=0 is likewise impossible because T_y!=S_y. Therefore |p|>=n,|q|>=1. The direct segment has displacement(2n,2), primitive direction(n,1), and lies wholly in the convex interior.

This proves the exact minimum for every n; no scan or finite failure is used. There is no bound depending only on W for the size of a primitive illuminating direction, even for illuminated convex rooms and even if arbitrary reflection counts are permitted. This is distinct from the earlier six-wall lower bound on REFLECTION COUNT: here the optimal path has ZERO reflections.

## 2. A precise bounded-state reduction that is impossible

Consider a proposed exact direction quotient for each room, with at most F(W) states. Assume:

- every primitive integer direction w has a state c(w);
- c(A*w) is determined ONLY by c(w) and A for each of the four fixed generators U,U^{-1},V,V^{-1}, where U=[[1,1],[0,1]] and V=[[1,0],[1,1]];
- the state determines exactly whether that direction's Gamma orbit gives an actual S/T connection;
- every primitive direction is reachable from e1 via these generators (their usual SL2Z action).

Then such a uniformly bounded quotient cannot exist.

Proof. In any illuminated room there is a state with illumination label true, reachable from c(e1). If the quotient has at most F states, a shortest state-path to a true state has at most F-1 edges. Applying the same generator word to e1 gives an ACTUAL primitive direction with true label, by deterministic transition compatibility and the exact label premise. Each generator has induced infinity norm at most2, so that direction has infinity norm at most2^(F-1). Choose the square family above with n>2^(F(4)-1). Every direction in the Gamma orbit differs only by signed coordinate permutation. Every actual illuminating direction has Euclidean norm>=sqrt(n^2+1), whereas a vector with infinity norm<=2^(F-1) has Euclidean norm<=sqrt(2)*2^(F-1). To avoid this norm-orbit issue choose n>sqrt(2)*2^(F(4)-1). Then neither it nor its Gamma orbit can illuminate, contradiction.

If states label a designated physical launch direction instead of a Gamma orbit, the sharper infinity-norm bound n>2^(F(4)-1) suffices directly. The orbit-qualified proof uses the safe sqrt(2) factor above. No parameter-dependent jump generators or weighted-state algorithms are excluded by this argument.

## 3. Effect on the current proof strategy

The number of combinatorial first-Xi-return edges is bounded by W, but the integer lengths, relative phases or return-word data cannot all be discarded to obtain the exact bounded-state SL2Z quotient above. A repeat of an unweighted graph type is not a stopping certificate for a search across directions.

The directionwise skeleton remains useful as a BOUNDED-DIMENSION WEIGHTED representation. A genuine next proof would need an invariant or reduction for arbitrary integer weights, or parameter-dependent arithmetic acceleration with a proof of completeness. We have not supplied that invariant. No further finite direction census follows from this result.

No dark pair, no uncapped lower bound, no global finite-case reduction and no novelty claim is established by this hostile family. It is an exact test that changes the admissible proof strategy.
