#!/usr/bin/env python3
"""Prescribed sanity checks for the all-n hand stabilizer proof; no search."""
from pathlib import Path
import json
out=[]
for n in (2,3,7):
    B=8*n*n;L=2*B
    X={(sx*(B//2)%L,sy*(B//2)%L) for sx in (-1,1) for sy in (-1,1)}
    Y={(sx*(B//2+2*n)%L,sy*(B//2+2)%L) for sx in (-1,1) for sy in (-1,1)}
    Z={(x,y) for x in (0,B) for y in (0,B)}
    for k in (-1,1,2):
        a=4*n*n*k;b=4*n*k;c=B*k%L
        H=lambda p:((p[0]+a*p[1]+c)%L,p[1])
        V=lambda p:(p[0],(p[1]+b*p[0]+c)%L)
        for Q in (X,Y,Z):assert {H(p) for p in Q}==Q and {V(p) for p in Q}==Q
        assert abs(n+a)+1>n+1 and n+abs(1+b*n)>n+1
        out.append({'n':n,'k':k,'horizontal_coefficient':a,'vertical_coefficient':b,'translation_component':c,'full_fibers_and_corners_preserved':True,'both_ranks_increase':True})
result={'status':'PASS_PRESCRIBED_STABILIZER_CALIBRATIONS','method':'Finite exact congruence replay corroborating independent all-n/all-k hand proof, not a completeness search','checks':out,'all_n_claim_proved_by':'weighted-return-square-shear.md','universal_decreasing_shear_availability':'REJECTED_BY_HAND_FOR_ALL_N_GE_2','whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'prescribed_checks':len(out)}))
