# Proof plan: is 22 walls minimal for strictly simple dark rooms?

Status: draft, 2026-10-31. Owner of the investigation: Peyton Wang. Claude and Codex draft and check.

## Target theorem

Every strictly simple polygon from the canonical 45-degree tiling that has two mutually dark interior A points has at least 22 walls.

The general question (any strictly simple polygon, any angles) stays out of scope.

## What a proof needs

A proof has two kinds of parts. Each part is either written by hand, or is a finite computation whose output an independent checker can verify.

| Part | Current status | What counts as proof |
|---|---|---|
| L1. Alternation: a connecting path meets A, X, A, X, ... where X is always B or always C | Proved (below) | Written proof |
| L2. Marks have full stars | Used throughout; written argument exists in Codex notes | Written proof, reviewed |
| L3. Darkness obstruction for k >= 5 exceptions (see below) | **Open. Main gap.** An absolute exception bound is impossible: dilating a dark room keeps W and darkness but multiplies exceptions (Codex) | Written proof |
| L4. I <= 3 when k <= 4 and W <= 21 | Proved: Q >= 4 - s_N gives W >= 6 + 6I - 2k (Codex, `persisted-replay/findings.md`) | Done |
| L5. Placement bound: intermediate connector triangles <= N - 16 (dual-edge distance <= N - 15) | Proof sketch by Codex; script correct | Codex writing |
| L6. Enumeration rules (corner types, local tables, simplicity) | Codex listed 7 obligations; static review passes | Codex writing |
| C1. k = 0..3 exclusions | Solver claims, no checkable proof for parts | Re-run as SAT with DRAT proofs and check with drat-trim, or replace with enumeration plus certificates |
| C2. k = 4 exclusion | Done: Codex replayed all 47,576 certificates exactly, valid in every completion (`illumination-k4-codex/persisted-replay/findings.md`) | Done |
| C3. Darkness of the 22-wall room | Two independent closed-orbit certificates agree | Done, given L1 and the unfolding lemmas |

## L1. Alternation lemma (proved)

Reflection in any tiling line (x = c, y = c, x - y = 2c, x + y = 2c) preserves the three classes A (even-even), B (odd-odd) and C (mixed). A diagonal reflection swaps the two C residues, so C is preserved only as a merged class. So unfold a billiard path from s to t into a straight segment from s to a lift of t. Both are A points, so the segment's displacement is k(p, q) with (p, q) primitive. Since (p, q) is not even-even, k is even. The segment meets integer points exactly at s + j(p, q). These alternate between A (j even) and one fixed class X (j odd): B when p and q are both odd, C otherwise. Each odd point folds to a B or C point of the room that the path passes through, so it must be an exception.

Consequence: with no exceptions, every room with interior A marks and corner B/C points is dark (Tokarsky's criterion). Each exception is a point the path must pass through on every other step.

## Net-charge identity (proved, checked on 301 rooms)

Give each tile weight w = 1/2 if its C vertex is an exception, plus 1/4 if its B vertex is. Each exception's weight 2J + s_N splits exactly over its tiles. For each A cell, let net = cost - (sum of w over its tiles), with cost 6 (full), 3 (smooth boundary A), m (other cell with m tiles) or 0 (empty). Then

    W = 2 + sum over A cells of net.

Each tile has w <= 3/4, so net >= 0 for every cell, and net >= m/4 for nonsmooth partial cells. Checker: `proofs/net_charge_check.py`. The 22-wall room has net 4 at each mark cell and 12 elsewhere. This localizes the wall budget; it does not by itself bound the room, because full and smooth-boundary cells can have net 0 ("bulk"), as dilation shows.

## L3: approaches to try

1. **Local lighting lemmas.** Show that an exception within small lattice distance of a mark, in a fixed local configuration, forces a connecting path. Enough of these would cap 2J + s_N.
2. **Unfolding count.** Use W = 2 + sum over Fix(rho) of m/4 (refolding report) and the lattice-surface structure. Lelievre, Monteil and Weiss classify non-illuminating pairs on torus covers; their midpoint construction may bound the transparent lifts a dark pair allows.
3. **Size bound.** A strictly simple room with W walls fits in a box of side W (Codex, for the no-exception class). Check whether this extends to rooms with exceptions. It would give finite but large K0 and I0, which only work with a much faster checker.

## Division of work (proposed)

- Claude: draft L3 and L4 with approach 1, then approach 2.
- Codex: adversarial review of each draft; write L5 and L6 proofs; replay C2 certificates.
- C1: re-encode as SAT with proof logging, after L3 and L4 fix the scope.
- Peyton: review each lemma and own the write-up.
