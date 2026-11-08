# Independent TR03 review: ACCEPT at the stated tall-spiral scope

Reviewed the complete pinned candidate, argument, checker source and checker evidence. All nine source pins match before and after the independent replay. The request hash is `6f5df96a327a3dc38b3d387848ac2720dafbd9f6ba528cb86af4697380e267af`.

The accepted assertion is every distinct actual interior pair in the ordered real spiral

`0<a<l<w<A`, `0<b<c<h<H`, with boundary
`(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)`,

provided `H >= c+2A/delta`, where `R=A-w`, `L=R/(2c)`, `Ns=ceil(Lh/(2a))+1`, `Nr=ceil(Lh/(2R))+1`, and `delta=L/(Ns+Nr+1)`.

This is an all-endpoint, arbitrary-real optical theorem for that metric subclass. Shorter roofs, other metric orders, the full (1,1,8) type, all r3 and the native r<=8 goal remain open. Failure of this sufficient inequality says nothing about darkness.

## Claim decisions and independent reasoning

1. **ACCEPT — uniform bottom interval and finite partition.** For `z=A-t>0`, `d=c-v` in `(0,c)`, the positive window `|z-tau*d|<R` has length `2R/d` when `z>=R`, and `(z+R)/d` otherwise. Both exceed `R/c=2L`. Consequently the closed interval from `q+L/2` to `q+3L/2`, `q=max(0,(z-R)/d)`, lies strictly inside that window. The source odd-boundary spacing is `2a/(h-u)>2a/h`; the right odd-boundary spacing is `2R/(h-v)>2R/h`. The proposed counts overestimate both, including any phase equality at the ends. Removing distinct interior points gives at most `Ns+Nr+1` gaps, of total length L. A gap has length at least delta. There is no dependence of delta on H or the marks. The gap's position and the integer labels can depend on the marks; no uniform location is needed.

2. **ACCEPT — simultaneous exact root.** Fix the nearest-even source/right labels on one such open gap. Then `tau D=C+2mA`, `D=2H-u-v`, is one exact target equation, not an independently selected approximation. Since `D-(H-c)=H-u+c-v>0`, equality in the stated roof bound still gives `2A/D<delta`. Any open interval longer than this spacing contains a progression point strictly inside. The author's first-root floor choice is valid. My replay selects the last maximal gap and the last progression point strictly below its upper end instead; it passes the same guards. All labels are finite for a fixed real input, even when some distances are arbitrarily small.

3. **ACCEPT — signed fold gluing and physical walls.** Independently, `F_q(x)=abs(x-2q floor((x+q)/(2q)))`. Near the first seam, both formulas are `abs(z0+tau*epsilon)`. Near the second seam use `F_A((2m+1)A+x)=A-abs(x)` for `|x|<A`; both adjacent formulas are `A-abs(z1+tau*epsilon)`. Near the third seam remove the even `2kR` period to obtain `A-abs(z2+tau*epsilon)`. These identities hold on a neighborhood because the inequalities are strict. Thus they preserve the signed horizontal velocity, including a zero residual that gives one smooth outer-wall reflection. Vertical velocity agrees across each seam; only the roof reverses it. Open bands use x=0,a in the left arm, x=0,A in the cap, x=w,A in the right arm, and x=l,A in the bottom chamber, each within its actual wall interval. No artificial cut is a mirror. Strict seam bounds avoid all reflex vertices and ledge endpoints. Finite widths, slope and flight length imply finitely many contacts without a uniform reflection cap.

4. **ACCEPT — roof corner exclusion or actual-source suffix.** For the left-arm source, a cap phase equal to an integer multiple of A at H makes its two equidistant cap-seam positions equal by even fold symmetry. Their required disjoint ranges `[0,a)` and `(w,A]` contradict that. For an upper-cap source, if the roof is singular, set `eta*=2H-u`. Its phase is `2q-s` with `q` an integer multiple of A, so its coordinate is exactly s and its actual height is exactly u. With u>h, `H<eta*<2H-h`; hence the suffix starts at the same actual interior S, inside the cap, after the bad event. Its phase is congruent to -s modulo 2A, so it starts with velocity `(-tau,-1)` and has no cusp at its start. Subsequent vertical-wall and seam guards already apply, and it cannot revisit the roof. With u=h, the same return would be at the right seam at x=s<=w, contradicting its strict x>w guard. No singular continuation is counted as part of the legal suffix.

5. **ACCEPT — target identity, first arrival, and exhaustive endpoint join.** The final bottom argument is exactly `z=A-t` in `(0,B)`, so x=t and y=v, in the original room. For a lower-arm source, the ascending portion below h has x<a<t; ascending cap positions have y>=h>v. The descending portion has y>v until its end. For an upper-cap source, the ascending portion has y>=u>=h>v; its descending portion or retained suffix has y>v until the end. Thus actual T is first reached at the final point. TR01's independently accepted join leaves exactly a lowest-chamber mark and a left/lower or upper/cut mark with x<=w. The two new cases exhaust these placements, including u=h in the actual left mouth and x=w,u>h. Reversal is legal. No extension to an actual-boundary mark is required or used.

## Independent reproducible evidence

Run `python3 -B .context/illumination-generalization-2026-11-06/review/three-reflex-tr03-independent-check.py`.

The new code independently pulls back arithmetic phase boundaries, chooses a different gap/root convention, constructs affine fold bands, and lists every event. It imports only pure predicates from an earlier reviewer-owned file through AST extraction; no author code executes. Ten prescribed inputs yield **2042 actual reflections and 20750 finite wall/leg guards**, all exact rational checks passing. The checks include original polygon simplicity, interior marks, every wall against every leg, no true corners, actual signed velocity at every contact/seam, no earlier T, roof-bound equality, near-boundary rational marks, a prescribed singular-roof suffix, and the previous short-roof fixed witness as a conditional formula control. The short-roof control is not evidence for the tall-threshold quantifiers. The real quantifiers follow from the hand argument above, not from the finite checks.

No corrections are required. This review starts no discovery effort and renews no old clock. The TR02 fixed-input search remains closed. Full goal status remains active and incomplete.
