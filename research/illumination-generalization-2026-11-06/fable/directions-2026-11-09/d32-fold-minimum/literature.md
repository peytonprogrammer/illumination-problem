# Literature check: dark pairs vs. marked-point theorems

Checked 2026-11-12 against arXiv PDFs: Apisa-Wright 1708.03411v3, Wolecki
1905.09358v3, Apisa 2110.07540v1, Moeller math/0410262v2. Tags: CITED means
quoted from the paper; ANALYSIS means this note's own reading.

## Claim under test

"For a rational polygon whose unfolding is not a torus cover, every
non-illuminating pair comes from (a) a translation cover mapping both points
to one point, or (b) periodic points, finite on non-arithmetic Teichmueller
curves and absent or classified otherwise."

## Verdict

Yes for (a) and the finiteness part of (b), with these corrections:

1. The cover in (a) goes to a half-translation surface, `(Q_min, q_min)`,
   not a translation surface.
2. In (b) both points must be periodic for the orbit closure `M` of the
   unmarked unfolding, or zeros. Periodic points are finite for every `M`
   that is not a torus-cover locus, not only for Teichmueller curves.
3. "Absent or classified otherwise" is false in general. Classification is
   known only in special loci, and Apisa-Wright pose the general case as
   Problem 1.5.
4. The theorem is a statement about finite blocking on the translation
   surface. It covers non-illumination because polygon darkness lifts to
   finite blocking on the unfolding.

## Exact statements (CITED)

- AW Theorem 1.3: "Let M be an affine invariant submanifold that does not
  consist entirely of branched covers of tori. Any irreducible n-point
  marking N over M with n > 1 arises from a half-translation surface
  covering construction: for any (X, ω, S) ∈ N , there is a translation
  covering map from (X, ω) to a half-translation surface that takes S to a
  single point."
- AW Theorem 3.6, under Assumption 3.2 ("(X, ω) is not a translation cover of
  a torus"): "If x1 and x2 are finitely blocked on (X, ω), then either they
  are both M-periodic points or zeros, where M is the orbit closure of
  (X, ω), or πQmin(x1) = πQmin(x2)." This is the theorem that applies to
  pairs. Theorem 1.3 is an input: the proof applies it to the orbit closure
  `M_{x1,x2,B}` of `(X, ω; x1, x2; B)`, after Lemma 3.8 shows neither point is
  free. Non-illumination is the case `B = ∅`. The introduction says the
  results "also apply to the illumination problem, which is the special case
  of the finite blocking problem when the blocking set is required to be
  empty."
- AW Lemma 3.3: `Q_min` is reached from `X_min` by a translation covering of
  degree 1 or 2. Every translation cover of `(X, ω)` to a quadratic
  differential factors through `π_{Q_min}`. This uses Moeller [Möl06,
  Theorem 2.6].
- AW Theorem 1.2 (Eskin-Filip-Wright): "An affine invariant submanifold has
  infinitely many periodic points if and only if it consists entirely of
  branched covers of tori."
- AW Theorem 1.4: "Suppose Q is not Q(−1^4), Q(2, −1^2), or Q(2^2). If Q is
  not hyperelliptic, the only Q̃-periodic points are fixed points of the
  involution J. If Q is hyperelliptic, the only Q̃-periodic points are fixed
  points for J and fixed points for the hyperelliptic involution." This
  holds only when the orbit closure is the full locus `Q̃`.
- AW Theorem 3.10: for a k-differential with k > 2 whose unfolding is not a
  torus cover, "there are only finitely many pairs of finitely blocked
  points." For this case, the proof rules out option (a) except at points
  over the fixed points of powers of `t` on `X_min`.
- AW Theorem 1.1(1): Gaussian, Eisenstein, or rectangle-tiled polygons give
  "any two points are finitely blocked." Proposition 3.11 says these are
  exactly the polygons whose unfolding is a torus cover.
- AW Problem 1.5 leaves open the periodic points over eigenform loci, the
  Veech-Ward-Bouw-Moeller curves, and the newer orbit closures. AW also
  notes "an unexpected periodic point over the golden eigenform locus in
  genus 2."
- Moeller Theorem 5.1: "The only periodic points on a primitive Veech surface
  in ΩM2(2) are the Weierstraß points." Theorem 3.3 says differences of
  periodic points are torsion in an r-dimensional quotient of the Jacobian.
  The abstract recovers finiteness on Teichmueller curves that do not come
  from torus covers, a result first proved by Gutkin-Hubert-Schmidt.
- Apisa 2110.07540, Theorem 9.3 (quoting AW): for a rank ≥ 2 component of a
  quadratic stratum, "If Q is a hyperelliptic component, then the only
  periodic points are fixed points of the hyperelliptic involution.
  Otherwise, there are no periodic points." Theorem 1.3: "If P is an
  unexceptional rational right or isosceles triangle then no two points of P
  are finitely blocked from each other." Theorem 9.7 classifies the blocked
  pairs for every rational right and isosceles triangle.

## Gap between dark pairs and the theorems (ANALYSIS)

1. Polygon to surface. Wolecki Lemma 2.1 says A and B are joined in Q minus E
   if and only if some lift of A is joined to some lift of B in M minus
   `π⁻¹(E) ∪ Σ`. A dark pair therefore lifts to pairs `(x, y)` that are
   finitely blocked by the preimages of the π/n vertices, which are
   removable singularities. They need not be non-illuminating on M. AW
   Theorem 3.6 handles any finite blocking set, so this step is sound.
2. Quadratic differentials. All AW theorems are stated for Abelian
   differentials, so they apply to the unfolding `(X, ω)` and not to the
   doubled polygon. The doubled polygon is `X / <T>`. For orthogonal rooms it
   is a quadratic differential, and `X` is a cover of it, not always its
   holonomy double cover. Quadratic differentials appear only as `Q_min` and
   through `Q̃` in Theorem 1.4.
3. The classification of (b) needs the orbit closure of the specific
   unfolding. Theorem 1.4 and Theorem 9.3 apply only when that orbit is dense
   in a quadratic stratum locus of rank ≥ 2.
4. Torus covers. Square-lattice rooms whose walls are axis-parallel or at
   45°, with integer vertices, are rectangle-tiled or Gaussian. By AW
   Proposition 3.11 their unfoldings are torus covers, so the claim's
   hypothesis fails for them. Every pair in such a room is finitely blocked
   (AW Theorem 1.1(1)), and the theorems give no structure for dark pairs.

## Wolecki (CITED, then ANALYSIS)

Theorem 1.2(i): "Only finitely many pairs of points in Q do not illuminate
each other." This holds for every rational polygon, including torus covers.
Theorem 1.2(ii) states that {BC ≤ n} is finite for all n if and only if M is
not a torus cover. Wolecki proves finiteness only and gives no classification
of type (a) or (b). The claim is therefore not in Wolecki.

Lemma 2.9 says that if `M_{|Γ|k} ⊊ M̂²`, then the lift `M_{Q,k}` meets each
translation surface S affinely embedded in `M̂²` in a finite set. The proof
applies the reflection `(R_h, 1)` and then requires the rank of the 4×4 system
(rows (a,0,b,0), (0,a,0,b), (a′,0,b′,0), (0,−a′,0,b′)) to equal 2. It derives
the contradiction −1 = 1 from that rank.

This note finds that the matrix splits into real-part and imaginary-part
blocks, with determinants `ab′ − ba′` and `ab′ + ba′`. Exactly one of these can
vanish, which gives rank 3. Then `S ∩ (R_h,1)⁻¹S′` is a horizontal or vertical
real segment that could hold infinitely many lifted pairs, and the proof does
not exclude this case. The other reflections of an orthogonal polygon (`R_v`
and −1) also preserve horizontal and vertical lines, so they cannot rule it
out. This matches the suspected gap for orthogonal polygons. For polygons
with an angle that is not a multiple of π/2, AW Theorem 3.10 gives finiteness
on its own.
