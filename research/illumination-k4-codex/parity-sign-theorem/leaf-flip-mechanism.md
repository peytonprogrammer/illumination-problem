# What the frozen leaf flip changes

[done] Codex, 2026-11-02. Bounded comparison of the original Section33 room and its supplied one-leaf counterexample. No new trajectory, direction, room or word discovery. Calculations only replay supplied contacts and extract frames/portal crossings from existing certificates.

## 1. The changed return and the compensating excursion

Use the same D-start z=(7/6,5/6), v=(-2,-1) in both rooms, with initial unfolding frame I. The original42-contact list is already in peer `b-not-in-k/certificate-3-2.log`. Its direction, supplied first-hit order and frame closure were checked during this comparison. The flipped78-contact list was independently checked previously in `mirror-candidate-check.json`.

In each room the path first exits the pocket through (1,3/4). In the original room its next entry is (1,1/4). In the flipped room its next entry is (1,3/4). The paths first disagree at their20th wall contact near the altered leaf. Thus a remote change reroutes an actual exterior return; the pocket itself and its scattering rule stay fixed.

Group moving hits into complete pocket excursions. Because the start lies on D, the excursion straddling the period boundary is counted cyclically; its last D hit is the final contact of the displayed certificate.

| Room | Excursion words and signed unfolding contributions | Total |
|---|---|---|
| Original | DH: (1,-1); D: (-1,-1) | (0,-2) |
| Flipped | DHDH: (0,2); DH: (1,-1); D: (-1,-1) | (0,0) |

For the flipped first excursion the four moving-hit increments are (-1,1), (2,0), (-1,-1), (0,2), whose sum is (0,2). The later DH contributes (-1,-1)+(2,0)=(1,-1); the closing D contributes (-1,-1). These are all evaluated in the single initial frame, so summation is legitimate. Opposite global frame conventions reverse these displayed signs without changing the conclusion.

The return routing is explicit. Original exterior legs have portal heights 3/4 -> 1/4 and 1/2 -> 1/2. Flipped exterior legs have 3/4 -> 3/4, 1/4 -> 1/4 and 1/2 -> 1/2. The changed first return sends the ray through the longer DHDH scattering channel, followed by another exterior leg before the DH and D channels close it. The flip supplies exactly the missing compensating contribution. This explains the one representative; complete fixed-direction blindness remains established by the preceding all-strip verification, not by extrapolating this representative alone.

Do not describe this as a proved general cylinder-merger operation: the actual flight times change from30 to52, not to the sum of the original two peer cylinder times30+26. A surgery theorem would require interface-state and frame matching across all its branches. No such theorem is supplied here.

## 2. Why (3,2) survives: a witness unaffected by the surgery

The already supplied short flipped-room certificate starts at z=(19/10,1/10), v=(-3,-2), and has contacts

    (7/4,0), (0,7/6), (1,11/6), (3/4,2),
    (0,3/2), (3/2,1/2), (11/6,0), (19/10,1/10).

Its frame and velocity close in8 reflections, and Q=(0,2). Its moving-hit increments are H:(0,2), D:(-1,1), H:(2,0), D:(-1,-1). Their sum is (0,2).

Every point and intervening straight segment lies in x>=0. The two rooms differ only in the triangle leaf with x between-5 and-3. Therefore their polygons and all relevant contacts agree throughout a neighborhood of this orbit. The same exact short certificate is valid in both rooms. It has positive clearance from the altered leaf and avoids physical corners; an open strip around it also survives. This is a geometric reason for detection surviving the flip, independent of the long104-contact cycles.

General conditional fact used: if two polygonal rooms agree in a neighborhood of a supplied nonsingular periodic trajectory, including all contacted walls and the designated moving mirrors, that trajectory and its slide response are unchanged. It is not a theorem that every raw room has such a trajectory near its pocket.

## 3. Assessment and stop condition

The bounded comparison has explained how an exterior rerouting inserts a compensating pocket visit, and has isolated an unchanged local detecting witness in another direction. It has NOT produced a uniform surgery construction, a way to defeat arbitrary finite direction sets, a universal detecting direction family, or actual S/T event coupling.

The cancellation identity is a concrete explanation of the verified counterexample, not new universal proof progress. Further itinerary decomposition is retired absent a new geometric argument. No additional scan or implementation is warranted by this result.

## Evidence

`leaf-flip-mechanism.json` records the extracted moving-hit increments, portal crossings and the short witness. Sources are the existing `mirror-candidate-check.json` and peer's supplied original `certificate-3-2.log`; original aggregate core counts are available in peer `core_loads.json` but are not promoted here to newly independently checked census claims. No peer code was imported. The first attempt to load own checker definitions for certificate replay omitted __file__; that execution failed before replay and was corrected. No geometry or contact certificate was changed.

Independent hand check: replay the listed moving reflections and their signed-permutation frames; compare the supplied exterior crossings and the short witness's x>=0 containment. This assessment used no new optical discovery.


## Independent peer review received

Opus `review-leaf-flip-mechanism/findings.md` accepts the hand mechanism with no corrections. It independently traces the DHDH, DH and D excursions, checks the exterior crossings and divergence at contact20, and derives the seven frame-weighted increments. It also hand-replays the eight-contact (3,2) witness, its frame closure, Q=(0,2), and containment in the unchanged x>=0 portion of both rooms. No discovery search was used.

This peer audit explicitly excludes flight times30/52/26 and does not re-audit complete all-strip coverage. Those scope limits are retained; the peer acceptance is not broader than the stated hand claims. The structural interpretation agrees with the existing pocket-entry model: the pocket response function is fixed, while a remote edit changes the exterior routing of entry states. It supplies no new universal detection theorem.
