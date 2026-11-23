"""Run the independent checker on every reported room (search-*.json best_room)."""
import json, glob
from check_room import check

BOUND = 30  # unfolded segment length, in lattice edge lengths
out = {}
for f in sorted(glob.glob('search-*.json')):
    r = json.load(open(f)).get('best_room')
    if not r or not r.get('T'): continue
    info = check(r, BOUND)
    out[f] = dict(search_walls=r['walls'], checker_walls=info['walls'], tiles=info['tiles'], S=r['S'], T=r['T'],
                  interior_A=info['interior_A'], C_tile_counts=info['C_tile_counts'], transparent_C=info['transparent_C'],
                  interior_B=info['interior_B'], flat_B=info['flat_B'], angle_histogram=info['angle_histogram'],
                  corners=info['corners'],
                  shots={k: {kk: vv for kk, vv in v.items() if kk != 'open'} for k, v in info['dark_tests'].items()},
                  verdict=info['verdict'], walls_agree=r['walls'] == info['walls'])
    print(f, out[f]['checker_walls'], out[f]['walls_agree'], out[f]['verdict'])
json.dump(out, open('check-results.json', 'w'), indent=1)
