"""Prescribed 74-family closed-square covers with independently derived guards."""
from fractions import Fraction as F
from pathlib import Path
from math import gcd,lcm
from importlib.util import spec_from_file_location,module_from_spec
import json,hashlib
HERE=Path(__file__).resolve().parent;PEER=HERE.parent/'unequal-depth'
def load(name,path):
    sp=spec_from_file_location(name,path);m=module_from_spec(sp);sp.loader.exec_module(m);return m
T=load('own_three_pass',HERE/'three-pass-check.py')
S=load('own_sign_arrangement',HERE/'short-line-margin-check.py')
SHEETS=((0,2),(1,2),(0,3),(1,3))
def gs_from(lo,hi,cs,ct,c0):return ((F(cs),F(ct),c0-lo),(-F(cs),-F(ct),hi-c0))
def main():
    geometry=json.loads((PEER/'critical-rectangles.json').read_text());parent=json.loads((PEER/'family-joint-margin.json').read_text())
    expected={i for i,row in enumerate(geometry['positive_dimensional_families']) if not any(row['affine_expressions'][x]==row['affine_expressions'][y] for x in (0,1) for y in (2,3))}
    assert len(expected)==74 and {r['family_index'] for r in parent['families']}==expected
    cache={};out=[];allcells=0;clausecount=0;sampling=0;maxq=0
    for row in parent['families']:
        i=row['family_index'];family=geometry['positive_dimensional_families'][i];expr=[tuple(map(F,e)) for e in family['affine_expressions']]
        assert row['affine_expressions']==family['affine_expressions'] and row['open_parameter_interval']==family['open_parameter_interval']
        eta=F(row['eta']);assert eta==F(1,8)
        if eta not in cache:cache[eta]=T.polygons(eta)
        guards=[];cuts=[]
        for clause in row['clauses']:
            mode=clause['mode'];sheet=clause['sheet'];m,n,r=clause['relation'];a,b=expr[SHEETS[sheet][0]],expr[SHEETS[sheet][1]]
            assert gcd(m,n,r)==1 and (a[0] or b[0])
            u,eps,k=clause['u'],clause['epsilon'],clause['k'];assert eps in (-1,1)
            if mode==1:
                assert m*a[0]+n*a[0]==r*(a[0]+b[0]) and m*a[1]+n*(a[1]+1)==r*(a[1]+b[1]+1)
                K=max(abs(m),abs(n));cs=m+n-r;candidate=[]
                for uu,c,l0,h0,l1,h1 in T.BOXES:
                    if u!=uu:continue
                    lo=min(m*l0,m*h0)+min(n*l1,n*h1)+eta*(abs(m)+abs(n))
                    hi=max(m*l0,m*h0)+max(n*l1,n*h1)-eta*(abs(m)+abs(n))
                    candidate.append(gs_from(lo,hi,cs,r*eps,F(r*u+4*k)))
            else:
                assert mode==3 and [m,n,r]==T.normal(a,b)
                K=max(abs(j*m-n) for j in range(4));cs=m-r;candidate=[]
                for p in cache[eta]:
                    if p['u']!=u:continue
                    values=[m*x+n*y for x,y in p['vertices']]
                    candidate.append(gs_from(min(values),max(values),cs,r*eps,F(r*u+4*k)))
            g=tuple(tuple(map(F,z)) for z in clause['guards']);assert g in candidate,(i,clause)
            assert K>0 and clause['cutoff']==2*K/eta
            guards.append(g);cuts.append(clause['cutoff']);clausecount+=1
        assert max(cuts)==row['uniform_q1_cutoff']<=64
        points,faces,lines=S.representatives(guards)
        for point in points:assert any(all(S.P.val(g,point)>0 for g in gs) for gs in guards),(i,point)
        allcells+=len(points)
        low,high=(F(z) if z is not None else None for z in family['open_parameter_interval'])
        lam=(low+high)/2 if low is not None and high is not None else low+1 if low is not None else high-1 if high is not None else F(0)
        depths=[x*lam+y for x,y in expr];assert depths[0]>0 and depths[2]>0 and depths[1]>depths[0] and depths[3]>depths[2]
        for j,(si,ti) in enumerate(SHEETS):
            A,B=depths[si],depths[ti];D=lcm(A.denominator,B.denominator);p=int(A*D);rr=int(B*D)
            assert gcd(p,rr,D)==1
            q1=p+rr+D;q3=p+rr+3*D
            assert q1==lcm((A/(A+B+1)).denominator,((A+1)/(A+B+1)).denominator)
            assert q3==lcm((A/(A+B+3)).denominator,(1/(A+B+3)).denominator)
            assert q1<q3<3*q1;maxq=max(maxq,q3)
            for mode,q,alpha,beta,rel in ((1,q1,A/(A+B+1),(A+1)/(A+B+1),family['relations'][j]),(3,q3,A/(A+B+3),1/(A+B+3),T.normal(expr[si],expr[ti]))):
                m,n,r=rel;assert m*alpha+n*beta==r
                aa,bb=int(q*alpha),int(q*beta);gg=gcd(abs(m),abs(n));assert gg and q%gg==0 and gcd(aa,bb,q)==1
                # Components are indexed by the normal level modulo gg.
                counts={}
                for z in range(q):
                    level=(m*(aa*z%q)+n*(bb*z%q))//q
                    assert (m*(aa*z%q)+n*(bb*z%q))%q==0
                    counts[level%gg]=counts.get(level%gg,0)+1
                assert len(counts)==gg and set(counts.values())=={q//gg};sampling+=1
        out.append({'family_index':i,'eta':str(eta),'cutoff':max(cuts),'clauses':len(guards),'closed_relative_cells':len(points),'faces':faces,'boundary_lines':lines})
    names=['family-joint-margin.md','family-joint-margin.py','family-joint-margin.json','critical-rectangles.json','three-pass-circle.md']
    result={'status':'PASS','families':len(out),'derived_clauses':clausecount,'closed_relative_cells':allcells,'rational_component_and_denominator_controls':sampling,'largest_control_q3':maxq,'max_uniform_cutoff':max(r['cutoff'] for r in out),'all_axes_edges_vertices_included':True,'source_sha256':{'unequal-depth/'+n:hashlib.sha256((PEER/n).read_bytes()).hexdigest() for n in names},'records':out,'limits':'Uniform real-parameter circle cover plus rigorous finite sampling bound; finite residual optical room closure excluded.'}
    (HERE/'family-joint-margin-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('records','source_sha256')}))
if __name__=='__main__':main()
