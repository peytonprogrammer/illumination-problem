"""Load enum_K.c output as canonical forms (tuple of 4 tuples), same format as d52 canon()."""


def load_txt(path):
    out = []
    for line in open(path):
        d, rest = line.split('|')
        rows = [tuple(int(v) for v in r.split()) for r in rest.split(';')]
        assert len(rows) == 4 and all(len(r) == int(d) for r in rows)
        out.append(tuple(rows))
    return out
