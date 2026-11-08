"""Prescribed exact both-corner purification, not another chart search."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util,json
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',H/'resumed-exact-check.py')
own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
w=list(map(Q,[10,3,2,1])); y=list(map(Q,[0,3,4,5,10])); C=[0,20,26,30]
S=(Q(6),Q(1));T=(Q(1,2),Q(49,8));tau=Q(4);start=Q(-1);end=20-T[1]
def phase(q,j):return S[0]+tau*(q-start)-C[j]
assert phase(0,0)==10 and phase(10,3)==20
assert own.fold(phase(S[1],0),w[0])==S[0]
assert own.fold(phase(T[1],3),w[3])==own.fold(phase(end,3),w[3])==T[0]
events={S[1],T[1],Q(3),Q(4),Q(5)}
bounds=[S[1],Q(3),Q(4),Q(5),T[1]]
for j in range(4):
    a,b=bounds[j:j+2]
    for n in range(int(phase(a,j)//w[j])-1,int(phase(b,j)//w[j])+2):
        q=start+(n*w[j]+C[j]-S[0])/tau
        if a<q<b:events.add(q)
path=[]
for q in sorted(events):
    j=max(i for i in range(4) if y[i]<=q)
    path.append((own.fold(phase(q,j),w[j]),q))
assert path[0]==S and path[-1]==T
out={'status':'BOTH_CONVEX_CORNER_EXCURSIONS_REMOVED','S':S,'T':T,'slope':tau,'source_revisit_parameter':S[1],'target_early_parameter':T[1],'discarded_floor_parameter':0,'discarded_roof_parameter':10,'path':path,**own.path_check(own.nested_polygon(w,y),path),'whole_goal_complete':False}
(H/'four-chart-corner-control.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('path','S','T','slope')} ,default=str))
