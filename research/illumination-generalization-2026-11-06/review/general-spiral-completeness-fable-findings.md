# Independent prerequisite findings on Fable's structural route

These findings concern the observed drafts fable/general-geometry-01-lifting.md, 02-r3-shapes.md and fable-frontier.md. They are not a final rejection of a corrected structural programme. Fable owns those files; no peer source is edited. The correct actual-endpoint and bad-set distinctions in the proposed Lemma F are retained.

## F1 — CORRECT: a ramified starting point does not determine a unique lifted prong

Lemma L as written allows gamma(0) to be a branch value and asserts uniqueness from x0 and the BASE direction alone. This is false. At a cone of angle 2pi*k mapping to a regular disc with local degree k, the base ray with angle theta has k distinct outgoing prongs at angles theta+2pi*j. All start at the SAME apex x0 and project to the same base ray. Specifying x0 does not select j.

Repair: require the chosen initial preimage x0 to be unramified and locally regular, or supply a specific outgoing lifted sector/prong. If the base starts outside branch values, the ordinary unique lift applies. A ramified final point may be reached by a unique continuation of an already selected interior lift; it does not cause the same starting ambiguity. The actual interior room source is regular on its unfolding, so a true translation-surface covering cannot ramify there; the needed actual-source version can therefore be recovered. Do not extend that fact to the orbifold example without its separate local analysis.

## F2 — CORRECT: four-copy sheet symmetries are affine isometries, not translations

The four-copy construction gives the usual translation surface, but the Gamma action permuting copies has linear parts id, the two coordinate reflections, and their product. It does not act entirely by translations. Existence of a billiard path may still be moved to another starting lift using the corresponding affine symmetry and transformed direction. The reason is preservation of the original projected billiard path, not a derivative-I deck action. This matters for fixed-direction and marked-sheet claims.

The reflex angle in the actual four-copy surface is 4*(3pi/2)=6pi; convex corners are regular marked points. That part is correct.

## F3 — REJECT the unproved restriction to global symmetry quotients

A translation covering need not be regular/Galois and need not be a quotient by a global translation automorphism group of the domain. A transitive monodromy action can have a nonnormal point stabilizer, so the covering has fewer deck transformations than sheets. This general covering-space distinction must be retained when claiming which reductions are available for all ordered spirals.

More directly, EVERY integer orthogonal room already has the coordinate-mod-Z^2 translation covering from its four-copy unfolding to the unit torus. On copy g use g(p) modulo Z^2. Across an integer-coordinate wall the chart transition differs by an integer translation, so this is globally well-defined. The map is locally a translation away from finitely many vertices and has finite degree 4*area(D). It does not require extra metric symmetry or a common divisor larger than one. Its existence does NOT prove illumination: all native endpoint lifts map to the same base point, and selecting the actual T fiber member remains the hard part. Also many regular transparent points lie over the same base point as the bad vertices, so two-sided bad-set matching need not hold.

Thus "only symmetry quotients exist" and "a quotient exists only for extra common period structure" are not established reductions or obstructions. If intended for a more restricted marked/reflection-compatible class of coverings, state and prove those additional restrictions first.

## F4 — CORRECT: transposition does not preserve the ordered chart

The exact global coordinate swap gives the normal-form parameters

(a1,l1,w1,A1;b1,c1,h1,H1)=(c,b,h,H;l,a,w,A).

For the ordered input b<c and a<l, this has a1>l1 and c1<b1. It lies in the accepted enlarged vertically separated chart, not again in a1<l1 and b1<c1. This exact map was independently audited in WJ01. Ordered spirals are still a proper immediate milestone and do not exhaust all r3 rooms; that conclusion is correct. The map error must not be used to remove the other metric charts or claim a structural classification is complete.

The eight turn-gap MULTISETS themselves match the established partition after adding one. That is combinatorics, not illumination, and no reopening of the accepted partition is needed. The full goal here is explicitly orthogonal; general diagonal canonical45 remains separate, so it is not silently added to the orthogonal r3 milestone.

## F5 — REJECT: cone points need not map to cone points or stay distinct

For a local translation covering, cone multiplicities satisfy m_X=e_local*m_Y, where total angle is 2pi*m. A domain 6pi cone can map with local degree 3 to a REGULAR 2pi base point. Even an unramified cover may send several distinct domain 6pi cones to the same base 6pi cone. Therefore "a covering cannot merge reflex corners because cone points map to cone points" is false. It does not prove that reduction of the reflex complexity is unavailable.

A useful replacement is the following precise GENERAL constraint. The unfolding of an orthogonal r=3 room has genus 4 and exactly three 6pi cones. For a nontrivial translation covering to a compact translation surface of genus at least 2, the ONLY possible case is an UNRAMIFIED degree-3 cover onto genus 2 with ONE 6pi cone.

Hand derivation: the base can only have multiplicities 1 or 3, because all domain multiplicities are 1 or 3. If its genus is >=2, it has q>=1 cones, all 6pi, hence q=g_base-1. Each base cone has d distinct unramified domain cone preimages. Any remaining domain cone must be a degree-3 ramification over a regular base point. Thus 3=d*q+b. With d>=2, q>=1, this leaves d2/q1/b1 or d3/q1/b0. The former would require a local degree-3 branch in a degree-2 cover, impossible. The latter is the stated degree-3 unramified genus-2 case. Genus-one torus quotients remain possible and include the standard coordinate cover, with ramification over regular base points. This is a necessary structural constraint, not proof that a desired marked cover exists or that its segment lifts to T.

Fable retains ownership of pursuing that structural alternative. The reviewer is identifying which covering premises need proof, not taking over the reduction construction.

## F6 — CORRECT category: the reflection orbifold is not a translation surface

Section 5 applies a theorem stated for translation coverings between translation surfaces to the mirrored (4,4,2) reflection orbifold. That is a different local category. The midpoint fold argument may be developed separately, but the application is not justified by Lemma L as presently written. Supply the orbifold path/prong/development statement or cite the already accepted exact reflection-fold proof at its original scope. This is not a rejection of that existing fold theorem.

## What remains valid and what needs reconciliation

With a regular/unramified starting lift (or explicit prong), the local-translation path-lifting principle is sound. The bad-set inclusions in Corollary R have the right respective roles: projection needs inverse bad fibers forbidden, while safe lifting needs original bad points mapping into the avoided base set. Correct endpoint-fiber selection is explicitly retained in Lemma F and remains unproved. Those are useful prerequisites; they do not prove a general reduction.

The next structural claim should therefore specify a genuine covering, its local branching/prongs, exact bad-set hypothesis, a provably simpler base and the actual T sheet. A base legal segment ending at another point of phi^{-1}(phi(T)) does not solve the original problem. Allowing the identity and an already illuminating segment makes Lemma F an equivalent restatement rather than a reduction theorem. No generic covering existence or topology alone supplies the endpoint clause.

All findings are hand reasoning. No new worker, numeric example, search, census, engine, clock or git mutation was used. These are draft observations pending Fable's explicit corrections/replies and fresh pinning; full r3/r<=8 remain open.
