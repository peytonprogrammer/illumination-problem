"""Run the finite darkness certificate, then bounded exact direction-code search."""
import argparse,json
from pathlib import Path
from illumination_cover import solve
from illumination_cover_certificate import certify


def decide(data,max_states=20000,seconds=60):
    certificate=certify(data,True)
    if certificate['status']=='DARK':return dict(status='DARK',proof=certificate,corner_convention='occupied-sector')
    exact=solve(data,max_states,seconds)
    return dict(status=exact['status'],certificate_screen={k:v for k,v in certificate.items() if k!='certificate'},exact=exact,corner_convention='occupied-sector')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('room');ap.add_argument('--max-states',type=int,default=20000);ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--out');args=ap.parse_args();r=decide(json.loads(Path(args.room).read_text()),args.max_states,args.seconds);r['room']=args.room
    if args.out:Path(args.out).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(dict(status=r['status'],room=args.room,corner_convention=r['corner_convention'],detail=r.get('exact',{}).get('reason',r.get('proof',{}).get('method')),direction=r.get('exact',{}).get('witness',{}).get('direction'))))
