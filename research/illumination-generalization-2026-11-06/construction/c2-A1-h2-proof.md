# A45: actual four-reflection closure of the entire h=2 A1 row

Status: author proof, pending independent acceptance. Original effort deadline2026-11-07T06:32:29.695294Z. Discovery stopped at its first actual witness after18 prescribed primitive directions. No remaining finite-prefix computation is needed.

For every even d>=2, let the core be[0,2] x [0,d+8], right teeth[2,3] x [1,3] and[2,3] x [5,7], and left teeth[-1,0] x [2,4] and[-1,0] x [d+4,d+6]. The actual marks S=(2,2) and T=(2,6) are interior. Use this exact path:

(2,2) -> (-1,3) -> (2,4) -> (0,14/3) -> (3,17/3) -> (2,6).

Initial velocity(-3,1) changes horizontal sign at each of the four turns; vertical velocity remains1. All five legs have absolute slope1/3. Therefore the stated collisions obey the actual specular law.

The first leg crosses x=0 at y=8/3, strictly in the first left mouth(2,4), then reaches its far vertical wall at(-1,3), strictly between its two corners. The next leg crosses that mouth again at y=10/3, then stays in the core until(2,4), a smooth right side-wall point between right mouths[1,3] and[5,7]. The next turn(0,14/3) lies strictly above4 and strictly below d+4, since d+4>=6>14/3. It is thus a smooth point of the actual left core wall, for EVERY allowed d, including d=2. The fourth leg crosses x=2 at y=16/3, strictly in the upper right mouth(5,7), then hits its far wall at(3,17/3), strictly between its two corners. The last leg lies in that tooth and ends at the actual interior T=(2,6).

All heights increase strictly from2 to6. Neither floor nor ceiling is reached; the second left opening is never entered. At d=2 its lower endpoint has y6, but the only point of the path at y6 is T at x2, not that corner at x0. No open segment passes through any corner. None reaches T earlier, by strict height monotonicity. All selected far-wall points are actual polygon walls, with no seam reflection or regular-corner continuation.

The discovery check used a finite lower cap with an artificial rejection roof at100. Its stored four-reflection path never used that roof, and its maximum height6 is explicit. The proof here directly checks the actual full room for every d, so no inference from a truncated room's illumination is needed. The saved path has80 all-wall leg guards in that16-wall auxiliary cap; it is not claimed those are the full20-wall family's guards. The hand argument supplies the full family's actual missing-tooth guards above. An independent reviewer should verify the displayed path directly in the20-wall A1 room.

Together with A44's frozen all-even-h>=4 variable-angle proof, this covers the ENTIRE two-parameter A1 family h_even>=2,d_even>=2, conditional on explicit independent acceptance of both packets. A42's accepted necessary classification still requires the separate B,C1,C2 and A0 optical closures. The universal canonical45 W<=21 goal remains open.
