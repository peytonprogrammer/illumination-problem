# A sharper cylinder-blindness gate

[in progress] Universal actual-event pocket detection remains OPEN. The hand
lemmas below narrow a possible cylinder-based proof. They do not supply a
loaded cylinder, an actual seed, or a room counterexample. The fixed matrix
control tests only the stated linear identities; peer review is pending.

## 1. Use the cylinder annihilator, without a Forni converse

Let H=H_1(X;R), with its nondegenerate intersection form Omega. Let C be the
span of all rational cylinder cores on the fixed raw arithmetic surface X.
The unit-torus cover is branched only over zero. Theorem B of
[Boggi--Putman--Salter](https://academicweb.nd.edu/~andyp/papers/HomologyCovers.pdf)
and the once-punctured torus straight-representative argument in
pocket-structural-obstruction.md, Section 5, imply that C is symplectic.
Work over Q first and extend scalars to R. Peripherals lift to disk boundaries
and add zero homology; all other simple curves on that torus have rational
straight representatives avoiding the puncture. Each such lift thickens to
a flat cylinder. Conversely, a generic parallel core of ANY rational cylinder
avoids the origin fiber and is a component of the preimage of its straight
torus leaf. Thus the two spans are equal, not merely included. This
identification is at the raw arithmetic base t=0. The live-peer structural
review accepts it with this converse made explicit.

Set K=C^perp. Then H=C direct-sum K, and K is symplectic as well. Every
orientation-preserving affine automorphism preserves C, because its
SL2(Z) derivative takes rational cylinders to rational cylinders. In
particular the persistent quarter-turn R preserves C and K.

The literal-pocket neck plane is

    B=span(beta_0,beta_1), R beta_0=beta_1, R beta_1=-beta_0.

Its two generators are independent and B is isotropic, by accepted Section 31.
In the collar convention of 31.1 the true absolute slide cochain is

    Q(z)=(Omega(beta_1,z), -Omega(beta_0,z)).

Thus every rational cylinder is Q-blind exactly when B is contained in K.
This criterion makes no claim that K equals the Forni subspace. The known
Forni-vanishing result supplies an obstruction in one direction, but the
argument here needs neither its converse nor a classification of zero
Lyapunov exponents.

## 2. One loaded core tests both neck directions

**Lemma (hand proof; pending independent review).** Exactly one of the following
holds:

1. B is contained in K, and every rational cylinder core has Q=0.
2. The projection B->C along K is injective. For every nonzero beta in B,
   some rational cylinder core c has Omega(beta,c) nonzero.

Proof. The kernel B intersect K of this projection is R-invariant. Any
nonzero vector b in B is independent of Rb, since R^2=-I there. Consequently
B has no one-dimensional real R-invariant subspace. The kernel is zero or
all of B. In the zero-kernel case a nonzero projection has a nonzero pairing
with C because C is symplectic; at least one of its spanning cylinder cores
has a nonzero pairing. This proves the alternatives.

More concretely, suppose a supplied cylinder core c has

    a=Omega(beta_0,c), b=Omega(beta_1,c), (a,b) nonzero.

The quarter-turn image Rc is also a cylinder core, and the matrix of neck
pairings against c,Rc is

    [[a,-b],[b,a]],     determinant=a^2+b^2>0.

Hence a SINGLE loaded core and its quarter-turn detect every nonzero neck
combination. This is an absolute-cycle statement. It does not turn either
core into a source-to-target midpoint event. The coupling condition of
Section 32.3 is still needed for actual events.

## 3. A necessary four-dimensional obstruction, sharpened by symmetry

Let K_- be the -1 eigenspace of R^2 inside K. Since R^2 is a symplectic
involution, its +1 and -1 eigenspaces are symplectically orthogonal and each
is symplectic. Indeed if x and y belong to different eigenspaces, invariance
gives Omega(x,y)=-Omega(x,y). Nondegeneracy of their direct sum then gives
nondegeneracy of each summand.

If every core is blind, B is an isotropic two-plane in K_-. Therefore

    dim_R(K_-) >= 4.

In particular, proving dim_R(K_-)<=2 for the actual room would prove loaded
cylinder existence. This improves the earlier Forni-specific dimension test:
it applies to the ENTIRE cylinder annihilator even if it contains classes
not known to be Forni classes. No bound on this dimension is proved here.

There is another sufficient test. On K_- define

    G_R(x,y)=Omega(x,Ry).

It is symmetric and nondegenerate: R^-1=-R there, which gives symmetry,
and Omega and R are nondegenerate. If G_R is definite on K_-, B cannot lie
in K_-, since G_R(beta_0,beta_0)=Omega(beta_0,beta_1)=0. Thus definiteness
would also prove loaded-cylinder existence. Quarter-turn symmetry alone
does not imply definiteness, as the next exact control shows.

## 4. Reflection and positive Hodge data do not force that test

This is a FORMAL polarized real linear control, NOT a surface, a flat
local system, a Forni space, or an in-class counterexample. It shows that
these pointwise symmetry/polarization equations alone cannot prove the
needed dimension or definiteness bound. It has no assigned cone orders
and makes no assertion about realizing the topological sphere quotient.

Use the basis (h,v,e1,f1,e2,f2), each ordered pair symplectic, and put

    O=[[0,1],[-1,0]], J=[[0,-1],[1,0]], A=diag(-1,1),
    Omega=diag(O,O,O),
    R=diag(J,J,-J), V=diag(A,A,A), J_H=diag(J,J,J),
    C=span(h,v), K=span(e1,f1,e2,f2),
    beta_0=e1+e2, beta_1=f1-f2.

Here R is symplectic of order four, V is antisymplectic of order two,
and VRV=R^-1. The complex structure J_H is compatible and positive:
Omega J_H is the identity matrix. R commutes with J_H, while V
anticommutes with J_H. Both preserve its positive metric. These are the
pointwise holomorphic/antiholomorphic symmetry requirements at the
quarter-turn base.

Nevertheless B is R-invariant, isotropic, and contained in K; K_-=K has
dimension four, and G_R on K has signature (2,2). On the two neck basis
vectors G_R is identically zero. Give only h,v the coordinate periods
(1,0),(0,1). Every vector in C is Q-blind, while Q is nonzero on H.
The cochain has the exact covariance

    Q R=J Q,   Q V=A Q.

In particular even a positive Hodge metric and the real reflection cannot
replace G_R by a positive form. The complex structure J_H need not equal
R on K_-; it equals R on one two-plane and -R on the other. The control
is not proof that this obstruction occurs on a room. It rejects only a
linear-symmetry shortcut to excluding it.

## 5. Why orbit-closure orthogonality is not an immediate rescue

[Avila--Eskin--Moeller](https://arxiv.org/abs/1209.2854) prove flatness of
the Forni bundle and its orthogonality to the tangent space of the SAME
affine invariant manifold. Our raw square-tiled base lies on an arithmetic
Teichmuller curve, whereas the nonzero irrational pocket slides used in
Section 21 have a larger common orbit closure M_*.

A slide tangent in T M_* therefore cannot be a nonzero Forni class of
M_*. This gives no assertion that it avoids the Forni space of the SMALLER
base Teichmuller curve, and no assertion that it pairs with a cylinder
already present at that base. One cannot replace these two manifolds in
that theorem. No bound on the lengths of limiting corner paths follows
from orthogonality to T M_*.

Similarly, an affine copy quarter-turn remains an affine map after an
arbitrary SL2 deformation, with derivative g R g^-1. It need not stay a
holomorphic rotation for the new complex structure. A classification of
four-point cyclic pillow covers or of globally equivariant Hodge blocks
cannot be imported from the single C4 symmetry at our base without checking
those extra hypotheses. No such application is established by this audit.

## 6. Consequence for the active goal

The next genuine cylinder-route advance must prove one of the following
using the raw room geometry: B is not contained in K, dim K_-<=2, or a
nonzero actual-event contrast of Section 32.3. Merely repeating nonzero
Q, isotropy, positive Hodge metric, or D4 symmetry cannot do it.

Even a loaded-cylinder proof would leave actual S/T coupling. Direct events
with even moving-diagonal parity remain allowed; failure of this particular
cylinder route would not refute universal pocket detection.

Opus's 23:45 update separately proves that transporting a longer boundary
walk by an affine map preserves its walk index. Thus a k>=2 chain cannot
be converted to k=1 merely by that action. Bounded approach and single-event
existence remain separate obligations. This observation is attributed to
Opus and is not independently certified here.

**Next move:** prioritize the actual-event overlap condition over another
pointwise-symmetry argument. An in-class proof must retain the actual S/T
occurrences, compatible strip phases, and the embedded intrinsic pi-sector.

## 7. Every invariant subspace of the cylinder span is symplectic

**Independently accepted with corrections incorporated (2026-11-02).**
The positive torus-leaf multitwists prove a general algebraic lemma: every
Gamma-invariant subspace V of C is symplectic. Applying it to differences
of actual legal events gives the statement below, but the symplecticity
proof does not use the seed or supply a detecting event. Independent review:
`claude-illumination-check/review-gate-module/findings.md`.

Let Sigma be the entire finite fiber over zero for the unit-torus map. It
contains all physical corners, all actual S/T lifts, and any other lattice
lifts. Extra regular points in Sigma are HOMOLOGICAL marks only; passing
through them is not made an illegal optical encounter. Work in
E=H_1(X,Sigma;R). Its exact sequence injects H into E, since H_1(Sigma)=0.

For each rational unoriented direction theta choose a positive pure
multitwist f_theta=I+N_theta of the torus-lift annuli as in Section 9.2.
Choose a common positive coefficient sufficiently divisible to fix Sigma
and its finite local prong labels; alternatively include all positive pure
powers, which gives the same argument. On absolute classes,

    N_theta x = sum_j m_(theta,j) Omega(c_(theta,j),x) c_(theta,j),
    m_(theta,j)>0, N_theta^2=0.                         (7.1)

A global reversal of the intersection convention reverses all these
signs and leaves the sums-of-squares argument unchanged. Each positive
coefficient is a whole annulus twist count. Torus annuli may artificially
subdivide a maximal flat cylinder; their core classes still span exactly C.

**Explicit affine realization of these generators.** Fix integer vectors
(theta,u) of determinant1 and use their affine coordinates (s,t) on the
unit torus. Cut along its theta-leaf through0. The complement is an open
annulus of transverse height1. Each lifted annulus has circumference n_j
in these coordinates. Choose a positive integer kappa divisible by every
n_j. On each lifted annulus set

    (s,t) -> (s+kappa*t,t),   0<=t<=1,

using its own transverse coordinate with lower boundary t=0. The lower
boundary is fixed; on the upper boundary the shift kappa is a whole number
of its boundary-walk circumferences. Thus every boundary occurrence is
fixed. The maps glue pointwise on the full inverse-image leaf graph.
Their common linear derivative in developed (theta,u) coordinates is
[[1,kappa],[0,1]]. It agrees across every regular boundary segment. Near
a cone point it maps the sectors continuously with that same derivative;
the inverse construction uses -kappa. Hence this is an affine
homeomorphism, not merely a lift of an isotopic topological map. It fixes
the whole origin fiber. The twist count on annulus j is kappa/n_j>0.
A further positive power fixes any finite auxiliary prong labels if
needed. All n_j are at most the cover degree, so a common sufficiently
divisible kappa works for every direction and is preserved by quarter-turn
conjugation. Artificial subdivision of a maximal cylinder does not change
its core class. This proves the positive affine generators used in (7.1).


Let Gamma be generated by all these pure twists and their inverses. It
preserves actual endpoints and the selected intrinsic pi continuation by
the previously reviewed affine-event transfer. Take ONE SUPPLIED actual
S/T primitive equal-half event eta. To keep quarter-turn symmetry, let
eta_a=R^a eta for a=0,1,2,3, retaining their different actual copy/prong
labels. All are physically S/T events. Choose the twists R-equivariantly,
or include their quarter-turn conjugates among the generators. Then R
normalizes Gamma. This does not require R itself to fix individual labels.

Define the absolute difference space

    V_eta = span{g eta_a - eta_a : g in Gamma, a=0,1,2,3} subset H.

Each displayed difference is absolute because g fixes Sigma pointwise.
It is a DIFFERENCE of actual event classes, not itself asserted to be a
single event. We have V_eta subset C: expand a word into successive
generator increments. Every N_theta applied to a relative class is a
linear combination of its annulus cores, by the relative multitwist
formula, and Gamma preserves C.

**Actual-event check for these explicit maps.** Each generator has derivative
in SL2(Z), so it sends an equal primitive half-vector w to the equal
primitive half-vector Df*w. Its affine restriction sends each straight arm
to a straight arm. It fixes every point of Sigma, so neither arm gains an
encounter with a physical corner. At the selected corner its homeomorphic
sector map sends the chosen developed half-plane to another half-plane:
the germs stay opposite and the intervening embedded sector still has
angle pi. This verifies the required event transfer for this generator
family. Inverses have the same properties. Quarter turns merely change
the actual source/target COPY labels, retaining the physical S/T labels.
No event is inferred unless eta was supplied in the first place. An image
can be wall-parallel and then does not yet meet the opening hypothesis;
Section 8 uses the main proof's axis transfer to handle that case.


The space V_eta is invariant under Gamma. For h,g in Gamma,

    h(g eta_a-eta_a)=(hg eta_a-eta_a)-(h eta_a-eta_a).

It is also invariant under R, by conjugation and the chosen seed set.
Set Z=V_eta intersect V_eta^perp, its radical. Since Gamma is symplectic
and preserves V_eta, it preserves Z. For z in Z and any theta, N_theta z
belongs to V_eta, so

    0=Omega(z,N_theta z)
     =-sum_j m_(theta,j) Omega(c_(theta,j),z)^2.       (7.2)

All weights are strictly positive. Thus z pairs to zero with every core
in every rational direction. Hence z belongs to C^perp. But z belongs to
V_eta subset C, and C is symplectic by Section 1. Therefore z=0.

This proves **V_eta is symplectic**, including the possible zero space.
The same proof works for every Gamma-invariant V subset C. It also shows
that K=C^perp is exactly the Gamma-fixed space H^Gamma: its vectors are
fixed by every twist formula, while a fixed vector must pair to zero with
every core by (7.2). Hence C has no nonzero Gamma-fixed vector. Successively
taking invariant symplectic orthogonal complements decomposes C into
irreducible symplectic Gamma-submodules. Since R^2 commutes with each
generator, its eigenspaces in C and V_eta are invariant as well.
The proof uses ALL rational-direction pure twists. It is not valid for an
arbitrary finite saved set unless its core span is separately known to be
symplectic. Negative powers do not spoil (7.2): one uses the available
positive generator in each direction for that step.

## 8. A direct obstruction criterion for actual-event blindness

Keep a supplied seed eta as in Section 7. If Q(eta) is nonzero, it already
detects. Otherwise Q(R^a eta)=J^a Q(eta)=0 for every a.

Then every Gamma-image g eta_a is Q-blind if and only if

    B subset V_eta^perp.                              (8.1)

Indeed blindness of these images is equivalent to Q killing their absolute
differences, whose span is V_eta; the exact collar formula in Section 1
identifies this with (8.1). Conversely, if B does not annihilate V_eta,
some finite linear combination of these actual differences has nonzero Q.
At least one difference has nonzero Q and, since its original eta_a is
blind, its actual image g eta_a detects. Axis transfer then supplies a
non-wall-parallel event and both opening signs, as in Section 5 of the
main proof. This retains actual S/T labels and the intrinsic pi-sector.

By Section 7, U=V_eta^perp is symplectic. It is R-invariant. Its -1
eigenspace U_- for R^2 is symplectic by the same involution argument as
Section 3. Thus complete blindness of this Gamma seed family requires
an isotropic neck two-plane inside U_-, and forces

    dim_R(U_-) >= 4.                                 (8.2, weak form)

In particular dim_R(U_-)<=2 would prove actual-event detection, conditional
on the supplied seed and the transfer facts. But K subset U, so this test
implies dim K_-<=2, the unproved Section 3 sufficient condition. It is
never easier than that condition. Section 10 removes the automatic
quarter-turn plane before stating the sharper dimension test.

Equation (8.1) is an exact linear reformulation of blindness of this
Gamma-orbit; it is not an existence theorem. The pointwise affine
stabilizer Aff_Sigma can be larger than Gamma and act nontrivially on K.
Blindness of Gamma-images does not imply blindness of all actual affine
images. The quarter-turn seed copies add no independent criterion, since
R normalizes Gamma and Q is quarter-turn covariant.

No estimate of U_- is established for an arbitrary raw room. A seed remains
a separate realization assumption even if the dimension test is proved.

## 9. Independent review and investment decision

The review accepts Sections 7, 8 and 10 with the corrections recorded here.
Their linear algebra is sound, conditional on a supplied actual seed.
They prove neither seed existence nor a nonzero neck pairing. Gamma acts
trivially on K, so further Gamma-module, dimension or symplecticity
refinements are retired as the next research task.

The geometric targets are:

1. Prove B is not contained in K from the actual room geometry: some
   rational cylinder core must have nonzero Q (main Section 32.1).
2. Obtain an actual primitive equal-half S/T seed. Opus owns this gap.
3. For a supplied seed, prove a nonzero average contrast in main (32.4).

Each is an unresolved mathematical assertion. Section 13 excludes one
family of geometric factors but does not imply the first assertion.
Aff_Sigma beyond Gamma is an algebraic possibility, not a recommended
route without room-specific evidence. No discovery scan is proposed.


## 10. Removing the mandatory tautological complement sharpens the gate

**Independently accepted with corrections incorporated.** Every supplied equal-half
event has hol_0(eta)=0 in the E convention used above. An affine image has
hol_0(g eta)=Dg hol_0(eta)=0. Consequently

    V_eta subset H_0 := ker(hol_0:H->R^2).             (10.1)

Let T_0 be the tautological homology plane, the Poincare dual of
span(Re omega, Im omega). It is symplectic because the flat area is positive,
and H_0=T_0^perp. Since V_eta is symplectic and contained in H_0, define

    W_0 = V_eta^perp intersect H_0,
    H = T_0 direct-sum V_eta direct-sum W_0.           (10.2)

These are symplectically orthogonal symplectic summands. They are preserved
by R. In particular the T_0 summand is ALWAYS present in V_eta^perp: it is
not an obstruction to detection. R^2=-I on T_0. Section31 proves hol_0(beta_j)=0,
so the pocket plane B lies in H_0 as well. Thus (8.1) is equivalently

    B subset W_0.

Set W_(0,-)=ker(R^2+I) within W_0. Complete blindness of the actual seed
family forces an isotropic two-plane inside this symplectic space, hence

    dim_R W_(0,-) >= 4,
    dim_R (V_eta^perp)_- >= 2+4=6.                   (10.3)

The total-complement bound>=4 in (8.2) was correct but missed the automatic
tautological contribution. The stronger sufficient test is therefore

    dim_R (V_eta^perp)_- <= 4,

or, equivalently, dim W_(0,-)<=2. This is still a condition to prove for
the actual room, not a new universal dimension bound.

There is a concrete wall-count version. Main Section15 proves, for the
connected canonical eight-copy disk unfolding,

    g(X)=W+d-3,    g(X/<R^2>)=d-1.

Real homology invariants under the involution R^2 have dimension
2g(X/<R^2>), by transfer. Therefore

    dim H_- = 2(g(X)-g(X/<R^2>)) = 2W-4,
    dim (H_0)_- = 2W-6.                              (10.4)

V_eta is R-invariant and symplectic, so its +/- eigenspaces for R^2 are
symplectic. Using (10.2), blindness would force

    dim (V_eta)_- <= (2W-6)-4 = 2W-10.               (10.5)

Hence proving

    dim (V_eta)_- >= 2W-8                            (10.6)

would prove actual-event pocket detection from this supplied seed. Ranks
are even, so (10.6) is exactly the next possible rank above the bound in
(10.5). No actual homology rank was computed or asserted here. For example,
W25 would require a minus-module rank of at least42, in a primitive minus
space of dimension44. This illustrates how strong the sufficient condition
is; it must not be treated as likely or established merely because it is
now expressible as a rank test.

There is a further restriction on this sufficient test. T_0 subset C, so
K subset H_0 and H_0=C_0 direct-sum K, where C_0=C intersect H_0.
Since V_eta subset C_0,

    dim (V_eta)_- <= (2W-6) - dim K_-.

Thus (10.6) forces dim K_-<=2; it does not bypass the unproved Section 3
condition. The exact criterion is that the projection pi_C(B) onto C_0
along K is Omega-orthogonal to V_eta. If V_eta=C_0, Gamma-orbit blindness
is equivalent to B subset K. These equivalences supply no existence proof.

The finite six-dimensional control from Section4 sits exactly at the new
minimal algebraic blind size: T_0 has dimension2, K=W_0 has dimension4,
and the whole minus space has dimension6. It is not a surface and does not
certify a blind actual seed module. It only prevents interpreting (10.3)
as an algebraic contradiction by itself.


## 11. The even-zero example passes the sphere test but fails the rational neck test

**Independently accepted with corrections incorporated (2026-11-02).**
For the known surface M, H_0(M)_-=H_b has no nonzero rational v with
Omega(v,Rv)=0. M lies in H(2,2,2), has no cone-multiplicity-5 zero, and
is not itself a literal-pocket room. This arithmetic statement and the
conditional transfer below neither construct an actual event nor prove
the goal. Review: `claude-illumination-check/review-gate11-12/findings.md`.

Source inputs are [Matheus--Yoccoz, original paper](https://arxiv.org/pdf/0912.1425),
Version 2 (2010-10-06), Sections 3.1, 3.3, 3.5 and 3.7, at q=3. They give the affine-group splitting
Z/3 times SL(2,Z), a homology splitting T_0 plus H_tau plus H_b of dimensions
2,2,4, and finite affine image on H_tau plus H_b. The generators S,T and
intersection pairings used below are the displayed tables in 3.3/3.7.
The lift fixing A_0 fixes the three REGULAR A_i, not each zero (3.1).
Also the H_tau action is through Z/6 (3.5), not Z/3 as stated after the
formulas in the lecture notes' 8.6. Use the original paper for these inputs.

The following deductions and norm-descent proof are ours. Let P send
index i to i+1 on vectors with sum zero, so P^3=I. On H_b, using ordered
coordinates (sigma_0,sigma_1,zeta_0,zeta_1), the source tables give

    S = [[I,0],[P^2,P]],  T = [[P^2,P],[0,I]],
    R = T^(-1) S T^(-1) = [[0,-I],[I,0]].

On H_tau both inverse-T and S act as -P; thus R acts as -I. On T_0,
R acts by the ordinary quarter-turn J. The split lift R has order four
because the derivative map is an isomorphism on the subgroup fixing A_0.
No homology invariant is fixed by R: it is J on T_0, -I on H_tau and
has square -I on H_b. Transfer therefore gives

    genus(M/<R>)=0,     genus(M/<R^2>)=1.

Thus an order-four SPHERE quotient and even zeros do not exclude this
example. We have not established its compatibility with the full real
boundary quotient of a canonical disk.

Next identify the full cylinder annihilator without a Forni converse.
A positive pure rational annulus multitwist is unipotent on homology.
Section 7's annulus shear construction makes it an element of Aff(M,omega).
Its restriction to H_0=H_tau plus H_b has finite order by the source
input, hence is the identity. For x in H_0 the positive twist formula
then gives

    0 = Omega(x,N_theta x)
      = -sum_j m_j Omega(c_j,x)^2,   m_j>0.

Consequently every cylinder core annihilates H_0. Since horizontal and
vertical cores have independent periods, their full span C is exactly
T_0. Thus K=C^perp=H_0 and K_- = H_b. This uses absolute classes only.

In the stated H_b basis, the source's pairings give

    Omega_b = [[ 0, 6,-4, 2],
               [-6, 0, 2,-4],
               [ 4,-2, 0, 6],
               [-2, 4,-6, 0]],
    G = Omega_b R
      = [[-4, 2, 0,-6],
         [ 2,-4, 6, 0],
         [ 0, 6,-4, 2],
         [-6, 0, 2,-4]].

The REAL form G is indefinite: its values on (1,0,0,0) and
(1,0,0,-1) are -4 and 4. Nonetheless it is anisotropic over Q.
For v=(a,b,c,d), put x=a+i*c, y=b+i*d. Direct expansion gives

    -v^t G v = |2x-(1+3i)y|^2 - 6|y|^2.             (11.1)

Suppose a rational v makes this zero. Clearing denominators gives an
integer equation A^2+B^2=6(C^2+D^2), with

    A=2a-b+3d, B=2c-d-3b, C=b, D=d.

Modulo 3, A and B must both be divisible by 3. Substitute A=3A_1,
B=3B_1; the resulting equation 3(A_1^2+B_1^2)=2(C^2+D^2) forces C,D
to be divisible by 3 as well. Dividing A,B,C,D by
3 gives a strictly smaller integer solution of the same equation. Infinite
descent excludes a nonzero solution. The displayed rational change of
variables is invertible, so v=0. This proves the asserted anisotropy.

Consequently H_0(M)_-=H_b contains no nonzero rational v satisfying
Omega(v,Rv)=0. It has four minus dimensions and an indefinite real
rotation form, yet no rational isotropic R-plane. This is a statement
about M's homology; M does not carry the literal pocket in question.

The same obstruction applies conditionally inside an ARBITRARY higher
cover. Suppose a finite degree-n TRANSLATION covering f:X->O intertwines
the quarter-turns (omega_X=f^*omega_O, up to a nonzero constant), and B
is wholly contained in the rational homology transferred from this
single O=M factor. Require R_O to have derivative J and order four;
the unique-lift argument below then gives R_O=R. Its preimages lie in H_0(O), since transferred periods
are n times the corresponding base periods, up to that constant, and
the neck periods are zero. Transfer is injective over Q and scales the intersection
form by n: Omega_X(f^!a,f^!b)=n Omega_O(a,b). It also commutes with R.
The preimages of beta_0,beta_1 would therefore be a rational isotropic
R-plane in H_0(O)_-=H_b, which has just been excluded. This does not
exclude a higher cover itself: its neck might have components in the
new homology, or in several blocks whose intersection contributions cancel.
No cylinder-blindness assumption was used: B is excluded from the entire
transferred H_1(O;Q). Separately f^!H_0(O) subset K_X, since pushing
forward cylinder cores gives multiples of cores. For literal-pocket rooms,
Section 13 excludes this geometric translation factor outright, so this
conditional transfer has no such room instance.

The example has a unique order-four lift with derivative J: any other
lift is D^a R with central D of order3, whose fourth power is D^a.
So changing the order-four lift does not evade this calculation.

**Scope and next consequence.** An indefinite real rotation form need not
admit a rational null vector. This gives a stronger possible exclusion
method than a real dimension bound. It is not universal: Section4's
formal model DOES have rational isotropic necks. Section11 alone does not rule
out higher covers, extra complementary blocks whose pairings cancel,
or the separate failure of actual S/T seed coupling. Those possibilities
remain open. Do not replace the goal by a classification of known examples.
The fixed checker verifies the published-matrix composition and norm
identity; the descent and geometric interpretation require hand review.


## 12. Rational anisotropy does not survive unrestricted component multiplicity

**Fixed algebraic limitation, not a surface or goal counterexample.** Section11
cannot be promoted to an arbitrary-complement exclusion merely by placing
more copies of the same rational block in the complement. Here is an explicit
failure retaining the neck's reflection constraint as well as integrality.
No surface or additional geometric input is constructed or assumed.

First retain the actual neck symmetry. With the annulus labels of main31.1,
the global reflection V takes annulus j to annulus -j and reverses its
boundary orientation. Hence V b_j=-b_(-j), and

    V beta_0=-beta_0,     V beta_1=beta_1.

Thus an appropriate rational null vector must be in the -1 eigenspace of V;
a null vector in an arbitrary real direction would not meet this condition.

On the single Section11 block define

    L=[[1,-1],[0,-1]],        V_b=diag(L,-L).

In the published cyclic-index convention L implements i->-i. Direct
multiplication verifies V_b^2=I, V_b^t Omega_b V_b=-Omega_b, and
V_b R V_b=R^(-1). This is a compatible RATIONAL LINEAR reflection; no claim
is made here that it is the action of a particular surface involution.
Its negative eigenspace consists of v=(a,2a,c,0). On this space,

    v^t G v = -4*((c-3a)^2-6*a^2).                  (12.1)

Consider the orthogonal direct sum of THREE copies of this same block,
with Omega_3, R_3 and V_3 the corresponding block diagonal matrices. Put

    b = (1,2,4,0 ; 0,0,1,0 ; 0,0,2,0),
    R_3 b = (-4,0,1,2 ; -1,0,0,0 ; -2,0,0,0).

Each component of b lies in the negative V_b eigenspace. Its three values
in (12.1) are respectively 20,-4,-16, whose sum is zero. Consequently

    Omega_3(b,R_3 b)=0,
    R_3^2 b=-b,
    V_3 b=-b,     V_3 R_3 b=R_3 b.

The two vectors are independent. Their rows 4 and 6 (zero-indexed) form
[[0,-1],[1,0]], of determinant1, so their span is saturated in the displayed
coordinate lattice Z^12. This is a statement about that coordinate lattice,
not an assertion about the full integral homology lattice of a surface.

Thus rationality, a pair spanning a saturated sublattice of the displayed
coordinate lattice, isotropy, quarter-turn and
anti-reflection relations CAN coexist in a sum of the individually
anisotropic published blocks. Adding a separate tautological plane and
assigning zero periods to these blocks preserves this conclusion. The
arithmetic contradiction in Section11 depends essentially on containment
in one block; it is not stable under unrestricted invisible components.

**Research consequence.** To use Section11 toward the universal goal, one
would have to prove that the actual neck belongs wholly to one such block,
or prove a different geometric restriction excluding the displayed kind
of cancellation. Neither has been proved. Do not infer the existence of
an equivariant higher cover or of a room realizing this formal direct sum.
Conversely, do not spend another turn listing more known blind factors:
this calculation already refutes the unrestricted algebraic extension.
The remaining substantive targets are room-geometric nonzero pairing and
actual S/T event realization. The accepted Section7--8/10 symplecticity
argument supplies neither of those targets.

The checker now verifies 30 original formal identities, 9 fixed
original-source matrix/norm identities, and 8 identities for this supplied
direct sum. These are not 47 independent mathematical tests, optical
tests, or a geometric existence proof: several equalities are consequences
of other checks or definitions. The independent review rebuilds the source
matrices separately; see its checker-audit section for the exact limits.


## 13. Coprime pocket cones exclude common-divisor torsion-fiber factors

**Independently accepted with corrections incorporated (2026-11-02).**
Review: `claude-illumination-check/review-gate13/findings.md`.
Unlike Sections11--12 this concerns every actual translation factor of the
room unfolding, without assuming rotation/reflection equivariance or
containment of the neck in an inherited homology block. It still does not
supply a loaded cylinder or an actual detecting S/T event.

Write E=C/(2Z+2iZ), E[2]={0,1,i,1+i}. Let pi_X:X->E be the actual
raw room developing map at t=0, with pi_X(S)=0 at a regular interior A
mark. X is connected (main Section 12). The inputs from main Sections
1, 10 and 14 and the local-angle calculation are:

1. The full absolute period lattice of omega_X is exactly 2Z+2iZ.
2. Every zero of omega_X maps under pi_X to E[2] (integral corners in
   Section 1, even translations in Section 10, developing map in Section 14).
3. A literal pocket has a zero x_B over 1+i with cone multiplicity5,
   and a zero x_C over 1 or i with cone multiplicity3.

Here cone multiplicity means ord(omega)+1, not the physical angle divided
by 2pi. The pocket angles 5pi/4 and 6pi/4 have multiplicities5 and3 by
m/gcd(m,4). The chosen S is regular as a point of X.

**Theorem.** Suppose p:Y->E is a finite-degree translation torus cover,
with Y compact and connected and omega_Y=p^*dz. Assume there is an integer d>=2 such that EVERY point over
E[2] minus {0} has cone multiplicity divisible by d. Then no finite
nonconstant holomorphic f:X->Y and nonzero complex lambda satisfy

    omega_X = lambda * f^*(omega_Y).                 (13.1)

No assumption about other fibers, deck groups, or the action of R is needed.

**Proof, including scale and shift.** Put alpha=1/lambda. For every
absolute loop gamma on X, alpha*integral_gamma omega_X is a period of
omega_Y, hence belongs to 2Z+2iZ. By input1, alpha*2 and alpha*2i belong
to that lattice. Consequently alpha is a nonzero Gaussian integer, and
multiplication [alpha]:E->E is a group endomorphism.

The maps h=p composed with f and [alpha] composed with pi_X have the
same differential alpha*omega_X. Their difference as maps to the torus
is therefore a constant t because X is connected. Thus

    p f = [alpha] pi_X + t.                          (13.2)

Every point y above any u in E[2] minus {0} is a zero, by the d assumption.
Surjectivity of f supplies x over y, and the local pullback formula makes
x a zero as well. By input2, pi_X(x) belongs to E[2]. Therefore

    E[2] minus {0}  subset  [alpha](E[2]) + t.        (13.3)

Since [alpha] is a group endomorphism of E, its image of E[2] is a
subgroup of E[2]. The right side is a coset of a subgroup with order1,2 or4. It contains
three distinct points, so this subgroup has order4. Multiplication by
alpha is thus bijective on E[2]. Its coset contains a point of E[2], so
t also belongs to E[2]. This is the step that prevents a rescaling from
collapsing the parity classes or an arbitrary torus translation escaping them.

The regular point S maps to a regular point f(S): at S, the pullback
order formula gives 1=e_S*(ord_(f(S)) omega_Y+1). Equation(13.2) gives
p(f(S))=t. The fibers over the three nonzero elements of E[2] consist
entirely of zeros, so regularity forces t=0.

It follows that both x_B and x_C map to points over nonzero E[2] values.
Indeed their base points are nonzero and [alpha] permutes E[2] bijectively,
fixing zero. Their target cone multiplicities are divisible by d. The
same local formula now yields

    5 = e_(x_B) * (ord_(f(x_B)) omega_Y+1),
    3 = e_(x_C) * (ord_(f(x_C)) omega_Y+1).

Hence d divides both5 and3, impossible. This proves the theorem.

**Application to the known even-zero factor and its published family.**
Section3.1 of [Matheus--Yoccoz](https://arxiv.org/pdf/0912.1425)
gives, for every odd q>=3, a degree-q torus cover whose three nonzero
2-torsion fibers each consist of one point of cone multiplicity q; the
fiber over0 has q regular points. Their form is the pullback of the
2Z+2iZ torus form. These facts also follow from their displayed algebraic
model w^(2q)=z^(q-2)(z^2-1), using

    y=w^q/z^((q-3)/2),   y^2=z(z^2-1),
    omega_Y=c^(-1) dz/y.

Choose d=q in the theorem. No member of this family, including q=3
(the genus4 example), can be a translation quotient of X, even after
complex rescaling and torus shift, at the raw grid base t=0. In particular,
allowing higher covers
of that surface does not restore it as a TRANSLATION FACTOR mechanism
for our room. For geometric factorizations this rules out the premise
of Section11's conditional transfer. It does not exclude an abstract
H_b-type block in the room homology.

**Exact limit of the conclusion.** This does not exclude an abstract
isomorphic homology representation, several such blocks with no geometric
factorization, or a torus-cover factor whose three nonzero torsion fibers
do not share the stated divisor. It does not prove that all cylinder cores
span H, that the actual seed increment module pairs with the neck, or
that an actual S/T seed exists. It is a geometric exclusion toward those
questions, not a replacement objective. No optical or factor search was run.
