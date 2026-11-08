# Supplemental correction to the frozen equal-depth proof and review

Codex01a1a00f. The frozen parent equal-depth/proof.md Section4 and the frozen
equal-depth-independent/review.md Section4 both give the wrong portal
coordinate for their q4center example. The correct coordinate at BOTH
portals is3/2, not7/4. My earlier independent review repeated the error.
Neither frozen file is changed; read this supplement with those sources.

The stated path is
(1,-1/2)->(5/2,1)->(3,1/2)->(5/2,0)->(1,3/2).
Its first segment has dx=dy=3/2, so at y0 its x is1+1/2=3/2.
Its final segment has dx=-3/2,dy=3/2; at y1 its x is5/2-1=3/2.
Both crossings remain strictly in(1,2). The three reflection points and
specular directions are unchanged and valid. The old exact physical checker
already used these correct path coordinates and passed; the error is in
the prose portal value, not the actual construction or its validation.

The own outer-leg-transfer-check.py independently computes both crossings
by exact segment interpolation, records them in equal-depth-portal-erratum.json,
and validates the actual path through the all-edge geometry checker as
part of the transferred-path controls. This supplemental correction reconciles
the numerical finding. The accepted equal-depth theorem and its outer-simple
property remain valid; no full unequal-depth conclusion follows.
