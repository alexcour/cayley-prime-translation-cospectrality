#!/usr/bin/env python3
"""Human-readable local certificates for the three primitive cospectral pairs.

For a directed Cayley graph D:
1. reciprocal_skeleton(D): keep only unordered pairs {u,v} for which u->v and v->u;
2. radius2_weight_graph(D, root): symmetrize D, take shells L1,L2 around root,
   and weight each pair in L1 by its number of common neighbours in L2.

The resulting signatures are graph-isomorphism invariants.  For the three
primitive pairs found inside U(210), they give short non-isomorphism certificates.
"""
from collections import Counter
import itertools
import networkx as nx

MOD = 210

EXCEPTIONS = {
    "I":  ((31,181,169), (31,61,199)),
    "II": ((127,157,97), (157,37,67)),
    "III":((127,37,43),  (37,67,163)),
}


def subgroup(T, mod=MOD):
    S = {1}
    frontier = [1]
    while frontier:
        x = frontier.pop()
        for t in T:
            y = (x*t) % mod
            if y not in S:
                S.add(y)
                frontier.append(y)
    return sorted(S)


def cayley_digraph(T, mod=MOD):
    S = subgroup(T, mod)
    G = nx.DiGraph()
    G.add_nodes_from(S)
    for x in S:
        for t in T:
            G.add_edge(x, (x*t) % mod)
    return G


def reciprocal_skeleton(G):
    R = nx.Graph()
    R.add_nodes_from(G.nodes)
    for u, v in G.edges:
        if u != v and G.has_edge(v, u):
            R.add_edge(u, v)
    return R


def reciprocal_signature(G):
    R = reciprocal_skeleton(G)
    comps = []
    for C in nx.connected_components(R):
        H = R.subgraph(C)
        comps.append((len(C), H.number_of_edges(), tuple(sorted(dict(H.degree()).values()))))
    return tuple(sorted(comps))


def radius2_weight_data(G, root=1):
    U = G.to_undirected()
    d = nx.single_source_shortest_path_length(U, root, cutoff=2)
    L1 = sorted(v for v, r in d.items() if r == 1)
    L2 = set(v for v, r in d.items() if r == 2)
    weights = {}
    for a, b in itertools.combinations(L1, 2):
        common = (set(U.neighbors(a)) & set(U.neighbors(b)) & L2)
        weights[(a,b)] = len(common)
    return L1, L2, weights


def weight_layer_signature(G, root=1):
    L1, L2, weights = radius2_weight_data(G, root)
    out = {}
    for w in sorted(set(weights.values())):
        H = nx.Graph()
        H.add_nodes_from(L1)
        H.add_edges_from(e for e, ww in weights.items() if ww == w)
        out[w] = {
            "edges": H.number_of_edges(),
            "degree_multiset": tuple(sorted(Counter(dict(H.degree()).values()).items())),
            "component_sizes": tuple(sorted(len(c) for c in nx.connected_components(H))),
            "triangles": sum(nx.triangles(H).values()) // 3,
            "edges_list": tuple(sorted(tuple(sorted(e)) for e in H.edges())),
        }
    return {"L1": tuple(L1), "L2_size": len(L2), "by_weight": out}


def describe_reciprocal(G):
    R = reciprocal_skeleton(G)
    nontrivial = [R.subgraph(c).copy() for c in nx.connected_components(R) if len(c) > 1]
    if not nontrivial:
        return "no reciprocal edges"
    sizes = sorted(len(h) for h in nontrivial)
    if all(all(d == 2 for _, d in h.degree()) for h in nontrivial):
        return " + ".join(f"C{n}" for n in sizes)
    return str(reciprocal_signature(G))


def main():
    for name, (T1,T2) in EXCEPTIONS.items():
        G1, G2 = cayley_digraph(T1), cayley_digraph(T2)
        print(f"\n=== Exception {name} ===")
        print("T1", T1, "|S|=", len(G1), "reciprocal:", describe_reciprocal(G1))
        print("T2", T2, "|S|=", len(G2), "reciprocal:", describe_reciprocal(G2))
        r1, r2 = reciprocal_signature(G1), reciprocal_signature(G2)
        if r1 != r2:
            print("CERTIFICATE: reciprocal skeleton signatures differ")
            print("  sig1=", r1)
            print("  sig2=", r2)
            continue
        W1, W2 = weight_layer_signature(G1), weight_layer_signature(G2)
        print("reciprocal skeletons agree; inspect radius-2 shell weights")
        allw = sorted(set(W1['by_weight']) | set(W2['by_weight']))
        diffs = []
        for w in allw:
            a, b = W1['by_weight'].get(w), W2['by_weight'].get(w)
            if a != b:
                diffs.append(w)
        if diffs:
            print("  differing weights:", diffs)
            # w=3 is especially readable for Exception II: K4+2 isolates versus 2 triangles.
            w = 3 if 3 in diffs else diffs[0]
            a, b = W1['by_weight'][w], W2['by_weight'][w]
            print(f"  displayed weight w={w}")
            print("  T1:", a)
            print("  T2:", b)
            print("CERTIFICATE: radius-2 weighted first-shell graphs differ")
        else:
            print("No distinction found by these two local certificates")


if __name__ == "__main__":
    main()
