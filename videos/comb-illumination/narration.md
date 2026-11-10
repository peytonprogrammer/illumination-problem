# Light through comb rooms: a finite matching proof

## More walls, still a route

The twenty-two-wall dark room might suggest that enough corners can always trap light. This comb theorem gives a different lesson. A room may have arbitrarily many teeth and still guarantee connections for a specified class of points. The key is not a bound on walls, but a geometric structure we can exploit.

## The endpoint condition matters

The room consists of a rectangular spine and finitely many separated rectangular teeth attached on one side. A marked point may lie anywhere inside the spine, or on the middle horizontal line of a tooth. Every pair of distinct interior points in that class illuminates. Arbitrary off-middle-row tooth points are outside this theorem.

## Choose two teeth

The hard case selects two different teeth, one below the other. Translate vertically so the lower tooth spans zero to u, and the upper spans H minus v to H. Their positive gap gives H greater than u plus v. The marks lie at heights u over two and H minus v over two.

## Name the horizontal distances

Let c be the spine width. The source and target lie distances D sub s and D sub t beyond their mouths. Both distances are positive, and their far walls are farther out. A is the sum of these two distances plus twice the spine width. These are arbitrary positive real numbers.

## What must the ray accomplish?

The planned route leaves the source tooth through its open mouth, crosses the spine, reflects once at the actual left wall, and enters the target tooth. Inside a tooth, the ray may reflect from its horizontal walls. The other teeth never enter this route, however many there are.

## Unfold the tooth reflections

Unfold reflections across the horizontal tooth walls. For a point exactly halfway up a tooth of height u, the two signed image families combine into one progression, u over two plus integer multiples of u. That half-period spacing is special to the middle row. An arbitrary endpoint height would not have the same property.

## Count how many folds are needed

Use tau for the positive absolute vertical slope. The two floor functions shown here count the selected tooth folds. As tau increases, neither count decreases. Between jump values, the counts stay constant. At a jump, the associated unfolded mouth position lies exactly at the end of a tooth aperture, which we must avoid.

## Match the height budget

Now define the matching map Phi. Its numerator is the vertical separation between the middle rows, plus the unfolded heights contributed by the two fold counts. Its denominator is A. A fixed point, tau equals Phi of tau, will make the two tooth pieces and the spine piece fit the same slope.

## Start the iteration at zero

Phi is nondecreasing, and Phi of zero is positive because the teeth are separated. Start at zero and repeatedly apply Phi. The first step increases; monotonicity then makes every later step nondecreasing. This is not yet enough for a finite construction. We also need a bound and a finite range.

## Trap the iterates in a bounded interval

Use floor x less than or equal to x to obtain the displayed upper bound. At tau equal to H over two c, that upper bound is tau itself, because A equals D sub s plus D sub t plus two c. Monotonicity therefore keeps every iterate in the interval from zero to H over two c.

## Finite range gives an actual stop

On this bounded interval, each floor function can take only finitely many integer values. Consequently Phi has only finitely many output values there. A nondecreasing iteration among those values must eventually repeat a value, and then it is stationary. We get an exact finite stopping point, not just convergence toward a limiting slope.

## The stop cannot occur at a jump

Take the first stationary iterate tau sub j. The preceding iterate is strictly smaller. If the source fold count jumped at tau sub j, Phi there would exceed Phi at the previous iterate by at least u over A. But Phi of the previous iterate is already tau sub j. That contradicts the fixed-point equation. The target count is identical.

## Both mouths have strict clearance

Define the remainders r sub s and r sub t by subtracting the selected integer tooth heights from the unfolded mouth coordinates. Floor division puts them between zero inclusive and their tooth heights exclusive. Zero occurs precisely at a jump. Since the fixed point is not a jump, both inequalities become strict. The fixed-point equation gives the matching identity.

## Why parity of the fold count works

Write the source fold count as even or odd. For an even count, launch with positive vertical sign; for an odd count, use negative sign. Because the source lies at the middle height, these choices represent genuine reflected source images. The formula reaches the lower mouth at height r sub s, moving upward.

## Every tooth contact is smooth

The source tooth segment travels left, so its wall contacts occur strictly before the mouth and strictly to the left of the source and far wall. The strict remainder keeps the last reflection away from the aperture endpoint. Every contact is therefore on a smooth horizontal tooth wall. There are only finitely many of them.

## One spine reflection joins the mouths

The lower mouth is at c, r sub s. The upper mouth is at c, H minus r sub t. Reflect once at M, whose height is r sub s plus c tau. The matching identity makes both spine legs have the same absolute slope. M lies strictly between the mouth heights, so it is a smooth point of the actual left wall.

## Other teeth cannot interfere

The open spine legs stay strictly to the left of every tooth mouth. They cannot hit a boundary gap or enter an unwanted tooth. Reversing and reflecting the corresponding upper-tooth construction carries the outgoing ray to the actual target. The total number of reflections is n sub s plus n sub t plus one.

## Watch the matching map stop

Here is one fixed arithmetic illustration. Choose spine width two, tooth heights one, separation parameter five, and the two indicated horizontal distances. The iterates are zero, eight seventeenths, twelve seventeenths, then fourteen seventeenths. Applying Phi once more gives fourteen seventeenths again. The procedure has stopped exactly.

## A strict, four-reflection connection

The source count is one and the target count is two. The two remainders are one hundred sixty-seven over one hundred seventy, and one hundred twenty-three over one hundred seventy. Both are strictly between zero and one. The displayed construction has one source-tooth bounce, one spine-wall bounce, and two target-tooth bounces: four reflections in total.

## One point in the spine

What if one point lies in the spine? If its height lies inside the target tooth band, a direct segment works. Otherwise reflect the source in the left wall and consider the middle-row target images. Their induced mouth heights form a two-sided arithmetic progression with spacing strictly smaller than the tooth height.

## A small spacing finds an open mouth

An open mouth of height u must contain a member of that progression, because the spacing is smaller than u. The corresponding unfolded segment folds to a left-wall reflection and tooth reflections ending at the actual target. The mouth inequalities are strict, so no corner contact is hidden in this choice.

## Direct and seam cases complete the proof

Two points in the same tooth see each other directly. Spine points are directly visible unless both lie on different mouth seams. In that special case, the straight seam segment might run along boundary gaps. Instead reflect at the actual left wall, halfway between their heights. Both open legs stay inside the spine. All endpoint cases are now covered.

## Height-two teeth give a corollary

Suppose all boundary coordinates are integers and every tooth has height two. Any interior even-even lattice point outside the spine must lie on a tooth middle row. If the lower tooth height is even, there is no even ordinate strictly inside; if it is odd, the only one is the middle ordinate. Thus the theorem covers every interior even-even pair.

## Structure matters more than wall count

The proof never bounds the number of teeth, the area, or the room diameter. It selects two teeth and uses the open spine between them. Its scope remains precise: one-sided rectangular combs and points in the spine or on tooth middle rows. It does not establish illumination for all off-middle endpoints or all polygons with many walls.

## A finite matching proof

The central mechanism is a finite matching argument. A monotone bounded iteration has finite range, stops away from jumps, and supplies strict aperture clearance. That clearance turns an algebraic match into an actual corner-avoiding ray. The construction and proof are by Daniel Wang and Peyton Wang, with Codex and Claude assistance. The manuscript remains a working draft.