"""New narrow-endpoint-region four-sheet obstruction test, original deadline."""
from pathlib import Path
from fractions import Fraction as F
import json,time,signal
B=Path(__file__).parent;E=json.loads((B/'narrow-rectangle-effort.json').read_text())
def timeout(*_):raise TimeoutError('original narrow-rectangle aggregate deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
def works(a,b):
    q=a+b+1;C=a+1;D=100;unit=q*D
    for j in range(q):
     for u in (0,2):
      for eps in (1,-1):
        x=((q-a)*70+a*(D*u+eps+4*D*j))%(4*unit);y=((q-C)*70+C*(D*u+eps+4*D*j))%(4*unit)
        c=1 if unit<x<2*unit else 3 if 2*unit<x<3*unit else None
        if c is None:continue
        lo,hi={(0,1):(1,2),(0,3):(2,3),(2,1):(0,1),(2,3):(3,4)}[u,c]
        if lo*unit<y<hi*unit:return (u,eps,j,c)
    return None

def check(a,b):
    s,t=F(E['s']),F(E['t']);q=a+b+1
    for j in range(q):
     for u in (0,2):
      for eps in (1,-1):
        x=((q-a)*s+a*(u+eps*t+4*j))/q%4;y=((q-a-1)*s+(a+1)*(u+eps*t+4*j))/q%4
        c=1 if 1<x<2 else 3 if 2<x<3 else None
        if c is None:continue
        lo,hi={(0,1):(1,2),(0,3):(2,3),(2,1):(0,1),(2,3):(3,4)}[u,c]
        assert not lo<y<hi
    return {'a':a,'b':b,'phase':[a,a+1,q],'Fraction_evaluations':4*q}

def main():
    edges={};tested=0
    for a in range(1,E['integer_depth_cap']+1):
      bs=set()
      for b in range(1,E['integer_depth_cap']+1):
        tested+=1
        if works(a,b) is None:bs.add(b)
      edges[a]=bs
      for aa,old in edges.items():
        if aa>=a:continue
        common=sorted(old&bs)
        if len(common)>=2:
            b,Bb=common[:2];rows=[check(x,y) for x,y in [(aa,b),(a,b),(aa,Bb),(a,Bb)]]
            out={'status':'FOUR_CAP_PORTAL_MECHANISM_REFUTED','s':E['s'],'t':E['t'],'a':aa,'b':b,'hm':str(F(aa+a,2)),'hp':str(F(b+Bb,2)),
                 'effective_depth_rectangle':[aa,a,b,Bb],'four_exact_failures':rows,'tested_depth_pairs':tested,'effort':E,
                 'scope':'Mechanism obstruction only; NO darkness claim. Exact full-period conditions for all four cap sheets fail.'}
            (B/'narrow-rectangle.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return
    out={'status':'NO_INTEGER_DEPTH_RECTANGLE_IN_FIXED_NARROW_REGION','tested_depth_pairs':tested,'failure_edges':sum(map(len,edges.values())),
         'failure_rows':{str(a):sorted(bs) for a,bs in edges.items() if bs},'effort':E,'scope':'Bounded negative evidence only; no universal four-cap cover.'}
    (B/'narrow-rectangle.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
    try:main()
    except TimeoutError:
        out={'status':'ORIGINAL_DEADLINE_REACHED','effort':E};(B/'narrow-rectangle.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
