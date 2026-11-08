"""Exact closed-square affine cover and quantitative margins for30short relations."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import importlib.util,json,signal,time
B=Path(__file__).parent;E=json.loads((B/'short-line-margin-effort.json').read_text())
spec=importlib.util.spec_from_file_location('frozen_clip',B/'finite-short-cover.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def timeout(*_):raise TimeoutError('original short-line-margin aggregate deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
def subtract_closed(P,gs):
    if any(max(m.val(g,p) for p in P)<=0 for g in gs):return [P]
    if all(min(m.val(g,p) for p in P)>0 for g in gs):return []
    R=P;out=[]
    for g in gs:
        Q=m.clip(R,tuple(-x for x in g))
        if Q:out.append(Q)
        R=m.clip(R,g)
        if not R:break
    return out

def cover(mm,nn,rr,eta):
    pieces=[[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]]
    boxes=[(0,1,2,1,2),(0,2,3,2,3),(2,1,2,0,1),(2,2,3,3,4)]
    for u,lx,hx,ly,hy in boxes:
      lo=min(mm*lx,mm*hx)+min(nn*ly,nn*hy)+eta*(abs(mm)+abs(nn))
      hi=max(mm*lx,mm*hx)+max(nn*ly,nn*hy)-eta*(abs(mm)+abs(nn))
      for eps in (1,-1):
       for k in range(-9,10):
        c0=rr*u+4*k;cs=mm+nn-rr;ct=rr*eps
        gs=[(cs,ct,c0-lo),(-cs,-ct,hi-c0)]
        out={}
        for P in pieces:
            for Q in subtract_closed(P,gs):out[m.key(Q)]=Q
        pieces=list(out.values())
        if not pieces:return []
    return pieces

def main():
    rows=[]
    for mm in range(0,5):
     for nn in range(-4,5):
      if not 0<abs(mm)+abs(nn)<=4 or (mm==0 and nn<=0):continue
      for rr in range(min(0,nn,mm+nn)+1,max(0,nn,mm+nn)):
        if gcd(gcd(abs(mm),abs(nn)),abs(rr))!=1:continue
        P=cover(mm,nn,rr,F(0));row={'relation':[mm,nn,rr],'depth_line':[mm+nn-rr,-rr,rr-nn],
           'closed_blind_pieces':[[[str(x),str(y)] for x,y in Q] for Q in P]}
        if not P:
            for raw in E['margins']:
                eta=F(raw)
                if not cover(mm,nn,rr,eta):
                    row['uniform_margin']=raw
                    # q>2*Euclidean_norm/eta; rational sufficient ceiling usingl1.
                    row['rational_phase_cutoff']=int(2*(abs(mm)+abs(nn))/eta)
                    break
            assert 'uniform_margin' in row,('need smaller proof margin',row)
        rows.append(row)
    assert len(rows)==30
    out={'status':'COMPLETE_CLOSED_ENDPOINT_SHORT_LINE_MARGIN_CLASSIFICATION','rows':rows,
         'unbounded_critical_lines':[r['depth_line'] for r in rows if r['closed_blind_pieces']],
         'uniformly_sampled_line_count':sum(not r['closed_blind_pieces'] for r in rows),
         'effort':E,'scope':'Candidate exact affine proof; finitephasecases/criticalfamilies andwholegoal remain.'}
    (B/'short-line-margin.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'}));print('uniform margins',[(r['relation'],r.get('uniform_margin'),r.get('rational_phase_cutoff')) for r in rows])
if __name__=='__main__':main()
