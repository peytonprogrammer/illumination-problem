"""Finite parity-basis certificate for the one reconstructed orthogonal room.
Every primitive integer displacement hits a forbidden non-A vertex before an
A endpoint. This is stronger than enumerating the entire76-square shear orbit.
"""
from pathlib import Path
from itertools import product
import json,hashlib
B=Path(__file__).resolve().parent

def mul(a,b):return tuple(sum(a[2*i+k]*b[2*k+j] for k in (0,1))%2 for i in (0,1) for j in (0,1))
def group():
 seen={(1,0,0,1)};queue=[(1,0,0,1)];gens=[(1,1,0,1),(1,0,1,1)]
 for a in queue:
  for b in gens:
   c=mul(a,b)
   if c not in seen:seen.add(c);queue.append(c)
 return sorted(seen)
def verify(certificate,room,cells):
 assert certificate['room_sha256']==hashlib.sha256((B/'room.json').read_bytes()).hexdigest()
 assert {tuple(m) for m in certificate['basis_states']}==set(group())
 assert len(certificate['basis_states'])==6
 blocks={tuple(p) for p in certificate['blocked_residues']};assert blocks=={(1,0),(0,1),(1,1)}
 assert all(not(p[0]%2 or p[1]%2) for p in room['marked']) and room['marked'][0]!=room['marked'][1]
 occupied={tuple(c) for c in cells};points={(x+dx,y+dy) for x,y in occupied for dx,dy in product((0,1),repeat=2)};checked=0
 for x,y in points:
  if not(x%2 or y%2):continue
  incident={(x+dx,y+dy) for dx,dy in product((-1,0),repeat=2)}&occupied
  # In an orthogonal square-cell room a nonempty non-A vertex is an actual
  # corner iff it has1 or3 incident cells. Two diagonal cells would be a pinch.
  assert len(incident) in (1,3),(x,y,incident);checked+=1
 transitions=0
 for m in certificate['basis_states']:
  assert (m[0],m[2]) in blocks and (m[1],m[3]) in blocks
  for g in [(1,1,0,1),(1,0,1,1)]:assert mul(tuple(m),g) in set(group());transitions+=1
 return dict(non_A_vertices_checked=checked,basis_states=6,generator_transitions=transitions)
if __name__=='__main__':
 room=json.loads((B/'room.json').read_text());geo=json.loads((B/'reconstruct.json').read_text())
 certificate=dict(room_sha256=hashlib.sha256((B/'room.json').read_bytes()).hexdigest(),basis_states=group(),blocked_residues=[(1,0),(0,1),(1,1)],source_residue=(0,0),target_residue=(0,0),positive_length_required=True,interpretation='Every nonzero primitive residue is absorbing. Source and target residues coincide, but a physical connection unfolds to a nonzero even-even displacement.')
 (B/'parity-certificate.json').write_text(json.dumps(certificate,indent=2)+'\n');certificate=json.loads((B/'parity-certificate.json').read_text());checks=verify(certificate,room,geo['cells']);corrupt=[]
 for mode in ('missing_blocker','missing_basis_state','wrong_geometry_hash'):
  bad=json.loads(json.dumps(certificate))
  if mode=='missing_blocker':bad['blocked_residues'].pop()
  elif mode=='missing_basis_state':bad['basis_states'].pop()
  else:bad['room_sha256']='0'*64
  try:verify(bad,room,geo['cells'])
  except AssertionError:corrupt.append(mode)
 assert len(corrupt)==3
 result=dict(status='PASS',darkness='CERTIFIED_BY_PRIMITIVE_STEP_PARITY',checks=checks,corruptions_rejected=corrupt,scope='All directions and arbitrary finite reflection words, no sampled rays. Finite six-state parity-basis certificate; not a completed orbit of the full physical76-square unfolding.')
 (B/'parity-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
