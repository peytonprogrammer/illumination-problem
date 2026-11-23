# d27: literature scout, free-group and origami results for vertex connectivity (r <= 8)

Date: 2026-11-10. Scope: published theorems that could settle or constrain
"every same-parity corner pair is connected for r <= 8". Verdict codes:
(a) classification usable at r <= 8, (b) partial constraint, (c) analogy only.

## Summary verdict

No paper found gives (a). The general illumination machinery explicitly
excludes torus covers, which is our case. The closest working analogue is
Duryev's proof of an illumination conjecture on square-tiled modular curves.

## Results read at the source

### 1. Apisa, Wright, "Marked points on translation surfaces", arXiv 1708.03411, Geom. Topol. 25 (2021)
Read from the PDF introduction.
- Thm 1.1(1): "If P is Gaussian, Eisenstein, or rectangle-tiled, then any two
  points are finitely blocked." (Our square-lattice rooms, with or without
  45-degree walls, are rectangle-tiled or Gaussian.)
- Thm 1.3: "Let M be an affine invariant submanifold that does not consist
  entirely of branched covers of tori. Any irreducible n-point marking N over M
  with n > 1 arises from a half-translation surface covering construction: for
  any (X, w, S) in N, there is a translation covering map from (X, w) to a
  half-translation surface that takes S to a single point."
- Thm 1.4: for Q not Q(-1^4), Q(2,-1^2), Q(2^2), periodic points over Q~ are
  only fixed points of J (plus hyperelliptic fixed points if Q is hyperelliptic).
- The authors state: when M consists of torus covers, "there are infinitely
  many irreducible n-point markings for all n >= 1".
Judgment: (c). Thm 1.3 is the exact shape of our conjecture (non-connected
implies a covering that collapses {s,t}), but its hypothesis excludes every
origami. Thm 1.4 is for generic surfaces in Q(1^r,-1^{r+4}), not square-tiled
ones. The proof of Thm 1.3 builds on Hubert-Schmoll-Troubetzkoy [HST08, Thm 5];
both use orbit-closure dimension, which is 2 for a closed SL(2,Z) orbit.

### 2. Duryev, "Teichmuller curves in genus two: square-tiled surfaces and modular curves", arXiv 1905.09312, Geom. Topol. 28 (2024)
Read from the PDF introduction.
- Thm 1.4: "The number of irreducible components of W_d^2[n] is equal to the
  number of SL2Z orbits in A_d^2[n] in X(d)." (A_d^2[n] = primitive n-rational
  points of the squares tiling X(d).)
- Conj 1.5 (illumination): "Light sources at the cusps of the modular curve
  illuminate all of X(d) except possibly for some of the vertices of the
  square-tiling." Proved for d <= 5; the author shows a vertex of X(5) that is
  not illuminated by the cusps. Parity conjecture implies illumination (Sec. 10)
  via LMW16 plus SL2Z-invariance of the illuminated set.
- Thm 1.2: parity conjecture for d = 2..5; d, n prime with n > (d^3-d)/4; d
  prime with n > C_d.
Judgment: (c), strongest methodological analogue. It is the only paper found
that proves vertex-to-vertex illumination on a specific square-tiled surface by
pairing an SL2Z-orbit classification of marked-point data with explicit
"lighthouses and eaves" (Sec. 6) cylinder arguments. Read Sec. 6 and Sec. 10.

### 3. Lelievre, Monteil, Weiss, "Everything is illuminated", arXiv 1407.2975, Geom. Topol. 20 (2016)
Abstract read. Per Apisa-Wright's summary: the only surfaces where every pair
is finitely blocked are torus covers; for any point p on any translation
surface, the set of points not illuminated by p is finite.
Judgment: (b) at most. Finiteness per point does not exclude a corner, and
corners are exactly the possible exceptions.

### 4. Wolecki, "Illumination in rational billiards", arXiv 1905.09358 (v3 2024)
Abstract read: in a rational polygon, the set of pairs of points that do not
illuminate each other is finite.
Judgment: (b). Consistent with a finite list of bad corner pairs; says nothing
about which pairs.

### 5. Hubert, Schmoll, Troubetzkoy, "Modular fibers and illumination problems", arXiv math/0602394, IMRN 2008
Abstract read: invariant subspaces of X^n under the affine group of a Veech
surface; finitely many of special shape for non-arithmetic Veech surfaces;
non-illuminable sets finite on Veech surfaces.
Judgment: (c). The finite-invariant-subspace result is for non-arithmetic
surfaces; arithmetic X^n has infinitely many (torsion-point fibers).

### 6. Free-group / Markoff line
- Chen, "Nonabelian level structures, Nielsen equivalence, and Markoff
  triples", arXiv 2011.12940, Ann. Math. 199 (2024): congruence on the degree
  of a Hurwitz-space component over M(1,1), i.e. on sizes of Nielsen classes of
  generating pairs; Markoff mod p transitive for all but finitely many p.
- Eddy-Fuchs-Litman-Martin-Tripeny(-Vanyo), arXiv 2308.07579, Proc. LMS:
  connectivity for p > 3.448e392. Brown, arXiv 2401.00630: p < 10^6.
- Martin, "Markoff triples and Nielsen equivalence in SL2(F_p)",
  arXiv 2510.07577 (2025): Q-classification conjecture for primes with
  24,504,480 not dividing p^2-1.
- Zmiaikou, arXiv 1403.2775: even permutations moving >= 3n/4 + o(n) points
  are commutators of generating pairs of A_n, S_n; exponential lower bound on
  T_2-systems.
Judgment: (c) for all. These fix the commutator class and count or connect
Nielsen classes in SL2(F_p) or A_n. Our commutator class is 3^r with mostly
fixed points (support 3r, far below 3N/4), and we need orbits of pairs plus
two marked cycles, not of pairs alone. Chen's divisibility idea (orbit sizes
divisible by p via a ramification argument at the cusp) is the only transferable
tool; no statement applies.

Not verified at source (memory only, do not cite as read): Hubert-Lelievre
and McMullen H(2) orbit classification (via arXiv 2107.08786 summary);
Schmithusen's Aut(F_2) description of origami Veech groups (math/0704.0416
summary); Ellenberg-McReynolds on Veech groups of origamis with marked points.

## Searched, found nothing applicable
- Classification of SL(2,Z) orbits of origamis with two marked points, or of
  pillowcase covers in Q(1^r,-1^{r+4}).
- Illumination/finite blocking classification for square-tiled surfaces after
  2016 beyond Duryev.
- Theorems on images of (positive) primitive elements of F_2 in finite groups
  covering conjugacy classes.
- Monodromy A_N/S_N results for H(2^r) or Klein-four-symmetric origamis.

## Suggested first lemma (cylinder-crossing criterion)
If in some rational direction s lies on the bottom boundary and t on the top
boundary of one cylinder C, then s and t are connected: C's open interior
contains no marked point, and the segments from s to t + k*circ(C) cross C.
In group terms: s, t connected if some gamma in SL(2,Z) maps (h, v) to (h', v')
with s a corner on the bottom of an h'-cycle cylinder and t a corner on its top.
This turns "connected" into an orbit-reachable condition on cylinder diagrams,
which is the form Duryev's lighthouse argument uses. Next check: does every
non-connected pair in the census fail this criterion in all directions, and
is that failure equivalent to the covering obstruction for r <= 8?
