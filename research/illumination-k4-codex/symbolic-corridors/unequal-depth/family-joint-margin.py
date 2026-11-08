"""Exact closed-endpoint joint1/3pass cover with rational sampling cutoffs."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,signal,time
B=Path(__file__).parent;E=json.loads((B/'family-joint-margin-effort.json').read_text())
def load(name,file):
    sp=importlib.util.spec_from_file_location(name,B/file);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
sm=load('closed_complement','short-line-margin.py');tp=load('three_pass','three-pass-circle.py');clip=sm.m.clip
def timeout(*_):raise TimeoutError('original joint-family margin deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
boxes=[(0,1,1,2,1,2),(0,3,2,3,2,3),(2,1,1,2,0,1),(2,3,2,3,3,4)]

def poly3(eta):
    out=[]
    for u,c,l0,h0,l3,h3 in boxes:
      ints=[2,3] if c==1 else [0,1]
      for l1,l2 in product(ints,repeat=2):
       for k1,k2,k3 in product(range(4),repeat=3):
        P=[(F(l0)+eta,F(0)),(F(h0)-eta,F(0)),(F(h0)-eta,F(4)),(F(l0)+eta,F(4))]
        for j,lo,hi,k in [(1,l1,l1+1,k1),(2,l2,l2+1,k2),(3,l3,h3,k3)]:
            P=clip(P,(1,j,-F(lo+4*k)-eta));P=clip(P,(-1,-j,F(hi+4*k)-eta))
            if not P:break
        if tp.area(P):out.append({'u':u,'c':c,'vertices':P})
    return out

def guards_from_interval(mm,rr,u,lo,hi,mode,cutoff,sheet,relation):
    if mode==1:cs=relation[0]+relation[1]-rr
    else:cs=mm-rr
    for eps in (1,-1):
      ct=rr*eps;c0=rr*u;cmin=c0+min(F(0),cs)+min(F(0),ct);cmax=c0+max(F(0),cs)+max(F(0),ct)
      for k in range(((lo-cmax)/4).__floor__()-1,((hi-cmin)/4).__floor__()+2):
        gs=((F(cs),F(ct),F(c0+4*k)-lo),(-F(cs),-F(ct),hi-F(c0+4*k)))
        if any(max(g[2],g[0]+g[2],g[1]+g[2],sum(g))<=0 for g in gs):continue
        yield gs,{'mode':mode,'cutoff':cutoff,'sheet':sheet,'relation':relation,'u':u,'epsilon':eps,'k':k}

def clauses(row,eta,polys):
    for j,rel in enumerate(row['relations']):
        mm,nn,rr=rel;w=abs(mm)+abs(nn);K=max(abs(mm),abs(nn));cut=int(2*K/eta)
        for u,c,l0,h0,l1,h1 in boxes:
            lo=min(mm*l0,mm*h0)+min(nn*l1,nn*h1)+eta*w
            hi=max(mm*l0,mm*h0)+max(nn*l1,nn*h1)-eta*w
            yield from guards_from_interval(mm,rr,u,lo,hi,1,cut,j,rel)
    expr=[tuple(map(F,R)) for R in row['affine_expressions']]
    records=[]
    for j,(si,ti) in enumerate([(0,2),(1,2),(0,3),(1,3)]):
        rel=tp.normal(expr[si],expr[ti]);assert rel is not None
        mm,nn,rr=rel;K=max(abs(k*mm-nn) for k in range(4));cut=int(2*K/eta)
        for P in polys:
            vals=[mm*x+nn*y for x,y in P['vertices']];lo,hi=min(vals),max(vals)
            records.extend(guards_from_interval(mm,rr,P['u'],lo,hi,3,cut,j,rel))
    records.sort(key=lambda x:x[1]['cutoff'])
    yield from records

def check(row,eta,polys):
    P=[[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]];used=[]
    for gs,info in clauses(row,eta,polys):
        out={}
        for Q in P:
            for R in sm.subtract_closed(Q,gs):out[sm.m.key(R)]=R
        new=list(out.values())
        if set(out)!=set(sm.m.key(Q) for Q in P):
            used.append({**info,'guards':[[str(x) for x in g] for g in gs]})
        P=new
        if not P:return used
    return None

def main():
    source=json.loads((B/'critical-rectangles.json').read_text())['positive_dimensional_families'];records=[];polycache={raw:poly3(F(raw)) for raw in E['margins']}
    for i,row in enumerate(source):
        e=row['affine_expressions']
        if any(e[x]==e[y] for x,y in [(0,2),(1,2),(0,3),(1,3)]):continue
        result=None
        for raw in E['margins']:
            used=check(row,F(raw),polycache[raw])
            if used is not None:
                result={'family_index':i,'eta':raw,'uniform_q1_cutoff':max(r['cutoff'] for r in used),'clauses':used,
                        'affine_expressions':row['affine_expressions'],'open_parameter_interval':row['open_parameter_interval']};break
        records.append(result if result else {'family_index':i,'status':'NO_CERTIFIED_MARGIN'})
    out={'status':'COMPLETE_JOINT_FAMILY_MARGIN_ATTEMPT','families':records,'family_count':len(records),
         'covered_count':sum('uniform_q1_cutoff' in r for r in records),'max_cutoff':max((r.get('uniform_q1_cutoff',0) for r in records)),
         'effort':E,'scope':'Closedcirclecovers +candidate finiteqcutoffs; rationalparameterenumerationandroomclosurestillrequired.'}
    (B/'family-joint-margin.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='families'}));print('cutoffs',[(r['family_index'],r.get('eta'),r.get('uniform_q1_cutoff')) for r in records])
if __name__=='__main__':main()
