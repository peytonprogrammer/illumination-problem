# Every real wide-middle offset corridor illuminates

New exact arbitrary-real optical proof; independent review pending. The finite rational exploration is supporting control only. The proof below has no arithmetic, size, k, direction or reflection-count bound.

## Statement

Let

    0<a,B<A, 0<b<c<C,
    P=([0,B]x[0,b]) union ([0,A]x[b,c]) union ([a,A]x[c,C]).

Every distinct interior pair in P has a finite ordinary specular connection avoiding every genuine polygon corner. For marks S=(xs,ys) strictly in the lower arm and T=(xt,yt) strictly in the upper arm, there is a connection with y strictly increasing throughout, reflecting only on vertical walls. In particular, the order a versus B is unrestricted; separated outer arms a>B are included.

Write F_L for the triangular-wave folding map into [0,L], with period2L. It is even, equals |z| on [-L,L], and satisfies F_L((2j+1)L+z)=L-|z| for |z|<L. At a fold the derivative changes sign, giving reflection on a vertical wall.

## 1. Reduce opposite-arm data to B>=W

Put W=A-a, Hs=b-ys>0, g=c-b>0, Ht=yt-c>0 and D=Hs+g+Ht. Source and target satisfy 0<xs<B, a<xt<A.

If B<W, rotate P by180 degrees and exchange the marks. The new lower arm has width W and the new upper arm width B. Their vertical distances are exchanged and g is unchanged. Thus it suffices to prove the result when B>=W. This is an isometry and reversal, preserving actual physical marks and all reflection laws.

## 2. Put a whole exit window inside one valid entrance window

Choose an integer k>=0 so large that, with K=(2k+1)A,

    (Hs*K+g*xs)/(2B*g) >=1.

Let n be a nearest integer to that expression (either tie choice works). Then n>=1. Set

    theta=(2nB-xs)/Hs,
    R=B*(Hs+g)/Hs.

Nearest-integer rounding gives

    |g*theta-K| <= B*g/Hs.

The slopes for which the lower portal lies strictly away from its reflex endpoint form

    I=((2nB-xs-B)/Hs, (2nB-xs+B)/Hs).

Since n>=1 and xs<B, I is entirely positive. The affine variable

    U(tau)=xs+(Hs+g)*tau-2nB

maps I onto (g*theta-R,g*theta+R). The exit portal window is

    K-W<U<K+W.

It is contained in that open image interval: the rounding bound and B>=W give

    |K-g*theta|+W <= B*g/Hs+W <= R.

Equality merely makes endpoints coincide; the OPEN exit window is still inside the OPEN entrance window. Therefore the nonempty open interval

    J=((2nB+K-xs-W)/(Hs+g),
       (2nB+K-xs+W)/(Hs+g))

is a subset of I. Every tau in J is positive and gives both strict portal guards

    |xs+Hs*tau-2nB|<B,
    |xs+(Hs+g)*tau-2nB-K|<W.

No rationality or density theorem was used.

## 3. Select an actual target image inside that window

Set Y=A-xt, so 0<Y<W. On J the affine coordinate

    Z(tau)=xs+D*tau-2nB-K

runs through an open interval of length

    2W*D/(Hs+g) > 2W.

The target images Y+2mW have spacing2W. Hence this open interval contains one of them strictly. For example, if Zlo is its lower endpoint, choose

    m=floor((Zlo-Y)/(2W))+1.

Then Zlo<Y+2mW<=Zlo+2W<Zhi. The slope

    tau=(2nB+K+Y+2mW-xs)/D

lies strictly in J and satisfies F_W(Z(tau))=Y. This is an explicit finite choice of one global direction and the same actual target.

## 4. The actual three-piece path and velocity matching

For ys<=y<=yt define x(y) by

    lower arm, ys<=y<=b:
        x(y)=F_B(xs+tau*(y-ys));

    middle band, b<=y<=c:
        x(y)=F_A(z+tau*(y-b)),
        z=xs+Hs*tau-2nB;

    upper arm, c<=y<=yt:
        x(y)=A-F_W(w+tau*(y-c)),
        w=xs+(Hs+g)*tau-2nB-K.

The guards give |z|<B and |w|<W. At y=b the lower fold reduces to |z|, and so does the middle fold because B<A. In a neighborhood of the portal both formulas are the SAME absolute-value expression. Their physical positions and velocities therefore match, including z=0: x=0 at that portal is a smooth actual vertical wall, and the matching absolute values describe its single legal reflection.

At y=c the middle argument is K+w with K an odd multiple of A. Thus the middle fold is A-|w| and agrees locally with the upper formula. Positions and velocities again match, including w=0: x=A at that portal is a smooth actual vertical wall. The only forbidden endpoint of the lower portal is (B,b), excluded by |z|<B. The only forbidden endpoint of the upper portal is (a,c), excluded by |w|<W.

The path starts at S. Its final x is A-F_W(Z(tau))=A-Y=xt, so it ends at the specified physical T. Its y coordinate is the strictly increasing path parameter; hence T is first reached at its specified height.

Every horizontal velocity is +tau or -tau, and every vertical velocity is1. Every fold is consequently an ordinary specular reflection in a vertical wall. Lower contacts occur on x=0 or x=B below b; middle contacts occur on x=0 or x=A between b and c; upper contacts occur on x=a or x=A above c. All are genuine P mirrors. No horizontal wall is touched. The other genuine corners (0,0),(B,0),(A,b),(A,C),(a,C),(0,c) are avoided by strict endpoint heights and the strict portal guards. Each finite coordinate interval crosses only finitely many fold lines, so the path has finitely many reflections.

This completes the opposite-arm arbitrary-real proof, including the nearest-integer equality and the two smooth-wall portal equality cases.

## 5. A needed boundary-endpoint L supplement

The accepted vertical-only L formula also permits a source on its smooth horizontal base when that point is interior to the actual larger room. Explicitly take the standard L

    Q=([0,L]x[0,h]) union ([0,l]x[h,H]), 0<l<L, 0<h<H,

source (x,0) with 0<x<L and target (t,y) with 0<t<l, h<y<H. If x<=l the direct segment works. Otherwise repeat the accepted formula with source height0: r=(y-h)/h>0, choose a nonzero nearest target-image displacement delta<=l from -r*x, and obtain strict portal q=delta/(1+r) in(0,l). The same lower fold and upper width-l fold give one globally matched direction and the actual target. The physical y increases strictly, so the base is contacted only at the initial mark; all later wall contacts are vertical and smooth. The former proof's strict source-height lower bound is used only to make the starting point interior to Q, not for its direction, portal or corner inequalities. Thus it can be dropped here when the starting point is an interior mark of the actual P. No actual boundary endpoint is admitted.

## 6. All other interior pair placements

The lower-plus-middle subroom

    Qlow=([0,B]x[0,b]) union ([0,A]x[b,c])

is an L. All of its vertical walls are actual P walls. Its artificial top horizontal cut contains the newly actual reflex corner (a,c), smooth on that cut, so a VERTICAL-only L path avoids both. Likewise

    Qup=([0,A]x[b,c]) union ([a,A]x[c,C])

has only an artificial bottom horizontal cut, containing (B,b); a vertical-only L path avoids it and that corner.

If the two marks belong to Qlow and are strictly below c, apply that L theorem. If they belong to Qup and are strictly above b, apply that L theorem. Marks on internal y=b and y=c seams are interior to P only in the corresponding open arm interval. A lower-arm mark and a seam mark on y=c use the base-endpoint supplement after reflecting Qlow vertically and reversing the path. An upper-arm mark and a seam mark on y=b use the supplement in Qup, with a horizontal reflection if needed to put its upper arm on the left. If both marks have heights in [b,c], their direct segment in the middle rectangle stays in the interior of P; the endpoint seam conditions exclude actual boundary points. The only remaining placement is one strictly lower-arm and one strictly upper-arm mark, proved in Sections1--4. This exhausts all interior pairs without an unstated endpoint-interiority assumption.

## 7. Verification and limits

The rational one-pass discovery code found paths in4455 prescribed center/quarter-position cases (39588 exact target candidates checked). The second input tranche found paths in9215 additional deterministic hostile rational inputs (239965 target candidates);785 inputs were skipped by a declared complexity cap. Both tranches finished under the SAME original840-second deadline. Neither census proves the arbitrary-real result. Its proof is the interval containment and single folded path above. The separate fixed constructor/wall checker passes160 exact checks and36 actual reflections across four prescribed fixtures, including simultaneous smooth-wall portal hits and nearest-integer/target-image boundary equalities. Independent hand review remains required.

This covers case4 of eight-wall-frontier.md, subject to independent review of both packets. It does not cover the staircase class, diagonal-wall rooms, larger W, arbitrary blockers or the main uncapped W<=21 theorem. No universal minimum or novelty claim.
