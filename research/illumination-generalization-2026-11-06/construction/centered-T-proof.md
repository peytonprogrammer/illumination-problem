# A cap-free illumination theorem for long-stem T rooms

New candidate for independent review. The filename retains the initial working name; the final statement does not require a centered stem. This is a positive unbounded-size subclass of the active objective, not the whole W<=21 theorem. No novelty claim is made.

## Statement

Let a,c,h>0, L<-a<a<R, and h>=3c/2. Put

P=([L,R]x[0,c]) union ([-a,a]x[c,c+h]).

Every two distinct interior points of P admit a finite ordinary specular billiard trajectory avoiding all eight genuine polygon corners. No rationality, coordinate, lattice-size, area, exception or reflection-count bound is assumed. Translating and reflecting the room preserves the statement.

More precisely, the construction below works for a cross-placement S=(s,y_s), T=(t,c+d), where 0<y_s<c, -a<t<a and 0<d<h, whenever either

    d>c-y_s, or 2h-d>2(c-y_s).

The first construction uses no horizontal-wall reflection. The second uses exactly one stem-roof reflection. Both allow an unbounded finite number of stem-side reflections. No artificial mirror is used.

## 1. Exhaustive point placement

The full base rectangle and the full stem-column rectangle [-a,a]x[0,c+h] are convex subsets of P. If the two marks share either rectangle, their direct segment works; a segment between interior marks remains in the room interior, including when one mark is on the open internal portal at height c.

Otherwise, after interchanging S,T, the source is in the base outside the stem column, and the target is strictly above c in the stem. Thus S,T have the cross-placement above. The source coordinate s may have either sign; no symmetry of [L,R] is used.

## 2. Genuine stem images

The horizontal folding map of the actual stem interval [-a,a] has period4a and is

    F(z)=a-abs(((z+a) modulo4a)-2a).

Its target images are exactly

    E_t={t+4ka, 2a-t+4ka : k in Z}.

These are the actual side-wall reflection images, not images of a half-room whose target sheet would have to be guessed. At every q in (-a,a), F(q)=q and its derivative is+1. A developed segment starting at such q folds into the actual stem. Odd multiples of a are precisely the developed images of its two genuine side walls.

Write D=c-y_s>0. For any developed target height c+v, v>0, and any X in E_t, the straight segment from (s,y_s) to (X,c+v) crosses y=c at

    q=(v*s+D*X)/(D+v).

Writing r=v/D and z0=-r*s, the open-portal condition is exactly

    abs(X-z0)<(1+r)*a.

Below y=c this segment joins two points of the convex base rectangle, since q lies in the actual stem interval, which is inside (L,R). There are no base-wall reflections and no base corners. Above the portal, fold only the horizontal coordinate into the stem. The folds agree with the identity near q, so there is one globally matched velocity across the portal.

## 3. Direct-height chart: d>D

Take v=d, so r>1. The two progressions E_t have alternating gaps 2(a-t) and 2(a+t), both positive and less than4a. A nearest image X to z0 has distance at most a+abs(t)<2a. Since (1+r)*a>2a, q lies strictly in (-a,a).

The upper developed height increases from c to c+d<c+h. Therefore it reaches neither the stem roof nor the lower portal again. Its finitely many side-wall contacts occur strictly between heights c and c+d, so none is a genuine corner. The horizontal fold ends at t. This is an actual S-to-T connection.

## 4. Reflected-roof chart: 2h-d>2D

Take v=2h-d, which lies strictly between h and2h, and r=v/D>2. The vertical fold about the actual roof maps the final height c+v to c+d. It has exactly one roof contact, at developed height c+h, and it never returns to height c after entry. It remains to choose X with an open portal and a roof contact away from the two genuine roof corners.

Set u=a-abs(t)>0. If t>=0, short-gap pairs in E_t have centers a+4ka and endpoints center +/-u. If t<0, they have centers 3a+4ka and the same half-gap u. Choose the center C nearest to z0; its distance from z0 is at most2a. Put

    X_1=C-u, X_2=C+u.

Both are genuine target images. Each satisfies abs(X_i-z0)<=2a+u<=3a<(1+r)*a. Hence both developed paths enter through the actual open portal, including possibly q=0, which is an ordinary interior point of P.

At the roof height the developed horizontal coordinate is

    B(X)=((v-h)*s+(D+h)*X)/(D+v).

A genuine roof corner is hit exactly when B(X) is an odd multiple of a. Put beta=(D+h)/(D+v). Since v>h, 0<beta<1. Therefore

    0<B(X_2)-B(X_1)=2*u*beta<2a.

Two distinct odd multiples of a are separated by at least2a. Consequently at least one of X_1,X_2 avoids all genuine roof corners. Choose that image. Contact at the roof center, if it occurs, is smooth and legal. Every other vertical-wall contact has physical height strictly between c and c+h, and the sole roof contact has |x|<a. The actual endpoint is T by the independent horizontal and vertical folding identities.

There are finitely many side-wall crossings because X_i, q and a are finite with a>0. Horizontal and vertical fold events do not coincide at a roof corner by the choice just made. These folds yield the ordinary reflection law at every actual contact. Thus the chosen trajectory is finite and avoids every genuine polygon corner.

## 5. Uniform geometric hypothesis covers every cross-placement

If d>D, section3 applies. Otherwise d<=D and

    2h-d>=3c-D>2D,

because h>=3c/2 and D=c-y_s<c. Thus section4 applies, with strict inequalities even at the geometric equality h=3c/2. Section1 exhausts every remaining placement. This proves the stated theorem if the formulas and lifting obligations survive independent review.

## Scope and required challenge

For canonical parameters this excludes all dark interior A pairs in this entire T8 subclass at arbitrary k. It does not prove all T rooms with shorter stems, all eight-wall polygons, other room families or the uncapped W<=21 goal. Existing all-real U8 and L6 theorems remain distinct dependencies; the present proof does not require them.

Review especially: the actual interval [-a,a] image set, asymmetric base inclusion, endpoint case split, nearest short-pair selection, strictness at h=3c/2, q=0, a target on the stem axis, the roof-corner test, simultaneous events and the fact that no base-side reflection or artificial axis reflection occurs. Prescribed exact controls test the two formulas, not a discovery search or a replacement for the quantified hand proof.
