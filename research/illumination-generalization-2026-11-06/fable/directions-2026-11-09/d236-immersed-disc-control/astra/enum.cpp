// Enumerate trees of maximal horizontal runs. A node is a closed integer interval of cells.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <ctime>
using namespace std;
struct Run { int x,y,w,parent; };
using Tree=vector<Run>;
struct Cell {int x,y; array<int,4> n{-1,-1,-1,-1};};
void join(vector<Cell>& c,int i,int d,int j){c[i].n[d]=j;c[j].n[d^2]=i;}
vector<Cell> cells(const Tree& t){
 vector<Cell> c; vector<int> start;
 for(auto r:t){
  int i=c.size();start.push_back(i);
  for(int u=0;u<r.w;u++){c.push_back({r.x+u,r.y});if(u)join(c,i+u-1,0,i+u);}
  if(r.parent<0)continue;
  auto p=t[r.parent];
  for(int x=max(r.x,p.x);x<min(r.x+r.w,p.x+p.w);x++)
   join(c,start[r.parent]+x-p.x,r.y>p.y?1:3,i+x-r.x);
 }
 return c;
}
// Canonical direction-labelled BFS from each lexicographically extremal projected cell.
string key(const vector<Cell>& c,bool rotate){
 string best;
 for(int d=0;d<4;d++)for(int sign:{1,-1}){
  if(!rotate && d%2)continue;
  pair<int,int> low{100,100};vector<int> roots;
  for(int i=0;i<(int)c.size();i++){
   int a[]={c[i].x,c[i].y,-c[i].x,-c[i].y};
   pair<int,int> p{a[d],a[(d+sign+4)%4]};
   if(p<low){low=p;roots.clear();}if(p==low)roots.push_back(i);
  }
  for(int root:roots){
   int order[17]={root},ids[17]={},size=1;ids[root]=1;string k;
   for(int j=0;j<size;j++)for(int s=0;s<4;s++){
    int nb=c[order[j]].n[(d+s*sign+8)%4];if(nb>=0 && !ids[nb]){order[size++]=nb;ids[nb]=size;}
    k.push_back(nb<0?0:ids[nb]);
   }
   if(best.empty()||k<best)best=k;
  }
 }
 return best;
}
int main(int argc,char** argv){
 int limit=stoi(argv[1]);if(limit<1||limit>16)return 2;
 vector<map<string,Tree>> levels(limit+1);
 for(int w=1;w<=limit;w++){Tree t{{0,0,w,-1}};levels[w][key(cells(t),false)]=t;}
 ofstream out("raw-counts.tsv"),jobs("jobs.txt");out<<"area\tW\tbucket\tdiscs\tpairs\n";
 for(int a=1;a<=limit;a++){
  set<string> counted;map<pair<int,string>,array<long long,2>> counts;
  for(auto &entry:levels[a]){
   const auto &t=entry.second; auto c=cells(t);
   if(counted.insert(key(c,true)).second){
    map<pair<int,int>,int> multiplicity;set<pair<int,int>> pos;
    int W=0,marks=0,vertices=0;
    for(auto p:c){pos.insert({p.x,p.y});for(int u:{0,1})for(int v:{0,1}){
      int h=p.n[u?0:2],z=p.n[v?1:3];
      if(h<0 && z<0){W++;vertices++;}
      if(h>=0 && z>=0){
       if(c[h].n[v?1:3]<0){W++;vertices++;}
       else if(!u&&!v){marks++;vertices++;}
      }
      if(h>=0 && z<0 && u && c[h].n[v?1:3]<0)vertices++;
      if(z>=0 && h<0 && v && c[z].n[u?0:2]<0)vertices++;
      multiplicity[{p.x+u,p.y+v}]++;
    }}
    string b=pos.size()<c.size()?"OVERLAP":vertices>(int)multiplicity.size()?"TOUCHING":"EMBEDDED";
    if(W<=20){auto &row=counts[{W,b}];row[0]++;row[1]+=marks*(marks-1)/2;
     if(b!="EMBEDDED"&&marks>=2){jobs<<a;for(auto p:c){jobs<<" "<<p.x<<" "<<p.y;for(int n:p.n)jobs<<" "<<n;}jobs<<"\n";}
    }
   }
   for(int i=0;i<(int)t.size();i++)for(int dir:{-1,1})for(int w=1;w<=limit-a;w++){
    auto p=t[i];
    for(int x=p.x-w+1;x<p.x+p.w;x++){
     int l=max(x,p.x),r=min(x+w,p.x+p.w); bool ok=true;
     for(int j=0;j<(int)t.size();j++)if((t[j].parent==i||p.parent==j)&&t[j].y==p.y+dir){
      if(max(l,max(t[j].x,p.x))<=min(r,min(t[j].x+t[j].w,p.x+p.w))){ok=false;break;}
     }
     if(ok){Tree next=t;next.push_back({x,p.y+dir,w,i});levels[a+w].try_emplace(key(cells(next),false),move(next));}
    }
   }
  }
  for(auto &[k,v]:counts)out<<a<<"\t"<<k.first<<"\t"<<k.second<<"\t"<<v[0]<<"\t"<<v[1]<<"\n";
  out.flush();cerr<<a<<" "<<counted.size()<<" cumulative CPU "<<double(clock())/CLOCKS_PER_SEC<<endl;levels[a].clear();
 }
}
