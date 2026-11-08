# Exact rectangular-band first-exit relation

2026-11-06, Codex01a18403. Standard unfolding identity, not a novelty claim. Purpose: test a bounded critical-skeleton mechanism while retaining arbitrarily many regular reflections. Hand proof only; no optical search or new code. Independent review pending.

## Model and exact statement

Let L,H>0. The open horizontal band is 0<x<L,0<y<H. Its entire horizontal sides are actual mirrors. The left and right sides contain entry/exit portals with OPEN height intervals I,J contained in (0,H). There are no other openings or corners along the horizontal sides. A path enters at (0,u), u in I, with velocity proportional to (1,m), m any finite real number. Stop it at its FIRST contact with x=L.

There is a legal exit through J if and only if there exist integer j, sign epsilon in {+1,-1}, and v in J such that

    u + m L = 2 j H + epsilon v.                 (B1)

The first exit is then (L,v) with velocity proportional to (1,epsilon m). All horizontal-wall contacts before that exit are smooth, and their number is finite. An exit at height0 orH is forbidden; open J excludes it. If the remaining parts of the end sides are mirrors, (B1) asserts the FIRST passage exits through J; it makes no claim about trajectories that reflect there and return later.

## Proof

Unfold successive reflections in y=0,H. Because vx>0 never changes inside the band, unfolded x increases strictly from0 toL and the unfolded height atx=L is z=u+mL. Refolding is the triangle wave

    F_H(z)=z-2jH             for 2jH<z<(2j+1)H,
    F_H(z)=2jH-z            for (2j-1)H<z<2jH.

The derivative is respectively+1 and-1, giving the stated outgoing velocity. These two open branches are exactly z=2jH+epsilon v,0<v<H. Conversely each such branch unfolds to one straight segment and refolds to the prescribed ray. If m!=0 the interior reflection times are exactly the finitely many levels kH strictly between u and z; each hit has0<x<L, so it is a smooth actual horizontal mirror point. Ifm=0 there is no reflection. This proves both directions with no count cutoff and no deletion of velocity sign.

For z/H not integral, the number of reflections is |floor(z/H)|, since0<u/H<1. This formula includes negative m. If m=0, floor(z/H)=0.

## Why the phase cannot be discarded

Take H=1,u=1/4,m=1,J=(1/8,3/8). For L=2 the ray exits atv=1/4 with positive slope and passes through J. For L=1 it exits atv=3/4 with negative slope and misses J. Both are exact first-exit calculations. Replacing a band by a shorter one while preserving its incidence pattern therefore does not preserve its transfer relation for a fixed incoming state. This is not a dark-room example: changing the initial slope can change that outcome.

Even recording the folded height alone is insufficient: the sign epsilon also matters for the next portal. The correct state is an unfolded phase modulo2H plus the directed velocity chart. Treating it merely as a point in[0,H] identifies opposite outgoing vertical velocities.

## What this does and does not reduce

For a prescribed finite itinerary of such bands, composing (B1) with the actual junction isometries is exact, with integer repetition variables retained. Ordinary D4 reflection charts change velocity by signed coordinate permutations; any slope inversion at a diagonal must be tracked. A prescribed connection satisfying all strict portal inequalities and final actual-endpoint equality is therefore a finite corner-avoiding witness in the ORIGINAL room.

There is presently NO proof that every relevant canonical45 room has a bounded-size optical skeleton consisting solely of these bands and controlled junctions. General convex/diagonal corners and multiportal pieces must be treated. There is also NO bound in W on how often a connecting trajectory must visit the critical pieces. The old six-wall reflection-count obstruction does not by itself refute a bound on critical visits, because many of its bounces lie in regular arms. Conversely, finite wall count alone does not prove such a critical-visit bound.

Thus the lemma provides an exact atom for a candidate strategy. The missing implications are: an exhaustive decomposition, exact junction scattering, and an actual-endpoint route/phase existence theorem at arbitrary length ratios. Without those, it is not an uncapped illumination theorem or a finite-case reduction.

## Bounded next test

Before implementing any search, analyze a single genuine reflex junction between perpendicular bands. Success is a phase-preserving scattering relation that remains exact for all numbers of wall contacts and explicitly handles its corner-hit boundary. The strongest objection is that a ray can revisit the same junction with a different phase; local solvability cannot be concatenated without fixing one global launch direction and the actual target lift. A universal claim from arbitrary concatenation is rejected.
