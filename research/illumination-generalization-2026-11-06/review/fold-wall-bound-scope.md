# Whole-copy wall counting beyond orthogonal bases

Candidate hand theorem for independent review. This is a geometric construction-class bound, not necessity of folding or a proof of W<=21 illumination. No computational geometry or optical discovery was performed.

## Exact hypotheses

Let B be a strictly simple polygonal disk with w genuine maximal walls and every angle an integer multiple of pi/4. Assemble m whole congruent copies B_i=g_i(B), with disjoint interiors, into a strictly simple polygonal disk Q. Require the literal inverse-copy maps g_i^{-1} to agree pointwise at ALL contacts. The maps take values in B itself, not in B modulo a symmetry. Assume a finite planar polygonal cell decomposition by the copies. In fact full-wall rigidity below gives this from the other finite-polygon assumptions.

Let E count internal seam edges, subdivided only at actual copy vertices. Let I count interior vertices of this cell decomposition. At a seam junction v, let k(v) be the number of incident copy corners, and theta(v) their common base-corner angle. Let N_s count smooth boundary junctions. Unshared corners have k=1 and are not seam junctions.

## 1. Local geometry and full seams

The accepted whole-copy rigidity argument does not use orthogonality. On a positive-length contact segment, g_j composed with g_i^{-1} fixes that segment pointwise. It must be its supporting-line reflection; the identity would violate disjoint interiors. Reflection fixes and matches the entire maximal wall containing the contact. Hence positive-length contacts are full walls of both copies.

Pointwise agreement at a physical junction maps every incident corner to the SAME actual point of B. Thus all incident corners have the same angle theta. A smooth neighbor cannot occur at a corner junction: its inverse image would make the same point of B both smooth and a genuine corner. An interior neighbor is excluded by overlap. At an open seam point exactly two smooth half-planes meet. At a corner junction the disjoint sectors each have angle theta; strict simplicity requires their union to be one sector on the boundary, or the full disk in the interior. Consequently

- boundary junction: k*theta<2pi, with k*theta=pi precisely when smooth;
- interior junction: k*theta=2pi.

A reflex base corner has theta>pi, so k=1 and it survives as a distinct actual corner. Interior junctions can occur only for theta=pi/2,k=4 or theta=pi/4,k=8. The other genuine multiples 3,5,6,7 of pi/4 do not divide 2pi with an integer k>=2. Smooth boundary junctions have theta=pi/2,k=2 or theta=pi/4,k=4.

## 2. Exact counting identity

The copy decomposition is a cellulation of a disk with m faces. Boundary edges and boundary vertices have equal counts, since the boundary is a Jordan cycle. Euler's formula therefore gives

    E=m+I-1.

At a genuine boundary junction, k copy-corner incidences become one actual corner, losing k-1 vertices. At a smooth boundary junction they lose k. At an interior junction they lose k. Counting seam ends gives

    2E = sum_boundary_junctions(k-1) + sum_interior_junctions k.

Here the first count is k-1 because sectors are linearly ordered at a boundary point, and the second is k because they are cyclically ordered in the interior. Combining the corner-incidence and seam-end counts yields

    W(Q) = m*w - 2E - N_s
         = m*(w-4)+4+D,

where

    D = sum_boundary_junctions [k-1-1_{k*theta=pi}]
        + sum_interior_junctions(k-4).

EVERY summand is nonnegative. At a smooth boundary junction k>=2, and at an interior junction k is4or8. Therefore

    W(Q) >= m*(w-4)+4.                         (A)

This includes shared endpoints and cycles. Equality requires all boundary seam junctions to be pairs of right-angle copy corners, and all interior junctions to be four right-angle copy corners. A smooth junction of four45degree corners contributes2 to D; an interior eightfold45degree junction contributes4. A pair of135degree corners contributes1. Those cases cannot be erased under an orthogonal-only counting identity.

For an orthogonal B, boundary threefold junctions contribute2 each and all other junctions contribute0, reproducing exactly the accepted D=2*t3 formula. Thus (A) extends the geometric assembly inequality, while retaining a defect that detects non-right-angle junctions.

## 3. What is still needed to infer22

The old numerical22 proof also used TWO separate facts about an ORTHOGONAL parity base:

1. w>=10, proved by a unit-square incidence count and a finite list of polyominoes of size<=4.
2. Two distinct smooth boundary marks require m>=3, using at most one permissible mark per base wall and the two-copy seam count.

The unit-square incidence proof is not a proof of item1 for diagonal-wall triangle bases. Its area and vertex-incidence identities change when a square can be partially occupied. Formula(A) alone therefore does NOT extend22 to all canonical45 parity folds.

For a diagonal-wall base, the two-copy argument also needs its premises checked. Since an interior junction needs at least4copies, m=2 implies I=0,E=1. Every actual interior preimage of a smooth base mark must be in the interior of that single seam. If at most one of the marks can lie on any one base wall, both marks cannot become interior with2copies, so m>=3. The 'at most one mark per wall' premise follows for the exact residue condition with marks in a+2Z^2 and all OTHER integer wall points genuine corners: two distinct same-residue smooth integer marks on one straight maximal wall have their integer midpoint in another residue class when adjacent along that residue lattice; choosing consecutive such marks gives a forbidden smooth point. This argument applies to primitive axial or diagonal lattice wall directions when the allowed mark residue is literally a+2Z^2 and all integer points of the base are in the stated census. Other parity conventions require their own argument.

Thus a sufficient numerical route would be an independently proved w>=10 for the precise admissible diagonal parity-base class, together with these mark hypotheses. Neither that minimum nor fold necessity is proved in this packet. If w=9 is possible, (A) with m=3 gives only19 plus the explicit D; if w=8 is possible it gives16 plus D. One must analyze those base classes or show their seam defects compensate. They are not asserted to exist.

## Scope

This packet extends only the assembly count for a PROVIDED literal whole-copy fold. It neither constructs a dark room nor classifies dark mechanisms. It does not establish a diagonal parity obstruction, preserve darkness under beveling, or assert a global minimal wall count. Those are separate optical obligations.

Dependencies read: ../..//illumination-k4-codex/shared-seam-test/findings.txt sections3-7 and shared-seam-review/review.txt sections2-7 (paths are indexed exactly in the accompanying review request). Their original files remain unchanged. The proof above independently uses finite cellulation, the angle list and Euler's formula; it does not import an unproved optical reduction.
