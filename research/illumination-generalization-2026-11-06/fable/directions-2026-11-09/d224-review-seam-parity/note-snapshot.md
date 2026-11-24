Advances: L1 — for the axial degree-two branch, an integral shear can turn the known half-room ray into a ray of opposite seam parity even when the original ray is on a saddle connection. A divisibility test gives a sufficient condition. I do not obtain both parities for every 11-cell half-room. The exact obstruction is a constant seam-crossing parity on all straight connections of the specified pair.

### Which parity is being counted

Let H be the closed half of the strictly simple room P cut along its axial mirror. The open seam is a wall of H. Its two ends are convex corners of H and smooth wall points of P. Take distinct interior lattice marks S₀,T₀ in H. Ordinary H-rays avoid all H corners. Counting their contacts with the open seam modulo two records the physical target side after unfolding just that wall. A path in P through a smooth seam end can still be legal even though its projection has a reversal at an H-corner. Thus both ordinary seam parities suffice to light both target representatives; their necessity for physical lighting would need an additional argument.

The branched double cover here is **f:Q→N**, where Q and N are the room doubles of P and H. On the physical polygons P→H is a mirror fold along a whole segment. On N the image of the seam is an embedded arc β from b₁ to b₂. Crossing β toggles the sheet of f. Off its ends the character of the double cover evaluates a closed curve as its mod-two intersection with β. In particular a simple closed curve has odd character exactly when it separates the ends. [Degree-two cover and census reduction](l1-imprimitive-22.md)

### A necessary and sufficient test for ordinary H-rays

Use the finite orbit of the four-copy unfolding of H with the corners forbidden, the seam crossings tracked by f, and compatible lifts of the two marks labeled. In each straightened direction divide the permitted horizontal lattice trajectories into closed regular levels and open intervals between forbidden corners. For each common component and lift choice, take one oriented subarc from S₀ to T₀ and record its seam bit ε. For an interval use the unique subarc, allowing either travel direction. For a circle also record the bit η of one full turn returning to the same directional lift. These bits are taken along the folded H-trajectory, or equivalently by transport in Q→N with target sides fixed. The continuation retains the terminal **velocity** as well as the terminal point.

The attainable parity set is exactly the union of {ε} for intervals and ε+⟨η⟩ in F₂ for circles. Indeed a legal chord unfolds in one primitive direction and stays on one component. On a circle any alternative arc or extra turn changes its bit by a multiple of η. Conversely every recorded subarc is legal, and so is adding a turn. The character can be tracked on the finite orbit by retaining the two-sheet cover with the marked origami, rather than assigning seam bits anew after a shear. [Cylinder and saddle-connection criterion](l1-cylinder-levels.md)

For the axial, disjoint off-axis case at area 22, H has area 11 and the two projected marks are distinct and interior. The census makes this union nonempty. **The exact remaining obstruction to both ordinary parities** is that every common circle has η=0 and all contributing circles and intervals give the same ε across all states and compatible incidences. An odd circle containing only T₀ cannot in general be appended to the known ray: changing its terminal direction at T₀ would break straightness. Another sufficient case is a single odd-character open cylinder containing lifts of both marks on different levels. In its developed strip the chords to two consecutive translates of the target remain in the strip. Their relative loop goes around the core once, hence their bits differ. [Census scope](census-a21-status.md)

### A target-level test that does not require appending a loop

Assume the mirror axis is vertical, x=c. Work on Q upstairs, starting from the census ray lifted to P. Split at the horizontal wall levels into rectangular bands, treating each interval of a slice separately. An interval of physical width W and band height h gives a cylinder of circumference 2W in Q (one trip on each copy). In its coordinates (ξ,d), where d is height above the band's floor and ξ goes right on the front and left on the rear, use the shear

    (ξ,d) → (ξ+λd mod 2W,d).

Choose λ integral with 2W dividing λh for every band. Both boundary circles of each band are fixed pointwise. The band maps glue to a single affine automorphism: in oriented flat charts their derivatives coincide, since chart changes have linear part ±I, and their boundary values agree. The inverse uses −λ. It fixes all physical corners and both smooth seam ends, which lie on horizontal wall levels. In particular it takes a legal upstairs path missing these endpoints to another such path. This changes the direction of the entire ray, so its incoming and outgoing velocities still match through every regular point.

Suppose T₀ lies strictly inside a band whose physical interval is centered on c and crosses the seam. Write Wₜ for its **full upstairs** width and dₜ for the height of T₀ in the band. Translation by Wₜ on its cylinder takes each lift of T₀ to a lift of σT₀: the rear copy at the reflected abscissa is half a circumference away. It also carries every lift of σT₀ back over T₀. To fix S, impose 2Wₛ dividing λdₛ in its band; omit this condition when S lies on a band boundary. Let

    L = lcm over all bands of 2W/gcd(2W,h),
    Lₛ = lcm(L, 2Wₛ/gcd(2Wₛ,dₛ)),

with Lₛ=L for a boundary source. There is an allowed shear fixing both lifts of S and exchanging the two physical targets precisely when

    gcd(Lₛ dₜ, 2Wₜ) divides Wₜ.

Indeed write λ=Lₛm and solve λdₜ≡Wₜ mod 2Wₜ. Apply this shear to either lifted census witness. It fixes the physical source and exchanges the target sides. Since it also fixes the seam ends, folding the new ray gives an ordinary H-ray of the opposite parity. This proves both parities under the displayed condition, at any area where one ordinary H-witness is known. Reversing the roles of the marks gives a second test. A mark on a band boundary or outside a seam-crossing interval can defeat this construction. An affine map fixing the seam ends suffices here; it need not fix the seam arc pointwise because only ordinary legality and the two **endpoint sides** are required after refolding.

### What a path to a seam end supplies

A transverse legal prefix from T to a smooth physical seam end E, followed by the reflected reverse prefix, lights σT. The actual wall reflection at E equals −Dσ. This proves a partner connection, but an S→T ray and a T→σT ray are not composable as a straight ray unless their germs at T agree in the same lift. Even with matching velocity the resulting physical path visits E, so it gives no ordinary seam-parity witness in H. A valid use for physical lighting is to extend the *known ray itself* to E in its arrival direction, before another forbidden event, then use the symmetry and retrace until the mirror target is reached. This closes that physical pair even though the projected path uses a reversal. No conclusion about reaching E follows from the area-11 interior-pair census.

### Half-turn quotient

For a half-turn about O the physical quotient P/σ has one interior cone point of angle π, the image of O. On the sphere doubles f:Q→N there are exactly **two** branch values, the images of the front and rear lifts of O. They are two of the eight poles of N. The other six are unbranched poles; there is no additional branch locus. Away from these two values, choose a cut arc joining them to read the same C₂ transport. For fixed regular quotient endpoints u,v, two legal straight segments whose relative closed loop has odd intersection with that cut reach opposite target lifts from a fixed s. A common cylinder with odd core character is sufficient by the same winding argument. Separate quotient mirror lifts must be tested with their physical target labels.

Here N is the double of a cone disk, and the 11-cell planar-room census supplies no first segment between arbitrary projected marks. A chord through O upstairs can help when its projected path uses a reversal; for a partner pair the half-turn of a reversed S→O prefix continues with the correct velocity. For distinct nonpartner marks neither a quotient segment nor a second target lift is forced by the branch count. Thus the half-turn follow-on still includes disjoint mark orbits.

**First open case.** In the imprimitive area-22 branch, take the axial 11-cell half-room with distinct off-axis same-parity projected marks in different symmetry orbits. One parity is known. When neither mark passes the target-level shear test and no common odd cylinder has been shown, one must produce the missing parity in the component test or a legal physical path through a seam end to the missing target. For the half-turn branch even the axial census reduction is unavailable. No larger census or direction search was used.
