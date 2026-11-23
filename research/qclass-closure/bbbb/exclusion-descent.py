"""Reconstruct the one named pillowcase quotient. No path or direction enumeration."""
from pathlib import Path
import sys

archive = Path(__file__).resolve().parents[2] / 'illumination-generalization-2026-11-06/fable/directions-2026-11-09'
sys.path.insert(0, str(archive / 'd10-mechanisms'))
import roomtools as rt

columns = [range(6), (2,3), (2,3), range(6), range(6), (2,3), (2,), range(3)]
cells = {(x,y) for x,col in enumerate(columns) for y in col}
source, target = (2,3), (4,3)
room, monodromy = rt.room_tuple(cells, source)
partitions = rt.d4.all_block_systems(monodromy, 28)
assert sorted(map(len, partitions)) == [1,4,28]
blocks = next(p for p in partitions if len(p)==4)
gens = [rt.induced(g, blocks) for g in monodromy]
assert gens == [(1,0,2,3), (1,0,3,2), (0,2,3,1), (0,2,1,3)]
where = {x:i for i,block in enumerate(blocks) for x in block}
for mark,expected in [(source,3),(target,2)]:
    lifts = rt.lifts(room, monodromy, mark, source)
    assert len(lifts)==2 and all({where[x] for x in lift}=={expected} for lift in lifts)
    print(mark,'projects to letter',expected)
print('quotient degrees',sorted(map(len,partitions)),
      'canonical degrees',[len(rt.class_congruence(monodromy,[i])) for i in range(4)])
for site,g in zip('abcd',gens):
    print(site,rt.cycles(g))
