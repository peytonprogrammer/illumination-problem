"""Build results_r3.tsv (one row per open position-type pair) from the logs."""
import json
from collections import Counter
U = {}
for l in list(open('thin_corridor_r3.tsv'))[1:]:
    m, sh, S, T, k, u, w = l.rstrip('\n').split('\t'); U[(int(m), S, T)] = (sh, k, u, w)
runs = {}
for f in ('logs/chain_door_D2.jsonl', 'logs/collinear_D2_long.jsonl'):
    for l in open(f):
        o = json.loads(l); runs[(o['mask'], str(tuple(o['S'])), str(tuple(o['T'])))] = o
d4 = {}
for l in open('logs/collinear_D4.jsonl'):
    o = json.loads(l); d4[(o['mask'], str(tuple(o['S'])), str(tuple(o['T'])))] = o
out = open('results_r3.tsv', 'w')
cols = ['mask', 'shape', 'S', 'T', 'kind', 'lemmaU', 'lemmaU_corridor', 'dims', 'status', 'D', 'dp',
        'trunc_closed', 'frac_est', 'boxes', 'cert_boxes', 'itins_used', 'max_ref_used',
        'replay_points', 'replay_fail', 'cpu_s', 'D4_frac_est']
out.write('\t'.join(cols) + '\n')
st = Counter(); used_ref = Counter(); cpu = 0
for key, (sh, k, u, w) in U.items():
    o = runs[key]; cpu += o['cpu_total']
    if u == '1': status = 'not closable by finitely many itineraries (Lemma U); truncated region partly covered'
    elif o['closed_trunc']: status = 'truncated region R(2,4) closed; full region open'
    else: status = 'truncated region R(2,4) partly covered'
    st[(k, u, o['closed_trunc'])] += 1
    if o['max_ref'] is not None: used_ref[o['max_ref']] += 1
    row = [key[0], sh, key[1], key[2], k, u, w, o['dims'], status, o['D'], o['dp'], int(o['closed_trunc']),
           1.0 if o['closed_trunc'] else o.get('frac'), o['boxes'], o['certs'], o['n_itins'], o['max_ref'],
           o.get('replay_points', ''), o.get('replay_fail', ''), o['cpu_total'],
           (1.0 if d4[key]['closed_trunc'] else d4[key].get('frac')) if key in d4 else '']
    out.write('\t'.join(str(x) for x in row) + '\n')
print('rows', len(U), dict(st)); print('max reflections among certified itineraries, per pair', sorted(used_ref.items(), key=str))
print('cpu in these two runs', round(cpu, 1))
