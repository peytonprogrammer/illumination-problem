# A same-surface control for the global affine realization gap

For every assigned d>=3, d=3 modulo4, the following is a HAND construction on the actual surface M_d. It does NOT refute the proposed affine norm bound. It proves that even a strong collection of topological, area, homology and local-path conditions does not imply global affine realization.

Put A=2d+1, v=(-d,d-1), and gamma(t)=(2d-1,1)+t v, 0<=t<=2, in the actual signed-cross chart. This is the prescribed p to ORIGINAL Rxq path. No replacement path or new direction is chosen.

## Precise control

There exists a smooth orientation- and area-preserving diffeomorphism H of the underlying flat surface, equal to identity near every physical corner, with the following properties:

1. H is isotopic to identity relative to all of Sigma, fixes Sigma POINTWISE, and induces identity on absolute homology and on the absolute period homomorphism.
2. H commutes with the actual half-turn J=RxRy.
3. H maps the ENTIRE actual gamma to its subarc gamma([1/4,1/2]), which lies strictly inside the original bottom-arm rectangle.
4. On an open neighborhood of gamma, H is affine in the translation coordinates, with ONE constant derivative L_loc of determinant1 and L_loc v=v/8. It therefore shortens the velocity of this entire path, not merely its endpoint distance.
5. H is NOT globally affine. Its endpoint images are not in the intrinsic cone fiber U. Thus H is not an admissible F in the norm-minimum question or in the affine compression gate.

This construction rules out promoting the listed weaker data to a genuine affine realization. It does not rule out a stronger invariant specific to global affine maps.

## The actual path has a corner-free embedded tubular disk

The signed cross is the union of the horizontal rectangle [-A,A]x[-d,d] and vertical rectangle [-d,d]x[-A,A], with the usual translated outer sides. Its interior is an injective translation chart; the coordinate axes are ordinary internal seams. The regular corner O is at its origin; other physical corner representatives lie on its boundary.

Along gamma, y>=1, -1<=x<=2d-1<A, and y<=2d-1<A. If x>d, then t<(d-1)/d and

    y < 1+(d-1)^2/d = d-1+1/d < d.

If y>d, then t>1 and -d<x<d-1. Hence every point of gamma lies in the OPEN cross. At x=d its y is d-1+1/d; at y=d its x is d-1. It avoids the reflex corner and every other physical corner. The line segment is injective in this chart, so it is an embedded arc on M_d, including its crossing of x=0.

Compactness gives a slightly extended embedded tubular rectangle N around gamma, with closure in this open chart, disjoint from Sigma. Choose it in y>0. Then N and JN are disjoint, since J acts as -I on this cross. Let n=(-v_y,v_x) and use tubular coordinates

    Psi(t,u)=p+t v+u n.

The flat area form is the positive constant |v|^2 times dt wedge du in these coordinates. Shrink the transverse width and the extension beyond t=0,2 as needed; no uniform tube width in d is asserted or required.

## A supported area-preserving contraction of this arc

Let kappa=1/8, c=log(kappa), and t_star=2/7. Choose a smooth cutoff rho(t,u), compactly supported in the interior of the tubular rectangle, equal to1 on a neighborhood of [0,2]x{0}. On this rectangle take the Hamiltonian

    K(t,u)=c*(t-t_star)*u*rho(t,u).

Use the area-preserving vector field

    dt/ds = partial K/partial u,
    du/ds = -partial K/partial t.

The constant multiple in the flat area form does not affect preservation of area; this vector field preserves dt wedge du and therefore the actual flat area. It extends by zero outside N to a smooth vector field on M_d, supported away from the cone and every marked corner. Its time1 map H_N exists globally, is identity near the boundary of N, and is isotopic to identity relative to Sigma by its own flow.

For initial (t,0), 0<=t<=2, the explicit solution is

    t(s)=t_star+kappa^s*(t-t_star),  u(s)=0.

It stays on [0,2]x{0}, because t_star is in (0,2). Thus the cutoff remains1 throughout, and the displayed solution is the actual supported flow, not an unguarded formal trajectory. At s=1,

    t(1)=1/4+t/8.

Consequently H_N(gamma(t))=gamma(1/4+t/8) for every t in [0,2]. Continuous dependence and compactness of the swept axis give an open neighborhood of the initial arc whose trajectories remain in the rho=1 region for all 0<=s<=1. On that neighborhood the time1 map is exactly

    (t,u) -> (1/4+t/8, 8u).

In the original translation coordinates its derivative is the ONE constant matrix

    L_loc = [v n] diag(1/8,8) [v n]^{-1}.

It has determinant1 and sends v to v/8.

For the half-turn condition, define H as the product of H_N and J H_N J^{-1}. Their supports lie in the disjoint disks N and JN, so these maps commute. Conjugation by J interchanges the two factors; hence H commutes with J. The second factor is identity on gamma. H has all the stated area, support and path properties. The paired flows also give an isotopy from identity commuting with J and fixing Sigma throughout.

## Exact copy, endpoints and periods

For t in [1/4,1/2],

    x >= 3d/2-1 > d,
    x < A,
    0 < y <= (d+1)/2 < d.

Thus the whole image lies in the open bottom arm of the ORIGINAL copy. Its exact endpoints are H(p)=gamma(1/4) and H(ORIGINAL Rxq)=gamma(1/2), with displacement v/4. There is no projected target substitution. The actual whole path, rather than an endpoint-only proxy, has been computed.

Since H is isotopic to identity, [H(alpha)]=[alpha] in absolute H_1 for every closed cycle alpha. Therefore the integrals of the flat translation form over all such closed cycles are unchanged. This is an absolute-homology/period assertion, not pointwise equality of the translation form and not an assertion about relative periods with moving endpoints. The same isotopy fixes Sigma pointwise, so it acts trivially on relative homology with endpoints in Sigma as well.

The cone fiber U has odd integer representatives in the signed cross. In particular gamma(1/4) has x=7d/4-1, which is nonintegral for every odd d. It is not in U. Likewise gamma(1/2) has x=3d/2-1, also nonintegral. Thus the construction does not preserve U and is excluded by an accepted necessary consequence of genuine global affinity.

Independently, H is identity on a nonempty open set outside N union JN and has derivative L_loc != I near gamma. A global affine map of a connected translation surface has a common derivative in every regular chart. H therefore cannot be globally affine. No choice of its locally computed derivative as a putative global DF repairs this failure.

## Consequence for the present bound

The existence of H does not show that ANY admissible DF shortens v. It proves that the exact same surface and prescribed path admit shortening and one-copy compression while preserving corners, area, absolute periods, the hyperelliptic half-turn and a constant local derivative around the entire path. The missing feature is genuine GLOBAL affinity, which additionally enforces intrinsic torus/fiber action and compatible behavior on every chart.

Accordingly, an author proof must supply an invariant of the entire realized affine group, not infer it from these weaker data. An author counterexample must supply a global common derivative/gluing action and exact marked-fiber behavior. The proposed minimum remains UNPROVED and UNREFUTED here. The fixed-gamma gate and broad r<=8 goal remain open. No numerical replay, new room/ray/direction/matrix/orbit search, census, engine, worker, frozen edit, git mutation or discovery-clock renewal was used.
