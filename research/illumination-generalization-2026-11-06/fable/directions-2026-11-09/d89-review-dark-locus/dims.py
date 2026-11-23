# Exact dimension bookkeeping for dark-locus.md, r = 1..8. No rooms are searched.
from fractions import Fraction as F
print("r  g  dimQ  H1-  dimH(2^r)  k_allowed  max_cover_rank")
for r in range(1, 9):
    g = r + 1                       # orientation cover of Q(1^r,-1^(r+4)): 2g-2 = -4 + (2r+4)
    assert 2*g - 2 == 2*(-2) + (2*r + 4)
    dimQ = -2 + (2*r + 4)           # genus-0 quadratic stratum: 2*0-2 + #singularities
    h1minus = 2*g                   # H^1 of a sphere is 0, so H^1_- is all of H^1
    assert dimQ == h1minus          # no rel in the unmarked quadratic stratum
    dimH = 2*g + r - 1              # H(2^r): 2g + #zeros - 1
    ks = [k for k in range(2, g + 1) if F(k) < F(g, 2) + 1]
    cover = F(g + 1, 2)             # rank <= base genus h <= (g-1)/2 + 1 for degree >= 2 covers
    assert cover < F(g, 2) + 1
    print(r, g, dimQ, h1minus, dimH, ks, cover, "component case possible" if dimH == dimQ else "")
