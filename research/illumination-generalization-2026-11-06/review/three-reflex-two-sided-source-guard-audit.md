# SG01: an accepted successful source prefix is cut well before a full gate sweep

Status: exact prescribed-control evidence plus a HAND guard-interval argument, offered for independent review. This challenges an automatic-width inference for SC01. It does not refute SC01's conditional sufficiency, universal availability of SOME OTHER branch, or illumination. No new room/direction search was performed.

## The unchanged accepted input

K1R01 room (a,l,w,A;b,c,h,H)=(12,20,28,32;1,3,4,5), actual S=(8,4),T=(24,2). The ONLY physically replayed direction is the already accepted tau=369232/1923=192+16/1923, with first actual T at normalized vertical time3846. Existing reviewer earliest-wall and whole-path guard routines reproduce47748 ordinary reflections and path hash a4f18c0022a6ed0149887720e05bf978f25c69a9251a0b0e128d02b4bc706e12. The only extracted scope assertion omitted is the old single-roof assertion, exactly as in the accepted two-sided review. No author checker/main or different direction was executed.

Its final negative/downward R-cap crossing is

    D_S=3364,
    x_h=53864/1923=28+20/1923,
    C=56, alpha=C-w=28,
    z0=1923/16,
    q_S=28z-3365, q_S(z0)=1/4.

There are39844 actual reflections before this cap state. The final safe preturn target tail has m=80, downward target sign, and duration6m+h-v=482. Thus D_S+482=3846 exactly; at the matched parameter Theta=32z-3365=481=6*80+3-2. This is a literal safe target gate root, not a fitted coefficient.

## The actual regular source component is narrow

The affine gate alone would permit

    3365/28 < z < 3371/28,
    0<q_S<6.

However the connected regular fixed-prefix component through the accepted witness, after intersection with that gate, is only

    3365/28 < z < 601/5,
    0<q_S<3/5.

Its q=0 boundary is the future target-gate endpoint, where the subsequent bottom entry would meet(w,c). The OTHER boundary is an earlier actual SOURCE-prefix reflex failure at physical corner(w,h)=(28,4), at prefix developed time2404. In the relevant unfolded copy that physical corner is(461596,2408), so

    tau_corner=(461596-8)/(2408-4)=115397/601,
    epsilon_corner=5/601,
    z_corner=601/5.

At the accepted direction the unfolded ray at that same vertical time misses this image by exactly4/1923 in horizontal coordinate: (16/1923-5/601)*2404=4/1923. The corner is not an artificial section endpoint or a new physical blocker. Repeated image appearances do not count as new distinct corners.

For this component the target phase span is

    (alpha+w-t)*length(J)=32*(601/5-3365/28)=24/35,

while the paired-target maximum gap is2max(v,c-v)=4. Thus this successful prefix FAILS SC01's sufficient width test, although it contains its particular exact target root. The test is sufficient, not necessary. In particular neither existence of a successful ray nor existence of a regular source gate state guarantees that its parameter component spans the full gate or exceeds the residue-gap threshold.

## How the interval was checked

The prescribed checker unfolds the ACTUAL fixed reflection word copy by copy, using coordinate sign changes and integer translations at its actual finite walls. It does not launch any alternative billiard ray. In each visited copy it considers the images of the ten ACTUAL room vertices. A candidate parameter for a vertex image(X,Y) is tau=(X-s)/(Y-u), with positive developed timeY-u. It is retained only if that time lies between that copy's preceding and following prescribed wall times AT THAT CANDIDATE PARAMETER, and before the final cap stop D_S. This time qualification is essential: arbitrary developed vertex slopes outside their traversed segment are not prefix obstructions.

Inside the full gate parameter interval there are six such qualified vertex incidences, counting visited-copy occurrences. The nearest one on the smaller-epsilon side is the stated(w,h) incidence; on the larger-epsilon side the future gate boundary is reached first. The source interval follows by taking the adjacent forbidden parameters around the accepted ray and intersecting with the geometric gate.

Why this gives the fixed-prefix regular component: all nonaxial finite specular words depend continuously on slope until a first-hit domain changes. With all contact times ordered and each finite-wall contact ordinary, such a change in a simple orthogonal polygon must encounter a true wall endpoint; interior grazing cannot occur while tau>0 and |vy|=1. The developed corner at the first boundary belongs to its traversed copy and segment by the time test. Conversely a qualified developed corner cannot lie strictly inside an otherwise regular word component: that straight segment would then actually meet the physical vertex. Hence the nearest qualified corner parameters, together with the final gate boundary, delimit this component. This is an interval statement for the ONE fixed actual word, not a complete full-ray parameter census.

The source guard endpoint may admit another itinerary after changing slope, or a different source prefix may be wider. Those are not certified here. A chosen-word failure is not failure of existential rerouting. No convex singular continuation or reflex repair is used.

## Effect on the research frontier

SC01 remains a conditional optical lemma pending independent review. A global argument would need to produce a sufficiently wide source component for EACH pair despite prefix corner cuts, or establish some OTHER actual intersection mechanism. It may not infer width by extending one successful prefix through the reflex endpoint shown here. The component can contain a target root without meeting the width threshold, so failure of that threshold supplies no dark control.

The concrete new evidence is the actual earlier-corner cut and its exact interval, not a new positive family or room-coverage result. All full ordered/r3/r<=8 goals remain OPEN. The checker had one hard840-second parent timeout and completed successfully; no restarted effort, new discovery clock, new engine, worker, frozen edit or git change. Existing computational dependencies are disclosed and pinned; independent peer review is pending.
