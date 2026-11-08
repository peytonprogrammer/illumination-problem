from pathlib import Path
from fractions import Fraction as F
import contextlib,io,runpy
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    model=runpy.run_path(str(root/'check.py'))
a=F(1);M=F(2);x=F(1,2);y=F(2);H=F(3);c=F(1);h=M/2;Y=y/c

configs=[]
for phase in ('minus','plus'):
    L,n=model['first_length'](a,x,h*(Y-1),phase)
    path,_=model['prescribed_path'](a,M,x,y,H,c,'bottom',phase,L,n)
    configs.append((path,'Bottom path '+('A' if phase=='minus' else 'B'),'#2863a5'))
T=h*(Y-1)/2
L,n=model['first_length'](a,x,T,'minus');phase='minus'
if L==h*Y: L,n=model['first_length'](a,x,T,'plus');phase='plus'
path,_=model['prescribed_path'](a,M,x,y,H,c,'notch',phase,L,n)
configs.append((path,'Notch path','#b84d20'))
W,HH=1440,590
im=Image.new('RGB',(W,HH),'white');draw=ImageDraw.Draw(im)
font='/System/Library/Fonts/Supplemental/Arial.ttf'
def ft(n): return ImageFont.truetype(font,n)
draw.text((45,25),'Three connecting paths have no shared boundary contact',font=ft(32),fill='#17212d')
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HH}"><rect width="100%" height="100%" fill="white"/>', '<text x="45" y="58" font-family="Arial" font-size="32">Three connecting paths have no shared boundary contact</text>']
for i,(path,title,color) in enumerate(configs):
    offset=55+480*i
    def xy(p): return (offset+90*float(p[0]),460-90*float(p[1]))
    poly=[(0,0),(4,0),(4,3),(3,3),(3,1),(1,1),(1,3),(0,3)]
    draw.text((offset,110),title,font=ft(25),fill='#17212d')
    svg.append(f'<text x="{offset}" y="135" font-family="Arial" font-size="25">{title}</text>')
    draw.polygon([xy(p) for p in poly],fill='#f4f5f7')
    draw.line([xy(p) for p in poly+[poly[0]]],fill='#293442',width=3)
    draw.line([xy(p) for p in path],fill=color,width=3)
    for points,attrs in [(poly,'fill="#f4f5f7" stroke="#293442" stroke-width="3"'),(path,f'fill="none" stroke="{color}" stroke-width="3"')]:
        tag='polygon' if points is poly else 'polyline'
        svg.append(f'<{tag} points="'+ ' '.join(f'{xy(p)[0]},{xy(p)[1]}' for p in points)+f'" {attrs}/>')
    for p,label in [((.5,2),'s'),((3.5,2),'t')]:
        xx,yy=xy(p);draw.ellipse((xx-5,yy-5,xx+5,yy+5),fill='#17212d')
        draw.text((xx-5,yy-29),label,font=ft(20),fill='#17212d')
        svg.append(f'<circle cx="{xx}" cy="{yy}" r="5" fill="#17212d"/><text x="{xx-5}" y="{yy-12}" font-family="Arial" font-size="20">{label}</text>')
    xx,yy=xy((2,0));draw.ellipse((xx-8,yy-8,xx+8,yy+8),fill='white',outline='#9a3150',width=3)
    svg.append(f'<circle cx="{xx}" cy="{yy}" r="8" fill="white" stroke="#9a3150" stroke-width="3"/>')
text='The two bottom paths share only the circled midpoint. The notch path avoids it.'
draw.text((45,520),text,font=ft(24),fill='#435263')
svg.append(f'<text x="45" y="545" font-family="Arial" font-size="24">{text}</text></svg>')
im.save(root/'three-paths.png');(root/'three-paths.svg').write_text('\n'.join(svg))
print('Saved three prescribed formula paths; exact geometry controls pass.')
