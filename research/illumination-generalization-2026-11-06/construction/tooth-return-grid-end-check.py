from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import json,math
ROOT=Path(__file__).resolve().parent
E=json.loads((ROOT/'tooth-return-grid-effort.json').read_text())
def alive():assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
def clip(ints,a,b,lo,hi):
 x,y=sorted(((F(lo)-b)/a,(F(hi)-b)/a));return [(max(p,x),min(q,y)) for p,q in ints if max(p,x)<min(q,y)]
def avoid(ints,a,b,lo,hi):
 x,y=sorted(((F(lo)-b)/a,(F(hi)-b)/a));out=[]
 for p,q in ints:
  if q<=x or p>=y:out.append((p,q))
  else:
   if p<x:out.append((p,x))
   if y<q:out.append((y,q))
 return out

def candidates(h,d,D,tooth):
 ys=(h,h+(4 if d is None else d+2));G=2*h+(4 if d is None else d+4);t=2*h+2
 left=[(y,y+2) for y in ys]+[(2*G-y-2,2*G-y) for y in ys]
 right=[(1,3),(t-1,t+1),(2*G-3,2*G-1),(2*G-t-1,2*G-t+1)]
 out=[]
 for tc in (t,2*G-t):
  H=(tc-2)//2
  for Y in (ys[tooth],2*G-ys[tooth]-2):
   if Y>=tc+1:continue
   for n in (0,1,2,3):
    alive();C=2-2*n;L=tc+2*n
    for l in range(1,25):
     pre=clip([(max(F(0),F(2*n-1,D)),F(2*n+1,D))],D+2*l-1,C,Y,Y+2)
     if not pre:continue
     for j in range(1,2*l-1):
      for lo,hi in (left if j%2 else right):pre=avoid(pre,D+j,C,lo,hi)
      pre=avoid(pre,D+j,C,G,G)
      if not pre:break
     if not pre:continue
     for r in range(1,25):
      if l==r and (H+2-Y)%2==0:continue
      ints=clip(pre,-D-2*r+1,L,Y,Y+2)
      if not ints:continue
      for j in range(1,2*r-1):
       for lo,hi in (left if j%2 else right):ints=avoid(ints,-D-j,L,lo,hi)
       ints=avoid(ints,-D-j,L,G,G)
       if not ints:break
      for lo,hi in ints:
       need=F(2 if l==r else 4)/(hi-lo)
       w_min=max(1,math.floor(need)-(D+l+r-1)+1)
       assert w_min+D+l+r-1>need
       out.append({'n':n,'l':l,'r':r,'lo':lo,'hi':hi,'w_min':w_min,'H':H,'Y':Y,'target_copy':tc,'G':G,'far_phase_constant':H+2-Y,'two_candidates':l!=r})
 return sorted(out,key=lambda z:(z['w_min'],z['l']+z['r'],z['n'],z['target_copy']))

def select(cs,h,D,w):
 for v in cs:
  den=w+D+v['l']+v['r']-1
  lo=v['lo'];hi=v['hi'];n=v['n'];H=v['H']
  k0=max(0,math.floor((lo*den-H-2*n)/2)+1)
  for k in (k0,k0+1):
   tau=F(H+2*n+2*k,den)
   if not lo<tau<hi:continue
   far=v['far_phase_constant']+2*k+(v['l']-v['r'])*tau
   if far.denominator==1 and far.numerator%2==0:continue
   return dict(v,k=k,tau=tau,w=w,far_phase=far)
 return None
patterns=[('A0',h,None) for h in range(3,9)]
patterns += [('A1',h,d) for d in range(1,6) for h in range(max(5,2*d),2*d+5)]
patterns += [('A1',h,d) for h in (3,4) for d in range(1,h+3)]
rows=[]
for kind,h,d in patterns:
 for D in (1,2):
  alive();row={'kind':kind,'h':h,'d':d,'D':D,'targets':[]}
  for tooth in (0,1):
   cs=candidates(h,d,D,tooth);best=cs[0] if cs else None
   missing=[];small=[]
   if best:
    for w in range(1,best['w_min']):
     z=select(cs,h,D,w)
     if z:small.append(z)
     else:missing.append(w)
   row['targets'].append({'tooth':tooth,'candidate_intervals':len(cs),'best':best,'small_width_witnesses':small,'uncovered_widths':missing,'intervals':cs})
  rows.append(row)
  print(kind,h,d,'D',D,[(z['candidate_intervals'],None if z['best'] is None else z['best']['w_min'],z['uncovered_widths']) for z in row['targets']],flush=True)
alive()
out={'status':'EXACT_COMPLEMENTARY_END_CHART_INTERVAL_ANALYSIS','discovery':True,'proof_question':'Actual one-excursion normal form, not darkness','rows':rows,'both_tails':sum(all(t['best'] for t in z['targets']) for z in rows),'one_tail':sum(sum(bool(t['best']) for t in z['targets'])==1 for z in rows),'no_tail':sum(not any(t['best'] for t in z['targets']) for z in rows),'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat()}
(ROOT/'tooth-return-grid-end-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
