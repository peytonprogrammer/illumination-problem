"""Prescribed exact checks for the B01 notch obstruction. No discovery."""
import ast
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
HERE = Path(__file__).resolve().parent
src = HERE.parent / 'review/resumed-exact-check.py'
names = {'vec','det','dot','edges','on','location','intersect','simple','path_check'}
module = ast.parse(src.read_text())
ns = {'Q': Q}
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[]), str(src), 'exec'), ns)
rows=[]
for n in (1,2,7,100):
    p=[(0,0),(16*n,0),(16*n,12*n),(8*n+2,12*n),(8*n,12*n-2),(8*n-2,12*n),(0,12*n)]
    s,t=(4*n,4*n),(12*n,4*n)
    ns['simple'](p)
    assert len(p)==7 and all(x%2==y%2==0 for x,y in p+[s,t])
    for a,b in ns['edges'](p):
        dx,dy=ns['vec'](a,b)
        assert dx==0 or dy==0 or abs(dx)==abs(dy)
        if dx and dy:
            assert (a[1]-(1 if dx*dy>0 else -1)*a[0])%2==0
    direct=ns['path_check'](p,[s,t])
    eps=Q(1,n)
    pn=[(Q(x,2*n),Q(y,2*n)) for x,y in p]
    q=(Q(4),Q(6)); hit=(4-eps/3,6-2*eps/3)
    assert ns['location'](pn,q)==-1
    assert ns['on'](pn[4],pn[5],hit)
    assert ns['det']((1,2),ns['vec']((2,2),hit))==0
    vin=(1,2); normal=(1,1)
    refl=tuple(vin[k]-2*Q(ns['dot'](vin,normal),ns['dot'](normal,normal))*normal[k] for k in (0,1))
    assert refl==(-2,-1)
    assert ns['det'](refl,ns['vec'](hit,(6,2)))!=0
    xleft=2+(6-eps)**2/(8-2*eps)
    assert xleft>4
    xright=8-xleft
    assert xright<4
    rows.append({'n':n,'walls':7,'direct_path':direct,'notch_hit':list(map(str,hit)),'left_candidate_x':str(xleft),'right_candidate_x':str(xright)})
limit=[(0,0),(8,0),(8,6),(0,6)]
roof=ns['path_check'](limit,[(2,2),(4,6),(6,2)])
result={'scope':'Exact prescribed controls; all-n claims require hand proof. All pairs in these controls ARE illuminated.','validator_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rows':rows,'limit_roof':roof,'status':'PASS'}
(HERE/'global-bridge-notched-limit-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
