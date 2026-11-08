# Optical cover mechanism: a strict limitation on small reflex reductions

Author hand lemma for independent review. This is a negative result about
ONE proposed optical mechanism, not about existential rerouting, illumination
or a bound on the degree/size of arbitrary rooms. Keep every regular sheet.

## Question and exact scope

Can one of the accepted strict-r geometric reductions be implemented by a
finite affine branched cover between the COMPLETE connected physical
orientation unfoldings, so that projecting or lifting a simpler-room ray
would supply an original-room ray? Such a cover would still need a separate
actual-target lifting argument. Here we first test whether the cover itself
can exist, without forgetting the surface or corner data.

Let D and E be finite strictly simple orthogonal rooms with r and r'
reflex corners, respectively. Their standard connected four-copy
translation unfoldings M_D and M_E have genus g=r+1 and g'=r'+1.
Each physical reflex corner has one zero of order2 (angle6pi), and every
other point is regular as a translation-surface point. Convex physical
corners remain named regular marks; they are not discarded as physical
obstacles merely because their differential order is0.

The hypothesis examined is a finite affine branched covering f:M_D->M_E
with one fixed invertible derivative on regular flat charts. Composing an
orientation-reversing map with a conjugation, or applying a common linear
deformation to its target, makes the map a translation/holomorphic covering
without changing its degree, topology, local cone multiplicities or this
obstruction. This is the standard full-surface affine-cover mechanism.
Arbitrary direction-dependent rerouting, discontinuous partial maps, local
reflection words or correspondences are not assumed to be such covers.

## 1. Genus alone already rules out most one-corner reductions

For a degree d finite branched cover, Riemann-Hurwitz gives

    2r = d*(2r') + B,  B>=0,
    r >= d*r'.                                      (1)

A degree1 cover between compact connected surfaces has no ramification
and is an isomorphism. It cannot change genus. Thus r>r'>0 requires d>=2,
and in particular r>=2r'. In the reverse direction M_E->M_D, already
2r' >= d*2r is impossible for every d>=1 when r>r'>=0 with r>0.

For a C1 reduction r'=r-1, every r>=3 satisfies r<2r'. Therefore there
is NO affine finite cover in EITHER direction between the full unfoldings.
This includes every adjacent reflex decrease8->7,7->6,...,3->2 relevant
to the programme. It does not exclude a non-cover optical argument.

## 2. The actual zero orders give a sharper restriction

At a point of local covering degree e, cone angles multiply by e. Equivalently
the differential orders satisfy

    k_source+1 = e*(k_target+1).

Since each order is0 or2 here, the possibilities are only:

- target order2: e=1, source order2;
- target order0: either e=1, source order0, or e=3, source order2.

Thus every target zero has exactly d DISTINCT unramified source zeros.
Every remaining source zero is a degree3 branch point over a regular
target point. If b is the number of those remaining zeros, then

    r = d*r' + b,   B=2b,   b>0 implies d>=3.          (2)

For r'>=1, a nontrivial cover therefore has one of these necessary forms:

    d=2: r=2r', b=0 (unramified everywhere);
    d>=3: r>=3r'.

In particular the whole interval 2r'<r<3r' is ALSO impossible. These
conditions do not assert sufficiency or physical realizability. The
exceptional adjacent decrease2->1 is not excluded: topology allows an
unramified double cover, subject to geometry, physical symmetry, marks
and actual-target monodromy. The adjacent decrease1->0 can have torus
targets with degree>=3; no universal upper degree is inferred there.

No degree bound on M_D's square count or primitive torus quotient is
obtained. Indeed the old six-wall unbounded primitive-degree controls
remain intact. Formula(2) only restricts covers to THIS prescribed simpler
full unfolding when its genus is positive. No regular component is
suppressed to make the inequality work.

## 3. Consequence for the accepted reduction programme

The accepted geometric C1 move decreases r by1. For r>=3, its optical
transfer cannot be supplied by an ordinary finite affine cover between
the complete two room unfoldings, in either direction. This statement
does not depend on a convenient endpoint lift, and allowing alternate
target monodromies cannot create a cover that topology rules out.

For H/V completions that remove more reflex corners, equations(1)-(2)
give the corresponding necessary test. A cover is not ruled out solely
by these counts when, for example, r'=0; but its existence and correct
actual endpoint transport still require proofs. Inherited accepted
full-fiber and physical-symmetry qualifications remain in force.

This is a precise reason to abandon the finite-affine-cover implementation
for adjacent-genus reduction, not to abandon the geometric system or claim
that its existential transfer is false at r<=8. The remaining positive
mechanism must genuinely reroute, use a different relation with independently
proved endpoint behavior, or select another reduction. Nothing here
proves the target or exhibits a low-r dark room.

## Dependencies and status

The full-surface genus and order counts were already independently accepted
in construction/genus-and-degree-review.md and review/genus-and-degree.md.
The new application is to covers implementing the specific strict-r
geometric reductions. The Riemann-Hurwitz calculation is hand mathematics;
no census, coefficient fitting, degree suppression, new engine or numerical
test is used. Independent review is requested before treating this mechanism
exclusion as accepted. Native geometric goal remains active and unfinished.
