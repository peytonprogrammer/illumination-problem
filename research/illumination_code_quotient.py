"""Exact canonical forms for colored pairs of sheet permutations.

Simultaneous color-preserving conjugacy respects product codes and their powers,
so merging these states preserves every descendant's complete visibility test.
"""
from collections import Counter


def canonical(low,high,colors):
    n=len(colors);remaining=set(range(n));components=[]
    while remaining:
        root=min(remaining);component={root};todo=[root]
        for i in todo:
            for j in (low[i],high[i]):
                if j not in component:component.add(j);todo.append(j)
        remaining-=component
        counts=Counter(colors[i] for i in component);rare=min(counts,key=lambda c:(counts[c],c));best=None
        for root in sorted(i for i in component if colors[i]==rare):
            order=[root];index={root:0}
            for i in order:
                for j in (low[i],high[i]):
                    if j not in index:index[j]=len(order);order.append(j)
            assert len(order)==len(component)
            key=(tuple(colors[i] for i in order),tuple(index[low[i]] for i in order),tuple(index[high[i]] for i in order))
            if best is None or key<best:best=key
        components.append(best)
    return tuple(sorted(components))


def conjugate(p,relabel):
    q=[0]*len(p)
    for i,j in enumerate(p):q[relabel[i]]=relabel[j]
    return tuple(q)
