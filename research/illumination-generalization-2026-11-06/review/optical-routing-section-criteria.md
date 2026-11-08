# Independent section matching prerequisites

Codex01a1a00f, resumed optical phase, 2026-11-07. HAND derivation with prescribed exact controls. No discovery search. This establishes necessary and conditional sufficient criteria only; no positive low-reflex theorem is asserted.

## 1. Physical convention and a complete state

D is a finite strictly simple orthogonal polygon. Every actual vertex is forbidden, including convex corners that become regular points in an unfolding. S,T are distinct actual interior points. A section J is an open segment in D, transverse to the trajectory, and creates no reflecting wall. A mouth may be an interior seam of an original room. In a covering description retain its actual lift label, not just projected coordinates.

On a vertical section x=c write a state as (z, sigma, m, sheet): actual point (c,z), signed horizontal velocity sigma in {+1,-1}, slope m=v_y/v_x, and actual sheet. Unit velocity is sigma*(1,m)/sqrt(1+m^2). Equal slopes alone admit opposite directed velocities. For gluing source and REVERSED-target trajectories at a section, their directed velocities must be negatives; if both states are oriented in the final forward direction, they must be equal. Sheet and section-component labels must agree. Artificial seam endpoints need not be actual polygon corners, but open-section formulas exclude them; completeness needs another chart if a valid path crosses an excluded regular seam endpoint.

Horizontal sections use swapped coordinates. The vertical-direction case v_x=0 is not represented by finite m and must be checked separately. A trajectory exactly parallel to J does not define a transverse crossing.

## 2. Exact fixed-word scattering formula

Start from P=(c,z) with v_x>0. Fix a finite physical wall itinerary w, ending at Q=(c',z') on another vertical section. Develop the itinerary by successive reflections into the initial Euclidean chart. Its terminal chart map is

    U_w(q)=E q+v, E=diag(e_x,e_y), e_x,e_y in {+1,-1}.

All supports are axis parallel, so E is diagonal. For integer wall coordinates v lies in (2Z)^2. The terminal section develops to x=e_x*c'+v_x. Put L=e_x*c'+v_x-c. Straight development gives

    L>0,
    z'=e_y*(z + m*L - v_y),
    v_out proportional to (e_x,e_y*m),
    sigma_out=e_x,
    m_out=e_x*e_y*m.

The common positive normalization does not change reflection laws. The total developed vector is L*(1,m); time is L*sqrt(1+m^2) at unit speed. L=0 cannot represent a positive-length transverse flight in this chart. A negative horizontal start requires sigma*L>0 and outgoing horizontal sign sigma*e_x.

Proof: U_w(Q)-P=(L,e_y*z'+v_y-z). A developed billiard is a straight flight, so the second coordinate equals mL. Physical terminal velocity is E^{-1}(1,m)=E(1,m). This proves the formula. It does NOT prove that the selected physical itinerary occurs.

For identical physical position AND directed velocity on a repeated section with sigma=+1, necessarily e_x=+1 and e_y*m=m, as well as

    (e_y-1)*z + e_y*m*L - e_y*v_y=0.

At nonzero m the sign requirement also forces e_y=+1, leaving mL=v_y. Returning at the same section coordinate while reversing horizontal velocity is not an identical-state return. A forward continuation can legitimately require a changed return state; identical-state resonance is not assumed necessary for existential rerouting.

## 3. Source and target branches are affine graphs

Fix a complete development in which a source branch and a compatible forward target suffix are compared at a developed vertical section x=C. Let the source and target images in this SAME chart be (X_S,Y_S) and (X_T,Y_T), and assume the forward developed horizontal sign is +. The source crossing and reversed-target crossing, oriented forward, satisfy

    z_S(m)=Y_S+m*(C-X_S),
    z_T(m)=Y_T+m*(C-X_T),
    f(m)=z_S(m)-z_T(m)
        =Y_S-Y_T + m*(X_T-X_S).

Thus a transverse positive flight through this section requires

    X_S<C<X_T,
    f(m)=0,
    m=(Y_T-Y_S)/(X_T-X_S),

plus legal source/suffix itinerary guards and correct actual endpoint/lift identities. The section can occur at an endpoint of the decomposition only with an explicitly adjusted convention. If an intervening scattering branch is present, substitute the formula in section 2, transform its slope/sign into the target chart, and require common orientation. For fixed reflection signs its resulting position defect is still affine in the original m.

If X_T=X_S, a positive transverse flight in this chart is impossible. If also Y_T=Y_S, f vanishes identically but the coincident unfolded endpoint gives zero total displacement, not a positive straight path. An identically zero matching expression therefore requires separate time/orientation scrutiny. It cannot by itself establish a family of actual paths.

For a full physical word from S, the developed target U_w(T) determines at most one positive directed launch. With even-even S,T and integer supports its displacement is in (2Z)^2; every nonvertical exact-target slope is rational. This is an arithmetic necessary condition, not a bound on words or a finite search algorithm.

## 4. Strict first-hit domain and connected branches

A wall word is legal only if every designated contact lies strictly inside its finite wall, reflection is genuine and specular, successive contact times strictly increase, and no earlier wall or actual corner interrupts a segment. The final flight must terminate at actual T on the specified sheet before its next true-wall collision. A valid path that encounters T earlier may be truncated there, but then the claimed later itinerary is not its first-arrival itinerary.

There is an exact way to derive the guard set. In the fixed developed strip, each transformed true wall has fixed finite endpoints and horizontal or vertical support. For source (X,Y), a vertical-support crossing has horizontal parameter lambda=constant; a horizontal-support crossing has lambda=(constant-Y)/m. Restrict to m>0, m<0, or the isolated m=0 case before clearing denominators. Finite-wall endpoint tests and chronological comparisons become strict linear inequalities in m. A source crossing z=a+b*m at a fixed section gives horizontal lambda=(constant-a)/m-b, again yielding linear inequalities after the sign split.

For a fixed finite word, the finitely many transformed endpoints, support crossings and chronological comparisons give a finite partition of the slope chart. Each connected open cell has fixed signs for all guard predicates. The legal domain is a finite union of such intervals, with separately handled zero-slope and geometric degeneracies. Calling a word a branch does not itself prove its legal domain connected: occlusion predicates must be resolved, and a connected component must be selected before using an interval argument. Strict tests deliberately exclude true corner collisions and simultaneous adjacent-wall hits. Coordinates or derivatives of these graphs say nothing about whether a missing boundary point is admissible.

Conditional root criterion: if a SAME branch has a nonempty connected interval I with every guard proved, compatible orientation/lift labels, and f=A+B*m, then for B!=0 it yields a path exactly when -A/B belongs to I. A strict sign change f(m_0)*f(m_1)<0 at two legal slopes in I proves an interior root. Two legal slopes belonging to DIFFERENT itinerary components provide no such conclusion. Testing only the two prefixes is insufficient: the entire connecting branch must be legal. This criterion is sufficient by gluing the actual segments with equal position and directed velocity; it does not force the hypotheses to hold.

## 5. Three exact controls the author must survive

1. Opposite velocity: in [0,8]^2, start at section (3,2), velocity (1,1/4), and reflect once at x=8. Return to x=3 at height9/2 with velocity(-1,1/4). E=diag(-1,1), v=(16,0), L=10. Slope changes sign. Reflect instead at right then left before returning: E=I, v=(16,0), L=16, final point(3,6), original velocity restored but position not restored. Both paths are smooth. A projection-only return or a sign-free slope comparison is not a gluing certificate.

2. Root on excluded corner: Q=[0,8]^2, S=(2,2), T=(6,6), nominal wall word top then right has target image(10,10). Matching m=1 gives an exact unfolded target equality, but the ray hits(8,8) simultaneously on both walls. There is no legal realization of that word. The actual pair is directly illuminated by another word. Hence this control invalidates a guard-free implication, not existential illumination.

3. Inherited controls, no new search: the r1 square-ear example in geometric-reduction-resonance-gap.md is lit and has no reduced-room target witness satisfying identical-state ear resonance. The original r9 known22 room is actually dark despite illuminated H/V/C1 simplifications. A valid universal phase-space formalism applies to both, so the formalism alone supplies no positive r<=8 statement. Any low-reflex conclusion needs a new geometric fact forcing a legal root or an avoidance witness, not merely a cutoff appended to these equations.

## 6. What would count as new positive progress

The exact missing assertion is not existence of these curves or equations. It is a noncircular low-reflex theorem guaranteeing that at least one compatible pair of branch graphs has its exact root inside its guarded domain, or producing an original-room path by another explicitly justified construction. This needs a proved effect of ORIGINAL r<=8. Topological reachability, measure preservation, open finite-prefix cones, recurrence and qualitative density do not establish intersection with a specified target curve.

This packet is an independent prerequisite audit, not the first positive rerouting lemma requested of the author. No entire-room result is claimed. Frozen prior files are unchanged; mixed axial/diagonal canonical45 remains separate and open.
