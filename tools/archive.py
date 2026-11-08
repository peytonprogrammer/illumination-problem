#!/usr/bin/env python3
"""Verify/download the research archive and reconstruct its historical file layout.

No research checker or archived shell command is executed by this tool.
"""
from pathlib import Path, PurePosixPath
import argparse,functools,hashlib,json,shutil,subprocess,tarfile
ROOT=Path(__file__).resolve().parents[1]
def manifest_records():
 manifests=[ROOT/'manifests/files.jsonl']+sorted((ROOT/'manifests').glob('files-*.jsonl'))
 for manifest in manifests:
  with manifest.open() as f:
   for line in f:yield json.loads(line)
def records():
 # Follow-ups replace the current version/location; old manifests remain history.
 latest={r['source_path']:r for r in manifest_records()}
 return latest.values()
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def safe_path(base,name):
 p=PurePosixPath(name)
 if p.is_absolute() or '..' in p.parts:raise ValueError('Unsafe archive path')
 return base.joinpath(*p.parts)
def verify_git():
 n=0
 for r in records():
  if r['storage']!='git':continue
  p=safe_path(ROOT,r['path'])
  if p.stat().st_size!=r['bytes'] or digest(p)!=r['sha256']:raise ValueError('Hash mismatch: '+r['path'])
  n+=1
 print(f'Verified {n} Git research files.')
def discard(_sha,chunks):
 for _ in chunks:pass

def package_catalog():
 return {p['id']:p for p in json.loads((ROOT/'manifests/packages.json').read_text())['packages']}

def package_file(meta,cache,download=False):
 cache.mkdir(parents=True,exist_ok=True)
 path=safe_path(cache,meta['name'])
 if path.exists():
  if path.stat().st_size==meta['bytes'] and digest(path)==meta['sha256']:return path
  raise ValueError('Cached package failed verification; remove it before retrying: '+str(path))
 if not download:raise FileNotFoundError('Download this package first: '+meta['name'])
 temporary=path.with_name(path.name+'.download')
 if temporary.exists():raise ValueError('Incomplete download exists; inspect/remove it: '+str(temporary))
 subprocess.run(['gh','release','download',meta['release_tag'],'--repo',meta['repository'],
                 '--pattern',meta['name'],'--output',str(temporary)],check=True)
 if temporary.stat().st_size!=meta['bytes'] or digest(temporary)!=meta['sha256']:
  raise ValueError('Downloaded package hash mismatch: '+meta['name'])
 temporary.replace(path)
 return path

@functools.lru_cache(maxsize=1)
def package_members(root):
 grouped={}
 manifests=[root/'manifests/files.jsonl']+sorted((root/'manifests').glob('files-*.jsonl'))
 for manifest in manifests:
  with manifest.open() as f:
   for line in f:
    r=json.loads(line)
    if r['storage']=='package':grouped.setdefault(r['package'],{})[r['member']]=r
 return grouped

def read_package(meta,path,consumer):
 expected=package_members(ROOT).get(meta['id'],{})
 if len(expected)!=meta['files']:raise ValueError('Package manifest count mismatch')
 proc=subprocess.Popen(['zstd','-d','-q','-c',str(path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 seen=set()
 try:
  with tarfile.open(fileobj=proc.stdout,mode='r|') as tf:
   for member in tf:
    if not member.isfile() or member.name not in expected or member.name in seen:
     raise ValueError('Unexpected/duplicate package member: '+member.name)
    safe_path(Path('.'),member.name)
    record=expected[member.name]
    if member.size!=record['bytes']:raise ValueError('Package member size mismatch')
    reader=tf.extractfile(member);h=hashlib.sha256();size=0
    def chunks():
     nonlocal size
     for b in iter(lambda:reader.read(4*1024*1024),b''):
      h.update(b);size+=len(b);yield b
    consumer(record,chunks())
    if size!=record['bytes'] or h.hexdigest()!=record['sha256']:
     raise ValueError('Package member hash mismatch: '+member.name)
    seen.add(member.name)
  while proc.stdout.read(4*1024*1024):pass
  if proc.wait():raise RuntimeError('Package decompression failed: '+proc.stderr.read().decode())
  if seen!=set(expected):raise ValueError('Missing package members')
 except BaseException:
  proc.kill();proc.wait();raise
 finally:
  proc.stdout.close();proc.stderr.close()

def restore(destination,selected,cache):
 dest=destination.resolve()
 if dest.exists() and any(dest.iterdir()):raise ValueError('Restore workspace must be empty')
 if not selected:raise ValueError('No research files match the selection')
 if any(r['storage']=='dataset' for r in selected):raise ValueError('Selection has legacy-only data')
 # Resolve/download every needed package before writing the restored layout.
 catalog=package_catalog();ids=sorted({r['package'] for r in selected if r['storage']=='package'})
 paths={i:package_file(catalog[i],cache,download=True) for i in ids}
 wanted={r['source_path']:r for r in selected}
 for r in selected:
  if r['storage']=='git':
   source=safe_path(ROOT,r['path'])
   if source.stat().st_size!=r['bytes'] or digest(source)!=r['sha256']:raise ValueError('Git source hash mismatch')
   target=safe_path(dest/'.context',r['source_path']);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
 def put(r,chunks):
  current=wanted.get(r['source_path'])
  if not current or current['storage']!='package' or current['sha256']!=r['sha256']:
   return discard(None,chunks)
  target=safe_path(dest/'.context',r['source_path']);target.parent.mkdir(parents=True,exist_ok=True)
  temporary=target.with_name(target.name+'.partial')
  with temporary.open('xb') as f:
   for b in chunks:f.write(b)
 for i in ids:
  read_package(catalog[i],paths[i],put)
  # Install extracted files only after this entire package passed verification.
  for r in selected:
   if r.get('package')==i:
    target=safe_path(dest/'.context',r['source_path'])
    target.with_name(target.name+'.partial').replace(target)
 print(f'Restored {len(selected):,} files using {len(ids)} independent packages under {dest}/.context.')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['verify-git','list-data','download','verify-data','restore']);p.add_argument('--cache',type=Path,default=ROOT/'.data-cache');p.add_argument('--workspace',type=Path);p.add_argument('--prefix',default='');p.add_argument('--all',action='store_true',help='Explicitly select all current research');a=p.parse_args()
 if a.command=='verify-git':return verify_git()
 if a.command=='restore' and not a.workspace:p.error('restore requires --workspace')
 if not a.prefix and not a.all and a.command!='list-data':p.error('Choose --prefix RESEARCH/PATH or explicitly use --all; use list-data to browse')
 selected=[r for r in records() if r['source_path'].startswith(a.prefix)]
 if not selected:p.error('No research files match that prefix')
 if a.command=='restore':return restore(a.workspace,selected,a.cache)
 catalog=package_catalog();ids=sorted({r['package'] for r in selected if r['storage']=='package'})
 for i in ids:
  meta=catalog[i]
  if a.command=='list-data':print(f'{meta["bytes"]:>12,} bytes  {meta["files"]:>5} files  {meta["family"]}  {meta["name"]}')
  else:read_package(meta,package_file(meta,a.cache,download=a.command=='download'),discard)
 print(f'{len(selected):,} selected research files; {len(ids)} packages ({sum(catalog[i]["bytes"] for i in ids):,} compressed bytes).')
if __name__=='__main__':main()
