# Fable frontier — structural route

Revision 2, 2026-11-08, after reviewer F1–F10 and `nonemptiness-next.md`. Fable (Claude Fable 5.1, Conductor chat "Illumination problem improvement") read `direction.md` and `nonemptiness-next.md` in full. Native goals, accounting, waivers, clocks, and frozen artifacts unchanged. No new workers, searches, censuses, engines, fitting, frozen-file edits, or git mutations.

## Owned files

- This file.
- `fable/general-geometry-00-reconciliation.md` — F1–F10 dispositions (all ten accepted; false statements retired with provenance).
- `fable/general-geometry-01-lifting.md` rev 2 — Lemma L (unramified start), Corollary R, Theorem E, torus version of the trivial-fold class.
- `fable/general-geometry-02-r3-shapes.md` rev 2 — eight turn types; three simple charts of the spiral type; transposition corrected.
- `fable/general-geometry-03-reduction.md` rev 2 — Propositions 1–2 (fold-map classification; torus covers vacuous), Lemma M (chosen-lift covering form = vertex walk), degree-3 genus-2 case as a per-room test.

Earlier `claude-illumination-check/spiral-selection-critique/findings.md` (residue-ladder review) stands; its hand instance was re-verified on 2026-11-08.

## Result of the structural route so far (verified, partial)

Negative, proved: for an ordered spiral with corners in all three parity classes, no translation covering of O_D available without a per-room block-system coincidence reduces illumination to a smaller surface. Rectangle and torus covers are vacuous for even-even pairs (Proposition 2); L-room folds exist only on 4-parameter subfamilies and still leave a 3-way sheet choice (Proposition 1). Induction on reflex corners by coverings is therefore not a general route; the premise is replaced.

Replacement premise (Lemma M): with the chosen target lift kept, illumination in direction θ is membership of T~ in the forward σ_θ-chain of S~, where σ_θ is a partial injection on the finite set of A-lifts. The chain reaches T~, ends at a corner, or cycles back to S~. Nothing structural forces the first outcome for some θ; that is the nonemptiness gap in walk form.

## Candidate for the next step (stated, not proved)

Lemma W (walk-cycle exclusion). For an ordered spiral and a residual pair, let θ range over rational directions with |p|,|q| ≤ Q(D) for the author's accepted finite first-cap bound Q. If for every such θ the σ_θ-chain of S~ ends at a corner before reaching T~, then the pair is dark (this is result 12 and needs no proof). The open claim is its contrapositive in a usable form: exhibit θ for which the chain from S~ contains T~.

Proof obligation that would make Lemma W a structural statement rather than a restatement: a bound C(D) on the number of distinct σ_θ-chains that pass through the source arm's A-lifts, uniform in θ, together with a count showing that the chains through T~'s bottom-chamber A-lifts and the chains through S~ cannot all be disjoint. I do not have such a bound. The chain count per direction is about (area)·|θ|/(leaf length) and is not small; so a counting argument fails as stated. This is recorded as a dead end, not a plan.

Coordination with the author's return map: the author's relation on (position, signed direction) at the left mouth is the first-return map of σ_θ to the source-arm A-lifts (03 §3). Its iterate structure is the chain trichotomy. The property the author needs is: for some θ, the S-exit state's chain contains the T-entry state. A symbolic obstruction would be a θ-independent reason the two states lie on different chains; I see none, and none is claimed.

## Falsification

The structural route is falsified as a reduction already (Propositions 1–2). Lemma M cannot be falsified; it is an identity. A dark residual pair in an ordered spiral would falsify the milestone; result 12 makes that a finite check per pair, which needs Daniel's approval to run.

## Status

Partial. Corrections complete; no nonemptiness progress. Full ordered/r3/r ≤ 8 goal open.
