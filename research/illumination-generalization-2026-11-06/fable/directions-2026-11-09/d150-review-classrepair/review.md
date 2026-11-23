# d150: referee report on class-repair (snapshot 2026-11-22 01:00)

Reviewed file: `../d95-review-queue/snapshots/class-repair.2026-11-22-0100.md`. It's byte-identical to the live `qclass-closure/bbbb/class-repair.md`. Context read: `deletion-invariance.md`, `cyclic-separation.md`, and the d148 review with its `checks.py`.

Code: [checks.py](checks.py), log [checks.log](checks.log), 10.4 CPU-seconds. It uses the named room DB55 only, with no room search and no network. The script compares two independent implementations:

- **Physics.** `walk()` is a cell-level billiard tracer adapted from d148. It matches d148's tracer on 426 rays with 0 mismatches. It also records the unfolded horizontal cylinder of each leg and the open rim arc of each seam crossing.
- **Arithmetic.** `propagate()` is the note's forward propagation in cylinder coordinates. It uses only circumferences, rim stops and chart translations, and it never looks at cells.

## Verdict

**Sound with gaps.** Both criteria are correct, both directions of each iff hold, and the DB55 data reproduce exactly. The sliding test agrees with physics on all 5,720 residues tested, with 0 disagreements. The gaps concern what the note leaves out. Most important, the residue sweep the note didn't run shows that sliding the crossings *does* repair the class on DB55. The fixed-crossing obstruction is therefore an artefact of keeping the crossings fixed. It isn't a property of the routes. The existence gap is unchanged.

## Check 1: the repair criteria

### Fixed crossings

The derivation is correct.

- On each leg, the new chord closes up mod C_i exactly when tH_i ∈ C_iℤ. The intersection of these groups is Pℤ, with P = lcm(C_i/H_i).
- Ph = Σk_iC_i is an integer, and v₂(P) = max(v₂(C_i) − v₂(H_i)).
- The new class is the core class iff v₂(u + jPh) < b. Given v₂(u) ≥ b, that happens for odd j iff v₂(P) < 0, and never otherwise.

**Arithmetic.** I tested the iff exhaustively for 1–3 legs with small H_i and C_i, covering 483,296 seeds. It had 0 failures, and Ph was never fractional.

**Physics.** On DB55, every one of 238 shifted shots U → U ± Ph is a legal arrival at T. Each one keeps the same chain and endpoint charts, so the sufficiency mechanism is confirmed.

### Sliding crossings

Both directions hold. With fixed charts, summing the legs gives sh ∈ X + gℤ, so the gcd condition is necessary. Conversely, a slope that passes every open arc and the terminal test assembles a legal segment, because a cylinder's interior holds no stops.

In numbers:

| Check | Result |
|---|---|
| Residues compared, 6 chains | 5,720 |
| Disagreements, test against physics | 0 |
| Same-chain arrivals off the coset U ≡ U₀ mod g | 0 |
| Pass status periodic in m with period Ph/g | Yes, on every chain tested |

The physics side here means a legal arrival at T with the same chain and endpoint charts.

### Line-transversal form

The test is a line-transversal condition, though the note doesn't say so. Develop the chain into the plane for a winding vector k = (k_i). Each seam becomes an open window on a horizontal line, and the developed target T(k) is fixed. A legal slope on that chain is then a segment from S to T(k) that passes through every window. That is point-to-point visibility through n open windows.

For each k, the terminal point fixes s = (X + Σk_iC_i)/h. So each winding vector allows at most one slope, and the note's m collapses k to its sum. Forward propagation recovers the unique k for a given s. The two formulations are equivalent.

### Seam endpoints

Open arcs correctly exclude stops. Over the 6 chains, 418 residues failed because they hit a seam endpoint. All 418 are physically blocked at a corner.

Chart cuts at regular points, such as x = a or x = b on a smooth wall point, need the overlapping-chart convention the note mentions. Under that convention the gluing on each arc is one translation mod C. The checker's `Geo` asserts that the next cylinder is constant on every arc.

## Check 2: the DB55 claim

**Cylinder data.** DB55 has 5 horizontal strips. In (a, b, y0, y1) form, they are:

| Strip | Height | Circumference |
|---|---:|---:|
| (0, 5, 0, 2) | 2 | 10 |
| (8, 13, 0, 2) | 2 | 10 |
| (0, 13, 2, 3) | 1 | 26 |
| (0, 5, 3, 5) | 2 | 10 |
| (8, 13, 3, 5) | 2 | 10 |

The corridor strip is the one at 2 < y < 3. Its rims carry the stops (5,2), (8,2), (5,3) and (8,3), and no level strictly between them carries a stop. Every strip unfolds into two cylinders, one for each vertical sign.

**Legal shots.** I took all legal S → T shots with |p| ≤ 30 and transverse travel h ≤ 40. That's 119 other-class shots, 53 in class c and 66 in class d, plus 51 core-class shots.

- All 119 other-class shots satisfy ΣH_i = h.
- All 119 have a strip leg with H = 1 and C = 26.
- Each has v₂(P) = 1, so none can be repaired with fixed crossings, as the note claims.
- All 51 core-class shots also cross the strip.

**Direction (3,2).** This is the core-class shot with displacement (48, 32). Its chain has 20 legs, 8 of them strip legs with H = 1. It has P = 130 and v₂(P) = 1. That fits the criterion: its fixed-crossing family U + jPh stays in the core class, and no other-class seed reaches it with fixed crossings.

## Check 3: the sliding test on named chains

**DB55 (3,2) chain.** Here h = 32, g = 2, Ph = 4,160, and the joint period is 2,080. Exactly 1 residue passes, the witness itself, and physics agrees on all 2,080 residues.

**d148 lost row (2,2) → (10,4), class b.** All 64 DB55 lost rows are horizontal-class. In this row T lies inside the open cylinder 3 < y < 5, so the last leg is partial with H = 1 and C = 10. The lowest witness is (−12, 8), which is direction (−3,2). It has 6 legs and a joint period of 520. Exactly 1 residue passes, and physics agrees on all 520. Fixed crossings can't repair any of the row's 53 other-class seeds, because each has v₂(P) = 1.

**Other-class seed chains, the sweep the note didn't run.** For 83 of the 119 seeds, v₂(h) ≤ v₂(g) = 1, so the class is constant along the coset. On the first 4 eligible chains, all with h = 12:

| Seed (class) | Passing slopes | Core-class slopes |
|---|---:|---|
| (28, 12) (c) | 1 | none |
| (−32, 12) (d) | 6 | (−346, 12), (−42, 12) |
| (44, 12) (c) | 5 | (−574, 12), (−270, 12), (378, 12), (682, 12) |
| (−52, 12) (c) | 5 | (−670, 12), (586, 12) |

So 3 of the 4 chains carry core-class slopes, and each one is physically legal. For example, the class-d seed (−32, 12) = 4·(−8,3) and the class-b shot (−42, 12) = 6·(−7,2) use the same 8 legs and the same open seam arcs. The criterion predicts legal reachability correctly in every case tested.

## Check 4: scope

**Proved:**

- The fixed-crossing iff.
- The sliding-chain iff, as a finite periodic test for one prescribed chain.
- The DB55 obstruction, for fixed crossings in the physical horizontal frame.
- The equivalence of three-class illumination with all-class relaxed existence plus arbitrary-arc deletion. This one is a tautology, and the note says so.

**Not proved:** any existence statement.

**Precise remaining gap.** Fix the physical horizontal frame. Every non-horizontal legal shot has a chain there, and for each h only finitely many chains have total height h. So L_c is equivalent to the following: for some h and some chain of height h, a residue passes every open arc and the terminal test, with v₂(X + mg) < b, or else a horizontal leaf joins S and T legally.

Quantified over all chains, this is a restatement of L_c. It gives a semi-decision procedure, not a proof. To close the gap you need one of two things:

- A bound on h in terms of the room, such as walls or area.
- A theorem that starts from a relaxed connection and produces an open-arc residue. A relaxed path meets stops only on rims, so it gives a chain with closed seam conditions at those stops. The theorem would have to perturb that chain into the open arcs, either keeping the class or in a chosen class.

Two facts make the second option harder:

- DB55's relaxed b-class witness at pencil residue 0 is the horizontal leaf itself, with h = 0. It has no chain in the horizontal frame, so the theorem must change frame or route.
- The fixed-crossing method can't start from total darkness, as the note says.

## Gaps

1. **Medium: the sliding sweep is missing, and the DB55 limitation is overstated.** The note calls DB55 a "sharp limitation" and ran no residue sweep. The sweep shows that sliding within the same chain repairs the class on 3 of the 4 eligible seed chains. For example, the class-d seed (−32, 12) and the class-b shot (−42, 12) share all 8 legs and seam arcs. The DB55 obstruction applies to fixed crossings only. The note should say that same-route sliding defeats it.
2. **Medium: the closing question doesn't address frame or degenerate witnesses.** A relaxed witness can be a rim leaf with h = 0, as at DB55 residue 0, and that leaf has no chain in the core frame. Any existence theorem must say which frame or route it perturbs from. It must also handle stop contacts as closed seam conditions.
3. **Low: a class-rigidity corollary is unstated.** If v₂(h) ≤ v₂(g), every slope on the chain has the same class. In DB55 g = 2, so class change needs 4 | h. That rules out 83 of the 119 other-class seeds, and it gives a cheap filter for any future search.
4. **Low: the line-transversal form is unstated.** Each winding vector allows at most one slope, so the test is visibility of T(k) from S through n open windows. This form makes the "boundary of the allowed intervals" remark exact: a relaxed path meets a window endpoint.
5. **Low: the chart convention at regular cut points is informal.** The overlapping-chart rule is correct. However, X depends on the chart representatives. Only X mod g is intrinsic, while the parity test uses the actual sh = U. The note should define the representatives explicitly. The checker sidesteps this by using U ≡ U₀ mod g from a witness.
6. **Low: the DB55 claim is verified only to a bound.** The general argument is correct. The numerical check covers |p| ≤ 30 and h ≤ 40.
