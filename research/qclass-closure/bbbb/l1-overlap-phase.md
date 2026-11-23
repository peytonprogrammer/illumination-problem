Advances: L1 — Crossing a narrow horizontal mouth through its vertical overlap column forces a short resonance with a nonzero aperture coefficient. In the comparable-size regime it bounds the two axis ratios separately if the source-to-far-wall phase has bounded denominator.

# Let the trajectory cross the seam inside the overlap

A lower-to-upper path crosses a separating horizontal mouth an odd number of times, counting transverse crossings. The construction below permits any odd number. It does not assume that three always suffice.

**Geometry and scope.** Measure horizontal and vertical lengths in the upper stretch units u and t and use normalized speed σ=dy/dx. The lower box has normalized height α=h/t and physical width D. Its rightmost width w is the overlap: a column of normalized width ε=w/u and *full* normalized height α+β. In the column the horizontal seam at height α is open throughout. Its floor and roof are solid. At its left edge a ray from the lower wing can enter at any height in (0,α); at its right edge it can leave into the upper wing in (α,α+β). The physical source abscissa measured from the left wall is c<D−w. Put x=(D−w−c)/u and θ=d/h. Both endpoint wings are outside the open column. This geometry is a hypothesis; a side gate narrower in height, a notch inside the overlap, or an endpoint inside the overlap needs a different argument.

Suppose 0<α_min≤α≤α_max, 0<x≤L, 0<ε≤1, and θ∈[m,1−m] for m>0. Assume the upper wing, viewed from the *right vertical edge* of the column, supplies one backwards open approach interval J, upper horizontal travel B≥B_min>0 and a period P>0 in σ that preserves its exit position and signed sheet under σ→σ+kP. Write η=|J| and |σ|≤V on J. Here β is fixed. A fixed integral upper-wing template with target and vertical side portal gives these inputs by the reviewed d124 first-hit construction and the unit-band period argument with axes interchanged. The thin horizontal mouth is not the portal to which that theorem is applied. The hypotheses also allow a varying upper approach with the same uniform controls. [D124](effective-chamber.md) · [First-hit period](l1-crossing-gate-resultants.md) · [Two-rectangle overlap geometry](doorway-word-bound.md)

## The aperture coefficient cannot disappear

There is an explicit K depending on these controls such that darkness implies

    p P x/(2α) + q P ε/[2(α+β)] ∈ ℤ,       |p|,|q|≤K,       q≠0.        (1)

The two denominators are the vertical periods in the lower wing and in the taller overlap. A straight flight across the overlap can cross the old horizontal seam repeatedly without an intermediate gate test, since every such crossing occurs inside the open column.

**Uniform window.** Parameterize vertical billiard motion in an interval [0,H] by a circle of circumference 2H: folding the coordinate gives physical height and its sheet gives the sign relating physical velocity to the signed speed. At the left edge the lower phase is θα+xσ modulo 2α. On each of its two open sheets, embedding in the taller column with the same height and physical velocity adds a constant in the unfolded phase (0 or 2β). On the upper approach, the required right-edge phase of the taller column can likewise be lifted as e−Bσ on J: backwards development has horizontal travel B, and the entrance sheet is fixed. Shifting by kP preserves this phase at the same base σ, including its folding sheet. The left-wing flight is monotone in horizontal position and makes no side-wall turn.

Here are uniform constants ensuring that the left edge is cleared. Put x_min=mα_min/[2(V+1)], N=3+ceil(Lη/α_min), and l=η/(8N). If x<x_min the entire base interval stays at least mα_min/2 from a lower fold boundary. Otherwise remove from J the slopes with θα+xσ∈αℤ. At most N components remain, so the midpoint of a longest component is at least 4l from each of its ends. Its lower phase is at least 4l x_min from the nearest fold boundary. In the first case take the midpoint of J. In both cases call the midpoint σ₀ and put

    m₀=min(mα_min/2,4l x_min),    r=min(l,m₀/[4(L+1)]),
    ρ=min(1/8,m₀/(8α_max), B_min r/[8(2α_max+β)]).

All are positive, independently of ε. Consider the discrete two-circle rotation by

    (f₁,f₂)=(P x/(2α), P ε/[2(α+β)]).

Seek k whose first coordinate kf₁ is within ρ of zero. This keeps the left phase and sheet close to their base values. Set the second target φ so adding 2(α+β)φ to the left tall phase plus εσ₀ gives the required right phase at σ₀ modulo 2(α+β). If kf₂ is within ρ of φ, the signed mismatch at σ₀ has a representative of magnitude ≤2(2α_max+β)ρ. On σ∈(σ₀−r,σ₀+r) the left sheet stays fixed (phase drift ≤Lr+2α_maxρ); the right approach follows its original upper itinerary with the period shift. The mismatch derivative there is x+ε+B≥B_min. Adjusting σ within that interval therefore makes the endpoint exact. Floor and roof reflections inside the open column are smooth; the two end heights lie strictly inside their vertical gates. This constructs one legal trajectory.

To prove (1), use the product of two normalized triangular circle bumps of radius ρ centered at (0,φ). Truncate at K=1+ceil(16/(π²ρ³)); the omitted absolute Fourier mass is <1/4 by d184. Average over positive integer k. A mode (p,q) survives precisely when pf₁+qf₂ is integral (finite geometric sum). All surviving q=0 terms are nonnegative because the first bump is centered at zero. The constant coefficient is 1. If no retained mode with q≠0 survived, the average would be positive, yielding the legal shot just proved. This is a necessary arithmetic condition for darkness, not a sufficient one. [Fourier bound](l1-gap-hyperplanes.md)

## When this separates the two heights

Set x₀=x+ε=(D−c)/u and z₀=P x₀/(2α). Suppose z₀ is rational with denominator at most H₀. For example this follows if the source fraction c/D and the coupled aspect (D/u)/α each have bounded rational height and P is a fixed integer. Do not infer that bound from comparable magnitudes alone. Equation (1) becomes

    p z₀ + (Pε/2)[q/(α+β)−p/α] ∈ ℤ.                                (2)

If ε P K [1/α_min+1/(α_min+β)]/2 < 1/H₀, then p z₀ must be integral: otherwise its distance from an integer is at least 1/H₀. The correction has absolute value <1, so it must vanish. Hence p≠0, q−p≠0 and

    α = β p/(q−p),                  p z₀ ∈ ℤ.                         (3)

For integral template β this bounds the reduced numerator of h/t by βK and its denominator by 2K. If c/D is also a specified bounded-height rational and P a fixed integer, then D/u=2α z₀/[P(1−c/D)] has bounded height as well: z₀ has denominator ≤K by (3) and numerator bounded using x₀≤L+1. For example if c/D=i/j in lowest terms with j≤J₀, write n=p z₀. Then D/u=2β n j/[P(q−p)(j−i)], with |n|≤KP(L+1)/(2α_min). These separate bounds exclude the equal high-denominator example from d191 in this subclass when its aperture is sufficiently narrow. The constants are effective given the upper-wing controls.

**First unresolved source placement.** For arbitrary lattice marks z₀ can itself have large denominator. Formula (2) still puts z₀ within O(ε) of an integer divided by p once ε is small enough to exclude p=0. Its deviation can cancel the aperture term exactly. For instance at the arithmetic level p=q=1 allows z₀=n+(Pε/2)(1/α−1/(α+β)) for any positive rational α. This is a relation among phases, not an example of a dark pair. A second trajectory imposing an independent condition on the same source coordinate would be needed to eliminate this cancellation. Also, (3) bounds ratios for these placements; it gives no upper bound on the area of an arbitrary dark product.

## If the upper wing changes shape

There is a direct test for reusing the preceding estimate on an upper itinerary. Split it at each new constant-height vertical band and at every horizontal-direction reversal. In a piece of horizontal travel bᵢ>0 and vertical height Hᵢ the phase shift from changing σ by Δ is ±bᵢΔ modulo 2Hᵢ. Thus a sufficient common shift preserving all signed exits is the rational least common multiple of 2Hᵢ/bᵢ for all pieces (least positive number divisible by each in the integer-multiple sense). This suffices when the pieces have solid parallel walls between the stated exits and all interfaces are included. The original first-hit interval and strict gates are still required. If a decomposition into further scale classes keeps the normalized period, window, travel lower bound and speed bound uniform, the same proof goes through without changing its number of phase coordinates.

Scale order alone supplies no such period estimate. With physical b₁=b₂=1 and H₁=M,H₂=M+1 the period preserving both signed exits is 2M(M+1); measuring heights in units of M still leaves normalized period 2(M+1). Both heights belong to the same d182 scale class. This is exact arithmetic for the piecewise exit-preserving condition, not a lower bound on all possible route periods. In (1) a growing P weakens the coefficient-height consequence even if the Fourier truncation K stays bounded. A general induction must either tolerate moving internal exit phases or find another uniformly controlled upper approach. No room, direction, word, ray or size search was run.

**What is the smallest W ≤ 20 room this result doesn't cover?** No whole word changes status. The W=10 word LLLRLLLRLR remains open as an all-length statement, with ledger realization (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2).
