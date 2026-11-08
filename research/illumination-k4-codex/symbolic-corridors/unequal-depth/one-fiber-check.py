"""Exact controls for one-fiber transport, not direction discovery."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import importlib.util,json,hashlib
B=Path(__file__).parent
spec=importlib.util.spec_from_file_location('own_frozen_horizontal',B/'horizontal-parity-check.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def main():
    grid=[]
    for N in (1,2,3,4,5,6,7,8,9,16,31):
        # Breakpoints at which a grid point meets 1,2,3; one representative per open interval.
        cuts={F(0),F(1)}
        for j in range(N):
            for z in (1,2,3):
                for k in (-1,0,1):
                    t=F(z+4*k)-F(4*j,N)
                    if 0<=t<=1:cuts.add(t)
        cuts=sorted(cuts);reps=cuts+[ (x+y)/2 for x,y in zip(cuts,cuts[1:]) ]
        for t in reps:
            if not 0<t<=1:continue
            success=any(1<m.fold(t+F(4*j,N))<2 for j in range(N))
            exceptional=N==1 or (N in (2,4) and t==1) or (N==3 and t==F(2,3))
            assert success!=exceptional
            grid.append({'N':N,'t':str(t),'success':success})
    fixtures=[('1/2','1/4','1/2','1/3','2','2'),
              ('1/3','1/3','1/2','1/3','2','2'),
              ('1/2','1/4','1/2','2/3','2','2'),
              ('1/3','1/4','1/4','1/6','3/2','5/2'),
              ('2/5','1/4','1/6','1/9','2','3')]
    paths=[]
    for raw in fixtures:
        s,t,a,b,hm,hp=map(F,raw);delta=m.rgcd([hm,F(1),hp]);n=(2*a/delta).denominator;L=4*n/delta
        rr=2*n*a/delta;assert rr.denominator==1 and int(rr)%2==1
        ss=m.fold(s-L*a);arg=(t+L*(1+b))%4;tt=m.fold(arg)
        assert 1<ss<2 and 1<tt<2 and arg not in (0,2)
        source_images={m.fold(s+sigma*tau*L*(-a)) for sigma in (-1,1) for tau in (-1,1)}
        target_images={m.fold(t+sigma*tau*L*(1+b)) for sigma in (-1,1) for tau in (-1,1)}
        assert source_images=={ss} and len(target_images)==2
        ds=-1;dt=1 if arg<2 else -1;vy=1+a+b;vx=ds*((tt-ss)-dt*L*vy)
        result=m.trace(s,t,a,b,hm,hp,vx,vy)
        paths.append({'fixture':raw,'n':n,'L':str(L),'source_image':str(ss),'selected_target_image':str(tt),
                      'other_target_images':sorted(map(str,target_images)),'original_velocity':[str(vx),str(vy)],**result})
    out={'status':'PRESCRIBED_ONE_FIBER_CONTROLS_PASS','grid_cells':len(grid),'physical_paths':len(paths),
         'wall_contacts':sum(r['wall_contacts'] for r in paths),'paths':paths,'grid_cells_checked':grid,
         'frozen_dependency_sha256':{'horizontal-parity-check.py':hashlib.sha256((B/'horizontal-parity-check.py').read_bytes()).hexdigest()},
         'scope':'Candidate hand theorem; exact prescribed controls only; fullgoalOPEN.'}
    (B/'one-fiber-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('grid_cells_checked',)}))
if __name__=='__main__':main()
