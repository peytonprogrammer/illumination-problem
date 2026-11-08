import json,glob
from fractions import Fraction as F
CERT='<SOURCE_WORKSPACE>/.context/claude-illumination-check/parity-enum/certs/'
def posspan2(vs):
    # vectors in R^2 positively span the plane iff no closed half-plane contains them all
    import math
    vs=[v for v in vs if v!=(0,0)]
    if len(vs)<3: return False
    ang=sorted(math.atan2(float(v[1]),float(v[0])) for v in vs)
    gaps=[(ang[(i+1)%len(ang)]-ang[i])%(2*math.pi) for i in range(len(ang))]
    return max(gaps)<math.pi-1e-12
same=0; tot=0; good=0; corners=0; rooms_all=0
for f in sorted(glob.glob('funcs-parity-*-R12.json')):
    tag=f[6:-9]; tot+=1
    same+= json.load(open(f))['funcs']==json.load(open(CERT+f))['funcs']
    rows=json.load(open(f'events-{tag}-R12.json'))['rows']
    s,t=json.load(open(CERT+tag+'.json'))['marked']
    allok=True
    for m in (s,t):
        for e in ((1,0),(-1,0),(0,1),(0,-1)):
            c=[m[0]+e[0],m[1]+e[1]]
            hs=[]
            for r in rows:
                if r['corner']!=c: continue
                L=r['L']; a=(F(r['a0'][0]),F(r['a0'][1]))
                sg=(r['side'] if r['side'] else r.get('sign',1))
                sg = 1 if sg>0 else -1
                # g contains a0 x (L dc) = a0[0]*(L dc)[1]-a0[1]*(L dc)[0]; as row vector in dc:
                h=(a[0]*L[1][0]-a[1]*L[0][0], a[0]*L[1][1]-a[1]*L[0][1])
                hs.append((sg*h[0],sg*h[1]))
            corners+=1; ok=posspan2(hs); good+=ok; allok&=ok
    rooms_all+=allok
print('funcs identical to stored certs',same,'of',tot)
print('axis ring corners whose corner-part vectors positively span R^2:',good,'of',corners,'; rooms with all 8:',rooms_all)
