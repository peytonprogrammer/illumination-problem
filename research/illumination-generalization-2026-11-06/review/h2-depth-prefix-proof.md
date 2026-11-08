# R57: partial continuous protected prefix; full compact-prefix obligation remains open

Original effort 2026-11-07 08:02–08:16 UTC, 840 seconds aggregate. Retired early after bounded discovery failure; no restart, continuation scan, or renewed deadline. Main universal goal remains OPEN.

## Result and precise scope

Core [0,1]×[0,9]; RIGHT teeth [1,3] of width1/3 and [5,7] of width w_t>D; LEFT bands [2,4],[5,7] with arbitrary independent positive widths. S=(1,2), T=(1+D,6). Six protected reflection words give continuous coverage of **0<=D<14/15**, pending independent review. No claim at D=14/15 or the rest of [0,2]. Accepted R42 separately covers D>2. This is a limited result of the already-running effort, not a proposed universal bridge or a reason to continue a case catalogue.

Use the ordered20-vertex probe contour in h2-depth-prefix-check.py. Its LEFT widths are1 and target widthD+1. Wall IDs refer to consecutive ordered vertices. Exact certified subsets sufficient for the join are:

|word|open parameter intervals|additional exact points|
|--|--|--|
|19,0,3,15|(0,2/9)|0|
|19,0,1,19,5,15|(0,2/9),(2/9,2/5)|2/9|
|3,15|(0,2/3)|none|
|15,9,10,11,6|(4/11,1/2),(1/2,4/5)|1/2|
|0,19,5,11,10,6|(4/7,4/5),(4/5,12/13)|4/5|
|4,3,0,19,5,11,10,6|(2/3,5/6),(5/6,14/15)|5/6|

Overlaps fill every listed internal endpoint, giving [0,14/15). No extra target turn or left-tooth visit is permitted. The target far wall8 and left-mouth/far/horizontal walls12,13,14,16,17,18 are rejected. Walls11,15,19 are real core-left mirrors. A collision in the target band at x>1+D is also rejected. Thus every accepted path is confined to the core, source tooth, and portion of the target tooth before its actual target depth. Arbitrary positive LEFT widths and any target width>D preserve the entire path and actual first-target arrival. Positive scaling x by c gives source widthc/3 and target depthcD.

## Why parameter cells suffice

For a fixed word avoiding wall8 and LEFT entries, all reflecting support lines are independent of D. Compose actual reflections on the RIGHT of the current developed copy map. Every copy map is C_j(x,y)=(epsilon_x x+u,epsilon_y y+v) with constant translations. The unfolded final target C_n(1+D,6) has affine horizontal coordinate and constant vertical coordinate. The developed ray from S consequently has direction (alpha D+beta,gamma). For the six displayed words gamma is nonzero.

In each visited copy, all20 polygon corners have affine horizontal and constant vertical coordinates. Their determinants with the ray are affine functions of D. Split [0,2] at every nonidentically-zero determinant root and at the horizontal-direction pole alpha D+beta=0. Include early-target determinants for C_j(T(D)) at every prefix and protection-line determinants for C_j(1+D,5), C_j(1+D,7). All cuts are rational; check EACH cutpoint separately.

On a complementary open interval, collision combinatorics cannot change. Starting from the actual interior source, a strict first collision varies continuously until the ray passes a polygon vertex or becomes parallel to its support. Those events are in the cut set (gamma never vanishes). Induct on successive prescribed collisions using the developed copies. A change of the nearest wall requires a tie, which is a physical corner for a strictly simple polygon; disjoint physical edges cannot tie at the same ray point. Identically zero corner determinants remain degenerate throughout that cell and fail the representative check when encountered; they do not hide a transition.

An earlier actual target occurs only when its copy is collinear. Nonidentical such events are cutpoints. If collinearity is identical, its position order cannot change without passing the source or a collision. Passing the source is impossible because S and T(D) differ in y; passing a collision is impossible because T(D) stays strictly interior. Protection can change only when a target-band horizontal collision crosses x=1+D; its y is5 or7 and the corresponding cut is included. Other collision vertices have x<=1, or belong to the forbidden target far wall. Linear legs attain their horizontal extrema at endpoints. Therefore exact first-hit tracing at one rational representative proves the strict prescribed word and protection for that whole open cell. Singleton cutpoints are traced independently and are never inferred by continuity.

The checker uses Fraction throughout. For every collision it minimizes positive ray/finite-wall intersection times, rejects corner ties/endpoints, reflects the actual velocity, and stops at the ORIGINAL T only if strictly before the next wall. It rejects a different word when certifying a cell. This is continuous-cell certification with exact witnesses, not a finite grid promoted to an all-real assertion. Independent mathematical review of this cell argument is required before acceptance.

## Failure and handoff

Bounded group-image discovery at D=14/15 found no protected witness with max(|k|,|r|)<=24 and at most70 reflections. The tested vectors were (sigma D+sigma-1+2k/3,2r). This finite failure proves no nonexistence statement, even in the protected subclass. It certainly does NOT show darkness. The full-prefix goal is unfinished; wider words, tooth excursions, or another mechanism may cover the remainder. Daniel's approved bridge pivot supersedes further comb expansion after the current reviews.
