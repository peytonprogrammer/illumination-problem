# d47 brief: close the scope gaps of the certificate-side theorem

Budget about 100k tokens, theory only. No room, ray, direction or
reflection-word searches or enumerations. Read-only checks on named rooms
only (22-wall room, P6, 12-wall cross and their scalings): under 5 CPU
minutes, one process. Put your full answer in your final message.

Directory D = .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09

## Established (read these first)
- D/d43-review-d39/review.md: the exact statement and its scope gaps.
- D/d46-cert-check/README.md: the finite check, now complete with 0
  positives (13.3e9 rooms, 52.7e9 pairs at W = 20; 471M rooms at W <= 18).
- D/d45-review-fstar/review.md, D/d38-review/review.md,
  D/d36-amalgamation/astra.md, D/d39-mixed-class/astra.md,
  D/d2-review/review.md for the ingredients.

Theorem so far (computer-assisted): a strictly simple orthogonal lattice
room with W <= 20 (r <= 8) and corners in at least 3 parity classes has no
pair of same-class interior lattice marks certified dark by Par, Cut or
Rig certificates over the unit pillowcase B.

## Task: scope and, where possible, close the three gaps
1. Coarser pillowcases. A room dilated by an odd factor (example: the
   22-wall room scaled by 3) is dark with no certificate over B, only
   over a coarser pillowcase. d43 says rectangular coarser pillowcases
   reduce to the coarser presentation and non-rectangular ones need new
   work. Define precisely the class of "relative certificates" (which
   pillowcases D([0,a]x[0,b]) can a lattice room cover compatibly?).
   Prove the reduction for the rectangular case in full, including
   a != b (anisotropic rescaling: axis scalings preserve darkness, see
   D/d40-thick-thin/astra.md). Decide whether non-rectangular bases can
   occur for orthogonal rooms at all; if they can, say what check or
   argument covers them.
2. Rooms whose corners occupy at most 2 parity classes (for example even
   refinements; the cross scaled by 2). The n <= 5r bound and the z = 0
   step fail there. Either reduce such a room to a normalized
   presentation where the theorem applies (does gcd normalization on each
   axis always give >= 3 corner classes? d36 claims so: check that every
   room with <= 2 corner classes is non-normalized or otherwise covered),
   or state the residual case exactly.
3. Marks. Same-class interior lattice marks are covered. Handle
   (a) different-class lattice marks, and (b) rational non-lattice marks,
   which need a lattice refinement (D/d16-real-to-rational/, D/d16-review/).
   After refinement the room is non-normalized, so this interacts with
   gaps 1 and 2. Give the cleanest statement: for which (room, pair) does
   "certified dark" make sense, and does the theorem extend to all of
   them?

## Deliverable
A single clean theorem statement with every hypothesis explicit, a proof
or proof sketch for each reduction, and a list of what (if anything)
still needs a finite check or new argument, with its size. Tag claims
PROVED / CITED / GUESSED. Prefer a correct narrow statement to a broad
conditional one. Test every reduction on: the 22-wall room and its
scalings by 2 and 3 (must stay certified dark, r = 9), the cross and its
scalings (must stay uncertified).
