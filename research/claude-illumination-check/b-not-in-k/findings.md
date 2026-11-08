# B ⊄ K from room geometry

[in progress] Claude Opus, 2026-11-02. §33's room: B ⊄ K (Section 5). Daniel chose this target after the seed work stopped.

**Target.** Show that some rational cylinder core has Q ≠ 0 in every raw room with a literal pocket. By `pocket-reflection-gate.md` §1–2 this is equivalent to B ⊄ K, where:
- B is the neck plane;
- C is the span of the rational cores;
- K = C^⊥.

**Result so far.**
- The diagonal direction is settled exactly (Section 2). A loaded diagonal core exists unless the outside of the pocket acts as a mirror for diagonal rays.
- Codex's §33 room is such a mirror room.
- Every other direction reduces to a finite zero-sum condition for each phase class (Section 4).
- **The §33 room has B ⊄ K (Section 5, fixed-room check approved by Daniel).** Every non-axis, non-diagonal class with |θ|² ≤ 25 has loaded cores. One (3,2) core hits D exactly once, so its load is odd.
- No universal proof yet. Section 6 gives a parity reformulation. Section 7 gives an exact per-direction test through the pocket square and explains why it still needs global input. Sections 8–9: in the 57 existing rooms, every one of the 210 literal pockets has B ⊄ K, detected by (1,1) or (2,1). This suggested a two-direction conjecture (Section 9). **Section 11 refutes it:** a raw 28-triangle room with a literal pocket is blind in both (1,1) and (2,1). B ⊄ K still holds there through (3,1), (3,2), (4,1), and (4,3). **Section 12 goes further:** 56 raw rooms of 35–40 triangles are blind in all seven classes with |θ|² ≤ 25. Each still has B ⊄ K, first loading at a class with 26 ≤ |θ|² ≤ 41. So the seven classes with |θ|² ≤ 25, and every subset of them, fail to detect every room. Longer finite lists stay consistent with the data. **Section 13 extends this to 41–60 triangles:** 166 more rooms are blind in all seven classes, and each still first loads at |θ|² ≤ 41. No room tested is blind through |θ|² ≤ 100.

All coordinates follow `pocket-detection.md` §1:
- The pocket is B0 = (1,1), A0 = (2,2), C0 = (1,2), with portal x = 1, 1 < y < 2.
- D is the wall y = x and H is the wall y = 2.
- a_D = (1,−1) and a_H = (0,−2).

Sections 1–4, 6, 7, and 10 use no computation. Sections 5, 8, and 9 are fixed-room checks that Daniel approved, each with its rooms and directions fixed in advance. Sections 11, 12, and 13 are bounded room enumerations that Daniel approved on 2026-11-02. No other room, ray, direction, word, cylinder, or orbit search was run.

## 1. Tools

**Parity of a closed core.** For a closed orbit, Q = Σ L_j a_j over its hits on moving mirrors (§3 formula (1)). Every L_j ∈ D4 permutes coordinates up to sign, so

    Q(core) ≡ (number of D hits per period)·(1,1)  (mod 2).

An odd number of D hits per period gives Q ≠ 0.

**Phase.** For velocity v and position z, put φ = det(z, v) mod 2. Each wall reflection sends φ to −φ mod 2:
- Axial walls lie on integer lines.
- Diagonal walls are radial A–B edges, so they lie on lines x ± y ∈ 2Z.
- So each translation part t satisfies det(t, ·) ≡ 0 mod 2.

Hence ±φ mod 2 is constant along every billiard path.

## 2. Diagonal lemma (proved)

Diagonal velocities (±1, ±1) reflect off axial walls into diagonal velocities. They meet a diagonal wall either in parallel (no hit) or at a right angle (a reversal). So every periodic diagonal orbit that hits a diagonal wall is palindromic: it has exactly two right-angle hits per period, at its two ends.

For generic s ∈ (1,2), let γ_s leave d = (s,s) ∈ D at a right angle into the pocket, and let ι(s) be its other end.

**Lemma.** Exactly one of the following holds.
- **(a)** ι(s) lies on D. Then ι(s) = (3 − s, 3 − s), the mirror point in the other half of D, and the core through γ_s has Q = 0.
- **(b)** ι(s) lies on a diagonal wall other than D. Then the core has an odd number of D hits, so Q ≢ 0 mod 2, and B ⊄ K.

**Proof.**
1. **Ends.** The orbit through d is periodic: the direction is rational and X is square-tiled. It is palindromic because it hits d at a right angle. So it has a second right-angle hit, and with diagonal velocity that hit is on a diagonal wall.
2. **No middle visit.** A diagonal ray that enters the portal hits D at a right angle, either directly with velocity (1,−1) or after H with velocity (1,1). So the path between the two ends never visits the pocket, and each end contributes one D hit.
3. **Case (b).** There is one D hit per period, so the parity rule gives Q ≢ 0.
4. **Case (a), position.** Right-angle rays at D lie on lines x + y = 2s. The phase forces 2s′ ≡ ±2s mod 2. So s′ = s or s′ = 3 − s, and s′ = s would make the orbit its own reverse halfway, which is impossible.
5. **Case (a), exact Q.**
   - The two ends lie in different halves of D, so H is hit exactly once on the forward pass: at the start if s > 3/2, or at the end otherwise.
   - Let σ be the y-sign of the frame before that H hit. Pairing each hit with its time-reversed partner gives

         Q = 2(1,−1)·(−1 + Σ σ).

   - σ = +1 in both cases, so Q = 0. This matches the direct calculation in §33.

**Corollary 1: the diagonal mirror condition.** If B ⊂ K, then (a) holds for every s. Equivalently, every diagonal ray that leaves the portal at height h returns to the same point with only its x-velocity reversed. It meets no diagonal wall on the way.

**Corollary 2: local triggers.** Each of the following makes B ⊄ K. The parent fan is F, centered at (0,2). Rawness forces F to contain τ0 = [(0,2),(0,1),(1,1)], τ1 = [(0,2),(1,1),(1,2)], and τ2 = [(0,2),(1,2),(1,3)]. It also forces the square [0,1]×[0,1] from the fan at (0,0).
- **F lacks τ3 = [(0,2),(1,3),(0,3)].** Rays from the first half of D leave the portal with velocity (−1,1). They cross τ1 and τ2 and hit the wall (0,2)–(1,3) at a right angle, at ((h−1)/2, (h+3)/2).
- **F has [(0,2),(−1,1),(0,1)], the fan at (0,0) is only the square [0,1]×[0,1], and F lacks [(0,2),(−1,2),(−1,1)].** Rays from the second half of D bounce at (0, h−1), (h−1, 0), and (1, 2−h). They then hit the wall (0,2)–(−1,1) at a right angle.

**§33 is a mirror room.** In §1 coordinates, §33 has F as a full star and the fan at (0,0) as one quadrant. Its loop runs (−a,3) → (−1,2+a) → (1,a) → (1−a,0) → (0,1−a). It then re-enters the portal at the exit height 2 − a, so it is case (a) for every a. So the diagonal direction alone can't prove B ⊄ K in every room.

## 3. Why mirror rooms are blind and what that means

Suppose the outside acted as a vertical mirror on the portal in every direction. Then every orbit through the pocket would be an orbit of the closed right isosceles triangle. That triangle translates rigidly under the slide, so every Q would vanish.

So B ⊂ K needs the outside to look like a mirror in a weak sense in every direction, not only the diagonal one. Section 4 makes this exact for each direction.

## 4. Every direction reduces to a finite zero-sum test

Fix a primitive class θ = (p, q). Pocket entries have velocities (p, ±q) and (q, ±p).
- An entry at (1, 1 + e) has phase q′ − p′ − p′e for velocity (p′, q′).
- So each phase class has exactly 2p + 2q entry states, one for each solution e ∈ (0,1) of p′e ≡ q′ − p′ ∓ c (mod 2).
- A periodic orbit visits each state at most once per period. So each phase class contains at most 2p + 2q pocket excursions in total.

**B is blind in direction θ exactly when, for every phase class, the cycles of (outside return) ∘ (pocket map) on these entry states each have Q-sum zero.**

**Worked class (2,1).** Every pocket excursion in this class is non-neutral. Contributions are in the developed frame θ = (2,1).

| Type | Entry velocity | e range | Pocket word | Exit state | Q contribution |
|---|---|---|---|---|---|
| 1 | (2,1) | all | DHDH | (1−e, (−2,−1)) | (0,−2) |
| 2 | (2,−1) | e < 1/2 | D | (2e, (−1,2)) | (1,1) |
| 3 | (2,−1) | e > 1/2 | DH | (2−2e, (−1,−2)) | (−1,1) |
| 4 | (1,2) | all | HD | (1−e/2, (−2,1)) | (−1,1) |
| 5 | (1,−2) | all | D | (e/2, (−2,1)) | (1,1) |

- Each phase class has six entries: types 1, 1, 2, 3, 4, and 5. Their sum is zero, which is the per-phase form of the §32.1 zero-mean identity.
- A cycle has Q-sum zero exactly when #type 1 = #(types 2 and 5) = #(types 3 and 4).
- So in each phase class, either one orbit carries all six entries, or two orbits each carry one entry from each group.
- The mirror return gives two such triples, as the closed triangle predicts. Any outside return that breaks this pattern loads a (2,1) core.
- Time reversal maps types 2 ↔ 5 and 3 ↔ 4 and preserves Q, as it must.

## 5. Fixed-room check: §33's room is not blind

Daniel approved this check on 2026-11-02. It computes Q for every cylinder core that meets a moving mirror, in all seven D4 direction classes with |θ|² ≤ 25. Cores that avoid both moving mirrors have Q = 0.

**Method.** The room is §33's 28 prescribed triangles, in §33 coordinates. There, D_t: x + y = 2 + t, H_t: y = t, a_D = (1,1), and a_H = (0,2).
- Every pocket excursion hits D, so every loaded core crosses D.
- For outgoing velocity w = (a,b), the singular points on D lie in (1/|a+b|)Z. Each interval between them carries one strip of height 1/|θ|.
- `core_loads.py` traces the midpoint of each strip exactly, with rational arithmetic, until the state and the frame both close.
- It computes Q twice. The first path uses the running frame, Σ L_j a_j (§3 formula (1)). The second differentiates the composed affine reflections in t.

**Checks.** All pass.
- Room: 28 triangles, area 14, 25 walls after merging the straight point (−2,0). This matches §33.
- The two Q computations agree on every core.
- Every core satisfies the parity rule Q ≡ #D·(1,1) mod 2.
- The strip sum Σ_E Q(c_E) is 0 in every direction, matching §32.1.
- `independent_trace.py` uses a different method: ray against the 26 boundary edges, closed-triangle containment, and corner avoidance. It reproduces the hits, D count, H count, and Q of all 30 cores, with 0 mismatches.
- The diagonal core is §33's family: 14 hits, 2 D, 2 H, hol (14,14), and Q = 0.

**Result.**

| θ | Strips on D | Cores meeting D | Loaded | Q values |
|---|---|---|---|---|
| (1,0) | 2 | 1 | 0 | (0,0) |
| (1,1) | 2 | 1 | 0 | (0,0) |
| (2,1) | 8 | 4 | 4 | (0,±2) |
| (3,1) | 12 | 4 | 4 | ±(1,−1) |
| (3,2) | 12 | 6 | 6 | (1,1) ×2, (−1,1) ×2, (0,−2) ×2 |
| (4,1) | 16 | 8 | 4 | (0,±2) ×4, (0,0) ×4 |
| (4,3) | 16 | 6 | 6 | (0,2) ×2, (2,2) ×2, (−2,−4) ×2 |

The axis and diagonal rows reproduce the known blindness. Every other class has loaded cores. In (2,1), the four cores cover all 112 units of X's area, and every one is loaded.

**Odd certificate.** The (3,2) core that starts at (11/10, 9/10) ∈ D with velocity (−3,−2) has 42 wall hits. It enters the pocket once, through the portal at (1, 3/4), and hits D once and H never. So Q ≡ (1,1) mod 2 with no frame bookkeeping. Its full hit list is in `certificate-3-2.log` and can be checked by hand.

**Conclusion.** B ⊄ K in §33's room, so it is not a counterexample to target 1. Its mirror behavior is diagonal-only. In the §4 language, the (2,1) cycles pair a D excursion with a DH or HD excursion, and no DHDH excursion balances them.

## 6. Next target: a parity reformulation

The parity rule turns target 1 into a mod-2 question.
- Let σ_D ⊂ X be the preimage of the open wall D. Four D-seams end at the single lift of B0, and four end at the single lift of A0. So σ_D is a mod-2 cycle.
- The D-crossing parity of a closed curve is therefore the class φ_D ∈ H^1(X; Z/2) dual to σ_D.
- φ_D ≠ 0 whenever the room has a diagonal wall other than D, as §33's room does. The portal-side walls give a vertical reflection, and with a diagonal one they generate D4. So X minus σ_D is connected, and some closed curve crosses σ_D once.
- **Sufficient condition for B ⊄ K:** φ_D is nonzero on some cylinder core. Equivalently, some periodic billiard orbit that closes on X hits D an odd number of times.
- In covering language, φ_D defines a double cover X_D → X. B ⊄ K follows if some cylinder of X lifts to a single cylinder of X_D. This is a monodromy question about the square-tiled surface X_D, close to the Alt(n) monodromy facts in `seed-unbounded/findings.md` §8.4.
- **Limit.** Cores need not span H_1(X; Z/2), so φ_D ≠ 0 alone doesn't finish the proof. Even core loads such as the (2,1) cores here can also be nonzero, so the parity condition is sufficient, not necessary.

## 7. The pocket square: an exact model for every direction

This section develops the parity route by hand (2026-11-02). This section uses no computation. It doesn't prove B ⊄ K in general. It turns blindness in each direction into an exact finite test, and it shows where the global input enters.

### 7.1 The pocket lifts to one square

Use the coordinates of `pocket-detection.md` §2, which translate §1 by (−1,−1). The pocket is B0 = (0,0), A0 = (1,1), C0 = (0,1), with portal x = 0, 0 < y < 1.
- The eight pocket copies form one embedded open square Sq = [0,2]² in X, centered at the single lift of A0.
- B0 (225°) has one lift, of cone angle 10π. It is all four corners of Sq.
- C0 (270°) has two lifts, each of cone angle 6π. One is the midpoints of the left and right sides; the other is the midpoints of the top and bottom sides.
- The D-seams are the two diagonals of Sq. The H-seams are its four half-medians.
- Each of the eight half-sides is one portal image: L_low, L_up, R_low, R_up, Bo_l, Bo_r, T_l, T_r. A billiard excursion into the pocket is one straight passage through Sq.

### 7.2 Q slides the sides of Sq

Give each half-side e the unit vector v_e that points along e toward the nearest corner of Sq.
- **Passage rule.** A passage that enters through e and exits through e' contributes v_e' − v_e to Q. For entry through L_low, this reproduces the six return maps of `pocket-detection.md` §2 with one global sign change. For example, L_low → R_low (DHD) gives 0, and L_low → R_up (DHDH) gives (0,2).
- **Cycle form.** So Q is intersection with the integral cycle Z = Σ v_e·e, with ∂Sq oriented counterclockwise. Its components are Z_x = Bo_r − Bo_l − T_r + T_l and Z_y ≃ T − 2M + Bo, with horizontal pieces oriented in +x.
  - M is the horizontal midline of Sq. It's a saddle connection between the two side midpoints, through the regular center.
  - Z_x and Z_y should be the neck classes β0 and β1 of `pocket-detection.md` §31, up to sign. I haven't cross-checked the orientation convention there.
- **Check.** In the closed 45-45-90 triangle, Sq's opposite sides are glued by translation. That gives X = T₂, and each gluing pairs equal vectors, so Q = 0, as it must.

### 7.3 Parity is "adjacent versus opposite"

- **Odd and even passages.** A passage through adjacent sides crosses one diagonal of Sq, so it's odd. A passage through opposite sides crosses both diagonals, so it's even.
- **Homology form.** So φ_D is mod-2 intersection with L ∪ R, or equally with T ∪ Bo.
- **Passage counts.** In direction θ = (p, q) with p > q > 0, Sq carries 2p + 2q strip passages of height 1/|θ|. The odd passages are exactly those that meet T or Bo, 4q strips in all.

If 2q ≤ p:

| Passage | Strips | Contribution |
|---|---|---|
| L_low → R_low and L_up → R_up | p − 2q each | 0 |
| L_low → R_up | 2q | (0,2) |
| L_up → T_l | q | (−1,−1) |
| L_up → T_r | q | (1,−1) |
| Bo_l → R_low | q | (1,−1) |
| Bo_r → R_low | q | (−1,−1) |

If q < p < 2q:

| Passage | Strips | Contribution |
|---|---|---|
| L_low → R_up | 2(p − q) | (0,2) |
| L_low → T_r | 2q − p | (1,1) |
| L_up → T_l | q | (−1,−1) |
| L_up → T_r | p − q | (1,−1) |
| Bo_l → R_up | 2q − p | (1,1) |
| Bo_l → R_low | p − q | (1,−1) |
| Bo_r → R_low | q | (−1,−1) |

Each table sums to zero, which is §32.1's zero mean restricted to Sq.

### 7.4 Near-axis directions: a six-unit test

Directions (n, 1), n ≥ 0, interpolate from vertical (n = 0) through diagonal (n = 1).
- **Units.** Mark every lattice point of X. Then X is a union of unit squares, and each horizontal unit edge carries one strip in direction (n, 1).
- **Strip permutation.** Let π_0(e) be the top edge of the square above e. Let ρ(e) be the top edge of the right neighbor of the square below e. Then the strip permutation in direction (n, 1) is exactly π_n = ρ^n π_0.
  - ρ has finite order, so π_n depends only on n modulo that order.
  - Each cycle of π_n is a closed leaf of a cylinder in direction (n, 1), so it carries that cylinder's load.
- **Load from units.** By §7.2, a cycle's load depends only on which of six special units it contains: Bo_l and Bo_r (Sq's bottom), M_l and M_r (Sq's midline), and T_l and T_r (Sq's top).

      Q_x = [Bo_l] − [Bo_r] + [T_r] − [T_l],
      Q_y = 2([M_l] + [M_r]) − ([T_l] + [T_r] + [Bo_l] + [Bo_r]).

- **Exact test.** Direction (n, 1) is blind exactly when the cycles of π_n meet the six units in one of these ways:
  - one cycle holds all six;
  - two cycles each hold one M unit, plus Bo_l and T_l on one side and Bo_r and T_r on the other;
  - two cycles each hold one M unit, plus Bo_l and Bo_r on one side and T_l and T_r on the other.
- **Any other pattern loads a core.** A cycle that meets 1, 2, 4, or 5 special units is loaded. A 3-set with the wrong composition is loaded too. A cycle is D-odd exactly when it meets an odd total number of T and Bo units.
- n = 0 is the axis case, which is always blind. n = 1 is the diagonal case, which Section 2 settles.
- Cylinders Cyl_low and Cyl_up contain Sq's lower and upper halves, and both have height 1. So π_n(Bo_l) is the unit n steps along Cyl_low's top from M_l, and π_n(M_l) is the unit n steps along Cyl_up's top from T_l. For n ≥ 2 these leave Sq. The cycles close only through the rest of X.

### 7.5 Mirror rooms

- **Exterior acts as a gluing.** In a mirror room, the exterior's diagonal return is exactly the T₂ gluing of Sq's opposite half-sides: R(y) to L(y) and T(x) to Bo(x).
- **Diagonal cylinders.** So every diagonal X-cylinder that meets Sq crosses it exactly twice. It uses either {Bo_l → R_up, L_up → T_l} or {Bo_r → R_low, L_low → T_r}, and each pair cancels.
- **Near-diagonal directions.** For (n + 1, n), the passages that cross Sq's three diagonal saddle connections carry the load:
  - x − y = 0 (corner to corner): L_low → R_up, (0,2), 2 strips;
  - x − y = 1: Bo_l → R_low, (1,−1), 1 strip;
  - x − y = −1: L_up → T_r, (1,−1), 1 strip.
- **Where loads come from.** The remaining load comes from places where a near-diagonal return crosses a singular diagonal leaf outside Sq. The diagonal multitwist preserves Q in a mirror room (`pocket-detection.md` §33). So the family is periodic in n and blind at n ≡ 0 or −1 (the axis directions).

### 7.6 Which directions are blind for free

`pocket-reflection-gate.md` §7 shows that K is the fixed space of the group generated by the positive multitwists f_θ. Its sum-of-squares identity (7.2) gives two consequences that use only Sq.
- **Per-direction test.** Direction θ is blind exactly when f_θ fixes Z_x and Z_y. Equivalently, Ω(Z, N_θ Z) = 0 for each component, where f_θ = I + N_θ.
- **Axis orbit.** Axis cores never cross Z, so f_h and f_v fix Z in every room. For g in ⟨f_h, f_v⟩, the conjugate g f_h g⁻¹ is a positive multitwist in direction Dg·(1,0) that fixes Z. So that direction is blind too, and likewise for f_v.
- **The axis orbit is thin.**
  - The horizontal cylinder through Sq's lower half has height 1, because B0* lies on y = 0 and C0* lies on y = 1.
  - It contains the two lower squares of Sq, the forced room square s0 = [−1,0]×[0,1] behind the portal, and the mirror copy of s0 behind R_low. So its circumference is at least 4.
  - So f_h has derivative [[1,a],[0,1]] with a ≥ 4, and every direction in the axis orbit is ≡ ±(1,0) or ±(0,1) mod a.
  - The diagonal, and every (n, 1) with n ≢ 0 mod a, lies outside it. This matches the period of π_n in Section 7.4.
- **Mirror rooms.** If the diagonal is blind, f_d fixes Z too. The blind-for-free set grows to the orbits of (1,0), (0,1), and (1,1) under ⟨f_h, f_v, f_d⟩. This is the periodicity of Section 7.5.
- **What a counterexample needs.** A blind room needs Z fixed by a positive multitwist in every rational direction, including those outside these orbits. §33's room fails at (2,1).

### 7.7 Why this doesn't close yet

- **Global input.** Every test in Sections 7.4–7.5 is finite and exact. Each still needs the cycle structure of π_n, which depends on the room far from the pocket.
- **Related problem.** B ⊂ K asks whether the two classes Z_x and Z_y are fixed by every positive multitwist (Section 7.6). This resembles the Putman–Wieland question about invariant homology of finite covers, but the group here is generated only by multitwists.
  - Such invariant classes can exist. In the Eierlegende Wollmilchsau origami, the affine group acts on the non-tautological part H^(0) through a finite group. A multitwist is unipotent, so it fixes H^(0). The sum-of-squares identity (gate (7.2)) then makes every core orthogonal to H^(0).
  - So no general theorem gives B ⊄ K. The proof has to use the room, through Z's support on Sq.
- **What is proved.**
  - The diagonal lemma (Section 2).
  - The six-unit and passage tests (Sections 7.3–7.4), which are exact.
  - §33's room (Section 5).
- **What is not proved.** That in every mirror room, some direction outside the blind-for-free orbits of Section 7.6 moves Z.

## 8. Fixed-room check: (2,1) at every literal pocket in the 57 existing rooms

Daniel approved this check on 2026-11-02. It uses the 31 rooms of `seed-unbounded/study.jsonl` and the 26 of `seed-unbounded/res_rooms.jsonl`, with no new rooms. The only direction is (2,1), fixed in advance.

**Method.**
- A literal pocket follows `pocket-detection.md` §1. It's a leaf triangle B, A, C attached through its axial edge BC, and the wall continues straight past B and past C.
- `existing_rooms_21.py` finds every such pocket. It moves each one by a lattice symmetry onto the §33 position, then runs `core_loads.py` on every (2,1) core that meets D.
- A second tracer reflects off the polygon's own unit wall segments, with a polygon inside test. It must reproduce hits, D, H, and Q for every core.

**Checks.** All pass.
- For every pocket, the triangle count equals twice the polygon area.
- The second tracer matches every core, with 0 mismatches.
- Every strip sum is 0.

**Result.**
- 56 of the 57 rooms have a literal pocket, and there are 210 pockets in all.
- (2,1) loads a core at 148 of 210 pockets. At 104 of them, some core is D-odd.
- At the other 62 pockets, (2,1) is blind. Every blind pocket has exactly 2 cores meeting D. Every loaded pocket has 4 or 6.
- In 9 rooms, every pocket is (2,1)-blind: study 8, 17, 18, 19, 22, and 26, and res 9, 10, and 14.
- Only five Q patterns occur:

| Q values of the cores meeting D | Pockets |
|---|---|
| (0,0) ×2 | 62 |
| (0,2) ×2, (0,−2) ×2 | 44 |
| (1,1) ×2, (−1,1) ×2, (0,−2) ×2 | 40 |
| (1,1) ×2, (−1,−1) ×2 | 36 |
| (1,−1) ×2, (−1,1) ×2 | 28 |

**Local geometry doesn't decide it.** Group the pockets by which triangles of nearby fans are present, in §33 coordinates.
- With the fans at (0,0) and (0,±2), 12 of 46 patterns contain both blind and loaded pockets. Those patterns hold 157 pockets.
- Adding the fans at (2,±2) and (−2,0) still leaves 7 of 92 mixed patterns, holding 48 pockets.
- This supports Section 7.7: whether a (2,1) cycle closes blind depends on the room far from the pocket.

**Conclusion.** (2,1) alone can't be the universal direction. A proof needs a family of directions, or an argument that doesn't name one direction.

## 9. Fixed-room check: every short direction at the 62 (2,1)-blind pockets

Daniel approved this check on 2026-11-02. The pockets are exactly the 62 with no loaded (2,1) core in Section 8. The directions are the seven D4 classes with |θ|² ≤ 25, the same list as Section 5. `blind_pockets_25.py` reuses the Section 8 placement and both tracers.

**Checks.** All pass: the second tracer matches every core with 0 mismatches, and every strip sum is 0.

**Result.**
- Every one of the 62 pockets has a loaded core.
- The diagonal loads at all 62. Each has exactly 2 diagonal cores meeting D, and both are D-odd. That's case (b) of the diagonal lemma (Section 2), so none of these pockets is a diagonal mirror room.

| θ | (1,0) | (1,1) | (2,1) | (3,1) | (3,2) | (4,1) | (4,3) |
|---|---|---|---|---|---|---|---|
| Pockets with a loaded core | 0 | 62 | 0 | 44 | 45 | 31 | 52 |
| Pockets with a D-odd core | 0 | 62 | 0 | 20 | 34 | 15 | 38 |

- With Section 8, every one of the 210 literal pockets in the 57 rooms has B ⊄ K, and (1,1) or (2,1) always detects it.

**Two-direction conjecture (refuted in Section 11).** At every literal pocket of a raw room, the diagonal or the (2,1) direction has a loaded core. Equivalently, no pocket is blind in both directions.
- **Evidence.** All 210 pockets here, and §33's room, which is a diagonal mirror room loaded at (2,1).
- **Gap in the evidence.** Only 2 diagonal mirror pockets are known, and they look alike near the pocket (Section 9.1).
- **Why it's a good target.** By Corollary 1, diagonal blindness is exactly the mirror condition: every diagonal ray from the portal returns to its own point through axial walls only. The conjecture says that this condition and the (2,1) balance of Section 4 can't hold together. That's one concrete statement about two directions, instead of a statement about every direction.
- A proof of the conjecture would prove target 1. It would still leave the S/T coupling obligation in `parity-route-audit.md` §4.

### 9.1 Diagonal mirror rooms are rare (approved follow-up check)

Daniel approved this check on 2026-11-02. `diag_148.py` traces the diagonal cores at the 148 pockets where (2,1) is loaded, with the same placement and both tracers. The second tracer has 0 mismatches.
- At 147 pockets, the diagonal is loaded: 2 cores, each with exactly 1 D hit.
- Exactly one pocket is a diagonal mirror room: study 27, pocket B, A, C = (3,5), (4,6), (4,5). It has one diagonal core with 14 hits and 2 D hits, as in §33's room. Its (2,1) loads are (0,2) ×2 and (0,−2) ×2, also as in §33's room.
- **Both mirror pockets share their local geometry.** In §33 coordinates, both rooms have the full fan at (0,0), the square [0,1]×[1,2], and the leaf triangle at (0,−2), with the same walls next to them. They differ farther out.
- **Consequence.** The conjecture's hard half (a mirror room is loaded at (2,1)) is tested at only 2 pockets, and they look alike near the pocket. The 210-pocket count overstates the evidence.
- **Hand route this suggests.** Corollary 2 already shows that the mirror condition forces local structure. If a finite case analysis shows that it forces this one configuration, then the remaining step is (2,1) near a fixed local shape. Each branch traces the two diagonal families from the portal by hand. A closed branch, such as the box [0,1]×[0,3] in §1 coordinates, leaves no room for interior marks S and T, so it's excluded.

## 10. Hand analysis: what the diagonal mirror condition forces (partial)

This section gives a hand argument (2026-11-02). It uses no computation and §1 coordinates. It doesn't classify mirror rooms. Section 10.6 explains where it stops.

**Setup.** Let U(h) be the ray from the portal point (1,h) with velocity (−1,1), and L(h) the ray with velocity (−1,−1).
- Section 2's palindrome shows that U(h) is the reverse of L(h).
- So the mirror condition says this: for every h in (1,2), U(h) returns to (1,h) with velocity (1,1), and it meets only axial walls on the way.

### 10.1 One itinerary for the whole family

Unfold U(h) by its axial reflections. Reflections in integer lines preserve the lattice and the A sublattice. The developed lines x + y = 1 + h, 1 < h < 2, contain no lattice point. So no ray of the family meets a corner or a wall endpoint, and all U(h) share one wall sequence. The family travels as one band.

### 10.2 Cell structure of the band

In developed coordinates the band is 2 < x + y < 3.
- **Cells.** It alternates T-cells and F-cells.
  - A T-cell is a whole canonical triangle with its hypotenuse parallel to the band. The band enters and leaves through its two legs.
  - An F-cell is a unit square whose canonical diagonal the band crosses at a right angle. So both of its triangles must be in the room.
- **Boundary lines.** The upper line x + y = 3 consists of C points. The lower line alternates A and B points. Every crossed edge joins one point of each line.
- **Ends.** The loop starts with τ1 and then the F-cell [0,1]×[2,3]. That F-cell is why Corollary 2 forces τ3. The loop ends with the upper-left triangle of [0,1]² as a T-cell, then [0,1]×[1,2] as an F-cell, then the portal.
- **Length.** The developed x-length is 2k. So the loop has 4k cells, an odd number of vertical bounces, and an even number of horizontal bounces.

### 10.3 The shortest branch is excluded

Suppose every edge the band meets near the pocket is a wall. Then the loop closes after 12 cells (k = 3) inside the 1×3 box [0,1]×[0,3].
- Every edge of that box is then a wall, so the room is the box plus the pocket.
- It has no interior A point, so it can't hold S and T.
- §33's loop also has 12 cells, but it runs through the full fan at (0,2) and leaves the room open.

### 10.4 Without rawness, mirror rooms are easy

Take the rectangle [−n, 1]×[0,3] with the pocket on its right side. It is a diagonal mirror for every n ≥ 0.
- The ray U(h) meets x = 1 again every 2(n+1) units of travel.
- Its heights there are h, 4 − h, or 2 − h modulo the period 6. Only h lies on the portal, and it arrives with velocity (1,1). The other two land on the flank walls.
- n = 0 is the box of Section 10.3.

Rectangles have interior C points, so they aren't raw rooms. **Any proof that mirror rooms are short or rare has to use rawness.** One local consequence: each C point on the band's upper line is a corner. Where both band edges at that point are interior, the room has exactly 270° there.

### 10.5 Rawness doesn't prune at the band's C points

In a raw room, every C point is a 90° or 270° corner. Its two walls are the legs of one quadrant, so they're axial and perpendicular.

At an upper C point, name the quadrants in the band's developed frame:
- Q1 (SE) is the physical quadrant the band arrives through.
- Q2 (SW) is the T-cell, and Q3 (NW) is the next F-cell.
- Q4 (NE) lies outside the band.

The band crosses two edges at C: e_v (S, between Q1 and Q2) and e_h (W, between Q2 and Q3). After a wall at e_v, the developed W edge folds onto the physical E edge. Rawness then forces this table:

| e_v | e_h | Physical quadrants | Walls at C | Angle |
|---|---|---|---|---|
| open | open | Q1, Q2, Q3 | N, E | 270° |
| wall | open | Q3, Q4, Q1 | S, W | 270° |
| open | wall | Q4, Q1, Q2 | W, N | 270° |
| wall | wall | Q1 | S, E | 90° |

The four raw corner types that contain Q1 match the four wall patterns one to one. So rawness at C points never closes a branch. It only fixes the two walls that the band doesn't cross.

Pruning has to come from elsewhere:
- **Lower B points.** If both band edges at a B point are open, the band covers a 180° half-disk there. Rawness forbids 180° and 360°, so one, two, or three extra triangles sit on the far side.
- **Global embedding.** The folded band has to fit inside one simple polygon, and cells it visits twice have to agree.

**Consequence.** No bound on k can come from rawness at C points alone. A bound needs the B points and the global embedding.

### 10.6 Where this stops

The case tree doesn't close by hand.
- Each band edge is a wall or not, and the band can run through a chain of fans.
- Nothing shown here bounds the loop length k.
- Neither of these is proved: "the mirror condition forces §33's local shape," or the two-direction conjecture.

**Next options.**
- **(a) Bounded enumeration.** Build raw rooms around a pocket up to a fixed radius, and keep those with a closed mirror loop. For each survivor, test (2,1). This is a discovery search, so it needs Daniel's approval.
- **(b) A rawness lemma that bounds k.** Section 10.5 shows that it has to use lower B points or the global embedding. I don't have a candidate yet.

## 11. Bounded enumeration: the two-direction conjecture is false

Daniel approved this on 2026-11-02 ("ok do 1 then 2"). It uses §33 coordinates: pocket B = (1,1), A = (2,0), C = (1,0), with portal x = 1, 0 < y < 1.

### 11.1 Stage A: mirror bands around the pocket (`mirror_bands.py`)

- **Start.** The only fixed cells are the literal pocket, the triangle across its portal, and the straight walls past B and past C.
- **Search.** The search traces one mirror-band ray from (1, 1/3) with velocity (−1,−1). Section 10.1 shows that this one ray stands for the whole band.
  - At each undecided cell the ray enters, the search branches on whether the cell is in the room or is a wall.
  - A diagonal wall ends the branch. After each choice, raw fan rules propagate at every touched lattice point.
- **Box.** The search uses squares i ∈ [1−R, R] and j ∈ [−R, R−1]. It counts a ray that leaves the box as escaped and never drops it silently.

| R | Closed mirror bands | Escaped branches | Longest closed band (crossings) |
|---|---:|---:|---:|
| 3 | 3 | 28 | 24 |
| 4 | 36 | 1,011 | 48 |
| 5 | 26,753 | 998,223 | over 130 |

No branch returned to the portal in the wrong state. Locally, the mirror condition allows many band shapes, and band length grows with the box. Of the 26,753 bands at R = 5, only 1,359 contain the full fan at (0,0).

These are partial rooms. A flood fill from the pocket (`band_space.py`) shows which bands leave space for two full fans:

| R | Closed bands | Closed off, no space | Open or with space |
|---|---:|---:|---:|
| 3 | 3 | 2 | 1 (§33's band) |
| 4 | 36 | 11 | 25 |
| 5 | 26,753 | 1,603 | 25,150 |

The two closed-off bands at R = 3 enclose a 1×3 column plus one square. Stage B checks which open bands complete to real raw rooms.

### 11.2 Stage B: complete to raw rooms, then test (2,1)

`mirror_complete.py` and `min_blind.py` use SAT to complete a closed band to a full room inside the box widened by 4.
- **Room class.** The room is strictly simple, every B and C point is a corner, and it has at least two full A fans for the marks.
- **SAT constraints.** Connectivity and holes are enforced by separator cuts.
- **Tests.** Each completion runs (1,1) and (2,1) through `core_loads.py`. A second tracer that reflects off the room's own walls must match every core.
- **Ordering.** `min_blind.py` enumerates completions in order of a rising triangle cap.

**Results for R = 3, band 0.** This is §33's band, with 18 crossings and 5 wall hits.
- With at most 30 triangles there are 76 completions. All are diagonal mirrors, and 7 are blind in (2,1). The smallest have 28 triangles.
- Ten unrestricted completions of 122–154 triangles include 2 more (2,1)-blind rooms.

**Results for R = 4, bands without §33's full fan.** Six of the 22 open bands were run, with caps of 20 to 60 triangles.
- Bands 1, 10, 11, 13, and 14 have no completion with at most 60 triangles. Their local model is satisfiable, so they may still complete with more triangles.
- Band 34 (24 crossings, 7 wall hits) completes. It has 160 completions with at most 32 triangles, and 75 of them are (2,1)-blind. The smallest have 31 triangles.

So the mirror condition doesn't force §33's local shape.

### 11.3 Independent verification (`verify_blind.py`)

All 9 blind rooms passed these checks, with 0 tracer mismatches. The table shows four of them.
- The original detector `existing_rooms_21.pockets` finds the literal pocket.
- `existing_rooms_21.triangles` rebuilds the same triangle set, and its area matches the polygon.
- The raw test copied from `seed-unbounded/seedcheck.py` passes with 2 interior A marks.
- All seven classes with |θ|² ≤ 25 run, with the polygon tracer of `existing_rooms_21.py` checking every core.

| Room | Triangles | (1,0) | (1,1) | (2,1) | (3,1) | (3,2) | (4,1) | (4,3) |
|---|---:|---|---|---|---|---|---|---|
| smallest | 28 | 0/1 | 0/1 | 0/2 | 4/4 | 4/4 | 4/8 | 6/6 |
| second 28 | 28 | 0/1 | 0/1 | 0/2 | 4/4 | 6/6 | 4/4 | 6/6 |
| large 1 | 149 | 0/1 | 0/1 | 0/2 | 0/2 | 6/6 | 0/4 | 6/6 |
| large 2 | 135 | 0/1 | 0/1 | 0/2 | 4/4 | 6/6 | 0/2 | 6/6 |

Each entry is loaded cores over cores meeting D. Every one of the 9 rooms loads at (3,2) and (4,3), so B ⊄ K holds in all of them.

**All 75 band-34 blind rooms, all seven short directions** (`verify_all_blind_R4_b34.json`). All pass every Section 11.3 check, with 0 mismatches.

| Directions with a loaded core | Rooms |
|---|---:|
| (3,2) and (4,3) | 46 |
| (4,3) only | 27 |
| (3,1) and (4,3) | 1 |
| (3,1), (3,2), and (4,3) | 1 |

None is blind in all seven classes. But 27 rooms of 31 triangles load only at (4,3).

### 11.4 The smallest counterexample is §33's room with one leaf moved

The smallest room equals §33's room except for one triangle. The leaf under the full fan at (−4,0) moves to the other side of x = −4:
- §33's room has ((−5,−1),(−4,−2),(−4,−1)).
- The counterexample has ((−4,−2),(−4,−1),(−3,−1)).

It has 28 triangles, 25 corners, and the same marks S = (−4,0) and T = (0,0). Its corner polygon is in `verify_min_blind_R3_b0.json`, room 0.

Codex verified this room independently on 2026-11-02 (`illumination-k4-codex/parity-sign-theorem/mirror-candidate-review.md`): ACCEPT. Codex's own tracer finds 0 loaded representatives at (1,1) and (2,1), and 12 of 12 at (3,2).

That leaf is 6 units from the pocket. Moving it switches (2,1) from 4 loaded cores to none. The diagonal band doesn't change, so the room stays a mirror.

### 11.5 What this settles

- **Refuted:** the two-direction conjecture of Section 9.
- **Shown:** whether a fixed direction loads depends on geometry far from the pocket. A proof that a fixed direction loads can't use local geometry alone.
- **Not refuted:** B ⊄ K. Every room tested so far has a loaded direction with |θ|² ≤ 25. The margin is thin: 27 rooms of 31 triangles load only at (4,3).
- **Retired:** the k-bound route of Section 10. It only served the two-direction conjecture.

## 12. Bounded search: the seven short classes don't detect every room

Daniel approved this on 2026-11-02 ("yes"). The search looks for rooms blind in all seven classes with |θ|² ≤ 25. It uses §33 coordinates, as Section 11 does.

### 12.1 What ran (`allblind_search.py`)

The scope was fixed in the script's docstring before the run:
- **Bands:** the 25 R = 4 bands that `band_space_R4.json` marks open, plus R = 3 band 0 (§33's band).
- **Completions:** the Section 11.2 SAT model, with a triangle cap that rises 20, 24, …, 40. Each completion is tested once.
- **Limits:** at most 3,000 completions and 20 minutes per band.
- **Short test:** the seven classes run in order (1,1), (2,1), (3,2), (4,3), (3,1), (4,1), (1,0). The test stops at the first loaded class.
- **Long test:** each room that is blind in all seven classes runs every primitive class (p,q) with 0 ≤ q ≤ p and p² + q² ≤ 100. There are 25 such classes.
- **Checks:** the second tracer of `mirror_complete.py` checks every core.

Results:
- Twelve R = 4 bands have no completion with at most 40 triangles: 0, 1, 5, 6, 10, 11, 13, 14, 20, 21, 28, and 29.
- Six bands hit the 3,000-completion or 20-minute limit: R = 3 band 0, and R = 4 bands 2, 7, 15, 26, and 34.
- In total, 15,798 rooms were tested.

### 12.2 Results

- **56 rooms are blind in all seven short classes.** They come from three bands:
  - band 16 (11 rooms, 39–40 triangles);
  - band 26 (41 rooms, 35–40 triangles);
  - band 31 (4 rooms, 39–40 triangles).
- **Every one of the 56 has B ⊄ K.** Each room loads in some class with |θ|² ≤ 41. The first loaded class in the |θ|² order is shown in the following table.

| First loaded class | \|θ\|² | Rooms |
|---|---:|---:|
| (5,1) | 26 | 18 |
| (5,2) | 29 | 18 |
| (5,3) | 34 | 15 |
| (6,1) | 37 | 4 |
| (5,4) | 41 | 1 |

- **No room is blind in all 25 classes** with |θ|² ≤ 100.
- **R = 3 band 0 has none.** Its 3,000 rooms of at most 36 triangles all load at (2,1) or (3,2).
- **The three productive bands are long.** Their diagonal itineraries have 42–48 crossings. Band 34, the Section 11 band, has 24.

### 12.3 Independent verification

`allblind/verify_allblind.py` reruns all 56 rooms through the separate pipeline of `verify_blind.py`:
- `existing_rooms_21.pockets` finds the pocket.
- `existing_rooms_21.triangles` rebuilds the same triangles and area.
- The raw test from `seedcheck.py` passes, with 2 interior marks.
- All seven short classes, plus (5,1), (5,2), (5,3), (6,1), and (5,4), run through `core_loads.py`. The polygon tracer of `existing_rooms_21.py` checks each core.

All 56 rooms pass, with 0 mismatches. Both pipelines agree on which classes load in every room.

Two rooms mark the extremes:
- **Smallest:** band 26, completion 0. It has 35 triangles, 32 corners, and marks (0,−2) and (0,2). The loads are (5,1) 4/4, (5,2) 0/2, (5,3) 0/2, (6,1) 4/4, and (5,4) 6/6.
- **Latest first load:** band 31, completion 1. It has 40 triangles, 37 corners, and marks (0,2) and (2,6). Every class through (6,1) is blind, and (5,4) loads 4/4.

Their corner polygons are in `allblind/verify_allblind.json`.

### 12.4 What this settles

- **Refuted:** the claim that the seven classes with |θ|² ≤ 25, or any subset of them, detect B ⊄ K in every raw room.
- **Not refuted:** larger finite lists. The 25 classes with |θ|² ≤ 100 detect every room tested.
- **Observed, not shown:** the largest first-load |θ|² in this bounded data is 41, in a 40-triangle room. That doesn't show the needed |θ|² is unbounded. Showing that would need a construction or a theorem for every bound.
- **Not refuted:** B ⊄ K. All 15,798 rooms tested have a loaded class, and every class found has |θ|² ≤ 41.
- **Consequence for target 1:** a proof that uses a fixed finite list needs classes beyond |θ|² ≤ 25. Choosing the direction from the room is a reasonable strategy, but the data doesn't make it necessary. (Corrected after Codex's review, 2026-11-02.)

## 13. Extension to rooms of 41–60 triangles

Daniel approved this on 2026-11-02 ("ok go"), after a level-of-effort estimate. It uses the same coordinates and tests as Section 12.

### 13.1 What ran (`allblind60_search.py`)

The scope was fixed in the script's docstring before the run:
- **Bands:** the same 26 as Section 12.
- **Size windows:** 41–44, 45–48, 49–52, 53–56, and 57–60 triangles. Each window runs separately, with at most 500 completions and 4 minutes. A lower-bound constraint keeps every room above 40 triangles, so no Section 12 room repeats.
- **Tests:** the Section 12.1 short and long tests. The second tracer checks every core.

Results:
- The same 12 bands as Section 12 have no completion of 41–60 triangles.
- Each of the 70 windows in the other 14 bands hit its limit. So each window is a partial sample in the solver's order, not a complete enumeration.
- In total, 31,602 rooms were tested, using 3.5 CPU hours.

### 13.2 Results

- **166 rooms are blind in all seven short classes.** They come from the same three bands as Section 12:
  - band 16 (81 rooms, 41–59 triangles);
  - band 26 (19 rooms, 41–45 triangles);
  - band 31 (66 rooms, 41–59 triangles).
- **Every one of the 166 has B ⊄ K.** The first loaded class in the |θ|² order is shown in the following table.

| First loaded class | \|θ\|² | Rooms |
|---|---:|---:|
| (5,1) | 26 | 46 |
| (5,2) | 29 | 62 |
| (5,3) | 34 | 56 |
| (6,1) | 37 | 1 |
| (5,4) | 41 | 1 |

- **No room is blind in all 25 classes** with |θ|² ≤ 100.
- **The first-load |θ|² doesn't grow with room size in this data.** The largest value per size window is 37, 34, 41, 34, and 34. The 59-triangle rooms first load at (5,3).
- In the three productive bands, 166 of 5,445 rooms (3.0%) are blind in all seven classes.

### 13.3 Independent verification

`allblind60/verify_allblind60.py` runs the Section 12.3 pipeline on all 166 rooms. All 166 pass, with 0 mismatches. The two pipelines agree on which of the 12 classes load in every room. The rooms have 37–53 corners.

Two rooms mark the extremes:
- **Smallest:** band 16, completion 0. It has 41 triangles, 37 corners, and marks (−4,2) and (0,2). The loads are (5,1) 0/2, (5,2) 4/4, (5,3) 6/6, (6,1) 4/4, and (5,4) 4/4.
- **Largest:** band 16, completion 75. It has 59 triangles, 53 corners, and marks (−4,0) and (0,2). The loads are (5,1) 0/2, (5,2) 0/2, (5,3) 6/6, (6,1) 4/4, and (5,4) 4/4.

Their corner polygons are in `allblind60/verify_allblind60.json`.

### 13.4 What this adds

- **Section 12.4 stands unchanged.** The 25 classes with |θ|² ≤ 100 detect every room tested. Sections 12 and 13 together test 47,400 distinct rooms.
- **Observed, not shown:** the largest first-load |θ|² stays 41 from 35 to 59 triangles. That supports trying a fixed finite list for target 1. It doesn't prove that any list works.
- **Limits:** every productive window stopped at its limit, so these are samples, not complete enumerations. R = 5 bands weren't tested.

## Files
- `mirror_bands.py` and `mirror_bands_R{3,4,5}.json`: Section 11.1.
- `mirror_complete.py`, `mirror_complete_R3.json`, `min_blind.py`, `min_blind_R3_b*.json`, `min_blind_R3_b*.log`: Section 11.2.
- `verify_blind.py`, `verify_blind_R3_band0.json`, `verify_min_blind_R3_b0.json`, `verify_min_blind_R4_b34.json`, `verify_all_blind_R4_b34.json` and `.log`: Section 11.3.
- `band_space.py` and `band_space_R{3,4,5}.json`: Section 11.1.
- `allblind_search.py`, `allblind/R*_b*.json` and `.log`: Section 12.1–12.2.
- `allblind/allblind_rooms.json`, `allblind/verify_allblind.py`, `allblind/verify_allblind.json` and `.log`: Section 12.3.
- `allblind60_search.py`, `allblind60/R*_b*.json` and `.log`: Section 13.1–13.2.
- `allblind60/allblind60_rooms.json`, `allblind60/verify_allblind60.py`, `allblind60/verify_allblind60.json` and `.log`: Section 13.3.
- `min_blind_R4_b*.json` and `.log`: Section 11.2, R = 4.
- `core_loads.py`, `core_loads.json`, and `core_loads.log`: main computation.
- `independent_trace.py` and `independent_trace.log`: second tracer.
- `certificate-3-2.log`: hit lists for the odd (3,2) core and one (2,1) core.
- `existing_rooms_21.py`, `existing_rooms_21.json`, and `existing_rooms_21.log`: Section 8.
- `blind_pockets_25.py`, `blind_pockets_25.json`, and `blind_pockets_25.log`: Section 9.
- `diag_148.py`, `diag_148.json`, and `diag_148.log`: Section 9.1.
