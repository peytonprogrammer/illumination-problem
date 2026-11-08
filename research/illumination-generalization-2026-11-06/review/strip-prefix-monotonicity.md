# Even strip insertion does not preserve illumination without a wall hypothesis

R25 exact discriminator for the finite-prefix program. Pending independent review. This is not a W<=21 counterexample or a claimed obstruction within that exact class.

Let Q0 be the accepted22-wall dark polygon in fold-area-invariant.md section3, with actual S0=(0,0),T0=(2,2). All its distinct x levels are -1,0,1,2,3,4,5. Define the continuous increasing piecewise-linear x map F with F(x)=x for x<=0, F(x)=3x for0<=x<=1, and F(x)=x+2 for x>=1. Apply (F(x),y) to the polygon and actual marks. This inserts width2 into JUST the gap (0,1). Call the resulting22-wall room P. Its actual marks are S=(0,0),T=(4,2), both interior even-even A points. Product monotone coordinate changes preserve strict simplicity and all genuine orthogonal turns; both polygons are canonical triangle disks.

P illuminates that actual pair by the STRAIGHT segment y=x/2,0<=x<=4. Hand check: for0<=x<2 it lies in the widened central rectangle (-1,3)x(-1,1); for2<x<=4 it lies in the upper band (0,6)x(1,2) and its endpoint's upper continuation band (3,5)x(2,3). At (2,1) it crosses the interior overlap, not a wall: both bands overlap across y=1 on0<x<3. The source and target are strictly interior. Thus no boundary or corner is touched. The exact independent wall-leg guard checker also validates this segment against all22walls.

Now insert width2 into EACH of the OTHER five x gaps, anchoring the source x=0. Every final x gap has width3, so the final room is EXACTLY Q3=diag(3,1)Q0, with actual marks (0,0),(6,2). It is dark: diag(3,1) commutes with every axial reflection and its inverse preserves all corners, actual endpoint visits and finite legal paths. An actual path in Q3 would give one in Q0. This uses the accepted physical darkness proof, not a finite failed search or selected dark lift.

Therefore arbitrary nonnegative even coordinate-gap insertions can change an actual illuminated pair into a dark pair, at the SAME22 maximal walls. In particular a W-independent theorem saying that EVERY single even-gap insertion preserves illumination is false: applying it successively to those five insertions would contradict the dark final room. This argument does not identify which intermediate insertion first loses illumination, and makes no verdict about those intermediate rooms.

## Consequence for the positive program

The unconditional induction step from an illuminating compressed room to every larger coordinate-gap member must be retired. It fails for actual existence, even with original ranks, wall count, strict simplicity, A parity and physical endpoint identities all retained. Merely proving continuity of one reflection word or checking the compressed base cannot repair the quantifier. The W<=21 restriction could still make a more specialized transfer true, but that requires a proof using that restriction; this control does not refute it.

The accepted one-witness eventual theorem remains valid: the dark Q3 may lie in a finite prefix on a particular one-parameter ray, and the five-coordinate construction changes more than one parameter. No contradiction with eventuality or rational affine propagation is inferred.

## Reproducibility and discovery scope

strip-prefix-monotonicity-check.py performs the one recorded precursor search only: fixed P/S/T, primitive directions through maxnorm24 and at most500contacts per direction, original aggregate deadline enforced including setup and process time. It stopped at its first witness, direction(2,1), after16directions:0reflections,22wall-leg guards. The actual segment was then reconstructed above independently by hand. No replacement room/pair or subsequent direction scan was used. Its exact positive certificate is in strip-prefix-monotonicity-check.json.

Dependencies: fold-area-invariant.md and its independent acceptance for the displayed Q0 and exact axial transport of darkness; strip-generators.md for coordinate-gap parity/rank conventions; resumed-exact-check.py for the separate geometric/path guard checker. The control disqualifies the W-independent shortcut only. The uncapped W21 theorem and its finite-prefix/joint-growth bridge remain OPEN.
