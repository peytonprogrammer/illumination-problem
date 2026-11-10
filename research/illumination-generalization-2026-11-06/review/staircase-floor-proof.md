# A source-floor reflection closes another real staircase subclass

New exact optical extension; independent review pending. The earlier window theorem and peer roof construction are separate inputs/scopes. No k, arithmetic, scale or reflection-count bound is imposed.

## Statement

Let 0<a<b<A and 0<c<d<H and

    P=([0,A]x[0,c]) union ([0,b]x[c,d]) union ([0,a]x[d,H]).

Every distinct actual interior pair illuminates if

    (A-b)(d-c) <= c(b-a),                      (F)

or its transposed counterpart

    (H-d)(b-a) <= a(d-c).                      (Ft)

These conditions add valid geometries not covered by the four conditions in staircase-window-proof.md. For instance (A,b,a;c,d,H)=(6,4,3;3,4,6) satisfies F and Ft while all four earlier conditions fail. This is not a theorem for all staircases or all W<=21 rooms.

## 1. Opposite outer marks and one reflected source

It suffices first to connect

    S=(xs,ys), b<=xs<A, 0<ys<c,
    T=(xt,yt), 0<xt<a, d<yt<H.

Put g=d-c, Hs'=c+ys, Ht=yt-d>0 and D=Hs'+g+Ht. Reflect the source in the genuine floor to (xs,-ys). We construct an upward path from that unfolded source and fold its lower height to |y|. Its only new horizontal contact is at y=0, whose two actual corners must be avoided explicitly.

The already independently accepted nested-window rounding construction applies with Hs' replacing Hs. Condition F gives

    rho'=g/(c+ys) < g/c <= (b-a)/(A-b).

Choose a sufficiently large even multiple K=2kb, and n nearest to

    (Hs'*K+g*xs)/(2Ag),

so n>=1. Exactly as in the accepted window proof, the bound

    |g*(2nA-xs)/Hs'-K| <= A*g/Hs'

puts the whole open second-portal window (K-a,K+a) inside the first admissible image interval of radius b(1+g/Hs'). Thus

    J=((2nA+K-xs-a)/(Hs'+g),
       (2nA+K-xs+a)/(Hs'+g))

lies wholly inside the positive source window where

    |z|<b, z=xs+Hs'*tau-2nA.

For every tau in J one also has |w|<a for

    w=xs+(Hs'+g)*tau-2nA-K.

The source positivity proof remains valid because xs<A and b<A. The first portal guard is radius b, not A. No physical source or target is moved by the eventual fold.

## 2. Two actual target images avoid the actual floor corners

On J the target coordinate Z=xs+D*tau-2nA-K ranges over an open interval of length

    2a*D/(Hs'+g) > 2a.

The actual target images are +xt+2ma and -xt+2ma. Any open interval longer than2a contains at least two consecutive distinct such images Y1<Y2. Their gap satisfies0<Y2-Y1<2a. Let their corresponding slopes be tau1,tau2 in J.

The unfolded horizontal coordinate of the floor contact is

    L(tau)=xs+ys*tau.

A genuine floor corner is hit exactly when L(tau) belongs to A*Z. But

    0<L(tau2)-L(tau1)
      =ys*(Y2-Y1)/D
      <2a*ys/D
      <a<A,

because D>c+ys>2ys. Therefore BOTH phases cannot belong to A*Z. Choose a candidate whose phase does not. This removes both possible floor corners, not merely the same one in two copies. Nearest-integer and window equalities do not affect this strict argument. The two-image choice is essential; a single selected target image can hit a true floor corner.

One can generate the two images by taking the next point in the union of the two progressions strictly above Zlo, then the next strictly above that point. Both lie strictly below Zhi because Zhi-Zlo>2a. Invert Z for each slope and choose the first floor-noncorner candidate. These are finite exact operations on real inputs.

## 3. One actual path with matched velocities

Use an unfolded vertical parameter q from -ys to yt. For -ys<=q<=c put

    x(q)=F_A(xs+tau*(q+ys)), y(q)=|q|.

For c<=q<=d use

    x(q)=F_b(z+tau*(q-c)), y(q)=q;

and for d<=q<=yt use

    x(q)=F_a(w+tau*(q-d)), y(q)=q.

Here F_l is the usual even triangular-wave fold. The initial point is exactly S at q=-ys. Before q=0 the actual height decreases from ys to0; then it rises to c. All those points stay in the actual bottom rectangle because ys<c. Every vertical contact there is on x=0 or x=A at height strictly below c. At q=0 the physical y velocity changes from -1 to+1 and x velocity is unchanged: the ordinary reflection in the genuine floor. Section2 guarantees its x lies strictly in(0,A), so the contact is smooth.

At c the two formulas agree locally as the same |z+tau*(q-c)| because the first argument is an even multiple2nA plus z and |z|<b<A. At d the formulas agree locally as |w+tau*(q-d)| because K is an even multiple2b and |w|<a<b. Thus a single global slope matches actual positions and velocities at both interfaces, including z=0 or w=0: those are single ordinary contacts on the common smooth vertical wall x=0. The actual reflex corners (b,c) and (a,d), and the other step endpoint corners, are strictly avoided.

The final x is F_a(Y)=xt and final height yt, so the path ends at the specified physical T. Since yt>d>c>ys, the target cannot be visited on the initial downward excursion; after the floor reflection height increases strictly. The path may revisit its source, which is allowed and does not change target arrival. All other reflections are genuine vertical mirrors. The roof H and other horizontal ledges are never contacted, and finite coordinates/positive widths give finitely many folds.

## 4. Seam target and all remaining pair placements

The same orientation-avoiding Qlow/Qup subrooms and exhaustive placement argument as the accepted staircase-window theorem cover all pairs except the outer placements in Section1 and the possible seam yt=d. Their endpoints are strictly interior to those L subrooms, so no endpoint extension is silently assumed.

For T=(xt,d),0<xt<a, the vertical-only L construction in

    Qlow=([0,A]x[0,c]) union ([0,b]x[c,d])

extends exactly to that target on its smooth narrow-arm roof. This follows directly from the accepted formula: if xs<=b, use the direct segment inside the vertical column; otherwise set r=(d-c)/(c-ys)>0 and choose a nonzero nearest target-image displacement delta<=b, producing strict portal delta/(1+r) in(0,b). All vertical contacts in the upper arm have heights strictly between c and d. The only roof contact is the endpoint T, an interior point of the ACTUAL P since xt<a. No continuity-limit argument or boundary-mirror reflection is needed. The actual reflex corner(a,d), smooth on the artificial Qlow roof, is not contacted by this vertical-only path; its endpoint is distinct from it. This proves the seam case without needing two images in an interval of length exactly2a.

The equality source xs=b is interior to the actual lower rectangle and is permitted by the reflected-source window proof. The other placement equalities are covered by Qlow/Qup as in the accepted theorem. Hence F proves every distinct interior pair.

Transposition sends parameters (A,b,a;c,d,H) to (H,d,c;a,b,A) and carries F to Ft exactly. It is a Euclidean isometry, giving the second whole-room alternative.

## 5. Scope and controls

The new example (6,4,3;3,4,6) lies outside all four accepted earlier staircase conditions and outside H>=3d or A>=3b. Exact prescribed controls check both ordinary rounded windows and a deliberately admissible window where the first target candidate hits an actual floor corner and must be discarded. They are supporting arithmetic verification, not the arbitrary-real proof.

The valid room (10,4,3;3,4,10) fails all four earlier conditions, F/Ft, and H>=3d/A>=3b. This identifies a remaining METRIC geometry, not a dark pair or an assertion that no other mechanism covers it. The full staircase and main W<=21 goal remain open.
