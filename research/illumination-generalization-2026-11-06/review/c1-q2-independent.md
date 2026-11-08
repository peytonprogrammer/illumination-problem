# Independent full acceptance of A48: entire q2,h>=3 branch

ACCEPT the complete q2,h>=3 theorem in its unitwidth/height2 c1 W<=21 comb class. It imposes no bound on height, support or exceptions. It does not cover q1 or h2.

## Entire-room reduction

A38 applies to actual seam marks of equal height2/depth0, even after the integer floor translation. Their relative heights differ by an even integer, so h and mu are integers. All four forced opposite endpoint levels lie in[3,G-3], excluding every flush blocker. The selected teeth are nonflush because q2. At least three distinct levels require at least two height2 teeth, hence two nonflush blockers. Two selected plus two opposite teeth exhaust2N+F<=8. No unused attachment remains.

The ordered level gaps are2,d,2. For d>0 two disjoint height2 bands covering four levels must pair the lower two and upper two. Other pairings interlace or leave distant outer levels. For d0, reflection makes one band[h,h+2]; a band covering h+4 must extend outward to h+6, since inward extension would touch the first. Vertical reversal preserves the actual pair and normalizes s2. The resulting complete rooms are exactly stated A0 or A1. Nonflushness gives h>2; integer h>=3. The core has no strict interior integer x, its other seam has odd x, and unit teeth have no interior integer x, so exactly the two actual A marks follows after normalization. It was not an imposed support cap.

## Infinite parameter coverage

The three-turn formula has absolute slope h/2, with first right contact below h when h>4 and left contact strictly between3 and2h+1. Only its last right contact can fail, exactly when2d<=h<=2d+4. In this strip with d>=5,h>=10, the seven-turn path is strict: lower two right contacts are below h since h>8; third is above h+2 but below h+d+2 since h/4<d; last exceeds h+d+4 since3h/4>d+2. These inequalities hold at both equality edges for d>=5. All intervening left turns lie between selected bands, all open core legs have0<x<1, and y increases to actual T.

At h4 the floor path has absolute slope3; its floor contact2/3 is strictly between0 and1, and right levels1,7 avoid both mouths for every d>=2 and for A0d0. The left turn4 is smooth. The sole excluded A1 case h4d1 is included separately.

For h3,d>=2 the twelve-reflection fixed path is legal in the actual room: the added second right opening starts d+5>=7, while all right core contacts are at or below6. Every open part above6 lies in the open core or selected upper-left tooth; the actual roof d+10 is strictly above its maximum9. Thus no artificial cap reflection or general attachment monotonicity is used. I separately checked its full20-wall path at d2,d3 and d1000000.

For h>=5 with d1..4 the integer exceptional strip has exactly16 cells:2+4+5+5. The A1h3d1/h4d1 and A0h3/6/8 cases complete exactly21 isolated certificates. A0h5/h7 have the peer's independent prefix acceptance, and all remaining A0h>=9 use the strict three-turn formula. These cover every A0integerh>=3 and A1integerh>=3,d>=1.

## Independent exact evidence

I rebuilt each entire20-wall polygon from the displayed core and bands, compared its unordered edge cycle with the stored polygon, checked actual endpoints/initial direction/wall indices, and replayed all finite legs with the separate Fraction checker. All21 exception certificates pass672 reflections and13860 wall-leg guards. Three full-room h3 transports and nine hand-formula controls give33 total paths,754 reflections and15740 guards. None is counted as independent evidence of unseen parameter cells; the full parameter proof is the hand argument above. No peer optical code or discovery search was executed.

All logical dependencies are accepted separately. This closes the entire q2 branch by contradiction with its exhaustive entire-room reduction. The native universal goal remains OPEN.
