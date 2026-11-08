# R51: a continuous two-tooth witness cell with joint metric growth

Author theorem, pending independent review. The universal canonical45 W<=21 goal remains OPEN. Original conservative discovery start07:29Z/deadline07:43Z includes the pre-compaction reasoning. The initially proposed full [1/2,2]^2 cover failed; the theorem below states only the region actually proved.

## 1. Statement and original endpoints

Take core [0,c]x[0,16v], with c,v>0 real. Attach two RIGHT teeth of width2c in height bands [v,3v] and [13v,15v], and two LEFT teeth of independently positive real widths A,B in bands [6v,8v] and [10v,12v]. This is a strictly simple orthogonal disk with exactly20 maximal walls. Let actual S=(2c,2v), T=(2c,14v). If

    5A-4B<c and 5B-4A<c,                         (1)

then an explicit13-reflection corner-free specular path joins ORIGINAL S to ORIGINAL T. No witness, reflection-tail hypothesis or size bound is assumed.

In particular (1) holds for every A=B<c. It also holds on the whole closed box A/c,B/c in[1/2,7/12]. Positive integer c,v,A,B give actual interior even-even A marks, integer axis walls and the corresponding canonical45 triangle disk. Other interior A marks are unrestricted. Horizontal and vertical scales grow independently without changing the proof.

This is a sufficient continuous metric region of one four-tooth generator family. It is NOT the full arbitrary-core comb theorem, all marked fibers, or the universal strip-program bridge.

## 2. One explicit same-velocity path

Normalize x byc, y byv, put a=A/c,b=B/c and

    tau=9/(7+a+b).

The two strict inequalities (1) give a,b<1 and a+b<2; hence1<tau<9/7. The following are the ACTUAL thirteen reflections, in order, between S=(2,2) and T=(2,14):

| index | reflection point | actual wall |
| --- | --- | --- |
| 1 | (2-1/tau,1) | lower selected tooth floor |
| 2 | (0,2tau) | left core, below lower left mouth |
| 3 | (1,3tau) | right core, between selected mouths |
| 4 | (0,4tau) | left core, below lower left mouth |
| 5 | (1,5tau) | right core, between selected mouths |
| 6 | (-a,(6+a)tau) | lower left tooth far wall |
| 7 | (1,(7+2a)tau) | right core, between selected mouths |
| 8 | (-b,(8+2a+b)tau) | upper left tooth far wall |
| 9 | (1,(9+2a+2b)tau) | right core, between selected mouths |
| 10 | (0,(10+2a+2b)tau) | left core, above upper left mouth |
| 11 | (4-3/tau,15) | upper selected tooth roof |
| 12 | (3,12+tau) | upper selected tooth far wall |
| 13 | (2+1/tau,13) | upper selected tooth floor |

All successive legs have absolute slope tau in the normalized room. At every vertical reflection only the horizontal velocity changes sign; at every horizontal reflection only the vertical velocity changes sign. Thus this is ONE matched-velocity trajectory through BOTH left teeth. No independent one-tooth paths are concatenated.

The four left portals, in order, occur at

    p1=6tau,
    p2=(6+2a)tau,
    p3=(8+2a)tau,
    p4=(8+2a+2b)tau.                            (2)

The lower excursion has p1<p2 in(6,8); the upper excursion has p3<p4 in(10,12). Specifically:

- p1>6 follows from tau>1.
- p2<8 is EXACTLY 5a-4b<1.
- p3>10 is EXACTLY 5b-4a<1.
- p4<12 is EXACTLY a+b<2.

Their two far heights are the arithmetic means of their respective entry and exit heights, so both are strict far-wall interiors. Neither left excursion has a horizontal tooth reflection or a forbidden corner.

The source mouth is(1,tau), strictly in(1,3). Reflection1 lies strictly at1<x<2. The two early left mirrors have heights2tau,4tau in(0,6), and the right mirrors3tau,5tau are strictly in(3,13).

Reflection7 has height p2+tau, between7tau and8+tau, hence in(3,13). Reflection9 is p4+tau. Since p3>10 and b>0, it is>10; directly

    13-(9+2a+2b)tau = 5(2-a-b)/(7+a+b)>0.

Reflection10 is p4+2tau, above12 because

    (10+2a+2b)tau-12 = 6(1+a+b)/(7+a+b)>0,

and below16 because a+b<2. Thus both post-excursion core mirrors are actual and strict.

The upper selected mouth is

    (1,(11+2a+2b)tau)=(1,18-3tau),

strictly in(13,15). The equality uses(14+2a+2b)tau=18 and is the global closure equation; it is not an approximate phase match. Reflection11 has1<x<3 because1<tau<9/7<3. Reflection12 has13<12+tau<15. Reflection13 has1<2+1/tau<3. These are the original finite selected-tooth walls. The last leg reaches ORIGINAL T=(2,14).

Every other open portion of each core leg has0<x<1. Every open portion outside the core lies entirely in its designated tooth rectangle. The strict portals in(2) and the selected portals exclude all concave corners and all unintended walls. Each wall contact in the table is a strict interior point, so no nonspecular corner continuation is used. Earlier target arrival cannot occur: core/left-tooth legs havex<=1; the source arm hasy<=2; on the upper selected arm the only preterminal crossings ofy14 are atx>2, while the terminal leg reachesx2 exactly aty14. The construction therefore arrives first at the actual target.

## 3. Joint growth and canonical applications

Map each normalized point(x,y) to(cx,vy). For horizontal or vertical normals the reflection sign-change matrices commute with diag(c,v). Thus the mapped incoming and outgoing vectors satisfy the ordinary Euclidean reflection law, with actual absolute slope(v/c)tau. Positivity and all wall/portal inequalities are preserved. This is an elementary direct check, not an assumption of general affine optical invariance for diagonal-wall rooms.

Consequently c and v may grow independently and the two opposite widths may vary independently anywhere in(1). There is a uniform finite witness,13 reflections, on this WHOLE continuous fiber region, including every integer/rational member and the displayed compact box. No eventual-propagation theorem or finite room census is needed there. The result supplies a genuine joint-growth cell; it does not show all residual generator fibers enter that cell.

## 4. Independent exact checks and failed broader premise

coupled-two-tooth-check.py records the bounded discovery: a fixed upward two-tooth profile inventory, common tau, strict finite-wall guards and far-corner exclusions. The unreduced endpoint equations rederive

    tau=(6+n_t-n_s+2(k1+k2)) /
        (a+b+(e_s+e_t)/2+m+n+2).

The preliminary summary's numerator2 was incorrect for this h6 room; it was corrected to6 before any computation or claimed result. The theorem's profile is(e_s,e_t,m,n,n_s,n_t,k1,k2)=(1,3,2,1,-1,2,0,0), giving exactly9/(7+a+b).

The proposed whole[1/2,2]^2 cover did NOT follow: only140 of289 prescribed grid points had a candidate in that restricted inventory. The remaining149 are not claimed dark or outside all possible words. No sampled coverage is used in the theorem.

coupled-two-tooth-region-check.py independently checks every affine guard numerator on all four closure vertices(0,0),(1/5,0),(1,1),(0,1/5). Each is nonnegative there and nonzero somewhere, hence positive throughout the open convex region(1). This is an exact finite verification of explicitly given linear inequalities on an all-real domain, not interpolation from sampled paths. It verifies all strict guards throughout the stated closed box as well.

Own actual-wall checker then validates77 prescribed rational paths:1001 reflections/30800 leg-wall guards, plus three anisotropically scaled controls, including large independent integer scales and real rational scales. Original endpoint arrival, no earlier target, all actual walls, corner exclusion and specular law are checked. The table and inequalities above supply the proof for every unchecked parameter.

## 5. Remaining obligation

Independent peer acceptance is pending. Even after acceptance this does not settle widths outside(1), different tooth-band geometries, arbitrary selected depths, other strip generators or arbitrary canonical45 rooms. It does not complete the unfinished universal goal. Frozen prior results and peer construction/ files remain untouched.
