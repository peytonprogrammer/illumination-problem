#!/usr/bin/env python3
"""Complete finite TR02 phase audit for ONE predeclared fixed input only."""
from fractions import Fraction as F
from pathlib import Path
import json
r=Path(__file__).parent
rows=[];counts={'first_portal_pass':0,'cap_pass':0,'right_pass':0,'target_pass':0}
for i in range(1344):
 tau=F(i,12)
 for sign in [-1,1]:
  q=sign*2+14*tau;n=(q+4)//8;z0=q-8*n
  if not -4<z0<4:continue
  counts['first_portal_pass']+=1
  q1=z0+16*tau;m=q1//56;z1=q1-(2*m+1)*28
  if not -8<z1<8:continue
  counts['cap_pass']+=1
  q2=z1+12*tau;k=(q2+8)//16;z2=q2-16*k
  if not -8<z2<8:continue
  counts['right_pass']+=1;q3=z2+6*tau
  for targetsign in [-1,1]:
   j=(q3-targetsign*14)/32
   if j.denominator==1:
    assert tau*48==8*n+(2*m+1)*28+16*k+32*j+targetsign*14-sign*2
    counts['target_pass']+=1;rows.append({'tau':str(tau),'source_sign':sign,'target_sign':targetsign,'indices':[int(n),int(m),int(k),int(j)],'residuals':list(map(str,[z0,z1,z2]))})
assert len(rows)==178 and rows[0]['tau']=='7/6'
# This recorded result can be replayed as prescribed verification; discovery is finished.
out={'status':'PASS_COMPLETE_FIXED_INPUT_PHASE_REPLAY','counts':counts,'period':112,'root_grid':'1/12 Z','residue_count':1344,'witnesses':rows[:4],'total_witness_residues':len(rows),'scope':'This fixed TR02 chart input only, not universal feasibility or actual darkness.','whole_goal_complete':False}
r.joinpath('three-reflex-tr02-fixed-replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'witness_residues':len(rows),'first_tau':rows[0]['tau']}))
