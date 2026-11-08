# Exact compatible diagonal phases on the declared odd-d control family

HAND positive affine-seed lemma for the author's EXISTING symbolic family, not a new room or direction search. The direction is the author's already chosen diagonal (1,1). No numerical orbit traversal, ray search, engine or discovery clock is used.

## Result and exact scope

Let d>=3 be odd, A=2d+1. Start with the normalized L

P0=[0,A]x[0,d] union [0,d]x[d,A],

then dilate all coordinates by 2, as in the author's native family. The actual native marks are S=(4d-2,2), T=(2,4d-2). Put g0=gcd(d-1,4) and

k0=(4d+1)(3d+1)/g0.

There is a genuine global affine boundary-fixing diagonal multitwist F with derivative

DF=[[1+k0,-k0],[k0,1-k0]].

For EVERY d=1 modulo 4 (hence d>=5), F and the ORIGINAL target lift Ryq give a corner-free straight seed in ONE identified polygon copy. In normalized signed coordinates,

F(p)=((d-3)/2,-(3d-1)/2),
F(Ryq)=Ryq=(1,-2d+1).

Both points lie in the same open lower-arm rectangle (0,d)x(-A,-d) of the signed cross model, so their segment avoids every physical corner. Scaling by 2 gives actual image coordinates (d-3,1-3d) and (2,2-4d). Inverse transport restores the exact original p and Ryq, giving an actual S-to-T ray.

For d=3 modulo 4, every power of THIS multitwist fails all four target choices for the nominated p. This is a limitation of this map/power family, not a full affine-group obstruction. All native L pairs and the broad r<=8 goal remain unresolved.

## 1. Actual signed cross model

Place the four reflected copies in the four signed quadrants. After gluing the physical x=0 and y=0 walls, their union is the cross

Q=([-A,A]x[-d,d]) union ([-d,d]x[-A,A]).

The remaining actual identifications are translations: x=A with x=-A in the horizontal arm; y=A with y=-A in the vertical arm; x=d with x=-d separately in the upper and lower arms; and y=d with y=-d separately in the left and right arms. The corresponding translations are 2A or 2d. Quadrant signs record the actual original copy labels. These are not additional mirrors inside P0.

Use diagonal flow velocity v=(1,1) on the underlying translation surface. Regular convex corner marks may lie on such a closed orbit; that does not cut an underlying cylinder. These flow segments are used to define an affine map, not offered as legal optical trajectories. The final inverse image of a Sigma-free seed, separately below, is the optical path.

## 2. First exact diagonal cylinder

For 0<delta<2 start at (d+delta,-d), after the right-arm lower-edge identification. Flow along v. The following table gives cumulative time and the representative AFTER each actual boundary translation:

| Cumulative time | Signed representative |
|---|---|
| 0 | (d+delta,-d) |
| d+1-delta | (-A,1-delta) |
| 2d | (-d-2+delta,-d) |
| 4d+2-delta | (-d,d+2-delta) |
| 5d+1 | (delta-1,-A) |
| 6d+2-delta | (-d,-d-delta) |
| 8d+2 | (d+delta,-d) |

The six flight durations are d+1-delta, d-1+delta, 2d+2-delta, d-1+delta, d+1-delta, 2d+delta. All are positive for d>=3,0<delta<2. Each indicated hit is the first actual boundary in that leg: between them the trajectory crosses only the internal overlap rectangle or arm entries. At delta=0 the initial point is the cone (d,-d); at delta=2 one intermediate event is the cone (-d,d). Thus the strip cannot extend beyond these transverse endpoints.

The return period in v-time is T1=8d+2 and the transverse parameter width is W1=2. The first-return section x=d inside the central square meets this cylinder at y=d-delta, namely r=x-y in (0,2). No earlier positively directed crossing of that central section occurs. The cylinder area is T1*W1=16d+4; the Jacobian of (flow time,delta) in flat coordinates has absolute value 1.

## 3. Second exact diagonal cylinder

Use the central section (x,y)=(d,d-r) for 2<r<2d. There are two event orders, separated by a REGULAR convex corner at r=d+1.

For 2<r<d+1:

| Cumulative time | Signed representative AFTER translation |
|---|---|
| 0 | (d,d-r) |
| r | (d+r,-d) |
| d+1 | (-A,1-r) |
| 3d+r+1 | (r-1,-A) |
| 4d+2 | (-d,-d-r) |
| 6d+2 | (d,d-r) |

For d+1<r<2d:

| Cumulative time | Signed representative AFTER translation |
|---|---|
| 0 | (d,d-r) |
| d+1 | (-A,A-r) |
| r | (r-3d-2,-d) |
| 4d+2 | (-d,3d+2-r) |
| 3d+r+1 | (r-2d-1,-A) |
| 6d+2 | (d,d-r) |

At r=d+1 the simultaneous corner identifications are consistent: the first merged event is (A,d) and the later one is (d,A), both regular marked corners of the unfolded surface. The orbit continues in the underlying flat cylinder. There is no cone at this interior r value; it does not become a cylinder boundary merely because it is optically forbidden as a ray contact.

All listed actual boundary contacts are first hits in the corresponding legs. For example, in the first case the left-to-top passage crosses x=-d at y=d+2-r<d and later y=d at x=r-d-2>-d, both internal entries; hence the next real contact is the roof. In the second case the left-arm horizontal reflection occurs before entering the overlap, and the next real upper-arm contact is x=d. The later bottom-arm passages reach the stated central section without another real wall.

The next positively directed crossing of the central section is exactly the final one, with the SAME r. Intermediate x=d contacts are at y>d or y<-d and are real arm-wall identifications, outside that central section. Therefore the return is primitive and different r values in this interval describe different orbits. At r=2 the extended orbit meets the cone (-d,d), and at r=2d the initial point is the cone (d,-d). This is a maximal cylinder of period T2=6d+2 and transverse parameter width W2=2d-2.

The two cylinders have disjoint central-section ranges (0,2) and (2,2d), and their explicit return orbits have no other central-section crossings, so they are disjoint. Their areas exhaust the entire surface:

T1*W1+T2*W2=(8d+2)*2+(6d+2)*(2d-2)
=12d^2+8d
=4*(2dA-d^2)=area(M).

The remaining finite boundaries are the cone saddle connections exhibited by the endpoint orbits. Thus no additional positive-width cylinder or unaccounted chart region is needed for the twist construction. No numerical cylinder census has been used.

## 4. Common derivative and compatible coefficient

In cylinder 1 take transverse coordinate zeta=delta, measured from its delta=0 boundary. In cylinder 2 take zeta=r-2, measured from its r=2 boundary. In every local translation chart their gradient is (1,-1); chart translations change only the offset. Define F_k in each cylinder by advancing along v by time k*zeta modulo its full return period Tj.

The local derivative is I+k*(1,1)^t*(1,-1), the matrix stated in the result. The lower boundary has zero displacement; the upper boundary has displacement k*Wj along the full primitive flow. The exact pointwise gluing conditions are

2k/(8d+2) in Z,
(2d-2)k/(6d+2) in Z,

or equivalently k/(4d+1) in Z and k(d-1)/(3d+1) in Z. These conditions fix BOTH boundaries pointwise and give one common derivative across every regular boundary arc. The inverse is F_-k. The map extends at the cone as an affine homeomorphism of the actual unfolding. The accepted L centrality/fixed-set result then preserves every regular physical corner mark as well.

The first condition already makes k an integral multiple of 4d+1. Since gcd(4d+1,3d+1)=1 and gcd(d-1,3d+1)=gcd(d-1,4), the minimum positive common boundary-fixing coefficient is exactly k0 above. This classifies these boundary-fixing multitwist coefficients, not the complete diagonal foliation stabilizer.

## 5. Exact original endpoint phases

In normalized coordinates p=(2d-1,1), q=(1,2d-1). Source p lies in cylinder 2 at transverse coordinate zeta_p=2d-4: it is reached from the central section with r=2d-2 before that orbit's first wall. The actual diagonal coordinate-swap symmetry preserves cylinder 2 (its period differs from cylinder 1) and reverses its transverse interval. Since q is the swapped p, zeta_q=W2-zeta_p=2. This computes actual cylinder levels, not an arbitrary projected target choice.

The source displacement fraction of a full T2 orbit is

k0*zeta_p/T2=(4d+1)(d-2)/g0.

The target's fraction is

k0*zeta_q/T2=(4d+1)/g0.

The other ORIGINAL target lifts Rxq and Ryq lie on genuine diagonal saddle-connection boundaries: their signed differences x-y are -2d and +2d, respectively, and their straight diagonal lines reach a reflex cone. The displayed cylinder endpoint paths contain them. Thus EVERY F_k fixes Rxq and Ryq pointwise. The fact that these points lie on a cone connection does not make them themselves corners: they are regular actual lifts of the interior target.

For d=1 modulo4, g0=4, and the source fraction is 3/4 modulo1. Thus F(p) is backward diagonal flow by exactly T2/4=(3d+1)/2. That backward flow has NO actual cross-boundary translation before this time: it passes from the right arm through the central overlap and into the lower arm. Its endpoint is

(2d-1,1)-((3d+1)/2)*(1,1)
=((d-3)/2,-(3d-1)/2).

The inequalities d>=5 imply 0<(d-3)/2<d and d<(3d-1)/2<A. The selected original target lift Ryq=(1,-2d+1) satisfies 0<1<d and d<2d-1<A. Both exact image points therefore lie in the open convex rectangle (0,d)x(-A,-d), in the SAME signed (+,-) polygon copy. Their straight segment remains strictly inside this rectangle, so it contains no Sigma point, including its endpoints.

After rescaling by 2 this is the native seed stated at the start. Because the global affine map preserves Sigma, its inverse restores a regular straight segment from the exact original p to the exact ORIGINAL Ryq. Refolding gives the actual S-to-T billiard ray. If physical T is encountered earlier on refolding, truncate at its first encounter as in the accepted inverse-transport theorem. No reflection bound, minimum, finite optical enumeration or explicit long-ray replay is asserted.

## 6. The other residue class is a controlled failure of this map only

For d=3 modulo4, g0=2 and BOTH fractions are 1/2 modulo1. Starting at p, forward time T2/2=3d+1 gives F(p)=(d-2,d+2). The coordinate-swap symmetry conjugates F_k to F_-k; on a half-period displacement the inverse is the same point. Hence F(q)=(d+2,d-2). These two original-copy image points have midpoint (d,d), the actual reflex.

Rxq and Ryq are still fixed in their distinct signed copies; Jq maps to JF(q) in the opposite copy. Thus no one-copy seed from F(p) to ANY F(gq) is possible for this F. For even powers the original p,q return, and for odd powers the displayed half-period pair returns; in both cases the same reasoning excludes all four g. This is an exact all-power statement for this multitwist. It does not exclude arbitrary affine maps or new combinations with other directional actions.

## What this changes

For the d=1 modulo4 part of the author's obstruction family, the complete-target-fiber gate DOES hold for the specified native S,T, by an actual outside-safe-kernel affine map and a rigorously identified Ry target lift. The safe arbitrary-large twist construction was too coarse to see that movement. This is a substantive endpoint-action lemma, not merely map existence or a new illuminated family (physical L illumination was already known).

It is NOT coverage of all native pairs in these rooms, all d, all L metrics, ten walls, or r<=8. The d=3 modulo4 calculation leaves a genuine residual even for this diagonal-power constructor. The full affine seed gate remains open. No seed class or physical endpoint was changed, and no numerical discovery, orbit census, worker, engine, frozen-source edit, git action or effort-clock restart was used.
