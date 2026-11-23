# D145: review of clean-site-cost.md (snapshot 2026-11-22 02:15)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/clean-site-cost.2026-11-22-0215.md`. It's byte-identical to `qclass-closure/bbbb/clean-site-cost.md`. Context read: `corner-support.md` and `corner-support.py`, `fold-converse.md` (excerpt), `search-plan.md`, the d68 and d69 READMEs, and the d143 and d144 reviews and scripts.

Code: [checks.py](checks.py), log [checks.log](checks.log), 0.03 CPU-seconds. It uses exact integer and Fraction arithmetic on 4 named rooms: R22, cov4181, a 3-cell L-room, and the V-notch B (angle arithmetic only). It runs no search and makes no network calls. Its billiard tracer is new code, written independently of d8's tracer, so the archived routes are replayed by a second implementation.

## Verdict

**Sound with gaps.** No gap is high. Every arithmetic claim checks. The weaknesses are about what the claims mean:

- The "exactly six" count is a statement about R22's fixed geometry. It restates the nine-singleton result of `corner-support.md`, sorted by midpoint class.
- The six certificates occupy only 4 of the 12 residual cells.
- The R22 fold check excludes degree 2 for a trivial reason: 2 doesn't divide 15.
- Claims (2) and (4) are d68's Corollary C and Lemma B, restated in torus language.
- Nothing in the note gives a wall lower bound for BBBB rooms. The note says so itself.

## 1. Claim (1) on R22

**Room.** The d144 construction from the manuscript gives the same 15 cells as d8's `R22-base`. Both axis gcds of the wall lengths are 1, so Per(X) = 2ℤ² and d = n = 15.

**Clean site contents.** The table shows the fiber count 4i + 2b + f + 3r per parity class. Here i, b, f and r count interior points, smooth wall points, convex corners and reflex corners.

| Class | i | b | f | r | Fiber | Clean |
|---|---:|---:|---:|---:|---:|---|
| (0,0) | 2 | 2 | 3 | 0 | 15 | no |
| (1,0) | 0 | 2 | 2 | 3 | 15 | no |
| (0,1) | 0 | 2 | 2 | 3 | 15 | no |
| (1,1) | 0 | 0 | 6 | 3 | 15 | yes |

The corner-only site (1,1) holds 6 convex and 3 reflex corners, and 15 = 6 + 3·3. This matches d143's 9 forbidden and 0 regular X points. The site blocks the holonomy class w ≡ (2,2) mod 4ℤ² for each of the 4 target sheets. That's 4 of 16 cells, as claimed.

**Replay of the routes.** Each route is replayed as two legs: one from S = (0,0) and one backward from T = (2,2). For all 9 archived routes, the replay confirms these facts:

- Both legs stop at the stated reflex C.
- The arrival velocities are exact negatives, so the route continues straight through C.
- Every other lattice point on the route is a smooth wall point or an interior point.
- The developed endpoint D is consistent with the target sheet: D − g·T ∈ 2ℤ².

The six routes through axial reflexes:

| C | Steps | D | Target sheet | D mod 4ℤ² | Midpoint (physical, class) |
|---|---|---|---|---|---|
| (0,−1) | 1+3 | (−32, 44) | I | (0,0) | (2,−2), even-even smooth point |
| (0,1) | 1+1 | (−4, 2) | diag(−1,1) | (0,2) | C, class (0,1) |
| (1,−2) | 1+1 | (14, −8) | diag(1,−1) | (2,0) | C, class (1,0) |
| (1,2) | 1+1 | (6, 4) | −I | (2,0) | C, class (1,0) |
| (3,2) | 1+1 | (18, 4) | −I | (2,0) | C, class (1,0) |
| (4,1) | 1+1 | (8, 14) | diag(−1,1) | (0,2) | C, class (0,1) |

Each route passes through exactly one corner, its own reflex. None of them meets the three odd-odd reflexes. No midpoint lies on the corner-only site. The three odd-odd routes have D ≡ (2,2) mod 4 and midpoints on site (1,1), so the site test blocks them, as the note's split requires.

**What "exactly six" means.** R22 has exactly 6 axial reflexes.

- **Lower bound.** Each singleton route forces its own reflex into every blocking set, so any blocking set contains all 6.
- **Upper bound.** With all 6 stopped you have the original room, which is dark by the manuscript.

So "exactly six" means "all six". It's both a lower and an upper bound, but only in R22.

**What "indispensable" proves.** Fix R22's walls and the relaxed straight-through rule. Then every set of reflex stops that blocks all relaxed routes contains that reflex. This is a minimum over stop sets for one fixed room. It says nothing about rooms with other walls. The sum 3 + 6 = 9 and "W = 22" are R22's own counts, not a derived lower bound.

## 2. Claim (2): n = f_x + 3r_x

**Derivation.** Let X be the four-sheet translation unfolding, so its area is 4n. If both axis gcds are 1, then Per(X) = 2ℤ². The wall-and-half-turn loop gives twice each wall vector as a period. Reflections in integer lines give only even translations. So the torus R²/2ℤ² has area 4, and d = 4n/4 = n.

Over an integer site x, the X points come from physical lattice points of parity x:

- an interior point gives 4 points of degree 1;
- a smooth wall point gives 2 points of degree 1;
- a convex corner gives 1 point of degree 1 (cone angle 2π);
- a reflex corner gives 1 point of degree 3 (cone angle 6π).

So n = 4iₓ + 2bₓ + fₓ + 3rₓ. Here fₓ is the number of **convex corners of parity x**. At a clean site iₓ = bₓ = 0, which gives n = fₓ + 3rₓ. Summing over the four classes recovers Pick's formula.

**Checks.** The four-class identity holds in every room checked.

| Room | n | W | Clean classes |
|---|---:|---:|---|
| R22 | 15 | 22 | (1,1): 15 = 6 + 3·3 |
| cov4181 | 28 | 20 | (1,0): 28 = 7 + 3·7, as claimed |
| L-room {(0,0),(1,0),(0,1)} | 3 | 6 | (0,0): 3 = 3 + 0, and (1,1): 3 = 0 + 3·1 |

The angle inequality d|Z| ≤ M(W−2)/2 holds in all three rooms. For orthogonal rooms it reads n|Z| ≤ 2W − 4.

The V-notch row is an equality case: Σ Mθ/2π = 2 + 2 + 1 + 6 + 1 = 12 = 3·4. Its lift degrees agree with d143's four corner-only sites.

## 3. Claim (3): the fold budget

**Derivation.** Q is the room's double, a sphere. Every point of Q over a pillowcase corner x has local degree e ≤ 3 over B:

- e = 1 at convex corners;
- e = 2 at smooth points and interior points (these are the q points);
- e = 3 at reflex corners.

Write the local degree of Q → B as (degree of Q → N) × (degree of N → B).

- **At a zero of N,** N → B has degree at least 3. So the zero is simple, and it has k unramified preimages, all of them reflexes.
- **At a pole of N,** the preimages satisfy b₁ + 2b₂ + 3b₃ = k.

Every point over J is a pole or a zero. So qₓ = b₂ and rₓ = kzₓ + b₃, which gives b₃ ≥ rₓ mod k. The ramification of Q → N over J is at least Σ(b₂ + 2b₃). Riemann–Hurwitz between two spheres gives −2 = −2k + R, so R = 2k − 2. The inequality is correct.

**R22.** The off-source classes have (q, r) = (2,3), (2,3) and (0,3). At k = 3, with J the three off-source classes, the cost is 4 = 2k − 2. The budget is tight, and checks.py reconstructs the forced fiber data:

- Each class in J has one zero and two poles, with (b₁, b₂, b₃) = (2,2,0), (2,2,0) and (6,0,0). In each case b₁ equals fₓ.
- The class (0,0) has 1 pole and 2 regular points of N, so N has degree 5 over B.
- N has 7 poles and 3 simple zeros, and 7 − 3 = 4, as a sphere requires.
- N's canonical double has genus 4 and area 20. This matches the 20-square, genus-4 quotient that d143 found.

The 4 units sit at the four smooth seam endpoints (−1,0), (1,0), (2,1) and (2,3), as claimed.

**Degree 2.** k must divide n = 15, so no fold of inner degree 2 exists. The inequality isn't needed for this. It also excludes k = 2 only when J contains an axial class. For J = {(1,1)} the cost is 2 ≤ 2, so it passes.

## 4. Claim (4): BBBB has no corner-only fiber

**Definition.** `search-plan.md` defines BBBB as a normalized room in which every canonical factor Nₓ equals B. "Normalized" means both axis gcds of the wall lengths are 1, as used in `band-reachability.md`.

d68 Lemma B says a class has type Q (Nₓ = Q) exactly when it has no interior point and no smooth wall point. So BBBB implies that every parity class has a regular point. On R²/2ℤ² that means no fiber is corner-only.

Any translation map from X to a torus R²/L has the form dev + const, with L ⊇ Per(X) = 2ℤ². Each of its fibers is a union of whole 2ℤ²-fibers. Non-integer sites carry no corners at all. So claim (4) holds on every torus quotient, and it's consistent with the definition.

It is equivalent to "no Q class" and uses nothing else from BBBB. A room with a proper non-B factor and no Q class also satisfies it.

## 5. Scope

The note gives **no wall lower bound for BBBB rooms**:

- The direct charge in claim (2) needs a clean fiber, and claim (4) shows BBBB has none.
- The fold charge in claim (3) needs a proper factor with corner-only classes. BBBB excludes such canonical factors.
- The incremental count in claim (1) is an R22-only minimum in the relaxed model.

Two things remain open:

- A cost, in reflexes, for a developed-path obstruction in a room that has neither a clean fiber nor a proper corner-only factor.
- A proof that darkness forces min_A(|A| + Σ hₓ(A)) ≥ 9 in the `corner-support.md` formula, or any weaker statement that yields nine stops.

cov4181 shows that counting reflexes on relaxed routes of one failed class can't supply that cost.

## Gaps

1. **Medium. "Exactly six" and "W = 22" are R22 facts, not bounds.** R22 has exactly 6 axial reflexes, so "exactly six" means "all of them". The proof is `corner-support.md`'s singleton argument restricted to the axial reflexes. "Indispensable" shows only this: within R22's fixed walls and the relaxed straight-through rule, every blocking set of reflex stops contains that reflex. The note should say that "3 + 6 = 9, so W = 22" recounts R22's walls and gives no lower bound for other rooms.
2. **Medium. The certificates occupy 4 of the 12 residual cells.** The six routes land in these cells: (I, 0), (diag(−1,1), (0,2)) twice, (diag(1,−1), (2,0)), and (−I, (2,0)) twice. The other 8 residual cells carry no certificate. The note correctly declines to divide the six stops among cells. But "the other 12 need exactly 6 more" reads as coverage of all 12 cells. State the joint claim and list the 4 occupied cells.
3. **Low. Degree 2 is excluded trivially in R22.** k must divide n = 15. The inequality excludes k = 2 only when J contains an axial class, and J = {(1,1)} passes with 2 ≤ 2. The k = 3 analysis is correct, but it assumes that both axial classes have only poles and zeros in N. That's a hypothesis, satisfied by the d143 staircase quotient. It isn't derived.
4. **Low. Claims (2) and (4) are known results.** n = fₓ + 3rₓ is d68 Corollary C. For one clean site, the angle bound n ≤ 2W − 4 is d68's n ≤ 4r + 4. Claim (4) is "no Q class" from d68 Lemma B. Cite them, and define fₓ as the number of convex corners of parity x. Also define "normalized" as both axis gcds equal to 1, because d = n depends on it.
5. **Low. The source-sheet symmetry remark isn't needed.** Every archived route starts at S on sheet I by construction. For the (0,−1) route, the midpoint is the smooth point (2,−2), not a corner. The note's "even-even" is correct.
