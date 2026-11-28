"""Control: marks found by fp.marks_of reproduce the census pair counts."""
import fp, multiprocessing as mp
def cnt(args):
    l, skip = args; f = l.split(); v = list(map(int, f[skip:])); cells = [v[k:k + 6] for k in range(0, len(v), 6)]
    m = len(fp.marks_of(cells)); return m * (m - 1) // 2
if __name__ == '__main__':
    for path, skip, want in (('../d237-dark-examples-w22-26/astra/production/jobs.txt', 3, 1015031), ('../d236-immersed-disc-control/astra/production/jobs.txt', 1, 857156)):
        with mp.Pool(12) as pool, open(path) as fh:
            tot = sum(pool.imap_unordered(cnt, ((l, skip) for l in fh if l.strip()), chunksize=5000))
        print(path.split('/')[1], 'pairs', tot, 'census figure', want, 'match', tot == want)
