#include <algorithm>
#include <array>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <vector>
using namespace std;
constexpr int den=65536;
struct I {int l,h;};
I operator+(I a,I b){return {a.l+b.l,a.h+b.h};}
I operator*(int k,I a){return k>=0?I{k*a.l,k*a.h}:I{k*a.h,k*a.l};}
int fl(int x){return x>=0?x/den:-((-x+den-1)/den);}
struct Label {vector<int> code;int at(int k)const{int n=code.size();return code[(k%n+n)%n];}};
struct Dir{int p,q;Label lab[18][2];};
struct Result{int op=-1,cl=-1,extra=-1;};
Result labels(const Label& L,I t){
 int beg=fl(t.l),end=fl(t.h);
 // For a single integer point both adjacent cylinder closures are available.
 if(t.l==t.h && t.l%den==0){int a=L.at(beg),b=L.at(beg-1);return {(a&1)?a/2:-1,a/2,b/2};}
 int last=end-(t.h%den==0);
 int cl=L.at(beg)/2;bool op=true;
 for(int k=beg+(t.l%den!=0);k<=end;k++){
  if(!(L.at(k)&1))op=false;
  if(k<=last && L.at(k)/2!=cl)return {};
 }
 return {op?cl:-1,cl,-1};
}
struct End{int c,x,y,a,b;}; // center and lower-left cell
vector<Dir> dirs;
End marks[2];
using Box=array<I,6>; // positive x,y magnitudes for each endpoint, then two phases
int main_endpoint,rad,period;
int chosen_j,chosen_p,chosen_q;
bool witness(Box z){
 for(int j:{0,1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8,12,-12,16,-16,24,-24,32,-32})
 for(const auto& d:dirs){
  Result labs[2][2];
  for(int e=0;e<2;e++){auto E=marks[e];int sx=E.x==E.a?1:-1,sy=E.y==E.b?1:-1;
   for(int sh=0;sh<2;sh++){int sg=sh?-1:1;
    int base=d.q*(E.x-E.a)-d.p*(sh?1-(E.y-E.b):E.y-E.b);
    I t=I{base*den,base*den}+ (d.q*sx)*z[e*2]+(-d.p*sg*sy)*z[e*2+1]+(-d.q*j*sg*sy)*z[4+e];
    labs[e][sh]=labels(d.lab[E.c][sh],t);
   }}
  for(auto a:labs[0])for(auto b:labs[1])
   if((a.op>=0&&(a.op==b.cl||a.op==b.extra))||(b.op>=0&&(b.op==a.cl||b.op==a.extra))){chosen_j=j;chosen_p=d.p;chosen_q=d.q;return true;}
 }
 return false;
}
long long count_,miss;int budget;
bool rec(Box z,int depth){
 if(z[4+(1-main_endpoint)].l>z[4+main_endpoint].h){puts("E");return true;}
 if(witness(z)){printf("W %d %d %d\n",chosen_j,chosen_p,chosen_q);count_++;return true;}
 if(depth==0 || count_>budget){miss++;return false;}
 int dim=0;
 for(int i=1;i<6;i++)if((z[i].h-z[i].l)*(i>=4?4:1)>(z[dim].h-z[dim].l)*(dim>=4?4:1))dim=i;
 int mid=(z[dim].l+z[dim].h)/2;if(mid==z[dim].l){miss++;return false;}
 Box lo=z,hi=z;lo[dim].h=hi[dim].l=mid;
 printf("S %d\n",dim);
 return rec(lo,depth-1)&&rec(hi,depth-1);
}
int main(int argc,char**argv){
 if(argc!=6)return 2;
 ifstream f(argv[1]);string line;while(getline(f,line)){istringstream s(line);int p,q,c,h,k;s>>p>>q>>c>>h;
 if(c==0&&h==0){Dir d{};d.p=p;d.q=q;dirs.push_back(d);}
 while(s>>k)dirs.back().lab[c][h/2].code.push_back(k);}
 sort(dirs.begin(),dirs.end(),[](auto&a,auto&b){return a.p+a.q<b.p+b.q;});
 rad=atoi(argv[2]);period=atoi(argv[3]);budget=atoi(argv[5]);
 while(cin>>marks[0].c>>marks[0].x>>marks[0].y>>marks[0].a>>marks[0].b>>marks[1].c>>marks[1].x>>marks[1].y>>marks[1].a>>marks[1].b){
 for(main_endpoint=0;main_endpoint<2;main_endpoint++){Box z;for(int i=0;i<4;i++)z[i]={0,rad};
 int start=den/8;z[4+main_endpoint]={start,max(2*start,period*rad)};z[4+1-main_endpoint]={0,max(2*start,period*rad)};
 printf("R %d %d %d\n",marks[0].c,marks[1].c,main_endpoint);count_=miss=0;bool ok=rec(z,atoi(argv[4]));printf("%d %d %d %d %lld\n",marks[0].c,marks[1].c,main_endpoint,ok,count_);fflush(stdout);}}
}
