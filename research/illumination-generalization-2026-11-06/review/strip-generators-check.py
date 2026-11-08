"""Four prescribed exact geometric normal forms and cut trees. No optical search."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import importlib.util,json,time,signal
H=Path(__file__).resolve().parent
e=json.loads((H/'strip-generators-effort.json').read_text())
deadline=datetime.fromisoformat(e['aggregate_deadline_utc']).timestamp()
assert time.time()<deadline,'Original R19 deadline expired'
signal.alarm(max(1,int(deadline-time.time())))
sp=importlib.util.spec_from_file_location('own',H/'resumed-exact-check.py')
own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
def base(p,S,T):
    p=[(x-S[0],y-S[1]) for x,y in p];T=(T[0]-S[0],T[1]-S[1]);S=(0,0)
    own.simple(p);assert own.location(p,S)==own.location(p,T)==1
    maps=[];parameters=[]
    for axis in (0,1):
        levels=sorted({z[axis] for z in p}|{0,T[axis]});s=levels.index(0)
        gaps=[b-a for a,b in zip(levels,levels[1:])]
        residues=[1 if d%2 else 2 for d in gaps]
        counts=[(d-r)//2 for d,r in zip(gaps,residues)]
        assert min(counts)>=0
        baselevels=[None]*len(levels);baselevels[s]=0
        for j in range(s,len(gaps)):baselevels[j+1]=baselevels[j]+residues[j]
        for j in range(s-1,-1,-1):baselevels[j]=baselevels[j+1]-residues[j]
        rebuilt=[None]*len(levels);rebuilt[s]=0
        for j in range(s,len(gaps)):rebuilt[j+1]=rebuilt[j]+residues[j]+2*counts[j]
        for j in range(s-1,-1,-1):rebuilt[j]=rebuilt[j+1]-residues[j]-2*counts[j]
        assert rebuilt==levels
        assert max(baselevels)-min(baselevels)<=2*(len(p)+1)
        maps.append(dict(zip(levels,baselevels)))
        parameters.append({'axis':axis,'residues':residues,'unbounded_counts':counts,'levels':levels,'base_levels':baselevels})
    bp=[tuple(maps[k][z[k]] for k in (0,1)) for z in p]
    bt=tuple(maps[k][T[k]] for k in (0,1))
    own.simple(bp);assert own.location(bp,S)==own.location(bp,bt)==1
    assert all(c%2==0 for c in bt)
    return {'walls':len(p),'base_polygon':bp,'base_source':S,'base_target':bt,'parameters':parameters}
def tree(p,c):
    xs=sorted({Q(z[0]) for z in p}|{Q(c)});ys=sorted({Q(z[1]) for z in p})
    c=Q(c);cut=xs.index(c);assert 0<cut<len(xs)-1
    assert c not in {z[0] for z in p}
    cells=set()
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            if own.location(p,((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2))==1:cells.add((i,j))
    components={};label=0
    for cell in sorted(cells):
        if cell in components:continue
        todo=[cell];components[cell]=label
        while todo:
            i,j=todo.pop()
            for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                nb=(i+di,j+dj)
                if nb in cells and nb not in components and (nb[0]<cut)==(i<cut):
                    components[nb]=label;todo.append(nb)
        label+=1
    mouths=[]
    for j in range(len(ys)-1):
        l,r=(cut-1,j),(cut,j)
        if l in cells and r in cells:
            pair=(components[l],components[r])
            if mouths and mouths[-1]['top']==ys[j]:
                assert mouths[-1]['components']==pair;mouths[-1]['top']=ys[j+1]
            else:mouths.append({'bottom':ys[j],'top':ys[j+1],'components':pair})
    parent=list(range(label))
    def root(x):
        while parent[x]!=x:x=parent[x]
        return x
    degree=[0]*label
    for m in mouths:
        a,b=m['components'];degree[a]+=1;degree[b]+=1
        a,b=root(a),root(b);assert a!=b;parent[a]=b
    assert len({root(k) for k in range(label)})==1
    assert label==len(mouths)+1 and len(mouths)<=len(p)//4
    return {'cut_coordinate':c,'parallel_necks':len(mouths),'fixed_chambers':label,'tree_degrees':sorted(degree),'mouths':mouths}

comb=[(0,0),(20,0),(20,4),(4,4),(4,8),(20,8),(20,12),(4,12),(4,16),(20,16),(20,20),(4,20),(4,24),(20,24),(20,28),(4,28),(4,32),(20,32),(20,36),(0,36)]
fixtures=[('rectangle',[(0,0),(38,0),(38,22),(0,22)],(8,6),(30,18),19,False,1),
          ('primitive_L',[(0,0),(17,0),(17,8),(8,8),(8,16),(0,16)],(4,4),(4,12),6,False,1),
          ('U_same_side_middle',[(0,0),(20,0),(20,12),(14,12),(14,4),(6,4),(6,12),(0,12)],(2,10),(18,10),7,True,2),
          ('five_neck_comb',comb,(8,2),(8,34),6,False,5)]
rows=[]
for name,p,S,T,c,swap,expected in fixtures:
    assert time.time()<deadline
    normal=base(p,S,T)
    oriented=[(y,x) for x,y in p] if swap else p
    cut=tree(oriented,c);assert cut['parallel_necks']==expected
    rows.append({'name':name,'normal_form':normal,'cut_tree':cut})
assert rows[-1]['cut_tree']['tree_degrees']==[1,1,1,1,1,5]
out={'status':'EXACT_ALL_ORTHOGONAL_NORMAL_FORM_AND_CUT_CONTROLS_PASS','rows':rows,'within_original_deadline':time.time()<deadline,'whole_goal_complete':False,'optical_equivalence_claim':False,'independent_acceptance':False}
(H/'strip-generators-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
signal.alarm(0)
print(json.dumps({'status':out['status'],'normal_forms':len(rows),'neck_counts':[r['cut_tree']['parallel_necks'] for r in rows],'comb_tree_degrees':rows[-1]['cut_tree']['tree_degrees']}))
