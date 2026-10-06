#!/usr/bin/env python3
"""Independent exact verification of the lattice formulation, Python stdlib.

This is a new verifier, not a recovered copy of lattice_exact.py,
criterion_check.py or pdiv_check.py. Every full-rank sublattice of index at
most the supplied bound is enumerated in column Hermite normal form.
Cospectrality is decided by integer power sums up to the matrix dimension;
the morphism criterion is evaluated independently on the lattice basis.
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path


def contains(a, b, d, w, r):
    """L = Z(a,0) + Z(b,d), a,d>0 and 0<=b<a."""
    return r % d == 0 and (w - b * (r // d)) % a == 0


def lattices(bound):
    for index in range(1, bound + 1):
        for a in range(1, index + 1):
            if index % a:
                continue
            d = index // a
            for b in range(a):
                if not contains(a, b, d, 1, -1):
                    yield a, b, d


def criterion(a, b, d, p):
    return [s for s in (1, 2) if a * s % p == 0 and (b * s + d) % p == 0]


def AB(a, b, d):
    sign = a % 2 == 0 and (b + d) % 2 == 0
    swap = contains(a, b, d, 0, a) and contains(a, b, d, d, b)
    return sign and swap


def scan(p, bound):
    maximum = p * bound
    choose = [tuple(math.comb(n, w) for w in range(n + 1)) for n in range(maximum + 1)]
    residue = [[1] + [0] * (p - 1)]
    for w in range(1, maximum + 1):
        prev = residue[-1]
        residue.append([prev[r] + prev[(r - 1) % p] for r in range(p)])
    # The following coefficients depend on n,w,p, never on the criterion.
    delta = [tuple(choose[n][w] * (residue[w][0] - residue[w][(-n) % p])
                   for w in range(n + 1)) for n in range(maximum + 1)]
    rows = []
    for a, b, d in lattices(bound):
        dimension = p * a * d
        first = None
        first_delta = None
        for n in range(1, dimension + 1):
            value = sum(delta[n][w] for w in range(n % d, n + 1, d)
                        if (w - b * ((n - w) // d)) % a == 0)
            if value:
                first, first_delta = n, value
                break
        h = criterion(a, b, d, p)
        rows.append({'HNF_columns': [[a, 0], [b, d]], 'index': a*d,
                     'dimension': dimension, 'cospectral': first is None,
                     'criterion_values': h, 'C3_AB': AB(a,b,d) if p == 3 else None,
                     'power_sums_checked': dimension if first is None else first,
                     'first_different_power': first,
                     'difference_of_returns_per_vertex': first_delta})
    exceptions = [r for r in rows if r['cospectral'] and not r['criterion_values']]
    summary = {'p': p, 'index_bound': bound, 'lattices_distinct_generators': len(rows),
               'cospectral': sum(r['cospectral'] for r in rows),
               'criterion': sum(bool(r['criterion_values']) for r in rows),
               'cospectral_outside_criterion': len(exceptions),
               'exceptions_divisible_by_p': sum(r['index'] % p == 0 for r in exceptions),
               'exceptions_satisfying_AB': sum(bool(r['C3_AB']) for r in exceptions),
               'exception_index_counts': dict(sorted(Counter(r['index'] for r in exceptions).items()))}
    assert all(r['cospectral'] for r in rows if r['criterion_values'])
    if p >= 5:
        assert not exceptions, summary
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return {'summary': summary, 'rows': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='lattice_independent_results.json')
    parser.add_argument('--p', type=int)
    parser.add_argument('--bound', type=int)
    args = parser.parse_args()
    if (args.p is None) != (args.bound is None):
        parser.error('--p and --bound must be supplied together')
    cases = [(args.p,args.bound)] if args.p is not None else [(5,60),(7,56),(11,24),(3,48)]
    result = {'method': 'Column HNF enumeration and exact integer Newton power sums; no floating point.',
              'origin': 'New independent verifier written for the complete consolidated report.',
              'convention': 'Ordered marked generators are images of e1,e2; e1 != e2; no quotient by group automorphisms.',
              'runs': [scan(p,bound) for p,bound in cases]}
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
