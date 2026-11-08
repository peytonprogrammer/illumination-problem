# Global affine normalization also cannot give a uniform exception cap

Author Codex01a18403, 2026-11-06. Hand proof, independent review requested. This supplements the frozen scale-normal-form.md; that file is unchanged.

## Claim

Even among six-wall rational orthogonal marked rooms, the minimum k after ANY global affine map that preserves Euclidean specular reflection at every wall (for all incident directions), AND makes the room canonical45 with its actual marks interior A points, is unbounded. This refutes only an unconditional global affine normalization, not a darkness-dependent or nonaffine reduction.

## Proof

For integer L>=2 take the L room

    P_L=([0,L+1] x [0,1]) union ([0,1] x [0,L+1]),
    S=(L,1/2), T=(1/2,L).

It has W=6, area 2L+1, rational vertices/marks, and distinct interior marks. By scale-normal-form Lemma 1, it has a canonical45 presentation with A marks. These pairs are already known illuminated by the earlier accepted L-room theorem; no darkness is asserted.

Let A be the linear part of an invertible affine map preserving Euclidean reflection at the horizontal and vertical walls. Its two columns must be orthogonal. Indeed reflecting reverses the wall normal and fixes its tangent; their images must again be perpendicular normal/tangent eigenlines. Equivalently A^T A commutes with both axis reflections and is diagonal. Write A=O diag(alpha,beta), with O orthogonal and alpha,beta>0, absorbing possible signs into O. This reproves the needed part of peer bridge.md B3 without importing its conclusion unexamined.

At S, the segment through S perpendicular to its horizontal arm meets the two local walls at distances 1/2. Its affine image has half-clearance beta/2 in direction O e_y. At any interior A mark the full square [-1,1]^2 centered at the mark is contained in the new room. For every unit direction u this square contains mark +/- u (the closed unit disk is contained in the square). In particular it contains the unit segments in both directions O e_y. Since the actual image wall is only beta/2 away along that line, beta/2>=1. Thus beta>=2. This uses local radial clearance at S, not the width of the whole nonconvex room.

At T, the same argument perpendicular to its vertical arm gives alpha>=2. Hence the new area is

    area' = alpha beta (2L+1) >= 4(2L+1).

For every canonical45 disk, counting one C incidence per triangle gives

    N=2 area' <=4k+3W.

Here a regular interior C contributes4, a smooth boundary C2, a genuine C corner at most3; all these statements hold in the NEW lattice presentation. Since W=6,

    k >= (2 area'-18)/4 >=4L-5/2.

For integer k, k>=4L-2. This tends to infinity despite the fixed six-wall boundary pattern and freedom to choose the global affine map and final canonical lattice.

## Consequence and limitations

Together with the earlier similarity lemma this rules out the entire unconditional global-affine compression strategy, including independent axis scaling of orthogonal rooms. The marks impose two independent local clearances. A proposed successful normal form must exploit darkness, change the geometry nonaffinely with a proved transfer, or handle unbounded k directly.

No bound on the reflection count, no new illuminated class, no dark counterexample and no lower bound on dark-room wall counts is established here.

## Independent review of peer bridge B1--B4

B1 agrees with the separately derived exact scaling equivalence. B2 counts checked by hand: in [0,4]x[0,2n+1], total interior integer points6n, interior A n, J5n; smooth boundary total4n+6, smooth A2n+1, s_N2n+5, hence k7n+5. For the square [0,2n]^2 the stated I,J,s_N counts also follow directly. B3 eigenline criterion is valid, including sufficiency. B4 fixed-word stability is valid with finite transverse hits and positive nonincident-wall clearance. Dense rational illumination cannot by openness alone prove illumination of a real limit. A full global affine invariant is not being inferred from local stability.
