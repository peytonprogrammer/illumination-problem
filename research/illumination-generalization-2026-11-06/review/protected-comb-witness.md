# Protected comb witnesses: complete parameter coverage and a precise interior-mouth obstruction

R30. Candidate for independent review. The universal W<=21 theorem remains OPEN. The statements below concern a specified multi-mouth subclass and its actual endpoints; they do not classify arbitrary generator fibers.

## 1. General protected-U transfer from an accepted eight-wall base

Let P be a comb consisting of the spine [0,c]x[0,H] and finitely many disjoint right-hand rectangular teeth [c,R_j]x[l_j,u_j]. Assume c>0, 0=l_0<u_0<l_1<u_1<...<l_N<u_N=H and R_j>c. Actual marks are

    S=(c+D_s,b_s), T=(c+D_t,H-b_t),
    0<D_s<R_0-c, 0<b_s<u_0,
    0<D_t<R_N-c, 0<b_t<H-l_N.

Then S and T illuminate for EVERY such set of real dimensions, independently of every intermediate tooth's width/height/position. No growth threshold or finite-prefix question remains in this stated class.

Proof: Delete the intermediate teeth only to define the auxiliary U room Q with the same spine and two extreme teeth. Apply the accepted opposite-arm U construction with the coordinate swap (X,Y)=(physical y,physical x), parameters

    a=u_0, b=H-l_N, M=H-a-b, A=H,
    x_s=b_s, y_s=c+D_s, x_t=b-b_t, y_t=c+D_t.

All are in the strict domains required by all-heights.md. Import its SPECIFIED connection, whose only horizontal contact in U coordinates is the smooth bottom hit Y=0; all other reflections are vertical, it avoids the notch Y=c and both roofs, and its middle portion satisfies 0<=Y<c. This is not generic billiard monotonicity under adding material.

In physical coordinates the middle portion lies in the spine x<c and reflects only at the actual walls x=0,y=0,y=H. The arm portions lie in the extreme teeth until entering the spine. The only Q boundary removed by restoring intermediate teeth is contained in x=c,u_0<y<l_N. No selected contact or open segment touches that removed boundary: the middle has strict x<c; the prefixes lie below u_0 or above l_N when x>=c. The first and last mouth crossings are strict at their inner reflex ends by the accepted U proof. A crossing at the OUTER mouth end y=0 or H is allowed only as a smooth actual wall reflection; that outer wall remains genuine in P.

Every new P vertex is on the removed middle boundary x=c. It is likewise avoided, including new corners which were smooth in Q. All retained reflection supports are actual P supports, with identical velocities. Every leg lies in P and reaches the specified actual T. Thus the Q witness transfers unchanged. This works with arbitrarily many intermediate teeth and arbitrary real widths, so includes every W<=20 comb in the stated outer-tooth endpoint class, with no support/k/size restriction. It requires neither a supplied finite-member witness nor independent positive-growth asymptotics.

This is a direct use of an already accepted <=8-wall base for a class of higher-wall generator fibers. It does NOT say that all marked strip-generator patterns have this protected embedding, or that all pairs of a comb are in its extreme teeth.

## 2. Explicit floor witness without an iteration or a prefix

A useful closed formula requires only equal extreme-tooth heights u, equal horizontal mark depths D and possibly UNEQUAL vertical offsets b_s,b_t. Put

    delta=|b_s-b_t|,
    0<b_s,b_t<u, H>2u,
    D >= c*(u+delta)/(u-delta).

The tooth ends must extend strictly beyond c+D. Set

    Z=c*min(b_s,b_t)+D*(H-delta)/2,
    k=floor(Z/(2uc)),
    tau=(H-b_s-b_t+4uk)/(2(c+D)),
    r_s=b_s+D*tau-2uk, r_t=b_t+D*tau-2uk.

Here k>=0 and tau>0. Direct algebra gives

    min(r_s,r_t)=(Z-2uc*k)/(c+D),
    0<=min(r_s,r_t)<2uc/(c+D)<=u-delta,
    max(r_s,r_t)=min(r_s,r_t)+delta<u,
    r_s+r_t+2c*tau=H.

Starting from S, travel left with vertical speed tau. Unfolding the bottom tooth, its height increases from b_s to 2uk+r_s. The contacts j=1,...,2k are exactly

    (c+D-(ju-b_s)/tau, u if j odd, 0 if j even).

Each is at x>=c, and x>c except possibly the last one when r_s=0. All contacts are left of S and of the far tooth end. After 2k ordinary horizontal-wall reflections the velocity points left/up at the portal (c,r_s). If k=0 there are no tooth reflections; r_s=b_s+D*tau>0. Thus a zero portal cannot create a zero-length first leg.

In the spine connect (c,r_s) to

    M=(0,r_s+c*tau)

and then to (c,H-r_t), reflecting once on x=0. The matching identity gives both slopes tau. Its midpoint has strict 0<r_s+c*tau<H because c*tau>0 and H-(r_s+c*tau)=r_t+c*tau>0. Hence M is not a corner. All open central legs have x<c, so avoid every intermediate mouth/corner. For the final tooth portion, reverse the analogous bottom path with source offset b_t, then reflect y to H-y. It starts with the matching right/up velocity and reaches the actual T.

There are exactly 4k+1 reflections. If r_s=0 the lower portal is (c,0), strictly inside the ACTUAL maximal floor from x0 to R_0, and is an ordinary smooth reflection. If r_t=0 the same is true at (c,H). These are not genuine polygon vertices; an auxiliary mouth subdivision cannot make them forbidden corners. Values r_s=u or r_t=u, which would hit the true reflex ends, are excluded by the strict bound. No artificial cap is used. Earlier target arrival is impossible: lower legs stay below u, central x<c while T has x=c+D, and the final upper portion increases x to T for the first time.

Symmetric offsets b_s=b_t=b reduce the width condition to D>=c. In particular the complete independent-growth lattice family

    spine [0,4]x[0,36+2m], tooth right ends20+2n,
    tooth bands [0,4],[8,12],[16+2m,20+2m],
                 [24+2m,28+2m],[32+2m,36+2m],
    S=(8+2n,2), T=(8+2n,34+2m), n,m>=0 integers

has a strict20-wall canonical45 boundary and actual distinct interior A marks for all n,m. The formula covers its entire integer quadrant. For n=0,m=4, k=3,tau=11/2 and both portals have zero offset; all13 reflections remain smooth actual-wall contacts. This two-parameter example calibrates the proof and is not a universal progress claim.

## 3. Exact obstruction to extending this formula to arbitrary marked teeth

The outer-mouth premise cannot simply be deleted from the preceding proof. Consider the ACTUAL16-wall comb with spine [0,4]x[0,64], tooth right ends20, bands

    [0,4], [10,14], [50,54], [60,64],
    S=(8,12), T=(8,52).

Apply the same floor formula to the selected inner pair after subtracting y10: H=44,u=c=D=4,b_s=b_t=2 gives k3,tau11/2,r_s=r_t=0. It prescribes contacts (4,10) and (4,54). BOTH are genuine reflex vertices in the actual room, so this candidate fails. The marks are actual interior A points and the room is strictly simple. This is an exact counterexample to that proposed formula extension, not a dark pair or a failure of illumination.

The accepted general U witness also cannot be transferred from a subroom truncated at these levels without further checks: its spine reflections on the artificial horizontal cuts y10 or y54 need not be actual mirrors. Thus the arbitrary marked-fiber bridge remains a substantive boundary/phase obligation, not a consequence of U illumination or topology alone.

## 4. Reproducible prescribed checks and limits

protected-comb-witness-check.py constructs every actual polygon and formula contact independently of peer code, then uses reviewer all-wall predicates. Eight prescribed controls pass206 reflections and3912 complete wall/leg guards. Four test the independent n,m lattice family, one tests unequal offsets at the sufficient-width equality with a zero smooth portal, and three test the stronger asymmetric protected-U transfer with short/unequal depths and rational dimensions. No direction/word discovery was used. The general quantifiers follow from the hand proofs, not these controls.

The original840-second R30 deadline covers setup, authoring and controls. Source hashes and the exact accepted U dependency are pinned in the review request. Independent peer acceptance remains required. Main W<=21 illumination, arbitrary selected inner teeth, diagonal generators and changing chamber shapes remain OPEN.
