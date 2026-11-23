# A joint obstruction for two target classes at a time

Fix a same-parity pair of distinct interior lattice marks S,T over a pillowcase pole a. Choose an embedded system of tails to the poles, based just off a. Take two of the other poles b,c with adjacent tails, and write B,C for their monodromies. Tail conventions may be chosen so that the enclosing loop has monodromy h=BC (compose right to left). Transport the incident source and target sheet labels to the basepoint by the a-tail. Choose one such label i at S and one j at T.

**Lemma for review.** On the sheet labels draw one colored undirected edge for each actual transposition of B or C, retaining parallel edges. Components are alternating paths, even cycles, or isolated vertices. A missing edge at a path end is either a fixed point of that color or belongs to a 3-cycle. Either of the following suffices for a legal shot from S to T with midpoint over b or c:

1. i and j lie in the same component at odd graph distance.
2. i and j lie in the same path component and at least one end has a missing color that fixes its end label.

This test works with 3-cycles elsewhere, even in the permutations being twisted. It does not require a one- or two-cylinder decomposition. A fixed point in (2) is a convex corner. The shot does not visit that corner.

## Proof

Twist the two adjacent tails together k times about a simple loop enclosing b and c and disjoint from the a-tail. This leaves the labels at the marks unchanged and conjugates both B and C by h to the power k (the opposite twist gives the opposite sign). This follows by following the added enclosing loop on the way in and its inverse on the way out. In particular it suffices that h^k(i), h^k(j) form one regular transposition of either color. In that basis the corresponding simple arc from a to that target lifts out along one sheet and back along the other. The common end over b or c is regular, and both interiors avoid all poles. The pillowcase simple-arc/straight-billiard dictionary makes this a legal shot with that off-class midpoint. This is the one-transposition case of the archived pure-braid path test. [Exact path criterion](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d61-fold-converse/README.md) · [Independent review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d62-review-d61/)

Index a subpath between i and j by consecutive integers. On an alternating line the product BC moves one parity two steps to the right and the other two to the left. Its inverse reverses those motions. If the distance is odd, move the two labels toward each other. At separation one, stop; at separation three, one more product swaps their order and leaves separation one. At every stage even the intermediate one-edge moves are inside the original subpath. Thus the actual permutations agree with this line computation, irrespective of the unused edges beyond the ends. The final adjacent pair is a regular transposition. The same argument uses a simple subpath on an even cycle.

For (2), only even distances still need proof. Number the path from the fixed end by 0,1,... . Extend across that end by reflecting labels via t ↦ −1−t. The edge between −1 and 0 is the missing color, and its action after folding is exactly the fixed permutation at 0. The coloring extends alternately, with the same color on mirror edges. Use i's original index and the reflected index of j; their distance is odd. The interval between these two indices folds inside the original path. Part (1)'s inward moves on the extended line therefore agree at every step with the real permutations after folding. The final adjacent pair cannot fold to a single label: i and j were distinct and the same permutation h^k has acted on both. So it is an actual regular edge. The line computation concerns transport of labels by a twist; the only physical midpoint contact is on that final regular edge.

## Consequence for simultaneous failure

For *every* tail basis, each applicable choice of b,c, and every pair of endpoint sheet choices, simultaneous failure requires one of these:

- the labels lie in different components;
- they lie on the same even cycle on the same side of its bipartition;
- they have even separation on the same path and **both** ends are missing their edge because of a 3-cycle.

The last alternative costs two incidences with 3-cycles. For this target pair of colors there are at most floor(3(r_b+r_c)/2) such path components, since every reflex at b or c supplies three missing edge ends. Counting the three choices of two targets in compatible bases gives at most 3(r−r_a) such components in total (counted separately by choice, not over all bases). In the r≤8 range this is at most 24. A single such path can still contain arbitrarily many sheet positions as far as this count shows. In particular this is a count of components, not a budget on hidden points.

On a component with no 3-cycle incidence the alternatives are sharp for this twist test. On a cycle h preserves the index parity and every regular edge changes it, so it cannot join same-side labels by this construction. On a path with fixed ends the lemma covers every distinct pair. Distinct components free of 3-cycle incidences are preserved by B and C. A circuit through other poles or a different choice of tails may change the outcome.

**Open step.** Large valency bounds missing coincidences in the entire sheet-monodromy orbit by 14. It gives no placement of the *specific* endpoint sheet labels inside these alternating components in a common tail basis. In particular the different-component and same-side cycle alternatives cost no reflex incidences in this graph. To finish by this lemma would require showing that some basis and some two colors put two endpoint labels in a successful position, or a further argument for pairs that always escape in those alternatives. The current result gives a joint necessary condition for failure and does not exclude simultaneous failure at n≥120. No search was used.
