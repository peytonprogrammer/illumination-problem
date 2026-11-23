"""Extend the previous verifier to larger rooms and split the large-phase case."""
from pathlib import Path
import subprocess,sys
base=Path(__file__).resolve().parent
out=Path(sys.argv[1])
s=(base.parent/'two18/shear.cpp').read_text().replace('lab[18][2]','lab[64][2]').replace('struct I {int l,h;};','struct I {long long l,h;};').replace('int fl(int x)','long long fl(long long x)').replace('int at(int k)','int at(long long k)').replace('int beg=fl(t.l),end=fl(t.h);','long long beg=fl(t.l),end=fl(t.h);').replace('int last=end','long long last=end').replace('for(int k=beg+','for(long long k=beg+').replace('int main_endpoint,rad,period;','int main_endpoint,rad,period; bool fixed_phase;')
s=s.replace('I t=I{base*den,base*den}+ (d.q*sx)*z[e*2]+(-d.p*sg*sy)*z[e*2+1]+(-d.q*j*sg*sy)*z[4+e];','''I t=I{base*den,base*den}+(d.q*sx)*z[e*2];
    if(fixed_phase) t=t+(-sg*sy*(d.p+d.q*j*period))*z[e*2+1];
    else t=t+(-d.p*sg*sy)*z[e*2+1]+(-d.q*j*sg*sy)*z[4+e];''')
s=s.replace('if(z[4+(1-main_endpoint)]','if(!fixed_phase && z[4+(1-main_endpoint)]')
a=s.index(' for(main_endpoint=0;');s=s[:a]+''' for(main_endpoint=0;main_endpoint<2;main_endpoint++)for(int mode=0;mode<2;mode++){
 fixed_phase=mode==1;Box z{};
 const int start=den/8, cap=(start+period-1)/period;
 if(fixed_phase && rad<cap)continue;
 const int rr=fixed_phase?rad:std::min(rad,cap);
 for(int i=0;i<4;i++)z[i]={0,rr};
 if(fixed_phase)z[2*main_endpoint+1].l=start/period;
 else {int top=std::max(2*start,period*rr);z[4+main_endpoint]={start,top};z[5-main_endpoint]={0,top};}
 printf("R %d %d %d %d %d\\n",marks[0].c,marks[1].c,main_endpoint,mode,rad);count_=miss=0;
 bool ok=rec(z,atoi(argv[4]));printf("END %d %d %d %d %d %lld\\n",marks[0].c,marks[1].c,main_endpoint,mode,ok,count_);fflush(stdout);}}
return 0;
}
'''
axis=s.replace('if(fixed_phase)z[2*main_endpoint+1]', 'z[0]=z[2]=I{0,rad};\n if(fixed_phase)z[2*main_endpoint+1]')
(out/'axis.cpp').write_text(axis)
subprocess.run(['c++','-std=c++17','-O3','-fsanitize=undefined','-fno-sanitize-recover=all',out/'axis.cpp','-o',out/'axis'],check=True)
(out/'shear.cpp').write_text(s)
subprocess.run(['c++','-std=c++17','-O3','-fsanitize=undefined','-fno-sanitize-recover=all',out/'shear.cpp','-o',out/'shear'],check=True)
subprocess.run([sys.executable,base.parent/'two18/export_labels.py',out/'labels.c'],check=True)
subprocess.run(['cc','-O2',out/'labels.c','-o',out/'labels'],check=True)
