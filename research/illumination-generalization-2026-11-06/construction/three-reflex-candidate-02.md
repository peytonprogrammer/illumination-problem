# TR02: a one-roof candidate for the uncovered spiral cross pair

Predeclared hand candidate. Use the same ordered spiral P and real parameter orders as TR01. First restrict to the genuinely uncovered placements

    S=(s,u), 0<s<a, b<u<h;
    T=(t,v), l<t<A, 0<v<c.

The proposal is that every such pair has a path increasing in actual height to one reflection at the genuine top wall y=H, then decreasing in height to actual T, with all other reflections on genuine vertical walls. This is a hypothesis, not a theorem. Other uncovered placements, including a source in the upper cap or on x=w above h, remain separate.

## Exact simultaneous-window version to prove or refute

Put R=A-w, B=A-l, d0=h-u, g0=2(H-h), g1=h-c, d2=c-v and D=d0+g0+g1+d2=2H-u-v. All are positive, with B>R.

Find signs eS,eT in {+1,-1}, finite integers n,m,k,j and a finite tau>0 such that

    tau D = 2n a+(2m+1)A+2k R+2j B+eT(A-t)-eS s,

and all three inequalities hold strictly:

    |eS s+tau d0-2n a|<a;
    |eS s+tau(d0+g0)-2n a-(2m+1)A|<R;
    |eS s+tau(d0+g0+g1)-2n a-(2m+1)A-2k R|<R.

No upper bound on the integer indices or slope is assumed. Integers describe finite wall periods, not independently chosen local rays. For the native lattice objective the geometry and marks are integral/even-even; an arbitrary-real proof is optional.

## Why this is the relevant physical chart

Unfold the one top-wall reflection into the increasing developed height eta from u to 2H-v. The four traversed bands are left arm [0,a], upper cap [0,A], right arm [w,A], lowest chamber [l,A]. Their successive developed heights are d0,g0,g1,d2.

Use F_L(q)=distance(q,2L Z). The first portal argument is z0=eS s+tau d0-2n a. In the upper cap use F_A(z0+tau(eta-h)). At its far portal subtract the odd period (2m+1)A, giving z1 in (-R,R); the adjoining right-arm fold is A-F_R(z1+tau Delta). The last portal subtracts the even period 2kR, giving z2 in (-R,R); the lowest-chamber fold is A-F_B(z2+tau Delta). At each interface the neighboring formulas agree locally, including signed velocities, because they reduce to the same absolute value. A zero portal argument is a smooth outer-wall contact; the strict endpoint bounds exclude all reflex/ledge corners.

The target equation gives F_B(z2+tau d2)=A-t, hence the ORIGINAL target T after folding height back about H. At the sole roof event, a convex roof-corner contact would require the cap argument at its midpoint to be an integer multiple of A. Triangular-wave symmetry would then make the two cap portal x coordinates equal. The first lies in [0,a), the second in (w,A], impossible since a<w. Thus both strict cap portal guards exclude roof corners without a genericity assumption.

Every open-band vertical mirror in this chart is genuine in P: 0/a below h in the left arm; 0/A in the cap; w/A between c and h in the right arm; l/A below c in the bottom chamber. The chart therefore provides a concrete positive finite optical path whenever the simultaneous system is feasible. This sufficiency reasoning still needs independent checking; the substantive open step is UNIVERSAL FEASIBILITY, not another restatement of the root equation.

## Test criterion and strongest objection

Prove the simultaneous-window system feasible for all stated metrics and actual endpoint placements, or rigorously exhibit a prescribed allowed input where the entire chart fails. Separate failure of this chart from actual darkness. The strongest objection is that the three portal windows and exact target progression can be arithmetically incompatible; satisfying each separately or invoking a complete-fiber replacement does not prove intersection.

No discovery search, deadline, engine or worker has been started. If a focused discovery effort is subsequently justified, declare its exact proof question and one aggregate <=840-second clock before running it, including setup and restarts. Existing related clocks remain unchanged.
