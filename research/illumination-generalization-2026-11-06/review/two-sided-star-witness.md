# R35: actual midpoint transits and returns in a two-sided strip star

Candidate positive witness theorem, pending independent review. No supplied path, finite-prefix assumption or large-parameter threshold is needed for the stated classes. The universal W<=21 theorem remains OPEN.

## Geometry and exact classes

A two-sided rectangular-spine comb consists of the rectangle [0,c] x [y_min,y_max], c>0, finitely many right teeth [c,c+w_j] x [l_j,l_j+u_j], and finitely many left teeth [-w_j,0] x [l_j,l_j+u_j]. On each side distinct tooth bands have positive gaps. Bands on opposite sides may overlap arbitrarily. All dimensions are positive real numbers, and the resulting polygon is strictly simple. Actual corners are all forbidden before the actual target. Redundant collinear boundary points are not corners.

The following pairs illuminate:

1. Any two interior tooth-midline points in teeth on OPPOSITE sides, with arbitrary independent widths, heights, abscissae and vertical locations.
2. Two midpoint marks in different teeth on the SAME side, at the same abscissa and in selected teeth of the same height u, provided their average height m lies either on a smooth opposite spine wall or on the midline of one opposite tooth. Selected tooth widths need not be equal; each only has to extend beyond its actual mark.

The second clause explicitly replaces a removed spine mirror by an actual tooth excursion. It does not assume global symmetry of the room. Other teeth and all unused boundary walls may be asymmetric.

## Protected opposite-side matching

If the actual midpoint heights coincide, the horizontal segment between the marks lies in their two teeth and the spine, avoiding all corners. Otherwise exchange endpoints to make the lower midpoint the source. Translate its lower band edge to0. The source band is[0,u], the upper midpoint's band is[H-v,H], with

    H-(u+v)/2 = y_T-y_S >0.

There is NO requirement H>u+v: opposite-side bands may partially overlap or one may contain the other. Write the horizontal mark depths from their mouths as D_s,D_t>0. Put

    A=D_s+D_t+c,
    n_s(tau)=floor(D_s*tau/u+1/2),
    n_t(tau)=floor(D_t*tau/v+1/2),
    Phi(tau)=(H-(u+v)/2+u*n_s(tau)+v*n_t(tau))/A.

Iterate tau_0=0, tau_(i+1)=Phi(tau_i). This map is nondecreasing, Phi(0)>0, and

    Phi(tau) <= (H+(D_s+D_t)*tau)/A.

Thus the increasing iteration remains in[0,H/c]. Both indices take finitely many integer values there. The output set is finite even for irrational data, so the iteration stabilizes. At the FIRST stationary value tau_j>0 its predecessor is strictly smaller. A floor jump at tau_j would increase the next output by at least u/A or v/A relative to Phi(tau_(j-1))=tau_j. Hence no floor jumps at stationarity. The actual residues therefore obey

    r_s=u/2+D_s*tau-u*n_s in(0,u),
    r_t=v/2+D_t*tau-v*n_t in(0,v),
    r_s+r_t+c*tau=H.                         (1)

Use parity n=2k or2k+1 to select the actual +/- midpoint image, as in accepted A32. The source prefix moves horizontally toward its own mouth. Its unfolded starting height is sigma_s*u/2 and terminal height2u*k_s+r_s. Its ordinary horizontal reflections occur at unfolded j*u with j=1,...,2k_s for sigma_s=+1 or j=0,...,2k_s for sigma_s=-1. Every contact is after the source and strictly before its mouth. Its abscissa lies strictly between the actual source and mouth. Its far end is beyond the source, so no far end is encountered. The source reaches its strict mouth with physical upward vertical velocity.

Across the spine use the single straight segment joining its mouth height r_s to the upper tooth's mouth height H-r_t. Equation(1) gives the EXACT same slope and upward velocity. Both portal heights are strictly inside actual tooth bands and hence the spine height range. Every open central point has0<x<c. No vertical spine mirror, global cap, other tooth or mouth endpoint is touched.

The vertically reflected reverse of the upper prefix completes the ray at the original actual target with the same velocity. All target horizontal contacts are strictly between its mouth and its mark. The total reflection count is n_s+n_t. The source and target teeth lie on different sides, so no earlier target can occur in the source prefix or central segment; the final target prefix reaches its actual abscissa for the first time. Arbitrary additional branches on either side cannot remove a used mirror.

This proof also permits the upper target depth D_t to equal its tooth width if the terminal point is the smooth midpoint of its far wall. In that terminal version the path uses no far-wall contact before arrival. Such a boundary endpoint is used ONLY as an intermediate reflecting point in the next construction; it is not a claim about arbitrary boundary endpoint conventions.

## Same-side return with a real opposite tooth

Let the selected marks be S=(c+D,m-d), T=(c+D,m+d), d>0, in right teeth of the same height u, on their midlines. Thus their selected bands and the used horizontal wall segments are reflections of one another in J(x,y)=(x,2m-y). Their far-end widths may differ because each prefix uses only c<x<c+D. Both marks are actual interior points.

If (0,m) is on a smooth actual spine wall, the accepted A32 midpoint matching has identical n_s=n_t and r_s=r_t, since the selected u and D are equal. Its sole left-wall reflection is EXACTLY(0,m). Consequently that path remains legal after arbitrary opposite teeth are restored away from this smooth point. There is no appeal to global room symmetry.

Otherwise assume one actual left tooth is[-w,0] x [m-v/2,m+v/2]. Let

    M=(-w,m).

Apply the protected opposite-side theorem to S and the terminal far-wall midpoint M. The lower selected source midpoint is m-d and upper terminal midpoint is m, so the positive midpoint gap is d. The intervening spine segment and both prefixes are protected regardless of other teeth. This gives a finite legal half-path gamma from actual S to M, with no earlier far-wall hit. At M its incoming horizontal component is strictly negative.

Follow gamma by J applied to its reverse. J maps its selected source-tooth horizontal contacts to the actual target-tooth horizontal walls, whose used portions extend to the same mark abscissa. It maps the opposite tooth to ITSELF because that tooth is centered at m. The two central spine segments remain in0<x<c: their endpoint heights lie in the selected upper band and opposite tooth, hence between the global spine ends. The rest of the room need not be J-invariant.

If v_in=(v_x,v_y) is the incoming velocity at M, the outgoing velocity of J(reverse gamma) is -J(v_in)=(-v_x,v_y), exactly the reflection in the actual vertical far wall. M is a strict wall-interior point. Every other reflected contact is on an actual horizontal wall interior, and all open segments remain inside the corresponding actual teeth or spine. The second half ends at J(S)=T. The full path has twice the half-path's horizontal reflections plus one actual far-wall reflection. It does not pass through or reflect at a removed spine cap.

First actual T arrival is also explicit: gamma stays in the lower selected right tooth, the open spine or the left tooth, and so cannot reach the upper selected right mark. The return has the corresponding reverse ordering and reaches the target only in its terminal selected-tooth prefix. Thus the whole path is an actual S-to-T witness.

Swap left and right for the other same-side orientation.

## A complete canonical pair class under arbitrary joint growth

Suppose all tooth bands have integer height2 and odd integer lower edges, and all axial boundary coordinates are integers. All interior even-even A points lying beyond a spine side are on tooth midlines. Consider any two such A points in different teeth:

- If they lie on opposite sides, clause1 always applies.
- If they lie on the same side, have equal abscissae and their ordinates are congruent modulo4, their average m is an EVEN integer. Every opposite tooth-mouth endpoint is ODD. Thus m cannot be an opposite mouth endpoint. It either lies on a smooth opposite spine wall or lies inside an opposite height2 tooth; in the latter case that tooth's midpoint is exactly m. Clause2 applies.

This class allows arbitrary finite numbers of teeth, arbitrary independent tooth widths, all extra branch positions, spine width, endpoint depths, size and k, as long as the stated alignment hypotheses remain true. There is no initial witness, tail threshold, finite-prefix or joint-growth exception in this class. Its W<=21 members are therefore covered without a k bound. Same-tooth pairs are directly visible.

This does NOT settle same-side unequal-abscissa pairs, different modulo4 midpoint pairs at opposite-mouth endpoints, arbitrary off-midline endpoints, arbitrary two-sided combs, diagonal rooms, or the universal W21 goal. Merely applying A32 to a capped one-sided room would not prove clause2: it could hit a now-open opposite mouth. The actual far-wall return is the new transfer in this packet.
