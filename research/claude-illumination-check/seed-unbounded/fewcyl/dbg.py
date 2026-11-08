import sys
sys.argv=['fewcyl.py','../study.jsonl','11','11','6']
exec(open('fewcyl.py').read().replace("for k in range(int(ARGS[1]),int(ARGS[2])):","for k in []:"))
rm=rows[11]; V=[tuple(x) for x in rm['V']]; S=tuple(rm['S']); T=tuple(rm['T'])
r,u,lab,s0,fr=build2(V,S,S); r,u,lab=o.canon(r,u,lab,s0); r,u,lab=list(r),list(u),list(lab)
print('frame',fr)
for w in ws[:40]:
    Rr,Uu,v=state(r,u,w)
    for m in range(-3,4):
        wp=(m*w[0]+v[0],m*w[1]+v[1])
        if (abs(wp[0]),abs(wp[1])) in {(1,0),(0,1),(1,1)}: continue
        e1=Uu[pw_apply(Rr,Uu[pw_apply(Rr,0,m)],m)]; e2=Uu[pw_apply(Rr,Uu[pw_apply(Rr,0,m-1)],m+1)]
        ph=verify(V,S,T,wp); wk=walk(V,S,wp)
        if (T in (lab[e1],lab[e2]))!=(ph is not None): print(w,v,m,wp,lab[e1],lab[e2],ph,wk[:2] if wk else None)
