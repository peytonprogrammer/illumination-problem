# C1: geometry proved; optical transfer and global availability not proved

Codex01a18403, 2026-11-07. Candidate published in
geometric-reduction-candidate-01.md before prescribed control testing.
This milestone does not complete the active native goal.

## 1. Exact geometric reduction

Use the candidate's coordinates and isolation hypotheses. The old local
boundary runs horizontally into A=(0,H), vertically down to C=(0,0),
horizontally right to B=(L,0), then vertically down. Its turns are
convex, reflex, convex. The replacement continues the preceding horizontal
edge from A to V=(L,H), then continues vertically through B along the old
following edge. Thus A,B become smooth, C disappears, and V is convex.

Every other maximal wall and turn remains unchanged. In particular

    r(D')=r(D)-1,  W(D')=W(D)-2,  area(D')=area(D)+LH.

The open rectangle is exterior to D, and the two replacement sides have no
other contact with the old boundary. Consequently replacing this local arc
by the new arc gives a simple closed orthogonal boundary; its interior is
the old interior together with the added rectangle and its old seam sides.
There is no slit, self-contact, detached component or newly enclosed hole.
All vertices remain lattice vertices. Both actual marks stay strictly
interior because D is contained in D' and their original neighborhoods
remain inside. There is no quotient endpoint or selected target image.

Hence, whenever this rectangle is available, it is a valid geometric
strict-r reduction in the actual induction domain. This conclusion alone
says nothing about illumination transfer.

## 2. Base case

An orthogonal strictly simple room with r=0 has four maximal walls by the
turning equation c-r=4, and therefore is a rectangle. More generally any
convex room contains the complete segment between two interior points in
its interior. For distinct S,T this segment has positive finite length,
zero reflections, no wall contact and no corner contact. This proves the
actual convex base case without an unfolding or arithmetic assumption.

## 3. An existence-level obstruction to removing the r<=8 restriction

Take the accepted known22 room D and actual S=(0,0),T=(2,2), with boundary

    (-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),
    (2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),
    (5,1),(4,1),(4,2),(3,2),(3,3),(1,3),
    (1,2),(0,2),(0,1),(-1,1).

The triple (-1,-1),(0,-1),(0,-2) is an isolated convex-reflex-convex
corner. Complete it by adding [-1,0]x[-2,-1]. Reading the local boundary
in reverse order and rotating by180 degrees gives precisely the C1 coordinates.
The new maximal-wall cycle is

    (-1,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),
    (1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),
    (3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1).

The independent author geometry check, which imports no peer checker,
verifies all nonadjacent contacts including touches, every genuine turn,
strict actual mark interiority, exact area, integer points and smooth wall
points. Its values are:

| Room | W | r | Area | J | s_N | k |
|---|---:|---:|---:|---:|---:|---:|
| D | 22 | 9 | 15 | 0 | 4 | 4 |
| D' completed | 20 | 8 | 16 | 1 | 5 | 6 |

The filled room's interior integer points are exactly S,T,(0,-1).
The last is non-A. Filling makes the old convex points (-1,-1) and
(0,-2) smooth; only the former is non-A. The previous four smooth non-A
points remain. This explains J=1,s_N=5,k=6 directly, not by assuming a
wall-count bound on k.

By the independently accepted all-support theorem W<=21,k<=6, D'
illuminates these actual marks. That theorem is stated in
illumination-k4-codex/restricted-theorem-note/theorem.txt and its exact
scope/acceptance is reconciled in construction/baseline-and-gap.md and
baseline-receipts.json. D is dark by the accepted hand proof of the known22
construction. Those proof results are inherited; this check does not rerun
their large certificate chains or infer darkness from a finite ray search.

Therefore existence in D' does NOT imply existence in D for arbitrary r.
This is a genuine existence-level failure of the unrestricted C1 transfer,
not just the failure of one selected path. Its original room has r=9 and
is outside the C1 target restriction. The actual r<=8 candidate remains
unproved and unrefuted. A proof using only the displayed local rectangle
and no further global restriction would also apply here and be invalid.

## 4. C1 alone is not globally available, even beyond the r<=2 bases

One exact hand-defined room is

    [0,20]x[0,4] union
      ([0,4] union [8,12] union [16,20])x[4,12],

with actual interior even-even S=(2,10),T=(18,10). Its maximal boundary is

    (0,0),(20,0),(20,12),(16,12),(16,4),(12,4),
    (12,12),(8,12),(8,4),(4,4),(4,12),(0,12).

It is a strictly simple lattice disk with W=12,r=4. The four reflex corners
occur in two adjacent pairs: (16,4),(12,4) and (8,4),(4,4). Each has a
reflex neighbor. Hence NO reflex corner has the two convex neighbors
required by C1, regardless of isolation or endpoint positions. This
disproves availability of the C1 move throughout the nonconvex class
when the only bases are convex rooms, and still defeats the bare move
after adding all r<=2 rooms as bases.

It does not disprove a scheme with more moves, or an already proved direct
solution for this room. In particular a disjunction allowing ANY already
proved illuminated case cannot be refuted merely by this geometric example.
The statement proved here is only absence of C1 at every reflex vertex.
This is one prerequisite control, not a new comb catalogue or ray search.

## 5. Realignment and justified next repair

C1's geometric reduction and convex base are proved. Its low-r optical
transfer is OPEN; its unqualified extension is false at r=9; C1-only
availability fails at r=4. None of these is a dark target-class example.

A concrete repair of the availability failure is to permit completing a
rectangular notch whose bottom has TWO adjacent reflex corners. In the
displayed r4 control, either exterior rectangle [4,8]x[4,12] or
[12,16]x[4,12] eliminates a reflex pair without moving either endpoint.
That repair avoids exactly the no-convex-neighbors obstruction just proved.
It belongs to this same corner-completion effort; it receives no fresh
discovery clock. It still needs its own global availability proof and
existential optical theorem. More general exterior pockets or endpoint-
containing corridors are not silently covered by these two local moves.

The next substantive issue is whether this expanded completion scheme can
be organized by exterior-pocket topology while remaining strictly simple
and decreasing r, and whether any low-r optical continuation survives.
No positive transfer law has yet been obtained. The native goal stays
active and unfinished; independent review of this milestone is requested.
