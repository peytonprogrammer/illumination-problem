from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parent
V=[(0,0),(1,1),(2,1),(2,3),(1,3),(1,2),(-1,2),(-1,1),(0,1)]
im=Image.new('RGBA',(1200,670),'white');d=ImageDraw.Draw(im);fn='/System/Library/Fonts/Supplemental/Arial.ttf'
def ft(n):return ImageFont.truetype(fn,n)
def p(q,offset):return offset+100*q[0],560-100*q[1]
d.text((46,25),'Why the nine-wall base cannot open both marks',font=ft(31),fill='#172b45')
d.text((46,79),'The wall through A is not a supporting line of the whole base.',font=ft(22),fill='#526274')
for offset,label in [(180,'Base P'),(790,'P and its reflection across A\'s wall')]:
 d.text((offset-110,140),label,font=ft(23),fill='#172b45')
 if offset==790:
  lay=Image.new('RGBA',im.size,(0,0,0,0));ld=ImageDraw.Draw(lay)
  ld.polygon([p((x,4-y),offset) for x,y in V],fill=(234,99,90,100),outline='#ce493e',width=3)
  im=Image.alpha_composite(im,lay);d=ImageDraw.Draw(im)
 lay=Image.new('RGBA',im.size,(0,0,0,0));ld=ImageDraw.Draw(lay);ld.polygon([p(q,offset) for q in V],fill=(61,139,214,100),outline='#2466a1',width=3)
 im=Image.alpha_composite(im,lay);d=ImageDraw.Draw(im)
 if offset==790:
  x0,y1=p((1,1),offset);x1,y0=p((2,3),offset);d.rectangle((x0,y0,x1,y1),fill=(145,89,170,150),outline='#723c92',width=3)
 for x in range(offset-135,offset+250,15):d.line([(x,360),(x+8,360)],fill='#ce493e',width=2)
 for txt,q,delta in [('A',(0,2),(-20,-35)),('B',(2,2),(10,-12))]:
  x,y=p(q,offset);d.ellipse((x-5,y-5,x+5,y+5),fill='#172b45');d.text((x+delta[0],y+delta[1]),txt,font=ft(24),fill='#172b45')
 if offset==180:
  x,y=p((1.5,2),offset);d.ellipse((x-7,y-7,x+7,y+7),fill='#b86813');d.text((offset-105,590),'y = 2 crosses the interior at (3/2, 2).',font=ft(20),fill='#526274')
 else:d.text((offset-120,590),'Purple: overlap of the two copy interiors.',font=ft(20),fill='#526274')
im.convert('RGB').save(B/'supporting-line.png')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="670"><rect width="1200" height="670" fill="white"/>','<text x="46" y="55" font-family="Arial" font-size="31">The nine-wall base: reflection forces overlap</text>']
for offset in [180,790]:
 if offset==790:svg.append('<polygon points="'+' '.join(f'{p((x,4-y),offset)[0]},{p((x,4-y),offset)[1]}' for x,y in V)+'" fill="#e9635a" fill-opacity=".4" stroke="#ce493e" stroke-width="3"/>')
 svg.append('<polygon points="'+' '.join(f'{p(q,offset)[0]},{p(q,offset)[1]}' for q in V)+'" fill="#3d8bd6" fill-opacity=".4" stroke="#2466a1" stroke-width="3"/>')
 svg.append(f'<path d="M{offset-135} 360 H{offset+250}" stroke="#ce493e" stroke-dasharray="8 7"/>')
 for t,q in [('A',(0,2)),('B',(2,2))]:
  x,y=p(q,offset);svg.append(f'<circle cx="{x}" cy="{y}" r="5"/><text x="{x-10}" y="{y-15}" font-family="Arial" font-size="24">{t}</text>')
svg.append('</svg>');(B/'supporting-line.svg').write_text('\n'.join(svg))
