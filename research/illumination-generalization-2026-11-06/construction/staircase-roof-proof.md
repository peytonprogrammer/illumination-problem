# Staircase illumination with one outer roof reflection

New arbitrary-real optical theorem for independent review. This adds a different sufficient geometric regime to staircase-window-proof.md; it is not the whole staircase or W<=21 theorem.

## 1. Statement and precise pair condition

Let 0<a<b<A, 0<c<d<H, and

P=([0,A]x[0,c]) union([0,b]x[c,d]) union([0,a]x[d,H]).

Every distinct interior pair illuminates if H>=3d OR A>=3b. No k, scale, arithmetic or reflection-count bound is imposed.

For the nontrivial cross-placement

    S=(xs,ys), b<=xs<A, 0<ys<c,
    T=(xt,yt), 0<xt<a, d<=yt<H,

write Hs=c-ys, g=d-c, h=H-d, Ht=yt-d, T0=Hs+g and v=2h-Ht. The construction applies whenever

    v>=2T0.                                    (1)

The lower and middle pieces have increasing physical height. The upper piece reflects once at its genuine horizontal roof; all other reflections are vertical. Actual endpoints and all seam equalities are retained.

## 2. A partial exit window always has length greater than a

Set n=1 and theta=(2A-xs)/Hs. Let K be a nearest nonnegative multiple of2b to g*theta. Put

    R=b*(Hs+g)/Hs, delta=abs(K-g*theta).

Then delta<=b and R>b>a. The source-admissible slope interval

    I=((2A-xs-b)/Hs,(2A-xs+b)/Hs)

is strictly positive. Under U=xs+T0*tau-2A it maps to (g*theta-R,g*theta+R). Intersect that open interval with the desired upper-portal window (K-a,K+a), obtaining (Ulo,Uhi).

Because K lies strictly inside the source image interval and its radius R is greater than a, at most one endpoint of the exit window can be clipped. Thus its overlap length ell is either2a or R+a-delta. In particular

    ell>=min(2a,R+a-b)>a.                       (2)

The preimage J of this overlap under U is a nonempty positive open slope interval. Every tau in J has BOTH strict actual portal guards

    abs(z)<b, z=xs+Hs*tau-2A;
    abs(w)<a, w=xs+T0*tau-2A-K.

Unlike the earlier whole-window theorem, this step needs no relative-width or source-depth inequality.

## 3. Two genuine target images in the enlarged final window

Set D=T0+v. The coordinate Z=xs+D*tau-2A-K maps J to an open interval (Zlo,Zhi) of length

    ell*D/T0 >= 3ell > 3a,

by(1) and(2). The actual target images of the width-a interval[0,a] are E={+xt+2ma,-xt+2ma}.

Put u=min(xt,a-xt), so 0<u<=a/2. The short-gap pairs in E have centers2ma if xt<=a/2, and a+2ma if xt>a/2. Choose such a center nearest the midpoint of (Zlo,Zhi). Its distance from that midpoint is at most a; both points Y1=center-u and Y2=center+u are therefore strictly inside (Zlo,Zhi), since its half-length is greater than3a/2. They are distinct genuine target images, with gap2u<=a.

For each candidate put

    tau_i=(2A+K+Y_i-xs)/D.

Both lie strictly in J and hence satisfy both open-portal guards. At the developed roof height d+h their upper horizontal coordinate is

    B(Y)=xs+(T0+h)*tau(Y)-2A-K.

Its slope with respect to Y is beta=(T0+h)/(T0+v), strictly between0 and1 because v=2h-Ht>h. A genuine upper roof corner is hit exactly when B(Y) is an integer multiple of a: both x=0 and x=a are genuine corners in this room. But

    0<B(Y2)-B(Y1)=2u*beta<a.

Two distinct multiples of a are separated by at least a. Therefore at least one candidate avoids BOTH genuine roof corners. Select that candidate. This is a finite exact selection, not a direction search.

## 4. Actual path and all corners

Use developed height eta as the path parameter. From ys through c,d use

    x=F_A(xs+tau*(eta-ys)), y=eta,     ys<=eta<=c;
    x=F_b(z+tau*(eta-c)), y=eta,       c<=eta<=d.

For d<=eta<=d+v use

    x=F_a(w+tau*(eta-d)),
    y=d+F_h(eta-d).

Here F_l is the even triangular-wave map into[0,l] of period2l. Since h<v<=2h, there is exactly one roof reflection. At eta=d+v, y=d+Ht=yt and x=F_a(Y)=xt, giving the actual target. Ht=0 is permitted: the upper path first returns to the portal at its terminal target. It does not cross a lower portal earlier. If the actual target is encountered earlier on a repeated segment, truncate there; such a prefix is already a legal connection.

At c the lower and middle expressions locally agree because their arguments differ by the even multiple2A and |z|<b<A. At d the middle and upper expressions locally agree because K is an EVEN multiple of b and |w|<a<b. The equalities z=0 or w=0 are smooth genuine vertical-wall contacts at x=0; the same absolute-value expression on both sides gives their one ordinary reflection. The actual reflex corners (b,c) and(a,d) are excluded by the strict guards.

In each band every other x fold is an ordinary reflection on an actual vertical wall. The sole y fold is on the actual roof, with horizontal coordinate strictly between0 and a by Section3. It cannot coincide with a vertical reflection. All lower and middle genuine corners are excluded as in the window proof by strict endpoint heights and portal guards. Upper physical height remains>d except at the initial and possible terminal portal; the roof endpoints are excluded explicitly. Thus no path segment or contact uses an artificial mirror or a genuine corner. Finite coordinates and positive widths give finitely many folds. The vertical velocity is1 before the roof and-1 afterward; horizontal velocity is always+/-tau, so every contact satisfies ordinary specular reflection.

## 5. Whole-room and transpose corollaries

If H>=3d, then h=H-d>=2d. Since T0=d-ys<d and v>h, one has v>2T0 for EVERY cross-placement, including Ht=0. Sections2--4 apply.

Other placements are exactly those handled by the two orientation-avoiding L subrooms in staircase-window-proof.md Section6. Both marks strictly below d use Qlow and vertical-only reflections; both strictly left of b use Qup and horizontal-only reflections. If neither condition holds, they are the cross-placement above. All seam equalities remain in that explicit cross-placement. Hence the H>=3d statement covers every distinct interior pair.

Transposition changes the staircase's width triple to H,d,c and height triple to a,b,A. The same theorem gives A>=3b. Transposition is an isometry and preserves actual endpoints and reflection laws.

## 6. Quantified frontier

Combined with the earlier independently accepted staircase-window theorem, all staircase pairs are covered whenever ANY of these six sufficient inequalities holds:

    b²>=aA; b(d-c)>=ac; d²>=cH;
    d(b-a)>=ca; H>=3d; A>=3b.

If all six fail, this theorem does not assert illumination or darkness. In particular the remaining normalized geometry has A<3b and H<3d as well as b²<aA and d²<cH; these are restrictions on the unresolved class, not a denominator, k, endpoint-clearance or reflection bound. The full W<=21 objective remains open. No novelty claim.
