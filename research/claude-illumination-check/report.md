# Claude verification of the two-exception illumination exclusion

**Result: confirmed.** For simple canonical 45-degree rooms with exactly two
transparent B/C points and distinct interior A marks, no room with at most 23
walls is dark. Each check below either reruns Codex's work in an isolated copy
or uses code Claude wrote without importing Codex modules.

Date: 2026-10-29. Directory: `.context/claude-illumination-check/`.

## Scope and independence

Before starting, Claude read Codex's board entry stating the conclusion. The
checks are therefore not blind, so they were designed to fail loudly instead.

- `claude_ray_guard_check.py` and `claude_relaxed_replay.py` import only the
  standard library and OR-Tools. They share no geometry, support, or model code
  with Codex.
- One step uses Codex's tracer, `illumination_paths.find_path`, to *find*
  rays. Claude's checker then verifies those rays.

## 1. Analytic reduction: no gap found

Claude rederived the following by hand:

- W = 2 + 6I + Q − E.
- The graph-degree bound P + m ≤ 9.
- The support radius 9 − b and the bound D ≤ 4, which leave seven targets.
- The I ≥ 4 exclusion.
- The I = 3 equality case. All three exception mixes, (J, s_N) = (2,0), (1,1),
  and (0,2), need exactly seven external neighbors, which forces the L and J = 2.

## 2. Codex audits rerun from the copy

| Audit | Result |
| --- | --- |
| `audit_illumination_three_star.py` | PASS: 0 solutions, 257 nodes |
| `audit_illumination_two_exception.py` | PASS, identical to the original (timing fields ignored) |
| `audit_illumination_exception_pairs.py` | PASS, identical to the original (timing fields ignored) |

Codex's original outputs are kept in `codex-original/`.

## 3. Ray-cut soundness: all 3,660 guards pass

`claude_ray_guard_check.py` rebuilds each support from the analytic definition
and matches the recorded triangle-index SHA-256. For every guard it then does
two things:

- It checks with exact rationals that the path is a legal billiard path between
  the marks. Open segments must stay in the interior, every bounce must obey the
  reflection law on a straight wall, and the path must hit no nonsmooth corners.
- It computes every tile whose closure meets the path and confirms the guard
  fixes each of those tiles to its state in the room.

Any room that satisfies a guard therefore contains the same illuminating path.

| Source | Guards |
| --- | ---: |
| two-global 1-1 / 2-0 / 2-1 / 2-2 | 613 / 882 / 439 / 76 |
| two-pair-search 1-1 / 2-0 / 2-1 | 1076 / 316 / 258 |

The checker was tested with four kinds of negative control, 60 trials each.
All 240 trials behaved as expected:

- dropping a guard fact
- flipping a tile on the path
- moving a bounce point off its wall
- flipping a tile away from the path, which should not invalidate the path

Output: `claude-ray-guard-check.json`.

## 4. Independent model replay: all seven placements INFEASIBLE

`claude_relaxed_replay.py` is a new CP-SAT model. It is a relaxation of
Codex's model, with these constraints:

- per-vertex single-sector tables
- walls equal corners, at most 23
- transparent B/C points counted
- Euler characteristic 1
- both marks fixed as full stars
- the verified cuts

It omits connectivity, the triangle bound, and the counting identity, so an
INFEASIBLE result also holds for the real family.

| Target | Cuts | At most 2 exceptions | Exactly 2 exceptions |
| --- | ---: | --- | --- |
| (3,0), (3,1), (4,0) | 0 | INFEASIBLE | implied |
| (2,2) | 76 | INFEASIBLE | implied |
| (1,1) | 1689 | feasible, 1 exception | INFEASIBLE |
| (2,0) | 1198 | feasible, 1 exception | INFEASIBLE |
| (2,1) | 697 | feasible, 1 exception | INFEASIBLE |

The three rooms the at-most-2 run found are connected 23-wall rooms with one
exception, which places them in the one-exception phase. Each is lit: the
tracer found paths with 16, 17, and 13 bounces, and the checker accepted all
three. This is consistent with Codex's one-exception result but doesn't
re-verify it.

Positive controls for the model:

- The known 24-wall room is accepted at a cap of 24 and rejected at 23.
- 19 sampled illuminated rooms are accepted with matching wall and exception
  counts, and each is removed by its own cuts.

## Remaining limits

- The result is still conditional on CP-SAT. Two different CP-SAT models now
  agree, but neither produces an UNSAT proof file.
- Claude didn't re-verify the zero- and one-exception phases, which the
  "at most two" conclusion depends on.
- Pair classification is used only for discovering rays, so its correctness
  doesn't affect the result.

# Three full A stars with exactly three exceptions (blind check)

**Result: confirmed.** Claude derived the reduction and ran its own model before
reading `three-star-extension-findings.md` or the summary.

- **Reduction** (`three-star/claude_three_star_reduction.py`): P+m ≤ 8, and
  the 3,945 normalized three-cell shapes out to Manhattan distance 12 leave
  exactly 5. These are the line, L, skew, V, and diagonal shapes, with outside
  budgets 0,0,0,0,1. They match Codex's 5 shapes, 11/11/11/11/21-cell supports,
  and external counts. I ≥ 4 gives W ≥ 28.
- **Mark cases:** there are 11 orbits. The 3 adjacent pairs light up directly
  through the shared interior C. The other 8 are the same as Codex's 10 raw
  cases, before symmetry reduction.
- **Rays** (`three-star/claude_three_star_replay.py`): all 23 guards pass
  Claude's exact checker. Sampled saved rooms are accepted with matching wall
  counts.
- **Independent model:** shapes 0–2 are INFEASIBLE with no marks or cuts. The
  line, with 1 cut, and the L, with 22 cuts, are INFEASIBLE.
- **Codex audit** rerun from the copy: PASS, identical to the original apart
  from timing fields.
- **Digests:** the case files for shapes 0–2 store no triangle digest. Those
  cases have no cuts, so this has no effect.

**Next branch, I=2 with k=3:** Claude derived the bounds by hand and they match
Codex's: P+m ≤ 10, outside cells ≤ 10−b, D ≤ 5, 10 nonadjacent placements, and
N ≤ 36.

# Two full A stars with exactly three exceptions (partial verification, 2026-10-29)

**Status: partly verified.** Codex is still working on this branch, so these
are interim checks.

| Check | Result |
| --- | --- |
| Bounds: P+m ≤ 10, outside ≤ 10−b, D ≤ 5, 10 placements, N ≤ 36 | Derived by hand; agree with Codex |
| Frozen inputs: 134 files from both manifests | SHA-256 match |
| All 4,786 saved guards in `three-two-star/` and `three-triples/` | PASS on Claude's exact checker; supports match Codex digests |
| Path-charge lemma in `illumination_cell_path_bound.py` | Derivation checked; holds |
| Connected outside-cell table | Derivation checked; holds |
| Path minima, recomputed with Claude's own enumerator | Equal to Codex's closed form for all 8 targets with D ≥ 3 |
| (4,1) and (5,0) | Excluded by the path bound alone: W ≥ 24 and W ≥ 26 |
| No-cut geometry, Claude's relaxed model, 180 s cap | FEASIBLE at (1,1), (2,0), (2,1), (3,0), (2,2), (3,1); UNKNOWN at the far four |
| Codex-closed (3,1) with 84 cuts, (3,2), and (4,0) | UNKNOWN after 1,500 s in Claude's relaxed model |

Claude's relaxed model has no connectivity, no counting identity, and no
path-charge or cell-set constraint. Its UNKNOWN results neither confirm nor
refute Codex's exclusions.

To close the gap, Claude would add the now-verified lemmas to its own model:
the charge Q + m ≥ path bound, and the outside-cell table.

Not yet done:

- Codex's own audits for this branch (`audit_illumination_three_two_star.py`
  and `audit_illumination_exception_triples.py`)
- The triple-classification projection check for (3,0)

## Update: strengthened Claude model (`two-star-k3/claude_k3_strong.py`)

The model adds only constraints Claude derived or checked:

- vertex tables that carry the A charge and the exception type
- W = 2 + 6·I_A + Q − 2J − s_N
- N ≤ 36 and P+m ≤ 10
- Q+m ≥ the path minimum, from Claude's own enumerator
- outside cells limited to connected sets of size ≤ 2
- tile connectivity, enforced as a flow
- Euler characteristic 1
- the verified cuts

| Target | Cuts | Result |
| --- | ---: | --- |
| (3,1) | 84 | INFEASIBLE (25 s) |
| (3,2) | 0 | INFEASIBLE (1 s) |
| (4,0) | 0 | INFEASIBLE (6 s) |
| (4,1), (5,0) | — | Excluded by the path bound alone |

**All five placements that Codex reports closed are now independently
confirmed.**

Controls:

- Nine saved illuminated rooms from (3,1), (3,0), and (2,2) are accepted when
  fixed with no cuts. Each has 23 walls and matches Codex's counts.
- At (3,2), raising the wall cap to 24 finds a 24-wall room.

Caveat: (4,0) has no placement-specific positive control. With the
cap-dependent constraints removed, it is UNKNOWN after 300 s at caps 23, 25,
and 27. Its exclusion relies on code that passes controls elsewhere.

Still open in Codex's search: (1,1), (2,0), (2,1), (2,2), and (3,0). Not yet
run: Codex's audit scripts for this branch.

## Update 2026-10-30: final cuts for (3,0), (2,2), and (2,1)

Inputs: the 102-path `double-fan-proof-inputs-2-1.json`. All hashes match.

- **In-place guards:** all 7,338 pass Claude's exact checker, and every digest
  matches.
- **Seed cuts:** these are rays reused from lower-exception phases, stored only
  as references plus recompiled facts. Claude's earlier guard checks skipped
  them. `claude_k3_seed_check.py` resolves each reference and verifies it, and
  all 3,908 pass: 1,853, 1,266, 713, and 76 at (1,1), (2,0), (2,1), and (2,2).

| Target | Verified cuts | Claude strong model | Codex claim |
| --- | ---: | --- | --- |
| (3,0) | 26 | INFEASIBLE (114 s) | excluded |
| (2,2) | 1,390 including seeds | INFEASIBLE (62 s) | excluded |
| (2,1) | 3,207 including seeds | FEASIBLE: a 23-wall survivor with 3 smooth exceptions, lit by a 13-bounce path that Claude's checker verified | open |

The first (2,2) run omitted the 76 seed cuts and found a 21-wall room. That
room is lit, so it was a gap in Claude's cut loading, not a counterexample.
Codex's parent model, with that room fixed, is INFEASIBLE through 4 seed cuts.

**Status: 7 of 10 placements are independently confirmed excluded.** These
are (3,0), (3,1), (3,2), (4,0), (4,1), (5,0), and (2,2). Placements (1,1),
(2,0), and (2,1) remain open, matching Codex.

Not yet done:

- Codex's own audit scripts for this branch
- The fan-partition, neck-budget, and gate-bound requests

These refine the open (2,1) case and don't affect the seven exclusions.

## Update 2026-10-30: (2,1) neck-type-7 midpoint cover

**Result: confirmed.** In Claude's model, every completion of neck type 7 is lit
by one of Codex's 37 core one-pass rays. Neck type 7 has no outside cells, mask
40 at A-cell (1,0), and mask 83 at (1,1).

Inputs: the 137 files in `midpoint-cover-proof-inputs-2-1.json`, copied to
`midpoint-2-1/`. All hashes match.

| Check | Result |
| --- | --- |
| Codex audits rerun from the copy: cover audit, core analysis, parent replay | All PASS; identical to the originals apart from timing fields |
| All 1,066 guards (286 seeds, 780 derived) on Claude's exact checker | 0 failures |
| Guard rooms that have the type-7 signature | 31, including Codex's control (guard 86) |
| Claude's strong model, type 7 fixed, no cuts | FEASIBLE, 23 walls |
| Same, Codex's control room fixed | FEASIBLE, 23 walls |
| Same, only the 37 core cuts | INFEASIBLE |
| Same, all 1,066 cuts | INFEASIBLE |
| Drop-one control: remove each core cut in turn | 35 of 37 drops reopen the model; the dropped cut's ray lights every reopened room |

The type-7 neck is fixed with Claude's own fan ordering: bit j is the j-th
sorted tile that contains the cell's A vertex. Code is in
`midpoint-2-1/claude_midpoint_check.py` and `claude_midpoint_dropone.py`.
`claude_k3_strong.py` gained an `extra` hook for the restriction.

Scope:

- This proves the cover for one of 12 neck types. Codex's parent replay
  reports `placement_excluded: false`, so (2,1) stays open.
- The result is still conditional on CP-SAT, with no UNSAT proof file.

## Update 2026-10-30: (2,1) midpoint extension

**Result: confirmed.** Types 5, 9, 10, and 12 are each covered by their own
geometry-only core cuts. With historical cuts added, types 4 and 11 are also
excluded. Five neck types stay feasible, matching Codex: 1, 2, 3, 6, and 8.

Inputs: the 151 files in `midpoint-extension-proof-inputs-2-1.json`, copied to
`midpoint-ext-2-1/`. All hashes match.

| Check | Result |
| --- | --- |
| Codex audits rerun from `midpoint-ext-2-1/codex-run/.context/` | All 3 PASS; identical to the originals apart from timing fields |
| All 2,598 geometry-only guards on Claude's exact checker | 0 failures |

Claude's strong model, geometry only, with the neck fixed:

| Type | No cuts | Codex control fixed | Core cuts only | Drop-one reopens |
| --- | --- | --- | --- | --- |
| 5 | FEASIBLE | FEASIBLE | INFEASIBLE (147) | 97 of 147 |
| 9 | FEASIBLE | FEASIBLE | INFEASIBLE (91) | 64 of 91 |
| 10 | FEASIBLE | FEASIBLE | INFEASIBLE (91) | 60 of 91 |
| 12 | FEASIBLE | FEASIBLE | INFEASIBLE (105) | 80 of 105 |

In every reopened run, the dropped cut's ray lights the room it lets back in.

Composed model: 3,207 verified historical and seed cuts plus all 2,598
midpoint guards.

| Type | No cuts | Composed |
| --- | --- | --- |
| 4, 11 | FEASIBLE | INFEASIBLE |
| 1, 2, 3, 6, 8 | — | FEASIBLE, matching Codex |

Scope:

- Seven of 12 neck types are excluded at (2,1). The placement stays open, so
  the whole-placement count is still 7 of 10.
- The result is still conditional on CP-SAT, with no UNSAT proof file.
- Codex's scripts resolve inputs as `<root>/.context/...`, so the rerun uses a
  nested copy. The first rerun from the flat copy failed with
  `FileNotFoundError`; that was a layout issue, not a result.

## Update 2026-10-30: placement (2,1) excluded

**Result: confirmed.** No room at placement (2,1) is dark under Claude's model
and Claude's own cuts. **8 of 10 placements are now independently confirmed
excluded.**

Inputs: the 179 files in `mask12-proof-inputs-2-1.json`, copied to
`placement-2-1/run/.context/`. All hashes match.

Claude didn't use Codex's tile facts or triangle indices for this check.
`claude_placement_check.py` works as follows:

1. It collects every room and illuminated path in the 49 target-(2,1) input
   files. That's 6,125 distinct witnesses.
2. It checks each path with Claude's exact checker. None are rejected.
3. It builds each cut from the tiles whose closure meets the path, indexed in
   Claude's own support. This gives 5,615 unique cuts, the same count Codex
   reports.

| Check | Result |
| --- | --- |
| Codex `audit_illumination_mask12.py` and `audit_illumination_partition_closure.py`, rerun | Both PASS; identical to the originals apart from timing fields |
| Claude's strong model, whole placement, all 5,615 cuts | INFEASIBLE (398 s). Codex's monolithic model was UNKNOWN. |
| Claude's own split by outside-cell set: all 105 connected sets | All 105 INFEASIBLE, 60 s cap each; no fan split needed |

Controls:

| Control | Result |
| --- | --- |
| Remove the 360 newest mask12 cuts; empty outside set | FEASIBLE; one of the removed rays lights the reopened room |
| Each outside set with no cuts | 11 FEASIBLE, 94 INFEASIBLE from geometry and counting alone |

The partition doesn't depend on Codex's cell, fan, or neck hierarchy. The
outside-cell table, the path bound, and the strong model are Claude's own
derivations, checked earlier in this report.

**Status: placements (1,1) and (2,0) remain open.**

Limits:

- The result is still conditional on CP-SAT. Two different models agree, but
  neither produces an UNSAT proof file.
- The zero- and one-exception phases were not re-verified.
- This covers simple rooms in the canonical 45-degree tiling with at most 23
  walls, two full A stars, and three B/C exceptions.

Superseded checks: Codex's type-8 and type-6 requests are steps inside this
exclusion. This whole-placement check covers them, so Claude didn't run them
separately.

## Update 2026-10-30: whole-placement runs at (1,1) and (2,0)

**Result: both placements stay open, matching Codex.** Every room Claude's
model leaves open is lit by a verified ray, so no candidate dark room was
found.

The method is the same as for (2,1). `claude_placement_check.py` now takes
`CLAUDE_TARGET`. Inputs are a snapshot of every `*1-1*.json` and `*2-0*.json`
file in `.context/`, `three-triples/`, and `three-two-star/`, with SHA-256 in
`placement-*/snapshot/snapshot-sha256.json`. Codex hasn't frozen these, so the
rays are checked one by one rather than trusted.

| Placement | Witnesses (all pass) | Cuts | Outside sets | Excluded | Open | Open rooms lit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| (1,1) | 3,632 | 3,379 | 2,530 | 2,484 | 46 | 46 |
| (2,0) | 2,399 | 1,910 | 699 | 680 | 19 | 19 |

Codex's tracer found each ray, and Claude's exact checker verified it. Two
(1,1) rooms needed a wider search, up to direction bound 30, with 19 and 21
bounces. Their outside sets are {(0,2),(0,3)} and {(1,-2),(1,-1)}, which are
mark-exchange partners.

The 65 lit rooms and their paths are in
`placement-{1-1,2-0}/claude-placement-*-traced.json`, and they can serve as
new cuts. Each open set is FEASIBLE after one solve, so adding these cuts and
resolving would likely surface more rooms.

## Update 2026-10-30: (1,1) thin-tip certificate and open-set recheck

Inputs: the 247 files in `thin-tip-pairs-proof-inputs-1-1.json`, copied to
`placement-1-1/cert/run/.context/`. All hashes match.

- Codex `audit_illumination_thin_tip_pairs.py`, rerun: PASS, identical to the
  original apart from timing. It makes no exclusion claim
  (`placement_excluded: false`, residual branch OPTIMAL).
- Claude's collector found 3,664 witnesses in the certificate. All pass, and
  they give 3,411 cuts, the same count Codex reports.
- Recheck of the 46 open outside sets: all 46 stay FEASIBLE with Codex's 3,411
  cuts. They also stay FEASIBLE with Claude's 65 traced rays added, for 3,457
  cuts. The 2,484 excluded sets need no rerun, because adding cuts can't reopen
  them.

Codex's hub, forced-C, and thin-tip work refines (1,1) into cases. Claude's
split by outside-cell set is independent of that hierarchy, and it gives the
progress measure: 46 of 2,530 sets open at (1,1), and 19 of 699 at (2,0).

## Update 2026-10-30: placement (2,0) excluded by Claude's cut loop

**Result: excluded in Claude's model. Codex verification is pending.** With
5,710 verified cuts, every room at (2,0) is lit. **9 of 10 placements are now
excluded; only (1,1) remains open.** Codex runs the ray search at (1,1); this
loop ran at (2,0) at Codex's request.

Method, in `placement-2-0/claude_cut_loop.py`:

1. Start from the 1,910 cuts Claude rebuilt from Codex's (2,0) rays.
2. For each open outside set, solve Claude's strong model.
3. Search for a ray in the returned room with Codex's tracer, which only
   searches, at direction bounds 12 and 30.
4. Check the ray with Claude's exact checker.
5. Add the cut built from the tiles the path touches.
6. Repeat until the set is INFEASIBLE.

Pass 2 also adds each ray's mirror image under y → −y. That reflection fixes
both marks (0,0) and (4,0), and each mirrored path is checked exactly too.

| Step | Result |
| --- | --- |
| Pass 1, at most 300 rounds per set | 1,259 new rays; 17 of 19 open sets INFEASIBLE |
| Pass 2 on {(1,-1)} and {(1,1)}, with mirrors | 1,040 rays; both INFEASIBLE. {(1,1)} needed 0 rounds after the mirrors. |
| Full replay of all 699 outside sets, final cuts | 699 INFEASIBLE |
| Rebuild every cut from scratch, then one monolithic solve | INFEASIBLE (215 s, 5,710 cuts) |
| Control: drop the pass-2 rays | {(1,-1)} is FEASIBLE again, and a dropped ray lights the room |
| Unlit rooms or solver caps during the loop | None |

The tracer found a ray in every room the model produced. No room went unlit at
direction bound 30.

The 2,299 rays, each with its room and exact path, are in
`placement-2-0/claude-rays-2-0.json`.

Limits:

- So far only Claude's model and checker support this. Codex's model hasn't
  replayed it yet.
- The result is still conditional on CP-SAT, with no UNSAT proof file.
- The zero- and one-exception phases were not re-verified.

## Update 2026-10-30: placement (1,1) excluded; all 10 placements excluded

**Result: in Claude's model, every placement of the two-star, three-exception
branch is excluded.** (1,1) and (2,0) were closed by Claude's cut loop; the
other 8 were Codex exclusions that Claude independently confirmed. **Codex
verification of (1,1) and (2,0) is pending.**

Method, in `placement-1-1/claude_cut_loop_11.py`: the same loop as (2,0), with
two changes.

- Rays are reused through all three isometries of the canonical tiling that
  keep the mark pair {(0,0),(2,2)}: (y,x), (2−x,2−y), and (2−y,2−x). Each image
  path is checked exactly in the image room.
- A cut is kept only if its room lies inside Claude's support. Claude also
  rechecked that no (2,0) ray or mirror image leaves the support. None does,
  and the (2,0) support is symmetric under y → −y.

Inputs: a snapshot of all 51 current `*1-1*.json` files, with SHA-256 in
`placement-1-1/snapshot2/`. All 4,240 witnesses pass, giving 3,987 Codex cuts.

| Step | Result |
| --- | --- |
| Loop over the 46 open outside sets | All 46 INFEASIBLE, with 136 new rays. The empty set took 1 round. |
| Unlit rooms or round caps | None |
| Full replay of all 2,530 outside sets | 2,530 INFEASIBLE (4,671 cuts) |
| Rebuild every cut from scratch, then one monolithic solve | INFEASIBLE (22 s) |
| Drop control: Codex cuts only, 5 sets | All 5 FEASIBLE again, and each reopened room is lit by a Claude ray |

The 182 Claude rays at (1,1), each with its room and path, are in
`placement-1-1/claude-rays-1-1.json`.

### Branch status

| Placement | Excluded by | Independent check |
| --- | --- | --- |
| (3,0), (3,1), (3,2), (4,0), (4,1), (5,0), (2,2), (2,1) | Codex | Claude confirmed |
| (2,0), (1,1) | Claude's cut loop | Codex pending |

Scope: simple rooms in the canonical 45-degree tiling with at most 23 walls,
exactly two full A stars, and exactly three B/C exceptions.

Conditions:

- The finite reduction holds. Claude checked it by hand.
- The exact path checker is correct.
- CP-SAT returns correct INFEASIBLE results. No UNSAT proof file exists.
- The zero- and one-exception phases are still not re-verified by Claude.

## Update 2026-10-31: literature review and the 30-60-90 family

See `research-brief.md` for the literature review and the research program.

New result: in the 30-60-90 reflection tiling, the n = 6 case of Wolecki's
Lemma 3.1, no simple Tokarsky room has two interior A points.

| Evidence | Result |
| --- | --- |
| CP-SAT, fixed and free placements, radius 4–5 | INFEASIBLE |
| CP-SAT, maximum tiles with one interior A, radius 3/5/7 | 24 at every radius |
| Exhaustive enumeration, no solver | 416 closed configurations; max 24 tiles; no second full A; never reaches the window edge |
| Same model and enumerator at n = 4 | Reproduces Castro's 24 as the optimum; unbounded growth; finds the two-star configuration |

## 2026-10-31: solver-free 45-degree zero-exception bound, and Codex refolding review

- `tokarsky-n/claude_n4_bound.py 23` branches over every allowed local pattern from a
  full star, pruning when walls exceed 23. It visits 7,871,705 nodes and finds 213,576
  closed configurations, with no second full A and no window hit. The minimum of 24
  for strict simple 45-degree Tokarsky rooms no longer depends on CP-SAT. The WMAX=24
  control finds two-star configurations at 24 walls, 124 of them in the first 10M nodes.
- Codex's refolding gate and lattice obstruction are accepted after an independent
  rebuild. See `refolding/report.md`. Refolding the three known dark surfaces can't
  give a simple room below 24 walls.

## 2026-10-31: exact, complete darkness decision for canonical rooms

`exact-dark/claude_origami_dark.py` decides darkness with no ray bound. The room's
unfolding X is square-tiled, and every source and target lift lies over 0 mod 2Z². So a
connecting segment has primitive direction (p, q) and meets integer points only at
multiples of (p, q). Each integer point is a blocker (cone or ρ-fixed), a target lift, or
transparent. Some γ ∈ SL(2,Z) maps (p, q) to (1, 0). The room is dark exactly when, for
every labelled origami in the finite SL(2,Z) orbit, each source square's horizontal walk
meets a blocker before a target. Shears fix lower-left corners, so labels carry over.

- Validation: 2,435 of 2,435 rooms with verified rays are decided lit. That's 136 at
  (1,1) and 2,299 at (2,0). Each returned word gives a direction. The folded exact path
  passes Claude's checker in every case. Typical runtime is about 0.1 s per room.
- Cost: a dark verdict needs the full orbit. On the 22-wall control, the orbit exceeded
  280,000 surfaces, at about 220 per second, before I stopped it. Use the decider to
  confirm an unlit candidate, not as a filter.
- Consequence: an UNLIT_CANDIDATE from the cut loop is now decidable exactly, either as a
  new dark room or with a lit direction.

## Dark 22-wall polyomino (k=4, placement (2,2))

Credit: Peyton Wang (Daniel's son, 16) leads this investigation; Claude and Codex ran the search and verification.

The k=4 search found a dark simple room with 22 walls: `k4/cand-2_2-1.json`.

- Shape: a 15-cell polyomino with 22 axis-parallel walls, marks (0,0) and (2,2), both interior.
- Transparent points: 4 smooth C points (-1,0), (1,0), (2,1), (2,3). No interior B or C points.
- Exact decider: dark, 2 components, orbit 2,592 each. Dark under both corner conventions: absorb, and 90-degree corners reflect straight back (`CLAUDE_RETRO90=1`).
- Ray sweeps found no lit direction: `fold` up to |p|, |q| <= 40, Codex `find_path` up to bound 60.
- Mechanism: folding across integer lines preserves coordinate parity. A primitive direction first meets an odd-odd or mixed point, and every such point is a corner except the 4 smooth C points.

Literature: Wolecki (arXiv 1905.09358, Theorem 1.3) gives a 22-sided dark room with 45-degree walls, and Monteil reports an unpublished 22-gon. Wolecki's room has a boundary point contact at its central triangle (Codex verified the published SVG on 2026-10-28), so it is not strictly simple. This room is strictly simple: no pinch vertices and no holes, checked from the cell list. The best published strictly simple room has 24 walls (Castro), so this room improves it by 2. It also uses smooth boundary C points, which Tokarsky's criterion does not allow. Rectilinear dark rooms are not new: O'Rourke's forthcoming book (Fig. 9.14, "Orthogonal Tokarsky polygon") shows one with 34 walls by Codex's grid reconstruction. This room improves that count to 22.

Independent verification (2026-10-31): Codex rebuilt the 4-sheet unfolding with its own code and got a closed 2,592-state set; its audit passes (`.context/illumination-k4-codex/closed-orbit-audit.json`). Codex's 2,592 states equal Claude's orbit set exactly for both components, after canonicalization. Claude's export: `k4/cand-2_2-1-orbit-certificate.json`.

The open target is now W <= 21. The k=4 placement runs restarted with WMAX=21 (`k4/run_queue_w21.sh`, logs `k4/log-k4w21-L*.txt`). Partial W <= 23 logs are in `k4/w23-partial/`.

- 2026-10-31: placement (2,2) closed at WMAX=21, no candidates (65,428,331 nodes, 4,065 learned certificates). Placement (2,0) closed at the root earlier. 18 placements remain.

## Literature search (2026-10-31)

Two parallel searches, one academic and one informal, found no public strictly simple dark room under 24 sides, and no public rectilinear dark room with fewer than 28 walls.

- Under 24 sides, every public example is non-simple or uses boundary points:
  - 18 walls + post, 20 slit, 22 hole/point contact (Tokarsky 1996)
  - Wolecki 22 (pinch)
  - Double Star 20 (hole)
  - 3-, 4- and 12-sided rooms with boundary dark points
- Rectilinear:
  - Tokarsky 1995 square-cell room, 34 walls, interior pair. It is in Abel's 2012 blog post and is likely O'Rourke Fig. 9.14.
  - Tokarsky's "Spider's home" (YouTube, 2024), 28 walls, center against boundary midpoints.
- Method: Tokarsky's square rule (every B, C, D point a corner makes A points dark) is public. This room breaks that rule at 4 smooth C points, so its darkness needs the full orbit proof.
- Quanta (Feb. 2024 correction): smallest known has 22 sides (Wolecki); smaller is open.
- Not reached:
  - Tokarsky & Boese, Math. Mag. 73(5) 2000 (paywalled). This is the most likely place a prior square-cell room would appear.
  - Castro's Quantum note
  - Monteil's unpublished 22-gon
  - Non-English Wikipedia articles
- 2026-10-31: placement (4,0) closed at WMAX=21 with persistence, no candidates (521,918,121 nodes, 4,352 learned). Closed so far: (2,0), (2,2), (4,0). 17 remain.
- 2026-10-31: placement (4,2) closed at WMAX=21, no candidates (1,508,351,132 nodes, 3,164 learned). Closed: (2,0), (2,2), (4,0), (4,2). 16 remain.
- 2026-10-31: placement (6,6) closed at WMAX=21, no candidates (3,243,090,546 nodes; every closed leaf non-simple, 0 learned). Closed: (2,0), (2,2), (4,0), (4,2), (6,6). 15 remain.
- 2026-10-31: placement (6,0) closed at WMAX=21, no candidates (2,997,314,251 nodes, 19 learned). Closed: (2,0), (2,2), (4,0), (4,2), (6,0), (6,6). 14 remain.
- 2026-10-31: placement (6,2) closed at WMAX=21, no candidates (3,109,356,734 nodes, 54 learned). Closed: (2,0), (2,2), (4,0), (4,2), (6,0), (6,2), (6,6). 13 remain.
- 2026-10-31: placement (6,4) closed at WMAX=21, no candidates (3,223,424,839 nodes, 0 learned). Closed: (2,0), (2,2), (4,0), (4,2), (6,0), (6,2), (6,4), (6,6). 12 remain.
- 2026-10-31: placement (8,0) closed at WMAX=21, no candidates (3,241,636,653 nodes, 0 learned). Closed: 9 of 20. 11 remain.
- 2026-10-31: placement (4,4) closed at WMAX=21, no candidates (2,846,619,563 nodes, 1,025 learned). Closed: 10 of 20. 10 remain.
- 2026-10-31: placement (8,2) closed at WMAX=21, no candidates (3,241,960,163 nodes, 0 learned). Closed: 11 of 20. 9 remain.
- 2026-10-31: placement (8,4) closed at WMAX=21, no candidates (3,242,999,969 nodes, 0 learned). Closed: 12 of 20. 8 remain.
- 2026-10-31: placement (8,8) closed at WMAX=21, no candidates (3,243,285,466 nodes, 0 learned). Closed: 13 of 20. 7 remain.
- 2026-10-31: placement (8,6) closed at WMAX=21, no candidates (3,243,285,446 nodes, 0 learned). Closed: 14 of 20. 6 remain.
- 2026-10-31: placement (10,0) closed at WMAX=21, no candidates (3,243,285,466 nodes, 0 learned). Closed: 15 of 20. 5 remain.
- 2026-10-31: placement (10,2) closed at WMAX=21, no candidates (3,243,285,466 nodes, 0 learned). Closed: 16 of 20. 4 remain.
- 2026-10-31: placement (10,4) closed at WMAX=21, no candidates (3,243,285,466 nodes, 0 learned). Closed: 17 of 20. 3 remain.
- 2026-10-31: placement (10,6) closed at WMAX=21, no candidates (3,243,285,466 nodes, 0 learned). Closed: 18 of 20. Remaining: (12,0), (12,2).
- 2026-10-31: placement (12,0) closed at WMAX=21, no candidates (3,243,285,466 nodes, 0 learned). Closed: 19 of 20. Remaining: (12,2).

### k=4, W <= 21: complete (2026-10-31)

All 20 placements are closed with no dark candidate. The 19 runs (`k4/log-k4w21-L*.txt`) all ended `exit 0`. Placement (2,0) closes at the root: the direct segment is forced. Run arguments: K=4, WMAX=21, NMAX=38, IMAX=3.

Scope: simple canonical 45-degree rooms with interior A marks, exactly 4 transparent exceptions, and I <= 3. Every exclusion uses a saved certificate: `k4/certs-paths-*.json` holds the precomputed ones and `k4/claude-k4-w21-learned-*.jsonl` the learned ones. Combined with the earlier 0-3 exception results, no simple room in this family with at most 4 exceptions has 21 walls or fewer. That makes the 22-wall room minimal within that scope.

Open:
- Codex replay audit of the saved certificates.
- k >= 5 exceptions.
- I > 3.
- Rooms outside the canonical 45-degree tiling.
