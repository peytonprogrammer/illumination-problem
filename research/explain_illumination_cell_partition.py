"""Draw two coarse cell patterns from the complete diagonal partition."""
from html import escape
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).parent/'three-triples'
W,H=1280,650
im=Image.new('RGB',(W,H),'#ffffff')
draw=ImageDraw.Draw(im)
font_path=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
def font(size):
    return ImageFont.truetype(str(font_path),size) if font_path.exists() else ImageFont.load_default(size=size)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>']
def text(x,y,value,size=22,fill='#1f2937'):
    draw.text((x,y),value,font=font(size),fill=fill)
    svg.append(f'<text x="{x}" y="{y+size}" font-family="Arial,sans-serif" font-size="{size}" fill="{fill}">{escape(value)}</text>')
def line(a,b,fill='#cbd5e1',width=1):
    draw.line([a,b],fill=fill,width=width)
    svg.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{fill}" stroke-width="{width}"/>')
def rect(box,fill,outline='#cbd5e1',width=1):
    draw.rectangle(box,fill=fill,outline=outline,width=width)
    x,y,x2,y2=box
    svg.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" fill="{fill}" stroke="{outline}" stroke-width="{width}"/>')
def dashed(box):
    x,y,x2,y2=box
    for a,b in [((x,y),(x2,y)),((x2,y),(x2,y2)),((x2,y2),(x,y2)),((x,y2),(x,y))]:
        length=max(abs(b[0]-a[0]),abs(b[1]-a[1]))
        for k in range(0,length,12):
            p=tuple(a[i]+(b[i]-a[i])*k/length for i in (0,1))
            q=tuple(a[i]+(b[i]-a[i])*min(k+7,length)/length for i in (0,1))
            line(p,q,'#64748b',2)
text(45,22,'A complete cell partition for the farther diagonal marks',30)
text(45,65,'Fewer than 24 walls + three exceptions allow at most two occupied cells outside the marked neighborhoods.',20)
full={(0,0),(2,2)}
required=full|{(x+dx,y+dy) for x,y in full for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]}
for left,extras,title in [(100,{(1,1)},'One example: central bridge'),(740,{(1,1),(3,3)},'Another example: bridge plus outer cell')]:
    top=153
    step=72
    text(left-30,110,title,23)
    def box(p):
        x,y=p
        x0=left+(x+1)*step
        y0=top+(3-y)*step
        return x0,y0,x0+step,y0+step
    for x in range(-1,4):
        for y in range(-1,4):rect(box((x,y)),'#ffffff','#e2e8f0')
    for p in required-full:
        b=box(p);rect(b,'#f1f5f9','#e2e8f0');dashed(tuple(v+3 if i<2 else v-3 for i,v in enumerate(b)))
    for p in extras:
        b=box(p);rect(b,'#ffedd5','#ea580c',3)
        text(b[0]+26,b[1]+19,'?',29,'#9a3412')
    for p in full:
        b=box(p);rect(b,'#dbeafe','#2563eb',3)
        x,y,x2,y2=b;center=((x+x2)//2,(y+y2)//2)
        for q in [(x,y),((x+x2)//2,y),(x2,y),(x2,(y+y2)//2),(x2,y2),((x+x2)//2,y2),(x,y2),(x,(y+y2)//2)]:line(center,q,'#93c5fd')
        rect((center[0]-4,center[1]-4,center[0]+4,center[1]+4),'#1d4ed8','#1d4ed8')
text(45,545,'Blue: full cells around the two marks.  Dashed: neighboring positions; some may be absent.',21)
text(45,580,'Orange: occupied partial cells. Two examples from the complete list of 40 cell patterns.',21)
text(45,614,'All 40 choices were excluded below 24 walls in the stated canonical tile family.',20)
im.save(BASE/'cell-partition-explanation.png')
svg.append('</svg>')
(BASE/'cell-partition-explanation.svg').write_text('\n'.join(svg))
