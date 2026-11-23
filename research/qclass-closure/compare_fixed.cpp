// Expand each isometry representative to all oriented shapes with bottom anchor.
#include <cstdio>
#include <vector>
#include <set>
#include <algorithm>
#include <cassert>
using namespace std;
int main(){
    long long bins[4][37]={};int n,w,x,y;
    while(scanf("%d %d",&n,&w)==2){
        vector<pair<int,int>> p;
        for(int i=0;i<n;i++){assert(scanf("%d%d",&x,&y)==2);p.push_back({x,y});}
        set<vector<pair<int,int>>> forms;
        for(int op=0;op<8;op++){
            vector<pair<int,int>> v;
            for(auto [a,b]:p){if(op&1)swap(a,b);if(op&2)a=-a;if(op&4)b=-b;v.push_back({b,a});}
            sort(v.begin(),v.end());auto [dy,dx]=v.front();
            for(auto &t:v){t.first-=dy;t.second-=dx;}
            if(!forms.insert(v).second)continue;
            int degree[80][80]={},mask=0;
            // Coordinates shifted by even offsets; first coordinate is y.
            for(auto [b,a]:v)for(int i=0;i<2;i++)for(int j=0;j<2;j++){
                degree[b+i][a+38+j]++;
            }
            for(auto [b,a]:v)for(int i=0;i<2;i++)for(int j=0;j<2;j++){
                int c=degree[b+i][a+38+j];if(c==2||c==4)mask|=1<<(((a+j+38)&1)+2*((b+i)&1));
            }
            for(int q=0;q<4;q++)if(!(mask&(1<<q)))bins[q][n]++;
        }
    }
    for(int q=0;q<4;q++){
        char path[64];snprintf(path,sizeof(path),"ind-%d.tsv",q);
        FILE *f=fopen(path,"r");assert(f);
        for(int k=1;k<=36;k++){int m;long long cnt;assert(fscanf(f,"%d%lld",&m,&cnt)==2);
            if(m!=k||cnt!=bins[q][k]){fprintf(stderr,"mismatch q=%d n=%d raw=%lld unique expansion=%lld\n",q,k,cnt,bins[q][k]);return 1;}}
        fclose(f);
    }
    puts("All 144 phase-by-area counts match the independent enumeration.");
}
