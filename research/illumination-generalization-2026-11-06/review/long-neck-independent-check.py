"""Four independently constructed prescribed neck paths, no angle or room search."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util,json
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',H/'resumed-exact-check.py')
own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
rows=[]
for sigma in (-1,1):
    for L in (Q(7),Q(37)):
        beta=Q(3) if sigma==-1 else Q(-1)
        c=sigma*beta-3;D=L+10
        lower=(D*Q(-3,5)-c)/4
        n=lower//1+1
        tau=(c+4*n)/D
        assert Q(-3,5)<tau<Q(-1,3)
        zl=3+5*tau;zr=beta-5*sigma*tau
        assert 0<zl<2 and 0<zr<2 and zl+L*tau==4*n+sigma*zr
        if sigma==-1:
            p=[(-6,0),(L+4,0),(L+4,4),(L+2,4),(L+2,2),(-2,2),(-2,4),(-4,4),(-4,1),(-6,1)]
        else:
            p=[(-6,0),(L+2,0),(L+2,-2),(L+4,-2),(L+4,2),(-2,2),(-2,4),(-4,4),(-4,1),(-6,1)]
        p=[tuple(map(Q,z)) for z in p];own.simple(p)
        S=(Q(-3),Q(3));T=(L+3,beta)
        neck=[(Q(0),zl),(L,zr)]
        zlast=zl+L*tau
        for k in range(int(zlast//2)-1,int(zl//2)+2):
            x=(2*k-zl)/tau
            if 0<x<L:neck.append((x,Q(0 if k%2==0 else 2)))
        neck.sort()
        path=[S,(Q(-4),3+tau)]+neck+[(L+4,beta-sigma*tau),T]
        guards=own.path_check(p,path)
        assert guards['reflections']==len(neck) # two end mirrors plus len(neck)-2 neck mirrors
        rows.append({'sigma':sigma,'L':L,'slope':tau,'n':n,'source':S,'target':T,'path':path,**guards})
out={'status':'INDEPENDENT_NECK_CONTROLS_PASS','rows':rows,'total_reflections':sum(r['reflections'] for r in rows),'total_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False}
(H/'long-neck-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
