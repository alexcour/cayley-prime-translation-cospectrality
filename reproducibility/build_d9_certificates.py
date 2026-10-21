#!/usr/bin/env python3
"""Build finite D9 certificates using 54 explicit group automorphisms, no GI.

The source corpus and original nauty CSV are read; no nauty/VF2 is run.
The separate check_d9_certificates.py does not import this producer.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import platform
import sys

import verify_d9_nauty as source

ROOT = Path(__file__).resolve().parent.parent
UNITS = (1, 2, 4, 5, 7, 8)


def image(x, u, v):
    return (u*(x % 9) + v*(x // 9)) % 9 + 9*(x // 9)


def traces_by_convolution(support, table):
    w, traces = [1]+[0]*17, []
    for _ in range(18):
        nxt = [0]*18
        for i, value in enumerate(w):
            for s in support:
                nxt[table[i][s]] += value
        w = nxt
        traces.append(18*w[0])
    return traces


def characteristic_from_traces(traces):
    c = [1]
    for k in range(1, 19):
        numerator = sum(c[k-j]*traces[j-1] for j in range(1, k+1))
        assert numerator % k == 0
        c.append(-numerator//k)
    return c


def motif_lookup():
    edges = [(i,j) for i in range(4) for j in range(4) if i != j]
    index = {e:i for i,e in enumerate(edges)}
    transforms = [[index[p[i],p[j]] for i,j in edges]
                  for p in permutations(range(4))]
    lookup = [min(sum(((mask >> j) & 1) << i for i,j in enumerate(t))
                  for t in transforms) for mask in range(4096)]
    return edges, lookup


def motifs(matrix, lookup):
    edges, canonical = lookup
    counts = Counter(canonical[sum(matrix[q[i]][q[j]] << b
                                  for b,(i,j) in enumerate(edges))]
                     for q in combinations(range(18),4))
    return [[k,v] for k,v in sorted(counts.items())]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    supports, matrices = source.corpus()
    ref = source.reference_corpus()
    old_csv = ROOT/'reproducibility/results/d9_nauty_20261021/nauty_partition.csv'
    archived = source.read_reference(old_csv, supports)
    members, by_rep = [], defaultdict(list)
    for s in supports:
        targets = [(tuple(sorted(image(x,u,v) for x in s)),u,v)
                   for u in UNITS for v in range(9)]
        representative,u,v = min(targets)
        row = {'support': list(s), 'representative': list(representative),
               'automorphism': {'u':u,'v':v},
               'vertex_image': [image(x,u,v) for x in range(18)]}
        members.append(row)
        by_rep[representative].append(row)
    reps = sorted(by_rep)
    assert len(reps) == 12
    lookup, classes = motif_lookup(), []
    for i, rep in enumerate(reps, 1):
        label = f'N{i:02d}'
        for row in by_rep[rep]:
            row['class'] = label
        traces = traces_by_convolution(rep, ref['TABLE'])
        classes.append({'class': label, 'representative': list(rep),
                        'size': len(by_rep[rep]), 'traces_1_to_18': traces,
                        'charpoly_descending': characteristic_from_traces(traces),
                        'motif4': motifs(matrices[supports.index(rep)], lookup)})
    labels = [row['class'] for row in members]
    agreement = source.compare_partitions(archived, labels)
    assert agreement['equal']
    witnesses = []
    for a,b in combinations(classes,2):
        k = next(i for i,(x,y) in enumerate(zip(a['traces_1_to_18'],b['traces_1_to_18']),1) if x != y)
        witnesses.append({'left':a['class'], 'right':b['class'], 'trace_power':k,
                          'values':[a['traces_1_to_18'][k-1],b['traces_1_to_18'][k-1]]})
    first_h = next(h for h in range(1,19) if len({tuple(c['traces_1_to_18'][:h]) for c in classes}) == 12)
    summary = {'graphs':len(members), 'classes':len(classes),
               'class_sizes':[c['size'] for c in classes],
               'spectral_classes':len({tuple(c['charpoly_descending']) for c in classes}),
               'motif4_classes':len({tuple(map(tuple,c['motif4'])) for c in classes}),
               'joint_spectrum_motif4_classes':len({(tuple(c['charpoly_descending']),tuple(map(tuple,c['motif4']))) for c in classes}),
               'trace6_trace9_classes':len({(c['traces_1_to_18'][5],c['traces_1_to_18'][8]) for c in classes}),
               'first_complete_trace_prefix_horizon':first_h,
               'nauty_membership_partition_agreement':agreement['equal'],
               'vf2_rerun':False,
               'historical_vf2_membership_equality':'NOT_ESTABLISHED_MISSING_ARCHIVE',
               'scope':'Generating identity-free 3-subsets of D9 only; no spectral determination among arbitrary digraphs or other orders.'}
    assert (summary['spectral_classes'],summary['motif4_classes'],summary['trace6_trace9_classes'],first_h)==(12,10,12,9)
    certificate = {'schema':'d9-explicit-certificate-v1',
                   'corpus_source_commit':source.SOURCE_COMMIT,
                   'nauty_archive_commit':'dc569782920bfec007a304e542b9c3a00f363960',
                   'classes':classes, 'members':members,
                   'pair_separation':witnesses, 'summary':summary}
    (out/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    with (out/'representatives.csv').open('w',newline='') as f:
        w = csv.writer(f,lineterminator='\n')
        w.writerow(['class','support','size','trace6','trace9','root_closed_walks6','root_closed_walks9'])
        for c in classes:
            t=c['traces_1_to_18']
            w.writerow([c['class'],','.join(map(str,c['representative'])),c['size'],t[5],t[8],t[5]//18,t[8]//18])
    sources = [Path(__file__),ROOT/'reproducibility/check_d9_certificates.py',
               ROOT/'reproducibility/verify_d9_nauty.py',
               ROOT/'reproducibility/verify_spec_obs_09.py',old_csv]
    provenance = {'python':sys.version,'platform':platform.platform(),
                  'build_argv':sys.argv,'cwd':str(Path.cwd()),
                  'source_sha256':{str(p.relative_to(ROOT)):source.digest(p) for p in sources},
                  'methods':{'isomorphism_search':'none; enumerate 54 explicit automorphisms',
                             'trace_producer':'group convolution',
                             'characteristic_producer':'integer Newton identities',
                             'checker':'separate stdlib script; matrix traces and 19 Bareiss determinants per representative'},
                  'trace6_trace9_choice':'exploratory post-hoc choice after inspecting D9; not preregistered or asserted minimal among arbitrary observables'}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    (out/'SHA256SUMS').write_text(''.join(f'{source.digest(p)}  {p.name}\n' for p in sorted(out.iterdir())
                                       if p.is_file() and p.name!='SHA256SUMS'))
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
