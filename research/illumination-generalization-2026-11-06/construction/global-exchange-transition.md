# B05: exact shear exchange and a concrete potential obstruction

Original effort08:56–09:10 UTC, aggregate840seconds, no renewal. The orthogonal target is r<=8, since W=2r+4; mixed-direction rooms require a separate argument. Universal illumination remains OPEN. This is hand transition algebra and prescribed frozen controls, not a new orbit census or lower bound.

## 1. Entire labelled-state algebra

Use composition right-to-left. A state is(h,v,L), with the ENTIRE connected labelled cover, all regular sheets and all source/target labels retained. Before the canonical relabelling used by the saved decider, the anchored moves are

    T(h,v,L)=(h,v h^-1,L),
    U(h,v,L)=(h v^-1,v,L).

Their inverses are T^-1(h,v)=(h,vh) and U^-1(h,v)=(hv,v). The southwest-vertex permutation

    C=v h v^-1 h^-1

is EXACTLY unchanged under T and U, not just conjugate. Consequently its nontrivial cycles mark the same true zeros. In the saved orthogonal22control there are nine cycles of length3 and33 fixed points. All genuine-zero indices are forbidden. Labels marking regular convex corners remain present but are TRANSPARENT for these tests. Every transformed state retains all four actual source and four target lifts. Canonicalization is a common relabelling only; every feature below is invariant under it.

Let P_w(s) follow a permutation w from EACH source-labelled index. Stop at its first genuine zero, first target or return to that SAME starting source index; another source index is allowed in between. Put H_w equal to the number of source starts reaching a target, and R_w equal to the number returning periodically with no zero or target. R counts MARKED SOURCE STARTS, not distinct cycles: two source marks on one periodic component count twice. This includes the regular periodic source components singled out by the coordinator.

Write H=H_h, R_h,R_v, and R_d=R_(h v^-1). In particular

    (h v^-1)^-1=v h^-1.

For a source-only regular periodic cycle, reversing its orientation changes neither zero-freeness nor the absence of target labels. Therefore

    R_v(Ts)=R_h(Us)=R_d(s).

This is exact for ALL permutations/labels with the stated full-cycle convention. A source-only periodic component cannot turn into a zero-terminated trace under reversal. We do not claim equality of forward first-target counts or of forward stopping lengths under inverse permutations in general.

Any potential Phi depending on h and labels alone has Phi(Ts)-Phi(s)=0. Any Psi depending on v and labels alone similarly has zero U-coboundary. Thus ALIGNED directional potentials cannot provide exchange charge. A crossed proposal is Phi=lambda R_v, Psi=mu R_h, giving

    D(s)=lambda(R_d-R_v)+mu(R_d-R_h).

It has actual, testable transitions; no ray directions are concatenated.

## 2. Three prescribed states disprove the crossed count charge at the threshold

The existing60-square known22certificate has raw SHA256
2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346.
Its lexicographic saved state462 (zero-based) is the FIRST saved state whose root returns without a true-zero hit. The coordinator had already verified1728 such states exist. Retrieving this first state is frozen-certificate retrieval, not construction of a new orbit. Its root cycle is0->1->3->5->0. Its other source indices are3,37,54; all four source starts return periodically. The complete labelled state and all trace lists are in global-exchange-periodic-check.json.

Call it A, put B=U^-1 A, and put C0=T U^-1 T A (the anchored quarter-turn WORD, applied in that listed order). All three have r9 and H_h=H_v=H_d=0. Exact values are:

|state|(R_h,R_v,R_d)|crossed D|
|---|---|---|
|A|(4,0,0)|-4mu|
|B|(0,0,4)|4(lambda+mu)|
|C0|(0,4,0)|-4lambda|

For any proposed inequality

    H(s)>=(9-r)*a(s)+D(s)

asserted INCLUDING the threshold r9, these three dark states require mu>=0,lambda+mu<=0,lambda>=0. Thus lambda=mu=0. No NONZERO constant crossed linear return-count potential can meet that threshold calibration. The unit proposal lambda=mu=1 fails already at B:0>=8 is false. Adding linear zero-stop counts does not repair this class, because on these dark controls B_w=4-R_w; additive constants disappear from coboundaries.

This does NOT refute an inequality stated ONLY for r<=8, arbitrary label-dependent potentials, coefficients allowed to vanish at r9, or the conjectured minimum itself. The distinction is essential. The known22 control falsifies a specific proposed threshold-uniform charge, not every possible charge.

## 3. Actual first-hit lengths reject a larger symmetric cost class

Let F_w=sum_sources f(type,first-stop length), using the SAME terminal-cost function for both directions, and take Phi=F_v,Psi=F_h. This includes regular periodic components without deleting them. Unlike R, first-zero lengths are orientation-sensitive; compute the actual transformed permutations v h^-1 and h v^-1 separately.

The prescribed checker global-exchange-cost-check.py/json records these exact bags. Write P=f(periodic,4), X=f(zero,1), Y=f(zero,3).

|state|h|v|T-vertical|U-horizontal|actual crossed increment|
|---|---|---|---|---|---|
|A|4 P4|4 Z1|2 Z1+2 Z3|2 Z1+2 Z3|4Y-4P|
|B|2 Z1+2 Z3|4 Z1|4 P4|4 P4|8P-2Y-6X|
|C0|4 Z1|4 P4|2 Z1+2 Z3|2 Z1+2 Z3|4Y-4P|

Here P4/Zj denote terminal TYPES and LENGTHS, not geometric suppression. If the proposed inequality extends to r9, H=0 forces both increments nonpositive. Hence

    P>=Y,    8P<=2Y+6X,

and therefore Y<=X. Consequently ANY symmetric additive terminal cost with f(zero,3)>f(zero,1) is impossible in this threshold-valid crossed form, REGARDLESS of its assigned periodic-return cost. In particular the total first-stop-length potential cannot be repaired simply by reweighting periodic returns: lengths give Y=3>X=1. Its actual crossed increments on A,B,C0 are -4,24,-4.

This is a symbolic necessary condition from two exact controls, not fitted coefficients and not a universal exclusion of label-aware or direction-asymmetric potentials. A decreasing or constant zero-length cost, a richer feature, or an inequality confined to r<=8 remains unexcluded. No inverse first-hit-length identity was assumed.

## 4. An r0 blind control limits positive weights on regular returns

Reuse the already independently accepted W4 square[0,24]^2 with actualA marks S=(12,12),T=(16,18); this is an EXISTING control, not a new room case. Its four-copy unfolding is the flat torus modulo48Z². Source images are{12,36}x{12,36}, target images{16,32}x{18,30}. No genuine zero exists. Horizontal source cycles have y12or36; targets have y18or30. Vertical source cycles have x12or36; targets have x16or32. Diagonal h v^-1 cycles have x+y=0or24mod48 at the sources, versus2,14,34,46 at targets. Therefore H_h=0 and R_h=R_v=R_d=4.

Every crossed count coboundary above is0 at this state. An inequality using these potentials and r0 thus forces a(s)=0 there. In particular the concrete choices a=1/N or a=R_h/(4N), positive even after degree normalization, FAIL: their positive9a cannot be paid. This refutes a natural regular-return weight IN THE REQUIRED LOW-W DOMAIN. It does not refute a weight allowed to vanish on these states and have a positive orbit sum elsewhere. The square is directly illuminated in primitive direction(2,3); those other directions are indispensable.

## 5. Finite-orbit averaging needs a constructive local claim

On a finite connected T/U orbit, any sum of coboundaries has orbit sum0. At dark r9 with H=0, a threshold-valid inequality forces D=0 pointwise, because D<=0 everywhere and its finite sum is0. This explains why the known22 control is a stringent calibration of local potentials.

Unrestricted existence of Phi,Psi supplies no theorem by itself. The incidence/divergence map of the connected T/U orbit graph has image equal to all zero-sum functions (solve along a spanning tree). Thus f>=Delta_T Phi+Delta_U Psi is solvable iff sum f>=0. Applied to f=H-(9-r)a, the proposed potential existence is just its desired orbit-mean inequality unless Phi,Psi and a are explicitly constructed and locally proved. For r<9, allowing an arbitrarily small uniform a makes unconstrained existence equivalent to some H being positive. No novelty or positive wall bound follows from this reformulation.

This graph statement does not erase the distinction between the finite LABELLED cover orbit and the FULL transported physical real involution. The latter need not have finite orbit; see global-exchange-real-structure.md. Averaging a structure-dependent potential requires a descent theorem.

## 6. Result and next proof obligation

We have exact anchored transition identities, a concrete falsification of the simple threshold-valid periodic-count charge, an obstruction to all strictly increasing symmetric zero-length costs in the threshold-valid crossed form, and an r0 obstruction to positive regular-return weights with count potentials. No positive9-reflex inequality is proved. The original specialist target remains viable only with a genuinely richer, precisely defined local feature/weight and a demonstrated descent or equivariance treatment of the physical real structure. Raw ramification, unlabelled connectivity and degree suppression were not used.
