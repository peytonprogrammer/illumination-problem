# Preliminary independent challenge of author candidate C1

This reviews the current published candidate snapshot, SHA256 `2c04bd5f87fe21ce809e9d807779bd9a2d05049ba60e6ff3c2a634ed5005249a`, before an author proof/review packet is frozen. It is not a final acceptance of an unprovided optical proof. Author ownership is preserved; these reviewer files are separate.

## Geometric completion and reflex count — ACCEPT as a local conditional statement

Under the stated isolation hypotheses, the old boundary arc A-C-B and its replacement A-(L,H)-B are simple and meet the rest of the boundary only at A,B. The rectangle interior is outside D and has no other boundary contacts. Replacing the old arc by the new arc therefore bounds exactly D union the rectangle, a strictly simple disk. This can also be seen by the rectangle being glued to D along two adjacent sides forming one connected boundary arc, with no extra contacts.

The preceding and following supports make A,B smooth after filling. The old reflex C disappears into the interior. The new far corner is convex. All other turns persist, so r drops by exactly1, W drops by2, and the turning equation is preserved. Original actual interior marks remain interior because the room only gains area. Integer orthogonal walls keep the canonical tiling class and even-even endpoints. Thus the complexity claim has the required strict decrease. No optical implication follows yet.

## Availability countercontrol at r=3 — CORRECT any stronger unconditional availability claim

Use the exact strictly simple orthogonal lattice spiral with boundary

    (2,2),(2,10),(10,10),(10,4),(6,4),
    (6,0),(14,0),(14,14),(0,14),(0,2),

and actual even-even interior S=(2,12),T=(12,2). There are10maximal walls and3reflex corners. In the displayed counterclockwise order its turn types are

    convex, reflex, reflex, reflex, convex, convex, convex, convex, convex, convex.

Thus no reflex vertex has TWO convex neighbors. C1's initial three-vertex condition fails everywhere, before checking rectangle isolation. Translation and axis rotation cannot change adjacency or convex/reflex type. This is an exact room in the target class outside the W<=8/r<=2 base.

The raw geometry checker independently verifies strict simplicity, all10genuine axial turns, interior actual marks, area128 and absence of any convex-reflex-convex subchain. No room or ray search is used. Its certificate is geometric-reduction-c1-prereview-check.py/json.

This rejects the availability assertion "every nonconvex target room admits C1." The author does not currently assert that theorem: its actual induction obligation allows an ALTERNATIVE previously proved actual illumination result. The control therefore identifies a necessary branch of that disjunction, not a contradiction of the candidate's stated existential optical implication. C1 alone with only convex bases cannot cover this room. A valid programme must prove a direct/path theorem for all such uncovered cases or add another globally justified reduction.

For any room having no convex-reflex-convex subchain, every maximal cyclic block of reflex corners has length at least2. If there are b blocks, b<=floor(r/2)<=4 in this target. There are r+4 convex corners, so some convex block has length at least ceil((r+4)/b)>=3. This is a useful exact combinatorial constraint on the uncovered cases; it does not establish a geometrically isolated ear or optical transfer. In particular a long convex run cannot be turned into an endpoint-free ear without further proof.

## Existential optical C1 claim at r<=8 — OPEN

The non-nested completion avoids P1's obstruction to contained deletions, and it preserves endpoint interiority. P2's failed selected-bounce replacement does not reject it. A proof still needs existence of SOME actual original-room ray from the existence of a ray in the completed room. Neither the geometric angle calculation nor the availability control supplies that implication. A bound-sensitive argument or another genuinely optical mechanism is required; it is not legitimate to infer the transfer from these geometry facts alone.

The author is separately checking an r9known22 control. That can test an r-independent strengthening but not falsify the stated r<=8 claim. No verdict of darkness is made for the r3spiral control here. No author discovery allowance has been restarted, and no new reviewer discovery effort was needed for these prescribed hand constructions.
