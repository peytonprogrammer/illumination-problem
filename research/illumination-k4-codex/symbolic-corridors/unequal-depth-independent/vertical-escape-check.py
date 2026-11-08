"""Independent prescribed vertical-denominator escape controls.
No direction discovery: a fixed published example is pulled back from an
accepted deterministic L-route through the two specified affine maps.
"""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
def load(name,path):
    sp=spec_from_file_location(name,path);m=module_from_spec(sp);sp.loader.exec_module(m);return m
M=load('own_tracer',HERE/'horizontal-parity-check.py');G=M.G
R=load('own_accepted_L',HERE/'midpoint-check.py')
def factors(n):
    r={};p=2
    while p*p<=n:
        while n%p==0:r[p]=r.get(p,0)+1;n//=p
        p+=1
    if n>1:r[n]=r.get(n,0)+1
    return r
def closed(D,q,s,t):return D%2==0 or q%2==0 or (D!=q and not ((D==3*q and s==F(2,3)) or (q==3*D and t==F(2,3))))
def main():
    rows=[];growth=0;fiber=0
    for hm,hp in ((F(2),F(2)),(F(3,2),F(5,2)),(F(2),F(3))):
        delta=M.rgcd([hm,F(1),hp]);Hm,Hp,Gg=hm/delta,hp/delta,1/delta
        assert all(x.denominator==1 for x in (Hm,Hp,Gg))
        lam=lcm(*(int(x) for x in (Hm,Hp,Gg,Hm+Hp+Gg)));C=2*lam;K=delta*C
        assert K.denominator==1 and int(K)%2==0
        for circ in (2*hm,2*hp,F(2),2*(hm+1+hp)):assert (K/circ).denominator==1
        for q in (1,3,5,7,9,15,21):
            a,b=delta/q,(1 if q==1 else 2)*delta/q
            assert 0<a<hm and 0<b<hp and (a/delta).denominator==(b/delta).denominator==q
            for s in (F(1,7),F(1,11),F(2,13),F(2,3)):
                for t in (F(1,5),F(1,3),F(2,3)):
                    n0=((K/hp)*t).denominator;shift=n0*K*t
                    assert (shift/hp).denominator==1
                    image={G.fold(b+sigma*tau*shift,hp) for sigma in (-1,1) for tau in (-1,1)}
                    assert len(image)==1;bp=image.pop();assert 0<bp<hp and (bp/delta).denominator==q;fiber+=4
                    z=a/delta-C*n0*s;ap=delta*G.fold(z,Hm);D=(ap/delta).denominator;E=F(C*n0*s).denominator
                    ep,qp=factors(E),factors(q);larger=[p for p,e in ep.items() if e>qp.get(p,0)]
                    criterion=bool(larger) and s!=F(2,3)
                    if larger:
                        assert D!=q and q%D!=0 and D>1 and 0<ap<hm
                        dp=factors(D)
                        for p in larger:assert dp[p]==ep[p]
                    if criterion:assert closed(D,q,s,t);growth+=1
                    rows.append({'hm':str(hm),'hp':str(hp),'delta':str(delta),'q':q,'s':str(s),'t':str(t),'K':str(K),'C':C,'n0':n0,'E':E,'D':D,'a_prime':str(ap),'b_prime':str(bp),'growth_primes':larger,'criterion':criterion})
    # Published q3->D21 illustration, with explicit original initial lift.
    s,t,a,b,hm,hp=map(F,['1/7','1/5','1/3','2/3','2','2']);K=F(20);L=F(12);ap=F(31,21);bp=b
    assert G.fold(a-K*s,hm)==ap and G.fold(b+K*t,hp)==bp
    assert ap.denominator==21 and bp.denominator==3
    # V sends the identity source lift back to its y-positive copy modulo4.
    Y=-a+K*s;assert Y+ap==4
    arg=s-L*ap;ss=M.fold(arg);tt=M.fold(t+L*(1+bp))
    assert ss==F(11,7) and tt==t and 2<arg%4<4
    # One common-column endpoint; construct accepted actual L-route after reversal.
    Q=R.Lroute(tt,ss,bp,ap,F(1),F(1),hp,hm)
    P=[(x,1-y) for x,y in reversed(Q)]
    image_contacts=G.verify(P,F(1),F(1),ap,bp,ss,tt,hm,hp)
    dx,dy=G.sub(P[1],P[0])
    # Image source x-sign -1,y-sign +1; inverse H then inverse V.
    wx=-dx-L*dy;wy=dy;velocity=(wx,wy-K*wx)
    actual=M.trace((s,t,a,b,hm,hp),velocity)
    physical={'example':['1/7','1/5','1/3','2/3','2','2'],'a_prime':str(ap),'b_prime':str(bp),'horizontal_L':str(L),'final_common_source':str(ss),'image_L_contacts':image_contacts,'original_velocity':list(map(str,velocity)),'original_contacts':actual['contacts'],'reverse_contacts':actual['reverse_contacts'],'scaled_contacts':actual['contacts'],'first_target_time':actual['time'],'path_sha256':hashlib.sha256(json.dumps(actual['path']).encode()).hexdigest(),'edge_word_sha256':hashlib.sha256(json.dumps(actual['edges']).encode()).hexdigest()}
    names=['unequal-depth/vertical-denominator-escape.md','unequal-depth-independent/twist-acceptance.json','unequal-depth-independent/one-fiber-acceptance.json','unequal-depth-independent/horizontal-parity-check.py','unequal-depth-independent/midpoint-check.py','unequal-depth-independent/vertical-escape-check.py']
    out={'status':'INDEPENDENT_VERTICAL_DENOMINATOR_ESCAPE_CONTROLS_PASS','prescribed_arithmetic_cases':len(rows),'whole_target_fiber_identities':fiber,'positive_growth_criterion_cases':growth,'original_physical_paths':3,'original_contacts_including_reverse_and_scaling':2*actual['contacts']+actual['reverse_contacts'],'image_L_contacts':image_contacts,'physical_example':physical,'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names},'arithmetic':rows,'limits':'Fixed arithmetic controls and one deterministic inverse-transport physical example. Universal valuation and fiber arguments separately hand-reviewed; shared odd torsion not solved.'}
    (HERE/'vertical-escape-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','arithmetic')}))
if __name__=='__main__':main()
