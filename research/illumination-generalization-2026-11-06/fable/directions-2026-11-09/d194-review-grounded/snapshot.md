Advances: L1 — For a fixed marked upper template with aligned mouth edges, a target outside the columns attached to the lower box has a transverse first entry into one of them. Distinct column heights can be eliminated from the resulting gate equation. A two-return argument now bounds area for an inside-column source when the opposite side is solid above the roof or the lower height dominates the cap.

# First entry and the divisor that survives a seam cut

Use horizontal and vertical template units u,t. The lower rectangle has width X=D/u and height H=h/t=m/n in lowest terms. Assume the comparable bounds of d191–d192, including positive lower bounds on H and on the source's fractional clearance from the floor and roof. The upper chamber, target and designated open roof intervals are fixed in template coordinates for the first-entry assertion. Assume an integral template, including the target abscissa and the endpoints of those intervals. A common bounded denominator also suffices after changing units. The estimates below apply to the residual lower-to-upper pairs. They do not concern all pairs in an arbitrary union of rectangles.

## Which side is actually accessible?

Cut the upper template at its wall and mouth abscissas. In each open vertical strip over a mouth, take the component whose bottom edge is that mouth. Call it a grounded cell. Its union with the lower part of that strip is a rectangle of height H+β, with solid horizontal sides. Components higher up in the *same* strip are separate cells. Take the union of the grounded cells, regarding common open sides as internal wherever they connect.

For a target strictly outside the closure of this union, there is a backward approach of positive horizontal travel B to a vertical side of a grounded cell. Its speed varies over an open interval J and may be shifted by integer multiples of a fixed integer P while preserving the signed heights at all preceding vertical exits. J may be chosen at arbitrarily small positive speed magnitude.

**Proof.** Temporarily seal the horizontal mouths. Launch at a small irrational normalized slope avoiding trajectories from the mark to a grid vertex. In the integral marked template any irrational slope from a rational mark does this. More generally remove the countably many exceptional slopes for a fixed real mark. The irrational directional flow on the unfolded template is minimal (no saddle connection in that direction), so the ray enters the interior of a grounded cell. This uses the same minimal-direction input as the long-corridor note. Before first entry the ray cannot use a sealed mouth, since it would already have been inside the adjacent grounded cell. The cell roof is a physical wall. Thus the first entry is through an open vertical side. Avoiding all cut vertices gives strict clearance and the same finite itinerary on an interval J. If the ray visits a component above a grounded cell, simply continue along it.

In each preceding strip passage the two horizontal walls are solid, the horizontal travel is integral, and increasing speed by a multiple of twice its integral height preserves the signed exit. Split at vertical reflections and retain the side assignment at each interface. An integer common multiple P of the doubled heights therefore preserves the approach by induction on its exits. This proof needs no bound on how often a cell is revisited. With a fixed marked template and fixed aligned mouths, the approach data are independent of the lower box. One may obtain J by following the prescribed irrational launch to first entry and taking the strict inequalities for that finite prefix. A cut at a *moving clipped mouth endpoint* can have nonintegral template travel, and this argument gives no uniform P there. A target on the union boundary or inside it is outside this first-entry assertion.

## Lower approach through several solid columns

Let the side obtained above be the exit, with its required horizontal sense. Send the lower source across the columns toward this exit in that sense. If needed, start in the opposite sense and turn once at the lower box's vertical end wall before approaching the exit. Choose the itinerary to include positive terminal travel inside the grounded column. In particular, when the source is outside it, a full final traversal is possible. The total lower horizontal travel is at most 2X. At sufficiently small reference speed every lower cut and the optional end-wall reflection occur strictly between floor and roof, since the vertical drift is at most 2X times the speed. Choose J in this range in the preceding proof. Split at every change of upper height and at the optional turn. Let w_i>0 be the physical horizontal travels, including partial first and last travels when appropriate. Put β_i=0 for runs with solid lower roof and use the grounded upper height otherwise. A disconnected higher cell over a closed roof adds nothing to β_i.

Necessarily, for darkness,
```
Σ p_i P w_i / (2u(H+β_i)) ∈ ℤ,       |p_i| ≤ K,      p_last ≠ 0.      (1)
```
Here K is uniform in the comparable bounds for a fixed approach with B>0 and boundedly many passages. To see this, center the phase bumps of all earlier passages at zero, and center the last at the correction needed to meet the backward target phase. At the reference speed the earlier crossings have clearance γ>0 from both lower edges. On fixed signed sheets the embedding across a cut is a translation of the developed vertical phase. In units of physical template height, errors at successive cuts therefore add. A vertical wall reversal changes horizontal sense and preserves vertical velocity. If there are s passages and H_* bounds all their heights, s phase errors of radius ρ change any gate height by at most 2sH_*ρ. Choose an interval of radius r inside J about the reference speed with 2Xr < γ/4. Choose ρ < min(1/8, γ/(8sH_*), Br/(4sH_*)). Earlier gates and the turn stay legal. The final signed mismatch has derivative B+Σ w_i/u and can be corrected inside this interval. This is the d193 overlap argument with one coordinate per passage. For normalized triangular bumps the total absolute Fourier mass is at most ρ^(−s), and the omitted mass outside the box of radius K is at most 2s/(π²Kρ^(s+1)) by summing the one-dimensional tails. Take K greater than 4s/(π²ρ^(s+1)). On averaging over the integer shifts, all surviving terms with last coefficient zero are nonnegative, including the constant 1. Darkness therefore implies (1). The two-coordinate overlap construction passed d193 with corrections.

## Elimination by distinct heights

Write b=β_last, T=m+bn, J_h for the set of *distinct* β_i and S_j=Σ_{β_i=j}p_i w_i. For physical integer widths, (1) implies
```
T divides P C_b S_b,             C_b = ∏_{j∈J_h, j≠b}(j−b).          (2)
```
Indeed multiply (1) by 2u times the product of m+jn over distinct j. Modulo T only the term Pn S_b times the other factors remains. Each other factor equals (j−b)n modulo T, and n is invertible modulo T.

If the terminal height occurs just once and the full terminal width is w=(iD+ju)/r₀ with fixed integer coefficients and r₀>0, then S_b=p_last w. Under the anchored normalization gcd(h,t)=gcd(D,u)=1 and the d191–192 aspect hypothesis (D/u)/H=A/B₀ in lowest terms, multiply (2) by r₀ gcd(Am,B₀n) and reduce modulo T. This gives
```
T divides P C_b p_last (jB₀−iAb).
```
For nonzero determinant this explicitly bounds T by P |C_b| K |jB₀−iAb|. Thus n≤T/b, m≤T, D≤Am and u≤B₀n, giving the physical area bound A T² + V B₀(T/b)² for template area V. This extends the single-column divisor to paths through arbitrarily many *different* earlier heights in the fixed chart. No use of a smaller wall budget at a new seam is required.

**Why the proposed induction stops.** If a terminal column is traversed earlier in full, its two frequency coordinates coincide. Coefficients −1,+1 on these visits satisfy (1) identically with S_b=0. The first-entry proof controls the upper prefix but does not remove this earlier lower traversal. Cutting the itinerary at the repeated seam gives a new start of slope-dependent height and sheet. It is not a free marked start for an induction on fewer components. Thus (2) can carry no information even though the transverse approach exists. This is a failure of the proposed inference. It gives no dark pair. Other residuals include partial terminal widths involving the free source coordinate and targets already in grounded cells.

## Independent horizontal offset

Two routes at the same terminal height b give T dividing both P₁C₁S₁ and P₂C₂S₂. In particular if the terminal heights occur uniquely on both routes, with full widths w₁,w₂, then
```
T ≤ |P₁C₁P₂C₂| K₁K₂ gcd(w₁,w₂).
```
This follows by multiplying both divisibilities by the other route's coefficient and using Bézout. It suffices that the *two traversable widths* have bounded gcd. The global gcd(D,u,w)=1 does not supply such widths. Splitting one uninterrupted column into two creates no independent target approach at the artificial cut. On the d193 projective example T=w=2m+1, so a second certificate using the same full width still allows unbounded T. Whether a different legal route forces a coprime divisor or actually lights those placements is open. There is no proof of a dark family here.

## Source inside a template-width column: use the repeated visit

Here is the d193 pair-type convention. Orient the picture so the exit into the target wing is on the right. The lower box has normalized width X=D/u, height H=m/n in lowest terms, and X/H=A/B₀ in lowest terms. Its rightmost strip is a full column of width j=w/u (a fixed positive integer), height Z=H+b, with floor at zero. Assume 0<j<X, a solid lower roof throughout the left wing, solid lower side and floor, and a target approach on the right with phase e−Bv on a closed interval inside J, travel B>0, period P and a fixed signed exit. Use the uniform compact bounds of d193. Let the lower source be strictly inside the column, at horizontal distance ℓ∈(0,j) from the target-side edge. All speeds and travels in this section are in template units.

**Claim.** For this pair type there is a uniform effective area bound if either (i) the left side of the column above the lower roof is solid throughout, or (ii) H≥b. In (ii) that side may contain additional upper openings. Rectangularity of the target template is unnecessary. No thin-column inequality involving j is used.

1. Let C=2Z, and fix the initial signed vertical phase s of the source. For the direct rightward path the exit equation is s+ℓ(v+kP)=e−Bv modulo C. On an interval of length η the mismatch sweeps length (B+ℓ)η. The residues of kℓP form a grid of spacing C/q₀, where q₀ is the denominator of ℓP/C. The data are rational at lattice placements. Direct failure therefore gives q₀≤C/(Bη), including equality. Restrict subsequent shifts to k multiples of q₀. This freezes the source-dependent shift ℓkP modulo C, regardless of the denominator of the source abscissa.

2. Start leftward. First suppose that the whole left side of the column were a vertical mirror. The first travel is j−ℓ and the return travel is j. Write z for the adjustable increment in tall vertical phase on a full traversal. It also applies to the partial traversal because the ℓ shift is frozen. For fixed v the virtual reflected shot requires
```
2z = e−s−(B+2j−ℓ)v                 (mod C).
```
There are two solutions differing by Z. Their left-side contact phases, before folding, are
```
y(v)=(e+s−(B+ℓ)v)/2,               y(v)+Z       (mod C).
```
The folded contact heights sum to Z. In (ii) at least one is ≤Z/2≤H. In (i) any contact in (0,H) admits the lower excursion below, and any contact in (H,Z) reflects on the solid side.

Choose v away from where either contact folds to 0,H or Z. This can be done with uniform positive clearance, including when H=b. For example take the middle half of the approach interval and delete the roots y(v) ∈ {0,Z,H,−H}+Zℤ there. Each of the four progressions contributes at most 1+(B+j)η/(2Z_min) roots. The midpoint of a longest remaining subinterval is a positive distance from these roots and from the interval ends; roots just outside the middle half are covered by the same endpoint margin. Multiplication by the minimum speed B/2 gives a lower bound on phase clearance. This choice controls the contact and leaves an open speed interval for exact endpoint correction.

3. At a selected contact below H, send the trajectory through the entire lower wing, off its far vertical wall, and back to the column. Prescribe zero **total** vertical phase advance modulo 2H on this excursion. Its far-wall height is then the entrance height or its complement in H, so both the turn and both seam crossings have positive clearance. It returns to the same signed height as the virtual mirror route. At a selected solid contact above H use the mirror route itself. In the former case the extra adjustable phase, measured in turns of the lower circle, must cancel the base advance 2(X−j)v/(2H). In the latter case this extra phase is unrestricted.

4. The two rotation frequencies, per increment of k by q₀, are
```
f = q₀P j n/(2T),                  g = q₀P (A/B₀−j n/m),       T=m+bn.
```
They control respectively the full column's increment z/C and the wing excursion's increment in lower-circle turns. For the mirror route prescribe any center for g. A neighborhood of the prescribed two phases yields an exact shot after varying v. Explicitly, if each coordinate misses by at most ρ, each relevant entrance, return or endpoint misses its virtual phase by at most Eρ with E=2C+2H. At the far wall the relevant error is bounded by the same amount modulo the two possible complementary heights. On the fixed sheets, changing v changes lower contacts at rates ≤2X+j, and the final mismatch has derivative B+2j−ℓ, plus 2(X−j) on the wing route. Fix a speed radius r within the upper approach and less than the chosen contact clearance divided by 4(2X+j+1). Take ρ < min(1/8, clearance/(4E), Br/(2E)). The derivative is ≥B, so within this interval a zero of the mismatch exists and all the prescribed gates stay legal. Upper signed phases are periodic even during this speed correction, by the approach hypothesis.

5. Average the product of triangular bumps at the two prescribed centers as in (1). Unless some nonzero (p,q) with |p|,|q|≤K has pf+qg integral, the constant term alone survives Fourier truncation. One can take K=1+ceil(8/(π²ρ³)). Thus darkness forces such a relation. For p≠0, multiplying by 2B₀mT and reducing modulo T gives T dividing p q₀ P j B₀ m n. Since gcd(n,T)=1 and gcd(m,T)≤b, this gives T≤bKq₀PjB₀. For p=0 the same relation gives m dividing q q₀PjB₀, hence T≤(1+b/H_min)Kq₀PjB₀. Either bound is effective in the uniform template and aspect data. Wall-gcd normalization now gives the area bound derived after (2), using the larger of these bounds for T. This argument is independent of the d193 small-ℓ criterion.

**First case still open for this mechanism.** If H<b and the non-target side opens into another upper component, both virtual contacts can lie in its open gates. The precise failure of step 2 is that for every usable v and source-sheet choice both contacts miss the union of the lower wing and solid reflecting wall, up to grazing. No such failure is asserted for any particular room. Cutting there requires a return in the other component that preserves signed height or supplies a controllable replacement phase. First entry alone does not prove that return. If the target lacks the right-side approach, even the direct order bound in step 1 is unavailable.

**d193 scope and scale.** Its original full-width bound concerns a lower-wing source whose roof is solid up to the column and a target with the transverse approach. For an integral row w=iD+ju and 0<w<D its determinant is automatically nonzero: zero forces i,j to have the same sign when nonzero, and then a positive width is at least D. In w=D−ku the choice k=0 gives the entire box. The d193 constants already cost at least a power of H*. For the independent-offset controls, w=2m+1 absorbs L in the first family (no oddness restriction is needed); the distinct family where u absorbs L has w=u=m(2m+1), D=(m+1)(2m+1), c=m and (p,q)=(1,2). The two-return bound above uses gcd(D,u)=1 for its conversion to physical area and does not close that offset case.

**What is the smallest W ≤ 20 room this result doesn't cover?** No ledger word moves. The W=10 word LLLRLLLRLR remains open for all length assignments. Its ledger realization is (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2).
