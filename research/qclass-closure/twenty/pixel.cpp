#define main previous_main
#include "rays.cpp"
#undef main
#include <set>
vector<Dir> tables[2];int periods[2]; unsigned long long nodes=0,undecided=0;
int sgn(int t){return (t>0)-(t<0);}
vector<Dir> readtables(const char* fn){
 ifstream f(fn);string line;vector<Dir> res;
 while(getline(f,line)){istringstream s(line);int p,q,c,h,k;s>>p>>q>>c>>h;
 if(!c&&!h){Dir d{};d.p=p;d.q=q;res.push_back(d);}
 while(s>>k)res.back().lab[c][h/2].code.push_back(k);}
 sort(res.begin(),res.end(),[](const auto&a,const auto&b){return a.p+a.q<b.p+b.q;});return res;
}
bool literal(const B4& box,int lim){
 for(int j:{0,1,-1,2,-2,3,-3,4,-4,7,-7,12,-12,24,-24})for(int sw=0;sw<2;sw++)
 for(auto& d:tables[sw]){
 if(d.p+d.q>lim)break;
 Result both[2][2];for(int e=0;e<2;e++){
 int c=pairid[e];I x=box[2*e+sw],y=box[2*e+1-sw];
 for(int sh:{0,1}){
 int sg=sh?-1:1;
 // y is height relative to the physical lower edge; adding complete row periods is immaterial.
 I t=(d.q*x)+(-sg*(d.p+j*d.q*periods[sw]))*y+I{sh?-d.p*den:0,sh?-d.p*den:0};
 both[e][sh]=labels(d.lab[c][sh],t);
 }}
 for(auto a:both[0])for(auto b:both[1])if((a.op>=0&&(a.op==b.cl||a.op==b.extra))||(b.op>=0&&(b.op==a.cl||b.op==a.extra)))return true;
 }
 return false;
}
using Corner=array<int,4>;
set<Corner> calls;
int depthLimit;B4 firstFailure;
#include "axislocal.inc"
bool cover(const B4& z,int depth){
 nodes++;
 int k[2]={};bool near=true;
 for(int h=0;h<4;h++){
  if(z[h].h<=1024)continue;
  if(z[h].l>=den-1024)k[h/2]|=1<<(h%2);else near=false;
 }
 if(near){calls.insert({pairid[0],pairid[1],k[0],k[1]});return true;}
 // Check short explicit images first, then the cylinder lemma, then longer images.
 for(auto im:images)if(im.dist<=5 && shoots(z,im))return true;
 if(literal(z,9))return true;
 for(auto im:images)if(im.dist>5 && shoots(z,im))return true;
 if(literal(z,18))return true;
 if(getenv("LOCAL_PHASE") && (axislocal(z,0)||axislocal(z,1)))return true;
 if(getenv("RATIONAL_PHASE") && depth>=8 && (rational_axis(z,0)||rational_axis(z,1)))return true;
 if(depth==depthLimit){firstFailure=z;undecided++;return false;}
 int i=0;for(int j=1;j<4;j++)if(z[j].h-z[j].l>z[i].h-z[i].l)i=j;
 long long mid=(z[i].h+z[i].l)/2;if(mid==z[i].l){firstFailure=z;undecided++;return false;}
 B4 a=z,b=z;a[i].h=b[i].l=mid;return cover(a,depth+1)&&cover(b,depth+1);
}
int main(int argc,char**argv){
 if(argc!=7)return 2;
 ifstream f(argv[1]);int n,w,x,y;f>>n>>w;memset(ids,-1,sizeof ids);
 while(f>>x>>y){ids[x][y]=geom.size();geom.push_back({x,y});}
 for(int a=0;a<2;a++){tables[a]=readtables(argv[2+a]);periods[a]=atoi(argv[4+a]);}
 depthLimit=atoi(argv[6]);
 int i,j,u,v,ci=-1,cj=-1;long long checked=0;
 while(cin>>i>>j>>u>>v){
 if(i!=ci||j!=cj){marks[0].c=ci=i;marks[1].c=cj=j;prepare();}
 B4 z;for(int e=0;e<2;e++)for(int a=0;a<2;a++){int k=(e?v:u);k=a?k%16:k/16;z[2*e+a]=I{k*den/16,(k+1)*den/16};}
 if(!cover(z,0)){printf("OPEN %d %d %d %d",i,j,u,v);for(I a:firstFailure)printf(" %lld %lld",a.l,a.h);puts("");}
 checked++;
 }
 for(auto k:calls)printf("NEAR %d %d %d %d\n",k[0],k[1],k[2],k[3]);
 printf("TOTAL %lld %llu %llu\n",checked,nodes,undecided);
}
