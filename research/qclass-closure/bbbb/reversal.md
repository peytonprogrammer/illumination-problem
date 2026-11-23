# Lighting paths with a prescribed horizontal reversal

**Result.** A vertical wall can be included in the column placement test by recording a second traversal of the reflecting column and imposing an open height window at the turn. This works at a partly exposed internal wall as well as at an extreme back wall. It explains all three named witnesses below. For the DB55 pair the same construction guarantees a genuine right-wall reversal for every real corridor length ℓ>5, keeping the marks fixed relative to their chambers.

## Reconstructing the DB55 witness

D69 stores the family totals and its deterministic witness selector. Here is the reconstruction from that selector, independently replayed at its single derived velocity. The left room is [0,5]×[0,5], the corridor is [5,8]×[2,3], and the right room is [8,13]×[0,5]. The pair (1,1),(9,1) has no x-monotone path by the [midpoint argument](chain-criteria.md). Equal endpoint heights make a y-monotone path horizontal, which also misses the door.

D69's first back-wall branch reflects the target across x=13 to (17,1). Its horizontal travel is 16 and its column half-period is 5. The selector starts with even vertical displacements −78, −76, −74. At the first mouth these fold to heights 3/2, 2, 5/2 respectively; only the third is inside. Thus the successful slope is −74/16=−37/8. In the corridor the unfolded rise is −111/8; folding about 2 and 3 gives exit height 21/8 with downward velocity. In the doubled right chamber the remaining rise is −333/8. Its developed endpoint has height −39, which folds to 1.

| Physical portion | Contacts, in order |
|---|---|
| Left chamber to x=5 | Bottom, top, bottom, top (walls y=0,5). Enter at y=5/2. |
| Corridor to x=8 | Alternate y=2 and y=3 seven times each, starting at y=2. Exit at y=21/8. |
| Right chamber before reversal | Alternate y=0 and y=5 for five contacts, starting at y=0. At x=13 the developed height is −41/2, which folds to **1/2**. |
| Right chamber after reversal | Hit y=5, then 0, then 5. Reach **(9,1)** moving left. |

There are 26 horizontal-wall contacts and one vertical-wall contact. No turn occurs at a corner. [D69 selector](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/decomp.py) · [D69 back-wall verification](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/verify_b.log)

## A criterion for a prescribed sequence of columns and turns

Split the room into full rectangular runs at vertical lines through its vertices. Prescribe a finite walk through these runs, with partial first and last legs allowed. At each event either cross to an adjoining run through an open overlap, or hit the relative interior of an actual vertical wall and traverse the incident run in the opposite horizontal direction. For a turn choose an open subinterval wholly on that wall. Distinguish multiple visits to a run. All horizontal travel distances d_j are positive and are measured in the developed coordinate, which increases even when physical x decreases.

Run j has bottom l_j, period P_j twice its height, and E_{j,e}(y)=l_j+e(y−l_j) for e=±1. Choose a sign e_i for each event, including endpoints. With constant signed developed slope s, physical vertical velocity at event i has the sign of e_i s. With y₀=S and y_n=T the exact equations on these sheets are

    d_j s = E_{j,e_j}(y_j) − E_{j,e_{j−1}}(y_{j−1}) + P_j m_j,    m_j integer.

An integer solution with every event height strictly inside its specified window is a legal path with the prescribed reversals. In each full run fold the segment between the two stated vertical images. Both possible images have the correct height, and the common e_i makes the vertical velocity agree across the event. A crossing keeps horizontal velocity; a wall reflection reverses it. An internal reversal needs only its local physical wall interval. Other parts of the room at the same x can be open.

**Width test.** At a turn, runs j and j+1 are the same physical run traversed in opposite horizontal directions, with the same bottom l and period P. The open turn window must lie on a vertical wall facing that run. Write z_i=e_i y_i. The bottom-dependent terms in these equations are constants. After eliminating s the lattice generators for z_i are exactly G_ij=P_j(A_i/X−1_{j≤i}), where A_i is accumulated absolute horizontal travel and X the total. The windows become e_i times their physical intervals and retain their widths. Consequently the projected-index width inequalities in [the chain criterion](chain-criteria.md) guarantee a solution to this prescribed walk, including every turn. Signed windows may also be checked directly against the affine lattice when the sufficient widths fail. This reduces a specified reversal route to integer placement; choosing a successful walk in an arbitrary BBBB room remains open.

## One reversal chamber as a reusable length test

Suppose a horizontal corridor of width w joins two full rectangular chambers. Prescribe a right-chamber turn at its far vertical side, restricted to a smooth wall window K. Let a be the source-to-mouth horizontal distance on the left, c the target-to-mirror distance on the right, and b=c plus the mirror-to-mouth distance. Trace from the source and backward from the target. On any chosen unfolded branches the admissible slopes satisfy three open interval conditions: the left mouth height lies in its opening, the right mouth height lies in its opening, and the height after backward travel c lies in K. Compute each by intersecting the affine unfolded height with a reflected or translated copy of the relevant opening. The two right-hand tests use the same unfolded target and signed slope. The mirror reverses horizontal velocity only, so the backward travel to the right mouth is b. A full rectangle supplies no other obstacle.

Let Δ be the width of a common interval of these three tests. In corridor phase coordinates (height relative to its bottom, signed by the sheet orientation), the left mouth coordinate has derivative a and the required right coordinate has derivative −b with respect to signed developed slope. Matching across the corridor requires their difference plus ℓs to be a multiple of 2w. Thus **(a+b+ℓ)Δ>2w** guarantees a genuine reversal inside K. For shorter lengths test the actual open phase interval for a multiple of 2w. This is the earlier corridor length test with an extra mirror window; omitting that window can admit a corner hit or an escape through an opening.

## An explicit length condition for DB55

Keep the source (1,1), let the corridor length be ℓ, and keep the target one unit inside the right chamber at (6+ℓ,1). Use the full right wall, now x=10+ℓ. The forward left leg travels 4; the backward right leg travels 4 to its mirror and 5 more to its mouth. Write s=−37/8+t. The physical mouth heights on the sheets found above are

    x_left=5/2+4t,     y_right=21/8−9t.

Both lie in (2,3) for −1/24<t<5/72. At the mirror the backward developed height is 1−4s=39/2−4t, strictly between 15 and 20 throughout, so it misses the mirror corners. These formulas include all chamber reflections by unfolding. In the unit corridor the matching condition is x_left+ℓs−y_right ∈ 2ℤ. Its slope with respect to t is 13+ℓ. The allowed t-interval has width 1/9; its image has length greater than 2 for ℓ>5. Thus some interior slope matches both position and direction. At the original length ℓ=3 the actual placement at t=0 is −14, which explains why the shorter room also works. The length condition is sufficient.

## Two internal turns in cov2929 (one per pair)

D72 already records both direct lighting lines. Exact replay of these lines in D69's cell diagram gives the following complete reflection lists, in order from the source:

| Pair | Initial velocity | Physical contacts |
|---|---|---|
| (3,1) to (5,3) | (−2,3) | **(2,5/2)**, (3,4), (13/3,2) |
| (3,3) to (5,5) | (2,3) | (11/3,4), (5,2), **(6,7/2)** |

In the first path the exposed part of x=2 at height 5/2 acts as the mirror. After reversing, the ray crosses x=4 at height 5/2 through the overlap (2,4). In the second path the ray crosses x=4 at height 7/2, reverses at the exposed part of x=6 at height 7/2, and returns to the target. In each case the bold contact lies strictly inside a vertical wall. The remaining contacts are smooth horizontal reflections within the runs (a contact at an artificial unit-grid seam is allowed when the physical wall is smooth). Consecutive columns with identical runs can be merged. These are placements for the signed test, even though the simple left-to-right test fails. The room is a Q-class stress test for turning. [D72 saved lines](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d72-cylinder-test/cyl_H40.json) · [D69 cell diagram](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md)
