"""Compare executable sections/layout and imported-symbol bindings on Mach-O.
Ignores UUID/code-signature/link-edit bookkeeping, not program code or data.
"""
from pathlib import Path
import struct,subprocess,json,hashlib
B=Path(__file__).resolve().parent

def sections(path):
 data=path.read_bytes();header=struct.unpack_from('<IiiIIIII',data,0);assert header[0]==0xfeedfacf
 out={};pos=32
 for i in range(header[4]):
  cmd,size=struct.unpack_from('<II',data,pos)
  if cmd==0x19:
   nsects=struct.unpack_from('<I',data,pos+64)[0]
   for j in range(nsects):
    sect,seg,addr,length,offset,align,reloff,nreloc,flags,r1,r2,r3=struct.unpack_from('<16s16sQQIIIIIIII',data,pos+72+80*j)
    name=lambda s:s.split(b'\0')[0].decode()
    key=name(seg)+'.'+name(sect);kind=flags&0xff
    payload=b'' if kind in (1,0xc,0x12) else data[offset:offset+length]
    out[key]=dict(address=addr,size=length,align=align,flags=flags,payload_sha256=hashlib.sha256(payload).hexdigest())
  pos+=size
 return out

def indirect(path):
 return subprocess.check_output(['otool','-Iv',str(path)],text=True).splitlines()[1:]

def compare(a,b):
 sa,sb=sections(a),sections(b);assert sa==sb,[(k,sa.get(k),sb.get(k)) for k in set(sa)|set(sb) if sa.get(k)!=sb.get(k)]
 assert indirect(a)==indirect(b)
 return dict(binary=a.name,reconstructed=b.name,sections=sa,all_executable_and_data_sections_equal=True,indirect_symbol_bindings_equal=True,binary_sha256=hashlib.sha256(a.read_bytes()).hexdigest(),reconstructed_sha256=hashlib.sha256(b.read_bytes()).hexdigest())

out=dict(status='PASS',pairs=[compare(B/'inputs/enum2',B/'rebuilt-pre-split'),compare(B/'inputs/enum3',B/'rebuilt')],scope='Executable section bytes/layout and indirect bindings match. Mach-O UUID/signature/linkedit metadata may differ. Does not independently authenticate historical command arguments or logs.')
(B/'binary-compare.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:(len(v) if k=='pairs' else v) for k,v in out.items()},indent=2))
