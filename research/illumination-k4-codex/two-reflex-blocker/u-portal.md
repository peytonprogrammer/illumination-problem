# Next case: one boundary blocker in an eight-wall U room

[in progress] Theory only; disjoint from Opus's non-parity folding expansion.

## Geometry and the real new difficulty

Fix0<a<b<A and0<c<min(C_L,C_R). The U-shaped room has cyclic boundary

    (0,0),(A,0),(A,C_R),(b,C_R),(b,c),(a,c),(a,C_L),(0,C_L).

Let s=(x_s,y_s) be interior high in the left arm:0<x_s<a and c<y_s<C_L. Let t=(x_t,y_t) be interior high in the right arm:b<x_t<A and c<y_t<C_R. Every connecting path must enter the lower passage y<c and rise again. Since vertical reflections preserve the sign of vertical velocity, an ordinary connection must reflect at least once at a horizontal wall. Therefore the L-room proof's two-orientation avoidance property is false in this geometry. This does not imply a dark pair or an essential point blocker.

The two interior portals are x=a,y in(0,c), and x=b,y in(0,c). Aim first for paths strictly increasing in x; these use only horizontal-wall reflections and automatically avoid every smooth vertical-wall blocker. The unresolved singleton is therefore a prescribed point on a horizontal wall.

## Proposed exact criterion for a path crossing each portal once

Put L=a-x_s>0, M=b-a>0, R=x_t-b>0, D=L+M+R=x_t-x_s. Let

    Y_s=epsilon_s*y_s+2n*C_L,
    Y_t=epsilon_t*y_t+2m*C_R,

with epsilon_s,epsilon_t in{+1,-1} and n,m integers. These are the reflection images in the full-height left/right strips. For the lower passage choose an integer k and a middle-strip reflection sign sigma in{+1,-1}. Set

    lambda=(sigma*Y_t+2k*c-Y_s)/D,
    u=Y_s+L*lambda,
    v=sigma*(Y_s+(L+M)*lambda-2k*c).

The proposed necessary-and-sufficient condition within this x-monotone, one-crossing-per-portal class is

    0<u<c and 0<v<c.

Derivation: in the left strip, unfold backwards from portal height u to source image Y_s, giving u=Y_s+L*lambda. In the middle strip the developed exit height is u+M*lambda=2k*c+sigma*v. The physical outgoing slope after folding the middle strip is sigma*lambda. In the right strip its unfolded target is Y_t=v+sigma*lambda*R. Eliminating u,v gives the displayed formula.

Strict portal inequalities avoid the reflex corners. Every other horizontal-wall crossing lies strictly inside one of the three strips, hence on a smooth wall; there are only finitely many such crossings for a fixed choice of integers. This paragraph and the exact branch conventions still need an independent algebra/geometry check before acceptance.

## Next gate

1. Verify both directions of this parameterization and all middle-fold signs using prescribed formula controls.
2. Decide which parameters guarantee the two open portal windows can be satisfied. Do not assume the answer is always yes.
3. For a fixed smooth horizontal blocker z, derive its exact hit congruence within this family. Prove that some admissible integer choice avoids z, or identify the algebraic obstruction to this particular family. Failure of the family is not a dark-room certificate.

No ray, room, reflection-word or direction discovery searches. The objective is a blocker-removal theorem for this one8-wall family, or a precise limitation on the method. Other8-wall shapes, mixed-orientation multiple blockers, contacts, slits and global minimum remain outside this step.

## Verified portal parameterization and invariant

The parameterization is valid for the stated x-monotone family. Fold each strip's vertical coordinate with F_h(y)=dist(y,2h Z). At the left portal u is strictly between0 and c, so the left-strip fold is locally the identity. In the middle strip the exit lies in the branch 2kc+sigma v, whose derivative is sigma. The right strip begins at v in(0,c), so its fold is initially the identity. The derivatives therefore match at both portals. All other fold crossings occur at x strictly within a strip, hence away from its corners. Conversely unfold any x-monotone connection separately in the three strips: its source and target images and its middle exit branch give exactly the displayed integers and signs. A horizontal segment cannot connect the high opposite arms; lambda=0 cannot satisfy the portal conditions.

Elimination gives a useful necessary invariant:

    R*u + sigma*L*v = R*Y_s + sigma*L*Y_t.

This is necessary for every such connection, including arbitrarily many horizontal reflections. It proves that this family cannot establish a general U-room theorem.

### Exact obstruction 1: no x-monotone connection

Set a=2,b=3,A=5,C_L=C_R=1,c=1/10, x_s=1,x_t=4. Then L=R=M=1. Take y_s=1/3,y_t=2/3. Every right-hand side Y_s+sigma Y_t belongs to a signed sum +/-1/3+/-2/3+2Z. Its distance from zero is at least1/3. But the left-hand side u+sigma v has absolute value less than2c=1/5. Contradiction. This excludes only x-monotone paths, not all billiard paths.

### Exact obstruction 2: every x-monotone connection shares one smooth blocker

Keep the geometry, but set y_s=y_t=2/5 and z=(5/2,1/10), the midpoint of the notch bottom. The image-sum residues modulo2 are0,4/5,6/5. If sigma=+1, 0<u+v<1/5, impossible. If sigma=-1, |u-v|<1/10 forces Y_s-Y_t=0, hence u=v and Y_s=Y_t=+/-2/5+2n.

The portal formula becomes u=(Y_s+k/5)/3. The strict window0<u<1/10 gives

    0 < 10Y_s+2k < 3.

The middle expression is an even integer, so it equals2. Thus u=v=1/15 and k=1-(+/-2)-10n is odd. At x=5/2 the developed middle height is kc. Since k is odd, it folds to c. Every x-monotone connection therefore hits z.

Nevertheless the exact ordinary path

    (1,2/5) -> (0,2/7) -> (5/2,0) -> (5,2/7) -> (4,2/5)

avoids z. It reflects at the two outer vertical walls and the bottom wall; its portal heights are2/35<1/10. This is a prescribed algebraic construction, not a ray search. It proves that a common blocker for the restricted path family need not block the full billiard dynamics.

## Constructive lemma for symmetric U rooms

Let the arm widths and heights agree: b=a+M,A=2a+M,C_L=C_R=H. Let s=(x,y),t=(A-x,y), with0<x<a and c<y<H. These marks always have a corner-free connection whose sole horizontal reflection is at the bottom midpoint (A/2,0). Consequently it avoids every horizontal-wall blocker except that midpoint.

Proof. Put L_n=a-x+2na for n>=0. Choose the smallest n such that

    u_n = yM/(2L_n+M) < c,

which exists. Set beta=2y/(2L_n+M). In a horizontal unfolding of the left arm, move right from (x,y) with slope-beta for horizontal distance L_n. Fold the horizontal coordinate into[0,a]. At the last inner-wall crossing the point is(a,u_n); after it continue through the lower passage to(A/2,0), reflecting there, then take the mirror-reversed path to t.

It remains to check earlier inner-wall encounters, which must stay above c. If n=0 there are none. Otherwise the last earlier encounter is2a units before the portal, at height

    u_n+2a*beta = y(M+4a)/(2L_n+M).

Minimality gives2L_n+M<=yM/c+4a. Hence the last earlier encounter has height at least y(M+4a)/(yM/c+4a)>c, since y>c. All earlier encounters are higher still and belowH. Every outer-wall encounter has height strictly between u_n and y, so it is smooth. The final portal is strictly inside(0,c), the middle bottom hit is smooth, and reflection laws follow from horizontal unfolding and symmetry. There are finitely many bounces. This proves the lemma for real parameters, without rationality assumptions.

This one-phase lemma alone leaves the bottom midpoint and vertical blockers. The two-phase theorem below resolves both for these symmetric rooms and marks. Nonsymmetric rooms/marks and arbitrary finite blocker sets remain outside scope.

## Two-phase theorem: every single boundary blocker is avoidable

Let a,M,c,H>0 with c<H, A=2a+M, and let the U room be

    [0,A] x [0,c] union [0,a] x [c,H] union [a+M,A] x [c,H].

Take s=(x,y),t=(A-x,y), with0<x<a and c<y<H. For every smooth boundary point z there is a finite, corner-free billiard connection s to t avoiding z. In fact three explicitly constructed paths have no common boundary contact. This is a theorem for real parameters, not a claim about arbitrary U-room pairs or arbitrary finite blocker sets. A separate tools-disabled Opus reviewer accepted the theorem after symbolic audit (`peer-review.txt`); the live coordinating peer also accepts the theorem and its open-neighborhood corollary (`claude-illumination-check/u-review/findings.md`).

### Available arm lengths

A horizontal unfolding of the left arm reaches the portal x=a after one of the lengths

    L_minus(n)=a-x+2na,     L_plus(n)=a+x+2na,    n>=0.

The minus phase starts right; the plus phase starts left. Given any threshold T>=0, take the first length of each phase strictly greater than T. Both lengths lie in(T,T+2a], are distinct, and differ by less than2a. Explicitly, for base length ell=a-x or a+x,

    n=max(0,floor((T-ell)/(2a))+1),  L=ell+2na.

The nearest earlier encounter with the inner wall x=a, when one exists, is2a units before the final portal. The nearest outer-wall encounter, when one exists, is a units before it. These are distances in the horizontal unfolding.

### Two bottom-centered connections with disjoint vertical contacts

Put h=M/2 and Y=y/c>1. Use threshold T_B=h(Y-1), selecting both arm phases as above. For each selected L set

    beta_B=y/(L+h),     u_B=yh/(L+h).

The developed ray descends from height y to0 over total horizontal distance L+h. In the arm fold its horizontal coordinate into[0,a]; then pass through(a,u_B) and reflect at the bottom midpoint z_B=(A/2,0). Continue by vertical reflection and time reversal of the left half to t.

Since L>T_B, 0<u_B<c. If an earlier inner-wall encounter exists, its height is

    y(h+2a)/(L+h) > c,

because L<=T_B+2a<T_B+2aY. All arm heights are strictly positive and less than H, so no other corner or horizontal wall is hit. Thus both paths are valid and their sole horizontal contact is z_B.

Their vertical contacts are disjoint. A left outer-wall contact has remaining arm length r=(2j+1)a, and a left inner-wall contact has r=2ja with j>=1. Its height is

    v=y(h+r)/(L+h).

For two paths hitting the same vertical-wall point at height v,

    r_1-r_2=(v/y)(L_1-L_2).

For the same wall r_1-r_2 is a multiple of2a. But0<v<y and0<|L_1-L_2|<2a, so its magnitude is less than2a. It must be0, which would force L_1=L_2, a contradiction. Right-arm contacts obey the same argument by symmetry. Left and right vertical walls are distinct since M>0. Therefore the common boundary-contact set of these two paths is exactly{z_B}.

### A notch-centered connection avoiding z_B

Use threshold T_N=h(Y-1)/2. Take the first length of each phase strictly greater than T_N. At most one equals K=hY. Choose either one that does not equal K and write it L. Set

    beta_N=(y+c)/(L+h),     q=y-beta_N*L=c(K-L)/(L+h).

In the horizontal unfolding let the vertical coordinate be y-beta_N*d, where d is distance traveled. Fold this coordinate by absolute value and fold x into the arm until distance L. Then continue in the lower passage to the notch midpoint z_N=(A/2,c), which has developed height -c. Reflect at z_N and take the mirror-reversed left half to t.

The portal is strict: q!=0 since L!=K. If q>0, the bound |q|<c is equivalent to L>T_N; if q<0 it is automatic. Thus its physical height |q| lies in(0,c). The arm has exactly one possible horizontal reflection, at developed height0. It occurs either inside the arm or in the lower passage before z_N; it cannot be at the central bottom point because the half-path remains strictly left of x=A/2 until z_N.

Check all earlier inner-wall encounters. The last one's signed height, if present, is

    e_inner=y-beta_N*(L-2a).

The condition e_inner>c is equivalent to

    L<T_N+a(Y+1).

It holds because L<=T_N+2a and Y>1. All earlier inner-wall encounters are higher still, so none exits prematurely through the low portal or hits a reflex corner.

Check an outer-wall/bottom coincidence. The last outer encounter, if present, has signed height

    e_outer=y-beta_N*(L-a).

It is positive exactly when L<K+a(Y+1). This follows from L<=T_N+2a, since

    K+a(Y+1)-(T_N+2a) = h(Y+1)/2+a(Y-1) > 0.

All earlier outer encounters are higher. Thus a bottom hit inside the arm occurs strictly after its last vertical-wall hit and strictly before its final portal. It cannot hit a bottom corner. A bottom hit in the lower passage is also smooth because |q|>0 and the central endpoint has height c. Physical heights in the arm never exceed y<H; the open passage segment has height less than c. The notch endpoint lies strictly inside its horizontal wall. At z_N the incoming velocity has positive horizontal and vertical components. Reflecting the reversed left half across the vertical symmetry axis preserves its horizontal component and reverses its vertical component, exactly the horizontal-wall reflection law. The same check with downward incoming velocity applies at z_B. All slopes are finite and nonzero, so no path glides along a wall. There are finitely many wall hits. This proves validity, including the exact resonance case K equal to one phase length.

### Singleton removal

If z!=z_B, at least one of the two bottom-centered paths avoids z because their only common boundary contact is z_B. If z=z_B, use the notch-centered path. All three avoid every actual room corner. This proves the theorem.

The proof also gives a fixed three-path certificate for the absence of any singleton boundary blocker for each room/mark pair in this symmetric family. It does not imply that two or more boundary blockers can always be removed.

### Open-neighborhood corollary

For every symmetric U/mark configuration covered by the theorem, the absence of a singleton boundary blocker persists in an open neighborhood of that configuration. The nearby U rooms and mark pairs need not remain symmetric.

Each of the three constructed paths has a finite reflection word, with every wall contact strictly inside its wall and every segment avoiding all other walls/corners. Its reflections are transverse. Under sufficiently small changes of the wall positions and interior marks, unfold that same finite word and join the perturbed source to its reflected target. All strict intersection/order conditions persist, so each path and all its boundary contacts vary continuously.

Let A_1,A_2,A_3 be the finite boundary-contact sets of the three paths. They have empty triple intersection. Therefore

    delta=min{max(|p1-p2|,|p1-p3|,|p2-p3|): p_i in A_i}>0.

If every contact moves less than delta/4, a common point of the three new contact sets would make every old pair distance less than delta/2, contradicting the definition. Thus their triple intersection remains empty. All possible boundary blockers are simultaneously covered by this argument; the neighborhood is chosen before the blocker.

This supplies open regions in the U-room parameter space with singleton removal. It does not assert those regions cover every U room or every mark pair.
