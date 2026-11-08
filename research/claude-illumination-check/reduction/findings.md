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
- **Orbit-size study (`orbit_exp.py`, `unrooted.py`).** 24-wall parity room, 108 squares.
  - With full labels, rooted: over 3,000,000 states.
  - With every label removed, rooted at the start square: over 2,000,000 states (53 s).
  - With no labels and no root (the bare surface): over 60,000 states (148 s).
  - So label-forgetting can't fix it. The SL2(Z) orbit of the bare square-tiled surface is already large, as expected for a high-genus origami with about 100 squares.
  - R22's small orbit (10,368) is the exception. It's probably due to its three-copy fold structure, but that isn't checked.
  - Root-symmetry quotients, such as canonicalizing over all 8 lifts of S, save at most a factor of 8. That isn't enough.
- **Practical decider (recommended use).**
  1. Parity certificate: every non-A lattice point in the closed room is a corner. It's exact and instant, and holds for all 60 sampled parity rooms.
  2. Orbit BFS: exact for rooms with small orbits. It gives LIT verdicts quickly, because a lit direction shows up early.
  3. Event certificates (existing `parity-enum/certs`) for dark rooms outside both cases.
- **Consequence for the reduction.** The orbit is not a practical route to proving darkness of general rooms with 22–26 walls, so §3's counting idea has to be a proof, not a computation.

## 3. Consequences and next steps
- **Exact searches by size.** "No dark room with W <= 21 inside box B" becomes an exact finite statement for each B. That's still a window result, so the reduction doesn't follow from it.
- **A sharper target.**
  - In a dark room, a T-lift can't lie on S's leaf in any direction unless a corner lift intervenes.
  - In origami terms: for every orbit element, T's square isn't reached on S's r-cycle before a corner square.
  - With many squares relative to W, the r-cycles are long and few corners are available, which pushes rooms toward being lit. Turning this into a counting bound on k is the concrete lattice route to the reduction.
- **Exact classification testing.** The classification conjecture can now be tested exactly on any candidate.

## 4. Step 3: the counting route, and the narrowed sign theorem (2026-11-01)
- **The counting idea in §3 is false as stated.**
  - Dilating a dark room by k keeps it dark, because darkness depends only on the real geometry.
  - The dilated room has about k² times as many squares, with the same W and the same corners.
  - So no bound of the form "many squares relative to W forces lit" can hold. Any lattice bound must be scale-invariant.
- **What remains of the lattice route.**
  - Primitive near-dilates, such as kP with one wall moved by one lattice step, sit at normalized distance about 1/k from P.
  - Those rooms are lit for large k exactly when P is isolated. So the k-bound comes back to isolation (§1), which comes back to the sign theorem (`l3-analysis.md`, "The missing sign theorem").
- **Narrowed target, from re-analysis of the 327 existing R = 12 parity certificates.** Scripts are `parity-enum/analysis/ringsub.py` and `ringsub2.py`, using the venv at `/tmp/npenv`. No new search.

| Event corners kept | Full rank and positive span |
| --- | --- |
| 8 neighbors of both marks | 327 of 327 |
| 4 axis neighbors of both marks (the forced 270° corners) | 293 of 327 |
| 4 diagonal neighbors of both marks | 43 of 327 |
| 8 neighbors of one mark only | 72 (s) or 35 (t) of 327 |

  - In the 34 holdouts, the axis-neighbor events already have full rank. Only the positive span fails.
  - Adding the events of one diagonal neighbor of s or t fixes every holdout.
  - **Sharpest observed form.** For every parity room with W ≤ 26, the events at the 8 forced 270° corners around s and t, plus one diagonal neighbor, give an isolation certificate.
- **Why this is a better target.** Every parity room has the same local picture at those 8 corners: a full 8-tile star around each mark, with each axis neighbor a 270° corner that has exactly three tiles.
  - A proof can fix the corner and vary only the global part, which is the reflection word that brings the path back to the corner.
  - **First lemma to try.** Split each event functional at a ring corner c into two parts.
    - **Corner part.** Moving c by δc moves the developed corner by L_e·δc, which contributes σ_e·w_e × (L_e·δc).
    - **Wall part.** Each hit on a moved wall contributes a 2·g_k·n_W term.
    - The corner part has the same form as Wolecki-style mark isolation: 2D vectors σ_e·L_eᵀ·J·w_e. Positive spanning in the plane is plausible there, because event directions at one corner are spread.
    - The open step is the coupling. The walls through c move c and also change the other reflections, so the corner part isn't independent.
    - **Checked on data (`reduction/cornerpart/`).** I re-exported the 327 rooms with L_e, using `rigidity45_L.py` at R = 12; all 327 functional sets match the stored certificates exactly. Then I tested whether the corner-part vectors positively span R² at each axis corner.
      - They do at 2,229 of 2,616 axis corners (85%).
      - They do at all 8 axis corners in only 101 of 327 rooms.
    - **Conclusion.** The corner part alone doesn't supply the positivity. In most rooms, some axis corner's events all push its corner into one half-plane, and only the wall-hit terms close the cone. A proof has to handle the coupling directly; there's no corner-local shortcut.
- **Status.** This is a conjectural target backed by data from 327 rooms, not a proof. It applies only to parity rooms; R22's retracing mechanism needs its own version.
