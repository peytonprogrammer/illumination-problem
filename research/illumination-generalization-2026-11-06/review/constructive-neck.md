# Constructive arithmetic entry beams for the accepted neck theorem

Candidate algorithmic supplement; independent review pending. This specializes the accepted long-neck theorem to rational-coordinate orthogonal chambers and rational actual interior marks. It makes the chamber-dependent threshold effectively obtainable with exact arithmetic. It neither bounds that threshold or runtime in W nor resolves the uncapped canonical45 theorem.

## Claim

Under the accepted opposing-chamber/mouth hypotheses, if every chamber vertex and both marks have rational coordinates in the common orthogonal frame, a terminating exact procedure returns rational a,b,alpha,beta, a sign sigma, a rational signed open interval I of positive length, and a rational sufficient L0. For every real L>L0 the accepted integer-phase formula gives an ordinary finite actual S-to-T_L connection. With rational L, its entire finite connection can be constructed and verified with rational arithmetic.

The procedure does not enumerate directions, rooms, k or sizes. It uses the ONE fixed positive magnitude sqrt(2) in each closed auxiliary chamber, then certifies a finite interval around it. Its termination is mathematical for each fixed valid input; no uniform complexity bound is asserted. An implementation stopped by an effort timeout would be unfinished, not a disproof of termination or an optical counterexample.

## 1. Why this particular direction is admissible

An axis reflection in a rational wall sends every rational point to a rational point. Therefore every finite developed corner image and every finite developed image of a rational mark has rational coordinates. A nonzero vector between such points has rational slope or is vertical. Consequently no saddle connection and no finite actual-mark-to-corner trajectory has absolute slope sqrt(2). Zero developed vectors cannot represent positive-length straight trajectories.

The same primary minimality input independently audited in long-neck-independent.md applies: in these arithmetic translation surfaces, all saddle-connection directions are rational; the torus case has rational period directions as well. Hence the fixed irrational direction is minimal. The exact trajectories from the actual rational marks have no genuine or removable corner hits. Each reaches the relative interior of its designated mouth in finite forward time by the incoming flow-box argument. Choose any initial sign states with that magnitude; in the controls they are (1,sqrt(2)) on the left and (-1,sqrt(2)) on the right.

This uses rational COORDINATES, not merely rational angles, slopes or Euclidean wall lengths. It does not extend the fixed-sqrt(2) claim to arbitrary real chamber data.

## 2. Exact first-mouth computation

Coordinates, velocities, collision times and comparisons all lie in Q(sqrt(2)). Represent each element uniquely as p+q*sqrt(2), p,q rational. Addition, multiplication and division use rational operations; division by p+q*sqrt(2) uses norm p^2-2q^2, nonzero unless both coefficients vanish. Signs are exact: equal-sign coefficients determine the sign immediately, and opposite-sign coefficients are compared by p^2 versus2q^2. There is no floating-point approximation of a direction, wall contact or event order.

At each step compute the positive time to each actual horizontal/vertical wall line, retain intersections within that finite wall, and take the exact earliest event. A tie would be an actual corner, already excluded for the fixed irrational direction. Stop at the FIRST relative-interior mouth hit, before any auxiliary cap reflection. Otherwise reflect the relevant component. The primary argument supplies finite termination; the algorithm imposes no reflection cutoff. Record the finite word and the exact contacts.

For the outgoing chart after each reflection, reflect the previous virtual source in that physical wall. Starting from the actual rational mark, all such virtual points remain rational. The last one is the rational virtual source/target used in the accepted neck theorem.

## 3. Extract a rational interval certified by the finite words

For every leg in each recorded word, take the then-current virtual mark V, and list the positive finite absolute slopes from V to EVERY actual chamber corner. Also list slopes to both designated mouth endpoints, including endpoints that might merely be smooth points on a longer auxiliary cap. Add rational artificial bounds1 and2, which contain sqrt(2). Ignore vertical vectors, horizontal zero slopes, and zero vectors. All listed critical magnitudes are rational and therefore differ from sqrt(2).

Let l be the greatest listed magnitude below sqrt(2), and h the least above it. Then (l,h) is a bounded rational open interval containing sqrt(2). Intersect the two chambers' intervals. Every recorded first-mouth itinerary, its contact-interior conditions and its velocity signs persist throughout this intersection.

Here is the stability argument, rather than a sampling inference. Starting at the fixed mark, follow its first wall intersection as a function of positive finite magnitude. The type of earliest intersection can change only at an axis-parallel direction or when the moving collision reaches a wall endpoint; two competing earliest events coincide at the same physical boundary point, hence at a polygon corner. The corner event is exactly a listed rational slope from the initial virtual mark. On a component containing none of these values, the first collision remains transverse, smooth, of the same type and continuous. Induct after reflecting the virtual mark: its outgoing line again has slope plus or minus the magnitude through a FIXED rational virtual point, and all possible next-corner events have been listed. The finite prior contacts remain valid by the induction. Positive flight time cannot collapse to zero in the component without a preceding contact reaching a corner or an axis-parallel degeneracy. A hit of an earlier portion of the mouth can appear or disappear only by crossing one of its two endpoints, also listed. This proves the complete finite FIRST-mouth word is unchanged. No infinite future itinerary is assumed stable.

The use of absolute critical slopes is conservative: it lists extra events on backward line extensions or in the wrong sign state, but cannot omit an actual transition of these words. A virtual point equal to a corner corresponds to time zero on that developed line, behind the current positive-length itinerary; it is not an omitted future collision direction.

For the left final vertical sign e-, convert the common positive interval to signed tau=e-*m. The accepted sign formula sigma=-e-*e+ and rational virtual points give rational a,b,alpha,beta. The accepted aperture formulas hold throughout I by the certified itineraries, not merely at its midpoint. Thus

    L0=max(0,2w/|I|-a-b)

is a computable rational sufficient threshold. For rational L>L0 choose the first integer phase strictly above the lower interval endpoint. The resulting slope is rational and lies inside I. Replaying the finite chamber words and the finite neck folds constructs the entire physical path exactly. Real L uses the already accepted mathematical phase construction without claiming a finite exact machine representation of an arbitrary real input.

## 4. Reproducible controls and scope

constructive-neck.py uses only the SAME two prescribed chambers and marks as the accepted neck packet. It computes the sqrt(2) first-mouth words with14 and9 reflections using Q(sqrt(2)) arithmetic. It extracts common signed interval (7/5,10/7), sigma=+1, virtual points (-15,-21) and (11,17), hence a+b=26 and L0=4*35-26=114. Three prescribed rational magnitudes in each certified interval reproduce the words as controls; the finite-critical-set argument, not those six samples, proves the interval.

At the prescribed length L=L0+1=115, the first valid integer phase is n=40 and the actual slope is66/47. Exact replay reaches mouth ordinates3/47 and73/47 and joins actual S=(-3,3) to T_L=(118,3). The new independent physical checker passes all1060wall/leg comparisons and103genuine reflections, including both chamber itineraries and every neck bounce. Its vertices, contacts, target and phase are rational and unchanged from the specified physical geometry. This is not a new room search or a claim that114 is the optimal threshold; the earlier prescribed one-bounce entry words gave a much smaller threshold for these same chambers.

The original R17 aggregate840second deadline covers implementation, the corrected comparison dispatch, both executions, interval controls and full physical validation. No worker, subprocess search, changed room or extra direction was used. Discovery must not be restarted after that original deadline.

This supplement proves no uniform chamber-entry, interval-width, coordinate or complexity bound from wall count. It does not supply a decomposition of every W<=21 disk, handle coupled neck degenerations, or extend to diagonal chambers. Those are the actual remaining main-goal obligations. The full canonical45 theorem remains OPEN.
