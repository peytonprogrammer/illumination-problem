#!/usr/bin/env python3
"""Typeset the frozen corrected proof; does not run research or alter its source."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKET = ROOT / 'research/illumination-generalization-2026-11-06/fable/eight-wall-review-packet'
SOURCE = PACKET / 'theorem-and-proof.md'
PIN = '335e29267bdb3354ca43bd990094b2cbe9ca46d2d4f727b5fe927f1a818969f4'
GREEK = set('tau rho theta alpha beta lambda mu delta ell eta sigma Sigma Lambda Beta'.split())
WORDS = set('the first strictly greater than where in not or and with on way up length is to if for'.split())


def escape(s):
    table = {'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(table.get(c,c) for c in s).replace('<=',r'\(\le\)').replace('>=',r'\(\ge\)').replace('->',r'\(\to\)')


def math(s):
    """Translate the packet's explicit ASCII formula notation without algebra."""
    s = s.strip().rstrip(',;')
    # A terminal full stop is prose punctuation, not a decimal.
    if s.endswith('.'): s = s[:-1]
    s = re.sub(r'\]\s+x\s+(?=\[)', '] CARTESIAN ', s)
    token = re.compile(r"[A-Za-z]+(?:_(?:\{[^{}]*\}|\([^()]*\)|[A-Za-z0-9]+))?(?:\^(?:\([^()]*\)|[0-9]+))?|'|<=>|<=|>=|->|[{}]|[^A-Za-z{}']")
    out=[]
    for m in token.finditer(s):
        t=m.group()
        if t in {'<=>','<=','>=','->','{','}'}:
            out.append({'<=>':r'\Longleftrightarrow','<=':r'\le ','>=':r'\ge ','->':r'\to ','{':r'\{','}':r'\}'}[t]);continue
        if re.match('[A-Za-z]',t):
            base=re.split('[_^]',t)[0]
            rest=t[len(base):]
            if base in GREEK: base='\\'+base
            elif base=='Z' and not rest and not s[m.end():].lstrip().startswith('('): base=r'\mathbb{Z}'
            elif base in {'min','max'}:base='\\'+base
            elif base=='int':base=r'\operatorname{int}'
            elif base=='CARTESIAN':base=r'\times'
            elif base=='union':base=r'\cup'
            elif base=='intersect':base=r'\cap'
            elif base=='in':base=r'\in'
            elif base in {'floor','sqrt'}:base=r'\operatorname{'+base+'}'
            elif base in WORDS:base=r'\text{'+base+r'}\;'
            elif len(base)>3:base=r'\text{'+base+r'}\;'
            def sub(m):
                x=m.group(1)
                if x.startswith(('(', '{')):return '_{'+math(x[1:-1])+'}'
                if x in GREEK:x='\\'+x
                elif len(x)>1 and not x.isdigit():x=r'\mathrm{'+x+'}'
                return '_{'+x+'}'
            rest=re.sub(r'_(\{[^{}]*\}|\([^()]*\)|[A-Za-z0-9]+)',sub,rest)
            rest=re.sub(r'\^(\([^()]*\)|[0-9]+)',lambda m:'^{'+m.group(1).strip('()')+'}',rest)
            out.append(base+rest)
        else:out.append(t)
    return ''.join(out)


INLINE = re.compile(r"`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|\bsqrt\(p\)|\b(?:tau|rho|theta|alpha|beta|lambda|mu|delta|ell|eta|sigma|Sigma|Lambda|Beta)(?:_[A-Za-z0-9]+)?\b|\b[A-Za-z]+_(?:\{[^{}]*\}|\([^()]*\)|[A-Za-z0-9]+)|(?:[0-9]*[A-Za-z]|\([^()]*\))\^[0-9]+\b|\b[A-Za-z]\b")

def inline(s):
    out=[];pos=0
    for m in INLINE.finditer(s):
        out.append(escape(s[pos:m.start()]));t=m.group()
        if t.startswith('`'):out.append(r'\texttt{'+escape(t[1:-1])+'}')
        elif t.startswith('**'):out.append(r'\textbf{'+inline(t[2:-2])+'}')
        elif t.startswith('*'):out.append(r'\emph{'+inline(t[1:-1])+'}')
        elif t=='Z' and s[m.end():].lstrip().startswith('('):out.append(r'\(Z\)')
        elif t=='x' and s[:m.start()].rstrip().endswith(']') and s[m.end():].lstrip().startswith('['):out.append(r'\(\times\)')
        elif t=='sqrt(p)':out.append(r'\(\sqrt{p}\)')
        elif t in {'A','I'} or (t == 'a' and re.match(r' (?:compact|Jordan|straight|corner|proof|wall|finite|maximal|path|shorter|contact|multiple|vertical|reflection|Euclidean|room|nonnegative|cyclic|union|control|rectangle|common|strictly|nearest|point|height|source|target|horizontal|seam|smooth|full|fixed|nonempty|positive|normal|larger|limit|developed|supplied|simple|special|few|specular|convex|monotone|period|nonzero|remainder|jump|step|symmetric|new|single|boundary|non-strict|right|left|non-adjacent|complete|rational|window|slope|strict|function|floor|roof|case|number|non-corner|reflex|nondecreasing|constant|bounded|stronger)\b', s[m.end():])):
            # These can be the English article/pronoun; mathematical meaning is unchanged.
            out.append(t)
        else:out.append(r'\('+math(t)+r'\)')
        pos=m.end()
    out.append(escape(s[pos:]))
    return ''.join(out)


def figure():
    svg=ET.fromstring((PACKET/'figures/fig-normal-forms.svg').read_text().replace('u<v','u&lt;v'))
    ns='{http://www.w3.org/2000/svg}'
    parts=[r'\begin{figure}[htbp]\centering',r'\begin{tikzpicture}[x=0.018cm,y=-0.018cm]']
    for p in svg.findall(ns+'polygon'):
        coords=' -- '.join('('+x+')' for x in p.attrib['points'].split())
        parts.append(r'\filldraw[fill=gray!8,draw=black,line width=.6pt] '+coords+r' -- cycle;')
    for c in svg.findall(ns+'circle'):
        if c.attrib['fill']=='#222':parts.append(r'\fill ('+c.attrib['cx']+','+c.attrib['cy']+r') circle[radius=2.7];')
    labels=[(85,205,'Rectangle, $W=4$'),(385,205,'L, $W=6$'),(685,205,'U, $k=1$'),(90,365,'Staircase, $k=2$'),(390,365,'T, $k=3$'),(690,365,'Offset corridor, $k=4$')]
    for x,y,t in labels:parts.append(r'\node[font=\small,anchor=north] at ('+str(x)+','+str(y)+'){'+t+'};')
    parts += [r'\end{tikzpicture}',r'\caption{The six normal forms in Proposition 1.2. Black dots mark reflex corners. For eight-wall rooms, $k$ is the shorter cyclic edge distance between the two reflex corners. Drawings illustrate the classes; all dimensions in the theorem are arbitrary admissible positive reals.}',r'\end{figure}']
    return '\n'.join(parts)


FRONT = r'''\documentclass[11pt]{article}
\usepackage[letterpaper,margin=0.9in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb,amsthm,mathtools,microtype,graphicx,tikz,enumitem,needspace}
\usepackage[colorlinks=true,linkcolor=black,urlcolor=blue!50!black]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt plus 1pt minus 1pt}
\setlength{\emergencystretch}{2em}
\setlist{nosep,leftmargin=1.5em,topsep=4pt}
\newcommand{\Beta}{B}
\hypersetup{pdftitle={Illumination of orthogonal rooms with at most eight walls},pdfauthor={Daniel Wang and Peyton Wang}}
\title{Illumination of orthogonal rooms\\with at most eight walls}
\author{Daniel Wang \and Peyton Wang}
\date{Working draft v0.1 --- November 8, 2026}
\begin{document}
\maketitle
\begin{abstract}
Every finite strictly simple orthogonal polygon with at most eight maximal walls illuminates every pair of distinct interior points by a finite specular path avoiding every polygon corner. We present a constructive proof for arbitrary real dimensions and endpoints. A turning-angle classification gives six normal forms. Orientation-controlled paths in L rooms cover many endpoint placements; the remaining U, offset-corridor and staircase cases use explicit folding constructions. The staircase proof combines floor and roof charts whose sufficient inequalities exhaust all admissible metrics. Seam endpoints, rounding ties and potential floor or roof corner contacts are treated explicitly. There is no lattice or rationality assumption and no uniform bound on reflections is asserted.
\end{abstract}
\begin{center}\small Draft for external mathematical review. Not submitted or externally refereed.\end{center}
\section*{Reader's guide and provenance}
This manuscript typesets the corrected proof packet archived on November 8, 2026. Sections 0--8 retain that packet's numbering and proof text; display notation and typography are adapted for print. The proof is analytic. Fixed-input computations accompanying it are reproducibility controls and do not establish its real-parameter quantifiers.

Proof development and internal cross-review used Codex and Claude AI agents. A later coordinator review corrected a window-bound transcription and made seam cases, contact bounds and U-room termination explicit. No human mathematical referee or formal proof assistant has verified this work. Appendix A gives source links, reproduction instructions and the principal review checkpoints. Appendix B illustrates selected prescribed paths.

The result concerns at most \emph{eight walls}, equivalently at most two reflex corners. It does not address the separate eight-reflex-corner research target or the proposed universal 22-wall minimum. All point pairs in the theorem are interior pairs.
'''


def render_body(body):
    lines=body.splitlines();out=[];i=0;list_open=None
    def close():
        nonlocal list_open
        if list_open:out.append(r'\end{'+list_open+'}');list_open=None
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('### ') or line.startswith('## '):
            close();level='subsection' if line.startswith('### ') else 'section'
            title=line.lstrip('# ')
            if title.startswith('2. Rectangles'):out.append(figure())
            out.append(chr(92)+level+'*{'+inline(title)+'}')
            i+=1;continue
        if line.startswith('    '):
            close();block=[]
            while i<len(lines) and lines[i].startswith('    '):block.append(lines[i][4:]);i+=1
            out.append(r'\begin{gather*}')
            for j,formula in enumerate(block):
                out.append(math(formula)+(r' \\' if j<len(block)-1 else ''))
            out.append(r'\end{gather*}');continue
        m=re.match(r'(- |\d+\. )(.*)',line)
        if m:
            typ='itemize' if m.group(1)=='- ' else 'enumerate'
            if list_open!=typ:close();list_open=typ;out.append(r'\begin{'+typ+'}')
            para=[m.group(2)];i+=1
            while i<len(lines) and lines[i].strip() and lines[i].startswith('  ') and not lines[i].startswith('    '):para.append(lines[i].strip());i+=1
            out.append(r'\item '+inline(' '.join(para)));continue
        close();para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('##','    ','- ')) and not re.match(r'\d+\. ',lines[i]):para.append(lines[i].strip());i+=1
        text=' '.join(para)
        if text.startswith(('**Theorem','**Lemma','**Proposition','**Corollary','**Main theorem')):out.append(r'\Needspace{4\baselineskip}')
        out.append(inline(text)+'\n')
    close();return '\n'.join(out)


BACK = r'''
\clearpage
\section*{Appendix A. Source record, reproduction and review}
\textbf{Versioned proof source.} The mathematical text is the corrected \texttt{theorem-and-proof.md} in the included eight-wall review packet. Its exported SHA-256 is recorded in \texttt{provenance.json} next to this manuscript. The archive manifests record source and exported hashes separately. A review pin identifies the exact source version tested.

\textbf{Repository.} \url{https://github.com/peytonprogrammer/illumination-problem}. Repository access is private at this version. An external reviewer needs access or a supplied copy; a link alone does not grant access. The complete argument in this PDF does not require fetching numerical certificates.

\textbf{Reproduce prescribed checks.} From a checkout of the repository, run:
\begin{quote}\ttfamily\small
python3 tools/reproduce.py eight-wall
\end{quote}
The runner copies inputs into a temporary workspace and runs twelve prescribed scripts. The expected final markers are \texttt{ALL CHECKS EXITED 0} and the suite's \texttt{PASS} line. These checks exercise exact path guards, seam cases and symbolic identities on supplied inputs. They neither search for new paths nor prove the arbitrary-real statements. Python 3 is required; this suite needs no large-data downloads. The build instructions for this PDF are in the neighboring \texttt{README.md}.

\textbf{Review record.} The archived coordinator review is in \path{coordination/general-proof-priority/final-review/eight-wall-review.md} under the same research family. The original packet also contains \texttt{dependency-manifest.json}, \texttt{coverage.md}, \texttt{cover-note.md}, \texttt{reproduce.md} and exact figure paths.

\textbf{Suggested mathematical checkpoints.}
\begin{enumerate}
\item Proposition 1.2: six normal forms, positivity, closure and strict simplicity, especially the offset corridor.
\item Theorem 2.1 and Lemma 2.2: orientation control and source-on-seam use in larger rooms.
\item Theorem 3.1: finite termination away from step-function jumps, original-wall contacts and the open floor-contact interval.
\item Theorems 4.1 and 5.2: exhaustive endpoint placement splits and avoidance of artificial mirrors.
\item Lemmas 6.2--6.4: strict portal guards, the corrected partial-window length and velocity agreement at seams.
\item Theorem 6.5: two consecutive target images prevent both floor contacts from being corners.
\item Theorem 6.8, Step 4: a candidate roof-corner contact implies an earlier encounter with the actual target, including its seam case.
\item Proposition 6.10: the four staircase conditions exhaust all positive real metrics.
\end{enumerate}
A submission version would require a dedicated literature discussion, settled author details and an explicit record of any further mathematical revisions.

\clearpage
\section*{Appendix B. Prescribed example paths}
These illustrations reuse the corrected packet's fixed rational fixtures. Dots mark contacts and endpoints; dashed seams are open passages, not mirrors. The proof covers all admissible real parameters independently of the drawings. The archived figure generator and \texttt{paths.json} give the exact inputs and checks. The print figures retain the source geometry and paths; embedded headings and overlapping source legends are replaced by captions.
FIGURES_HERE
\end{document}
'''


def main():
    raw=SOURCE.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    if sha!=PIN:raise SystemExit('Corrected source changed; review it before updating the pinned build.')
    source=raw.decode();body=source[source.index('## 0. Conventions and statement'):]
    import pymupdf as fitz
    (HERE/'figures').mkdir(exist_ok=True)
    figures=[]
    for name,caption in [('fig-L','An L-room path with controlled reflection orientation (Theorem 2.1).'),('fig-U','The opposite-arm U construction, with one smooth floor reflection (Theorem 3.1).'),('fig-staircase-floor','The staircase floor chart (Theorem 6.5).'),('fig-staircase-roof','The roof chart (Theorem 6.8). The blue path has a smooth roof reflection; the red path reaches the target before its candidate roof-corner contact and stops there.')]:
        svg=ET.fromstring((PACKET/'figures'/(name+'.svg')).read_text())
        ns='{http://www.w3.org/2000/svg}'
        for text in list(svg.findall(ns+'text')):
            if (text.text or '').strip() not in {'S','T'}:svg.remove(text)
        svgdata=ET.tostring(svg)
        doc=fitz.open(stream=svgdata,filetype='svg')
        (HERE/'figures'/(name+'.pdf')).write_bytes(doc.convert_to_pdf())
        figures.append(r'\begin{figure}[htbp]\centering\includegraphics[width=0.70\linewidth,height=0.30\textheight,keepaspectratio]{figures/'+name+r'.pdf}\caption{'+caption+r'}\end{figure}')
    tex=FRONT+render_body(body)+BACK.replace('FIGURES_HERE','\n'.join(figures))
    (HERE/'manuscript.tex').write_text(tex)
    (HERE/'provenance.json').write_text(json.dumps({'source_path':str(SOURCE.relative_to(ROOT)),'source_sha256':sha,'body_start':'## 0. Conventions and statement','proof_text_policy':'all source proof paragraphs and displays retained; typesetting-only translation','mathematics_extended':False,'external_refereeing':False},indent=2)+'\n')
    print('Generated manuscript.tex from pinned corrected proof:',sha)


if __name__=='__main__':main()
