# Illumination results inventory

Snapshot: 7 November 2026. Prepared for Daniel while the existing author/reviewer pair continues its three-reflex work. This is an inventory and assessment, not a fresh independent proof review of every result.

## What deserves the most attention

The strongest established contributions in the project record are: the sharp lower bound in the restricted lattice model; complete arbitrary-real illumination for orthogonal rooms through eight walls; the exact four-parameter twelve-wall corridor theorem; unrestricted one-sided middle-row comb illumination and several complete two-sided comb classes; and eventual illumination/propagation in fixed long-neck families. The newly accepted tall ten-wall spiral theorem is a smaller, constructive extension.

No result currently has confirmed historical novelty. The 22-wall dark construction should be described as a likely independent rediscovery. The exact corridor theorem has the most developed existing priority audit. The eight-wall theorem, comb theorems and neck results are worthwhile candidates for focused priority review. A correct new proof of a known statement can also be useful, but has not been established as historically new here.

Do not count each guard, residue table, fixed path, or acceptance receipt as a separate discovery. Results below are grouped by substantive conclusion. Quantitative refinements and narrower dependencies are identified rather than added again to the headline count.

## Conventions

Illumination means a finite path from the specified source to the specified target, with ordinary equal-angle reflections at smooth walls and no physical polygon-corner contact. “Walls” means maximal straight sides after collinear edges are merged. For orthogonal disks, W=2r+4, with r the number of inward/reflex corners: eight WALLS means two reflex corners; the present target of eight REFLEX corners permits twenty walls.

A canonical45 room is a disk assembled from the specified 45–45–90 lattice triangles. It need not be triangular in outline. A marks are even-even lattice points. The parameter k counts transparent non-A lattice points, meaning interior or smooth-boundary non-A points. Bounds involving k depend on that fixed lattice presentation.

An acceptance below means independent internal AI mathematical review, sometimes with exact independent computation. It does not mean publication, expert refereeing, or formal proof-assistant verification.

## A. Completed illumination and minimum results

### 1. Sharp 22-wall minimum in the k<=6 lattice model — [done]

Every strictly simple canonical45 disk with W<=21 and k<=6 illuminates every pair of distinct interior A marks, for every support. The known dark 22-wall example has k=4 and attains the bound inside this model. Thus this is a genuine sharp restricted minimum, not just a search finding.

The computer-assisted argument derives finite support/geometry domains, validates continuous path guards and their clause provenance, and uses checked contradiction certificates. The final theorem records 64 refutations and 193,480 guard records. I inspected the reconciled theorem/verification record; I did not rerun the multi-gigabyte certificate corpus for this inventory. Removing k<=6 remains unproved.

Priority: unconfirmed for the restricted lower bound; the dark upper-bound mechanism is established prior art.

Sources: [Restricted theorem](<SOURCE_WORKSPACE>/.context/illumination-k4-codex/restricted-theorem-note/theorem.txt); [Reconciled verification](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/baseline-and-gap.md).

### 2. Every orthogonal room with at most eight walls illuminates — [done]

Every distinct real interior pair in every strictly simple orthogonal polygon with W<=8 illuminates, for arbitrary positive real dimensions. This includes L, U, unequal-floor T, offset-corridor and staircase shapes, all endpoint placements and limiting parameter equalities admitted by strict simplicity. There is no lattice, exception, area or aspect-ratio cap.

This is one of the cleanest statements to extract from the project. The individual L/U/T/staircase proofs are ingredients and stronger orientation-specific constructions, not five additional wall-minimum theorems. Earlier frozen files with “staircase open/unreviewed” banners are superseded by final acceptance.

Priority: unconfirmed; nearby elementary illumination results exist. It deserves a dedicated exact-statement comparison.

Sources: [Whole theorem review](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/whole-staircase-independent-review.md); [Final acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/whole-staircase-acceptance.json).

### 3. Exact four-parameter twelve-wall corridor theorem — [done]

For arbitrary positive real d,g,h_minus,h_plus, take the union

    [0,2d] x [-h_minus,0]
    [d,3d] x [0,g]
    [0,2d] x [g,g+h_plus].

Every interior point of the lower outer chamber illuminates every interior point of the upper outer chamber. The widths/offsets are those displayed; this is not a statement for arbitrary three rectangles or all pairs throughout arbitrary twelve-gons. No rationality restriction or uniform reflection bound is asserted.

The proof combines one- and three-pass constructions, actual-endpoint cap transfer, and exact continuous endpoint covers of a mathematically bounded residual rational list. This is a computer-assisted universal parameter theorem, not a collection of sampled trajectories.

Priority: strongest existing documented novelty candidate in the inventory. The bounded audit found no exact antecedent, but did not exclude derivation from known covering/periodic-point classifications. No “first” or priority claim is justified.

Sources: [Completed statement](<SOURCE_WORKSPACE>/.context/illumination-k4-codex/symbolic-corridors/unequal-depth/completion.md); [Independent acceptance](<SOURCE_WORKSPACE>/.context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/whole-result-acceptance.json); [Novelty assessment](<SOURCE_WORKSPACE>/.context/codex-proof-verification/corridor-novelty/assessment.txt).

### 4. One-sided combs: no wall-count bound for spine/middle-row pairs — [done]

In any rectangular-spine comb with arbitrarily many teeth on one side, every distinct pair drawn from the spine and the middle horizontal lines of teeth illuminates. Dimensions, tooth heights, widths and endpoint depths may be arbitrary real numbers. Extra unused teeth do not enter the construction.

For integer rooms with teeth of height two, every interior A mark lies on the relevant tooth middle row or in the spine. Thus the theorem covers every actual interior A pair in that entire one-sided height-two class, without any W or k cap. It does not cover arbitrary off-middle-row marks in arbitrary real teeth.

The finite monotone floor-matching argument is a particularly compact proof ingredient worth extracting. Priority unassessed.

Sources: [Comb proof](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/midheight-comb-proof.md); [Independent acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/midheight-comb-independent-acceptance.json).

### 5. Complete infinite two-sided comb subclasses through 21 walls — [done]

These are actual all-pair A-mark theorems, without k, area, support or diameter caps:

- Integer unit-width, height-two teeth, every integer core width >=1, W<=21.
- Integer height-two teeth of arbitrary independent integer widths, core width one, W<=21.
- A further uniform-width-two, height-two class with integer core width >=3, W<=21, as recorded in the accepted continuation ledger.

Opposite tooth bands need not be globally separated where the cited theorem allows overlap. These statements do not combine into an arbitrary-width/arbitrary-core/arbitrary-height theorem. They are more substantial than isolated comb fixtures: each closes an infinite model class. Priority unassessed.

Sources: [Whole unit-width acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/unit-thin-whole-independent-acceptance.json); [Arbitrary-width core-one review](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/c1-arbitrary-width-join-independent.md); [Broader continuation ledger](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/coverage.md).

### 6. Two arbitrary fixed chambers joined by a long neck — [done]

Two fixed arbitrary-real orthogonal chambers joined through smooth mouths by a positive-width rectangular neck illuminate each fixed opposing-chamber pair for every sufficiently large real neck length. The threshold depends on the chamber/mouth/mark data and is locally uniform under nondegenerate perturbations. A separate constructive rational-data result extracts explicit beam intervals and thresholds.

This gives a substantive way to exclude one type of degeneration of dark candidates. It is not a uniform threshold in wall count, and permits only the stated fixed-chamber regime. Priority unassessed.

Sources: [Long-neck proof](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/long-neck-proof.md); [Acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/long-neck-independent-acceptance.json); [Effective rational construction acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/constructive-neck-acceptance.json).

### 7. Long-neck networks and exceptional arithmetic growth — [done]

For fixed three-chamber/two-neck families, possible long-neck failures concentrate near finitely many rational length ratios, sharpened to finitely many weighted affine strips. Integer data leave finitely many offset arithmetic rays; those rays are not thereby illuminated.

For a finite tree of fixed chambers joined by parallel, commensurate-width necks, one provided legal actual witness implies eventual illumination along nonnegative rational-affine length growth. Repeated passages, branches and same-side mouths are included. Witness existence and the finite initial range remain separate obligations. This conditional propagation theorem is useful, but not an unconditional all-network illumination theorem. Priority unassessed.

Sources: [Precise network statement](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/neck-ray-propagation-parallel-tree.md); [Independent tree acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/parallel-tree-independent-acceptance.json); [Affine-strip/network review map](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/bridge-scope-report.md).

### 8. Nested staircase sufficient conditions, beyond eight walls — [done]

Accepted nested-band and bounding-triangle inequalities guarantee illumination for arbitrary real interior pairs in the stated multi-band staircase families. They keep one common slope through every portal and choose an actual target image. The geometric inequalities are essential; this is not an all-staircase theorem for arbitrary numbers of steps or dimensions. Priority unassessed.

Sources: [Proof](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/nested-window-proof.md); [Independent scope/guards](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/nested-extension-independent.md).

### 9. Explicit reflection bounds at fixed three-star support — [done]

At the fixed interior A support S=(0,0), U=(2,0), T=(2,2), the surplus-layer results include a 13-reflection bound for the stated second-surplus class, 37 for third surplus, and 32 for fourth surplus. The final fourth-surplus proof permits the classified remote attachments; it is not restricted to a fixed local drawing. Its W<=21 and k<=6 assumptions remain attached.

These are quantitative refinements and constructive decompositions. Their existence conclusions overlap the broader k<=6 theorem, so they should not be presented as unrelated general illumination theorems. Local improvements such as the nine-reflection O3 lemma fit under this heading. Priority unconfirmed.

Sources: [Third-surplus theorem](<SOURCE_WORKSPACE>/.context/illumination-k4-codex/third-surplus-review/theorem.txt); [Fourth-surplus theorem](<SOURCE_WORKSPACE>/.context/illumination-k4-codex/fourth-surplus-review/global-four-closure/theorem.txt); [Local nine-reflection priority assessment](<SOURCE_WORKSPACE>/.context/codex-proof-verification/O3-combined/novelty.md).

### 10. Sharp minimum within strict whole-copy parity folds — [done]

For the exact construction class of whole congruent copies of a strict canonical base, with literal inverse-copy agreement and actual interior marks mapping to two distinct smooth boundary A points, a dark pair requires W>=22. The known example attains it. Diagonal bases and arbitrary initial rigid placements are included; the common-similarity extension has separate acceptance.

The proof derives assembly/exception counts and normalizes seams, then uses the k<=6 theorem. It does not show that every dark room admits the required fold. This is a second restricted minimum with an explicit dependency on result 1, not a second proof of universal minimality. Priority unconfirmed.

Sources: [Fold-class statement](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/fold-class-theorem.md); [Normalization acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/fold-normalization-acceptance.json); [Similarity extension review](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/fold-similarity-independent-review.md).

### 11. Positive ten-wall spiral progress — [done, restricted scope]

TR01 covers specified pairs in two protected subregions of an ordered three-reflex spiral for arbitrary real metrics. TR03, newly independently accepted during this inventory, covers EVERY distinct interior pair in the ordered spiral when its upper chamber height exceeds an explicit sufficient threshold. The threshold depends only on lower geometry, not on the selected marks.

The new proof constructs a positive slope interval, removes finitely many bad phase boundaries, and forces an exact target root into a surviving component. A possible singular roof event is handled only by discarding it and launching from a later return to the same actual source. Short roofs, other spiral orders and the other ten-wall types remain open. Priority unassessed; this is recent project progress, not an established novel publication result.

Sources: [Tall-spiral statement](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/three-reflex-candidate-03.md); [Full independent review](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/three-reflex-tr03-independent.md); [Acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/three-reflex-tr03-independent.json).

## B. Supporting mathematical tools worth preserving

### 12. Exact per-room decision framework and reusable path certificates — [done, scope-limited]

The labelled finite origami-orbit method gives an exact decision route for each valid fixed arithmetic room when its entire required finite orbit is exhausted. Capped undecided runs do not certify darkness. Exact rational trajectory guards certify paths for all tile completions satisfying their required/forbidden sets, not just one drawn room. These methods are central to reproducibility; unfolding/group actions/SAT proof certificates are established tools, not inventions claimed by this project.

### 13. A wall-bounded skeleton for every individual rational direction — [done]

The first-return marked graph has exactly q(W+2)/2 edges, with q<=8, hence at most 92 for W<=21. It retains actual source/target sheets, absorbing corners, prongs and positive integer edge lengths. Its size is bounded while weights and the number of directions are not. It supplies no finite universal list of directions.

Sources: [Directional skeleton](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/direction-skeleton.md); [Acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/direction-skeleton-acceptance.json).

### 14. Finite geometric atlases and strip generators — [done, geometry only]

Every marked canonical45 W<=21 geometry lies in a finite family of rational-linear sign cells with unbounded integer deformation coefficients. The orthogonal subclass has a bounded-base description using at most 44 commuting even-gap insertions; a single gap exposes a tree of at most five parallel necks. These are exact structural reductions of infinite geometry, not finite optical verification or darkness-preserving compression. Priority of their elementary polyhedral ingredients is not claimed.

Sources: [Atlas](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/polyhedral-atlas.md); [Atlas acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/polyhedral-atlas-acceptance.json); [Strip theorem](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/strip-generators.md); [Strip acceptance](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/strip-generators-acceptance.json).

### 15. Globally available geometric simplification — [done, geometry only]

Horizontal/vertical section completion and isolated-corner completion preserve literal interior marks, strict simplicity and the lattice, and provide a strict decrease in reflex count down to a rectangle. That is a genuine global geometric result. The necessary optical implication from a simpler illuminated room to the original is unproved; unrestricted transfer is false at the known dark example.

Sources: [Geometric reduction proof](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/geometric-reduction-proof-02.md); [Reconciled optical limitation](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/geometric-reduction-optical-impasse.md).

### 16. Arithmetic bridges and genuine affine transfer — [done, exact hypotheses]

The work classifies torus-covered four-direction rooms into similarity-rational or independently axis-rational classes and supplies exact endpoint/coordinate bridges under cited published results. This is a specialization/application of existing theory, not an asserted new general classification.

Separately, cylinder-period least-common-multiple shears give genuine global affine self-maps preserving the complete actual endpoint/corner data and primitive first-hit times. Their existence is proved. The proposed rank descent is only conditional and has an accepted obstruction, so it supplies no general induction.

Sources: [Intrinsic arithmetic bridge](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/torus-cover-bridge.md); [Weighted affine transfer](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/weighted-return-argument-01.md); [Independent scope](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/weighted-return-handoff.md).

### 17. Local exact shooting, corner repair and interception lemmas — [done, conditional]

Useful proved ingredients include: an exact arithmetic progression of target roots on a jointly guarded chamber interval; a sufficient width condition forcing a root; a one-floor-bounce repair under a supplied physical corridor; the regular-domain Farey triangle endpoint identity; and two kinds of supplied cone-chain configurations that force a second parity-distinct physical reflex corner under darkness.

A physical reflection-group calculation also proves that a specified equal-half axial pi-sector split through a cone has the same physical endpoint. Consequently a qualifying triangle between distinct endpoints in that axial case yields illumination. These hypotheses are not proved globally available, and repeated application need not find new physical corners. The lemmas are tools, not a nine-corner lower bound.

Sources: [Shooting theorem and limits](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/optical-routing-handoff.md); [Corner transfer](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/endpoint-transfer-argument-01.md); [Interception reconciliation](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/dark-interception-local-final-reconciliation.json).

## C. Strong negative results and research diagnostics

These results eliminate specific mathematical implications. Their importance is avoiding invalid generalizations, not accumulating counterexamples to every conceivable proof.

### 18. Few walls do not bound primitive direction complexity — [done]

An accepted square family already forces arbitrarily large primitive illuminating vectors, although its direct path has zero reflections. The work further rules out the proposed universal affine rank descent even in already illuminated squares. A bounded wall count cannot justify a direction cutoff or an axis terminal case.

Sources: [Direction/rank obstruction review](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/weighted-return-handoff.md); [Baseline scope map](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/bridge-scope-report.md).

### 19. No automatic geometric normalization or limiting argument — [done]

Reviewed examples refute the proposed bounded similarity/global-affine normalization. Piecewise-affine rescaling cannot preserve all straight crossings unless interface derivatives agree. Illumination at rational or nearby inputs does not automatically pass to a limiting exact pair. Adding/removing mirrors can change illumination. These invalidate named proof routes, not the low-wall conjecture.

### 20. No unrestricted Euclidean whole-copy explanation of darkness — [done]

The anisotropically stretched known dark Q100 remains dark under axial reflection-preserving scaling, but violates proved similarity-invariant bounds for the stated strict whole-copy factor class at its wall count. A separate repaired 43-wall beveled control defeats an unrestricted orthogonal-base-only converse while retaining a diagonal parity factor. Neither is a <=21-wall counterexample.

Sources: [Explicit Q100 obstruction](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/fold-area-invariant.md); [Fold/bridge review map](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/bridge-scope-report.md).

### 21. Separator, finite-blocker and abstract monodromy shortcuts are insufficient — [done]

Darkness yields a genuine-cone separator and local excluded-chord inequalities in a marked geodesic triangulation. The accepted bounded triangulation counts do not force nine distinct reflex corners. Ordinary finite blocking is automatic for arithmetic torus covers and therefore supplies no special darkness obstruction. The reviewed Heisenberg example shows abstract monodromy transitivity is insufficient, but is not physically realizable as a room of this class; it is not a low-wall dark polygon.

Sources: [Global proof frontier and controls](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/coverage.md); [Precise physical gap](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/construction/global-bridge-impasse.md).

### 22. A useful exact minimum of two reflections — [done, one prescribed pair]

A verified fourteen-wall room has an actual pair with no direct path and no one-reflection path across any wall, but an exact legal two-reflection path. Thus the minimum for that pair is exactly two. It disproves universal one-wall repair, not illumination or a larger reflection bound. Related two- and four-reflex controls refute universal availability of the sufficient repair corridor and width criterion.

Sources: [Complete one-wall exclusion and two-bounce witness](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/endpoint-transfer-et02-independent.md); [Endpoint review closure](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/endpoint-transfer-handoff.md).

### 23. Three failed global joint-selection shortcuts — [done]

A shortest complete-fiber path excludes the strict narrow cone angle needed by the triangle lemmas. On the fixed unit lattice, an exact all-word divisibility obstruction excludes the two short templates in dark Q100. Even after choosing two arms to one cone, physical symmetries cannot reduce their minimum sector angle below their original physical wedge separation. These leave arbitrary-weight, non-minimizing global existence open. Q0/Q100 have nine reflex corners and do not refute the eight-reflex goal.

Sources: [Reconciled availability frontier](<SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/review/availability-frontier.md).

## D. Construction, experiments and historical position

### 24. The readable 22-wall dark construction — [done, likely rediscovery]

The strictly simple orthogonal example made of three reflected five-square staircases has 22 walls, area 15 and a hand proof for two actual interior dark marks. Its seam/convex-corner handling and independent verification are valuable artifacts. Exact coordinate identity with that historical example is unresolved. The general 22-edge existence bound was already published. Present it as an explicit, verified construction or likely rediscovery, not confirmed original research.

Older parity-family censuses, selected rigidity certificates, fixed counterexamples and explicit paths support investigation. Some have full geometry checks but only sampled independent certificate replay. They are evidence within stated finite domains, not a universal classification or a separate minimum theorem.

Sources: [Superseding historical assessment](<SOURCE_WORKSPACE>/.context/illumination-k4-codex/discovery-assessment.md); [Construction source](<SOURCE_WORKSPACE>/.context/illumination-k4-codex/research-note.tex).

## E. Novelty judgment and unresolved claims

The project has substantive completed results; it does not have a confirmed novelty verdict. My recommended order for an exact priority/implication check is:

1. Exact four-parameter corridor theorem and its constructive computer-assisted proof.
2. Whole arbitrary-real orthogonal W<=8 theorem.
3. The compact one-sided middle-row comb theorem, complete two-sided comb subclasses, and long-neck/network statements.
4. The restricted k<=6 minimum and strict-fold corollary, with their full certificate/dependency scope.
5. Quantitative fixed-support bounds and the newest spiral/local results.

This ordering is judgment about clarity and interest, not a ranking of proven originality or publication significance. The largest established statement is not necessarily the easiest novelty claim.

The existing bounded novelty audits have not shown that the family-specific theorems follow immediately from standard finiteness statements. Finitely many possible dark pairs is not zero dark pairs. Conversely, a missing exact search hit does not exclude a nontrivial derivation from known covering/periodic-point theory. Fresh narrow searches for eight-wall/corridor specular theorems did not resolve priority; many hits concern floodlights/diffuse reflection, different problems.

Primary comparison sources re-opened for this inventory: [Wolecki, Illumination in Rational Billiards](https://arxiv.org/html/1905.09358v3) and [Lelievre–Monteil–Weiss, Everything is illuminated](https://arxiv.org/html/1407.2975). Prior family-specific comparison and its access limits are recorded in the corridor assessment linked above. No fresh exhaustive literature audit was performed.

- [in progress] Complete ten-wall/three-reflex optical theorem: only scoped families/placements are established.
- [blocked: no global optical argument] General orthogonal r<=8 illumination, and removal of k<=6 for all canonical45 W<=21 rooms, remain unproved by the current results.
- [blocked: no general lower-bound proof] Universal 22-wall minimality among arbitrary polygons is unresolved by this project.
- [blocked: no priority confirmation] No “first”, “novel theorem”, or publication-priority assertion is currently established.
- No established consequence for ETH or P versus NP. SAT/certificate machinery here verifies bounded geometric exclusions and is not an algorithm for arbitrary SAT.

## Inventory verification boundary

I read final theorem/scope summaries, selected substantive arguments and acceptance/reconciliation records. A fresh source-integrity check of 13 selected acceptance receipts verified all 96 inspected pinned files. That is not a re-proof, not a replay of the large corridor/SAT certificates, and not a complete audit of every historical intermediate artifact. Frozen corrections/addenda and later acceptance receipts supersede stale status banners only at their exact scopes.

The companion coverage JSON lists the checked receipt paths and hashes. This report groups interesting mathematical results rather than counting all local claims or transcript activity. The existing peers were neither interrupted nor reassigned.

**Next move:** Extract short, self-contained theorem-and-dependency synopses for the corridor, eight-wall, comb and neck results, then obtain focused priority/implication review before making novelty claims. No external communication is authorized by this inventory request.


## Current inventory addendum — 8 November 2026

This addendum updates the historical snapshot above. It inventories established project conclusions, not confirmed historical discoveries. Older theorem records retain their exact restrictions; the current research does not supersede them. Internal independent AI reviews and exact certificates are evidence, not external refereeing or a proof-assistant formalization. No new literature search or external communication was performed for this update.

### Completed positive results

| Result family | Exact useful conclusion | Principal limit |
|---|---|---|
| Restricted sharp22-wall minimum | Every strictly simple canonical45 disk with W<=21 and k<=6 illuminates every distinct interior A pair; a22-wall k4 dark example attains the restricted minimum. | Fixed tiling, A=even-even marks, k counts transparent non-A lattice points. No arbitrary-polygon minimum. |
| All-real eight-wall theorem | Every finite strictly simple orthogonal room with <=8 maximal walls illuminates every distinct REAL interior pair, with arbitrary real dimensions. | Eight walls means <=2 reflex corners. Complete10-wall theorem remains open. Corrected standalone packet and coordinator review supersede manuscript transcription errors. |
| Exact twelve-wall corridor | For all positive real d,g,h_minus,h_plus, every lower-chamber point illuminates every upper-chamber point in [0,2d]x[-h_minus,0] union [d,3d]x[0,g] union [0,2d]x[g,g+h_plus]. | These widths/offsets and endpoint chambers are essential. Not every12-wall room or all interior pairs. |
| One-sided combs | Arbitrarily many teeth; every distinct pair in the rectangular spine or tooth middle rows illuminates, with arbitrary real dimensions. Height-two integer specialization covers all native A pairs. | Arbitrary off-middle-row real tooth points not covered. |
| Two-sided comb subclasses | Complete all-native-pair results for unit-width height-two teeth/core>=1, arbitrary integer tooth widths/core1, and the separately accepted width2/core>=3 class, under W<=21. | Different subfamilies do not combine into arbitrary comb geometry. |
| Long-neck families | For two fixed orthogonal chambers and a positive-width neck, every fixed opposing pair illuminates for all sufficiently large real neck lengths; threshold locally uniform. | Depends on fixed geometry and endpoints. Network/tree propagation additionally requires an existing legal witness and stated width/arithmetic conditions. |
| Restricted staircases/spirals | Nested-window inequalities, tall-roof real spiral thresholds and coprime-period lattice spiral theorems cover infinite families beyond8walls. Thin-cap10-wall coprime theorem covers ALL native pairs; later accepted arithmetic extensions strengthen it. | No theorem for all10-wall metrics/types or all real endpoints in lattice-only families. |
| Fixed-support quantitative bounds | Second/third/fourth surplus bounds13/37/32 reflections at the specified three-star support, including classified remote attachments. | These refine overlapping existence results; do not count them as independent universal minimum theorems. |
| Strict parity-fold construction minimum | A dark pair needs >=22walls within the precise whole-copy fold class, including accepted similarity extension. | Depends on restricted theorem and fold hypotheses; not every dark room has that fold. |

Sources and earlier scope details remain in items1–11 above. The corrected eight-wall manuscript is `../illumination-generalization-2026-11-06/fable/eight-wall-review-packet/theorem-and-proof.md`, with `coordination/general-proof-priority/final-review/eight-wall-review.md` beneath that research root. The initial coprime theorem is recorded in `../illumination-publication/repository/docs/FOLLOWUP-2026-11-08.md`; its then-pending equal-block supplement was subsequently accepted in `../illumination-generalization-2026-11-06/review/three-reflex-coprime-equal-block-independent.json`. Generalized-family and weighted-period acceptances exist separately; this addendum does not infer an unrestricted spiral theorem from their union.

### New useful positive mechanisms, without new room coverage

All paths below use the actual connected reflection unfolding and Sigma containing EVERY physical corner lift, including regular convex-corner marks.

- [done] **Exact affine pair transport.** Both endpoints may move under a genuine global Sigma-preserving affine map. A regular straight seed pulls back to the exact original source and chosen original target lift. Source fixation is unnecessary; smooth-wall-aligned unfolded seeds are permitted. This is conditional transport, not existence of an appropriate map.
- [done] **Uniform-source L shear criterion.** Explicit cylinder compatibility and a target congruence give one shear, optionally followed by a copy reflection, producing a seed for EVERY real interior source to that target. Integral subfamily solvability is exactly the stated gcd condition. Existing all-real L illumination is broader as coverage.
- [done] **An infinite-family endpoint-moving diagonal construction.** For normalized symmetric L with arm d and outer size2d+1, d=1mod4,d>=5, specified p=(2d-1,1),q=(1,2d-1) admit a seed under a genuine diagonal twist to ORIGINAL Ryq. This rescues that portion of the earlier subgroup-obstruction family. It is not all pairs in those rooms. One prescribed d5 check, independently repeated, gives41reflections; the all-d claim follows from the hand proof.

Proofs: `../illumination-generalization-2026-11-06/coordination/general-proof-priority/affine-seed-reduction/pair-transport.md`; `target-fiber-peer-goals/reviewer/diagonal-phase-lemma.md` and `reviewer/diagonal-reconciliation.json` beneath the same general-proof-priority directory.

### New negative results that materially change the strategy

- [done] **Exact-original-target one-copy coverage is false.** In the8-by8 L with arm4, original p=(6,2),q=(2,6) cannot be carried to a corner-free one-copy chord by ANY allowed affine map. Yet the physical pair illuminates after one reflection. Allowing all FOUR original target lifts evades this particular obstruction; that broader statement remains open.
- [done] **The full known coordinate/diagonal method fails on an infinite family.** For the specified d=3mod4 symmetric-L pairs, every word in the COMPLETE horizontal, vertical and both diagonal foliation stabilizers plus room symmetries fails all four target lifts. This subgroup is not proved to exhaust the full affine group.
- [done] **A legal light path need not be affine-compressible.** For that same residual family, EVERY connection in the original diagonal direction is excluded from one-copy compression by the ENTIRE affine group. A legal two-reflection path exists among those excluded connections. Antidiagonal connections are also excluded; original axes cannot connect the endpoints. This disproves “compress any given lit path,” not “some suitable path is compressible.”
- [done] **The surviving one-reflection path requires strict norm descent.** With primitive direction v=(-d,d-1), every compressor needs |DFv|_1<=2d-2, below its starting2d-1. Free chord geometry gives an exact necessary direction condition, but does not place the named actual endpoint images.
- [done] **No genuine affine map sends that surviving direction to ANY axis or diagonal.** A marked-corner return-time invariant proves this for every residual d, not just selected integer matrices. Other primitive directions remain undecided.
- [done] **Finite endpoint action does not determine path compression.** Infinitely many genuine maps can fix the complete relevant endpoint fiber while making the fixed path holonomy unbounded. One representative per endpoint permutation is insufficient.

Sources: `pair-coverage-peer-goals/author/obstruction.md`, `target-fiber-peer-goals/reviewer/noncompression-reconciliation.json`, and `primitive-one-left-peer-goals/{author/argument.md,reviewer/marked-return-obstruction.md,reviewer/marked-return-reconciliation.json,reviewer/endpoint-kernel-holonomy.md}` beneath `../illumination-generalization-2026-11-06/coordination/general-proof-priority/`.

These complement earlier negatives in items18–23: wall count does not bound primitive directions; mirrors are not monotone; nearby/generic illumination need not pass to an exact target; finite blocking is not illumination; geometric simplification alone gives no optical transfer; ordinary matrix reduction does not imply a realized affine map.

### Supporting tools and reproducibility

Preserve the exact rational path guards, complete checked SAT contradictions in the restricted model, finite geometric atlases, strip/neck decompositions, bounded per-direction marked graph, exact period lattice/content and corner-parity constraints. They help verify and organize proofs. None supplies a finite global direction cutoff or automatically solves the universal existence step. Unfolding, affine maps, SAT and these standard frameworks are not claimed as project inventions.

The22-wall dark construction remains an explicit internally verified example and likely independent rediscovery of a known mechanism. Exact historical coordinate identity is unresolved. The strongest existing documented novelty candidate remains the precise four-parameter corridor theorem; the eight-wall/comb/neck results also merit exact priority review. No result currently has confirmed historical originality.

### Open frontier and current work

- [blocked: general optical existence unproved] All10-wall orthogonal rooms, all orthogonal r<=8 rooms, canonical45 W<=21 without k<=6, and universal22-wall minimality remain unresolved by this project.
- [blocked: affine availability unproved] The all-pair/all-L four-target-lift seed criterion and compression of the fixed residual one-reflection path remain open.
- [in progress] Existing peers now assess the WHOLE realized affine orbit bound min|DF(-d,d-1)|_1=2d-1 for residual d=3mod4. It is a proposed premise, not a theorem. Author seeks proof or genuine counterexample; reviewer challenges full-group scope. No direction-by-direction extension programme is authorized by this phase.
- [blocked: priority review outstanding] No fresh historical-novelty clearance or external expert review was conducted here. No ETH/P=NP consequence is established.

**Judgment:** The main mathematical assets remain the completed room-family theorems. The recent affine work has produced valid scoped tools and strong counterexamples to proposed reductions, but has not advanced positive illumination coverage. Its value depends on whether the current full-group step closes rather than generating another indefinite list of exclusions.

**Next move:** While peers assess that precise full-group premise, consolidate the corridor and corrected eight-wall proofs into concise specialist-review material. This is a recommended next task; this inventory sends or publishes nothing.

Verification boundary: I reread the earlier inventory, restricted theorem/reconciliation, corridor completion/novelty assessment, corrected eight-wall statement/review, coprime follow-up and selected later acceptance records, and the recent affine arguments/reconciliation/handoffs. I did not re-prove every historical item, rerun large SAT/corridor certificates, conduct new discovery searches, or treat control examples as general proofs. The coverage record lists the inspected sources. Peer tasks were not interrupted.
