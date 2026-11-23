# Corner deletion on the identity cover

**Result.** The residue-labelled deletion implication for the pencils of d147 is false on DB55, a normalized BBBB room with 12 walls and four reflexes. Even allowing all four choices of physical lift pair and freely changing the power of the twist, a relaxed connection can disappear. Allowing *arbitrary* simple arcs in the same parity class is a strictly stronger repair mechanism. That implication remains open.

## Five residues suffice to decide the counterexample

Use the two closed 5-by-5 chambers [0,5]×[0,5] and [8,13]×[0,5] joined by [5,8]×[2,3]. Take S=(2,2), T=(10,2), source site a=(0,0) and target tail b=(1,0). For this tail the d147 adjacent non-source pencil pairs b with c=(1,1). Its boundary permutation h has ten 5-cycles and three fixed letters, hence order five. In the convention where i is incident to the b-cycle containing hʲi, the following table includes both physical lifts at each end.

| Power modulo five | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| Connected allowing corner continuations | 1 | 1 | 0 | 0 | 1 |
| Connected through regular points | 0 | 0 | 0 | 0 | 0 |

At zero power the horizontal segment runs from S to T along the lower corridor lip, through the reflexes (5,2) and (8,2). It is forbidden. The bottom row rules out *every* regular replacement in this pencil, including walks using different intermediate sites. The computation first uses d147's residue labels, then verifies this particular table by a second graph algorithm on the five prescribed residue slices. It closes under graph incidence for all endpoint choices, without a slope cutoff. The checker verifies all four canonical relations are universal. [Checker](deletion-check.py) · [d146 named room and quotient review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d146-review-exdescent/review.md)

## Exact deletion theorem for a single arc

Let A,D be the endpoint permutations in an adapted marking on the identity cover of an orthogonal room. Their cycles have lengths 1, 2, 3. Form the permutations U=A³ and V=D³. These retain every regular swap and fix every germ incident to a corner. On sheet labels, legal connectivity is exactly the orbit relation of ⟨U,V⟩ for regular endpoints: a change of sheet along the arc is allowed precisely across a regular two-cycle. Singletons give no move. A shortest walk in the resulting graph has no backtracking, and the degree-two continuation is straight at every intermediate vertex. For a pencil, replace V by its conjugate at the *same* power throughout.

Equivalently, for physical mark sheet sets I,J over a, a legal connection exists on that arc iff J meets (UV)ᵏ I for some integer k. Indeed I is U-invariant, and the group of two involutions consists of powers of UV and such powers followed on the input side by U. This equality applies separately to each marked arc, including arcs outside the d147 pencils. It avoids treating the whole monodromy group as a single legal trajectory.

A quantitative consequence holds without BBBB. Let z_a,z_d count the triples at the two sites. On the sheet set, deleting forbidden continuations increases the number of components by at most 2(z_a+z_d). To recover the unrestricted relation, join the three labels of each deleted triple by two edges. Each added edge merges at most two components. Convex poles cost zero because their singleton cycles never identified distinct sheets. In particular deletion invariance holds, for every arc and every marking, when both sites have no triples. The bound counts component mergers. A single merger can affect many marked pairs, so it gives no bound of two lost pairs per reflex.

BBBB means the normal closure of each local regular-swap permutation acts transitively. Its conjugates may use unrelated transport paths. It does not supply a single conjugating power that preserves earlier contacts. DB55 realizes exactly this distinction.

## The simultaneous test

Across the same two-tail pencils prescribed in d147, the named controls give the following counts. A row is a physical pair and one of its three primitive classes. A lost row connects in a relaxed pencil but in no legal pencil tested in that class. All proper factors are omitted.

| Room | Legal rows | Lost rows | No relaxed row | Physical pairs legal in at least two classes |
|---|---:|---:|---:|---:|
| DB55 | 272 | 64 | 0 | 112 / 112 |
| DBas | 196 | 38 | 9 | 81 / 81 |
| c4181s | 68 | 11 | 2 | 27 / 27 |
| U2 | 152 | 4 | 0 | 52 / 52 |

The proposed transitivity implication fails as a group inference. With multiple arcs one needs a union of cyclic orbits of the individual UV products. Transitivity gives the equivalence relation *generated* by whatever generators have been proved transitive, allowing a different generator at each step. Even transitive generators each given by a cycle can miss a particular pair in their individual orbits: on four letters take (12),(23),(34) and endpoints 1,4. This algebra example concerns the inference only. In DB55 the three products BC,BD,CD themselves generate a transitive action on all 53 sheets in the even/even marking. S,T above fail every zero-power legal arc in the three classes and every power of the b-pencil. Other powers in the other classes succeed. The checks therefore confirm simultaneous illumination on the four named controls. None tests the proposed last-class implication nonvacuously, since every pair already has at least two certified classes.

## Conditional chain and review status

1. **Reviewed in the stated scope.** Q-class closure covers the physical corner-only orthogonal branch for distinct real interior marks below 22 walls. D64/d67 and the saved replay cover the proper-canonical-factor branch for interior lattice pairs. The remaining normalized orthogonal same-parity lattice-pair problem is in BBBB. [Closure scope](../README.md)
2. **Reviewed structural reduction only.** D146 excludes proper pillowcase factors of degree 2–4 in BBBB. Projection to a larger factor can identify endpoint sheets. A relaxed connection there still needs to lift to the specified endpoint sets on the identity cover. Identity-cover deletion would start *after* this endpoint-lifting step. [d146 note](exclusion-descent.md)
3. **False for the prescribed pencils, open across arbitrary arcs of one class.** The DB55 counterexample and the component bound above are new, pending review. The cross equality under d147 review was a named-room result.
4. **Open and decisive.** For any one pair, regular reachability in a single class suffices by the reviewed arc dictionary. The claim that an unlit pair in two classes always has a regular connection in the third is already equivalent to same-parity illumination when quantified over all pairs and classes. A proof via residue closure needs a geometric hypothesis that forces a single dihedral orbit to meet both marked sets. Transitivity provides no such hypothesis. [Arc dictionary and review trail](per-class-converse.md)

The hardest step is the simultaneous one. Even granting deletion across arbitrary arcs would still require existence of at least one relaxed identity-cover connection. Conversely, proving the simultaneous statement with regular intermediates would bypass deletion altogether. The broader target additionally includes marks outside the same-parity lattice setting and mixed-wall rooms.

**Next falsifiable question.** For the three-class formulation, test a sum over three *single-arc* component relations, before taking their transitive closure: can the corner-free components through the source, taken over a geometrically prescribed triple of adapted arcs, miss both target lifts? Any positive general criterion must permit different triples for different pairs: DB55 already disproves sufficiency of the three reference arcs. The named computations above do not establish that such triples exist uniformly.
