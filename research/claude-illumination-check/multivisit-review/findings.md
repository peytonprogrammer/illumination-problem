# Review of Codex's orthogonal no-repeat theorem

Claude, 2026-11-01. Reviews `illumination-k4-codex/smooth-step-multivisit/findings.md` (read-only).

**Verdict: ACCEPT** the theorem, the essential-blocker corollary and the orthogonal scope as written.

## Hand check
- **Same outgoing state.** If visits at r1 < r2 < T leave z with equal velocity, uniqueness gives α(r1+u) = α(r2+u) for u ∈ [0, T−r2]. So α(T−L) = t with r1 < T−L < T, which contradicts first arrival. r1 > 0 because s is interior and z is on the boundary.
- **Other state.** At a vertical wall, the two outgoing states are (−p, ±q). If the second visit leaves with the other state, its incoming velocity is −v. So the reversed excursion starts at z with the same state, and β(u) = β(L−u).
  - At the midpoint, an interior point would force velocity 0. A wall collision would force v_after = −v_before, which is normal incidence and needs an axial velocity. A corner is invalid.
  - A midpoint at z itself is a wall collision, so the same argument covers it.
- **Axial case.** A transverse visit has one outgoing state. Motion parallel to z's wall can't reach z: the line x = x0 enters the wall segment only through an endpoint, and maximal-wall endpoints are corners.
- **Corollary.** An axial trajectory stays in one open component of (line ∩ int P), bouncing at smooth points of its two end walls. t lies in that component, so the direct segment s→t is interior and avoids every boundary blocker.
- **Scope.** A single orthogonal reflection never reverses a nonaxial velocity, but a 45° wall does at normal incidence. The triangle control shows exactly that.

## Independent checks
- Codex's `check.py`, run from a separate copy (`/tmp/mvreview`): `"status": "PASS"`.
- `controls.py` (own code):
  - The reversal lemma holds on 18 nonaxial velocities.
  - The triangle path replays exactly: legs interior, 3 specular reflections (the middle one normal), and t off every earlier leg. t lies on leg 1's line but outside that segment.

## Note for later use
This removes the repeated-visit gap only for orthogonal rooms. Canonical 45° rooms with diagonal walls still need a separate treatment, as Codex states.
