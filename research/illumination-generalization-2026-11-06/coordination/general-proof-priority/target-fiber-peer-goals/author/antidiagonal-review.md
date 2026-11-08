# Independent antidiagonal noncompression audit

Decision: ACCEPT all five requested claims, with no material findings. No numerical run was made. The negative theorem applies to every odd d>=3 in this specified family; the combined four-original-direction exclusion uses the earlier diagonal theorem only when d=3 modulo4.

This is an internal scoped review. Native get_goal reports the SAME goal BLOCKED; no user resumption, activation, accounting reset or objective change is inferred.

## 1. Actual conjugacy and critical-circle phases

Applying genuine Rx to a putative original antidiagonal path sends its source to p'=(-2d+1,1) and its chosen original target gq to Rxgq in Gq. A purported compressor F becomes F composed with Rx on this transformed path, giving exactly the same seed. Both endpoints are transformed before compression. This uses RxG=G and Rx squared equal to identity; it does not commute F with G or substitute G F(q).

Take the accepted r=2 limiting cylinder-2 boundary table. Its signed representatives after translations occur at times

0: (d,d-2);
2: (d+2,-d);
d+1: (-2d-1,-1);
3d+3: (1,-2d-1);
4d+2: (-d,-d-2);
6d+2: (d,d-2).

On the third displayed interval, adding time 2 to (-2d-1,-1) gives p'=(-2d+1,1), at total phase d+3. Adding time 2d instead gives ORIGINAL Rxq=(-1,2d-1), at phase 3d+1. Adding time d+1 gives the true cone (-d,d), at phase 2d+2.

These are actual signed-cross representatives, not projected copies. For every d>=3,

d+3 < 2d+2 < 3d+1.

The boundary table is a limiting singular parametrization; it is not a globally regular periodic orbit through the cone. It can overapproximate candidate target times, but legal paths are stopped at the first cone.

## 2. Exhaustion of the other original target choices

On the successive open pieces of that table, x-y is respectively 2, 2d+2, -2d, 2d+2, and 2. These are the only possible signed differences. The source p' and Rxq occur on the piece with difference -2d.

The remaining actual interior target lifts have differences:
q: -2d+2;
Jq: 2d-2;
Ryq: 2d.

None equals any of {2,2d+2,-2d} when d>=3. The one potential equality 2d-2=2 would require d=2, outside the family. Interior lifts have unique signed representatives; boundary-translation alternatives cannot add another occurrence of these points. Rxq itself occurs only once on the piece with difference -2d because both coordinates increase strictly there.

Thus the only possible target on the transformed source's regular boundary arc is Rxq. No original target-lift choice was omitted.

## 3. True-cone interception and signed times

With T=6d+2, candidate times on the chosen limiting circle satisfy

tau=2d-2+nT.

Every positive candidate has n>=0. The first forward true-cone time from the source is (2d+2)-(d+3)=d-1, strictly earlier than the smallest positive target time 2d-2. Therefore EVERY positive candidate is singular. Following the limiting circle through the cone cannot turn it into a regular optical path.

Any negative candidate has n<=-1, hence

tau <= 2d-2-(6d+2) = -4d-4.

Its absolute time is at least 4d+4. Further cone or regular-corner contacts may eliminate such candidates; they cannot introduce a shorter connection. The argument does not claim that arbitrary negative repeats are regular. Every legal connection is contained in the cone-free boundary arc dictated by its initial signed direction, so the table overapproximation is sufficient.

## 4. Full-affine content contradiction

In normalized coordinates the exact period lattice is 2Z², as already independently accepted. For any legal transformed connection the developed holonomy is tau(1,1), with even tau. Its intrinsic lattice content is m=|tau|/2>=2d+2.

A genuine global affine map acts unimodularly on this exact period lattice. Its image holonomy is consequently 2m times a primitive nonzero integer vector. If the image were contained in the closure of one copy, each coordinate displacement would have absolute value at most A=2d+1. Since a primitive vector has a nonzero integer component, that would force m<=floor((2d+1)/2)=d.

The inequalities m>=2d+2 and m<=d contradict each other. This rules out EVERY global affine compressor, including reversing maps and smooth-wall-aligned seeds. No preservation of a finer tiling is required. Reflection Rx itself is unimodular on the same lattice, so conjugating the original antidiagonal path does not change the content. Native dilation by 2 scales holonomy and the period lattice together, leaving the contradiction unchanged.

This part requires no new foliation-stabilizer classification.

## 5. Original axes and the exact combined statement

The horizontal orbit through original p has signed y=1, staying in the full-width horizontal cylinder with |y|<d. Horizontal boundary translations cannot change that y coordinate. Every gq has |y|=2d-1>d, so no horizontal connection reaches any target lift.

The vertical orbit through p stays at x=2d-1 in the right-arm vertical cylinder, with d<x<A and vertical period 2d. Every gq has |x|=1<d and is in the other vertical cylinder. There is no vertical connection to the actual target fiber. Any forbidden corner cut would only remove paths and cannot repair this non-access.

For d=3 modulo4, the earlier independently accepted theorem excludes affine compression of every original diagonal connecting path. The present argument excludes every original antidiagonal connecting path, and the original axes have no target connections at all. Hence ANY successful inverse-affine seed connection must have ORIGINAL unfolded direction outside the axes and both diagonals.

This constrains the original connection direction, not merely the image direction of F. It remains a necessary restriction only. The known one-left-reflection path has slope -(d-1)/d and is outside the four excluded directions. Its compressibility, other uncontrolled connecting directions, the existential full-target-fiber gate and the broad r<=8 theorem remain unresolved. No darkness or all-direction exclusion follows.

## Conclusion

ACCEPT all five scoped questions and the combined statement. The submitted pins match before and after this hand audit. There was no numerical run, direction or room search, orbit census, engine, worker, frozen-source edit, git mutation or discovery-clock restart.
