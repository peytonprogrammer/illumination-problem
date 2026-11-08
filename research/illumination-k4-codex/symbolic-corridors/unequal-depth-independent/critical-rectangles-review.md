# Critical-line rectangle algebra independently accepted

Scope: normalized positive depths a,b,A>a,B>b, every one of the four pairs assigned to one of the ten critical lines. This covers critical-line-only support rectangles. Mixed finite-point rectangles and optical illumination remain separate.

The independent checker enumerates all 10,000 assignments. It solves by successive intersection of an affine origin/basis with each hyperplane, using the last nonzero parameter for substitution. Strict feasibility uses elimination of the last parameter with positive integer/rational multipliers. For strict affine inequalities, elimination is equivalent: every positive lower bound must be strictly smaller than every negative upper bound; one-sided variables impose no additional condition. Zero constant inequalities must be positive. Thus arbitrary real feasibility, not a grid test, is decided.

830 assignments are inconsistent; 8,646 consistent assignments fail strict positivity; 524 assignments are feasible. Canonical row spaces deduplicate these into 90 lines and 288 isolated points. No feasible affine set has dimension two or higher. Every published affine expression satisfies every equation, has the correct full solution dimension, and has precisely the recorded open interval. Infinite bounds are preserved.

The common blind sets were intersected as complete unions of segments and points, not sampled only at square corners. For all feasible assignments every nonempty intersection consists entirely of singleton square corners. All reported family blind sets agree, including duplicate representations of each family. Isolated points can admit different assigned line representations and hence different circle-blind metadata; that metadata is assignment-specific and is not asserted to describe actual finite-orbit failure.

Exactly 16 families have one effective equality IDENTICALLY (a=b, A=b, a=B or A=B). They are fully closed by the already accepted equal-effective-depth transfer. A family is not removed merely because an equality occurs at one parameter. Of 24 families with a common blind corner, 16 remain after that removal; all 74 other families remain in the later joint-margin scope. This is accepted algebra only and does not establish illumination or darkness for any residual room.

Reproduce: python3 critical-rectangles-check.py. The checker imports no peer executable. All three peer source pins match the frozen hashes. No discovery effort or new room search was performed.
