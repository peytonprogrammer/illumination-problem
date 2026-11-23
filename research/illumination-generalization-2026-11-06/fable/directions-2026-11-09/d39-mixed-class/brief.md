# d39 brief: repaired visibility-to-certificate, mixing direction classes

Daniel approved one round, budget about 100k tokens. Theory only: no room,
ray, direction, or reflection-word discovery searches. Read-only checks on
three named rooms only: the 22-wall room, P6, and the 12-wall cross
(cap: under 5 CPU minutes total, one process at a time).

## What changed

An independent referee reviewed d35-d37: `d38-review/review.md`. Read it
first. Summary of its verdicts:
- d35 correct. d36 correct, but the 5r bound needs corners in >= 3 parity
  classes; even refinements (used by d16) put all corners in one class.
- d37 joint-majority hypothesis is FALSE at r = 4. With the trivial
  subgroup it says every pair in one phi_x fibre is x-lit. The 12-wall
  cross, S = (1,2), T = (3,2), has B_c one block, yet all four lift pairs
  carry Cut certificates at c (`d10-d12-review/room_r4.log`) and are
  c-dark. The room is lit through another class.
- The lift-graph and averaging lemmas hold, with a fixable gap for
  wall-point marks.

Cut and Rig are defined in `d10-mechanisms/theory.md` (section 2.4 and
around); Theorem U is confirmed in `d10-d12-review/`.

## Task

State and attack the repaired target, which must mix classes:

For an orthogonal lattice room with r <= 8 and interior marks S, T: if
for some class x the pair is x-lit, the pair is lit (trivial). The real
content: if in EVERY class x the pair is x-dark, then the darkness in each
class is explained by a certificate (separating B_x, Cut, or Rig at x),
AND those per-class certificates together force a separating parity
factor (common or per-class), which d2-review and the k <= 6 theorem
exclude at r <= 8 for the common case.

Questions, in order:
1. Per class: is "x-dark implies a certificate at x (B_x separation, Cut,
   or Rig)" true, false, or open? If false, give a counterexample or name
   the missing mechanism. Use the d37 lift graph and fibre lemma.
2. Across classes: in the cross, class c is explained by Cut while the
   room is lit through b or d. Characterize when three per-class
   certificates of mixed type (e.g. Cut at c, B-separation at b and d)
   can coexist at r <= 8. Can a reflex-corner count or the d36 bound
   (within its correct scope) rule out mixed triples?
3. Check every claim against the three named rooms: the cross must come
   out lit, the 22-wall room and P6 dark with their staircase
   certificates.
4. Updated probability for the whole programme and the single next step.

Tag every claim PROVED / CITED / GUESSED. Prefer a correct narrow result
to a broad conditional one; avoid hypotheses that restate the target.
State: `STATE.md`. Your earlier replies: d35, d36, d37 (`*/astra.md`).
Write to the -o file.
