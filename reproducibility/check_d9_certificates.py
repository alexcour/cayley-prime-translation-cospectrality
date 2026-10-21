#!/usr/bin/env python3
"""Stdlib-only finite certificate checker. No producer, nauty, VF2 or nx import.

Reconstruct D9 as 18 permutations of nine points; enumerate the exact corpus;
check every adjacency under explicit maps; independently check representative
traces, characteristic polynomials and four-motifs. Trust no summary counts.
"""
import argparse
from collections import Counter
from itertools import combinations, permutations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def group_table():
    # Composition of actions t -> a+(-1)^b*t on Z/9Z.
    actions = [tuple((a + (t if b==0 else -t)) % 9 for t in range(9))
               for b in range(2) for a in range(9)]
    indices = {p:i for i,p in enumerate(actions)}
    return [[indices[tuple(p[q[t]] for t in range(9))] for q in actions] for p in actions]


def generates(s, table):
    reached={0}
    while True:
        extended = reached | {table[u][x] for u in reached for x in s}
        if extended == reached:
            return len(reached) == 18
        reached=extended


def adjacency(s, table):
    matrix=[[0]*18 for _ in range(18)]
    for i in range(18):
        for x in s:
            matrix[i][table[i][x]]=1
    return matrix


def matrix_traces(a):
    n=len(a)
    power=[[int(i==j) for j in range(n)] for i in range(n)]
    traces=[]
    for _ in range(18):
        power=[[sum(power[i][k]*a[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        traces.append(sum(power[i][i] for i in range(n)))
    return traces


def bareiss_det(matrix):
    a=[r[:] for r in matrix]
    n=len(a)
    sign,previous=1,1
    for k in range(n-1):
        pivot_row=next((i for i in range(k,n) if a[i][k]),None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k],a[pivot_row]=a[pivot_row],a[k]
            sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                require(numerator % previous == 0,'Nonintegral Bareiss step')
                a[i][j]=numerator//previous
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]


def check_polynomial(a, coefficients):
    require(len(coefficients)==19 and coefficients[0]==1 and
            all(type(c) is int for c in coefficients),'Invalid monic degree-18 polynomial')
    # Two degree-at-most-18 polynomials agreeing at 19 distinct integers coincide.
    for x in range(19):
        expected=0
        for c in coefficients:
            expected=expected*x+c
        matrix=[[(x if i==j else 0)-a[i][j] for j in range(18)] for i in range(18)]
        require(bareiss_det(matrix)==expected,'Characteristic polynomial determinant mismatch')


def motif_histogram(a):
    # Directly enumerate all 24 labellings for each of the 3060 quadruples.
    # Bit shifts run opposite to the producer; the full permutation orbit has
    # the same minimum because reversing all vertex labels reverses these bits.
    histogram=Counter()
    for q in combinations(range(18),4):
        best=4096
        for p in permutations(q):
            code=0
            for i in range(4):
                for j in range(4):
                    if i!=j:
                        code=(code<<1)|a[p[i]][p[j]]
            best=min(best,code)
        histogram[best]+=1
    require(sum(histogram.values())==3060,'Wrong motif coverage')
    return [[key,value] for key,value in sorted(histogram.items())]


def check(certificate):
    require(certificate['schema']=='d9-explicit-certificate-v1','Unknown certificate schema')
    table=group_table()
    corpus={s for s in combinations(range(1,18),3) if generates(s,table)}
    require(len(corpus)==594,'Wrong reconstructed corpus')
    classes=certificate['classes']
    require(len(classes)==12,'Need exactly 12 representative classes')
    by_class={c['class']:c for c in classes}
    require(len(by_class)==12,'Duplicate class identifiers')
    representatives=[tuple(c['representative']) for c in classes]
    require(len(set(representatives))==12 and set(representatives)<=corpus,'Invalid representatives')
    matrices={c['class']:adjacency(c['representative'],table) for c in classes}
    members=certificate['members']
    require(len(members)==594,'Wrong number of membership certificates')
    seen=set()
    counts=Counter()
    actual_labels={}
    for row in members:
        s=tuple(row['support'])
        require(s in corpus and s not in seen,'Missing, duplicated or extraneous support')
        seen.add(s)
        label=row['class']
        require(label in by_class,'Unknown member class')
        require(row['representative']==by_class[label]['representative'],'Representative mismatch')
        p=row['vertex_image']
        require(len(p)==18 and set(p)==set(range(18)) and all(type(x) is int for x in p),'Not a permutation')
        u,v=row['automorphism']['u'],row['automorphism']['v']
        require(u in (1,2,4,5,7,8) and v in range(9),'Invalid automorphism parameters')
        require(p==[(u*(x%9)+v*(x//9))%9+9*(x//9) for x in range(18)],'Automorphism formula mismatch')
        a,b=adjacency(s,table),matrices[label]
        require(all(a[i][j]==b[p[i]][p[j]] for i in range(18) for j in range(18)),
                'Directed adjacency permutation mismatch')
        counts[label]+=1
        actual_labels[s]=label
    require(seen==corpus,'Incomplete enumeration')
    # Now all members have proven isomorphisms; establish separation of the reps.
    actual_traces={}
    for c in classes:
        label=c['class']
        require(counts[label]==c['size'],'Incorrect class size')
        require(actual_labels[tuple(c['representative'])]==label,'Representative in wrong class')
        t=matrix_traces(matrices[label])
        require(t==c['traces_1_to_18'],'Trace certificate mismatch')
        actual_traces[label]=t
        check_polynomial(matrices[label],c['charpoly_descending'])
        require(motif_histogram(matrices[label])==c['motif4'],'Four-motif certificate mismatch')
    required_pairs={frozenset((a,b)) for a,b in combinations(by_class,2)}
    found_pairs=set()
    for witness in certificate['pair_separation']:
        a,b=witness['left'],witness['right']
        pair=frozenset((a,b))
        require(pair in required_pairs and pair not in found_pairs,'Invalid pair coverage')
        k=witness['trace_power']
        require(type(k) is int and 1<=k<=18,'Invalid trace power')
        values=[actual_traces[a][k-1],actual_traces[b][k-1]]
        require(values==witness['values'] and values[0]!=values[1],'Invalid nonisomorphism certificate')
        found_pairs.add(pair)
    require(found_pairs==required_pairs and len(found_pairs)==66,'Incomplete nonisomorphism pair certificates')
    polynomials={tuple(c['charpoly_descending']) for c in classes}
    motifs={tuple(map(tuple,c['motif4'])) for c in classes}
    joint={(tuple(c['charpoly_descending']),tuple(map(tuple,c['motif4']))) for c in classes}
    compact={(t[5],t[8]) for t in actual_traces.values()}
    first_h=next(h for h in range(1,19) if len({tuple(t[:h]) for t in actual_traces.values()})==12)
    computed={'graphs':594,'classes':12,'class_sizes':[counts[c['class']] for c in classes],
              'spectral_classes':len(polynomials),'motif4_classes':len(motifs),
              'joint_spectrum_motif4_classes':len(joint),'trace6_trace9_classes':len(compact),
              'first_complete_trace_prefix_horizon':first_h}
    for key,value in computed.items():
        require(certificate['summary'][key]==value,'False summary value: '+key)
    require((len(polynomials),len(motifs),len(joint),len(compact),first_h)==(12,10,12,12,9),'Unexpected finite classification')
    # Explain one equal-four-motif pair without graph-isomorphism software.
    support_labels={tuple(c['representative']):c['class'] for c in classes}
    prism=matrices[support_labels[(1,8,9)]]
    bipartite=matrices[support_labels[(9,10,11)]]
    require(all(bool(prism[i][j]) ==
                ((i//9==j//9 and (j%9-i%9)%9 in (1,8)) or
                 (i%9==j%9 and i//9!=j//9))
                for i in range(18) for j in range(18)), 'Two-nine-cycle structure mismatch')
    require(all(not bipartite[i][j] or i//9!=j//9 for i in range(18) for j in range(18)),
            'Reflection-support bipartition mismatch')
    circulant_maps=[[(2*(x%9)+9*(x//9))%18 for x in range(18)],
                    [(8*(x%9)+x//9)%18 for x in range(18)]]
    for a,p,steps in zip((prism,bipartite),circulant_maps,((2,9,16),(1,9,17))):
        require(set(p)==set(range(18)) and all(
            bool(a[i][j]) == ((p[j]-p[i])%18 in steps)
            for i in range(18) for j in range(18)), 'Explicit circulant map mismatch')
    return {**computed,'directed_adjacency_checks':594*18*18,
            'representative_pairs_separated':66,'determinants_checked':12*19,
            'structural_witness':{'two_nine_cycles_with_matching_support':[1,8,9],
                                  'bipartite_support':[9,10,11],
                                  'odd_cycle_vertices':list(range(9)),
                                  'circulant_step_sets':[[2,9,16],[1,9,17]],
                                  'circulant_vertex_maps':circulant_maps},
            'checker_dependencies':'Python standard library only',
            'producer_or_graph_isomorphism_software_imported':False,
            'status':'PASS_FINITE_D9_CERTIFICATES'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=check(json.loads(args.certificate.read_text()))
    text=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text,end='')


if __name__=='__main__':
    main()
