# d158 referee report: simultaneous-door-fractions (snapshot 2026-11-22 04:20)

**Verdict: sound with gaps.** Both counterexamples hold exactly. The dumbbell
refutes denominator sufficiency on a 12-wall room, and the far-cap repair is
legal. The R22 sign argument is correct and complete for its one word per D.
It proves darkness for that itinerary family only, not for R22. No gap is
high. The main weakness is framing: neither obstruction depends on the size
of the denominators.

Artifacts: `checks.py` (exact `Fraction` arithmetic, tracer copied from
d157), `checks.log` (0.6 CPU seconds). Every vertex stops the ray. Named rooms
only. The only enumerations are over directions in a fixed room.

## 1. Dumbbell (checks.log section 1)

Room: cells [0,5]², [5,5+L]×[2,3], [5+L,10+L]×[0,5]. S=(4,1), T=(6+L,3).
Checked for L = 12, 22, 32 (D = 14, 24, 34).

| Claim | Result |
|---|---|
| 12 walls, strictly simple, S and T interior | Confirmed for all three L. |
| Positive sheets: h1+h2 ≡ 4 mod 10 | Confirmed. The only residue over a,c∈[−3,3] and b∈[−3D,3D) is 4. |
| Each door's positions in (2,3) are spaced 2/D | Confirmed. There are 6, 11, and 16 positions with gap 1/7, 1/12, 1/17. |
| One-unit-leg slope sets are disjoint for all signs | Confirmed exactly. Each unit interval is decided at its midpoint because the folds are linear there. The lower ends are {1,3,6,8} and {0,4,5,9}, with empty intersection. |
| No rightward-monotone shot S→T | Confirmed. All 20D slopes s=k/D (s mod 10 covers a full period) were traced, and none is monotone and hits T. This set is complete: any monotone hit has horizontal travel D and an integer transverse displacement. |
| Far-cap repair, 10/9<s<11/9, (L+10)s∈2ℤ | Confirmed. s=13/11 (L=12); 9/8 and 19/16 (L=22); 8/7 and 25/21 (L=32). Each reaches T with exactly one vertical bounce at x=10+L and no corner. The door heights equal 1+s and 13−9s exactly. |

**Coverage of the disjointness proof.** The proof covers every rightward-monotone
word. In those words |dy/dx| is invariant, the first leg has length 1 from
height 1, and the last leg has length 1 back from height 3. The corridor and L
never enter the argument. Integer |s| is a lip or corner hit and is correctly
excluded. Words with any longitudinal reversal fall outside the stated type,
and the repair shows that one reversal already suffices.

## 2. R22 (checks.log section 2)

| Claim | Result |
|---|---|
| Source box [−1,1]², openings 0<x<1 on y=±1, upper run [0,4]×[1,2] | Confirmed from the 15 cells. |
| s0=−4/(2D−3): lateral hit at (2D−3)/4, recrossing at D−3/2, x=2/(2D−3) at D−1, misses T | Confirmed exactly for m = 3, 4, 5. The endpoint is x = 6/(2D−3). Slopes s0 ± 1/(1000D) also follow the prefix. |
| Open interval of legal prefixes | Confirmed. This branch is s ∈ −(2/(D−1), 2/(D−3)) with the corner slope −2/(D−2) removed. The three endpoint slopes hit corners at (0,1), (0,−1), and (−1,1). The note never states this interval. |
| No slope completes the word | Confirmed exhaustively for D = 8, 16, 32. Any shot reaching T at vertical travel D has s∈(1/D)ℤ, and s mod 8 is a full period. All 16D such slopes were traced, and 0 follow the word and reach T. |
| Sign argument | Confirmed on every candidate s∈(2/D)ℤ that has a legal last crossing and lands on a T image. Every candidate violates visit 1 (positive sheet) or the pair 3, D−3 (negative sheet). |

**Sign argument check.** The case split is complete. The sheet at t=D−1 is
well defined because z∈(0,1) is open, and the T images ±2 mod 8 reduce to
2 mod 4. The positive case gives Ds≡2 mod 4 and z=f(2−s)=f(s), which
contradicts visit 1. The negative case gives Ds≡0 mod 4 and f((D−3)s)=−f(3s),
which contradicts visits 3 and D−3. That step needs 3<D−3, which holds for D≥8.

**Scope.** The result is darkness of one longitudinal word per D, over every
transverse reflection count. It is not a proof that R22 is dark for (S,T).
That theorem rests on the manuscript's cylinder certificate. The note's own
sentence ("this word of longitudinal contacts") is correctly scoped. As a side
observation, no slope of any route reached T at vertical travel D, which agrees
with the manuscript's theorem.

## Gaps

1. **Medium: neither obstruction depends on the denominators.** The dumbbell
   disjointness holds for every L≥1, and L never appears in it. The R22 argument
   holds for every D≡0 mod 4 with D≥8. Exhaustive runs for D=12 and D=20 also
   give 0 completions. The 2^m choice serves only to make every j/D reduced. The
   note should state that the obstruction is the pairing of the visits at t and
   D−t, and that large denominators neither cause it nor cure it.
2. **Medium: the refuted statement is not written out.** The note refutes
   "denominator sufficiency" without stating it. The R22 "denominator at every
   contact" is measured against a completion time D that no shot attains, since
   R22 is dark. The note should state the hypothesis it refutes; section 3 below
   proposes one.
3. **Low: undefined data in the dumbbell setup.** The symbols n=50+L and r=4,
   and the condition "j≥2 so n>64, criterion applies", are not defined or used.
   "DB55" names the L=3 room in d157, so the L=10j+2 stretch needs its own name.
   Restricting L to 10j+2 matters only for the gcd remarks.
4. **Low: the 2/D spacing is shown on positive sheets only.** The all-sheets
   paragraph replaces it with interval disjointness, which is stronger. The
   "every one-dimensional projection" sentence should still be limited to
   positive sheets.
5. **Low: the open prefix interval is implicit.** The interval is
   −(2/(D−1), 2/(D−3)) minus the corner slope −2/(D−2) (verified above). The note
   should state it, together with the corner at t=D/2−1.
6. **Low: the last paragraph of the R22 section is speculative.** The remarks
   on the dyadic staircase and the D142 converse are commentary, not results.
   They should be labeled as such.

## 3. What is refuted, and the joint obstruction

**Refuted (denominator sufficiency).** Fix a longitudinal word w with mandatory
visits at times t_i = n_i/D in reduced form, and open windows W_i. The claim is
this: if each visit's endpoint-constrained placement grid is finer than its
window (spacing < |W_i|), then some slope realizes w from S to T. The dumbbell
refutes it with two visits. R22 refutes the variant "no visit at t=1/2 and all
denominators large". Neither example refutes free-choice illumination or the
open route-selection statement in the note's table.

**Joint obstruction implied by the note.** The target fixes Ds modulo the fold
period, with one residue class per sheet ε. For each ε, this links the folded
position at time t, measured from S, to the folded position at time D−t,
measured back from T. The link is an isometry φ_ε of the fold period, so
h_{D−t} = φ_ε(h_t). Word w is dark if, for every ε, some pair of visits (i, j)
has φ_ε(W_i) ∩ W_j = ∅.

- **Dumbbell.** Visits 1 and D−1 give h1+h2 ≡ 4 mod 10 on positive sheets. The
  map φ sends (2,3) to (1,2), which misses (2,3). On all sheets, the same pair
  forces |s| mod 10 into the disjoint sets {1,3,6,8}+(0,1) and {0,4,5,9}+(0,1).
- **R22, positive sheet.** Visits D−1 and 1 satisfy h_{D−1} = h_1, but the
  windows are (0,1) and (−1,0).
- **R22, negative sheet.** Visits D−3 and 3 satisfy h_{D−3} = −h_3, but both
  windows are (−1,0).

A route-selection lemma must therefore control these paired constraints for
visits at t and D−t, or change the word to break the pairs. The far-cap
reversal in the dumbbell breaks the pair.
