# R47: every h=2 A1 minimal-common-depth room

Author proof pending independent review. Original effort start07:04Z/deadline07:18Z includes preliminary transfer algebra. Universal canonical45W21 remains OPEN.

## Exact statement

Let D in{0,1,2} and integer d>=1. The core is[0,1]x[-4,d+4]. Selected RIGHT teeth are[1,D+2]x[-3,-1] and[1,D+2]x[1,3], with actualS=(1+D,-2),T=(1+D,2). The opposite LEFT teeth have independently arbitrary widths a,b>0 in bands[-2,0] and[d,d+2]. Then S illuminatesT for EVERY positive INTEGERa and every positive REALb. The D0 proof also allows every reala>0. All rooms are strictly simple with20 maximal walls. Integera,b and a translation puttingS even-even give the canonical45 actualA-pair corollary. No bound on depth, size, k or other interiorA count is introduced. This is the literal A1h2 family, not a necessary classification claim for arbitrary rooms.

## 1. All d>=2 by the strict protected R46 paths

In frozen R46 subtractmu from its heights. Its path connects(1+D,-2) to(1+D,2); every LEFT CORE mirror has y in(-2,0), every RIGHT CORE mirror has y in(-1,1), and the only LEFT tooth entered is[-w,0]x[0,2]. All core legs stay in-3<y<3 and actual selected-tooth arms stay in their two original rectangles. The flush widths never enter these conditions.

Use w=a, reflect that explicit path by y->-y, and reverse its order. The original endpoint pair is restored. Its left central tooth is now[-a,0]x[-2,0], exactly the actual lower opposite tooth. Its left CORE mirrors lie in(0,2). Since the unused upper opposite band starts atd>=2, ALL those mirrors remain actual and strict, includingd2. Right core mirrors remain in(-1,1). Core legs stay inside the actual core[-4,d+4]. No end wall participates. The selected far mirrors remain at the originalx=D+2; their source/target roles exchange, and both actual selected widths areD+1. Every tooth fold/contact from R46 therefore remains an ordinary actual reflection, and originalT is reached.

This is a DIRECT check of the already explicit path in the actual A1 geometry. It is not an inference that arbitrary tooth changes preserve illumination. R45+R46, once independently accepted, supply all positive integera. The second widthb is unused, independently arbitrary and can be real.

## 2. d1,D0: one actual eight-reflection path, all a,b>0

Use the literal path

    (1,-2), (0,2/3), (1,10/3), (3/8,5), (0,4),
    (9/8,1), (15/8,3), (2,8/3), (11/8,1), (1,2).

Every leg has absolute slope8/3. The left turns at2/3 and4 lie in the smooth gaps(0,1),(3,5), disjoint from BOTH opposite mouths[-2,0],[1,3]. The right turn10/3 lies in(3,5), above the selected upper mouth. The roof turn(3/8,5) is in the ACTUAL smooth roof interior0<x<1. The four upper selected-tooth turns are ordinary horizontal-wall points at(9/8,1),(15/8,3),(11/8,1) and its true far point(2,8/3). All are strict wall interiors:1<x<2 for the horizontal contacts and1<8/3<3 for the far contact. Actual seamS/T are traversed as interior points, never used as mirrors. Direct sign changes show the ordinary specular law at each of the eight turns. All crossings are inside the original room and the last leg reaches originalT first.

The path never hasx<0, so neither a nor b enters its coordinates or wall guards. It proves the entire two-real-width family forD0. Five focused fixed-room searches(a2,b1/2/3/4/8) first produced this SAME path; the hand guards above replace every width-tail/finite-prefix dependency forD0. Earlier one-excursion charts and end-chart discrimination were useful discovery, but are NOT dependencies of this simpler finalD0 proof. Failure of their one remaining chart was never interpreted as darkness.

## 3. d1,D1/2: a lower-tooth round trip with protected exit shuttles

Let e_s,e_t beD(normal actual arm) orD+2(actual far-reflected arm). Choose integers n_s,n_t,k>=0 except that n_s,n_t may be negative, and n>=0. The positive slope tau and these values specify

    y_s=-2+2n_s+e_s*tau,
    y_t= 2+2n_t-e_t*tau,
    P1=y_s+tau,  P2=y_t-(2n+1)*tau.              (1)

The source/target folded arms are exactly R46 section2, with source/target bands[-3,-1],[1,3]. Normal arms stop before their far walls; far arms fold depthr atD+1 and terminate at originaldepthD. They are actual regular paths provided strict portals hold and tau is not an odd integer when either far arm is used. No source-to-central core mirror is used: cross from(1,y_s) directly to the actual lower left mouth(0,P1).

In that lower tooth use physicalx=-r thenr-2a for0<=r<=2a and y=-2+F(P1+2+tau*r), whereF is height2 folding modulo4. Require

    P1+2a*tau=P2+4k,    -2<P1,P2<0.             (2)

The exit is UPWARD. Its true far-wall phase P1+2+a*tau must not be an even integer. It then has one regular far reflection and2k ordinary horizontal reflections, all at strict actual depths. After exit make2n alternating core turns, beginning on the right, then enter the selected target mouth:

    x1,y=P2+(2i-1)*tau;  x0,y=P2+2i*tau,
    i=1,...,n; then x1,y_t.                      (3)

Every right turn will be in(-1,1), every left turn in(0,1). Thus both opposite mouths[-2,0],[1,3] are avoided strictly and their independent widths cannot affect this route. Append the actual target arm, ending at originalT.

### D1, every a>=2

Take e_s=e_t=1, n=1, n_s=n_t=0. Put

    j=floor((a+3)/4)+1, k=j-1, tau=2j/(a+3).

The interval ((a+3)/4,(a+3)/2) has length(a+3)/4>1, so1/2<tau<1 for EVERYa>=2. In(1), y_s=-2+tau, y_t=2-tau, P1=-2+2tau, P2=2-4tau. All portals are strict. The two core turns are2-3tau in(-1,1), and2-2tau in(0,1). Equation(2) follows from2(a+3)tau=4(k+1). The lower far phase is2+2k-tau in(1+2k,3/2+2k), never an even integer. No selected far arm is needed.

### D2, every a>=6 and the three smaller odd a1,3,5

Take e_s=4,e_t=2,n=1,n_s=-2,n_t=1. Set

    k=floor(a/2)+1, tau=(5+2k)/(a+5).

For a>=6 the allowablek interval(a/2,(6a+5)/10) has length(a+5)/10>1, giving1<tau<6/5. For a1,3,5 the respective slopes7/6,9/8,11/10 obey the SAME strict interval by direct comparison. In(1), y_s=-6+4tau, y_t=4-2tau, P1=-6+5tau, P2=4-5tau. All portals are strict. The two core turns are4-4tau in(-4/5,0) and4-3tau in(2/5,1). Equation(2) follows from(2a+10)tau=10+4k. The lower far phase is1+2k, an ODD integer and hence a smooth midrow far-wall point, never a corner. The selected source far arm is regular because1<tau<6/5 excludes every odd integer. The target arm is normal.

### Exactly three remaining (D,a) certificates

|D|a|e_s|e_t|n|n_s|n_t|k|tau|
|---|---|---|---|---|---|---|---|---|
|1|1|3|1|1|-1|0|0|3/5|
|2|2|4|2|1|-1|0|0|3/7|
|2|4|2|4|0|-2|3|3|13/8|

ForD1a1, (y_s,y_t,P1,P2)=(-11/5,7/5,-8/5,-2/5); the core turns are1/5,4/5 and the lower far phase is1. ForD2a2 these values are(-16/7,8/7,-13/7,-1/7); the core turns are2/7,5/7 and the lower far phase is1. ForD2a4 they are(-11/4,3/2,-9/8,-1/8); no intermediate core turn is required, and the lower far phase is59/8. Equation(2) holds in all three rows. Their nonintegral slopes exclude selected far corners. Consequently all are genuine finite paths for EVERY independentb>0.

## 4. Exhaustion, reproducibility and scope

For d>=2, section1 applies toD0/1/2. At d1, section2 handles everya,b forD0. Section3 handlesD1a>=2 plusa1; D2a>=6 plusa1/3/5 and remaininga2/4. Thus no vertical parameter or positive integer opposite width is left outside the literal theorem.

h2-A1-physical-check.py reconstructs the displayed arms, every lower horizontal fold, all intermediate core mirrors and actual endpoint arrival. It separately checks the rational formulas and replays234 prescribed original polygons/paths: all97 finiteR46 rows transferred atd2 andd1,000,000, local D1/2 controls including all small exceptions and largera with unequal realb, and theD0eight for independently variable reala,b. All2984 actual reflections and82160 wall/leg guards pass. These are prescribed controls, not independent peer review or a sample-based proof of the unbounded quantifiers.

Dependencies: frozen R45/R46 for the complete explicit protected family in section1, their own exact geometry definitions for prescribed replay, and elementary rectangle unfolding/specular reflections proved above. Sections2--3 do not assume a provided witness, illumination under compression, finite-state darkness, or the earlier unit-width A50 certificates. The discovered D0 path is now checked directly against every used ACTUAL wall. No all-comb or full canonical45 conclusion is claimed, and the existing native goal remains unfinished.
