# Round 3: make the (1,3,4) pi/8 minimum a finite problem and list profiles

Same rules: read-only, no searches, under 1,200 words, PROVED / CITED /
GUESSED. Your round-2 charge table is in `d32-fold-minimum/astra-r2.md`;
the enumeration results are in `d33-134-rooms/README.md` (no dark room at
W <= 21 with <= 8 extra tiles; Astra's 17-wall 40-tile room is lit).

Coordinator's finiteness observation (check it): every triangle has one B
vertex; a B point with k triangles has angle 3k pi/8, never pi or 2 pi,
so every B point is a room corner, 1 <= k <= 5. Hence F = sum over B
corners of k_B <= 5 W, and the turning identity
  sum_B (8 - 3 k_B) + sum_{A corners} (8 - k_A) + sum_C c = 16
gives F = (8 b - 16 + sum_A (8 - k_A) + sum_C c) / 3 with b = number of B
corners. So for W <= 21 the tile count is bounded (roughly F <= 55).

Tasks:
1. Confirm or correct the finiteness argument and give the exact maximum
   F for each W in 17..21, using also: A incidences (interior A = 16,
   flat A = 8, A corners k != 8, 16), F = sum over A points of k_A,
   C corners (k = 1 convex, k = 3 reflex), the two interior A stars of
   the pair (32 triangles, 16 distinct B corners, no shared C-tip and no
   shared edge, as you proved).
2. List every corner profile (b, the multiset of k_B, A corners with k_A,
   C corners, number of interior and flat A points, F) compatible with a
   dark pair for W = 18, 19, 20, 21. Prune with every necessary condition
   you can prove (for example the star structure, the mandatory 16 B
   corners, integrality of F, constraints from fans around B corners).
   Give counts per W and the profiles themselves if there are few.
3. Suggest the most efficient search organization: build rooms by
   attaching tiles to the two disjoint stars, prune by profile, and what
   invariant to track so the search provably covers every room with
   W <= 21. Estimate the number of rooms.

End with the feasibility verdict: can a computer search close W >= 22 for
this triangle, and roughly how large is it?
