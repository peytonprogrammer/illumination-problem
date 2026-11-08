"""Structural checks of the fan-tree proof on34frozen rooms, no optical scan."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib
if not __debug__:raise RuntimeError('Run without -O')
B=Path(__file__).resolve().parent
ns={'__name__':'frozen_cell_builder','__file__':str(B/'inputs/twist_origami.py')}
source=(B/'inputs/twist_origami.py').read_text();assert source.count('return r,u,lab,sstart')==1
exec(compile(source.replace('return r,u,lab,sstart','return r,u,lab,sstart,tris,sqs,sq'),str(B/'inputs/twist_origami.py'),'exec'),ns)


def inside(V,p):
    result=False
    for a,b in zip(V,V[1:]+V[:1]):
        det=(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        between=sum((p[j]-a[j])*(p[j]-b[j]) for j in (0,1))<=0
        if not det and between:return 'boundary'
        if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<a[0]+F(p[1]-a[1],b[1]-a[1])*(b[0]-a[0]):result=not result
    return 'inside' if result else 'outside'


def cycles(p):
    assert sorted(p)==list(range(len(p)))
    todo=set(range(len(p)));out=[]
    while todo:
        x=min(todo);c=[]
        while x in todo:c.append(x);todo.remove(x);x=p[x]
        assert x==c[0];out.append(c)
    return out


def examine(room):
    V=list(map(tuple,room['vertices']));s,t=map(tuple,room['marked'])
    r,u,lab,s0,tris,sqs,sq=ns['build'](V,s,t)
    edges=defaultdict(list);stars=defaultdict(list)
    octants=[(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
    for i,tri in enumerate(tris):
        a,b,c=tri;assert ns['cls'](a)==0 and ns['cls'](b)==2 and ns['cls'](c)==1
        stars[a].append(octants.index((b[0]+c[0]-2*a[0],b[1]+c[1]-2*a[1])))
        for j in range(3):edges[frozenset((tri[j],tri[(j+1)%3]))].append(i)
    assert all(len(ts) in (1,2) for ts in edges.values())
    adjacency={a:[] for a in stars};cuts=[];nonproper=[]
    for edge,ts in edges.items():
        if len(ts)!=2:continue
        classes=sorted(ns['cls'](p) for p in edge)
        aa,bb=tris[ts[0]][0],tris[ts[1]][0]
        if classes==[1,2]:
            assert aa!=bb;adjacency[aa].append(bb);adjacency[bb].append(aa)
            cuts.append({'edge':sorted(edge),'A_centers':[aa,bb]})
            if any(inside(V,p)!='boundary' for p in edge):nonproper.append(sorted(edge))
        else:assert aa==bb
    todo=[next(iter(stars))];seen={todo[0]}
    for a in todo:
        for c in adjacency[a]:
            if c not in seen:seen.add(c);todo.append(c)
    assert len(seen)==len(stars)
    fans_contiguous=True
    for a,indices in stars.items():
        assert len(indices)==len(set(indices))
        bits=[int(j in indices) for j in range(8)]
        fans_contiguous &= sum(bits[j]!=bits[(j+1)%8] for j in range(8)) in (0,2)
    forbidden=[]
    for x in range(min(p[0] for p in V),max(p[0] for p in V)+1):
        for y in range(min(p[1] for p in V),max(p[1] for p in V)+1):
            if ns['cls']((x,y))!=0 and inside(V,(x,y))=='inside':forbidden.append((x,y))
    result={'tag':room['tag'],'triangles':len(tris),'A_fans':len(stars),'BC_crosscuts':len(cuts),
        'fan_graph_tree':len(cuts)==len(stars)-1,'fans_contiguous':fans_contiguous,
        'nonproper_cut_count':len(nonproper),'interior_nonA':forbidden,'cuts':cuts,'axis_cycles':{}}
    for axis,p in ((0,r),(1,u)):
        cs=cycles(p);G=((-1,0),(0,1)) if axis==0 else ((1,0),(0,-1))
        rho=[]
        for pair in sqs:
            targets={sq[(ti,ns['mul'](G,g))] for ti,g in pair};assert len(targets)==1
            rho.append(targets.pop())
        inverse=[0]*len(p)
        for j,q in enumerate(p):inverse[q]=j
        assert all(rho[rho[j]]==j and rho[p[j]]==inverse[rho[j]] for j in range(len(p)))
        counts=[];self_reversed=[]
        for c in cs:
            hits=0
            for index in c:
                for ti,g in sqs[index]:
                    tri=tris[ti];pts=[ns['ap'](g,p) for p in tri];hi=max(p[axis] for p in pts)
                    for j,z in enumerate(pts):
                        zz=pts[(j+1)%3];a,b=tri[j],tri[(j+1)%3]
                        if z[axis]==zz[axis]==hi and len(edges[frozenset((a,b))])==1:
                            assert a[0]==b[0] or a[1]==b[1];hits+=1
            counts.append(hits);self_reversed.append({rho[x] for x in c}==set(c))
        result['axis_cycles']['horizontal' if axis==0 else 'vertical']={'count':len(cs),'normal_reflection_counts':counts,'all_self_reversed':all(self_reversed)}
    return result


# Symbolic same-portal obstruction, linear polynomials in r.
K=[((1,0),(0,1)),((-1,0),(0,-1)),((0,1),(1,0)),((0,-1),(-1,0))]
roots=[]
for R in K:
    equations=[(F(R[0][0]+1),F(R[0][1])),(F(R[1][0]),F(R[1][1]-1))]
    candidate=None;possible=True
    for a,b in equations:
        if not b:
            if a:possible=False
        elif candidate is None:candidate=-a/b
        elif candidate!=-a/b:possible=False
    assert not(possible and candidate is None),'portal identity for all r'
    if possible:assert candidate in (-1,0,1);roots.append(str(candidate))
selection=json.loads((B/'inputs/holdouts/selection.json').read_text());assert len(selection)==34
files=[B/'inputs/holdouts'/f"{entry['tag']}.json" for entry in selection]
rooms=[]
for path in files:
    room=json.loads(path.read_text());r=examine(room)
    assert not r['interior_nonA'] and not r['nonproper_cut_count']
    assert r['fan_graph_tree'] and r['fans_contiguous']
    for a in r['axis_cycles'].values():assert a['all_self_reversed'] and all(x==2 for x in a['normal_reflection_counts'])
    rooms.append(r)
    print(json.dumps({k:v for k,v in r.items() if k not in ('cuts','axis_cycles')}),flush=True)
# Prescribed controls: one complete A star, and a diamond outside the theorem.
star={'tag':'complete_A_star_control','vertices':[[-1,-1],[1,-1],[1,1],[-1,1]],'marked':[[0,0],[1,0]]}
diamond={'tag':'interior_C_diamond_negative_control','vertices':[[2,0],[0,2],[-2,0],[0,-2]],'marked':[[0,0],[0,1]]}
star_result=examine(star);assert star_result['A_fans']==1 and star_result['fan_graph_tree']
assert all(x['all_self_reversed'] and all(n==2 for n in x['normal_reflection_counts']) for x in star_result['axis_cycles'].values())
diamond_result=examine(diamond);assert diamond_result['interior_nonA'] and not diamond_result['fan_graph_tree']
assert all(not x['all_self_reversed'] and all(n==0 for n in x['normal_reflection_counts']) for x in diamond_result['axis_cycles'].values())
summary={'frozen_rooms':len(rooms),'horizontal_cycles':sum(r['axis_cycles']['horizontal']['count'] for r in rooms),'vertical_cycles':sum(r['axis_cycles']['vertical']['count'] for r in rooms),'all_fan_graphs_trees':True,'all_axis_cycles_have_two_normal_reflections':True,'same_portal_symbolic_exception_roots':roots}
out={'status':'EXACT_FAN_TREE_AND_AXIS_REFLECTION_PASS','summary':summary,'rooms':rooms,'controls':[star_result,diamond_result],
 'input_sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files+[B/'inputs/holdouts/selection.json',B/'inputs/twist_origami.py']},
 'scope':'Structural permutation/cellulation checks on34preselected rooms and two prescribed controls. No new room, direction, event, word or ray discovery.'}
(B/'axis-alignment.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,indent=2))
