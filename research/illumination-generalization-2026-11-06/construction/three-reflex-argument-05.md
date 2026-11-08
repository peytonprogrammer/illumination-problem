# TR05: actual rotated-U path and terminal-pair reduction

Independent review pending. Hypotheses are those of candidate-05.

## 1. The physical subroom

Set Q_B=[0,A]x[h,H] union [w,A]x[0,H] union [l,A]x[0,c].
Its boundary is the eight-wall cycle

    (0,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H).

All these walls are genuine walls of P, except y=h, 0<x<a. On
a<x<w, y=h is a genuine notch wall. The sole additional P corner on
the Q_B boundary is (a,h); the remaining additional corners (a,b),(0,b)
are outside Q_B. The separation disjunction ensures the left column
does not cover the bottom ledge or meet the bottom arm. All Q_B interior
is contained in P interior. Both stated endpoints are strict Q_B interior,
including s=w, which is a portal level rather than a subroom boundary.

Apply the global Euclidean isometry F(x,y)=(H-y,A-x). In canonical U
notation its parameters are

    alpha=H-h, omega=H-c, width=H, base= A-w,
    left_roof=A, right_roof=A-l.

Thus 0<alpha<omega<width and both roofs exceed base. The transformed
source lies strictly within the left arm in x', at height y'_S=A-s>=base;
the target has x'_T=H-v in (omega,width) and height y'_T=A-t>0.

## 2. Opposite arms, including the portal levels

If t<=w, both endpoints have transformed height at least base. Apply the
specific opposite-arm construction of all-heights.md sections 1-4, whose
real-parameter scope is independently accepted in all-real-U-dependency-review.
It uses one base-floor reflection, vertical arm/outer mirrors, and strict
portals. It avoids all U corners. Each source-arm reflection before the
left portal has transformed height STRICTLY LESS than y'_S: horizontal
developed distance is positive and the vertical component points toward
the base. This remains true when s=w (height exactly base); then the
initial path immediately enters the base and uses no forbidden high
source-arm contacts. All source-arm heights are positive.

Transforming back, every source-arm wall contact has original x>s>=a.
In particular every contact on original y=h lies at x>a; it is an actual
wall and is not (a,h). The target arm and base use only the other genuine
walls. The unique base-floor hit is on original x=A away from both outer
corners. Reflections and portal velocities transform with the SAME global
isometry, so there is no change of direction between pieces and the last
point is exactly actual T.

Equality t=w is included in the accepted U arm-level statement. Equality
s=a uses the strict x>s guard, not continuity. Equality s=w is an actual
interior endpoint, with the accepted construction starting at its exact
portal-level state.

## 3. Arm to base

If t>w, the target lies strictly below the transformed U base level. Use
the accepted vertical-only L construction in the left-arm-plus-base
subroom. The source-to-target path is monotone in transformed height
from A-s to A-t (reverse the L path if its construction starts at T).
All used vertical-wall contacts after S therefore have height strictly
less than A-s, unless the entire segment is direct at equal height.
Here t>w>=s gives strict endpoint height inequality, so the latter
case does not arise. Consequently their original x is strictly greater
than s>=a. The artificial source-side wall and added corner are avoided.
The L subroom's artificial horizontal roof at the omitted right arm is
unused by its vertical-only construction, exactly as in the accepted U
arm/base reduction. All horizontal supports used after mapping back are
genuine original walls. If s=w, both endpoints are in the closed base
rectangle and their direct segment, except possibly its source, lies
strictly in its interior. No limit of paths is required.

## 4. First target and finiteness

If an accepted construction encounters actual T earlier than its nominated
end, truncate at the earliest such encounter. It is an interior point, so
that truncation introduces no reflection or corner. There are finitely
many segments; hence a first encounter exists. All retained segments and
reflections are already legal. This is actual target identity, with no
substitution by another endpoint lift. Global F and its inverse preserve
signed velocities, incidence angles, finite mirror intervals and lengths.
Finite U iteration and finite L image choice supply a finite trajectory;
no uniform reflection count is asserted.

## 5. Exact uncovered placements after the join

Accepted TR04 section 2 covers pairs both in G* or both in int(R_L).
Its remaining unordered pairs have T in the lowest chamber and S either
in the left column x<a,y>b, or in the upper cap h<u<H with 0<s<=w.
TR05 covers every source in the latter set with s>=a. The remaining
sources have exactly 0<s<a and b<u<H. Conversely such sources are not
in R_L, while bottom points are not in G*, and TR05 has not claimed
them. Thus the precise remaining pair-placement class is

    S in (0,a)x(b,H), T in (l,A)x(0,c), up to relabelling.

Their closures are separated by a<l OR c<b. This reduction holds at
EVERY metric in the normal form, whether or not either TR04 tall/wide
threshold holds. It closes the upper-cut source s=w at all metrics.
It is not a proof of the remaining terminal pairs or of all (1,1,8) rooms.
