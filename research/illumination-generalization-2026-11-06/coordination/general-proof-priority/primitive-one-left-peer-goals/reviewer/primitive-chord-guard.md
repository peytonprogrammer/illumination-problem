# Exact primitive chord geometry and the actual-path verification gate

HAND result, pending independent review. No direction census, new checker, room/ray discovery, worker or engine. The family is normalized A=H=2d+1, a=B=d, odd d>=3; the assigned residual is d=3 modulo4. Physical native dilation2 conjugates all statements without changing their scope.

The accepted intrinsic period lattice is Lambda=2Z². Let U be the full fiber of its torus over the unique cone. In signed-cross coordinates its points have odd integer coordinates. Every genuine global affine map preserves U because it fixes the unique cone and acts on the intrinsic period torus. Thus BOTH images of p and ORIGINAL Rxq belong to U. No preservation of a finer chosen tiling is assumed.

## 1. Exact geometric classification, including closed-copy seams

For a primitive nonzero integer vector w=(i,j), there exists SOME regular straight segment of holonomy 2w in the closure of ONE actual polygon copy, with both endpoints in U, if and only if

max(|i|,|j|)<=d
and the unordered pair {|i|,|j|} is NOT {d,d-1}.

This is a classification of possible GEOMETRIC chords, with freely placed U endpoints. It is NOT a construction of F(p), F(Rxq) or an actual affine map; the required endpoint action remains a separate obligation.

Proof of necessity. In any closed copy the absolute physical coordinates of a U point are odd integers in [1,A]; x=0 or y=0 cannot represent U since their torus coordinate has the wrong parity. This also handles endpoints on smooth outer or inner walls: their closed-copy representatives are still odd. A chord of holonomy 2w therefore has |i|,|j|<=d.

Suppose unordered absolute components are {d,d-1}. Transposition allows the horizontal span to be 2d. Two odd x coordinates in [1,2d+1] with that span must be exactly 1 and A. The vertical span is 2d-2, so its lower odd y coordinate is 1 or 3, and its higher coordinate is 2d-1 or A respectively.

If the physical chord has positive slope, the endpoint at x=A is the higher one; its y is at least 2d-1>d, outside the closed L. If it has negative slope, the endpoint at x=A has the lower y=ell>=1. At x=d the chord height is

ell + ((A-d)/(2d))*(2d-2)
=ell+d-1/d>d.

It therefore passes through the missing notch, not through closure(P). These alternatives exhaust all signs and copies, after taking absolute physical coordinates. A boundary-aligned repair cannot change this strict exclusion. No forbidden corner endpoints have been allowed.

Proof of sufficiency. Whole-room coordinate reflections, transposition and segment reversal reduce geometric existence to constructing a negative-slope physical chord with absolute half-spans i,j>=0. These operations place the chord in an identified reflected copy with EXACT requested signed vector 2w; this is a geometric symmetry argument, not commutation of an arbitrary F with G.

If one component is zero, primitivity makes the other 1, and the segment (1,1)->(3,1), or its transpose/reversal/reflection, is inside the bottom rectangle and regular.

Let i,j>0. If max(i,j)<=d-1, take endpoints

(1+2i,1), (1,1+2j).

They are odd-odd actual interior points of the right or upper arm, possibly on an INTERNAL mouth line. They are below A in both coordinates. The negative-slope segment avoids the missing quadrant x>d,y>d precisely when

2ij <= (d-1)(i+j).

Here the inequality is strict: subtracting the left side gives

(d-1-i)j+(d-1-j)i>=0,

with equality only at i=j=d-1. That case is not primitive because d-1>=2. Thus the segment does not touch the reflex (d,d). The other corners all lie outside this positive-coordinate interior segment. Both endpoints and the entire chord avoid Sigma.

If max(i,j)=d, transpose to i=d. Primitivity excludes j=d; the forbidden pair already excluded j=d-1. For 1<=j<=d-2 take

(A,1), (1,1+2j).

The first endpoint is strictly inside the actual smooth outer right wall. The second is interior and below A. The same notch inequality is strict because

(d-1)(d+j)-2dj=d(d-1)-(d+1)j>0

for j<=d-2. No physical corner lies on the chord. These are the only remaining primitive vectors. This proves the exact classification for closed copies as stated.

## 2. Consequence for EVERY prospective full-affine compressor

Write v0=(-d,d-1) and h(gamma)=2v0. A genuine global affine F has derivative L inducing a unimodular integral automorphism of Lambda. Therefore

h(F gamma)=2w, w=L v0 in Z² primitive.

The actual prescribed path can be compressed only if w satisfies section1's classification. In particular no global map with L v0 parallel to a room-reflected or transposed copy of v0 can compress it. For such a map primitiveness forces

L v0= +/- n(v0)

for the corresponding room sign/transposition matrix n: an integral primitive vector parallel to another integral primitive vector has multiplier +/-1. Its absolute components remain {d,d-1}, which section1 excludes.

This rules out the ENTIRE original-direction stabilizer, with every phase and endpoint action, not merely a selected anchored twist or the previously controlled four-direction subgroup. It also rules out mapping that direction to any member of its whole-room symmetry orbit. The exclusion is a necessary full-group guard for that behavior; it does NOT classify the full affine group or exclude maps to other image directions.

The ambient unimodular matrix [[-1,-1],[d-1,d]] sends v0 to (1,0). This only shows that the intrinsic-lattice guard does not by itself forbid a short vector. It is NOT a global affine realization on M, supplies no actual translation phase, and does not determine either endpoint sheet. No positive availability is inferred from it.

## 3. Endpoint visibility alone is insufficient for THIS gamma

The earlier existential seed gate could choose the inverse image of any visible seed. The present question freezes gamma. A compressor must preserve its ENTIRE developed holonomy, not just its endpoint images on the quotient surface.

Let a,b be the actual closed-copy coordinates of F(p), F(Rxq), in a named copy C. A necessary condition is the EXACT equality

b-a=L h(gamma)=2L v0,

not merely equality modulo Lambda. Endpoint coincidence on the surface can hide a nonzero period winding, giving a different path from the visible segment.

Conversely, suppose F is already proved to be a genuine global Sigma-preserving affine map; a,b are its EXACT named endpoint images; the displayed equality holds; and [a,b] is a regular segment in closure(C). Then the image of the actual gamma IS this segment. Parametrize gamma on [0,1]; its derivative in translation charts is h(gamma). F gamma and the proposed seed start at the same regular surface point with the same constant developed velocity Lh(gamma). Regular geodesic continuation on a translation surface is unique until a genuine cone. Both paths avoid Sigma, so they agree throughout [0,1]. Smooth wall seams are regular surface points and introduce no extra choice of continuation.

Thus no separate numerical trace of a long image path is needed after these exact global-map, endpoint and holonomy conditions are proved. But none of them follows from a projected target choice, a bare integer matrix or endpoint visibility alone.

## Status

This proves a sharp necessary image-vector guard and eliminates full original-foliation preservation as a compressor mechanism. It leaves the quantified exact-gamma gate OPEN for maps changing its direction outside the forbidden symmetry orbit. Even a positive answer for every stated d would not prove all-path/all-four/all-native-L availability or the broad r<=8 theorem. No previous proof or discovery clock was altered.
