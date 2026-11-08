# Eventual illumination through a long rectangular neck

Candidate theorem, Codex01a18403. Independent review pending. This handles an unbounded geometric parameter and actual fixed endpoint lifts; it is not the universal W<=21 statement and has no claimed novelty.

## Precise statement

Fix w>0 and two finite strictly simple orthogonal closed polygonal disks C_- and C_+. Suppose C_- is contained in x<=0, C_+ in x>=0, and each has the segment M={0}x[0,w] in its boundary, with every relative-interior point of M smooth. Fix actual interior marks S in C_- and T in C_+. For L>0 form

    P_L = C_- union ([0,L]x[0,w]) union (C_+ + (L,0)).

Require these gluings to have no additional contacts, so P_L is a strictly simple polygonal disk. The former mouth interiors are now open passages. Let T_L=T+(L,0).

There is a finite L0, depending on these fixed chambers, mouths and marks, such that for EVERY REAL L>L0 the actual S and T_L connect in P_L by an ordinary finite specular trajectory avoiding every genuine corner.

Neither chamber needs to be convex or small. All dimensions and endpoints may be arbitrary real numbers. No k, area, lattice diameter or reflection cap is imposed. When a member is canonical45 and W<=21, it is a member of the active goal's class, but only the stated opposing-chamber pair is addressed here. No uniform L0 in terms of W is asserted.

## 1. Imported directional input and fixed-mark exclusions

The directional-minimality input is Zemlyakov--Katok (1975), Proposition3: outside a countable set of angular classes, a nonsingular semi-orbit in a rational-angle billiard is dense in its connected invariant surface. The orthogonal invariant surface contains all four velocity-sign choices with the same positive ratio |v_y/v_x|. This statement is independently cross-checked in Masur--Tabachnikov's author preprint Theorem1.8. Exact primary links and locations are in long-neck-sources.json.

For either fixed interior mark, directions of finite trajectories to ANY genuine corner form a countable set: unfolding a finite wall word gives a vector from a fixed developed mark to one of countably many reflected corner images. Exclude these additional directions, including removable convex corners, and exclude axes. One can therefore choose a single positive magnitude m0 such that the two auxiliary CLOSED chamber billiards, both launched in a direction with component magnitudes (1,m0), have complete forward trajectories dense in their respective invariant surfaces and meet no corner.

Each of these trajectories hits the relative interior of its mouth in finite time. Indeed, a small incoming flow box ending in any strict subinterval of the mouth is an open subset of the invariant surface. Density meets that box and then hits the mouth. Truncate each trajectory at its FIRST mouth hit, BEFORE reflecting in the auxiliary mouth wall. This produces finite legal entry paths from the ACTUAL S and T, with no earlier mouth visit.

Density is used only to obtain these two finite open beams. It is NOT used to infer that a ray hits the actual target point.

## 2. Stable entry beams and virtual source/target points

Because both finite paths avoid corners and all their horizontal/vertical contacts are transverse, their first-mouth itineraries persist for m in a common open interval about m0. Shrink this interval if necessary. The two fixed wall words unfold, in the final physical mouth charts, to fixed virtual points

    S_* = (-a, alpha),  T_* = (b, beta),  with a,b>0.

The inequalities a,b>0 follow from finite positive travel length with final nonzero horizontal component toward the mouth. The unfolded points are constant as the angle varies: they are affine reflections of the fixed actual marks in fixed walls.

Let epsilon_- be the sign of vertical velocity at the LEFT first-mouth hit and epsilon_+ the corresponding sign at the RIGHT first-mouth hit from T. The former horizontal velocity is positive; the latter is negative. Put

    tau=epsilon_- m,  sigma=-epsilon_- epsilon_+ in {+1,-1}.

The reversed RIGHT entry path then has physical slope sigma*tau, whereas the LEFT entry path has slope tau. Choose a bounded open interval I=(u,v) of signed slopes tau, lying wholly on one side of0, on which BOTH complete itineraries remain legal. Its length delta=v-u is positive. Throughout I the mouth coordinates are

    z_-(tau) = alpha + a*tau in (0,w),
    z_+(tau) = beta - b*sigma*tau in (0,w).

The second expression is the ordinate at x=0 of the line from the mouth to T_* with slope sigma*tau. These are strict aperture inequalities, not approximate equalities. All earlier chamber-wall and corner guards hold throughout I by its finite-itinerary construction.

## 3. Exact neck phase, with the actual target retained

For an integer n, place the unfolded right-chamber copy by

    H_(n,sigma)(x,y)=(L+x, 2*n*w+sigma*y).

Its virtual target is (L+b,2*n*w+sigma*beta). The line from S_* to this EXACT virtual image has slope

    tau_n = (c+2*n*w)/(L+C),
    c=sigma*beta-alpha,  C=a+b>0.

Set

    L0=max(0, 2*w/delta-C).

For any L>L0 the interval ((L+C)u-c,(L+C)v-c) has length greater than2w, hence contains an integer multiple2nw strictly inside it. Choose such an n. Then tau_n lies strictly in I and obeys every chamber itinerary and aperture guard. This is exact integer-phase matching; no rational approximation, target movement or endpoint-sheet replacement occurs. The strict inequality in the interval-length test avoids the possible open-interval endpoint tie.

In the physical neck use

    x in [0,L],
    y(x)=F_w(alpha+tau_n*(a+x)),

where F_w(q) is distance from q to 2wZ. At x=0 the developed ordinate is z_- in (0,w), so its physical coordinate and slope agree with the left entry path. At x=L the phase equation gives

    alpha+tau_n*(a+L) = 2*n*w+sigma*z_+(tau_n).

Therefore the physical exit ordinate is EXACTLY z_+, and the derivative of the fold there is sigma. Its physical slope is sigma*tau_n, precisely the slope of the reversed right entry path. The connection consequently ends at the actual T_L through that fixed reversed itinerary.

## 4. Complete physical guards

All chamber portions are the same finite corner-avoiding itineraries represented by I. Neither auxiliary reflection in a mouth cap is performed; the path instead passes through the now-open mouth with matching position and velocity. Both mouth ordinates are strictly between0 and w, excluding all four neck-joint endpoints whether or not some become smooth in the union.

Every neck contact with y=0 or y=w occurs at x strictly between0 and L, where the actual boundary is a smooth horizontal wall. The nonzero signed slope gives ordinary non-grazing specular reflection. Positive finite L,w and finite tau_n give finitely many such contacts. There are no vertical walls in the open neck. The three pieces therefore form one finite actual specular trajectory, with no corner encountered and no change of direction at an interior splice.

Revisits are permitted. No uniform reflection bound is inferred; the number of neck bounces may grow with L.

## 5. Local uniformity: a structural degeneration consequence

The conclusion is locally uniform in the fixed chamber geometries and actual marks, provided the wall patterns, mouths, orthogonal directions, strict simplicity and interior marks persist. To see this, replace I by a smaller bounded interval whose closure lies inside all its strict finite-itinerary guards. Every involved contact and virtual-point coordinate depends continuously on the finite geometric data. Thus the SAME two wall words, signs and smaller slope interval work in a neighborhood of the original data. Keep w at most2*w0 there. Since C remains positive, the common sufficient threshold L>4*w0/delta then works for that whole neighborhood, regardless of c.

Consequently a sequence of dark opposing-chamber pairs cannot have L tending to infinity while its two chamber data, mouth width and marks converge to nondegenerate fixed data satisfying these hypotheses. Some chamber, mouth or marked-point hypothesis must degenerate, or the proposed decomposition must fail. This does not classify all possible degenerations or supply an exhaustive decomposition of W<=21 rooms.

## 6. Exact prescribed controls, not discovery evidence

The read-only long-neck-check.py constructs and validates four fixed controls, covering both sigma signs and two L values. The chambers have a nonconvex extra spur; the finite end words are prescribed one-wall reflections. Each entire saved path is checked against every actual wall, every corner and the rational reflection law, including all neck contacts and actual endpoints. These controls test the phase and splice formulas; the quantified conclusion rests on sections1--5, not sampling.

For the left chamber use [-4,0]x[0,2], [-4,-2]x[2,4] and [-6,-4]x[0,1], with S=(-3,3). The source word reflects at x=-4 before reaching the mouth; S_*=(-5,3). For sigma=-1 the right chamber is [0,4]x[0,2] union [2,4]x[2,4], T=(3,3), T_*=(5,3). For sigma=+1 reflect that right chamber in y=1, so T=(3,-1), T_*=(5,-1). Both use I=(-3/5,-1/3), delta=4/15, w=2, a=b=5, hence L0=5. Fixed lengths L=6 and L=100 satisfy the strict bound. Common factor2 makes these integer-wall controls canonical45 with even-even actual marks.

## Exact remaining gap

There is no proved uniform bound on entry-word length, interval width or L0 as a function of wall count. We do not reduce every large canonical45 disk to two fixed orthogonal chambers and a straight neck. Mixed diagonal-wall chambers may swap the absolute horizontal/vertical velocity components, so the compatible-beam argument does not silently extend to them. Multiple necks with coupled degeneration, moving marks near corners, shrinking apertures, and rooms without such a separator remain open. The universal uncapped W<=21 objective is unresolved. This theorem and its local uniformity require explicit independent peer acceptance before being counted as established progress.
