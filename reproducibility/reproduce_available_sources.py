#!/usr/bin/env python3
"""NEW reproduction driver, 2026-10-04. Not a recovered mixed or audit script.

Reuses the exact cyclotomic encoder from the archived check_cp_translation.py.
It is therefore not an independent implementation of that spectral encoder.
"""
import argparse
import importlib.util
import itertools
import json
import platform
from pathlib import Path


def subgroup_h(g, a, b):
    zero = (0,) * len(g.mods)
    for s in (1, 2):
        values, todo = {zero: 0}, [zero]
        valid = True
        while todo and valid:
            x = todo.pop()
            for t, value in ((a, s), (b, 1)):
                y = tuple((u + v) % m for u, v, m in zip(x, t, g.mods))
                hy = (values[x] + value) % g.p
                if y in values:
                    if values[y] != hy:
                        valid = False
                        break
                else:
                    values[y] = hy
                    todo.append(y)
        if valid:
            return s, values
    return None


def mapping_on_cosets(g, witness):
    s, h = witness
    image = {}
    for rep in g.k:
        if rep in image:
            continue
        for u, value in h.items():
            x = tuple((r + v) % m for r, v, m in zip(rep, u, g.mods))
            image[x] = value
    return [g.index[x + ((y + image[x]) % g.p if s == 1
                         else (image[x] - y) % g.p,)]
            for x, y in ((e[:-1], e[-1]) for e in g.coords)]


def scan(cp, p, mods, expected_total, expected_cos, primitive, certificates):
    g = cp.Audit(mods, p)
    rows, mappings = [], []
    for a, b in itertools.permutations(g.k, 2):
        generated = g.generates(a, b)
        if primitive and not generated:
            continue
        left, right = g.spectra(a, b)
        cos = left == right
        witness = subgroup_h(g, a, b)
        assert cos == (witness is not None), (mods, p, a, b)
        row = {'kappa': a, 'kappa_prime': b, 'generates_K': generated,
               'cospectral': cos, 'h_on_generated_subgroup': witness is not None}
        if certificates and cos:
            mapping = mapping_on_cosets(g, witness)
            source, target = g.graph(a, b, 0), g.graph(a, b, 1)
            assert len(set(mapping)) == len(mapping)
            assert all({mapping[v] for v in source[u]} == set(target[mapping[u]])
                       for u in range(len(mapping)))
            row['certificate_index'] = len(mappings)
            mappings.append({'kappa': a, 'kappa_prime': b,
                             'vertex_order': 'lexicographic K coordinates, last C_p coordinate fastest',
                             'h_kappa': witness[0], 'h_values': sorted(witness[1].items()),
                             'vertex_bijection': mapping, 'all_arcs_verified': True})
        rows.append(row)
    count = sum(row['cospectral'] for row in rows)
    assert (len(rows), count) == (expected_total, expected_cos)
    return {'p': p, 'K_factors': mods, 'primitive_only': primitive,
            'tested': len(rows), 'cospectral': count, 'discrepancies': 0,
            'rows': rows, 'isomorphism_certificates': mappings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--mode', choices=('mixed', '416'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('archived_cp', args.source)
    cp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cp)
    cases = ([(5,(5,2),68,20), (5,(5,3),184,56), (5,(5,4),280,88),
              (5,(5,6),568,184), (7,(7,2),138,30), (7,(7,3),372,84),
              (7,(7,4),564,132), (5,(25,2),1780,580),
              (5,(5,2,2),144,48), (5,(5,2,4),576,192)]
             if args.mode == 'mixed' else
             [(5,(10,),90,24), (5,(15,),210,60), (5,(20,),380,112),
              (5,(25,),600,184), (7,(14,),182,36)])
    runs = [scan(cp, p, mods, total, cos, args.mode == 'mixed', args.mode == '416')
            for p, mods, total, cos in cases]
    result = {'origin': 'NEW reproduction using retrieved archived sources; not original execution artefacts',
              'python': platform.python_version(), 'dependencies': 'Python standard library',
              'mode': args.mode, 'spectral_encoder': 'archived check_cp_translation.py, reused',
              'runs': runs, 'tested': sum(r['tested'] for r in runs),
              'cospectral': sum(r['cospectral'] for r in runs)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k:result[k] for k in ('mode','tested','cospectral','python')}), flush=True)


if __name__ == '__main__':
    main()
