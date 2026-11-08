# Combined O3 illumination statement: at most nine reflections

**[done] Independently reviewed within the stated local class.**
November 5, 2026. This statement incorporates the diagnostics agent's
independent O3-five and L70-extension reviews. It supersedes the older
eleven-reflection *bound* for this combined branch; original discovery,
proof and review records remain unchanged.

## Theorem and scope

Consider a finite, strictly simple canonical 45-degree triangle room in
the established **local two-root e2+e1+b1 class**, with exactly the full
interior A stars

\[
S=(0,0),\quad U=(2,0),\quad T=(2,2).
\]

Let H be the union of those three full stars. All other occupied cells
are in the established local set

`K={L(-2,0), B(0,-2), D(2,-2), R(4,0), E(4,2), Tc(2,4), N(0,2)}`.

Assume the larger root is **O3=B701**, the other positive cell is an e1
root, and all remaining cells are ordinary H-facing caps or empty,
according to the inherited classification. Here sectors0–7 run
E, NE, N, NW, W, SW, S, SE; `B701` means precisely sectors7,0,1 at B.
The notation b=1 retains its established meaning: one extra smooth
non-A point beyond the uncovered H-side midpoint contribution M.

**Then actual S and T are connected by a finite, corner-avoiding,
specular billiard trajectory with at most nine reflections.**

In particular, this covers the active surplus-four branch with W<=21
maximal walls and k<=6 transparent exceptions. The optical witnesses
below do not require additional numerical budgets. The completeness of
the local root/ordinary-cap classification is an explicit upstream
assumption, not a new conclusion of this statement.

## Proof by exhaustive dispatch

### 1. Short forcing cases

If E4 is absent, the independently rechecked one-reflection `one_sigma`
witness connects S and T, with all other local support allowed.
Otherwise reduce to E4 present. If L0 is absent, the independently
rechecked ordinary-E4, E34 and E45 witnesses use four, three and two
reflections, respectively. An E root lacking E4 was already covered by
the first case. Thus the remaining cases may assume active E4 and L0.

These are optical implications, not assertions that every room must
contain those caps. No Tc5 restriction is introduced by this reduction.

### 2. Second root other than L70

The new five-reflection witness is

\[
S\to(-1,-2/5)\to(1,-6/5)\to(0,-8/5)
\to(1,-2)\to(2/7,-16/7)\to T.
\]

Its required support lies in H+B701 and its complete forbidden set is
`{L7,D3,D4,B2,B6}`. After forcing, every second-root window other than
L70 and D23 fits this envelope, with the allowed ordinary caps elsewhere.
The contact `(1,-2)` is smooth180 inside a straight finite mirror;
the genuine O3 apex `(0,-2)` is avoided.

For the exceptional D23 root, Tc is ordinary. If Tc5 is absent, the
independently rechecked four-reflection path applies; if Tc is ordinary5,
its complementary six-reflection path applies. These cases exhaust
ordinary Tc=empty/5/6, with full L/E/R/N support allowed by their envelopes.

Hence **every second-root partner except L70 is covered within six**.
The detailed window/forcing proof and exact support checks are in the
[O3-five independent review](../O3-five/review.md).

### 3. L70, N7 absent: six reflections

The two-contact lower/upper L70 return replaces the old L0 three-contact
return with the same exit state. The complete six-path is

\[
S\to(-12/7,-2/7)\to(-8/5,2/5)\to(16/5,6/5)
\to(10/3,2)\to(24/7,10/7)\to(1,11/6)\to T.
\]

Minimum support is `H+L70+E4`. Its complete forbidden set is
`{L1,L6,E3,E5,N7}`. Full B/D/R/Tc and all N sectors except7 are allowed.
The trajectory crosses `(2,1)` in the interior of H, rather than
reflecting at an exposed source ceiling. The equation `12d=2` gives
`d=1/6`, strictly in `1/7<d<2/11`.

Thus **all N7-absent L70 cases are covered within six**, independently
of D/Tc occupancy and without a b-budget exclusion of N5.

### 4. L70, ordinary N7 and ordinary R3: nine reflections

Use the independently checked nine-path

\[
\begin{aligned}
S&\to(-1/4,-1)\to(-3/4,1)\to(-6/5,-4/5)\\
 &\to(18/5,2/5)\to(7/2,0)\to(10/3,2/3)\\
 &\to(2/3,4/3)\to(1/2,2)\to(2/5,8/5)\to T.
\end{aligned}
\]

Minimum support is `H+L70+R3+N7`. Its complete forbidden set is
`{L6,B2,R2,R4,N0,N5,N6}`. Ordinary R3 and ordinary N7 supply exactly
the required presences and absences; full D/E/Tc support is harmless.
The equation `16d-2=2` gives `d=1/4`, strictly in `3/13<d<4/15`.

### 5. L70, ordinary N7 and R3 absent: four reflections

The original eleven-path revisits actual S on the open segment from
`(-8/5,-2/5)` to `(3,3/4)`, which lies on `y=x/4`.
Discard its prefix and launch along the supplied final segment sequence:

\[
S\to(3,3/4)\to(2/3,4/3)\to(1/2,2)
\to(2/5,8/5)\to T.
\]

This four-path needs only `H+N7`. Its complete forbidden set is
`{R3,N0,N6}`; all other local triangles are allowed. With N ordinary7,
N0 and N6 are absent. R3 absent means R is ordinary4 or empty, both
permitted. The equation `8d=2` gives `d=1/4`, strictly in
`1/5<d<2/7`.

This improves the original eleven-reflection case to **four**.
Its first actual target, reversed first-target path and sigma/reversal
all pass independent checks. The full original reverse reaches S early;
the shorter path avoids any first-target ambiguity.

### 6. Exhaustion and maximum

Because O3 and L70 are the two positive roots, N and R are ordinary.
N7 is either absent or the entire ordinary N cap. In the latter case,
R is ordinary3, ordinary4, or empty. Therefore the three L70 cases above
are exhaustive, without enumerating cap assignments or constructing rooms.

| Exhaustive branch | Upper bound |
|---|---:|
| Short forcing cases | 4 |
| Second root other than L70 | 6 |
| L70 and N7 absent | 6 |
| L70, ordinary N7, ordinary R3 | 9 |
| L70, ordinary N7, R ordinary4 or empty | 4 |

The maximum is **nine reflections**, as claimed.

## Verification and limits

The new five-, six-, nine-, and four-reflection witnesses have complete
independently recomputed required/forbidden support sizes **11/5, 15/5,
21/7, and 9/3**, respectively. Rational triangle clipping includes all
intermediate mesh-edge and vertex contacts, not just reflection points.
Exact specularity, open-segment interior, finite mirrors, actual first
target and the appropriate reverse/sigma checks pass. The inherited
short forcing and D23 four/six witnesses were independently rechecked.

See the [L70 independent review](../L70-extension/review.md) for the
four-suffix improvement and [coverage](coverage.md) for dependency limits.
The combined [receipt checker](check.py) validates frozen source hashes,
the proof-map bounds and their maximum. It adds no new discovery run.

This is a reviewed **local two-root O3** result. It does not establish
West1234, the whole b1 partition, single-leaf or remote cases, the full
surplus-four theorem, or the universal 22-wall minimum. It is independent
AI mathematical review with exact checks, not formal verification or
expert refereeing.
