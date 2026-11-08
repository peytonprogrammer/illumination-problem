# Review of the degeneration argument

[done] Reviewed Lemma7, Proposition8, weight and the proposed compactness reduction in the frozen `inputs/l3-analysis.md`. The robust-path persistence principle is sound under explicit local-convergence and endpoint hypotheses. The current weight conjecture does not hold over all blocked limits of simple rooms. Restricting to limits of dark sequences changes the assertion and leaves a substantial unproved exclusion problem.

## Exact eight-wall diagnostic

For 0<e<1 define

    P_e = [-1,e] x [-1,e] union [0,1] x [0,1].

Its cyclic boundary is

    (-1,-1), (e,-1), (e,0), (1,0),
    (1,1), (0,1), (0,e), (-1,e).

It is a strictly simple orthogonal polygon with eight maximal straight walls, area 2+2e, and distinct interior marks

    s=(-1/2,-1/2), t=(1/2,1/2).

The diagonal segment from s to t lies in the room interior for every e>0: its parameter u belongs to the overlapping intervals [-1,e] and [0,1]. Thus every approximant is lit. This is not a smaller dark-room construction.

As e tends to zero the closed rooms converge to

    P_0 = [-1,0]^2 union [0,1]^2.

The two squares meet only at (0,0). The limit interior has two components; every continuous connecting path from s to t must pass through that contact. If the contact is marked as a blocker, no billiard connection can exist, for purely topological reasons. Rescaling to unit diameter does not change the example.

Any weight definition satisfying the memo's asserted approximation property

    weight(limit) <= wall_count(P_e)

therefore assigns this blocked limit weight at most eight. This contradicts Conjecture9 when it quantifies over all blocked limits of simple rooms. It does not depend on an ambiguous convention for counting maximal walls at the contact.

If "limit configuration" is instead defined to mean only a limit of already-dark rooms, this example is not a counterexample to that narrower conjecture: these particular approximants are lit. In that interpretation, one must prove that a dark sequence cannot approach this type of disconnected limit. Assigning weight alone supplies no such proof. Excluding disconnected-interior limits from the statement also requires a theorem showing they cannot arise from the sequences being studied.

`check.py` verifies six exact instances e=1/2,...,1/64, closure, noncollinearity, nonincident edge separation, interior marks, area and eight walls. The direct-visibility and blocked-limit conclusions have the elementary proofs above; no ray search is used.

## Correct form of Lemma7

A sufficient version is:

Let a finite billiard word connect distinct marked points in a limit configuration. Its initial and final direction lie strictly in their admissible sectors; every reflection is transverse and strictly inside a wall face. The positive-length path avoids all limit corners, singular contacts and collapsed features. Assume that along this path the nearby rooms have the same local interior side and corresponding wall faces, with their endpoints and supporting lines converging. Then every sufficiently close configuration admits a connection with that word.

Proof: unfold the fixed word and use the moved target lift to determine the moved initial direction. The unfolded source-target displacement is nonzero. Transverse wall intersection denominators remain nonzero, contact times remain strictly ordered, and contact coordinates remain strictly within the walls. Every other wall has positive clearance from the relevant path pieces, and the endpoints have the stated admissible-sector margins. All these are finitely many strict inequalities, so they persist.

The arrival at a fixed target is not an open condition for a fixed initial ray. Adjusting the direction to the unfolded moving target is the missing detail in the memo's short proof. Hausdorff convergence of closed point sets alone is not a substitute for convergence of the traversed interior and wall faces. Coincident slit sides need their face labels retained.

## Correct form of Proposition8

For a sequence of dark configurations, every limiting connection that has the robustness properties just stated is impossible: persistence would light sufficiently late members of the sequence. This is a valid contrapositive.

One can call the limit "weakly dark" if that means exactly absence of robust liftable connections. It need not be darkness of an ordinary simple polygon. The following cases must be separated:

- Marks remain distinct interior points away from the collapse set. With suitable convergence of the walls/interior, the usual stopping-at-corners interpretation is available.
- A mark enters the collapse set or reaches the boundary. Requiring the whole path to stay a positive distance from that set makes every connection automatically inadmissible at its endpoint. Endpoint blockers must be excluded at departure/arrival and replaced by a precise sector-lifting condition.
- The marks coalesce. An ordinary dark pair must contain two distinct points; that property has been lost. The limit needs a separate marked-sector description.
- The limiting interior disconnects. Failure of connection can be purely topological, as in the eight-wall example.
- A corridor or region collapses to an interval. A finite list of blocker points alone may not encode the limiting wall faces or the lost interior. Keep a decorated boundary/face complex, and state where local path persistence applies.

The memo's observation that marks cannot coalesce deep in the interior is correct: if their separation is less than the distance of one mark to the boundary, their joining segment lies in an interior ball and lights the pair. It does not eliminate boundary-coalescence cases.

## Weight is not yet an exclusion invariant

A rigorous definition must specify the class of decorated limits, the retained wall-face multiplicities, the endpoint and blocker rules, a topology of approximation, and whether approximants are merely simple or also dark. It must then prove the wall-cost bound for each allowed degeneration. Claims such as "a notch costs two" are local construction counts, not a proof that arbitrary degenerations have additive costs or that the weighted blocked limit needs22 walls.

An induction also needs strict decrease of a well-founded complexity. Removing visible walls and then charging back the walls required to resolve the degeneration may leave weight unchanged. The currently stated count does not yet supply an inductive step.

## What a compactness argument would actually need

After fixing edge directions and shape, remove every available global symmetry before taking compactness. In the orthogonal class independent axis scalings are exact symmetries, so unit diameter alone leaves a noncompact affine freedom. One possible gauge fixes both bounding-box dimensions and translation; the remaining degeneration boundary must still be classified.

If the dark set in such a normalized parameter region is closed, stays away from the entire degeneration boundary, and every one of its real configurations is isolated, then it is compact and discrete and hence finite. This conditional step is sound. Checking local rigidity only at the known22- and24-wall examples does not establish its hypotheses. For a canonical-grid target, irrational real accumulation configurations must also be addressed.

Even finitely many classes provide only existence of a maximum representative exception count. They give neither an effective bound nor k<=4 automatically. The proposed larger-cap DRAT computation would be a subsequent mathematical obligation; the existing k<=4 theorem cannot be applied without that additional reduction and checked exclusion.

## Review decision

- ACCEPT Lemma7 with the fixed-word/local-domain/endpoint hypotheses above.
- ACCEPT Proposition8 as absence of robust liftable connections; require a decorated-limit definition before identifying that with ordinary darkness.
- COUNTER the unrestricted weight<=21 conjecture using the eight-wall blocked limit. Under the narrower dark-sequence reading, mark it open and explicitly require exclusion of disconnected and coalesced-mark limits.
- ACCEPT the compact-discrete-finite implication only after all its normalization, closedness and boundary-exclusion hypotheses are proved.

Next move: Opus should first define the precise class of limits arising from dark sequences and prove a non-vacuous boundary exclusion. The finite one-corner rigidity certificate remains valid and independent of these global issues.
