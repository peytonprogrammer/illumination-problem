"""Complete finite residual support list from analytic q bounds and affine families."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
from functools import lru_cache
import json,time,signal,hashlib
B=Path(__file__).parent;E=json.loads((B/'residual-rooms-effort.json').read_text())
def timeout(*_):raise TimeoutError('original finite residual generation deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
geometry=json.loads((B/'critical-rectangles.json').read_text());margin=json.loads((B/'family-joint-margin.json').read_text())
points={tuple(map(F,r['depths'])) for stem in ('exceptional-phase-support','short-line-finite') for r in json.loads((B/(stem+'.json')).read_text())['exceptions']}
lines=[tuple(map(F,R)) for R in geometry['critical_lines']];rooms={};skipped_equal=0

def add(v,origin):
    global skipped_equal
    a,A,b,Bb=v
    assert a>0 and b>0 and A>a and Bb>b
    if any(x==y for x in (a,A) for y in (b,Bb)):skipped_equal+=1;return
    rooms.setdefault(tuple(v),origin)

@lru_cache(None)
def phase_depths(rel,Q):
    mm,nn,rr=rel;out=[]
    for q in range(3,Q+1):
      for A in range(1,q-1):
        if nn:
            z=rr*q-mm*A
            if z%nn:continue
            Cs=[z//nn]
        else:
            if mm*A!=rr*q:continue
            Cs=range(A+1,q)
        for C in Cs:
            if not A<C<q or gcd(gcd(A,C),q)!=1:continue
            out.append((F(A,C-A),F(q-C,C-A),q,A,C))
    return out

def supported(x,y):return (x,y) in points or any(p*x+q*y==r for p,q,r in lines)
def main():
    for row in margin['families']:
        i=row['family_index'];Q=row['uniform_q1_cutoff'];family=geometry['positive_dimensional_families'][i];expr=[tuple(map(F,R)) for R in family['affine_expressions']]
        low,high=family['open_parameter_interval'];low=F(low) if low is not None else None;high=F(high) if high is not None else None
        for j,(si,ti) in enumerate([(0,2),(1,2),(0,3),(1,3)]):
          aa,ac=expr[si];ba,bc=expr[ti]
          assert aa or ba
          for U,V,q,A,C in phase_depths(tuple(family['relations'][j]),Q):
            lam=(U-ac)/aa if aa else (V-bc)/ba
            if (low is not None and lam<=low) or (high is not None and lam>=high):continue
            if aa*lam+ac!=U or ba*lam+bc!=V:continue
            v=tuple(c*lam+d for c,d in expr)
            add(v,{'kind':'family_small_phase','family':i,'parameter':str(lam),'sheet':j,'phase':[A,C,q],'Q':Q})
    family_count=len(rooms)
    for i,row in enumerate(geometry['isolated_points']):add(tuple(F(R[-1]) for R in row['affine_expressions']),{'kind':'critical_isolated','index':i})
    after_isolated=len(rooms)
    assert len(points)==11 and all(x!=1 and y!=1 for x,y in points)
    # Any rectangle containing a fixed exceptional point is finite: all adjacent line intersections are unique or disjoint.
    for x,y in sorted(points):
        xs={z for z,w in points if w==y};ys={w for z,w in points if z==x}
        xs|={(r-q*y)/p for p,q,r in lines if p};ys|={(r-p*x)/q for p,q,r in lines if q}
        for xx in xs:
         if xx<=0 or xx==x:continue
         for yy in ys:
          if yy<=0 or yy==y or not supported(xx,yy):continue
          a,A=sorted((x,xx));b,Bb=sorted((y,yy))
          add((a,A,b,Bb),{'kind':'exceptional_point_rectangle','point':[str(x),str(y)],'opposite':[str(xx),str(yy)]})
    records=[];maxq1=0;maxq3=0
    for i,(v,origin) in enumerate(sorted(rooms.items())):
        a,A,b,Bb=v;hm=(a+A)/2;hp=(b+Bb)/2
        q1=[];q3=[]
        for U,V in [(a,b),(A,b),(a,Bb),(A,Bb)]:
            h=U+V+1;q1.append(lcm((U/h).denominator,((U+1)/h).denominator))
            h=U+V+3;q3.append(lcm((U/h).denominator,(1/h).denominator))
        maxq1=max(maxq1,*q1);maxq3=max(maxq3,*q3)
        records.append({'id':i,'rectangle':list(map(str,v)),'a':str(a),'b':str(b),'hm':str(hm),'hp':str(hp),'q1':q1,'q3':q3,'origin':origin})
    out={'status':'COMPLETE_FINITE_RESIDUAL_ROOM_SUPPORT','room_count':len(records),'from_family_bounds_unique':family_count,
         'after_critical_isolated_unique':after_isolated,'equal_effective_depth_insertions_skipped':skipped_equal,
         'max_q1':maxq1,'max_q3':maxq3,'rooms':records,'effort':E,
         'dependency_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ['critical-rectangles.json','family-joint-margin.json','exceptional-phase-support.json','short-line-finite.json']},
         'scope':'Complete residual SUPPORT conditional on reviewed reductions; no finite room optical closure yet.'}
    (B/'residual-rooms.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rooms'}))
if __name__=='__main__':main()
