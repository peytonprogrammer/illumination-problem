# A W<=21 illumination theorem for integer thin two-sided combs

A39 candidate, pending independent review of the complete join. The global canonical45 objective remains OPEN. This proves a whole uncapped subclass, rather than a finite-prefix or fixed-growth statement.

## Theorem and exact class

Let P be any finite strictly simple two-sided rectangular-spine comb. Its core has integer boundary coordinates and integer transverse width c>=3. Every attached left or right tooth has width1 and height2, with integer coordinates. On each side, distinct tooth bands have strictly positive gaps. Opposite-side bands may overlap arbitrarily. All tooth bands lie within the core's global vertical range. Assume P has at most21 maximal straight walls.

Then EVERY pair of distinct actual interior even-even A points illuminates by a finite actual corner-avoiding specular path. There is no cap on transparent exceptions k, interior A count, support, height, diameter, area, number of gaps or reflection count.

Translate the core to [0,c]x[0,G], with integer G. The translation may change the displayed parity of an A point, but two original A ordinates still have even difference. No argument below requires that a translated horizontal coordinate remain even.

Dependencies: accepted A32 middle-row proof, accepted A35 protected direct core-to-midrow path, independently reviewed R35 opposite middle-row/actual far-wall return, accepted A37 actual zero-depth seam twist, and A38 actual reflected-spine four-level construction. A38 is a separately frozen candidate at the time of this authoring; this theorem must not be called accepted until its optical dependency and this join receive explicit independent acceptance.

## 1. All potentially dark endpoints are same-side seam midpoints

The open horizontal extent of each tooth has length1, so it contains no integer abscissa. An integer-coordinate actual interior point outside the STRICT core must therefore lie on a tooth mouth seam. Actual interiority excludes a boundary gap, an actual mouth corner and the far wall. In a height2 integer tooth, the only integer ordinate strictly between its band edges is its midpoint. Thus every actual A point is either strictly inside the core or is a tooth middle-row seam point.

Two strict-core points are directly visible. A strict-core point sees any strict seam point by a direct segment inside the core. Two points on opposite seams are directly visible across the open core. Distinct points on the same seam must belong to different same-side teeth, since each tooth contributes at most one integer midpoint at that seam.

Consequently it suffices to rule out darkness of two same-side midpoint seam marks. Reflect the horizontal coordinate if necessary, so these are on x=c. Write their relative ordinates as 0<s<t<G and define

    h=(t-s)/2, mu=(s+t)/2.

They are integers because the original actual A ordinates differ by an even integer. Same-side positive gaps and height2 imply h>1. Both selected teeth have width1 and actual depth D=0.

## 2. Four actual floor/ceiling charts

A38 uses the actual target images t,t+2G,-t,2G-t in the reflected core strip. Their physical central turning levels are

    L={h,mu,G-mu,G-h},                                    (1)

and their positive HALF separations from source s are respectively

    H_*={h,h+G,mu,G-mu}.                                  (2)

All four numbers in(2) are integers greater than1. The selected source and target tooth images have the same width1 and height2 in every chart. Their actual endpoints remain the original seam marks after folding by the physical core-end reflection map.

By A38, if any level in(1) is smooth actual wall or an opposite-tooth midpoint, a finite actual connection exists. Assume actual darkness. Since every opposite tooth has integer height2, every integer level inside such a tooth is its midpoint. Therefore every level in(1) must be an actual opposite MOUTH ENDPOINT.

## 3. A zero-depth far twist in each chart is physically available

Fix any one of the four charts. Its virtual midpoint lies over an actual opposite mouth endpoint. The adjacent opposite tooth opens on exactly one side there. The wall interval on the OTHER side has physical length at least1: all opposite-side tooth endpoints are integers and their same-side bands have positive gaps. Thus its first open unit interval is a smooth actual mirror.

In the reflected core strip, the corresponding virtual interval also has length1. It does not cross a global end line: the physical candidate level is an integer strictly between0 andG. If the tooth opens downward rather than upward, reflect the virtual y coordinate before applying the following argument.

Use the accepted A37 D=0 twist, with the chart's half-separation H_* and tooth width w=1. Its finite matching slope satisfies

    n(tau)=floor(tau+1/2),
    tau=(H_*+n(tau))/(1+c).

The two far-only endpoint choices have opposite central offsets m=tau-n(tau), with |m|<1/2. If c does NOT divide H_*, A37 proves m is nonzero: m=0 would force c*tau=H_* and integral tau. Choose the sign whose turning point lies on the adjacent smooth side of the mouth endpoint. Every selected far corner would require odd integral tau and is excluded. The ordinary arm is empty at its actual seam, and the far-only arm initially enters its actual selected tooth. All endpoint/corner guards are those proved in A37's seam supplement.

Fold this finite virtual path by the ACTUAL core-end map exactly as in A38. Its open core crossings have0<x<c and become ordinary smooth global floor/ceiling reflections. Its shifted turning point is less than1/2 from the candidate integer level, hence cannot meet a global end or a different tooth endpoint. Its selected copied teeth fold into the original actual selected teeth. Thus this is an actual S/T path, not an integer divisibility argument detached from optics.

Darkness consequently forces c to divide ALL FOUR numbers in(2). In particular

    c|h, c|mu, c|G,
    c|s, c|t.                                             (3)

Here c|G follows from h and h+G; then s=mu-h and t=mu+h. Divisibility is a necessary condition only. We next show it is incompatible with the wall budget.

## 4. Darkness forces at least five NONFLUSH teeth

There are at least THREE distinct levels in(1). Indeed h<G-h, and both mu and G-mu lie strictly between them: mu-h=s>0 and G-mu-h=G-t>0.

By(3), every one of these levels belongs to cZ. A single height2 tooth has endpoint difference2. For integer c>=3 it cannot have TWO distinct endpoints in cZ, since c does not divide2. Therefore at least THREE DIFFERENT opposite teeth are needed to make all distinct levels mouth endpoints.

Each of these three teeth is NONFLUSH: it touches neither the global floor nor ceiling. A floor-flush height2 tooth has endpoints0,2; neither is an eligible positive interior cZ level. A ceiling-flush tooth has endpointsG-2,G; because c|G and c does not divide2, neither is an eligible interior cZ level. Thus none of the required three blockers can be flush.

The two selected endpoint teeth are also nonflush. Their centers s,t belong to cZ by(3), as does G. A height2 tooth centered at s is flush only if s=1 or s=G-1, both incompatible with c>=3 and(3). The same holds for t. The selected pair and the three opposite blockers are distinct. Actual darkness therefore requires at least FIVE nonflush teeth.

## 5. Exact maximal-wall charge

For a two-sided comb with height2 teeth and G>2,

    W = 4 + 4*n_nonflush + 2*n_flush.                     (4)

Each nonflush attachment replaces an internal portion of a vertical core wall by its three exterior tooth edges and splits the remaining core wall into two pieces: a net increase of4 maximal straight walls. A floor- or ceiling-flush attachment extends the existing maximal horizontal core-end wall and adds its far vertical wall plus its other horizontal edge: a net increase of2. A tooth cannot be flush at both ends here, because the two separated selected height2 teeth force G>4.

Same-side positive gaps keep every counted vertical gap segment nonzero. Equal-coordinate far walls of distinct teeth remain disconnected. Opposite-side coincident band levels cannot merge exterior walls through the core INTERIOR. At the global floor or ceiling, the collinear extensions are already counted as a single core-end wall in the flush contribution. Thus(4) counts maximal straight walls, not elementary lattice edges or arbitrary collinear marks.

Five nonflush teeth give W>=4+4*5=24, contradicting W<=21. This excludes the assumed actual dark seam pair. Section1 exhausts all other actual A placements, completing the theorem in its exact class.

## Limits and remaining work

The proof handles arbitrary numbers of transparent points, heights and gaps by necessary geometry derived from actual darkness, with no enumeration or bounded ray failure. The condition c>=3 is essential to the stated counting step: for c=1 or2, opposite height2 endpoints can share the same residue class. Those narrow-core branches remain open here, as do wider/deeper teeth, general canonical45 disks and arbitrary real endpoints. No universal22-wall minimality or Independent acceptance of A38 and this complete join is still required.
