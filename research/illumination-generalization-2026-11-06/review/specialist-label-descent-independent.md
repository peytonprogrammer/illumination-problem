# Independent review: specialist label descent

Verdict: **ACCEPT all six scoped claims**, with the explicit regular-root, connected-component, sector and physical-cover qualifications below. This repairs finite bookkeeping. It proves no positive illumination theorem, wall bound, universal 3+6 split, or characterization of physical unfoldings.

## Inputs and independent method

Read the complete pinned argument, audit source, audit output and review request. All three requested SHA256 values match. Independently verified the saved known22 certificate's decompressed SHA256, `2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346`, and its exact initial state and tags. The certificate contains 10,368 distinct existing states of 60 squares. No author checker was run.

Own reproducible checker: `specialist-label-descent-independent-replay.py`; output: `specialist-label-descent-independent-replay.json`. It implements permutation composition independently, tracks original square slots rather than transported tag arrays, and uses a different U-before-T spanning tree. Every computed neighbor must already belong to the supplied certificate. This verifies its existing 20,736 directed edges; it never extends the saved state set or enumerates the refined orbit. A separate short replay checks the supplied 12-step word. Nine additional closed root loops certify the mergers needed for the reported label orbits.

## 1. Full reflection conjugation — ACCEPT

For A_n=[[1,n],[0,1]] and R=diag(1,-1), direct multiplication gives A_n R A_n^{-1}=[[1,-2n],[0,-1]]. The difference is in the derivative, not merely in the chosen vertex names.

On the prescribed square torus with period lattice 48Z^2, the horizontal permutation h has order48. Iterating the raw anchored T transformation gives (h,v h^{-k},color). Thus k=48 restores the exact raw triple and therefore its rooted canonical triple, with every color retained. The transported reflection instead has derivative [[1,-96],[0,-1]]. Repeating this same loop produces [[1,-96k],[0,-1]]. Translation isomorphisms have derivative I, so they cannot identify these distinct derivatives. This establishes the claimed failure of full-reflection descent under translation equivalence. It does not refute finite methods using only the coarse state or any feature separately proved invariant along the loops.

The checker verifies the matrix identities exactly and verifies the order48 permutation by its closed formula, without constructing a new torus orbit. Finite vertex permutations alone can miss this obstruction: the difference -96y is zero modulo48 at every integer vertex.

## 2. Twelve-step closed word — ACCEPT

The supplied word, in execution order, is:

`T T T U T U U Ti Ui Ti Ui Ui`.

The independent replay restores h, v and color EXACTLY, not just up to an unrecorded isomorphism. Its induced identity permutation is

- zeros: (0 7)(2 4)(3 6 5), fixing1 and8;
- sources: fixes9,10,11,12 individually;
- targets: (13 16)(14 15).

The final tag array also equals the pinned output exactly. At every raw step, the checker verifies C=v h v^{-1} h^{-1} is unchanged BEFORE canonical relabelling. It independently verifies that C has precisely nine nontrivial cycles, each of length3, and that all eight endpoint marks are regular fixed points of C. Thus these are genuine zero identities and the complete four-plus-four endpoint marks in this saved component. Regular corner marks remain present in the coarse color data; they are not misclassified as cone zeros.

## 3. Zero-label transport orbits — ACCEPT, for this certificate only

The independent all-existing-edge audit, with the alternate spanning tree, gives exactly:

- zeros: {0,1,7} and {2,3,4,5,6,8};
- sources: {9},{10},{11},{12};
- targets: {13,16} and {14,15}.

For sufficiency of the audit, a spanning tree gives a chosen identification from the initial root to each existing state. Each non-tree edge, followed by the inverse tree path, is a based closed word. These fundamental loops generate all loop transports, because every tree segment cancels in any closed walk. Checking every edge proves no orbit crosses the displayed partition. Separately replayed merger loops connect every label within each class, proving the reverse inclusion as well. The output records their words and induced root permutations; each merger a->b is directly checked.

Own gauge has10,031 disagreement edges, versus the author's10,058. This is expected: a different spanning tree changes which edges disagree with the chosen transport. It is not a mismatch in the claimed loop, partition or certificate. The partition, rather than that gauge-dependent edge count, is the invariant being accepted.

Fixed identity weights must be constant on each class if the weights themselves are to descend. This does not reduce every invariant relational feature to two counts, nor prove that any such feature gives positive charge. The 3+6 split and fixed source IDs are properties of this one rooted certificate; no universal lower bound follows.

## 4. Explicit-ID refinement bound — ACCEPT, for the stated identities

Over one connected rooted coarse state, the r distinct zero names can be assigned to its r zero cycles in at most r! ways. Four distinct source names and four distinct target names admit at most4! assignments each. The square permutations, all colors and regular sheets are already in the coarse state. Therefore the number of such ID refinements is at most r!*(4!)^2. The root constraint may lower the count; the stated upper bound is sufficient. For r=9 it is209,018,880 refinements per coarse state, not a manageable complexity guarantee.

The anchored raw T/U rules are invertible (Ti replaces v by vh, Ui replaces h by hv), and canonical relabelling transports the chosen root and IDs bijectively. Thus their reachable refined orbit is a finite set on which T/U are permutations. Any finite-valued potential on that set has zero summed coboundary. This proves telescoping is legitimate, not that an adequate potential or positive inequality exists.

The bound names ZERO identities, not independent labels for every incoming sector, every regular corner, or additional physical reflections. A potential using separately named prongs or sectors needs either a descent proof for those data or an additional finite refinement factor. Existing square slots record the surface's sectors, but naming a distinguished sector at each zero is extra information. The full transported reflection in claim1 has infinitely many possible derivatives and is not included in this factorial bound.

## 5. Regular-root determination of the half-turn — ACCEPT with explicit scope

On a fixed CONNECTED translation surface, suppose affine f and g have the same specified derivative and send the same REGULAR root p to the same actual surface point. Then g^{-1}f has derivative I and fixes p. In a regular translation chart it is a translation fixing a point, hence the identity locally. Continuation over the connected regular locus proves it is the identity everywhere, and continuity includes the cone zeros. Therefore f=g.

The physical intrinsic half-turn rho has derivative -I and preserves the complete source fiber. With four distinct source lifts in this connected component, its value at the rooted source has at most four possibilities. Thus at most four compatible maps exist per coarse surface. Some possibilities may not extend, preserve all required labels, or square to the identity; those conditions must still be checked. The statement is an upper bound, not an existence test or a recovery algorithm from a passport alone.

Because -I commutes with shears, its derivative remains fixed. Once the source IDs are retained, a transported rho can be specified by the ID of rho(p); uniqueness then determines its full action if it exists. There is no independent sector multiplicity at a regular image point. Naming its entire finite vertex/sector action is an alternative encoding, not a proof that arbitrary sector permutations are realizable.

Essential caveats: a CONE root permits several local sectors with the same derivative and point image, so the argument would fail there. A root on one connected component does not determine maps on other disconnected components. An image on the base torus does not specify which point above it is intended; the actual cover sheet must be retained. The saved rooted connected component and its four actual regular source lifts meet these requirements. If rho were appended independently rather than determined through retained source IDs, a conservative extra factor of at most4 could be used. Neither the four-choice bound nor rho alone reconstructs a physical reflection or a planar room.

## 6. Physical orthogonal scope under shears — ACCEPT

A shear preserves straight segments and transports the optical problem to the deformed translation surface. It does not preserve the Euclidean isometry property of a transported reflection: R_1=[[1,-2],[0,-1]] has R_1^t R_1 != I. Therefore a pointwise argument about orthogonal physical walls cannot simply follow that transported reflection through the finite orbit.

A fixed marked example strengthens this warning without a new search. Use the already prescribed square[0,24]^2, its torus R^2/(48Z^2), S=(12,12), T=(16,18), and ALL four target lifts (±16,±18). After A_1, those target lifts are

`{(2,18),(34,18),(14,30),(46,30)}` modulo48.

Their coordinate cardinalities are4 and2. Any strictly simple orthogonal room whose standard unfolding has no genuine zeros must be a rectangle: a reflex3pi/2 corner would produce a6pi zero; with no reflex corners, the orthogonal turning sum gives four convex corners. A rectangle whose standard unfolding torus is this square torus must have side lengths24,24, with side periods a primitive orthogonal basis of48Z^2. Such a basis is axis-aligned up to quarter-turn and signs: an integral orthogonal basis of determinant±1 has unit columns. Its full interior target fiber therefore has two x coordinates and two y coordinates. Translations, signs and axis exchange do not turn4-by2 coordinate cardinalities into2-by2. The sheared FULL marked object is consequently not the standard unfolding of an orthogonal room with those actual endpoint fibers.

This excludes pointwise physical realizability of the full marked structure in this explicit example. The unmarked torus remains the same square torus; discarding or changing marks would change the question. Arbitrary extra covers are not a loophole: an extra degree-m cover would lift a regular four-point endpoint fiber to4m points; the retained complete four-point fiber forces m=1. None of this refutes the legitimate invariant assertion that the SL2 orbit CONTAINS a physical representative—the original square already is one.

## Findings and limits

No correction to the frozen scoped argument is required. The sector, component and actual-cover-point qualifications above are necessary for using its finite repair and half-turn bound correctly. All input hashes were rechecked after verification. No author/coordinator file, shared git state, native goal or budget was changed. No room/orbit census, coefficient fitting or worker was used. The only larger check reads the existing pinned finite certificate.

The bookkeeping repair is accepted. The positive illumination theorem and any new maximal-wall lower bound remain unproved. This bounded review is complete.
