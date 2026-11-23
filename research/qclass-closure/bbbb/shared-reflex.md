# One source-parity reflex can intercept all three primitive parity classes

There is a normalized strictly simple eight-wall BBBB room with exactly one reflex corner of the marks' parity in which three relaxed routes for the *same* nondirect pair have the same singleton reflex support. Their primitive directions represent all three nonzero classes modulo two. Each route even has a **regular off-class midpoint**, strictly after the forbidden contact. This refutes a local restriction on how many classes one corner can serve. The pair is lit by a different route.

## Construction

In the box [−7,14] × [−14,7] cut the northeast quadrant at C=(0,0) and trim the southwest corner by a 1 × 1 square. Precisely, the cyclic boundary is

    (−7,−13), (−6,−13), (−6,−14), (14,−14),
    (14,0), (0,0), (0,7), (−7,7).

The boundary is simple; the only reflexes are C and (−6,−13). Both axis wall-length gcds are one because the trim has two unit edges. The area is 342. All four lattice parities occur in the interior. Put S=(−2,2) and T=(4,−4). Their direct segment hits C. Only C has their even-even parity.

Use the northwest square [−7,0] × [0,7] and the southeast square [0,14] × [−14,0]. The latter is the image of the former under X ↦ −2X, taking S to T. From C into the northwest square, the following three *prescribed* developed displacements fold to S. In the last two cases a single reflection at the far wall changes the developed coordinate of magnitude 12 to magnitude 2. Reverse this leg from S to C. Continue with the image of the C-to-S leg under X ↦ −2X, at the same physical speed. Its initial tangent agrees with the incoming tangent at C. The second leg has twice the length of the first. The southwest trim is outside both legs.

| C-to-S developed displacement | Primitive direction parity | NW wall contact | Physical midpoint of whole route |
|---|---|---|---|
| (−2,2) | (1,1) | none | (1,−1) |
| (−12,2) | (0,1) | (−7,7/6) | (6,−1) |
| (−2,12) | (1,0) | (−7/6,7) | (1,−6) |

The southeast wall contacts, when present, are the images of those listed under X ↦ −2X, hence are also smooth. Parametrize by primitive steps: C is reached at step 2, the midpoint at step 3, and T at step 6. Each midpoint is interior to the southeast square and has its route's nonzero parity. C is strictly inside the route, and its two incident open legs lie inside the room. No other corner is touched.

In fact identical incidence data occur at unbounded area: replace 7 by any odd b ≥ 7, replace 14 by 2b, and keep the marks and unit trim. The two long developed coordinate magnitudes become 2b−2. Dividing by two gives the even primitive component b−1 opposite a component of magnitude one. The unique trimmed reflex becomes (−b+1,−2b+1) of parity (0,1). This is an analytic construction using the single far-wall reflection, with no direction enumeration.

## What the example does and does not decide

Assign the three displayed routes nonnegative weights and impose capacity one at each physical reflex. Their weights must sum to at most one, even though all three midpoint parities occur. Avoiding simultaneous charges by using off-class midpoints, by insisting the midpoint itself be regular, or by excluding routes whose midpoint is the blocking corner does not solve the problem.

For this pair a legal route already comes from the image of T across the bottom wall, (4,−24). The segment from S to this image crosses x=0 at y=−20/3, reflects on the bottom at (22/13,−14), and folds to T. It stays in the room on either side of the reflection and avoids the southwest trim. Its physical midpoint is (1,−11). Thus the example does not say that C intercepts *every* route of any class, or that the proposed packing bound fails for the whole route family.

The saved cov4181 control gives a different piece of information: d66 records failure at target d but success at b. Class d has no reflex and the marks' class has only one. This controls what can obstruct the failed class without supplying a relaxed route through that corner. The construction above supplies actual routes in three classes; it makes no inference from algebraic candidates. [Earlier distinction and control](corner-support.md)

**Remaining question.** A global argument must produce routes avoiding C or bound their total blocking cost. More precisely, delete every relaxed route meeting C from the route family. If all the surviving routes can be intercepted by seven other physical reflexes, those seven together with C intercept the original family. Conversely, any eight-corner cover containing C leaves a seven-corner cover after this deletion. The relevant geometry is therefore reachability with C forbidden from the start. A local count of available incidence angles or of represented midpoint parities cannot establish that reachability.
