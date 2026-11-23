# Round 2: pushback, one reformulation, and two things to settle

Same rules: read-only, no searches, no file edits, under 900 words, mark
each claim proved, cited, or guessed. Do real mathematics this round:
attempt the lemmas, don't re-describe them.

## Pushback on round 1

- Your correction on d16 is right; the one-parameter question is a side
  issue for the lattice target.
- B: partly disagree. Twists of *maximal* cylinders (height h > 1) move
  lattice points inside the cylinder, and an earlier step used exactly
  that to kill most pairs (`d13-cylinder-cover/theory.md`). What is dead is
  the expansion claim: it is the orbit classification again.
- A: your multi-winding version is the route that already stalled. A
  complete r = 3 theorem leaves r = 4 to 8, where the count of position
  types grows from 13,608 to 564,629 and beyond. Unless the U-chain
  analysis yields a statement uniform in r, it doesn't reach the target.
- I: "at least nine independent contributions" has no mechanism yet. The
  known dark room has r = 9, so the claim is the conjecture restated
  unless the rank enters an actual inequality.

## Reformulation that might give your idea I something to bite on

Lattice room, S and T lattice points of the corner class A = (0,0) mod 2.
An unfolded segment with primitive displacement meets no lattice point
between its ends, so it is never blocked: every non-vertex lattice point
X and primitive direction d give a well-defined endpoint E_X(d), a
lattice point of the room. A displacement from S to an image of T is
(even, even), so every path from S to T passes through intermediate
lattice points. Hence:

  (S, T) is lit iff there is a chain of g - 1 >= 1 non-vertex lattice
  points on one straight path, i.e. for g = 2 a non-vertex point X (not of
  class A) and a primitive d with E_X(-d) = S and E_X(d) = T.

So darkness says: the "point reflection through X" relation
R_X = {(E_X(-d), E_X(d)) : d primitive} misses (S, T) for every one of
the k non-vertex points X, and longer chains fail too. The conjecture for
orthogonal rooms is: k >= 7 and r <= 8 force (S, T) into some R_X or a
longer chain. In permutation terms E_X(d) is transport of x along the
Christoffel word of d in the square permutations H, V of the unfolding,
and [H, V] is a product of r 3-cycles.

## Settle these two

1. *Idea I, made precise or killed.* With the reformulation, state an
   exact linear-algebra or counting lemma in which the rank 2r of
   [H, V] - I (or the r 3-cycles) bounds something about the relations
   R_X, and say what inequality between k, r, and the number of class-A
   points would follow. Then test it by hand against (i) a rectangle
   (r = 0, R_X is the full central symmetry), (ii) an L room (r = 1), and
   (iii) the fact that a dark pair exists at r = 9 with k = 6 or fewer.
   If no such lemma survives, say so and why.
2. *A statement uniform in r.* d17 says a proof must show that "the bad
   residues of all path families can't hold together with at most 8
   reflex corners". In the reformulation this is: for fixed (S, T), the
   k relations R_X and the chain relations all miss (S, T). Propose the
   strongest statement of pigeonhole, double-counting, or averaging type
   that you can actually prove about the family {R_X}, for example a
   lower bound on |R_X| in terms of area, or an identity for
   sum over X of |R_X| that forces coverage of all A-pairs when k is
   large relative to r. Give the proof or the exact point where it
   breaks. A minimal-counterexample argument (smallest area dark room
   with at most 20 walls; what local move reduces it?) is also welcome
   if you can make one step rigorous.

End with one line: after this round, is there any idea you would fund
with real effort, and at what probability?
