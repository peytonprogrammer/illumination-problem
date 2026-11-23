# Round 2: corner-charge bound for non-clean (1,3,4) pi/8 rooms

Same rules: read-only, no searches, under 1,000 words, PROVED / CITED /
GUESSED. Do the mathematics.

Your round-1 next move. Rooms are strictly simple polygons glued from
reflected copies of the triangle with angles pi/8, 3pi/8, pi/2. The
reviewed bound for a dark interior A pair is only W >= 16
(`d7-review/review.md` lines 80-230 and `d7-wolecki-triangles/theorem.md`);
the 30-60-90 and (1,2,5) cases reach 27 and 32 through clean-room
arguments, and every (1,3,4) room is non-clean. Searches found no dark
(1,3,4) room with <= 6 extra tiles up to W = 23; a 20-wall room with 38
tiles needed a 12-reflection path through a flat C point.

1. Derive a corner-charge bound: for a dark interior A pair, charge each
   transparent right-angle (C) vertex image and each B-tip to boundary
   corners, using your checkpoint criterion (every path must meet an
   A-fixed point midway; non-A preimages with p = 1, q even must be
   corners or the midpoint argument fails). Aim for W >= 22, or find the
   exact configuration where the charge argument allows fewer walls.
2. If a configuration below 22 survives, describe it concretely (tiles,
   which C points are transparent, the pair) so a search can test it.
3. Does the same argument extend to other right triangles with a
   pi/(2h) angle (pi/12, 5pi/12, pi/2; pi/10, 2pi/5, pi/2)?

End with the bound you can prove for (1,3,4) and your confidence.
