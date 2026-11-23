"""Select and print the exact witnesses and bisections used in the difficult-room replay."""
from pathlib import Path
import sys,subprocess
b=Path(__file__).resolve().parent;o=Path(sys.argv[1])
s=(b/'pixel.cpp').read_text()
s=s.replace('#include "axislocal.inc"', 'bool printing_phase=false;\n'+(b/'axislocal.inc').read_text())
s=s.replace('if(u.l>t.h)return true;', 'if(u.l>t.h){if(printing_phase)puts("E");return true;}')
needle='||(c.op>=0&&(c.op==a.cl||c.op==a.extra)))return true;'
assert s.count(needle)==1
s=s.replace(needle,'||(c.op>=0&&(c.op==a.cl||c.op==a.extra))){if(printing_phase)printf("K %d %d %d\\n",j,d.p,d.q);return true;}')
s=s.replace('for(I v2:{I{v.l,m},I{m,v.h}})', 'if(printing_phase)printf("B %d\\n",int(a));\n for(I v2:{I{v.l,m},I{m,v.h}})')
a=s.index(' return true;\n}',s.index('if(!phasecert(b,sw,dom,sign,'))
s=s[:a]+''' if(!printing_phase){
    printf("P %d 0 %d 1 %d 1\\n",sw,sign[0]<0,sign[1]<0);
    printing_phase=true;bool ok=axislocal(b,sw);printing_phase=false;if(!ok)abort();
 }
'''+s[a:]
s=s.replace('if(proved)return true;', '''if(proved){
 if(!printing_phase){
   printf("P %d 1 %d %d %d %d\\n",sw,a.n,a.d,c.n,c.d);
   printing_phase=true;
   for(int s0:{1,-1})for(int s1:{1,-1}){
    array<int,2> sg{s0,s1};long long lo[2],hi[2];bool possible=true;
    for(int e=0;e<2;e++){auto h=bs2[e];long long v=sg[e]==1?h.lo:-h.hi,w=sg[e]==1?h.hi:-h.lo;
     if(w<0){possible=false;break;}lo[e]=max(0LL,v)*(M/h.d);hi[e]=w*(M/h.d);}
    if(!possible)continue;
    for(int dom:{0,1}){if(hi[dom]<lo[1-dom])continue;int top=max((long long)den/4,hi[dom]);
     if(!phasecert(b,sw,dom,sg,{den/8,top},{0,top},7))abort();}
   }
   printing_phase=false;
 }
 return true;
 }''')
s=s.replace('||b.op==a.extra)))return true;', '||b.op==a.extra))){printf("L %d %d %d %d\\n",sw,j,d.p,d.q);return true;}')
s=s.replace('calls.insert({pairid[0],pairid[1],k[0],k[1]});','printf("N %d %d\\n",k[0],k[1]);calls.insert({pairid[0],pairid[1],k[0],k[1]});')
s=s.replace('&& shoots(z,im))return true;', '&& shoots(z,im)){printf("V %d %d %d %d\\n",im.ex,im.ey,im.tx,im.ty);return true;}')
s=s.replace('B4 a=z,b=z;a[i].h=b[i].l=mid;', 'printf("S %d\\n",i); B4 a=z,b=z;a[i].h=b[i].l=mid;')
s=s.replace('if(!cover(z,0))','printf("I %d %d %d %d\\n",i,j,u,v);if(!cover(z,0))')
(o/'px-receipt.cpp').write_text(s)
subprocess.run(['c++','-O3','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all',o/'px-receipt.cpp','-o',o/'px-receipt'],check=True)
