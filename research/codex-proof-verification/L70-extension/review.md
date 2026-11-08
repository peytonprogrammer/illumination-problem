# Independent L70 extension review

**Verdict: accept the extension and improve its bound from eleven to nine
reflections.** The eleven-reflection witness has a removable initial loop:
it passes through the actual source S again after its seventh reflection.
Its supplied final four reflections already connect S to T legally.

This review covers the frozen `O3-L70-hand/argument.txt` six-path and the
subsequently frozen `L70-N7-search/findings.txt` nine/eleven complement.
The previous independent O3-five review covers the other partners.
All conclusions below retain the established **local two-root e2+e1+b1
classification**; this review does not reprove that global classification.

## 1. Six-reflection extension: accepted

The path is

\[
S\to(-12/7,-2/7)\to(-8/5,2/5)\to(16/5,6/5)
\to(10/3,2)\to(24/7,10/7)\to(1,11/6)\to T.
\]

Its first two contacts are the lower and upper diagonals of L70. Starting
with velocity `(-1,-d)`, direct intersections give

\[
\left(-\frac2{1+d},-\frac{2d}{1+d}\right),\qquad
\left(\frac{4d-2}{1-d},\frac{2d}{1-d}\right).
\]

The outgoing state at x=-1 is `(-1,3d)` with direction `(1,d)`. Thus it
really replaces the old L0 three-contact return by two contacts with the
same exit state. The subsequent E4 three-contact return enters at `(3,7d)`
and exits at `(3,9d)`, heading `(-1,d)`. The bare target-left wall at x=1
is reached at height `11d`, and the final height at x=2 is `12d`.
Consequently actual T forces `d=1/6`, strictly in `1/7<d<2/11`.

All finite mirror contacts are strict. The segment from the second L
contact to E crosses `(2,1)` with its full 360-degree neighborhood supplied
by H; it does not hit an exposed ceiling. My independently implemented
rational triangle clipping reproduces exactly **15 required and five
forbidden triangles**:

`Z6 = {L1,L6,E3,E5,N7}`.

They prove the stated minimum `H+L70+E4` and maximum allowing full
B/D/R/Tc and every N sector except7. Specularity, first actual T,
reverse/sigma and unfolding `(-12,-2)` pass independently. There is no
dependence on a room census or on the b/W/k budget in this optical lemma.

## 2. New nine/eleven complement: accepted

For both new witnesses, launch `(-d,-1)`. The first three contacts are

\[
(-d,-1),\quad(-3d,1),\quad
\left(-\frac{6d}{1+d},\frac{4d-2}{1+d}\right).
\]

These are source floor, source ceiling, and the lower L70 diagonal.
The L inlet `(-1,4-1/d)` is interior. At `d=1/4`, it equals `(-1,0)`;
H and L70 supply its full 360-degree neighborhood. It is not a reflection.
The ray exits at `(-1,5d-2)` in direction `(1,d)`.

**Ordinary R3 present.** Its three-contact diagonal/floor/diagonal return
exits at `(3,11d-2)`. N7 is entered at height `13d-2` and its normal
three-contact return exits at height `15d-2`. The actual target equation
is `16d-2=2`, hence `d=1/4`, strictly inside `3/13<d<4/15`.

My independent check reproduces **21 required/seven forbidden triangles**:

`Z9 = {L6,B2,R2,R4,N0,N5,N6}`.

The required support lies in `H+L70+R3+N7`; full D/E/Tc is harmless.
All nine reflections, every intermediate segment, first actual T,
reverse/sigma and unfolding `(-4,-16)` pass. No additional room was
constructed: this is a universal conditional support check of the supplied
fixed path.

**R3 absent.** The supplied eleven-path uses two bare U-right reflections
and two distinct L visits. My independent check reproduces its complete
**22 required/seven forbidden triangles**:

`Z11 = {L1,L6,B2,R3,N0,N5,N6}`.

The same rational-root derivation gives `24d-4=2`, so `d=1/4` is strictly
inside `5/21<d<6/23`. I independently rebuilt the one supplied 33-triangle
room: one simple boundary, 20 maximal walls, only S/U/T full A stars,
J=3 and s_N=3. All eleven contacts are the first finite wall on their
legs, and actual T is first reached on the final leg.

Its bounce `(0,1)` is smooth180 and strictly inside the maximal ceiling
from `(-1,1)` to `(1,1)`. N5 and N6 are absent. It is not a corner.

## 3. Review improvement: keep only the last four reflections

The eleven-path leg from `(-8/5,-2/5)` to `(3,3/4)` lies on `y=x/4`.
It therefore passes through **S=(0,0) in its interior**. Removing the
prefix gives the supplied suffix

\[
S\to(3,3/4)\to(2/3,4/3)\to(1/2,2)\to(2/5,8/5)\to T.
\]

This is a four-reflection path with initial direction `(4,1)`.
It requires only `H+N7`; its independently derived forbidden set is

`Z4 = {R3,N0,N6}`.

The complete support has **nine required/three forbidden triangles**.
Thus the maximum may include all local triangles except those three.
It contains the eleven-path's entire claimed maximum. The shorter path
therefore applies everywhere that eleven-path was being used, and more.

Launching `(1,d)` gives U-right height `3d`, N7 entry height `5d`, exit
height `7d`, and target height `8d`. Hence `8d=2` again gives `d=1/4`,
strictly inside `1/5<d<2/7`. All finite contacts, open segments, first
actual T, reverse/sigma, and unfolding `(8,2)` pass. Physical replay on
the same frozen polygon also passes in all three orientations.

This is deletion of a loop in a supplied witness, not a direction or
reflection-word search. Passing the source again does not invalidate the
original forward billiard. It does mean the full reversed eleven-path
reaches its target S before the listed endpoint; use the four-reflection
reverse/sigma prefix for any **first-target** claim in those orientations.

## 4. Whole branch: the improved bound is nine

In the established local two-root O3+L70 class, E and N/R are ordinary.
If E4 is absent, the already independently checked one-reflection forcing
lemma applies. Otherwise E is exactly4.

| Remaining case | Independently checked cover |
|---|---:|
| N7 absent | Six reflections |
| N is ordinary7 and R is ordinary3 | Nine reflections |
| N is ordinary7 and R is ordinary4 or empty | Four reflections |

Ordinary7 excludes N0/N5/N6. Ordinary R3 excludes R2/R4; otherwise
ordinary R4 or empty excludes R3. Those absences are exactly what the
new optical maxima require. All D/Tc choices are permitted, so the split
needs no further budget exclusions or assembled-cap enumeration.

Therefore **the entire local two-root O3+L70 branch illuminates within
nine reflections**. Joining this with my previous independent review of
all other O3 partners within six gives **the entire local two-root O3 b1
branch within nine reflections**, conditional on the inherited class.

The earlier N7-remaining budget statements are consistent but superseded
by this complete cover. I independently checked the local angle sum
`b=1+N5+Tc5*N0+D1*R4` and J=3 using per-vertex coefficients without
enumerating completed rooms. Those calculations are not needed for the
stronger ordinary-R split above.

## 5. Evidence, scope and reproduction

The checker reuses only my own rational-clipping primitives from the
previous O3 audit. It executes/imports no author geometry, discovery or
verification code. It reconstructs only the supplied eleven-path room;
the other witnesses are checked through full conditional support. Five
fixed mutation controls reject admitting each protected six-path mirror
mate. Source hashes and exact outputs are in `check.json`.

```sh
python3 -B .context/codex-proof-verification/L70-extension/check.py
```

This review accepts the local O3 branch and improves its stated bound.
It does not establish the whole b1 partition, West1234, mixed single-leaf,
remote families, surplus-four theorem, or universal 22-wall minimum.
The root classification and ordinary-cap convention remain upstream
assumptions. This is an independent review with exact computational
checks, not formal verification or expert refereeing.

Original research files were left unchanged. The improvement and review
are posted to the shared coordination board for the research agents.
