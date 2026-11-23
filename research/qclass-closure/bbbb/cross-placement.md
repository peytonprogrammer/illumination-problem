# One capped arm lights a perpendicular arm

**Theorem for independent review.** In the strictly simple cross
P_b = ([−b,b] × [−2,2]) ∪ ([−2,2] × [−b,b]), every pair of distinct real interior points is lit for every odd integer b≥15. For every odd b≥11, every nondirect same-parity interior lattice pair has a legal path with a regular midpoint outside the source parity class. Direct pairs are already lit. Together with d87's finite certificates at b=7 and 9, ordinary illumination holds for **every same-parity interior lattice pair at every odd b≥7**. The finite certificates at 7 and 9 are used only for ordinary illumination.

This addresses the entire endpoint question on a family of area 16b−16 with four reflex corners. On this very family the two whole-room cylinder tests fail in every primitive direction, and the two axial affine stabilizers together preserve each lattice kernel orbit. The proof constructs a nonaxial shot directly. It does not assume that a global affine symmetry takes the endpoints to a visible pair. [Whole-room obstruction](every-direction.md) · [Axial subgroup obstruction](axial-stabilizers.md) · [D87 finite checks](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d87-review-cross-corners/review.md)

## The placement lemma

Use local coordinates at the meeting corner of two perpendicular arms. A central open rectangle (−W,0) × (−H,0) connects the right arm (0,L) × (−H,0) to an upper arm of horizontal span (−W,0). The right arm has reflecting sides at heights −H and 0 and a full reflecting cap at x=L. The two openings to the central rectangle are its full right and top sides. Assume the upper arm is unobstructed between its mouth and the target. The rest of the room is unrestricted if these wall and opening conditions hold.

Let the source be (X₀,−U₀), with 0<X₀<L and 0<U₀<H, and the target (−V,Y), with 0<V<W and Y>0. Write X=2L−X₀. **If X>3V, there is a legal shot via the right cap to the target. Either prescribed choice of transverse source-image sign works.**

Reflect the right arm in its cap and unfold its horizontal sides. The source images are (X,−U) with U in either of the progressions ±U₀+2H times an integer. Join such an image to (−V,Y). For the line to cross x=0 inside the open right doorway, the exact condition is

    XY/V < U < XY/V + H(1+X/V).

Indeed the ordinate at x=0 is (XY−UV)/(X+V). Under this strict condition it is between −H and 0. The next crossing of y=0 is strictly between x=−V and 0, hence inside the top doorway. Both crossings and the whole central leg are regular. The final segment stays in the upper arm without a side reflection. No assumption on Y other than positivity is used.

The open interval has length greater than 4H, so it contains **two consecutive images in the prescribed progression**. Return across the right cap might hit a cap corner; this is the only remaining forbidden contact. At x=L the ordinate changes in absolute value by

    2H (L+V)/(X+V)

between the two images. This lies strictly between H and 2H: use X=2L−X₀, X₀>0, and X>L. The forbidden cap ordinates are H times the integers. Hence the two candidates cannot both hit a cap corner. All other right-arm contacts are transverse reflections on open horizontal walls, since they occur away from the cap and doorway. Folding the successful line proves the lemma. The unequal endpoint heights and abscissas in this development give a nonaxial shot.

## Whole-cross application

Two marks in the same bar see each other directly. For interior room points the only possible chord along a bar side with both endpoints interior lies within the other bar's interior. Every nondirect case therefore reduces by symmetry and exchange to S=(s,u) in the right arm and T=(v,t) in the upper arm, with 2<s,t<b and |u|,|v|<2. Shift the corner (2,2) to the origin. Then H=W=4, L=b−2, X₀=s−2, U₀=2−u, V=2−v, Y=t−2. For real marks and b≥15 we have X>L≥13 and 3V<12. This proves the all-real statement. For lattice marks V≤3, so b≥11 gives X>L≥9≥3V. The same inequalities hold with the roles of the two arms exchanged.

## Forcing a regular off-class midpoint

Assume S,T have the same lattice parity. In the original coordinates the right-cap source image has abscissa 2b−s and ordinate u or 4−u modulo 8; those are exactly the two transverse sign choices in the lemma. The actual target is (v,t). For the first sign the developed displacement is, modulo four,

    (s+v−2b, t−u).

For the alternative sign the second entry is t+u−4. Reversing the roles and using the upper cap instead gives, with the first transverse sign, the displacement (s−v,u+t−2b) from the upper-cap image of T to S. All entries are even. If either first-sign vector is nonzero modulo four, use that route. If both vanish, then s≡v and t≡u modulo four, and 2v≡2u≡2b modulo four. Since b is odd, u and v are odd. Switching the right-cap transverse sign changes the second entry by 2u−4, which equals 2 modulo four. The placement lemma still gives a legal shot for that sign. This exhausts all lattice cases.

The developed endpoints fold to the given marks and have their parity because every mirror is an integer-coordinate line. Half the chosen displacement changes parity. Folding the half-time point also preserves its parity: the midpoint is a regular off-class lattice point, possibly on a smooth reflecting wall. By d82's correspondence it is a reached coincidence for the marked pair. [Midpoint dictionary](midpoint-necessity.md)

**Scope.** The reusable hypothesis is a full-width entrance and a second open side of a rectangular turn, with enough horizontal travel relative to V to admit two consecutive images. A shorter doorway or an obstruction in the upper arm changes the placement interval. The proof gives no implication from reflex count alone that a general BBBB pair has this geometry. No discovery search was used.
