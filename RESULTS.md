# Illumination results inventory

Readable PDFs and their sources are collected in the [manuscript catalog](preprints/README.md), with coverage gaps and historical notes identified.

This inventory groups 28 research conclusions by scope. Entries R01–R24 cover the main proof record; R25–R28 describe later affine mechanisms and obstructions. The [coprime-period spiral note](docs/FOLLOWUP-2026-11-08.md) explains the additional restricted family in R11. The [eight-wall and affine note](docs/UPDATE-2026-11-08.md) gives the later proof and review links.

Status refers to the scoped internal reviews cited below. This catalog is not a fresh proof review, external refereeing, or a determination of historical novelty. The [machine-readable index](manifests/results.json) uses the same stable result IDs.

## Overview

The main established results in the project record include the sharp lower bound in the restricted lattice model; complete arbitrary-real illumination for orthogonal rooms through eight walls; the exact four-parameter twelve-wall corridor theorem; unrestricted one-sided middle-row comb illumination and several complete two-sided comb classes; and eventual illumination/propagation in fixed long-neck families. The newly accepted tall ten-wall spiral theorem is a smaller, constructive extension.

No result currently has confirmed historical novelty. The 22-wall dark construction should be described as a likely independent rediscovery. The exact corridor theorem has the most developed existing priority audit. The eight-wall theorem, comb theorems and neck results are worthwhile candidates for focused priority review. A correct new proof of a known statement can also be useful, but has not been established as historically new here.

Do not count each guard, residue table, fixed path, or acceptance receipt as a separate discovery. Results below are grouped by substantive conclusion. Quantitative refinements and narrower dependencies are identified rather than added again to the headline count.

## Conventions

Illumination means a finite path from the specified source to the specified target, with ordinary equal-angle reflections at smooth walls and no physical polygon-corner contact. “Walls” means maximal straight sides after collinear edges are merged. For orthogonal disks, W=2r+4, with r the number of inward/reflex corners: eight WALLS means two reflex corners; the present target of eight REFLEX corners permits twenty walls.

A canonical45 room is a disk assembled from the specified 45–45–90 lattice triangles. It need not be triangular in outline. A marks are even-even lattice points. The parameter k counts transparent non-A lattice points, meaning interior or smooth-boundary non-A points. Bounds involving k depend on that fixed lattice presentation.

An acceptance below means independent internal AI mathematical review, sometimes with exact independent computation. It does not mean publication, expert refereeing, or formal proof-assistant verification.

## Illumination and minimum results

<a id="r01"></a>

### R01. Sharp 22-wall minimum in the k<=6 lattice model

Every strictly simple canonical45 disk with W<=21 and k<=6 illuminates every pair of distinct interior A marks, for every support. The known dark 22-wall example has k=4 and attains the bound inside this model. Thus this is a genuine sharp restricted minimum, not just a search finding.

The computer-assisted argument derives finite support/geometry domains, validates continuous path guards and their clause provenance, and uses checked contradiction certificates. The final theorem records 64 refutations and 193,480 guard records. The cited theorem and verification records describe that certificate corpus; this catalog does not report a fresh replay of it. Removing k<=6 remains unproved.

Priority: unconfirmed for the restricted lower bound; the dark upper-bound mechanism is established prior art.

Sources: [Restricted theorem](research/illumination-k4-codex/restricted-theorem-note/theorem.txt); [Reconciled verification](research/illumination-generalization-2026-11-06/construction/baseline-and-gap.md).

<a id="r02"></a>

### R02. Every orthogonal room with at most eight walls illuminates

Every distinct real interior pair in every strictly simple orthogonal polygon with W<=8 illuminates, for arbitrary positive real dimensions. This includes L, U, unequal-floor T, offset-corridor and staircase shapes, all endpoint placements and limiting parameter equalities admitted by strict simplicity. There is no lattice, exception, area or aspect-ratio cap.

The individual L/U/T/staircase proofs are ingredients and stronger orientation-specific constructions, not five additional wall-minimum theorems. Earlier frozen files with “staircase open/unreviewed” banners are superseded by final acceptance.

Priority: unconfirmed; nearby elementary illumination results exist. It deserves a dedicated exact-statement comparison.

Sources: [Whole theorem review](research/illumination-generalization-2026-11-06/construction/whole-staircase-independent-review.md); [Final acceptance](research/illumination-generalization-2026-11-06/review/whole-staircase-acceptance.json); [Corrected standalone proof](research/illumination-generalization-2026-11-06/fable/eight-wall-review-packet/theorem-and-proof.md); [Coordinator review and corrections](research/illumination-generalization-2026-11-06/coordination/general-proof-priority/final-review/eight-wall-review.md).
<a id="r03"></a>

### R03. Exact four-parameter twelve-wall corridor theorem

For arbitrary positive real d,g,h_minus,h_plus, take the union

    [0,2d] x [-h_minus,0]
    [d,3d] x [0,g]
    [0,2d] x [g,g+h_plus].

Every interior point of the lower outer chamber illuminates every interior point of the upper outer chamber. The widths/offsets are those displayed; this is not a statement for arbitrary three rectangles or all pairs throughout arbitrary twelve-gons. No rationality restriction or uniform reflection bound is asserted.

The proof combines one- and three-pass constructions, actual-endpoint cap transfer, and exact continuous endpoint covers of a mathematically bounded residual rational list. This is a computer-assisted universal parameter theorem, not a collection of sampled trajectories.

Priority: strongest existing documented novelty candidate in the inventory. The bounded audit found no exact antecedent, but did not exclude derivation from known covering/periodic-point classifications. No “first” or priority claim is justified.

Sources: [Completed statement](research/illumination-k4-codex/symbolic-corridors/unequal-depth/completion.md); [Independent acceptance](research/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/whole-result-acceptance.json); [Novelty assessment](research/codex-proof-verification/corridor-novelty/assessment.txt).

<a id="r04"></a>

### R04. One-sided combs: no wall-count bound for spine/middle-row pairs

In any rectangular-spine comb with arbitrarily many teeth on one side, every distinct pair drawn from the spine and the middle horizontal lines of teeth illuminates. Dimensions, tooth heights, widths and endpoint depths may be arbitrary real numbers. Extra unused teeth do not enter the construction.

For integer rooms with teeth of height two, every interior A mark lies on the relevant tooth middle row or in the spine. Thus the theorem covers every actual interior A pair in that entire one-sided height-two class, without any W or k cap. It does not cover arbitrary off-middle-row marks in arbitrary real teeth.

The finite monotone floor-matching argument is a particularly compact proof ingredient worth extracting. Priority unassessed.

Sources: [Comb proof](research/illumination-generalization-2026-11-06/construction/midheight-comb-proof.md); [Independent acceptance](research/illumination-generalization-2026-11-06/review/midheight-comb-independent-acceptance.json).

<a id="r05"></a>

### R05. Complete infinite two-sided comb subclasses through 21 walls

These are actual all-pair A-mark theorems, without k, area, support or diameter caps:

- Integer unit-width, height-two teeth, every integer core width >=1, W<=21.
- Integer height-two teeth of arbitrary independent integer widths, core width one, W<=21.
- A further uniform-width-two, height-two class with integer core width >=3, W<=21, as recorded in the accepted continuation ledger.

Opposite tooth bands need not be globally separated where the cited theorem allows overlap. These statements do not combine into an arbitrary-width/arbitrary-core/arbitrary-height theorem. They are more substantial than isolated comb fixtures: each closes an infinite model class. Priority unassessed.

Sources: [Whole unit-width acceptance](research/illumination-generalization-2026-11-06/review/unit-thin-whole-independent-acceptance.json); [Arbitrary-width core-one review](research/illumination-generalization-2026-11-06/construction/c1-arbitrary-width-join-independent.md); [Broader continuation ledger](research/illumination-generalization-2026-11-06/construction/coverage.md).

<a id="r06"></a>

### R06. Two arbitrary fixed chambers joined by a long neck

Two fixed arbitrary-real orthogonal chambers joined through smooth mouths by a positive-width rectangular neck illuminate each fixed opposing-chamber pair for every sufficiently large real neck length. The threshold depends on the chamber/mouth/mark data and is locally uniform under nondegenerate perturbations. A separate constructive rational-data result extracts explicit beam intervals and thresholds.

This gives a substantive way to exclude one type of degeneration of dark candidates. It is not a uniform threshold in wall count, and permits only the stated fixed-chamber regime. Priority unassessed.

Sources: [Long-neck proof](research/illumination-generalization-2026-11-06/construction/long-neck-proof.md); [Acceptance](research/illumination-generalization-2026-11-06/review/long-neck-independent-acceptance.json); [Effective rational construction acceptance](research/illumination-generalization-2026-11-06/review/constructive-neck-acceptance.json).

<a id="r07"></a>

### R07. Long-neck networks and exceptional arithmetic growth

For fixed three-chamber/two-neck families, possible long-neck failures concentrate near finitely many rational length ratios, sharpened to finitely many weighted affine strips. Integer data leave finitely many offset arithmetic rays; those rays are not thereby illuminated.

For a finite tree of fixed chambers joined by parallel, commensurate-width necks, one provided legal actual witness implies eventual illumination along nonnegative rational-affine length growth. Repeated passages, branches and same-side mouths are included. Witness existence and the finite initial range remain separate obligations. This conditional propagation theorem is useful, but not an unconditional all-network illumination theorem. Priority unassessed.

Sources: [Precise network statement](research/illumination-generalization-2026-11-06/construction/neck-ray-propagation-parallel-tree.md); [Independent tree acceptance](research/illumination-generalization-2026-11-06/review/parallel-tree-independent-acceptance.json); [Affine-strip/network review map](research/illumination-generalization-2026-11-06/review/bridge-scope-report.md).

<a id="r08"></a>

### R08. Nested staircase sufficient conditions, beyond eight walls

Accepted nested-band and bounding-triangle inequalities guarantee illumination for arbitrary real interior pairs in the stated multi-band staircase families. They keep one common slope through every portal and choose an actual target image. The geometric inequalities are essential; this is not an all-staircase theorem for arbitrary numbers of steps or dimensions. Priority unassessed.

Sources: [Proof](research/illumination-generalization-2026-11-06/construction/nested-window-proof.md); [Independent scope/guards](research/illumination-generalization-2026-11-06/review/nested-extension-independent.md).

<a id="r09"></a>

### R09. Explicit reflection bounds at fixed three-star support

At the fixed interior A support S=(0,0), U=(2,0), T=(2,2), the surplus-layer results include a 13-reflection bound for the stated second-surplus class, 37 for third surplus, and 32 for fourth surplus. The final fourth-surplus proof permits the classified remote attachments; it is not restricted to a fixed local drawing. Its W<=21 and k<=6 assumptions remain attached.

These are quantitative refinements and constructive decompositions. Their existence conclusions overlap the broader k<=6 theorem, so they should not be presented as unrelated general illumination theorems. Local improvements such as the nine-reflection O3 lemma fit under this heading. Priority unconfirmed.

Sources: [Third-surplus theorem](research/illumination-k4-codex/third-surplus-review/theorem.txt); [Fourth-surplus theorem](research/illumination-k4-codex/fourth-surplus-review/global-four-closure/theorem.txt); [Local nine-reflection priority assessment](research/codex-proof-verification/O3-combined/novelty.md).

<a id="r10"></a>

### R10. Sharp minimum within strict whole-copy parity folds

For the exact construction class of whole congruent copies of a strict canonical base, with literal inverse-copy agreement and actual interior marks mapping to two distinct smooth boundary A points, a dark pair requires W>=22. The known example attains it. Diagonal bases and arbitrary initial rigid placements are included; the common-similarity extension has separate acceptance.

The proof derives assembly/exception counts and normalizes seams, then uses the k<=6 theorem. It does not show that every dark room admits the required fold. This is a second restricted minimum with an explicit dependency on result 1, not a second proof of universal minimality. Priority unconfirmed.

Sources: [Fold-class statement](research/illumination-generalization-2026-11-06/review/fold-class-theorem.md); [Normalization acceptance](research/illumination-generalization-2026-11-06/review/fold-normalization-acceptance.json); [Similarity extension review](research/illumination-generalization-2026-11-06/construction/fold-similarity-independent-review.md).

<a id="r11"></a>

### R11. Positive ten-wall spiral progress (restricted scope)

TR01 covers specified pairs in protected subregions of an ordered three-reflex spiral for arbitrary real metrics. TR03 proves every distinct interior pair illuminates under an explicit sufficient upper-chamber height threshold. Independently accepted TR04 broadens the normal-form geometry to non-overlapping arms (`a<l OR c<b`) and proves all-pair illumination under either a tall or a transposed wide threshold. Neither threshold depends on the selected marks.

Independently accepted TR05 covers every upper-cap source `a<=s<=w, h<u<H` to every bottom target `l<t<A, 0<v<c`, at all metrics in that same normal form. With the protected-subregion results, the remaining arbitrary-metric pairs are left-terminal versus bottom-terminal pairs. The complementary metrics, other ten-wall types, and full eight-reflex goal remain unresolved.

The proofs control actual walls, corner avoidance and exact target attainment. Later first-exit and injection-margin controls show why arbitrarily many cap bounces do not automatically repair a short cap. TR06 presents an exact countercontrol to a particular nearest-period monotone iteration; its method-only negative conclusion received [independent acceptance](research/codex-proof-verification/specialist-ideas/terminal-resumption-2026-11-07/tr06-independent-review.md) and proves no dark room. General terminal-pair existence remains unresolved. Historical novelty is unassessed.

The separately reviewed coprime-period construction illuminates every distinct native even-even pair in its specified thin-cap ten-wall family, under the stated integer and coprimality hypotheses. It does not cover arbitrary real endpoints or all ten-wall rooms; see the [exact family and proof](docs/FOLLOWUP-2026-11-08.md).

Sources: [TR03 statement](research/illumination-generalization-2026-11-06/construction/three-reflex-candidate-03.md); [TR04 statement](research/illumination-generalization-2026-11-06/construction/three-reflex-candidate-04.md); [TR04 acceptance](research/illumination-generalization-2026-11-06/review/three-reflex-tr04-independent.json); [TR05 statement](research/illumination-generalization-2026-11-06/construction/three-reflex-candidate-05.md); [TR05 acceptance](research/illumination-generalization-2026-11-06/review/three-reflex-tr05-independent.json); [TR06 countercontrol](research/illumination-generalization-2026-11-06/construction/three-reflex-candidate-06.md); [Remaining gap](research/illumination-generalization-2026-11-06/construction/three-reflex-blocked-handoff.md); [Full independent review](research/illumination-generalization-2026-11-06/review/three-reflex-tr03-independent.md); [Acceptance](research/illumination-generalization-2026-11-06/review/three-reflex-tr03-independent.json); [Accepted November8 coprime-period follow-up](docs/FOLLOWUP-2026-11-08.md).
## Supporting mathematical tools

<a id="r12"></a>

### R12. Exact per-room decision framework and reusable path certificates (scope-limited)

The labelled finite origami-orbit method gives an exact decision route for each valid fixed arithmetic room when its entire required finite orbit is exhausted. Capped undecided runs do not certify darkness. Exact rational trajectory guards certify paths for all tile completions satisfying their required/forbidden sets, not just one drawn room. These methods are central to reproducibility; unfolding/group actions/SAT proof certificates are established tools, not inventions claimed by this project.

Sources: [Finite orbit solver](research/illumination_cover.py); [Sufficient darkness certificate](research/illumination_cover_certificate.py); [Exact path guards](research/illumination_paths.py).

<a id="r13"></a>

### R13. A wall-bounded skeleton for every individual rational direction

The first-return marked graph has exactly q(W+2)/2 edges, with q<=8, hence at most 92 for W<=21. It retains actual source/target sheets, absorbing corners, prongs and positive integer edge lengths. Its size is bounded while weights and the number of directions are not. It supplies no finite universal list of directions.

Sources: [Directional skeleton](research/illumination-generalization-2026-11-06/construction/direction-skeleton.md); [Acceptance](research/illumination-generalization-2026-11-06/review/direction-skeleton-acceptance.json).

<a id="r14"></a>

### R14. Finite geometric atlases and strip generators (geometry only)

Every marked canonical45 W<=21 geometry lies in a finite family of rational-linear sign cells with unbounded integer deformation coefficients. The orthogonal subclass has a bounded-base description using at most 44 commuting even-gap insertions; a single gap exposes a tree of at most five parallel necks. These are exact structural reductions of infinite geometry, not finite optical verification or darkness-preserving compression. Priority of their elementary polyhedral ingredients is not claimed.

Sources: [Atlas](research/illumination-generalization-2026-11-06/review/polyhedral-atlas.md); [Atlas acceptance](research/illumination-generalization-2026-11-06/review/polyhedral-atlas-acceptance.json); [Strip theorem](research/illumination-generalization-2026-11-06/review/strip-generators.md); [Strip acceptance](research/illumination-generalization-2026-11-06/review/strip-generators-acceptance.json).

<a id="r15"></a>

### R15. Globally available geometric simplification (geometry only)

Horizontal/vertical section completion and isolated-corner completion preserve literal interior marks, strict simplicity and the lattice, and provide a strict decrease in reflex count down to a rectangle. That is a genuine global geometric result. The necessary optical implication from a simpler illuminated room to the original is unproved; unrestricted transfer is false at the known dark example.

Sources: [Geometric reduction proof](research/illumination-generalization-2026-11-06/construction/geometric-reduction-proof-02.md); [Reconciled optical limitation](research/illumination-generalization-2026-11-06/construction/geometric-reduction-optical-impasse.md).

<a id="r16"></a>

### R16. Arithmetic bridges and genuine affine transfer (exact hypotheses)

The work classifies torus-covered four-direction rooms into similarity-rational or independently axis-rational classes and supplies exact endpoint/coordinate bridges under cited published results. This is a specialization/application of existing theory, not an asserted new general classification.

Separately, cylinder-period least-common-multiple shears give genuine global affine self-maps preserving the complete actual endpoint/corner data and primitive first-hit times. Their existence is proved. The proposed rank descent is only conditional and has an accepted obstruction, so it supplies no general induction.

Sources: [Intrinsic arithmetic bridge](research/illumination-generalization-2026-11-06/review/torus-cover-bridge.md); [Weighted affine transfer](research/illumination-generalization-2026-11-06/construction/weighted-return-argument-01.md); [Independent scope](research/illumination-generalization-2026-11-06/review/weighted-return-handoff.md).

<a id="r17"></a>

### R17. Local exact shooting, corner repair and interception lemmas (conditional)

Useful proved ingredients include: an exact arithmetic progression of target roots on a jointly guarded chamber interval; a sufficient width condition forcing a root; a one-floor-bounce repair under a supplied physical corridor; the regular-domain Farey triangle endpoint identity; and two kinds of supplied cone-chain configurations that force a second parity-distinct physical reflex corner under darkness.

A physical reflection-group calculation also proves that a specified equal-half axial pi-sector split through a cone has the same physical endpoint. Consequently a qualifying triangle between distinct endpoints in that axial case yields illumination. These hypotheses are not proved globally available, and repeated application need not find new physical corners. The lemmas are tools, not a nine-corner lower bound.

Sources: [Shooting theorem and limits](research/illumination-generalization-2026-11-06/review/optical-routing-handoff.md); [Corner transfer](research/illumination-generalization-2026-11-06/construction/endpoint-transfer-argument-01.md); [Interception reconciliation](research/illumination-generalization-2026-11-06/review/dark-interception-local-final-reconciliation.json).

## Counterexamples to proof mechanisms

These results eliminate specific mathematical implications. Their importance is avoiding invalid generalizations, not accumulating counterexamples to every conceivable proof.

<a id="r18"></a>

### R18. Few walls do not bound primitive direction complexity

An accepted square family already forces arbitrarily large primitive illuminating vectors, although its direct path has zero reflections. The work further rules out the proposed universal affine rank descent even in already illuminated squares. A bounded wall count cannot justify a direction cutoff or an axis terminal case.

Sources: [Direction/rank obstruction review](research/illumination-generalization-2026-11-06/review/weighted-return-handoff.md); [Baseline scope map](research/illumination-generalization-2026-11-06/review/bridge-scope-report.md).

<a id="r19"></a>

### R19. No automatic geometric normalization or limiting argument

Reviewed examples refute the proposed bounded similarity/global-affine normalization. Piecewise-affine rescaling cannot preserve all straight crossings unless interface derivatives agree. Illumination at rational or nearby inputs does not automatically pass to a limiting exact pair. Adding/removing mirrors can change illumination. These invalidate named proof routes, not the low-wall conjecture.

Sources: [Normalization, continuity, and fold review map](research/illumination-generalization-2026-11-06/review/bridge-scope-report.md).

<a id="r20"></a>

### R20. No unrestricted Euclidean whole-copy explanation of darkness

The anisotropically stretched known dark Q100 remains dark under axial reflection-preserving scaling, but violates proved similarity-invariant bounds for the stated strict whole-copy factor class at its wall count. A separate repaired 43-wall beveled control defeats an unrestricted orthogonal-base-only converse while retaining a diagonal parity factor. Neither is a <=21-wall counterexample.

Sources: [Explicit Q100 obstruction](research/illumination-generalization-2026-11-06/review/fold-area-invariant.md); [Fold/bridge review map](research/illumination-generalization-2026-11-06/review/bridge-scope-report.md).

<a id="r21"></a>

### R21. Separator, finite-blocker and abstract monodromy shortcuts are insufficient

Darkness yields a genuine-cone separator and local excluded-chord inequalities in a marked geodesic triangulation. The accepted bounded triangulation counts do not force nine distinct reflex corners. Ordinary finite blocking is automatic for arithmetic torus covers and therefore supplies no special darkness obstruction. The reviewed Heisenberg example shows abstract monodromy transitivity is insufficient, but is not physically realizable as a room of this class; it is not a low-wall dark polygon.

Sources: [Global proof frontier and controls](research/illumination-generalization-2026-11-06/construction/coverage.md); [Precise physical gap](research/illumination-generalization-2026-11-06/construction/global-bridge-impasse.md).

<a id="r22"></a>

### R22. A useful exact minimum of two reflections (one prescribed pair)

A verified fourteen-wall room has an actual pair with no direct path and no one-reflection path across any wall, but an exact legal two-reflection path. Thus the minimum for that pair is exactly two. It disproves universal one-wall repair, not illumination or a larger reflection bound. Related two- and four-reflex controls refute universal availability of the sufficient repair corridor and width criterion.

Sources: [Complete one-wall exclusion and two-bounce witness](research/illumination-generalization-2026-11-06/review/endpoint-transfer-et02-independent.md); [Endpoint review closure](research/illumination-generalization-2026-11-06/review/endpoint-transfer-handoff.md).

<a id="r23"></a>

### R23. Three failed global joint-selection shortcuts

A shortest complete-fiber path excludes the strict narrow cone angle needed by the triangle lemmas. On the fixed unit lattice, an exact all-word divisibility obstruction excludes the two short templates in dark Q100. Even after choosing two arms to one cone, physical symmetries cannot reduce their minimum sector angle below their original physical wedge separation. These leave arbitrary-weight, non-minimizing global existence open. Q0/Q100 have nine reflex corners and do not refute the eight-reflex goal.

Sources: [Reconciled availability frontier](research/illumination-generalization-2026-11-06/review/availability-frontier.md).

## Construction and experiments

<a id="r24"></a>

### R24. The readable 22-wall dark construction (likely rediscovery)

The strictly simple orthogonal example made of three reflected five-square staircases has 22 walls, area 15 and a hand proof for two actual interior dark marks. Its seam/convex-corner handling and independent verification are valuable artifacts. Exact coordinate identity with that historical example is unresolved. The general 22-edge existence bound was already published. Present it as an explicit, verified construction or likely rediscovery, not confirmed original research.

Older parity-family censuses, selected rigidity certificates, fixed counterexamples and explicit paths support investigation. Some have full geometry checks but only sampled independent certificate replay. They are evidence within stated finite domains, not a universal classification or a separate minimum theorem.

Sources: [Superseding historical assessment](research/illumination-k4-codex/discovery-assessment.md); [Construction source](research/illumination-k4-codex/research-note.tex).

## Affine mechanisms and obstructions

These conclusions retain the hypotheses in the [reviewed affine note](docs/UPDATE-2026-11-08.md). They do not establish a universal illumination theorem.

<a id="r25"></a>

### R25. Exact affine pair transport and uniform-source L criterion

Conditional exact endpoint transport; explicit L target/shear hypotheses provide a uniform-source seed mechanism. Existing all-real L illumination already gives broader room coverage.

Sources: [Argument and exact scope](research/illumination-generalization-2026-11-06/coordination/general-proof-priority/affine-seed-reduction/pair-transport.md).

<a id="r26"></a>

### R26. Scoped diagonal endpoint-moving construction

Specified d=1 mod4 symmetric-L pairs admit an exact original-Ry-target seed. Not all pairs or all L rooms.

Sources: [Argument and exact scope](research/illumination-generalization-2026-11-06/coordination/general-proof-priority/target-fiber-peer-goals/reviewer/diagonal-phase-lemma.md).

<a id="r27"></a>

### R27. Affine compression counterexamples and full-group direction obstructions

Exact-q coverage and any-given-lit-path compression fail at stated scopes. A surviving fixed one-left path requires norm shortening and cannot be sent to axes or diagonals by any genuine affine map; other directions remain open.

Sources: [Argument and exact scope](research/illumination-generalization-2026-11-06/coordination/general-proof-priority/primitive-one-left-peer-goals/reviewer/marked-return-obstruction.md).

<a id="r28"></a>

### R28. Limits of homological and local-geometric realization tests

Absolute symplectic/period compatibility admits unrealizable shortening actions; an actual nonaffine same-surface deformation compresses a path. Neither refutes the whole-group minimum.

Sources: [Argument and exact scope](research/illumination-generalization-2026-11-06/coordination/general-proof-priority/full-affine-bound-peer-goals/reviewer/blocked-handoff.md).

## Novelty and open questions

Historical novelty remains unconfirmed. The existing comparison priorities are:

1. Exact four-parameter corridor theorem and its constructive computer-assisted proof.
2. Whole arbitrary-real orthogonal W<=8 theorem.
3. The compact one-sided middle-row comb theorem, complete two-sided comb subclasses, and long-neck/network statements.
4. The restricted k<=6 minimum and strict-fold corollary, with their full certificate/dependency scope.
5. Quantitative fixed-support bounds and the newest spiral/local results.

This ordering is judgment about clarity and interest, not a ranking of proven originality or publication significance. The largest established statement is not necessarily the easiest novelty claim.

The existing bounded novelty audits have not shown that the family-specific theorems follow immediately from standard finiteness statements. Finitely many possible dark pairs is not zero dark pairs. Conversely, a missing exact search hit does not exclude a nontrivial derivation from known covering/periodic-point theory. Fresh narrow searches for eight-wall/corridor specular theorems did not resolve priority; many hits concern floodlights/diffuse reflection, different problems.

Published comparison sources in the record include: [Wolecki, Illumination in Rational Billiards](https://arxiv.org/html/1905.09358v3) and [Lelievre–Monteil–Weiss, Everything is illuminated](https://arxiv.org/html/1407.2975). Prior family-specific comparison and its access limits are recorded in the corridor assessment linked above. No fresh exhaustive literature audit was performed.

- [blocked: terminal-pair existence proof missing] Complete ten-wall/three-reflex optical theorem: only scoped families/placements are established; both research goals stopped at this gap.
- [blocked: no global optical argument] General orthogonal r<=8 illumination, and removal of k<=6 for all canonical45 W<=21 rooms, remain unproved by the current results.
- [blocked: no general lower-bound proof] Universal 22-wall minimality among arbitrary polygons is unresolved by this project.
- [blocked: no priority confirmation] No “first”, “novel theorem”, or publication-priority assertion is currently established.
- No established consequence for ETH or P versus NP. SAT/certificate machinery here verifies bounded geometric exclusions and is not an algorithm for arbitrary SAT.

## Verification scope

The cited theorem, review, and reconciliation records identify the mathematical statements and source versions they cover. Older status banners do not override a later scoped verdict. File integrity checks and prescribed examples do not re-prove all quantified statements or replay the entire certificate corpus.

See [reproduction](docs/REPRODUCIBILITY.md) for supported controls and [snapshot scope](docs/SNAPSHOT.md) for provenance and verification limits.
