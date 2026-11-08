"""Four-sheet falsification in a prescribed affine-fixed-fiber family."""
from pathlib import Path
from fractions import Fraction as F
import time,json,signal
B=Path(__file__).parent;E=json.loads((B/'fixed-fiber-cap-effort.json').read_text())
def timeout(*_):raise TimeoutError('original fixed-fiber effort deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
def survivors(a,b,D,pairs):
    q=a+b+1;C=a+1;unit=q*D;alive=list(pairs)
    for j in range(q):
      for u in (0,2):
       for eps in (1,-1):
        out=[]
        for s,t in alive:
            x=((q-a)*s+a*(D*u+eps*t+4*D*j))%(4*unit)
            y=((q-C)*s+C*(D*u+eps*t+4*D*j))%(4*unit)
            if u==0:hit=(unit<x<2*unit and unit<y<2*unit) or (2*unit<x<3*unit and 2*unit<y<3*unit)
            else:hit=(unit<x<2*unit and 0<y<unit) or (2*unit<x<3*unit and 3*unit<y<4*unit)
            if not hit:out.append((s,t))
        alive=out
      if not alive:break
    return alive

def exact_recheck(M,a,b,p,r):
    D=2*M+1;s,t=F(p,D),F(r,D);rows=[]
    assert 4*a%4==0 and 4*b%4==0
    K=2*M*D;assert (K*s)%(2*M)==0 and (K*t)%(2*M)==0
    for aa,bb in [(a,b),(2*M-a,b),(a,2*M-b),(2*M-a,2*M-b)]:
        q=aa+bb+1;A=F(aa,q);C=F(aa+1,q);evaluations=0
        for u in (0,2):
         for eps in (1,-1):
          for j in range(q):
            x=((1-A)*s+A*(u+eps*t+4*j))%4;y=((1-C)*s+C*(u+eps*t+4*j))%4;evaluations+=1
            c=1 if 1<x<2 else 3 if 2<x<3 else None
            if c is None:continue
            lo,hi={(0,1):(1,2),(0,3):(2,3),(2,1):(0,1),(2,3):(3,4)}[u,c]
            assert not lo<y<hi
        rows.append({'depths':[aa,bb],'q':q,'exact_evaluations':evaluations})
    return rows

def main():
    tested=0;first_sheet_failures=0;prefix=[]
    for M in range(E['M_min'],E['M_max']+1):
        D=2*M+1;pairs=[(p,r) for p in range(1,D) for r in range(1,D)]
        for a in range(1,M):
         for b in range(1,M):
          if a==b:continue
          tested+=len(pairs);alive=survivors(a,b,D,pairs);first_sheet_failures+=len(alive)
          for aa,bb in [(2*M-a,b),(a,2*M-b),(2*M-a,2*M-b)]:
            if not alive:break
            alive=survivors(aa,bb,D,alive)
          if alive:
            p,r=alive[0];rows=exact_recheck(M,a,b,p,r)
            out={'status':'FOUR_CAP_MECHANISM_OBSTRUCTION_IN_FIXED_FIBER_CLASS','M':M,'a':a,'b':b,'s':str(F(p,D)),'t':str(F(r,D)),
                 'four_exact_failures':rows,'tested_rooms':tested,'original_sheet_failures':first_sheet_failures,'prefix':prefix,
                 'scope':'No four-cap portal success; orthogonal generators fix full endpoint fibers. NOT a dark room.','effort':E}
            (B/'fixed-fiber-cap-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return
        prefix.append({'M':M,'tested_rooms':tested,'original_sheet_failures':first_sheet_failures})
    out={'status':'ALL_BOUNDED_FIXED_FIBER_CONTROLS_HAVE_A_FOUR_CAP_PORTAL','tested_rooms':tested,'original_sheet_failures':first_sheet_failures,
         'prefix':prefix,'scope':'Bounded evidence only; no unbounded fixed-fiber theorem or global closure.','effort':E}
    (B/'fixed-fiber-cap-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
    try:main()
    except TimeoutError:
        out={'status':'ORIGINAL_DEADLINE_REACHED','effort':E};(B/'fixed-fiber-cap-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
