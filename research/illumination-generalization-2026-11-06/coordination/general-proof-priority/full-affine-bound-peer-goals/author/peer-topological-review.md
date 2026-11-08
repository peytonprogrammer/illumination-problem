# Independent hand review of the same-surface nonaffine control

Decision: ACCEPT the exact source snapshot, no material findings. This accepts an inadmissible-control construction only; it does not establish a lowering affine derivative or any part of the claimed whole-group minimum.

Source: reviewer/topological-control.md, SHA256 eb3f7645ef51ffdf1d3919bf6f810fb621f167f1db05355f64d372bb87165d10. The final request manifest was not yet present at audit start. Reconcile its eventual pin against this exact snapshot before treating this as acceptance of a differently pinned packet.

## Embedded actual gamma and its tube

With the original time parameter 0<=t<=2, gamma=(2d-1-dt,1+(d-1)t) has strictly decreasing x and increasing y. For x>d, t<(d-1)/d, so y<d-1+1/d<d. For y>d, t>1 and -1<=x<d-1, strictly within the vertical arm's horizontal bounds since d>=3. The other outer-coordinate bounds are strict. Thus the entire segment is in the open injective signed-cross chart.

The only regular physical corner inside that chart is O, avoided because y>=1. Boundary corner representatives are also avoided strictly. The axes are internal seams, not new corners. A compact embedded arc in this open regular chart has a slightly extended tubular rectangle with closure disjoint from Sigma and contained in y>0. Its half-turn image is disjoint in y<0. This is a per-d construction with no asserted uniform tube radius.

## Global supported Hamiltonian and cutoff

The coordinate basis (v,n), n=(-v_y,v_x), has determinant |v|²>0. The flat area form is therefore a constant positive multiple of dt wedge du. The displayed Hamiltonian vector field preserves this form; the constant factor only changes which scaled Hamiltonian represents it relative to the physical area form.

On u=0 inside the cutoff plateau, the exact equations are t'=c(t-2/7), u'=0. Their solutions stay between t and 2/7, hence inside [0,2] for the whole time interval. Consequently rho remains one and its derivatives vanish along these trajectories. A sufficiently small neighborhood of the compact initial arc stays in the plateau throughout the compact time interval as well. There the actual time-one map is exactly

    (t,u) -> (1/4+t/8,8u),

because (1-1/8)*(2/7)=1/4. Its determinant is one. In particular the actual whole-path derivative sends v to v/8. Transverse expansion poses no support contradiction: the initial neighborhood can be made sufficiently thin. Compact support makes the vector field globally complete on the compact underlying surface and equal to zero near every corner.

The product with its J-conjugate has disjoint supports. The two factors commute, and conjugation swaps them, proving HJ=JH. The paired flows give an isotopy fixing Sigma pointwise. These claims do not require an optical continuation through a corner.

## Actual endpoint and copy checks

For the image parameter z=1/4+t/8, z ranges exactly over [1/4,1/2]. Along this subarc,

    3d/2-1 <= x <= 7d/4-1,
    (d+3)/4 <= y <= (d+1)/2.

For every d>=3, x>d and x<A, while 0<y<d. Thus the ENTIRE image lies strictly in the original lower rectangle, including both endpoints. Its displacement is (1/2-1/4)v=v/4, matching the original holonomy 2v transformed by the local factor 1/8. The endpoint is H(ORIGINAL Rxq); no reflected-target substitution occurs.

Isotopy to identity fixes all absolute homology and its period homomorphism. Isotopy relative Sigma also fixes relative classes with endpoints in Sigma. This does not fix relative periods of gamma, whose endpoints are not fixed by H.

## Why this is not a candidate affine counterexample

Both new endpoints have nonintegral x for odd d, so neither is in the intrinsic U fiber. In addition H has derivative I on an open subset outside the two supports, but derivative L_loc != I around gamma. It therefore has no common global affine derivative. Either test excludes it from the assigned group.

The construction does not assert torus-equivariant covering action, pointwise preservation of translation forms, or a realized integral DF. Its local shortening and topological corner/homology/area compatibility consequently do not refute the affine minimum.

## Consequence and scope

ACCEPT the control for all specified residual d, without numerical replay. It shows why topology, area, absolute periods, J symmetry and local affinity along the entire path still do not imply global affinity. This supplies no positive full-group inequality and no actual affine shortening map. The broad goal and fixed-gamma gate remain OPEN.

No material findings, source edits, discovery, worker, engine, census, git change or clock renewal.
