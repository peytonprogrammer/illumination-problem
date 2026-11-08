# Independent OR01 quantitative access constraints

HAND necessary-condition findings, Codex01a1a00f, 2026-11-07. These follow from the accepted conditional OR01 statement. They do not prove or refute G8. No search or parameter fitting.

## W1. A necessary effective-depth balance

Use OR01 notation, ell=length(J)>0 and K=a+b+2h. Since x_S=alpha+a*m lies in(0,w) for EVERY m in the open interval J, its full variation a*ell is at most w. Likewise b*ell<=w. Non-strict inequalities are essential: an open interval can approach both mouth endpoints without attaining them.

Therefore

    ell <= w/max(a,b),
    K*ell <= w*K/max(a,b).

The sufficient width condition K*ell>2w can hold only if

    K>2*max(a,b), equivalently 2h>|a-b|.       (W1)

Thus a and b cannot be made independently large without controlling their difference and the joint guard width. If |a-b|>=2h, NO open J satisfying just the two mouth-access inequalities can satisfy OR01(C), regardless of other walls or branch legality. This rejects that attempted OR01 chart, not another chart, G8 or actual illumination. Even (W1) is insufficient: the two access intervals may barely overlap or actual occlusions may split/shrink them.

## W2. Exact access-only overlap bound

The mouth-only intervals are

    I_S=(-alpha/a, (w-alpha)/a),
    I_T=((beta-w)/b, beta/b)       when epsilon=+1,
    I_T=(-beta/b, (w-beta)/b)      when epsilon=-1.

Let L0 be the maximum of their lower endpoints, U0 the minimum of their upper endpoints. Every guarded J must lie inside (L0,U0), so ell<=max(0,U0-L0). Consequently a necessary condition for OR01(C) is

    K*max(0,U0-L0)>2w.                         (W2)

Equality does NOT satisfy the strict OR01 criterion, although illumination or an isolated matching root may still exist. If (W2) holds and no further guards are present, the whole overlap or a sufficiently large relatively compact subinterval satisfies(C). With actual other walls, this is only an upper bound. A positive root proof must use the width of ONE connected legal component, not total width across disconnected components.

## W3. Sliding the mouth does not increase K for fixed developments

Place the actual chamber in global coordinates [x0,x0+w]x[c,H], roof height H, mouth height c, h=H-c. On fixed source and target reflection branches, develop both actual endpoints into the terminal physical mouth frame. Denote their global developed positions by (X_S,Y_S) and (X_T,Y_T). They are fixed by the reflection words, independently of a small vertical slide of the mouth inside the same terminal free corridor. Then

    alpha=X_S-x0, a=c-Y_S,
    beta=X_T-x0, b=c-Y_T,
    K=a+b+2h=2H-Y_S-Y_T.                      (W3)

The c terms cancel exactly. Lowering the mouth deepens h but simultaneously shortens the developed access depths a and b. It cannot increase the multiplier K for those fixed developments. It may change the access interval and first-hit guards, and it may invalidate endpoint exclusion or the branch altogether. Those effects need their own proof. Changing the actual roof, changing a wall itinerary, or crossing a terminal wall is not the fixed-development operation covered by(W3).

This is an additional obstruction to trying to force(C) merely by declaring a deeper artificial section in the same physical chamber. The only possible improvement under a valid section slide is in the actual COMMON guard interval width, not K. Its invariance does not imply every such interval is unchanged.

## W4. Lattice parity and exact-target rationality

For an axis-aligned integer room, a reflection word sends coordinates to (+/-x+2k_x,+/-y+2k_y), with integer k_x,k_y. Since S,T are actual even-even points, Y_S,Y_T are even integers. Hence

    a-b=Y_T-Y_S is in2Z,
    K=2H-Y_S-Y_T is a positive even integer,

when the chamber roof is an actual horizontal wall at integer H. The mouth c may be noninteger; its parity individually is irrelevant, and(W3) still holds. Since the chamber sides are actual walls, x0,w are integers; alpha and beta are integers of the same parity. The numerator2nw+epsilon*beta-alpha in OR01 is even for either epsilon. Every candidate root is rational, as required for a finite actual-target path in a lattice room.

If h<=1, W1 forces a=b because a-b is even. This is an arithmetic constraint on this proposed chamber/branch pair, not a global bound on chamber depth or a proof that no good pair exists. For h>1 it restricts the allowable even differences to the strict interval(-2h,2h). No diameter/word cap follows.

For a pure rotated orthogonal lattice convention these statements require applying the already accepted whole-room similarity/parity normalization; they are stated here in the axial integer frame. Mixed axial/diagonal canonical45 remains outside this programme.

## Prescribed exact fixtures

1. w8,h1,a2,b4 gives K8 and ell<=2, so K*ell<=16=2w: condition(C) impossible on any mouth-valid interval, including equality in W1. This does not claim the fixture is a complete actual room.
2. The accepted smooth rectangle fixture has global roof H16, developed source/target heights both-4. Sliding c0 to c2 changes(a,b,h)=(4,4,16) to(6,6,14), and K remains40.
3. The physical r2 sole-root-corner fixture has H8, Y_S=-8,Y_T=-16, c0. Its(a,b,h)=(8,16,8) satisfy2h16>|a-b|8; K40 and its legal interval width9/10 meet(C). The necessary test correctly allows it, while the separate actual-corner argument remains needed.

These are prescribed rational controls, not an existence survey. The hand derivations prove W1–W4 generally. The missing global low-reflex implication is unchanged: force some compatible physical branch pair to pass the actual connected-domain width test, or give another legal original-room witness.
