"""Independent prescribed finite audits. No discovery, imports of peer code, or peer writes."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
PEER = HERE.parent / 'construction'

def vec(a,b): return (b[0]-a[0], b[1]-a[1])
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def edges(p): return list(zip(p,p[1:]+p[:1]))
def on(a,b,z):
    return det(vec(a,b),vec(a,z)) == 0 and all(min(a[k],b[k])<=z[k]<=max(a[k],b[k]) for k in (0,1))
def location(p,z):
    if any(on(a,b,z) for a,b in edges(p)): return 0
    crossings=0
    for a,b in edges(p):
        if min(a[1],b[1]) <= z[1] < max(a[1],b[1]):
            x=a[0]+Q(z[1]-a[1],b[1]-a[1])*(b[0]-a[0])
            crossings += x>z[0]
    return 1 if crossings%2 else -1
def intersect(a,b,c,d):
    u,v=vec(a,b),vec(c,d); den=det(u,v)
    if den:
        return 0<=Q(det(vec(a,c),v),den)<=1 and 0<=Q(det(vec(a,c),u),den)<=1
    return det(u,vec(a,c))==0 and (on(a,b,c) or on(a,b,d) or on(c,d,a) or on(c,d,b))
def simple(p):
    assert len(set(p))==len(p)
    for i,(a,b) in enumerate(edges(p)):
        assert a!=b
        # Adjacent edges must not backtrack, and genuine vertices must turn.
        assert det(vec(p[i-1],a),vec(a,b))!=0
        for j,(c,d) in enumerate(edges(p)):
            if j>i and j-i not in (1,len(p)-1): assert not intersect(a,b,c,d)

def path_check(p,path):
    p=[tuple(map(Q,z)) for z in p]
    path=[tuple(map(Q,z)) for z in path]
    assert len(path)>=2 and location(p,path[0])==location(p,path[-1])==1
    contacts=0; guards=0
    for a,b in zip(path,path[1:]):
        u=vec(a,b); assert u!=(0,0)
        assert location(p,((a[0]+b[0])/2,(a[1]+b[1])/2))==1
        for c,d in edges(p):
            v=vec(c,d); den=det(u,v)
            if den:
                t=Q(det(vec(a,c),v),den); r=Q(det(vec(a,c),u),den)
                assert not (0<t<1 and 0<=r<=1)
            elif det(u,vec(a,c))==0:
                axis=0 if u[0] else 1
                lo,hi=sorted((Q(c[axis]-a[axis],u[axis]),Q(d[axis]-a[axis],u[axis])))
                assert max(lo,0)>=min(hi,1)
            guards+=1
        assert not any(on(a,b,c) for c in p)
    for i,z in enumerate(path[1:-1],1):
        vin,vout=vec(path[i-1],z),vec(z,path[i+1])
        walls=[(a,b) for a,b in edges(p) if on(a,b,z)]
        if not walls:
            assert det(vin,vout)==0 and dot(vin,vout)>0
        else:
            assert len(walls)==1 and z not in p
            a,b=walls[0]; e=vec(a,b); n=(-e[1],e[0])
            refl=tuple(vin[k]-2*Q(dot(vin,n),dot(n,n))*n[k] for k in (0,1))
            assert det(refl,vout)==0 and dot(refl,vout)>0
            assert dot(vin,n)*dot(vout,n)<0
            contacts+=1
    return {'wall_leg_guards':guards,'reflections':contacts}

def nested_polygon(w,y):
    p=[(Q(0),Q(0)),(w[0],Q(0))]
    for j in range(len(w)):
        p.append((w[j],y[j+1]))
        if j+1<len(w):p.append((w[j+1],y[j+1]))
    p.append((Q(0),y[-1]));return p
def fold(q,w):
    r=q%(2*w); return min(r,2*w-r)
def nested_construct(w,y,S,T):
    w,y=list(map(Q,w)),list(map(Q,y));s,ys=map(Q,S);t,yt=map(Q,T)
    assert ys<yt
    assert all(w[l]*(y[l+1]-y[l])>=w[l+1]*y[l] for l in range(1,len(w)-1))
    i=max(l for l in range(len(w)) if y[l]<=ys)
    j=max(l for l in range(len(w)) if y[l]<=yt)
    assert i<j
    C={i:Q(0),i+1:2*w[i]}
    low=(C[i+1]-s-w[i+1])/(y[i+1]-ys); high=(C[i+1]-s+w[i+1])/(y[i+1]-ys)
    for l in range(i+1,j):
        center=(y[l+1]-y[l])*(C[l]-s)/(y[l]-ys)
        # Choose the lower nearest integer on a tie (different permitted rounding).
        z=center/(2*w[l]); k=-((-z-Q(1,2))//1)-1
        assert abs(center-2*k*w[l])<=w[l]
        C[l+1]=C[l]+2*k*w[l]
        nlow=(C[l+1]-s-w[l+1])/(y[l+1]-ys)
        nhigh=(C[l+1]-s+w[l+1])/(y[l+1]-ys)
        assert 0<low<nlow<nhigh<high
        low,high=nlow,nhigh
    zlow=s+(yt-ys)*low-C[j];zhigh=s+(yt-ys)*high-C[j]
    images=[sg*t+2*w[j]*((zlow-sg*t)//(2*w[j])+1) for sg in (1,-1)]
    image=min(images);assert zlow<image<zhigh
    tau=(image+C[j]-s)/(yt-ys);assert low<tau<high
    heights={ys,yt}
    for l in range(i,j+1):
        a,b=max(ys,y[l]),min(yt,y[l+1])
        if a==b:continue
        heights.update((a,b))
        qa,qb=(s+tau*(eta-ys)-C[l] for eta in (a,b))
        for n in range(int(qa//w[l])-1,int(qb//w[l])+2):
            eta=ys+(n*w[l]+C[l]-s)/tau
            if a<eta<b:heights.add(eta)
    path=[]
    for eta in sorted(heights):
        l=max(k for k in range(i,j+1) if y[k]<=eta)
        x=fold(s+tau*(eta-ys)-C[l],w[l])
        if eta in y[i+1:j+1]:
            assert x<w[l]
            assert x==fold(s+tau*(eta-ys)-C[l-1],w[l-1])
        path.append((x,eta))
    assert path[0]==(s,ys) and path[-1]==(t,yt)
    p=nested_polygon(w,y);simple(p)
    return {'widths':w,'heights':y,'source':S,'target':T,'slope':tau,**path_check(p,path)}

def main():
    # Reconstruct the source cycle from the frozen TeX equation, not the peer census.
    tex=HERE.parents[1]/'illumination-k4-codex/preprint-review-codex/revised.tex'
    text=tex.read_text().split(r'\label{eq:vertices}',1)[1].split(r'\end{equation}',1)[0]
    P=[tuple(map(int,m)) for m in re.findall(r'\((-?\d+),\s*(-?\d+)\)',text)]
    assert len(P)==22;simple(P)
    census=json.loads((PEER/'local-surgery-check.json').read_text())
    witnesses=json.loads((PEER/'local-surgery-optics.json').read_text())
    witnessmap={r['deleted_index']:r for r in witnesses['rows']}
    surgeries=[]
    for i in range(22):
        p=P[:i]+P[i+1:];simple(p)
        assert location(p,(0,0))==location(p,(2,2))==1
        a,b=P[i-1],P[(i+1)%22];dx,dy=vec(a,b)
        eligible=abs(dx)==abs(dy)
        assert census['rows'][i]['eligible']==eligible
        if not eligible:continue
        factor=1 if (a[0]+a[1])%2==0 else 2
        p=[(factor*x,factor*y) for x,y in p]
        assert len(p)==21
        k=0;J=0;sN=0
        for x in range(min(z[0] for z in p),max(z[0] for z in p)+1):
            for y in range(min(z[1] for z in p),max(z[1] for z in p)+1):
                if x%2==y%2==0:continue
                loc=location(p,(x,y))
                J+=loc==1;sN+=loc==0 and (x,y) not in p
        k=J+sN
        assert (factor,J,sN,k)==tuple(census['rows'][i][x] for x in ('canonical_representative_factor','J','s_N','k'))
        result={'index':i,'deleted':P[i],'factor':factor,'J':J,'s_N':sN,'k':k}
        if factor==2:
            row=witnessmap[i];assert p==list(map(tuple,row['polygon']))
            path=[tuple(map(Q,z)) for z in row['witness']['path']]
            assert path[0]==(0,0) and path[-1]==(4,4)
            result.update(path_check(p,path))
            assert result['reflections']==row['witness']['reflections']
        else:assert k==5
        surgeries.append(result)
    assert len(surgeries)==12 and len(witnessmap)==5
    nested=[nested_construct([30,14,6,2],[0,2,5,11,20],[29,Q(3,2)],[1,18]),
            nested_construct([30,14,6,2],[0,2,5,11,20],[13,2],[1,11]),
            nested_construct([12,8,4,2],[0,1,Q(3,2),Q(9,4),4],[11,Q(1,2)],[1,3]),
            nested_construct(list(range(18,0,-2)),[0,1,2,4,8,16,32,64,128,256],[15,1],[1,128])]
    p=nested_polygon(list(map(Q,[13,12,11,10])),list(map(Q,[0,10,11,12,13])))
    axes=[]
    for S,T in [((Q(49,4),Q(37,4)),(Q(37,4),Q(49,4))),((11,10),(9,12)),((2,2),(3,3))]:
        s,u=S;t,v=T;disc=s*v-t*u
        if not disc:path=[S,T]
        else:
            Xc=Q(abs(disc),u+v);Yc=Q(abs(disc),s+t)
            mids=[(0,Yc),(Xc,0)] if Q(s,s+t)<Q(u,u+v) else [(Xc,0),(0,Yc)]
            path=[S]+mids+[T]
        axes.append(path_check(p,path))
    four_signs=[]
    for sx in (-1,1):
        for sy in (-1,1):
            z=(abs(Q(38+sx*2,2)),abs(Q(2+sy*38,2)))
            assert location(nested_polygon([40,12,8,4],[0,12,16,20,40]),z)==-1
            four_signs.append(z)
    out={'status':'INDEPENDENT_PRESCRIBED_CHECKS_PASS','discovery':False,'surgery':surgeries,'nested':nested,'axis_paths':axes,'axis_obstruction_midpoints':four_signs,'whole_goal_complete':False}
    (HERE/'resumed-exact-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps({'status':out['status'],'surgery_shapes':len(surgeries),'surgery_reflections':sum(r.get('reflections',0) for r in surgeries),'nested_reflections':sum(r['reflections'] for r in nested),'axis_reflections':sum(r['reflections'] for r in axes)}))
if __name__=='__main__':main()
