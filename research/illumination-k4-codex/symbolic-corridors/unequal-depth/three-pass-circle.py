"""Exact phase-window test for a specified three-pass middle reflection template."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import lcm,gcd
import importlib.util,json,time,signal
B=Path(__file__).parent;E=json.loads((B/'three-pass-circle-effort.json').read_text())
spec=importlib.util.spec_from_file_location('clip',B/'finite-short-cover.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def timeout(*_):raise TimeoutError('original three-pass aggregate deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
def area(P):return abs(sum(C[0]*D[1]-D[0]*C[1] for C,D in zip(P,P[1:]+P[:1]))) if P else F(0)
def polygons():
    out=[]
    for u,c,l0,h0,l3,h3 in [(0,1,1,2,1,2),(0,3,2,3,2,3),(2,1,1,2,0,1),(2,3,2,3,3,4)]:
      ints=[2,3] if c==1 else [0,1]
      for l1,l2 in product(ints,repeat=2):
       for k1,k2,k3 in product(range(4),repeat=3):
        P=[(F(l0),F(0)),(F(h0),F(0)),(F(h0),F(4)),(F(l0),F(4))]
        for j,lo,hi,k in [(1,l1,l1+1,k1),(2,l2,l2+1,k2),(3,l3,h3,k3)]:
            P=m.clip(P,(1,j,-F(lo+4*k)));P=m.clip(P,(-1,-j,F(hi+4*k)))
            if not P:break
        if not area(P):continue
        out.append({'u':u,'c':c,'vertices':P,'internal_lo':[l1,l2],'residue_shifts':[k1,k2,k3]})
    return out

def normal(a,b):
    aa,ac=a;ba,bc=b;ha=aa+ba;hc=ac+bc+3
    v=[ha,aa*hc-ha*ac,aa]
    if v==[0,0,0]:return None
    den=lcm(*(x.denominator for x in v));v=[int(x*den) for x in v];g=gcd(gcd(abs(v[0]),abs(v[1])),abs(v[2]));v=[x//g for x in v]
    if v[0]<0 or (v[0]==0 and v[1]<0):v=[-x for x in v]
    return v

def hit(poly,rel,s,t):
    mm,nn,rr=rel
    for P in poly:
      vals=[mm*x+nn*y for x,y in P['vertices']];lo,hi=min(vals),max(vals)
      for eps in (1,-1):
        C=(mm-rr)*s+rr*eps*t+rr*P['u']
        for k in range(((lo-C)/4).__floor__()-1,((hi-C)/4).__floor__()+2):
            if lo<C+4*k<hi:
                return {'relation':rel,'u':P['u'],'c':P['c'],'epsilon':eps,'level_k':k,'normal_interval':[str(lo),str(hi)],
                        'level':str(C+4*k),'polygon':[[str(x),str(y)] for x,y in P['vertices']],
                        'internal_lo':P['internal_lo'],'residue_shifts':P['residue_shifts']}
    return None

def main():
    poly=polygons();families=json.loads((B/'critical-rectangles.json').read_text())['positive_dimensional_families'];records=[]
    for i,row in enumerate(families):
        expr=[tuple(map(F,e)) for e in row['affine_expressions']]
        if not row['common_blind_boundary_points'] or any(expr[x]==expr[y] for x,y in [(0,2),(1,2),(0,3),(1,3)]):continue
        bounds=[]
        for raw in row['common_blind_boundary_points']:
            s,t=map(F,raw);witness=None
            for si,ti in [(0,2),(1,2),(0,3),(1,3)]:
                rel=normal(expr[si],expr[ti])
                if rel is None:continue
                witness=hit(poly,rel,s,t)
                if witness:witness['sheet']=[si,ti];break
            bounds.append({'endpoint_boundary':raw,'three_pass_circle_hit':witness})
        records.append({'family_index':i,'affine_expressions':row['affine_expressions'],'parameter_interval':row['open_parameter_interval'],'boundary_tests':bounds})
    assert len(records)==16
    out={'status':'THREE_PASS_BOUNDARY_CIRCLE_TEST_COMPLETE','phase_polygon_count':len(poly),'families_tested':len(records),
         'families_with_all_blind_limits_repaired':sum(all(x['three_pass_circle_hit'] for x in r['boundary_tests']) for r in records),
         'records':records,'effort':E,'scope':'Circle-level strict phase feasibility only; not finite rational orbit hit or full theorem. Optical template geometry still reviewrequired.'}
    (B/'three-pass-circle.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'}));print('unrepaired',[r['family_index'] for r in records if not all(x['three_pass_circle_hit'] for x in r['boundary_tests'])])
if __name__=='__main__':main()
