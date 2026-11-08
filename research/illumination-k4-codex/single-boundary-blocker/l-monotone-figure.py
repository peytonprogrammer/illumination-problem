from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fractions import Fraction as F
import json
B=Path(__file__).resolve().parent;f=json.loads((B/'l-monotone-fixture.json').read_text());paths=[[tuple(map(F,p)) for p in f[k]] for k in ['vertical_only','horizontal_only']]
V=[(0,0),(2,0),(2,1),(1,1),(1,2),(0,2)];W,H=1200,760;im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im);font='/System/Library/Fonts/Supplemental/Arial.ttf'
def ft(n):return ImageFont.truetype(font,n)
def xy(p,offset):return offset+210*float(p[0]),640-210*float(p[1])
d.text((45,26),'Two ways around a boundary blocker in an L-shaped room',font=ft(30),fill='#172b45')
d.text((45,78),'Choose reflections in the opposite wall orientation. The construction works for every interior pair.',font=ft(21),fill='#526274')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760"><rect width="1200" height="760" fill="white"/>','<text x="45" y="56" font-size="30" font-family="Arial">Two ways around a boundary blocker</text>']
for i,(P,offset,color,label) in enumerate(zip(paths,[80,690],['#1565c0','#16876d'],['Only vertical-wall reflections','Only horizontal-wall reflections'])):
 d.text((offset-20,145),label,font=ft(24),fill='#172b45')
 d.polygon([xy(v,offset) for v in V],fill='#f4f7fb');d.line([xy(v,offset) for v in V+[V[0]]],fill='#243c54',width=4)
 svg.append('<polygon points="'+' '.join(f'{xy(v,offset)[0]},{xy(v,offset)[1]}' for v in V)+'" fill="#f4f7fb" stroke="#243c54" stroke-width="4"/>')
 # Highlight wall orientation that this connection avoids.
 for a,b in zip(V,V[1:]+V[:1]):
  horizontal=a[1]==b[1]
  if horizontal==(i==0):d.line([xy(a,offset),xy(b,offset)],fill='#cf574e',width=5)
 a,b=xy((0,1),offset),xy((1,1),offset)
 for x in range(int(a[0])+8,int(b[0]),15):d.line([(x,a[1]),(x+6,a[1])],fill='#a9b5c5',width=1)
 d.line([xy(p,offset) for p in P],fill=color,width=3)
 svg.append('<polyline points="'+' '.join(f'{xy(v,offset)[0]},{xy(v,offset)[1]}' for v in P)+'" fill="none" stroke="'+color+'" stroke-width="3"/>')
 for a,b in zip(P,P[1:]):
  u,v=xy(a,offset),xy(b,offset);dx,dy=v[0]-u[0],v[1]-u[1];n=(dx*dx+dy*dy)**.5;dx/=n;dy/=n;cx,cy=(u[0]+v[0])/2,(u[1]+v[1])/2
  d.polygon([(cx+8*dx,cy+8*dy),(cx-6*dx+4*dy,cy-6*dy-4*dx),(cx-6*dx-4*dy,cy-6*dy+4*dx)],fill=color)
 for j,p in enumerate(P):
  # Portal marker is interior; only endpoints and actual bounces get dots.
  if p not in (P[0],P[-1]) and p in [(F(1,4),F(1)),(F(1),F(1,4))]:continue
  x,y=xy(p,offset);d.ellipse((x-5,y-5,x+5,y+5),fill=color)
 for txt,p,dx,dy in [('S',P[0],12,-10),('T',P[-1],12,-18)]:
  x,y=xy(p,offset);d.text((x+dx,y+dy),txt,font=ft(24),fill='#172b45')
 d.text((offset-15,675),'Avoids all '+('horizontal' if i==0 else 'vertical')+' walls (red).',font=ft(22),fill='#526274')
d.text((45,725),'Fixed illustration: S=(7/4,1/4), T=(1/4,7/4). Dashed segment is an open interior portal, not a wall.',font=ft(18),fill='#526274')
im.save(B/'l-monotone.png');svg.append('</svg>');(B/'l-monotone.svg').write_text('\n'.join(svg))
