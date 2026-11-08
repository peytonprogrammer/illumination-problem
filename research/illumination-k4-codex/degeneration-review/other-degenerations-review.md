# Review of Opus's other degenerations

[done] Reviewed the current Lemma 15, Corollary 16 and Propositions 17–18 in `claude-illumination-check/l3-analysis.md`. The useful local reductions survive with explicit hypotheses. The section does not yet exclude all degeneration limits.

## Lemma 15: angle monotonicity accepted, moving chart required

Step 3 is correct for an actual sector with origin at its actual vertex. Along x(u)=a+u d, the argument derivative has constant sign, since its numerator is cross(a,d). Unless the ray passes through the origin, its angular variation lies on the shorter arc from arg(a) to arg(d). If the two endpoint directions are in the same sector branch and differ by less than pi, their intervening arc stays in that sector. With the direction strictly inside and a strict less-than-pi margin, perturbations preserve this property, including a source approaching a wall.

The stated zoom uses the fixed limit point c instead of the nearby actual vertex c_n. Face convergence alone does not control |c_n-c| relative to |s_n-c|. The asserted fixed-sector zoom and the resulting angle test can fail.

Exact diagnostic: let h>0, c_n=(-h,0), and the local interior sector around c_n have angles (0,3pi/2). Put s_n=c_n+h^2(-1,-2), t_n=(2,1). Measured about fixed c=(0,0), arg(s_n) tends to pi, while the limiting direct word leaves c at psi=atan(1/2); their difference is less than pi. But the true angle arg(s_n-c_n)=pi+atan(2) differs from psi by more than pi. The direct segment crosses the forbidden fourth quadrant relative to c_n. The rational h=1/100 receipt gives a point on that segment in the forbidden quadrant.

This invalidates the proposed fixed-word proof under its written hypotheses. It does not show the whole room is dark, or contradict illumination through another word. Fix: define r_n=|s_n-c_n| and phi_s=lim arg(s_n-c_n), use the moving local vertex and its wall frame, and require the local wedge model to hold uniformly at that scale. A loop needs a positive-length developed limiting segment and the analogous moving-chart condition independently at its arrival end.

The final error estimate should use that corrected r_n and frame. It need not assume other endpoint motions are O(r_n): convergence of the aimed direction suffices for the local wedge margin, while strict contacts control the rest of the fixed word.

## Corollary 16: separate boundary conventions and tangent constraints

Items 2 and 3 are sound when the local convex sector or same-side wall strip persists, both actual marks remain interior, and no additional local feature degenerates. In a convex corner, use the moving vertex as above. They are not uniform statements under simultaneous neck collapse.

Item 1's no-robust-connection conclusion follows for every convex angle from the corrected lemma. The further regular-point explanation only covers the angles it lists: 45 and 90 degrees. A convex canonical 135-degree corner is not regular on the usual unfolding: its single lift has cone angle 6pi. Thus the argument cannot identify every convex-corner limit with a regular boundary point. Define admissible endpoint sectors directly; do not silently extend the regular-point case to 135 degrees.

The half-space certificate has the correct sign if dark event inequalities are g_i(v)>=0 and inward displacement is h(v)>=0: adding +h and obtaining positive spanning excludes any nonzero first-order feasible v. But h must be relative mark-to-moving-wall distance, not a normal applied only to the mark's absolute coordinates. For a corner use both active incident-wall inequalities in a convex wedge. The normalized slice, symmetry quotient, event endpoint validity and finite quadratic remainder are still required. Positive spanning of this augmented list is sufficient, not asserted necessary. If the test succeeds, it excludes nearby nonzero normalized inward approaches; tangent behavior must be included in the same uniform argument, not discarded by testing only strict inward vectors.

The reflex-wedge example is plausible in the unwrapped sector model: endpoint images are ±phi_t+2m alpha, and their angular separations from phi_s all exceed pi for the stated numbers. A physical-plane reflection image alone is not enough; retain the unwrapped sheet and valid word. The absence of robust loops in admissible endpoint arcs is a necessary condition for a dark sequence, not a classification of all sequences with no loops.

## Proposition 17: conditional acceptance

With distinct marks staying interior, one isolated contact as the only geometric degeneration, preserved labeled local faces on the complement, and ordinary billiard paths stopping at every genuine corner and at z, each finite connection is robust away from z. An interior-start segment cannot first graze the interior of a straight wall transversally; a tangent segment would have run on that line already. Wall-following connections require a separately declared convention and do not arise from an interior start without a corner. Thus Lemma 7 does give ordinary darkness in this explicitly blocked contact model.

As currently introduced, the section allows marks reaching the boundary or merging. Those cases are not covered by that argument. State the interior/distinct condition or carry endpoint sectors and apply corrected Lemma 15. Count at most W walls using inherited labeled faces, and specify how contact incidences split maximal segments. The sentence that the window's two corners merge is specific to a corner-window model; arbitrary corner-wall contacts require their own incidence description. No strict wall decrease or global exclusion follows.

## Proposition 18: proper-corner range and smooth-step counterexample

The angle-addition formula is correct. To infer a strictly simple W-1-wall limit, require 0<alpha<2pi, alpha!=pi, no other contact/overlap/collapsed feature, and two noncollinear remaining neighboring edges. Merely saying alpha!=pi does not exclude alpha=0 or 2pi. Marks must stay distinct and interior for ordinary darkness; boundary/merged marks retain the decorated endpoint conditions and are not automatically an ordinary distinct dark pair.

Case 2 is incorrect as a general description of one shrinking wall. A pi merged angle can be a smooth wall step, without any notch. Exact six-wall example, in counterclockwise order:

    (0,0), (2,0), (2,1), (2+h,1), (2+h,2), (0,2).

Only the horizontal edge of length h collapses. Its adjacent angles are 270 and 90 degrees, so their merged angle is pi. In the limit, the two vertical neighbors merge into one maximal wall and the room becomes a four-wall rectangle: W decreases by two. Nothing is a notch bottom, and no two-sided bounded shadow follows from these hypotheses. The diagnostic does not claim these approximants are dark; it refutes the geometric classification used in the proposed reduction.

A genuine shrinking notch typically involves a cluster of collapsing edges or an additional small scale. Its local passage intervals depend on that cluster, the chosen word and its direction. Derive them from the actual scaled local model before claiming a complement of a bounded interval or an O(epsilon) shadow. The earlier Corollary 14 applies once such a model and an open passage interval have been established; it cannot supply those premises itself.

## Scope and next move

[done] `other-degenerations-check.py/json/log` gives exact rational diagnostics for the moving-origin proof failure and six-to-four smooth-step collapse. It performs no ray or room search and proves no existence of a dark sequence.

[waiting on Claude] Incorporate moving-vertex endpoint frames, active boundary constraints, the proper-corner range, and the smooth-step/cluster distinction. Then the most useful next proof target is a reduction for clusters of collapsing edges with explicit decorated endpoints; the current list is a useful case map, not a complete global argument.
