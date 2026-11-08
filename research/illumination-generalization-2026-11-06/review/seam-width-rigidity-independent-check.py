"""Prescribed exact stationary-phase and reduced-divisor controls, no discovery."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd
import json
R=Path(__file__).resolve().parent
cases=nonres=res=0;maxsteps=0
for c in range(1,25):
 for w in range(1,2*c+1):
  for H in range(2,26):
   tau=Q(0);seen=set()
   while True:
    assert tau not in seen;seen.add(tau);n=int((w*tau+Q(1,2))//1);nxt=Q(H+n,w+c)
    if nxt==tau:break
    assert nxt>tau;tau=nxt
   steps=len(seen);maxsteps=max(maxsteps,steps);m=w*tau-n;assert -Q(1,2)<m<Q(1,2)
   assert m!=0 or (w*H)%c==0
   if m:
    assert (w*tau).denominator>1
    assert 0<1+2*m<2 and 0<1-2*m<2;nonres+=1
   else:assert c*tau==H;res+=1
   r=c//gcd(c,w);assert ((w*H)%c==0)==(H%r==0);cases+=1
ratios=[]
for c in range(1,200):
 good=[w for w in range(1,c+1) if c//gcd(c,w)<=2]
 assert good==([c//2,c] if c%2==0 else [c]);ratios.append({'c':c,'surviving_widths':good})
out={'status':'A56_STATIONARY_PHASE_AND_DIVISOR_CONTROLS_INDEPENDENTLY_PASS','exact_phase_cases':cases,'nonresonant_cases':nonres,'resonant_cases':res,'max_stationary_steps':maxsteps,'ratio_core_cases':len(ratios),'discovery':False,'whole_goal_complete':False,'limits':'Finite arithmetic controls, not a replacement for unbounded hand proof or actual path replay.'}
(R/'seam-width-rigidity-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
