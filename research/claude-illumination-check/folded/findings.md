# Folded parity rooms (broader class, first pass)

Claude, 2026-11-01. Approved by Daniel ("start on the broader class").

## Class
- A **parity base** is a simple polygon P in the canonical 45-degree tiling with walls on parity-preserving lines.
  - Its marks a != b are non-corner lattice points of class a + 2Z^2. Every other non-corner lattice point of P is in a + 2Z^2.
  - Marks may sit on the boundary or in the interior.
- A **folded parity room** is a strictly simple room Q made of m congruent copies g_i P with disjoint interiors.
  - Any two copies that share a boundary segment are mirror images across it, so the fold f: Q -> P is well defined.
  - Its marks S, T are interior points with f(S) = a and f(T) = b.
- The class contains every parity room (m = 1) and Codex's tree-of-copies class (Corollary in `research-note.tex`).
  - It also allows diagonal walls, cycles of copies, shared seam endpoints, and 3- or 4-copy points.
- **Darkness (needs Codex audit).** Let a lift point have k copies around a base corner of angle theta.
  - A lift is transparent when k*theta is pi (smooth) or 2*pi (interior).
  - Transparent lifts need theta in {45, 90} degrees with k even.
  - For even k, the folded continuation is velocity reversal, so Lemma retrace applies.
  - Concave and 135-degree base corners never lift to transparent points.

## Wall identity (needs Codex audit)
Let c = W_P, the corner count of P. Let n_s and n_i count smooth and interior lift points of 45-degree corners. Let E be the seam incidences at lift points that stay corners. Then

  W_Q = m (W_P - 4) + 4 + E + 2 n_s + 4 n_i  >=  m (W_P - 4) + 4.

- **Sketch, part 1: turning.** Sum (pi - k*theta) over all lift points. Smooth transparent lifts give 0 and interior ones give -pi. This gives L = m c - 2(m-1) - n_int and W_Q = m c - 2(m-1) - n_smooth - 2 n_int.
- **Sketch, part 2: Euler.** Euler on the copy decomposition of the disk gives seams sigma = m - 1 + n_int. Counting seam endpoints, 2 sigma = sum over points of s(p), with s = k-1 on the boundary and k in the interior. Eliminating n_smooth gives the identity.
- **Check.** The 22-wall room has m = 3, W_P = 10, E = 0, so W_Q = 22. In the orthogonal case, E = 2 n3, matching 2mr + 4 + 2n3.

## Enumeration
- **Bases.** `parity-enum/enum_base.c` is `enum2.c` with marks allowed on smooth boundary A points.
  - W_P <= 8: none.
  - W_P = 9: 8 listings, all diagonal-wall bases.
  - W_P = 10: 52; W_P = 11: 128; W_P = 12: 224.
- **Allowed copy counts.** Since W_P >= 9, W_Q <= 21 forces m <= 3.
  - m = 3 needs W_P = 9.
  - m = 2 needs W_P <= 12.
  - m = 1 is a parity room, and those need W >= 24.
- **Folds.** `folded.py` grows copies by wall reflections, then checks the following exactly on quarter-triangles:
  - disjoint interiors;
  - one strictly simple boundary cycle;
  - mirror consistency on every shared edge;
  - interior lifts of two distinct marks.
- **Result.** For all 412 bases with W_P <= 12, no folded parity room has W_Q <= 21: `hits.txt` is empty.
- **Validation.** With the threshold at 22, it finds exactly 12 hits, all m = 3 on 10-wall bases. These are the 22-wall room's listings (`hits22.txt`).

## Claim, conditional on the audits
Every folded parity room in the canonical 45-degree tiling has at least 22 walls. The bound is attained by Peyton's room.

## Not covered
- Darkness mechanisms other than parity folding.
- Folds onto non-parity bases.
- Rooms off the canonical tiling.

## Widening: folds onto dark non-parity bases (second pass)
The fold argument needs only a dark base, not a parity base. Lemma retrace holds for any room, and the wall identity doesn't depend on the darkness mechanism.
- **Bases.** `parity-enum/enum_t.c` allows up to K = 4 transparent B/C points, smooth or interior.
  - With K = 0 it reproduces `bases-W12.txt` exactly.
  - Raw listings with W_P <= 12: 6,480 (K=1), 51,760 (K=2), 285,546 (K=3), 1,190,825 (K=4).
- **Darkness filter.** `basetrace.c` searches every non-corner A pair for a lit path, over primitive directions up to 10 and 400 bounces.
  - All 412 parity bases pass, consistent with Lemma 25.
  - With k = 1–4 transparent points, 1,902 bases keep a pair with no lit path found. All have W_P >= 10.
- **Small bases are lit, exactly.** Every base with W_P <= 9 and k <= 4 has a lit path for every pair. `verify_lit.py` confirmed all 68,898 verdicts in exact arithmetic. So the wall identity forces m <= 2.
- **Folds.** `folded.py` on the 1,902 candidate bases finds 40 two-copy rooms with W_Q in {20, 21}.
  - In every one, the interiorized pair is lit in the base by an exact path. None is backed by a dark base pair.
  - Example: the base with the transparent mark pair (-2,4), (0,4) has a lit path in direction (-7,-4).
- **Lit exclusions for W_P = 10–12.** These started as float verdicts. A pair is fold-relevant when each mark is interior or on a wall with two convex endpoints.
  - All 504,842 fold-relevant verdicts are now confirmed in exact arithmetic (`verify_lit.py`, `recheck.py`).
  - 504,822 confirm in the float direction.
  - The other 20 failed in that direction but have exact lit paths in other directions; see `recheck.txt`.

## Claim, conditional on the audits
- No room with W <= 21 folds onto a dark base with k_P <= 4 transparent points, for m >= 2.
- The same holds onto a parity base, with no k limit.

## Not covered
- Bases with 5 or more transparent points.
- Dark bases whose darkness only shows past direction radius 10. They would be wrongly kept, which is the safe direction. The exclusion side is exact.

## Codex review and short proof (accepted by Claude)
- `illumination-k4-codex/folded-review/findings.md`:
  - It accepts darkness, with three hypotheses: a coherent fold, A = 2Z^2 preserved, and the tangent case handled by parity.
  - It accepts the wall identity, derived independently.
  - It includes an independent fold replay, `replay.py`: 2,096 assemblies, none below 22, and the 12 W22 listings form one shape.
- `short-proof.md` replaces the fold exhaustion with four lemmas. Claude checked each step:
  - **Lemma 1.** The 4(W-2) = 3N + E_A count and the fan argument give W_P >= 14 when one mark is interior. Each extra triangle has one mixed vertex, so the four requirements are distinct.
  - **Lemma 2.** An interiorized smooth mark needs exactly one mirror copy R_l(P), so l supports P.
  - **Lemma 3.** Euler gives one connected seam interval containing both marks. It then contains a smooth non-A lattice point, a contradiction.
  - **Lemma 4.** The 9-wall base's mark wall line y = 2 cuts [1,2]x[1,3], which lies inside P.
  - **Equality corollary.** It forces m = 3, W_P = 10, E = b45 = i45 = 0, a tree, and 4 distinct 90-degree endpoints.
  - **Universal two-copy corollary.** On the seam interval, intermediate boundary points have angle pi, so the joining segment is interior and the marks see each other.
- **Effect on the second pass.** The exclusion numbers stand; they only discard folds of bases that are lit. "Folds onto a dark base" isn't a darkness criterion, though: base darkness doesn't control paths that project along a base wall. The two-copy corollary is a case where this happens. A non-parity extension needs a mark interior in the base and a separate tangent argument.
