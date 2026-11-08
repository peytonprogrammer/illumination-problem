# Independent review of ST10-B: two partial windows and the actual roof

Decision: ACCEPT the quantified theorem and its transposed counterpart at the EXACT stated metric/endpoint scopes. All four frozen request pins match before and after independent work. No material mathematical correction is required. This is internal AI hand review supplemented by nine prescribed exact physical controls using the existing reviewer geometry/path checker; it is not formal verification or external refereeing. The full all-metric staircase10 and broad r<=8 objectives remain OPEN.

## Accepted statement and exact coverage

For arbitrary REAL strictly decreasing widths w0>w1>w2>w3>0 and positive band heights0=y0<y1<y2<y3<H, define

    E2=min(2w2,w2+w1*(y2-y1)/y1),
    r=E2*y3/(2y2),
    E3=min(2w3,2r,r+w3-w2).

If (H/y3)*E3>=2w3, EVERY distinct actual interior pair with at least one endpoint at physical height>=y3 illuminates by a finite ordinary original-wall path, with vertical-wall reflections and at most one actual roof reflection. All source bands and physically interior source/target seams are included. Native even-even marks in integral rooms are a subset.

The whole-room transpose has widths(H,y3,y2,y1) and heights(0,w3,w2,w1,w0). The same inequality on that geometry covers pairs having an original endpoint x>=w1, including physically interior equality placements. These are conditional metric/placement theorems. Neither inequality nor placement union is proved universal.

## Claim-by-claim hand audit

| Claim | Decision | Independent reason |
| --- | --- | --- |
| Open-interval overlap bound | ACCEPT | For radii R,a and center distance delta<R+a, max lower/min upper gives length min(2R,2a,R+a-delta); nearest2w-center has delta<=w. |
| First source window | ACCEPT | C1=2w0 makes the complete portal interval positive since2w0-s-w1>w0-w1>0. All source horizontal positions are allowed. |
| Second partial overlap | ACCEPT | R2=w1*(1+g1/T1)>w1>w2, so2R2 is irrelevant in the minimum. Nearest-center overlap length>=min(2w2,w2+w1*g1/T1)>=E2. The inverse interval lies in the SAME earlier source window. |
| Third partial overlap | ACCEPT | Its radius is actualell2*T3/(2T2). Because u>0 and y3>y2, T3/T2>y3/y2, so R3>r even if the second bound saturates. Metric B ensures r+w3>w2, making the third strict overlap positive with length>=E3. |
| Exact target at B equality | ACCEPT | D/T3>(H-u)/(y3-u)>H/y3 since v<H,u>0. Thus terminal image length>2w3 even when B is equality. Paired actual-target images have gaps strictly below2w3, so an interior image exists in the SAME launch interval. |
| Sources at y1 and y2 | ACCEPT | Assign the physically interior seam source to the narrower upper band. At y1 begin with the full width-w2 window; at y2 only the one-narrowing positive window remains. No zero denominator or artificial source-side mirror is introduced. |
| One-narrowing source case | ACCEPT independently | A full signed third-portal window has target-height image length>=2w3 for v>=y3; actual paired target images have maximum gap<2w3. One common slope therefore reaches actual T. This proves the used atom directly rather than relying only on a base theorem label. |
| Top-band and equal-height pairs | ACCEPT | Direct segments lie in the convex actual top rectangle or horizontal interior cross-section. Reversibility handles which endpoint is topmost. |
| Signed portal gluing and finite walls | ACCEPT | Subtracting an EVEN preceding-width period makes both adjacent folds locally the same absolute value on the strict narrower residual interval. The same tau is retained. Intermediate folds use actual finite vertical walls only. |
| Smooth wall versus genuine seam corners | ACCEPT | Residual0 is one ordinary common-left-wall bounce; residual equal to the narrower width or the old wider right endpoint is a genuine step corner and excluded. All true vertical-wall endpoints are at the guarded seam/floor/roof heights. |
| Roof corner | ACCEPT | If roof phase B is a multiple of w3, F(B-z)=F(B+z); therefore actual T occurs at its EARLIER ascending height v before the corner. Truncate there, including v=y3. This is an actual legal prefix, not singular continuation or a changed target lift. |
| First-hit and finiteness | ACCEPT | Before final-band entry height increases and never touches an internal horizontal ledge. Afterward it remains in the top band until actual T; only one ordinary roof can occur. Earlier actual T is retained. Finite positive widths, tau and heights give finitely many vertical bounces without a uniform bound. |
| All-metric/all-placement closure | NOT PROVED and NOT CLAIMED | Conditional B and its transpose leave metric/placement gaps. An eight-wall subroom cannot be imported with an artificial roof/right mirror. |

These checks explicitly include very shallow bands, arbitrarily large aspect ratios, rounding ties, real resonant values, source coordinates beyond a later width, and target/source seam equalities. Bounds are exact; no numerical genericity or density argument is used.

## Prescribed physical verification and independence

The first EIGHT cases were recorded in staircase10-top-window-independent-inputs.json before execution. The own selector rounds nearest-center ties upward and chooses the LAST actual target image strictly below the upper final-image endpoint, rather than the author's first above the lower endpoint. No author constructor or checker code was executed. The existing accepted reviewer pure geometry/path_check functions are reused and disclosed; every generated full path is checked against every actual finite wall, true corner and specular contact.

Those eight cases pass328 actual reflections and3520 finite-wall/leg guards in total. They include the old transposed axis-obstruction geometry; source y1/target y3; source y2; both endpoints in top band with one at y3; rational-H exact B equality twice; a band of height1/1000; and a forced roof-corner case.

The forced case uses widths(40,12,8,4),heights(0,12,16,20,48),S=(38,2),T=(2,46),prescribed initialvelocity(-3,+1). Its nominated reflected-target time is48, roof phase-84 is a multiple of4, and the actual ordinary prefix reaches T at time44 before the roof endpoint. That prefix passes22 reflections/250 wall-leg guards with NO singular contact. This tests the literal earlier-target remedy, not a post-corner continuation.

Coverage concern detected after the first eight PASS: the realized portal overlaps happened to be full. One ADDITIONAL fixed case was therefore HAND-derived and PREDECLARED before its prescribed evaluation, with no search or input sweep:

    widths=(40,12,8,4), heights=(0,84,112,140,320),
    S=(8,28), T=(2,140).

All geometry and marks are integral/native. B holds at EQUALITY: E2=12,r=15/2,E3=7/2 and H*E3/y3=8=2w3. Nearest-center selection at the second window is a tie. The actual overlap lengths are ell2=14<16 and ell3=20/3<8. The last-image selector gives tau=327/236, C1=80,C2=128,C3=160 and actual target time472. Its terminal phase span590/21>8 and ordinary roof phase14903/59 are exact. The full original-wall path passes136 reflections/1400 wall-leg guards. This directly exercises BOTH partial overlaps rather than merely their lower bounds.

Total NINE prescribed controls:464 reflections and4920 finite-wall/leg guards. The universal theorem rests on the hand inequalities/physical argument above, not these samples. No new ray engine, numerical discovery, census, fitting, worker, or discovery clock was used. The extra case reuses the same own selector and existing checker without rerunning the original eight.

## Scope calibration and final gap

The transposed frozen axis-obstruction geometry satisfies E2=32,r=24,E3=20 and terminal bound200/3>24, whereas its old transposed second full-window condition fails64<96. Thus the theorem adds genuine uniform conditional coverage beyond demanding full windows at every narrowing. The separate sixteen-reflection control remains valid and is not used to prove the universal quantifiers.

No all-metric staircase10, all-native-placement theorem, allr3/r<=8 theorem or actual dark construction is accepted from this packet. The next required author work is a complete coverage argument for the remaining metrics and placements, or a complete admitted-mechanism failure with all five programmes/signs proved exhausted. All original endpoint/first-hit/corner guards and prior scope restrictions remain. Frozen author files and native accounting/history/budget waiver/clocks are preserved.
