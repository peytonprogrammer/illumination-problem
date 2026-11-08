# Status: is there a dark simple room with fewer than 22 walls?

As of 2026-11-01. Peyton Wang led this investigation, with Claude and Codex as tools. This page summarizes `l3-analysis.md`, which has the statements, proofs, and review history. "Codex-reviewed" means Codex checked it adversarially and its corrections are in.

## Proved

| Result | Evidence |
| --- | --- |
| The 22-wall room is strictly simple and dark | Hand proof, plus two independent certificates |
| **Bounded theorem.** In the canonical 45° tiling, a strictly simple room with two dark interior A marks and at most 4 transparent points has at least 22 walls | Hand lemmas plus 31 SAT cases, each with a DRAT proof. Claude and Codex each checked the other's part. See `proof-guide-for-peyton.md` |
| The 22-, 24-, and 34-wall dark rooms are locally rigid: every nearby room of the same shape is lit, except stretched copies | Exact certificates. Both agents computed each one separately, and each replayed the other's |
| Wolecki's 22-wall pinch room is locally rigid, and every strictly simple room that opens its pinch slightly is lit | Claude's exact certificate at `R = 12` and `R = 18`, replayed by Codex with a clearance check at the pinch |
| Jain's 28-wall room, center to a wall midpoint, is dark and locally rigid, with the target free to leave the wall | Codex's parity proof and certificate at `R = 18`, replayed by Claude. The geometry comes from a video thumbnail |
| Robust lit paths survive small changes (Lemma 7), so a limit of dark rooms has no robust connection (Proposition 8) | Codex-reviewed |
| A separating pinch with a straight path through it is lit, for any neck shape (Lemma 10, Corollaries 11 and 14) | Codex-reviewed, with exact weights and bounded offsets |
| Two points in one open cylinder see each other (Lemma 12) | Codex-reviewed; the clearance shrinks as the grid refines |
| A mark near a corner sees out through every direction within `π` of its approach angle (Lemmas 15 and 22) | Codex-reviewed; Lemma 22 still awaits review |
| **Cost theorem.** A Jordan point collapse never raises the cost `W + 2B`, where `B` counts extra boundary blockers. Every collapse except an isolated smooth step lowers it | Codex's proof, checked by Claude |
| A mark in a thin dead-end corridor lights the room when the unfolded target is less than `2ℓ - d` from the mouth line (Lemma 21) | Claude's statement, with Codex's corner repair; both checked |
| **Sector density (Theorem 24).** On a lattice surface with rational points, connections from a corner to a point leave in a dense set of directions, if one exists | Codex's proof, checked by Claude |
| A *parity room* has every non-A lattice point as a corner. Parity rooms are dark, and every event has its corner at the unfolded midpoint (Lemmas 25 and 26). The 24-, 34-wall, Wolecki, and Jain rooms are parity rooms; your 22-wall room isn't | Short proofs, Codex-reviewed; checked on all 932 parity-room events |
| No strictly simple parity room with two interior A points has 22 or fewer walls. With 24 to 26 walls there are 327 room and mark classes, all locally rigid | Claude's exhaustive enumeration, `parity-enum/`, with no window, plus exact certificates at `R = 12`. Not yet reviewed by Codex |
| Every *folded parity room* has at least 22 walls. Such a room is mirror-glued copies of a parity base, with marks allowed on the base boundary, diagonal walls, and cycles of copies. Your 22-wall room attains this, and every 22-wall minimizer is 3 copies of a 10-wall base. Folds of dark non-parity bases with 4 or fewer transparent points also give nothing below 22 walls | Wall identity plus Codex's four-lemma short proof (`folded-review/short-proof.md`). Both agents reviewed it, and two independent fold enumerations agree. The non-parity extension is Claude-only (`folded/`) |

## The plan for the general case

1. Fix a shape with at most 21 walls.
2. Show that dark rooms of that shape are isolated. So far this is shown only for the three known rooms, one room at a time.
3. Show that dark rooms can't degenerate. Induct on the cost `W + 2B`.
4. Then each shape has finitely many dark rooms, with some largest number of transparent points. That number isn't known to be 4, so a final check would still be needed.

## Degenerations

| Case | Status |
| --- | --- |
| Marks merge in the interior, at a wall, or at a convex corner | Lit |
| A mark reaches a wall or a convex corner | Reduces to a dark boundary configuration of the same shape |
| A mark reaches a reflex corner | Rational limits: reduces to a finite exceptional set (Codex's Theorem 24). Real limits: reduces to Conjecture 24 |
| A collapse of two or more edges, or a collapse to a proper corner, that leaves a simple boundary | Reduces to a smaller cost |
| An isolated smooth step | Open in general. Codex's criterion excludes it near any fixed limit that passes a rank test and an interval certificate. In orthogonal rooms, the single-visit premise is now automatic. No six-wall L limit can have one: Codex's elementary monotone-path proof, checked by Claude, covers every L with any real dimensions |
| A thin slit | Reduces to dark slit rooms with `W - 1` walls |
| A mark in a thin dead-end corridor | Lit in a height range; open beyond it |
| A pinch with no straight path through it | Open (Conjecture 13) |
| A corridor that joins two parts | Open; it reduces to a periodic condition in the corridor width |
| A pinch that doesn't separate | Reduces to dark rooms with one point contact; open |

## Open questions

- **Isolation of every dark room.** Each known room is isolated, but there's no general argument yet. Lemma 27 writes each event as a taut string around a corner. Isolation then asks whether the classes `η_e` positively span. Straight-through events, cancelling pairs, and natural weights all fail to give it. The missing piece is a sign theorem: every nonsymmetric variation violates some event.
- **Smooth steps.** This is the only point collapse that keeps the cost the same.
- **Prescribed-target density.** Conjectures 13 and 24, and the joining corridor, all ask whether paths from a given place reach a given point in given directions, or uniformly as the room changes. Known density theorems pick the corner for you. That's why the draft question to Monteil asks about this (`monteil-followup-draft.txt`).
- **Dark rooms with one point contact and at most 21 walls.** Wolecki's 22-wall room is the smallest known.
- **Real rooms versus lattice rooms.** The induction needs claims about rooms with real-valued coordinates. The bounded theorem covers only lattice rooms with at most 4 transparent points.

## Not claimed

- No global lower bound of 22.
- No priority. The Monteil and Tokarsky replies are pending, and the 34-wall reconstruction isn't confirmed as Tokarsky's original room.
- Nothing about polygons outside the 45° family.
