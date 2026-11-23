#include <stdio.h>
#include <stdint.h>
void start_shoot(void);
void shoot_room(int,int,int,int,const uint32_t*,int);
int main(void) {
    int a,w,width,height,marks;
    uint32_t rows[24];
    if(scanf("%d%d%d%d%d",&a,&w,&width,&height,&marks)!=5 || a!=15 || w!=22 || height>24) return 1;
    for(int i=0;i<height;i++) if(scanf("%u",&rows[i])!=1) return 1;
    start_shoot();
    shoot_room(a,w,width,height,rows,marks);
    return 0;
}
