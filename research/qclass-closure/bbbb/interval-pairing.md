# Checking unbounded band itineraries by interval pairings

**Theorem for review.** Given a strictly simple orthogonal lattice room, two distinct interior lattice marks and a supplied primitive direction (p,b), one can decide whether some signed lift of that direction joins the marks in time polynomial in the binary input size. The number of integer interval pairings in the reduction is bounded in terms of the number of reflex corners alone. The algorithm neither expands the wall-reflection word nor iterates through successive piece changes. It applies to thin and fat rooms alike.

This is a substitute for bounded passage count at the *verification* step. It gives no bound on the bit length of a successful direction independent of the room dimensions, and no proof that one exists.

## Encoding a band

Handle horizontal or vertical directions by the straight same-row or same-column test in the appropriate connected interval. Otherwise put A=|p| and B=|b|. Start with the horizontal band decomposition and subdivide at the two mark heights wherever they meet a band interior. The resulting m≤3(r+1) rectangles have physical vertical sides. Their horizontal sides consist of open doors, solid mirror portions and isolated endpoints. Distinguish corners of the original polygon (always forbidden) from artificial subdivision points (regular).

For each rectangle, keep separate blocks for entering through its bottom moving up and through its top moving down. For width u, each block is the integer circle of length 2Bu. In local coordinates with left side l, the circle index z folds to physical x=l+min(z,2Bu−z)/B. Increasing phase fixes the horizontal velocity sign on each sheet. At 0 and Bu use the outgoing reflected germ on a smooth vertical wall. A lattice mark on the new section has integral indices. Include all its physically admissible outgoing germs, and likewise for the target.

Crossing the rectangle of height d acts by

    z ↦ z+dA mod 2Bu.

This accounts for every intermediate vertical-wall reflection. At the far horizontal side a regular open door transfers the folded x and outgoing horizontal sign to the next rectangle, keeping the vertical sense. Solid wall returns to the same rectangle and reverses the vertical sense. An artificial seam meeting a smooth vertical wall uses the unique continuation by reflection. A true polygon corner has no successor through that event. In particular exclude states located at true corners and all transitions incident on them. A path starting or ending at either interior mark is represented because its height was inserted as a section. The sign choices cover both forward and reverse physical times.

## Why the state map stays small

After the cyclic shift, split the exit circle at 0, Bu and the two folded preimages of each door endpoint on that side. Split off exceptional integer sites as singletons. Between consecutive split sites the successor belongs to one specified block, and its index is an integer isometry of the input interval: folding and unfolding use translations and sign changes only. Take inverse images by the cyclic shift, splitting a wrapped interval once, and split at a target-block wrap if necessary. All of these operations are integer arithmetic on interval endpoints. No splitting at the possibly numerous *intermediate* vertical-wall hits is necessary.

Concatenate the blocks into [1,N], N=4B times the sum of the rectangle widths. A conservative bound on the number of partial isometries is O(m²): each of the 2m sides can meet at most m neighboring rectangles and requires only a constant number of pieces per endpoint or door. The shift itself costs binary arithmetic in dA, irrespective of how many times it wraps. Bits needed for N and the shifts are polynomial in those of the input. Unused invalid sites may remain as isolated dummy points.

## Orbit test and correctness

Record each partial isometry as a pairing between integer subintervals. On actual states the original successor is a partial injection: inverse flow uniquely recovers the preceding section event until a forbidden corner. Its weak components are therefore uninterrupted directed paths or cycles. Two marked states in the same component have a legal connection in one time orientation. Conversely any legally developed segment in the supplied absolute direction traces edges of one component. Adjacent segment endpoints need no independent choice of slope or sheet.

Count the orbits once. For each pair of admissible source and target states, count again with the single extra pairing between their two singleton sites. The count stays the same exactly when the sites were already connected. Test pairs individually; joining all sheets at once can splice unrelated paths. The original orbits use only actual legal transitions. The extra pairing serves solely to compare counts.

Agol, Hass and Thurston's Theorem 12 accepts interval isometries on [1,N] and computes their orbit count in time polynomial in the number of pairings times log N. These are precisely the inputs above. The binary construction and constant number of calls give the claimed fixed-direction complexity. [Agol–Hass–Thurston, §4–5, Theorem 12](https://arxiv.org/pdf/math/0205057)

## A named test of actual revisits

Use DBw2 at its native corridor length four, chambers spanning x=0…5 and 9…14 and corridor 1<y<3. From (1,1) to (11,3) take the developed displacement (28j+10,2), j≥0. Its open segment stays at heights strictly between 1 and 3. Throughout that strip the only reflecting walls are x=0 and x=14. The developed endpoint folds to (11,3), and both marks are interior and same-parity. In the vertical band decomposition (or after rotating the named room for a horizontal convention), the sections x=5 and x=9 are crossed a total of 4j+2 times. Each unfolded period of length 28 contributes four, and the final ten units contribute two. No corner or lip is touched. This is a prescribed direction formula, not a sweep.

Thus even *actual changes of piece* can be arbitrarily numerous in a supplied direction in a room of fixed size. Orbit verification handles them without one instruction per change. This example does **not** give an existential lower bound: j=0 already lights the very same pair. The st279 passage lower bound counted normal reversals as well; it does not settle whether, after arbitrary cap returns inside each visit, the best direction requires unboundedly many changes of piece. [Passage bound and precise scope](passage-complexity.md)

## Consequence for the 20-wall goal

At r≤8 the number of pairings is absolutely bounded. The remaining existential problem is whether some coprime A,B make a source state and a target state belong to the same orbit. Interval endpoints still involve B times an unknown width and shifts dA; Theorem 12 decides individual inputs and supplies no uniform existential theorem in those parameters. The earlier marked-cover reduction supplies a finite but area-dependent direction decision for an individual room. Neither result turns a finite check of named rooms into a universal illumination proof. A sharper sufficient goal is a theorem selecting a successful pair of coefficients for this bounded collection of interval pairings, with no bound on the number of visits in the resulting orbit.
