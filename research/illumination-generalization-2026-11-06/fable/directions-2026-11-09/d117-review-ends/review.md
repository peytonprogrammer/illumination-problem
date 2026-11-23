# D117: review of the component-ends note

Date: 2026-11-20. Reviewer: independent referee.

Reviewed file: `component-ends.snapshot.md` in this directory (75 lines).

Context read: the d115 and d116 reviews, and the `COV279` cell list in `../d69-bbbb/decomp.py`. The d116 review records a primary-source check of LMW Theorem 2. I didn't refetch any paper, and no information went to outside services.

Own code: `checks.py`, log `checks.log`, 0.02 CPU-seconds. It's an exact `Fraction` tracer on the named cov279 pencil. It checks only the note's listed shots and finitely many parameters. It does no search over rooms, directions or reflection words.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Lighting is open; boundary persistence of limiting witnesses | Sound |
| 2. Same-chamber pinch transfer | Sound with fixable gaps |
| 3. cov279 control: exact shots and the reflection lower bound | Sound |
| 4. Opposite-lip theorem | Sound with fixable gaps |
| 5. Classification of ends and statement of what remains | Sound with fixable gaps |

## 1. Openness and boundary persistence

A lit pair has a legal path with finitely many transverse bounces in open edges. Its unfolded chord meets those edges in strict inequalities. Small affine motion of walls and marks keeps them strict, so lighting is open. The boundary version uses the same argument. It needs only that each bounce edge survives as an open edge and that the rest of the trace keeps positive clearance from changing boundary. The note states both conditions. The remark that a singular endpoint excludes only transferable witnesses is the correct scope.

## 2. Same-chamber pinch transfer

The proof is correct. The trace of a legal A-path that avoids p is compact, so it has positive distance from p. Claim 1 then transfers it. The contrapositive is stated correctly.

The two-reflex count is also correct. Cutting the overlap splits each reflex lip into a right angle in one piece and a straight angle in the other. So r_A + r_B = r − 2 when no other collapse occurs. I confirmed the local geometry at both lips of cov279.

**Gap 2a (medium).** The sentence "This gives the requested smaller-room induction" omits a caveat. The note states the same caveat for wall collapse: a rational limiting tuple need not give primitive lattice marks in a normalized smaller room. The induction hypothesis for rooms with fewer walls may cover only normalized lattice pairs, or only one parity class. Then darkness in A of a rational limiting pair contradicts nothing. Fix: repeat the normalization caveat here. Alternatively, state the induction hypothesis as illumination of all interior point pairs in strictly simple rooms with fewer walls.

**Gap 2b (low).** "If p is a vertex of A" reads as a restriction. For two strictly simple orthogonal pieces with disjoint interiors and a single contact point, p is always a convex corner of both, and the quadrants are opposite. Any other local configuration makes the contact a segment or makes the interiors meet. Fix: state this as a one-line lemma. It also justifies the "opposite convex quadrants" hypothesis of claim 4.

## 3. The cov279 control

**Room.** At t = 1 the table reproduces the d69 rows: (0,2), (1,4), (2,5), (4,6). For 0 < t < 1 both ends step right at all three interfaces, so r = 6 and the room has 16 walls. At t = 0 the chambers meet only at p = (2,2), a convex corner of each. Check 1 confirms the following for q = 12j + 4, j = 1..5:

- The horizontal wall gcd is 1.
- The area is 13q + 3.
- Both scaled marks are even-odd.

**Lit pairs.** I rederived the translate. A positive-sheet crossing at c satisfies c ∈ 7/4 + 2ℤ + (2 + t)ℤ = 7/4 + (1/q)ℤ at t = 3/q. The overlap (2 − 3/q, 2) has width 3/q, so it holds two lattice points. Check 2 replays both points for j = 1..5 as legal shots from S to T. The second point is c = 2 − 1/q, the exact-check mouth point.

**Exact-check shots.** The slopes match exactly: 4m + 3/2 − t/3 = 4m + 1 + t/3 + 2tm at t = 3/(12m + 4). Check 3 traces this shot for m = 1..8. Each shot crosses at c = 2 − t/3 and hits T with exactly 4m reflections, all on vertical walls. Check 5 is a control. The m = 2 slope at t = 3/28 ± 1/1000 doesn't reach T within 200 reflections.

**Lower bound.** I checked the note's argument line by line. It's correct.

- Every wall at t = 0 lies on X = 2x ∈ {0, 4, 8, 10, 12} or y ∈ {0, 2, 3, 4, 6}. So reflections preserve both coordinate parities of integer points.
- p, S and T have parities (0,0), (1,1) and (0,1). Hence det(p′ − S, T′ − S) is odd.
- Only the wall X = 4 − 2t moves. Reflections are isometries, so the developed X error is at most 4t per reflection. Replacing c by p adds less than 2t.
- Ordinates are unchanged. So |Δdet| ≤ |e_a||b_Y| + |e_b||a_Y| ≤ 6(m+1)(8m+2)t.

Check 4 evaluates every quantity in this chain on each replayed shot:

- det = 0 exactly at t.
- The formal t = 0 det is odd: 1 for the exact-check shots and 17 for the long translate shots.
- The X errors and ordinates satisfy the stated bounds.

**Observation (low).** The bound m + 1 ≥ 1/√(48t) is vacuous at every named parameter, since t ≥ 3/100 there. The replayed shots use 4m ≈ 1/t reflections. Divergence as t → 0 is all the note claims, so this is correct. Fix (optional): say the bound is asymptotic, or sharpen it with |e_a| ≤ 2t + 4t·(number of moving-wall bounces).

## 4. Opposite-lip theorem

**Matching at the opening.** Both legs are directed toward the mouth. The lower leg arrives up-right and the upper leg arrives down-left. With a common slope magnitude s, reversing the upper leg gives departure velocity equal to the lower leg's arrival velocity. So equal position and equal s suffice. The derivative formula dc_i/ds = σ_i D_i follows from unfolding: each vertical fold flips the sign of the accumulated displacement. Since σ_A = −σ_B, the mismatch has derivative ±(D_A + D_B) ≠ 0. The exact correction then closes the gap. The uniform chart radius keeps the correction inside the region where the combinatorics stay fixed. This step is correct.

**Torus step.** The final state of each leg is a function of the phases s·v_j mod 1, because runs have full-height vertical walls and the cuts include every wall ordinate. The positive half-orbit of a linear flow is dense in its orbit closure. The character criterion is stated correctly. At transcendental t, an integer relation Σ k_j d_j/P_j(t) = 0 is a rational-function identity. Residues at distinct poles separate the nonconstant classes, and the constant class follows. Repeated runs within one leg are harmless, because the target there is s_A·v.

**Role of proportionality.** The hypothesis is needed exactly where the note uses it. A shared class lets a relation mix the two legs. The condition then becomes (s_A − s_B)·Σ_A k_j v_j ∈ ℤ, as the residual paragraph says.

**Gap 4a (medium).** All constant widths form one proportionality class. The hypothesis therefore forbids both legs from using any run of unchanged width. Most runs are constant in a one-axis pencil. In cov279 only the band (2,3) run moves, so the theorem applies only because leg B stays in that run. The LMW corollary needs all chamber classes disjoint. It fails for cov279: the lower chamber has width 2, and the upper chamber has constant widths 3 and 2. Fix: state explicitly that at most one leg may use constant-width runs. Add that the chamber-level corollary needs one chamber whose run widths all vary.

**Gap 4b (low).** The "Exact check in cov279" isn't an instance of the theorem, which works at transcendental t. The rational shots come from direct arithmetic. Fix: call it an illustration of the matching mechanism. Note that the theorem gives lit transcendental members, and the arithmetic gives the rational ones.

**Gap 4c (low).** Step 1 aims each leg at a mouth point. That needs the mouth to lie within the clearance cone of each final chord. It does for small opening width, because both chords enter strictly inside their quadrants. Fix: add "for parameters close enough to the end that the mouth lies in both clearance cones."

**LMW access paragraph.** The 4-copy unfolding makes each convex corner a regular point. p has one lift. Reflex corners become cone points of angle 6π. Marking the other convex-corner lifts with order 0 fits the marked-point convention that d116 checked in LMW §2.2. A mark is hidden only if all four of its lifts are hidden, so the hidden set is finite. This is correct.

## 5. Classification of ends

The finite-end list is complete for a single event. Every end is a tie of two nonidentical rational affine abscissas, so it's rational. A tie is one of the following:

- A horizontal wall of length 0.
- Nonincident walls meeting.
- A mark meeting a wall, or two marks meeting.

Vertical walls can't vanish, because ordinates are fixed. The unbounded case reduces to a regular end or one of these events in the chart u + τe. The interior-collision, half-disk and reflex-sector statements are correct. I checked the 3π sector bound: separation ≥ π leaves no local geodesic. The horizontal-edge impossibility argument is also correct.

**Gap 5a (medium).** The "nonincident walls meet" bullet says the transfer lemma and control "address this case". They address only a single point pinch. Positive-length contacts are listed but untreated. These include two vertical walls closing an exterior gap into a slit, and several contacts at once. "What remains" doesn't name them. Fix: restrict the sentence to point contacts, and add positive-length contacts to the open list.

**Gap 5b (low).** The note doesn't overclaim elsewhere. Its open items are scattered across four sections. Fix: collect them in "What remains" as one list.

### What remains open

- Same-chamber pinch, once the smaller-room induction hypothesis is matched to rational limiting marks (gap 2a).
- Opposite-side pinch where every pair of access legs shares a width class, including the common case of constant widths on both legs.
- Opposite-side pinch with a limiting mark hidden from p. This is a finite set per chamber, but membership of a given lattice mark is undecided.
- Positive-length contacts and simultaneous degenerations.
- Wall collapse where the only witness uses a scar, or a surviving slit blocks it.
- A mark reaching a reflex corner with angular separation ≥ π, a mark reaching a corner alone, or a mark reaching a wall without a transverse departure.
- The r ≤ 8 question in the residual paragraph. No bound on n and no finite census follows.

## Ranked gaps

| Rank | Gap | Fix |
| --- | --- | --- |
| Medium | 2a: Smaller-room induction omits the lattice-normalization caveat. | Repeat the caveat, or state the induction hypothesis for all interior point pairs. |
| Medium | 4a: Constant widths form one class, so both legs can't use them. The chamber-level corollary fails for cov279. | State the constraint explicitly and add the condition for the corollary. |
| Medium | 5a: Positive-length contacts are claimed as addressed. | Restrict the claim to point contacts and list the rest as open. |
| Low | 2b: Point contact forces opposite convex corners, but the note doesn't say so. | Add a one-line lemma. |
| Low | 3: The √ bound is vacuous at the named parameters. | Call it asymptotic, or sharpen it. |
| Low | 4b: The cov279 exact check is arithmetic, not the theorem. | Relabel it as an illustration. |
| Low | 4c: Retargeting to the mouth needs the mouth inside both clearance cones. | Add the proximity condition. |
| Low | 5b: Open items are scattered. | Consolidate them in "What remains". |
