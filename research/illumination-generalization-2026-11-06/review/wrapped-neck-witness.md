# Actual witness existence through a neck without global supporting half-planes

R28 positive theorem for independent review. This removes an unnecessary supporting-line condition from the accepted one-neck construction and hence from the two-neck finite-lattice reduction. No arbitrary coordinate-strip decomposition or prefix illumination is asserted.

## 1. Precise model

Fix w>0 and two finite strictly simple orthogonal closed chamber disks C_- and C_+, each with the smooth relative-interior boundary mouth M={0}x[0,w]. Fix actual interior S in C_- and T in C_+. At a length L>0 form

    P_L=C_- union ([0,L]x[0,w]) union (C_+ +(L,0)).

A member is ADMISSIBLE only if the three piece interiors are disjoint, their only contacts are the intended mouths, the mouth gluings are two-sided, and the union is a strictly simple polygonal disk. In particular there is no unintended contact between a chamber and a neck sidewall. Chambers are allowed to wrap to either side of their mouth supporting line OUTSIDE the neck band. We do not require C_- subset{x<=0} or C_+ subset{x>=0}.

**Wrapped-neck theorem.** There is a finite threshold L_* depending on the fixed data such that EVERY admissible L>L_* illuminates the actual pair S,T+(L,0). If every member above a lower bound is admissible, this is an ordinary whole real tail. For rational data a valid threshold and a rational exact path above it are computable by the compatible-beam procedure described in effective-joint-prefix.md section3.

## 2. What admissibility supplies locally

At every relative-interior point of M, the left chamber has a smooth local interior half-disk. That half-disk must be on the LEFT: the neck occupies the right half-disk, and disjoint interiors prohibit the other choice. The translated right chamber similarly has its local half-disk on the RIGHT of its mouth. This is a LOCAL statement, not a claim about any other part of either chamber.

For an admissible member, every chamber boundary point outside its mouth remains an actual wall point of P_L. Otherwise another piece would fill or contact a neighborhood across that boundary, an unintended contact prohibited by the model. In the open neck, its two sidewalls remain actual smooth walls. These are the precise global boundary facts needed by the optical construction. A wrap outside the neck band changes none of them.

## 3. Compatible closed-chamber beams

Use the SAME independently accepted directional input as long-neck-proof.md section1: in fixed orthogonal rational-angle chambers choose one positive magnitude m0 outside the exceptional direction classes for density, corners, BOTH mouth endpoints (even when smooth subdivision points), and axes, for the two actual interior marks. Directions to these finitely many mouth endpoints form a countable set by the same finite-wall-word argument as directions to corners. Excluding them ensures that an earlier cap-endpoint reflection cannot become a forbidden created corner after gluing. Both auxiliary CLOSED chamber trajectories are dense on their invariant surfaces, avoid all genuine corners and hit the smooth mouth interior in finite time. Their first-mouth prefixes contain no prior cap reflection. Nothing in this directional theorem assumes a chamber lies on one side of its mouth line.

The local sidedness from section2 forces the left first-mouth velocity to have positive horizontal component and the right first-mouth velocity negative horizontal component. Their finite word/first-mouth guards persist on a common open magnitude interval. Unfolding those prefixes in their final physical mouth charts produces virtual points

    S_*=(-a,alpha), T_*=(b,beta), a,b>0.

This sign is obtained from POSITIVE travel time with the final directed horizontal velocity, not from physical locations of S,T or a global support assumption. Reflections in earlier chamber walls produce the virtual points even when the actual marks lie past the mouth supporting line in a wrapped lobe.

Let epsilon_-,epsilon_+ be the signs of vertical velocity at those two first-mouth hits, set tau=epsilon_-*m and sigma=-epsilon_-*epsilon_+. A bounded signed-slope interval I=(u0,v0), away from0, preserves both prefixes and all strict guards. Its positive length is delta. The mouth heights are exactly

    z_-(tau)=alpha+a*tau,
    z_+(tau)=beta-b*sigma*tau,

strictly in(0,w). This is the already checked common-magnitude sign calculation; it uses only the final mouth charts and finite word openness.

## 4. Exact phase and actual walls

Reflect/translate the right chamber's unfolded target to

    (L+b,2*n*w+sigma*beta).

The line from S_* to this point has slope

    tau_n=(sigma*beta-alpha+2*n*w)/(L+a+b).

If L>max(0,2w/delta-a-b), the corresponding open numerator interval has length greater than2w, so some integer n makes tau_n strictly inside I. This achieves the exact phase relation

    alpha+tau_n*(a+L)=2*n*w+sigma*z_+(tau_n).

Fold the line in the rectangular neck with period2w. At its left end it has exactly the source-prefix position and velocity; at its right end it has exactly the position and velocity of the REVERSED target-prefix. Both ends are strict interior mouth points, all sidewall hits are longitudinally interior and smooth, and the finite neck has only finitely many reflections.

Every source/target chamber contact before its mouth is on a nonmouth boundary wall and hence remains an ACTUAL wall by section2. Neither virtual cap reflection occurs. The chamber paths lie in their own piece interiors, and the neck path lies in the neck interior; disjointness and the intended mouth contacts ensure that no wrapped lobe adds a hidden mirror or crossing. This joins one ordinary finite path to the ACTUAL T+(L,0). Earlier actual target arrival only shortens it. Thus the accepted one-neck proof and threshold remain valid under these weaker geometric premises.

Admissibility for all large L is not needed to prove the implication for one admissible member: the finite beams are fixed, and the phase argument works at every admissible length exceeding its optical threshold. A known geometric validity lower bound may be added to L_* when claiming a whole tail.

## 5. First-witness and finite-prefix consequences

For a finite tree of fixed chambers joined by independently variable fixed-width necks, suppose all members in a positive length orthant satisfy the same valid disjoint gluing conditions. Fix every length except one neck whose deletion separates the actual marked chambers. The two closed unions on its sides are strictly simple orthogonal disks (inductively glue the tree pieces), with the actual marks interior. They may wrap past the selected mouth line. The theorem above nevertheless supplies a genuine witness for all sufficiently large lengths of that edge. Thus this coordinate fiber has a first witness and a real tail without a supporting-half-plane premise. If S,T are in the same fixed chamber, this argument need not apply and makes no claim.

In particular take the A25 three-chamber chain with one horizontal and one vertical neck, actual marks in opposite outer chambers, fixed widths, and ALL members L>=ell,K>=kappa admissible. At each fixed coordinate the wrapped-neck theorem supplies a real tail. Fix one allowed L0, choose a sufficiently large K0 and obtain the FIRST actual witness. The independently accepted A25 joint-curvature theorem supplies its joint tail. Taking finite maxima over the bounded lattice coordinate strips leaves a FINITE rectangle of possible dark integer members. The EXTRA opposing-half-plane cuts in A25 section6 are no longer required; full admissibility of the fixed-piece model remains required.

For rational data, every grouped chamber, mark and mouth at a fixed lattice coordinate is rational. The compatible-beam search and explicit R27 thresholds therefore make this finite rectangle effectively computable. All component hypotheses and exact actual-path checks are retained. This does not verify the remaining rectangle or prove a supplied certificate pack covers it.

A tree alone does not imply admissibility for independently changed lengths, and general crossing strip generators can alter chamber shapes or widths. Neither condition is inferred. The theorem supplies witness existence on individually separated fibers and on the full two-neck parameter family; it supplies no witness on every orientation-locked multi-neck ray. The universal W<=21 claim remains OPEN.

## Dependencies and verification

The only imported dynamical input is the primary-checked directional beam theorem already accepted in long-neck-independent-acceptance.json. The exact phase and velocity calculation is rederived here from long-neck-proof.md, with each previous use of global support audited. The two-neck joint tail is perpendicular-neck-joint-proof.md, independently accepted. R27's effective refinements are invoked only with their own eventual independent acceptance; the qualitative witness/tail and finite-lattice conclusions here do not depend on R27.

Review targets: local sidedness from disjoint gluing, retention of nonmouth actual mirrors, virtual source/target abscissa signs without global support, all wrap/neck/corner contacts, closed grouped tree chambers, arbitrary actual marks in their interiors, first witness rather than an assumed reference, exact extra conditions removed and those retained. No new scan, computation or external theorem was used.
