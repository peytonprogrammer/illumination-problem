# d59: strategy memo for the lit side at W <= 20

Date: 2026-11-18. Strategist pass, not a proof attempt. Tags: **PROVED**
(argument here or in a cited project file), **CITED** (published, statement
read at source or abstract this session), **COMPUTED** (exact check in this
directory, named rooms only), **GUESSED** (judgment).

## Answer

- **Literature.** Nothing published since 2015 applies to genus-0 doubles of
  lattice rooms with two marked points. Every illumination and marked-point
  classification theorem either excludes torus covers or concerns
  closed-orbit structure that carries no information here (section 1).
- **Candidates (a) to (d).** (a) survives only as the known d35 reformulation;
  its "few directions, uniform certificate" form is dead. (b) is dead. (c) is a
  restatement whose compactness step fails at dark degenerate rooms. (d) is
  dead for lattice rooms (section 2).
- **Own ideas.** A Farey-triangle coherence lemma (discrete Apisa-Wright) is
  falsified in its local form by r20a, a lit W = 20 room. "Darkness is
  arithmetic, so real-parameter limits can't reach it" is a diagnostic that
  re-ranks the programme (section 3).
- **Ranking.** 1: the tower (imprimitive) branch of the d12/d14 group route.
  2: the corridor-face programme of d57/d58, for the real-length target.
  3: a side route to a publishable incommensurable theorem (section 4).
- **Assessment.** About 5% that the lattice target at W <= 20 is provable with
  current tools in the next few rounds (GUESSED). A publishable intermediate
  paper exists now: "fold-certified darkness needs W >= 22" plus the W <= 8
  theorem, the generic-length theorem, and the census (section 5).

## New computations (COMPUTED, named rooms only, total under 15 CPU s)

| Script | What it checks | Result |
| --- | --- | --- |
| `axis_twist.py` | Orbits of axis-cylinder certificates under the horizontal and vertical multitwists of DP | R22 and P6 pairs not certified (controls pass). r20a pair (1,3)-(3,5) not certified; both multitwists fix every class point of r20a and R22. dumb12 has 3 uncertified interior pairs. |
| `lattice_trace.py` | Exact lattice-step tracer; lighting directions with \|p\|, \|q\| <= 15 | R22: 0 directions (control passes). r20a: 14 directions, the shortest has \|p\| + \|q\| = 11, for example (-6,-5) and (-4,7), each 2 lattice steps. |
| `cyl_cert.py` | Whether S lies on a closed regular leaf in each lighting direction | r20a: the 12 shortest lighting directions run along saddle connections (the leaf through S meets a corner). The first same-leaf cylinder certificate is (14,11), height 25. |
| `mt_named.py` | d14's point group M_t and cusp group N on the named rooms | R22, cross12 (2 classes), dumb12 (2 classes): G is imprimitive in all of them. M_t has 2 or 3 orbits on pairs in every case. r20a: the plain braid orbit exceeds 200,000 states; stopped. |

Consequence: every named room at or near the threshold, lit or dark, has an
imprimitive monodromy group (P6 by d30/d36: a 4-fold cover of the staircase
double, CITED; r20a not determined). The primitive branch of the group route (d14
Theorem R) covers none of them.

## 1. Literature

Searches used generic mathematical terms only.

| Paper | Statement | Applies to lattice-room doubles with two marks? |
| --- | --- | --- |
| Lelievre, Monteil, Weiss, "Everything is illuminated", Geom. Topol. 20 (2016), arXiv 1407.2975 | A translation surface is a torus cover iff every pair of non-singular points is finitely blocked. For each point, finitely many points are not illuminated from it. (CITED) | No. Finiteness only; says nothing about which pairs. |
| Apisa, Wright, "Marked points on translation surfaces", Geom. Topol. 25 (2021), arXiv 1708.03411 | Thm 1.3: off torus-cover loci, irreducible markings come from half-translation covers or periodic points. Thm 1.4: periodic points over generic quadratic strata are J-fixed points. (CITED) | No. Excludes torus covers explicitly; d35 shows why the proof needs a finite periodic set. Used in d18 for non-lattice rooms. |
| Wolecki, "Illumination in rational billiards", arXiv 1905.09358, v3 30 Nov 2024 ("correcting a technical gap") | Finitely many non-illuminating pairs in a rational polygon. Thm 1.3: the minimal number of edges of a polygon with a non-illuminating pair is at most 22 (Monteil's unpublished 22-gon). Tokarsky 26, Castro 24 cited. (CITED) | Finiteness yes. No lower bound; 22 is an upper bound only. |
| Apisa, "GL2R-invariant measures in marked strata", Geom. Topol. 24 (2020), arXiv 1601.07894 | Invariant point markings over components of Abelian strata exist only in hyperelliptic components (Weierstrass points or J-swapped pairs). Finite blocking solved for dense-orbit surfaces. (CITED, abstract) | No. Lattice-room surfaces have closed orbits. |
| Apisa, Wright, "High rank invariant subvarieties", arXiv 2102.06567 | Rank >= g/2 + 1 implies a stratum component or a locus of holonomy double covers. (CITED, abstract) | Only to non-lattice rooms of high rank (route 3). |
| Apisa, Wright, "Generalizations of the Eierlegende-Wollmilchsau", arXiv 2011.09452 | Classification of geminal orbit closures that are not torus covers. (CITED, abstract) | No. |
| Duryev, "Teichmuller curves in genus two: square-tiled surfaces and modular curves", Geom. Topol. 28 (2024), arXiv 1905.09312 | Illumination conjecture for X(d) (cusp light sources) proved for d <= 5; fails at a vertex of X(5). (CITED; d27 read the PDF) | No statement transfers. Best methodological analogue: orbit classification plus cylinder "lighthouse" arguments. |
| Jeffreys, Matheus, arXiv 2602.21984 (Feb 2026) | Euler characteristics of SL(2,Z)-orbit graphs of origamis in H(2) and Prym loci grow without bound. (CITED, abstract) | No marked points. No. |
| Hubert, Schmoll, Troubetzkoy, IMRN 2008, arXiv math/0602394 | Non-illuminable sets finite on Veech surfaces; finitely many invariant subspaces only for non-arithmetic surfaces. (CITED via d27) | No. Arithmetic case has infinitely many. |

Effective bounds on the length of an illuminating trajectory: nothing found.
Orbit classification of marked square-tiled surfaces in genus-0 pillowcase
strata: nothing found (consistent with d12 and d27). **Nothing applies.**

## 2. The four coordinator candidates

### (a) Arithmetic route: few directions, certificate uniform in side lengths

**Verdict: dead in the stated form. The reformulation is correct but already d35.**

1. Lit iff some primitive direction carries a lift of S to a lift of T before a
   corner. That's d35.3 (refereed in d38). The SL(2,Z)-orbit is finite per
   room, so illumination is decidable per room. PROVED, known.
2. "A few directions" can't work. Lemma U (d57, PROVED) needs
   2 sqrt(dh/(Hw)) - 2 reflections; scaling makes it apply to lattice rooms with
   long arms. Even without degeneration, r20a (area 14, W = 20) has no lighting
   direction with |p| + |q| <= 10 (COMPUTED).
3. Axis cusps don't help. Horizontal and vertical multitwists fix every
   class point of r20a and R22, and axis-cylinder certificates plus those twists
   miss lit pairs in r20a and dumb12 (COMPUTED). So "cylinder decompositions in
   horizontal, vertical, diagonals" needs the full Veech group. That brings back
   the handle problem of d14.
4. Structural reading (PROVED from Lemma P of d58): the resonance
   n = L h / (w D) in Z says the channel and corridor cylinders have moduli in
   integer ratio, so the twist family of directions collapses to one lasso
   monodromy. On a square-tiled surface every direction is parabolic, so
   Kronecker density is never available. Resonance is the generic state.

What survives: twist families with length-dependent base slopes (Lemma H, P,
E), which are route 2.

**W = 22.** R22 has 0 lighting directions (COMPUTED to height 15; proved dark by
d10 certificates), so any certificate fails there automatically. The route
offers no reason why W <= 20 differs.

### (b) Surgery induction on r

**Verdict: dead.**

- R22 is r20a plus one cell (d41). One bump turns the lit W = 20 pair into the
  dark W = 22 pair. The inductive step must know r, and nothing in a local
  surgery sees r. PROVED (by example).
- No persistence mechanism exists. Lighting paths are global objects of
  unbounded length (Lemma U). A bump cell meets infinitely many of them. The
  r20a witnesses are saddle connections (COMPUTED), which a new corner can cut.
- The thin-bump limit is a slit room. Slit rooms are dark below 22 walls
  (Monteil 19/20 sides; d55), so a degeneration argument meets real darkness.

### (c) Effective illumination bound plus compactness

**Verdict: restatement. Compactness fails at the faces.**

- Per room, an effective bound already exists. The Veech group of the marked
  surface has finitely many cusp classes, so a lit pair is lit in one of
  finitely many direction classes. The census uses this. PROVED, nothing new.
- A bound f(r, aspect data) on a compact core is equivalent to "all lit on
  the core". Lit is open (strict inequalities per itinerary), so a finite
  subcover gives the bound, and conversely. PROVED. So (c) adds no content.
- Compactness fails at the ends. Limits as w -> 0 are slit and pinched rooms,
  some dark at W < 22. Darkness is closed, so dark limits don't contradict
  anything. The face theorem near dark degenerate rooms is d57/d58's open
  problem.
- At W = 22 the bound is infinite at the dark room: 307 nearby itineraries fail
  there (d57 sanity). So f must blow up at R22, and the route must explain why it
  can't blow up at W <= 20. It doesn't.

### (d) Orbit-closure route

**Verdict: dead for lattice rooms.**

- With rational marks, the SL(2,R)-orbit of the marked surface is closed (a
  Teichmuller curve). The orbit closure contains no new surface. PROVED
  (rational points are periodic; d35.2, d38).
- Cusps of an arithmetic Teichmuller curve are fully degenerate. Every
  direction is completely periodic, and g_t pinches all cylinders of that
  direction at once. No boundary surface keeps a flat structure with the
  marks, so no limit room exists in which to refute darkness. PROVED (standard).
- Darkness is closed under limits (lit is open). That's correct but useless
  here, because the closure adds nothing.
- Off lattices this is Apisa-Wright, already used: d18 Theorem B (generic
  lengths lit) and Theorem C. Marked torus covers have infinitely many
  irreducible markings (AW), which is the SL(2,Z)-orbit problem again.
- W = 22: the dark pair is a torsion pair on its own Teichmuller curve.
  Nothing in (d) distinguishes it.

## 3. Own ideas

### Idea 1: Farey-triangle coherence (discrete Apisa-Wright)

Setting (PROVED). A Farey triangle {v1, v2, v1 + v2} has one slope in each
non-A parity class. On the pillowcase it is three disjoint arcs from pole A to
b, c, d. Their lasso monodromies satisfy g_A h_b h_c h_d = 1. Adjacent
triangles differ by one half-twist. This is the discrete replacement for
Apisa-Wright's continuously moving points. It couples the three classes by a
product relation, which d35's 12|34 vs 13|24 counterexample lacks.

Local lemma proposed: "dark in a triangle and its three neighbours implies a
certificate". **FALSIFIED (COMPUTED).** The r20a pair is lit, so it has no
certificate. It has no lighting direction with |p| + |q| <= 10. So the
triangle (1,0), (0,1), (1,1) and its three neighbours are all dark for it.

What remains is the global form: "dark on the whole Farey graph implies a
certificate". That's the target. Keep the triangle language only as notation
for route 1. It doesn't give a new lemma.

### Idea 2: darkness at lattice rooms is arithmetic, so it can't be reached by limits

Claim (argument from d10 and d38 data; the step "the deformed cover is still
a room" is GUESSED). R22's certificate is Par
over the unit pillowcase B. Its fold-back step uses "odd lattice points along
a primitive lattice segment map to poles". Real deformations of the factor N
(the staircase double) keep the cover but destroy the lattice. Geodesics
from phi(S) then miss the poles, and nothing folds back. The 2% perturbations
of d57 light the pair (COMPUTED there). So the dark set of a type region,
which is closed, meets lattice rooms in isolated arithmetic points. It isn't
the closure of non-lattice dark pairs.

Consequences for strategy (GUESSED, with reasons):

- The real-length target is strictly harder than the lattice target. Route 2
  must prove lit at every resonance, including resonances that aren't lattice
  rooms.
- No limit or compactness argument from the generic theorem (d18 B) can
  reach the lattice case. Candidates (c) and (d) die for this reason.
- The lattice case needs an existential, per-room argument (group or orbit),
  which Lemma U doesn't touch. Lemma U bounds witness length, not existence.
  That's why route 1 ranks first, despite its difficulty.

## 4. Ranked routes

### Route 1: the tower branch of the group route (d12, d14), with the census

**Key lemma (FH\*, relative completeness).** Let DP -> N -> B be a factor with
N minimal above DP (block system of G). If no Par, Cut, or Rig certificate over
any pillowcase separates the pair, and the images are lit in N or equal, then
some lift of the lighting lasso of N joins lifts of S and T in DP.
Induction runs up the block lattice. The primitive top uses d14 Theorem R
(n > 64, conditional on Lemma H). Small n uses the census.

**Why it might hold.** The fold side is closed at W <= 20 (d46, d52). Every
known dark pair is certified. Certificates are exactly block-system
obstructions. d14 Lemma H holds on 1,643 of 1,643 tested primitive orbits.
The route is existential, so Lemma U doesn't bite.

**Most likely failure.** Non-transitivity of "lit". Cut certificates (the
12-wall cross) show a class can be dark inside one block fibre. The lifting
step must then combine classes. Two further gaps:

- Lemma H is a connectedness statement about handles of the Hurwitz curve
  (d14 section 1.7).
- The census covers area <= 20 at W <= 21, not n <= 64 for primitive G.

**New fact for this route (COMPUTED; P6 CITED).** Every named room (R22, P6,
cross12, dumb12) has an imprimitive G and M_t with 2 or 3 orbits on pairs. So FH\*, not
Lemma H, carries the hard cases.

**W = 22.** R22 is imprimitive (B_b = B_d, 5 blocks, degree 3 over the
staircase double). FH\* has a certificate hypothesis, and R22 has a Par
certificate at r = 9, the first r where one exists (d52). So the route
predicts darkness exactly there.

**First test (under one round).** Use `marked_orbit` from d6 on the induced
tuples of each factor N of cross12 and dumb12 (both classes), and of R22. For
every pair whose images are lit in N, check that a lift of an N-witness lights
the pair in DP. This is the lift-or-certify dichotomy, level by level. Exact,
named rooms only, seconds of CPU (the d38 tuples are tiny). A lit-in-N pair
with no lifted witness and no certificate falsifies FH\* as stated. Skip r20a:
its plain orbit exceeds 200,000 states.

### Route 2: corridor faces and resonance for real lengths (d57, d58)

**Key lemma (no exceptional set).** For each door and chain configuration, the
exceptional sets of the available families (H, E, B, BE, K) have empty common
intersection inside the type region.

**Why it might hold.** Every double-resonance instance was lit by a short
chimney or back-wall path (d58, 10 of 10). Families add independent
integrality conditions.

**Most likely failure.** Chains through non-full strips fail on open sets of
lengths (d58), and the 553 chain pairs at r = 3 have no lemma. Each r needs its
own case analysis, so W <= 20 means r = 3 to 8 by hand. Idea 2 says this
proves more than needed.

**W = 22.** Lemma H's hypothesis 2 fails at R22 in all 16 frame-order cases
(d58 `check22.py`). Any complete family list must also fail there.

**First test.** Count, over the 553 chain pairs, the routes whose every strip
is a full channel (Lemma K's hypothesis). This is combinatorics on position
types from `kinds_r3.tsv`, not a search. If fewer than half qualify, the
route is not viable at r = 3, let alone r = 8.

### Route 3 (side route): the incommensurable theorem

**Key lemma.** Every non-torus-cover orthogonal room with W <= 20 has
orbit-closure rank at least g/2 + 1 = (r + 3)/2, or its dark pairs are folds.
Then Apisa-Wright (high rank, then marked points Thm 1.4) leave only folds,
which the fold side excludes.

**Why it might hold.** d18 Theorem C already confines dark pairs to E x E or
fold lines, and the fold lines vanish when a + b >= r + 3.

**Most likely failure.** Low rank. Rooms with lengths in Q + Q sqrt 2 have
a = b = 2 and may have rank-2 orbit closures (eigenform-type loci) with extra
periodic points. Non-arithmetic Veech orthogonal rooms are possible dark
candidates at W < 22 that the lattice target never sees (GUESSED).

**W = 22.** The route says nothing about lattice rooms, so R22 is out of scope.
It doesn't advance the main target. It yields a clean published-tools theorem.

**First test.** Theory check, one round. For a+b = 3 or 4, bound the rank of
the orbit closure from below by Wright's cylinder deformation theorem applied
to the horizontal and vertical cylinders of a concrete low-r room. Or produce
an orthogonal Veech room with W <= 20, which would show low rank occurs.

## 5. Overall assessment

- Lattice target at W <= 20 with current tools: about 5% (GUESSED). Every
  route reduces to one of two open statements: Lemma H plus FH\* (group), or
  "exceptional sets have empty intersection" (geometry). Neither has a
  mechanism that uses r <= 8 quantitatively, except the fold side, which is
  done.
- A conditional theorem (the target, assuming Lemma H and FH\*, plus a
  census for primitive n <= 64): about 15% in a few rounds (GUESSED).

Publishable now, as one paper, all proved or computer-assisted with stated
scope:

1. Fold-certified darkness needs W >= 22. At r = 9 the only triply
   Par-certified room is R22 (d46, d52, d54, d56).
2. Every pair is lit at W <= 8 for all real lengths (d15, reviewed).
3. Every pair is lit for Lebesgue-almost every side lengths at every W
   (d18 Theorem B). This is a corollary of Apisa-Wright and Mirzakhani-Wright.
4. Census: no dark pair at W <= 21 to area 20 (d9, d29).

"W <= 12" isn't realistic: W = 10 is open with 578 pair types and no chain
lemma. "Generic side lengths" is already item 3. "Fold-certified only" is item 1.

## Files

| File | Purpose |
| --- | --- |
| `axis_twist.py`, `axis_twist.json` | Axis multitwists, axis-cylinder certificates, orbit closure |
| `lattice_trace.py`, `lattice_trace.json` | Exact lattice-step tracer and lighting directions to height 15 |
| `cyl_cert.py`, `cyl_cert.json` | Closed-leaf test for lighting directions |
| `mt_named.py`, `mt_named.json` | Primitivity of G, M_t and cusp-group orbits on named rooms |

Run each with `python3 -B <script>` from this directory. They read d6, d10,
d14, d31, d41 files read-only.
