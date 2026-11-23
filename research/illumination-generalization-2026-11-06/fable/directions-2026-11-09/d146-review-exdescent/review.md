# d146: referee report on exclusion-descent (snapshot 2026-11-22 02:40)

Reviewed file: `../d95-review-queue/snapshots/exclusion-descent.2026-11-22-0240.md`. Context read: `qclass-closure/bbbb/canonical-transfer.md`, `chain-map.md`, the bbbb README, the d69 README and `decomp.py` room constructors, and the d144 and d145 reviews.

Code: [checks.py](checks.py), log [checks.log](checks.log), 0.07 CPU-seconds. The script uses exact integer and Fraction arithmetic. It builds 6 named rooms and runs no search and no network call. Its monodromy model is new code. Each room double is a set of squares (x, y, copy), and four edge-crossing involutions τ_L, τ_R, τ_Bo, τ_T act on them. The site monodromies are g_ij = τ_{V_i}τ_{H_j} on the n front squares. The relation g00·g10⁻¹·g11·g01⁻¹ = id holds upstairs and on the quotient.

## Verdict

**Sound with gaps.** Every computational claim about cov4181 checks exactly. The four-sheet exclusion argument is correct and in fact proves a stronger, corner-blind statement. The BBBB lemma (4) is correct under the project's definition of BBBB: all four canonical relations B_x are universal. It's false as an inference under the weaker gloss "no corner-only site", and the note doesn't state which definition it uses. Claims (3) and the isogeny half of (4) restate bounds already in `canonical-transfer.md`.

## Check 1: cov4181's quotients

The cell list matches `qclass-closure/offgrid/cov4181.room`. The room has n = 28, W = 20 and r = 8, and both axis gcds are 1, so it's normalized.

| Site (parity) | Upstairs cycle type | B_x | N cycle type | N permutation |
|---|---|---|---|---|
| a (0,1) | 3¹ 2¹² 1¹ | universal | (2,1,1) | (01) |
| b (1,1) | 2¹⁴ | universal | (2,2) | (01)(23) |
| c (1,0) | 3⁷ 1⁷ | none (no 2-cycles) | (3,1) | (132) |
| d (0,0) | 2¹² 1⁴ | universal | (2,1,1) | (12) |

- The monodromy group has exactly 2 block systems besides the discrete one: degrees 1 and 4 over B. So N, with 4 blocks of 7 sheets, is the unique proper quotient. This matches the note's degrees 1, 4 and 28.
- The labelling matches the note letter for letter. (132) equals the note's (123) inverted, which is the same cycle type.
- S = (2,3) and T = (4,3) are interior. Both Q-points of S map to letter 3, which A and D both fix. Both Q-points of T map to letter 2, which A fixes and D moves.
- N has a 2-cycle over d, and closing all 12 upstairs d-transpositions gives the universal partition. So the "relevant-site" assertion fails, as stated.
- Over c, N has one zero and one pole and no regular point. The corner-only site is c.

## Check 2: arc separation

**S₄ lemma.** The script tests all 4-tuples of types (2,1,1), (2,2), (3,1), (2,1,1) in S₄ whose product is the identity, in all 24 orders. It finds 1,728 solutions. In every one, the supports of A and D meet in exactly one letter. The note's proof through the action on the 3 pairings, with kernel V₄, is correct. So, for any simple a-to-d arc, the preimage graph in N has components {x,y,z} and {w}, and the two A-singletons z and w are separated.

**Concrete graphs.** For the edge arc L of direction (0,1), the preimage components in Q are the orbits of ⟨g_a, g_d⟩. There are 5, of sizes 3, 3, 4, 6 and 12. S and T lie in different ones. In N the orbits of ⟨A, D⟩ are {0,1,2} and {3}. For 9 more arcs with p even and q odd, the script traces every billiard segment from each parity-a point to its first lattice point. The arcs are (2,1), (2,−1), (2,3), (4,1), (4,−3), (2,5), (6,1), (8,3) and (10,−7). Each graph has exactly 28 edges, and in each one the S-lifts and T-lifts lie in different components.

**Does it explain the orbit exclusion?** Yes, and it proves more. The image of any class-(0,1) trajectory in N is a connected subset of the preimage of one arc. This holds for every continuation choice at corners. So the argument excludes relaxed routes too, consistent with the note's empty relaxed family and with d144's dark verdict over 3,888 orbit states. The exclusion is visible already in Q's arc graph. N gives a 4-letter certificate that doesn't depend on the slope.

## Check 3: the 7-reflex charge

The N-zero over c lifts to 7 upstairs 3-cycles. These are exactly the 7 parity-c reflexes (1,2), (1,4), (3,2), (3,4), (5,2), (5,4) and (7,2). The N-pole lifts to 7 fixed points, the 7 convex corners. So r ≥ k = 7 = n/4, and W = 20 ≥ n/2 + 4 = 18. The "extra cost zero" is correct but trivial: c is corner-only, so every parity-c reflex is already counted. The general r ≥ n/4 is correct for outer degree 4 with one zero.

## Check 4: BBBB has no factor of outer degree 2, 3 or 4

**Proof.** The proof is correct, given its definition, in 4 steps:

1. By `canonical-transfer.md` (1)⇔(3), a proper N with no regular point over x forces B_x to refine Π. So B_x isn't universal.
2. Under the canonical definition of BBBB, every site of N has a 2-cycle.
3. Quotient cycle lengths are at most 3. With at most 4 letters, a site can't carry both a 2-cycle and a 3-cycle, so N has no zeros.
4. Q is a sphere, so N is a sphere with 4 poles. Its orienting torus T_N satisfies 2ℤ² = Per(X) ⊆ Λ_N ⊆ 2ℤ², with index equal to the outer degree. So the outer degree is 1.

**Named rooms.** The script tests 5 named normalized rooms. It confirms they're BBBB in the canonical sense, with all four B_x universal.

| Room | n | r | W | Proper pillowcase factors (outer degree) |
|---|---:|---:|---:|---|
| DB55 (dumbbell) | 53 | 4 | 12 | none |
| DBas (dumbbell) | 48 | 4 | 12 | none |
| U2 | 46 | 3 | 10 | none |
| c4181s (stretched cov4181) | 41 | 8 | 20 | none |
| odd cross b = 7 | 96 | 4 | 12 | 24 (inner 4) and three of degree 48 (inner 2) |

None of these rooms has a factor of outer degree 2 to 4. The cross gives the informative case. Its 4 proper factors each have zeros, with poles − zeros = 4. Each has a site, (0,0), that carries both 2-cycles and 3-cycles, which is exactly what degree ≤ 4 forbids. This confirms canonical-transfer's claim of a degree-4 inner quotient Q/K.

## Gaps

1. **Medium: the definition of BBBB is left implicit, and the weaker gloss breaks step 2 of (4).** The proof needs every B_x to be universal. "No corner-only site" doesn't give that. A Q regular point can map to an N pole, so a quotient can be clean over x when Q isn't. The sentence "It cannot occur in BBBB, since its proper quotient is clean over c" needs the canonical definition too. To fix this, state the definition and cite `canonical-transfer.md` (1)⇔(3).
2. **Low: (3) and the isogeny step aren't new.** `canonical-transfer.md` already states "each zero consumes k distinct reflex preimages, so kz ≤ r". It also states that corrected normalization excludes intermediate pillowcases. For a corner-only c, r ≥ n/4 is within 1 of the Q-class bound n ≤ 4r + 4, so the "indirect cost" adds nothing beyond it. The new content of (4) is the single counting step "≤ 4 letters means no mixed 2-and-3 site".
3. **Low: the theorem's hypothesis on endpoint positions is stated per room, not derived.** The four-sheet theorem needs both endpoint orbits to map to the two A-singletons. For cov4181 this is verified, but nothing says when it holds in other rooms. If the endpoints map into the 2-cycle of A, the argument gives nothing.
4. **Low: degree 2 is vacuous.** For a sphere, a 2-cycle at all 4 sites already violates Riemann–Hurwitz, since the total ramification would be 4 > 2·2 − 2 = 2. The text treats degree 2 through the torus argument. That's harmless but redundant.
5. **Low: "k sheets above the c-zero" should read "k points".** These are 7 distinct 3-cycles, not 7 sheets. There are 21 sheets.

## Scope

**Proved:**

- cov4181's (0,1) exclusion, for all slopes, even with any continuation at corners, through the unique 4-sheet quotient.
- A general four-sheet exclusion theorem, under its stated cycle types and endpoint hypothesis.
- No proper pillowcase factor of outer degree 2, 3 or 4 in a normalized room with all B_x universal.

**Open, at degree ≥ 5:**

- In a BBBB room, every proper factor has z ≥ 1 zeros, each at a mixed site. So kz ≤ r and n ≤ (outer degree)·r.
- Degree 5 isn't excluded by counting. Types (3,2), (2,2,1), (2,2,1), (2,1,1,1) give total ramification 8 = 2·5 − 2, with 1 zero and 5 poles. At r ≤ 8 that means n = 5k ≤ 40.
- The named cross shows that BBBB rooms do have proper factors at degree 24 and 48. So the proper-factor branch inside BBBB isn't empty.
- Whether a 2-singleton-type separation can occur on such factors is the note's own open question. Nothing here addresses lifting or legality failures.
