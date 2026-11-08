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
