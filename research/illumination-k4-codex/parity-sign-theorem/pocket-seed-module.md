# Actual seed modules: mixed twists can reveal a blind seed

[in progress] The universal pocket-detection goal remains open. The algebra
and closure statements pass focused Opus review; the conjugacy scope
correction below is incorporated. This note
adds an exact mixed-twist mechanism and a prescribed algebraic control.
It does not construct a room, direction, cylinder or optical event.

## Mixed-twist lemma

Let eta be a SUPPLIED actual S/T one-corner intrinsic-pi event. Retain the
marked relative lattice for all physical corner lifts and actual endpoint
lifts. Let h=I+H be an established pure axis multitwist and f=I+N another
pure affine multitwist, each fixing these labels and the selected prongs.
Their actions here are on relative homology, with absolute twist increments.
The actual event has equal developed primitive halves, so hol(eta)=0 as
in Section26. Assume H^2=N^2=0, QH=0 on the whole marked relative group,
and Qeta=0.
The first condition is standard for the refined multitwists of Section9.2;
the second is the established axis-isoperiodic slide property.
For all integers a,b, including negative ones,

    f^a h^b eta = eta + b Heta + a Neta + ab NHeta,
    Q(f^a h^b eta) = a [ Q(Neta) + b Q(NHeta) ].        (M1)

In particular Q(Neta)=0 does not make this whole TWO-ACTION family blind.
If Q(NHeta)!=0, set a=1: all but at most one integer b detect. Under the
additional single-direction blindness Q(Neta)=0, every nonzero b detects. It preserves the actual S/T fibers and the embedded pi
continuation because both supplied affine maps do. A final established
axis action makes its direction non-wall-parallel and gives either scalar
opening sign without changing Q. This last geometric conclusion uses
Section5, not an assumption that a nonzero vector automatically gives a
nonzero determinant in its initial direction.

The order matters. Q(h^b f^a eta)=Q(f^a eta) because Qh=Q. One must
PRECONDITION the seed by the blind axis map, then apply f. Conjugating
an axis map by a Q-preserving group element is still blind; here f is
NOT assumed globally Q-preserving. A first-stage vanishing QNeta=0 is
only vanishing on this supplied eta, not on the entire homology group.
The new nonzero test concerns the specific absolute class NHeta, not
an arbitrary element of ker hol. Explicitly hol(Heta)=(D_h-I)hol(eta)and
hol(NHeta)=(D_f-I)(D_h-I)hol(eta). Both vanish because THIS supplied
primitive equal-half event has hol(eta)=0. No event is identified with an
arbitrarily selected zero-period cycle.

## Conjugacy correction: axis preconditioning adds directions, not depth

The focused reviewer correctly points out the identity

    Q(N h^b eta)=Q(h^(-b) N h^b eta).

The right side is a FIRST-ACTION increment for the conjugate pure twist
h^(-b) f h^b, in direction D_h^(-b)v. Thus the mixed mechanism escapes
blindness of a supplied direction, but CANNOT escape blindness of every
rational-direction pure twist on eta. More generally all Q-preserving
letters in a word can be moved to the left, conjugating other generators;
the leftmost Q-preserving action then disappears from its Q-value.
Actual source-fixing removes any equal-derivative translation ambiguity:
a translation automorphism fixing a regular point is the identity. For
the torus-leaf lift construction, the conjugated map fixes the conjugated
leaf graph pointwise, so it is itself an admissible pure twist.

This does extend the exact finite family of Section9.4, whose quantifier
is ONLY det(w,v)=1, NOT all rational directions. For a horizontal axis
shear of coefficient K and v=(r,s),

    det(w,D_h^(-b)v)=det(w,v)+b*K*w_y*s.             (M2)

For w=(2,1),v=(1,1), this is1+bK and generally has absolute value different
from1. Those conjugate directions are outside the fixed-seed unimodular
family. This is a symbolic direction relation; no direction or cylinder
has been discovered. The review's conditional all-rational blindness
objection is valid, but identifying that hypothesis with Section9.4
would incorrectly broaden the latter's actual quantifiers.

If first-stage blindness really holds in EVERY rational direction, a
higher-depth escape must instead use two non-Q-preserving twists, or a
longer module product. This note does not prove such an escape exists.

## A controlled algebraic counterexample to the single-stage shortcut

Work in a six-dimensional symplectic absolute lattice with basis
(h,v,e,f,g,k), pairings <h,v>=<e,f>=<g,k>=1 and the others zero. Give h,v
holonomies(1,0),(0,1), and give e,f,g,k holonomy0. Add one formal relative
boundary generator r with holonomy0 and fixed by the maps below. This is
an abstract split relative model, not asserted to be a translation surface
or a room. It preserves nonzero relative boundary of the test seed.
Let

    eta=r+e+g,
    Q(e)=(1,0),   Q(g)=(-1,0),   Q(h)=Q(v)=Q(f)=Q(k)=Q(r)=0.

Define two positive rank-two core operators by

    Hx=<h+f,x>(h+f)+<h-f,x>(h-f),
    Nx=<h+v+e,x>(h+v+e)+<h+v-e,x>(h+v-e).

Both pairs of core vectors are isotropic, and each pair has the same
nonzero holonomy within that pair. Thus H^2=N^2=0, I+H and I+N preserve
the absolute symplectic form, and their holonomy actions are parabolic:

    hol((I+H)x)=[1,2;0,1]hol(x),
    hol((I+N)x)=[-1,2;-2,3]hol(x).

All core coefficients have the same positive sign. The two core sums
are2h and2(h+v), so their pairings factor through holonomy; merely sharing
holonomy would not suffice for that covariance. This control does not
use arbitrary indefinite nilpotent matrices. Directly,

    QH=0,     Qeta=0,       Neta=0,
    Heta=-2f,              NHeta=-4e,
    Q((I+N)(I+H)eta)=(-4,0).

So a globally blind axis operator can prepare a seed for detection by
another operator that was blind on the original seed. This demonstrates
only an algebraic nonimplication. It is not an in-class counterexample,
not a construction of such operators in an actual room, and not proof
that all first-stage unimodular directions can vanish in this model.
In fact the conjugate h^(-1) f h already detects in this abstract control,
with core direction(-1,1); relative to the prescribed direction w=(2,1),
its determinant is3. This explicitly demonstrates first-stage detection
outside that particular unimodular family, not all-direction blindness.
Actual affine actions for EVERY rational direction obey further group
relations not specified in this two-operator control.

## Exact finite-dimensional closure for supplied generators

For a FINITE SUPPLIED collection of pure affine multitwists f_i=I+N_i,
write E=H_1(X,P;R), D=dim E, and

    V_0=span{eta},
    V_(j+1)=V_j+sum_i N_i V_j.

The span of the actual group orbit of eta equals the stable V_j. Indeed
each N_i=f_i-I is a difference of group actions, while f_i and f_i^-1
are I+N_i and I-N_i. The stable subspace is therefore invariant under
all supplied generators and their inverses, and is both contained in
and contains the orbit span. If V_j=V_(j+1), it is already stable; otherwise
dimension strictly increases. A nonzero eta therefore stabilizes by
j<=D-1. For actual events eta has nonzero boundary s+t-2p, so eta!=0.

If Q is nonzero on the stable module, some product N_(i_l)...N_(i_1)eta
of length l<=D-1 has nonzero Q. Expanding that product as a signed sum
of at most2^l actual group words proves at least one actual image with
word length at most l detects. Conversely, if Q kills the stable module,
EVERY actual image under THIS generated subgroup is blind. No claim is
made that a chosen finite set of pure twists generates the full affine
group or suffices for every detecting event. In particular, one-stage
Bezout-residue blindness from Section9.4 is not such a module certificate.

## Concrete next obligation

For the reviewed bounded seed and an arbitrary specified literal pocket,
prove Q(NHeta)!=0 for some justified non-axis f and one of the established
axis operators H, OR prove a longer supplied-generator module pairing.
The H^2=N^2=0 identities make this an exact mixed coefficient. By conjugacy,
it is a first-stage contrast in a potentially nonunimodular direction,
even though it can cross several strips relative to the original seed.
If ALL rational-direction first-stage contrasts are assumed zero, this
axis option is impossible and the next obligation is a product of two
non-Q-preserving twists. Neither hypothesis has been proved for a room.
The construction can succeed when the original one-strip contrast vanishes. It still
needs a real geometric proof of the mixed coefficient; the abstract
control and finite-dimensional stopping bound supply no such existence.
