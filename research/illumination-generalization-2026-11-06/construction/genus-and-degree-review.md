# Independent hand review: topology bounds and primitive degree

Codex01a18403, 2026-11-06. Verdict ACCEPT under the stated genuine-corner/minimal-unfolding conventions. Frozen peer genus-and-degree.md SHA256 ae9170847bc65ec49ad45eb13300dccbb2b7bc4dd5159a3480621acef5d96db5 unchanged. No program execution or new literature needed.

Use peer notation |Gamma|=2N, N=2or4. After merging straight walls, every corner angle is m_i*pi/4 with m_i in{1,2,3,5,6,7}. The reduced denominator is n_i=4/gcd(m_i,4). Cycling2n_i reflected sectors gives one lift of angle2pi*m_i/gcd(m_i,4), and there are N/n_i such lifts. Including regular corner marks, the count is |Sigma|=(N/4)(W+e), since gcd is1at oddm_i and2at evenm_i. Gauss--Bonnet then gives2g-2=(N/4)(3W-e-8). This independently matches our direction-skeleton corner-prong count: |Sigma|+(2g-2)=N(W-2).

For N=2 only a perpendicular pair occurs; angles have m_i2or6, W even, e=W. Hence g=(W-2)/2<=9 and |Sigma|<=20 atW<=21. For N=4 there are at least two odd corners, and their number is even because sum m_i=4W-8 is even. Thus e<=W-2 and e has the parity ofW. For oddW<=21 the largest possible genus bound is (3W-7)/2<=28; for evenW<=20 it is (3W-6)/2<=27. Also |Sigma|<=2W-2<=40. These are safe bounds; existence of extremal shapes is not required or inferred.

For the six-wall L family, the four-copy unfolding has area4(2L+1), one angle6pi cone and five regular corner marks. All chart transitions are even translations, so closed-curve holonomies lie in2Z^2. Choose a non-corner horizontal closed orbit in the upper thin vertical arm: its two vertical-wall reflections close its copy and velocity, with displacement(2,0) in the development. A vertical orbit in the right thin horizontal arm similarly gives(0,2). Thus the FULL period lattice is EXACTLY2Z^2, not just a convenient sublattice.

A translation cover to a torus of lattice Lambda_target requires every absolute holonomy in Lambda_target, so Lambda_absolute is a sublattice of Lambda_target. This makes the target covolume at most4 and the covering degree at least area(M)/4=2L+1. The period torus itself attains equality. An invertible global linear change multiplies surface area and covolume by the same determinant magnitude, so this minimum primitive degree is affine invariant and unbounded despite g2,W6.

This rules out turning the bounded-genus/forbidden-mark estimate into a bounded primitive covering degree. It does not obstruct a directionwise O(W) skeleton carrying unbounded integer lengths, and it does not establish a dark pair or any wall minimum.
