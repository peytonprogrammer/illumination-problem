# D92: review of mirror-suborbit.md (snapshot)

Date: 2026-11-20. Reviewer: independent referee. Reviewed file: `mirror-suborbit.snapshot.md`, SHA-256 prefix `28c74baf` (checked before and after review).

## Verdicts

| Claim | Verdict | Reason |
| --- | --- | --- |
| 1. 2e(S) ≤ B(r)(B(r)−1) for a mark with a dark partner | Sound | G preserves Q's corner set automatically, so G_s maps dark targets to dark targets. Both shared neighbours are distinct. The walk count is injective. Exact R22 data satisfies it (4 ≤ 6). |
| 2. e(S) ≥ max(u,v)/gcd(u,v) | Sound | Pure group theory. It held for every map tested. Small-word parabolics give ratio ≤ 2 in the cross, but some non-parabolic F attains the exact e(S) = 44. |
| 3. Growth of a stabilizer orbit of the actual pair | Sound, but adds little | 2 max(e) ≤ 4M(4M−1) is correct. Under darkness M ≤ B already holds directly, so this gives no new route to a cutoff. |
| 4. Axis marks have mirror orbit ≤ 4 (exhaustion open) | Sound, minor slack | G_s·ιs ⊆ Ks∖{s}, so the bound is 3. Confirmed in the cross. Diagonal-axis marks are not bounded (e = 44 at (1,1), b = 7). |
| Finiteness remark | Fixable gap | The stated reason (absolute periods in 2Z²) is not the operative one. Affine maps preserve the *relative* period lattice Z² of a normalized room, so they permute lattice points. |

## Claim 1

**Does G_s preserve darkness?** On Q every corner is a cone point: convex corners have angle π, reflex corners 3π, and every other point 2π. An orientation-preserving affine map preserves cone angles. So "preserving the corners" is automatic, and G maps legal Q segments to legal Q segments. Hidden pairs map to hidden pairs. This also holds on M with the convex lifts kept as marks, which the computation enforces explicitly.

**Two shared targets.** For s′ = gιs with g ∈ G_s, g maps the seed edges (ιs,t), (ιs,ιt) to (s′,gt), (s′,gιt). It maps (s,t), (s,ιt) to (s,gt), (s,gιt). For interior T, t ≠ ιt, so gt ≠ gιt. Also s′ ≠ s, since otherwise ιs = s. The physical partner's two lifts are exactly what provides the two shared neighbours. The claim is right.

**Injectivity.** A length-two walk s → w → x determines its endpoint x. Distinct endpoints s′ therefore own disjoint sets of at least two walks each. There are at most B choices of w and at most B − 1 choices of x ≠ s for each w. So 2e(S) ≤ B(B−1). Every right vertex w is a lift of a regular physical point, so B applies with w as the source.

**R22 test** ([r22.log](r22.log)). S = (0,0), T = (2,2), 22 walls (13 convex, 9 reflex), area 15.

- SL(2,Z)-orbit of the marked M: 144. |K| = 1.
- Hidden Q lattice points from s, over all primitive directions of length ≤ 30: {t, ιt, (2,−2)}, where (2,−2) is a smooth wall point. From t: {s, ιs, (4,0)}.
- G_s·t = G_s·ιt = {t, ιt, (2,−2)}. This is exactly the hidden set. The affine group alone shows (2,−2) is hidden once T is dark. That's an independent confirmation of the d85 observation.
- e(S) = 2, with G_s·ιs = {ιs, (4,0) wall lift}. e(T) = 2. The other lift gives the same values.
- Exact graph: 6 + 6 vertices, 18 edges, all degrees 3. Walks from s: 6. 2e(S) = 4 ≤ 3·2 = 6. The inequality holds with the actual hidden count in place of B.

## Claim 2

F^u ∈ G_s, and its cycle on ιs has length v/gcd(u,v). Symmetrically F*^v gives u/gcd(u,v). The identity period_F(ιs) = period_{F*}(s) was asserted for every case in the logs and passed.

Cross b = 7 ([cross7.log](cross7.log), [sub7.log](sub7.log), [scan7.log](scan7.log)):

- Parabolics in 7 short-word directions give ratio ≤ 2 at every mark. The group they generate with K has orbits of size ≤ 8 and e_H ≤ 2.
- Over all 5861 distinct Schreier-generator maps, the best single-F ratio equals the exact e(S) at (5,1), (3,1) and (1,1): 44, attained with (u,v) = (44,1). At (6,1) it reaches 20 against e = 40.
- So the certificate is valid and can be sharp, but it needs non-parabolic F. The note's parabolic cylinder formula alone does not see it.

## Claim 3

The degree bound 4M is correct. Each seed-edge orbit contributes |G_a·b| neighbours at a vertex in G·a, and these sizes are conjugation-invariant. Under darkness, though, G_s·t lies in H(s) and so |G_s·t| ≤ B directly. Claim 3 restates that bridge rather than adding to it. In R22, M = 3 and 4 ≤ 12·11.

## Claim 4

If ιs = ks with k ∈ K, then g ιs = (gkg⁻¹)s ∈ Ks for g ∈ G_s. Since ιs ≠ s, the bound is |K| − 1 ≤ 3, not 4.

Exact values in the cross, b = 7 (|K| = 4):

| Mark | Position | e(S) |
| --- | --- | --- |
| (6,0), (0,6) | on the y-axis or x-axis | 2 |
| (1,0) | on an axis | 1 |
| (0,0) | centre | 1 |
| (5,1), (3,1) | off all axes | 44 |
| (1,1) | diagonal only | 44 |
| (6,1), (4,1), (2,1) | off all axes | 40 |

The diagonal reflection lifts with derivative a quarter-turn, outside K, so it gives no bound. That matches the note's restriction to horizontal and vertical axes. In R22 (no symmetry) the dark marks have e = 2. A fixed room is finite, so "bounded" only has meaning along families. The exhaustion question stays open.

The cross numbers match the parallel d91 computation independently: orbit index 12672, |G·(6,0)| = 40, |G·(5,1)| = 48.

## Effectivity

B(r) has no value, so the theorem gives no area cutoff and no finite census. Its strongest form is this: for fixed r, a family in which **every** mark's e(S) tends to infinity is eventually lit, at an unknown size. Even that needs a growth theorem for e(S) that the note doesn't have. Axis marks always have e ≤ 3, so they need a separate argument in every symmetric family. For the 22-wall goal it buys nothing numerical. It can't certify any specific room, and it can't bound the rooms left to search.

## Method and limits

- `surf.py` builds M as an origami with τ, marks and corner-vertex classes. It enumerates the SL(2,Z)-orbit of the marked, τ-equipped surface, using cycle invariants and explicit isomorphism search. It turns each Schreier generator into a vertex map, adds Aut, and checks that every map preserves corners and commutes with τ. G_s·ιs is read off the G-orbit of the pair (s, ιs) on Q.
- `run.py` handles marks, parabolics, F* = ιFι, hidden sets and the claim-1 graph. `sub.py` gives subgroup lower bounds. `scan.py` gives the single-F ratios.
- Cross b = 9: exact G was not run, because the index is 34560 per d91 and it would exceed the CPU budget. [sub9.log](sub9.log) gives subgroup lower bounds only. Axis marks there have e ≤ 3 by claim 4.
- The R22 hidden set comes from a direction sweep of length ≤ 30, which is an upper bound. The G_s-orbit gives the matching lower bound, assuming T is dark.

Re-run: `python3 -B run.py r22; python3 -B run.py cross7; python3 -B sub.py 7; python3 -B sub.py 9; python3 -B scan.py`. Total CPU is about 320 s. Exact integer arithmetic, named rooms only, no web access.
