"""Prescribed multitwist increments of already-saved one-corner event classes.

No affine image paths or directions are traced. Only the 167 frozen words are
replayed to locate their intersections with the two fixed annulus systems.
"""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
import json, hashlib
if not __debug__: raise RuntimeError('Exact checks require no -O')
B=Path(__file__).resolve().parent
D=json.loads((B/'coupling.json').read_text()); W=D['walls']; dim=W+4
V=[tuple(map(F,p)) for p in D['room']['vertices']]
S,T=[tuple(map(F,p)) for p in D['room']['marked']]
normals=[tuple(map(F,n)) for n in D['offset_normals']]
dot=lambda x,y:sum(a*b for a,b in zip(x,y))
add=lambda x,y:tuple(a+b for a,b in zip(x,y))
sub=lambda x,y:tuple(a-b for a,b in zip(x,y))
mv=lambda A,x:tuple(dot(row,x) for row in A)
mt=lambda A:tuple(zip(*A))
mm=lambda A,C:tuple(tuple(dot(row,col) for col in zip(*C)) for row in A)
cross=lambda x,y:x[0]*y[1]-x[1]*y[0]
I=((F(1),F(0)),(F(0),F(1)))
h=[dot(n,p) for n,p in zip(normals,V)]
unit=lambda k:tuple(F(j==k) for j in range(dim))
zero=tuple(F(0) for j in range(dim))

# Preserve the frozen builder file; expose its existing local cell metadata only.
ns={'__name__':'frozen_builder','__file__':str(B/'inputs/twist_origami.py')}
source=(B/'inputs/twist_origami.py').read_text()
assert source.count('return r,u,lab,sstart')==1
exec(compile(source.replace('return r,u,lab,sstart','return r,u,lab,sstart,tris,sqs,sq'),str(B/'inputs/twist_origami.py'),'exec'),ns)
r,u,labels,s0,tris,sqs,sq=ns['build']([tuple(map(int,p)) for p in V],tuple(map(int,S)),tuple(map(int,T)))
n=len(r)

def cycles(p):
    unseen=set(range(n)); out=[]; membership={}
    while unseen:
        s=min(unseen); c=[]
        while s in unseen:
            membership[s]=len(out); unseen.remove(s);c.append(s);s=p[s]
        assert s==c[0]; out.append(c)
    return out,membership

hc,hi=cycles(r);vc,vi=cycles(u)

def vertex_forms(k):
    a,b=normals[k-1],normals[k]; det=cross(a,b); assert det
    return tuple((b[1]*unit((k-1)%W)[j]-a[1]*unit(k)[j])/det for j in range(dim)),tuple((-b[0]*unit((k-1)%W)[j]+a[0]*unit(k)[j])/det for j in range(dim))
cv=[vertex_forms(i) for i in range(W)]

def point_forms(p):
    if p in V: return cv[V.index(p)]
    if p==S: return unit(W),unit(W+1)
    if p==T: return unit(W+2),unit(W+3)
    for i,a in enumerate(V):
        b=V[(i+1)%W]; d=sub(b,a)
        if cross(sub(p,a),d)==0 and dot(sub(p,a),sub(p,b))<=0:
            j=0 if d[0] else 1; t=(p[j]-a[j])/d[j]
            return tuple(tuple((1-t)*x+t*y for x,y in zip(cv[i][k],cv[(i+1)%W][k])) for k in (0,1))
    # A material PL triangulation may fix all unmarked interior grid vertices.
    return zero,zero

pf={tuple(p):point_forms(tuple(p)) for tri in tris for p in tri}

def transform_forms(g,f):
    return tuple(tuple(sum(g[k][l]*f[l][j] for l in (0,1)) for j in range(dim)) for k in (0,1))

def edge_forms(s,axis):
    candidates=[]
    for ti,g in sqs[s]:
        tri=tris[ti]; pts=[mv(g,p) for p in tri]
        low=(min(p[0] for p in pts),min(p[1] for p in pts))
        for k,p in enumerate(pts):
            q=pts[(k+1)%3]
            if p[1-axis]==q[1-axis]==low[1-axis] and abs(q[axis]-p[axis])==1:
                a,b=tri[k],tri[(k+1)%3]
                if q[axis]<p[axis]:a,b=b,a
                f=tuple(sub(pf[b][z],pf[a][z]) for z in (0,1))
                candidates.append(transform_forms(g,f))
    assert candidates and all(x==candidates[0] for x in candidates)
    return candidates[0]

he=[edge_forms(s,0) for s in range(n)];ve=[edge_forms(s,1) for s in range(n)]
for s in range(n):
    for k in (0,1):
        assert add(he[s][k],ve[r[s]][k])==add(he[u[s]][k],ve[s][k]), ('face cochain not closed',s,k, sqs[s], sqs[r[s]], sqs[u[s]], sub(add(he[s][k],ve[r[s]][k]),add(he[u[s]][k],ve[s][k])))

def total_forms(c,edges):
    return tuple(tuple(sum(edges[s][k][j] for s in c) for j in range(dim)) for k in (0,1))
hforms=[total_forms(c,he) for c in hc];vforms=[total_forms(c,ve) for c in vc]
translation_x=tuple(n[0] for n in normals)+(F(1),F(0),F(1),F(0))
translation_y=tuple(n[1] for n in normals)+(F(0),F(1),F(0),F(1))
scale=tuple(h)+S+T
for axis,cs,forms in ((0,hc,hforms),(1,vc,vforms)):
    for c,f in zip(cs,forms):
        assert all(dot(row,t)==0 for row in f for t in (translation_x,translation_y))
        assert tuple(dot(row,scale) for row in f)==tuple(F(len(c) if k==axis else 0) for k in (0,1))
edge_incidence={}
for ti,tri in enumerate(tris):
    for k in range(3):edge_incidence.setdefault(frozenset((tri[k],tri[(k+1)%3])),[]).append(ti)
normal_bounces={}
for axis,cs in ((0,hc),(1,vc)):
    witnesses=[]
    for c in cs:
        hits=[]
        for s in c:
            for ti,g in sqs[s]:
                tri=tris[ti];pts=[mv(g,p) for p in tri];up=max(p[axis] for p in pts)
                for k,p in enumerate(pts):
                    q=pts[(k+1)%3];a,b=tri[k],tri[(k+1)%3]
                    if p[axis]==q[axis]==up and len(edge_incidence[frozenset((a,b))])==1:
                        assert a[0]==b[0] or a[1]==b[1]
                        hits.append({'square':s,'physical_edge':[list(a),list(b)],'copy':g})
        assert len(hits)==2,('normal bounce count',axis,c,hits)
        witnesses.append(hits)
    normal_bounces['horizontal' if axis==0 else 'vertical']=witnesses
ah=lcm(*map(len,hc));av=lcm(*map(len,vc))

def reflect(i):
    nn=normals[i];d=dot(nn,nn)
    return tuple(tuple(F(k==l)-2*nn[k]*nn[l]/d for l in (0,1)) for k in (0,1)),tuple(2*h[i]*x/d for x in nn)

# Exact location in the original triangular cellulation, at a fixed point of an
# already-saved segment. On cell edges both choices must give the same annulus.
def annulus(point,g,axis):
    opts=set(); membership=hi if axis==1 else vi
    for ti,tri in enumerate(tris):
        dets=[cross(sub(tri[(k+1)%3],tri[k]),sub(point,tri[k])) for k in range(3)]
        if min(dets)>=0 or max(dets)<=0:
            opts.add(membership[sq[(ti,g)]])
    assert len(opts)==1,(point,g,axis,opts)
    return opts.pop()

assert all(not any(f[1]) for f in hforms), 'horizontal cores can drift vertically'
assert all(not any(f[0]) for f in vforms), 'vertical cores can drift horizontally'
records=[]
slopes=[]
base_rows=[]
for e in D['events']:
    target=tuple(dot(tuple(map(F,row)),tuple(map(F,D['offset_base_point']))) for row in e['target_image_forms'])
    delta=sub(target,S);corner=tuple(dot(tuple(map(F,row)),tuple(map(F,D['offset_base_point']))) for row in e['corner_image_forms'])
    assert corner==add(S,tuple(x/2 for x in delta))
    O=I;shift=(F(0),F(0));start=F(0);cuts=[]
    for i in e['word']:
        nn=mv(O,normals[i]);den=dot(nn,delta);assert den
        t=(h[i]-dot(nn,sub(S,shift)))/den
        assert start<=t<=1
        cuts.append((start,t,O,shift)); start=t
        R,b=reflect(i);shift=add(shift,mv(O,b));O=mm(O,R)
    cuts.append((start,F(1),O,shift))
    assert add(mv(O,T),shift)==target
    incs=[]
    for axis,cs,forms,shear in ((1,hc,hforms,ah),(0,vc,vforms,av)):
        counts=[0]*len(cs)
        if delta[axis]:
            lo,up=sorted((S[axis],target[axis]));assert lo.denominator==up.denominator==1
            for level in range(int(lo),int(up)):
                tau=(F(level)+F(1,2)-S[axis])/delta[axis]
                assert 0<tau<1 and tau!=F(1,2)
                assignments=[]
                for a,b,g,sh in cuts:
                    if a<=tau<=b and a<b:
                        phys=mv(mt(g),sub(add(S,tuple(tau*x for x in delta)),sh))
                        assignments.append(annulus(phys,g,axis))
                assert assignments and len(set(assignments))==1
                first_or_second=1 if tau>F(1,2) else -1
                counts[assignments[0]]+=first_or_second*(1 if delta[axis]>0 else -1)
        assert sum(counts)==0 # zero holonomy of eta in the transverse direction
        coeff=[F(shear,len(c))*a for a,c in zip(counts,cs)]
        # Positive derivative shears x+=a*y or y+=b*x fix all grid vertices.
        assert sum(t*len(c) for t,c in zip(coeff,cs))==0
        response=tuple(tuple(sum(t*f[k][j] for t,f in zip(coeff,forms)) for j in range(dim)) for k in (0,1))
        incs.append({'annulus_crossing_difference':counts,'twist_coefficients':list(map(str,coeff)),
            'zero_on_room_deformations':not any(x for row in response for x in row),
            'period_derivative':[[str(x) for x in row] for row in response]})
    E=[tuple(F(a)-2*F(b)+F(j==W+k) for j,(a,b) in enumerate(zip(e['target_image_forms'][k],e['corner_image_forms'][k]))) for k in (0,1)]
    half=tuple(x/2 for x in delta); p,q=half; side=F(e['side'])
    primitive=tuple(map(F,e['direction'])); factor=next(x/y for x,y in zip(half,primitive) if y)
    assert factor>0 and half==tuple(factor*x for x in primitive)
    g0=tuple(-side*(p*E[1][j]-q*E[0][j]) for j in range(dim))
    assert g0==tuple(factor*F(x) for x in e['offset_gradient'])
    base_rows.extend((g0,g0))
    H=list(map(F,incs[0]['period_derivative'][0])); Z=list(map(F,incs[1]['period_derivative'][1]))
    hs=tuple(side*q*(x-ah*y) for x,y in zip(H,E[1]))
    vs=tuple(side*p*(av*x-y) for x,y in zip(E[0],Z))
    assert all(dot(row,t)==0 for row in (g0,hs,vs) for t in (translation_x,translation_y,scale))
    slopes.extend((hs,vs))
    records.append({'horizontal_row_slope':list(map(str,hs)),'vertical_row_slope':list(map(str,vs)),'index':e['index'],'direction':e['direction'],'horizontal':incs[0],'vertical':incs[1],
        'nonaxis':all(e['direction']), 'both_zero':all(x['zero_on_room_deformations'] for x in incs)})

def rank(rows):
    bs={}
    for row in rows:
        row=list(map(F,row))
        for k,v in sorted(bs.items()):
            if row[k]:
                a=row[k];row=[x-a*y for x,y in zip(row,v)]
        k=next((i for i,x in enumerate(row) if x),None)
        if k is not None:
            a=row[k];bs[k]=[x/a for x in row]
    return len(bs)
# Extract an independent slope basis, carrying exact representations.
basis={}; chosen=[]
for i,original in enumerate(slopes):
    row=list(original); combo={i:F(1)}
    for k,(v,c) in sorted(basis.items()):
        a=row[k]
        if a:
            row=[x-a*y for x,y in zip(row,v)]
            for j,t in c.items(): combo[j]=combo.get(j,F(0))-a*t
    k=next((j for j,x in enumerate(row) if x),None)
    if k is not None:
        a=row[k]; basis[k]=([x/a for x in row],{j:t/a for j,t in combo.items() if t});chosen.append(i)
assert len(chosen)==W+1
A=[]
for i in chosen:
    row=list(base_rows[i]);combo={}
    for k,(v,c) in sorted(basis.items()):
        a=row[k]
        if a:
            row=[x-a*y for x,y in zip(row,v)]
            for j,t in c.items():combo[j]=combo.get(j,F(0))+a*t
    assert not any(row)
    coeff=[combo.get(j,F(0)) for j in chosen]
    assert all(sum(t*slopes[j][k] for t,j in zip(coeff,chosen))==base_rows[i][k] for k in range(dim))
    A.append(coeff)
# A common finite power makes a strictly positive zero stress explicit.
colbound=max(sum(abs(row[j]) for row in A) for j in range(len(chosen)))
direction_bounds=[]
for i in chosen:
    p,q=map(F,D['events'][i//2]['direction'])
    denominator=ah*abs(q) if i%2==0 else av*abs(p)
    assert denominator>0
    direction_bounds.append((abs(p)+abs(q))/denominator)
bound=max([colbound]+direction_bounds)
power=bound.numerator//bound.denominator+1
def orbit_direction(i,sign):
    e=D['events'][i//2];direction=tuple(map(F,e['direction']))
    p,q=direction
    return (p+sign*power*ah*q,q) if i%2==0 else (p,q+sign*power*av*p)
def avoids_wall_parallel(w):return w[0]*w[1]!=0 and abs(w[0])!=abs(w[1])
assert all(avoids_wall_parallel(orbit_direction(i,t)) for i in chosen for t in (-1,1))
orbit_rows=[];weights=[];packets=[]
for k,i in enumerate(chosen):
    diff=-sum(row[k] for row in A)/power
    assert abs(diff)<1
    for sign in (1,-1):
        weight=(1+sign*diff)/2;assert weight>0
        row=tuple(x+sign*power*y for x,y in zip(base_rows[i],slopes[i]))
        orbit_rows.append(row);weights.append(weight)
        packets.append({'saved_index':i//2,'twist':'horizontal' if i%2==0 else 'vertical','power':sign*power,'weight':str(weight),'row':list(map(str,row))})
assert rank(orbit_rows)==W+1
assert all(sum(t*row[j] for t,row in zip(weights,orbit_rows))==0 for j in range(dim))
selected=[x['index'] for x in records if x['both_zero'] and x['nonaxis']]
rows=[e['offset_gradient'] for e in D['events'] if e['index'] in selected]
summary={'saved_events':len(records),'horizontal_evaluated_fixed':sum(x['horizontal']['zero_on_room_deformations'] for x in records),
    'vertical_evaluated_fixed':sum(x['vertical']['zero_on_room_deformations'] for x in records),'both_evaluated_fixed_nonaxis':len(selected),
    'selected_indices':selected,'selected_row_rank':rank(rows),'full_quotient_rank_required':W+1,'all_core_derivatives_aligned':True,'signed_orbit_slope_rank':rank(slopes),'horizontal_shear':ah,'vertical_shear':av,'orbit_packets':len(packets),'common_integer_power':power,'strict_positive_orbit_stress':True,'orbit_row_rank':rank(orbit_rows),'minimum_stress_weight':str(min(weights))}
assert len(records)==167 and [e['index'] for e in D['events']]==list(range(167))
assert rank([translation_x,translation_y,scale])==3
out={'status':'EXACT_FIXED_EVENT_ACTION_PASS','scope':'Only frozen words; prescribed horizontal/vertical annuli; no affine-image optical replay or discovery.',
    'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'summary':summary,'orbit_stress_certificate':packets,'base_in_slope_basis':[[str(x) for x in row] for row in A],'chosen_slope_indices':chosen,'normal_bounce_witnesses':normal_bounces,'core_period_derivatives':{'horizontal':[[list(map(str,row)) for row in f] for f in hforms],'vertical':[[list(map(str,row)) for row in f] for f in vforms]},'events':records,'input_sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (B/'coupling.json',B/'inputs/twist_origami.py')}}
(B/'twist-action.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,indent=2))
