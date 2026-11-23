# D143: review of per-class-relay.md (snapshot 2026-11-22 01:25)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/per-class-relay.2026-11-22-0125.md`. Context read: the d142 snapshot `two-image-midpoints.2026-11-22-0100.md` (not reviewed), the d141 review and `checks.py`, and the R22 manuscript (`illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex`).

Code: [checks.py](checks.py), log [checks.log](checks.log), 2.4 CPU-seconds. It uses exact integer and Fraction arithmetic. It imports d141's unfolding model read-only and constructs 3 named rooms: B, O and R22. It runs no room search, no ray search and no network calls.

## Verdict

**Sound with gaps.** No gap is high.

- The two-site lemma is correct, and its proof checks.
- The B and O deductions are correct as stated, and conditional on d142.
- The exhaustive replay below confirms their conclusions for B and O without using d142.

The gaps are about sharpness and scope:

- The lemma is weaker than the same proof gives. Site p matters only for paths whose holonomy lies in 2Λ.
- The same-site hypothesis is restrictive, and the note doesn't say so.
- For R22, the answer to the note's closing question is no (§3). No midpoint test explains R22's darkness.

## Method

For each room, `checks.py` re-tiles d141's unfolding X by developed unit squares, which gives right and up permutations r and u on the squares of X. It then enumerates every midpoint mechanism.

- **Every translation quotient of genus 2 or more.** Such a Y has a zero, and every zero lies over the origin of ℝ²/ℤ², so X → Y → ℝ²/ℤ². These quotients are exactly the block systems of ⟨r, u⟩, and the script enumerates all of them by Atkinson closure and joins.
- **Every −I involution on each quotient.** Each one maps zeros to zeros, so it permutes squares with s r = r⁻¹ s and s u = u⁻¹ s.
- **Genus-one quotients ℝ²/L.** Here every X point over the midpoint site maps to a fixed point. The test therefore reduces to "every X point over this site of ℝ²/Per(X) is forbidden". That condition doesn't depend on L.

For a source lift s, a target lift t and an e with e f(s) = f(t), the script splits holonomies into the 4 classes of (w0 + Per(X)) / 2Per(X), where w0 is the displacement from s to t. It applies these tests:

| Test | Blocks a holonomy class w when |
|---|---|
| FULL | every fixed preimage is forbidden |
| NOTE | the note's two-site test (Λ = Per(Y), same-site case) blocks w's direction class |
| SITE | the single site p + w/2 mod Per(Y) is clean |
| XSITE | as SITE, but preimages are sorted by their site mod Per(X) |
| TORUS | every X point over π_X(s) + w/2 mod Per(X) is forbidden |

## 1. The two-site lemma

**Definition.** Let γ be a legal path from s to t, with π(s) = π(t) = p. Its holonomy w lies in Λ \ {0}. Write w = k v with k ≥ 1 and v primitive in Λ. Then:

- The primitive parity class is c = v mod 2Λ. It is nonzero because v is primitive, and the sign of v doesn't affect it.
- k is the number of primitive steps. Equivalently, γ passes over p at the k − 1 interior times j/k.

**The site rule is correct.** The midpoint lies over p + kv/2. That is p for even k and p + c/2 for odd k, and v/2 mod Λ depends only on c. `checks.log` §1 confirms this on 5 lattices: 3,360 cases, 0 failures.

**The midpoint step is correct.** Take an involution ι of derivative −I and a segment γ from x to ι(x) that avoids zeros. Reverse ι∘γ. It starts at ι(ι(x)) = x with the velocity of γ. Unique continuation gives ι(γ(½)) = γ(½), so the midpoint is ι-fixed. The note's other steps also hold:

- A zero has only zero preimages.
- Every zero is a forbidden corner lift, so a legal path's image on Y is regular.
- The relation π∘e = −π + 2p holds globally, because π∘e + π is locally constant.

The replay checks this directly on O. In 100 cases, a direct chord joins s and t and some quotient involution exchanges their images. In every case, the chord midpoint is e-fixed and lies over p + w/2 mod Per(Y). No chord's holonomy class is ever reported blocked, on B (480 chords) or O (210 chords). Every fixed point of every exchanging e lies on the 4 sites (πs + πt)/2 + ½Per(Y). This check is an assertion in `pair_tests`.

**The lemma is not sharp (gap 1).** The proof locates the midpoint by w mod 2Λ, not by the direction class.

- If w ≢ 0 mod 2Λ, then k is odd and the midpoint lies over p + c/2. Site p plays no role.
- Site p matters only for w ∈ 2Λ, which is the even-k paths of every direction.

The note sorts paths by direction class, so it folds the even-k paths of all 3 directions into each class test. That makes p mandatory everywhere. So "a single such preimage over p disqualifies this involution from this test in every class" is a feature of its test, not of the mechanism. With p dirty, the one-site form still blocks every odd-k path whose site p + c/2 is clean.

On O this matters. 16 (target lift, holonomy class) cells are blocked by SITE but by neither NOTE nor FULL. Here is one example:

- S = (1/2, 3/2) and T = (3/2, 1/2), with the target on sheet −swap.
- The mechanism is the −I lift of the reflection y = x on X itself. Its 8 regular fixed points lie over 2 sites, and p is one of them.
- NOTE blocks nothing. SITE blocks 2 of the 4 holonomy classes.

**Same-site hypothesis (gap 2).** If π(s) = π(t) = p, then 2p = C_e. So p is one of e's 4 fixed sites, and the marks sit over a half-period site of e. Generic marks have π(t) = −π(s) + C ≠ π(s). One example is d141's B source (53/40, 27/40) and its hidden targets. For such marks the lemma applies only after you coarsen Λ to contain w0, which merges sites. The direct fix is the affine form: the sites are (πs + πt)/2 + ½Λ, and you label them by w − w0. The script implements this form.

The note also leaves Λ open. The class depends on Λ. For example, R22's parity classes appear with Λ = 2ℤ² but not with Λ = ℤ².

**A further refinement (gap 4).** The midpoint lies over π_X(s) + w/2 in X's own period torus ℝ²/Per(X), which can be finer than Λ ⊇ Per(Y). Sorting fixed preimages by that site is valid and stronger. It blocked no extra cells in B, O or R22.

## 2. Replay on B and O

| | B (V-notch) | O (octagon) |
|---|---|---|
| X | 96 squares, genus 3 | 56 squares, genus 9 |
| Per(X) | ⟨(4,4), (0,8)⟩, index 32 | ⟨(1,1), (0,2)⟩, index 2 |
| Block systems | 26 | 12 |
| Genus ≥ 2 quotients (degree: genus) | 1: 3; 2: 2 (three times) | 1: 9; 2: 5 (five times); 4: 3 (three times); 8: 2 |
| −I involutions on genus ≥ 2 quotients | 7 | 25 |
| Full-fiber-clean involutions | 1 (τ on X) | 2 (τ on X; one degree-2 involution with no fixed points) |
| Most full-fiber-clean involutions on one Y | 1 | 1 |

`checks.log` §2 tabulates the fixed fibers of each involution over its 4 sites. For B:

- The degree-1 non-τ involutions have 1 regular fixed point over each site, so they fail every test.
- Each degree-2 quotient X/C2 has one involution. Two of its sites are clean (6 and 2 corner lifts), and two carry 2 regular points each.

Under the note's lemma with p at a clean site, that involution would block one direction class. On the 33 interior half-integer marks of B, it never exchanges a pair in a way that blocks anything. Exchanges occur in 42 of 4,224 cases, and none produces a clean midpoint site.

**The C3 quotient of B is the period torus.** The degree-3 quotient X/C3 is the 32-square genus-1 quotient, ℝ²/Per(X). Its [τ] blocks through one coset (1,1) + ½Per(X) of 4 sites. Those sites carry exactly the 8 corner lifts and nothing else. This blocking is a corner-only-site fact, so the mechanism needs no symmetry of B. Across the 528 half-integer pairs, it blocks 108 cells, and only the TORUS test catches them. This sharpens d141 §5 and is consistent with the note's statement that this quotient "can block selected lifts".

**The note's deductions are correct.**

- *V-notch, "needs genus ≥ 5".* Riemann–Hurwitz gives genus(Z) ≤ genus(X) = 3. The enumeration agrees: every genus ≥ 2 quotient has genus 2 or 3.
- *Octagon, "≤ 3 partners against ≥ 4 images".* genus(Z) ≥ 5 forces degree ≤ 2, and the degree-2 quotients have genus exactly 5. Each elliptic-branch source has at most 3 partners, while 8 distinct target lifts have at least 4 images. The quarter-turn quotient is one of the degree-2 quotients, and its involution is free.
- *Stronger, without d142.* No quotient of B or O carries more than one full-fiber-clean involution. A generic mark has 8 distinct images on every Y, because their torus coordinates g·S are distinct. So the all-lift full-fiber hypothesis fails for every generic pair. A direct check also finds that none of the 528 (B) and 210 (O) half-integer pairs satisfies it on any Y.
- *No dark pair appears.* No pair in either room has all 32 (lift, class) cells blocked. That is consistent with both rooms being illuminated.

## 3. R22: the answer to the closing question is no

The room is the manuscript's 22-vertex list, with S = (0,0) and T = (2,2).

- X has 60 squares, genus 10 and 22 forbidden corner lifts. These figures match `cylinder-period-index.md`.
- Per(X) = 2ℤ², and all 8 endpoint lifts lie over X-site 0.
- There are 7 block systems. Only 2 quotients have genus ≥ 2: X itself, and the degree-3 staircase unfolding (20 squares, genus 4). That second quotient matches d93's unique block system.
- Each of those 2 quotients carries one −I involution, its τ-type deck map. **Neither exchanges f(s) and f(t) for any of the 4 lift pairs.**

So no quotient involution acts on this pair at all. Only the torus test remains. Here are the X points over the lattice classes mod 2ℤ²:

| Class mod 2ℤ² | Forbidden | Regular | Regular physical points |
|---|---:|---:|---|
| (0,0) | 3 | 12 | (0,0), (2,2), (2,−2), (4,0) |
| (1,0) | 5 | 4 | seam endpoints (−1,0), (1,0) |
| (0,1) | 5 | 4 | seam endpoints (2,1), (2,3) |
| (1,1) | 9 | 0 | none |

The 4 holonomy classes are w mod 4ℤ², and the midpoint lies over w/2 mod 2ℤ². Midpoint tests block only w ≡ (2,2) mod 4, through the corner-only site (1,1). **12 of 16 (target lift, class) cells stay unblocked by every test, in every quotient.**

- The classes (2,0) and (0,2) fail because the 4 seam endpoints E_j are regular points of X over the odd sites.
- The class 0 mod 4 fails because the marks and two smooth wall points sit at the even site.

The manuscript's proof overcomes both, using tools that no midpoint test has:

- It folds to the staircase, where each E_j becomes a convex corner, and handles reversal there.
- It locates the lattice point B/2^r, or equivalently the first primitive lattice step, on an odd site. That works for every w ∈ 2ℤ², including w ∈ 4ℤ².

That is a developed-path invariant of the kind the note's last sentence anticipates. R22's darkness isn't explained by per-class two-site blocking, or by its one-site or X-site sharpenings (gap 3).

## 4. Scope

- **Proved unconditionally in the note:**
  - the two-site lemma;
  - the four-site location of fixed points;
  - recovery of the full fixed-fiber hypothesis from all 3 classes, and the bookkeeping for sites other than p;
  - the order-four remark.
- **Conditional on d142:**
  - "genus(Z) ≥ 5" under the all-lift full-fiber hypothesis;
  - the H-branch bound genus(Z) ≥ 11;
  - the elliptic partner bound.

  The B and O deductions use these. §2 confirms their conclusions independently for those two rooms.
- **Relay section:** argued but not replayed here. The "iff" holds as argued once you fix the definitions. Its finite form relies on the unreviewed cusp argument in `per-class-converse.md`.

## Gaps

1. **Medium. The lemma is weaker than its proof.** The midpoint site is determined by w mod 2Λ, which gives 4 holonomy classes with one site each. Site p matters only for w ∈ 2Λ. The note should state the one-site form. It should also withdraw or qualify "a single preimage over p disqualifies this involution … in every class": that statement is true only of its two-site test. On O, the one-site form blocks 16 cells that neither the two-site test nor full-fiber blocks.
2. **Medium. Same-site hypothesis and choice of Λ are implicit.** π(s) = π(t) forces 2p = C_e, so the marks must lie over one of e's own fixed sites. Generic marks, such as d141's B example, need the affine form (πs + πt)/2 + ½Λ, or a coarsened Λ. The note should fix Λ explicitly, because the class depends on it. Λ = Per(Y) is the natural choice. The relay section's "physical parity coordinates" are 2ℤ² for orthogonal rooms.
3. **Medium. R22 isn't reachable by any midpoint test.** This answers the note's closing question, and the note should record it. On R22's X and on all 7 of its translation quotients, no −I involution exchanges the endpoint images. Only the class w ≡ (2,2) mod 4ℤ² is blocked, through a corner-only site. 12 of 16 cells stay open, because of the seam endpoints and the even-site marks. A proof strategy that seeks a quotient satisfying the two-site test for a dark BBBB pair therefore cannot cover R22-type darkness. A developed-path argument, such as the first lattice step together with fold and reversal, is necessary there.
4. **Low. A finer sort is available.** You can sort fixed preimages by their site in ℝ²/Per(X), and only the sites hit by w0 + Per(X) matter. Both refinements are valid and stronger, but they changed nothing in the 3 rooms checked.
5. **Low. B's C3 mechanism is a corner-only torus site.** X_B/C3 = ℝ²/Per(X). Its blocking comes from the coset (1,1) + ½Per(X), which carries exactly the 8 corner lifts. The note's remark is correct, but describing the mechanism as an involution overstates what it uses.
6. **Low. The relay section uses a second meaning of "primitive step".** It counts steps in the pole lattice ½Λ, while §1 counts them in Λ, and it leaves "physical parity coordinates" undefined. State both, and give the conversion: an even number of pole steps equals k steps in Λ.
