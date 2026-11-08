#!/usr/bin/env python3
"""Exactly the frozen22 single-vertex deletions; no optical search."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
from math import gcd
import json, hashlib, signal, time
ROOT=Path(__file__).resolve().parent
EFFORT=json.loads((ROOT/'local-surgery-effort.json').read_text())
DEADLINE=datetime.fromisoformat(EFFORT['aggregate_deadline_utc']).timestamp()
if time.time()>=DEADLINE:
    raise SystemExit('Original A15 aggregate deadline expired; no restart')
signal.alarm(max(1,int(DEADLINE-time.time())))
P=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),
   (2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),
   (5,1),(4,1),(4,2),(3,2),(3,3),(1,3),
   (1,2),(0,2),(0,1),(-1,1)]
S=(0,0);T=(2,2)
def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on(a,b,z):
    return cross(a,b,z)==0 and all(min(a[k],b[k])<=z[k]<=max(a[k],b[k]) for k in (0,1))
def intersects(a,b,c,d):
    o1,o2,o3,o4=cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
    if any((z==0 and on(u,v,w)) for z,u,v,w in [(o1,a,b,c),(o2,a,b,d),(o3,c,d,a),(o4,c,d,b)]):return True
    return (o1>0)!=(o2>0) and (o3>0)!=(o4>0)
def edges(p):return list(zip(p,p[1:]+p[:1]))
def simple(p):
    n=len(p)
    if len(set(p))!=n:return False
    for j,(a,b) in enumerate(edges(p)):
        if a==b:return False
        for l,(c,d) in enumerate(edges(p)):
            if l<=j or l==j+1 or (j==0 and l==n-1):continue
            if intersects(a,b,c,d):return False
    return True
def where(p,z):
    if any(on(a,b,z) for a,b in edges(p)):return 'boundary'
    hit=False
    for a,b in edges(p):
        if (a[1]>z[1])!=(b[1]>z[1]):
            x=F(a[0])+F((b[0]-a[0])*(z[1]-a[1]),b[1]-a[1])
            if x>z[0]:hit=not hit
    return 'interior' if hit else 'outside'
def canonical_edge(a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]
    if dx==0 or dy==0:return True
    return abs(dx)==abs(dy) and (a[0]+a[1])%2==0

def count(p):
    J=[];smooth=[];As=[];corner=set(p)
    for x in range(min(a[0] for a in p),max(a[0] for a in p)+1):
        for y in range(min(a[1] for a in p),max(a[1] for a in p)+1):
            z=(x,y);loc=where(p,z);A=x%2==0 and y%2==0
            if loc=='interior':
                (As if A else J).append(z)
            elif loc=='boundary' and z not in corner and not A:smooth.append(z)
    return {'I':len(As),'J':len(J),'s_N':len(smooth),'k':len(J)+len(smooth),
            'interior_A':As,'interior_non_A':J,'smooth_non_A':smooth}
assert simple(P) and count(P)['k']==4
rows=[]
for i,v in enumerate(P):
    if time.time()>=DEADLINE:raise SystemExit('A15 aggregate deadline reached')
    poly=P[:i]+P[i+1:];prev=P[i-1];nxt=P[(i+1)%len(P)]
    canonical=canonical_edge(prev,nxt)
    dx,dy=nxt[0]-prev[0],nxt[1]-prev[1]
    diagonal45=abs(dx)==abs(dy)
    strict=simple(poly)
    endpoint_status=[where(poly,S),where(poly,T)] if strict else None
    eligible=diagonal45 and strict and endpoint_status==['interior','interior']
    row={'deleted_index':i,'deleted_vertex':v,'new_edge':[prev,nxt],
         'canonical_edge':canonical,'geometric_diagonal45':diagonal45,'strictly_simple':strict,'endpoint_status':endpoint_status,'eligible':eligible}
    if eligible:
        walls=sum(cross(poly[j-1],poly[j],poly[(j+1)%len(poly)])!=0 for j in range(len(poly)))
        factor=1 if canonical else 2
        rep=[(factor*x,factor*y) for x,y in poly]
        counts=count(rep)
        assert walls<=21 and all(canonical_edge(a,b) for a,b in edges(rep))
        assert where(rep,(factor*S[0],factor*S[1]))=='interior' and where(rep,(factor*T[0],factor*T[1]))=='interior'
        row.update({'W':walls,'canonical_representative_factor':factor,**counts,
          'covered_by_baseline':counts['k']<=6,'canonical_polygon':rep,
          'marked':[(factor*S[0],factor*S[1]),(factor*T[0],factor*T[1])]})
    rows.append(row)
valid=[r for r in rows if r['eligible']]
result={'kind':'EXACT_PRESCRIBED_GEOMETRY_AUDIT_NOT_RAY_SEARCH',
        'effort':'A15','ended_utc':datetime.now(timezone.utc).isoformat(),
        'within_original_deadline':time.time()<DEADLINE,'original_polygon':P,'S':S,'T':T,
        'original_counts':count(P),'deletions_checked':len(rows),'eligible_count':len(valid),
        'eligible_k_values':sorted(set(r['k'] for r in valid)),
        'all_eligible_covered_by_accepted_theorem':all(r['covered_by_baseline'] for r in valid),
        'rows':rows,'dark_counterexample':False,'independent_review':False,
        'source_geometry':'.context/illumination-k4-codex/preprint-review-codex/revised.tex, equation vertices',
        'geometry_source_sha256':hashlib.sha256((ROOT.parents[1]/'illumination-k4-codex/preprint-review-codex/revised.tex').read_bytes()).hexdigest()}
(ROOT/'local-surgery-check.json').write_text(json.dumps(result,indent=2)+'\n')
signal.alarm(0)
print(json.dumps({k:result[k] for k in ['deletions_checked','eligible_count','eligible_k_values','within_original_deadline','all_eligible_covered_by_accepted_theorem']}))
