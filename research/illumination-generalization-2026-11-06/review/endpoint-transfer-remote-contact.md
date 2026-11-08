# A remote wall contact is necessary for the opposed-arm match

Status: independently hand derived; submitted for peer challenge. This is a prerequisite, not a positive illumination theorem or a corner-count bound.

## Exact statement

Let D be a finite strictly simple orthogonal polygon. An actual reflex corner C=(0,0) has its two incident maximal walls contained in the positive coordinate rays, with interior locally west of the vertical wall and south of the horizontal wall. Let actual interior marks S=(a,-b), T=(-c,d), where a,b,c,d>0 and ad=bc. No legal finite billiard from S to T can use only those two incident walls for its reflections. Every legal connection must have at least one reflection on a different actual wall.

The marks need not fit a full L corridor. The conclusion holds even when their distances exceed the local corner collar. Other actual walls can only obstruct proposed paths that have no collisions with them. Earlier actual target arrival is included: apply the argument to the trajectory truncated at its first actual T.

## Proof, with all finite local words covered

At an ordinary contact F=(0,y), y>0, on the incident vertical wall, the incoming horizontal velocity is strictly positive and the outgoing horizontal velocity is strictly negative. Before a subsequent collision, x therefore stays strictly negative. The ray cannot hit the positive horizontal wall, nor revisit x=0. At an ordinary contact F=(x,0), x>0, on the horizontal wall, the incoming vertical velocity is strictly positive and the outgoing vertical velocity is strictly negative. It then stays strictly below y=0, so cannot hit either incident wall again. Tangent contacts do not create a reflection from an interior straight segment; endpoints of walls are forbidden true corners.

Consequently a finite trajectory with reflections on only these two walls has zero or one reflection. This is a physical first-hit restriction, not a finite-state assumption about arbitrary trajectories.

With zero reflections, the segment from S to T passes through C: its x=0 crossing has y=(ad-bc)/(a+c)=0. It is illegal.

With one horizontal reflection, unfold the actual target to T_H=(-c,-d). The straight developed segment joins S=(a,-b) to T_H; every point on it has y<0. It cannot contain the required reflection on y=0. Equivalently a physical ray that meets the horizontal wall from below leaves with negative vertical velocity and cannot reach T above it without another reflection.

With one vertical reflection, unfold the actual target to T_V=(c,d). Both endpoints of the developed segment have x>0, so it cannot contain the required reflection on x=0. Equivalently a contact approached from west cannot be the first reflection of a straight segment starting at S with x>0. These arguments use the actual target, positive travel order and correct sides of actual walls. They exclude the last possible words, proving the claim.

## What this adds and what it does not

L1-L2 addressed a specified incoming SW germ and a two-word V/H replacement with fixed exterior development. This statement instead covers every finite itinerary supported on the two incident walls for opposed actual SE/NW marks. It explains why a construction such as ET01 necessarily uses a wall away from C. It does not establish availability of that wall excursion, or allow local germs on unrelated developed sheets to be treated as the actual S,T.

For a general degenerate connection with exterior reflection words, the marks at the ends of its local germs are auxiliary states. The theorem applies to a local replacement that preserves those auxiliary points in an opposed-arm configuration; it does not prohibit changing the exterior words and launch direction. Such a change requires a new global first-hit/target proof.

A nonincident wall is not a new reflex corner. It may be an existing floor; arbitrarily many developed visits may use the same actual walls. Thus this condition supplies no increase in distinct reflex count and no nine-corner obstruction. Nor does it cover components with no matching root at their endpoints.

No search, room census, numerical fitting or author-checker execution was used. The proof is the exhaustive physical zero/one-contact argument above, with arbitrary positive real offsets.
