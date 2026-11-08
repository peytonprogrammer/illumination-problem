# Explanatory correction to the frozen all-affine rank proof

The frozen weighted-return-all-affine-rank.md says in its arithmetic-bound section that a Euclidean-norm lower bound alone would be insufficient for this L1 conclusion. In this setting that explanatory claim is incorrect. The independent peer identified the omitted integrality step; the finding is accepted and resolved here. Preserve the original frozen source and its pins.

For a primitive integer direction (p,q), rho=|p|+|q| is an integer and satisfies

    rho >= sqrt(p^2+q^2) >= sqrt(n^2+1) > n.

Therefore rho>=n+1. The actual direct direction (n,1) attains rho=n+1. Thus the previously accepted Euclidean lower bound, together with integrality, also establishes the minimum used in the all-affine rank corollary. The direct all-reflected-image congruence proof in the frozen source is valid independently and additionally records n|p and nonzero components.

Replace the explanatory interpretation of the frozen sentence with: “The all-image proof establishes the relevant L1 minimum directly; the earlier Euclidean-norm bound plus the integrality of rho supplies another proof of that same minimum.”

No theorem, endpoint/sheet condition, all-n quantifier, affine-map class, rank conclusion or scope caveat changes. In particular equality rho=n+1 implies the component magnitudes n and1 by the direct congruence proof, and the statement still rules out only same-rank descent on the same actual marked family. It does not establish the full r<=8 illumination theorem or exclude other weighted ranks, terminal classes or transported surface/marking schemes.

Verification: hand inequalities above; no new numerical check, search, engine or author-code execution.
