**[Guessed] Best bet: A, expanded to several independent winding parameters and exact arithmetic failure conditions.** I would pursue a complete \(r=3\) theorem first. My subjective probability that this develops into the full orthogonal result is **10%**.

Labels: **[Proved]** means an elementary deduction given below; **[Cited]** means supported by the supplied notes, without independent verification; **[Guessed]** includes proposals and judgments.

**[Cited] One correction:** d16 states a complete real-to-rational reduction. Its surviving one-parameter families contain rational dark pairs. Thus excluding these families separately is unnecessary if illumination of *all rational pairs* is established.

1. **A — salvageable; strongest candidate.**

   **[Proved]** Openness alone does not give the proposed finite cover: normalized strictly simple rooms form a nonclosed parameter domain, and thin corridors, corner collisions, and endpoint degenerations occur at its boundary.

   **[Guessed]** A single repeated core \(w_0c^nw_1\) is too restrictive. Use templates
   \[
   w_0c_1^{n_1}w_1\cdots c_m^{n_m}w_m,
   \]
   with independent integer winding parameters. The useful output is an exact description of each template’s failure set, followed by incompatibility of *simultaneous* failures.

   **[Cited]** d17’s door lemma already supplies precisely this kind of arithmetic obstruction. **[Guessed]** Start with the two-width U-shaped chains; proving incompatible resonance conditions there would be more informative than adding many isolated word certificates.

2. **B — dead for the stated generators and principal target.**

   **[Cited]** d16 explicitly constructs horizontal and vertical multi-twists fixing every lattice lift pointwise. Consequently, their action on lattice lift pairs has singleton orbits.

   **[Proved]** A singleton orbit cannot expand into a visibility region it initially misses. Moreover, darkness of a room pair is not preserved as one room pair under these twists: reflection classes separate.

   **[Guessed]** Using the full affine group might revive an orbit-hitting question, but first one needs a theorem guaranteeing useful motion of the marked pair. Expansion cannot substitute for that missing hypothesis.

3. **C — dead as stated; salvageable only with sheet-sensitive counting.**

   **[Cited]** d24 identifies an obstruction independent of vertex interception: a projected segment can avoid every vertex and terminate on the wrong lift.

   **[Proved]** Counting all planar target images therefore counts candidates that need not realize the desired endpoint upstairs.

   **[Guessed]** A viable replacement would estimate the number of *correct-sheet* primitive segments from below, then subtract corner interceptions. That lower bound is the difficult theorem, not a routine density estimate. Surface-averaged counting would not automatically control every exceptional lattice room.

4. **D — salvageable as a boundary transfer method, not ordinary induction.**

   **[Proved]** Cutting introduces artificial reflecting walls. A billiard path proved inside a piece may reflect at the cut and fail to be a path in the original room.

   **[Guessed]** The inductive object must record door position **and direction**, with transmission through the door. Seek a class of transfer relations closed under gluing, retaining winding numbers. Endpoint illumination alone discards the compatibility information needed for induction.

Two additional ideas:

**I. Low-rank commutator obstruction with reflection symmetry.**

- **Key statement — [Guessed]:** On an orthogonal room unfolding, darkness between entire Klein-group endpoint orbits forces at least nine independent reflex-corner contributions to the failure of horizontal and vertical transport to commute.
- **Why plausible — [Proved]:** For the square-tiled unfolding, the commutator of horizontal and vertical square permutations has one 3-cycle per reflex corner. On the permutation vector space,
  \[
  \operatorname{rank}(HVH^{-1}V^{-1}-I)=2r.
  \]
  Thus area increases the representation dimension but not this defect rank. Convex corner blockers must be retained separately.
- **First lemma — [Guessed]:** Express primitive-segment transport through Christoffel cutting words, including endpoint sectors and corner absorption, then derive a rank obstruction from vanishing transport to all four target lifts. Arbitrary permutation words are inadmissible substitutes.
- **Cheap kill — [Guessed]:** Check the proposed linear-algebra lemma against the saved 22-wall example and elementary rectangle/L-room permutation descriptions. Kill it if it assumes that group reachability implies straight-segment reachability.

**[Guessed]** This is a different monodromy attack: exploit small commutator rank and the planar reflection structure, without proving same-fibre classification or classifying braid orbits.

**II. Intersection obstruction for the four dark correspondences.**

- **Key statement — [Guessed]:** A room’s four homogeneous dark correspondences cannot share the required real arc when \(r\le8\).
- **Why plausible — [Cited]:** d24 permits each correspondence separately but leaves their simultaneous compatibility with the disc quotient unresolved. Abstract dark correspondences are real phenomena; [LMW](https://msp.org/gt/2016/20-3/gt-v20-n3-p11-s.pdf) supplies examples.
- **First lemma — [Guessed]:** Handle \(|a|=|b|=1\) when the components are graphs of translation automorphisms. Translate common-arc compatibility into relations with the two reflections, then constrain their fixed loci.
- **Cheap kill — [Guessed]:** Test those relations symbolically on d24’s finite-group examples. If the proposed obstruction ignores whether the reflection quotient is a disc, discard it.
- **Scope — [Guessed]:** Useful structural progress, but unlikely by itself to settle isolated rational dark pairs.

**Next move — [Guessed]:** Derive one exact, two-door transfer relation for d17’s two-width U-chain and determine whether its winding families have a nonempty simultaneous failure set.