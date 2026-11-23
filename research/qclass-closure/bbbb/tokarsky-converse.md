# Testing the single-fixed-corner converse to Tokarsky

**Verdict.** R22 refutes the proposed converse, even if one chooses the endpoint lifts first: for each lift choice there are two candidate paths whose sole forbidden contacts are different reflex corners.

## 1. Statement and counterexample

For a nonvacuous formulation, call a candidate a billiard itinerary from S to T obeying ordinary smooth-wall reflection, with straight physical continuation permitted through a reflex corner when both adjacent open legs lie inside the room. Convex contacts are still forbidden. Every legal path is a candidate. This narrow relaxation already suffices to test a universal obstruction. If “candidate” instead means an already legal path, condition (c) is vacuous for every dark pair and yields no corner count.

The proposed converse requires an affine involution exchanging chosen endpoint lifts, and **one fixed corner lift c, independent of itinerary**, through which all candidates for those lifts pass. On the ordered-pair cover U the endpoint exchange is interpreted as exchange of the ordered coordinates, and a corner lift must project to a room corner in at least one coordinate. Passage through one specified c on either surface entails a visit to one specified physical corner. This last consequence is false regardless of what affine involutions exist.

In the unmodified R22, S=(0,0) and T=(2,2) are dark. Four saved certificates suffice. The vectors below launch from S and **backward** from T. Both legs have equal length, meet at the indicated corner, and join with straight physical continuation. Each open leg avoids all corners, and the indicated corner is the only intermediate lattice point of the combined path. The nine-row exact checker was replayed, without any discovery search. [Certificates and verifier](corner-support.py) · [Reviewed corner-support argument](corner-support.md)

| Source launch | Backward target launch | Sole corner | End copy relative to start |
|---|---|---|---|
| (9,−5) | (−9,5) | (1,−1) | same |
| (1,1) | (−1,−1) | (1,1) | same |
| (−2,1) | (−2,−1) | (0,1) | opposite |
| (7,−4) | (−7,−4) | (1,−2) | opposite |

To verify the copy column, each ordinary reflection changes the sign of exactly one velocity component and switches halves of the room double. Straight continuation at the reflex changes neither. Thus the parity of the number of reflections is read off by comparing the sign of the product of the components at the two ends; negating the backward launch leaves that product unchanged. Starting on the other copy mirrors the entire construction. The first two rows therefore exclude a common corner for either same-copy lift choice, and the last two do so for either opposite-copy choice. In synchronized coordinates on U, both tracks run corner-free until their common midpoint corner in each row. A single point of U projecting to a corner cannot belong to both such tracks from the same lift choice: their projected corner sets are disjoint. This refutes (c); deciding (a) or (b) separately cannot rescue the conjunction.

Lemma MP gives the half-turn of each *developed segment* about its own lattice midpoint. That midpoint depends on the itinerary: the table exhibits the dependence even for fixed endpoint lifts. MP gives no common midpoint or global affine involution. Likewise, the stabilizer of s fixes s; its orbit of t propagates an already known dark pair to other targets. This does not produce an element exchanging s and t or a common blocker. [MP review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d101-small-p1/review.md) · [Mirror review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d92-review-mirror/review.md)

## 2. What can actually be counted

In R22 there is a singleton-support certificate for **each** of the nine reflex corners. A set of reflex stops intercepting all relaxed routes must contain all nine, and all nine suffice by the proved darkness. Thus the minimum is nine for this room and this pair. Deriving a universal r≥9 from the proposed converse fails at its premise. Nothing here settles the W≤20 theorem.

## 3. The mechanism that survives

The proved R22 argument is a three-copy fold onto the five-square staircase. For a proposed ordinary staircase path, parity forces an intermediate odd-coordinate lattice point; every such point in the staircase is a vertex. **Which vertex is hit can depend on the itinerary.** At any of four smooth seam endpoints upstairs the folded path reverses and retraces; taking the segment from the last visit to the source image to the first arrival at the target image rules out that escape. The obstruction is collective: every candidate meets the forbidden set, while different candidates can require different members of it. R22 still uses a Tokarsky-type unfolding argument. It disproves the stronger formulation with one fixed corner upstairs or on U, without classifying the mechanisms of all dark rooms. [Manuscript, parity and reversal lemmas](../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex)
