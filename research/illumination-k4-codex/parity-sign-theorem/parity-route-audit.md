# Independent audit of the pocket parity route

2026-11-02. Bounded review authorized by Daniel. No discovery of rooms, directions, paths, words, cylinder cores, or orbits. Replayed one supplied contact list only. Opus retains ownership of the parity proof.

## Verdict

1. ACCEPT the supplied 42-contact (3,2) witness in the fixed Section33 room. It is a legal periodic trajectory with nonzero absolute slide response.
2. ACCEPT the local seam-cycle and connected-double-cover construction under the stated raw room and additional-diagonal-wall hypotheses, with the chamber argument below.
3. DO NOT infer an odd cylinder core from nontrivial cohomology or connectedness of the double cover. That implication fails on square-tiled surfaces in general. A rigorous obstruction is given below; it is not a counterexample in the raw-pocket-room class.
4. Even a universal odd-core theorem would leave the actual source/target midpoint-event coupling obligation.

## 1. Independent fixed-certificate replay

Inputs: the first contact list in peer `claude-illumination-check/b-not-in-k/certificate-3-2.log`, and the fan assembly in Codex `pocket-detection.md` Section33. The checker imports no peer tracer, geometry helper, or frame code.

Reconstructed the 28 triangles and canceled their shared edges: 26 atomic boundary segments, 25 actual corners/maximal walls. The one redundant collinear boundary vertex is not treated as a corner.

Starting at (11/10,9/10) with velocity (-3,-2), checked the supplied 42 successive points using exact rational arithmetic. Each displacement follows the current velocity forward; every segment has no earlier boundary contact; its midpoint lies inside the triangle union; its final point is a unique smooth wall contact. The tangent reflection formula supplies the next velocity. The final position, velocity, and full unfolding frame equal the initial ones; no earlier contact closes that full state. The unfolding frame closes to I, so this is closed on X, not just a physical periodic billiard with residual sheet change.

The pocket crossings are an exit at (1,5/6) and an entry at (1,3/4). There is exactly one D contact (the last listed point) and no H contact. With initial unfolding frame I the exact response is

    Q = (-1,-1),    holonomy = (-54,-36).

The latter equals 18 times the initial velocity. A different initial D4 frame can rotate/sign-change the response; its nonvanishing and odd coordinates are invariant. The single moving contact also gives an independent short argument: a signed-permutation image of the D displacement (1,1) is nonzero. No cancellation between moving contacts is possible.

Four corrupted inputs are rejected: a displaced contact, an omitted contact, a changed initial direction, and reversed initial velocity. The checker was initially too strict about the portal count (it conflated one entry with all crossings); it was corrected to count oriented entry and exit separately. This did not change the peer path or result.

Receipt: `parity-witness-check.json`. Reproduce:

    python3 -B .context/illumination-k4-codex/parity-sign-theorem/parity-witness-check.py

This writes the adjacent JSON. An independent reviewer should copy the checker and inputs or redirect its output path into their own directory. The receipt binds the checker and peer input hashes. It does not verify the peer's other29cores or complete strip census.

## 2. The seam is a nonzero mod-2 cycle

Let sigma_D be the union of the four D seams in the standard eight-copy unfolding X. Each seam joins the unique lift of the odd-angle A corner to the unique lift of the odd-angle B corner. Four seam edges are incident at each endpoint. Thus its boundary is zero over F2, including at the regular A tip. This gives a closed mod-2 one-cycle and a dual class phi_D in H^1(X;F2).

For nontriviality, use the copies of the physical room as chambers. Delete all D seams. Each chamber interior is connected, and crossing any remaining open wall connects the corresponding pair of D4 sheet labels. The fixed axial flanks of a literal straight-attached pocket provide an axial reflection. The assumed additional diagonal wall provides a diagonal reflection. These two reflections generate D4, so the chamber adjacency graph through the remaining walls is connected. Crossings can be chosen away from all wall endpoints.

Take two points on opposite sides of one smooth D-seam point. Join them in this connected complement; close the path by one short transversal through D. The resulting closed curve meets sigma_D once mod2. Therefore phi_D is nonzero. This proof does not straighten that curve, and makes no cylinder claim.

Since phi_D is an absolute cohomology class, it defines an unramified two-sheeted cover X_D -> X, connected because phi_D is nonzero. Pull back the translation differential. For a rational cylinder with primitive core c, the restricted cover is connected precisely when phi_D(c)=1. If phi_D(c)=0, its preimage consists of two separate cylinders. The connected case is one annulus covering the original cylinder twice around its circumference.

Together with Q(c) = (#D contacts)(1,1) mod2, an odd cylinder core suffices for nonzero response. The reverse implication fails: the peer's (2,1) cores already have nonzero even responses.

## 3. A rigorous obstruction to the generic cover shortcut

**Lemma.** Let X be a square-tiled surface, and let C_Q be the rational span in H_1(X;Q) of all rational cylinder cores. If C_Q is proper, there exists a connected unramified double translation cover Y -> X for which the preimage of every rational cylinder of X is disconnected.

**Proof.** Write L=H_1(X;Z), a free abelian group. A proper rational subspace C_Q has a nonzero rational linear functional ell vanishing on C_Q. Choose an integral basis of L, clear denominators in ell, and divide all its coefficients by their greatest common divisor. The resulting integral functional ell:L->Z is primitive, still vanishes on every cylinder core, and reduces to a nonzero functional bar(ell):L->F2. This gives a nonzero H^1(X;F2) class and hence a connected unramified double cover. On every cylinder core c, bar(ell)(c)=0. The restricted annular cover is therefore trivial, giving two cylinders. Pullback of the square tiling makes Y square-tiled too. QED.

Such base surfaces exist. The previously source-checked genus4 q=3 Matheus–Yoccoz origami has cylinder span equal to its two-dimensional tautological homology, inside eight-dimensional absolute homology; see `pocket-reflection-gate.md` Section11 and peer `review-gate11-12/findings.md`. The primary source is https://arxiv.org/pdf/0912.1425 (v2), Theorem1.17 and Section3. The source gives finite affine action on the six-dimensional complementary rational summand. A positive rational cylinder multitwist is unipotent, so acts trivially there; its positive sum-of-squares pairing formula forces every cylinder core to annihilate that summand. Horizontal and vertical cores then show that C_Q is exactly the tautological plane. This is the already accepted deduction in Section11, not a fresh matrix experiment or a claim made verbatim by the paper.

Consequently connectedness alone cannot imply odd cylinder monodromy, even with square tiling. This counterexample concerns general translation surfaces and general mod-2 classes. It does NOT show that the specific phi_D of any raw pocket room kills all cores. The published origami is already excluded as a geometric translation factor of our room class by Section13. The lemma is a gate against a generic covering argument, not a refutation of universal pocket detection or a recommendation to resume dimension/module work.

## 4. The actual S/T obligation remains independent

The fixed witness is a closed periodic trajectory whose starting point is on D. It is not a one-corner path between the actual S=(-4,0) and T=(0,0). Nonzero Q on that cycle does not change its endpoint labels into S,T.

The existing valid transfer in main Section32.3 starts with a supplied actual midpoint event eta, preserves its endpoint labels and embedded intrinsic pi-sector under pure affine maps, and uses a nonzero normalized overlap contrast in (32.4). The four-term identity (32.5) then forces one actual image to detect the slide. The contrast is an additional geometric statement; a loaded cylinder or zero-mean load alone does not establish it. For the unbounded objective, seed existence itself remains open in general. For the separate small-wall application, existing bounded seeds can be used, but the response/coupling gap still remains.

## 5. Coverage, decision, and handoff

Completed the authorized fixed-witness replay and the seam/cover sufficiency audit. The concrete advance is independent acceptance of the witness. The concrete obstruction is the failure of the generic connected-cover-to-odd-cylinder implication, proved above. No general parity theorem or in-class counterexample has been obtained.

Opus needs a geometric property special to the literal pocket seam that excludes this type of cylinder blindness. Another nontriviality proof or a generic covering reformulation will not do so. Codex has no new credible universal endpoint-coupling argument from this audit; the earlier module and empty-triangle limits remain in force. Stop this bounded task after delivering the result; do not launch a larger check campaign.

Independent peer request: hand-check Sections2--3, particularly the primitive-integral-covector reduction and its scope; independently replay the one supplied witness using the script in an owned output copy. No optical search is requested, and no peer review is claimed complete until received.


## 6. Assessment of Opus two-direction update (2026-11-02)

Opus independently accepted Sections1--3 without corrections and replayed the fixed witness in its own directory; see peer `review-codex-parity-audit/findings.md`. This is received peer verification, separate from our independent witness check.

Peer `b-not-in-k/findings.md` Sections8--9.1 reports that every one of 210 literal pockets in 56 of 57 existing rooms has a loaded core in direction (1,1) or (2,1). These are peer computations with a second tracer; Codex has not independently replayed this census. The proposed universal two-direction conjecture is sharper than arbitrary-direction detection, but remains unproved.

Evidence for the difficult implication is much smaller: among those 210 pockets only one is diagonal-blind. Together with the separately supplied Section33 room, there are two known diagonal mirror pockets, with identical nearby geometry. The 62 pockets blind at (2,1) all load diagonally. Thus the broad count chiefly supports the already available diagonal alternative; it does not provide 210 independent tests of the mirror-room implication.

Answer to Opus's exterior-return question: this audit supplies no constraint linking the two directions strongly enough to exclude simultaneous blindness. Separate zero-sum cycle conditions are not a compatibility theorem for return maps realized by one raw planar room. Conversely, abstract balanced permutations in two directions would not be an in-class counterexample without that common geometric realization. The generic double-cover obstruction in Section3 remains insufficient for either conclusion.

A bounded hand target is to test whether diagonal mirror behavior forces the reported local configuration. It must explicitly handle branches escaping the inspected neighborhood, rather than assuming a finite local classification. Even a successful local classification leaves a second obligation: force an unbalanced (2,1) core despite all allowed exterior returns. Mixed local patterns in Section8 do not refute a classification conditional on diagonal blindness, but they warn against concluding global cycle balance from a fixed neighborhood alone. A proof needs a forced complete itinerary or an invariant controlling those exterior returns.

Recommendation: keep the two-direction statement as a focused conjecture and assess the proposed conditional local classification by hand. Do not expand the census on this assessment's authority. Its proof would settle existence of a loaded periodic core (target1); it would still not supply the actual S/T one-corner midpoint event or prove universal 22-wall minimality. No new proof, computation, or discovery search was performed in this bounded assessment.


## 7. Reply to Opus Section10: rawness and mirror-loop length

Read peer Section10 and the existing raw fan-tree rules in main Sections1/24/26.4. This is a bounded hand assessment; no independent verification of every Section10 geometric assertion or new experiment is claimed.

Opus asks whether rawness bounds the mirror-band length k. I have no proved uniform bound. The local 270-degree observation does not by itself bound the number of C corners, and an upper bound on their number would additionally need a bound on how often the band uses each corner/prong.

The already accepted fan incidence rules do not supply a uniform size bound: a partial fan with (m,q)=(4,0) has outdegree1 and may have indegree1. Subdividing an oriented tree edge by any number of vertices with this degree pattern preserves the tree identities and the source/merger counts. This is only a combinatorial limitation of those rules, not a construction of embedded raw rooms or mirror bands of arbitrary length. A geometric argument might still forbid the chains specifically for mirror bands.

Another exact necessary condition is available but also insufficient: append the portal endpoint to close a supplied mirror return in the remainder. Each interior BC crosscut separates the disk, so a transverse closed path crosses each such cut an even number of times. A tree forces backtracking in its projected walk, but supplies no bound on the number of backtracks. Optical reflection can return through an earlier portal; combinatorial backtracking alone is not a contradiction or a corner hit.

Reply: do not treat the rectangle examples as counterexamples to a rawness bound, or a finite local case tree as exhaustive until escaping/repeated branches are controlled. A successful bound needs a geometric restriction on repeated visits or on which indegree1/outdegree1 chains a mirror band can traverse. Neither is currently proved here. A uniform k bound is also stronger than necessary for target1: the original two-direction incompatibility could hold for arbitrary k. No new credible bound or in-class counterexample resulted from this assessment; no enumeration is authorized by it.
