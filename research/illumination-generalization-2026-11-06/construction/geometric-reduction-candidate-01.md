# C1: non-nested rectangular corner completion

Published before control testing, 2026-11-07. This is a conjectured optical
transfer with explicit geometric prerequisites, not a proved reduction.

## Quantified target and transformation

Let D be a finite strictly simple orthogonal lattice polygonal disk with
1<=r(D)<=8. Let S,T be distinct actual interior even-even lattice points.
Allow any translation and axis rotation of the following local description.
The boundary contains three consecutive vertices

    A=(0,H), C=(0,0), B=(L,0),   H,L positive integers,

with A,B convex and C reflex. The preceding edge approaches A horizontally
from x<0 and the following edge leaves B vertically toward y<0. The open
rectangle R=(0,L)x(0,H) is exterior to D. Its other two sides, and its
new corner (L,H), have no contact with D except the existing vertices A,B.
No other boundary vertex lies on the two selected old edges AC,CB.

Replace AC union CB by [(0,H),(L,H)] union [(L,H),(L,0)]. Equivalently,
take the closure of int(D union [0,L]x[0,H]) and call it D'. No point or
coordinate is moved. S'=S and T'=T literally. The isolation hypotheses
are intended to make D' a strictly simple orthogonal lattice disk.
The proposed complexity is r. The geometric claim is r(D')=r(D)-1.

## Optical candidate (unproved)

For EVERY D,S,T and isolated rectangle satisfying these hypotheses with
r(D)<=8, if D' admits a finite actual S-to-T corner-avoiding specular ray,
then D also admits such a ray. The new ray may have a different direction,
number of reflections and reflection word. No fixed-word continuation,
same-mouth-point return or coordinate projection is assumed.

This is deliberately restricted to low-reflex actual rooms. An obstruction
outside r<=8 would reject an r-independent strengthening, not this candidate.
Failure of one chosen D' ray in D would not refute the existential statement.

## Global induction obligation

An induction with only C1 additionally needs: every nonconvex target room
either is already proved illuminated for its actual pair, or admits at least
one isolated completion rectangle of this form. This availability is OPEN;
the three-vertex condition and rectangle isolation cannot be omitted.
The convex base is the actual direct segment in D.

The reviewer's r1 L-room obstruction to contained deletion does not apply to
this non-nested move: S,T remain interior after adding area. It nevertheless
warns against replacing the OPEN availability theorem with an ear assertion.

## Bounded success criteria and strongest objection

First prove the geometric surgery and complexity change. Next decide whether
a local existential optical argument can distinguish r<=8 from r=9; if no
such use of the bound appears, do not present a local argument as a universal
transfer theorem. A prescribed known22 control may challenge the stronger
r-independent claim. Separately test the availability prerequisite by hand,
with exact original marks and strict simplicity retained.

Strongest objection: the filled rectangle adds actual new mirrors and
developed target images. Existence in the enlarged room may depend on them;
their disappearance is not repaired by a failed chosen-ray lifting map.
No positive transfer theorem is asserted without resolving this objection.

Original conservative focused allowance: 2026-11-07T16:44:47Z through
2026-11-07T16:58:47Z, including programme/setup/prior-work reads and all C1
adaptive checks. No deadline renewal. Hand reasoning and independent review
are not represented as a new discovery allowance. No new orbit/room census,
workers, parameter sweep, fitting, engine or git mutation.
