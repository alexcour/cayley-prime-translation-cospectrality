#!/usr/bin/env python3
"""Check whether the three primitive U(210) exception digraphs admit a 3-generator cyclic Cayley representation.

For each primitive exception on n=12 or 24 vertices, enumerate every generating 3-subset
S of Z_n\{0} and test directed graph isomorphism against Cay(Z_n,S).
"""
import itertools, math
import networkx as nx
from local_cayley_certificates import cayley_digraph, EXCEPTIONS


def cyclic_cayley(n, T):
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for x in range(n):
        for t in T:
            G.add_edge(x, (x+t) % n)
    return G


def generates(n, T):
    g = n
    for t in T:
        g = math.gcd(g, t)
    return g == 1


def main():
    for name, (T1,T2) in EXCEPTIONS.items():
        G1, G2 = cayley_digraph(T1), cayley_digraph(T2)
        n = len(G1)
        m1, m2 = [], []
        for T in itertools.combinations(range(1,n),3):
            if not generates(n,T):
                continue
            H = cyclic_cayley(n,T)
            if nx.is_isomorphic(G1,H): m1.append(T)
            if nx.is_isomorphic(G2,H): m2.append(T)
        print(f"Exception {name}: n={n}")
        print("  cyclic representations of first graph:", m1)
        print("  cyclic representations of second graph:", m2)

if __name__ == '__main__':
    main()
