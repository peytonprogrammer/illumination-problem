"""Independent finite support enumeration using positive depth numerator triples."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
from collections import defaultdict
import hashlib,json
HERE=Path(__file__).resolve().parent;PEER=HERE.parent/'unequal-depth'
SHEETS=((0,2),(1,2),(0,3),(1,3))
POINTS={tuple(map(F,r)) for r in [('1/2','1/2'),('1/5','3/5'),('3/5','1/5'),('3','5'),('5','3'),('1/3','7/3'),('7/3','1/3'),('1/7','3/7'),('3/7','1/7'),('5','8'),('8','5')]}
def main():
    geometry=json.loads((PEER/'critical-rectangles.json').read_text());margin=json.loads((PEER/'family-joint-margin.json').read_text());parent=json.loads((PEER/'residual-rooms.json').read_text())
    lines=[tuple(map(F,x)) for x in geometry['critical_lines']];maxQ=max(r['uniform_q1_cutoff'] for r in margin['families'])
    relations={tuple(r) for fam in geometry['positive_dimensional_families'] for r in fam['relations']}
    phases=defaultdict(list);triples=0
    # Minimal depth numerators U=p/D,V=r/D, with one-pass period p+r+D.
    for D in range(1,maxQ-1):
        for p in range(1,maxQ-D):
            for rr in range(1,maxQ-D-p+1):
                if gcd(p,rr,D)!=1:continue
                q=p+rr+D;triples+=1
                for m,n,r in relations:
                    if (m+n-r)*p-r*rr+(n-r)*D==0:phases[m,n,r].append((F(p,D),F(rr,D),q))
    rooms=set();family_rooms=set();point_rooms=set();provenance_checks=0
    def add(v,target=None):
        a,A,b,B=v;assert a>0 and b>0 and A>a and B>b
        if any(x==y for x in (a,A) for y in (b,B)):return
        rooms.add(tuple(v))
        if target is not None:target.add(tuple(v))
    for row in margin['families']:
        fam=geometry['positive_dimensional_families'][row['family_index']];expr=[tuple(map(F,e)) for e in fam['affine_expressions']]
        low,high=(F(x) if x is not None else None for x in fam['open_parameter_interval'])
        for j,(si,ti) in enumerate(SHEETS):
            ca,ka=expr[si];cb,kb=expr[ti];assert ca or cb
            for U,V,q in phases[tuple(fam['relations'][j])]:
                if q>row['uniform_q1_cutoff']:continue
                # Orthogonal projection onto the affine one-dimensional pair,
                # then enforce zero residual exactly (no coordinate-specific inversion).
                lam=(ca*(U-ka)+cb*(V-kb))/(ca*ca+cb*cb)
                if ca*lam+ka!=U or cb*lam+kb!=V:continue
                if low is not None and lam<=low or high is not None and lam>=high:continue
                add(tuple(c*lam+k for c,k in expr),family_rooms)
    assert len(rooms)==len(family_rooms)==22328
    for row in geometry['isolated_points']:add(tuple(F(e[0]) for e in row['affine_expressions']))
    assert len(rooms)==22372
    def supported(x,y):return (x,y) in POINTS or any(p*x+q*y==r for p,q,r in lines)
    for x,y in POINTS:
        assert x!=1 and y!=1
        other_x={u for u,v in POINTS if v==y};other_y={v for u,v in POINTS if u==x}
        for p,q,r in lines:
            if p:other_x.add((r-q*y)/p)
            else:assert q*y!=r  # No complete horizontal slice through an exceptional point.
            if q:other_y.add((r-p*x)/q)
            else:assert p*x!=r  # No complete vertical slice through an exceptional point.
        for u in other_x:
            for v in other_y:
                if min(u,v)<=0 or u==x or v==y or not supported(u,v):continue
                add((*sorted((x,u)),*sorted((y,v))),point_rooms)
    actual={tuple(map(F,r['rectangle'])) for r in parent['rooms']}
    assert actual==rooms and len(rooms)==len(parent['rooms'])==22538
    max1=max3=0;ordered=sorted(rooms)
    for index,row in enumerate(parent['rooms']):
        a,A,b,B=map(F,row['rectangle']);assert row['id']==index
        assert row['rectangle']==list(map(str,ordered[index]))
        assert (F(row['a']),F(row['b']),F(row['hm']),F(row['hp']))==(a,b,(a+A)/2,(b+B)/2)
        assert a<F(row['hm']) and b<F(row['hp'])
        periods1=[];periods3=[]
        for U,V in ((a,b),(A,b),(a,B),(A,B)):
            assert supported(U,V)
            D=lcm(U.denominator,V.denominator);p=int(U*D);r=int(V*D);assert gcd(p,r,D)==1
            periods1.append(p+r+D);periods3.append(p+r+3*D)
        assert periods1==row['q1'] and periods3==row['q3'];max1=max(max1,*periods1);max3=max(max3,*periods3)
        origin=row['origin']
        if origin['kind']=='family_small_phase':
            fam=geometry['positive_dimensional_families'][origin['family']];lam=F(origin['parameter'])
            assert tuple(F(c)*lam+F(k) for c,k in fam['affine_expressions'])==(a,A,b,B)
            p,c,q=origin['phase'];assert gcd(p,c,q)==1 and 0<p<c<q<=origin['Q']
            si,ti=SHEETS[origin['sheet']];vv=(a,A,b,B);assert (F(p,c-p),F(q-c,c-p))==(vv[si],vv[ti])
        elif origin['kind']=='critical_isolated':assert tuple(F(e[0]) for e in geometry['isolated_points'][origin['index']]['affine_expressions'])==(a,A,b,B)
        else:
            assert origin['kind']=='exceptional_point_rectangle';x,y=map(F,origin['point']);u,v=map(F,origin['opposite']);assert (x,y) in POINTS
            assert (*sorted((x,u)),*sorted((y,v)))==(a,A,b,B)
        provenance_checks+=1
    assert (max1,max3)==(750,752)==(parent['max_q1'],parent['max_q3'])
    assert {tuple(map(F,r['rectangle'])) for r in parent['rooms']}==set(sorted(rooms))
    for name,h in parent['dependency_sha256'].items():assert hashlib.sha256((PEER/name).read_bytes()).hexdigest()==h
    names=['residual-rooms.md','residual-rooms.py','residual-rooms.json','critical-rectangles.json','family-joint-margin.json','exceptional-phase-support.json','short-line-finite.json']
    out={'status':'PASS','primitive_positive_depth_triples_enumerated':triples,'bounded_family_rooms':len(family_rooms),'after_isolated':22372,'all_residual_rooms':len(rooms),'exceptional_point_support_rectangles_after_equalities':len(point_rooms),'actual_height_period_and_provenance_checks':provenance_checks,'max_q1':max1,'max_q3':max3,'source_sha256':{'unequal-depth/'+n:hashlib.sha256((PEER/n).read_bytes()).hexdigest() for n in names},'limits':'Complete residual support only; continuous optical coverage and final whole-result join separate.'}
    (HERE/'residual-rooms-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
