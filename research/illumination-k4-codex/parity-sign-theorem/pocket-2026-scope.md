# April2026 theorem: angle-family applicability and the remaining gap

[in progress] The actual S/T one-corner detection goal remains open.

Primary source: [Apisa-Aygun, Components of strata of k-differentials and
their orbit closures, 2604.26177v1](https://arxiv.org/html/2604.26177v1),
Theorem1.2 and Corollary1.3. The former concerns the smallest invariant
variety containing all holonomy covers in a component. The latter gives
maximal possible orbit closure for almost every polygon with the specified
angle multiset, when a subset S of the angles sums to (|S|-1)pi. For even k,
maximal possible refers to the ambient quadratic-double locus, not an
arbitrary full Abelian stratum. These are family/generic conclusions.

## The literal pocket guarantees the angle-subset condition

**Hand lemma accepted by independent tools-disabled review (exit0).**
Assume every physical corner angle is an integer multiple of pi/4, as in
our canonical class, and the literal pocket has three distinct physical
vertices of angles45,225,270degrees. Let n_m count physical
corners of angle m*pi/4, m in{1,2,3,5,6,7}. Smooth pi points are omitted.
The literal pocket gives n_1>=1, n_5>=1, n_6>=1. The turning identity is

    3n_1+2n_2+n_3-n_5-2n_6-3n_7=8.

If n_3>=1, take the pocket45degree corner and a135degree corner:
their sum is pi=(2-1)pi. If n_2>=2, take two90degree corners, with the
same sum. Otherwise n_3=0 and n_2<=1. The turning identity and the two
pocket reflex corners give

    3n_1+2n_2=8+n_5+2n_6+3n_7>=11,
    n_1>=3.

Take two distinct45degree corners and a270degree corner.
Their sum is2pi=(3-1)pi. Thus every strictly simple room in the literal
pocket class meets Corollary1.3's angle-subset hypothesis. This is only
an angle-count argument; no room, ray or direction is generated.

## Why this still does not prove the pocket statement

The theorem's almost-every quantifier ranges over the full polygon
family with those angles. It gives no orbit-closure equality for our
specified one-complex-parameter period line, nor for every small
transcendental parameter on that line. A measure-zero exceptional set
in a higher-dimensional family may contain an entire chosen line.

Section21's algebraic coefficient separation proves that the whole small
period line lies in one common orbit closure. It does not prove that
this orbit closure contains every holonomy cover in the full component.
The new rank>=3 bound is still not equality with that larger locus.
Finally, even an equality/periodic-point argument would need a separate
bridge to the original actual S/T one-corner event at the raw base.

No periodic-point classification or actual endpoint-seed conclusion is
imported from the2026 paper. The route would need a theorem proving that
this particular slide line is not contained in an exceptional invariant
subvariety, or a direct actual-endpoint construction.
