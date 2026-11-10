# Cap-free staircase illumination by nested windows

New arbitrary-real optical theorem for independent review. The whole uncapped W<=21 objective remains open. This proof adapts the peer's wide-middle window idea, but independently proves the different inequalities needed when BOTH passages narrow.

## 1. Room, quantified subclass, and actual endpoints

Let 0<a<b<A and 0<c<d<H. Put g=d-c and

P=([0,A]x[0,c]) union([0,b]x[c,d]) union([0,a]x[d,H]).

Every distinct interior pair in P illuminates whenever at least one of the following holds:

    b²>=a*A; or b*(d-c)>=a*c;
    d²>=c*H; or d*(b-a)>=c*a.

No bound on k, lattice size, denominator, area or reflections is imposed. All dimensions and actual endpoints may be arbitrary real numbers. The last two alternatives are the first two after transposing x,y.

A stronger pairwise sufficient statement underlies the proof. For

    S=(xs,ys), b<=xs<A, 0<ys<c,
    T=(xt,yt), 0<xt<a, d<=yt<H,

set Hs=c-ys>0, Ht=yt-d>=0, D=Hs+g+Ht, rho=g/Hs. There is a finite y-increasing, vertical-reflection-only actual connection if

    rho<=(b-a)/(A-b) OR rho>=a/b.                 (1)

The equality endpoints xs=b and yt=d are deliberately included: they can be actual interior marks. Other pairs are reduced to accepted L connections in Section6.

## 2. Exact two-window requirement

Use the usual even triangular-wave F_l into[0,l], of period2l. Choose integers n>=1 and k>=0; put K=2kb, theta=(2nA-xs)/Hs and R=b*(Hs+g)/Hs. For slopes tau in

    I=((2nA-xs-b)/Hs,(2nA-xs+b)/Hs),

the first portal is represented by z=xs+Hs*tau-2nA, with |z|<b. Since xs<A and b<A, I is entirely positive.

Under U(tau)=xs+(Hs+g)*tau-2nA, the image of I is

    (g*theta-R,g*theta+R).

Thus the WHOLE desired second-portal window (K-a,K+a) is inside that open image whenever

    |K-g*theta|+a<=R.                            (2)

Equality in(2) is harmless: endpoints can coincide, but the OPEN smaller window is still contained. Its slope preimage is

    J=((2nA+K-xs-a)/(Hs+g),
       (2nA+K-xs+a)/(Hs+g)) subset I.

Both portal guards hold strictly on J: |z|<b and |w|<a, where

    w=xs+(Hs+g)*tau-2nA-K.

## 3. Two finite rounding choices prove(2)

If rho<=(b-a)/(A-b), choose k so large that

    (Hs*K+g*xs)/(2A*g)>=1,

and take n to be a nearest integer to this expression. Then n>=1 and

    |g*theta-K|<=A*g/Hs=A*rho.

Consequently

    |g*theta-K|+a<=A*rho+a<=b+b*rho=R.

An explicit permissible choice is k=1+ceil(A*g/(b*Hs)).

If rho>=a/b, take n=1 and take K to be a nearest nonnegative multiple of2b to g*theta. Here theta>0, so this nearest multiple is indeed nonnegative. Its distance is at most b, hence

    |g*theta-K|+a<=b+a<=b+b*rho=R.

Either tie choice works. This proves(2) in both regimes of(1), without rationality or a density argument.

## 4. Hit the actual target, including the seam Ht=0

On J the coordinate

    Z(tau)=xs+D*tau-2nA-K

ranges over an open interval (Zlo,Zhi) of length

    2a*D/(Hs+g)>=2a.

The images of the actual xt under F_a are {+xt+2ma,-xt+2ma}. Their alternating gaps2xt and2(a-xt) are BOTH strictly less than2a because0<xt<a. Therefore the open interval contains an actual image strictly, even at equality Ht=0.

Explicitly for each sign epsilon choose

    m_epsilon=floor((Zlo-epsilon*xt)/(2a))+1,
    Y_epsilon=epsilon*xt+2m_epsilon*a,

and take Y to be the smaller of the two. Then Zlo<Y<Zlo+2a<=Zhi: if one progression's next point is Zlo+2a, the other has a point strictly earlier. The slope

    tau=(2nA+K+Y-xs)/D

lies strictly in J and has F_a(Z(tau))=xt.

## 5. One actual physical path

For ys<=y<=yt define

    x(y)=F_A(xs+tau*(y-ys)),              ys<=y<=c;
    x(y)=F_b(z+tau*(y-c)),                c<=y<=d;
    x(y)=F_a(w+tau*(y-d)),                d<=y<=yt.

At c, the first argument is2nA+z with |z|<b<A, so both neighboring formulas are locally the SAME |z+tau*(y-c)|. At d, the middle argument is K+w, with K an EVEN multiple of b and |w|<a<b; both neighboring formulas are locally the SAME |w+tau*(y-d)|. Thus positions and velocities match exactly across both portals.

The equalities z=0 and w=0 mean a smooth contact with the actual common vertical wall x=0 at the corresponding height. The matching absolute values describe one ordinary vertical reflection, not a splice or a corner contact. The forbidden first reflex corner (b,c) is excluded by |z|<b; the second (a,d) by |w|<a. Other genuine corners at the two steps are excluded by these same strict guards and the strict source/target inequalities. For Ht=0 the final upper piece has zero length and its endpoint is the specified actual interior T on the portal, with0<xt<a; no reflection is asserted there.

Every remaining fold is on a genuine vertical wall: x=0 orA belowc, x=0 orb between c,d, and x=0 ora above d. The height increases strictly, so no horizontal wall is contacted. The initial point is S and the final point is T by Section4. Finite coordinates and positive widths imply finitely many fold crossings. Hence this is one finite ordinary corner-free S-to-T connection.

## 6. Whole-room conditions and exhaustive placement

If b²>=aA, then (b-a)/(A-b)>=a/b. The two regimes(1) cover EVERY positive rho. Alternatively b*g>=a*c implies rho=g/Hs>g/c>=a/b for every possible lower-arm source because Hs<c. Thus either of the first two geometric conditions proves every cross-placement in Section1.

The remaining placements use accepted orientation-avoiding L paths. The subroom

    Qlow=([0,A]x[0,c]) union([0,b]x[c,d])

has all vertical walls genuine P walls. The only artificial horizontal cut is its top y=d; it contains the possible actual P reflex corner(a,d), which a vertical-only L path avoids. Thus any two actual marks with heights STRICTLY below d connect by that L theorem, including an internal first-portal mark.

The subroom

    Qup=([0,b]x[0,d]) union([0,a]x[d,H])

has all horizontal walls genuine P walls. Its artificial right vertical cut contains the actual corner(b,c), which a horizontal-only L path avoids. Any two actual marks with x STRICTLY less than b connect by that L theorem, including an internal second-portal mark.

If neither subroom condition covers the pair, one mark has y>=d and therefore x<a<b. The other must have x>=b and therefore y<c. These are exactly the cross-placements already proved, including the equality seams. All L endpoints used are strictly interior to their respective L; the seam cases outside them are handled by the explicit formula, not an unstated extension.

Finally swapping coordinates turns the staircase parameters into outer width H, middle width d, inner width c, lower height a, next height b, top height A. Thus the same proof gives the two transposed sufficient alternatives d²>=cH and d*(b-a)>=ca. Transpose is a Euclidean isometry and preserves actual endpoints and specular paths.

## Limits

This is a genuine all-interior-pair theorem for an unbounded metric subclass of eight-wall staircases, not all staircases. In particular, when ALL FOUR inequalities in Section1 fail, this proof gives only the pairwise regime(1) and its transpose; it does not cover every endpoint. The thin-middle geometry and the complete W<=21 objective remain open. Exact prescribed controls supplement the hand proof; the earlier16-fixture test did not establish this theorem.
