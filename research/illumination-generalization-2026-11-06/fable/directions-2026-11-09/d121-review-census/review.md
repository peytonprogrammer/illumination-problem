# D121: review of the z ≤ 2 full-family exclusion

Date: 2026-11-20. Reviewer: independent verifier, one session, no network.

Question: is the "full-family exclusion" for minimal quadratic quotients with
z ≤ 2 zeros established? The d119 review (item 2c) found that it rests on the
final section of the d19–23 review, which one unreviewed reader wrote.

Read: d19–23 `review.md`, `counts_z2.py`, `slice.py`; d20 `periodic.md`; the
d21, d22 and d23 READMEs and scripts; d119 `review.md` and its snapshot of
`minimal-quotient-rigidity.md`; RESULTS §11 "Minimal quotient".

## Answer

**Established, with fixable gaps.** The logic is sound, and every saved
census verdict that fit the budget reproduces exactly. The one gap that keeps
it short of a full proof is that the LIT verdicts come from one
implementation. Independent code has checked only the (k, z) = (4, 1) slice.

Two findings shrink the dependency list:

1. **d23 Lemma 2 is correct, and the minimal-quotient note doesn't need it.**
   In that note, all four lifts s±, t± are regular periodic points, so each
   is an e = 2 point of f: Q → Y. That needs c₂ ≥ 4. All 300 members of the
   three dark families have exactly c₂ = 2 (replayed). Counting alone
   excludes them, as d119 gap 2c-2 already does for k = 2.
2. **Darkness of the three families is not an input.** The exclusion needs
   only "every other P1 and P2 family has a lit member". So d22 Lemma A, the
   d21 arc proof and the d19–23 wall-point addition aren't used. They prove
   that the three families *are* dark, which the exclusion doesn't need.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1a | d23 Lemma 1: a shared ramification point determines a 2-transitive cover | Correct, with the cone-angle hypothesis that d19–23 added |
| 1b | d23 Lemma 2: f∘ρ = σ∘f when ρ fixes a ramification point | Correct |
| 1c | Lemma 2 excludes each of the three families for interior marks | Correct for all three (A₄, A₅, S₅) |
| 1d | Lemma 2 is needed in the minimal-quotient application | No. The count c₂ ≥ 4 against c₂ = 2 suffices |
| 2a | Enumeration covers every (k, z) with z ≤ 2 allowed by Riemann–Hurwitz at r ≤ 8 | Complete: z = 1 with k ≤ 8, z = 2 with k ≤ 4, t ≤ 8 − kz |
| 2b | Every P1 and P2 family has a tested node | Yes. z = 1 P2 uses braid transitivity on pole positions. z ≥ 2 has no grouping, see gap M1 |
| 2c | Verdicts follow: only the three families lack a lit member | Follows, given LIT soundness (gap H1) |
| 3 | Replays match saved results | 20 runs, every verdict identical (table below) |
| 4 | z ≤ 2 exclusion | Established, with fixable gaps |

## 1. d23 Lemmas 1 and 2

### Lemma 1

Statement: f: X → Y and g: X → Y′ are half-translation covers with
2-transitive monodromy. They share a ramification point Z. Then g = φ∘f for a
half-translation isomorphism φ.

Proof check, step by step:

1. Over the unbranched locus, X ×_Y X minus the diagonal is a covering whose
   components match the monodromy orbits on ordered pairs of distinct sheets.
   2-transitivity gives one orbit, so the closure C_f is irreducible. Correct.
2. Let Z have cone angle mπ. The local automorphisms of q_X fixing Z form a
   cyclic group of order m. A ramification point over a pole has local degree
   e = m. So the local deck group is the whole local automorphism group, and
   it doesn't depend on f. This needs e = m, which holds when every cone
   angle is π, 2π or 3π. That is the d19–23 correction, and it's right. At
   6π, degrees 2 and 3 give different subgroups.
3. The germ {(x, τx)} lies in C_f and C_g. Two irreducible analytic curves
   that share a germ are equal. So f and g have the same fibres. The induced
   map φ is a homeomorphism, because f is a closed quotient map. It's a local
   isometry off finitely many points. Correct.

### Lemma 2

Put g = c∘f∘ρ, with c the identity onto the mirror surface. Then g is a
half-translation cover with conjugate monodromy, so it's 2-transitive. g is
ramified at Z because ρ(Z) = Z. Lemma 1 gives g = φ∘f. Then σ = c⁻¹∘φ
satisfies f∘ρ = σ∘f. Also σ²∘f = f∘ρ² = f, and f is onto, so σ² = 1.
Correct.

### Application to the three families

Hypotheses, checked for each family:

| Family | k | Group | 2-transitive | 3-cycle over a pole | c₂ per member |
| --- | --- | --- | --- | --- | --- |
| P1, A₄ | 4 | order 12 | Yes, all 30 members | Yes | 2 |
| P1, A₅ | 5 | order 60 | Yes, all 240 members | Yes | 2 |
| P2, S₅ | 5 | order 120 | Yes, all 30 members | Yes | 2 |

Source: `d23.py groups`, replayed here (`logs/d23_groups.log`). A 3-cycle
over a pole gives a zero of X = D(P). Zeros are reflex corners, and ρ fixes
the boundary pointwise. So Lemma 2 applies.

Conclusion: R(f) is ρ-invariant and has two points. Either both are ρ-fixed,
so both are wall points, or ρ swaps them, so they're the two lifts of one
point. A pair of distinct room points with at least one interior point
can't be R(f). This excludes all three families for interior marks. It also
excludes one wall point plus one interior point.

### The shorter route in the minimal-quotient note

The note's setting (d119 §2a, §2c step 4) makes s+, s−, t+ and t− distinct
regular periodic points. Each maps to a pole with e = 2. So the full family
containing (Q; s+, t+) has c₂ ≥ 4. The three dark families have c₂ = 2.
They can't occur, with no use of Lemma 2, the reflection, or Lemma 1.

This route depends on individual periodicity of all four lifts. d119 rated
that "sound with fixable gaps (low)". Lemma 2 stays as a second proof, which
doesn't need periodicity of s− and t−.

## 2. Census logic

### What the exclusion needs

The dark set is closed (d19) and GL(2, ℝ)-invariant. If (Q; s+, t+) is dark,
its orbit closure, the full family F, is dark at every member. So one lit
member of F contradicts darkness. The exclusion therefore needs three facts:

1. Every P1 and P2 family over Q(1^z, −1^(z+4)), z ≤ 2, r ≤ 8, has a tested
   node.
2. Every LIT verdict is a real segment that avoids the singularities.
3. Each family with no LIT node is excluded by c₂ or by Lemma 2.

DARK verdicts, CAP verdicts and Lemma A play no part.

### Enumeration

- **Strata.** A cover branches only over poles, with cycle lengths at most 3.
  X = D(P) is a sphere, so the index sum is 2k − 2. Then r = kz + t with
  r ≤ 8. That gives z = 1 with 2 ≤ k ≤ 8, and z = 2 with 2 ≤ k ≤ 4. Both
  censuses cover exactly these, with cap t ≤ 8 − kz.
- **z = 2.** `d22.brute` takes all 5-tuples of allowed permutations and sets
  the sixth to the inverse product. It filters on type, index sum, t and
  transitivity, then reduces up to conjugation. That is complete. Counts
  15, 135 and 680 match the independent `counts_z2.py`.
- **z = 1.** The d21 census enumerates seeds for one ordering of each type
  multiset, then closes under braid moves. Every braid orbit meets every
  ordering, so this is complete if the seed list is complete. The mass check
  confirms seed completeness, for all orderings at k ≤ 5 and for the seed
  ordering at k ≥ 6. It returned `true` again on replay. The k = 4 count
  (665) matches `slice.py`. No independent count exists at k = 5 to 8 (gap L3).
- **Nodes.** A P1 node is two 2-cycles over one pole. A P2 node is two
  2-cycles over different poles. Families are braid orbits of nodes.

### Verdicts, by (k, z)

The census is needed only at k ≥ 3, because k = 2 has c₂ = 2 < 4.

| (k, z) | P1 source | P2 source | Families without a lit node |
| --- | --- | --- | --- |
| (3, 1) | No P1 nodes | bipole stage 2 | 0 |
| (4, 1) | `exh 4`, `z1 4`, `slice.py` | bipole stage 2 | P1 A₄ |
| (5, 1) | `z1 5` (grouped); `exh 5` saved only | bipole stage 2 | P1 A₅, P2 S₅ |
| (6, 1) | `exh 6 P1`, `z1 6` | bipole stage 2 | 0 |
| (7, 1) | `z1 7` (grouped); `exh 7 P1` saved only | bipole stage 2 | 0 |
| (8, 1) | `z1 8` (grouped); `exh 8 P1` saved only | bipole stage 2 | 0 |
| (3, 2) | No P1 nodes | `small` | 0 |
| (4, 2) | `small` | `small` | 0 |

- **z = 1, P2.** Stage 2 tests every cover of the tromino double and every
  pair over poles 3 and 4. Braid moves act on pole positions through all of
  S₅, so every family has such a node. Nodes dark on L(2,2) were retested
  with the same tuple on L(3,2): 1 at k = 4, 32 at k = 6, 660 at k = 8, all
  lit. That transfer is valid because L(A, B) deforms continuously with fixed
  combinatorics (gap L2).
- **z = 2.** `small` tests each node on room 0 and then on rooms 1 and 2.
  Rooms 1 and 2 have different shapes, so the same tuple there may be a
  different family. The code doesn't argue the identification (gap M1). I
  grouped the saved node set into braid families with `family_check_small.py`.
  It reuses the same covers, room 0 and tracer depth 8. Every family has a
  node lit on room 0. So the verdicts stand without rooms 1 and 2.

| (k, z) | Kind | Node classes | Families | Families with no room-0 lit node |
| --- | --- | --- | --- | --- |
| (2, 2) | P2 | 15 | 1 | 0 |
| (3, 2) | P2 | 420 | 2 | 0 |
| (4, 2) | P1 | 780 | 3 | 0 |
| (4, 2) | P2 | 8,160 | 7 | 0 |
| (2, 3) | P2 | 21 | 1 | 0 |
| (2, 4) | P2 | 28 | 1 | 0 |

Node classes are counted up to cover automorphisms, so (4, 2) P2 shows 8,160
rather than d22's 9,420.

## 3. Replays

All runs used `python3 -B` on byte-identical copies in `replay/` (hashes in
`replay/sha256_sources.txt`). Original directories weren't touched. Outputs
are in `logs/` and `replay/*/result_*.json`. `compare.py` diffs each result
against the saved file, ignoring timing keys (`logs/compare.log`).

| Run | CPU s | Saved result | Verdicts |
| --- | --- | --- | --- |
| `slice.py` (independent code, (4, 1)) | 8.0 | d19–23 review text | Match: 665 covers, 8 orbits, 420 P1 in 5 families, 30 unlit = Lemma A set, 0 of 3,990 P3 unlit |
| `counts_z2.py` | 5.2 | d19–23 review text, d22 table | Match: 15, 135, 680, 21, 28 covers; 780 P1; 15, 420, 9,420, 21, 28 P2 |
| `d22.py small` | 3.6 | `result_small.json` | Identical |
| `d22.py z1 2`, `3`, `4` | 3.6 | `result_z1_d2–4.json` | Identical counts and statuses. Saved file keeps 6 sample members per unlit family, the current script keeps 3; samples agree |
| `d22.py z1 5` | 21.1 | `result_z1_d5.json` | Identical counts and statuses; the A₅ family is the only unlit P1 family. Saved run used cap 400,000 on L(3,4), current script 150,000; CAP both times |
| `d22.py z1 6`, `7`, `8` | 50.4 | `result_z1_d6–8.json` | Identical |
| `d22.py exh 4` | 1.8 | `result_exh_d4.json` | Identical: 30 dark P1 nodes, 0 dark P3. Replay adds `covers` keys only |
| `d22.py exh 6 P1` | 73.6 | `result_exh_d6_P1.json` | Identical: 0 dark of 198,780 |
| `bipole.py 2` to `5` | 51.0 | `result_d2–5.json` | Identical. Replay adds the keys `dark_nodes_other_bases`, `dark_on_all_bases`. At k = 5 the 3 dark nodes are S₅-family nodes, unlit on all 4 bases |
| `bipole.py 6` | 27.7 | `result_d6.json` | Identical |
| `bipole.py 7` | 148.0 | `result_d7.json` | Identical (new keys only) |
| `bipole.py 8` | 114.0 | `result_d8.json` | Identical |
| `d23.py groups` | 0.1 | `result_groups.json` | Identical |
| `family_check_small.py` (new grouping, no new search) | 2.0 | none | Table in §2 |

Total: about 510 CPU-seconds.

**Not replayed, over budget:** `d22.py exh 5` (519 s saved), `exh 7 P1`
(268 s), `exh 8 P1` (207 s), d21 `checks.py`, and d23 `validate`, `invol`
and `run` (about 19 minutes). The family-grouped `z1` route covers the same
P1 verdicts at k = 5, 7, 8. The d23 runs don't bear on the exclusion.

Replays show that the saved files come from these scripts. They don't show
the scripts are correct. Only `slice.py` is independent code.

## 4. Gaps, ranked

| Rank | Gap | Fix |
| --- | --- | --- |
| High | H1: LIT soundness rests on one implementation (d22 `Cx.visible`, the d21 edge test and pillowcase decider). Independent code checked only (4, 1), plus d21's saved tracer comparison at k = 4, 5. No LIT witness is stored. | Make the scripts emit one witness segment per family: tuple, base, start sheet, (p, q). Verify each with code like `slice.py`'s `fly`. That is a certificate check, not a search. It needs about 430 witnesses: 137 lit z = 1 P1 families, 276 lit z = 1 P2 families, and 13 z = 2 families. |
| Medium | M1: d22 `small` credits a node lit on rooms 1 or 2 without showing that the tuple there lies in the same family. | Closed by `family_check_small.py`: every family has a room-0 lit node. Add this check to d22 and cite it. |
| Medium | M2: d119 and RESULTS list d22 Lemma A, the d21 arc proof, the wall-point addition and d23 Lemma 2 as inputs. The exclusion uses none of the first three. With all four lifts periodic, it doesn't need Lemma 2 either. | Restate the inputs: census enumeration, LIT verdicts, and c₂ = 2 for the three families. Keep Lemma 2 as an alternative route. |
| Low | L1: d23 Lemma 1 lacks the hypothesis "every cone angle is π, 2π or 3π". | Add it to the statement, as d19–23 said. |
| Low | L2: the transfer of a tuple from L(2,2) to L(3,2) or L(2,3) is asserted, not argued. | Add one sentence: L(A, B) varies continuously with fixed corner order and start pole, so the boundary basis transports. |
| Low | L3: cover counts at z = 1, k = 5 to 8 have no independent check; the mass check covers seed orderings only at k ≥ 6. | Compare with the Frobenius character formula for the number of tuples of given cycle types. |
| Low | L4: saved results come from earlier script versions (sample size 6 against 3, cap 400,000 against 150,000, missing keys). | Re-save with the current scripts, or record script hashes next to each result. |
| Low | L5: P1 at k = 5, 7, 8 was replayed only through family grouping, which uses d22's point-tracking map. | Replay `exh 5`, `exh 7 P1` and `exh 8 P1` (about 17 CPU-minutes), or cite the saved runs as the tracking-free control. |

## 5. What is missing for "established"

1. An independent check of the LIT witnesses for the (k, z) slices other
   than (4, 1) (H1).
2. The rewritten dependency statement in the minimal-quotient note and
   RESULTS (M2), with the room-0 family check cited (M1).

Everything else is wording.

## Files

- `review.md`: this file.
- `family_check_small.py`, `family_check_small.json`: z ≥ 2 family grouping.
- `compare.py`: diff of replayed against saved results.
- `logs/`: stdout, timing and comparison logs for every run.
- `replay/`: script copies and the result files they wrote.

Re-run, from this directory:

```
cd replay && python3 -B d22-structured/d22.py small   # likewise z1 D, exh D, bipole.py D 1000
cd .. && python3 -B family_check_small.py && python3 -B compare.py
```
