# Illumination strategy judgment

[done] The fan partition is the best-supported incremental route to a stronger lower bound within the canonical right-isosceles triangle family. There is no evidence yet that it is the most promising route to constructing a room below24 walls.

## Evidence and limits

The complete-cell argument closed the diagonal placement. The subsequent105-set skew experiment reached100 exclusions. The central fan refinement added393 illuminated configurations and786 guards, closing two additional whole cell sets and267/285 fan branches. This is real proof progress. However,102/105 does not mean97% of the research is done: cells contain very different numbers of room geometries. Eighteen fan branches remain feasible after the current cuts, and two other mark placements remain open even if this placement closes.

Earlier strategies have weaker experimental support: the direction-code quotient showed negligible compression; the midpoint-involution pilot covered no required lift pairs on the known controls; the tested30–60–90 patches produced no improvement. These failures concern those bounded implementations/certificates, not impossibility of the broader ideas.

## Recommended next step

Use one bounded second-central-cell split as a diagnostic, and inspect the remaining layouts and successful rays for a common connecting-path mechanism. Try to replace many individual ray guards with a small general illumination lemma. Such a lemma could address the remaining placements and explain the24-wall barrier. Its existence is a hypothesis, not a result.

Success should mean closing a whole placement or establishing a reusable geometric mechanism, rather than merely increasing the fraction of branches excluded. Do not indefinitely increase solve limits or recursively split fans without reassessing this return.

If the target is a smaller construction, a different geometry/blocking mechanism deserves separate effort. There is no better-supported specific construction proposal yet. A surface-only obstruction is insufficient: every target lift and a valid planar billiard realization must be handled. Wolecki explicitly distinguishes arbitrary translation surfaces from polygon unfoldings, so this is a substantive compatibility gate, not bookkeeping.

Primary source checked: [Wolecki, Illumination in Rational Billiards, sections1–2](https://arxiv.org/html/1905.09358v3). [Lelièvre–Monteil–Weiss, Everything is illuminated, Proposition16](https://arxiv.org/html/1407.2975v1#S6.SS1) supplies an alternative ramified-cover blocking mechanism; it does not supply a smaller simple planar room for this project.

Local evidence: `three-triples/fan-findings-2-1.md`, `three-triples/fan-audit-2-1.json`, and the direction-code/midpoint pilot sections of `illumination-analysis.md`.

Claude has resumed his strengthened independent model, according to his current board line. His results remain pending. No new solver run or research delegation was started for this strategy review.

**Next move:** inspect the18 remaining fan branches for shared connecting-ray structure before choosing the second split in detail.
