"""Reconstruct primary-source vector figures; no ray or room search."""
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations
import xml.etree.ElementTree as ET
import re,json,hashlib
D=Path(__file__).resolve().parent
P=D/'novelty-inputs'
NS={'s':'http://www.w3.org/2000/svg'}
def parse(d):
    ts=re.findall(r'[MHVLZ]|[-+]?(?:\d*\.\d+|\d+)',d);i=0;pts=[];cmd=None;x=y=0
    while i<len(ts):
        if ts[i].isalpha():cmd=ts[i];i+=1
        if cmd=='Z':break
        if cmd in ('M','L'):
            x,y=map(float,ts[i:i+2]);i+=2;cmd='L'
        elif cmd=='H':x=float(ts[i]);i+=1
        elif cmd=='V':y=float(ts[i]);i+=1
        else:raise ValueError(cmd)
        pts.append((x,y))
    if len(pts)>1 and pts[-1]==pts[0]:pts.pop()
    return pts

def edge(a,b):return tuple(sorted((a,b)))
def boundary(tris):
    c=Counter(edge(t[i],t[(i+1)%len(t)]) for t in tris for i in range(len(t)))
    assert all(n in (1,2) for n in c.values())
    return {e for e,n in c.items() if n==1}
def receipt(es):
    g=defaultdict(set)
    for a,b in es:g[a].add(b);g[b].add(a)
    contacts={str(p):len(ns) for p,ns in g.items() if len(ns)!=2}
    smooth=[]
    for p,ns in g.items():
        if len(ns)==2:
            a,b=list(ns)
            if (a[0]-p[0])*(b[1]-p[1])==(a[1]-p[1])*(b[0]-p[0]):smooth.append(p)
    seen=set();components=0
    for p in g:
        if p not in seen:
            components+=1;todo=[p];seen.add(p)
            while todo:
                q=todo.pop()
                for v in g[q]-seen:seen.add(v);todo.append(v)
    axis=all(a[0]==b[0] or a[1]==b[1] for a,b in es)
    if axis:
        for (a,b),(c,d) in combinations(es,2):
            if a[0]==b[0] and c[1]==d[1]:
                q=(a[0],c[1])
                if min(a[1],b[1])<=q[1]<=max(a[1],b[1]) and min(c[0],d[0])<=q[0]<=max(c[0],d[0]):assert q in {a,b}&{c,d}
            elif a[1]==b[1] and c[0]==d[0]:
                q=(c[0],a[1])
                if min(a[0],b[0])<=q[0]<=max(a[0],b[0]) and min(c[1],d[1])<=q[1]<=max(c[1],d[1]):assert q in {a,b}&{c,d}
            elif a[0]==b[0]==c[0]==d[0]:assert min(max(a[1],b[1]),max(c[1],d[1]))<=max(min(a[1],b[1]),min(c[1],d[1]))
            elif a[1]==b[1]==c[1]==d[1]:assert min(max(a[0],b[0]),max(c[0],d[0]))<=max(min(a[0],b[0]),min(c[0],d[0]))
    return dict(unit_edges=len(es),maximal_segments=len(es)-len(smooth),boundary_components=components,non_degree_two_vertices=contacts,all_axis_aligned=all(a[0]==b[0] or a[1]==b[1] for a,b in es),jordan_cycle_graph=components==1 and not contacts,edges=sorted(es))

root=ET.parse(P/'wolecki-figure.svg').getroot();triangles=[];residual=0
for t in root.findall('.//s:path',NS):
    if t.get('fill-opacity')!='.1':continue
    ps=parse(t.attrib['d']);assert len(ps)==3
    grid=[]
    for p in ps:
        q=tuple(round(v/56.693635) for v in p)
        residual=max(residual,*(abs(v/56.693635-w) for v,w in zip(p,q)));grid.append(q)
    triangles.append(grid)
assert residual<0.000001
assert (P/'wolecki-v1-source-22gon_vert.pdf').read_bytes()==(P/'wolecki-source-22gon_vert.pdf').read_bytes()
w=receipt(boundary(triangles));w['triangles']=len(triangles);w['vector_to_integer_max_error']=residual
assert w['maximal_segments']==22
assert w['non_degree_two_vertices']=={'(2, 0)':4}
root=ET.parse(P/'orourke-figure.svg').getroot()
t=next(t for t in root.findall('.//s:path',NS) if t.get('fill')=='#eff8fb')
ps=parse(t.attrib['d']);grid=[tuple(round(v/72) for v in p) for p in ps]
assert all(abs(v/72-q)<1e-8 for p,g in zip(ps,grid) for v,q in zip(p,g))
o=receipt({edge(grid[i],grid[(i+1)%len(grid)]) for i in range(len(grid))})
assert o['maximal_segments']==34 and o['jordan_cycle_graph'] and o['all_axis_aligned']
room=json.loads((D/'peer-fast-inputs/cand-2_2-1.json').read_text());c=receipt(boundary([[tuple(p) for p in t] for t in room['triangles']]))
assert c['maximal_segments']==22 and c['all_axis_aligned'] and c['jordan_cycle_graph']
# Grid edges intersect only at integer endpoints; degree 2 and one component suffice here.
files=['novelty-inputs/wolecki-v1-source-22gon_vert.pdf','novelty-inputs/wolecki-source-22gon_vert.pdf','novelty-inputs/wolecki-figure.svg','novelty-inputs/orourke-orthogonal.pdf','novelty-inputs/orourke-figure.svg','peer-fast-inputs/cand-2_2-1.json']
out=dict(status='PASS',scope='Geometry comparison, not darkness or historical priority. Wolecki integer normalization is explicit with a bounded rounding residual.',wolecki_v3=w,orourke=o,candidate=c,sha256={f:hashlib.sha256((D/f).read_bytes()).hexdigest() for f in files})
(D/'novelty-geometry-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{n:v for n,v in r.items() if n!='edges'} for k,r in [('wolecki',w),('orourke',o),('candidate',c)]},indent=2))
