from pathlib import Path
import sys,subprocess
base=Path(__file__).resolve().parent
out=Path(sys.argv[1])
s=(out/'shear.cpp').read_text()
n=s.index('long long count_')
s=s[:n]+(base/'visibility.inc').read_text()+'''
vector<Image> images;
void prepare(){
 for(int i=0;i<2;i++)pairid[i]=marks[i].c;
 images.clear();auto c=geom[pairid[0]],t=geom[pairid[1]];
 for(int a=-10;a<=10;a++)for(int b=-10;b<=10;b++)for(int ex:{1,-1})for(int ey:{1,-1}){
 int tx=ex*t.x+2*a-(ex<0),ty=ey*t.y+2*b-(ey<0);
 int dist=abs(tx-c.x)+abs(ty-c.y);if(dist<=16)images.push_back({ex,ey,2*a,2*b,dist});
 }
 stable_sort(images.begin(),images.end(),[](Image a,Image b){return a.dist<b.dist;});
}
bool shot_witness(const Box& z){
 B4 b;for(int i=0;i<2;i++){
 auto m=marks[i];b[2*i]=m.x==m.a?z[2*i]:I{den-z[2*i].h,den-z[2*i].l};
 b[2*i+1]=m.y==m.b?z[2*i+1]:I{den-z[2*i+1].h,den-z[2*i+1].l};
 }
 for(auto g:images)if(shoots(b,g)){printf("V %d %d %d %d\\n",g.ex,g.ey,g.tx,g.ty);return true;}
 return false;
}
'''+s[n:]
s='#include <climits>\n#include <cstring>\n'+s
s=s.replace(' if(witness(z))', ''' if(fixed_phase){
   for(int i=0;i<4;i++)if(z[i].l>z[2*main_endpoint+1].h){puts("G");return true;}
 }
 if(shot_witness(z)){count_++;return true;}
 if(witness(z))''')
s=s.replace('if(argc!=6)return 2;','''if(argc!=7)return 2;
 ifstream room(argv[6]);int n,w,a,b;room>>n>>w;memset(ids,-1,sizeof ids);while(room>>a>>b){ids[a][b]=geom.size();geom.push_back({a,b});}''')
s=s.replace(' for(main_endpoint=0;',' prepare();\n for(main_endpoint=0;')
s=s.replace('if(depth==0 || count_>budget){miss++;return false;}','''if(depth==0 || count_>budget){printf("FAIL");for(I s:z)printf(" %lld,%lld",s.l,s.h);puts("");miss++;return false;}''')
(out/'rays.cpp').write_text(s)
subprocess.run(['c++','-O3','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all',out/'rays.cpp','-o',out/'rays'],check=True)
