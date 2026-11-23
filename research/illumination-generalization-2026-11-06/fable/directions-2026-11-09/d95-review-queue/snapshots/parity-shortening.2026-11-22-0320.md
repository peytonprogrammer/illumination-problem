# Shortening a corridor by two can create a legal shot

**Verdict.** The reviewed named examples do not establish a positive-length, one-unit shortening that takes a room with a dark pair to a room lit for all real interior pairs. The proposed monotonicity for individual shots is false in the specified three-chamber skeleton, at arbitrarily large comparable corridor lengths and with all four canonical relations universal. Descent for *existence of some dark pair* remains open. There is no resulting length cap.

## The one-unit question

R22 has a reviewed dark pair and 22 walls. Its manuscript-scale corner abscissas are precisely −1,0,1,2,3,4,5 and its corner ordinates −3,−2,−1,0,1,2,3. All the independent ordered supporting-line gaps are already one. Decrementing one by one would leave that positive-gap shape cell. This observation concerns that coordinate model, not every possible local surgery or rescaled R22. The named edit R22-L1-005 **adds** cell (0,−3), increases area from 15 to 16, and removes two walls. It is not a shortening between two positive lengths of the same separating corridor. D85's length-27 result there is for one source and same-parity lattice targets. It is not an all-real-pairs verdict for the edited room. [Edit geometry](bottom-step.md) · [d85 scope](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d85-shadow-kill/README.md)

D142 and d144 describe the path-dependent R22 fold and corner/orbit exclusions. The named cov4181 pair in d144 is already horizontally lit. D8's R34 edits give marked lattice-pair verdicts, and its dark two-edit control moves a cell while retaining the obstruction. These records supply neither the required corridor comparison nor an all-real lit shorter endpoint. Also a valid dark-to-lit example at W=22 or 34 would disprove a universal assertion including those wall counts; by itself it could not refute a theorem restricted to W≤20. [D8 perturbation scope](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d8-perturbation-test/README.md) · [R22 and cov4181](dyadic-classes.md)

## Exact failure of shot monotonicity in the requested geometry

Use three 3×3 chambers on the same baseline, separated by corridors of width one over 1<y<2 and of lengths X,Y. The marks are S=(2,1) in the left chamber and T=(4+X,1), one unit inside the middle chamber. Shorten X by two, translating the middle chamber, T, and everything to its right two units left. Both mark parities are unchanged.

Fix the **one unoriented primitive line (2,1)**, allow all four physical launch signs, and allow any positive traversal count. The following terminal events exhaust the possibilities. A repeated (position, signed velocity) precludes a later first arrival. The comparison is on the identity cover, not just in one chosen chain or one twist pencil.

| X,Y | Target | Launch outcomes in sign order −−, −+, +−, ++ |
|---|---|---|
| 4,4 | (8,1) | corner, repeat, repeat, corner |
| 2,4 | (6,1) | corner, repeat, repeat, target |
| 28,28 | (32,1) | corner, repeat, repeat, corner |
| 26,28 | (30,1) | corner, repeat, repeat, target |

The checker uses the saved cell-level tracer until a stop, a target or a repeated state. This replays one prescribed direction, with no direction or room discovery. [Exact checker](parity-shortening.py)

**Unbounded extension.** Increasing either corridor length by 12 adds signed transverse travel ±6 to every full traversal of that corridor. Its signed height phase has period two. Any traversal starting in the open mouth therefore resumes at exactly the old physical height and vertical sign. There are no vertical obstacles inside the corridor, its two long walls are smooth, and neither mark is in the insertion. A corner hit at an exit is preserved as well. This transfers absence as well as presence of a hit: compress the extra flight in the reverse comparison, or follow the same successive chamber states. Hence the first two rows hold for X=Y=4+12k before shortening, and X=2+12k, Y=4+12k afterward, at every k≥0. Both rooms have W=20. Each has vertical gcd one and horizontal gcd one since there are widths 3 and Y≡1 mod 3. For k≥2 their areas 27+X+Y exceed 64, hence both are BBBB by the reviewed area criteria. [Geometry and area bounds](uniform-tail.md)

In fact at either length this pair is illuminated by a simple independent shot. Launch to the right with slope 2/(X+2). It enters the first mouth strictly above its lower lip, bounces once on the smooth corridor ceiling at the midpoint in x, then reaches T at height one. Thus the example proves creation of *line visibility* on shortening; it says nothing against preservation of an actual dark pair. It refutes the proposed ordering of directions through a door. A missed line in the long room represents a failed marked affine cusp there; the shorter room has its own marked action, and there is no given common orbit identification.

## Why parity does not give descent

Shortening the unit-width corridor removes two cell sheets. Corner counts in each parity stay fixed, so n=f_x+2q_x+3r_x forces the number q_x of regular swaps to fall by one at **each** site. All four canonical quotient degrees stay one for k≥2. Parity preserves those coarse types in this example, but not the permutations or the registered transport between marks. D151's density theorem is for one marked surface. It compares no affine orbits on two different surfaces. [Local degrees](stretch-stability.md) · [Density theorem](local-global.md)

There is also a quantifier issue with replacing a unit step by an even step. For the dilation-closed real-mark problem, suppose dark-long ⇒ dark-short holds for shortening a *specified* corridor by two above a wall-only threshold. To compare any positive integral lengths L+1 and L, dilate by an even m with mL above threshold; shorten m/2 times, then rescale. The conclusion is dark-long ⇒ dark-short for that *one-unit* shortening too. Consequently, a genuine unit dark-to-lit example in the same wall range and same family would also rule out the uniform specified-corridor even-step descent there. This argument does not apply unchanged to normalized-only rooms, lattice-only witnesses, or a theorem that may choose the other comparable corridor. [Scaling scope](uniform-tail.md)

What remains is a weaker implication at the level of rooms: if the long room really has a totally dark pair, then *some* dark pair survives at *one* permitted shorter geometry, possibly with different marks. Nothing in the single-line counterexample decides it. Even this would give a finite family only with a shortening move for every unbounded shape coordinate, including the types with arms or indentations and no separating two-mouth corridor. No finite census follows from the available results, and none was run.
