/* Read packed records without generating rooms or tracing any directions. */
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
static int gcd(int a,int b){return b?gcd(b,a%b):a;}
int main(int argc,char **argv){
    int p[512],q[512],nd=0;
    for(int s=1;s<=40;s++) for(int x=s;x>=0;x--) if(gcd(x,s-x)==1){p[nd]=x;q[nd++]=s-x;}
    for(int f=1;f<argc;f++){
        FILE *in=fopen(argv[f],"rb"); assert(in); setvbuf(in,NULL,_IOFBF,1<<20);
        uint64_t counts[9][41]={0},rooms=0;
        int maxslow=0,maxslowratio=0,maxheightratio=0,maxm=0,maxrefl=0;
        unsigned char h[3];
        for(;;){
            size_t got=fread(h,1,3,in);if(!got)break;assert(got==3);
            int r=h[0],ny=h[1],np=h[2];assert(r<=8 && ny<=21 && np>=2 && np<=21);
            uint16_t rows[21]; assert(fread(rows,2,ny,in)==(size_t)ny);
            unsigned int mask=0;for(int i=0;i<ny;i++)mask|=rows[i];
            int nx=32-__builtin_clz(mask),span=nx>ny?nx:ny;
            uint32_t rec[210];int pairs=np*(np-1)/2;assert(fread(rec,4,pairs,in)==(size_t)pairs);
            for(int i=0;i<pairs;i++){
                unsigned int a=rec[i];int d=a&511, m=(a>>11)&127, b=a>>18;assert(d<nd && m>0);
                int hi=p[d]>q[d]?p[d]:q[d],lo=p[d]+q[d]-hi;
                int travel=m*lo;
                int xp=(p[d]+nx-1)/nx,yp=(q[d]+ny-1)/ny;
                int xt=(m*p[d]+nx-1)/nx,yt=(m*q[d]+ny-1)/ny;
                int ratio=xt<yt?xt:yt,hr=xp>yp?xp:yp;
                if(travel>maxslow)maxslow=travel;
                if(ratio>maxslowratio)maxslowratio=ratio;
                if(hr>maxheightratio)maxheightratio=hr;
                if(m>maxm)maxm=m;if(b>maxrefl)maxrefl=b;
                counts[r][hi]++;
            }
            rooms++;
        }
        assert(!ferror(in));fclose(in);
        printf("FILE %s %llu %d %d %d %d %d\n",argv[f],(unsigned long long)rooms,maxslow,maxslowratio,maxheightratio,maxm,maxrefl);
        for(int r=0;r<=8;r++)for(int h=1;h<=40;h++)if(counts[r][h])printf("BIN %d %d %llu\n",r,h,(unsigned long long)counts[r][h]);
    }
}
