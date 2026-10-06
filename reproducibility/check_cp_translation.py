#!/usr/bin/env python3
"""Exact audit of T={(a,0),(a,1),(b,0)} and T+(0,1) in K x C_p.

Python standard library only. Spectra retain full tuples of integer
coefficients modulo Phi_lcm(exp(K),p), including multiplicities. No floating
point comparisons and no hash-only identifiers. All ordered a != b are tested,
including pairs that do not generate K; those are counted separately.
"""
import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def divide_monic(a, b):
    a = list(a)
    q = [0] * max(1, len(a) - len(b) + 1)
    for k in range(len(a) - len(b), -1, -1):
        q[k] = a[k + len(b) - 1]
        for j, v in enumerate(b):
            a[k + j] -= q[k] * v
    assert not any(a), (a, b)
    return tuple(trim(q))


@lru_cache(None)
def cyclotomic(n):
    a = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            a = divide_monic(a, cyclotomic(d))
    return tuple(a)


@lru_cache(None)
def roots(n):
    phi = cyclotomic(n)
    degree = len(phi) - 1
    r = [1] + [0] * (degree - 1)
    out = []
    for _ in range(n):
        out.append(tuple(r))
        top = r[-1]
        r = [0] + r[:-1]
        for j in range(degree):
            r[j] -= top * phi[j]
    assert r == list(out[0])
    return tuple(out)


def refine_iso(a, b):
    """Complete directed joint refinement/backtracking, rooting vertex zero.

    Rooting is sufficient for these Cayley graphs by vertex transitivity.
    Positive answers always include a directly verified vertex bijection.
    """
    n = len(a)
    pa = tuple(frozenset(v for v in range(n) if u in a[v]) for u in range(n))
    pb = tuple(frozenset(v for v in range(n) if u in b[v]) for u in range(n))

    def search(ca, cb):
        while True:
            sa = [(ca[u], tuple(sorted(ca[v] for v in a[u])),
                   tuple(sorted(ca[v] for v in pa[u]))) for u in range(n)]
            sb = [(cb[u], tuple(sorted(cb[v] for v in b[u])),
                   tuple(sorted(cb[v] for v in pb[u]))) for u in range(n)]
            labels = {s: i for i, s in enumerate(sorted(set(sa + sb)))}
            na, nb = tuple(labels[s] for s in sa), tuple(labels[s] for s in sb)
            if Counter(na) != Counter(nb):
                return None
            done = len(set(na + nb)) == len(set(ca + cb))
            ca, cb = na, nb
            if done:
                break
        classes = defaultdict(list)
        for u, c in enumerate(ca):
            classes[c].append(u)
        if len(classes) == n:
            rev = {c: v for v, c in enumerate(cb)}
            mapping = tuple(rev[c] for c in ca)
            assert len(set(mapping)) == n
            assert all({mapping[v] for v in a[u]} == set(b[mapping[u]])
                       for u in range(n))
            return mapping
        color = min((c for c in classes if len(classes[c]) > 1),
                    key=lambda c: (len(classes[c]), c))
        u = classes[color][0]
        new_color = max(ca + cb) + 1
        for v in range(n):
            if cb[v] == color:
                na, nb = list(ca), list(cb)
                na[u] = nb[v] = new_color
                result = search(tuple(na), tuple(nb))
                if result is not None:
                    return result
        return None

    initial = tuple(1 if u == 0 else 0 for u in range(n))
    return search(initial, initial)


class Audit:
    def __init__(self, mods, p):
        self.mods, self.p = tuple(mods), p
        self.k = list(itertools.product(*(range(m) for m in mods)))
        self.coords = [v + (j,) for v in self.k for j in range(p)]
        self.index = {v: i for i, v in enumerate(self.coords)}
        self.exp = math.lcm(*mods)
        self.conductor = math.lcm(self.exp, p)
        self.root = roots(self.conductor)
        self.dim = len(self.root[0])
        self.phases = {v: [sum(c * x * (self.exp // m)
                               for c, x, m in zip(chi, v, mods)) % self.exp
                           for chi in self.k] for v in self.k}
        self.sums = {}

    def value(self, a, b, c):
        key = tuple(sorted((a, b, c)))
        if key not in self.sums:
            self.sums[key] = tuple(self.root[a][d] + self.root[b][d]
                                  + self.root[c][d] for d in range(self.dim))
        return self.sums[key]

    def conditions(self, a, b):
        gamma = set(zip(self.phases[a], self.phases[b]))
        cond_a = self.exp % 2 == 0 and (self.exp // 2, self.exp // 2) in gamma
        cond_b = {(v, u) for u, v in gamma} == gamma
        return cond_a, cond_b

    def generates(self, a, b):
        found = {(0,) * len(self.mods)}
        todo = list(found)
        while todo:
            x = todo.pop()
            for t in (a, b):
                y = tuple((i + j) % m for i, j, m in zip(x, t, self.mods))
                if y not in found:
                    found.add(y)
                    todo.append(y)
        return len(found) == len(self.k)

    def spectra(self, a, b):
        first, shifted = [], []
        unit = self.conductor // self.p
        factor = self.conductor // self.exp
        for qa, qb in zip(self.phases[a], self.phases[b]):
            u, v = qa * factor, qb * factor
            for j in range(self.p):
                w = unit * j
                first.append(self.value(u, (u + w) % self.conductor, v))
                shifted.append(self.value((u + w) % self.conductor,
                                          (u + 2 * w) % self.conductor,
                                          (v + w) % self.conductor))
        return tuple(sorted(first)), tuple(sorted(shifted))

    def graph(self, a, b, shift):
        steps = (a + (shift % self.p,), a + ((shift + 1) % self.p,),
                 b + (shift % self.p,))
        mods = self.mods + (self.p,)
        return tuple(frozenset(self.index[tuple((i + j) % m
                                              for i, j, m in zip(x, t, mods))]
                               for t in steps) for x in self.coords)

    def noniso_profile(self, a, b):
        """Return-walk profiles are graph invariants on vertex-transitive graphs."""
        aa, bb = self.graph(a, b, 0), self.graph(a, b, 1)
        n = len(aa)
        ra, rb = Counter({0: 1}), Counter({0: 1})
        inv = [self.index[tuple(-v % m for v, m in zip(x, self.mods + (self.p,)))]
               for x in self.coords]
        for length in range(1, n):
            qa, qb = Counter(), Counter()
            for x, count in ra.items():
                for y in aa[x]:
                    qa[y] += count
            for x, count in rb.items():
                for y in bb[x]:
                    qb[y] += count
            ra, rb = qa, qb
            va = sorted(ra[inv[v]] for v in aa[0])
            vb = sorted(rb[inv[v]] for v in bb[0])
            if va != vb:
                return {'length': length, 'profile_T': va, 'profile_shift': vb}
        return None

    def walk_trace_check(self, a, b):
        """Independent integer trace comparison, through the group order."""
        rows = []
        n = len(self.coords)
        for shift in (0, 1):
            adj = self.graph(a, b, shift)
            counts = Counter({0: 1})
            traces = []
            for _ in range(n):
                nxt = Counter()
                for x, count in counts.items():
                    for y in adj[x]:
                        nxt[y] += count
                counts = nxt
                traces.append(n * counts[0])
            rows.append(traces)
        sa, sb = self.spectra(a, b)
        assert (rows[0] == rows[1]) == (sa == sb)
        first_diff = next((i + 1 for i, (x, y) in enumerate(zip(*rows)) if x != y), None)
        return {'first_different_trace_power': first_diff}

    def run(self):
        row = {'K_factors': self.mods, 'K_order': len(self.k), 'K_exponent': self.exp,
               'p': self.p, 'cyclotomic_conductor': self.conductor,
               'pairs_ordered_distinct': 0, 'pairs_generating_K': 0,
               'AB_instances': 0, 'AB_generating_instances': 0,
               'cospectral_pairs': 0, 'cospectral_generating_pairs': 0,
               'nonisomorphic_generating_pairs': 0, 'isomorphic_generating_pairs': 0,
               'eigenvalue_obstruction_cases_checked': 0,
               'cospectral_generating_details': []}
        witness = self.value(0, 0, self.conductor // self.p)
        first_pair = None
        for a, b in itertools.permutations(self.k, 2):
            row['pairs_ordered_distinct'] += 1
            gen = self.generates(a, b)
            row['pairs_generating_K'] += gen
            cond_a, cond_b = self.conditions(a, b)
            ab = cond_a and cond_b
            row['AB_instances'] += ab
            row['AB_generating_instances'] += ab and gen
            sa, sb = self.spectra(a, b)
            cospectral = sa == sb
            row['cospectral_pairs'] += cospectral
            row['cospectral_generating_pairs'] += cospectral and gen
            if first_pair is None:
                first_pair = (a, b)
            if self.p == 3 and ab:
                assert cospectral, (self.mods, a, b)
            if self.p >= 5 and self.exp % self.p:
                assert witness in sa and witness not in sb
                assert not cospectral
                row['eigenvalue_obstruction_cases_checked'] += 1
            if cospectral and gen:
                profile = self.noniso_profile(a, b)
                detail = {'kappa': a, 'kappa_prime': b, 'A': cond_a, 'B': cond_b}
                if profile is not None:
                    detail['nonisomorphism_certificate'] = profile
                    row['nonisomorphic_generating_pairs'] += 1
                else:
                    mapping = refine_iso(self.graph(a, b, 0), self.graph(a, b, 1))
                    if mapping is None:
                        detail['nonisomorphism_certificate'] = 'complete rooted backtracking'
                        row['nonisomorphic_generating_pairs'] += 1
                    else:
                        detail['vertex_bijection'] = mapping
                        row['isomorphic_generating_pairs'] += 1
                row['cospectral_generating_details'].append(detail)
        if first_pair is not None:
            row['independent_integer_trace_control'] = self.walk_trace_check(*first_pair)
        print('K=' + 'x'.join(map(str, self.mods)), 'p=', self.p,
              'AB=', row['AB_instances'], 'AB-gen=', row['AB_generating_instances'],
              'cospectral-gen=', row['cospectral_generating_pairs'],
              'noniso-gen=', row['nonisomorphic_generating_pairs'], flush=True)
        return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='cp_translation_results.json')
    args = parser.parse_args()
    assert cyclotomic(3) == (1, 1, 1)
    assert cyclotomic(6) == (1, -1, 1)
    assert cyclotomic(12) == (1, 0, -1, 0, 1)
    groups = [(2,), (4,), (2, 2), (6,), (8,), (2, 4), (10,), (12,),
              (16,), (3,), (5,)]
    primes = (3, 5, 7, 11)
    rows = [Audit(mods, p).run() for mods in groups for p in primes]
    controls = {tuple(r['K_factors']): r['AB_instances'] for r in rows if r['p'] == 3}
    assert [controls[(n,)] for n in (4, 8, 10, 16)] == [2, 14, 4, 38]
    # A,B do not imply non-isomorphism when K has a 3-primary component.
    g = Audit((6,), 3)
    a, b = (1,), (5,)
    assert g.conditions(a, b) == (True, True)
    source, target = g.graph(a, b, 0), g.graph(a, b, 1)
    mapping = tuple(g.index[(u, (2 * (u % 3) + 2 * v) % 3)] for u, v in g.coords)
    assert len(set(mapping)) == len(source)
    assert all({mapping[v] for v in source[u]} == target[mapping[u]]
               for u in range(len(source)))
    # The coprimality hypothesis in the negative theorem is essential.
    # On C_p x C_p, kappa=1, kappa'=1/2 gives an explicit isomorphism.
    for p in primes:
        q = Audit((p,), p)
        source, target = q.graph((1,), (pow(2, -1, p),), 0), q.graph((1,), (pow(2, -1, p),), 1)
        f = tuple(q.index[(u, (2 * u - v) % p)] for u, v in q.coords)
        assert len(set(f)) == len(source)
        assert all({f[v] for v in source[u]} == target[f[u]] for u in range(len(source)))
        assert q.spectra((1,), (pow(2, -1, p),))[0] == q.spectra((1,), (pow(2, -1, p),))[1]
    # Match the user's first residue witness with the abstract C3 family.
    alpha, beta, c = 169, 181, 151
    coord = {(pow(alpha, u, 210) * pow(beta, v, 210) * pow(c, w, 210)) % 210: (u, v, w)
             for u in range(2) for v in range(2) for w in range(3)}
    assert len(coord) == 12
    first = {beta, beta * c % 210, alpha}
    assert first == {31, 181, 169}
    translated = {t * c % 210 for t in first}
    shear = {r: (pow(alpha, u, 210) * pow(beta, (v + u) % 2, 210) * pow(c, w, 210)) % 210
             for r, (u, v, w) in coord.items()}
    assert {shear[r] for r in translated} == {31, 61, 199}
    summary = {'rows': len(rows), 'ordered_parameter_cases': sum(r['pairs_ordered_distinct'] for r in rows),
               'negative_eigenvalue_cases': sum(r['eigenvalue_obstruction_cases_checked'] for r in rows),
               'C3_AB_cases': sum(r['AB_instances'] for r in rows if r['p'] == 3)}
    result = {'scope': 'Only the explicit family T={(kappa,0),(kappa,1),(kappa_prime,0)}; '
                       'not a census of all triplets or all translates.',
              'status': 'Exact finite verification; general statements require the accompanying written proof. '
                        'No Lean formalization or novelty claim.', 'summary': summary,
              'explicit_isomorphic_AB_case': {
                  'K_factors': [6], 'p': 3, 'kappa': [1], 'kappa_prime': [5],
                  'automorphism': '(u,v) -> (u, 2*(u mod 3)+2*v mod 3)',
                  'vertex_bijection': mapping},
              'explicit_Cp_primary_isomorphisms_checked': list(primes),
              'first_exception_coordinates': {'alpha': alpha, 'beta': beta, 'c': c,
                  'translated_T1': sorted(translated),
                  'group_automorphism': '(u,v,w) -> (u,v+u mod 2,w)',
                  'images': [[r, shear[r]] for r in sorted(translated)]}, 'rows': rows}
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
