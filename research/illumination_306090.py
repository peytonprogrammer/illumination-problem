"""Exact 30–60–90 reflection tiles in coordinates (x, sqrt(3)*y).
A is an equilateral-lattice vertex, B a centroid, C a midpoint.
The metric is diag(1,3); angles are counted in units of 30 degrees.
"""
import argparse, itertools, json, time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from illumination_geometry import edge, owners_of, save


def add(a,b): return tuple(a[k]+b[k] for k in (0,1))
def sub(a,b): return tuple(a[k]-b[k] for k in (0,1))
def dot(a,b): return a[0]*b[0]+3*a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def lattice(i,j): return (12*i+6*j,6*j)

def patch(radius):
    tiles=[]; labels={}
    for i in range(-radius,radius):
        for j in range(-radius,radius):
            a,b,c,d=[lattice(*p) for p in [(i,j),(i+1,j),(i,j+1),(i+1,j+1)]]
            for eq in [(a,b,c),(b,c,d)]:
                center=tuple(sum(p[k] for p in eq)//3 for k in (0,1));labels[center]='B'
                for p,q in itertools.combinations(eq,2):
                    mid=tuple((p[k]+q[k])//2 for k in (0,1));labels[mid]='C'
                    for v in (p,q):
                        labels[v]='A';tiles.append(tuple(sorted((v,mid,center))))
    return sorted(tiles),labels

def sectors(tiles,p,opens,owners,labels):
    ids={i for i,t in enumerate(tiles) if p in t};graph=defaultdict(set);wall=False
    if not ids:return [],False
    for e,os in owners.items():
        if p not in e:continue
        if e in opens:
            a,b=os;graph[a].add(b);graph[b].add(a)
        elif any(i in ids for i in os):wall=True
    seen=set();sizes=[]
    for i in ids:
        if i in seen:continue
        seen.add(i);todo=[i];size=0
        while todo:
            k=todo.pop();size+={'A':1,'B':2,'C':3}[labels[p]]
            for q in graph[k]:
                if q not in seen:seen.add(q);todo.append(q)
        sizes.append(size)
    full=not wall and sum(sizes)==12
    return ([] if full else sorted(sizes)),full

def check(data):
    ts=[tuple(sorted(map(tuple,t))) for t in data['triangles']];legal,labels=patch(data['radius'])
    assert len(set(ts))==len(ts) and set(ts)<=set(legal)
    owners=owners_of(ts);cuts={edge(*e) for e in data['slits']}
    assert all(len(owners[e])==2 for e in cuts)
    opens={e for e,os in owners.items() if len(os)==2 and e not in cuts};graph=defaultdict(set)
    # Exact, metric-correct reflections, including agreement of the labeled vertices.
    for e in opens:
        a,b=owners[e];graph[a].add(b);graph[b].add(a);p,q=e;u=next(v for v in ts[a] if v not in e);v=next(v for v in ts[b] if v not in e)
        d=sub(q,p);w=sub(u,p);r=add(p,tuple(2*F(dot(w,d),dot(d,d))*d[k]-w[k] for k in (0,1)))
        assert r==v and labels[u]==labels[v]
    seen={0};todo=[0]
    while todo:
        for j in graph[todo.pop()]:
            if j not in seen:seen.add(j);todo.append(j)
    assert len(seen)==len(ts)
    fulls=[];walls=0;contacts=[]
    for p in {p for t in ts for p in t}:
        sizes,full=sectors(ts,p,opens,owners,labels)
        if full:assert labels[p]=='A';fulls.append(p)
        else:
            assert labels[p]=='A' or 6 not in sizes
            walls+=sum(s!=6 for s in sizes)
            if len(sizes)>1:contacts.append(p)
    assert len(data['marked'])==2 and len(set(map(tuple,data['marked'])))==2 and all(tuple(p) in fulls for p in data['marked'])
    euler=len({p for t in ts for p in t})-len(owners)+len(ts);simple=not cuts and not contacts and euler==1
    if data['require_simple']:assert simple
    return dict(walls=walls,tiles=len(ts),simple=simple,contacts=contacts,slits=len(cuts),interior_A=fulls,certificate='PASS: exact labeled reflection folding and absorbing B/C corners; Wolecki Lemma 3.1')

def draw(data,path):
    from PIL import Image,ImageDraw
    import math
    ts=data['triangles'];pts=[p for t in ts for p in t];x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts);scale=18;pad=50
    im=Image.new('RGB',(int((x1-x0)*scale+2*pad),int((y1-y0)*math.sqrt(3)*scale+2*pad+40)),'#fafafa');d=ImageDraw.Draw(im)
    def xy(p):return ((p[0]-x0)*scale+pad,(y1-p[1])*math.sqrt(3)*scale+pad)
    for t in ts:d.polygon([xy(p) for p in t],fill='#e4ecf5')
    owners=owners_of([tuple(map(tuple,t)) for t in ts]);cuts={edge(*e) for e in data['slits']}
    for e,os in owners.items():d.line([xy(p) for p in e],fill='#122d49' if len(os)==1 or e in cuts else '#b6c6d8',width=4 if len(os)==1 or e in cuts else 1)
    for name,p in zip(('S','T'),data['marked']):
        x,y=xy(p);d.ellipse((x-5,y-5,x+5,y+5),fill='#c0392b');d.text((x+8,y-15),name,fill='#a0251c')
    r=check(data);d.text((pad,im.height-30),f"30–60–90 tiles | {r['walls']} walls | {r['tiles']} tiles",fill='#122d49');im.save(path)

def main():
    from ortools.sat.python import cp_model
    ap=argparse.ArgumentParser();ap.add_argument('--radius',type=int,default=2);ap.add_argument('--slits',type=int,default=1);ap.add_argument('--simple',action='store_true');ap.add_argument('--seconds',type=float,default=90);ap.add_argument('--max-walls',type=int);ap.add_argument('--out',default='306090');args=ap.parse_args();started=time.monotonic();ts,labels=patch(args.radius);owners=owners_of(ts);shared={e:o for e,o in owners.items() if len(o)==2};model=cp_model.CpModel();x=[model.new_bool_var(f't{i}') for i in range(len(ts))];op={e:model.new_bool_var(f'o{k}') for k,e in enumerate(shared)};cuts={}
    for k,(e,(a,b)) in enumerate(shared.items()):
        model.add(op[e]<=x[a]);model.add(op[e]<=x[b]);c=model.new_bool_var(f'c{k}');cuts[e]=c;model.add(c==x[a]+x[b]-op[e]-1).only_enforce_if([x[a],x[b]]);model.add(c<=x[a]);model.add(c<=x[b]);model.add(c+op[e]<=1)
    model.add(sum(cuts.values())<=args.slits);costs=[];fulls={};used=[]
    # Full-patch stars, restricted to each local selected subset, are checked by a fan graph.
    for p in sorted(labels):
        ids=[i for i,t in enumerate(ts) if p in t];es=[e for e in shared if p in e];rows=[];localowners={e:o for e,o in owners.items() if p in e}
        for mask in range(1<<len(ids)):
            bits=[(mask>>j)&1 for j in range(len(ids))];chosen={i for i,b in zip(ids,bits) if b};eligible=[e for e in es if set(shared[e])<=chosen]
            for count in range(min(args.slits,len(eligible))+1):
                for closed in itertools.combinations(eligible,count):
                    oe=set(eligible)-set(closed)
                    # Tile fan components; edge joins exist exactly at oe.
                    graph=defaultdict(set)
                    for e in oe:a,b=shared[e];graph[a].add(b);graph[b].add(a)
                    seen=set();sizes=[]
                    for i in chosen:
                        if i in seen:continue
                        seen.add(i);todo=[i];size=0
                        while todo:
                            k=todo.pop();size+={'A':1,'B':2,'C':3}[labels[p]]
                            for q in graph[k]:
                                if q not in seen:seen.add(q);todo.append(q)
                        sizes.append(size)
                    full=sum(sizes)==12 and all(e in oe for e,o in localowners.items() if any(i in chosen for i in o))
                    if full:sizes=[]
                    if labels[p]!='A' and (full or 6 in sizes):continue
                    if args.simple and len(sizes)>1:continue
                    rows.append(bits+[int(e in oe) for e in es]+[sum(s!=6 for s in sizes),int(full)])
        c=model.new_int_var(0,12,f'cost{p}');f=model.new_bool_var(f'full{p}');costs.append(c);fulls[p]=f;model.add_allowed_assignments([x[i] for i in ids]+[op[e] for e in es]+[c,f],rows);u=model.new_bool_var(f'used{p}');model.add_max_equality(u,[x[i] for i in ids]);used.append(u)
    model.add(fulls[(0,0)]==1);model.add(sum(f for p,f in fulls.items() if p!=(0,0) and labels[p]=='A')>=1)
    if args.simple:
        model.add(sum(cuts.values())==0);ue=[]
        for k,os in enumerate(owners.values()):u=model.new_bool_var(f'e{k}');model.add_max_equality(u,[x[i] for i in os]);ue.append(u)
        model.add(sum(used)-sum(ue)+sum(x)==1)
    root=next(i for i,t in enumerate(ts) if (0,0) in t);model.add(x[root]==1);rank=[model.new_int_var(0,len(ts)-1,f'r{i}') for i in range(len(ts))];model.add(rank[root]==0);parents=[[] for t in ts]
    for e,(a,b) in shared.items():
        for u,v in [(a,b),(b,a)]:par=model.new_bool_var(f'p{u}_{v}');parents[v].append(par);model.add(par<=op[e]);model.add(rank[v]>=rank[u]+1).only_enforce_if(par)
    for i in range(len(ts)):model.add(sum(parents[i])==(0 if i==root else x[i]))
    walls=sum(costs)
    if args.max_walls is not None:model.add(walls<=args.max_walls)
    model.minimize(walls);solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_search_workers=4
    print(json.dumps(dict(event='model',tiles=len(ts),build_seconds=time.monotonic()-started,args=vars(args))),flush=True)
    class Capture(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            marks=[(0,0),next(p for p,f in fulls.items() if p!=(0,0) and labels[p]=='A' and self.value(f))];data=dict(triangles=[t for i,t in enumerate(ts) if self.value(x[i])],slits=[e for e,c in cuts.items() if self.value(c)],marked=marks,radius=args.radius,require_simple=args.simple,search=vars(args));r=check(data);assert r['walls']==round(self.objective_value);base=Path(__file__).parent;save(base/(args.out+'.json'),data);draw(data,base/(args.out+'.png'));print(json.dumps(dict(event='candidate',**r)),flush=True)
    status=solver.solve(model,Capture());r=dict(status=solver.status_name(status),best=solver.objective_value if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None,lower_bound=solver.best_objective_bound,solve_seconds=solver.wall_time,total_seconds=time.monotonic()-started,args=vars(args));save(Path(__file__).parent/(args.out+'-result.json'),r);print(json.dumps(r),flush=True)
if __name__=='__main__':main()
