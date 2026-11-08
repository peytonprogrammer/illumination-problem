# Commensurate widths: exact copy induction for witness propagation

Supplement to the frozen A21 candidate. Same original effort and deadline; independent review pending. This leaves the frozen original unchanged and proves the stronger statement for unequal COMMENSURATE widths within the same fixed three-chamber/two-neck family.

## Statement

Assume fixed positive neck widths w1,w2 have a common positive multiple H:

    H/w1 and H/w2 are positive integers.

Keep arbitrary fixed orthogonal chambers, arbitrary fixed vertical mouth origins and the actual opposing marks. Let Lj(lambda)=pj*lambda+cj, where pj are nonnegative integers, not both zero. If one valid parameter lambda0 has any finite actual corner-avoiding illuminating path, then EVERY sufficiently large real parameter has such a path. No one-pass condition is imposed. In particular all integer or rational widths qualify after choosing H; no bound on H is claimed.

The A21 fixed-buffer repartition is retained: absorb a small fixed rectangle from each end of each neck, choosing the cuts away from the finitely many witnessed horizontal reflections. It changes no physical room and ensures every cut crossing is transverse and strictly inside its aperture. The growth coefficients pj are unchanged. All chamber blocks and actual source/target words are finite and stable in their input slope and phase. Each neck visit is a complete traversal because its horizontal velocity cannot reverse there.

## Reference charts and the exact arithmetic identity

Choose developed coordinates with the actual S at (0,0), initial horizontal velocity positive, and normalize its magnitude to1. Let tau0 be the witness slope. At every entry/exit of a buffered neck, and at the final actual T image, the cumulative developed abscissa is

    X_i(lambda)=r_i*lambda+c_i,
    D(lambda)=q*lambda+C,

with nonnegative integers r_i, positive integer q and fixed real c_i,C. Each full traversal of neck j increments r_i by pj. Across a fixed chamber block r_i is constant. The final coefficient is q=sum_j nj*pj>0, where nj are the witnessed traversal counts, both positive.

Fix the ACTUAL fully unfolded reference copies of all these blocks, including every witnessed neck winding. Their vertical charts are specific affine isometries with fixed signs, not merely projection classes. Let Y0=tau0*D(lambda0) be the reference actual-T image ordinate. For any integer z set

    tau_z=(Y0+2Hq*z)/D(lambda).

Choose z nearest to the real value making tau_z=tau0, so

    |tau_z-tau0|<=Hq/D(lambda).

Put e_i=c_i-r_i*C/q. The exact identity is

    tau_z*X_i(lambda)-tau0*X_i(lambda0)
       =2H*r_i*z+e_i*(tau_z-tau0).                 (*P)

Define the proposed new copy of each portal/chamber chart by translating its reference chart VERTICALLY by exactly

    2H*r_i*z.

After subtracting this translation, the actual line's height at that portal differs from the reference height by just e_i*(tau_z-tau0). Thus there are finitely many continuously small local-coordinate changes, with all reflection signs retained. The following induction verifies that these proposed charts are physically consistent, rather than assuming modulo agreement is enough.

## Copy induction through chamber blocks and necks

At the initial source chamber, r_i=0. Its chart is unchanged, its starting point is the actual S, and its direction varies from tau0 to tau_z. Finite strict word guards realize the initial block for sufficiently small slope change.

Across any fixed chamber block, the input and output coefficients r_i are equal. The proposed vertical translation is therefore the SAME at both ends. Translating the whole unfolded chamber copy by this constant preserves its actual fixed reflection word and signs. The differences in local line heights at its two ends obey ordinary straight-line propagation because their e_i difference equals the fixed developed horizontal block distance. Openness of the finite witnessed contacts and mouth ordering preserves the block. This includes returns to the same mouth and any finite number of true reflections inside the chamber.

Across a traversal of neck j, r_out-r_in=pj. The proposed outgoing copy translation minus the incoming translation is

    2H*pj*z = 2wj * ((H/wj)*pj*z).

This is an EXACT integer multiple of that particular neck's true unfolding period. It is therefore an allowed change of neck winding, retaining the reference entrance and exit fold signs. With those copies chosen, identity (*P) supplies the actual continuous entrance and exit ordinates of the straight developed segment across length Lj(lambda). No independently chosen angle or ordinate is spliced in. For small enough slope change both are in the same strict half-period branches as the witness. The segment folds to a legal finite traversal; any intervening horizontal contacts are smooth actual wall points. It cannot encounter an artificial vertical cap. Nonnegativity of the physical number of reflections is enforced by the monotone vertical developed segment and the entrance/exit sheets: those sheets contain its endpoints, and the line crosses exactly the intervening horizontal levels. This remains true for either sign of slope. If tau0=0, the reference has no neck horizontal reflections; the same strict-coordinate construction remains valid.

These steps prove the full itinerary inductively. They also show why a common multiple is sufficient, even though the two neck periods differ. There is no assumption that all possible target images form a single common period; the proof constructs a valid subset of images from the supplied reference witness.

## The actual target and eventual threshold

The terminal chamber block has coefficient r_i=q: no neck remains to be traversed. Its entire actual reference chart, including its actual T image, is translated by exactly2Hq*z. The developed final abscissa is D(lambda), and the chosen line endpoint is exactly

    (D(lambda),Y0+2Hq*z).

It is the translated actual T image, with the reference terminal reflection signs. Thus the target is reached by equality in the realized chart, not inferred from congruence alone. The backwards actual-T word has the required direction and strict mouth ordinate; the finite word guards and exact line endpoint preserve it.

Choose eta>0 such that all finitely many chamber-block contact/ordering and cut-phase guards survive the local perturbations e_i*(tau-tau0) when |tau-tau0|<eta. Such eta exists from the nonsingular finite buffered witness. For D(lambda)>Hq/eta, the chosen z satisfies this condition. Since D=q*lambda+C tends to infinity, this holds for every sufficiently large real lambda. All neck lengths remain positive after lambda0 because pj>=0.

This proves the stated propagation lemma for commensurate widths. It imports no new literature or numerical evidence. The equal-width A21 statement follows by H=w. The stronger, explicitly realized-copy induction also identifies the precise invariant behind the original modulo argument.

## Research implication and limits

The accepted A20 strip theorem leaves finitely many integer-offset length rays for each FIXED integer-width/chamber/mark family. The present candidate would reduce eventual illumination on each such ray to ONE actual finite certificate anywhere on it, permitting arbitrary finite repeated passages. It does not provide the certificate, bound the threshold or cover the finite small parameters. Neither the chambers nor the marks may move except by their prescribed rigid translations.

Common-multiple existence fails for arbitrary irrational width ratios, so that extension is not claimed. More than two necks, diagonal chambers and arbitrary global atlas generators are outside this assigned scope. The cap-free W<=21 theorem remains OPEN, and independent acceptance of this supplement is required before using it as a lemma.
