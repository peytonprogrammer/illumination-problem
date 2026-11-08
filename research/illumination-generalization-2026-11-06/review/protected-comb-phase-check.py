"""Exact prescribed phase-repair certificates; no ray or direction search."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import json,importlib.util,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
effort=json.loads((R/'protected-comb-witness-effort.json').read_text());assert datetime.now(timezone.utc)<datetime.fromisoformat(effort['deadline_utc'])
def comb(c,H,teeth):
    p=[(0,0),(teeth[0][2],0)]
    for j,(lo,hi,right) in enumerate(teeth):
        assert lo<hi and right>c
        p.append((right,hi))
        if j+1<len(teeth):
            nxt=teeth[j+1];assert hi<nxt[0];p.extend([(c,hi),(c,nxt[0]),(nxt[2],nxt[0])])
    p.append((0,H));p=[tuple(map(Q,z)) for z in p];own.simple(p);return p

def phase(c,u,H,D,bs,bt,lo):
    c,u,H,D,bs,bt,lo=map(Q,(c,u,H,D,bs,bt,lo));delta=abs(bs-bt);period=2*u*c
    assert H>2*u and 0<bs<u and 0<bt<u and D>=c*(u+delta)/(u-delta)
    zp=c*min(bs,bt)+D*(H-delta)/2;zm=-c*max(bs,bt)+D*(H-delta)/2
    assert zp>0 and zm>0 and 0<zp-zm<period
    sigma=1 if zp%period else -1;z=zp if sigma==1 else zm
    assert z%period>0;k=int(z//period);tau=(H-sigma*(bs+bt)+4*u*k)/(2*(c+D))
    rs=sigma*bs+D*tau-2*u*k;rt=sigma*bt+D*tau-2*u*k
    assert 0<rs<u and 0<rt<u and rs+rt+2*c*tau==H and tau>0
    indices=range(1 if sigma==1 else 0,2*k+1)
    def leg(b):return [(c+D,b)]+[(c+D-(j*u-sigma*b)/tau,u if j%2 else Q(0)) for j in indices]
    low=leg(bs);back=leg(bt);M=(Q(0),rs+c*tau)
    path=[(x,y+lo) for x,y in low+[M]+[(x,H-y) for x,y in reversed(back)]]
    assert all(x>c for x,y in low[1:]+back[1:])
    return path,{'sigma':sigma,'k':k,'tau':tau,'source_portal_offset':rs,'target_portal_offset':rt,'expected_reflections':4*k+1+(2 if sigma==-1 else 0)}
rows=[]
controls=[
 (4,4,44,4,2,2,10,64,[(0,4,20),(10,14,20),(50,54,20),(60,64,20)]),
 (4,4,12,12,1,3,10,32,[(0,4,20),(10,14,20),(18,22,21),(28,32,16)]),
 (4,4,36,4,2,2,10,64,[(0,4,20),(10,14,20),(42,46,20),(60,64,20)]),
 (4,4,9,4,Q(7,2),Q(7,2),10,30,[(0,4,20),(10,14,20),(15,19,20),(26,30,20)]),
 (Q(3,2),Q(5,2),19,9,Q(1,2),2,3,28,[(0,1,15),(3,Q(11,2),17),(Q(39,2),22,18),(25,28,16)])]
for c,u,H,D,bs,bt,lo,Hg,teeth in controls:
    p=comb(Q(c),Q(Hg),teeth);path,meta=phase(c,u,H,D,bs,bt,lo)
    result=own.path_check(p,path);assert result['reflections']==meta['expected_reflections']
    assert all(not own.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
    rows.append({**meta,**result,'path':path,'actual_wall_count':len(p)})
assert rows[0]['sigma']==-1 and rows[0]['reflections']==11
assert rows[3]['sigma']==-1 and rows[3]['k']==0 and rows[3]['reflections']==3
out={'status':'ALL_FIVE_PRESCRIBED_PHASE_REPAIR_PATHS_PASS','rows':rows,'total_reflections':sum(x['reflections'] for x in rows),'total_wall_leg_guards':sum(x['wall_leg_guards'] for x in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()},'scope':'Strict actual internal-tooth portal repair under equal-height/equal-depth sufficient-width hypotheses; no arbitrary comb claim.'}
(R/'protected-comb-phase-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_sha256')}))
