# A populated orbit exclusion with reflex-stop cost zero

**Result.** In cov4181, the failed primitive parity (0,1) of the pair S=(2,3), T=(4,3) has hitting number **zero** in the class-wall-budget model. Even if every physical reflex admits straight passage, no relaxed route of this class joins the pair. The stronger fact is directional: every target lift lies on a closed regular leaf disjoint from every source lift and every reflex lift in this entire parity class, when convex-corner lifts are made transparent on the translation unfolding. The pair is lit horizontally. This room has one empty parity class and does not settle the BBBB-only problem.

## Why this implies zero

Work backwards from T. Up to the first reflex, a relaxed path agrees with ordinary billiards, hence lifts to the appropriate straight leaf on the four-copy unfolding. If its closed leaf misses every reflex, no relaxed continuation can ever use a reflex. If it also misses every lift of S, it cannot finish at S. Stopping at convex corners can only shorten the available path. Thus the relaxed route family is empty and its minimum hitting set is the empty set. The same argument works in any orthogonal room and does not require a bound on the wall count.

## An exact check on d144's existing finite orbit

I reused d144's two permutation transitions and canonical relabeling for its named 112-square surface. The replay keeps the matrix **modulo two only**. It computes no new slope, trajectory, or direction representative. With the same initial state, transitions and state equivalence, this is precisely the 3,888-state orbit in d144. Exactly 1,296 states have the required parity. The extra calculation reads vertical permutation cycles in those states, with their existing S, T and physical-corner labels.

If h,v are the horizontal and vertical square permutations, a bottom-left square germ i goes around its vertex to v h v⁻¹ h⁻¹(i). A moved germ belongs to a reflex lift: here there are 24 moved germs, three for each of the eight angle-6π points. A convex lift is labeled as a physical stop but has a fixed germ. On a v-cycle avoiding all moved germs the vertical lattice continuation is unique, even at a convex lift on the translation surface. If a neighboring germ on that cycle were singular the same permutation test would detect it. Looking for a first reflex on either side requires only checking that the cycle is disjoint from the moved germs.

| Ordinary intervals incident to a reflex, by the endpoint labels they contain collectively | Class states |
|---|---:|
| Neither S nor T | 108 |
| S only | 1,188 |
| T only | 0 |
| Both | 0 |

The stronger check omits the convex cuts entirely: in **every** one of the 1,296 states, each uncut cycle containing T is disjoint both from S and from the commutator support. This checks both orientations and all four target lifts. The target-cycle lengths range from 2 to 42 primitive lattice steps. The counts are counts of finite states and cycles, not estimates of the angular frequency of physical directions. D144 independently validated the underlying orbit and ordinary illumination result; this further cycle statistic is new. [Checker](orbit-exclusion-cost.py) · [D144 input and review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d144-review-dyadic/review.md)

## Consequence for wall accounting

A positive universal charge to corners *hit by relaxed routes* for a populated orbit exclusion is impossible in the normalized W≤20 range. In this named case the cost is zero even though one source-parity reflex was available and source legs reach a reflex in 1,188 states. Ten regular sites in the off-source class do not change the answer. This is not a zero-wall construction: the room's walls determine which leaves contain its marks.

The original vertical direction illustrates the distinction. At x=4 the target bounces between y=0 and y=6. For every nearby abscissa in (3,5) the same walls sustain the vertical periodic motion. At x=3 and x=5 the square pattern has reflexes at heights 2 and 4. Those four reflexes have parity (1,0), exactly the empty class already counted in the other obstruction. Thus a charge to the boundary of this particular family of parallel closed trajectories would reuse corners paid for elsewhere. This one direction does not prove that the same four corners account for the complete orbit.

**Remaining budget question.** For a physically dark BBBB pair, any target cylinder with a regular target leaf must also exclude every source lift from its open interior, since two points in that interior can be joined by a strip chord. The zero-cost example identifies what an additional charge would have to measure: walls that keep the two endpoint lifts apart across whole families of closed trajectories, even though no relaxed route hits those walls at a corner. A blanket charge of one reflex per populated exclusion fails in the larger normalized class. A bound on this indirect wall cost, or a BBBB argument that precludes such simultaneous exclusions, remains open. [Earlier budget](class-wall-budget.md)
