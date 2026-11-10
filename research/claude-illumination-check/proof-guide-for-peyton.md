# Proof guide: the 22-wall dark room

Written for Peyton Wang, 2026-10-31. This guide lists what is proved, what each proof depends on, and what is still open. It points to the file that holds each piece, so that you can check every step yourself.

## The result in one paragraph

Your 22-wall room is dark, and it is strictly simple. It's the smallest folded parity room in the 45° tiling, and folded parity rooms in the 30-60-90 tiling need at least 28 walls. No smaller dark room exists in a bounded class: rooms built from the canonical 45° tiling, with two interior marks at A points, and at most 4 transparent points. The general question, with any number of transparent points, is open.

## Definitions

- **Canonical 45° tiling.** The lines `x = c`, `y = c`, `x - y = 2c`, and `x + y = 2c`, for every integer `c`, cut the plane into right isosceles triangles. These triangles are the tiles.
- **Point classes.** An **A** point has both coordinates even. A **B** point has both coordinates odd. A **C** point has one even and one odd coordinate. Every tile has exactly one A, one B, and one C vertex.
- **Room.** A room is a union of tiles whose boundary is a single closed curve. It has no holes, slits, or points where the boundary touches itself. That's what "strictly simple" means.
- **Walls.** A wall is a maximal straight piece of the boundary, so `W` equals the number of corners.
- **Rays.** A light ray reflects off wall interiors and stops when it reaches a corner.
- **Dark pair.** Two points are a dark pair when no ray from one reaches the other.
- **Transparent point.** A B or C point that a ray can pass through. That is either an interior point or a boundary point where the boundary runs straight. Write `J` for interior ones and `s_N` for straight-boundary ones. Then `k = J + s_N`, and `E = 2J + s_N`.
- **Full cell.** An A point whose 8 surrounding tiles are all in the room. `I` counts them.

## Your room

| Quantity | Value |
| --- | --- |
| Walls `W` | 22 |
| Tiles `N` | 30 |
| Marks | `(0,0)` and `(2,2)` |
| Full A cells `I` | 2 (the two marks) |
| Interior transparent points `J` | 0 |
| Straight-boundary transparent points `s_N` | 4, at C points `(-1,0)`, `(1,0)`, `(2,1)`, and `(2,3)` |

Corners, in order: `(-1,-1), (-1,1), (0,1), (0,2), (1,2), (1,3), (3,3), (3,2), (4,2), (4,1), (5,1), (5,0), (3,0), (3,1), (1,1), (1,-1), (2,-1), (2,-3), (1,-3), (1,-2), (0,-2), (0,-1)`.

The room is three reflected copies of a 5-square staircase. Drawing: `k4/cand-2_2-1.png`. Data: `k4/cand-2_2-1.json`.

## The theorem

**Theorem.** Suppose that a room in the canonical 45° tiling is strictly simple and has two distinct interior A points that form a dark pair. Suppose also that it has at most 4 transparent points. Then it has at least 22 walls. Your room shows that 22 is reached.

## How the proof fits together

Read the parts in this order. Each later part uses the earlier ones.

| Step | Statement | Kind | Where |
| --- | --- | --- | --- |
| 1. Darkness of your room | No ray joins `(0,0)` and `(2,2)` | Hand proof, plus two independent computer certificates that agree | Codex `research-note.tex`; `k4/cand-2_2-1-orbit-certificate.json` |
| 2. Alternation (L1) | Unfold a ray into a straight line. It meets lattice points that alternate between A and one fixed class X, either B or C | Hand proof | `proof-plan.md`, section L1 |
| 3. Marks are full (L2) | An interior A point has all 8 tiles around it | Hand proof | Codex `proofs/placement-enumeration.md` |
| 4. Counting identities | `W = 2 + 6I + Q - E` and `N <= (4/3)(W - 2 + 2k)` | Hand proof (Euler's formula) | Codex `proofs/placement-enumeration.md` |
| 5. Few full cells (L4) | `Q >= 4 - s_N`, so `W >= 6 + 6I - 2k`. With `W <= 21` and `k <= 4`, that gives `I <= 3` | Hand proof | Codex `persisted-replay/findings.md` |
| 6. Finite cases (support lemma) | The other cells stay close to the full cells. That leaves 31 cases: 14 with two full cells and 17 with three | Hand proof, plus a short enumeration | Codex `bounded-proof/support-proof.md` |
| 7. Boolean encoding | Each case becomes a formula that every dark room in that case would satisfy | Hand proof that every clause is necessary | Codex `bounded-proof/encoding-proof.md` and `encode.py` |
| 8. No solutions | A SAT solver shows all 31 formulas are unsatisfiable, and `drat-trim` checks each proof | Computer, independently checkable | `drat-review/regen/`, `drat-review/regen-drat.txt` |

### Step 2 in plain words

Reflect the room across the wall each time the ray hits it. The ray then becomes a straight segment from `s` to a copy of `t`. Reflections in tiling lines keep A points as A points, and they keep B and C as classes. The segment's displacement is an even multiple of a primitive vector `(p, q)`. So the lattice points on it are `s + j(p, q)`, and they alternate between A and X. For darkness, each ray toward a copy of `t` must hit a corner first.

### Step 6 in plain words

Build a graph whose vertices are the A cells that hold tiles. Join two cells when their tiles share an edge. The room is connected, so this graph is connected. A partial cell costs at least as many walls as it has neighbors. Each missing neighbor of a full cell forces a straight-boundary C point. Together these facts give:

    2(P + m) <= W - 4I + 2k

Here `P` counts partial cells and `m` counts missing neighbors of full cells. That bound keeps every cell within a short distance of the full cells, so each case is finite.

### Step 7 in plain words

Each tile gets a true/false variable. The formula states facts that every eligible dark room satisfies:

- Each boundary point has exactly one wedge of tiles (strict simplicity).
- The full A cells are exactly the ones in the case.
- At most 36 tiles, at most 21 walls, and at most 4 transparent points.
- The corner angles add up the way they must for a closed curve.
- The tiles are connected.
- No saved lighting certificate applies. Each certificate is a set of tiles that must be present and a set that must be absent. Whenever both hold, a ray joins the marks.

The proof needs only one direction: a dark room would make the formula true. So if no assignment makes it true, no such room exists.

## The trust base

The theorem is as reliable as these pieces:

1. The hand proofs in steps 1 to 7. Claude and Codex each reviewed the other's work. No human mathematician has checked them yet.
2. The local fan table in `illumination_geometry.py`. It decides which wedges of tiles around a point are legal, and Codex checked all 528 cases.
3. `encode.py`, which turns step 7 into clauses. Claude read it clause by clause against `encoding-proof.md`.
4. The 47,576 lighting certificates. Codex replayed each one exactly and found every one valid.
5. `drat-trim`, a standard proof checker. Claude built it from the upstream source, and its SHA-256 matches Codex's copy.

To find a weak spot, start with items 1 and 2. They are the parts a computer did not check.

## Rerun the computer part

From `.context/claude-illumination-check/drat-review/`:

    PY=../../illumination-k4-codex/bounded-proof/venv/bin/python
    cat tags.txt | xargs -P 6 -n 1 $PY -B regen_solve.py
    cat tags.txt | xargs -P 6 -n 1 ./regen_check_drat.sh

The first command builds and solves all 31 formulas. Each takes under 20 seconds. The second command checks every proof. Expect `UNSAT` 31 times, then `s VERIFIED` 31 times.

## What is not proved

- **More than 4 transparent points.** This case is open. Scaling a room up by an integer keeps it dark and keeps its wall count, but multiplies its transparent points. So a cap on transparent points can't settle it alone. See "The general case: progress since the theorem".
- **Rooms outside the tiling.** The theorem says nothing about polygons with other angles or with corners off the lattice.

## The general case: progress since the theorem

This section is new as of 2026-11-01. It covers the attack on rooms with more than 4 transparent points. All of it is in `l3-analysis.md`, and Codex has reviewed each part.

### The plan

Scaling a room up keeps its shape and its darkness, so count shapes, not rooms. Fix a shape with at most 21 walls. Its rooms form a region of real parameters: edge lengths and mark positions. The plan has two parts:
1. **Dark rooms are isolated.** Near any dark room, every other room of that shape is lit, except scaled copies. A room with only horizontal and vertical walls can also be stretched along each axis.
2. **Dark rooms stay away from the edge of the region.** No sequence of dark rooms can degenerate, for example by shrinking a wall to a point.

Together, these would leave finitely many dark rooms of each shape. Each would have some largest number of transparent points. That number isn't known to be 4, so a final check would still be needed.

### Part 1: local rigidity

A computer test proves part 1 for one room at a time. It finds light paths that graze a reflex corner. Moving the room slightly in any direction pushes at least one of them off the corner on the open side, and that lights the room. The test is exact, and a computer checks it in about 10 seconds.

| Room | Walls | Result | Checked by |
| --- | --- | --- | --- |
| Your room | 22 | Rigid | Claude and Codex, separately |
| The 24-wall room with diagonal walls | 24 | Rigid | Claude; Codex checked the algebra |
| Tokarsky's room, from O'Rourke's figure | 34 | Rigid | Claude and Codex, each replaying the other's certificate |
| Wolecki's room, where two corners touch at one point | 22 | Rigid. Every simple room made by pulling the two corners apart is lit | Claude; Codex replayed it |
| Bhavya Jain's "Spider's home", center to a wall midpoint | 28 | Dark and rigid. The shape is read off a video thumbnail | Codex; Claude replayed it |

That's evidence for part 1, not a proof. A proof must cover every dark room, including ones not found yet.

### Part 2: degenerations

Each way a room can degenerate needs its own argument. Some are settled:
- Two marks can't merge inside the room, at a wall, or at a convex corner. The straight segment between them lights the room.
- A pinch where you can see straight through the gap lights the room.

Others reduce to a smaller question:
- A wall that shrinks to a corner leaves a dark room with fewer walls. That suggests an induction on the number of walls.
- A mark that moves onto a wall or a convex corner gives a dark room with a mark on its boundary.
- A thin slit leaves a dark room with a zero-width wall.

- A mark moving into a reflex corner, in a room with rational coordinates. Codex proved that light leaves the corner in a dense set of directions. That leaves finitely many exceptional cases.
- A group of short walls collapsing together. Codex found a cost, walls plus twice the extra blockers, that never goes up in such a collapse. It goes down in every case but one, a single small step in a wall.

Still open:
- that single small step;
- a mark moving into a reflex corner, when the coordinates aren't rational;
- a pinch where you can't see straight through the gap;
- a thin corridor that joins two parts of the room;
- rooms with one point where the boundary touches itself.

### Toward a proof of part 1 for every room

Four of the dark rooms share a pattern, which Claude called *parity rooms*. Color the lattice points by the parity of their coordinates, measured from a mark. In a parity room, every point with an odd coordinate is a corner. That alone makes the room dark, by the argument from step 2. Jain's room, the 24-wall room, the 34-wall room, and Wolecki's room are parity rooms.

**Your room is not a parity room.** Four of its odd points, `(-1,0)`, `(1,0)`, `(2,1)`, and `(2,3)`, sit inside walls instead of at corners. Its darkness uses mirror images and paths that bounce straight back. So your room works by a different mechanism, which makes it more unusual.

In a parity room, every grazing path has the same shape. Unfold it, and the corner sits exactly halfway between the marks. Each grazing path then acts like a string pulled tight around a peg. The room stays dark only if every string stays tight when you move the walls. A general proof of part 1 would show that some string always goes slack, for any move other than scaling. That's the missing step. Three simple ideas for it were tested and failed; see "Toward isolation of every dark room" in `l3-analysis.md`.

### Where to look for a weak spot

Start with the lemmas in `l3-analysis.md` from Lemma 15 on, in the sections "Other degenerations", "Clusters of collapsing edges", and "Toward isolation of every dark room". These are the newest and least tested. Codex has already found and fixed several mistakes in them. The rigidity certificates are on firmer ground, because two independent programs agree on each one.

## Results from 2026-11-01

This section covers the work after the general-case plan in the preceding section. Each result names its status.
- **Both agents** means Claude and Codex each checked it.
- **Claude only** means Codex hasn't reviewed it yet.

### Your room is optimal in a larger class: folded rooms

Your room is three mirror copies of a 10-wall staircase, glued along two seams. Call any room built this way a *folded room*.
- **Construction.** Take a parity base `P` and glue `m` mirror copies of it. Every seam must reflect one copy onto the next.
- **Marks.** The marks sit over two A points of `P`, and they can lie on the boundary of `P`. Diagonal walls and cycles of copies are allowed.

**Theorem (both agents).** Every folded parity room has at least 22 walls.

The proof has three parts:
- **Wall count.** It counts walls exactly: `W = m(W_P − 4) + 4 + E + 2b45 + 4i45`. Every extra term is zero or positive.
- **One or two copies.** One copy is a parity room, which needs more than 22 walls. Two copies need at least 24 walls. With fewer, the marks end up on one seam and see each other along it.
- **Three copies.** These need a base with at least 10 walls. The only 9-wall base can't be folded the right way, because its mark sits on a wall whose mirror line cuts through the room.

**Equality (both agents).** A 22-wall folded room is three copies of a 10-wall base, joined in a chain. Your room is that case, and two separate computer enumerations find no other shape.

**Non-parity bases (Claude only).** Bases that aren't parity rooms, with up to 4 transparent points, also give no folded room under 22 walls. A useful side fact came out of this check: "the base is dark" doesn't imply "the folded room is dark".

### The same idea in the 30-60-90 tiling

Wolecki's Lemma 3.1 also makes parity rooms dark in the tiling by 30-60-90 triangles. A web search found no one who has looked for small rooms there.

**Theorem (both agents).** In that tiling, every folded parity room has at least 28 walls. The class excludes copies that meet transparently at a 60° corner, since the darkness proof fails there. So this folded class can't beat 22.
- Codex found one gap: a 120° corner covered by 3 copies. It's excluded because each seam flips orientation, so the copies around a point must come in an even number.
- Codex independently reran the search over local tile patterns. It got the same 416 end states and the same wall-count histogram as Claude.

### Two steps toward removing smooth-step blockers

One open degeneration is a single smooth boundary point that blocks every path between the marks.
- **L-shaped rooms (Codex, checked by Claude).** In any six-wall L room, any two interior points connect by a path that bounces only off vertical walls. They also connect by one that bounces only off horizontal walls. One boundary point can't block both paths, so it's never the only blocker.
- **Symmetric U rooms (Codex, checked by Claude).** In an eight-wall U room with mirror-image marks, three explicit paths share no boundary point. So no single point blocks every path.
  - The same holds for every room close enough to a symmetric one.
  - Claude checked the proof by hand and with exact simulation on 4,000 random rooms. It also tested 1,800 slightly lopsided rooms.

### An exact darkness test for lattice rooms (Claude only)

`reduction/origami_dark.py` decides whether a lattice room is dark, with no limit on how far it looks.
- **How it works.** It unfolds the room into a surface made of unit squares. It then follows how that surface changes under the shears of the integer lattice.
- **Check against exact tracing.** On 360 rooms, every "lit" answer came with an exact light path. The test never called a known dark room lit.
- **Limit.** For most rooms with 24 or more walls, the search space has millions of states, so the test can't finish. It's practical for lit answers and for small rooms such as yours, which needs 10,368 states.

### What the general case now hinges on (Claude only)

- **Wall count against squares.** A natural idea is that a fine lattice room, with many squares per wall, must be lit. That's false. Scaling a dark room up keeps it dark and multiplies its squares.
- **The real open step.** Showing that each dark room is isolated needs the "sign theorem" from the preceding section: every move of the walls loosens some taut string.
- **The narrowed target.** Take all 327 parity rooms with 24 to 26 walls. In each one, the strings at a few corners next to the marks already prove isolation.
  - Strings at the 4 corners directly beside each mark work in 293 rooms.
  - Adding one diagonal neighbor works in all 327.
  - These corners look the same in every parity room, which makes them a good place to start a proof.
- **An idea that failed.** The motion of each corner alone doesn't explain the result. The interaction with other walls along each string does the work.

## Problems you could try

These are open, and each is about the right size for a first attack.
1. **Prove the narrowed sign theorem for one family.** For example, take parity rooms whose marks are in mirror position. The data is in `parity-enum/certs/`, and `parity-enum/analysis/ringsub.py` shows which strings work.
2. **Asymmetric U rooms.** Extend Codex's three-path argument to U rooms whose arms have different widths or heights (`illumination-k4-codex/two-reflex-blocker/u-portal.md`).
3. **Rooms built from π/8 triangles.** The literature check found no minimum-wall search in this tiling. As a first step, find which corners can be transparent.
4. **Why your room's test is small.** Your room needs 10,368 states in the exact test, but parity rooms of similar size need millions. Explain the difference; the three-copy structure is the likely cause.

## Mistakes found and fixed along the way

These are worth knowing, because they show where the argument is fragile:

- An early plan tried to cap the number of transparent points outright. Scaling defeats that, so the plan changed.
- An early search ran without saving its lighting certificates. It was rerun with saving turned on, so that every certificate could be replayed.
- 29 of Codex's 31 saved formulas came from older encoder versions that were never kept, so nobody could audit them. Claude regenerated all 31 from the reviewed encoder and checked the new proofs.
- Claude first claimed that every known dark room is a parity room. Codex checked your room and showed it isn't.
- In the general case, Codex refuted several claims by exact counterexample. Examples: an early form of the degenerate-limit conjecture, the pinch test using approximate weights, and a corner lemma measured from the wrong point. Each claim was narrowed or fixed.
- Claude first wrote that a folded room is dark whenever its base is dark. Codex showed that two copies glued along a seam can let the marks see each other directly, even when the base is dark.
- Claude's 30-60-90 case list missed a 120° corner. Codex caught it, and the orientation argument closes it.
- Claude's first U-room simulator reported false corner hits. The bug was in the simulator, not the theorem, and the counts were rerun after the fix.
- Claude proposed counting squares to bound transparent points. Scaling refutes it in one line.
