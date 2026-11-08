"""Reconstruct one published thumbnail as an idealized unit-square room."""
from pathlib import Path
from collections import Counter
import json,hashlib,re
from PIL import Image
B=Path(__file__).resolve().parent
# Screen-grid coordinates, manually transcribed from author's thumbnail.
outline=[(2,0),(3,0),(3,2),(4,2),(4,1),(5,1),(5,2),(6,2),(6,3),(4,3),(4,4),(5,4),(5,5),(4,5),(4,6),(3,6),(3,4),(2,4),(2,5),(1,5),(1,4),(0,4),(0,3),(2,3),(2,2),(1,2),(1,1),(2,1)]
def inside(x,y):
 return sum((a[1]>y)!=(b[1]>y) and x<a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]) for a,b in zip(outline,outline[1:]+outline[:1]) if a[1]!=b[1])%2==1
screen_cells={(x,y) for x in range(6) for y in range(6) if inside(x+.5,y+.5)}
im=Image.open(B/'inputs/video-thumbnail.jpg').convert('RGB'); probes=[]
for x in range(6):
 for y in range(6):
  px,py=round(367+91*(x+.5)),round(88+91*(y+.5));r,g,b=im.getpixel((px,py));observed=r>100 and r>g*1.5 and r>b*1.5
  assert observed==((x,y) in screen_cells),(x,y,(r,g,b));probes.append(dict(cell=[x,y],pixel=[px,py],rgb=[r,g,b],occupied=observed))
cells=sorted((x-3,2-y) for x,y in screen_cells);edges=Counter()
for x,y in cells:
 v=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
 for a,b in zip(v,v[1:]+v[:1]):edges[tuple(sorted((a,b)))]+=1
adj={}
for (a,b),n in edges.items():
 if n==1:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
assert all(len(v)==2 for v in adj.values());start=min(adj);cycle=[start];old=None;current=start
while True:
 nxt=min(v for v in adj[current] if v!=old)
 if nxt==start:break
 assert nxt not in cycle
 cycle.append(nxt);old,current=current,nxt
assert len(cycle)==len(adj)
def cross(a,b,c):return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
vertices=[v for i,v in enumerate(cycle) if cross(cycle[i-1],v,cycle[(i+1)%len(cycle)])]
assert len(vertices)==28
assert set(vertices)=={(x-3,3-y) for x,y in outline}
triangles=[]
for x,y in cells:
 triangles.extend([[[x,y],[x+1,y],[x+1,y+1]],[[x,y],[x+1,y+1],[x,y+1]]])
room=dict(triangles=triangles,marked=[[0,0],[-2,0]],require_simple=True,slits=[],boundary_targets=[[-2,0],[2,0],[0,2],[0,-2]],provenance='Idealized unit-square reconstruction of author-linked video ahm4knwln7I thumbnail. Original coordinate/settings file unavailable. Center and four long-wall midpoints stated in author description; no claim that raster pixels specify exact lengths.')
(B/'room.json').write_text(json.dumps(room,indent=2)+'\n')
result=dict(status='PASS',walls=28,cells=cells,square_count=len(cells),vertices=vertices,thumbnail_cell_probes=probes,room_sha256=hashlib.sha256((B/'room.json').read_bytes()).hexdigest(),exact_original_coordinates=False)
(B/'reconstruct.json').write_text(json.dumps(result,indent=2)+'\n')
s= (B/'inputs/video-page.html').read_text();m=re.search(r'var ytInitialPlayerResponse\s*=\s*(\{.*?\});',s);d=json.loads(m.group(1));detail=d['videoDetails'];(B/'inputs/video-details.json').write_text(json.dumps({k:detail[k] for k in ['videoId','title','author','channelId','shortDescription']},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['thumbnail_cell_probes','cells','vertices']},indent=2))
