# Independent geometric-reduction prerequisites

Reviewer Codex01a1a00f. Native goal active; the complete orthogonal r<=8 target remains open. These are hand-proved necessary conditions and exact controls for the new programme, not an illumination theorem or a review of an author packet that has not yet arrived.

## Prior-work reconciliation

Read the programme and proof-goal in full, B01 author assessment and independent review, both global impasse reports, the specified local-surgery analysis and independent acceptance, and the earlier strip-prefix monotonicity countercontrol. B06 and label-descent results retain their accepted limited scope.

Three different failures must not be conflated:

1. B01's roof-notch control destroys a selected reflected word while the actual pair remains directly visible. This rejects automatic chosen-word lifting, not existential transfer.
2. The fixed known22 single-vertex surgery family has positive paths in every qualifying deletion shape. It provides no universal surgery implication.
3. The prior even-gap insertion chain changes a lit actual pair to a certified dark one at W22. It rejects W-independent existential gap-insertion monotonicity. Its wall count is outside this programme's r<=8 class, so it does not reject an r<=8-specific argument.

The new endpoint-bearing-ear finding below concerns availability of a strict complexity decrease. It is independent of whether optical transfer would hold if a reduction existed.

## P1. A contained r-decreasing reduction need not exist, even at r=1

Let D be the strictly simple orthogonal lattice L-room with counterclockwise boundary

    (0,0),(8,0),(8,4),(4,4),(4,8),(0,8),

and keep actual S=(6,2), T=(2,6). Equivalently its closed region is

    [0,8]x[0,4] union [0,4]x[0,8].

All vertices and actual marks are even-even. The orthogonal tiling-edge boundary bounds a canonical triangle disk; both marks have full interior A stars. D has six maximal walls and exactly one reflex vertex, at (4,4).

**Claim.** There is no strictly simple orthogonal subroom D' contained in D, containing S and T strictly in its interior, with r(D')<r(D).

**Proof.** Reflex counts are nonnegative integers, so r(D')=0. For any strictly simple orthogonal polygon, the turning equation is c-r=4. Thus an r=0 polygon has precisely four maximal straight walls and is an axis-aligned rectangle. A rectangle containing S and T contains their coordinate box [2,6]x[2,6], in particular (5,5). But (5,5) is outside D. Contradiction. This argument excludes every contained r-decreasing orthogonal subroom, not merely one chosen ear cut. No grid assumption on D' is needed, so it certainly excludes qualifying lattice subrooms.

For the two usual rectangular ear cuts, the vertical cut from (4,4) to (4,0) removes the arm containing S, and the horizontal cut to (0,4) removes the arm containing T. Keeping one instead leaves only that endpoint's rectangle. The whole-subroom argument above avoids dependence on which cuts are called ears.

**Scope.** A universal induction with only convex base cases cannot always use endpoint-preserving deletion and strict decrease of r. It must allow an actual direct solution in this case, a broader base family, enlargement, a non-nested deformation, multiple marked subproblems with an optical gluing theorem, or another well-founded measure. This does not rule out any of those repairs. If r=1 is already an accepted base, this example is absorbed by that base; it is not a claim against such an induction's remaining availability.

### The actual pair is illuminated

The legal path is

    (6,2) -> (5,0) -> (2,6).

The first leg lies in the lower rectangle. On the second leg, crossing x=4 occurs at y=2; crossing y=4 occurs at x=3. Therefore both open legs lie strictly inside D, except for the one specified floor contact. The contact (5,0) is smooth. Incoming velocity (-1,-2) reflects from y=0 to (-1,2); the final displacement (-3,6) is a positive multiple. The actual target is reached after one reflection and is not met earlier.

Filling D to the bounding rectangle reduces r from1 to0 and retains actual S,T. The direct rectangle witness passes through the old reflex corner (4,4) and is illegal in D, while the displayed one-bounce path is legal in D. This makes the quantifier distinction explicit: one selected ray breaks, but for this pair existential transfer holds. Nothing here establishes existential transfer for arbitrary fills.

## P2. Exact compatibility needed to replace one artificial mirror by a rectangular-ear excursion

This is a local control on a proposed lifting map, not a general transfer obstruction. Let an ear be the rectangle0<x<w,0<y<d, attached to a core below its open mouth0<x<w,y=0, with genuine vertical sides and roof y=d. A reduced room closes that mouth by an artificial horizontal mirror. Suppose its transverse ray hits the artificial mirror at (x,0), with0<x<w, incoming velocity (u,v), v>0. Its reduced reflected velocity is (u,-v).

Put m=u/v. In the actual ear the vertical coordinate first rises to d, reflects once at the roof, and falls to0, with any number of side reflections. Unfolding the side reflections gives mouth exit coordinate

    x_exit = fold_w(x+2dm),

and exit velocity (epsilon*u,-v), where epsilon is the slope of fold_w on the containing interval. For a corner-free excursion to return to the SAME mouth point with the SAME reflected velocity as the reduced bounce, it is necessary and sufficient that

    dm is an integer multiple of w.

For u!=0, a matching velocity requires epsilon=+1. On these positive-slope fold branches, fold_w(q)=q-2kw, so equality with x requires2dm=2kw. Conversely dm=kw makes the exit x, with positive fold derivative. The roof location folds x+kw to x or w-x, strictly inside(0,w), and neither roof nor mouth is a corner. All intermediate side contacts have0<y<d. Thus the excursion is legal and has the desired exit data. The vertical case u=0 also satisfies the condition, with no side contacts.

For example w=d=4, x=1, m=1/2 gives unfolded exit5, hence actual exit3 with reversed horizontal velocity. The roof contact is (3,4), and the side contact is (4,2), both smooth. The excursion is legal but does not replace the reduced bounce at (1,0). A missing commensurability condition therefore breaks this PARTICULAR bounce-replacement construction even without a corner accident.

This does not disprove existential ear removal: a proof could choose another reduced ray, use a different ear itinerary, or reroute globally. The missing requirement for this construction is an existence theorem providing a reduced ray with all required mouth compatibilities simultaneously, or a different transfer mechanism that avoids point-and-velocity matching.

## Current frontier

No author candidate is accepted yet. P1 identifies an exact availability obstruction for the pure contained/r-decreasing/convex-base scheme. P2 identifies the exact local arithmetic condition for an unshifted rectangular-ear bounce replacement. Neither is a dark room or a global impossibility result. Next independent work: audit endpoint-on-mouth cases and global ear availability without assuming endpoints lie off a chosen rectangulation; then review the author's quantified transformation and transfer claim from its pinned raw data.
