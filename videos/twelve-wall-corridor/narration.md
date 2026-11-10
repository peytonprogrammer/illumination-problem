# Light through a twelve-wall corridor

## Light through three offset chambers

Put a source in the lower chamber and a target in the upper chamber of this offset mirrored corridor. The theorem guarantees a legal finite connecting ray for every such pair, with arbitrary positive real dimensions. The proof combines explicit unfolding geometry with exact computer certificates. It is a statement about a particular room family, not every twelve-sided polygon.

## Four parameters define the room

The lower chamber spans x from zero to two d and has depth h minus. The middle spans d to three d, over height g. The upper returns to zero through two d and has depth h plus. The overlap intervals at the joins are open portals. The exterior boundary has twelve maximal walls and four reflex corners.

## What counts as a connection?

A legal path reflects only at smooth exterior wall points and avoids every physical corner. The source and target lie strictly inside their outer chambers. The dashed portals are passages, not mirrors. There is no uniform bound on reflection count, and the theorem does not assert illumination for every other pair of points throughout the room.

## Why axial scaling is allowed

Scale horizontal coordinates by one over d and vertical coordinates by one over g. For horizontal and vertical mirrors, reflection simply reverses one velocity component. This diagonal scaling commutes with those sign changes, so legal reflected paths and corner avoidance survive. This special argument does not justify arbitrary affine shears of billiard rooms.

## Reduce to the left portions

In normalized coordinates the outer chambers have width two and the portals run from one to two. If both marks are in the right portions, a direct segment works. Mixed left and right placements reduce to an orientation-controlled L-room construction using genuine walls. The remaining domain has both horizontal coordinates positive and at most one.

## Unfold a route through the portals

The proof first works with effective endpoint depths U and V in unbounded outer strips. An admissible chart will produce an outer-simple connection: it reaches each portal strictly, has no earlier portal visit in the initial outer piece, and stays in the middle rectangle between the first and last crossings. End-wall caps are handled afterwards.

## One straight developed line

Choose u equal to zero or two, epsilon equal to plus or minus one, and an integer M. The horizontal target image is u plus epsilon t plus four M. A straight line from the developed source to that image determines the horizontal coordinate X of z. The four-unit period comes from reflecting a strip of width two.

## The portal values are affine

Evaluate that line at the portal and ledge levels, calling the values E sub j. Their residues modulo four determine which folded copies match. The admissibility conditions are strict open boxes in these portal residues. A table in the manuscript specifies the compatible folding signs, so positions and velocities agree when the ray crosses a portal.

## A one-pass chart

For one pass, the physical height simply increases through the middle band. The compatible portal box puts both crossings strictly inside the open intervals from one to two. Horizontal folding may add vertical-wall reflections, but none occurs at a portal corner. The displayed fixed example is obtained from one of the manuscript’s equal-depth charts.

## Why allow three middle passes?

One-pass charts alone are not the complete proof strategy. A three-pass chart unfolds the middle rectangle through three vertical bands. After folding, the ray goes up, down, and up through the middle. The two intermediate ledge contacts must lie strictly between x equals two and x equals three, avoiding both endpoints.

## Every extra bounce needs a strict guard

At the middle ceiling and floor, a three-pass route reflects on the actual ledges to the right of the portals. The strict ledge guards exclude the reflex and convex corners there. At an open portal, adjacent formulas match position and derivative. We do not bend the ray by hand or insert a mirror across a passage.

## The four endpoint sheets

The actual source depth is a and target depth is b. Reflecting them in the outer end walls supplies alternative effective depths A and B. Their four combinations are called sheets. A chart on any one of those sheets can be transferred back to a path between the actual source and target in the finite room.

## Fold across the end-wall caps

If a sheet uses the reflected source depth, fold the portion below the lower end wall back into the chamber. The symmetric operation handles the upper end wall. Ordinary cap contacts add legitimate smooth reflections. The edits take place outside the portals and preserve the middle chart, including all of its strict guards.

## A candidate cap corner is not allowed

The proof does not permit a ray to reflect at a cap corner. Instead, symmetry of the triangular fold shows that a lower cap-corner candidate returns to the actual source after that event; discard the prefix. At the upper cap, the actual target is reached before the candidate corner, so stop there. This removes the forbidden event from the connecting subpath.

## A complete five-reflection example

The manuscript’s displayed example uses effective depths one and one, with three middle passes. After cap transfer, the actual ray has five reflections: the lower end wall, three middle walls, and the upper end wall. Its source and target are the exact marked points shown here, and both portal crossings are strict.

## Equal depths have a separate argument

The universal proof next shows that some chart succeeds, or supplies a separate explicit connection. Equal effective depths are handled first using arithmetic progression windows. Irrational phases are dense modulo four; sufficiently fine rational grids hit a window; and the few small denominators have explicit formulas. Thus a hypothetical failure cannot have an equal-depth sheet.

## Irrational data: use the orbit closure

For a sheet, define alpha as U over H and beta as U plus one over H. If the phases have no integer relation, their joint orbit is dense in the torus. With an integer relation, the closure is instead the full corresponding level set, including its components. The proof must check that this closure actually meets an admissible open portal box.

## Short relations need exact coverage

When the relation coefficients have total absolute size at least five, the relevant open box is large enough to meet the closure. Thirty short primitive triples remain. Certificate C one checks their continuous endpoint domain, with two centered exceptions. The manuscript handles the remaining centered case by an explicit path. This is not a numerical sampling argument.

## Rational phases give a finite grid

For rational vertical data, the orbit is finite. A sampling lemma shows that when the phase denominator exceeds one hundred and there is no short relation, every translated orbit meets each open unit square. Short relations are handled using strict-margin covers and their own denominator cutoffs. Only a bounded arithmetic remainder remains.

## A necessary support, not a dark set

The finite-support proposition says that failure of all one-pass charts forces the effective depth pair onto one of ten lines or eleven isolated points. Being on that support does not mean the pair is dark. It only identifies where this particular chart method needs further work. The four endpoint sheets must all lie in that support if illumination fails.

## Four sheets form a rectangle

The four depth pairs form the corners of a rectangle in the U,V plane. Exact elimination over assignments of the ten support lines gives ninety one-parameter families and isolated cases, with no higher-dimensional solution. Sixteen families have an equal-depth sheet and are already covered. Seventy-four families remain for the next reduction.

## A positive margin bounds the remainder

On those families, the proof combines one-pass and three-pass windows with a fixed positive margin. Certificate C five covers the closed endpoint square by three hundred twenty-four clauses. The margin gives enough room for rational orbit spacing to force a hit above a bounded denominator. This turns infinite parameter families into finitely many exceptional rooms.

## Exactly 22,538 residual rooms

Certificate C six enumerates the remaining list: twenty-two thousand three hundred twenty-eight family members, forty-four further isolated rectangles, and one hundred sixty-six additional rectangles through the exceptional support points. The finite list follows from the analytic and arithmetic bounds. Merely trying rooms up to a chosen size would not prove this reduction.

## A chart covers a continuous region

In a fixed rational room, every selected chart supplies four or eight strict rational affine inequalities in s and t. Their conjunction describes an open region of actual endpoint coordinates. The picture shows the four exact guards of one equal-depth chart, not an arbitrary grid of tested point pairs. A single valid region covers infinitely many endpoint pairs.

## Boundary pieces must survive subtraction

Certificate C seven starts with the closed endpoint square and subtracts the chart regions using exact rational arithmetic. It retains boundary segments and isolated points rather than dropping them through numerical tolerance. Only pieces on the excluded axes s equals zero or t equals zero may be discarded without a chart. Every final admissible complement is empty.

## What the computer-assisted claim means

The manuscript records seven certificate stages, including seven hundred seventy thousand nine hundred twelve saved clauses and over three million integer guard identities in the final cover. These counts describe the archived proof record; this video is not a fresh replay of that full corpus. The reasoning depends on the exact reductions and guards, not on the counts alone.

## Geometry and certificates complete the route

The proof now closes. Normalize and reduce the endpoint placement. Use folding charts and cap transfer. Resolve equal and irrational data, reduce the rational remainder to a finite list, and cover its continuous endpoint domains exactly. This establishes the stated outer-chamber theorem, without a uniform reflection bound or a claim about every twelve-wall polygon.

## A proof map for a precise family

The visible ray constructions explain what the certificates certify: genuine smooth-wall paths to the actual target, with strict portal and ledge clearance. The manuscript contains the full chart tables, arithmetic reductions, and certificate dependencies. It is by Daniel Wang and Peyton Wang, with Codex and Claude assistance, and remains a working draft without external refereeing.