# Independent review of the local rigidity certificate

[done] ACCEPT the local rigidity result for the fixed orthogonal shape and ordered interior marks, up to translations and positive independent axis scalings. This accepts a local theorem at the certified 22-wall room. It does not establish a global wall minimum, the rigidity conjecture for other rooms, or historical novelty of local rigidity.

## Independent implementation and exact results

No Claude executable or source was read or imported. Frozen inputs and hashes are in `manifest.json`. The room boundary was independently extracted from its triangle incidence graph; smooth atomic vertices were removed, retaining the 22 genuine walls. Coordinates use two anchor variables, 22 signed edge displacements, and four mark coordinates (28 variables). Closure imposes two independent linear equations, leaving dimension 26.

`check.py` replays only the 129 directions supplied with Opus's 147 events. Each prescribed direction is resolved on its two sides using exact first-order infinitesimals; no new directions are searched. Both the reflected and nonreflected branch at a reflex corner are included. Unfolded corner images distinguish repeated visits to the same physical vertex.

| Check | Result |
| --- | --- |
| Supplied direction sides resolved | 258 |
| Exactly one-corner events reconstructed | 147 |
| Other sides stop at a second corner | 111 |
| Signed derivative constraints matching peer | 147/147, positive normalization |
| Event direction/corner metadata matching peer | 147/147 |
| Events with no reflection at the corner / one reflection | 65 / 82 |
| Rank on the closure subspace | 22 |
| Common kernel on the closure subspace | dimension 4 |
| Independent affine symmetry directions | dimension 4; all annihilated |
| Strictly positive dependency coefficients | all 147 positive, exact rational identity modulo closure |
| Independent exact quadratic derivative checks | 4,116 |
| Rejected corruptions | negative weight, missing weight, reversed row, wrong gradient |
| Event-specific descending deformations | 147/147 fixed words connect |
| Further deterministic predictions | 881/881 agree; one tangent case skipped |

The 881 further predictions consist of 436 valid connecting words and 445 invalid words. An invalid word is not evidence that the perturbed room is dark. Every perturbed polygon used in these controls was checked for closure, preserved edge signs, strict simplicity, and interior marks. These are exact fixed-word validation controls, not room or direction discovery.

## One-sided corner criterion and sign

Unfold a supplied word into the source plane. Let A(theta) be its target lift minus source and C(theta) the blocking corner lift minus source. Each is affine-linear in the coordinate parameters, so the event determinant

    P(theta) = det(A(theta), C(theta))

is quadratic, with P(theta0)=0. The limiting segment reaches the corner strictly between source and target. Every other reflection is transverse and lies strictly inside its wall; the final arrival is interior. These strict conditions survive in some neighborhood.

At a reflex right-angle corner's missing quadrant, each one-sided continuation either has no reflection or reflects at exactly one incident wall. Resolving the incident line on a side picks one open local sector; the appropriate sign of P characterizes that sector. There is no requirement that the labels left/right retain their names under an orientation-reversing wall unfolding. Signs must be transported through the actual unfolding.

Our implementation fixes the sign in the source plane: perturb the prescribed initial direction q to q + epsilon*side*(-q_y,q_x). If the corner and target lie at beta*q and alpha*q, with 0<beta<alpha, then

    det(alpha*(q + epsilon*side*perp(q)), beta*q)
      = -epsilon*side*alpha*beta*|q|^2.

Consequently the signed event polynomial is side*P, so its negative side is the side admitting the connecting word. Its derivative g gives the necessary first-order survival inequality g.delta>=0. Every one of these independently derived oriented rows matches Opus's row up to a positive factor, not merely up to an arbitrary sign.

A convex right-angle continuation is not needed by this certificate: all 147 events are reflex. Any general use of the convex case must remove retracing paths to the same physical mark; regularity of the unfolded point alone does not ensure a nontrivial connecting path between distinct room points.

## Why the first-order certificate proves a full neighborhood result

Rank alone would only constrain the common zero set of the linearized event polynomials. The positive dependency is essential.

Let V be the 26-dimensional closure subspace and S its four-dimensional affine-symmetry tangent space. Write the restricted signed gradients as g_i. Exact rank and symmetry checks give

    intersection ker(g_i) in V = S.

The saved strictly positive coefficients satisfy sum_i lambda_i*g_i=0 on V. If every g_i.delta>=0, their positive weighted sum is zero, so every g_i.delta=0. Thus the first-order survival cone is exactly S.

To pass rigorously to a uniform nonlinear neighborhood, normalize each nearby configuration by the unique positive axis-affine map restoring its first vertex and its first two signed edge lengths to their original values. Both first edge lengths are nonzero. This fixes translation and both independent scalings, and gives a smooth local normalization preserving the billiard connection relation in both directions. The normalized configurations lie in an affine slice whose displacement space H has dimension 22 and intersects S only at zero.

For every unit delta in H, some g_i.delta is strictly negative. Compactness of the unit sphere and finiteness of the events supply c>0 with

    max_i(-g_i.delta) >= c*|delta|, for delta in H.

The finitely many signed determinants are quadratic, so for a common M their remainders are bounded by M*|delta|^2. Taking |delta| sufficiently small makes the selected event polynomial negative. Also take the neighborhood small enough to preserve all the other strict wall-contact and endpoint conditions in these finitely many words. The one-sided criterion then produces a valid connecting path.

Hence the only nearby dark normalized configuration is the original one. Undoing normalization proves that the local dark set is precisely the four-parameter axis-affine orbit. The reverse inclusion follows from the already certified darkness and exact affine conjugacy for orthogonal billiards. No numerical sampling is used to justify this universal conclusion.

The argument proves existence of a neighborhood; this audit does not give an explicit numerical radius. It applies to the fixed horizontal/vertical edge directions and cyclic shape. Common rotation can be quotiented separately if one chooses a parameter space that includes it.

## Reproduction

From the workspace root:

    .context/illumination-venv/bin/python -B .context/illumination-k4-codex/rigidity-review/check.py
    .context/illumination-venv/bin/python -B .context/illumination-k4-codex/rigidity-review/certificate-check.py
    .context/illumination-venv/bin/python -B .context/illumination-k4-codex/rigidity-review/validate.py

All three scripts use Python's standard library and local Codex code; they do not need the peer venv. Run in a separate output copy to preserve receipts. `coverage.md` states the remaining limits.

## Consequence and next research gate

This establishes a local deformation obstruction for the known room, independent of its lattice subdivision. It supports the rigidity strategy at this one configuration. It cannot exclude a different 20-wall dark room or control degenerating sequences with short edges, contacts, or changing combinatorial type. Discreteness on a noncompact parameter space does not imply finitely many classes.

Opus retains the global rigidity conjecture and degeneration work. The foundations review `../proofs/l3-foundations-review.md` supplies corrections to the older unfolding and parameter-space discussion; those corrections do not invalidate the independently checked local certificate.
