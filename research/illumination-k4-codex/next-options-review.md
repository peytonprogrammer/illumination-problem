# Review of Opus’s next-work proposals

[done] 2026-11-01. Source review and hand algebra only. No new enumeration, SAT, rays, directions or reflection-word discovery. No independent rerun of the historical n6 enumeration. The literature note was read; its external-source coverage claims were not independently audited here.

## Recommendation

Prioritize a precise structural question over another bounded room search. Codex should continue the already claimed U-room singleton-blocker theorem. Opus should first reconcile his proposed 30–60–90 family with his earlier strict-family exclusion, then examine whether folding boundary marks opens a genuinely broader class. Before enumerating that class, prove its seam-transport criterion and a useful wall bound. k5 is a worthwhile bounded fallback, not the strongest route to a global mechanism.

## 1. The proposed strict n6 family was already examined

Sources: `../claude-illumination-check/research-brief.md` §3 and `../claude-illumination-check/tokarsky-n/claude_n6_enumerate.py`, with persisted `claude-n6-enumeration.json` (paths relative to .context).

The code seeds a full A star and branches on contiguous local sectors: B has 1,2,4,5 triangles; C has 1 or3; A is unrestricted. These are precisely the stated strict 30–60–90 rules forbidding smooth/interior B/C points. Its saved receipt reports 5,975 nodes,416 closed configurations,max24tiles,no second full A,and no window hit. The research brief explicitly concludes no strict simple room with two interior A marks. This review confirms the overlap in scope; it does not independently certify that historical exclusion.

Absence of a published search does not make this an unexplored branch in our project. An audit of the existing exclusion could be useful, but a port of enum2.c should not start until the difference in class is explicit. The brief’s old global minimum24 wording is superseded and must not be revived.

A potentially broader class is a base with boundary A marks, interiorized by reflected copies, or transparent B/C exceptions. The historical two-interior-star exclusion alone does not exclude these.

## 2. A concrete obstruction to transferring the folding proof

At a transparent smooth lift formed from q=pi/theta wedge sectors, the two physical half-rays through the lift are separated by pi. Write F_theta(t)=dist(t,2theta Z), the folded angular coordinate in[0,theta]. Retracing requires F_theta(t+pi)=F_theta(t).

For theta=90degrees,q=2, and theta=30degrees,q=6, this holds: pi is a multiple of2theta. For theta=60degrees,q=3,

    F_theta(t+pi)=theta-F_theta(t).

These rays coincide only on the wedge bisector. Thus a smooth lift made from three60degree sectors does NOT generically project to retracing. This is a local angular calculation, not an exclusion of all such rooms. It blocks the automatic transport of our 45degree proof. A candidate class must prohibit these lifts or supply a different argument for them. Interior lifts require their own treatment; this calculation only concerns smooth boundary lifts.

This is a specific theory task for Opus, with a useful outcome even if negative.

## 3. k5/k6 bounds are sound, with a substantial new branch

From the independently accepted bounds at W<=21,

    I <= floor((15+2k)/6),
    N <= floor(4(19+2k)/3).

| Exception cap k | Full stars I, upper bound | Triangles N, upper bound |
|---|---:|---:|
|4|3|36|
|5|4|38|
|6|4|41|

These are conservative necessary bounds, not existence claims. k5 already introduces I=4, so extending only the old I2/I3 support list is incomplete. The support inequality P+m<=floor((21-4I+2k)/2) remains available, but full-star support coverage must be proved afresh, including disconnected overlap graphs if allowed by its budget. Estimate runtime only after counting supports and preparing the reduction; no basis here for promising completion in one session. A k5 theorem still leaves k>=6 open.

Sources: `persisted-replay/findings.md` and `bounded-proof/support-proof.md` in this directory.

## 4. Classification is an aspiration, not yet a reduction

“No alternative found” for rotation gluings and mixed-class marks does not show every dark pair folds onto a parity base. The proposed necessity of retracing is the missing theorem itself. Define the exact canonical45/mark hypotheses, formulate a falsifiable local necessity lemma, and test it by proof before treating this as a global-minimum route. Do not infer classification from known examples.

## 5. Disjoint next tasks

- Codex: continue `two-reflex-blocker/u-portal.md`, checking the one-crossing portal parameterization and deriving conditions for avoiding one specified horizontal-wall point. A proof or a precise obstruction to this restricted family both count as progress. No claim that all U rooms illuminate follows yet.
- Opus: reconcile strict n6 scope, then prove the smooth60degree seam transport condition or a no-go result for the proposed folded subclass. Supply a wall-budget argument before any new enumeration.
- k5: retain as an optional bounded-computation project after scope and authorization are settled.

The immediate aim is an accepted new structural lemma. This is not a promise of a smaller room or a global lower bound.
