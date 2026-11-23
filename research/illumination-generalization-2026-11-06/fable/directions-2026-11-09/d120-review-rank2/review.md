# d120 review: periodic markings on the minimal rank-two sphere locus

Date: 2026-11-20. Reviewed file: [rank-two-periodic.snapshot.md](rank-two-periodic.snapshot.md).
Predecessor under separate review: d119 (`minimal-quotient-rigidity.md`). This review takes d119's minimality conclusion as an input.

## Summary

The note is mathematically sound. Its torsion criterion matches Filip's Theorem 5.2 and generalizes Möller's Theorem 3.3 as stated. The three-dimensional variation of the abelian surface holds by the Kummer rigidity argument. The degree-two real-placement analysis is correct in both deck cases. Every source statement the note cites matches the paper.

The main weakness is framing. The stated next question presupposes a residual locus M that may not exist. Apisa's own introduction expects that it doesn't. The note's dimension result already turns that existence question into a concrete algebraic problem, which comes before any torsion analysis.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1a | Forward criterion: a periodic regular mark gives a dominating branch with j_b(x) in A[N] | Sound with fixable gaps (L1) |
| 1b | Converse: a dominating torsion branch with a regular mark is periodic | Sound with fixable gaps (L2) |
| 1c | A is the abelian-surface quotient of Jac(X) attached to V = p(TM), and its forms contain ω | Sound |
| 1d | j_b is birational onto B, j_b(Jx) = −j_b(x), and B/±1 is rational in the Kummer quotient | Sound, given d119 minimality (L6) |
| 1e | P(M) maps to the moduli of polarized abelian surfaces with finite generic fibers, so A varies in three dimensions | Sound with fixable gaps (L3) |
| 1f | Counts for z = 3: genus 4, 10 Weierstrass points, double zeros at 3 of them; general z: z+1, 2z+4, z | Sound (checks.log, part A) |
| 2a | Apisa Theorem 1.5 stops at two zeros, and the introduction names the one essential use | Sound (checked against source) |
| 2b | Apisa–Wright Theorem 1.3 needs an irreducible n-point marking with n > 1; {p, Jp} is reducible | Sound (checked against source) |
| 2c | Apisa–Wright Theorems 1.2 and 1.4, Apisa genus two Theorems 1–2, high-rank Theorem 1.1 | Sound (checked against source) |
| 3a | τu = u ⇔ δs = ιs for a regular image, and two real images put both marks on one axis | Sound with fixable gaps (L4) |
| 3b | A surviving dark pair needs a nonreal regular periodic image distinct from its conjugate | Sound |
| 3c | Pole placement: all poles real in the exchange case; one nonreal pole pair in the preserve case | Sound (checks.log, part B) |
| 4a | Overclaims | None material; the verdict and status paragraphs claim only necessary tests |
| 4b | Next question is well posed | Gap (M1): well posed only conditionally on the existence of M |

## Gaps, ranked

There are no high-severity gaps.

### Medium

**M1. The next question presupposes the residual locus.** "The genus-four family" is the family over a hypothetical proper, minimal, rank-two, field-ℚ, rel-zero locus M in Q(1³, −1⁷). No such locus is known. Apisa's introduction (2110.07540, p. 6) says the conclusion of Theorem 1.5 "may hold for arbitrary genus zero strata." That conclusion would make every such M a locus of covers, which contradicts minimality. So the expected answer is that the residual case is empty.

Fix: state the existence question first, in the note's own terms. The dimension argument proves the following rigorous consequence.

> If M exists, there is a polarization type, a component F of three-dimensional families of pairs (A, C), and a choice of z Weierstrass points such that: A is a polarized abelian surface; C is a rational curve on its Kummer quotient; the inverse image B of C is birational to a hyperelliptic curve of genus z+1; and the pulled-back invariant forms contain one with double zeros at those z points, identically on F.

The pulled-back forms span a line in P(H⁰(K_X)) = P^z. Forms with double zeros at z chosen Weierstrass points are C(2z+4, z) isolated points. A line passing through one of them is a codimension z−1 condition. A heuristic count gives expected dimension 4−z for this locus, against the required 3 (checks.log, part A). The count returns 3 at z = 1, where the full stratum Q(1, −1⁵) is the example. It returns 2 at z = 2, consistent with Apisa's theorem. This is a heuristic, not a proof. It does suggest that the identity on F is the real obstruction.

Recommended next question, in order:

1. Show that no three-dimensional component F with the zero pattern exists for z = 3 (or extend Apisa §4 to three zeros). Either result removes the case without torsion.
2. Only if such an F exists, ask for a dominating non-Weierstrass torsion branch. A fixed N-torsion section meets a moving curve B in a codimension-one subset of the base. Dominance therefore needs an identity, which is an unlikely-intersection problem.

### Low

**L1. Marked points in Filip's setup.** Filip §5.1 works with W₀ built from the zero set. Apply it to the marked locus by treating x as a zero of order 0. Say so, and cite Apisa–Wright §4 and the proof of Theorem 3.12, which use this convention. The zero-relative-kernel step is correct: if v ∈ TN is purely relative, its image in TM is purely relative, hence zero. Then v lies in the forgetful kernel, which meets TN trivially because dim N = dim M.

**L2. GL-invariance in the converse.** The relation N·∫_b^x ω = ∫_γ ω has integer coefficients in period coordinates of the marked stratum. State that this is why the local graph is GL(2, ℝ)-invariant. The rest of the argument holds: the set of group elements keeping the point in the closed incidence is closed and open.

**L3. Kummer rigidity step.** Spell out two points. First, on a level cover, choose a continuous identification of A along a connected fiber, so the curves B_t lie in one surface. Second, a non-constant one-parameter family of rational curves covers the Kummer K3 surface. That makes it uniruled, which contradicts h^{2,0} = 1. The note's remaining steps are correct. Translates of B by non-2-torsion points break the ±1 symmetry, and B is the full inverse image of B/±1 because B is symmetric.

**L4. Axis lemma proof.** The note cites d99 for "both marks on one axis see each other." The d99 review states without proof that a simply connected symmetric room meets its axis in one interval. Proof: suppose a < p < b on the axis, with a and b in the room and p outside it. Join a to b by a path γ in the room. The loop γ followed by its reversed reflection has winding number Δarg(γ)/π about p, which is odd. That contradicts simple connectivity. The axis segment from a to b then lies in the open room, so it's a zero-reflection shot. checks.log part C confirms the odd-winding identity on 500 random loops.

**L5. Möller precedent.** Cite Möller's Theorem 3.3 and Proposition 3.5 as the rank-one model. Filip states that Theorem 5.2 generalizes Möller's Theorem 3.3. One difference is worth recording. Möller's converse needs no torsion hypothesis, because Theorem 3.1 makes the Mordell–Weil group over a Teichmüller curve finite. By 1e, the rank-two family A over M is a generically finite pullback of a universal family over a Siegel modular threefold. If its Mordell–Weil group is also finite, the converse could drop "torsion." That finiteness is from memory and unverified here.

**L6. Inherited minimality.** Birationality of j_b needs X = X_min, not only minimality of Y among quadratic quotients. Add the one-line derivation: the map X → Y factors through X_min, has degree 2, and Y is not a translation surface. Therefore X_min = X. This depends on d119.

## Section 3 check: the degree-two branch

The equivalence τu = u ⇔ δs = ιs holds for a regular image u = f(s), since f(ιs) = τf(s) and the fiber is {s, δs}.

- **Exchange case.** δι restricts to an orientation-reversing isometry of the room. It has the form z ↦ ±z̄ + c, so it's a horizontal or vertical reflection with one axis. Fixed points of δ lie on the seam, so both interior marks have regular images. Two real images put both marks on that axis. By L4 they see each other.
- **Preserve case.** δ is a half-turn, so no interior mark collapses. The two ramification points are the center and its mirror. At most one mark is the center, so the other mark has a regular, nonreal image.

The pole statements also hold. Upstairs zeros are reflex corners on the seam, so downstairs zeros are real. A nonreal pole must be a branch value. In the exchange case both branch values are real. In the preserve case f(c) and f(ιc) are distinct and exchanged by τ. checks.log part B verifies all of these identities on explicit sphere models of both cases, with 20,000 samples each and 0 failures.

The note correctly limits the conclusion. A nonreal regular periodic image puts its mark off the axis, so the d99 lemma doesn't apply. Periodicity alone doesn't supply that lemma's hypothesis.

## Literature checked

Checked against the source text (arXiv or author PDF, read locally):

- Apisa, *Billiards in right triangles and orbit closures in genus zero strata*, arXiv:2110.07540v1: Theorem 1.5 ("two or fewer zeros"), the introduction's remark on Section 4 and the expectation for arbitrary genus-zero strata, and Corollaries 1.6–1.7.
- Apisa–Wright, *Marked points on translation surfaces*, arXiv:1708.03411v3: the definitions of point marking, periodic point, fiberwise union, and irreducible marking; Theorems 1.2 (Eskin–Filip–Wright), 1.3 and 1.4 with its three exceptions; the proof of Theorem 3.12 on factor torsion.
- Filip, *Splitting mixed Hodge structures over affine invariant manifolds*, arXiv:1311.2350v3: §5.1, Definition 5.1, Theorem 5.2 and its proof, Remark 5.3, and Theorem 5.4.
- Möller, *Periodic points on Veech surfaces and the Mordell–Weil group over a Teichmüller curve*, arXiv:math/0410262: Theorem 3.3, Corollary 3.4, Proposition 3.5, and Corollary 3.6.
- Apisa, *Periodic points in genus two*, arXiv:1710.05505v1: Theorems 1 and 2 and Corollary 1.
- Apisa–Wright, *High rank invariant subvarieties* (author PDF): Theorem 1.1.

From memory, not checked:

- Uniruledness of a surface covered by a family of rational curves, and non-uniruledness of K3 surfaces.
- Manin–Mumford (Raynaud): B has finitely many torsion points in each fiber. This is consistent with Eskin–Filip–Wright finiteness.
- Finiteness of Mordell–Weil groups of universal families over Siegel modular varieties (Silverberg type), used only in L5.
- The Kummer rational-curve reference the note links (Tschinkel's notes); not opened.

One citation note: Apisa–Wright attribute the periodic-point torsion statement to Filip's *Semisimplicity* paper [Fil16a]. The statement is Theorem 5.2 of the *Splitting* paper [Fil16b], which is the one this note cites correctly.

## Computation

[checks.py](checks.py) runs in under 0.1 s with `python3 -B`. Its output is in [checks.log](checks.log). It runs no search over rooms, rays, directions or reflection words.

- Part A: genus, Weierstrass, stratum dimension and rank, and divisor bookkeeping for z = 1–8. It also tabulates the heuristic count in M1.
- Part B: explicit sphere models of both deck cases. Exchange case: ι(w) = w̄, δ(w) = 1/w, f(w) = w + 1/w. Preserve case: ι(w) = 1/w̄, δ(w) = −w, f(w) = w².
- Part C: the odd-winding identity behind L4.
