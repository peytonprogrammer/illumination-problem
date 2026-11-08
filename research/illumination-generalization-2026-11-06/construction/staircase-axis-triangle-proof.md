# Two actual axis reflections in a staircase containing its bounding triangle

Candidate elementary optical lemma, Codex01a18403. Independent review pending. It complements the nested-window sufficient class; it does not prove every four-band staircase or the canonical45 W<=21 target. No novelty assertion.

Let P be the nested staircase of nested-window-proof.md, with outer width A=w_0 and outer height H=y_m, 2<=m<=9. Suppose every intermediate reflex corner satisfies

    w_j/A + y_j/H >= 1,  1<=j<=m-1.             (B_j)

Then every distinct actual interior pair S=(s,u), T=(t,v) connects with at most two ordinary specular reflections, avoiding every polygon corner. Coordinates and dimensions are arbitrary real numbers.

## Geometric premise

The staircase is a down-set in the positive quadrant: if (x,y) is interior and 0<x'<=x, 0<y'<=y, then (x',y') is also interior. Its horizontal sections have nonincreasing widths w_j. Conditions B_j are exactly the assertion that P contains the closed triangle

    Delta = {(x,y): x>=0, y>=0, x/A+y/H<=1}.

Indeed, in band j the greatest triangle width occurs at its lower height y_j and equals A(1-y_j/H), which is at most w_j. The strict interior of Delta is interior to P. Equality at a reflex corner is allowed by the premise, but the path constructed below remains strictly below the oblique side of Delta.

## One straight development and its physical fold

Consider the segment

    (X(q),Y(q))=(1-q)(s,u)-q(t,v),  0<=q<=1,

from S to the image (-t,-v). Fold it to gamma(q)=(|X(q)|,|Y(q)|). Its initial point is the ACTUAL S and its terminal point is the ACTUAL T. The coordinates vanish at qx=s/(s+t), qy=u/(u+v), respectively. Both times lie strictly between0 and1.

If qx=qy, then sv=tu. The two actual points lie on a common ray from the origin and are componentwise ordered. Their direct segment is interior to P by the down-set property. Use that direct connection, rather than the folded segment which would hit the origin.

Assume qx!=qy. The fold makes exactly two distinct axis contacts, at

    (Xc,0), Xc=|sv-tu|/(u+v),
    (0,Yc), Yc=|sv-tu|/(s+t).

Both coordinates are strictly positive. Also Xc<max(s,t)<A and Yc<max(u,v)<H. Thus these are smooth points of the actual outer bottom and left walls; neither is an endpoint or polygon corner. At one contact only X changes sign, and at the other only Y changes sign. Folding therefore gives precisely ordinary reflection in those two walls, with constant speed and no other axis contact.

## Why the entire path stays in the actual room

Before the first axis contact, both physical coordinates decrease from S, so every open point is componentwise below S and lies in the interior of P.

After the second axis contact, both physical coordinates increase toward T. Every open point is componentwise below T and also lies in the interior of P.

Between contacts the physical path is the straight segment joining (Xc,0) to (0,Yc). Since Xc<A and Yc<H, every point of this segment satisfies x/A+y/H<1. Its open points have positive x,y, and so belong to the strict interior of Delta, hence to the interior of P. Its endpoints are the already verified smooth axis contacts.

Consequently there is no visit to any step wall or reflex/convex staircase corner. There are exactly two finite legal reflections in the noncollinear case, and zero for the collinear direct case. This proves the quantified sufficient-class statement including actual marks on internal horizontal seams.

## Complementary metric example and exact remaining scope

Take four bands with widths (13,12,11,10) and heights (0,10,11,12,13). Every B_j holds. Both nested-window G conditions fail: 12*1<11*10 and 11*1<10*11. The room is invariant under transposition, so that alternative also fails. This is a nonempty complementary ten-wall class, not a restatement of the tall-band theorem.

For S=(25/2,19/2), T=(19/2,25/2), the direct segment hits all three reflex corners (12,10),(11,11),(10,12). The actual two-reflection connection is instead

    S -> (3,0) -> (0,3) -> T.

All three open legs and both smooth actual contacts satisfy the preceding proof exactly. Multiplying these coordinates by2 gives a lattice member with even-coordinate interior marks if that canonical normalization is required.

There remain four-band metrics outside BOTH new sufficient mechanisms, even allowing transposition. For example widths (10,3,2,1) and heights (0,3,4,5,10) fail G_1 and G_2, fail the transposed G_2, and fail B_1. Failure of these hypotheses is not darkness; no universal four-band exclusion is claimed. More general nonnested orthogonal and diagonal-wall rooms remain outside these lemmas.
