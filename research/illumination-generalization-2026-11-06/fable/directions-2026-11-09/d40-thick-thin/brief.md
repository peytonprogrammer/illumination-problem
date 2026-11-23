# d40 brief: thick-thin size reduction

Budget about 100k tokens, theory only. No room, ray, direction, or
reflection-word discovery searches or enumerations. Read-only checks are
allowed on the named rooms below only (cap: under 5 CPU minutes total,
one process at a time). Write your answer to the -o file.

## Setting

Directory D = .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09
Read D/STATE.md first for the problem, terminology and what is proved.

Target: no strictly simple orthogonal lattice room with W <= 20 walls
(r <= 8 reflex corners, W = 2r + 4) has a dark pair of interior points.
Exhaustive census: none up to area 20. The obstacle to any finite search
is that W does not bound size. We want a size-reduction theorem.

## Idea to test

Partition the room into at most r + 1 maximal rectangles. Treat a large
rectangle as a "mixer": light entering it can leave through nearly any
exit point, up to lattice parity classes. Treat a narrow passage as a
"filter" that passes only some slopes. Conjecture: there is an explicit
f(r) such that a room is lit whenever all rectangles in some suitable
decomposition have both side lengths >= f(r); more usefully, a dark pair
forces a bounded box, so a finite census decides W <= 20.

## Deliverables, in order

1. Prove one clean special case. Suggested: a room containing one
   rectangle R of size a x b with a, b >= f(r), the rest arbitrary with
   r <= 8; show any dark pair must avoid R and its "shadow", or that the
   room is lit, or that R can be shrunk by a computable amount keeping
   darkness (the contrapositive of a lit-preserving insertion). State
   f(r) explicitly. Use lattice parity honestly: in a room with all
   coordinates divisible by 4 (d25-astra/astra-round2.md, L-room), a
   large chamber acts as a parity filter, not a free mixer.
2. Relate to existing tools: the band lemma (D/d28-band-stabilization/,
   inserting a band of height a multiple of M = 2Lp/gcd(q, 2L) preserves
   a witness; Lit_p periodic), Theorem R (D/d30-rigidity-proof/), and
   d16 (rational pairs lit implies real pairs lit).
3. Test against:
   - P6 (W = 28; D/d30-rigidity-proof/, D/d31-run-dark-min/found.json):
     dark only at corridor height 2, lit at 0, 1, 3, 4, 5, 6.
   - The 22-wall dark room (D/d29-rigidity-test/, D/d9 census).
   - The d26 near-dark family: two D x D chambers joined by a 1 x 1
     corridor, r = 2 (D/d26-adversarial/); lit, but shortest lighting
     path grows without bound.
   Any proposed lemma must keep P6 and the 22-wall room dark.
4. If you get a bound, state the resulting box size for r <= 8 and what
   finite check would then decide the target. If you don't, name the
   exact obstruction.
5. Probability that a size-reduction theorem of this type exists at
   r <= 8, and the single next step.

Tag every claim PROVED / CITED / GUESSED. Prefer a correct narrow result
to a broad conditional one. Avoid hypotheses that restate the target.
