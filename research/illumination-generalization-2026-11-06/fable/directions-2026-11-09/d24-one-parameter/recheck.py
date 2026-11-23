"""Re-test survivors of search.py with a larger radius. Usage: recheck.py FILE R [max]"""
import sys, re, ast, collections
import search as s
R = int(sys.argv[2]); mx = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
rooms = collections.OrderedDict()
for l in open(sys.argv[1]):
    if not l.startswith('SURVIVOR'): continue
    cells = l[l.index('['):l.index(']') + 1]
    rest = l[l.index(']') + 1:]
    lab, S, T = [ast.literal_eval(x) for x in re.findall(r'\([^)]*\)', rest)]
    rooms.setdefault(cells, []).append((lab, S, T))
print("rooms with survivors", len(rooms), "survivors", sum(map(len, rooms.values())))
left = n = 0
for cells, lst in rooms.items():
    cs = set(ast.literal_eval(cells)); dark = []
    for lab, S, T in lst:
        if n >= mx: break
        n += 1
        if s.lit(cs, S, T, 202, R) is None: dark.append((lab, S, T))
    if dark:
        left += len(dark); print("STILL", cells, len(dark), "of", len(lst), dark[:3], flush=True)
print("tested", n, "still unlit at R =", R, ":", left)
