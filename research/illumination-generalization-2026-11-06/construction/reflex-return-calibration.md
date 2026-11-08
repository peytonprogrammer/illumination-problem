# A complete lattice family in the previously uncovered reflex-coalescence stratum

A26 positive calibration. Pending independent review of this additional packet; the general reflex-coalescence theorem has separate independent acceptance. This is not the universal W21 theorem.

Use the sixteen-wall P0 and O=(2,2) in reflex-visibility-obligation.md. For each INTEGER lambda>=2 put P_lambda=lambda*P0 and actual marks

    S_lambda=(2lambda-2,2lambda+2),
    T_lambda=(2lambda+2,2lambda-2).

Both marks are distinct interior A points. P_lambda remains canonical45, strictly simple and sixteen-walled at every integer lambda. Their normalized limits coincide at the REFLEX corner O, so strict regular-contact limiting-witness and off-trace coalescence certificates do not apply.

## Analytic tail for every real lambda>8

Let E4 be the bottom wall y=-4lambda, E6 the hook top y=-3lambda, and E5 its left end x=-2lambda. The path starts at the ACTUAL S with velocity (-1,-3) and follows the physical wall word

    [4,6,4,6,4,6,5,4,6,4,6,4,6,4].

Its first six contacts have x=-j*lambda/3-8/3, j=0,...,5, alternating y=-4lambda,-3lambda. The next contact is

    (-2lambda,-4lambda+8),

strictly in E5 when lambda>8. The next bottom contact is (-2lambda+8/3,-4lambda). The remaining six alternating contacts have x=-j*lambda/3+8/3 for j=5,4,...,0, alternating top and bottom. The final contact is (8/3,-4lambda), after which velocity (1,3) reaches the ACTUAL T.

Every top contact has -2lambda<x<0, and every bottom contact has -2lambda<x<2lambda, for lambda>8. The first leg has equation y=3x-4lambda+8. At y=2lambda it has x=2lambda-8/3, inside the top arm; at y=0 it has x=(4lambda-8)/3, inside the central/bottom arm; at y=-3lambda it has x=(lambda-8)/3>0, and it reaches the first bottom contact inside the hook. Thus it crosses each actual arm through an interior aperture, not through a missing quadrant or wall. The hook legs remain in its rectangular strip. The final leg has y=3x-4lambda-8: it exits the hook into the bottom arm at x=(lambda+8)/3>0, crosses y=0 at x=(4lambda+8)/3<2lambda, and crosses x=2lambda at y=2lambda-8 in the right arm, before reaching T. These inequalities prove containment and exclude every extra wall contact for all real lambda>8.

The unfolded target under this palindrome is 2*(-2lambda,-10lambda)-T=(-6lambda-2,-22lambda+2). Its displacement from S is (-8lambda,-24lambda), so the chosen direction and final target equality are exact. Total affine travel time at velocity magnitudes(1,3) is 8lambda. Both split contacts near the remote corner have positive distances8 and8/3 along its physical walls; no corner is hit.

The independent symbolic algebra in reflex-return-symbolic.py also expresses EVERY ray-wall first-hit decision as one of975 rational affine sign predicates in lambda. All nonzero roots have absolute value<=8. Its tail sign audit verifies the complete14-reflection actual path for ALL real lambda>=10, a conservative computable cutoff. The sharper lambda>8 statement follows from the hand inequalities above, not sampled values. The checker output and all coefficients are frozen in reflex-return-symbolic.json.

## Exact finite lattice prefix

For lambda=2,...,8 the files reflex-prefix-check.json/log give actual finite path certificates, including every rational contact, the actual source/target and the wall word. The discovered witnesses are:

    lambda2: direction(1,-2), word[2] (1 reflection);
    lambda3: direction(-1,-1), word[8,12,11,8,12,3,7,4,3,7] (10);
    lambda4: direction(1,1), word[15,14,13,2,1,0] (6);
    lambda5,6,7,8: direction(-1,-1),
      word[8,12,11,9,11,10,9,11,12,3,4,6,5,4,6,4,3,7] (18).

Each was checked using exact rational FIRST-hit times against all sixteen actual walls, with every corner excluded and target arrival tested strictly before the next wall. There are no negative/darkness inferences. Discovery was bounded to these seven prescribed members, maxnorm10 and250contacts per direction, and stopped on the first positive witness for each. The original aggregate A26 deadline includes setup, discovery and validation; it was not renewed.

Together with the analytic tail, these finite certificates cover every integer lambda>=2 in this fixed marked family. Independent peer validation of the finite certificates and hand tail is required before the complete-family claim is treated as accepted. It is a calibration of a new reflex-corner mechanism and an uncovered degeneration, not a substitute for classifying every W<=21 geometry or every actual pair.
