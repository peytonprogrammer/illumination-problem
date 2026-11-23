from pathlib import Path
from ast import literal_eval
import sys, subprocess
p=Path(__file__).resolve().parent
out=Path(sys.argv[1])
ls=[l for l in (p.parent/'offgrid/results/eighteen-audit.txt').read_text().splitlines() if l.startswith('cells ')]
subprocess.run([sys.executable,p.parent/'offgrid/build_pairskip.py',out/'base.c'],check=True)
s=(out/'base.c').read_text()
conditions=[]
with (out/'rooms').open('w') as f:
 for r,l in enumerate(ls,1):
  c,ps=l[6:].split(' open tile pairs '); print('18 18',c,file=f)
  conditions.extend(f'(rid=={r} && ca=={a} && cb=={b})' for a,b in literal_eval(ps))
needle='        const char *status = "DONE";'
s=s.replace(needle,'if (!('+'||'.join(conditions)+')) continue;\n'+needle)
needle='            if (big) status = "BIG";'
s=s.replace(needle,'''            for(int i=0;i<nl;i++) {
               Live *l=live+i; for(int j=0;j<l->Q->n;j++){
                 Poly *v[2]={&l->P,&l->Q->a[j].P};
                 printf("REG %lld %d %d %d",rid,ca,cb,l->cell);
                 for(int z=0;z<2;z++){printf(" |"); for(int k=0;k<v[z]->n;k++){Pt a=v[z]->v[k];printf(" %lld %lld %lld",a.x+sx*a.d,a.y+sy*a.d,a.d);}}
                 puts("");
               }
            }
'''+needle)
(out/'localize.c').write_text(s)
