# Assessment of the illumination contributions

2026-11-02. Retrospective assessment for Daniel and Peyton; no new experiment or discovery search.

## Priority assessment from published sources

Wolecki's published Theorem 1.3 already establishes a 22-edge upper bound. The present construction therefore does not improve the unrestricted numerical bound. Its exact geometric identity with earlier examples remains unresolved; historical novelty is unconfirmed. Treat it as an explicit, internally reviewed construction and exposition, with no confirmed original-research claim.

Published comparison sources include Wolecki (https://arxiv.org/html/1905.09358v3), Hubert--Schmoll--Troubetzkoy (https://arxiv.org/pdf/math/0602394) and Monteil (https://numdam.org/articles/10.5802/aif.2124/). These establish relevant prior work without proving coordinate identity with the present room. The restricted lower bound and later positive illumination results require their own priority assessments.

## Earlier candidate-contribution assessment

A strictly simple orthogonal 22-wall room, made of 15 unit squares arranged as three reflected copies of a five-square staircase, with two distinct interior marks that cannot illuminate each other under finite corner-avoiding billiards. The construction has a hand proof and independent internal geometry/dynamics reviews. A distinct four-copy 30-wall extension is also supported by the clarification review.

The precise potential novelty is the compact simple orthogonal realization. Wolecki already published a general 22-edge upper bound; his paper also acknowledges Monteil's unpublished 22-gon. Our audit distinguishes the displayed Wolecki construction and the 34-wall orthogonal O'Rourke figure, but does not establish historical priority over all earlier work.

Evidence: novelty-audit.md; proof-adversarial-review/findings.md; proof-clarification/peer-review.txt. Primary prior art checked again: https://arxiv.org/html/1905.09358v3, Theorem 1.3, acknowledgment, Remark 2.2.

The parity argument and convex-corner retracing are established ingredients. Our seam-endpoint analysis makes their use in this particular construction rigorous; it should not be presented as an invented physical mechanism.

## Restricted lower bound

The certificate-backed result through k=6 excludes W<=21 for strictly simple slit-free canonical 45-degree tile rooms with two interior even-even A marks and at most six transparent non-A lattice vertices (interior or smooth boundary points). Thus 22 is optimal in this specified class. It is not a theorem for arbitrary polygons, arbitrary marks, or unlimited exceptions. Dilation makes k unbounded, so k=6 does not finish a universal reduction.

Evidence: k5-proof-continuation/findings.md; peer k6-run/findings.md; k6-i4-review/findings.md; k6-final-review/findings.md. Local proof checking covers the reported formulas; independent peer review of k6 includes all case/hash/base-prefix checks and sampled optical/proof replay, not an independent replay of every certificate and guard.

## Constructive elementary results

L rooms: for arbitrary real dimensions and distinct interior marks, there is a connection using only vertical-wall reflections, and another using only horizontal-wall reflections. Any boundary blocker set confined to one wall orientation is avoidable.

U rooms: the stated rectangular U family permits a corner-free connection between every pair of interior points, including unequal arm sizes and arbitrary upper-arm mark heights. The opposite-arm construction has one bottom reflection and finitely many vertical-wall reflections, using repeated lower-passage traversals. It does not prove arbitrary singleton-blocker removal. The new opposite-arm proof has a separate symbolic review; the live coordinating-peer review is still recorded as pending in its report.

Evidence: single-boundary-blocker/l-monotone-proof.md; two-reflex-blocker/all-heights.md. These are concrete internally established arguments, but their literature priority has not been audited. Do not call either the first theorem of its kind.

## Supporting results and evidence

The labeled finite-orbit method can in principle decide darkness exactly for valid canonical rooms with interior integer marks, once its complete finite orbit is exhausted. It is an application of established unfolding/group-action ideas. Capped UNDECIDED runs do not certify darkness; boundary endpoints need additional conventions. Evidence: origami-decider-review/findings.md.

The saved raw parity census has 327 room/mark classes through 26 walls: 12 at 24, 89 at 25, 226 at 26. All saved geometries were independently checked. Opus reports rigidity certificates for all 327; Codex independently replayed six. These support local isolation with fixed wall directions, modulo translations and scaling. They do not establish a universal sign theorem or isolation against arbitrary wall-angle changes. Evidence: parity-cert-review/findings.md.

The empty-triangle composition lemma and geometric-factor exclusions are supporting theory with explicit hypotheses. No separate literature novelty has been established for them. They do not supply universal actual-event existence or nonzero pocket response.

## Unresolved

No proof of universal 22-wall minimality. No universal pocket-detection theorem or in-class counterexample. No completed reduction of every dark polygon to the enumerated lattice class. No confirmed historical priority for the construction.

## Recommended emphasis

Lead with the simple orthogonal 22-wall construction and its readable proof. Present the k<=6 lower bound as a separate computer-assisted result with full scope. Treat L/U arguments as potential secondary contributions requiring literature checks. Keep the large universal-theorem campaign and its unresolved gaps separate from completed discoveries.
