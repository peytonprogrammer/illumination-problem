# L-shaped rooms admit connections with reflections in either wall orientation alone

Elementary theorem accepted by a separate tools-disabled Opus adversarial review; live peer handoff posted. Exact prescribed-formula controls pass. No novelty claim. No rays or direction search.

## The claim

Let P=([0,A]x[0,c]) union ([0,a]x[c,C]), with0<a<A and0<c<C, and let s,t be distinct interior points. There is an ordinary corner-free billiard connection between them reflecting only at vertical walls. There is also one reflecting only at horizontal walls. A direct connection counts as using neither orientation.

Consequently, no set of boundary blockers contained in closed horizontal walls (corners included) can block this pair; likewise for blockers contained in closed vertical walls (corners included). In particular a single smooth boundary point is never essential. This is for arbitrary real dimensions and interior marks, not just commensurable rooms.

## The only nontrivial point placement

The room is also the union of the convex rectangles H=[0,A]x[0,c] and V=[0,a]x[0,C]. If both marks lie in one rectangle, their direct segment is contained in the room interior. Points on the open portal and on {a}x(0,c) are interior points too; whenever one of these is a mark, the two marks share at least one of the convex rectangles and the direct segment applies. Otherwise exchange labels so that

    s=(x_s,y_s),  a<x_s<A, 0<y_s<c,
    t=(x_t,y_t),  0<x_t<a, c<y_t<C.

It suffices to construct a path strictly increasing in y, crossing the open portal(0,a)x{c} exactly once, and reflecting only at vertical walls.

## Target images and the open-portal formula

Write D_s=c-y_s>0, D_t=y_t-c>0, r=D_t/D_s>0. The upper rectangle has horizontal reflection images of the target at

    E={epsilon*x_t+2m*a : epsilon in {+1,-1}, m in Z}.

This set is symmetric under negation. It is the union of two distinct progressions of period2a, since0<x_t<a.

Let h=-r*x_s. Choose x in E such that

    0<|x-h|<=a.

Such x always exists. Consecutive points of E have alternating gaps2x_t and2(a-x_t), both less than2a. If h is not itself in E, a nearest point is at distance strictly less than a. If h is in E, choose its nearer distinct neighbor; its distance is2min(x_t,a-x_t)<=a. Only elementary integer rounding is needed to select this x.

If x>h, put X_s=x_s and X_t=x. If x<h, put X_s=-x_s and X_t=-x. In both cases X_t is an upper-rectangle image of x_t. The straight developed segment from(X_s,y_s) to(X_t,y_t) crosses y=c at

    q=(r*X_s+X_t)/(1+r)=|x-h|/(1+r).

Therefore0<q<=a/(1+r)<a. It crosses strictly inside the open portal.

## Fold the segment into the room

Below y=c:

- If X_s=x_s, the developed x-coordinate runs from x_s to q. It stays in(0,A), so there is no reflection below the portal.
- If X_s=-x_s, it runs from -x_s to q, stays in(-A,A), and crosses x=0 exactly once. Fold its negative-x portion by reflection in x=0. This yields the physical source s and exactly one smooth left-wall bounce, at a height strictly between y_s and c.

Above y=c, fold the x-coordinate into[0,a] by the usual triangular-wave map of period2a. The portal coordinate q is fixed by this folding. The final coordinate is x_t since X_t is in E. Each crossing of an integer multiple of a becomes an ordinary reflection at x=0 or x=a. All such crossings occur at heights strictly between c and y_t<C, so none is a polygon corner. There are finitely many because the developed segment is finite and a>0.

The two folds agree near the portal because0<q<a, so velocity is continuous there. The physical y-coordinate is strictly increasing throughout; no horizontal wall is reached. The source is interior, the sole lower bounce if present is smooth, upper bounces are smooth, and the portal crossing avoids both endpoints. Hence the construction is a valid finite corner-free connection.

## Transpose and remove one smooth boundary blocker

Swap the two coordinates. The transposed polygon is again an L of the same form, with(A',a',c',C')=(C,c,a,A). For the cross-arm pair, the original t becomes the lower/right source and the original s the upper/left target. The preceding construction then gives an original-x-monotone path from t to s, using only horizontal-wall reflections; reverse it if the direction s-to-t is desired.

A smooth boundary point belongs to either a horizontal wall or a vertical wall. If z is on a horizontal wall, the y-monotone connection has no horizontal-wall contacts and avoids z. If z is on a vertical wall, use the x-monotone connection. Directly visible pairs already avoid the entire boundary. Thus z cannot be essential.

## Scope and possible failure points to challenge

This proof uses interior marks; it does not assert the same statement for boundary or corner marks. The portal has positive width, and both arm heights are positive. Forbidding two blockers on different wall orientations is not addressed. The construction does not produce a uniform reflection bound as the aspect ratios and marks vary. It says nothing about general polygons with more than one reflex corner.

Please scrutinize: selection of a nonzero target-image displacement when h itself lies in E; the simultaneous sign change for X_s=-x_s; the lower-strip fold at x=0; target folding after the portal; smoothness and finiteness of all bounces; and the transpose mapping. An exact implementation should evaluate these prescribed formulas and their resulting wall contacts, not search for another path.

## Corollary for isolated smooth-step limits

Assume a sequence of dark rooms has a Jordan six-wall orthogonal limit P0 with distinct interior limiting marks. Suppose the already established decorated-limit persistence hypotheses apply, and the only extra obstruction retained from the collapsed features is one smooth boundary point z. Such a limit is impossible: the theorem constructs a valid connection in P0 avoiding z, contrary to decorated darkness. More generally the same holds if all extra retained smooth boundary blockers lie on walls of one orientation.

This excludes isolated smooth-step approaches to six-wall L limits, including commensurable limits. It uses the existing persistence theorem; it is not a proof about contacts, slits, merged/boundary marks, interior blockers or higher-genus limits. It does not decide mixed-orientation multiple-blocker limits.

## Checks and review

`arithmetic-check.py` evaluates the prescribed formula in both orientations for486 fixed rational interior pairs over6 fixed L shapes. All972 constructed connections pass exact segment containment, wall-intersection, specular-reflection and corner checks, covering7,132 wall contacts. Both source-image sign branches occur;72 evaluations have h exactly a target image, testing the nonzero-displacement choice. Two additional equality-fixture connections and the prior central-core direct bypass pass. These are controls of the formula, not a direction search or a proof by sampled rays. The written argument applies to arbitrary real parameters.

The separate Opus reviewer accepts the proof and recommends only the cosmetic changes now incorporated (`l-monotone-peer-review.txt`). Its aside that a vertical upper segment is possible is unnecessary: for the cross-arm construction the matching lower/upper slope is nonzero. No conclusion depends on that aside.
