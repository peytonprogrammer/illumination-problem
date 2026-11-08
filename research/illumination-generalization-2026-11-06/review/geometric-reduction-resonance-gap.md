# R3: target-reaching rays need not admit any ear-return resonance

Independent necessary-condition finding, Codex01a1a00f. This is a hand argument with exact prescribed controls, not a discovery search. It strengthens the earlier single-ray P2 obstruction to an entire fixed pair's set of reduced-room witnesses. It does NOT disprove existential illumination transfer or the r<=8 target.

## 1. The precise proposed sublemma that fails

A possible repair of P2 would say: after one reduced-room ray fails the square-ear return condition, choose a DIFFERENT ray to the SAME actual target whose incoming velocity meets that resonance. Even allowing arbitrarily many reflections and all reflection words, that proposed availability of a resonant target-reaching ray is false without extra hypotheses.

Let the reduced room be Q=[0,8]x[0,8], with actual S=(2,2), T=(4,6). Attach the endpoint-free square E=[0,4]x[8,12] along J=[0,4]x{8}. The original D=Q union E has boundary

    (0,0),(8,0),(8,8),(4,8),(4,12),(0,12).

These are canonical orthogonal lattice disks. Original D has r1, reduced Q has r0, and both retain distinct actual interior even-even marks. The full-side ear is geometrically admissible and its deletion strictly decreases r. Thus this is an in-domain low-reflex control for the lifting METHOD, not an r9-only warning.

**All-witness exclusion.** Every legal actual S-to-T ray in Q has a noninteger ratio of horizontal to vertical velocity, including at every horizontal reflection. Consequently NO such ray can satisfy the same-mouth-point/same-velocity square-ear return condition, at any mouth encounter.

## 2. Complete hand proof, without a reflection cutoff

Unfold any finite legal rectangular-room path. Reflections in x=0,8 generate target x-images epsilon_x*4+16n; reflections in y=0,8 generate target y-images epsilon_y*6+16m, where epsilon_x,epsilon_y are signs and n,m integers. This contains every image from every finite wall word. The unfolded ray starts at S and is straight with its initial directed velocity.

Its displacement therefore satisfies

    Delta_x = epsilon_x*4+16n-2 = 2 mod4,
    Delta_y = epsilon_y*6+16m-2 = 0 mod4.

Delta_y is never zero: the two possibilities are4+16m and-8+16m. Delta_x is never zero either. If Delta_x/Delta_y were an integer, Delta_x would be divisible by4, contradicting its residue2. Thus u/v is never an integer for any legal connecting ray. At actual walls only velocity signs change, so integer/noninteger status of that ratio is unchanged at any later horizontal contact.

For this square ear w=d=4, the already derived necessary and sufficient matching condition is d*(u/v) in wZ, namely u/v in Z. Hence no target-reaching ray of Q satisfies the required resonance. The proof covers arbitrarily many reflections, all realizable finite words and even the superset of all image sign/integer combinations. No finite unsuccessful ray list is used.

The result excludes the existential RETUNING SUBLEMMA: there need not exist any resonant Q witness, even though Q is illuminated. It is not merely a failure of one chosen Q witness.

## 3. Explicit smooth witness and the failed replacement

Q has the smooth one-bounce actual path

    (2,2) -> (7/2,8) -> (4,6),

with incoming u/v=1/4. The bounce is in the relative interior of the ear mouth J and the reduced top wall. Both legs are strictly inside Q away from that reflection. The target-reflection image is (4,10), making the exact shooting slope (4-2)/(10-2)=1/4.

In original D, the ray continues through the open mouth instead of reflecting there. Its genuine-wall prefix is

    (2,2) -> (4,10) -> (7/2,12) -> (5/2,8).

The first two intermediate points are respectively a smooth vertical-ear-side and a smooth roof reflection. The final point is an interior mouth exit, with velocity proportional to(-1,-4), rather than the reduced reflected velocity(1,-4) at the original mouth point(7/2,8). The unfolded exit x is7/2+2*4*(1/4)=11/2; folding into width4 gives5/2 with the opposite horizontal sign. This is a legal excursion, not a corner accident.

## 4. Why no actual transfer is disproved

The actual pair is directly illuminated in BOTH Q and D by the segment (2,2)->(4,6), which stays in the original square. That witness never uses the artificial top mirror. Therefore the existence-level implication Lit(Q;S,T)=>Lit(D;S,T) is true in this example. Another global ray or a ray avoiding J can succeed even though no resonant witness exists.

A general reduction proof may exploit such avoidance, a different interaction with the modified region, or a genuine low-reflex rerouting theorem. What it cannot assume is that switching among Q's target-reaching rays will automatically supply the required local resonance. Excluding only one selected word would be weaker than the all-witness arithmetic obstruction proved here.

## 5. Fixed-target directions are not an open shooting interval

More generally, for a fixed room, source and target and one finite reflection word, unfold the ACTUAL target through that word. A legal ray of positive length has a uniquely determined initial direction from the source to that image. If the image coincides with the source, that word yields no positive straight flight. Since there are countably many finite words, the set of exact target-reaching directions is at most countable; in particular it contains no open angle interval.

Strict positive wall/corner clearances do give an open interval of directions following the same finite PREFIX itinerary. They do not imply that all those directions hit the fixed point target. Varying a direction in that interval generally moves its endpoint away from the actual target. The rectangle example proves that, even when MANY exact target-reaching directions are available, a prescribed arithmetic matching set can be missed by ALL of them. Countability or a qualitative density assertion cannot replace a proved intersection with the required compatibility set.

## Evidence and programme frontier

geometric-reduction-resonance-gap.py/json independently validates the two raw polygons, actual marks, direct paths, the reduced one-bounce path, the original excursion with correct axis reflection signs, and the symbolic residue equations. It uses no author checker and no room/orbit/ray census. The all-words result is the hand congruence proof, not sampling.

This leaves the full orthogonal r<=8 illumination goal unfinished. Geometric H/V/C1 availability remains independently accepted. A successful optical step must control target attainment and avoidance/phase constraints JOINTLY, rather than retune an arbitrary reduced witness under an unsupported resonance-existence assertion. General nonorthogonal canonical45 rooms remain a separate open scope.
