# Unbounded actual-seed existence (Section 26.4 without W ≤ 26)

Claude, 2026-11-01. Assigned by Codex on the board; Daniel approved. Theory only, with no discovery scans.

**Status: open.** No proof or counterexample exists. Proved: the reduction to one finite orbit test per room (Sections 1–3), actual generation by seed loops (Section 4), and the one-sided limit lemma (Section 6.1). Open: bounded-length existence and the k = 1 shortening (Section 6.2). Fixed-room evidence for the Section 7.6 route is in Sections 8.4 and 8.5. Section 10 proves three W-free special cases and explains why its local arguments don't reach the general case. Section 11 audits Codex's triangle-closing rule.

## Target
Let P be a raw, strictly simple canonical room with distinct interior A marks S and T. Find a primitive w that isn't parallel to a wall, and a developed path S → c → T′ with both halves equal to w. Here c is one physical corner, T′ is a lift of the actual T, and the continuation at c bounds an embedded π-sector. Alternatively, prove that no such path exists for some room in the class.

## 1. The midpoint is forced (parameter-1 lemma)
- Let X be the unfolding, with 8 copies. Every glue map preserves 2Z², and every axis or diagonal wall offset contributes an even translation. So X is a translation cover of the torus T₂ = R²/2Z².
- X is branched only over the four 2-torsion points: O (class A), B (1,1), and C (1,0) and (0,1).
- Take any primitive w that isn't parallel to a wall. The developed ray from S meets no lattice point before parameter 1. At parameter 1 it reaches S + w, which is a B or C point. Rawness makes that point a physical corner.
- So every corner-free ray from S stops exactly at parameter 1. This restates the parity darkness certificate.
- No lattice point lies strictly between parameters 1 and 2, so the second half can't hit a corner. The point at parameter 2 is an A point.
- **Consequence.** A seed exists if and only if the π-continuation through the parameter-1 corner lands exactly on a lift of T at parameter 2. Equal halves and the single corner come free. The only freedom is the choice of w and the side of the π-sector.

## 2. Monodromy form
- Consider the closed geodesic γ_w of T₂ through O in direction w. It passes through exactly one other 2-torsion point, h_w = w mod 2, at its midpoint.
- Push γ_w off h_w to the left or right, giving the based loops γ_w^±.
- Corners of 45° and 90° lift to regular points of X, so both pushes agree there. Corners of 135°, 225°, 270°, and 315° lift to cone points (Section 7.1).
- At a cone corner with cone angle 2πn, the two π-continuations are exactly the two pushes. Continuations of 3π or more correspond to extra winding, and Section 1 excludes them.
- **Seed criterion.** Let μ be the monodromy of X over T₂ minus its 4 branch points. Some T-lift lies in {μ(γ_w^±)·s : w primitive, not wall-parallel}.

## 3. Origami form (exactly decidable for each room)
- Use the unit-square origami (r, u, labels) of `origami_frame.py`, based at the S square s. Apply A ∈ SL2(Z) with A·w = e1.
- The two seed endpoints are the lower-left labels of r²(s) (push up) and r·u·r·u⁻¹(s) (push down).
- **Criterion.** A seed exists if and only if some element of the finite SL2(Z) orbit has label T at one of those two squares. The element must come from a direction that isn't wall-parallel.
- Horizontal shears leave both words unchanged, so each direction contributes at most 2 endpoints. The seed set from s is a finite union over the orbit.
- Per room this is a finite exact check. I haven't run it on any room, because that would be a direction scan.

## 4. What this rules out and what remains
- **No covering obstruction (actual generation, corrected after Codex review).**
  - Base the loops at a tangential point b near O, not at O. O ramifies at partial A corners, so a basepoint at O isn't well defined.
  - Let F₂ = ⟨r, u⟩ = π₁(unit torus minus 0, b). Then π₁(T₂°, b) is K = ker(F₂ → (Z/2)²), which is free of rank 5.
  - `generation.py` writes each push of γ_w as a reduced word and runs Stallings folding. The loops generate K exactly when the folded graph is the 4-vertex covering graph.
  - **Result.** Up and down pushes over non-wall-parallel w with |w|² ≤ 10 (32 loops) generate K. This holds at four different tangential basepoints. With |w|² ≤ 5, the folded graph has 21 vertices and isn't a cover.
  - Up pushes alone don't appear to generate K: the folded graph kept growing (17 to 57 vertices) without closing. Both sides are needed.
  - **Scope.** Generation rules out only an obstruction that every seed loop shares, such as an intermediate cover X → Y → T₂ separating S from T. It says nothing about one loop at a time, which is what the seed needs.
- **The remaining difficulty.** The condition uses one loop, not a product. Transitivity of the monodromy group is therefore not enough. The bounded proof found its seeds in two local configurations with |T − S| = 4. For W > 31, I ≥ 3 and the S–T fan path can be long, so w has to be long.
- **Next step.** Use the cylinder structure in direction w: s and a T-lift on one boundary component of a cylinder, two unit steps apart, with the parameter-1 corner between them. Try to force this configuration from the fan-tree merger on the S–T path (Sections 24 and 27). Alternatively, find an in-class room whose finite orbit avoids T at both words. Finding that room would need Daniel's approval for a fixed-room orbit check.

## 5. Fixed-room test: no counterexample in 26 raw rooms (Daniel approved)
- **Rooms.** `seedcheck.py` takes raw models (kmax = 0) from Codex's frozen encoder, then re-checks them as simple and raw. Raw means every non-A lattice point in the closed room is a vertex.
  - Controls: 3 rooms with I = 2 and W = 24, which the bounded theorem covers.
  - Tests: 23 rooms with I = 3 to 5, W = 36 to 65, and |S − T| = 8 to 16 along the full-star chain. The shapes are straight chains (including wider gaps), an L, a diagonal chain, and a zigzag.
- **Check.** The seeds come from the origami orbit test in Section 3. The search stops after 3 seeds or 3 million states.
  - Every hit is re-verified by an exact physical walk. Both halves reach the same corner at parameter 1, and a π-sweep fold check passes at that corner.
- **Result.** 26 of 26 distinct rooms have seeds, and every listed hit verifies. The largest orbit needed was 909 states.
  - Seed length grows with |S − T|. Straight chains give (−7,2) for |S − T| = 8, (−9,2) for 12, and (−24,7) for 16.
- **Reading.** This is evidence that the assertion holds, not a proof. The test found no counterexample. Next is a proof for chains, for example by matching the pattern (−(2j+1), 2) to the corridor geometry. Output is in `results.jsonl` and `run*.out`.

## 6. Proof attempt for chains: what the seeds actually do
- **Seeds are global, not local.** In every chain room the seed's first half leaves S away from T and reflects off the far end cap. It then reaches c and continues to T after reflecting off the other cap. For example, S = (0,0), T = (8,0), and w = (−7,2) give c = (5,0) by folding at both ends. The straight-chain pattern (−(2j+1), 2) reflects the corridor length, not a local mechanism near the merger. So no local hand proof along the fan path follows from these rooms. The rooms' corridors are also pinched to height 1 at the C notches between stars, so no clean rectangle-fold model applies.
- **Seed corners are cone corners (corrected).** The original note said "reflex" and called one hit "convex". That hit is a 135° B corner (`anomaly.py`), which is a cone point. Section 7.1 proves that every S→T seed uses a cone corner: 135°, 225°, 270°, or 315°. Of the 78 verified hits, 46 use 270° C corners and 32 use cone B corners.
- **One-sided limit lemma (precise; replaces the earlier sketch).** Section 6.1 states and proves it.
- **Exact remaining gap.** Section 6.2 lists it.

### 6.1 One-sided limit lemma under a length bound
**Definitions.**
- Marked points of X are all lifts of room vertices and of interior A marks. Each one projects to a 2-torsion point of T₂.
- A *lit segment* from s is a straight segment in X that starts at s and meets no marked point except at s.
- Fix a primitive w and a side ε ∈ {up, down}. The *ε-walk* from s in direction w is the path that starts at s in direction w. At each marked point it meets, it leaves by the prong at link angle π on side ε. At an unmarked or regular point, it goes straight.
- Write W_w^ε(s, x) for the walk point at arclength x|w|. The walk meets 2-torsion lifts exactly at integer x. Even x gives O-lifts, and odd x gives h_w-lifts.
- Every O-lift is unlit from s: a segment with displacement 2kw passes the marked h_w-lift at parameter 1. So the hypothesis on t̂ in the lemma always holds.
- In the origami of Section 3, W_w^up(s, 2k) is the lower-left label of r^{2k}(s), and W_w^down(s, 2k) is the label of u r^{2k} u⁻¹(s).

**Lemma.** Let t̂ ≠ s be a marked O-lift that isn't lit from s, and fix L > 0. The following are equivalent:
- (a) There are points q_n → t̂, with q_n ≠ t̂, each the endpoint of a lit segment from s of length at most L.
- (b) t̂ = W_w^ε(s, 2k) for some primitive w, side ε, and k ≥ 1 with 2k|w| ≤ L.

**Proof of (a) ⇒ (b).**
1. Let the segment to q_n have unit direction θ_n and length ℓ_n ≤ L. Pass to a subsequence with θ_n → θ and ℓ_n → ℓ.
2. The developed endpoints s̄ + ℓ_n θ_n project to π(q_n) → O in T₂. So ℓθ ∈ 2Z². Since t̂ ≠ s, ℓ > 0. Write ℓθ = 2k w with w primitive and k ≥ 1. So the limit direction is rational, and ℓ = 2k|w| ≤ L.
3. The point at parameter 1 on the ray in direction w is a B or C lift, which rawness makes a marked corner. If θ_n = θ infinitely often, those segments stop before it, so ℓ_n < |w|. That contradicts ℓ_n → 2k|w|. So θ_n ≠ θ for large n. Pass to a subsequence on one side ε of θ, at angles α_n → 0⁺.
4. **Strip chart.** Choose 0 < δ < 1/|w|. Let H be the open developed strip {s̄ + t·ŵ + y·ε·ŵ^⊥ : 0 < t < L + 1, 0 < y < δ}.
   - Integer points off the line s̄ + Rw lie at distance at least 1/|w| from it. So H contains no integer point, and its image in T₂ avoids the four branch points.
   - X minus its marked points is an honest covering of T₂ minus the branch points. H is simply connected, so it lifts uniquely to a chart Φ: H → X once you fix the germ at s on side ε. Φ may be immersed rather than embedded; that doesn't matter.
   - Every marked point develops to an integer point, so Φ(H) contains no marked point.
   - Φ extends continuously to the edge y = 0. At each marked point on that edge, the lifted strip occupies a half-disk on side ε, so the edge leaves by the prong at angle π. So the edge is the ε-walk: Φ(t, 0) = W_w^ε(s, t/|w|).
5. The lit segment at angle α_n on side ε starts at s and develops to s̄ + t(cos α_n·ŵ + sin α_n·ε·ŵ^⊥). It stays in H while t·sin α_n < δ, which holds for all t ≤ L once n is large. Both the segment and Φ lift the same path from the same germ, so they agree. So q_n = Φ(ℓ_n cos α_n, ℓ_n sin α_n).
6. By continuity of Φ, q_n → Φ(2k|w|, 0) = W_w^ε(s, 2k). Limits in X are unique, so t̂ = W_w^ε(s, 2k).

**Proof of (b) ⇒ (a).** Take the segment from s at angle α on side ε with length 2k|w|. For small α > 0, it lies in Φ(H), which has no marked point, so it's lit. Its endpoint tends to t̂ as α → 0⁺.

**Sheet and prong convergence.** Step 5 identifies the sheet of q_n through the chart Φ, not through developed coordinates. At each cone point on the walk, Φ selects the side-ε prong. So the limit is a specific T-lift, not only a point over O.

**Consequences.**
- A seed in the sense of Section 1 is exactly case (b) with k = 1 and w not wall-parallel.
- The set of boundedly approachable O-lifts is ⋃_{w,ε} ⟨ρ_w^ε⟩·s, where ρ_w^ε = W_w^ε(·, 2) as a permutation of O-lifts. These are the O-lifts on the same side-ε cylinder boundary component as s, in some direction.
- Seeds are the first step of each orbit: ⋃_{w,ε} {ρ_w^ε(s)}.

### 6.2 What stays open
- **Bounded-length existence (separate obligation).** Lelièvre–Monteil–Weiss gives lit points q → T, but not lit segments of bounded length. Segments to q with displacement 2v + δ, where |v| ≫ 1/|δ|, are generic and don't track any walk. So LMW doesn't imply (a).
- **No shortening by affine maps.** An affine automorphism maps the ε-walk in direction w to an ε′-walk in direction Dw, and it preserves the step index j. So the Veech group can't turn k ≥ 2 into k = 1. A shortening has to change the T-lift or the direction, not transport the walk.
- **No shortening along the walk.** For k ≥ 2, the consecutive O-lifts on the walk are pairwise seeds (Section 7.2), which gives only a chain S → A₁ → … → T. Turning a chain into one seed needs a transitivity property of the seed graph, which isn't proved.
- **Status.** Neither a shortening lemma nor an in-class obstruction exists. The evidence in Section 8 favors existence, with k = 1 seeds in 17% to 34% of orbit states.

## 7. Structural lemmas (proved)

### 7.1 Regular corners retro-reflect, so seeds need cone corners
- Let τ be the D4 element −I acting on X. It is an isometry with derivative −I, it fixes every corner lift, and it preserves physical labels.
- At a corner lift with cone angle 2πn, τ rotates the link by πn.
- A corner of interior angle 45° or 90° has n = 1. Corners of 135° and 270° have n = 3, 225° has n = 5, and 315° has n = 7.
- If n = 1, the straight continuation from s through c ends at τ(s), which is an S lift. So a seed between distinct S and T uses a corner with n ≥ 3.

### 7.2 Corner-prong form of the seed relation
- Fix a cone corner lift c and a primitive w ≡ c (mod 2) that isn't wall-parallel. The 2n prongs of c in directions ±w sit at link angles kπ and alternate in sign.
- Each prong reaches an A lift at parameter 1 with no corner in between. Call its label ℓ_k. Because of τ, ℓ_(k+n) = ℓ_k.
- The seeds through c in direction ±w are exactly the cyclically adjacent pairs {ℓ_k, ℓ_(k+1)}.
- Physically, the n prong directions are the images of one direction u under the group generated by the two flank reflections at c, restricted to the room sector at c.

### 7.3 Triple lemma for n = 3
- At 135° and 270° corners, n = 3, so every pair among {ℓ_0, ℓ_1, ℓ_2} is a seed pair.
- Take a 270° corner p whose missing quadrant is IV, and a, b > 0 with (a, b) ≡ p (mod 2). The three prongs are the physical directions (a, b), (−a, b), and (−a, −b).
- So the three A points reached from p by billiard paths of length |(a, b)| in those directions are pairwise joined by seeds through p.

### 7.4 Every full fan has four 270° portals
- Let S be a full fan. Each C point S ± e1 and S ± e2 carries the two S triangles (180°) plus 0, 1, or 2 neighbor triangles of 90° each.
- Rawness excludes 180° and 360°. So each of the four C points is a 270° corner with axis-parallel flanks.
- Every interior A mark is therefore at distance 1 from four cone corners with n = 3.

### 7.5 Relation to Codex Section 26.5
- Take any seed with direction w, and any v with det(v, w) = ±1. Each half then crosses one integer strip of direction v, so the seed is an instance of the adjacent-strip construction of Section 26.5.
- So Section 26.5 is a complete criterion, not only a sufficient one. The open question is still whether the strip incidences exist.

### 7.6 Cylinder-adjacency form and coprime coverage (proved; formula checked)
**Cylinders.** Fix any primitive strip direction w, including wall directions, and v with det(w, v) = 1.
- Developed lattice lines parallel to w are s̄ + iv + Rw. Even i gives *O-lines* (O and h_w points). Odd i gives *BC-lines* (the two other classes).
- Every integer point on a BC-line is a B or C lift, so rawness makes it a marked corner. The open strip between consecutive lines has no integer point.
- So every cylinder of X in direction w has height exactly 1/|w|. It has one O-boundary and one BC-boundary, and its circumference is 2q|w| for an integer q.
- *Type I* cylinders have the O-boundary at the bottom; *type II* have it at the top. A BC corner of cone angle 2πn has 2n half-disks that alternate between type I below and type II above.

**Seed form.** Let C be the type I cylinder above s, with half-circumference q. Take w′ = mw + v.
- The first half crosses C and stops at the corner c_m = s̄ + v + mw on C's top. c_m depends only on m mod 2q.
- At c_m, the two π-continuations enter the type II half-disks H_± next to C's half-disk, across the prongs ±w. Let C_± be their cylinders, with half-circumferences q_±.
- The second half crosses C_± and ends at an O-lift on its top.
- In the origami with w = e1, the two endpoints are lab(u r^m u r^m s) and lab(u r^(m+1) u r^(m−1) s).
- This is the strip criterion of Section 7.5 and Codex Section 26.5, made explicit at the level of cylinders.

**Coprime coverage lemma.** Fix a corner c of C's top and a side ±. As m runs over one residue class mod 2q, the endpoints run over the O-lifts on the top of C_± in steps of 2q|w|.
- So they cover q_±/gcd(q, q_±) of the q_± O-lifts there.
- If gcd(q, q_±) = 1, s is joined by a k = 1 seed to every O-lift on the top of C_±. Wall-parallel w′ excludes at most four values of m, so it doesn't matter.
- At a regular corner, τ maps C to C_±, so q_± = q and you get only τ(s). This agrees with Section 7.1.

**Check.** `cylinder.py` compares the origami formula with the orbit test (r² and r u r u⁻¹ after mapping (m, 1) to e1). It covers room 11 of `study.jsonl` and four rooms of `res_rooms.jsonl`, with |m| ≤ 12. All 125 comparisons agree. A negative control that shifts one exponent by 1 mismatches in 13 to 20 of 25 values per room.

**Use.** An S→T seed exists if, in some direction w, the type I cylinder of an S-lift is corner-adjacent to a type II cylinder with a T-lift on top, with coprime half-circumferences. The same holds with the sides reversed. This condition is sufficient, not necessary. It is not proved to hold in every room: in room 11 it fails for all four wall directions (Section 8.3).

## 8. Evidence from fixed rooms (approved checks)

### 8.1 All pairs of A points are seed-connected in 57 rooms
- `reach.py` runs the orbit test with physical A labels. For each non-corner A point as the source, it records which A labels appear at r²(b) or r u r u⁻¹(b) from a direction that isn't wall-parallel.
- Rooms: the 26 rooms of Section 5 and the 31 rooms of `study.jsonl`. Non-corner A points include full fans and wall midpoints, 3 to 10 per room.
- **Result.** In all 57 rooms, every ordered pair of non-corner A points is joined by a seed. The largest orbit prefix needed was 951 states. Output is in `reach*.out`.

### 8.2 Seeds are a fixed fraction of all directions
- `density.py` counts the orbit states, up to 750,000 per room, whose direction gives a seed from S to T. Every room hit the cap, so these are prefix fractions.
- In all 31 rooms of `study.jsonl`, the fraction is 0.17 to 0.34. A model with independent, uniformly distributed prong labels predicts 0.23 to 0.55 (`model.py`). The observed values are about 0.6 to 0.75 of the model value.
- Short directions are sparse. The room with the longest fan path (9 fans) has 1 seed with |w| ≤ 13, but about 25% of all orbit states are seeds. The seeds exist at longer w.

### 8.3 Strips parallel to a wall don't suffice
- `farey.py` tests every w with det(v, w) = ±1 for the four wall directions v, with |n| ≤ 80.
- In `study.jsonl` room 11 (W = 53, S = (0,0), T = (8,4)), none of these w is a seed. The horizontal and vertical cylinder periods are 120, so those two families are complete.
- That room's shortest seed has w = (8, 5) through the 270° corner (5, 2). Its strip partners are (3, 2) and (5, 3), which aren't wall directions.
- So a proof can't rely only on wall-direction strips, whose combinatorics are explicit.

### 8.4 The even subgroup acts as the alternating group on every fiber
Daniel approved this check on 2026-11-02. It's a group computation on the 57 fixed rooms, with no search. Script and output: `mono/mono.py`, `mono/mono.out`.
- K = ker(F₂ → (Z/2)²) is generated by r², u², [r, u], r u² r⁻¹, and u r² u⁻¹. Stallings folding confirms this. K has 4 orbits on squares, the fibers over the 4 unit squares of T₂.
- **Result.** In all 57 rooms, K acts on each of the 4 fibers (sizes 37 to 78) as exactly Alt(n).
  - Each action is primitive (Atkinson's minimal-block test).
  - Each contains an element with a single cycle of prime length p, where n/2 < p ≤ n − 3. Jordan's theorem then gives Alt(n) ⊆ image.
  - Every generator is even on every fiber, so the image is Alt(n), not Sym(n).
- **Consequence.** No intermediate cover X → Y → T₂ exists in these rooms, so an imprimitivity obstruction is ruled out there. A proof along this line still needs the SL2(Z) orbit of the based origami to equidistribute in its Nielsen class. That question is open in general.

### 8.5 Strip directions: few cylinders, coprime adjacency, and q = 1
Daniel approved this check on 2026-11-02. It covers the 57 fixed rooms and the 264 strip directions w with |w| ≤ 12. Script and output: `fewcyl/fewcyl.py`, `fewcyl/all.out`.
- For each w, the script builds the state with M e1 = w by Euclid on SL2(Z). The cylinders are the R-cycles. The endpoint set of the whole strip family is E_w(s) = {u r^m u r^m s, u r^(m+1) u r^(m−1) s : m ∈ Z}. Each endpoint residue class holds infinitely many m, so the at most four wall-parallel w′ never matter.
- **Validation.** The script compares the formula with exact physical walks (`verify`) for |m| ≤ 3 on the first 40 directions of each room. It finds 0 mismatches in 12,540 comparisons. An earlier run without the copy-frame map had 4 mismatches in room 11, all from the frame −I.

| Measure, over directions with \|w\| ≤ 12 | Range over the 57 rooms |
|---|---|
| Strip families that contain an S→T seed | 76% to 99% |
| Directions where the Section 7.6 coprime criterion holds | 40% to 77% |
| First coprime direction | \|w\|² ≤ 13 in every room |
| Minimum cylinder count | 2 (10 rooms), 4 (30), 6 (13), 8 (3), 10 (1) |
| Directions where s's cylinder has q = 1 | 0.8% to 4.9% |

- **Few cylinders.** A two-cylinder direction has one type I and one type II cylinder, each with q = N/4. So the coprime lemma never applies there. The full E_w(s) still hits T in every minimum-cylinder direction of every room.
- **Wall directions.** 35 of the 57 rooms have a seed in some wall-direction strip family. Room 11 has none, which matches Section 8.3.
- **q = 1.** Then gcd(q, q_D) = 1 for free, and s reaches every A-lift on top of the at most two type II cylinders above it. In 56 of 57 rooms, some q = 1 direction with |w| ≤ 12 also has a T-lift there. These directions are rare, so q = 1 isn't a better route than the general coprime criterion.
- **Heuristic link to Section 8.4.** If the cylinder data in a direction behaves like the cycle type of a random element of Alt(n), two adjacent cycles are coprime with probability near 6/π² ≈ 0.61. The observed 40% to 77% is consistent with this heuristic. No theorem makes it rigorous.

## 9. What a proof needs
- **No covering obstruction.** Section 4 shows that up and down seed loops generate π₁(T₂°) at a tangential basepoint. This excludes only an obstruction that all seed loops share.
- **No affine shortening.** Section 6.2 shows that affine maps preserve the walk index k.
- **No local or wall-strip argument.** Seeds are global (Section 6), and wall-direction strips miss some rooms (Section 8.3).
- **Most concrete sufficient condition.** Section 7.6 needs one direction with a coprime corner-adjacency between the cylinders of an S-lift and a T-lift. Proving that such a direction always exists would close the problem. In the 57 fixed rooms it holds in 40% to 77% of short directions (Section 8.5), so the condition has a wide margin.
- **Group-theoretic route.** K acts as Alt(n) on every fiber in all 57 rooms (Section 8.4). Equidistribution of the SL2(Z) orbit in its Nielsen class would turn the coprime heuristic of Section 8.5 into a proof. That step is the open part.
- **Remaining route.** Seed existence is a statement about the finite SL2(Z) orbit of the labeled, based origami. The base label must reach every other A label in one step. A proof needs the orbit to be large or mixing for this family of surfaces.
- The literature classifies SL2(Z) orbits of origamis only in small strata, for example H(2) (Hubert–Lelièvre, McMullen). It has no result of this kind for unfoldings of large rooms.
- **Conjecture (stronger than the target).** In a raw, strictly simple canonical room, every two distinct non-corner A points are joined by an admissible one-corner seed.

## 10. Proof attempt for every room (2026-11-02)
Section 9 seeks a proof that every raw room has a coprime direction. This attempt doesn't reach it. It proves three W-free lemmas and explains why these local arguments don't close the general case.

### 10.1 Corner form of the coprime criterion (proved)
- Fix a cone corner lift ĉ with n = 3 and a strip direction w0 with ĉ on a BC-line. Let C_0, C_1, C_2 be the type I cylinders that hold the three half-disks below ĉ, with half-circumferences q_j.
- The prong from sheet j in direction −(m w0 + v) crosses C_j and ends at position a_j − m on C_j's O-boundary. τ maps each down prong to an up prong with the same label, so any two of the three down-prong labels form a seed pair. This is Section 7.3 restated in the strip.
- **Criterion.** Suppose an S-lift sits on C_i's O-boundary and a T-lift on C_k's, with i ≠ k. By the Chinese remainder theorem, some m puts both on the prongs when a_i − p_S ≡ a_k − p_T (mod 2 gcd(q_i, q_k)). If gcd(q_i, q_k) = 1, parity alone decides it, and the parity always matches.
- This is Section 7.6 re-centred on the corner. It's the same condition, but it names the corner, which is what a geometric proof would have to produce.

### 10.2 Visible-midpoint lemma (proved, any W)
Suppose T − S = 2w with w primitive, and the closed segment [S, T] lies in the closed room. Then S and T are joined by a seed in direction w through c = S + w.
- c has class w mod 2 ≠ 0, so it's a B or C point in the closed room. Rawness makes it a corner.
- w isn't wall-parallel. If w = ±e_i, the C point between S and T carries 360° from two full fans. If w = (±1, ±1), the B point between them carries 180°. Rawness excludes both, as in Section 27.1.
- The open halves contain no lattice point and run along no wall, because w isn't wall-parallel. So they lie in the open room and hit nothing.
- Both germs at c, −w and +w, are interior to c's single sector. So the sector exceeds π, which makes c a cone corner (225°, 270°, or 315°). The arc of length π between the germs is embedded.

### 10.3 Fan distance 2 (proved, any W)
Suppose full fans S and T have a common portal neighbor M. Then a seed exists, with direction (2, 1) up to symmetry.
- Section 26.4's connected-H argument already proves this. It uses W ≤ 26 only to classify H, not to build the seed.
- The shape of M follows from rawness alone.
  - Spacing: S = (0,0), M = (2,0), T = (4,0). A perpendicular step would make S and T diagonal neighbors.
  - Reflect so that the S portal is (1,0)–(1,1). Then M contains UL = [M,(1,0),(1,1)] and not LL, or the point (1,0) carries 360°.
  - M's arc is contiguous. To reach a triangle at (3,0) it must pass U1, U2, and UR, and it must stop there, or (3,0) carries 360°.
  - So M is exactly the upper half-star, and Section 26.4's construction applies unchanged.

### 10.4 Straight upper corridor (proved, any length)
Let S = (0,0) and T = (2k, 0), with k ≥ 2, and suppose every triangle of [0, 2k] × [0, 1] lies in the room. Suppose also that c = (k, 1) has a horizontal wall ray.
- **Claim.** A seed exists in direction (k, 1) through c, reflecting at that ray as in Section 26.4.
- For even k, c is a C point. Its lower quadrants are present, so rawness makes it a 270° corner with axis flanks. One horizontal ray is then always a wall.
- For odd k, c is a B point of 225°, 270°, or 315°. The hypothesis fails only when both upper 45° triangles next to the horizontal rays are present.
- This gives unbounded fan distance, but only for this corridor shape.

### 10.5 Why local arguments can't finish
- **Short seeds disappear at fan distance 3.** `study.jsonl` has a straight corridor S = (0,0), (2,0), (4,0), T = (6,0) whose shortest seed has |w|² = 29. That seed is w = (2, 5) through the middle portal corner (3, 0). Its halves reflect off walls outside the corridor, so it isn't forced by the corridor's tiles.
- **Coprimality needs global data.** The half-circumferences q_j are lengths of closed billiard paths through the whole room. Lemmas 10.2 to 10.4 avoid cylinders entirely, which is why they're local, and why they only cover special shapes.
- **First coprime directions vary.** The first coprime direction ranges over |w|² ∈ {1, 2, 5, 10, 13} across the 57 rooms (Section 8.5). This doesn't exclude a universal finite family: every one of the 57 rooms has a coprime direction with |w|² ≤ 13. A finite-family theorem would still need cylinder data, which is global. (Corrected 2026-11-02 after Codex's review. An earlier version said no fixed set works and that the first direction grows with complexity; neither was shown.)
- **Conclusion.** The route this file follows needs an orbit-level theorem: equidistribution of the cusp data of X's SL2(Z) orbit, given Alt(n) monodromy (Section 8.4). I don't know of such a theorem for origamis outside small strata. This is one route, not a proved necessity; Section 11 records another candidate. A counterexample, if one exists, needs an invariant that the 57 rooms don't show.

## 11. Triangle-closing rule (Codex brainstorm candidate 3, audited 2026-11-02)
Full audit: `../review-triangle-closing/findings.md`. Verdict: ACCEPT WITH PRECISIONS.
- **Rule.** Take edges ŝ → â and â → t̂ with half-vectors u and v, det(u, v) = ±1, and both π-sides on the turning side. If the X-angle at â matches the Euclidean angle, then ŝ → t̂ is a seed with half-vector u + v. This holds automatically at a regular apex: interior, 45°, 90°, or 180°. The proof lifts the empty triangle conv(0, 2u, 2u + 2v) through the unbranched cover.
- **Converse.** Every seed splits into its two Farey-parent edges, in infinitely many ways, so the rule is 2 out of 3.
- **Fan distance 2** (Section 10.3) is one move with apex at the half-star M.
- **Fan distance 3, straight corridor.** The move with apex M1 leaves the tree at the 135° corner (2,2), and M2 is a 270° A corner. The tree path doesn't supply a chain there.
- **Status.** The rule is valid and local. A global lemma would need a strengthened induction on fan distance that controls Farey intervals and π-sides, and none is in hand.

