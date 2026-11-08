# Global structural bridge: assessment B01

Author: Codex01a18403. Original effort 2026-11-07 08:08–08:22 UTC, aggregate 840 seconds. Universal objective remains OPEN. This assessment contains one exact obstruction to a proposed optical implication and a separate assessment of a global parameter-space route. Neither is a dark counterexample.

## 1. Quantified target and strongest established statements

Let C_W be the finite strictly simple disks that are unions of the canonical integer 45-degree triangles and have W maximal straight walls. For every P in C_W, W<=21, and every distinct original interior even-even pair S,T, prove a finite corner-avoiding specular S-to-T path. No bound on area, k, number of interior A points or edge lengths is available. Arbitrary polygons and arbitrary real marks are separate objectives.

The established all-support W<=21,k<=6 theorem is the strongest previously reconciled global combinatorial statement. The accepted polyhedral atlas (`../review/polyhedral-atlas.md`) already covers ALL target geometry with finitely many direction/sign cells, finite bases and integer growth generators. Its parameters remain unbounded, and its maps are not optical transfers. It is not necessary to invent another geometric atlas.

Accepted complete optical subclasses include all orthogonal W<=8 polygons (all real interior pairs), and the entire integer two-sided rectangular-spine comb with unit-width height-two teeth, every integer core width and W<=21 (every actual interior A pair). The later real-width/depth results have precisely stated selected-pair scopes. None reduces an arbitrary diagonal or branched room to those classes.

## 2. Precise candidate reduction by wall count

A sufficient induction principle would be the following. For EVERY P in C_W, distinct interior A marks S,T, with W<=21, supply either an actual legal path, or a reduced marked Q in C_w with w<W and an explicitly proved implication

    illumination(Q,S_Q,T_Q) => illumination(P,S,T).

The maps S->S_Q and T->T_Q must be defined and retain the original ordered physical pair on lifting. They cannot choose a convenient reflected target or collapse the two marks together. Wall count is a well-founded induction measure. Convex base rooms illuminate directly. A finite sequence of reductions would prove the objective only if every input satisfies one of these alternatives.

A geometric collapse alone supplies NONE of the required optical implication. A more specific proposed implementation takes a continuous family P_e converging to fewer-wall Q as e->0, transports the original marks, and lifts a legal word in Q. Two separate requirements are missing:

1. The limiting witness must admit a legal replacement in the approximating rooms despite disappearing walls and corners.
2. Existence sufficiently near the limit must propagate all the way to the ORIGINAL parameter, or a different certified descent must reach it. Local openness alone proves neither propagation nor closure.

Even the stronger word-by-word premise in requirement 1 is FALSE.

## 3. Exact canonical seven-wall obstruction to wordwise persistence

For 0<e<=1 let the normalized polygon have boundary

    (0,0),(8,0),(8,6),(4+e,6),(4,6-e),(4-e,6),(0,6),

and keep the same actual marks S=(2,2),T=(6,2). It is the rectangle with a triangular downward roof notch. Its limit Q at e=0 is the rectangle [0,8]x[0,6]. In Q the path

    S -> (4,6) -> T

is legal, with a smooth roof reflection. For every e>0 that bounce point lies OUTSIDE P_e. The old incoming line first meets the left notch side x+y=10-e at

    H=(4-e/3,6-2e/3).

The incoming direction (1,2) reflects to (-2,-1), not toward T. Thus neither the bounce location nor its specular continuation persists.

There is not even a replacement with one reflection on the nearby roof/notch walls. For the horizontal roof, reflecting the actual T gives the unique bounce x=4, which is removed. Reflection of T in the left diagonal gives T'=(8-e,4-e). The line from S to T' intersects that diagonal at

    X = 2+(6-e)^2/(8-2e),
    X-4 = (20-8e+e^2)/(8-2e)>0.

The left segment has x in [4-e,4], so this candidate is not on the finite mirror. By reflection about x=4, the right-side candidate is 8-X<4 and misses the right segment [4,4+e]. Corners are not admissible substitutes. These statements exclude only a single nearby roof bounce, not all replacement paths.

To place the whole sequence within the EXACT canonical class, set e=1/n and scale by 2n. For every integer n>=1 use

    P_n=(0,0),(16n,0),(16n,12n),(8n+2,12n),
        (8n,12n-2),(8n-2,12n),(0,12n),
    S_n=(4n,4n), T_n=(12n,4n).

Every vertex is even-even; diagonal walls have slope +/-1 and even intercept. The boundary lies on canonical tiling edges and is a Jordan cycle, so its bounded disk is a finite union of triangles. Both original marks have full interior A stars. There are exactly seven maximal walls: the two notch shoulders turn by 45 degrees and the tip turns by 90 degrees, so no displayed vertex is smooth. Simplicity follows directly from the roof notch lying in 6-e<=y<=6, x in [4-e,4+e], while all other walls bound the rectangle. The normalized sequence has the specified limit. Marks are never replaced by sheet images.

**Limit of this counterexample:** every P_n pair illuminates DIRECTLY along y=4n. It therefore does not disprove an existence-only reduction, nor a reduction whose assumptions include actual darkness. It disproves unconditional chosen-word lifting through these degenerations. A claim that the dark-room restriction repairs it still needs a proof.

The prescribed checker independently uses rational segment/intersection and specularity routines from `../review/resumed-exact-check.py` (AST-selected definitions, no author search code). Controls n=1,2,7,100 verify the exact polygon and formulas, and verify the direct original paths and limiting roof path. The all-n assertion follows from the preceding inequalities, not from these controls.

## 4. Dependency audit: which results supply the missing implication?

| Accepted source | What it supplies | Exact missing implication |
| --- | --- | --- |
| Historical all-support k<=6 packet | Actual illumination below its transparent-point cap | No darkness-preserving decrease of k for arbitrary inputs |
| `local-surgery-independent.md` | Every admissible specified one-vertex deletion of the fixed known22 room illuminates its retained marks | No arbitrary-room deletion theorem or monotonicity under surgery |
| `reflex-coalescence-proof.md` and peer review | Tail construction with a supplied full-trace convex return, strict sector and ghost-trace clearance | No universal existence of that return; arbitrary collapses need not satisfy its hypotheses |
| `../review/strip-generators.md` | Complete ORTHOGONAL geometric compression/expansion; one-generator tree of <=5 parallel necks | Product coordinate map bends rays; no diagonal coverage or general multi-mouth witness theorem |
| Fixed-neck/tree and joint-growth proofs | Tail/continuation with the stated fixed chamber, routing, prefix and witness conditions | No witnesses on every atlas fiber; nonuniform thresholds cannot be iterated as uniform ones |
| `../review/polyhedral-atlas.md` | All canonical45 marked geometry, including diagonal and noncomb topology, finite module representation | No actual-path transfer along its unbounded integer generators |
| Strict supplied parity-fold exclusion | Under its hypotheses W<=21 forces k<=6 | Actual darkness does not imply existence of such a factor |
| R22 stretch, A23/R23/R24 | Obstructions to specific factor/global-symmetry explanations | No necessity theorem; their negative conclusions do not imply illumination |
| Fixed-shape finite-dark-pair collars | Qualitative neighborhoods for one fixed shape | No uniform collar while shape and marks degenerate |

The geometric atlas already has a primitive, nondegenerate six-wall L sequence with k tending to infinity. Consequently unbounded arithmetic complexity need not appear as a geometric degeneration at all. This is a DISPROVED premise, not just a technical missing estimate.

## 5. Genuinely different mechanism: a global optical cover of metric strata

Instead of surgery, retain every polygon and its original marks in the accepted atlas. Translate S to zero. Fixed directions and positive integer edge lengths with closure, parity and strict simplicity encode every input. Normalize perimeter for a geometric compactification; this does not identify different optical data or bound lattice denominators.

For a FIXED finite reflection word, each wall reflection is affine, with fixed direction matrix and an offset linear in the atlas data. Composition makes the developed actual target affine in those offsets and its actual coordinates. Strict finite-wall ordering, no-corner and interior-leg conditions are semialgebraic, with a finite disjunction if necessary. Any genuine finite specular witness with nonzero flight length and transverse smooth contacts persists in a sufficiently small neighborhood of its own marked data. If an earlier actual target is met, truncate at its first arrival. This is an existence statement retaining the actual endpoint; no fixed sheet is substituted for it.

Thus the illuminated locus is a countable union of legal finite-word cells. A compact subset ALREADY covered by witnessed open cells has a finite subcover. This is useful only after a substantive global continuation theorem. It does not prove the compact set is covered, and the qualifying rational/integer-normalized locus is not itself closed under limits.

The required new implication would have to cover every normalized limiting stratum, including collapsed edges, slit/contact limits, colliding marks and marks approaching corners, AND the nondegenerate primitive arithmetic sequences. It must supply witnesses with a neighborhood that covers nearby ORIGINAL pairs, not only the limit. A proof for all real normalized parameters would be stronger than the stated arithmetic objective and cannot be assumed. Finite direction/sign cells do not remove the countably many optical word boundaries.

This is independent of wall-count surgery, but currently UNSUPPLIED, not disproved. The notch example prevents using automatic fixed-word persistence at a degenerate boundary. The accepted atlas's nondegenerate L sequence prevents restricting the whole analysis to degenerations.

## 6. Recommendation and concrete next positive obligation

ABANDON unconditional collapse-and-lift and automatic compactness shortcuts. Do not abandon the conjecture or count this assessment as universal positive coverage. Retain the exact atlas and actual-pair representation as useful foundations.

A defensible next positive obligation is to identify a darkness-derived constraint on the WEIGHTED atlas or intrinsic return data that is not merely the desired theorem restated. A candidate must handle diagonal and branched rooms and keep full actual endpoint fibers. Before another local path construction, specify how its hypotheses follow for every allegedly dark input. The peer's independent branched-diagonal challenge will test that implication. No further comb catalogue is authorized by this pivot.

B01 has supplied a concrete obstruction to one lifting premise and exposed the exact stronger gap. Universal illumination, existence-only dark-room descent, and uniform optical coverage of atlas parameters remain OPEN. No final independently reviewed universal result is claimed.
