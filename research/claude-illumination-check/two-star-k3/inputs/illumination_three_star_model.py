"""Frozen family builder for the three-exception extension.

Copied to preserve Claude's two-exception verification inputs. The sole logic
change is permitting budget3; existing formulas already parameterize it.
"""
import argparse
import json
import time
from collections import defaultdict
from pathlib import Path
from ortools.sat.python import cp_model
from illumination_geometry import label, owners_of, local_sectors, check
from illumination_family_bound import support, triangles_in_cells, counts

BASE = Path(__file__).parent


def build_model(target, max_walls=23, transparent_budget=0, bounded=None):
    assert transparent_budget in (0, 1, 2, 3)
    if bounded is None:
        bounded = support(target, max_walls-14+2*transparent_budget)
    interior_count = len(bounded['full'])
    ts = triangles_in_cells(bounded['allowed'])
    owners = owners_of(ts)
    incident = defaultdict(list)
    for i, t in enumerate(ts):
        for p in t:
            incident[p].append(i)
    model = cp_model.CpModel()
    x = [model.new_bool_var(f't{i}') for i in range(len(ts))]
    used, costs, charges, bads, defects = {}, {}, [], [], []
    defect_at = {}
    fulls = {(2*a, 2*b) for a, b in bounded['full']}
    for p, ids in sorted(incident.items()):
        kind = label(p)
        rows = []
        for mask in range(1 << len(ids)):
            bits = [(mask >> j) & 1 for j in range(len(ids))]
            chosen = [ts[i] for i, bit in zip(ids, bits) if bit]
            es = owners_of(chosen)
            opens = {e for e, o in es.items() if len(o) == 2}
            sizes, full = local_sectors(chosen, p, opens)
            if len(sizes) > 1:
                continue
            if kind == 'A' and full != (p in fulls):
                continue
            bad = int(kind != 'A' and (full or 4 in sizes))
            if bad and not transparent_budget:
                continue
            cost = sum(s != 4 for s in sizes)
            charge = 0 if kind != 'A' or full or not sizes else (3 if sizes[0] == 4 else sizes[0])
            defect = (2 if full else 1) if bad else 0
            rows.append(bits+[int(bool(chosen)), cost, charge, bad, defect])
        used[p] = model.new_bool_var(f'u{p}')
        costs[p] = model.new_bool_var(f'w{p}')
        charge = model.new_int_var(0, 7, f'charge{p}')
        bad = model.new_bool_var(f'bad{p}')
        defect = model.new_int_var(0, 2, f'defect{p}')
        model.add_allowed_assignments([x[i] for i in ids]+[used[p], costs[p], charge, bad, defect], rows)
        bads.append(bad)
        defects.append(defect)
        defect_at[p] = defect
        if kind == 'A':
            charges.append(charge)
    edge_used = []
    parents = [[] for _ in ts]
    max_tiles = 4*(max_walls-2+2*transparent_budget)//3
    rank = [model.new_int_var(0, max_tiles-1, f'rank{i}') for i in range(len(ts))]
    root = next(i for i, t in enumerate(ts) if (0, 0) in t)
    model.add(x[root] == 1)
    model.add(rank[root] == 0)
    for j, (e, os) in enumerate(owners.items()):
        u = model.new_bool_var(f'e{j}')
        model.add_max_equality(u, [x[i] for i in os])
        edge_used.append(u)
        if len(os) == 2:
            a, b = os
            for before, after in [(a, b), (b, a)]:
                parent = model.new_bool_var(f'p{before}_{after}')
                parents[after].append(parent)
                model.add(parent <= x[before])
                model.add(parent <= x[after])
                model.add(rank[after] >= rank[before]+1).only_enforce_if(parent)
    for i in range(len(ts)):
        model.add(sum(parents[i]) == (0 if i == root else x[i]))
    model.add(sum(used.values())-sum(edge_used)+sum(x) == 1)
    walls = sum(costs.values())
    model.add(walls <= max_walls)
    model.add(sum(bads) == transparent_budget)
    model.add(walls == 2+6*interior_count+sum(charges)-sum(defects))
    model.add(sum(x) <= max_tiles)
    # Connected cell graph: partial charges cover their incident graph degrees.
    model.add(sum(charges) >= 2*sum(used[p] for p in incident if label(p) == 'A')-4*interior_count-2)
    model.add(sum(used[p] for p in incident if label(p) == 'A') <= max_walls-2-5*interior_count+2*transparent_budget)
    # Every neighbor of either interior A is forced occupied by its C sector.
    if not transparent_budget:
        for a, b in bounded['mandatory']:
            model.add(used[2*a, 2*b] == 1)
    else:
        missing = sum(1-used[2*a, 2*b] for a, b in bounded['mandatory']-bounded['full'])
        model.add(missing <= transparent_budget)
        model.add(sum(charges) >= 2*sum(used[p] for p in incident if label(p) == 'A')-4*interior_count-2+missing)
        model.add(missing+sum(defects) <= 2*transparent_budget)
        model.add(sum(charges)+missing <= max_walls-2-6*interior_count+2*transparent_budget)
    return model, ts, x, bounded, dict(walls=walls, used=used, charges=charges,
                                     rank=rank, costs=costs, max_tiles=max_tiles,
                                     defects=defects, defect_at=defect_at)

