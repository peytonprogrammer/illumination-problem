# Filling the bottom step opens a path through an old reflex corner

D8 already contains this exact edit as R22-L1-005. Its 16 cells equal the R22 base cells plus (0,−3), in manuscript coordinates. Its boundary has 20 maximal walls and eight reflex vertices. The direct diagonal between S=(0,0) and T=(2,2) still hits the reflex vertex (1,1).

The archived marked-pair record gives the unfolding vector (24,−16). D8's perturb.py stores the raw vector w after its certify routine finds the physical sign choice ws. From S the certified full-time physical launch is (−24,−16). The original and edited trajectories first differ at (1,−2), on the third primitive step: the original trajectory terminates at a reflex corner, whereas the edited room permits straight continuation there. In the edited room the path has already returned to S after its second primitive step. Removing that loop gives the simpler developed displacement (18,−12), or six steps of initial primitive velocity (3,−2).

For that shortened path, the first two bounces are (1,−2/3) and (0,−4/3), both unchanged smooth walls. The ray then reaches (1,−2) moving southeast. The old room already contains the northwest cell it leaves and the southeast cell it enters. Adding the southwest cell fills the missing quadrant, turning the old reflex corner into an interior point. Passage through that point becomes legal even before the ray first enters the added square. The six successive lattice hits of the shortened shot in the edited room are (1,−2), (0,−2), (1,−2), (2,−2), (−1,0), (2,2). Intermediate smooth-wall reflections between lattice hits are implicit.

Both D8's Fraction tracer and its independent surface.segment checker accept both physical displacements in the edited room and reject both in R22. To reproduce, load the R22-base and R22-L1-005 cell sets from rooms.json, run tracer.trace(cells,(0,0),D) and certify.second_check(cells,(0,0),(2,2),D) for each listed displacement. The first returns the endpoint, legality and lattice hits. No new direction enumeration is needed.

The old darkness proof requires legal paths to avoid original vertices. This specific route violates that condition exactly at its first visit to (1,−2). The smoothed convex corner at (1,−3) is a separate change and is never visited by this witness. The computation establishes the role of this reflex corner for one path and one edit; it supplies no universal lower bound.

[D8 records and checking method](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d8-perturbation-test/README.md)
