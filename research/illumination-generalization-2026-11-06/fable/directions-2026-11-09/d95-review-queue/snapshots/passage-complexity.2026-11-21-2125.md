# Unbounded passage count for a fixed horizontal band decomposition

**Theorem for review.** For the canonical horizontal decomposition there is no K(6) bounding the number of normal traversals needed to light every *lit* same-parity interior lattice pair. This already fails for the four-band normalized st279 end-square stretches. In these rooms a set of Ω(√m) target candidates at one prescribed height has the following property: all but at most B(6) are lit, and every lighting route to any of them has Ω(√m) passages. B(6) is the reviewed, noneffective ordinary endpoint shadow bound. No direction or word search enters.

## What counts as a passage

In a horizontal band one passage advances monotonically in physical y, with any number of reflections on its two vertical sides. It ends at the target, at a horizontal cut crossed into the next piece, or at an actual horizontal mirror where the vertical velocity reverses. A return through the same rectangle is another passage. This is the definition for which one phase congruence suffices. For width u, origin l, normal travel d and signed horizontal sheet e, put E(l,e,x)=l+e(x−l). The exit phase minus the entry phase equals ds modulo 2u, with s the nonnegative horizontal travel per unit of absolute vertical travel in developed coordinates. Carry the horizontal sheet across every interface and require the actual crossing or mirror window. At a simultaneous smooth-wall reflection use the one-sided outgoing germ. Axis-parallel paths can be tested separately. A whole visit that permits arbitrary normal reversals at a partially open wall additionally needs first-exit conditions.

## A uniform slope shift turns short routes into short physical words

Let m run through multiples of eight, tending to infinity. Use the four st279 widths m,3,3,m, with heights m,1,1,m. The source is S=(m/2,m/2). Take all targets

    T_j=(3m/2+2+2j, 5m/4+2),       |2j|≤√m.

The marks have even coordinates, are interior for sufficiently large m, and lie in opposite end squares. All are in the same normalized, strictly simple room with six reflexes.

Every intermediate full passage has ratio d/u equal to 1 in an end square and 1/3 in a middle band. The initial partial passage has ratio 1/2. The final partial passage has ratio 1/4 or 3/4. Hence in **every possible route**, 24d is an integer multiple of 2u on each passage. Replace a positive slope by its representative in (0,24] modulo 24. Folding proves inductively that every signed event occurs at exactly its original position. New or removed transverse bounces are on smooth vertical sides inside an open band; at a horizontal event the original legality is preserved. This works for arbitrary revisits and either initial vertical sense. A horizontal path cannot cross the separator; the two marks also have different abscissas. In the compressed path each passage has horizontal travel at most 24u. It has at most 25 transverse contacts and at most one terminal normal reflection. Thus a route with k passages gives an actual legal path with at most 26k physical reflections.

## A lower bound that applies simultaneously to the entire target row segment

Divide both axes by m. The source is exactly S₀=(1/2,1/2), all targets are within O(1/√m) of T₀=(3/2,5/4), and the first crossing into the neck is within 1/m of p=(1,1). Every mirror lies within 3/m of an integral mirror in these coordinates. Apply the full formal word to the target and its prefix to the crossing. At the limiting integral mirrors, in units of 1/4, any image of p is (0,0) modulo four, S₀ is (2,2), and every T₀ image has even abscissa and odd ordinate. The determinant of the two displacement vectors from S₀ is 2 modulo four, hence at least 1/8 in absolute value in scaled coordinates. For the actual trajectory it is zero.

For R reflections, the actual developed vectors have sup norms at most 3(R+1) by summing segment displacements. The coordinate replacement errors are at most δ=C/√m+6R/m with a single absolute C for the entire displayed row segment. Consequently 1/8≤12(R+1)δ+2δ². This excludes any subsequence with (R+1)/√m tending to zero, uniformly in j. Combining with slope compression gives k=Ω(√m). This is the determinant argument in [reflection-complexity.md](reflection-complexity.md), reproduced here for the different, fixed heights needed by the compression.

**Why this refutes a bound for lit pairs.** The row segment contains 2 floor(√m/2)+1 distinct physical targets. At most B(6) regular physical targets are hidden from S over the whole room. Thus for all sufficiently large m there are lit candidates, and indeed their proportion on this segment tends to one. This existence step does not identify a particular j as lit. It uses the ordinary physical endpoint theorem, not any proposed bound for synchronized lifts. [Uniform endpoint bound and literature dependencies](shadow-budget.md) · [Independent review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d86-review-shadow/review.md)

## Controls and scope

The d117 cov279 lit control uses two horizontal passages. The earlier constructed st279 shot uses four, but its endpoint heights were deliberately adjusted by O(√m) and do not give the shift 24. Fixing the heights exactly here is load-bearing. The bounded-width dumbbell witness has one horizontal reflection and a bounded number of passages. For resonant cov279 at 3|q the variable-entry repair for heights (1,3) has an unbounded count of cap traversals in the displayed construction. That counts its particular witness only. For (1,5) the halfway obstruction rules out the reviewed one-cap route for the aligned marked coordinates; the general lighting status remains open. No inference about that family's shortest route is needed here.

The negative theorem uses the **fixed horizontal decomposition** specified above. Interchanging axes gives the corresponding obstruction for a predetermined vertical convention. It does not exclude choosing the better of the two decompositions separately for each pair, nor a macro-description counting an arbitrary first-return loop as one instruction.

## Decision follow-on

For a fixed lattice room, fixed lattice pair and fixed finite route, acceptance is decidable directly. With integral event heights one may reduce the slope modulo 2 lcm(u_i), keeping the same signed events. There are then finitely many admissible transverse winding indices for each passage. Fixing those indices and sheets leaves linear equations and open interval tests in the crossing positions and slope, with the room dimensions constant. Smooth lip events can be included separately. For the unrestricted fixed room, the finite marked-cover directional test in [route-residues.md](route-residues.md) still applies.

Across variable rooms the congruence contains both u_i times an integer winding and d_i times an unknown slope. A finite route list would not by itself establish ordinary Presburger definability. There is even an exact example for an open-door route on specified sheets in the previously used height-five dumbbells. Use left width U, right width U+1, corridor length L odd, and marks (1,1) and (2U+L,3). They have matching parity. The two horizontal passages below and above y=2 have widths U and 2U+1+L and unit travels. On the positive endpoint and crossing sheets the crossing abscissas form

    (1+2U+L)/2 + gcd(U,L+1)ℤ.

Require the crossing in (0,U). If the gcd is less than U it succeeds. Otherwise the translate misses exactly when 2U divides L+1. This statement is about the prescribed open crossing; a simultaneous reflection on the common wall or another sheet is a different certificate. For each even U≥4 the rejecting fiber in L consists of the single residue −1 modulo 2U. Such a relation cannot be Presburger in (U,L): quantifier elimination gives a Boolean combination of linear inequalities and congruences with finitely many constant moduli. At fixed U the inequalities stabilize for sufficiently large L, so the lcm of those moduli would be an eventual period for every fiber. No constant is a multiple of 2U for every even U. This does not rule out a different proof for the union of all possible routes.

A viable compressed description would need a repeat count and guards checking *every earlier return* to a partially open wall. The existing first-entry arithmetic is an example. Whether a bounded number of such instructions suffices remains open; a finite check on named rooms cannot certify the proposed universal bound.
