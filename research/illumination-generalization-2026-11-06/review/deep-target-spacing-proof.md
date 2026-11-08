# R42: seam-to-deep-midrow witness existence at every core width

Author theorem pending independent review. Original conservative effort deadline06:55:00Z is retained. Universal canonical45W21 remains OPEN.

## Statement

Let P be a finite strictly simple two-sided rectangular-spine comb, with core[0,c]x[0,G]. All vertical boundary coordinates are integers and every tooth has height2. Horizontal dimensions c>0 and tooth widths may be arbitrary positive REAL numbers. Same-side tooth bands have positive gaps; opposite-side bands may overlap. Let actual interior marks S=(c,s), T=(c+D,t) be on the midrows of different selected right teeth, with s<t and t-s an even integer. The source is an actual strict mouth seam, not a boundary mirror. The target is inside its tooth, whose width exceeds D. Suppose

    D>2c.

Then S illuminates T when W<=23. There is no horizontal commensurability assumption, input witness, depth/size/exception cap or finite-prefix hypothesis. The canonical integer A-pair corollary follows whenever the two original marks are actual A points. General off-midrow marks, other depth ratios and other polygon families remain outside this theorem.

## 1. A matched ray from a seam to a deep middle row

Take copied selected centers a<b, with seam source at(c,a), deep target(c+D,b), center gap2H=b-a, H>=2. The legitimate midpoint images of the height2 target have ordinates b+2n, n integer. Reflecting the source once in the opposite wall gives its image(-c,a). A straight line to(c+D,b+2n) has positive slope

    tau_n=(2H+2n)/(2c+D).

Its physical opposite-wall turn is M_n=(0,a+c*tau_n), followed by its target-mouth portal(c,a+2c*tau_n). Put mean=(a+b)/2 and

    delta_n=M_n.y-mean=(2cn-DH)/(2c+D).

The deltas are an arithmetic progression of step eta=2c/(2c+D)<1/2. Write x=DH/(2c)>H>=2 and choose

    n_minus=ceil(x)-1, n_plus=floor(x)+1.

Then -eta<=delta_minus<0<delta_plus<=eta. Even when x is an integer both are NONZERO, and their absolute values are STRICTLY below1/2 because eta<1/2. Both n are positive, so tau is positive and finite.

The actual target portal ordinate is b+2delta_n, strictly in(b-1,b+1). No portal corner occurs. Starting at that portal with upward velocity tau, unfold only the actual target tooth to its legitimate midpoint image b+2n. In local height phase the portal is1+2delta in(0,2), the target image phase is2n+1, and the intervening contacts are2,4,...,2n. Their horizontal distances are strictly between0 and D. Hence all n ordinary horizontal-wall reflections occur strictly between the actual mouth and original target, before its unused far wall. Folding the terminal midpoint image gives exactly the actual target middle row for either parity of n. The portal's folded derivative is upward, matching the incoming core leg. Source has no tooth arm and launches directly inward from its interior seam; no seam reflection is inserted.

The two core legs have the same slope and a genuine vertical reflection if M_n is on a smooth actual opposite wall. Their open interiors satisfy0<x<c. Therefore there are two fully matched finite candidates, one turn strictly on each side of the nominal mean, within distance1/2. A candidate inside an opposite mouth or at a corner is NOT accepted.

If the selected deep target center is BELOW the seam source, first reflect the vertical coordinate, apply exactly this construction and reflect it back. Both signs remain available; no equality of actual endpoint depths or swapped physical endpoint is assumed.

## 2. Three physical end charts

Use the target copies with centers t,-t,2G-t and the ORIGINAL source s. Their positive half-separations are h=(t-s)/2, mu=(s+t)/2 and G-mu, all integers>=2. The lower-target chart uses the vertical reflection just described. Fold the whole finite candidate by the actual core-end map F(y)=y on[0,G], F(-y)=F(y), F(y+2G)=F(y).

Their physical nominal turn levels are mu,h,G-h. Each lies in[2,G-2]. Its two candidates remain within distance<1/2 of that level, in a single open local isometry cell of F. Thus each chart still supplies TWO physical opposite turn heights, one strictly on each side of its nominal level. The distances need not be equal, which is unnecessary.

Every strict copied portal maps into the actual selected tooth band. Each target prefix contact maps to a smooth actual horizontal selected-tooth wall. Existing flush-tooth end-line contacts are ordinary reflections, not double-counted end crossings. Every open core crossing of a global end line has strict0<x<c and is a genuine smooth floor/roof reflection. All counts are finite. The starting point is original S and terminal image folds to original T. No target-sheet substitution or forbidden-corner continuation occurs. The selected actual target abscissa is first reached on the terminal target prefix; an earlier actual arrival after global folding, if any, can be used instead.

## 3. Darkness forces three opposite middle rows

Assume actual darkness. At any integer nominal level ell outside all closed opposite bands, an actual wall interval of radius at least1 is smooth, so either candidate connects. At an opposite mouth ENDPOINT, the smooth adjacent side has length at least1, because the bands have integer edges and positive same-side gaps. The candidate on that side again connects. Only a nominal level STRICTLY INSIDE a band can obstruct both sides. For height2 integer bands it is exactly the tooth midpoint.

Consequently darkness requires all three distinct nominal levels h,mu,G-h to be opposite tooth MIDPOINTS. Their adjacent separations are s and G-t. Put q=min(s,G-t). If q<=2, two of those height2 tooth midpoints are at distance at most2, making their bands touch or overlap, contrary to positive same-side gaps.

If q>=3, both selected teeth are nonflush. The three opposite midpoint teeth are different and nonflush: nominal levels lie in[2,G-2], excluding flush midpoints1,G-1. The entire room therefore has at least five distinct nonflush teeth, giving exact maximal-wall count W>=4+4*5=24. All extra attachments add nonnegative charge; opposite-side overlapping bands cannot merge exterior walls through core interior. This contradicts W<=23.

Thus at least one of the explicit candidates provides an actual finite trajectory. The proof supplies witnesses without a seed and is uniform in all independent horizontal dimensions under D>2c. The threshold equality D=2c is excluded: progression step1/2 could leave the nearest nonzero candidates exactly at target mouth corners. No conclusion about that boundary or smaller depths is imported from this proof.
