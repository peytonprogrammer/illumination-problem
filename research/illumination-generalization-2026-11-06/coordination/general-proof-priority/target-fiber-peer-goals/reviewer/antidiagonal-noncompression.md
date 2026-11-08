# Complementary original-direction exclusion, with the cone guard

HAND supplement to noncompressible-connection.md. It uses only the ALREADY ACCEPTED four controlled foliations on the existing odd-d family. No new direction, room, ray discovery or numerical check.

## Claim and scope

For every odd d>=3, normalized P=[0,2d+1]x[0,d] union [0,d]x[d,2d+1], p=(2d-1,1), q=(1,2d-1), NO regular ORIGINAL antidiagonal connection p->gq can be compressed into one-copy closure by ANY global Sigma-preserving affine map. In the horizontal or vertical original directions there is no connection to any original target lift at all.

Combined with noncompressible-connection.md, this implies for d=3 modulo4 that ANY successful inverse-affine seed connection must have an original direction OUTSIDE the axes and both diagonals. This is a necessary condition on the ORIGINAL actual path, in addition to the accepted restriction on where F sends controlled directions.

It does NOT exclude arbitrary original directions, prove the existential target-fiber gate false, or establish darkness. The native statement is obtained by dilation by 2; all period contents are unchanged by that conjugacy.

## 1. Convert the original antidiagonal to the already analyzed diagonal

Apply the genuine original copy reflection Rx BEFORE any prospective affine compression. It maps the source to

p'=Rxp=(-2d+1,1),

and maps the four ORIGINAL target lifts bijectively to Gq, since RxG=G. It maps original antidiagonal trajectories to diagonal trajectories of velocity v=(1,1), with either sign. If F compressed the original path, F'=F Rx would compress its Rx image to the same seed. This is an exact global conjugacy; it is not a substitution of G F(q) for F(Gq).

We therefore study the actual diagonal flow through p'.

## 2. Its critical boundary circle is explicit

Take the accepted cylinder-2 boundary r=2, starting at (d,d-2). Its period as a circle on the underlying translation surface is T=6d+2. The relevant accepted event representatives are

s=0: (d,d-2),
s=2: (d+2,-d),
s=d+1: (-2d-1,-1),
s=3d+3: (1,-2d-1),
s=4d+2: (-d,-d-2),
s=6d+2: (d,d-2).

All representatives are AFTER the corresponding boundary translation. Along each straight portion the signed coordinate difference x-y is one of

2, 2d+2, -2d.

At time s=2d+2 the left-to-upper passage hits the genuine cone (-d,d). There is exactly one cone occurrence in this period, as independently accepted in the complete-diagonal review. A regular optical trajectory cannot cross it. The underlying closed-circle parametrization is used ONLY to overapproximate possible endpoint times and to enforce this exclusion; it does not authorize singular continuation.

On the portion from s=d+1 to s=3d+3, the point p'=(-2d+1,1) occurs at

s_p=d+3,

and ORIGINAL Rxq=(-1,2d-1) occurs at

s_q=3d+1.

The cone lies strictly between these times, since d+3<2d+2<3d+1 for d>=3.

No OTHER original target lift is on this critical circle. They are physical interior points, with unique signed representatives. Their x-y values are

q: -2d+2,
Jq: 2d-2,
Ryq: 2d.

For d>=3 none belongs to {2,2d+2,-2d}. At actual polygon boundary translations there is no alternate representative for these strictly interior marks. Thus this coordinate-difference exclusion suffices; there is no hidden choice of target sheet.

## 3. Every permitted time has excessive period content

The only possible target is Rxq, and all signed connecting times on the underlying boundary circle satisfy

tau=2d-2+n(6d+2), n integral.

Every positive member (n>=0) crosses the true cone on its way from phase s_p to phase s_q, so it is NOT regular. A negative member has

tau<=-(4d+4), hence |tau|/2>=2d+2.

Any additional regular corner contacts can only remove possibilities; they cannot create a shorter legal connection. No completeness assertion about a singular graph is used.

The exact period lattice is 2Z². Therefore any regular connection here has developed holonomy tau(1,1), with unimodular-invariant period content m=|tau|/2>=2d+2. Under EVERY global affine map its image vector is 2m times a primitive integer vector. A seed in closure of any copy of this room has coordinate displacements at most 2d+1, so necessarily m<=d. This is incompatible with m>=2d+2.

This contradiction proves the claimed full-group noncompression for original antidiagonal connections, independently of the affine foliation-stabilizer classification. Smooth-wall seeds satisfy the same closed coordinate bounds. The finer nominated tiling need not be preserved.

## 4. Original axis directions cannot attain the target fiber

In the signed-cross model, the horizontal flow through p has fixed y=1 and stays in the horizontal full-width cylinder with -d<y<d. Every gq has |y|=2d-1>d; no horizontal connection reaches it.

The vertical flow through p stays in the right-arm vertical cylinder, represented by fixed x=2d-1 with d<x<2d+1. Every gq has |x|=1<d and belongs to the other vertical cylinder; no vertical connection reaches it. Physical reflections correspond exactly to these translations. Corner cuts only remove trajectories, so they cannot repair either lack of access.

## What has and has not been ruled out

For d=3 modulo4, the original diagonal family is excluded by the preceding full-group theorem; the antidiagonal family is excluded here; axis directions never connect. Thus selecting ANY original path in the four controlled directions cannot prove the affine gate for these pairs, even if the FULL affine group is allowed to compress that path afterward.

This is stronger than showing that four foliation stabilizers fail as a group: it constrains the original inverse-image direction of any hypothetical successful seed. It still leaves all other original directions unrestricted. The known one-left path has slope -(d-1)/d, which is outside these four directions and therefore is not contradicted. Whether that path or another can be compressed is OPEN. Full native L coverage and r<=8 remain OPEN.
