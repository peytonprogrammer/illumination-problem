#!/usr/bin/env python3
"""Prescribed exact algebra controls for W1-W4, no search."""
from fractions import Fraction as F
from pathlib import Path
import json

def access(w,a,b,alpha,beta,e):
 S=(-alpha/a,(w-alpha)/a)
 T=((beta-w)/b,beta/b) if e==1 else (-beta/b,(w-beta)/b)
 lo=max(S[0],T[0]); hi=min(S[1],T[1])
 return S,T,max(F(0),hi-lo)
w,h,a,b=map(F,[8,1,2,4]);K=a+b+2*h
assert K==2*max(a,b)
assert K*w/max(a,b)==2*w
H,Ys,Yt=map(F,[16,-4,-4]);invariant=[]
for c in [F(0),F(2)]:
 aa,bb,hh=c-Ys,c-Yt,H-c
 assert aa+bb+2*hh==2*H-Ys-Yt==40
 invariant.append({'c':str(c),'a':str(aa),'b':str(bb),'h':str(hh),'K':'40'})
S,T,l=access(F(16),F(8),F(16),F(4),F(-2),-1)
assert S==(F(-1,2),F(3,2)) and T==(F(1,8),F(9,8)) and l==1
assert F(40)*l>32
assert 16>abs(8-16)
output={'status':'PASS_PRESCRIBED_WIDTH_CONTROLS','depth_balance_equality_case':{'w':8,'h':1,'a':2,'b':4,'max_K_ell':16,'two_w':16,'strict_C_possible':False},'fixed_development_section_slides':invariant,'actual_r2_access_only_intervals':{'source':[str(x) for x in S],'target':[str(x) for x in T],'overlap_length':str(l),'other_guards_still_required':True},'proof_basis':'Hand W1-W4 inequalities, affine cancellation and integer reflection parity; no finite controls substituted for proof','G8_proved':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
