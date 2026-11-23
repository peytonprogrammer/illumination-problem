# D111: review of qclass-closure/bbbb/thick-thin.md

Date: 2026-11-20. Reviewer: independent referee. All path checks are exact, in
Q(√2) with `fractions.Fraction` coefficients. The tracer is new code that follows
the physical ray wall by wall and kills it at any polygon vertex, so it shares
nothing with the note's unfolding. Python with `-B`, about 6.5 CPU-minutes in
total. No room search was run; the three test rooms are constructed below.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Thin-door theorem | Sound. Every step checks, including the four-ratio equivalence and the cap-corner truncation. 25 of 25 constructed witnesses trace exactly. |
| 2. Unbounded words | Sound. The inequality (Nₕ+1)(Nᵥ+1) ≥ ΔL/(Bw) is correct for every lighting path. The note gives the example family only in words; instance A below instantiates it. |
| 3. Conditional reduction | Sound as a conditional statement. Openness holds under the project's corner-avoidance convention. One wording gap and one scope gap in the list of missing inputs; see below. |
| 4. Scope | Removes nothing from the open core. Lattice rooms with lattice marks are triply rational, which is exactly the exception. |

## Claim 1: the thin-door theorem

**Setup.** Chamber 1 is [0,D₁]×[0,H₁] with door y ∈ (c,c+w) on x = D₁. The
corridor is [D₁,D₁+L]×[c,c+w]. Chamber 2 is [D₁+L,D₁+L+D₂]×[e,e+H₂]. This is a
12-wall room.

**Phases.** Launch upward with horizontal travel a to the door wall. The
unfolded height at the door is y_S + sa. The upward-arrival door phase is
u(s) = y_S + sa − c − 2H₁k, required in (0,w). That gives windows of width w/a
and step 2H₁/a. The target leg in backward time gives
u₂(s) = y_T − c − sb + 2H₂m in (0,w), with windows of width w/b and step 2H₂/b.
The corridor condition is u + sL − u₂ ∈ 2wℤ. The mismatch has derivative
a + L + b. All of this matches the note.

**Irrationality.** The map s ↦ (s mod 2H₁/a, s mod 2H₂/b) is a line on a 2-torus.
Its positive half is dense exactly when H₁b/(H₂a) is irrational, by Kronecker.
So both open windows can be aligned to within any ε at arbitrarily large s. The
overlap then exceeds min(w/a, w/b) − ε > δ. No approximation rate is needed,
because nothing bounds k or m. The proof is pointwise in w: each w gets its own
k, m and j. "Uniformly as w → 0" means only that one hypothesis covers every
w > 0. It does not mean a uniform word or a uniform slope interval, and the note
does not claim either. The interval condition 2w/(L+a+b) < δ < w/max(a,b) is
equivalent to L > |a−b|. A closed range of length (L+a+b)δ > 2w contains a
multiple of 2w.

**Legality.** On each chosen leg the ray meets a vertical wall only at the cap,
if used, and then at the door wall, once. So the door endpoints are met only
inside the open door. The corridor has no corners other than the door
endpoints. Every horizontal-wall hit is at a smooth point, because corners lie
on vertical walls. An exact cap-corner hit reverses both velocity components.
The formal straight continuation in the rectangular unfolding is therefore the
retraced leg. It passes through S again, and from there it is the direct leg
with the opposite vertical sign, on the same unfolded line. Truncating there
keeps both phases. This is correct.

**Corollary.** For L ≥ 2 max(D₁,D₂), a ∈ (0,2D₁) and b ∈ (0,2D₂) give
|a−b| < L. The ratio of the two a-choices at fixed b is (2D₁−x)/x, so all four
ratios are rational iff x/D₁, z/D₂ and H₁D₂/(H₂D₁) are rational. Both claimed
consequences follow.

**Exact tests (`thin_door.py`, `thin_door.log`).** The script builds the
witness exactly as the proof does: it aligns the windows, picks j and solves for
s in Q(√2). It then traces s with the independent tracer. It also traces a
mutant slope s + w/10⁶, which must fail.

| Instance | Dimensions | Hypothesis | Widths | Witnesses lit | Mutants lit |
| --- | --- | --- | --- | --- | --- |
| A | D₁=H₁=D₂=1, H₂=√2, L=2 | aspect quotient irrational | 1/20 (4 branches, 2 pairs), 1/60 (2 pairs), 1/150 | 11/11 | 0/11 |
| B | D₁=H₁=1, D₂=H₂=2, L=4 | commensurable, x/D₁ = √2/2 | 1/20 (4 branches), 1/60 | 5/5 | 0/5 |
| C | D₁=√2, H₁=1, D₂=1, H₂=1+√2, L=2√2 | quotient 1/(2+√2) | 1/20 (4 branches), 1/60 | 5/5 | 0/5 |

Instance C has an irrational target mark x-coordinate, 3√2 + 1/2. The longest
witness has 168,776 horizontal-wall hits (B, w = 1/60). The direct/direct
branches hit no vertical wall; the cap branches hit one vertical wall per cap,
as the proof predicts.

**Control (`rational_control.py`, `rational_control.log`).** With H₂ = 1 in
instance A, the dimensions and marks are triply rational. The same search,
up to k = 200,000, finds no window overlap on any branch at w = 1/60, 1/150,
or 1/1000. With H₂ = √2 it finds one on every branch at every width. This
shows that the construction really uses irrationality. It says nothing about
darkness: the search fixes the launch sign and the target image sign.

**Tracer control (`tracer_check.py`).** Shots aimed exactly at the reflex door
corner and at a convex corner die, and a straight corridor shot lights.

## Claim 2: unbounded words

The argument checks. Between consecutive vertical-wall hits the ray is
horizontally monotone, so the total horizontal travel is at most (Nᵥ+1)B. The
vertical travel is at least Δ, so s ≥ Δ/((Nᵥ+1)B). The corridor has no vertical
walls, so some traversal covers horizontal length L. Inside the strip each
vertically monotone piece rises at most w, so sL ≤ (Nₕ+1)w. Combining gives
the bound. It is scale-invariant and applies to every lighting path, not only
the constructed one.

The note states the example family in words only: fixed rectangles with an
irrational aspect quotient, fixed L ≥ 2 max(D₁,D₂), marks of distinct heights,
and a shrinking door. Instance A is such a family. At S = (1/3, 1/5),
T = (37/10, 6/5) the bound is 10, 30 and 75 at w = 1/20, 1/60 and 1/150. Every
traced witness exceeds it by a wide margin. These checks are consistency checks;
the theorem is the inequality.

## Claim 3: conditional thick-part reduction

**Openness.** RESULTS §2 kills a ray at every corner, convex or reflex. Under
that convention a legal path meets the boundary only at reflection points in
open edges. Each such point is at positive distance from every other edge. Each
open segment of the path is in the open interior and cannot touch a straight
wall tangentially without lying on it. So the path has positive clearance from
every vertex and every unused edge. Small changes to the shape and endpoints
preserve all the finitely many strict inequalities. A ray that grazes a reflex
corner is illegal under this convention, so it needs no stability argument. If
a later variant allows grazing, openness fails at those paths.

**Wording gap.** The list of preserved conditions names transverse crossings,
interior endpoints and vertex clearance. A complete certificate also needs each
developed segment to cross no other edge of its copy. That condition follows
from the same clearance, but the semialgebraic certificate must include it
explicitly.

**Semialgebraic.** Reflections in axis-parallel supporting lines are affine with
integer coefficients in (shape, S, T). Crossing parameters are ratios of
polynomials. After clearing denominators with sign conditions, the domain of
one word in one chart is an open semialgebraic set over ℚ, in fact quantifier
free. The note is right that the determinants are quadratic, not linear.

**Covering logic.** The added boundary is a closed subset of a finite union of
compact charts, so it is compact. Finitely many certified neighborhoods cover
it. The complement is compact and consists of valid configurations. If each of
these is lit, the open word domains have a finite subcover. The converse check
and the quantifier-elimination remark are correct. The note correctly states
that compactness gives no word bound and no procedure for a negative answer.

**Reflex-sector lemma.** The unfolded angles are ±ε and ±(3π/2 − ε) modulo 3π.
The least separation is 3π/2 − 2ε > π for ε < π/4. A segment that avoids the
apex sweeps less than π of polar angle. This is correct.

**Is the list of missing inputs complete?** For orthogonal rooms with W ≤ 20 and
all-real marks, yes. It names the boundary certificates, including mixed and
simultaneous degenerations and endpoint faces, and full lighting of the
remainder. Three omissions:

1. **45-degree rooms.** The charts use horizontal and vertical supporting lines
   only. The project target includes 45-degree walls, and RESULTS §11 lists
   them as open. They need their own charts.
2. **Strength of the target.** The reduction proves the all-real statement,
   which is stronger than the lattice-pair goal. One real dark pair at a thick
   W ≤ 20 point would defeat the reduction even if every lattice pair is lit.
   The note says the all-real statement is open, but it does not list this as a
   risk of the method.
3. **Charts meeting at a boundary point.** A boundary point can lie in the
   closure of several charts. Each boundary certificate must cover the valid
   configurations from all those charts. "Repeated over the finitely many
   charts" covers this only if each chart is closed separately.

## Claim 4: scope

A lattice room with lattice marks has rational H₁D₂/(H₂D₁), x/D₁ and z/D₂. That
is the exception, as the note says. So the theorem lights no lattice pair and
removes nothing from the open core (BBBB lattice pairs, r ≤ 8).

What it adds is outside the core. In lattice dumbbells with L ≥ 2 max(D₁,D₂),
opposite-chamber real pairs with an irrational horizontal offset are lit at any
door width. Its length threshold is far below the K ≈ 10⁶ that D110 computes for
the period-one tail. At n ≥ 120, d80 already lights every pair with an
irrational coordinate. Pairs in the corridor or in one chamber are not covered.
The conditional reduction removes nothing until its two inputs are supplied.

## Reproduce

From this directory:

    python3 -B thin_door.py          # about 6 CPU-minutes, writes thin_door.log via redirect
    python3 -B rational_control.py   # under 30 s
    python3 -B tracer_check.py       # under 1 s

Files: `qr2.py` (Q(√2) arithmetic), `tracer.py` (exact wall-by-wall tracer),
`thin_door.py`, `rational_control.py`, `tracer_check.py` and their `.log` files.
