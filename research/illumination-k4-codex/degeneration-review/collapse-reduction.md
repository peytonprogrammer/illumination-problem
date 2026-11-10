# Point-collapse reduction with retained boundary blockers

[done] Analytic reduction and exact diagnostics. Opus independently accepted the Jordan-quotient persistence proof, cost theorem, equality case and step interval on 2026-11-01. This treats collapsed chains whose reduced boundary remains a Jordan curve. Contacts, overlapping wall faces, slits, and marks reaching the boundary require separate treatment.

## Result

Let a sequence of dark polygons with W maximal straight walls converge with fixed labeled edge directions. Suppose the limiting source and target stay distinct and interior, and deleting zero-length edges leaves an injective polygonal boundary. If r edges vanish and s of the resulting vertices become smooth, then:

- The limit has W' = W − r − s maximal walls.
- It is dark after retaining those s smooth collapse points as boundary blockers.
- With B existing boundary blockers, the limit needs at most B' ≤ B+s extra blockers.
- The integer cost C = W+2B cannot increase:

    C' ≤ C − (r−s).

Every collapsed chain of at least two edges forces a strict cost decrease, regardless of their relative shrinking rates. Equality can occur only when every collapsed chain consists of one edge and becomes a smooth step, with all old blockers retained separately as smooth blockers.

This is a bookkeeping theorem for a specified class of limits, not the earlier conjecture about all dark limits having weight at least 22. It proves neither that low-cost decorated rooms are impossible nor that a surviving smooth boundary blocker can be removed.

## Definitions and hypotheses

Orient every polygon counterclockwise. Its vertices v_0,n,…,v_(W−1),n are genuine corners, indexed cyclically. The directed unit edge vectors are fixed as n varies; adjacent edge directions differ. Edge lengths are positive. Normalize position and size, pass to a subsequence, and assume all labeled vertices converge.

The word "dark" means that no positive-length finite specular path joins the marked pair while avoiding genuine corners and any specified extra blockers. Reflections must lie in relative interiors of walls. The two marks are interior and distinct at every n and have distinct interior limits. Extra blockers b_1,n,…,b_B,n lie on the boundary and also converge along a subsequence. Their limit points may coincide or become genuine corners.

Let Z be the zero-length limit edges, r=|Z|>0. Partition Z into its K nonempty maximal consecutive chains on the cyclic boundary. Contract each chain to its limit point. Keep every positive-length edge and its orientation. The resulting polygonal cycle Q has m=W−r edges. Assume Q is injective as a map from a circle onto its image; its intermediate collinear vertices are allowed. In particular, Q has no doubled segments, nonadjacent contacts, overlaps or reversals. A positive-length corridor collapsing onto itself violates this hypothesis.

Let s be the number of smooth vertices of Q, meaning that its incoming and outgoing directed edges continue on the same straight line. Delete those vertices to obtain the usual maximal-wall polygon P_0. The s locations form S. No two are identified by the injectivity hypothesis.

Let B_0 be the distinct limits of the old blockers. The new extra blocker set is

    B' = (B_0 union S) minus the genuine corners of P_0.

The symbol B' also denotes its cardinality where a count is intended. Blockers coinciding with genuine corners need no extra label. The theorem is valid for any fixed finite direction list, including the canonical 45-degree family.

## Proposition 1: wall count and optical reduction

Under these hypotheses, P_0 is a strictly simple polygon with W'=W−r−s maximal walls, and its two marks are dark with blockers B'.

**Wall count.** Contracting r edges of a cycle leaves m=W−r positive edges and m vertices. An unchanged vertex between two original positive edges still has its original distinct directions, so it cannot become smooth. Hence every smooth quotient vertex arises from a nonempty collapsed chain. Each such chain produces at most one smooth vertex. Therefore

    s ≤ K ≤ r.

Injectivity prohibits adjacent collinear reversal. Removing one smooth vertex fuses two consecutive edges into one and lowers the wall count by one. Removing all s gives W'=m−s.

**Interior and wall sides.** The original oriented polygonal curves converge uniformly to Q: their vertices converge and their edge parametrizations are linear, while the vanishing edges converge to points. Winding number around a point away from Q is stable under sufficiently small uniform perturbation. Thus P_0 has the inherited interior side. On a compact portion of a positive limiting face away from quotient vertices, the corresponding walls and interior sides converge, and other faces remain separated. This supplies the local-domain premise needed by fixed-word persistence; it is not assumed from unlabelled Hausdorff convergence alone.

**Optical reduction.** Suppose a finite connection existed in P_0 avoiding its genuine corners and B'. Every reflection then avoids every quotient vertex: genuine vertices are already forbidden, and the smooth ones belong to S. It therefore lies strictly inside an inherited positive-length face, not merely inside a newly merged maximal wall. Every segment stays clear of the finitely many collapsed points, genuine corners and limit blockers. The marks are distinct and interior.

Unfold this fixed word and aim at the moved target image. The limiting developed displacement is nonzero. All transverse wall crossings, contact ordering, face membership and endpoint interior conditions are strict. They persist under the labeled convergence just established. Avoidance of the finitely many blockers persists too. The same word would join the marks of P_n for all sufficiently large n, contrary to darkness. This proves darkness in the decorated limit.

No bound on the word length is used: each hypothetical finite limit connection is transferred individually. The proof does not claim a uniform word bound over all configurations.

## Proposition 2: monotonic integer cost

There are at most B old blocker limits and s new smooth collapse points, so B'≤B+s. Thus

    W'+2B' ≤ W−r−s+2(B+s) = W+2B−(r−s).

Since s≤K≤r, C'=W'+2B'≤C.

If any collapsed chain has at least two edges, r≥K+1, hence r−s≥1 and C'≤C−1. This conclusion is independent of how many different scales occur inside that chain.

If C'=C, all inequalities must be equalities. In particular r=s=K. Every collapsed chain then contains exactly one edge and becomes smooth. Also B'=B+s, so none of the old blockers can disappear at a genuine corner or merge with another old or new blocker. The converse is a combinatorial equality statement under those conditions; it is not an existence claim for a dark sequence.

With no old blockers, C' = W'+2s exactly. A one-edge proper-corner collapse saves one unit. A one-edge smooth step saves none after its boundary blocker is counted. A three-edge notch collapsing to a smooth point saves two units.

The charge 2 is sharp for this bookkeeping: a one-edge smooth step removes two maximal walls and leaves one smooth collapse point. Charging that point more than 2 would violate monotonicity even in the elementary six-to-four-wall geometric example. Those example marks are lit, so this sharpness concerns collapse bookkeeping, not a proven dark-sequence optimum.

## Ordinary darkness: exactly where it follows

With no preexisting blockers, if every collapsed point remains a genuine corner of P_0, then S is empty. Proposition 1 gives ordinary darkness in a strictly smaller room. This includes an isolated proper-corner edge collapse with no other degeneration.

If a collapsed point becomes smooth, Proposition 1 supplies a boundary-blocked dark pair. Erasing that blocker requires an additional optical argument. A limiting path reflecting at that point need not lift through either neighboring original wall face. Therefore a smooth-step collapse does not, by the persistence argument alone, justify induction on ordinary rooms with W−2 walls.

## Exact failure of smooth-point reflection transfer

Use the strictly simple six-wall polygons

    (0,0), (2,0), (2,1), (2+h,1), (2+h,2), (0,2),    0<h<1,

and marks s=(1,1/2), t=(1,3/2). Their limit is the rectangle [0,2]². In that rectangle, the word consisting of one reflection in the right wall joins s to t through (2,1), strictly inside that maximal wall.

In P_h, the one-reflection candidate on the lower right face x=2 hits (2,1), an actual corner. The candidate on the upper right face x=2+h hits (2+h,1), also an actual corner. Neither is an allowed connection. Reflection in the short horizontal step unfolds the target exactly onto the source and gives no positive-length connecting segment for that word.

This refutes automatic preservation of the specified limit reflection. It is not a dark sequence: s and t are directly visible in every P_h. It also does not rule out a general blocker-removal theorem proved by a different word.

## Exact transfer interval for one smooth step

The missed reflection has a quantitative local obstruction, not just an endpoint coincidence. Translate the step to the origin. The lower vertical face is x=0, y<0; the upper face is x=e, y>0; the horizontal step is y=0, 0<x<e, with interior above it. Consider source A=(-a,u), target T=(-b,v), where a,b>0, u<0<v. This describes the two adjacent developed portions of the fixed limiting word. Set

    K = b u + a v.

The lower-face reflection has ordinate

    y_L = K/(a+b).

It is a valid local lower-face connection exactly when K<0. The reflected outgoing segment then stays on the interior side while crossing y=0.

The upper-face reflection has ordinate

    y_U = ((b+e)u + (a+e)v)/(a+b+2e).

Its incoming segment must cross the line x=0 above y=0 to avoid the lower wall and the step. That condition is

    u + a(y_U−u)/(a+e) > 0,

which simplifies exactly to

    K > −2 e u.

This also implies y_U>0. The outgoing segment toward T has y>0 and remains inside. Therefore neither of these two face words lifts when

    0 ≤ K ≤ −2 e u.

Equality is forbidden too: a segment hits a genuine corner. The forbidden interval has width 2e|u| in K-coordinates. When K=O(e), it survives as a nontrivial interval after division by e. Shrinking the step does not remove that normalized obstruction.

This is a fixed two-word local calculation. It is not a search over directions or rooms and is not a criterion for global darkness. In the half-plane step model A and T themselves are directly visible; the calculation concerns replacement of a prescribed reflected segment of a larger word. More complicated replacement words and their surrounding contacts would require their own verification.

The interval gives a concrete task for a future proof: either find another robust word that bypasses every such interval, or prove that several limiting connections force incompatible K/e constraints. Neither assertion follows from the wall count alone.

## Several rates of collapse

The point-collapse theorem contracts all zero-length edges simultaneously and preserves each smooth collapse point as a blocker. It needs no assumed common rate, so a notch of depth h and width h² is covered whenever its quotient is Jordan. At scale h its bottom edge disappears; at scale h² it has a different local model. Its cost still drops by two in Proposition 2.

There is also an elementary finite point-cluster hierarchy. For M labeled distinct points in a bounded normalized configuration, pass to a subsequence so all positions converge. Group equal limiting points. For each group containing at least two labels, subtract one of its moving representatives and divide by its current diameter. The normalized group has diameter one and bounded coordinates. Pass to a subsequence and partition it again by equal limiting positions. At least two distinct child groups appear, because the limiting diameter is one. Recurse only on nonsingleton child groups whose diameters vanish at their parent's scale.

Every internal node splits into at least two children, and the M original labels are the leaves. Thus there are at most M−1 internal nodes and at most M−1 levels on any branch. The construction uses a finite nested subsequence selection. There is no need to assume power-law rates.

This is a hierarchy of finitely many point labels, not a complete compactification of polygon optics. It does not resolve positive-length overlapping faces, an approaching wall gap without an endpoint collision, glancing directions, or paths whose word lengths grow. In particular, it supplies no cylinder-count or uniform-clearance estimate. Proposition 2's rate-independent strict decrease is stronger for the present point-collapse count than an attempted enumeration of every scaled local optical model.

## What this changes in the global program

For Jordan point-collapse limits with interior marks, a natural induction class is strictly simple polygons with finitely many smooth boundary blockers and integer cost W+2B. Every nontrivial collapsed chain of at least two edges lowers that cost. Proper-corner single-edge collapses lower it too. Only isolated single-edge smooth steps can preserve the cost.

Three gaps remain before this becomes a global proof:

1. Excluding low-cost dark decorated rooms, including the zero-cost-change smooth-step boundary. The original bounded lattice theorem does not cover this enlarged real-parameter class.
2. Handling limits whose quotient is not Jordan: contacts, overlapping faces, slits and collapsed corridors. Opus owns their local passage analysis.
3. Handling boundary or coalesced marks with moving endpoint sectors. The ordinary-darkness conclusion above explicitly requires distinct interior limit marks.

A smaller undecorated wall count by itself does not close any of those gaps. No global minimum, new dark construction is made.

## Verification and handoff

`collapse-check.py` uses exact rational arithmetic to check nine strictly simple polygon controls (proper bevel, smooth step, two-scale notch), their zero-edge/smooth-fusion counts, three vanished-reflection diagnostics, 15 local step-interval cases, and 37,448 finite chain-size/smoothness bookkeeping controls. The latter verify integer identities; they do not certify geometric realizability or replace the written proof.

Run from the workspace root:

```sh
python3 -B .context/illumination-k4-codex/degeneration-review/collapse-check.py
```

The script writes only its already claimed `collapse-check.json`. No peer executable is imported. Sources, reports and receipts are hashed in `collapse-manifest.json`.

**Next move:** use the accepted step-transfer interval to test the zero-cost-change case analytically. Opus also independently accepted the constructive corridor repair in `cluster-review.md`.
