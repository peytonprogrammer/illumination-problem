"""Independent one-fiber and circle-grid prescribed controls.
Imports only frozen reviewer-owned tracer; reads peer fixed records as data.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sp=spec_from_file_location('own_horizontal',HERE/'horizontal-parity-check.py');M=module_from_spec(sp);sp.loader.exec_module(M)
def exceptional(N,t):return N==1 or (N in (2,4) and t==1) or (N==3 and t==F(2,3))
def main():
    peer=json.loads((BASE/'unequal-depth/one-fiber-check.json').read_text());assert peer['status']=='PRESCRIBED_ONE_FIBER_CONTROLS_PASS'
    paths=[];fiber=0
    for row in peer['paths']:
        s,t,a,b,hm,hp=map(F,row['fixture']);delta=M.rgcd([hm,F(1),hp]);n=(2*a/delta).denominator;L=4*n/delta
        source={M.fold(s+sign*L*(-a)) for sign in (-1,1)}
        targets={M.fold(t+sign*L*(1+b)) for sign in (-1,1)}
        assert len(source)==1 and len(targets)==2
        ss=source.pop();arg=(t+L*(1+b))%4;tt=M.fold(arg)
        assert 1<ss<2 and 1<tt<2
        for sigma in (-1,1):
            for tau in (-1,1):assert M.fold(s+sigma*tau*L*(-a))==ss;fiber+=1
        ds=-1;dt=1 if arg<2 else -1;vy=1+a+b;vx=ds*((tt-ss)-dt*L*vy)
        assert list(map(str,(vx,vy)))==row['original_velocity']
        r=M.trace(row['fixture'],(vx,vy));assert r['contacts']==row['wall_contacts'] and r['edges']==row['edges'] and r['time']==row['time']
        paths.append({'fixture':row['fixture'],'source_image':str(ss),'target_images':sorted(map(str,targets)),'chosen_target_image':str(tt),'n':n,'L':str(L),**r})
    grid=[]
    for N in (*range(1,13),31,64,127):
        cuts={F(0),F(1)}
        for j in range(N):
            for wall in range(4):
                x=(F(wall)-F(4*j,N))%4
                if 0<=x<=1:cuts.add(x)
        xs=sorted(cuts);reps=cuts|{(a+b)/2 for a,b in zip(xs,xs[1:])}
        for t in sorted(reps):
            if not t:continue
            success=any(1<M.fold(t+F(4*j,N))<2 for j in range(N))
            assert success== (not exceptional(N,t)),(N,t)
            grid.append({'N':N,'t':str(t),'success':success})
    # Check every peer breakpoint/control as well, without trusting its verdict.
    for row in peer['grid_cells_checked']:
        N,t=row['N'],F(row['t']);success=any(1<M.fold(t+F(4*j,N))<2 for j in range(N))
        assert success==row['success']==(not exceptional(N,t))
    arithmetic=[]
    qs=(1,2,3,4,5,7,8,9,15,21,25,27)
    for q in qs:
        for r in qs:
            for s in (F(1,3),F(2,3)):
                for t in (F(1,3),F(2,3)):
                    A,B=F(1,q),F(1,r);n=(2*A).denominator;m=(2*B).denominator
                    N=r//gcd(n,r);Q=q//gcd(m,q)
                    forward=int(2*n*A)%2==1 or not exceptional(N,t)
                    reverse=int(2*m*B)%2==1 or not exceptional(Q,s)
                    expected=q%2==0 or r%2==0 or (q!=r and not ((r==3*q and t==F(2,3)) or (q==3*r and s==F(2,3))))
                    assert (forward or reverse)==expected,(q,r,s,t)
                    arithmetic.append({'q':q,'r':r,'s':str(s),'t':str(t),'forward_order':N,'reverse_order':Q,'closed':expected})
    names=['unequal-depth/one-fiber-transport.md','unequal-depth/one-fiber-check.py','unequal-depth/one-fiber-check.json','unequal-depth-independent/horizontal-parity-acceptance.json','unequal-depth-independent/horizontal-parity-check.py','unequal-depth-independent/one-fiber-check.py']
    out={'status':'INDEPENDENT_ONE_FIBER_CONTROLS_PASS','prescribed_forward_paths':len(paths),'actual_paths_with_reverse_and_scaling':3*len(paths),'contacts_including_reverse_and_scaling':sum(2*r['contacts']+r['reverse_contacts'] for r in paths),'source_fiber_identities':fiber,'split_target_fibers':len(paths),'own_continuous_grid_cells':len(grid),'peer_grid_controls_recomputed':len(peer['grid_cells_checked']),'denominator_classification_controls':len(arithmetic),'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names},'paths':paths,'grid':grid,'arithmetic':arithmetic,'limits':'AllN circle lemma and backward fiber transport require separate universal hand proof. Exact fixed paths and rational sign-cell/arithmetic controls do not prove universal rational coverage.'}
    (HERE/'one-fiber-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','paths','grid','arithmetic')}))
if __name__=='__main__':main()
