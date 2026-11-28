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

## Census-wide fold test and certificate test (2026-11-27 23:48 HST; approved by Daniel)

Scope: every stored census disc with at least two marks. d237 list: 832,942 discs, W = 22 to 26, area <= 16. d236 list: 552,166 control discs (touching or overlapping), W <= 20, area <= 16. Embedded W <= 20 rooms aren't stored and weren't run.
Controls: link-based moves equal the coordinate-based ones on 1,589 embedded rooms. Marks found reproduce both census pair counts exactly (1,015,031 and 857,156). The dark room gives 5 blocks.

Fold test (foldtest.py; lists in folds-d237.tsv, folds-d236.tsv):
- d237: 66 of 832,942 discs fold (0.008%). Embedded W = 22: 8 of 491,310, and the dark room is one of the 8. Embedded W = 24: 54. Touching W = 24: 4. W = 26: none.
- d236: 82 of 552,166 fold (0.015%).
- Prediction (under 1% fold, 70%) held.

Certificate FP for a same-class pair S, T: an invariant partition of the cells (single cells allowed) whose quotient moves for the other three classes have no 2-cycles, with S and T over different base points.
Why FP gives darkness (sketch, unreviewed): a path from S first meets a lattice point of another class. With no quotient 2-cycles, that point is a corner or sends the base path straight back. So the path only meets class-a points over the base point of S.
Certificate test (fp.py): 167,043 same-class pairs in the two lists. FP holds for exactly one, the dark pair, with the 5-block partition. Prediction (75%) held.

Scaled copies of the dark room, scales (3,1), (2,1), (1,3), (3,3): the pair stays unreached, the room still folds, but FP on the unit lattice fails. So FP must be stated on the coarsest lattice that contains the vertices and the marks. Predicted before the run.

Limits: one dark pair in the data. The tests show FP never fires on a lit pair, and folding is rare. They can't show that every dark pair has a certificate.

Conjecture C: in a strictly simple orthogonal lattice room, on the coarsest lattice containing vertices and marks, a pair is dark exactly when it is a same-class pair with an FP certificate.
Goal from C: (A') no room with W <= 20 carries an FP certificate, at any area. (B') no certificate implies lit.
