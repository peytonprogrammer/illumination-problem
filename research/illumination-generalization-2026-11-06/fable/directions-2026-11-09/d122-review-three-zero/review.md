# d122 review: the three-zero boundary, divisor, and recognition notes

Date: 2026-11-20. Reviewer: independent referee.

Reviewed files, as snapshots in this directory:

- `three-zero-boundary.snapshot.md` (the free collision mark lemma)
- `three-zero-divisor.snapshot.md` (two cylinder directions on arithmetic spheres)
- `three-zero-recognition.snapshot.md` (synchronized hexagon forces a degree-three cover)

Context read: `../d120-review-rank2/review.md` and `../d119-review-minquot/review.md`.

Primary sources: I fetched arXiv 2110.07540 (Apisa, genus zero) and arXiv 2103.02133 (Apisa, minimal homological dimension). I extracted the text locally and then deleted both downloads. No project information went to outside services.

Own code: [checks.py](checks.py), log [checks.log](checks.log), 2.2 CPU-seconds. It uses explicit hyperelliptic sphere models only. There's no search over rooms, rays, directions or reflection words.

## Summary

All three notes are mathematically sound in their stated scope. I found no false claim. The 64-array determinant distribution in the recognition note reproduces exactly.

The batch proves two things about z = 3:

1. No rational rank-two locus M in Q(1³, −1⁷) has a boundary divisor from one isolated zero–pole collision with connected normalization and only the collision pair marked.
2. If M carries two synchronized matchings forming an embedded alternating hexagon, M is a locus of degree-three covers of Q(1, −1⁵). So a minimal M can't carry one.

Neither result decides whether a minimal M exists.

Two framing issues matter more than any proof step. First, the cylinder-rigid hypothesis is a theorem, not an assumption: Apisa 2103.02133, Lemma 4.2 and Proposition 4.12, makes every boundary component of M cylinder rigid. Second, the divisor note's "remaining lemma" now contradicts the note's own theorem. It's equivalent to the nonexistence of a minimal M, so it isn't a reduction.

The stated remaining gap, proportional rather than equal vanishing periods, is real but is one of three missing inputs. The first missing input is that a minimal M has a coupled zero–pole degeneration at all.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| B1 | Setup counts: genus z+1, 2z+4 branch points, codimension z−1, no relative tangent kernel | Sound (source and checks.log, part C) |
| B2 | Rank-two, rel-zero, field-ℚ restriction at z = 3 | Sound with fixable gaps (L4: two citations from memory) |
| B3 | Diagnosis of where Apisa's §4 stops at z = 3 (tree path of three weight-one vertices, Lemma 2.12) | Sound as a diagnosis; Apisa's statements match the source |
| B4 | Isolated zero–pole divisor: dimension 3, rank 1, rel 1, free collision point, torus-cover normalization | Sound with fixable gaps (L1) |
| B5 | Free collision mark lemma: a cylinder-rigid divisor has one J-orbit of cylinders in every periodic direction | Sound; hypothesis is automatic (M1) |
| D1 | Every arithmetic sphere in Q(1^s, −1^(s+4)), s ≥ 1, has a periodic direction with at least two intrinsic cylinders | Sound |
| D2 | Distinct intrinsic cylinders lift to distinct J-orbits on the double | Sound |
| D3 | Hence no cylinder-rigid isolated zero–pole divisor, for s = z−1 ≥ 1 | Sound; can drop "cylinder-rigid" (M1) |
| D4 | Scope: "existence of such a divisor for a minimal locus remains" | Gap (M2): the remaining lemma is now vacuous |
| D5 | Covering explanation: k = 3, z₀ = 1, four simple ramifications over distinct poles, coupled collisions | Sound (checks.log, part C) |
| R1 | Step 1: all three zeros have one image in A[2] | Sound; needs only mod-2 agreement (L2) |
| R2 | Step 2: minors, 1 ≤ \|det F\| ≤ 9, Pf(K) ≤ 9, D²/2 = Pf(K) | Sound (checks.log, part A) |
| R3 | Step 3: birational image needs delta ≥ 9 but has at most 6 | Sound |
| R4 | Step 4: genus-two target, degree 3, unramified, descends to Q(1, −1⁵) | Sound |
| R5 | Diagnostic: \|det F\| < 9 excludes a configuration | Sound; can be sharpened (L3) |
| O1 | Overall: what the batch proves about z = 3 | Correctly stated as not closing z = 3 |
| O2 | Remaining gap is "proportional, not equal, vanishing periods" | Gap (M3): necessary but incomplete |

## Gaps, ranked

There are no high-severity gaps.

### Medium

**M1. Cylinder rigidity is automatic, and the notes treat it as a hypothesis.** Apisa 2103.02133, Lemma 4.2, says a rel-zero locus of connected surfaces is cylinder rigid (CR). Its Proposition 4.12 says every boundary component of a CR locus of connected surfaces is CR. Apisa 2110.07540, p. 7, uses exactly this: "every component of the boundary of a rank two rel zero invariant subvariety is a rank one cylinder rigid invariant subvariety." M has rel zero, so every boundary divisor of M is CR.

Consequence: the divisor note proves more than it claims. No rational rank-two M in Q(1³, −1⁷) has an isolated zero–pole boundary divisor of the stated type, cylinder rigid or not.

Fix: in the boundary note, cite Lemma 4.2 and Proposition 4.12, and restate the lemma for any boundary divisor of M. In the divisor note, delete "cylinder-rigid" from the verdict and from the remaining lemma.

**M2. The divisor note's remaining lemma contradicts its own theorem.** The note proves that no rational rank-two locus has the isolated divisor. The remaining lemma asserts that every minimal locus has one. Together they give "no minimal locus exists," but only because the lemma would then be vacuously true. Proving the lemma is the full classification problem, not a step toward it.

Fix: replace the remaining lemma with the positive statement the theorem proves.

> Every codimension-one zero–pole degeneration of a hypothetical minimal M is coupled, disconnected, or marks more than one conjugate pair. Classifying those degenerations is the remaining problem.

The note's "coupled collisions" section already moves in this direction. The verdict paragraph and the boxed lemma should match it.

**M3. The stated remaining gap is one of three missing inputs.** The recognition note needs three things that no current result supplies.

1. **A coupled zero–pole degeneration exists.** A minimal M may degenerate only through zero–zero mergers, or through cylinder collapses with disconnected limits. Apisa's own induction (2110.07540, §§5–6) runs through cylinder collapses and handles disconnected limits with §3 joinings. None of the three notes shows that a minimal M has any divisor where three zero–pole arcs vanish together.
2. **Equal, not proportional, signed periods.** On a single divisor the vanishing functionals are proportional on TM. Their ratios are rational because M is defined over ℚ. Write a relation as λ·j₊δ(a₁) = μ·j₊δ(a₂) with coprime integers. Step 1 survives when λ and μ are both odd, since the relation still gives agreement modulo 2. It fails when one of them is even. Step 2 changes in either case, because the vectors in K become λδ(a₁) − μδ(a₂) and the bound 9 no longer holds. Nothing in the batch excludes ratios other than ±1.
3. **A second matching, shifted by a three-cycle, disjoint from the first on one sphere.** Two boundary divisors live on different degenerations. Transporting both arc systems to one smooth surface while keeping interiors disjoint is a separate topological problem.

The recognition note names items 2 and 3 in its last paragraph. Item 1 comes first logically, and only the divisor note's coupled-collision section hints at it.

The cover locus itself shows that item 1 is subtle. Moving the base zero to a branched pole gives one zero–pole cancellation plus a zero–zero merger. That divisor is neither isolated nor triply synchronized.

Fix: state the open problem as a classification of the CR rank-one boundary loci of M in codimension-two hyperelliptic loci. This is the analog of Apisa's Proposition 4.3, which Apisa's introduction names as the only essential use of the two-zero bound. Then list the three items above as one possible route through that classification.

### Low

**L1. Name the boundary model and the count bound in the free mark lemma.** The divisor is a component of the Mirzakhani–Wright boundary. Its marked points p and Jp are limits of the collapsing singularities. The subequivalence count bound, at most rank plus rel, is Wright's, cited as Apisa–Wright [AWb, Theorem 7.10 (2)] in Apisa 2110.07540, proof of Lemma 3.4. I confirmed that citation at source. Fix: add both sentences and state that the contradiction is checked at a surface with p at a generic height.

**L2. Step 1 of the recognition note uses only mod-2 agreement.** The A[2] computation needs j₊δ(aᵢ) to agree modulo 2H₁(A, ℤ), and signs don't matter modulo 2. Integral agreement enters only in step 2, where the differences must lie in K. Fix: state step 1 under the weaker hypothesis. Step 1 then also covers odd proportionality ratios (see M3), so for odd ratios a proportional-coefficient version needs new input only in step 2.

**L3. Sharpen the |det F| diagnostic.** The conclusion forces Pf(K) = 9. Since Pf(K) times the sublattice index equals |det F| and |det F| ≤ 9, a synchronized configuration must have |det F| = 9 exactly. Only 2 of the 64 sign arrays give 9 (checks.log, part A). Both lie in the class where the product of the six intersection signs is −1.

On explicit genus-four hexagon models, that product equals −1 exactly when the hexagon separates the other four poles evenly (checks.log, part B2). Fix: state the sharper test. A synchronized hexagon must split the four remaining poles 0|4, 2|2 or 4|0, and its synchronized sign array must be ±(I − S).

**L4. Some citations are from memory.** I didn't check these at source:

- Wright's field-degree bound (arXiv 1210.4806)
- Apisa–Aulicino, Theorems 1.1–1.2 (arXiv 2404.10273)
- the Apisa–Wright high-rank theorem
- the Mirzakhani–Wright boundary tangent formula (arXiv 1508.01446)
- Gekhtman–Marković, Proposition 6.1
- the Springer one-cylinder pillowcase paper

None is load-bearing for the free mark lemma or the two-cylinder theorem. The rationality step in B2 depends on Wright and Apisa–Aulicino. Fix: check those two statements at source before B2 is cited elsewhere.

## Note-by-note checks

### Boundary note

Counts. For z simple zeros the double has 2z+4 branch points and genus z+1. The sphere stratum has dimension 2z+2, and H(2^z) has dimension 3z+1. The codimension is z−1, matching Apisa's Lemma 2.1 with unmarked poles (k+1 = z). At z = 3: dimensions 8 and 10, codimension 2.

Apisa statements checked at source:

- Definition 2.6 (vertex weights kᵢ+1 sum to k+1)
- Lemma 2.8 (rel basis from the tree vertices)
- Lemma 2.12 (codimension one, with a proof that cuts to a codimension-zero piece)
- Proposition 2.13 (boundary codimension at most k, no strict drop)
- Proposition 4.3, Lemma 4.4 and Sublemma 4.5

The note's description of where the one-edge inference fails at z = 3 is accurate. It's a diagnosis of the proof, not a proof that the statement fails, and the note says so.

Isolated divisor. Upstairs the vanishing loop γ ∪ Jγ is nonseparating. Collapsing it lowers the genus from 4 to 3 and leaves two regular points p and Jp. The total zero order drops from 6 to 4, matching H(2, 2). A dimension of 3 with positive area forces rank 1 and rel 1. The torus-cover conclusion follows because the boundary tangent is the intersection of two ℚ-subspaces.

Free mark lemma. Moving p is a deformation inside the divisor because the fiber is all of the surface. In the exchanged case the pieces have heights y and H−y; in the fixed case, y, H−2y and y. A cylinder in a second J-orbit keeps constant height. Definition 4.1 (3) of 2103.02133 makes modulus ratios of subequivalent cylinders locally constant. So the three height functions give three disjoint subequivalence classes, against the bound of 2.

With one J-orbit there are exactly two classes, so the lemma is sharp. This also matches Apisa's Proposition 4.3 (1)–(2): there the rel-one CR loci are covers with full fibers of a free point marked, not a single conjugate pair.

### Divisor note

One-cylinder case. Each side of the core circle is a disk that retracts onto its horizontal critical graph, so the graph is a tree. Zeros are trivalent vertices and poles are leaves. A tree with k trivalent vertices has k+2 leaves, and the two trees together give s+4 poles (checks.log, part C). Each edge is traversed twice by a rim of length C, so edge lengths sum to C/2.

Pocket. The shortest pendant edge on the larger tree has length at most C/(2(k+2)). Aligning one pole on each rim gives closed vertical leaves of length 2H for 0 < u < m. The pocket is bounded by a folded pole-to-pole connection on one side and a zero on the other, so it is maximal. Its area fraction is at most 1/(k+2), which is 1/3 at s = 2.

The direction is periodic because a pole-to-pole saddle connection on a pillowcase cover develops to a rational direction. A second cylinder fills the positive-area complement.

Lift to the double. Each intrinsic cylinder lifts to one J-orbit. The only continuation upstairs is across a folded pole-to-pole rim, where the two lifts of one cylinder join. So distinct intrinsic cylinders give distinct J-orbits, as the lemma needs.

Covering section. The target must have a zero, so 3 = kz₀ + c₃. Degree two can't have a local degree of three, so k = 3, z₀ = 1 and c₃ = 0. Riemann–Hurwitz gives four ramification points, over four distinct poles, and 4 + 3 = 7 poles upstairs (checks.log, part C). The local model 4(u² − a)du² for the zero–zero merger is correct.

### Recognition note

Step 1. Integrating anti-invariant forms on γ − Jγ gives twice the integral on γ. The A[2] identity zᵢ + pᵢ = c, zᵢ + pᵢ₊₁ = d then forces c = d. All pᵢ coincide, and all zᵢ coincide.

Step 2. The support of C is the six-cycle {(i, i), (i, i−1)}. All maximal minors of E and all 2-by-2 minors of C are ±1 (checks.log, part A). The 64-array distribution 1: 30, 3: 26, 5: 6, 9: 2 reproduces exactly; the value 7 never occurs.

The discriminant argument is correct. K is primitive in a unimodular lattice, so |disc K| = |disc K⊥|. K⊥ = j*H¹(A, ℤ) carries the form (u, v) ↦ ∫_D u ∧ v, with Pfaffian D²/2.

Step 3. Adjunction on A gives pₐ = 1 + B²/2 ≤ 10. With geometric genus 4, the delta budget is at most 6. At each zero, y − y₀ has order 3 and both centered coordinates are odd. A branch is therefore either smooth with contact order at least 3 with y = y₀, or of multiplicity at least 3. Each pairwise intersection is at least 3, so delta is at least 9 > 6.

Step 4. Riemann–Hurwitz with target genus at least 2 allows only (genus 2, degree 2, ramification 2) and (genus 2, degree 3, ramification 0) (checks.log, part C). The common fiber of three zeros excludes degree 2. Surjectivity on H₁ makes Jac(Y) → A an isomorphism. Negation on A restricts to the hyperelliptic involution because j is based at a Weierstrass point.

### Explicit model: the theorem is sharp on the cover locus

I checked that the hypothesis holds on the degree-three cover locus and gives |det F| = 9 there.

Take a bigon on the base sphere from the zero z₀ to the unbranched pole q₅. It encloses two of the four branched poles, so its monodromy is a three-cycle. The two base arcs lift to two matchings shifted by a three-cycle. Their union is the preimage of the bigon boundary, which is one embedded hexagon. Lifts of one base arc have equal signed periods, so the matchings are synchronized.

Near the zeros and the poles above q₅ the cover is a local isometry. So C = s_z·I + s_q·S, where s_z and s_q are the base crossing signs at z₀ and q₅.

On an explicit genus-two model, δ(a)·δ(b) = 0 when the bigon encloses an even number of branch points and −2 when odd (checks.log, part B1). With two enclosed, s_q = −s_z, so C = ±(I − S) and |det F| = 9 (part A). This matches the forced Pfaffian 9.

## What the batch proves about z = 3

Proved, given the notes' explicit degeneration hypotheses:

- A proper rank-two locus M in Q(1³, −1⁷) has field ℚ and rel zero. This rests on B2, with the two citations in L4 from memory.
- M has no boundary divisor from one isolated zero–pole collision with connected normalization and only {p, Jp} marked. This holds at every z ≥ 2 under the same hypotheses.
- A synchronized embedded hexagon on M forces M to be a locus of degree-three covers of Q(1, −1⁵). A minimal M therefore has none.

Not proved: that a minimal M has no other kind of codimension-one degeneration. So z = 3 stays open, and the notes say so.

Is the stated gap the right one? It is a genuine obstruction to the recognition route, and the note states it correctly. As the headline gap it is too narrow (M3). The first open question is which boundary types a minimal M must have. Apisa's framework poses that question as the codimension-two analog of Proposition 4.3.

## Literature checked

| Statement | Checked |
| --- | --- |
| Apisa 2110.07540, Theorem 1.5 and the introduction's remark that §4 is the only essential use of the two-zero bound | At source |
| Apisa 2110.07540, p. 7: boundary components of rank-two rel-zero loci are rank-one CR | At source |
| Apisa 2110.07540, Lemma 2.1, Definition 2.6, Lemmas 2.8 and 2.12, Proposition 2.13 | At source |
| Apisa 2110.07540, Proposition 4.3, Lemma 4.4, Sublemma 4.5 | At source |
| Apisa 2110.07540, proof of Lemma 3.4: disjoint subequivalence classes number at most rank plus rel | At source |
| Apisa 2103.02133, Definition 4.1, Lemma 4.2, Proposition 4.12 | At source |
| Mirzakhani–Wright connected-boundary tangent formula | From memory |
| Apisa–Wright high-rank theorem; Wright field-degree bound; Apisa–Aulicino Theorems 1.1–1.2 | From memory |
| Gekhtman–Marković Proposition 6.1; Springer one-cylinder pillowcase paper | Not checked |
| Hironaka delta formula for plane curve germs; adjunction on abelian surfaces | From memory (standard) |
