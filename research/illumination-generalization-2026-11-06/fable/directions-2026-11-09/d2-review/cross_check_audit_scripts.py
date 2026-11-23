"""Compare the audit's room_model.py with the reviewer's check_rooms.py.

Read-only import of the audit code (no bytecode is written). For every
strictly simple polyomino of area <= 8 and the hand rooms, in all four
origins, compare: corner permutations as sets of cycles, B_min, and the list
of block systems. Also count how often room_model.all_block_systems (single
pair closures only) misses a block system.
"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "../d2-factor-audit")
import room_model as RM          # audit code
import check_rooms as CR         # reviewer code

stats = {"cases": 0, "perm mismatch": 0, "bmin mismatch": 0,
         "cases where all_block_systems misses a system": 0, "systems missed": 0,
         "principal systems not in full list": 0}
rooms = [p for n, ps in CR.fixed_polyominoes(8).items() for p in ps if CR.strictly_simple(p)]
rooms += [frozenset(c) for c in CR.HAND.values()]
for cells in rooms:
    n = len(cells)
    for origin in ((0, 0), (1, 0), (0, 1), (1, 1)):
        order, idx, perms = CR.corner_perms(cells, origin)
        cl, idx2, lam, rho, the = RM.pillow_model(set(cells), origin)
        assert cl == order
        cp = RM.class_perms(lam, rho, the)
        stats["cases"] += 1
        for X in CR.CLASSES:
            mine = {frozenset(c) for c in CR.cycles(perms[X])}
            theirs = {frozenset(c) for c in CR.cycles(cp[X])}
            if mine != theirs:
                stats["perm mismatch"] += 1
            # same permutation up to inversion on the whole class
            if not (tuple(cp[X]) == perms[X] or tuple(RM.inv(cp[X])) == perms[X]):
                stats.setdefault("class perm differs beyond global inversion", 0)
                stats["class perm differs beyond global inversion"] += 1
        gens_theirs = (lam, rho, the)
        full_mine = CR.systems_join_closure(n, [perms[X] for X in CR.CLASSES])
        full_theirs_gens = CR.systems_join_closure(n, list(gens_theirs))
        assert full_mine == full_theirs_gens, "groups differ"
        seeds = [c for X in ("C1", "B", "C2") for c in CR.cycles(cp[X]) if len(c) == 2]
        b_theirs = frozenset(frozenset(b) for b in RM.closure_partition(n, gens_theirs, seeds))
        seeds2 = [c for X in ("C1", "B", "C2") for c in CR.cycles(perms[X]) if len(c) == 2]
        b_mine = CR.closure(n, [perms[X] for X in CR.CLASSES], seeds2)
        if b_theirs != b_mine:
            stats["bmin mismatch"] += 1
        principal = {frozenset(frozenset(b) for b in part) for part in RM.all_block_systems(n, gens_theirs)}
        if not principal <= full_mine:
            stats["principal systems not in full list"] += 1
        trivial = frozenset(frozenset([a]) for a in range(n))
        missed = full_mine - principal - {trivial}
        if missed:
            stats["cases where all_block_systems misses a system"] += 1
            stats["systems missed"] += len(missed)
for k, v in stats.items():
    print(f"{k}: {v}")
