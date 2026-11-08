# Physical wall realization does not force a midpoint

## Result

The local physical-geometry premise is insufficient, not merely the abstract-circle premise. Two of the three existing central-circle controls are realizable in the same fixed six-wall L room, with a smooth wall blocker, an invariant ordinary cylinder, and no midpoint relation on the physical covering torus for ANY reflected source/target/blocker images.

Both pairs have direct bypasses. This is not a counterexample to the conjecture that a GLOBALLY essential smooth wall blocker must satisfy a torus midpoint relation. That conjecture would need the global all-connections hypothesis, not just local cylinder separation plus physical realization.

## Fixed physical room and central cylinder

Scale the earlier prescribed L by two so its corners are integral. Boundary:

    (0,0),(6,0),(6,3),(5,3),(5,4),(0,4).

Let c0=(0,0), c1=(6,0), z=(3,4). The path c0 -> z -> c1 reflects at the smooth top wall y=4. It avoids the unique reflex corner (5,3), with squared distances 5 and 1 from its two legs. Its continuation through regular convex corner lifts retraces physically and closes on the four-copy unfolding. The positive clearance gives an ordinary cylinder neighborhood. Its maximal cylinder is invariant under the derivative-minus-identity involution because it contains the fixed corner lifts, and this closed curve is its central core, as in the previously accepted critical-leaf proof.

Parameterize that core by theta modulo one, developed period (12,16):

    physical(theta)=(fold_6(12 theta),fold_4(16 theta)),
    fold_L(v)=min(v modulo 2L, 2L-(v modulo 2L)).

The corner parameters are 0 and 1/2; the two lifts of z are 1/4 and 3/4; the involution is theta -> -theta. The physical fold agrees for theta and -theta.

## Two realized fixed controls

1. theta_s=1/7, theta_t=3/8 gives s=(12/7,16/7), t=(9/2,2).
2. theta_s=2/5, theta_t=1/6 gives s=(24/5,8/5), t=(2,8/3).

For each pair, the two source occurrences and two target occurrences on the central circle lie in opposite components after deleting {1/4,3/4}. Every core arc between those selected occurrences therefore meets a z lift.

The third abstract control put its supposed blocker at theta=3/8, which folds to (9/2,2), an interior point. It fails the physical-wall condition, but the two examples above pass it.

## Direct exclusion of the physical torus midpoint relation

The four-copy unfolding covers R^2/2Z^2. An interior point p has torus images (plus-or-minus p_x, plus-or-minus p_y) modulo 2, with independently chosen signs. The two distinct lifts of z both project to (1,0). A midpoint modulo half-periods requires

    2B-X-Y in 2Z^2

for some source, target and blocker images X,Y,B. Check all sign choices, not only the core's involution pair.

For pair 1, source heights modulo two are 2/7 and 12/7, target height is zero, and blocker height is zero. Thus the vertical residue of 2B-X-Y is always 2/7 or 12/7, never zero.

For pair 2, all vertical residues are 4/15,14/15,16/15,26/15 modulo two, again never zero. Either example excludes the midpoint relation on the actual covering torus, even allowing all four physical endpoint lifts.

The old positive control theta_s=1/8, theta_t=3/8 does satisfy the midpoint test, so the arithmetic test is not rejecting every configuration.

## Why the controls are globally lit

All four physical marks above lie in the convex open rectangle (0,6)x(0,3), contained in the room. The direct segment for each pair stays in that rectangle and avoids z=(3,4). Therefore z is not globally essential.

In fact choose any theta_s in (1/8,3/16) and theta_t in (5/16,7/16). The source and target lie on opposite sides of z along the corner-to-corner quotient arc while staying in the same convex lower rectangle. Thus core separation persists on an open family of physical marks. Within this parameter rectangle the exact midpoint locus is the line theta_s+theta_t=1/2. Its complement is open and dense, giving physical separated, midpoint-free marks. To check the locus, put S=theta_s+theta_t and D=theta_t-theta_s. The horizontal condition is either 6S integral or 6D integral; the vertical condition is either 8S integral or 8D integral. In these ranges, 6S integral forces S=1/2, 6D integral forces D=1/6, 8S integral forces S=1/2, and 8D integral forces D=1/4. Choosing both D alternatives is impossible, so midpoint implies S=1/2; the converse uses both S alternatives.

## Consequence for the research route

A proof of the global midpoint conjecture must use interactions between different physical connections. Local central-cylinder geometry and physical wall realization alone cannot prove it, already in form (B). The missing global step is equally substantive here and for the reflex saddle-connection form (A). The common-cylinder-bypass route remains open.

No new optical discovery search was run. The room and reflecting arc are the previously fixed analytic control; only two prescribed source/target placements were evaluated.

## Recheck

Run `python3 -B check.py` in this directory. `check.json` records exact room coordinates, torus residues, core separation, reflection law, positive reflex clearance, old midpoint positive control and nine formula controls inside the displayed open parameter ranges.

## Independent review

Separate tools-disabled Opus ACCEPTS the two fixed physical examples, complete lift arithmetic, cylinder realization and direct bypasses. Its valid correction was incorporated: the two-parameter family midpoint locus is a line, not isolated points. The nine family controls now explicitly report eight midpoint-free cases and one midpoint-positive case (1/6,1/3), matching that exact locus. Review in `peer-review.txt`; no global-essentiality claim.
