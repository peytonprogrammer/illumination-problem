# General geometry 03: coverings of an ordered-spiral unfolding give no reduction

Fable, 2026-11-08, revision 2 after reviewer findings F3, F5, F7–F10 (`review/general-spiral-completeness-fable-findings.md`, `-fable-return-findings.md`). Hand proofs. Independent review requested.

Retired from revision 1 (false or unproved, kept here for provenance):
- "Room-compatible coverings exist only for metrics with common period structure" (F3). False: the coordinate-mod-lattice torus cover exists for every lattice room.
- "A covering cannot merge reflex corners because cone points map to cone points" (F5). False.
- Lemma C as an equivalence ("S lights T iff S~, T~ lie on one closed leaf of an open cylinder with no marked point") (F7). The "open set of directions" step is false for a fixed target, and a legal finite segment need not extend to a bad-set-free leaf. Only the sufficient direction survives, and it is not used below.
- Lemma G as stated (whole cylinder unmarked; "≤ 6" as a bound on legal states) (F8). Withdrawn.
- "No accepted theorem covers all L-rooms" (F9). False: the accepted W ≤ 8 base covers every L-room with real metrics and actual endpoints.
- "deg f ∈ {2,3}" for L-folds (F9). Degree 2 is impossible; see Proposition 1.

Result of revision 2. Two proved negatives and one exact reformulation:
1. (Proposition 1) A fold map from an ordered spiral onto a room with fewer reflex corners is either a rectangle fold or a degree-3 fold onto an L-room; the latter exists only on a 4-parameter subfamily of the 8-parameter chart.
2. (Proposition 2) Every torus covering of O_D that is lifting-safe for Corollary R(b) is vacuous for even-even pairs whenever D has a corner of parity class A. For such rooms, torus coverings transfer nothing in either direction.
3. (Lemma M) With the chosen target lift kept, the covering formulation of illumination is exactly the project's vertex walk (result 12). The structural route therefore reduces the ordered-spiral milestone to that finite walk, not to a smaller room, unless O_D has a degree-3 unramified cover onto a genus-2 surface with one 6π cone (reviewer F5 constraint), which is decided per room by a block-system test (section 4).

## 1. Fold maps and Proposition 1

A fold map f: D → D0 between orthogonal rooms is a continuous surjection, locally an isometry on interiors, sending walls into walls, and locally a reflection across each interior point of D lying over a wall of D0. A fold map lifts to a translation covering O_D → O_{D0} that commutes with the sheet symmetries (file 01, section 1); conversely such an equivariant covering descends to a fold map. This section classifies fold maps only. Non-equivariant translation coverings are treated in section 4 and are not classified here (F10).

Angle count. At q ∈ D with interior angle α(q) ∈ {90, 180, 270, 360} degrees (convex corner, wall point, reflex corner, interior point) and f(q) with angle α0, the fold map multiplies angles: α(q) = k(q) α0 for a positive integer k(q) ≤ deg f. So over a reflex corner of D0 (270) every preimage is a reflex corner with k = 1; over a convex corner (90) preimages have k ∈ {1,2,3,4} (convex corner, wall point, reflex corner, interior point); over a wall point, k ∈ {1,2}; over an interior point, k = 1. Summing local degrees over a reflex corner of D0:

    r(D) = deg(f) · r(D0) + #{reflex corners of D lying over convex corners of D0}.     (*)

Proposition 1. Let D be an ordered spiral (r = 3) and f: D → D0 a fold map with deg f ≥ 2. Then either D0 is a rectangle, or deg f = 3, r(D0) = 1 (an L-room), and D is tiled by three mirror copies of D0.

Proof. From (*), deg(f) r(D0) ≤ 3, so r(D0) ∈ {0, 1}. r(D0) = 0 gives a rectangle. If r(D0) = 1 then deg f ∈ {2, 3} and (*) says 3 − deg f reflex corners of D lie over convex corners of D0 with local degree 3. For deg f = 2 that is one such corner with k = 3 > deg f, impossible. So deg f = 3 and no reflex corner lies over a convex corner. A fold map of degree d exhibits D as a union of d copies of D0 with disjoint interiors, adjacent copies being mirror images across their common wall. □

Parameter count. An L-room has 4 metric parameters and finitely many ways to place three mirror copies; the spiral chart has 8. So spirals admitting an L-fold form a finite union of 4-parameter subfamilies. On those subfamilies Corollary R(b) lifts the accepted L-room paths (F9), but lands on one of the three points of f⁻¹(f(T)); choosing the right sheet is not provided by the fold. This is recorded as a special subfamily with an unproved endpoint step, not as coverage.

Rectangle folds. If D0 = [0,p]×[0,q] (D a union of p×q blocks), then O_{D0} is the torus R²/(2pZ×2qZ). The composite O_D → O_{D0} is the coordinate-mod-(2pZ×2qZ) map. Its endpoint behaviour is Proposition 2 with Λ = 2pZ × 2qZ.

## 2. Proposition 2: torus coverings are vacuous for rooms with an A-class corner

Let Λ be a sublattice of Z² such that φ_Λ: O_D → R²/Λ, p ↦ developed position mod Λ, is well defined. Crossing a vertical wall x = k identifies developed positions differing by (2k, 0), so well-definedness needs (2k, 0) ∈ Λ for every wall abscissa k, and similarly for ordinates. Λ = Z² always works (reviewer F3) and Λ = 2Z² always works; for a room with a wall at an odd coordinate, 2Z² ⊆ Λ is forced. φ_Λ is a translation covering branched over images of reflex corners. Let P ⊂ R²/Λ be the set of images of all corners of D.

Corollary R(b) (lifting) needs P ⊆ Bad_0. Theorem E and Corollary R(a) (projection) need that no non-corner point of the closed room lies over Bad_0.

Proposition 2. Let 2Z² ⊆ Λ ⊆ Z², let S, T be even-even interior points, and let Bad_0 ⊇ P. A straight segment in R²/Λ from φ_Λ(S) to φ_Λ(T) with interior avoiding Bad_0 exists only if there is v ∈ Z² \ {0}, v = 2^j w with w ∉ 2Z², such that T ≡ S + 2v (mod Λ), the classes [2^i w] (0 ≤ i ≤ j) contain no corner class of D, and 2^i w ∉ Λ for 1 ≤ i ≤ j. In particular, if D has corners in each of the parity classes A, B, C, the base is dark for every such Λ and Bad_0, and Corollary R(b) lifts nothing.

Proof. The segment develops from S to T' with T' a lift of T, so T' − S ∈ 2Z²; write T' − S = 2v, v ≠ 0. The points S + 2^i w, 0 ≤ i ≤ j, are lattice points in the interior of the segment. Since S is A-class and 2Z² ⊆ Λ, the point S + 2^i w lies over the class [2^i w] modulo Λ. For i ≥ 1, if 2^i w ∈ Λ the point lies over [0] = φ_Λ(S), which is the image of every A-class point, including an A-class corner if one exists, so it is in P ⊆ Bad_0. Otherwise it lies over a non-zero class, which must not be a corner class. For i = 0 the class [w] is non-zero and must not be a corner class. If all three classes occur among corners, the i = 0 condition already fails for every v. □

For an ordered spiral with corners in all three parity classes (the general case: corners sit at (a,b), (a,h), (w,h), (w,c), (l,c), (l,0), (A,0), (A,H), (0,H), (0,b), and the classes are forced to spread as soon as the metrics have mixed parities), the torus covers transfer nothing in either direction. For the all-even metrics of the accepted families every corner is A-class and the base is dark too. The one-mark torus (Λ = Z²) and the four-mark torus (Λ = 2Z²) are distinct cases of the same statement (reviewer F10).

Reviewer F10 asked for the four-mark torus and the one-mark torus to be kept distinct. They are: with Λ = Z² there is one mark and every segment of even displacement passes through it; with Λ = 2Z² there are up to four marks and the condition above applies.

## 3. Lemma M: the chosen-lift condition is the vertex walk

Keep the chosen target lift T~ (nonemptiness-next.md). Let θ = (p, q), gcd(p,q) = 1, be a rational direction and consider the straight ray from S~ in direction θ on O_D. Its development is the line S + t(p,q). The lattice points on it are S + n(p,q), n ≥ 1; the point with n even is A-class, with n odd is class (p,q) mod 2. In O_D each such point is either a corner lift (ray ends, illegal beyond) or an interior/wall lattice point (transparent, ray continues).

Lemma M. S lights T along direction θ with the chosen lift T~ if and only if there is n ≥ 1 with S + 2n(p,q) developing to T~ and all 2n − 1 intermediate lattice points S + m(p,q), 1 ≤ m ≤ 2n − 1, transparent on the sheet the ray occupies at that moment. The map σ_θ: (A-lift x) ↦ (A-lift at developed position x + 2(p,q) along the ray from x), defined when the two intermediate points are transparent, is a partial injection on the finite set of A-lifts, and S lights T in direction θ iff T~ ∈ {σ_θ^n(S~) : n ≥ 1}.

Proof. A legal segment from S~ to T~ is straight, so it is the ray above with the stated displacement; the parity of displacement is 2Z² because both endpoints are even-even lifts. Legality is transparency of the intermediate lattice points on their sheets. Injectivity of σ_θ: σ_{−θ} is its inverse on the image. Finiteness: there are 4I A-lifts. □

This is the project's result 12 restated with the lift kept. The union over θ of the σ_θ-orbits of S~ is the set of lit lifts. A general existence theorem must show T~ lies in that union; a dark pair is exactly a pair where it never does. No covering argument changes this set: by Propositions 1–2 the only coverings available for a generic spiral are tori, and those cannot see the orbit.

Coordination with the author's return map. Fix θ. The author's left-mouth return relation on (position, signed direction) is, in this language, the first-return map of σ_θ-iteration to the set of A-lifts in the source arm, composed with the direction sign changes recorded on the sheet. Because σ_θ is a partial injection on a finite set, the forward orbit of S~ is a finite chain: it either reaches T~, ends at a corner, or returns to S~ (a cycle). The author's return map inherits this trichotomy: iterates from the S-exit state either reach the T-entry state, end at a corner, or cycle back to the S-exit state; no other behaviour exists, and cycling back is a genuine possibility, not an error. A return-map proof therefore has to exclude "corner" and "cycle back to S without passing T" for some θ. This is the exact intersection property the author needs; the structural side supplies nothing stronger.

## 4. The remaining covering case and a finite test

By the reviewer's F5 count, a nontrivial translation covering from O_D (genus 4, three 6π cones) to a surface of genus ≥ 2 must be unramified of degree 3 onto a genus-2 surface Y with one 6π cone (Y ∈ H(2)), all three cones of O_D lying over the one cone of Y. Whether such Y exists is a property of the monodromy of O_D over its period torus: intermediate covers O_D → Y → torus correspond to block systems of the monodromy permutation group with blocks of size 3 (standard Galois correspondence for coverings; the claim that every translation covering of a square-tiled surface factors through its period-torus map is used here and should be cited from the origami literature before this section is relied on). For a spiral whose monodromy group is primitive there is no such Y, and sections 1–3 are the whole story for coverings. I do not know which spirals have primitive monodromy; deciding it is a finite computation per room and is not requested.

Even when Y exists, Corollary R(b) lands on one of three points of the fiber over φ(T~), and no accepted theorem covers all of H(2) square-tiled surfaces with marked points, so Y is not a "covered case" today.

## 5. Status

- Proved: Propositions 1 and 2, Lemma M.
- Retired: the six statements listed at the top.
- Open: Lemma F (frontier) is, by Lemma M, equivalent to the vertex-walk statement for all coverings available to a generic spiral; the structural route gives no reduction of the ordered-spiral milestone. The degree-3 genus-2 case is a per-room finite test, not a general reduction.
- No nonemptiness progress. Full ordered/r3/r ≤ 8 goal open.
