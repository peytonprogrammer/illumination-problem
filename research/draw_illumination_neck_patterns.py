"""Check mark-exchange symmetry of saved residuals and draw the fixed necks."""
import hashlib
from html import escape
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from illumination_family_bound import triangles_in_cells
from illumination_three_two_star_bound import complete_support
from search_illumination_fan_partitions import fan_masks

OUT=Path(__file__).parent/'three-triples'
bounded=complete_support((2,1));ts=triangles_in_cells(bounded['allowed'])
ids,_=fan_masks(ts,(1,0));ids2,_=fan_masks(ts,(1,1))
source=OUT/'double-fan-audit-2-1.json';audit=json.loads(source.read_text());assert audit['status']=='PASS'
assert ids==json.loads((OUT/'fan-search-2-1.json').read_text())['summary']['fan_triangle_ids']
assert ids2==json.loads((OUT/'double-fan-search-2-1.json').read_text())['summary']['second_triangle_ids']
def transform(t):return tuple(sorted((4-p[0],2-p[1]) for p in t))
assert {transform(t) for t in ts}==set(ts)
p12=[ids2.index(ts.index(transform(ts[i]))) for i in ids]
p21=[ids.index(ts.index(transform(ts[i]))) for i in ids2]
def move(mask,perm):return sum(1<<perm[j] for j in range(8) if mask>>j&1)
def swap(row):
    outside,a,b=row
    return tuple(sorted((2-x,1-y) for x,y in outside)),move(b,p21),move(a,p12)
rows={(tuple(map(tuple,c['outside_cells'])),c['first_mask'],c['second_mask']) for c in audit['classes'] if c['status']!='INFEASIBLE'}
assert len(rows)==24 and {swap(row) for row in rows}==rows
assert all(swap(swap(row))==row for row in rows)
canonical=sorted({min(row,swap(row)) for row in rows});assert len(canonical)==12
result=dict(status='PASS',audit_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),raw_residual_patterns=sorted(rows),canonical_patterns=canonical,first_to_second_permutation=p12,second_to_first_permutation=p21,scope='Necessary residual central-fan patterns under the verified ray cuts; each represents many room outlines. Half-turn exchanges marked points and central cells. No darkness or universal illumination claim.')
(OUT/'neck-patterns-2-1.json').write_text(json.dumps(result,indent=2)+'\n')
W,H=1200,1220
im=Image.new('RGB',(W,H),'white');draw=ImageDraw.Draw(im)
font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
def font(size):return ImageFont.truetype(font_path,size)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>']
def text(x,y,s,size=16,fill='#172033'):
    draw.text((x,y),s,font=font(size),fill=fill)
    svg.append(f'<text x="{x}" y="{y+size}" font-family="Arial,sans-serif" font-size="{size}" fill="{fill}">{escape(s)}</text>')
def polygon(points,fill,stroke='#ffffff',width=1):
    draw.polygon(points,fill=fill);draw.line(points+[points[0]],fill=stroke,width=width)
    svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
def box(bounds,fill,stroke='#cbd5e1',width=1):
    a,b,c,d=bounds;polygon([(a,b),(c,b),(c,d),(a,d)],fill,stroke,width)
text(30,18,'The 12 remaining central-neck shapes',28)
text(30,57,'Target displacement (4,2). The 24 audited residual patterns pair under exchanging the two marks.',17)
text(30,83,'Blue: full marked cells. Purple: fixed triangles. Gray: undetermined neighbors, possibly absent.',16)
text(30,106,'Orange: one occupied outside cell. White inside either central cell: absent triangles. These are not room outlines.',15)
for number,(outside,a,b) in enumerate(canonical):
    col=number%3;row=number//3;left=24+col*392;top=148+row*262
    box((left,top,left+376,top+246),'#f8fafc','#dbe2ea')
    text(left+12,top+9,f'{number+1}. '+('No outside cell' if not outside else 'Outside cell (1,-1)'),17)
    text(left+12,top+31,f'Central masks: {a} / {b}',13,'#536174')
    scale=21;ox=left+85;oy=top+162
    def xy(p):return ox+scale*p[0],oy-scale*p[1]
    def cell_box(c,fill,stroke):
        x,y=(2*c[0],2*c[1]);tl=xy((x-1,y+1));br=xy((x+1,y-1));box((*tl,*br),fill,stroke)
    for c in sorted(bounded['mandatory']-{(0,0),(2,1),(1,0),(1,1)}):
        cell_box(c,'#e2e8f0','#b8c2cf');px,py=xy((2*c[0],2*c[1]));text(px-4,py-8,'?',12,'#66758b')
    for c,label in [((0,0),'S'),((2,1),'T')]:
        cell_box(c,'#2563eb','#1d4ed8');px,py=xy((2*c[0],2*c[1]));text(px-6,py-9,label,16,'#ffffff')
    for c,mask,cell_ids in [((1,0),a,ids),((1,1),b,ids2)]:
        cell_box(c,'#ffffff','#9e8bc4')
        for j,i in enumerate(cell_ids):
            if mask>>j&1:polygon([xy(p) for p in ts[i]],'#8854c0','#e0cbed')
    for c in outside:
        cell_box(c,'#fed7aa','#f59e0b');px,py=xy((2*c[0],2*c[1]));text(px-4,py-8,'?',12,'#92400e')
text(30,1200,'Necessary patterns only. Each still allows many boundary shapes; no dark room has been found.',14,'#536174')
im.save(OUT/'neck-patterns-2-1.png');(OUT/'neck-patterns-2-1.svg').write_text('\n'.join(svg)+'</svg>\n')
print(json.dumps(dict(status='PASS',raw_patterns=len(rows),symmetry_types=len(canonical),permutation=p12)))
