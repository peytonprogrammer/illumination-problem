# General geometry 01: optical lifting in covering form

Fable, 2026-11-08, revision 2 after reviewer findings F1, F2, F6 (`review/general-spiral-completeness-fable-findings.md`). Hand proof. Independent review requested. This file proves the path-lifting statement that the structural route needs before any reduction is used, and the covering-form darkness theorem. It proves no new illumination result for the ordered spiral.

Changes from revision 1: Lemma L now requires an unramified starting lift (F1). The deck action is described as affine, not translation (F2). The de Winter–Tokarsky instance uses the torus R²/(2Z)² with four marked points instead of the reflection orbifold, so Theorem E applies inside one category (F6).

## 1. Setting

Room. D is a simple orthogonal polygon with vertices on Z². Corners(D) is its vertex set; reflex corners have interior angle 270°, convex corners 90°. A legal path from S to T is a finite billiard trajectory that starts at S, ends at T, reflects specularly on walls, and meets no corner. S and T are interior points.

Unfolding. O_D is the four-copy unfolding: copies g(D) for g in Γ = {id, ρx, ρy, ρxρy}, glued along walls so that crossing a vertical wall passes from copy g to copy gρx and crossing a horizontal wall passes to copy gρy. The developed-position charts make O_D a closed translation surface. Write π: O_D → D and Lift(p) = π⁻¹(p); an interior point has four lifts.

Sheet symmetries (F2). The maps that permute the four copies act in the charts by the linear parts id, diag(−1,1), diag(1,−1), diag(−1,−1). They are affine isometries of O_D, not translations. They preserve the set of straight segments and the bad set, and they change a direction by the corresponding sign flips. So a legal path from one lift of S to a lift of T gives a legal path from any other lift of S, in the transformed direction. Nothing below needs more than this.

Marked points. A convex corner q has one preimage q* in O_D, a regular point. A reflex corner has one preimage, a cone point of angle 6π. Bad_D is the set of these preimages. A legal path from S to T is the same thing as a straight segment in O_D from a point of Lift(S) to a point of Lift(T) whose interior avoids Bad_D.

Translation covering. φ: X → Y between translation surfaces is a translation covering if it is a continuous finite-degree surjection that is a translation in charts away from a finite set Br(φ) ⊂ Y, and a covering map over Y \ Br(φ). Over a branch value the local model is z ↦ z^k with k ≥ 2. A cone point of X of angle 2πm maps to a point of angle 2πm' with m = k·m' for the local degree k; in particular a 6π cone can map with k = 3 to a regular point (reviewer F5).

## 2. Lemma L (optical lifting)

Lemma L. Let φ: X → Y be a translation covering and E ⊂ Y a finite set containing Br(φ). Let γ: [0, ℓ] → Y be a straight segment with γ(t) ∉ E for 0 < t < ℓ, and let x0 ∈ φ⁻¹(γ(0)) be a point at which φ is unramified (local degree 1). Then:

1. There is a unique continuous γ~: [0, ℓ] → X with γ~(0) = x0 and φ∘γ~ = γ. It is a straight segment of the same direction and length.
2. γ~(t) ∉ φ⁻¹(E) for 0 < t < ℓ.
3. Conversely, if δ: [0, ℓ] → X is a straight segment whose interior avoids φ⁻¹(E), then φ∘δ is a straight segment in Y of the same direction and length whose interior avoids E.

Proof. (1) Since φ is unramified at x0, there is a neighbourhood U of x0 on which φ is a translation onto a neighbourhood of γ(0). Lift γ|[0, ε) by the inverse translation. For t ∈ [ε, ℓ) the path lies in Y \ E ⊆ Y \ Br(φ), where φ is a covering map, so the lift continues uniquely. At t = ℓ the lift extends by continuity because the lift on [0, ℓ) has finite length and φ is proper. Straightness and length follow because φ is a local translation along the interior. Uniqueness: on [0, ε) by the local inverse, on [ε, ℓ) by unique path lifting for covering maps.

(2) If γ~(t) ∈ φ⁻¹(E) with 0 < t < ℓ then γ(t) ∈ E, excluded.

(3) φ∘δ is continuous and locally a translation image of a straight segment on (0, ℓ), hence straight with the same direction and length; if φ(δ(t)) ∈ E then δ(t) ∈ φ⁻¹(E), excluded. □

Remark (F1). If x0 is a ramified point of local degree k, the base direction has k outgoing prongs at x0 and the lift is not unique; a prong must be specified. In every application below the starting point is a lift of an interior room point, which is a regular point of O_D with local degree 1 under every translation covering, so the hypothesis holds. The segment's endpoint γ(ℓ) may lie in E; the lift still ends at a unique point.

## 3. Corollary R (which bad-set inclusion each transfer needs)

Let φ: O_D → O_0 be a translation covering with finite marked set Bad_0 ⊇ Br(φ). For interior S, T of D and S~ ∈ Lift(S):

(a) Projection. If φ⁻¹(Bad_0) ⊆ Bad_D and δ is the development of a legal path from S~ to a lift T~, then φ∘δ is a legal segment in O_0 from φ(S~) to φ(T~).
(b) Lifting. If Bad_D ⊆ φ⁻¹(Bad_0) and σ is a legal segment in O_0 from φ(S~) to y1, then the lift of σ from S~ is a legal segment in O_D from S~ to some point of φ⁻¹(y1).

Proof. (a) is Lemma L(3) with E = Bad_0; (b) is Lemma L(1)–(2), S~ being regular. □

Part (b) ends at some point of φ⁻¹(y1), not at a chosen one. Any reduction that uses (b) to prove illumination must separately show the lift ends at T. Nothing in this file provides that.

## 4. Theorem E (darkness descends through coverings)

Definition. y0 in a translation surface Y with marked set Bad_Y is self-dark if every straight segment σ: [0, ℓ] → Y with σ(0) = σ(ℓ) = y0, ℓ > 0, and σ(t) ≠ y0 for 0 < t < ℓ, meets Bad_Y \ {y0} at some 0 < t < ℓ.

Theorem E. Let φ: O_D → O_0 be a translation covering with Bad_0 ⊇ Br(φ). Suppose
1. φ⁻¹(Bad_0 \ {y0}) ⊆ Bad_D,
2. y0 is self-dark in O_0,
3. S ≠ T are interior points of D with Lift(S) ∪ Lift(T) ⊆ φ⁻¹(y0).
Then S does not light T in D.

Proof. Let δ: [0, ℓ] → O_D be the development of a legal path from S~ to a lift T~. Let 0 = t0 < t1 < … < tn = ℓ be the times with δ(t) ∈ φ⁻¹(y0); finitely many since the fiber is finite and δ is straight; n ≥ 1 since ℓ > 0. On each (t_i, t_{i+1}) the segment avoids φ⁻¹(y0) and avoids Bad_D ⊇ φ⁻¹(Bad_0 \ {y0}), so it avoids φ⁻¹(Bad_0). The starting point δ(t_i) is a regular point of O_D unless it is a cone point; cone points lie in Bad_D, and δ avoids Bad_D except possibly at t = 0 and t = ℓ where δ is at S~ and T~, regular. So each δ(t_i) is regular and Lemma L(3) applies: φ∘δ|[t_i, t_{i+1}] is a straight segment from y0 to y0 whose interior avoids Bad_0, in particular avoids y0 and Bad_0 \ {y0}. That contradicts hypothesis 2. □

Note on hypothesis 1. It is the first inclusion of Corollary R, restricted to Bad_0 \ {y0}. It fails exactly when some non-corner point of the closed room lies over a marked point other than y0. For the torus instance in section 5 that is a transparent B or C lattice point.

## 5. The de Winter–Tokarsky class, torus version (F6)

Torus. Let T = R²/(2Z)² with Bad_0 = {[0,0], [1,1], [1,0], [0,1]} and y0 = [0,0]. The classes are the A, B, C parity classes of Z².

Covering. Define φ: O_D → T on copy g by p ↦ g(p) mod (2Z)². Across a vertical wall x = k (k integer) the two copies g and gρx agree at wall points because g(k, y) and gρx(k, y) differ by (2k, 0) ∈ (2Z)²; similarly for horizontal walls. In the developed charts φ is the identity modulo (2Z)², so it is a translation covering of degree area(D), branched only over images of cone points, which are integer points, hence in Bad_0. This is the reviewer's coordinate-mod-lattice cover (F3) with the lattice 2Z² chosen so that the three parity classes stay distinct.

Claim. y0 is self-dark in T. Proof. A straight segment from y0 to y0 develops to a segment from (0,0) to (2i, 2j) ≠ (0,0). Its midpoint (i, j) is an integer point. If (i, j) ∈ (2Z)², the segment passes through y0 in its interior and is excluded by the definition. Otherwise the midpoint lies in Bad_0 \ {y0}. □

Consequence. For an orthogonal lattice room D in which every lattice point of parity class B or C in the closed room is a corner, hypothesis 1 of Theorem E holds, and every pair of distinct even-even interior points is dark. This is the project's trivial fold class, now obtained inside the translation-surface category. The accepted reflection-fold proof is not replaced; this is a second derivation.

For a spiral with transparent B or C points, hypothesis 1 fails and Theorem E says nothing. The actual paths in such rooms pass through transparent lattice points at their midpoints, which φ sends into Bad_0. So this φ is useless for lifting (Corollary R(b)) as well: legal torus segments from y0 to y0 do not exist. Any torus-based reduction has to mark fewer points on the torus and then loses hypothesis 1 for projection. That is the exact sense in which "a failed route is not darkness" on this route.

## 6. What this file does not do

It does not provide a covering for the ordered spiral (file 03). It does not prove the converse of Theorem E. It changes no accepted result.
