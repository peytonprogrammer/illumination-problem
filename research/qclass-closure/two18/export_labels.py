from pathlib import Path
import sys
base=Path(__file__).resolve().parent
src=next(base.parents[1].glob('illumination-generalization*/fable/directions*/d13-cylinder-cover/cover.c')).read_text()
s=src[:src.index('/* ------------------------------------------------------------ geometry */')]
Path(sys.argv[1]).write_text(s+'''
int main(int argc,char**argv){
int n,w;while(scanf("%d %d",&n,&w)==2){
ncell=n;memset(cellid,-1,sizeof(cellid));
for(int c=0;c<n;c++){scanf("%d%d",&CX[c],&CY[c]);cellid[CX[c]][CY[c]]=c;}
build_surface(); Dir D;
for(int p=1;p<=9;p++)for(int q=1;q<=9;q++){
int a=p,b=q;while(b){int t=a%b;a=b;b=t;}if(a!=1)continue;
compute_dir(&D,p,q);
for(int c=0;c<n;c++)for(int sh=0;sh<=2;sh+=2){
int t=sqi(c,sh),start=t;
printf("%d %d %d %d",p,q,c,sh);
do{for(int j=0;j<q;j++)printf(" %d",2*LAB(t*q+j)+regl_[cyc_[t*q+j]]);
t=Rr[t];}while(t!=start);puts("");
}
}
}}
''')
