# A finite depth test for the dead-end doorway

Use coordinates in which a rectangular viewer channel has transverse width L, and a target chamber has transverse width w. Its entire near side is an open doorway on y=0, inside the span of the channel. Its two sides are physical walls and its far end y=e is a physical wall. Let 0<h<e be the target's depth, and D>0 the source's distance from the door. Require the viewer channel's two physical sides all the way from the source height to the door. When reflecting at a viewer back wall, also require the channel to be a full rectangle of depth A with a physical back wall and both side walls, 0<D<A. Other parts of the room are unrestricted. Protrusions across the unused part of the doorway line are harmless. Marks lie strictly between their respective side walls.

## Removing the corner exception

Use the existing convex-corner retracing argument on the formal reflection at a far cap. A ray aimed at a reflected target has an ordinary trajectory up to that cap corner. Its formal continuation reverses both velocity coordinates, so it retraces its incoming path. The nominal target on the return leg was already reached on the outgoing leg at height h. The physical ray can stop there. The corresponding source-backwall case is the time reverse: discard the formal prefix returning to the source. Both deletions can be made together, on opposite sides of the strict doorway crossing. A far cap endpoint here is convex because the cap and side are both physical walls and the room is strictly simple. The argument never allows a trajectory through a reflex vertex or the endpoint of the doorway.

The retracing principle already occurs in the project's spiral proofs. Applying it to both ends removes the cap-corner alternatives left open in D58.

## Arithmetic of a failed crossing

Choose a source depth d (D, or 2A-D if the full back wall is available) and a target depth z (h or 2e-h). Reflected transverse coordinates of source and target range over two signed images with periods 2L and 2w respectively. A line between the images crosses the door at the weighted average (z s'+d t')/(d+z). A crossing strictly inside its width-w window suffices. All side reflections before reaching the cap are in physical walls. The preceding truncation treats any simultaneous side/cap contact.

Here is the D58 phase argument, including strictness. Normalize transverse coordinates in units of w, with zero at the left door edge. For a fixed source image the open interval of acceptable target-image coordinates has length 1+z/d. The signed target images form two distinct residues modulo 2. Therefore z≥d always works. If z<d, the phases for which the interval misses both residues form at most one closed arc of length strictly less than 1: the two gaps between the target residues sum to 2, so at most one can contain an interval of length 1+z/d; its admissible starting positions span less than 1. Shifting a viewer image by one period rotates the interval's phase by 2Lz/(wd) modulo 2. An irrational rotation is dense. A nontrivial rational rotation has at least two equally spaced orbit points which cannot all be contained in an arc of length less than 1 (the shortest containing arc for k points has length 2-2/k). Thus failure of this family requires

    1 ≤ L z / (w d) < L/w, with L z / (w d) an integer.

This is an implication from darkness, not a test that declares a pair dark.

## Two consequences for real wall lengths

With the target cap, set R=L/w. Both u=R h/D and v=R(2e-h)/D must be positive integers, with u<v<R. Thus:

* If w≥L/2, every such distinct interior pair is lit.
* At any fixed dimensions, a dark pair must have D=2Re/(u+v) and h=2eu/(u+v). The two normal coordinates belong to an explicit finite list, even when the lengths are arbitrary real numbers. The transverse coordinates still require treatment.

With both back walls, the matrix with rows d=D,2A-D and columns z=h,2e-h, entries Rz/d, must consist of positive integers strictly below R. It has rank one. Write the reduced ratio of the two columns as k:l, k<l, and the rows as m(k,l), n(k,l). Then m>n≥1 and l>k≥1. The largest entry ml is at least 4. Consequently **if w≥L/4, every such pair is lit**. This includes equality. More generally U=m(k+l) and V=n(k+l) satisfy the room-only test

    A w / (L e) = 1/U + 1/V,  with U>V and ml<R.

If no quadruple satisfies these finite conditions the entire source-target chamber pair is illuminated. A qualifying quadruple is a necessary condition only.

D58's ten remaining door position types all have target caps. Its five full-back configurations also get the four-entry test, provided the rectangular side walls continue to the back wall as stated above. The width ratios can be arbitrarily large on the full parameter spaces. This does not close all ten position types at unrestricted lengths.
