# Six-wall limits: the non-torus case is already excluded

[done] Primary-source theorem checked and application written by Codex.
[waiting on Claude] Independent review of the application requested.
This is an application of published genus-two results, not a novelty claim.

## Exact scope

Let P be a bounded strictly simple orthogonal polygon with six maximal walls,
and s,t distinct interior points. If its unfolding is not a torus cover, then
no finite set B in P minus {s,t} blocks all ordinary billiard connections.
In particular, a single smooth boundary point cannot be essential.

This statement permits arbitrary real coordinates for the two interior marks.
It is not restricted to rational marks, source/target cylinder membership,
or the critical-leaf dichotomy. It does not cover rational-grid L rooms.

## 1. Published input

Apisa's accessible preprint 1710.05505v1, Theorem 4, classifies finite blocking
on primitive genus-two translation surfaces: regular points can be finitely
blocked only from their hyperelliptic conjugates. Theorem 6 gives the matching
six-wall polygon classification and torus-cover condition. This paper appeared
in IMRN in 2025; the theorem used here is already in the 2017 preprint.
The publisher result was found in search, but the full journal page failed to
fetch, so the directly inspected theorem text is the preprint.

Primary text: [Apisa, Theorems 4 and 6](https://arxiv.org/html/1710.05505v1).
Publisher record: https://academic.oup.com/imrn/article/2025/16/rnaf254/8237719.

The hypotheses "primitive" and "genus two" are indispensable. The theorem
cannot be applied to our arithmetic higher-genus rooms or to all real limits.

## 2. Why it applies to a six-wall orthogonal room

The angle identity gives one reflex and five convex corners. Their four-copy
unfolding M has one order-two zero and genus two. A translation covering of
M to a strictly smaller-genus translation surface could only be onto genus
one, since a sphere has no nonzero holomorphic one-form. Therefore, when M
is not a torus cover, it is translation-primitive.

Its canonical iota, induced by changing both reflection signs, has derivative
-I and has the six corner lifts as its fixed set. It is the hyperelliptic
involution of the genus-two Riemann surface. As always,

    pi(iota(x))=pi(x).

Suppose a finite physical set B blocks the interior pair. For any lift x of
s and any lift y of t, the finite regular set

    pi^(-1)(B) minus {zeros}, together with all regular convex corner lifts

is a blocking set on the unmarked translation surface M. True zeros are
already disallowed as interior trajectory contacts. Adding regular convex
lifts enforces the physical corner-stopping convention. If this were not a
surface blocking set, an avoiding surface segment would fold to an ordinary
billiard connection avoiding B. Thus it is a blocking set.

Apisa's theorem forces y=iota(x). But then

    t=pi(y)=pi(iota(x))=pi(x)=s,

contradicting distinct physical marks. Hence B cannot exist. This argument
excludes every finite blocker set, not only smooth boundary blockers.

## 3. An elementary test for the excluded shape family

Up to a rigid motion, a six-wall orthogonal room is an L shape. Write its
positive dimensions as a,b,c,d and use the cyclic boundary

    (0,0), (a+b,0), (a+b,c), (a,c), (a,c+d), (0,c+d).

**Claim.** M covers a torus if and only if both a/b and c/d are rational.

For necessity, there are ordinary axial periodic trajectories in each of the
two horizontal strips and each of the two vertical strips. Their lifts have
absolute holonomy periods

    (2(a+b),0), (2a,0), (0,2(c+d)), (0,2c).

If M covers a flat torus, all these periods lie in its lattice. The intersection
of a discrete lattice with an axis is cyclic when nontrivial. Therefore

    a/(a+b) and c/(c+d)

are rational, equivalently a/b and c/d are rational. No numerical rationality
test is asserted; this is an exact condition on the parameters.

For sufficiency, choose hx,hy>0 such that a,b are integer multiples of hx and
c,d are integer multiples of hy. P is tiled by congruent hx-by-hy rectangles.
In the four-copy unfolding every seam translation is a multiple of 2hx
horizontally and 2hy vertically. The developed coordinate modulo the lattice
2hx*Z x 2hy*Z defines a translation covering onto the rectangular torus.
This also agrees with Apisa's six-wall criterion.

Thus if either ratio is irrational, the finite-blocker question for distinct
interior marks is closed by Section 2. If both are rational, the argument
supplies no removal theorem. Our fixed six-wall control in critical-leaf.md
has rational ratios and is deliberately outside the excluded subclass.

## 4. Consequence for the point-collapse program

Consider a dark sequence with a Jordan six-wall orthogonal limit P0, distinct
interior limiting marks s0,t0, and only finitely many collapsed point features.
Assume the previously proved decorated-limit persistence hypotheses hold:
face convergence, no positive-length contacts/slits, and the finite collapse
points account for all lost corner obstructions.

Then the decorated limit would be dark after adding a finite blocker set B.
Section 2 rules this out whenever P0 is not a torus cover. Therefore any such
six-wall limit must satisfy both commensurability conditions above.

In particular, this excludes isolated smooth-step approaches to an irrational
six-wall L limit without needing a rank computation or an incompatible-band
certificate. A single smooth-step collapse from eight walls is one instance.
It does not exclude arithmetic six-wall limits, reflex-corner mark limits,
merged marks, contacts, slits or arbitrary larger-genus limits.

## Verification and next use

The work here checks the primary theorem's scope, the unfolding genus, the
blocking lift, and the exact axial period argument. It is not a ray or room
search, and no finite algebra count is offered as a proof of the cited deep
classification. The theorem and its published polygon consequence are prior
art. The point-collapse application is stated with our explicit persistence
hypotheses for independent review.

For the remaining task, focus on arithmetic L limits or higher-genus limits,
rather than attempting to prove a new cylinder theorem for this excluded
non-torus genus-two family.

## Subsequent elementary boundary result

The remaining arithmetic six-wall *smooth-boundary singleton* problem is now closed by `l-monotone-proof.md`, using a direct strip-unfolding construction for arbitrary real L dimensions. It also avoids any boundary blocker set contained in one wall orientation. This does not replace the stronger published non-torus finite-blocking theorem for arbitrary blocker locations, or settle arithmetic finite blockers of mixed orientations/interior locations. The earlier proposed rational monodromy work was not necessary for the singleton question.
