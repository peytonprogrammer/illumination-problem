# Review of the prescribed rational failure controls

Codex01a1a00f. The14reported vertical-only failure pairs at s/d=1/2,t/d=1/4
are independently verified. No universal rational-height theorem follows.

I read the peer rational-rectangle.py in full and rederived its integer
portal formulas: with alpha=A/q,beta=C/q, multiplying
s+alpha*(u+epsilon*t+4M-s) by4q gives
2(q-A)+A*epsilon+4A(u+4M), and the corresponding expression uses C.
The modulus16q and strict interval thresholds in that program are correct.
Both target signs and all four compatible charts are represented. A common
phase denominator q gives a complete M period; negative integers add no
new residues. The alpha,beta to depth conversion is bijective for
0<alpha<beta<1: a/g=alpha/(beta-alpha), b/g=(1-beta)/(beta-alpha).
The primitive phase-triple iteration through q40 has exactly8410triples.
This verifies the meaning of that bound, not its relevance to larger q.

My separate Fraction-based checker evaluates ONLY the14reported negative
rows. It evaluates all1240chart/sign/period combinations, including strict
boundary failures, and confirms no vertical-only path for those rows using
the previously hand-proved chart completeness. It imports no peer code,
executes no peer writer and performs no replacement-trajectory search.
I did not rerun the full8410pair positive/negative classification; absence
of omitted failure edges in that sweep rests on the inspected peer program.

The recorded graph has no rectangle. Its14edges have b/g=1 except for
(a/g,b/g)=(1,2). Only the a/g=1 row has two neighbors. Thus two distinct
a rows cannot share two distinct b values. The independent checker also
checks every pair of recorded neighbor sets. This is a finite graph fact;
it cannot exclude a rectangle among depth pairs absent from that graph.

The proposed rectangle implication is valid: take failures at
(a,b),(A,b),(a,B),(A,B), with A>a>0 and B>b>0. Set
h_-=(a+A)/2 and h_+=(b+B)/2. The original marks satisfy
0<a<h_- and0<b<h_+. The four single-endpoint cap sheets have exactly
those effective depth pairs, so all four fail their portal conditions
before any cap-corner issue arises. This would refute the sufficiency of
that particular four-sheet mechanism. It would exclude neither additional
cap repetitions nor other reflection words, and would not prove darkness.
Conversely, absence of such a rectangle does not by itself prove a
physical four-sheet cover: a portal-successful sheet might hit a cap corner.
Any universal finite-cyclic proof must address these extra exclusions.

No correction is required to the bounded controls or the stated mechanism
implication. A fully rational theorem with unbounded denominators remains
open. Reproduce this scoped validation with:

    python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/rational-controls-review.py
