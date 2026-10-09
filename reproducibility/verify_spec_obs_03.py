#!/usr/bin/env python3
"""SPEC-OBS-03: exact isomorphism partitions for cyclic 3-support digraphs.

Standard library only; exact integer/combinatorial verification.
Run: python3 reproducibility/verify_spec_obs_03.py
Optional: python3 reproducibility/verify_spec_obs_03.py output.json
"""
from collections import defaultdict
from itertools import combinations
import json
import math
import sys

ORDERS = (8, 10, 12, 14, 15, 16, 18, 20)
EXPECTED = {
    8: (56, 19, 19, 19, 67, 0, 0),
    10: (120, 32, 32, 32, 172, 0, 0),
    12: (220, 71, 72, 72, 287, 16, 0),
    14: (364, 64, 64, 64, 884, 0, 0),
    15: (455, 65, 65, 65, 1479, 0, 0),
    16: (560, 85, 85, 85, 1783, 0, 0),
    18: (816, 147, 148, 148, 2008, 36, 0),
    20: (1140, 172, 172, 172, 3569, 0, 0),
}

def walks(n, S):
    a = [1] + [0] * (n-1)
    out = []
    for _ in range(n):
        b = [0] * n
        for i, x in enumerate(a):
            if x:
                for s in S:
                    b[(i+s) % n] += x
        a = b
        out.append(tuple(a))
    return out

def charpoly(w):
    n = len(w[0])
    s = [n * v[0] for v in w]
    c = [1]
    for k in range(1, n+1):
        t = sum(c[k-j] * s[j-1] for j in range(1, k+1))
        assert t % k == 0
        c.append(-t//k)
    return tuple(c)

def color_table(w):
    n = len(w[0])
    return tuple(tuple((w[k][d], w[k][(-d) % n])
                       for k in range(n)) for d in range(n))

def two_point_key(c):
    return tuple(sorted(c))

def multiplier_key(n, S):
    return min(tuple(sorted(u*s % n for s in S))
               for u in range(n) if math.gcd(u,n) == 1)

def iso_mapping(n, ca, cb):
    """Return an explicit isomorphism fixing vertex 0, or None.

    Any isomorphism can be post-composed with a translation of the target
    to fix 0. The k=1 walk color encodes directed adjacency, so any complete
    color-preserving permutation is an actual graph isomorphism.
    """
    if two_point_key(ca) != two_point_key(cb):
        return None
    dom = {i: tuple(j for j in range(n) if ca[i] == cb[j])
           for i in range(n)}
    if 0 not in dom[0]:
        return None
    mapped = {0: 0}
    used = {0}
    def recurse():
        if len(mapped) == n:
            return tuple(mapped[i] for i in range(n))
        node = None
        possible = None
        for i in range(1, n):
            if i in mapped:
                continue
            candidates = [j for j in dom[i] if j not in used and all(
                ca[(i-u) % n] == cb[(j-v) % n]
                for u,v in mapped.items())]
            if not candidates:
                return None
            if possible is None or len(candidates) < len(possible):
                node, possible = i, candidates
                if len(possible) == 1:
                    break
        for j in possible:
            mapped[node] = j
            used.add(j)
            result = recurse()
            if result is not None:
                return result
            used.remove(j)
            del mapped[node]
        return None
    return recurse()

def choose2(k):
    return k*(k-1)//2

def pair_count(groups):
    return sum(choose2(len(items)) for items in groups)

def scan(n):
    entries = {}
    spectral = defaultdict(list)
    fingerprints = defaultdict(list)
    multipliers = defaultdict(list)
    for S in combinations(range(n), 3):
        w = walks(n, S)
        p = charpoly(w)
        c = color_table(w)
        sig = two_point_key(c)
        entries[S] = (p, sig, c)
        spectral[p].append(S)
        fingerprints[(p,sig)].append(S)
        multipliers[multiplier_key(n,S)].append(S)
    assert all(len({entries[s][:2] for s in xs}) == 1
               for xs in multipliers.values())
    classes = []
    comparisons = 0
    nonaffine = []
    for _, members in fingerprints.items():
        orbit = defaultdict(list)
        for S in members:
            orbit[multiplier_key(n,S)].append(S)
        partition = []
        for xs in orbit.values():
            s = xs[0]
            destination = None
            for prior in partition:
                comparisons += 1
                permutation = iso_mapping(n, entries[s][2],
                                           entries[prior[0]][2])
                if permutation is not None:
                    destination = prior
                    # An explicit certificate for a non-multiplier isomorphism.
                    nonaffine.append({'S':list(s),'T':list(prior[0]),
                                      'vertex_permutation':list(permutation)})
                    break
            if destination is None:
                partition.append(list(xs))
            else:
                destination.extend(xs)
        classes.extend(partition)
    assert sum(map(len, classes)) == len(entries)
    spairs = pair_count(spectral.values())
    fpairs = pair_count(fingerprints.values())
    ipairs = pair_count(classes)
    assert spairs >= fpairs >= ipairs
    index = {S:i for i,cl in enumerate(classes) for S in cl}
    def restricted(key):
        d = defaultdict(list)
        for S in entries:
            if 0 not in S and math.gcd(n,*S) == 1:
                d[key(S)].append(S)
        return d
    subsp = restricted(lambda s:entries[s][0])
    subfp = restricted(lambda s:entries[s][:2])
    subiso = restricted(lambda s:index[s])
    result = {
        'n':n,
        'supports':len(entries),
        'spectral_classes':len(spectral),
        'two_point_classes':len(fingerprints),
        'exact_isomorphism_classes':len(classes),
        'unit_multiplier_classes':len(multipliers),
        'cospectral_support_pairs':spairs,
        'two_point_separated_pairs':spairs-fpairs,
        'isomorphic_support_pairs':ipairs,
        'cospectral_nonisomorphic_support_pairs':spairs-ipairs,
        'undistinguished_nonisomorphic_pairs':fpairs-ipairs,
        'nonmultiplier_isomorphism_comparisons':comparisons,
        'nonmultiplier_isomorphism_witnesses':nonaffine,
        'connected_loopless_subcorpus':{
            'supports':sum(len(g) for g in subsp.values()),
            'spectral_classes':len(subsp),
            'two_point_classes':len(subfp),
            'exact_isomorphism_classes':len(subiso),
            'cospectral_support_pairs':pair_count(subsp.values()),
            'two_point_separated_pairs':pair_count(subsp.values())-
                                       pair_count(subfp.values()),
            'undistinguished_nonisomorphic_pairs':pair_count(subfp.values())-
                                                  pair_count(subiso.values())
        }
    }
    observed = tuple(result[k] for k in (
        'supports','spectral_classes','two_point_classes',
        'exact_isomorphism_classes','cospectral_support_pairs',
        'two_point_separated_pairs','undistinguished_nonisomorphic_pairs'))
    assert observed == EXPECTED[n], (n, observed, EXPECTED[n])
    return result

def selftest():
    for n, S in [(8,(0,1,3)),(12,(1,3,9)),(18,(1,5,13))]:
        a = color_table(walks(n,S))
        for u in range(n):
            if math.gcd(u,n)==1:
                T = tuple(sorted(u*s%n for s in S))
                b = color_table(walks(n,T))
                permutation = iso_mapping(n,a,b)
                assert permutation is not None
                assert all(
                    {permutation[(i+s)%n] for s in S} ==
                    {(permutation[i]+t)%n for t in T}
                    for i in range(n))
    print('EXACT ISOMORPHISM SELFTEST PASS')

def main():
    selftest()
    rows = [scan(n) for n in ORDERS]
    for r in rows:
        print('n={n} supports={supports} spec={spectral_classes} '
              'two_point={two_point_classes} iso={exact_isomorphism_classes} '
              'noniso={cospectral_nonisomorphic_support_pairs} '
              'unresolved={undistinguished_nonisomorphic_pairs}'.format(**r))
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w', encoding='utf-8') as f:
            json.dump({'experiment':'SPEC-OBS-03','rows':rows}, f, indent=2)
            f.write('\n')
    print('SPEC-OBS-03 EXACT CHECK PASS')

if __name__ == '__main__':
    main()
