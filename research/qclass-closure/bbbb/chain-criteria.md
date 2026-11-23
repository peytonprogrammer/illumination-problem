# When rational column chains guarantee illumination

The tests below use full rectangular columns between successive vertical seams, strictly positive horizontal travels, and open overlaps. A path proceeds to the right and may reflect off horizontal walls. Distances and periods are rational unless explicitly varied. Marks can have real heights. In particular none of the criteria requires the special horizontal offsets in D58.

## Any number of columns: a width test independent of the marks' heights

Use the [placement formula](placement.md) with travels d_j, X their sum, seam distances A_i from the start, and periods P_j twice the column heights. The seam-height lattice has generator matrix

    G_ij = P_j (A_i/X − 1_{j≤i}).

The endpoint heights enter only in the translate. Pick an ordering of the seams. Clear a common denominator D from G, and let h_i be the gcd of the absolute i-rowed minors of the first i rows of DG, with h_0=1. If every open seam width exceeds **h_i/(D h_{i−1})** in this order, every translate of the lattice meets the product of overlaps. Thus all choices of the two interior heights are lit for those travels. One passing order suffices.

Let n be the number of columns and let Λ_i be the projection of DGℤⁿ onto the first i seam coordinates. It has rank i because, with real indices and a common slope, each column index can be chosen to realize the desired rise. Full row rank gives finite index [ℤⁱ : Λ_i] = h_i by integer diagonal reduction. Deleting the last coordinate maps Λ_i onto Λ_{i−1}. Their ranks differ by one, so the kernel has rank one along the last coordinate, with step h_i/h_{i−1} by the index product formula. Having placed the first i−1 heights, the next therefore ranges over an arithmetic progression of the stated spacing. A strictly wider open interval contains a point in every such progression. This proves the test by induction. Failure of the inequalities leaves the actual translate to check.

## Three columns: a sharp compatibility test before lengthening the middle one

Let the outer travels be a,b and the middle length be ℓ. Write I,J for the two overlap intervals, with widths u,v and centers i,j. Let S,T be the endpoint heights and P,Q,R the periods of the three columns. These statements use the positive sheet at both seams. The slope s is signed. The outer legs accept physical crossing heights x∈I and y∈J exactly when

    x = S+a s mod P,      y = T−b s mod R.

Eliminating s gives b x+a y ∈ bS+aT+gℤ, where g=gcd(bP,aR) is the positive generator of their integer span. Bézout proves the converse, including common slope and correct signs. Put e=dist(bi+aj−bS−aT,gℤ). An open common slope interval exists **if and only if** 2e<bu+av. No length of the middle column can fix incompatibility on these sheets.

More quantitatively, define

    δ = min(u/a, v/b, (bu+av−2e)/(2ab)).

For any 0<δ′<δ, erode the first interval at each end by aδ′/2 and the second by bδ′/2. The same congruence finds a center slope in both eroded windows. The full closed slope interval of width δ′ works. Along it the mismatch x+ℓs−y has derivative a+ℓ+b. If **(a+ℓ+b)δ>Q**, choose δ′ just below δ; the mismatch sweeps a full middle period. At its multiple of Q all three legs glue. For an endpoint-height-independent test substitute g for 2e, since 2e≤g. This separates the finite arithmetic needed to enter both doors from the gain obtained by lengthening the corridor.

## Shrinking the travel in the last column

Fix a rational prefix of any length. Suppose a positive-sheet path in that prefix reaches the center of the final overlap at slope s₀. A_i denotes the distance to an earlier seam and m_i its actual clearance from the nearer edge of its overlap. Let A be the total prefix travel, w the last overlap width and c the travel from that seam to the target. Put

    η = min(w/(2A), min_i m_i/A_i).

Omit the inner minimum when there are no earlier seams. Every slope s₀+t with |t|<η stays in the same unfolded overlap windows; its last height changes by At. Choose any L>0 such that Ld_j/P_j is an integer for every prefix column. Adding an integer multiple of L to the slope and the corresponding whole periods in each prefix column preserves every seam height and the exit orientation. Up to the target period P_last, the possible final heights therefore include intervals of width 2(A+c)η with centers differing by cL. For rational c, **2(A+c)η > gcd(cL,P_last)** suffices for every target height. In particular **cL < 2(A+c)η** suffices even without using a gcd, since the successive centers on the developed line have spacing cL. This argument also permits varying P_last.

With a fixed positive-width last overlap and a fixed prefix witness, every sufficiently small c works. If the last overlap shrinks about the same accessible center and the earlier clearances stay fixed, then eventually η=w/(2A). For example c≤w/L suffices for c>0. The hypothesis is substantive: changes to the prefix can destroy the center witness or drive L to infinity.

## Application: every lattice pair in the long DBw2 dumbbell

Use D69's two chambers of sizes 5 by 5 and 5 by 6, both with bottom at 0, joined by a width-two horizontal corridor with vertical span (1,3). Keep the chamber shapes fixed and allow any integer corridor length ℓ>10. **Every two distinct interior lattice points are lit.** D69 identifies the original length-four room as true BBBB. Lengthening retains 12 walls. In particular lengths coprime to 5 give primitive horizontal differences, and the unit vertical offset gives primitive vertical differences. Their area 55+2ℓ exceeds 64, so D69’s Q/proper-factor bounds put this infinite normalized subfamily in true BBBB. The illumination argument holds regardless of normalization.

For opposing chamber marks the distances a,b to the two mouths lie in {1,2,3,4}. Here u=v=2, P=10, Q=4 and R=12. Substituting g=gcd(10b,12a) for 2e gives the following lower bounds on δ, rows a and columns b:

| a | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| 1 | 1 | 1/2 | 1/3 | 1/2 |
| 2 | 1 | 1/2 | 1/3 | 1/4 |
| 3 | 2/3 | 1/2 | 1/3 | 5/12 |
| 4 | 1/2 | 1/2 | 1/3 | 1/4 |

The largest 4/δ−a−b is 10, at (2,4). At ℓ = 10, using the actual endpoint heights leaves four pairs uncovered, including (3,1)–(19,2). Whether those four pairs are lit remains unchecked. The resulting proof also allows arbitrary real transverse heights at these longitudinal coordinates.

A lattice mark in the corridor or either mouth has height 2. For a chamber mark at distance a from the mouth and a corridor target at depth c>0, fix the source image and unfold the corridor target. Its images at heights 2+2k use the two possible final orientations. The straight segments to those images cross the mouth in a progression of step 2a/(a+c)<2. Some segment crosses strictly inside (1,3). The rectangles on both sides justify folding. At c=0 the chamber segment is direct. Two marks contained in one chamber or in the closed corridor see each other directly, with interior endpoints as assumed.

## Where the criteria stop

* **A true BBBB obstruction to monotone placement.** In D69's original DB55, S=(1,1), T=(9,1) are interior and same-class. Their x-midline is the first mouth x=5. Any x-monotone lighting path has a lattice midpoint there, by unfolding about horizontal integer walls. The open mouth is 2<y<3 and contains no integer. Its endpoints are corners, and elsewhere the line meets a vertical boundary or exterior. Thus even the union over sheets misses; letting all rational chains pass unconditionally is impossible. D69's saved verdict lights the pair by allowing more paths.
* **A turn already at one seam.** In cov2929, S=(3,1), T=(5,3) straddle x=4 with equal travels and adjacent runs (0,4), (2,6). A monotone path would cross in (2,4) at the average of an image ±1 mod 8 and an image 3 or 1 mod 8. The residues are 0,1,2 mod 4. All miss the open window. This is a Q-class turning control. D72 supplies a lighting path on the line of direction (−2,3). A hub whose available section changes inside the purported column must first be split; then all new seam constraints must hold together. When the path must reverse horizontally, even a valid full-column split cannot bring it into this family.

Thus these are geometric and arithmetic sufficient conditions on a pair or on specified endpoint positions in a room. They give no wall-count-only criterion for the whole BBBB class. [Named geometries and midpoint lemma](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md) · [Turning witnesses](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d72-cylinder-test/README.md)
