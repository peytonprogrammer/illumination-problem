# The remaining reflex-sector return obligation

The accepted reflex-coalescence theorem needs an actual corner-to-convex connection leaving the reflex vertex in its opposite interior quadrant. This connection may contain ordinary reflections. It does NOT follow from direct visibility or from two inward axis rays at low wall count.

## Prescribed sixteen-wall test geometry

Take the cyclic vertices

    (2,2),(4,2),(4,0),(2,0),(2,-4),(-2,-4),(-2,-3),(0,-3),
    (0,0),(-3,0),(-3,-2),(-4,-2),(-4,2),(0,2),(0,4),(2,4).

The room is the union of the central square [0,2]^2, the top/right arms [0,2]x[2,4] and [2,4]x[0,2], the left arm [-4,0]x[0,2] with down-hook [-4,-3]x[-2,0], and the bottom arm [0,2]x[-4,0] with left-hook [-2,0]x[-4,-3]. These rectangles join into a strictly simple hole-free orthogonal disk. Its boundary has sixteen genuine turns (six reflex, ten convex). Let O=(2,2), with missing NE quadrant.

The west and south inward axis rays first hit genuine reflex corners (0,2) and (2,0). Neither supplies a smooth normal return. The ONLY convex vertices strictly SW of O are (-2,-4),(-2,-3),(-3,-2),(-4,-2). They are all hidden: the lines from O to the first two leave the bottom arm above its hook (for example at y=-2), and the lines to the other two leave the left arm before its down-hook (for example at x=-2). The intervening points have negative x and y strictly between -3 and zero, outside the stated union. Thus a low-wall theorem asserting either a visible SW convex corner or a smooth first-axis return is false even at sixteen walls.

This is not a dark example. In fact the next paragraph supplies the required REFLECTED return, illustrating why the proper target is larger than direct visibility.

## A reflected return that succeeds

From O take velocity (-1,-3). It reaches the bottom hook after crossing the central square and bottom arm and has the exact ordinary contacts

    (0,-4),(-1/3,-3),(-2/3,-4),(-1,-3),
    (-4/3,-4),(-5/3,-3),

then reaches convex p=(-2,-4). No other corner is touched. The six ordinary wall indices are [4,6,4,6,4,6] in the displayed boundary ordering. All contacts are strict sidewall interiors. The developed p image is (-2,-10), strictly SW of O, so the accepted palindromic return criterion applies. The search found this prescribed-geometry witness after four directions; the displayed rational word itself supplies a hand proof independent of that discovery bound.

## Positive open question, not an assumed theorem

For an arbitrary reflex vertex of a low-wall orthogonal disk, can one prove existence of SOME finite corner-to-removable-convex-corner trajectory leaving in its opposite sector, with no intermediate corner? Equivalently for this purpose, produce an admissible non-strict limiting return with the right source/target sectors. Direct visibility and axis graphs are insufficient. The generic density theorem does not hit a specified corner, and a corner-to-corner connection must not be inferred from it. No universal existence or nine-reflex charge is proved here.

The prescribed sixteen-wall room is a positive calibration of the reflected version, not evidence that it always holds. Its scaled actual interior-pair family is resolved in reflex-return-calibration.md by a quantified tail and exact finite prefix.
