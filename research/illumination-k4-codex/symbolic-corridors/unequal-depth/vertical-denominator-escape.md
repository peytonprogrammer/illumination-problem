# Escaping equal odd depth denominators with a vertical shear

Codex01a18403. Candidate conditional reduction, independent review required. It depends on the frozen one-fiber transport and horizontal denominator theorem, which are themselves pending review.

Normalize d=g=1. Suppose all six parameters are rational, 0<s,t<1, and put delta=gcd(h_-,1,h_+). Write

    Hm=h_-/delta, Hp=h_+/delta, G=1/delta,
    Htot=Hm+G+Hp,
    Lambda=lcm(Hm,Hp,G,Htot), C=2Lambda, K=delta*C.

These H quantities and Lambda,C are positive integers; K is an even positive integer because Lambda is divisible by G. K is an integer multiple of the four vertical cylinder circumferences 2h_-,2h_+,2,2(h_-+1+h_+). Thus the accepted vertical-twist construction gives an affine automorphism V of derivative [[1,0],[K,1]], fixing all vertex lifts including regular convex corners.

Assume the two depth ratios A=a/delta and B=b/delta have the SAME odd reduced denominator q. This is one of the residual strata in one-fiber-transport.md.

## A sufficient denominator-growth condition

Set

    n0 = denominator((K/h_+)*t),
    E  = denominator(C*n0*s),

where denominator always means reduced positive denominator. If s!=2/3 and some prime has strictly greater exponent in E than in q, then the original pair illuminates.

There is a symmetric criterion obtained by exchanging source and target chambers:

    m0 = denominator((K/h_-)*s),
    E' = denominator(C*m0*t).

If t!=2/3 and E' has a prime exponent strictly exceeding that in q, illumination follows as well. Both criteria are sufficient; their failure is not darkness or failure of every affine mechanism.

## Proof of the first condition

By the definition of n0, the displacement n0*K*t is an integer multiple of h_+. On all four target lifts, the signed displacements are plus or minus this quantity. Modulo the target cylinder's period 2h_+, these signs agree. Thus V^n0 maps the ENTIRE T fiber onto the fiber of one interior physical T', at the same horizontal coordinate t and with depth either b or h_+-b. In units delta, the new target depth has reduced denominator exactly q, since Hp is an integer.

Choose the identity lift of S. The image under V^n0 has physical source depth

    a' = F_(h_-)(a-n0*K*s),

where F_h is the triangular fold into [0,h] of period 2h. Its horizontal coordinate remains s. In units delta, the developed depth before folding is A-C*n0*s. The folding only changes its sign and adds an integer multiple of 2Hm.

Take a prime p whose exponent in E is strictly larger than its exponent in q. In p-adic valuation terms, C*n0*s has strictly more negative valuation than A. Their difference therefore has exactly that more negative valuation: multiply by the larger p power to see a numerator not divisible by p. Folding preserves this denominator exponent. Consequently the new reduced denominator D of a'/delta has a prime exponent strictly larger than q's. In particular D!=q, and D is not a divisor of q. The image source cannot lie on a horizontal boundary: those depths have integral values in delta units, whereas this image has denominator D>1. Thus S' is interior.

The transformed endpoints still have 0<s,t<1. If D is even, the horizontal denominator theorem applies immediately. If D is odd, the denominators D and q are distinct. Its only possible exclusions are (i) D=3q and s=2/3, or (ii) q=3D and t=2/3. Exclusion (i) is ruled out by hypothesis. Exclusion (ii) is impossible because D has a prime exponent larger than q. Therefore S',T' illuminate.

Use the one-fiber transport lemma in reverse endpoint order: the full T fiber has coalesced, while the chosen S image is interior. Lift the transformed connection from that chosen source image and end at some T' lift; the inverse of V^n0 returns its endpoints to actual original S and T. All forbidden vertex lifts are fixed. This proves the stated criterion.

## Exact arithmetic illustration

For h_-=h_+=2, delta=1, Lambda=10 and K=C=20. Choose

    a=1/3, b=2/3, s=1/7, t=1/5.

The original depths have common odd denominator q=3. Here n0=den(10/5)=1 and E=den(20/7)=7, so the condition holds. The new source depth is F_2(1/3-20/7)=31/21, while the target depth is still 2/3 because 20t=4. Denominators 21 and 3 differ by a factor 7; the horizontal shear reduction then applies. This illustrates the general valuation argument and is not its proof.

## Remaining gap

This reduction does not cover equal-odd-denominator data when both coalescing vertical shears introduce no new prime-power denominator, nor all horizontal coordinates 2/3, nor the mixed centered cases outside the general one-fiber orbit criterion. In particular shared torsion denominators can survive both shear reductions. A uniform arithmetic or geometric argument is still needed; no finite denominator cutoff or full goal completion follows.
