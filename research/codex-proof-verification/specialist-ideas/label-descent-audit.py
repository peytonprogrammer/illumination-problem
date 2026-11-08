"""Audit label transport on an existing saved orbit; do not discover states."""
from pathlib import Path
from collections import deque, Counter
import gzip
import hashlib
import json

folder = Path(__file__).resolve().parent
certificate = folder.parents[1] / 'illumination-generalization-2026-11-06/review/marked-origami-known22-closure.gz'
raw = gzip.decompress(certificate.read_bytes())
digest = hashlib.sha256(raw).hexdigest()
assert digest == '2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346'
n = 60
states = {tuple(raw[k+i*n:k+(i+1)*n] for i in range(3)) for k in range(0, len(raw), 3*n)}

def inverse(p):
    q = [0]*n
    for i, j in enumerate(p): q[j] = i
    return q

def step(state, tags, kind):
    h, v, labels = state
    if kind == 'T': v = bytes(v[inverse(h)[i]] for i in range(n))
    elif kind == 'U': h = bytes(h[inverse(v)[i]] for i in range(n))
    elif kind == 'Ti': v = bytes(v[h[i]] for i in range(n))
    elif kind == 'Ui': h = bytes(h[v[i]] for i in range(n))
    else: raise ValueError(kind)
    order = [0]; index = {0: 0}
    for a in order:
        for b in (h[a], v[a]):
            if b not in index: index[b] = len(order); order.append(b)
    return (bytes(index[h[a]] for a in order), bytes(index[v[a]] for a in order), bytes(labels[a] for a in order)), tuple(tags[a] for a in order)

initial = min(states)
h, v, labels = initial
hi, vi = inverse(h), inverse(v)
commutator = [v[h[vi[hi[i]]]] for i in range(n)]
tags = [-1]*n; zero = 0
for i in range(n):
    if commutator[i] == i or tags[i] >= 0: continue
    j = i
    while tags[j] < 0: tags[j] = zero; j = commutator[j]
    assert j == i
    zero += 1
assert zero == 9
for color, base in ((1, 9), (2, 13)):
    for offset, i in enumerate(i for i in range(n) if labels[i] == color): tags[i] = base+offset
initial_tags = tuple(tags)
parents = {initial: None}; transported = {initial: initial_tags}; queue = deque([initial])
counts = Counter(); witness = None
label_parent = list(range(17))
def representative(a):
    while label_parent[a] != a:
        label_parent[a] = label_parent[label_parent[a]]; a = label_parent[a]
    return a

def word(state):
    result = []
    while parents[state] is not None:
        state, kind = parents[state]; result.append(kind)
    return list(reversed(result))

while queue:
    state = queue.popleft()
    for kind in ('T', 'U'):
        nxt, nt = step(state, transported[state], kind)
        assert nxt in states
        if nxt not in transported:
            parents[nxt] = (state, kind); transported[nxt] = nt; queue.append(nxt)
        elif nt != transported[nxt]:
            old = transported[nxt]
            for a, b in zip(old, nt):
                if a >= 0: label_parent[representative(a)] = representative(b)
            counts['edges_with_any_label_disagreement'] += 1
            for name, lo, high in (('zero', 0, 9), ('source', 9, 13), ('target', 13, 17)):
                if any(lo <= a < high and a != b for a, b in zip(old, nt)): counts[name+'_disagreement_edges'] += 1
            if witness is None:
                loop = word(state)+[kind]+[x+'i' for x in reversed(word(nxt))]
                replay, rt = initial, initial_tags
                for letter in loop: replay, rt = step(replay, rt, letter)
                assert replay == initial and rt != initial_tags
                permutation = {}
                for a, b in zip(initial_tags, rt):
                    if a < 0: assert b < 0; continue
                    assert permutation.setdefault(a, b) == b
                witness = {'closed_word': loop, 'length': len(loop), 'label_permutation': permutation, 'final_tags': rt}
assert len(transported) == len(states)
classes = {}
for a in range(17): classes.setdefault(representative(a), []).append(a)
out = {'status': 'SAVED_ORBIT_LABEL_DESCENT_AUDIT', 'raw_sha256': digest, 'saved_states': len(states), 'checked_directed_edges': 2*len(states), 'disagreements': counts, 'label_monodromy_orbits': sorted(classes.values()), 'witness': witness, 'initial_state': [list(x) for x in initial], 'initial_tags': initial_tags, 'limits': 'Disagreement disproves descent of individual IDs to the existing coarse state, not of every label-aware potential. Explicitly enriching the state by finitely many labels remains finite; no enriched orbit was enumerated. No wall bound or new physical room follows.'}
(folder/'label-descent-audit.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k: out[k] for k in ('status', 'saved_states', 'checked_directed_edges', 'disagreements')}))
print('Witness:', None if witness is None else {'length': witness['length'], 'permutation': witness['label_permutation']})
print('Label monodromy orbits:', out['label_monodromy_orbits'])
