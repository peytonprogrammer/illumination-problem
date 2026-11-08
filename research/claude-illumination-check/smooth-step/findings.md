# Single smooth blocker, rational orthogonal rooms: attempt notes

Claude, 2026-11-01. Builds on Codex's `single-boundary-blocker/{findings.md,critical-leaf.md}`, which Claude reviewed earlier.

## Where the rational case stands
In a rational orthogonal room with an essential smooth blocker z, every connection has one of two forms (Codex, `critical-leaf.md` §4):
- **(A)** a segment of a saddle connection between reflex-corner lifts;
- **(B)** a segment of the central core of an ι-invariant cylinder, with z separating s and t on the folded corner-to-corner arc.

## What I tried, and why it doesn't close
- **Affine-group bypass.** Let H be the finite-index group of affine maps of the unfolding M that fix every marked lift: corners, s, t, z. This is step 1 of Theorem 24. Each φ ∈ H maps a connection through b to a connection through b = φ(b). It also maps saddle connections to saddle connections and ι-invariant cylinders to ι-invariant cylinders.
  - **Lemma (proved).** Forms (A) and (B), and passage through z, are all H-invariant. So no argument that uses only H-images of a known connection can produce a bypass.
  - This is the affine analogue of Codex's §6, where copy symmetry gives the same physical path.
- **Density.** Connection directions from s to t are dense when one exists, by the Theorem 24 argument at a regular point. But density is compatible with every connection passing through z, so it gives no contradiction alone.
- **Counting.** Prefixing gives #(s→t, length ≤ L) ≤ #(s→z, length ≤ L). That's no contradiction either.

## What a proof needs
A bypass has to come from a cylinder in a direction where some lift of s and some lift of t are interior to the same cylinder and off the central core. For form (A), x lies on a boundary saddle connection in direction θ. The open question is whether some other rational direction θ' puts x and a t-lift inside one cylinder at different heights. If it does, Codex's ordinary-cylinder theorem finishes the proof.

## Status
Open. No counterexample and no proof. A bounded computation on fixed small lattice rooms could look for a form-(A) essential blocker or rule one out. That would be a new room search, so it needs Daniel's approval.

## Common-cylinder existence: reformulation and a midpoint pattern (2026-11-01)
Scale so that every corner is in Z². Then M covers the torus R²/2Z², branched only over integer points.

- **Lemma (good directions, elementary).** Let x project to (a, b) on the torus, and take a primitive direction (p, q). If qa − pb ∉ Z, the torus leaf through x avoids every integer point.
  - So x's leaf on M avoids every zero and every convex-corner lift.
  - Then x lies in the interior of a cylinder and not on any ι-invariant central core, because that core contains two corner lifts.
  - A connection in such a direction is neither form (A) nor form (B). Codex's ordinary-cylinder theorem then gives a bypass.
- **Reformulation.** z is essential only if every connection from x runs in a bad direction, where qa − pb ∈ Z.
  - Per room, this is a finite SL2(Z)-orbit statement on the labeled origami with fractional mark positions. It's decidable, like `origami_dark`.
  - The general claim needs a connection in a good direction. The obstacle: a closed torus leaf from x that reaches t's torus image Q lifts to a segment ending over Q. That endpoint can be a grid-congruent physical point t' ≠ t, not t.
- **General theory doesn't forbid single blockers.** Torus covers have the finite blocking property: on the torus, the 4 half-period midpoints (P+Q)/2 + Z² block P from Q. So the proof has to use the physical constraint that z has only the 2 lifts {b, ι(b)} and lies on a wall.
- **Midpoint pattern in every known obstruction.**
  - Codex's four-winding lemma puts both blockers at the cylinder midpoint of x and y, modulo half-periods.
  - In the six-wall control, z = (s+t)/2 + (0, 1), and (0, 1) is a half-period of 2Z². On the central core, the z parameters {1/2, 3/2} are exactly the midpoints of the separated pairs (1/4, 3/4) and (7/4, 5/4).
  - **Conjecture (midpoint).** If z is essential in a rational orthogonal room, then z's torus image is (P+Q)/2 modulo half-periods, for some lifts P of s and Q of t.
  - If the conjecture holds, it leaves finitely many candidate z for each pair (s, t). That's a strong restriction, which a wall-placement argument could then finish.
  - Where it could fail: in form (A), b only has to lie between x and y on the saddle connection, and nothing obvious forces the midpoint. Form (A) is still the case to attack.

## Denominator lemma and the exact remaining gap (2026-11-01)
Use torus coordinates on R²/2Z², with corners integral. Let D be a common denominator of the torus coordinates of s, t and z, and let P, Q be lifts of s and t.

- **Fact.** A coset u + NZ² contains a primitive vector exactly when gcd(u1, u2, N) = 1.
- **Lemma (clean segments).** Put u = D(Q − P). If gcd(u1, u2, 2D) = 1, some developed segment from P to Q + 2λ has b = u + 2Dλ primitive.
  - Its interior then misses every point of P + (1/D)Z², so it misses all integer points, every lift of z, and every lift of s and t.
  - The segment therefore lifts to M as a clean segment from x to some point over Q.
- **What the gcd condition means.**
  - u is even exactly when the midpoint (P+Q)/2 lies in (1/D)Z².
  - If an odd prime p divides 2D and both entries of u, then every segment in the coset passes through the (1/D)-points at parameters j/p.
  - So the only torus-level blockers are rational section points P + j(Q − P + 2λ)/p, and midpoints are the case p = 2. This is the general form of the midpoint conjecture. On the torus itself, it matches the classical blocking set made of the 4 midpoints (Gutkin 2005; Ho, arXiv 0807.2934).
- **Exact remaining gap (fiber monodromy).** The clean segment ends over Q, at a lift of some physical point t' in the fold class [t] = {w ∈ P : w ≡ (±τ1, ±τ2) mod 2}.
  - If [t] = {t}, the segment is a clean connection, so z isn't essential.
  - In general, the claim is that x's closed leaf in some good primitive direction passes through a lift of t itself. If it does, x and that lift share a cylinder off its central core, and Codex's theorem gives the bypass.
  - The which-fiber-point question is a monodromy problem in the cylinder; it isn't arithmetic. This is the precise open step.
- **Consequence if the gap closes.** An essential smooth blocker forces z to be a rational section point of s and t, which leaves finitely many candidates per pair.
