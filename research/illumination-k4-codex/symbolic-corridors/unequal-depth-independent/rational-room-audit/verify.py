"""Reproducible exact verifier for the saved fixed-room candidate certificate.
No discovery deadline is needed for later reruns; the original effort supervisor
still bounds the first run. Only own frozen helpers are imported.
"""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;REVIEW=HERE.parent

def load(name,path):
    sp=spec_from_file_location(name,path);m=module_from_spec(sp);sp.loader.exec_module(m);return m
C=load('own_polygon_clip',REVIEW/'phase-lines-check.py')
G=load('own_cap_formula',REVIEW/'cap-sheet-check.py')
DOMAIN=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
BOXES={(u,c):(I,J) for u,c,I,J in [(0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4))]}

def main():
    saved=json.loads((HERE/'result.json').read_text())
    assert hashlib.sha256((HERE/'audit.py').read_bytes()).hexdigest()==saved['source_sha256']
    assert saved['status']=='FIXED_ROOM_CAP_COVER_PROVED' and not saved['uncovered']
    a,b,hm,hp=map(F,['1/2','1','3/4','5/4']);clauses=[]
    for raw in saved['clauses']:
        lc,uc,u,c,eps,M=(raw[k] for k in ('lc','uc','u','c','eps','M'))
        A=2*hm-a if lc else a;B=2*hp-b if uc else b;H=A+1+B
        assert lc in (0,1) and uc in (0,1) and eps in (-1,1) and M>=0
        I,J=BOXES[(u,c)];gs=[tuple(map(F,g)) for g in raw['guards']]
        for ii,(rate,interval) in enumerate([(A/H,I),((A+1)/H,J)]):
            E=(1-rate,rate*eps,rate*(u+4*M));lo,hi=interval
            k=(E[2]-lo-gs[2*ii][2])/4
            assert k.denominator==1
            assert gs[2*ii]==(E[0],E[1],E[2]-lo-4*k)
            assert gs[2*ii+1]==(-E[0],-E[1],hi+4*k-E[2])
        # Reconstruct cap-corner lines independently over the ENTIRE square,
        # even those omitted from the discovery receipt as locally irrelevant.
        caps=[]
        if lc:caps.append(((A-hm)/H,0))
        if uc:caps.append(((A+1+hp)/H,u))
        bad=[]
        for rate,offset in caps:
            E=(1-rate,rate*eps,rate*(u+4*M)-offset)
            lo,hi=min(C.val(E,p) for p in DOMAIN),max(C.val(E,p) for p in DOMAIN)
            for j in range((lo/2).__floor__()-1,(hi/2).__floor__()+2):
                line=(E[0],E[1],E[2]-2*j)
                if min(C.val(line,p) for p in DOMAIN)<=0<=max(C.val(line,p) for p in DOMAIN):bad.append(line)
        Q=lcm(*(r.denominator for r in [A/H,(A+1)/H]+[r for r,offset in caps]))
        assert Q==raw['period'] and M<Q
        clauses.append((raw,gs,bad))
    lines=sorted({C.linekey(g) for raw,gs,bad in clauses for g in gs+bad if g[0] or g[1]})
    polygons=[DOMAIN]
    for L in lines:
        polygons=[Q for P in polygons for Q in (C.clip(P,L,1),C.clip(P,L,-1)) if Q]
    points=set()
    for P in polygons:
        points.add(tuple(sum(p[k] for p in P)/len(P) for k in (0,1)))
        for x,y in zip(P,P[1:]+P[:1]):
            points.add(x);points.add(tuple((a+b)/2 for a,b in zip(x,y)))
    tested=contacts=trimmed=0;records=[]
    for s,t in sorted(points):
        if not 0<s<=1 or not 0<t<=1:continue
        choices=[(raw,gs,bad) for raw,gs,bad in clauses if all(C.val(g,(s,t))>0 for g in gs) and all(C.val(g,(s,t))!=0 for g in bad)]
        assert choices,('uncovered continuous sign cell',s,t)
        raw,gs,bad=choices[0]
        P,n,early,Q=G.construct(s,t,a,b,hm,hp,raw['lc'],raw['uc'],raw['u'],raw['eps'],raw['M'],raw['c'])
        tested+=1;contacts+=n;trimmed+=early
        records.append({'s':str(s),'t':str(t),'clause':{k:raw[k] for k in ('lc','uc','u','c','eps','M')},'contacts':n,'early_target_trimmed':early})
    pins={str(p.relative_to(REVIEW.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [REVIEW/'phase-lines-check.py',REVIEW/'cap-sheet-check.py',HERE/'audit.py',HERE/'result.json',HERE/'verify.py']}
    out={'status':'FIXED_RATIONAL_ROOM_CONTINUOUS_COVER_AND_PHYSICS_VERIFIED','valid_clauses':len(clauses),'full_domain':'0<s<=1,0<t<=1','all_cap_bad_lines_reconstructed':True,'arrangement_lines':len(lines),'open_faces':len(polygons),'actual_paths_and_sign_cells':tested,'wall_contacts':contacts,'early_target_prefixes':trimmed,'source_sha256':pins,'records':records,'limits':'One fixed rational room. Exact sign-invariant faces/edges/vertices prove continuum coverage, with an actual physical path checked at every representative. No universal commensurable or darkness claim; peer review requested.'}
    (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','source_sha256')}))
if __name__=='__main__':main()
