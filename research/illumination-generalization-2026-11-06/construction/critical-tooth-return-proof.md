# A53: controlled tooth returns close a whole critical two-width family

Author theorem pending independent review. Conservative ORIGINALstart06:47/deadline07:01Z includes preliminary derivation. Main canonical45W21 objective remains OPEN.

For EVERY positive integer a,b, take the room

core[0,1]x[0,16];
selected RIGHT teeth[1,3]x[1,3] and[1,3]x[13,15];
LEFT tooth[-a,0]x[6,8] and LEFT tooth[-b,0]x[10,12].

Then ACTUALS=(2,2) andT=(2,14) illuminate. This is a strictly simple20wall disk for everya,b. There is no upper bound on either width and they vary independently. These are its only actual interior A points: the selected right teeth have sole interior integer x2 and even middle rows2/14; opposite tooth middle rows7/11 are odd regardless of width; the unit core has no strict integer abscissa. Thus this theorem covers every actual A pair in this entire family.

This is the previously critical c1, common-depth1, selected-width2, h6 vertical pattern. The theorem supplies first witnesses for all a,b, not only a residue extension of one old path.

## 1. A source/target prefix shared by both constructions

For either slope tau below,1<tau<3. Initial actual velocity(-1,-tau) fromS hits its actual lower selected horizontal wall at(2-1/tau,1), a strict interior point because1<2-1/tau<2<3. It then reaches the actual source mouth at(1,tau), with upward vertical velocitytau. This prefix uses only the source's depth1 portion, not its unused far end.

The reflected reverse prefix abouty8 takes the actual target mouth(1,16-tau) to its smooth horizontal wall(2-1/tau,15), then to the ORIGINALT=(2,14). It also has exactly one horizontal reflection. Both mouths are strict for1<tau<3. These are interior seam passages, never reflecting walls.

## 2. Actual tooth excursion with an integer winding phase

Let a chosen opposite tooth have widthw and height2, bottom ordinateY. Enter its actual mouth atx0 withphaseA=y_entry-Y in(0,2), velocity(-1,tau). Develop a horizontal distance2w, with one reflection at its actual far vertical wallx=-w. Fold its increasing vertical phaseA+tau*r modulo4 into[0,2], where0<=r<=2w; physical horizontal coordinate is-r forr<=w andr-2w afterwards.

If A+2w*tau=B+4k with B in(0,2), k a nonnegative integer, the exit is the actual point(0,Y+B) with UPWARD vertical componenttau and horizontal component+1. There are exactly2k actual horizontal-wall reflections. The only possible simultaneous far/horizontal collision occurs when A+w*tau is an even integer. The formulas below make that phase noninteger. Strict entry/exit excludes mouth corners, and the noninteger far phase excludes both far corners. All other contacts lie strictly on actual horizontal walls. Thus this is a legal actual excursion, not a fictitious reflection at an open mouth or a periodic fold through a mouth.

## 3. ALL b>=2: use the upper tooth

Choose an integer k so that

5/2 < tau=(8+2k)/(b+3) < 3.                         (U)

Suchk exists for EVERY integerb>=2: this grid has step2/(b+3)<1/2, strictly shorter than the open interval's length1/2. Explicitly k=floor(((5/2)(b+3)-8)/2)+1 is positive and gives both strict inequalities.

After the source prefix, follow the core through

(0,2tau), (1,3tau), upper-tooth entry(0,4tau).

The first contact is strictly below6 and above5, so avoids BOTH left openings regardless ofa. The selected-side contact3tau lies in(15/2,9), a smooth right wall between the selected bands. The entry4tau lies strictly in(10,12).

For the widthb upper tooth, set Y10,A=4tau-10. Its desired exit isy_exit=16-2tau in(10,11), so B=6-2tau in(0,1). Equation(U) gives

A+2b*tau = B+4k,
A+b*tau = 2k+tau-2.

The latter phase is noninteger for5/2<tau<3. Therefore section2 supplies a legal far reflection and2k horizontal reflections, returning at(0,16-2tau) with upward velocity. One core leg then reaches the target mouth(1,16-tau), strictly in(13,27/2). Append the actual target prefix from section1.

All core legs are open in0<x<1; all used side contacts and portals are strict. The other left tooth is never entered. No global floor or roof is touched. The finite complete path reaches actualT and has5+2k ordinary reflections. This proves the whole independently unbounded region b>=2,a>=1.

## 4. b=1 and a in{4,5,6} or a>=8: use the lower tooth

Choosek so that

3/2 < tau=(8+2k)/(a+5) < 5/3.                       (L)

For EVERYa>=8 the grid step2/(a+5)<1/6, strictly shorter than the interval length. Taking k=floor(((3/2)(a+5)-8)/2)+1 works. At a4,5,6 the same formula gives respectivelytau14/9,8/5,18/11, all strictly in(L). Widtha7 does NOT satisfy this choice and is retained as an isolated case; it is not forced through an equality.

Follow the source prefix and core through

(0,2tau), (1,3tau), lower-tooth entry(0,4tau).

The first opposite contact lies in(3,10/3), below the lower tooth. The selected-side contact lies in(9/2,5), between selected bands. The lower entry4tau lies in(6,20/3), strictly inside its mouth.

SetY6,A=4tau-6. Desired exit isy_exit=16-6tau in(6,7), withB=10-6tau in(0,1). Equation(L) gives

A+2a*tau = B+4k,
A+a*tau = 2+2k-tau.

The far phase is noninteger for3/2<tau<5/3, so the actual lower-tooth excursion is legal. Continue from(0,16-6tau) through

(1,16-5tau), (0,16-4tau), (1,16-3tau),
(0,16-2tau), target mouth(1,16-tau).

The remaining opposite contacts have heights strictly in(28/3,10) and(38/3,13), respectively: the first is between the left openings and the second above them. In particular the unit-width upper tooth is never entered. The two intervening selected-side turns are in(23/3,17/2) and(11,23/2), both strictly between3 and13. The target mouth is in(43/3,29/2), strictly inside(13,15). Append the actual target prefix. All segments are in the stated actual core/tooth regions, with no invented end mirror or corner continuation. The complete finite path has9+2k reflections.

Thus b1 is proved forALLa4/5/6 andALLa>=8, without a finite seed.

## 5. Four isolated cases and full exhaustion

Only(a,b)=(1,1),(2,1),(3,1),(7,1) remain. Their complete exact actual paths are stored in critical-tooth-return-seeds.json:

| a | b | Actual initial velocity | Reflections | All-wall leg guards |
|---|---|---|---|---|
|1|1|(-12,7)|31|640|
|2|1|(-5,12)|10|220|
|3|1|(-8,11)|28|580|
|7|1|(-8,5)|17|360|

All four source/target pairs, finite-wall intersections, unique wall interiors and axial reflections were checked with exact Fractions. They total86reflections/1800guards. The first case recovers the already acceptedR36 critical witness and is NOT counted as a new geometric discovery. The other cases are precisely the isolated missing widths; no room census or enlarged candidate pack was run. Independent peer replay is required for final acceptance.

Seven PRESCRIBED formula controls in critical-tooth-return-check.py/json verify the explicit source/target arms, all actual excursion reflections, strict far phases, core contacts and first actualT in both infinite branches, includinga4/5/6 and a larger width. They total149reflections/3680guards. Their validator reuses accepted read-only definitions and is not represented as independent verification. No helper's top-level writer or census is executed. The unbounded proofs are the exact phase-grid inequalities, not these controls.

The upper construction covers everyb>=2; for b1 the lower construction coversa4/5/6 andALLa>=8, and the four stored isolated cases cover the complement. This exhausts EVERY positive integer pair(a,b). There is no remaining large-width or residue gap in this stated two-parameter family. Other minimal-width selected-depth patterns and other vertical arrangements remain open. This does not prove all arbitrary-width combs, arbitrary canonical45 rooms, or the universal22-wall minimum.
