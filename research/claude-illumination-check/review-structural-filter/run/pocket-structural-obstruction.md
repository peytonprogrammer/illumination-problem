# Structural audit: cylinder blindness versus actual-event blindness

[in progress] Universal pocket detection remains open. This audit does not add
coordinate cases. It tests a premise behind the non-axis twist route.

## 1. A genuine general obstruction to the naive cylinder argument

A nonzero cohomology class need not load any cylinder core. Lemma4.3 of
[Aulicino–Benirschke–Norton (2024)](https://www.numdam.org/item/10.5802/ahl.198.pdf)
states that Forni classes integrate to zero on every cylinder core.
The same paper uses the symplecticity of the Forni subspace in Proposition4.4.
Consequently one cannot infer a loaded rational cylinder solely from the
pocket cochain being nonzero. These are statements about the absolute
cohomology of an orbit closure, not about a supplied relative event.

Conditional consequence in our notation: if both absolute pocket components
Qx,Qy belong to the Forni subspace F of the arithmetic base, every pure
marked cylinder multitwist preserves Q on each relative event, since its
increment is a sum of cylinder cores. A supplied blind seed would then
remain blind on that twist-generated orbit. Endpoint terms still matter:
this does not prove that every actual seed is blind, or that Qx,Qy lie in F.
The converse of Lemma4.3 is NOT assumed. All-cylinder blindness need not be
identified with membership in F without an additional theorem.

## 2. An elementary quotient filter specific to our room class

**Lemma.** Every zero of the Abelian differential on a connected canonical
D4 room unfolding has even order. If this surface admits a translation
cover onto another Abelian differential surface, all local ramification
indices are odd and all zeros of that quotient differential have even order.

**Proof.** At a polygon vertex with interior angle m*pi/4, 1<=m<=7, the
local reflections generate a dihedral subgroup with

    n(m)=8/gcd(m,4)

sectors in each lifted cone. Thus its total cone angle is

    n(m)*m*pi/4 = 2*pi*q(m),  q(m)=m/gcd(m,4).

For m=1,...,7, q(m) is respectively1,1,3,1,5,3,7. Every q is odd, so
its zero order q-1 is even. The smooth m4 boundary case and ordinary
interior points are regular, also of even zero order0. These exhaust
points of the unfolded surface; the literal pocket ensures the full D4
unfolding is connected.

For a nonconstant translation covering f with omega_X=c*f*omega_Y,
c!=0, at any x over y the local order formula is

    ord_x(omega_X)+1 = e_x*(ord_y(omega_Y)+1).

The left side is odd. Therefore both e_x and ord_y(omega_Y)+1 are odd.
Surjectivity onto the compact quotient supplies a preimage for every y.
This proves both conclusions. The claim concerns translation coverings;
it does not exclude an arbitrary holomorphic map that fails the
differential pullback identity. No ray, direction or word argument is used.

**Corollary.** The Eierlegende Wollmilchsau cannot be a translation quotient
of any surface in this room class. Its differential has four simple zeros,
as recorded in the AppendixA stratum statement of
[Forni–Matheus–Zorich (2011)](https://webusers.imj-prg.fr/~anton.zorich/Papers/SQUARE_TILED_CYCLIC_COVERS.pdf).
At a preimage of any such zero the order formula would give an even cone
multiplicity, contradicting the lemma. The exclusion covers branched as
well as unbranched translation coverings.

This is an elementary filter, not a novelty claim. It rules out importing
that particular known cylinder-blind factor. It does NOT exclude an
abstract isomorphic representation inside H1, all other Forni subspaces,
or the genus-four example in H(2,2,2), whose zero orders pass the filter.
The latter stratum is also recorded in the same AppendixA.

## 3. The pocket requires at least four real Forni dimensions to hide this way

Accepted Sections21.1 and31 give two linearly independent absolute pocket
cohomology classes Qx,Qy spanning an isotropic plane for cup product.
If their plane lies in F, and F is symplectic, dim_R(F)>=4: an isotropic
subspace in a symplectic space of dimension2r has dimension at most r.
A two-dimensional F cannot contain this two-dimensional isotropic plane.
This eliminates the proposed *Forni hiding* mechanism whenever one can
independently prove dim_R(F)<=2. No such uniform bound has been proved
for our room class. An isotropic plane in a symplectic space of dimension4
is possible; the local algebra alone does not give a contradiction.

## 4. What the audit changes

[done] The shortcut “nonzero absolute slide implies some loaded cylinder”
is not a valid general-surface theorem. Any proof using it must establish
a room-specific hypothesis. The standard genus-three blind translation
factor is excluded by an elementary local-angle argument, but that does
not remove the general obstruction.

[in progress] Even a theorem supplying a loaded cylinder would leave the
actual-event overlap/cancellation requirement in Sections9 and32. Our goal
is not just to find a class z with Q(z)!=0. It requires the class of a legal
one-corner midpoint event between the specified S and T.

**Next move:** ask whether the room's real C4 quotient and literal-pocket
neck plane force a noncompact, event-coupled homology component. Establish
that implication or expose an in-class obstruction before restarting any
coordinate catalogue. Opus retains the separate actual-seed existence task.

Validation: `pocket-structural-check.py` checks only the prescribed seven
local-angle formulas and local covering-order arithmetic; it is not proof
of any orbit-closure or universal detection assertion.

## 5. Full topological twists detect the neck plane; affine realization is missing

[done: theorem application, pending peer check] For the quotient q:X->X/C4,
the four necks b_j are lifts of the simple circle bounding the pocket disk.
Thus beta=b_1-b_3 lies in the lifted-simple-curve homology subspace C_q.
[TheoremB of Boggi–Putman–Salter (2024)](https://academicweb.nd.edu/~andyp/papers/HomologyCovers.pdf)
makes C_q symplectic. Since beta!=0, some lifted simple curve c has
<beta,c>!=0. Choose its base circle delta; write c_i for all its lifts.
A sufficiently divisible Dehn twist lifts to a multitwist with positive
integer powers m_i. Choosing its sign convention so

    (tau_*-I)z=sum_i m_i <z,c_i> c_i,

and using31.1 gives

    Q_x((tau_*-I)beta)=sum_i m_i <beta,c_i>^2 > 0.

This is a universal TOPOLOGICAL detector for the absolute neck class.
Neither beta nor its increment is an actual S/T event. The lifted twist
need not be affine, preserve straightness, or preserve zero holonomy.
It therefore supplies no optical detector. It isolates the missing step:
replace these physical-sphere twists by permitted flat affine actions
while retaining a genuine event between the specified marks.

The same paper's TheoremB applies to the unit-torus cover X->R²/Z²,
branched only at0. On a once-punctured torus every essential simple curve
has a straight rational-slope representative avoiding0. Its lifted curves
are cylinder cores, so the span C_flat of ALL rational cylinder cores is
symplectic. This last argument uses the ONE-puncture unit torus; it must
not be substituted unchanged for the four-puncture2-lattice torus.
There is no proved inclusion of the physical neck plane in C_flat.
The two covering maps have different simple-curve lift subspaces.

In particular, proving that a nonzero neck combination belongs to C_flat
would prove existence of a loaded cylinder: a nonzero vector in the
symplectic space C_flat cannot annihilate that space. That hypothesis is
not inferred from its membership in C_q. Even that loaded-cylinder result
would still require the actual-event coupling from Sections9/32.

## 6. The stronger axis-only inclusion is false in a frozen actual room

[done: focused hand review64930 ACCEPTS scoped, with exact-type/index/plane
certificate hardening incorporated; no independent rerun claimed] Use the already frozen
raw room `parity-W25-24` and its saved40horizontal/vertical core classes.
No new core or direction is computed. This is a counterexample to the
AXIS-ONLY homological shortcut, not to all-cylinder inclusion or detection.

The pocket has B=(1,1), A=(2,2), C=(1,2). Its two outer vertical flanks
are walls1and4, both oriented by the normal(-1,0), with line offsets c1,c4.
Transport the neck crosscut alpha between these two flanks. Its doubled
boundary loop in the identity and vertical-reflection copies has period

    hol(b0)=Delta(alpha)-V Delta(alpha)=(2(c1-c4),0).

The affinely translated reflection at the upper endpoint yields this same
formula: the lower and upper x coordinates are -c1 and -c4. The constant
reflection translations must not be dropped in the development. Quarter
turns give hol(b1)=(0,2(c1-c4)), hol(b2)=-hol(b0), hol(b3)=-hol(b1).
These are period formulas under the larger fixed-angle room deformation
space, not a claim that the two flanks stay collinear in that space.

Take the exact offset velocity

    delta c4=-1, delta c20=+1, all other offsets and both marks fixed.

For EACH of the80saved scalar core-period derivative rows, its entries at
columns4and20are identical. Hence all40vector core periods have derivative0
on delta. In contrast,

    d hol(b0)[delta]=(2,0), d hol(b1)[delta]=(0,2),
    d hol(a*beta0+b*beta1)[delta]=(4a,4b).

Here beta0=b0-b2, beta1=b1-b3 are31's actual antisymmetric neck classes.
Any fixed real homology combination of the40axis cores has period
derivative0 on delta. Thus no nonzero element of their neck plane belongs
to the axis-core span in THIS room. This conclusion does not require the
period-form map to be injective: equality in homology would necessarily
imply equality of these transported period derivatives.

The offset change is a legitimate small fixed-angle polygon deformation:
adjacent supporting lines stay nonparallel, all edge lengths remain
positive, the simple boundary and interior marks persist by openness.
It moves the upper right flank and a separate diagonal wall, so it is NOT
the literal pocket slide. It is used solely as a separating functional
for a proposed HOMOLOGY identity at the base. Such an identity would hold
under every sufficiently small material deformation, making this test valid.

`pocket-structural-axis-forms.py/json` pins the original coupling/twist-action/twist-pf input hashes,
checks the inherited20+20unit-annulus/112-square coverage ledger,
checks all80entry equalities exactly, and records the sparse separating
velocity. A separate exact RREF of the40vector forms has rank20 and also
rejects both neck period forms; the80scalar forms have rank10. These are
checks of the saved forms, not a new optical computation. Complete axis
coverage is inherited from the earlier cycles(r)/cycles(u) construction
and its prior verification; it is not independently rebuilt here.

**Consequence for the next proof attempt:** a proof that the necks lie in
C_flat must use genuinely non-axis cylinder classes or a different global
argument. The axes cannot supply that inclusion, even though they remain
useful for sign transfer after an actual detecting event is supplied.
