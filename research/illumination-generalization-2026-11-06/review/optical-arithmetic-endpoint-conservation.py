#!/usr/bin/env python3
"""Exact abstract-window inference controls; no physical realization asserted."""
from fractions import Fraction as F
from pathlib import Path
import json
from collections import Counter

def floor(q):return q.numerator//q.denominator
def ceil(q):return -floor(-q)
def mod1(q):return q-floor(q)
def count(ws,theta):
 return sum(max(0,ceil(B-theta)-floor(A-theta)-1) for A,B in ws)
def ends(ws):return Counter(mod1(A) for A,B in ws),Counter(mod1(B) for A,B in ws)
base=[(F(0),F(1,2)),(F(1,2),F(1))]
shift=[(F(1,4),F(3,4)),(F(3,4),F(5,4))]
rows=[]
for N in [1,3]:
 ws=base*N;L,U=ends(ws);assert L==U
 M=sum(B-A for A,B in ws);assert M==N
 assert count(ws,F(0))==count(ws,F(1,2))==0
 assert count(ws,F(1,4))==count(ws,F(3,4))==N
 for theta in set(L)|{F(1,4),F(3,4)}:
  assert count(ws,theta)==M-U[theta]
 rows.append({'copies':N,'total_length':str(M),'start_end_charges_balance':True,'C_target_0':count(ws,F(0)),'C_quarter':count(ws,F(1,4)),'U_target_0':U[F(0)]})
assert count(shift,F(0))==1
assert ends(shift)[0]==ends(shift)[1]
# Endpoint convention for one long window, whose endpoints project to same phase.
long=[(F(0),F(2))];assert count(long,F(0))==1 and count(long,F(1,4))==2
L,U=ends(long);assert L==U and count(long,F(0))==2-U[F(0)]
out={'status':'PASS_EXACT_ABSTRACT_ENDPOINT_CONTROLS','balanced_but_target_missing':rows,'rotated_same_cyclic_structure':{'total_length':'1','C_target_0':count(shift,F(0)),'target_phase_registration_matters':True},'long_window_endpoint_deficit':{'C_target_0':1,'C_regular':2,'endpoint_multiplicity':1},'physical_room_realization_claimed':False,'global_coverage_proved':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
