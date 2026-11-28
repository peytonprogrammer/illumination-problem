"""Generate the 16-variable linear contradiction from the eight vertical itineraries."""
from pathlib import Path
import sys

witnesses = [(0,k,1) for k in (-5,-4,-3,-2)]
witnesses += [(i,k,-1) for i in (0,1) for k in (-1,0)]

def form(poly):
    terms=[]
    for row in range(4):
        x=[int(i==row) for i in range(4)]
        for col in range(4):
            y=[int(j==col) for j in range(4)]
            coef=poly(x,y)
            if coef:
                terms.append(f'(* {coef if coef>0 else f"(- {-coef})"} p{row}{col})')
    return '(+ '+' '.join(terms)+')' if terms else '0'

def distances(X,Y):
    x,t,r,l=X
    a,d,b,_=Y
    w=x+t; u=w+r; z=u+l
    return w,u,x,z,a,d,b

def tests(X,Y,i,k,sign):
    w,u,x,z,a,d,b=distances(X,Y)
    D=a+d+b
    start=sign*x+2*k*w
    # Interpolate from start to z+2ui. At the second gate subtract 2ui.
    first=(d+b)*start+a*(z+2*u*i)
    second=b*start+(a+d)*(z+2*u*i)-2*u*i*D
    return (w*D-first,w*D+first,u*D-second,u*D+second)

def model():
    lines=['(set-logic QF_LRA)']
    for i in range(4):
        for j in range(4):
            lines += [f'(declare-const p{i}{j} Real)', f'(assert (> p{i}{j} 0))']
    assumptions=[
        ('>',lambda X,Y:(X[0]+X[1])*Y[2]-sum(X[:3])*Y[1]),
        ('>',lambda X,Y:sum(X[:3])*(Y[1]+Y[2]-Y[0])),
        ('>=',lambda X,Y:(3*X[1]-X[2])*Y[2])]
    for j in range(4):
        assumptions.append(('>=',lambda X,Y,j=j:(X[1]+X[2]-X[3])*Y[j]))
    for op,poly in assumptions:
        lines.append(f'(assert ({op} {form(poly)} 0))')
    for i,k,sign in witnesses:
        margins=[form(lambda X,Y,j=j: tests(X,Y,i,k,sign)[j]) for j in range(4)]
        lines.append('(assert (or '+' '.join(f'(<= {margin} 0)' for margin in margins)+'))')
    return '\n'.join(lines)+'\n(check-sat)\n'

if __name__=='__main__':
    import cvc5
    data=model()
    Path('mask761.smt2').write_text(data)
    solver=cvc5.Solver()
    solver.setOption('produce-proofs','true')
    solver.setOption('check-proofs','true')
    parser=cvc5.InputParser(solver)
    parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,data,'mask761')
    while not parser.done():
        cmd=parser.nextCommand()
        if cmd.isNull():break
        result=cmd.invoke(solver,parser.getSymbolManager()).strip()
        if result: print(result)
    assert result=='unsat'
    solver.getProof()
