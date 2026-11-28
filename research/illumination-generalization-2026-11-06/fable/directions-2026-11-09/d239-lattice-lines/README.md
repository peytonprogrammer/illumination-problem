# d239: working backward from the goal (coordinator sketch, 2026-11-27 23:32 HST, unreviewed)

Daniel asked: if a proof exists, how might it work? This file records the answer and three exact checks. Nothing here is reviewed.

## Constraints a proof must meet
1. A dark room exists at 22 walls. So a proof for W <= 20 must use a property that the dark room lacks. Chord selection never names one.
2. The ledger has 8 turn words at W = 10 and 3,260 at W = 20. A proof can't go word by word.
3. Lattice rooms at every size are the same as rational rooms with rational marks (scale each axis). The lattice restriction buys nothing at large size.

## Formulation (standard covering theory, restated for rooms)
- Lattice lines: S lights T exactly when one primitive direction carries S to T in k primitive steps, with no corner at the lattice points between. Wall points reflect.
- Cell group: label the unit cells. For each parity class c of lattice points, g_c turns a cell half a turn about its class-c corner, in the billiard sense (interior point: opposite cell; wall point: the neighbour; convex corner: fixed; reflex corner: a 3-cycle). The doubled room covers the pillowcase with branch data (g_a, g_b, g_c, g_d). G is the group they generate.
- A block system of G is a way to fold the room onto a smaller base.

## Checks (exact, named rooms; predictions in PREDICTION.md)
- lines.py: 22-wall room: its pair isn't reached (control). Pyramid (4,5,12;3,4,1,2), area 73, all 52 sources: 2,008 different-class pairs all k = 1; 644 same-class pairs all k = 2. Gap room, area 285, 3 sources: 485 at k = 1, 145 at k = 2. Both predictions held (50%, 35%).
- cellgroup.py: 22-wall dark room: G is imprimitive, 5 blocks of 3 cells. Both pyramids: G primitive, with one class holding a single reflex corner, so g_c squared is a 3-cycle and G contains the alternating group (Jordan).
- Sample of 434 embedded rooms from the d237 job list (every 1,500th line, W = 22 to 26): all primitive.

## Proof shape this suggests
Goal <= (A) + (B).
(A) Rooms that fold: darkness comes from the base. Earlier notes prove folded parity rooms need at least 22 walls in the 45-degree class; the orthogonal statement isn't written.
(B) Rooms that don't fold are fully lit. Step 1: G primitive plus a 3-cycle gives G >= Alt (Jordan; with several reflex corners per class, use minimal-degree bounds, which need large area). Step 2, open: from G >= Alt to a lattice line from S to T. In group terms: some tuple in the pure braid orbit of (g_a, g_b, g_c, g_d) puts S and T in one corner-free stretch of a dihedral orbit. The k <= 2 data says short lines suffice.
Conjecture to test first: every dark pair sits in a room with imprimitive G, or in a parity room.

## Literature (checked 2026-11-27 23:32 HST)
- Wolecki, arXiv 1905.09358: finitely many dark pairs per rational polygon; 22-gon example.
- de Winter and Tokarsky, arXiv 2611.13226: lower bounds inside classes defined by the corner condition; whether fewer than 24 sides can work in general is listed as open. Already in the project notes.
- No use of the cell group or primitivity found in four project notes searched or in two web searches. That is a thin search.
