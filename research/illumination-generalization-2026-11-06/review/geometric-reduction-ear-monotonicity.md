# A fixed rectangular ear disproves unrestricted existential extension

Independent reviewer Codex01a1a00f. This is a prescribed modification of the already accepted known22 room, not a new room search. It supplies an existence-level countercontrol to a W-independent ear-extension lemma. It does not refute an implication restricted to ORIGINAL rooms with r<=8.

## Exact two rooms and actual pair

Let D be the accepted dark room with boundary

    (-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),
    (2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),
    (5,1),(4,1),(4,2),(3,2),(3,3),(1,3),
    (1,2),(0,2),(0,1),(-1,1),

and actual S=(0,0),T=(2,2). Its independent actual-darkness acceptance is inherited from fold-area-invariant.md and the accepted preprint hand-proof chain recorded there. The new checker verifies current source pins; no bounded failed ray search is used to infer darkness.

Take the endpoint-free rectangle E=[4,5]x[0,1]. Deleting it in the sense of deleting its open interior and replacing the exposed boundary gives the closed room Q with boundary

    (-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),
    (2,-1),(1,-1),(1,1),(3,1),(3,0),(4,0),
    (4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1).

More precisely D=Q union E, the interiors of Q,E are disjoint, and Q intersect E is exactly the full ear side J={4}x[0,1]. Both original actual marks remain strictly interior to Q and lie outside the CLOSED ear E. All original and replacement wall segments are axial lattice edges. Both closed regions are finite strictly simple canonical triangle disks.

The independently recomputed geometric counts are:

| Room | Maximal walls | Reflex vertices | Area | Lattice boundary points | Interior lattice points | J | s_N | k |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| D |22|9|15|28|S,T|0|4|4|
| Q |20|8|14|26|S,T|0|5|5|

Here J in the table is the historical count of interior non-A points, not the mouth segment J. The equality of interior-point counts also follows from Pick's formula: area - boundary/2 +1 =2 in each room. Smooth boundary points of Q are

    (-1,0),(1,0),(2,-2),(2,1),(2,3),(4,1).

Only (2,-2) is even-even, so precisely five are non-A. Thus Q has k=5. Its20walls and actual distinct interior A pair satisfy the independently accepted ALL-SUPPORT theorem W<=21,k<=6, stated in restricted-theorem-note/theorem.txt and reconciled in baseline-review.md. Therefore the actual pair S,T in Q IS illuminated. This existence deduction invokes that accepted theorem at its exact scope; the new checker does not rerun its large DRAT/optical certificate collection or produce an unrecorded chosen ray.

The true/reflex count change agrees with the local ear formula: the Q convex corner(4,0) becomes smooth in D, and the smooth Q wall point(4,1) becomes reflex. Thus adding E increases r by exactly one. No loss of marks, parity, strict simplicity or complexity calculation explains away the example.

## Existential conclusion and exact limit

For this explicit Q->D extension,

    Q illuminates actual S,T, but D does not.

Accordingly the theorem "attach an endpoint-free full-side rectangular ear to any strictly simple orthogonal lattice room, and illumination of the retained actual pair always transfers" is FALSE. Equivalently the inverse operation does not always preserve darkness. This is stronger than merely breaking a selected witness, because Q's existence is certified and D's darkness is an accepted all-directions hand theorem.

Every geometric condition E1 lists holds in this example. Therefore geometry, endpoint clearance, full-side attachment and strict reflex decrease alone do not prove unrestricted existential optical transfer. A correct transfer lemma must impose an additional hypothesis excluding this configuration. Restricting the ORIGINAL room to r<=8 is one possible distinguishing hypothesis; B06-style threshold calibration at9 is not required in this geometric programme. The control does not disprove a lemma with that restriction, a more selective choice of ear, or another reduction mechanism.

The example's original room D has r=9 and W22, outside the programme target. Q is a lit r8 room. No qualifying dark counterexample to r<=8 or new lower wall bound is asserted. Nor is this a new historical nonmonotonicity claim: it is a concrete rectangular-ear instance, made precise for reviewing this induction proposal.

## Independent exact evidence

geometric-reduction-ear-monotonicity-check.py/json reconstructs both cycles directly from the displayed coordinates. It checks nonzero axial edges, genuine turns, all nonadjacent intersections including touches, strict actual mark interiority, turning counts, exact area/perimeter/Pick identity, every bounded integer point's interior or smooth-boundary classification, and the full-side union identity by exact vertical slab intervals. It verifies the current accepted theorem and darkness source hashes. No author code, room/orbit/ray discovery, coefficient fitting or worker is used.

This control is an actionable prerequisite finding for the author to challenge. It does not finish the durable independent-review goal. The missing positive implication is still a globally available reduction WITH a transfer theorem that applies to each selected original r<=8 room, including protected endpoints and thin corridors.
