# Clarification of the irrational-depth step in finite-support-theorem.md

Read this supplement with frozen finite-support-theorem.md (sha256577c9d57c6771a105eb63730e37ab2c8a6f6549262420a7407caba3c72a33fe0).

Its first paragraph under "Uniform reductions before computation" is too broad: the accepted phase-lines theorem gives illumination for every irrational depth pair, but its two centered exceptional relation rows use cap repairs, rather than vertical-only charts. Thus one must not conclude globally that EVERY vertical-only failure has rational phases.

The required corrected argument is:

First suppose the depth pair lies OUTSIDE the10critical lines in the theorem statement. If either depth is irrational, Sections1-3 of phase-lines.md supply a strict vertical-only chart, except possibly its two centered rows alpha=1/2 or beta=1/2 at s=t=1. Those rows are respectively a=b+1 or b=a+1, which are excluded critical lines. Therefore a vertical-only failure OUTSIDE the10critical lines has rational phases. Apply the new lattice/margin/finite-certificate reductions to this rational case.

This proves exactly the originally stated10lines-plus11points support condition. The correction changes the order of the reduction and its intermediate claim; it does not change the final support statement, computations or frozen hashes. The centered irrational failures on the two critical lines were never omitted from that support.
