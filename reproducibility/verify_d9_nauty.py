#!/usr/bin/env python3
"""Independent nauty replay of PR #6's D9 corpus. Never invokes VF2.

Usage: python3 reproducibility/verify_d9_nauty.py --out /tmp/d9-nauty
Optional: --vf2-partition archived.csv (columns support,class; support=1,2,9).
An archived aggregate count is NOT a full VF2 partition.
"""
import argparse
import ast
import csv
import hashlib
import io
import itertools
import json
import os
from pathlib import Path
import platform
import random
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict

SOURCE_COMMIT = '89d2709f03bc003b97ebb36765786935b97de0a3'
SOURCE_SHA256 = 'e8c1ca53872bf141241ea9ea2b9628184cdb66621704304b33fb340ae12e35aa'
SUMMARY_SHA256 = '798170f8941f03a6a7be36f6ca3c065d2ce1e7ac3ad2d2e478047e9092510993'
ROOT = Path(__file__).resolve().parent.parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode(a):
    """digraph6 (called direct6 in the correspondence), row-major n*n bits."""
    n = len(a)
    if not 0 < n < 63:
        raise ValueError('This encoder deliberately supports orders 1..62 only')
    bits = [int(x) for row in a for x in row]
    bits += [0] * (-len(bits) % 6)
    return '&' + chr(n + 63) + ''.join(
        chr(63 + sum(bits[i+j] << (5-j) for j in range(6)))
        for i in range(0, len(bits), 6))


def decode(line):
    if not line.startswith('&'):
        raise ValueError('Expected directed digraph6, never undirected graph6')
    n = ord(line[1]) - 63
    if not 0 < n < 63 or len(line) != 2 + (n*n+5)//6:
        raise ValueError('Invalid order or encoded length')
    bits = [(ord(c)-63) >> b & 1 for c in line[2:] for b in range(5, -1, -1)]
    return [bits[i*n:(i+1)*n] for i in range(n)]


def partition(labels):
    groups = defaultdict(list)
    for i, label in enumerate(labels):
        groups[label].append(i)
    return sorted(groups.values(), key=lambda g: g[0])


def compare_partitions(reference, candidate):
    """Class IDs/order are irrelevant. Return actual split/merge evidence."""
    if len(reference) != len(candidate):
        raise ValueError('Different corpus lengths')
    cells = Counter(zip(reference, candidate))
    splits = {str(r): sorted({str(c) for rr, c in cells if rr == r})
              for r in set(reference)}
    merges = {str(c): sorted({str(r) for r, cc in cells if cc == c})
              for c in set(candidate)}
    splits = {k: v for k, v in splits.items() if len(v) > 1}
    merges = {k: v for k, v in merges.items() if len(v) > 1}
    return {'equal': not splits and not merges, 'splits': splits, 'merges': merges,
            'contingency': [{'reference': str(r), 'nauty': str(c), 'count': n}
                            for (r, c), n in sorted(cells.items())]}


def read_reference(path, supports):
    rows = list(csv.DictReader(Path(path).open(newline='')))
    found = {}
    for row in rows:
        s = tuple(sorted(map(int, row['support'].split(','))))
        if len(s) != 3 or len(set(s)) != 3 or s in found:
            raise ValueError('Invalid or duplicate reference support')
        found[s] = row['class']
    if set(found) != set(supports):
        raise ValueError('VF2 reference must contain exactly the same 594 supports')
    return [found[s] for s in supports]


def reference_corpus():
    """Load only corpus definitions from the frozen script; no imports or main."""
    path = ROOT / 'reproducibility/verify_spec_obs_09.py'
    if digest(path) != SOURCE_SHA256:
        raise ValueError('Source changed: this replay targets the frozen PR #6 corpus')
    tree = ast.parse(path.read_text())
    names = {'M', 'N', 'EL', 'IDX', 'TABLE'}
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name in {
                 'prod', 'generating', 'matrix', 'canonical_motifs_4', 'histogram'})
             or (isinstance(node, ast.Assign) and any(
                 isinstance(t, ast.Name) and t.id in names for t in node.targets))]
    ns = {'permutations': itertools.permutations, 'defaultdict': defaultdict}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), ns)
    return ns


def shortg_partition(stderr, count):
    groups, current = [], None
    for line in stderr.splitlines():
        match = re.fullmatch(r'\s*(\d+)\s*:\s*([\d\s]+)', line)
        if match:
            current = [int(i)-1 for i in match[2].split()]
            groups.append(current)
        elif current is not None and re.fullmatch(r'\s+\d[\d\s]*', line):
            current.extend(int(i)-1 for i in line.split())
        else:
            current = None
    assert sorted(i for group in groups for i in group) == list(range(count))
    return sorted([sorted(g) for g in groups], key=lambda g: g[0])


def corpus():
    """Independent index formula; compare every support and matrix with PR #6."""
    def mul(i, j):
        a, b, c, d = i % 9, i // 9, j % 9, j // 9
        return (a + (c if b == 0 else -c)) % 9 + 9*((b+d) % 2)
    supports, matrices = [], []
    ref = reference_corpus()
    for s in itertools.combinations(range(1, 18), 3):
        seen, queue = {0}, [0]
        for u in queue:
            for x in s:
                v = mul(u, x)
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        generated = len(seen) == 18
        assert generated == ref['generating'](s)
        if generated:
            a = [[int(any(mul(u, x) == v for x in s)) for v in range(18)]
                 for u in range(18)]
            assert a == ref['matrix'](s)
            assert all(sum(row) == 3 and row[i] == 0 for i, row in enumerate(a))
            assert all(sum(a[u][v] for u in range(18)) == 3 for v in range(18))
            supports.append(s)
            matrices.append(a)
    assert len(supports) == 594
    return supports, matrices


def self_test():
    a = [[0, 1, 0], [0, 0, 1], [0, 0, 1]]
    assert decode(encode(a)) == a
    assert encode(a) != encode(list(map(list, zip(*a))))
    assert compare_partitions(['a', 'a', 'b'], ['2', '2', '1'])['equal']
    assert compare_partitions(['a', 'a', 'b'], ['1', '2', '3'])['splits']
    assert compare_partitions(['a', 'a', 'b'], ['1', '1', '1'])['merges']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--vf2-partition', type=Path)
    args = ap.parse_args()
    self_test()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    commands = []
    tools = {}
    for name in ('shortg', 'labelg', 'amtog', 'listg'):
        tools[name] = shutil.which('nauty-'+name) or shutil.which(name)
        if tools[name] is None:
            raise SystemExit('Missing executable: '+name)

    def run(name, flags, infile=None, outfile=None, tag=None):
        tag = tag or name
        argv = [tools[name], *flags]
        if infile is not None:
            argv.append(str(out / infile))
        if outfile is not None:
            argv.append(str(out / outfile))
        p = subprocess.run(argv, capture_output=True, text=True, check=False)
        (out / (tag+'.stdout')).write_text(p.stdout)
        (out / (tag+'.stderr')).write_text(p.stderr)
        commands.append({'argv': argv, 'returncode': p.returncode,
                         'stdout': tag+'.stdout', 'stderr': tag+'.stderr'})
        (out/'commands.json').write_text(json.dumps(commands, indent=2)+'\n')
        if p.returncode:
            raise RuntimeError(f'{argv!r}: {p.stderr}')
        return p.stdout

    for name in tools:
        run(name, ['--help'], tag=name+'-help')
        run(name, ['--version'], tag=name+'-version')
    # A digraph and its transpose need not be isomorphic. This unequal-degree
    # control catches accidental symmetrisation or suppression of directions.
    control = [[0, 1, 0], [0, 0, 1], [0, 0, 1]]
    transpose = [list(row) for row in zip(*control)]
    (out/'direction-control.d6').write_text(encode(control)+'\n'+encode(transpose)+'\n')
    run('shortg', ['-k'], 'direction-control.d6', 'direction-control-representatives.d6', 'shortg-direction-control')
    assert len((out/'direction-control-representatives.d6').read_text().splitlines()) == 2
    supports, matrices = corpus()
    lines = [encode(a) for a in matrices]
    for a, line in zip(matrices, lines):
        assert decode(line) == a
    (out/'corpus.d6').write_text('\n'.join(lines)+'\n')
    (out/'corpus.am').write_text('n=18\n'+''.join(
        'm\n'+'\n'.join(''.join(map(str, row)) for row in a)+'\n' for a in matrices))
    (out/'supports.json').write_text(json.dumps(supports, indent=2)+'\n')
    run('amtog', ['-z'], 'corpus.am', 'amtog.d6', 'amtog-corpus')
    assert (out/'amtog.d6').read_text().splitlines() == lines
    run('listg', ['-A'], 'corpus.d6', 'listg.am', 'listg-corpus')
    # listg -A emits spaced n*n entries; check each matrix, including arc direction.
    listed = (out/'listg.am').read_text()
    blocks = listed.split('Graph ')[1:]
    assert len(blocks) == 594
    for block, a in zip(blocks, matrices):
        rows = [row.strip() for row in block.splitlines()
                if len(row.strip().split()) == 18
                and all(x in ('0', '1') for x in row.strip().split())]
        assert [[int(x) for x in row.split()] for row in rows] == a

    # shortg executes McKay's suggested flags; -v records all class memberships.
    run('shortg', ['-fa', '-k', '-v'], 'corpus.d6', 'rooted-representatives.d6', 'shortg-rooted')
    run('shortg', ['-k', '-v'], 'corpus.d6', 'unrooted-representatives.d6', 'shortg-unrooted')
    run('labelg', ['-fa'], 'corpus.d6', 'rooted-canonical.d6', 'labelg-rooted')
    run('labelg', [], 'corpus.d6', 'unrooted-canonical.d6', 'labelg-unrooted')
    rooted = (out/'rooted-canonical.d6').read_text().splitlines()
    plain = (out/'unrooted-canonical.d6').read_text().splitlines()
    assert len(rooted) == len(plain) == 594
    assert partition(rooted) == partition(plain)
    parts = partition(plain)
    assert len(parts) == 12
    for name in ('rooted', 'unrooted'):
        representatives = (out/(name+'-representatives.d6')).read_text().splitlines()
        assert len(representatives) == 12 and set(representatives) <= set(lines)
        assert shortg_partition((out/('shortg-'+name+'.stderr')).read_text(), 594) == parts

    rng = random.Random(20261021)
    relabelled = []
    for a in matrices:
        p = list(range(18))
        rng.shuffle(p)
        relabelled.append(encode([[a[p[i]][p[j]] for j in range(18)] for i in range(18)]))
    (out/'relabelled.d6').write_text('\n'.join(relabelled)+'\n')
    run('labelg', ['-fa'], 'relabelled.d6', 'relabelled-canonical.d6', 'labelg-relabelled')
    assert (out/'relabelled-canonical.d6').read_text().splitlines() == rooted

    labels = [None]*594
    for c, members in enumerate(parts, 1):
        for i in members:
            labels[i] = f'N{c:02d}'
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(['support', 'class', 'input_line', 'canonical_sha256'])
    for i, (s, label, canonical) in enumerate(zip(supports, labels, plain), 1):
        writer.writerow([','.join(map(str, s)), label, i,
                         hashlib.sha256((canonical+'\n').encode()).hexdigest()])
    (out/'nauty_partition.csv').write_text(stream.getvalue())
    oldpath = ROOT/'reproducibility/results/spec_obs_09_D9_exact_summary.json'
    assert digest(oldpath) == SUMMARY_SHA256
    old = json.loads(oldpath.read_text())
    witnesses = []
    for pair in old['representatives']:
        indices = [supports.index(tuple(s)) for s in pair]
        assert labels[indices[0]] != labels[indices[1]]
        witnesses.append({'supports': pair, 'nauty_classes': [labels[i] for i in indices],
                          'distinct': True})
    # Rebuild only the old motif invariant; never the old VF2 classification.
    ref = reference_corpus()
    lookup, quads = ref['canonical_motifs_4'](), list(itertools.combinations(range(18), 4))
    histograms = [ref['histogram'](a, lookup, quads) for a in matrices]
    motif_parts = partition(histograms)
    motif_fibers = [{'representative': supports[g[0]], 'supports': len(g),
                     'nauty_classes': sorted({labels[i] for i in g})} for g in motif_parts]
    assert len(motif_parts) == 10
    assert sorted(len(f['nauty_classes']) for f in motif_fibers) == [1]*8 + [2]*2
    for group in parts:
        assert len({histograms[i] for i in group}) == 1
    for pair in old['representatives']:
        assert histograms[supports.index(tuple(pair[0]))] == histograms[supports.index(tuple(pair[1]))]
    (out/'motif_fibers.json').write_text(json.dumps(motif_fibers, indent=2)+'\n')
    full = {'status': 'UNAVAILABLE_ARCHIVED_VF2_MEMBERSHIPS',
            'reason': 'Frozen JSON stores aggregate counts and four witness supports only; no full partition. VF2 was not rerun.'}
    if args.vf2_partition:
        reference = read_reference(args.vf2_partition, supports)
        shutil.copyfile(args.vf2_partition, out/'vf2_reference.csv')
        full = {'status': 'COMPARED', **compare_partitions(reference, labels)}
    identities = {str(p.relative_to(ROOT)): digest(p) for p in
                  [ROOT/'reproducibility/verify_spec_obs_09.py', oldpath, Path(__file__)]}
    env = {'python': sys.version, 'platform': platform.platform(),
           'executables': {k: {'path': v, 'sha256': digest(v)} for k, v in tools.items()},
           'LD_LIBRARY_PATH': os.environ.get('LD_LIBRARY_PATH', ''),
           'networkx_used': False}
    (out/'environment.json').write_text(json.dumps(env, indent=2)+'\n')
    report = {'source_commit': SOURCE_COMMIT, 'source_files_sha256': identities,
              'graphs': 594, 'nauty_classes': 12,
              'class_sizes': [len(g) for g in parts],
              'vf2_archived_classes': old['isomorphism_classes'],
              'vf2_archived_checks': old['VF2_checks'],
              'vf2_rerun': False, 'aggregate_count_agrees': old['isomorphism_classes'] == len(parts),
              'motif_classes': len(motif_parts), 'motif_fibers_split_by_nauty': 2,
              'full_vf2_partition_comparison': full, 'archived_witnesses': witnesses,
              'checks': {'source_corpus_all_matrices_equal': True, 'amtog_byte_equality': True,
                         'listg_all_matrices_equal': True, 'rooted_unrooted_partitions_equal': True,
                         'all_594_relabellings_equal': True, 'shortg_keeps_original_labels': True,
                         'shortg_verbose_partitions_equal_labelg': True,
                         'asymmetric_direction_control_separated': True},
              'scope': 'Finite D9 computation only; not a general proof or global endorsement by McKay.'}
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    (out/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.name}\n' for p in sorted(out.iterdir())
                                       if p.is_file() and p.name != 'SHA256SUMS'))
    print(json.dumps(report, indent=2))
    if full.get('status') == 'COMPARED' and not full['equal']:
        raise SystemExit('VF2/nauty partition mismatch; see report.json')


if __name__ == '__main__':
    main()
