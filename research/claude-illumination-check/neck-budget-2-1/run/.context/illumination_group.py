"""Exact affine reflection group: finite point group and translation lattice index."""
from math import gcd
from itertools import combinations
from illumination_paths import room

def reflection(e):
    (x,y),(u,v)=e;dx=u-x;dy=v-y
    if dx==0:return (-1,0,0,1,2*x,0)
    if dy==0:return (1,0,0,-1,0,2*y)
    if dx==dy:return (0,1,1,0,x-y,y-x)
    assert dx==-dy;return (0,-1,-1,0,x+y,x+y)
def compose(a,b):
    aa,ab,ac,ad,ax,ay=a;ba,bb,bc,bd,bx,by=b
    return (aa*ba+ab*bc,aa*bb+ab*bd,ac*ba+ad*bc,ac*bb+ad*bd,aa*bx+ab*by+ax,ac*bx+ad*by+ay)
def describe(data):
    generators={reflection(e) for e in room(data)[0]};identity=(1,0,0,1,0,0);reps={identity[:4]:identity};todo=[identity]
    while todo:
        g=todo.pop()
        for r in generators:
            h=compose(r,g)
            if h[:4] not in reps:reps[h[:4]]=h;todo.append(h)
    translations=set()
    for g in reps.values():
        for r in generators:
            h=compose(r,g);rep=reps[h[:4]];d=(h[4]-rep[4],h[5]-rep[5])
            for a,b,c,e in reps:translations.add((a*d[0]+b*d[1],c*d[0]+e*d[1]))
    index=0
    for a,b in combinations(translations,2):index=gcd(index,abs(a[0]*b[1]-a[1]*b[0]))
    all_even=all(x%2==0 and y%2==0 for x,y in translations)
    full=len(reps)==8 and index==4 and all_even
    return dict(point_group_order=len(reps),translation_lattice_index=index,all_translations_even=all_even,full_even_translation_D4_group=full,schreier_translation_vectors=sorted(translations))
if __name__=='__main__':
    import sys,json
    print(json.dumps(describe(json.load(open(sys.argv[1]))),indent=2))
