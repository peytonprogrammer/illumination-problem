# Attacking the reduction (k bound)

Claude, 2026-11-01. Approved by Daniel ("attack reduction").

## Target
- **Reduction(σ).** Fix a combinatorial shape σ: the cyclic sequence of wall directions in the canonical tiling, with W <= 21.
- **Claim.** Up to the symmetries of σ, only finitely many lattice rooms of shape σ have a dark pair of interior A marks.
  - The symmetries are scaling, plus axis stretches for orthogonal σ.
  - Each such room then has a primitive representative with some k <= f(σ), and finitely many SAT cases settle σ.
- **Why it's needed.** Without the quotient the claim is false. Dilations, and stretches of orthogonal rooms, map dark rooms to dark rooms with unbounded k.

## 1. The reduction is the isolation-plus-degeneration program (no shortcut)
- **Setup.** Suppose infinitely many inequivalent dark lattice rooms P_n of shape σ exist. Normalize by the symmetries, for example by total wall length 1. The normalized length vectors lie in a compact simplex, so a subsequence converges to some θ0.
- **Case 1: θ0 is a nondegenerate room P0 (real parameters).**
  - Robust lit paths persist (Lemma 7), so P0 has no robust connection (Proposition 8).
  - P0 is a non-isolated point of the decorated-dark set of shape σ, since P_n ≠ P0 mod symmetry and P_n -> P0.
  - Each event e of P0 forces g_e·δ_n >= 0 at first order, with δ_n = θ_n − θ0. A strictly negative value moves the corner-path to the lit side.
  - If the events of P0 positively span (the sign theorem), δ_n = 0 at first order. A second-order argument, or certificate radius control, then finishes.
- **Case 2: θ0 is degenerate.** These are exactly the degenerations tabulated in `l3-status.md`.
- **Conclusion.** Reduction(σ) follows from [sign theorem at every decorated-dark real room of shape σ] plus [every dark degeneration of shape σ excluded].
  - The converse holds in spirit. A positive-dimensional family of dark rooms with a rational accumulation point would defeat the reduction.
  - The k-bound is therefore not easier than the general program, and no lattice-only shortcut follows from compactness.

## 2. What being on the lattice does add: darkness is exactly decidable
- **New tool:** `origami_dark.py`.
  - The unfolding X is a square-tiled surface over R^2/Z^2, branched only at lattice points.
  - Darkness of (S, T) means every primitive direction's ray from a lift of S meets a corner lift before a T lift.
  - With A ∈ SL2(Z) sending w to e1, that ray is the horizontal ray on A·X. It runs along square bottom edges through lower-left corners s, r(s), r²(s), ….
  - The shears T: (r,u) -> (r, u r^-1) and L: (r,u) -> (r u^-1, u) keep lower-left corners, so corner labels survive.
  - The orbit of the labeled origami, canonicalized from the start square, is finite.
- **What this gives.** An exact, finite darkness proof or lit verdict for any lattice room, with no direction radius.
- **Validation.**
  - The 22-wall room (0,0)-(2,2) is DARK (orbit 10,368, 0.3 s).
  - (0,0)-(2,-2), another preimage of b, is DARK.
  - (0,0)-(4,0), a preimage of a, is LIT, as the fold proof predicts.
- **Cross-check (`xcheck.py`, `xcheck.out`, `four.py`, `four.out`).** 360 rooms, orbit cap 200,000.
  - 150 tracer-lit pairs from `lit-rel.txt`: all 150 LIT.
  - 150 pairs where the bounded tracer found no path (`dark-k*.txt`): 146 LIT, 4 DARK.
    - 142 of the 146 have an exact lit path at R = 15.
    - The other 4 have exact lit paths at R = 40, in directions (-40,7), (-39,16), (-13,-30), (-39,8).
    - So every LIT verdict is confirmed by an explicit exact path. The tracer's "no path found" was a radius artifact in 146 of 150 cases.
  - 60 proven-dark parity rooms (W = 22–26): all 60 UNDECIDED at the cap. None came out LIT.
    - One 24-wall room is still UNDECIDED at cap 3,000,000 (90 s).
  - **Verdict.** No contradiction in 300 decided cases. The decider is sound on this sample, but its orbit is too large for most parity rooms. R22's orbit of 10,368 is the exception, not the rule.
  - **Fix to try next.** Shrink the orbit by forgetting labels the verdict doesn't use, or by stopping at the first orbit element where every corner square precedes T on all relevant r-cycles.

## 3. Consequences and next steps
- **Exact searches by size.** "No dark room with W <= 21 inside box B" becomes an exact finite statement for each B. That's still a window result, so the reduction doesn't follow from it.
- **A sharper target.**
  - In a dark room, a T-lift can't lie on S's leaf in any direction unless a corner lift intervenes.
  - In origami terms: for every orbit element, T's square isn't reached on S's r-cycle before a corner square.
  - With many squares relative to W, the r-cycles are long and few corners are available, which pushes rooms toward being lit. Turning this into a counting bound on k is the concrete lattice route to the reduction.
- **Exact classification testing.** The classification conjecture can now be tested exactly on any candidate.
