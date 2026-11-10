# New illumination mechanisms: working synthesis

[done] Prior result: the canonical 45-degree family with distinct interior A marks and at most three B/C exceptions has minimum 24 walls. This is a restricted-family computer-assisted result, not a general polygon theorem. See ../three-triples/three-exception-complete.md.

[done] Opus challenge consultation completed; verbatim final response is in opus-challenge.md. Both read-only Opus consultations completed; the broader response is in opus-first-pass.md. No proposed new room has been constructed.

## Strongest distinct proposal: midpoint avoidance with one source star

Opus's first pass proposes keeping an interior A source S and placing T at an interior tile-edge midpoint, outside the source's full eight-triangle star. Keep k=0: every B/C vertex is an absorbing physical corner. This escapes the earlier two-A-mark hypothesis and needs only one full A star. It is a candidate construction mechanism; no dark example is known from this work.

The all-ray reduction is elementary. In unfolded integer coordinates with S=(0,0), a primitive integer direction (a,b) reaches its first subsequent lattice vertex at(a,b). That vertex cannot be A because a,b are not both even, so its physical image is a blocking B/C corner. A half-lattice point not on the integer lattice can occur before that endpoint only at parameter1/2: if2ta and2tb are integers and gcd(a,b)=1, then2t is an integer. Irrational directions cannot reach a rational target lift. Consequently, an interior edge midpoint T is illuminated exactly when it is the physical image of the halfway point of one of these primitive source-to-corner paths. Other reflections do not invalidate this reasoning because the canonical reflection tiling preserves the vertex classes and half-lattice.

This changes the design problem: build a pocket whose midpoint is absent from that entire midpoint image set. The source is still a vertex of the tiling, but the target is not. The old count W=2+6I+Q now has I>=1, not I>=2; with exactly one full A star it becomes W=8+Q. The connected-cell bound supplies W>=12. These inequalities leave room under24; they do not predict a dark midpoint.

The cheap falsification test is to generate strict one-source rooms, select interior edge midpoints outside the source star, and look for exact positive paths. Every verified path rejects that candidate. Any finite direction miss remains unresolved. The potential fatal failure is that every such midpoint is illuminated, possibly because affine symmetries act transitively on the relevant midpoint classes. A theorem of that form would kill this branch more effectively than a larger direction sweep.

The first5-cell pilot checked16 rooms/31 target midpoints: all31 have independently checked positive paths. The13-cell follow-up sampled20 distinct configurations, all with23 walls, and280 target midpoints. All280 have exact positive paths checked by the separate segment/reflection verifier. Four initial misses at direction bound8 were illuminated on refinement through bound32. A fresh audit independently recomputed connectedness, single-fan vertices, Euler characteristic1, strict B/C status, the unique interior A source, wall count, and target edge membership. This bounded sample is not complete over the family and has not produced a dark candidate. Rooms can be symmetry-equivalent; the280 figure counts room/target instances. Reproduce the audit with `.context/illumination-venv/bin/python .context/illumination-new-mechanisms/midpoint-pilot.py --audit` without rerunning the search.

## Other proposals and their limits

Selective blocking of reflected target classes remains a broader alternative: some blocker preimages can remain regular and traversable, provided a direction-coherent invariant proves they cannot connect any physical source to any target lift. Coordinated multi-corner surgery on the24-wall room is one possible realization. Four exceptions alone give no new obstruction; the missing proof is a closed invariant for transmitted trajectories.

Opus also proposed an orthogonal room with enough deck translations to produce four useful half-turns, rather than the eight needed in the45-degree setting. This still needs a simple planar quotient with automorphisms that exchange distinct physical marks and have entirely absorbing fixed sets. No such room or small positive realization was supplied. Existing involution pilots already tested the key realization difficulty, so this is lower priority.

The first-pass assertion that all dark pairs are either involution-type or arithmetic is not established here. Its broad recollection about periodic points and hyperelliptic involutions is not used.

## Strict triangle route has a small no-go argument

Assume a connected, label-preserving, edge-to-edge assembly of congruent triangles, angle A=pi/n, even n, with at least two full A stars. Every B/C point is a genuine boundary corner; only A may be interior or smooth boundary. Let N be tile count, I full A stars, S smooth A vertices. Euler and A incidence give

    W=N-2I+2-S; N>=2nI+nS.

Therefore W>=(1-1/n)N+2>=4n-2. For n>=8 this is at least30.

For right triangles, each full A star forces n right-vertex two-tile fans, each requiring a third tile; no two full A stars can supply each other's third tile because that would fill all four right sectors. Hence N>=3nI. Combining with S<=N/n-2I gives W>=(1-1/n)N+2>=6n-4, so n=6 needs at least32 walls. These are necessary lower bounds, not attainable constructions. Opus called the direct N-to-W step a gap, but the already-stated S-incidence bound supplies the missing algebra. Its proposed stronger smooth-star count is not needed or relied on.

For n=6, the only non-right option up to swapping B/C is 30-30-120. Every full A star has only BC boundary edges; its C endpoints already contain two120-degree sectors. Any neighboring triangle across BC adds the third120-degree sector, making C interior, contrary to strictness. Thus a full A star is an isolated tile component, ruling out two in a connected strict assembly. Opus independently reached this local obstruction. Its additional claim about swapping equal-angle labels reducing to a right half-triangle is not used.

For n=4 the triangle is45-45-90. Thus within these strict assumptions, changing the basic no-return triangle cannot give a new sub24 family. Transparent exceptions, other assemblies, and other blocking mechanisms are outside this argument.

## Torus-cover construction and realization gates

An exact S3 enumeration finds90 transitive monodromy assignments for a degree3 torus cover, fully ramified over the three nonzero2-torsion points. Each branch cycle is a3-cycle; Riemann-Hurwitz gives genus4. Every torus return from0 has a primitive first piece whose midpoint is nonzero2-torsion, so any two distinct regular lifts of0 are blocked on the abstract surface. This is known torus-cover blocking published context, not a new mechanism or a planar room.

If a torus projection is equivariant for the full billiard dihedral action and0 is fixed on the base, two distinct interior physical marks require two free group orbits in that fiber. Therefore degree>=8 for D2 and>=16 for D4. The degree3 example fails this necessary realization condition.

In the standard orthogonal equivariant setting, corners map to2-torsion, convex corners have local degree1, and reflex corners degree3. If all preimages of the three nonzero2-torsion points are genuinely ramified, their total degree requires d reflex corners. With r0 further reflex corners at0, the disk angle sum demands c=d+r0+4 convex corners; only d-3r0 regular slots remain over0. The deficit4r0+4 excludes this full-ramification scheme. It does not exclude selective blocking or all mirror rooms.

More generally, under the stated D2/D4-equivariant rectangular-torus projection, every physical corner image lies in T[2]. A universal fixed1/n-time blocker set is a coset of T[n], containing n^2 points. It fits in T[2] only when n divides2. Third-point and higher-fraction universal fiber schemes therefore face a location obstruction; selective itinerary-dependent blocking escapes this particular premise. The finite residue check in mechanism-probe.py illustrates the exact torsion argument; it is not a search over rooms.

## Opus's strongest challenge proposal is not a fresh mechanism

Opus proposed computing the affine symmetry group preserving source, target, and absorbing-corner labels, then checking one direction per cusp (rational-direction orbit). This is a sound conditional finite-decision framework if the labeled orbit/group calculation is complete. Rational coordinates must be tracked, regular absorbing corners preserved, every reflected target lift checked, and trajectories on cylinder boundaries included. Also, the first pass calls Visit(v) finite on rational points, which is false without fixing a denominator: even a finite segment contains infinitely many rational points. Fix target denominator q and refine the grid, or preserve the actual target set as in the challenge response. It overlaps the Tan modular-orbit/permutation-pair approach already tried here; that attempt stopped at20000 processed states with UNKNOWN. A better group computation might help verification, but no improved compression or constructive reason for a smaller room has been supplied. Do not label this a new physical mechanism.

[waiting on Claude] Independent review of the new strict-triangle and conditional realization deductions can use mechanism-probe.py and this derivation. The probe is an arithmetic consistency check, not an independent geometric proof.

## Current judgment

[done] Two Opus consultations, primary-source checks, arithmetic probes, and the bounded midpoint pilot are complete. No smaller dark room or new all-ray certificate was found. The most distinct construction branch is one-source midpoint avoidance; the pilot gives unfavorable evidence for its smallest pockets, while leaving the general mechanism open. Its next useful target is a structural reachability criterion or obstruction, rather than a larger unstructured geometry sweep.

**Next move:** ask whether every interior edge midpoint is illuminated from the unique interior A source in a strict simple assembly; prove this or identify a concrete invariant that separates a pocket midpoint.
