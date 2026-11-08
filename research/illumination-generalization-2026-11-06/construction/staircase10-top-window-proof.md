# ST10-B: actual illumination from two partial windows and the real roof

Author hand proof, pending independent review. The candidate was declared in staircase10-top-window-candidate.md before this proof. This is a quantified optical theorem at the stated metric/placement scope, not all staircase10 or broad r<=8 completion.

## 1. Statement

Take arbitrary real 0<w3<w2<w1<w0 and 0=y0<y1<y2<y3<y4=H and the four-band original room P. Define

 g1=y2-y1,
 E2=min(2w2,w2+w1*g1/y1),
 r=E2*y3/(2y2),
 E3=min(2w3,2r,r+w3-w2).

If

 (H/y3)*E3 >= 2w3,                            (B)

then every distinct actual interior pair with at least one endpoint at height >=y3 illuminates by a finite ordinary path using genuine vertical walls and at most one genuine outer roof reflection. This includes all source bands and internal-seam placements. Actual real endpoints are allowed; native even-even pairs are included.

Condition B implies E3>0, hence r+w3>w2. We never assume that an intermediate portal window is full. No source-width restriction other than actual interior placement is imposed.

Put F_w(z)=distance(z,2wZ), the triangular fold into [0,w]. A common unfolded horizontal speed tau>0 and vertical speed1 will be selected jointly.

## 2. Interval-overlap fact

Two open intervals of radii R,a>0 with center distance delta<R+a have intersection length

 min(2R,2a,R+a-delta).

This follows by taking the larger lower endpoint and smaller upper endpoint. If an interval center is rounded to a nearest multiple of 2w, then delta<=w. Therefore, whenever R+a>w, its overlap with the radius-a interval around that nearest multiple is nonempty and has length at least

 min(2R,2a,R+a-w).                            (O)

No continuity across a corner is used: these intervals impose strict portal inequalities.

## 3. Source in the bottom band: first two strict portal windows

Write S=(s,u),T=(t,v), with 0<u<y1,0<s<w0 and y3<=v<H,0<t<w3. Define Tj=yj-u>0 for j=1,2,3, and choose C1=2w0. The open positive interval

 J1=((C1-s-w1)/T1,(C1-s+w1)/T1)

makes the first signed portal phase z1=s+T1*tau-C1 lie in (-w1,w1). Positivity follows from 2w0-s-w1>w0-w1>0.

At y2 the phase before the width-w1 period subtraction is U2=s+T2*tau-C1. Its image of J1 has radius

 R2=w1*T2/T1=w1*(1+g1/T1)>w1>w2.

Its center is rounded to a nearest multiple K1 of 2w1. Center distance is at most w1. Formula O gives a nonempty overlap with (K1-w2,K1+w2), of length

 ell2 >= min(2w2,R2+w2-w1)
      = min(2w2,w2+w1*g1/T1)
      >= E2.                                  (1)

The simplification drops 2R2 because R2>w2. Its inverse image J2 is a positive open subinterval of J1. On J2 the second signed phase z2=s+T2*tau-C2, C2=C1+K1, is strictly inside (-w2,w2). All earlier guards hold with the same tau. Since u>0, T1<y1; the strict improvement is available whenever (1) is not saturated at 2w2.

## 4. Third narrowing: a second partial overlap

At y3 use U3=s+T3*tau-C2. Its image of J2 has radius

 R3=ell2*T3/(2T2).

Because u>0 and y3>y2,

 T3/T2=(y3-u)/(y2-u)>y3/y2,
 R3>E2*y3/(2y2)=r.                            (2)

Round its center to a nearest multiple K2 of 2w2. The center distance is at most w2. Condition B gives r+w3>w2, so R3+w3>w2 and O applies. Its strict third-portal overlap has length

 ell3 >= min(2w3,2R3,R3+w3-w2) >= E3>0.        (3)

Let J3 be its inverse image inside J2. Every tau in J3 is positive and satisfies ALL three original strict portal bounds. Put C3=C2+K2; the final entry phase is z3=s+T3*tau-C3 in (-w3,w3). No assertion that J3 maps onto the entire final portal is needed.

## 5. Joint actual-target choice through the original roof

Reflect the target height across the actual roof, giving developed final height 2H-v. Put D=2H-v-u and Z=s+D*tau-C3. Its image of J3 has length ell3*D/T3. Since v<H and u>0,

 D/T3 > (H-u)/(y3-u) > H/y3.

Together with B and (3), this proves STRICTLY

 length Z(J3) > E3*H/y3 >= 2w3.                (4)

The exact images of actual target t under F_w3 are {t+2mw3,-t+2mw3:m integer}. Successive gaps are 2t and 2(w3-t), both strictly below 2w3 because 0<t<w3. Hence the open interval Z(J3) contains an actual target image Y strictly. Choose

 tau=(C3+Y-s)/D.

It lies in J3 and satisfies every earlier portal guard at the SAME slope. Target-image choice is made after the common portal interval is fixed; no independent source/target rays are concatenated.

For an explicit finite selection, take the next element strictly above the lower endpoint from each of the two arithmetic progressions, and choose the smaller. By (4) it is strictly below the upper endpoint.

## 6. Source in the other bands and source/target seams

If y1<=u<y2, assign the source to band1, where actual interior requires 0<s<w1. Start directly with the positive full second-portal interval

 J2=((2w1-s-w2)/(y2-u),(2w1-s+w2)/(y2-u)).

Its second-portal image length is exactly 2w2>=E2. The proof of (2)--(4) then applies unchanged. This includes u=y1 and every actual horizontal source position, including ones beyond w2.

If y2<=u<y3, only one narrowing remains. The positive full third-portal window from source band2 has signed entry range (-w3,w3). At the actual target height v>=y3 its monotone target-phase image length is at least 2w3. The same two-progression gap argument selects a strict actual target image. This is the accepted one-narrowing construction, with no roof contact needed. It includes u=y2 and v=y3.

If u>=y3, both endpoints lie in the convex top rectangle and the direct segment is interior. Equal-height pairs also use the direct horizontal segment. If necessary reverse the required connection to place the top endpoint last; billiard reversibility preserves every physical guard.

An actual source on a band seam belongs to the narrower upper band and satisfies strict x<that band's width. A target at v=y3 satisfies 0<t<w3 and is interior to P. It is not replaced by a boundary point of a subroom.

## 7. One physical ray and every corner/first-hit guard

For a bottom source, use the horizontal folds

 F_w0(s+tau*(eta-u)) for u<=eta<=y1,
 F_w1(s+tau*(eta-u)-C1) for y1<=eta<=y2,
 F_w2(s+tau*(eta-u)-C2) for y2<=eta<=y3,
 F_w3(s+tau*(eta-u)-C3) above y3.

Skip the preceding pieces for a higher-band source, using its corresponding initial C. Before y3 physical height is eta and increases strictly. Above y3 set physical y=eta for y3<=eta<=H and y=2H-eta for H<=eta<=2H-v.

At each upward narrowing, the preceding signed phase differs from the next by an EVEN period of the preceding width. The common residual is strictly between minus/plus the narrower width. Both neighboring folds therefore locally agree with the same absolute-value function, giving exactly the same physical position and signed horizontal velocity. A zero residual is one ordinary reflection on the true common wall x=0, smooth across that height. It is not a polygon corner. No reflection is inserted at a portal.

The strict bounds exclude both step corners: the inner reflex corner at the narrower width, and the outer convex endpoint at the previous larger width. All vertical reflections between distinct portal heights are on original open vertical walls. The strictly increasing lower height excludes every internal horizontal ledge. In the final band the ray stays strictly above y3 until its possible terminal return to y3. Thus no unintended step or cut can interrupt the prescribed ray. The only possible new corner issue is a roof endpoint.

Let B=z3+tau*(H-y3). If B is not a multiple of w3, the roof contact is strictly inside the genuine finite roof, so the complete path is ordinary and ends at actual T by F_w3(Y)=t and physical y=v.

If B is a multiple of w3, use the exact identity F_w3(B-z)=F_w3(B+z). The descending target coordinate then equals the coordinate at the EARLIER ascending visit to physical height v:

 F_w3(B-tau*(H-v))=F_w3(B+tau*(H-v))=t.

Truncate at that earlier actual T. It occurs before the roof because v<H. For v=y3 this is the initial final-portal visit. The retained prefix has every portal guard and has no roof corner contact at all. This is exact actual-target attainment, not continuation through a corner or a perturbed target.

All selected parameters and widths are finite and positive, so there are finitely many genuine vertical reflections. Horizontal velocity is always +/-tau; vertical velocity is +1 until the sole possible ordinary roof reflection and -1 after it. These are specular updates at the actual finite original walls. Truncation at any still earlier actual T is legal. Actual S and T, not chosen other lifts, are the physical endpoints.

## 8. Transpose and substantive extension beyond full windows

Transposition is an isometry. Its widths are (H,y3,y2,y1) and its heights are (0,w3,w2,w1,w0). The same B inequality evaluated on these parameters proves the corresponding actual illumination assertion whenever an original endpoint has x>=w1. It preserves all signed velocities and genuine-wall guards when transported back.

For the already frozen axis-obstruction geometry (40,12,8,4;0,12,16,20,40), the TRANSPOSED parameters give E2=32,r=24,E3=20, so H*E3/y3=200/3>24=2w3 in the transposed notation. Therefore the theorem covers EVERY real actual pair in that original room with an endpoint x>=12, not merely its frozen pair. The old transposed nested FULL-window second condition fails: 16*(12-8)=64<12*8=96. This demonstrates the quantified extension beyond requiring full windows at each narrowing. No new room or numerical discovery was used; the independent peer's explicit velocity(-3,+1) witness is a separate prescribed control.

## 9. Exact remaining task

Neither B nor its transpose is proved automatic for arbitrary four-band geometry. Even when B holds, it currently covers top-band endpoint pairs; its transpose covers rightmost-overhang endpoint pairs. Do not infer other endpoint placements from an eight-wall subroom with artificial roof/right walls. ST10-A's complete five-programme all-metric/all-native-pair existence remains unresolved, as do whole staircase10/all-r3/r<=8. This positive uniform lemma is a proof ingredient and milestone, never broad goal completion. No search, worker, engine, census, fit, clock reset or git mutation was used.
