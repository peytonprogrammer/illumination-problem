"""Independently replay bin traversal, numerical ranges, path DAGs and parabolic witnesses."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from math import lcm
from collections import Counter
import gzip,sys
from verify_boxes import geometry
from rational import tracer
den=65536
def check(d,cert,grid,near):
    data=[geometry(d/str(a)) for a in range(2)]
    cells,_,_=data[0];C=set(cells);assert data[1][0]==[(y,x) for x,y in cells]
    count=Counter();seen=set();needed=set()
    def ray(z,image):
        ex,ey,tx,ty=image;assert ex in (-1,1) and ey in (-1,1) and tx%2==ty%2==0
        (a,b),(c,f)=(cells[i] for i in ids)
        ax,ay=ex*c+tx-(ex<0),ey*f+ty-(ey<0)
        def shift(p,k,sg=1):
            return sorted(k*den+sg*w for w in p)
        sx,sy,ux,uy=shift(z[0],a),shift(z[1],b),shift(z[2],ex*c+tx,ex),shift(z[3],ey*f+ty,ey)
        def overlap(x,y):return -(-max(x[0],y[0])//den)<=min(x[1],y[1])//den
        assert not (ay!=b and overlap(sx,ux) or ax!=a and overlap(sy,uy))
        dx=(ax>a)-(ax<a);dy=(ay>b)-(ay<b)
        # Each state records both chart orientation signs and physical cell, plus the developed cell.
        live={(a,b,a,b,1,1)}
        for turn in range(abs(ax-a)+abs(ay-b)):
            targets=set()
            for x,y,h,k,fx,fy in live:
                crossx=x!=ax;crossy=y!=ay
                if crossx and crossy:
                    X=(x+(dx>0))*den;Y=(y+(dy>0))*den
                    values=[dx*dy*((X-s)*(v-t)-(Y-t)*(u-s)) for s,t,u,v in product(sx,sy,ux,uy)]
                    crossx=min(values)<=0;crossy=max(values)>=0
                    if crossx and crossy:
                        vx=h+(dx*fx>0);vy=k+(dy*fy>0)
                        assert sum((vx-i,vy-j) in C for i,j in product((0,1),repeat=2)) in (2,4)
                if crossx:
                    hx=h+fx*dx
                    targets.add((x+dx,y,hx,k,fx,fy) if (hx,k) in C else (x+dx,y,h,k,-fx,fy))
                if crossy:
                    ky=k+fy*dy
                    targets.add((x,y+dy,h,ky,fx,fy) if (h,ky) in C else (x,y+dy,h,k,fx,-fy))
            live=targets
        assert live=={(ax,ay,c,f,ex,ey)}
        # Check the center trajectory with the separate point-to-point physical tracer.
        mid=[F(l+h,2*den) for l,h in z]
        S=(a+mid[0],b+mid[1]);T=(c+mid[2],f+mid[3])
        target=(ex*T[0]+tx,ey*T[1]+ty)
        if all(u!=v for u,v in zip(S,target)):
            scale,_,_,trace=tracer(C,S,T)
            assert trace(int(target[0]*scale),int(target[1]*scale))
            count['midpoint paths']+=1
    def cylinder(z,sw,j,p,q,phases=None,sgs=None):
        _,period,options=data[sw];pairs=[]
        for e in [0,1]:
            opened=set();closed=set()
            for sg in [1,-1]:
                off=-p*den if sg==-1 else 0
                terms=[(q,z[2*e+sw])]
                if phases is None:terms.append((-sg*(p+j*q*period),z[2*e+1-sw]))
                else:terms.extend([(-sg*p,z[2*e+1-sw]),(-sg*q*j*sgs[e],phases[e])])
                vr=[sorted([k*a,k*b]) for k,(a,b) in terms]
                lo,hi=(off+sum(w[r] for w in vr) for r in (0,1))
                a,b=options(p,q,ids[e],sg,lo//den,-(-hi//den),-(-lo//den),hi//den)
                opened|=a;closed|=b
            pairs.append((opened,closed))
        assert (pairs[0][0]&pairs[1][1]) or (pairs[1][0]&pairs[0][1])
    def visit(z):
        ls=next(tokens).split();tag=ls[0];v=list(map(int,ls[1:]));count[tag]+=1
        if tag=='S':
            i,=v;l,r=z[i];m=(l+r)//2;assert l<m<r
            for child in [(l,m),(m,r)]:visit(z[:i]+[child]+z[i+1:])
        elif tag=='L':cylinder(z,*v)
        elif tag=='V':ray(z,v)
        elif tag=='N':
            for e,k in enumerate(v):
                for a in (0,1):
                    l,r=z[2*e+a]
                    assert (l>=den-1024 if k&(1<<a) else r<=1024)
            needed.add((*ids,*v,1024))
        else:
            assert tag=='P';sw,variant,*refs=v
            refs=[F(refs[0],refs[1]),F(refs[2],refs[3])]
            assert variant in (0,1) and all(0<=h<=1 for h in refs)
            if not variant:assert all(h in (0,1) for h in refs)
            L=data[sw][1]*lcm(*(h.denominator for h in refs))
            delta=[[a-h*den for a in z[2*e+1-sw]] for e,h in enumerate(refs)]
            positive=any(l>0 or r<0 for l,r in delta)
            for e,h in enumerate(refs):
                if h in (0,1):
                    x,y=cells[ids[e]];w=1 if h else -1
                    positive|=(x+(w if sw else 0),y+(0 if sw else w)) not in C
            assert positive
            signs=product((1,-1),repeat=2) if variant else [tuple(1 if h==0 else -1 for h in refs)]
            for sg in signs:
                un=[sorted(sg[e]*n*L for n in delta[e]) for e in (0,1)]
                if any(h<0 for l,h in un):continue
                ranges=[(max(0,l),h) for l,h in un]
                for dom in (0,1):
                    if ranges[dom][1]<ranges[1-dom][0]:continue
                    top=max(den//4,ranges[dom][1]);assert int(top)==top
                    def phased(t,u):
                        row=next(tokens).split();kind=row[0];count[kind]+=1
                        if kind=='E':assert u[0]>t[1]
                        elif kind=='K':
                            phases=[None,None];phases[dom]=t;phases[1-dom]=u
                            cylinder(z,sw,*map(int,row[1:]),phases=phases,sgs=sg)
                        else:
                            assert kind=='B';split_t=int(row[1]);l,r=t if split_t else u;m=(l+r)//2;assert l<m<r
                            for w in ((l,m),(m,r)):phased(w if split_t else t,u if split_t else w)
                    phased((den//8,int(top)),(0,int(top)))
    for f in sorted(cert.glob('receipts?.gz')):
      with gzip.open(f,'rt') as tokens:
        for l in tokens:
            if l.startswith(('NEAR ','TOTAL ')):continue
            tag,i,j,u,v=l.split();assert tag=='I'
            key=tuple(map(int,(i,j,u,v)));assert key not in seen;seen.add(key)
            ids=key[:2];idx=[n for a in key[2:] for n in divmod(a,16)]
            visit([(k*den//16,(k+1)*den//16) for k in idx])
    expected={tuple(map(int,l.split()[1:])) for l in grid.open() if l.startswith('PIX ')}
    assert seen==expected
    assert needed=={tuple(map(int,l.split())) for l in (near/'boxes').read_text().splitlines()}
    print(len(seen),'reciprocal bin pairs;',len(needed),'corner neighborhoods;',dict(count))
if __name__=='__main__':check(*map(Path,sys.argv[1:]))
