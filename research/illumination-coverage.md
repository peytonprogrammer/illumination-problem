## Current one-exception complete-family result (2026-10-29)

[done]24 remains optimal for simple canonical45-degree rooms with at most one transparent B/C vertex and interior A marks, over arbitrary assembly size. Extended identity W=2+6I_A+Q-(2J+s_N) gives exactly2 full A stars,≤30 triangles, and14 complete nonadjacent placements. Eleven are geometrically impossible; the remaining3 are exhausted by535 exact ray cuts across512 distinct room-and-mark configurations (423 reused/89 new). Fresh CP-SAT replay of all14 cases passes, with independent physical-ray verification, two positive defect-type controls,138 grid patterns, three full/clipped guard comparisons, and64 guard-preserving tile mutations. The strict-family audit also still passes. Secondary SCIP checks reproduce only four geometric cases; another caps, so there is no full second-solver replication of this extension. No formal UNSAT proof, general polygon bound, or smaller room. Does not exclude≥2 exceptions, other marks/geometries, or nonsimple rooms. Final proof/reproduction is in `.context/illumination-analysis.md`; audit `.context/one-global-final-audit.json`.

The historical sections below are superseded only where this complete-family result applies.

## Current complete-family result (2026-10-29)

[done] Strict simple canonical 45-degree rooms require at least24 walls, over assemblies of any size. Counting gives exactly two full A stars, charge≤9, ≤28 triangles below24; connectivity reduces all placements to seven finite supports. CP-SAT excludes all seven at≤23; a separately built fan formulation with SCIP independently excludes all seven. Known24 control passes both. Audit528 local masks/617 connected supports/16 transformed controls passes. This is a computer-assisted result conditional on solver/model correctness, not a formal UNSAT proof or global polygon minimum. Does not extend to transparent B/C vertices, slits, contacts, holes, other tilings, or non-A marks. Full argument/reproduction is the final section of `.context/illumination-analysis.md`.

Historical coverage follows; earlier bounded simple-family statements are superseded only within the strict certificate family.

# Illumination research coverage

[done] 2026-10-28. Verified the idealized 20-wall slit room and published 22-wall contact room using exact coordinates. Reproduced a 24-wall simple polygon. All use the absorbing-corner convention.

Completed three final searches over 288 triangles in [-4,8]², source (0,0), any other interior A target, arbitrary tile subsets. The solver reported no certificate below 20 walls with arbitrary slits, none below 22 without slits, and a simple-polygon optimum of 24. No run timed out. These results are bounded by patch, source placement, and sufficient certificate family.

Validation: seven saved certificates pass; 4,461 local states agree between two sector algorithms; four invalid certificate mutations fail. Exact data, scripts, dependency pins, rendered diagrams, solver statuses, and logs are saved in `.context/`.

The 20-wall coordinates idealize a raster image; original creator coordinates/code and historical priority remain unverified. The search did not cover other triangle families, arbitrary rational or irrational rooms, larger patches, or alternative darkness certificates. Solver infeasibility has not been exported as a formally checked proof. No new global bound or record is claimed.

Primary literature: Wolecki v3 (November 30, 2024), especially Section 3 and Theorem 1.2; Lelièvre–Monteil–Weiss metadata checked earlier. Firsthand 20-wall upload metadata and image checked. No comprehensive bibliographic search or external communication.

## Transparent vertex follow-up

[done] Five screening runs over two finite patches yielded 939 distinct smaller candidate rooms, all independently proved illuminated by explicit rational paths. One bounded case was exhausted: no simple room with at most 23 walls, one transparent B/C point, source (0,0), target (4,0), inside the 64-triangle patch [-2,6]×[-2,2], within this model. Slit searches with one/two exceptions timed out and remain incomplete.

All 939 reflection groups were computed exactly and equal the full even-translation square-symmetry group. A derived obstruction explains why a reflection-orbit coordinate test loses the information needed for these candidates. This is not a proof that arbitrary transparency is impossible. Related primary literature checked: Wolecki Section 3 and Tan, Codes for Square-Tiled Surfaces (arXiv:1207.3493); no square-tiled surface orbit enumeration was implemented.

Audit artifacts include all witness records, 939 independent path validations, 20 cut patterns under 836 unrelated geometry mutations, the group calculations, and two examples that initially passed a small direction search before exact longer paths were found. No global bound, safe transparent construction, or new record is claimed. No outward communication or publication.

## Two-vertex simple-room extension

[done] Same source (0,0), target (4,0), 64-triangle patch [-2,6]×[-2,2], simple boundary, arbitrary tile subsets. The search allowing one or two transparent B/C vertices and at most 23 walls is exhausted. Zero exceptions are separately excluded. A matching 24-wall room passes its exact darkness certificate, establishing a patch/model optimum of 24.

The final record contains 500 distinct candidate rooms (165 reused one-exception cases, 335 new two-exception cases) and 2,000 symmetry-derived exact ray cuts. Independent audit validates every path and rebuilds every cut, checks 2,932 unrelated tile mutations, and confirms both controls. A fresh-model replay reproduces infeasibility from the saved cuts. Combined with the previous follow-up, 1,274 distinct candidate rooms are illuminated. All 500 final reflection groups match the earlier exact affine-group obstruction.

No unresolved ray-sampling survivor remains in this completed model. The result does not extend to different marks, patches, three exceptions, slits, or other tilings. CP-SAT infeasibility and cut correctness are computational evidence, not a formally checked unsatisfiability proof. No new dark construction or global bound; no publication or external communication.


## Placement sweep and 30–60–90 pilot

[done] Three non-axis placements tested under the two-transparent-vertex relaxation. Simple rooms with ≤23 walls are exhausted for T=(2,2), 72-tile patch [-2,4]², and T=(4,4), 128-tile patch [-2,6]². Simple T=(4,2) in its 96-tile rectangle and two-slit T=(2,2) with ≤19 walls remain incomplete at time caps. The four final runs contain 503 distinct room-and-mark configurations, all with exact illumination witnesses. Source is always (0,0). Nearest-axis T=(2,0) has a forced direct ray only when slits are prohibited; the known 20-wall slit room is the counterexample to extending that assertion. Generalized symmetry cuts preserve each patch and unordered pair; all derived paths are checked before cutting.

Independent placement audit checks 1,686 exact symmetry-derived paths and reconstructs their cuts. The prior 2,000-path horizontal audit still passes after the symmetry change. `placement-final-audit.json` records counts and cut-preserving mutation checks. No finite direction miss is treated as darkness.

Exact 30–60–90 barycentric equilateral tiling implemented with rational arithmetic in metric diag(1,3). Under the strict absorbing-B/C certificate, the 192-tile radius-2 patch has optimum 30 walls with at most one atomic slit edge and contacts/holes allowed. A 34-tile room is certified using Wolecki Lemma 3.1; it has one slit and one boundary contact. In the 432-tile radius-3 patch, ≤19 walls with ≤1 atomic slit and ≤21 without slits are infeasible. No certified simple polygon exists at any wall count in either tested patch. Every target is any second full A star; source is fixed at the origin.

The 30–60–90 audit independently compares 16,576 local configurations, checks 272 shared reflections with the correct metric and labels, and validates the saved room/wall count. No larger patch, longer/multiple slit model, transparent-vertex version of this family, or formal unsatisfiability proof is covered.

A proposed next certificate retains the unfolded square-sheet permutations and blocker/mark decorations, enumerating a finite SL₂(Z) orbit before checking horizontal visibility. Tan's primary abstract supports orbit enumeration for square-tiled surfaces; the decorated billiard adaptation and its all-direction coverage are proposals only. No such certifier or inverse polygon construction was implemented. No smaller dark room or global lower bound; no external communications or publication.


## Reflected-copy certificate prototype

[done] Exact eight-orientation triangle unfolding to square permutations implemented for canonical 45–45–90 rooms with interior A marks. A finite palindrome-endpoint relation supplies a sufficient all-direction darkness certificate; a separate Stern–Brocot neighbor-code search supplies exact illumination witnesses or UNKNOWN at a resource cap. Combined CLI: `illumination_decide.py`.

Three dark controls certified; both earlier false survivors independently illuminated with their 13- and 9-reflection witnesses. Audit: 3,640 exact cover/physical comparisons across seven controls, direct versus Farey crossing codes, 16 independently checked small relation pairs, six corrupt certificates rejected. Two additional zero-reflection controls pass. At mixed contacts, smooth sectors reflect; other sectors absorb. Two fixtures expose why globally absorbing all occurrences of a coordinate is too strong under this convention. Original dark controls and earlier positive paths remain valid. The prior adjacent-axis claim was explicitly limited to no-slit rooms; a perpendicular slit tip defeats it.

A complete local one/two tile mutation pilot attempts 2,244 changes, finds 611 geometrically valid transparent configurations, and certifies none dark. On all 611, the computed endpoint relation equals the parity-permitted relation, so no extra discriminatory power is demonstrated by this relaxation. This is not an illumination proof for those 611 rooms.

Full direction-code enumeration on the dark20 control caps at20,000 processed/40,001 discovered neighbor pairs without closure; it returns UNKNOWN. Ordinary color-preserving automaton minimization reduces none of five controls. No general completed exact negative decision, smaller room, global bound, formal proof-assistant verification, or new transparent dark construction is claimed. All artifacts remain local; no publication or external communication.


## Coherent direction-code quotient

[done] Added an optional exact simultaneous color-preserving conjugacy quotient for neighboring direction-code permutations. It preserves one code across every lattice step and all future Farey descendants. Canonical forms are exact component/root traversals; no heuristic equivalence is used.

At20,000 processed pairs each, the20/22/24-wall controls merge5/11/0 duplicate children and still hit the state cap. Their known darkness remains established by the earlier sufficient certificates; these detailed enumerations do not close. The option stays disabled by default.

Audit:972 exhaustive small colored systems agree with brute-force isomorphism, three full small orbit closures agree before/after quotient,140 real-cover relabelings preserve keys/visibility, and all four positive controls retain checked physical witnesses. No new smaller room, orbit-size bound, global impossibility result, or performance improvement is claimed. Artifacts: `cover-code-quotient-summary.json`; report updated in place.


## Midpoint-symmetry pilot (2026-10-29)

Checked complete grid-preserving affine half-turn enumeration and all fixed-point types on seven existing room controls; none covers any source-to-target lift pair. Checked three rectangular rooms with 3/4 interior rectangular holes, 129 distinct interior integer-grid point pairs, no fully covered pair. Partial coverage in the 16-wall room is defeated by an independently validated 12-reflection ray. Enumeration audits cover all 617 permutation systems with at most four squares; a positive abstract torus fixture and three corrupt-certificate rejections pass. No search over arbitrary surface gluings, non-lattice marks, arbitrary obstacle placements, or global polygon minima. Noncertification is not illumination. The positive torus fixture is not a room. Details and commands are in the cumulative report.


## Two-exception complete support reduction (2026-10-29)

[done] Complete structural reduction and bounded experiment for exactly two transparent B/C points in simple canonical45-degree rooms with distinct interior A marks. The wall identity excludes four or more full A stars; the three-star equality case has one L pattern and is excluded both by an80-triangle CP-SAT model and an independent seven-singleton-cell fan enumeration (257 nodes). All56 partial A fan masks satisfy charge>=incident cell-side count. The connected-cell degree argument gives P+m<=9 and marked A-cell distance<=4, leaving seven complete supports. At most33 triangles and9 partial stars are possible. Historical two-exception cell graphs and all three interior/smooth exception combinations are included in the checks. All seven finite supports were searched. Three placements are excluded geometrically and one by42 ray configurations/76 cuts; the remaining three placements cap without exclusion. Audit977 distinct configurations (193 new),2010 exact derived rays/cuts,335 historical cell graphs,3 fixed exception-type controls,3 full/clipped comparisons,64 mutations, and4 fresh exclusion replays passes. Prior14-case one-exception replay and fixed24-wall control pass. Finite searches use recompiled exact positive ray guards; the three capped cases remain incomplete. No two-exception family minimum, formal UNSAT proof, general polygon bound, or smaller dark construction is claimed for the three unresolved placements. All jobs have stopped.


## Completed two-exception family exclusion

[done] The typed-pair follow-up supersedes the preceding capped status. Complete projections yield45/38/49 classes; every one of132 fixed-pair models and all three combined parents independently replay INFEASIBLE.477 new distinct room-and-mark configurations and1650 new exact derived rays/cuts are independently checked, along with132 fixed positive projection models,3 projection exhaustion replays,6 full/clipped guard comparisons,48 guard-preserving mutations and the three fresh global exclusions. The longest new path has48 reflections. Together with the previous phase,1454 configurations and3660 exact derived rays/cuts cover the two-exception search.

The final parent models use complete geometric supports and exact positive-ray cuts only; pair constraints guide discovery and do not restrict the final exclusion replays. Composing the final3 placements with the previous4, the three-star equality exclusion and the higher-star analytic bound rules out at most23 walls for exactly two exceptions at arbitrary assembly size. Previous zero/one-exception exclusions and the known24-wall control establish minimum24 for at most two exceptions. Summary: `two-complete-summary.json`; latest audit: `two-pair-final-audit.json`.

No three-exception search, arbitrary non-A marks, different tiling, non-grid mirrors, holes, slits, contacts, general polygon lower bound, formal UNSAT proof, or literature-priority claim. All jobs stopped; no outward actions or tracked edits.


## Three exception extension and connecting cell paths

[done] The three-full-star branch covers all five complete arrangements and ten raw mark cases, with 23 illuminated configurations and guards; Codex's CP-SAT/fan audits and Claude's independent model agree. The two-full-star branch has ten complete supports. Six placements are excluded in the current necessary models and four remain unresolved: (1,1), (2,0), (2,1), (2,2). All 318 new configurations and 4,944 guards pass the exact audit, including independent closed-triangle coverage, 72 mutations, 72 corrupt-guard checks, and independent path-cost/outside-set enumerations. A longer direct replay excludes (3,0) after the shorter replay caps; both receipts remain visible. No full three-exception minimum or smaller dark construction is claimed. Current phase peer verification is pending. All Codex jobs stopped. See `three-two-star/findings.md`, `summary.json`, `audit.json`, and the frozen `proof-inputs.json`. This section supersedes the preceding statement that three-exception work was unsearched.


## Complete diagonal cell partition

[done] The three-exception extension now excludes seven of ten two-full-A-star placements below 24 walls in the canonical family. New triple searches audit 150 fixed positive representatives, 128 excluded classes, 558 illuminated configurations and 1,988 guards; their projections remain incomplete. Target (2,2) is instead covered by a complete 40-outside-cell-set partition, whose 40 branches and unrestricted parent independently replay infeasible after 51 further configurations/202 guards. All 609 configurations, 2,190 guards, 40 mutations and 40 corrupt-guard checks pass. Independent enumeration checks all 698,437 bounded outside-cell subsets across four supports. Current peer verification is pending. Three placements remain unresolved, (1,1),(2,0),(2,1); no complete three-exception minimum, general bound, or smaller dark room. All Codex jobs stopped. See `three-triples/findings.md` and its receipts/manifests. This supersedes the previous six-placement status.


## Complete 105 set follow up

[done] Target(2,1) has105 exhaustive outside-cell sets. Search claims99 exclusions; fresh replay of all105 establishes100, leaving five raw sets/three mark-exchange symmetry types. All516 additional configurations and1032 new guards,8 mutations and8 corrupt-guard checks pass. Every two-outside-cell set is excluded; the residuals have zero or one outside cell. This does not exclude the whole placement. Overall seven of ten placements remain excluded. Claude has independently checked the structural/path/cell-set lemmas; further independent model/new-ray verification remains pending. All Codex jobs stopped. Explanation/diagram: `three-triples/cell-2-1-findings.md` and `cell-partition-explanation.png`; audit/input manifests alongside.


## Central-cell fan refinement narrows the skew placement

[done] A complete 57-mask split at A-cell(1,0), including absence, refines all five residual target(2,1) outside sets into285 branches. The discovery passes exclude264; fresh audit excludes267 and leaves18 feasible-after-cuts branches. All57 fan masks are excluded for each of {(-1,-1)} and {(3,2)}, closing two more outside sets. Combined with the previous100 audited exclusions,102/105 sets are excluded. The remaining sets are empty, {(1,-1)}, {(1,2)}, forming two mark-exchange types.

The audit checks393 new illuminated configurations,786 exact guards,8 mutations and8 corrupt guards; longest path39 reflections. Independent triangle adjacency verifies the56 nonempty partial fans plus the empty mask. The separate three-second replay directly excludes98/105 original cell branches; four previously proved two-cell branches cap at this shorter limit. Their earlier exclusions persist under the added valid constraints, so the cumulative102 count uses the union of prior proofs and two complete new fan proofs. The unrestricted parent remains feasible. Overall seven of ten placements remain excluded; no smaller room/full three-exception minimum.

Detailed report: `three-triples/fan-findings-2-1.md`. Frozen94-input manifest: `fan-proof-inputs-2-1.json`. Fresh receipt: `fan-audit-2-1.json`. All Codex jobs stopped; independent peer check pending.

**Next move:** split the18 residual branches at central cell(1,1), including absence.


## Double central-fan refinement and common-ray diagnostic

[done] The18 prior residual families refine into1,026 complete second-cell masks. Fresh audit excludes1,002, closes four first-fan families, and leaves24 feasible-after-cuts patterns across14 families. The physical half-turn exchanges them in12 pairs, verified from the triangle permutation. No additional outside set or whole placement closes: cumulative102/105 outside sets and seven of ten placements excluded remain unchanged. The unrestricted parent remains feasible.

The mechanism probe samples18 distinct rooms and tests61 directions/1,098 exact traces. Within this catalogue, an exact set-cover solve requires15 directions; no universal few-ray lemma follows. Five selected directions supply9 of129 new search witnesses, with120 using fallback. Audit verifies147 total new illuminated configurations and292 unique new guards,8 mutations/8 corrupt checks; longest new path28 reflections. An internal CP-SAT duplicate-column presolve assertion occurred at a saved discovery checkpoint; resume and fresh audit disable presolve without changing constraints. All checks pass and all jobs stop.

Claude now independently confirms the earlier(3,1),(3,2),(4,0) exclusions, plus(4,1),(5,0) by his checked path bound; his report notes no placement-specific positive control for(4,0). Newer(3,0)/(2,2)/(2,1) inputs are sent for independent replay. No smaller room or full three-exception minimum.

Report/figure: `three-triples/double-fan-findings-2-1.md`, `neck-patterns-2-1.png`; fresh receipt `double-fan-audit-2-1.json`; frozen102-input manifest `double-fan-proof-inputs-2-1.json` and supplementary symmetry manifest `neck-pattern-proof-inputs-2-1.json`.

**Next move:** seek a geometric illumination argument for the12 necessary neck types using the remaining wall/exception budget. The hoped-for common-ray shortcut remains unproved.


## Exceptional-state bound and a common midpoint-path candidate

[done] A local budget/connectivity propagator preserves422 valid saved/half-turned room controls across all12 neck types.17,440 local fan masks,200 exhaustive budget fixtures and200 exhaustive connectivity fixtures pass audit. Types8–10 force one additional detour triangle, but no universal illumination conclusion follows from the local propagation.

A derived elementary lemma bounds exceptional-vertex visits of a first-arrival ray by K=rJ+(r/2)S, where J counts interior B/C exceptions, S smooth-boundary B/C exceptions, and r=|D4*d|. Hence K<=24 with three exceptions. Primitive unfolding time is twice the encounter count. Canonical grid-line crossings then give a reflection bound2K*(|p|+|q|+max(|p|,|q|)) for each fixed primitive direction. The implementation decides that direction without an arbitrary bounce cutoff. Primitive directions remain infinite; this is not an all-direction darkness decision or a new room exclusion. Independent peer verification of the derivation is pending.

All147 saved rooms now have exact paths with one exceptional encounter at their optical midpoint, including104 samples spanning all12 current neck types.122 original rays already had this property. A128-direction probe finds21 alternatives; a targeted component-bound16 pass finds the last four. Fresh independent triangle tracing replays all1,940 direction tests and25 alternative witnesses. The gate audit also checks490 affine edges/four parity classes,64 point-group products,147 original positives,192 low-direction negatives,32 strict-dark directional controls and three rejected inputs. All pass. This is evidence from a selected positive population, not a universal single-pass theorem.

No new room geometry or exclusion guard is added. Twelve neck types remain; cumulative102/105 outside sets and7/10 placements excluded are unchanged. All jobs stopped. Proof/findings: `three-triples/neck-budget-findings-2-1.md`; frozen123-input manifest: `neck-budget-proof-inputs-2-1.json`; receipts `neck-budget-audit-2-1.json` and `gate-bound-audit-2-1.json`.

**Next move:** prove or disprove single-pass midpoint-gate sufficiency for every completion of the12 neck types under the wall/exception budget.


## First universal conditional midpoint cover

[done] The geometry-only parent now proves every completion of neck type 7 is illuminated by an exact one-exception midpoint ray. Its fixed signature is no outside cells, central masks 40 and 83. A finite catalogue of 1,066 sufficient triangle patterns covers this family; a fresh replay needs only a sufficient 37-pattern assumption core. All paths, independent closed-triangle coverage, twelve fixed positive controls, eight mutations and eight corrupt guards pass. The longest path has33 reflections. This is a computer-assisted conditional theorem; independent peer review and a formal UNSAT certificate remain unavailable/pending respectively.

The central-gate-only and forced-pair finite catalogues remain inconclusive. The successful core uses variable third-exception locations. One canonical family and its mark-exchange partner close:24 raw/12 canonical patterns become22/11. The whole target(2,1) placement remains open, with102/105 outside sets and7/10 whole placements excluded.

Of390 processed geometries,380 are genuinely new and10 revisited. The midpoint phase adds586 genuinely new guards (542 learned and44 alternative seed paths), bringing the composed parent to3,793 guards. Cumulative three-triples totals are2,045 new geometries and4,886 new guards. Counts and old input hashes are checked by `finalize_illumination_midpoint.py`; receipt `three-triples/midpoint-cover-dedup-2-1.json`.

[done] Claude independently confirms all seven earlier whole-placement exclusions. His23-wall survivor also has a verified12-reflection one-pass midpoint ray via(4,3), outside the previous sufficient catalogue. This separate peer check is not included in phase search totals.

[waiting on Claude] New conditional theorem/core review, plus prior fan/neck/gate derivations. Frozen137-input manifest: `three-triples/midpoint-cover-proof-inputs-2-1.json`. Full report: `three-triples/midpoint-cover-findings-2-1.md`.

**Next move:** a bounded sufficient-cover extension over the eleven remaining neck types, seeded by the peer survivor, with separate outputs and fresh audits.


## Midpoint extension closes seven of twelve residual neck types

[done] The fresh geometry-only audit proves universal one-pass midpoint illumination for types5,7,9,10,12. New sufficient cores have147,91,91,105 guards for types5,9,10,12, respectively; the original type7 core has37. Fresh core-only replays and positive controls pass; none of these subsets is claimed minimum. The2,598-pattern catalogue includes1,066 inherited conditions, two peer seeds, and1,530 learned conditions. All765 recorded positive geometries and1,530 learned paths/guards pass exact checks and independent closed-triangle coverage; twelve fixed positive controls and8 mutation/8 corrupt-guard checks pass. New rays use at most24 reflections; inherited rays reach33. Both peer guards pass independent coverage checks.

Composition with historical cuts gives5,063 unique half-turn-closed guards and additionally excludes types4 and11. Thus7/12 canonical neck types (14 raw patterns) are excluded;5 types (10 raw patterns) remain:1,2,3,6,8. The standalone midpoint theorem still has seven open types; the smaller-dark-room search only needs the five that survive composition. All three remaining outside sets and the unrestricted parent remain feasible. Counts102/105 outside sets and7/10 whole placements excluded stay unchanged; no smaller dark room or full three-exception minimum.

Cross-phase reconciliation finds746 genuinely new geometries among765 (19 revisits),1,268 new learned guards, and2 new peer guards. Cumulative three-triples totals become2,791 new geometries and6,156 new guards. The separate peer geometry is not added to search-geometry totals. All Codex jobs finished.

[waiting on Claude] New neck implications/composition review. The151-input `three-triples/midpoint-extension-proof-inputs-2-1.json` freezes the new scripts, results, findings and original137-input dependencies. Earlier frozen inputs remain unchanged. Full report: `three-triples/midpoint-extension-findings-2-1.md`.

**Next move:** focus the midpoint argument on the five live types, especially type8, the only surviving canonical outside-cell case. Avoid further universal-only work on already excluded types4 and11.


## Type 8 and type 6 reduce the remaining placement to three neck types

[done] Both new searches exhausted and fresh audits passed. Type8 adds70 new geometries/140 guards; type6 adds26 new geometries/52 guards. All96 are new against frozen earlier inputs. Exact paths, independent triangle coverage, positive geometry controls and mutation/corrupt-guard checks pass. The composed parent has5,255 unique guards and remains feasible.

Type8 closes both remaining nonempty outside-cell sets;104/105 complete outside sets are excluded. Type6 leaves three canonical necks1,2,3, all with empty outside set and first central mask12 (second masks82,83,210). Nine of12 canonical necks are excluded. Their geometry-only midpoint parents remain feasible, so these two exclusions require historical positive-ray cuts. Whole-placement count stays7/10; no smaller dark room or full three-exception minimum.

Cumulative three-triples totals:2,887 new geometries/6,348 new guards. Frozen inputs: `three-triples/type8-proof-inputs-2-1.json` (159 paths), `three-triples/type6-proof-inputs-2-1.json` (168 paths). Reports: `type8-findings-2-1.md` and `type6-findings-2-1.md` in that directory.

[waiting on Claude] Neutral reproduction commands for both phases posted on the board. Claude has independently confirmed the original type7 core and seven prior whole-placement exclusions; the new phase checks remain pending.

**Next move:** search the shared empty-outside / first-mask12 parent, then require a fresh unrestricted-parent replay before claiming closure of placement(2,1).


## Eighth placement excluded by complete partition composition

[done] Placement(2,1), physical displacement(4,2), is excluded below24 walls for the canonical simple two-A-star / exactly-three-B/C-exception family. The shared first-mask12 search exhausts after180 new geometries/360 new sufficient ray guards. Fresh exact paths, independent triangle coverage, three positive controls,8 mutations and8 corrupt-guard checks pass; all12 canonical necks replay INFEASIBLE. The composed parent has5,615 unique half-turn-closed guards.

The unsplit parent solve returns UNKNOWN at60 seconds. Exclusion instead follows from the checked exhaustive certificate hierarchy:105 cell sets (100 already excluded),285 first-fan branches (267 excluded),1,026 second-fan branches (1,002 excluded), then24 raw patterns paired into the12 freshly excluded neck types. `audit_illumination_partition_closure.py` checks all branch keys, independent57-mask lists, source hashes/provenance, symmetry and guard inclusion. All earlier branch conditions remain valid with the new positive-ray cuts. Every leaf is excluded; no UNKNOWN is treated as proof. The geometry-only midpoint parent remains feasible.

Whole-placement count is now8/10. Only(1,1),(2,0) remain; the full three-exception minimum remains open. All180 phase geometries are new against frozen inputs, bringing cumulative three-triples totals to3,067 new geometries/6,708 new guards. This does not establish a general-polygon bound or export a formal UNSAT proof.

[waiting on Claude] New179-input manifest `three-triples/mask12-proof-inputs-2-1.json` freezes paths, audits and the complete composition checker. Neutral independent-review instructions are on the board. Earlier manifests and peer files are untouched. Report: `three-triples/mask12-findings-2-1.md`.

[done] Next-case saved-path comparison verifies37 paths for(1,1) and39 for(2,0). Single-event midpoint witnesses account for34/37 and29/39, respectively. This is sample evidence only; multi-event witnesses do not preclude alternative single-event paths. Receipt: `three-triples/remaining-gates.json`. All Codex jobs finished.

**Next move:** target(1,1). Try exact alternative single-event paths for its three saved multi-event rooms, then formulate a bounded midpoint-cover parent.


## Placement(1,1): one-pass samples and a complete two-family hub reduction

[done] All three saved multi-event samples have alternative single-event midpoint rays; all37 original samples now have one-pass witnesses. A bounded complete-parent run adds110 illuminated configurations; fresh exact rays, independent triangle coverage, three positive controls,8 mutations and8 corrupt-guard checks pass.96 geometries are genuinely new,14 revisited. The588-pattern midpoint catalogue remains feasible as a geometry-only parent.

[done] Historical reconciliation corrected the initial parent: it had2,001 original cuts but omitted a626-cut later extension.112 of448 phase guards were already in that extension, so only336 are globally new. All514 restored missing guards received fresh exact and coverage checks. The merged2,963-guard parent, with the previously audited2,530-set connected-cell table, remains feasible. Cumulative three-triples totals now3,163 new geometries/7,044 new guards. The eight-placement exclusion count is unchanged.

[done] The two full marked stars meet at physical(1,1), forcing four of eight hub triangles. Independent adjacency and sector enumeration agree on seven possible masks. Full hub255 is always illuminated by the direct zero-reflection ray; a positive full-hub control and sufficient-condition implication pass. The other six masks form exactly two symmetry families: two six-triangle masks175/243, and four seven-triangle masks191/239/247/251. All six fixed-mask models replay feasible. These are local necessary shapes, not six room outlines or dark examples.

[waiting on Claude] New193-input manifest `three-triples/midpoint-proof-inputs-1-1.json`; neutral check commands posted, with required `<root>/.context/` copy layout. Peer now independently confirms the earlier(2,1) midpoint extension, including all2,598 paths and four new standalone cores; newer eighth-placement phases remain pending. Peer files and all earlier frozen inputs untouched. All Codex jobs finished.

**Next move:** target the denser seven-triangle hub family, canonical mask191. Reconstruct the merged parent from original2,001 + current448 + restored514 guards (2,963 total), apply the audited connected-cell table, then attempt a bounded exact one-pass cover. Do not restart from the incomplete2,001-cut base alone. No smaller dark construction or full three-exception minimum established.


## Seven-hub refinement excludes five of seven tip fans

[done] Canonical hub191 raw search adds50 genuinely new geometries/200 sufficient guards, freshly audited with independent triangle coverage and mutation/corrupt controls. Family remains feasible. The absent hub triangle has A tip physical(2,0); hub191 fixes one present and one adjacent absent star bit. Independent cycle/sector enumeration gives exactly seven compatible tip masks4,5,7,23,87,215,247, containing1–7 triangles.

[done] Bounded complete seven-fan synthesis adds24 new geometries/96 guards. Fresh exact paths, coverage, three fixed controls,8 mutations/8 corrupt checks and all seven replays pass. Five tip branches close:7,23,87,215,247. The last two are geometrically impossible without rays; the first three need historical cuts and remain feasible with the midpoint-only catalogue. All four mark stabilizers preserve the3,259-guard parent. Only tip masks4,5 remain, differing by one bit; whole hub191 and placement(1,1) remain feasible. Global counts8/10 placements,3,237 new geometries/7,340 guards.

[done] Claude independently confirms the complete(2,1) exclusion:6,125 exact witnesses,5,615 independently rebuilt cuts, all105 outside sets excluded and monolithic INFEASIBLE in his own stronger model. All eight whole-placement exclusions now independently confirmed. New(1,1) phases await his review.

[waiting on Claude] Frozen204-input raw-hub certificate `three-triples/hub7-proof-inputs-1-1.json` and212-input fan certificate `hub7-fan-proof-inputs-1-1.json`; neutral nested-layout commands on the board. Older inputs and peer files untouched.

**Next move:** the union of tip masks4,5 fixes every tip bit except bit0. Test this residual parent under all3,259 guards and audit the full seven-fan composition.


## Two residual tip patterns differ by one fixed C exception

[done] The residual union of masks4,5 adds30 genuinely new geometries/120 sufficient one-pass guards; fresh exact paths, independent coverage, three fixed positive controls,8 mutations/8 corrupt checks pass. Maximum new reflections22. The3,379-guard parent is closed under all four mark stabilizers. Both residuals remain feasible; the prior five fan exclusions replay intact. Whole seven-hub and whole(1,1) remain open; counts stay8/10 independently confirmed whole placements. Cumulative three-triples totals3,267 new geometries/7,460 new guards.

[done] Exact incident-triangle geometry shows why the two residuals differ: at C(1,0), mask4 fixes3 of4 right triangles, an ordinary270-degree concave boundary corner. Mask5 adds the fourth, forcing an interior C exceptional vertex and leaving only two of the three B/C exceptions unfixed. Independent sector and right-angle assertions pass without a solver. This does not force rays to use that C point or prove illumination.

[waiting on Claude] Frozen223-input certificate `three-triples/hub7-residual-proof-inputs-1-1.json` includes the current fresh audit and `tip-gate-1-1.json`; neutral nested-layout commands are on the board. Earlier inputs and peer files unchanged. All Codex jobs finished. Across this continuation104 new geometries and416 new guards; five of seven tip branches excluded, not an entire placement.

**Next move:** target tip5 with fixed interior C(1,0); project the two remaining typed exceptional vertices under the3,379-guard parent. Keep tip4 and the six-hub family as separate open branches. Full three-exception minimum remains unproved.


## Forced-C case closes: six of seven tip fans excluded

[done] Local geometry fixes both interior C(1,0) and smooth C(2,1) under hub191/tip5. The third exception has exactly six typed possibilities after3,379 historical-ray guards. Projection exhausts, with144 logical partition checks, positive rooms/controls and a fresh complementary-parent exclusion. This is complete, not a capped sample.

[done] All six cases exhaust after8 illuminated configurations/32 sufficient one-pass guards. Fresh audit: all six cases, the complementary parent and the unsplit tip5 parent INFEASIBLE;6 fixed positives and8 mutation/8 corrupt checks pass, new rays at most21 reflections.3 geometries genuinely new,5 revisit projection controls. The3,411-guard parent retains all four mark symmetries. Geometry-only midpoint parent remains feasible, so historical cuts are essential to this exclusion.

Six of seven hub191 tip fans are now closed:5,7,23,87,215,247. Only one-triangle tip4 remains open within this hub family; the six-triangle hub family remains open separately. Whole count8/10 independently confirmed; cumulative3,270 new geometries/7,492 new guards. No smaller dark room or full three-exception minimum.

[waiting on Claude] Frozen231-input pair-partition and239-input case-cover manifests; neutral nested-layout commands posted. Earlier certificates/peer files untouched.

**Next move:** project the two free typed exceptions in tip4 with smooth C(2,1) fixed, ordinary concave C(1,0), and all3,411 guards.


## Last thin-tip projection retains an open remainder

[done] After the verified tip5 exclusion, tip4 is the sole remaining fan within hub191. A finite local check confirms smooth C(2,1) is fixed and C(1,0) is ordinary concave. Two free exceptional vertices remain. Bounded projection lists25 typed pairs; fresh audit accepts physical/model controls and1,012 logical disjointness/complement assignments. The unlisted remainder is feasible (witness smooth(3,1),smooth(5,1)), so projection is incomplete. The25 listed branches plus their explicit complement form the complete partition.

No new illumination cuts or placement exclusion. Whole count8/10 independently confirmed;3,411 current guards, cumulative3,270 new geometries/7,492 new guards. The six-hub family stays separately open. New247-input certificate `three-triples/thin-tip-pairs-proof-inputs-1-1.json` and prior239-input six-case exclusion frozen; neutral peer commands posted. All Codex jobs finished.

**Next move:** targeted ray covers of25 known pair branches AND the explicit remainder, without treating capped enumeration as complete.


## Thin-tip ray phases:24 of25 listed pairs excluded

[done] Fresh replay excludes24 of25 listed typed pairs under hub191/tip4. The sole listed survivor fixes interior C(1,2) and interior C(2,3), in addition to the forced smooth C(2,1). The unlisted-pair complement also remains feasible. Both are retained explicitly. Tip4, the seven-hub family, and placement(1,1) remain open; the six-hub family is separate. Whole-placement count stays8/10 independently confirmed.

[done] This extension adds27 verified one-pass witnesses/108 sufficient guards:26 geometries new relative to the256-input lineage, one revisit. Fresh audit accepts three pre-extension positive controls, eight mutations, eight corrupt-guard checks, and all four mark stabilizers. Maximum new reflections20. Parent now3867 unique guards.

Across both thin-tip ray phases:114 verified configurations,100 genuinely new geometries,14 revisits,456 new sufficient guards. Cumulative three-triples totals3370 new geometries/7948 new guards. These are computer-assisted exclusions under the historical ray cuts, not geometry-only universal midpoint lemmas or formal UNSAT certificates.

[done] Claude independently confirmed the preceding247-input thin-tip projection and3411 guards. The256-input first ray cover and newest continuation have been handed off neutrally; their independent review remains pending. Claude has been offered disjoint discovery at placement(2,0), while Codex retains(1,1). No Claude-owned files changed.

[waiting on Claude] Verify thin-tip-extension-proof-inputs-1-1.json, preserving the nested root/.context layout, with audit_illumination_thin_tip_extension.py. This manifest freezes all inputs and receipts.

**Next move:** analyze the interior-C survivor pair geometrically, and refine or search the explicit unlisted complement. Any complete tip4 exclusion must close both. No smaller dark room or full three-exception minimum is established. All Codex jobs finished.


# All originally listed pairs closed; complete remainder classification

[done] All25 originally listed typed pairs under hub191/tip4 now replay INFEASIBLE with3987 guards. The final interior-C pair was refined into five complete local fans; one new11-reflection ray at direction(4,11), together with historical conditions, closes the last fan. Independent local angular-slot/triangle-adjacency checks agree on34600 masks. The pair forces22 present/8 absent triangles; local and solver positive controls pass.

[done] The unlisted complement is now split completely by the number of free interior exceptional vertices:0,1,2. Each exceptional vertex has type1(smooth boundary) or type2(interior), and the fixed gate C(2,1) has type1. The four assignments(1,1),(1,2),(2,1),(2,2) have unique counts0,1,1,2 and total defect credits3,4,4,5. This gives an exact exhaustive logical partition. The solver-only complementary query remains UNKNOWN; it is not used as an infeasibility proof. The initial audit stopped on that query; its traceback is retained in the log, followed by the corrected audit and PASS receipt.

[done] Remainder phase:26 genuinely new geometries/104 sufficient one-pass guards; fresh counts0/1/2 all feasible. Six positives include a fixed room in each count group;8 mutations/8 corrupt checks and all four mark stabilizers pass. Maximum17 new reflections. All25 earlier pairs freshly replay INFEASIBLE; unsplit tip4 remains feasible.

Across this continuation:30 verified configurations,29 genuinely new geometries,1 revisit,120 new sufficient guards. Cumulative three-triples totals3399 new geometries/8068 guards; current parent3987 unique guards. Interior-pair/fan certificate276 inputs is frozen separately. Latest remainder certificate includes all dependencies and receipts. New phase independent review pending.

[waiting on Claude] Verify remainder-types-proof-inputs-1-1.json in a nested root/.context copy with audit_illumination_remainder_types.py; independently derive the count partition and check sufficient tile conditions. Claude is actively running the disjoint(2,0) cut loop in his own directory. His files remain untouched.

Whole placements remain8/10 independently excluded. Tip4 and the six-hub family at(1,1) remain open; placement(2,0) remains open pending Claude's ongoing search. No smaller dark room or full three-exception minimum. All Codex jobs finished.

**Next move:** inspect the surviving zero-interior group, where all three exceptional vertices lie on smooth boundary segments, and choose a complete geometric split of their boundary arrangement. Retain the one- and two-interior groups explicitly.


## Three-exception family completed (2026-10-30)

[done] All ten two-full-A-star placements are excluded below24 walls. Final audits check7725 exact paths, rebuilding5710 and4671 sufficient conditions at(2,0)/(1,1). All190/657 symmetry groups are INFEASIBLE, with explicit maps covering699/2530 outside-cell cases. The earlier I=3 exclusion and W>=6+6I-2k bound for I>=4 complete the exactly-three-exception branch. Prior results cover k<=2; the strict24-wall control attains the bound. A smaller simple room in this tiling with interior A marks needs at least four B/C exceptions. No smaller dark construction or general-polygon result was obtained.

[done] Allowing multi-event paths improved the finite cover:457 of2299 new(2,0) witnesses use more than one exceptional event. The saved single-event-only cover remains feasible in both difficult subcases. This limits that finite certificate; it does not prove another single-event path impossible.

[done] Final proof uses complete partition/symmetry composition, passing independent physical/condition checks and positive controls. UNKNOWNs and interrupted experimental runners are not proofs. Scope, frozen manifests and reproduction: `three-triples/three-exception-complete.md`.

[done] Projection specialization:28550+46710=75260 Boolean condition comparisons pass. Earlier higher-star and k<=2 results are composed, not rerun wholesale. Scope excludes arbitrary polygons, non-A marks, other tilings and k>=4. No formal UNSAT certificate or improved construction.
