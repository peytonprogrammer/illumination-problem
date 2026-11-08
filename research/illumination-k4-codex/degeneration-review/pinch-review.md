# Separating-pinch and cylinder review

[done] Reviewed Lemma10, Corollaries11/14 and Lemma12 as mathematical statements in the peer memo. Conjecture13 and the uniform counting problem remain open. These are fixed analytic diagnostics; no rays or rooms were searched.

## Lemma10: accept with explicit orientation and an open window

Use the open interval (0,e): its endpoints are corners and therefore excluded. Develop the two words so that their endpoints lie on opposite sides of the same window line, and orient their direction parameter from the source side toward the target side (reverse a target-to-window fan). Restrict to a common transverse angular branch.

The source crossing map is strictly increasing and the target crossing map strictly decreasing. At the left endpoint of a positive-length overlap, one crossing tends to0 or the other tends to e, giving a strictly negative difference. At the right endpoint the opposite inequality holds. Continuity gives exactly one interior crossing. The two ordinary words concatenate there without a reflection. This proves the stated sufficient condition under the full-window fan hypothesis.

## Corollary11: replace approximate weights or add a margin

Put the window on x=0, with developed source S=(-a,y_s) and target T=(b,y_t), a,b>0. For a reference slope m0, let

    c_s=y_s+a*m0, c_t=y_t-b*m0.

The exact joining segment crosses at

    w_exact=(b*c_s+a*c_t)/(a+b).

Thus exact current perpendicular distances a,b give the valid criterion 0<w_exact<e, provided the two fixed words cover the whole window. At the limit direction, a0 and b0 are proportional to the limiting developed lengths L_s,L_t, so the memo's length weights are correct only asymptotically.

Strict membership of an approximation is not enough. For 0<e<1/2 take

    a=1-e, b=1, c_s=-e+e^3, c_t=e.

The limiting lengths are equal. Their weighted prediction is e^3/2, strictly in (0,e). The exact crossing is (-e^2+e^3)/(2-e)<0, so these two fans do not meet. This refutes the proof's overlap inference, not the possibility that some other pair of words lights the room.

A safe first-order version assumes the predicted crossing divided by e stays in [eta,1-eta] for a fixed eta>0, and proves the interpolation error is o(e). Alternatively use the exact a_n,b_n weights and omit the Taylor approximation.

## Corollary14: accept after controlling normalized offsets and local face convergence

An open limiting passage interval is the right margin condition, but convergence of the weighted mean alone does not control individual offsets. Here is a cancellation diagnostic with e=h^2:

    a=1-h, b=1,
    c_s/e=-1/h+1/2, c_t/e=1/h.

The mean using limiting equal weights is1/4, inside the normalized window(0,1). Both unscaled offsets tend to0, so the limiting line still goes through the pinch. But the exact normalized crossing is (-1/2)/(2-h)<0. The direction error is of order h, not e; the memo's asserted O(e) estimate does not follow from its present hypotheses.

Require the individual offsets in neck units to stay bounded, or explicitly assume that the difference between exact and predicted normalized interpolation tends to zero. Then current distance ratios converge to their limiting ratios, and an interior limit rho in the open passage interval does give eventual passage. Also require convergence of the labelled local wall faces and interior sides along the prescribed local word, as in the corrected Lemma7. Hausdorff convergence alone does not supply that local stability.

Exact Fraction-arithmetic examples for both issues are in `pinch-check.py/json`.

## Lemma12: accept the fixed-grid facts; retain the scale dependence

The common-open-cylinder criterion is sound: a cylinder lifts to a convex strip with no marked corner inside, so joining lifts stays in the strip. For the converse description by rational cylinders/boundary leaves, state explicitly that the source and target are lattice points, as in the canonical-family problem. Integer wall vertices alone do not make the displacement of arbitrary real marks an integer vector.

On an unscaled integral translation surface, perpendicular coordinates of marked lattice vertices in primitive direction (p,q) differ by integer multiples of1/sqrt(p^2+q^2). Thus cylinder heights, and a lattice mark's positive distance to a cylinder boundary, have that lower bound.

After normalizing a changing room to unit size, replace1 by its grid spacing h_n. The bound is h_n/sqrt(p^2+q^2), which tends to zero when the lattice refines or the direction denominator grows. The statement therefore supplies an exact clearance for each fixed cylinder, not a uniform neck-scale clearance or a lower bound on how many cylinders simultaneously contain both marked lifts. It does not by itself settle the earlier fan-cutting/counting concern.

Moreover Lemma12's cylinder criterion includes the boundary-leaf alternative. A claim that a lit room must have an open cylinder containing both marks would need a separate proof; Conjecture13 is stronger than mere illumination near a pinch.

## Recommended next step for Opus

Use exact developed-distance interpolation for each fixed finite word. For growing words, formulate the needed uniform estimate in normalized grid units and separate open-cylinder connections from boundary-leaf connections. Do not replace the uniform estimate by the unscaled lattice-spacing bound.
