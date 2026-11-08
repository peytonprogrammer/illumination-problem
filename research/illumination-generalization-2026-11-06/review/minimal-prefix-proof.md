# R46: the entire h=2 B/C minimal-common-depth families

Author proof pending independent review. This joins the explicit R45 tails with a COMPLETE finite central-width prefix. It proves illumination for the literal B/C rooms in R45, for every D in {0,1,2}, every positive integer central width w, every allowed integer mu, and independently arbitrary positive REAL floor/roof widths. The canonical45 W<=21 theorem remains OPEN: these rooms are only one residual part of one orthogonal-comb model.

Original effort start 2026-11-07T07:00Z/deadline07:14Z includes the generalized-shuttle preliminary reasoning. Exact chart discrimination found certificates, not a darkness test. The proof relies on finite positive certificates plus the strict all-parameter argument below, not on completeness of the chart search.

## 1. Geometry and finite complement

Subtract mu from every ordinate. Core x in [0,1], y in [-mu,G-mu]; selected right teeth [1,D+2]x[-3,-1] and [1,D+2]x[1,3]. Actual S=(1+D,-2), T=(1+D,2). Central LEFT tooth [-w,0]x[0,2]. The floor-flush left tooth has upper ordinate 2-mu<=-2. The roof-flush left tooth, when present, has lower ordinate G-mu-2>=3. The exact B/C restrictions and tooth list are those of frozen R45. No extra teeth are silently allowed.

Every core mirror used below has either x=0,y in(-2,0) or x=1,y in(-1,1). These are ACTUAL smooth mirrors independent of both flush widths. No path uses an end wall. All central-tooth points have y in[0,2], and all selected-tooth points stay in their actual rectangles. Thus all geometric parameters outside the local tuple (D,w) disappear from the strict legality proof.

R45 supplies all w>=13 forD0, w>=20 forD1, w>=67 forD2. The complement has EXACTLY 12+19+66=97 (D,w) rows, listed in section5. Each is a finite exact rational certificate uniform in mu and both flush widths. A translation making S even-even also makes T even-even since T-S=(0,4); no other interior marks are excluded. Noninteger flush widths give a stronger orthogonal-room implication, not a claim of canonical lattice geometry for those noninteger inputs.

## 2. Endpoint charts, with actual far folds

A row gives integers e_s,e_t in {D,D+2}, m,k>=0, n_s,n_t, sign sigma in {+1,-1}, and positive rational tau. Define

    y_s = -2+2n_s+e_s*tau,
    y_t =  2+2n_t-sigma*e_t*tau,
    P1  = y_s+(2m+1)*tau,
    P2  = y_t-sigma*tau.

All rows satisfy y_s in(-3,-1), y_t in(1,3), P1,P2 in(0,2). For a normal endpoint arm e=D, unfold from its actual mouth to depthD. For a far arm e=D+2, unfold to depthD+2, folding depth by

    depth(r)=r (0<=r<=D+1),
    depth(r)=2(D+1)-r (D+1<=r<=D+2).

This maps the end to the ORIGINAL depthD and inserts exactly one ACTUAL far-wall reflection. At D0 the far-arm endpoint is the actual seam, and no interior r maps to depth0. Use height fold F(z)=min(z mod4,4-(z mod4)). The source arm, written in reverse from mouth to source, is

    x=1+depth(r), y=-3+F(y_s+3-tau*r), 0<=r<=e_s.

Its terminal phase is1+2n_s, which folds to midpoint1, so it ends at actualS. Reverse this finite path. Its outgoing mouth velocity is(-1,+tau). The target arm from mouth is

    x=1+depth(r), y=1+F(y_t-1+sigma*tau*r), 0<=r<=e_t.

Its terminal phase is1+2n_t and hence ends at actualT. For e=D use depth(r)=r throughout. At D0,e0 the corresponding arm has zero length; the seam is not used as a mirror.

In either far arm the far-wall phase equals1+2n_s+tau (source reverse) or1+2n_t-sigma*tau (target). A far corner occurs precisely when this is an even integer, equivalently tau is an ODD INTEGER. Every selected row with a far arm excludes odd integral tau. All other horizontal folds occur at strictly positive depth and strictly short of the actual far wall; strict mouth phases exclude mouth corners. Normal arms cannot touch their unused far walls. Endpoint horizontal reflection counts can vary, but every row is finite and every actual contact is regular.

## 3. Actual core and central-tooth matching

From (1,y_s), follow upward slope tau through exactly 2m alternating core mirrors

    (0,y_s+(2i-1)*tau), (1,y_s+2i*tau), 1<=i<=m,

then enter the central LEFT mouth at(0,P1). Every row checks

    -2<y_s+(2i-1)*tau<0,
    -1<y_s+2i*tau<1.                               (C)

Hence all these are the protected actual mirrors from section1. Open crossings have0<x<1. All core heights are between-3 and3, strictly inside the core's actual floor/roof levels in every B/C family.

Inside the central tooth use horizontal developed distance r from0 to2w, physical x=-r forr<=w and x=r-2w forr>=w, and physical y=F(P1+tau*r). The exact matching equation is

    P1+2w*tau = P2+4k,       sigma=+1,
    P1+2w*tau = 4-P2+4k,     sigma=-1.             (M)

For sigma+ the exit derivative is upward; for sigma- it is downward, matching the chosen target core velocity. Both have one genuine central far-wall reflection. Its phase P1+w*tau is NOT an even integer in any row, so no far corner occurs. Strict P1/P2 exclude any horizontal contact at the open mouth. All other horizontal contacts have positive depth strictly less thanw. There are2k horizontal reflections for sigma+, and2k+1 for sigma-.

After exiting at(0,P2), cross the core directly to(1,y_t), with velocity(+1,sigma*tau), then take the actual target arm in section2. This reaches originalT; it does not merely hit a periodic image. Every point belongs to the original rectangle-union room. Earlier target arrival, if present, can be truncated and already supplies illumination; the independent controls additionally check first arrival.

## 4. Exact finite certificate verification

The table below supplies tau and the seven integer/sign parameters. Its validity can be verified without any search: for EACH literal row, recompute y_s,y_t,P1,P2 as rational numbers; verify the strict intervals, (C), (M), k>=0, no forbidden odd-integer far-arm slope, and P1+w*tau not an even integer. These finite rational comparisons and equalities, together with sections1--3, prove the entire finite complement for arbitrary mu and flush widths. No limiting argument, continuity at a corner, monotonicity under widening or unit-flush witness transfer is used.

The chart-check JSON records all97 witnesses; the physical checker reconstructs each selected arm, every horizontal fold, every core mirror and the actual central far reflection. It replays ALL97 rows in four prescribed ACTUAL room instances each: minimum B, minimum C1, minimum C2, and a distant C1 with mu=1,000,000, including noninteger and large unequal flush widths. All388 original-wall paths pass, totaling4640 actual reflections and127140 exact wall/leg guards. Those388 checks are controls; the UNBOUNDED parameter quantifiers come from the strict protected-mirror argument. The finite checker does not assert the explored chart inventory exhaustive.

Together with independently reviewed R45 (once accepted), these finite certificates give EVERY positive integerw for all three stated h2 B/C minimal-depth families. They do not cover other vertical patterns, general core widths, taller teeth, arbitrary chamber trees or diagonal walls, and supply no universal canonical45 conclusion.

## 5. Complete finite table

All entries are literal rationals/integers. The order is D,w; sigma is the target-arm vertical sign.

|D|w|e_s|e_t|m|n_s|n_t|sigma|k|tau|
|---|---|---|---|---|---|---|---|---|---|
|0|1|0|2|1|0|1|1|0|3/4|
|0|2|0|0|1|0|0|1|1|1|
|0|3|0|0|1|0|0|1|1|4/5|
|0|4|0|2|1|0|1|1|1|5/7|
|0|5|0|0|1|0|0|1|2|6/7|
|0|6|2|0|1|0|0|1|1|4/9|
|0|7|0|2|1|0|1|1|2|7/10|
|0|8|2|0|2|0|0|1|1|1/3|
|0|9|2|0|2|0|0|1|1|4/13|
|0|10|2|0|1|0|0|1|2|6/13|
|0|11|2|0|1|0|0|1|2|3/7|
|0|12|2|0|2|0|0|1|2|3/8|
|1|1|1|3|1|0|1|1|0|3/5|
|1|2|1|1|1|-1|1|1|1|6/5|
|1|3|1|1|1|0|0|1|1|2/3|
|1|4|1|1|1|0|0|1|1|4/7|
|1|5|1|3|1|0|1|1|1|5/9|
|1|6|1|1|1|0|0|1|2|2/3|
|1|7|1|1|1|0|0|1|2|3/5|
|1|8|1|1|1|0|0|1|2|6/11|
|1|9|1|3|1|0|1|1|2|7/13|
|1|10|3|1|2|0|0|1|1|4/15|
|1|11|1|1|1|0|0|1|3|4/7|
|1|12|1|1|1|0|0|1|3|8/15|
|1|13|1|1|2|0|0|1|2|6/17|
|1|14|1|3|2|0|-1|-1|2|7/19|
|1|15|1|3|2|0|-1|-1|2|7/20|
|1|16|3|1|2|0|0|1|2|2/7|
|1|17|3|1|2|0|0|1|2|3/11|
|1|18|3|1|2|0|0|1|2|6/23|
|1|19|1|1|2|0|0|1|3|8/23|
|2|1|2|4|1|-1|2|1|0|5/6|
|2|2|2|4|1|0|1|1|0|3/7|
|2|3|2|2|1|-1|1|1|1|6/7|
|2|4|2|4|2|0|-1|-1|0|3/10|
|2|5|2|2|1|0|0|1|1|4/9|
|2|6|2|4|1|0|1|1|1|5/11|
|2|7|2|4|1|0|1|1|1|5/12|
|2|8|2|2|2|0|0|1|1|4/13|
|2|9|2|2|1|0|0|1|2|6/13|
|2|10|2|2|1|0|0|1|2|3/7|
|2|11|2|4|1|0|1|1|2|7/16|
|2|12|2|4|1|0|1|1|2|7/17|
|2|13|2|2|1|0|0|1|3|8/17|
|2|14|2|2|1|0|0|1|3|4/9|
|2|15|2|2|1|0|0|1|3|8/19|
|2|16|2|4|1|0|1|1|3|3/7|
|2|17|2|4|1|0|1|1|3|9/22|
|2|18|2|4|2|0|-1|-1|2|7/24|
|2|19|4|2|2|0|0|1|2|6/25|
|2|20|4|2|2|0|0|1|2|3/13|
|2|21|2|2|2|0|0|1|3|4/13|
|2|22|2|2|2|0|0|1|3|8/27|
|2|23|2|4|2|0|-1|-1|3|9/29|
|2|24|2|4|2|0|-1|-1|3|3/10|
|2|25|2|4|2|0|-1|-1|3|9/31|
|2|26|2|2|2|0|0|1|4|10/31|
|2|27|4|2|2|0|0|1|3|8/33|
|2|28|4|2|2|0|0|1|3|4/17|
|2|29|4|2|2|0|0|1|3|8/35|
|2|30|2|4|2|0|-1|-1|4|11/36|
|2|31|2|4|2|0|-1|-1|4|11/37|
|2|32|2|4|2|0|-1|-1|4|11/38|
|2|33|4|2|3|0|0|1|3|1/5|
|2|34|4|2|3|0|0|1|3|8/41|
|2|35|4|2|2|0|0|1|4|10/41|
|2|36|4|2|2|0|0|1|4|5/21|
|2|37|4|2|2|0|0|1|4|10/43|
|2|38|4|2|2|0|0|1|4|5/22|
|2|39|2|4|2|0|-1|-1|5|13/45|
|2|40|4|2|3|0|0|1|4|10/47|
|2|41|4|2|3|0|0|1|4|5/24|
|2|42|4|2|3|0|0|1|4|10/49|
|2|43|4|2|2|0|0|1|5|12/49|
|2|44|4|2|2|0|0|1|5|6/25|
|2|45|4|2|2|0|0|1|5|4/17|
|2|46|4|2|2|0|0|1|5|3/13|
|2|47|4|2|2|0|0|1|5|12/53|
|2|48|4|2|3|0|0|1|5|12/55|
|2|49|4|2|3|0|0|1|5|3/14|
|2|50|4|2|3|0|0|1|5|4/19|
|2|51|4|2|2|0|0|1|6|14/57|
|2|52|4|2|2|0|0|1|6|7/29|
|2|53|4|2|2|0|0|1|6|14/59|
|2|54|4|2|2|0|0|1|6|7/30|
|2|55|4|2|2|0|0|1|6|14/61|
|2|56|4|2|2|0|0|1|6|7/31|
|2|57|4|2|3|0|0|1|5|3/16|
|2|58|4|2|3|0|0|1|5|12/65|
|2|59|4|2|2|0|0|1|7|16/65|
|2|60|4|2|2|0|0|1|7|8/33|
|2|61|4|2|2|0|0|1|7|16/67|
|2|62|4|2|2|0|0|1|7|4/17|
|2|63|4|2|2|0|0|1|7|16/69|
|2|64|4|2|2|0|0|1|7|8/35|
|2|65|4|2|2|0|0|1|7|16/71|
|2|66|4|2|3|0|0|1|6|14/73|
