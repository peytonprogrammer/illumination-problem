# D58 double resonance is illuminated in the named shrinking construction

**Result.** All eight midpoint position types in the D58 double-resonance builder are lit for every integer exponent k≥2 for which the builder gives the prescribed room. This includes all 18 recorded simultaneous H/E failures and arbitrarily small widths. The other two position types of mask 971 have a different cap depth and are outside the double-phase assertion. The named rooms have ten walls. Rational rescaling to lattice coordinates preserves the lighting paths.

The direct and cap image families really do miss: β=1/20, D=16h and cap depth 3h give the two pairs of bad phases recorded in [the D58 memo](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d58-corridor-limit/memo.md). Use a path monotone in the **transverse** coordinate x instead. Between source x and target x the room consists of two or three full rectangular columns. Crossing their common sides at strictly interior overlap heights gives a physical path. In the last column, folding away the whole vertical periods leaves height T at the target’s horizontal coordinate, so the path ends at the target itself.

## A placement lemma for rational chains of full columns

Let the traversed horizontal distances be d_j>0 (partial distances in the first and last columns), total X, and let P_j be twice each column's vertical height. Write S,T for endpoint heights. At every interface choose the sheet on which the physical vertical velocity has the sign of the unfolded slope s. Each column admits an independent integer number of vertical periods. For integer indices m_j set

    s = (T−S+Σ P_j m_j)/X,
    y_i = S + (d_1+...+d_i)s − Σ_{j≤i} P_j m_j.

If the affine lattice of vectors (y_i) meets the product of the open vertical overlaps, the endpoints are lit. Indeed in column j the unfolded rise equals the difference of the prescribed physical exit and entry heights plus P_j m_j. Folding stays inside that column, and at each seam the physical height and signed slope agree. Open overlaps exclude every seam corner. The rectangles have no internal corners. This is a sufficient test for any number of full columns, including resonant chains. It specializes D58's Lemma K by testing actual discrete placement. A miss would exclude only these sheet choices.

## The finite arithmetic

For k=2 through 15, substitute D58's exact rational dimensions. In two columns, the single height progression has spacing equal to the gcd of its rational generators. In three, clear denominators. Let the integer generator columns be (v_j,w_j). The first-coordinate step is g=gcd(v_j). Bézout gives one displacement (g,t). The vertical kernel spacing is H=gcd of the absolute two-by-two minors divided by g (integer lattice index, or column elimination). Thus at first coordinate c+gi the second coordinates are e+ti+Hℤ for base point (c,e). The number strictly inside a scaled second window (l,u) is

    floor((u−1−e−ti)/H) − floor((l−e−ti)/H).

Sum over the first window using Euclidean floor sums; the script repeats the count with coordinates interchanged. Each count gives the number of distinct crossing-height vectors inside the open overlaps. Several paths can realize the same vector. Every applicable count is positive. This computes counts without enumerating rays, directions, words or candidate indices. A dash denotes an unavailable construction; “outside” denotes the different cap depth. Columns of the output are k=2,...,15. [Exact calculation](placement.py) · [Output](placement.txt)

## All k ≥ 16

Use the builder's units. The last horizontal travel is c=w/20. In the two-column case the seam progression contains a displacement of magnitude P₁c/X (vary only the first index). This is smaller than the overlap, which is at least 2, by the bound on X/c below.

In the three-column case write the travels a,b,c. If p is the door's left x-coordinate and u is the source x-coordinate, the intervening vertical seams are at 15p/16 and p. Thus b=p/16, a=15p/16−u. The D58 formulas give p/w=14/5+32j, u/w=6/5+32i. For n=2^(k−2), j is the nearest integer to n/6−7/80, and i the nearest integer to j/2+1/160. Since n modulo 12 is 4 or 8, j is odd and i=(j+1)/2. Consequently

    a=7b−316c,    X=a+b+c,    8a−7X=−323c,
    X/c=33+320(j−1)>800000.

The same X/c formula holds in two columns since the endpoints are unchanged horizontally. The numerical bound follows from n≥16384 and j≥n/6−1. Throughout this range j≥2 gives a>0, hence u<15p/16, and p+w=(19/20+8j)/n<4 since j≤n/6+1. The builder varies only horizontal coordinates with k, so the same column layout and heights apply throughout.

Write y₁,y₂ for the two crossing heights. From the placement formula, increasing m₁ by one changes **8y₁−323y₂** by −P₁ (use 8a+323c=7X). Choose m₁ by rounding so that this linear combination is within P₁/2 of its value at the center of the overlap box. Let M be the least real number M>0 such that both M/P₁ and M/P₂ are integers. The integer change

    (Δm₁, Δm₂, Δm₃) = (7M/P₁, M/P₂, 0)

preserves that linear combination and changes y₁ by −323Mc/X. Round a multiple of this change to bring y₁ within 323Mc/(2X) of the first window center. The resulting error in y₂ is at most (P₁/2+8·323Mc/(2X))/323.

Here the first two periods (P₁,P₂), by named three-column type in builder order, are (13/2,6), (8,6), (6,4), (25/4,6), (6,8), and (17/2,6). These follow by summing the fixed vertical gaps of each occupied column. Thus M≤150 and P₁≤17/2; both overlap widths are at least 2. The two errors are respectively less than 0.031 and 0.014. Both seam crossings are strictly inside. This gives an integer placement for every remaining exponent with no search.

**Scope.** The counting lemma applies to rational chains of full rectangular columns. The all-exponent proof uses the specific transverse offsets of D58's builder, especially 8a−7X=−323c. The four bad H/E phases alone do not imply that identity or the full-column geometry. Placement for arbitrary rooms with those phases, and for general chains with cut hubs, remains open. This construction supplies no dark pair.
