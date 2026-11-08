from pathlib import Path
from html import escape,unescape
import json,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak,Table,TableStyle,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parent;j=json.loads((ROOT/'check.json').read_text())
INK=colors.HexColor('#172b45');GRAY=colors.HexColor('#526274');LIGHT=colors.HexColor('#edf2f7')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='T',fontName='Helvetica-Bold',fontSize=21,leading=25,textColor=INK,spaceAfter=10))
styles.add(ParagraphStyle(name='H',fontName='Helvetica-Bold',fontSize=12,leading=16,textColor=INK,spaceBefore=8,spaceAfter=7))
styles.add(ParagraphStyle(name='B',fontName='Helvetica',fontSize=10.4,leading=14,textColor=INK,spaceAfter=8))
styles.add(ParagraphStyle(name='S',fontName='Helvetica',fontSize=9,leading=12,textColor=GRAY,spaceAfter=7))
styles.add(ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=9.6,leading=12.8,textColor=INK,spaceAfter=0))
styles.add(ParagraphStyle(name='Call',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=INK,spaceAfter=8,backColor=LIGHT,borderPadding=8))

def para(s,style='B'):return Paragraph(s,styles[style])
def img(name,width=516,height=None):
 w,h=PILImage.open(ROOT/(name+'.png')).size
 scale=min(width/w,height/h) if height else width/w
 return Image(str(ROOT/(name+'.png')),width=w*scale,height=h*scale)
def table(rows,widths):
 t=Table([[para(escape(str(c)),'Cell') for c in row] for row in rows],colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#b8c7d6'))]));return t

def footer(label):
 def fn(c,doc):
  c.setFont('Helvetica',8);c.setFillColor(GRAY);c.drawString(48,28,label);c.drawRightString(564,28,str(doc.page))
 return fn

def coords(vs,n=6):
 lines=[]
 for i in range(0,len(vs),n):lines.append(', '.join('('+','.join(map(str,p))+')' for p in vs[i:i+n]))
 return '<br/>'.join(lines)

story=[];md=[]
def p(s,style='B'):
 story.append(para(s,style));prefix='# ' if style=='T' else '## ' if style=='H' else ''
 md.append(prefix+unescape(re.sub('<[^>]+>','',s.replace('<br/>','\n'))))
def image(name,width=516,height=None):story.append(img(name,width,height));md.append('!['+name.replace('-',' ')+']('+name+'.png)');story.append(Spacer(1,5))
def page():story.append(PageBreak());md.append('---')

p('A 22-wall mirror room','T')
p('An expanded elementary proof, with the seam events shown explicitly.','S')
p('Statement. In the room below, S = (0,0) and T = (2,2) cannot be joined by any finite, corner-avoiding billiard path.','Call')
p('The mirrors are the solid outside boundary. Dashed lines are open passages between copies; they are not mirrors. A path may reflect at a smooth point of a wall, but it may not hit an actual corner.')
image('room-panel',516,247)
p('Build the room from one five-square piece','H')
p('Let P be the union of the five closed unit squares with lower-left corners (-1,-1), (0,-1), (0,-2), (1,-2), (1,-3). Mark a = (0,0) and b = (2,-2) on its boundary. Both are smooth wall points, not corners.')
p('Take these three reflected copies:')
story.append(table([['Copy','Point in Q corresponding to (x,y) in P'],['P0','(x,y)'],['P1','(x,-y)'],['P2','(4-x,-y)']],[72,444]));story.append(Spacer(1,8))
p('P0 and P1 meet on the horizontal interval [-1,1] x {0}. P1 and P2 meet on the vertical interval {2} x [1,3]. Their interiors are disjoint, and there are no other contacts. Their union Q is a simple polygon.')
p('S is the midpoint of the first seam and T is the midpoint of the second. Folding every copy back onto P sends S to a and T to b. We will show that a connecting path in Q would force an impossible connection in P.')
page()

p('1. The lattice obstruction in P','T')
p('First consider ordinary billiard paths in P. Here is its complete integer-point census.','B')
base_side=[para('<b>Integer-point census</b><br/><br/>The only smooth integer boundary points are a = (0,0) and b = (2,-2).<br/><br/>The seven convex corners are:<br/>(-1,-1), (-1,0), (0,-2), (1,-3), (1,0), (2,-3), (2,-1).<br/><br/>The three concave corners are:<br/>(0,-1), (1,-2), (1,-1).<br/><br/>There are no interior integer points.','Cell')]
story.append(Table([[img('base-panel',235,190),base_side]],colWidths=[252,264],style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8)]));story.append(Spacer(1,8));md.append('Integer-point census: only a and b are smooth; seven convex and three concave corners, no interior integer points.')
p('Reflecting across an integer-coordinate wall preserves parity','H')
p('Reflection in a vertical wall x = c changes x to 2c - x. Reflection in a horizontal wall y = d changes y to 2d - y. Here c and d are integers. Thus both kinds of reflection preserve the integer lattice and each coordinate modulo two. The inverse unfolding maps are compositions of the same reflections, so they preserve parity too.')
p('Assume an ordinary path joined a to b. Unfold its reflections: reflect each successive copy of P instead of bending the ray. The path becomes a straight segment from a = (0,0) to an image V of b. Both coordinates of b are even, so both coordinates of V are even. Also V is nonzero: unfolding preserves the positive length of the proposed path.')
p('An odd-coordinate integer point occurs before V','H')
p('Halve both coordinates of V while both are even. Stop at the first integer point z with an odd coordinate. At least one division was made, so z lies strictly between 0 and V on the unfolded segment.')
image('parity-panel',490,118)
p('Fold z back along the proposed path. Its image is an integer point of P with at least one odd coordinate. It is therefore neither a nor b. By the census, it is an actual corner. That contradicts corner avoidance. If z is exactly at a join between unfolded copies, the same argument still identifies an actual boundary corner.')
p('<b>Conclusion 1.</b> No ordinary corner-avoiding billiard path in P joins a to b.')
page()

p('2. The two kinds of seam event','T')
p('Inside each copy, folding preserves straight motion and ordinary wall reflections. Two events need to be distinguished.','B')
p('Crossing the interior of an open seam','H')
image('fold-panel',490,130)
p('The two folding maps agree on the seam and reflect the normal velocity component. A straight crossing in Q therefore becomes an ordinary reflection in a smooth wall of P.')
p('Hitting a seam endpoint on the outside wall','H')
image('reversal-panel',490,140)
p('For example, let E = (1,0). A ray approaching E through P1 has physical velocity (u,-v), with u,v &gt; 0. Before the hit, folding by (x,y) -&gt; (x,-y) gives velocity (u,v). The actual vertical mirror changes the physical velocity to (-u,-v), and the ray now enters P0. Its folded velocity is also (-u,-v). The folded path reverses exactly, along the line it just followed.')
story.append(table([['Smooth point in Q','Corner in P','Actual mirror','Folded velocity'],['(-1,0)','(-1,0)','vertical','(p,q) -> (-p,-q)'],['(1,0)','(1,0)','vertical','(p,q) -> (-p,-q)'],['(2,1)','(2,-1)','horizontal','(p,q) -> (-p,-q)'],['(2,3)','(2,-3)','horizontal','(p,q) -> (-p,-q)']],[127,115,110,164]));story.append(Spacer(1,8));md.append('The four endpoint images are (-1,0)->(-1,0), (1,0)->(1,0), (2,1)->(2,-1), (2,3)->(2,-3).')
p('In the table, (p,q) is the incoming folded velocity; its components may have either sign. The listed maps hold in both directions of travel. All other base-corner preimages are actual corners of Q and cannot be hit. In particular, the three concave base corners give nine actual concave corners of Q. The 21 convex-corner incidences give 13 actual convex corners and two incidences at each of the four smooth points above. This accounts for all 30 corner incidences.')
page()

p('3. Why a reversal cannot help','T')
p('A projected path can revisit a or reach b before the physical ray reaches T. The following choice of subpath handles those possibilities.','B')
p('<b>Step A.</b> Suppose a finite valid path in Q joined S to T, and fold it onto P. Stop the folded path at its first arrival at b. Within that prefix, start at its last visit to a. Call this subpath gamma. It goes from a to b and has no interior visit to either mark.')
p('At every interior or smooth-wall point of P, folded motion follows the ordinary billiard law of P, regardless of the current copy. Thus ordinary folded motion is deterministic and reversible.')
p('<b>Step B.</b> If gamma has a corner reversal of the kind shown on page 3, take the first one. Before it, gamma has only ordinary reflections at smooth walls of P. Those reflections are deterministic and reversible. After reversing, gamma must retrace that same route until it returns to its starting point a.')
p('Let d be the length from the start of gamma to this first reversal. The next d units of travel must retrace that same route backward. If gamma ended at b during that retrace, then b would already lie on its preceding route, contrary to Step A. At the end of the retrace it is at a, not b. Thus this return to a is an interior visit. This contradicts Step A, so gamma has no corner reversal.')
p('<b>Step C.</b> Gamma is now an ordinary corner-avoiding a-to-b billiard path in P. Conclusion 1 says that no such path exists. Therefore the original S-to-T path in Q does not exist.','Call')
p('Why the first and last visits are well defined','H')
p('An axis-parallel path cannot connect S to T: reflection in an orthogonal wall cannot create a missing velocity component, while both coordinates of S and T differ. Every possible connecting path is therefore nonaxial. Reflections change only signs, so both velocity components stay nonzero. Each of its finitely many straight legs crosses each of the two seams at most once. Folding subdivides it into finitely many nonconstant straight pieces, so there are only finitely many visits to either mark.')
p('The other preimages of the marks','H')
story.append(table([['Base point','All its preimages in Q'],['a = (0,0)','S = (0,0), and (4,0)'],['b = (2,-2)','T = (2,2), and (2,-2)']],[155,361]));story.append(Spacer(1,8))
p('The extra preimages are smooth boundary points. Step A allows all their possible visits; it does not assume that a return to a must be a return to S.','S')
p('Cyclic coordinates of the 22-wall boundary','H')
original=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
p(coords(original),'S')
p('This proves the stated dark pair for every finite corner-avoiding billiard path. It makes no assumption about a bound on directions, path length or number of reflections.','S')
fn=footer('22-wall mirror room | Expanded elementary proof')
SimpleDocTemplate(str(ROOT/'proof-expanded.pdf'),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=39,bottomMargin=44,title='A 22-wall mirror room: an expanded elementary proof',author='').build(story,onFirstPage=fn,onLaterPages=fn)
(ROOT/'proof-expanded.md').write_text('\n\n'.join(md)+'\n')

# Additional room: a fourth reflected copy, with the same verified folding rule.
story=[];md=[]
p('A second room: 30 walls','T')
p('Four reflected copies of the same five-square base, with S = (0,0) and T = (2,2).','S')
image('second-example',516,324)
p('Add one reflected copy on the left','H')
p('Keep P0, P1 and P2 from the 22-wall construction. Add P3 = {(-2-x,y) : (x,y) in P}. This reflects P0 across x = -1. Its interior is disjoint from the other three copies. It attaches to P0 on the interval {-1} x [-1,0].')
p('The new union is a strictly simple orthogonal polygon with 30 maximal walls: 17 convex corners and 13 concave corners. S and T are still interior points. The new open seam is green and dashed; its lower endpoint (-1,-1) is a smooth wall point.')
p('At (-1,0), three copies meet in three quadrants. The missing fourth quadrant makes this an actual 270-degree corner, so a valid billiard path cannot hit it. There is no pinch or hole. This is a different four-copy layout with 30 walls.')
p('Fold P3 back by (x,y) -&gt; (-2-x,y), together with the previous three folding maps. All the maps agree at every shared point. The same base obstruction will prove that S and T remain dark.','B')
page()
p('Why the second room is dark','T')
p('The base P is unchanged: its only noncorner integer points are the even-even marks a and b. Unfolding any ordinary a-to-b path produces an even-even nonzero endpoint. Repeated halving forces an odd-coordinate integer point earlier on that straight segment. Folding it back gives an actual base corner. Thus no such ordinary base path exists.')
p('The four smooth seam-endpoint events','H')
story.append(table([['Smooth point in the 30-wall room','Convex corner in P'],['(-1,-1)','(-1,-1)'],['(1,0)','(1,0)'],['(2,1)','(2,-1)'],['(2,3)','(2,-3)']],[260,256]));story.append(Spacer(1,9))
p('At each listed point, a physical wall reflection switches the adjacent copy. Folding therefore reverses both velocity components, exactly as in the 22-wall proof. Every other preimage of a base corner is an actual room corner. No concave base corner becomes a smooth or interior room point.')
p('For a precise count, the 40 base-corner incidences consist of 17 convex room corners, 12 ordinary concave room corners, three incidences at the actual concave corner (-1,0), and eight incidences at the four smooth points in the table: 17 + 12 + 3 + 8 = 40.')
p('Now suppose an S-to-T path existed. Fold it, stop at its first b and start at its last a before that b. A first corner reversal would retrace to a before reaching b, contradicting that choice. With no reversal, the resulting a-to-b path would be ordinary, contradicting the lattice argument. Hence S and T do not illuminate each other.','Call')
p('All preimages of the two marks','H')
story.append(table([['a = (0,0)','(-2,0), (0,0), (4,0)'],['b = (2,-2)','(-4,-2), (2,-2), (2,2)']],[135,381]));story.append(Spacer(1,6))
p('The same first-b/last-a choice handles these extra smooth-boundary preimages. The finite-event argument is unchanged because all seams are horizontal or vertical and a connecting path would be nonaxial.','S')
p('Cyclic coordinates of the 30-wall boundary','H')
p(coords(j['packets'][1]['room']['vertices']),'S')
p('Thus the four-copy construction gives a second simple mirror room with a dark pair of interior points.','S')
fn=footer('30-wall additional example | Four-copy construction')
SimpleDocTemplate(str(ROOT/'additional-example.pdf'),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=39,bottomMargin=44,title='A second mirror room: a 30-wall four-copy example',author='').build(story,onFirstPage=fn,onLaterPages=fn)
print('Created expanded proof and additional-example PDFs.')
