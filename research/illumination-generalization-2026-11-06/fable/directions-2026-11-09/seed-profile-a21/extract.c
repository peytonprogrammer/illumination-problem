#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
int main(int argc,char **argv){
  FILE *in=fopen(argv[1],"rb"); assert(in);
  unsigned long goal=strtoul(argv[2],0,10);
  setvbuf(in,NULL,_IOFBF,1<<20);
  for(unsigned long i=1;i<=goal;i++){
    unsigned char h[3];assert(fread(h,1,3,in)==3);
    uint16_t rows[21];uint32_t records[210];
    assert(fread(rows,2,h[1],in)==h[1]);
    int pairs=h[2]*(h[2]-1)/2;
    assert(fread(records,4,pairs,in)==pairs);
    if(i==goal){
      for(int y=0;y<h[1];y++)printf("%d ",rows[y]);puts("");
      for(int k=0;k<pairs;k++)printf("%u ",records[k]);puts("");
    }
  }
  return 0;
}
