# An entire pyramid winding family can miss an interior pair

**Verdict.** D172's proposed extension to every length and pair by arbitrary indices (i,j,k) in its specified sweep is false. The obstruction survives both source signs, both target signs and optional initial and final cap reflections. The same pair has a legal shot in the perpendicular sweep. Consequently this does not refute all-pairs illumination.

## Construction in a d169 residual cell

Use pyramid mask 761, with open horizontal runs, listed from the bottom, of (0,2), (0,V), (0,4), (0,2) at heights separated by y=0,1,65,67,69. Let V be any positive multiple of 192 greater than 192. The room is strictly simple and has ten maximal walls; its word is LLLLRLLRLR. Put S=(1/100,68) and T=(192,33). They occupy the top and right cells of the d169 residual. A common dilation makes both marks lattice marks if desired.

Consider a path traversing the top-to-bottom three-run chain once, allowing any number of transverse side reflections. Even allowing a turn at the top cap before entry gives effective initial travel a=1 or 3. The middle travel is d=2. The last travel is b=32 or, after reflecting across y=1, b=96. We may grant the entire latter line as a mirror for this exclusion. A legal turn into the additional bottom tooth is outside this family.

Let E be the signed first gate coordinate, folded about the common left side. Its necessary range is |E|≤2. Write s for the signed transverse travel per unit of longitudinal travel in a chart in which the first two runs fold by absolute value near that crossing. For an intermediate winding i and a terminal image Z=±192+2Vj, put L=2+b and M=(Z+8i)/L. The unfolded endpoint equation and both gates give exactly

    s=M−E/L,
    (1+a/L)E ≡ ±1/100+aM   (mod 4),
    |G|≤4,      G=R+bE/L,      R=2M−8i=(2Z−8bi)/L.

These are necessary even with closed gate windows. The first congruence incorporates every source winding k. The second gate follows by subtracting 8i at exit from the width-4 band. The same chart works for a cap reversal because only the longitudinal sign flips there.

For either b, Z/b≡2 modulo 4. Hence R is an odd multiple of 4b/L. Any such multiple except ±4b/L gives |G|≥10b/L>4. Write R=ε4b/L with ε=±1. Then legality at the second gate requires εE≤8/b≤1/4. On the other hand M=(Z−R)/b≡2−ε4/L modulo 4. Since a is 1 or 3, the possible values of ε(1+a/L)E are congruent to 2−4a/L±1/100 modulo 4. Only these positive representatives can satisfy |E|≤2: subtracting 4 gives magnitude at least 2+4a/L−1/100>2+2a/L, since L≤98 and 2a>L/100. Adding 4 also leaves the window. Thus

    εE ≥ (2L−4a−L/100)/(L+a) > 1

for L≥34 and a≤3. The gates contradict one another. The two integer signs and all windings were retained throughout.

## Transposed repair

Travel from T leftward. With transverse origin y=1, the first two runs are (0,64) and (0,66). The last is (−1,68), so the last run shares neither endpoint with the middle run. It is enough for the second signed crossing to fall inside the *physical* interval (0,66). Both folds are the identity there. This is a smaller window than the double-width window at a shared side, but its center can be used to aim the shot.

The travels are a=188, d=2, b=199/100. The target ordinate in this chart is 67. Take i=j=0 and M=67/(d+b)=6700/399. The representative of 32+aM modulo 128 nearest zero is X=−4432/399. Using slope M−X/(a+d+b)=323500/19199 gives the signed crossings −4432/19199 and 642568/19199. The first lies strictly within 64 of the shared side; the second lies strictly between 0 and 66. The terminal ordinate is 67 in the chart, or 68 physically. D164's exact tracer, using physical launch (−19199,323500) from T, returned S with 50 reflections. The traversed slab is identical for the entire V family. No ray or room search was used.

The open question for this word is now whether at least one of the two orientations, with the actual physical-overlap window when a shared side is absent, or a route that revisits a joint, always works. The forward winding indices alone cannot prove it. [Reviewed three-run lemma](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d172-review-pyramid/review.md)

## Ledger words moved and smallest word still OPEN

No additional move from this obstruction. LLLLRLLRLR is PARTIAL under d172. LLLRLLRLLR is PARTIAL under d169. A smallest word still OPEN is LLLRLLLRLR, W=10, realized by (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2).
