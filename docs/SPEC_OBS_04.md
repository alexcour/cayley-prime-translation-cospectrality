# SPEC-OBS-04 — Known noncyclic Cayley counterexample to universal two-point walk completeness

**Status (research review):** E = elementary proof and exact finite reproduction. N = known antecedent for the underlying Shrikhande/rook pair; **no priority claim**, broader originality not audited. Q = standard-library verification passed locally; independent human review remains open. Date of note: 2026-10-09. This is a scope correction and new research direction, **not** a modification of SPEC-OBS-03's correct finite cyclic three-element counts.

## Precise counterexample

Let `G = (Z/4Z)^2`. Construct simple undirected Cayley graphs (viewable also as symmetric loopless digraphs with both orientations) with supports:

- `S_rook = {(1,0),(2,0),(3,0),(0,1),(0,2),(0,3)}`.
- `S_shrikhande = {(1,0),(3,0),(0,1),(0,3),(1,1),(3,3)}`.

Both supports have size **six**; this example does **not** lie in the degree-three cyclic support family of SPEC-OBS-01/03. Both graphs are connected, undirected, simple, Cayley on the same **noncyclic abelian group**, and strongly regular with parameters `(v,k,lambda,mu)=(16,6,2,2)`. The classical Shrikhande/4x4 rook nonisomorphism and cospectrality are established background, not discoveries of this programme.

## Universal two-point obstruction (elementary proposition)

For a strongly regular graph `A` with parameters `(v,k,lambda,mu)`, the adjacency matrix satisfies

`A^2 = (k-mu) I + (lambda-mu) A + mu J`, where `J` is all-ones.

Moreover `A J = J A = k J`. Hence by induction all powers `A^h`, for `h>=0`, lie in `span{I,A,J}`, with coefficients depending **only on the common parameters**. For any two strongly regular graphs with identical parameters, every walk count `(A^h)uv` depends only on whether `u=v`, `u~v`, or `u!=v` and nonadjacent. The counts of such ordered pairs are parameter-determined. Therefore their entire multisets

`I_H(A) = multiset_{(u,v)} (((A^h)uv,(A^h)vu))_{h=1..H}`

are identical **for every finite H**, even if the graphs are nonisomorphic. The proof concerns this *multiset* invariant, not equality of their labelled adjacency matrices.

For these parameters, `A^2 = 4I+2J`; the shared characteristic polynomial is `(x-6)(x-2)^6(x+2)^9`.

## Exact nonisomorphism certificate

The neighborhood induced on the six neighbors of any vertex is:

- For the rook graph: two disjoint triangles `K3 + K3`. Each root lies in **two** four-cliques, and the graph has **eight** `K4` in total.
- For Shrikhande: a six-cycle `C6`, with **zero** triangle in each root neighborhood and **zero** `K4`.

An isomorphism preserves this property; therefore the graphs are **not isomorphic**. The exact script checks degree, adjacency symmetry, absence of loops, `A^2=4I+2J`, characteristic polynomial, identical `I_H` through `H=20`, and full enumeration of `K4` and neighborhood triangles. Infinite-horizon equality follows from the proved identity, not from the finite scan.

## A useful higher-order observable

For each **adjacent unordered vertex pair** `{u,v}`, define

`Q_A(u,v) = number of edges induced inside (N(u) intersection N(v))`.

This is an isomorphism-equivariant *pair-anchored, four-vertex* observation. For each of the 48 undirected edges:

- Rook: `Q_A(u,v)=1` (the two common neighbors are adjacent).
- Shrikhande: `Q_A(u,v)=0` (the two common neighbors are nonadjacent).

The scripts count each undirected edge twice when using ordered arcs: histograms `{1:96}` and `{0:96}`. Thus the enriched observation separates this known pair while the complete two-point **walk** signature cannot.

## Scientific interpretation and scope boundary

SPEC-OBS-03 established `I_n` completeness only for the explicitly enumerated small cyclic digraphs with **three** support elements. SPEC-OBS-04 falsifies the unconditional extrapolation to all Cayley graphs already within finite abelian groups of order 16, even when both graphs are connected and loopless. It does not falsify a theorem restricted to cyclic ternary digraphs, and does not demonstrate completeness of `Q` for other classes.

The pair is classical. A useful aim is to characterize which **adjacency algebras/coherent configurations** cause moment/walk-signature degeneracy; then preregister a falsifiable study of restricted cyclic three-element supports at larger orders and noncyclic three-element supports, keeping tests separated from known antecedents.

### Reproducibility and references

- `python3 reproducibility/verify_spec_obs_04.py` (Python standard library). Exact expected values are asserted.
- `reproducibility/results/spec_obs_04_exact_summary.json`: fixed local output snapshot, not a historical execution log.
- E. W. Weisstein, [Shrikhande Graph, MathWorld](https://mathworld.wolfram.com/ShrikhandeGraph.html).
- [Shrikhande graph](https://en.wikipedia.org/wiki/Shrikhande_graph), Cayley support, SRG parameters and local hexagon.
- [Four-by-four rook / Shrikhande comparison](https://mathdrum.blogspot.com/2014/12/), explicit two Cayley supports.

No modification to the main manuscript or theorem witnesses 10A6/10C3/10B1. Stable release/Zenodo/HAL/arXiv remain NO-GO. PR remains a draft; independent review open.
