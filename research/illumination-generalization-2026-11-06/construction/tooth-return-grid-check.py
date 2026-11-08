from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import json,math
ROOT=Path(__file__).resolve().parent
E=json.loads((ROOT/'tooth-return-grid-effort.json').read_text())
assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
def clip(ints,a,b,lo,hi):
    assert a
    x,y=sorted(((F(lo)-b)/a,(F(hi)-b)/a))
    return [(max(p,x),min(q,y)) for p,q in ints if max(p,x)<min(q,y)]
def avoid(ints,a,b,lo,hi):
    x,y=sorted(((F(lo)-b)/a,(F(hi)-b)/a))
    out=[]
    for p,q in ints:
        if q<=x or p>=y: out.append((p,q))
        else:
            if p<x:out.append((p,x))
            if y<q:out.append((y,q))
    return out

def candidates(h,d,D,target,n=1):
    # d=None denotes A0; otherwise A1.
    ys=(h,h+(4 if d is None else d+2));C=2-2*n;L=2*h+4-C;Y=ys[target]
    out=[]
    for l in range(1,min(30,math.ceil(F((D+2)*(Y+2-C),2))+2)):
      for r in range(1,min(30,math.ceil(F((D+2)*(L-Y),2))+2)):
        if l==r and (h+2-Y)%2==0:continue
        ints=[(max(F(0),F(2*n-1,D)),F(2*n+1,D))]
        ints=clip(ints,D+2*l-1,C,Y,Y+2)
        ints=clip(ints,-D-2*r+1,L,Y,Y+2)
        for j in range(1,2*l-1):
            a=D+j
            if j%2:
                for B in ys:ints=avoid(ints,a,C,B,B+2)
            else:ints=clip(ints,a,C,3,2*h+1)
        for j in range(1,2*r-1):
            a=-D-j
            if j%2:
                for B in ys:ints=avoid(ints,a,L,B,B+2)
            else:ints=clip(ints,a,L,3,2*h+1)
        for lo,hi in ints:
            # Enough to fit TWO consecutive grid points; one if constant odd phase.
            need=F(2 if l==r else 4)/(hi-lo)
            w_min=max(1,math.floor(need)-(D+l+r-1)+1)
            # denominator > need is the exact strict sufficient bound.
            assert w_min+D+l+r-1>need
            out.append({'n':n,'l':l,'r':r,'lo':lo,'hi':hi,'w_min':w_min,'far_phase_constant':h+2-Y,'two_candidates':l!=r})
    return sorted(out,key=lambda z:(z['w_min'],z['l']+z['r'],z['lo']))
patterns=[('A0',h,None) for h in range(3,9)]
patterns += [('A1',h,d) for d in range(1,6) for h in range(max(5,2*d),2*d+5)]
# Include low h3/4 prefix plus one certified potential d-tail representative.
patterns += [('A1',h,d) for h in (3,4) for d in range(1,h+3)]
rows=[]
for kind,h,d in patterns:
 for D in (1,2):
  row={'kind':kind,'h':h,'d':d,'D':D,'targets':[]}
  for tooth in (0,1):
    cs=sorted([v for n in (0,1,2,3) for v in candidates(h,d,D,tooth,n)],key=lambda z:(z['w_min'],z['l']+z['r'],z['n']))
    row['targets'].append({'tooth':tooth,'candidate_intervals':len(cs),'best':cs[0] if cs else None})
  rows.append(row)
assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
out={'status':'EXACT_GEOMETRIC_INTERVAL_ANALYSIS','discovery':True,'proof_question':'Prescribed one-excursion normal form; not a darkness decision','rows':rows,'both_tails':sum(all(t['best'] for t in z['targets']) for z in rows),'one_tail':sum(sum(bool(t['best']) for t in z['targets'])==1 for z in rows),'no_tail':sum(not any(t['best'] for t in z['targets']) for z in rows),'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat()}
(ROOT/'tooth-return-grid-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
for z in rows:
 print(z['kind'],z['h'],z['d'],'D',z['D'],[(t['candidate_intervals'],None if not t['best'] else (t['best']['w_min'],t['best']['n'],t['best']['l'],t['best']['r'],str(t['best']['lo']),str(t['best']['hi']))) for t in z['targets']])
