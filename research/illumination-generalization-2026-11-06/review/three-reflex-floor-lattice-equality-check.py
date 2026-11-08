"""FE01 three prescribed two-column Euclidean constructions, no search."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,floor,ceil,lcm
import ast,json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-lower-joint-lattice-check.py').read_text()
env={'__file__':__file__}
# Only existing own geometry, Bezout, data and physical functions are loaded;
# none of the previous fixtures, author code or old module outputs is executed.
exec(compile(source.split('\ndef select')[0],'<own-floor-roof-geometry>','exec'),env)
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='select')
code=ast.get_source_segment(source,fn)
assert 'assert H0<K*Hx' in code
code=code.replace('assert H0<K*Hx','assert H0==K*Hx and P*d>2*Hx')
old='''wx=floor(-C0/(2*e*Hx)+Q(1,2));wy=floor(-(C1/(2*e)+wx*yw)/Fy+Q(1,2))
 triple=[wx*w+wy*ff for w,ff in zip(wcoeff,fibercoeff)];ni,mi,j=triple'''
new='''Hy=gcd(gcd(P*f,N*f),g*(r+n))
 assert Hy<Fy and gcd(yw,Fy)==Hy and yw%Fy!=0
 wx0=floor(-C0/(2*e*Hx)+Q(1,2))
 x0=(C0+2*e*Hx*wx0)/d
 direction=-1 if x0>0 else 1
 candidates=[]
 for wx in [wx0,wx0+direction]:
  wy=floor(-(C1/(2*e)+wx*yw)/Fy+Q(1,2))
  triple=[wx*w+wy*ff for w,ff in zip(wcoeff,fibercoeff)]
  x=(C0+2*e*sum(xx*c for xx,c in zip(xs,triple)))/d
  y=(C1+2*e*sum(yy*c for yy,c in zip(ys,triple)))/d
  assert abs(x)<P*e and abs(y)<=K*e
  candidates.append(dict(column=wx,source=x,cap=y,triple=triple,strict=abs(y)<K*e))
 assert any(row['strict'] for row in candidates)
 selected=next(row for row in candidates if row['strict'])
 ni,mi,j=selected['triple']'''
assert old in code;code=code.replace(old,new)
code=code.replace('if fixed is None:assert abs(z0)<=e*Hx/d<P*e and abs(z1)<=e*H0/Hx<K*e',
 'if fixed is None:assert abs(z0)<P*e and abs(z1)<K*e')
code=code.replace('Fy=Fy,vectors=vectors','Fy=Fy,Hy=Hy,columns=candidates,vectors=vectors')
exec(compile(code,'<own-FE01-two-column-construction>','exec'),env)
fixtures=[
 ('P1-r4-equality',(4,1,2,8,11,1,3,6,7),(2,4),(28,2)),
 ('P3-r3-equality',(2,3,2,8,13,1,3,6,7),(2,2),(14,2)),
 ('P5-r5-mouth-equality',(2,5,2,8,17,1,3,6,7),(2,6),(22,2))]
rows=[]
for label,params,S,T in fixtures:
 sel=env['select'](params,S,T)
 rows.append(dict(selection=sel,**env['physical'](label,params,S,T,sel['final_slope'])))
assert [row['selection']['Hx'] for row in rows]==[1,3,5]
assert [row['selection']['Fy'] for row in rows]==[14,12,16]
assert all(row['selection']['Hy']==2 for row in rows)
paths=[HERE/('three-reflex-floor-lattice-equality-'+s) for s in ['candidate.md','proof.md']]
out=dict(status='PASS_FE01_THREE_PRESCRIBED_TWO_COLUMN_PHYSICAL_EQUALITY_CASES',
 source_pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],
 rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),
 wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,
 discovery_search_used=False,independent_acceptance=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins']}))
print(json.dumps([{'label':row['label'],'slope':str(row['slope']),
 'columns':row['selection']['columns'],'floor_suffix':row['floor_corner_suffix_used']}
 for row in rows],default=str))
