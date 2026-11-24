# D216 review: periodic obstruction note

**Overall verdict: CORRECT WITH GAPS.** Every checkable claim holds. The gaps concern wording and scope. None of them reverses a conclusion. The note's controls are weaker than they appear: the f=4 pinned pair is **lit by a reflected path** in every room from M=7 to M=12. The note states this pair only fails direct visibility, so the note stays correct, but neither control is a dark candidate.

Checks: [checks.py](checks.py), output in [checks.log](checks.log). It reports 37 PASS and 0 FAIL in 0.2 CPU seconds. It reuses the d212 exact cell tracer, imported unchanged. It adds an independent leg-by-leg `Fraction` tracer for the six reflected paths. The papers came from arXiv PDFs and were read with `pdftotext`.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | Exact dark criterion on X; genus r+1; J is the hyperelliptic involution and fixes no lift of an interior mark | CORRECT |
| 2 | Literature readings (Wolecki, HST, Apisa–Wright, LMW) | CORRECT WITH GAPS (scope remarks) |
| 3 | Periodicity costs zero reflexes; rectangle half-turn example | CORRECT |
| 4 | r ≥ kz for a pillowcase factor; W ≥ 22 for k, z ≥ 3 | CORRECT |
| 5 | R22 darkness by dyadic parity and seam reversal | CORRECT WITH GAPS (sketch; the manuscript is complete) |
| 6 | Pinned eight-reflex controls, M=7..12 | CORRECT; the f=4 pair is lit by reflection (new) |

## Claim 1: CORRECT

- The four-copy unfolding is the orientation double cover of the room double Q. Q lies in Q(1^r, −1^{r+4}). The cover branches at all 2r+4 corners, so 2g−2 = −4 + (2r+4) and g = r+1. The checker verifies this from an exact V−E+F count of X. It runs on R22 (g=10), the staircase (g=4), the rectangle (g=1) and the controls C(7,4) and C(7,13) (g=9).
- The orientation involution J acts on copies by −I. It fixes exactly the 2r+4 = 2g+2 corner lifts and no lift of an interior or smooth-wall point (checked). The quotient X/J = Q is a sphere. For g ≥ 2 this makes J the unique hyperelliptic involution.
- The criterion is the standard unfolding equivalence. Wolecki's Lemma 2.1 and Remark 2.2 state it with trajectories that stop at vertices. Under that convention the smooth convex-corner lifts belong in F. Fixing s loses nothing, because the copy group {±1}² preserves F and the fibers.

## Claim 2: CORRECT WITH GAPS

Each reading was checked against the paper's text.

- **Wolecki, Theorem 1.2(i)** (arXiv 1905.09358v3): "Only finitely many pairs of points in Q do not illuminate each other." The paper's convention (p. 2) is that trajectories "stop upon hitting a vertex", so the marked-corner convention matches. *Gap (cosmetic):* the link label says "§2", but the theorem is in §1. §2 contains Lemma 2.1 and Remark 2.2.
- **HST, Theorem 2** (math/0602394v2): on a Veech surface, the set of points not illuminable from any p is finite. This matches. **Theorem 8** assumes that X_red² contains exactly D+ and D− = D_φ as non-parallel invariant subspaces. Its conclusion lists the regular pairs in π₂⁻¹(D−), under a cone-point condition, plus "some pairs … of periodic points". It adds: "one needs to check for illuminability case by case." The note's reading matches. *Gap (scope):* the proof of Theorem 8 notes that its hypothesis forces X to be **non-arithmetic**. Every lattice room has a square-tiled X, so Theorem 8 never applies here. The phrase "even under that hypothesis" is vacuous for this project, and the note should say so.
- **Apisa–Wright, Theorem 1.4** (1708.03411v3): "Suppose Q is not Q(−1⁴), Q(2,−1²), or Q(2²). If Q is not hyperelliptic, the only Q̃-periodic points are fixed points of the involution J. If Q is hyperelliptic …, [also] fixed points for the hyperelliptic involution." This matches. Q̃-periodicity is periodicity over the whole locus, so the note's warning holds. A mark that is periodic on one arithmetic orbit need not be Q̃-periodic. R22's S and T lifts are not J-fixed (checked), so the full-locus test would wrongly discard R22. For r ≥ 1 the stratum Q(1^r, −1^{r+4}) is not among the three exceptions. The r=0 rectangle is Q(−1⁴), which is excluded.
- **LMW, Theorem 2 and Corollary 3** (1407.2975v1): Theorem 2 states that for any translation surface M and any x, the set of y not illuminated by x is finite. Moreover, the set of non-illuminating pairs is "the union of a finite set, and of finitely many translation surfaces" in M×M. Corollary 3 gives the per-source finiteness for a rational polygon. The note's wording is correct, and the finite-set clause permits isolated exceptional pairs. This settles the item d215 left UNVERIFIED. *Gap (minor):* on M, LMW block only at singularities. The polygon statement in Corollary 3 is the relevant one for marked convex corners.

## Claim 3: CORRECT

X is a square-tiled cover of R²/Z². Its absolute period lattice Λ has full rank, because X has horizontal and vertical cylinders with integer circumferences. Λ therefore has finite index in Z². The map π: X → R²/Λ is a finite branched cover. Displacements between grid vertices are integral, so all lattice lifts map into Z²/Λ, which lies inside the N-torsion. An affine automorphism g of (X, F) satisfies π(gp) = π(go) + Aπ(p) mod Λ, with AΛ = Λ and go ∈ F. The N-torsion preimage is therefore a finite invariant set. This is the standard rational-points-are-periodic fact. The rectangle example also checks out. The half-turn about (2,1) preserves [0,4]×[0,2] and swaps (1,1) and (3,1), and the horizontal segment between them is legal (exact trace). X is the 8×4 torus, and N=8 works.

## Claim 4: CORRECT

The pillowcase map factors through Q→N, so Q→N is a branched local isometry. Each local degree e over a 3π point gives a cone angle of 3πe. The room double has maximum cone angle 3π, so e=1 and each fiber consists of k distinct reflex corners. Hence r ≥ kz, which matches fold-converse.md (r = kz + c₃). Then W = 2r+4 ≥ 22 when k, z ≥ 3. For R22 the checker confirms k=3, z=3, r=9, W=22, 13 convex corners, area 15 and strict simplicity.

## Claim 5: CORRECT WITH GAPS

The note agrees with the manuscript (Lemmas 1–3 and the darkness proof). The checker confirms the following:

- The fold maps S to a=(0,0) and T to b=(2,−2).
- The staircase has no interior lattice points.
- Its only non-vertex lattice points are a and b.

As a sanity check, no primitive direction with |p|,|q| ≤ 15 reaches T from S within 60 grid crossings (4·area). The note's sketch has three gaps:

1. **Odd point at a vertex.** The odd intermediate point folds to a vertex of P. A *convex* vertex of P can be a seam-end image, which is a reversal event, not a forbidden point. The no-reversal case is still correct, because an ordinary path can't pass straight through any vertex of P. The note's word "forbidden" should carry that clause.
2. **Reversal argument.** "Back and forth on the same orbit" is correct, but the note should cite the manuscript's first-arrival and last-visit truncation (Lemma 3). That truncation makes the "ordinary subarc" rigorous.
3. **Folding preliminaries.** The note omits two steps that make the folded path a finite event sequence. A path can't be axis-parallel, and each leg crosses each seam at most once. The manuscript has both.

## Claim 6: CORRECT, with one new observation

For each M = 7..12 and each f ∈ {L−1, 4}, the checker confirms:

- r = 8 and W = 20, with no pinch, strict simplicity, four mutually disjoint closed notches, and half-turn symmetry of the cell set.
- S=(u,3) and T=(L−u, L−3) are interior and pinned (u is the top-notch wall, 3 the left-notch level, and so on). The half-turn exchanges them, and their differences (4, L−6) are even.

- **f = L−1:** the direct chord is legal (exact trace) and misses all four closed notches.
- **f = 4:** the slope is m = (L−6)/4 = (M−3)/2 > 1, and the chord meets y=4 at u+1/m, strictly inside (u, u+1). For example, the crossing is at 11/2 when M=7 and at 92/9 when M=12. The direct trace fails. *Imprecision:* by the half-turn, the chord also meets the bottom notch's ceiling y=L−4 at L−u−1/m. This doesn't change the conclusion.
- **Reflected paths (optional; named rooms only; primitive |p|,|q| ≤ 9; grid crossings ≤ 4·area):** the f=4 pair is **lit in every room**. It has 50–72 lit directions per room. The shortest paths zigzag up the width-2 corridor between the notch walls x=M−1 and x=M+1. Both tracers confirm each one exactly.

| M | Area | Shortest direction × steps | Reflections |
|---:|---:|---|---:|
| 7 | 174 | (3,2) × 4 | 4 |
| 8 | 230 | (6,5) × 2 | 4 |
| 9 | 294 | (4,3) × 4 | 6 |
| 10 | 366 | (8,7) × 2 | 6 |
| 11 | 446 | (5,4) × 4 | 8 |
| 12 | 534 | (4,3) × 6 | 10 |

The note says that its f=4 calculation "tests only the direct segment", so this observation doesn't contradict it. It does mean that both controls are **lit**. They show that pinning, periodicity, the half-turn and non-directness don't decide darkness. They give no evidence that a dark pinned eight-reflex pair exists. The note should say that the f=4 pair is lit by reflection.

The U section repeats midpoint-necessity.md: a budget of 24 for R22, with 6 regular and 18 reflex branches. Its sufficiency statement is correct by reading. This review didn't recompute it. All four relative links resolve from `qclass-closure/bbbb/`.

## Which lemma advanced

**L1 (the exceptional specified pair), by scoping only.** The note proves no new theorem. It rules out two proof strategies:

- **Periodicity:** periodic marks cost zero reflexes, so a periodicity count can't force a reflex lower bound.
- **Endpoint symmetry:** a symmetry exchanging the endpoints costs zero reflexes too, so it can't force a bound either.

Its r ≥ kz count restates the reviewed fold count. The literature readings are now verified, including the LMW wording that d215 left open.

## First case still open

A **dark** pinned, nondirect, same-parity pair in a positive eight-reflex chart. Neither named control is such a pair: f=L−1 is directly lit, and f=4 is lit by reflection for M=7..12. The missing step is still midpoint-necessity.md's reachability lemma. It asks for a compatible straight approach on U to one regular off-class coincidence. Equivalently, it asks for a proof that failure of every approach forces a branched quotient with r ≥ 9.
