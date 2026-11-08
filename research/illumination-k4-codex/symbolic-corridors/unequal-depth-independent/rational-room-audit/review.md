# Fixed rational-room cap-cover audit

Codex01a1a00f, 6 November 2026.

Result: an internally verified, complete continuous four-cap-sheet cover for
ONE prescribed normalized rational room. Peer review is requested before
promoting this new local certificate to an independently accepted theorem.
It does not settle the full unbounded commensurable class.

## Exact candidate statement

Set d=g=1, a=1/2,b=1,h_-=3/4,h_+=5/4. For every real
0<s,t<=1, at least one of the original/lower-cap/upper-cap/both-cap
sheets has a legal strict four-chart connection avoiding cap corners.
Every such successful sheet gives an actual finite path by the already
audited cap-sheet folding lemma, truncated at first actual T if needed.
For either s>1 or t>1, the already accepted actual-mirror L reduction
applies. Thus the proposed local theorem covers every allowed horizontal
outer pair0<s,t<2 at these fixed vertical parameters.

Positive independent coordinate scaling would also give every d,g>0 with
 a=g/2,b=g,h_-=3g/4,h_+=5g/4. No other vertical parameter is varied
by this audit. The full ENDPOINT SQUARE0<s<=1,0<t<=1 is used: ordering
s,t at fixed unequal a,b would be an invalid case reduction unless depths
and caps were swapped too.

## Finite family enumeration

The four effective depth pairs use A=a or2h_--a and B=b or2h_+-b,
with H=A+1+B. A fixed u,c,epsilon,M has portal affine values
 E1=(1-alpha)s+alpha*epsilon*t+alpha*(u+4M), alpha=A/H,
 E2=(1-beta)s+beta*epsilon*t+beta*(u+4M), beta=(A+1)/H.
Strict portal boxes give four affine inequalities after exact period
translation. Interval extrema on the closed square enumerate every box
translate capable of meeting it; clauses with no open feasible region
are discarded by exact polygon clipping and strict centroid evaluation.
A strictly feasible point on a square boundary always has strictly feasible
points in the square interior nearby, so this discards no isolated legal
boundary success.

Complete arithmetic M periods, including selected cap times, are respectively
5,12,12,14 for sheets(0,0),(0,1),(1,0),(1,1). These periods follow by
clearing denominators of A/H,(A+1)/H and selected cap-flight fractions.
M->M+Q changes each relevant coordinate by a multiple of4, preserving
both portal residues modulo4 and cap-corner residues modulo2. Thus no
signed integer M outside the enumerated period has a new phase outcome.
For this POSITIVE cover result, however, completeness of enumeration is
not even required: a valid subset that covers the square is sufficient.

For a selected cap with time gamma, the developed cap coordinate is
(1-gamma)s+gamma*epsilon*t+gamma*(u+4M), subtracting upper shift u
when needed. Its even-integer values are the forbidden cap/side corners.
All intersecting affine zero lines are retained; corners are not treated
as permissible limits. Thirty-four valid clauses survive.

## Continuous coverage and independent physical validation

The first program audit.py decomposes the square by all retained guard and
locally relevant cap-corner lines. It checks every open face, open edge and
vertex, excluding only s=0 or t=0 as required by interior marks. Every
affine expression has constant sign on each such relative cell, so one
representative per cell is a COMPLETE continuous proof, not sampling.
It finds68lines,257open faces and948admissible relative-cell representatives,
with no uncovered cell.

The separate reproducible verifier verify.py does not trust those exclusions.
It rederives every listed clause's four portal guards directly from its
physical sheet and target lift. It reconstructs ALL possible cap-corner
zero lines over the ENTIRE square, including lines omitted as locally
irrelevant in the first run. It uses the separately audited own polygon
clipping implementation, creating69lines,272open faces and1,006admissible
relative-cell representatives. Every cell is covered. For each representative
it builds a full physical path using the own independent cap-fold constructor,
then checks it against all actual polygon edges for first contacts,
strict mirror interiors, boundary nonoverlap, positive specular directions,
actual endpoints and first target arrival. All1,006paths and4,405wall
contacts pass. The recorded witnesses use7different prescribed formulas.
No early-target truncation was needed at these representatives, but the
universal cap lemma permits truncation wherever it is needed between them.
First-arrival pattern constancy is not assumed for the continuous proof.

Run the long-term reproducible verification:
`python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/rational-room-audit/verify.py`.
It reads the saved finite certificate and executes no peer writer. Unlike
the discovery/setup script, this proof verifier does not depend on an expired
search deadline. It imports only the existing own exact geometry and polygon
helpers; their source hashes and the certificate hash are saved in
verification.json.

## Effort limit, provenance and peer-review obligation

The named effort's hypothesis, exact one-room scope and aggregate840second
deadline were saved BEFORE coding in effort.json. Both the initial audit
and physical verification were supervised with the same original deadline,
using their own process groups and TERM/KILL on timeout. They ended normally;
combined setup and initial physical validation took157.31seconds. No
replacement room, timeout reset, restart sequence or agent worker was used.
No process from this effort remains running. supervisor.json and
supervisor-verify.json preserve the completed process outcomes.

This is a new local certificate produced while the peer develops the general
commensurable proof. It needs the peer's independent challenge of the guard
enumeration, cap-corner exclusions and continuous square cover. It is not
an independently accepted full-goal result, a rational-parameter sampling
argument, a valid-room census, a darkness claim, a new universal reflection
bound or a wall-minimality result. All previous frozen proof/review files
and all peer files remain unchanged.
