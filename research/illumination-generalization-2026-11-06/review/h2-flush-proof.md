# R48: the entire h=2 floor-flush minimal-depth family

Author proof pending independent review. Original effort start07:14Z/deadline07:28Z includes preliminary end-chart reasoning. Universal canonical45W21 remains OPEN.

## Exact statement

In relative coordinates use core[0,1]x[-3,5]. Selected RIGHT teeth have widthD+1, bands[-3,-1] and[1,3], and actual marks S=(1+D,-2),T=(1+D,2), D in{0,1,2}. The lower selected tooth is FLOOR-FLUSH. LEFT teeth have bands[-3,-1],[0,2],[3,5] and independently arbitrary positive widths f,a,g. The first and last are floor-/roof-flush; the central tooth has positive INTEGER widtha. Then S illuminatesT for EVERY a>=1 and independently every positive REALf,g. ForD0, a can also be any positive real.

Translation by(0,3) gives the original A50D form withG8,S=(1+D,1),T=(1+D,5), selected bands[0,2],[4,6] and opposite bands[0,2],[3,5],[6,8]. Every literal room is a strictly simple disk with18 maximal walls. For integerwidths, an integer translation makingS even-even also makesT even-even; the optical proof retains the actual marks regardless of their names.

## 1. D0: a universal five-reflection path

Use

    (1,-2), (7/5,-3), (2,-3/2), (9/5,-1),
    (1,-3), (0,-1/2), (1,2).

All six legs have absolute slope5/2. The two turns at ordinate-3 are ordinary reflections on the ACTUAL floor of the flush source tooth. The entire floor is one straight wall fromx=-f to2; in particular(1,-3) is a SMOOTH wall point, not a corner at a core/tooth subdivision. The far source point(2,-3/2) lies strictly between its bottom/top edges. The source-tooth top contact(9/5,-1) has strict depth0<4/5<1. The only left core mirror(0,-1/2) lies strictly in the smooth gap(-1,0), between the floor-flush and central left teeth. The last leg crosses the core directly to originalT at(1,2), an actual interior seam.

Each turn changes the appropriate velocity sign and obeys the ordinary reflection law. All tooth-wall contacts are strict, all open segments are interior, and originalT is reached first. The path never hasx<0, so it enters NONE of the three left teeth. Its coordinates and guards are independent ofa,f,g. This proves the complete three-real-widthD0 family. The one focused discovery used a2,f1,g1 and stopped at its first protected verified path after64 primitive directions; the argument above, not a sampled width extrapolation, supplies the unrestricted widths.

## 2. D1/2: explicit protected transfer from R47 section3

Use the R47 d1 LOWER-tooth paths for the SAME D and central widtha. That proof supplies actual paths for every integera>=1: two unbounded winding formulas and exactly three rational exceptions, with original selected widthsD+1. It uses the opposite lower tooth[-a,0]x[-2,0]; its only LEFT CORE mirrors are in(0,1), its RIGHT CORE mirrors in(-1,1), and no core end wall is used. The selected-tooth arms stay within their actual two rectangles. Source/target far folds terminate at actualdepthD, including all horizontal contacts and actual target arrival.

Reflect each explicit path by y->-y and reverse its order. The actualS/T are restored. The lower used tooth becomes exactly[-a,0]x[0,2], the actual central tooth of the present family. Every left core mirror becomes a point in(-1,0), which is a smooth actual gap between the floor-flush band[-3,-1] and central band[0,2]. Right mirrors remain in(-1,1), the actual selected gap. All core legs stay strictly between heights-3 and3, so they remain in the actual core[-3,5]. The newly present upper flush tooth starts at3 and removes no used left mirror or core crossing. The lower flush tooth ends at-1 and similarly removes none.

All selected arms are mapped into their original actual rectangles; selected far walls remain atx=D+2. An arm's horizontal contact at the source floor y=-3 has x>1, a regular point of the full actual flush floor. No core leg reaches that floor or either side/end corner. Every selected and central fold from R47 remains legal, with no created mirror or actual mouth reflection. Thus the full explicit R47 section3 paths are valid in the actual present room for arbitrary independentf,g. This is a direct contact-by-contact guard; no general illumination monotonicity under additions or widening is assumed.

The dependency is R47 section3 ONLY. Its D0 eight-reflection path uses an unsuitable end wall after this reflection and is NOT imported. Section1 above separately proves the neededD0 case.

## 3. Coverage and exact controls

The D0 five proves all reala,f,g. AtD1/2 the R47 all-a formulas/exceptions plus the actual protected transfer prove every integera and arbitrary realf,g. Hence no central-width prefix, flush-width parameter or depth in{0,1,2} remains outside the stated literal family.

h2-flush-physical-check.py reconstructs the displayed five and the exact R47 D1/2 profiles by independently applying the physical coordinate reflection/reversal. It builds the full original18-wall contour, including the LONG unsplit floor through(1,-3), and checks actualS/T, first target arrival, strict simplicity, every finite-wall intersection, unique regular reflection and ordinary specular law. All72 prescribed paths pass with1020 reflections and23112 wall/leg guards. Controls includea1..6,17,100 and unequal flush widths as small as1/3 or2/7 and as large as100009. The all-parameter proof follows from sections1--2, not those samples.

Earlier chart discrimination leftD0a2 outside its one-excursion inventory. It was not darkness; the five-reflection physical path removes that gap and makes every chart tail unnecessary as a proof dependency. The original search deadline was preserved. No workers, new room replacement, git action or external communication was used.

Together with accepted R45/R46 and R47 once accepted, this closes the literal h2 B/C/A1/D minimal-depth patterns. It does not independently establish their necessary classification at arbitrary common depth, all comb placements, taller teeth, other core widths or the universal canonical45 theorem. Those separate structural joins must be audited before broadening the claim. Existing goal/accounting remain unfinished.
