"""Prescribed exact genuine-roof-corner suffix. No discovery search."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib
HERE=Path(__file__).parent
# Only reviewer-owned pure geometry and earliest-original-wall code are reused.
helpers={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'roof_control_geometry'}
exec(compile((HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0],'<own-predicates>','exec'),helpers)
ns=helpers['ns'];fold=ns['fold'];source=HERE/'three-reflex-coprime-independent-check.py';txt=source.read_text();tree=ast.parse(txt);f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='replay_actual')
code=ast.get_source_segment(txt,f).replace('def replay_actual(P,S,T,slope,D):','def replay_actual(P,S,T,slope,D,velocity):').replace('velocity=(slope,Q(1))','velocity=velocity')
code=code.replace('assert len(roofs)==len(horizontal)==1','assert len(roofs)==len(horizontal)==0').replace("roof=roofs[0]","roof=None")
rns={'Q':Q,'ns':ns};exec(compile(code,'<existing-own-earliest-wall-no-horizontal-suffix>','exec'),rns)
e=12;P=1;N=7;L=4;a=12;A=84;R=12;B=48;b=2;c=3;h=4;H=12;S=(6,6);T=(38,2);tau=Q(41);s,u=S;t,v=T
C=2*H-h-u;D=2*H-u-v;f=H-u;roofphase=s+f*tau
assert roofphase==252==3*A and fold(roofphase,A)==A
# Formal full two-sided roof expression is algebra only; its corner is never traversed.
assert fold(2*roofphase-s,A)==s
X=s+C*tau;m=X//(2*A);z1=X-(2*m+1)*A;k=(z1+(h-c)*tau+R)//(2*R);z2=z1+(h-c)*tau-2*R*k;E=z2+(c-v)*tau
assert (z1,z2,E)==(-8,9,50) and abs(z1)<R and abs(z2)<R and fold(E,B)==A-t
remaining=D-2*f;assert remaining==u-v==4
polygon=[(a,b),(a,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
ray=rns['replay_actual'](polygon,S,T,tau,remaining,(-tau,-Q(1)))
assert ray['actual_target_time']==4
out=dict(status='PASS_PRESCRIBED_EXACT_UPPER_S_ROOF_CORNER_DESCENDING_SUFFIX',parameters=dict(e=e,P=P,N=N,L=L,b=b,c=c,h=h,H=H),S=S,T=T,tau=tau,formal_roof_corner=(A,H),formal_roof_time=f,formal_exact_S_return_time=2*f,formal_duration=D,retained_suffix_duration=remaining,retained_initial_velocity=(-tau,-Q(1)),residuals=(z1,z2),E=E,target_image='negative; conditional physical transfer test, not a positive-grid selector output',ray=ray,author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='ray'},default=str));print('reflections',ray['reflections'],'guards',ray['wall_leg_guards'])
