# OR03: all-word obstruction to the large-interval criterion at a fixed ear

Author hand result, pending independent review. This supplements OR01; its frozen candidate and proof remain unchanged. No discovery search or computation is needed.

## 1. Necessary depth balance for the sufficient criterion

On the WHOLE J=(l,u), write ell=u-l. From 0<alpha+a*m<w and 0<beta-epsilon*b*m<w, the total ranges obey

    a*ell <= w, b*ell <= w.

This follows by taking limits at the two ends of J; strict interior values do not require strict inequalities for their limiting spans. Set M=max(a,b)>0 and delta=|a-b|. Then

    (a+b+2h)*ell
       <= w*(a+b+2h)/M
       = w*(2+(2h-delta)/M).

Consequently OR01's strict width criterion REQUIRES delta<2h. If delta>=2h, it cannot hold for ANY connected guarded interval, any alpha,beta, or either epsilon. This is a limitation of that sufficient criterion, not a prohibition on exact matching roots or illumination.

Long source/target words do not repair the criterion automatically: their developed positive vertical distances must be within2h of one another, in addition to having overlapping guarded slopes of sufficient width.

## 2. An actual r2 fixed-ear obstruction for ALL exterior reflection words

Let

    B=[-8,24]x[-200,0], E=[0,16]x[0,2], D=B union E,
    S=(4,-2), T=(6,-100).

D is a strictly simple orthogonal integer polygon with ordered vertices

    (-8,-200),(24,-200),(24,0),(16,0),
    (16,2),(0,2),(0,0),(-8,0).

The two mouth corners(0,0),(16,0) are its only reflex corners; r=2. Actual S,T are distinct even-even strict interior points. The direct S-to-T segment lies in the interior of the convex lower rectangle, so this is explicitly NOT a dark-pair counterexample.

For any source branch first reaching M=(0,16)x{0} from outside E, every preceding horizontal physical reflection support is y=0 or y=-200. Reflections in those supports generate y images of an actual ordinate y0 of the form +/-y0+400n. Vertical-wall reflections do not affect y. Thus in the terminal mouth frame the source image is at y=-a with

    a=+/-2+400n,

and a compatible reverse-target image is at y=-b with

    b=+/-100+400m,

for integers n,m, retaining only positive a,b. This includes every finite exterior word, without a word bound or assumption that every abstract word is physically legal. Taking a superset of possible words is sufficient for this obstruction.

Hence a-b=400k+/-2+/-100. Its residue modulo400 is one of98,102,298,302, so |a-b|>=98. Since2h=4, Section1 proves OR01's width criterion impossible through this E for ALL actual source/reverse-target branch words and both signed target charts.

This is stronger than one narrow interval or one failed chosen ray. No longer exterior word can fix this particular criterion for this ear.

## 3. Cutting the mouth closer to the same roof does not repair it

For0<=c<2, replace the chamber by E_c=[0,16]x[c,2] and section M_c=(0,16)x{c}. Its depth is h_c=2-c. Prior to a FIRST M_c crossing from below, no trajectory can reach the roof y=2. All preceding horizontal supports remain0 and-200, even if it uses vertical sides within0<y<c. Therefore

    a_c=c+/-2+400n, b_c=c+/-100+400m.

Their difference has the SAME residue lower bound98, whereas2h_c<=4. Thus every cut of this fixed roof chamber fails the same large-interval criterion. The mouth is an interior section, not a new reflecting support y=c; including reflections there would invalidate the argument.

## 4. Exact consequences and limitations

OR01 remains a correct sufficient local lemma. This actualr2 control excludes automatic global forcing of its width condition from the reflex bound alone at a prescribed chamber, and excludes fixing this fixture simply by lengthening its prefix words or moving the section toward the same roof.

It does NOT refute G8 as stated: this pair is already directly lit, and G8 allows other chambers and applies to pairs not already directly visible. It does NOT show any originalr<=8 pair is dark, and does not exclude narrower intervals that contain an arithmetic matching root. No inference about all physical chambers of D is made.

The constructive programme therefore needs an additional selection theorem or a sharper arithmetic/guard argument for intervals below the sufficient-width threshold. The existing geometric H/V/C1 availability theorem supplies neither. No positive global intersection inequality has been obtained.
