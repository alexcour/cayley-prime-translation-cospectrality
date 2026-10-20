# SPEC-OBS-08 — Exact directed induced motifs on the SPEC-OBS-07 nonabelian corpus

**Status**: E = exhaustive finite integer enumeration and exact graph-isomorphism check via NetworkX VF2; N = **NON AUDITÉE** (novelty and prior art); Q = reproducible implementation, permutation invariance tests; external human review pending.

## Fixed domain and definitions

Reuse *exactly* the corpus of SPEC-OBS-07: all identity-free generating connection triples of the dihedral groups D3,..,D8 (|Dm|=2m), Q8 and A4, with directed right Cayley adjacency A[u,v]=1 iff v=u*s. There are **1,068** digraphs. Comparisons include different groups at the same order.

For each graph count the **induced directed** motifs on all unordered sets of 3 vertices and then 4 vertices. A motif type is its complete ordered 0/1 adjacency pattern modulo all permutations of its vertices (the canonical code is the minimum bit pattern over permutations). Motif-count histograms are intrinsic isomorphism invariants. Spectral classes, full two-point walk I_n classes, three-motif classes and four-motif classes are all computed **within fixed graph order**; no cross-order identification.

Exact isomorphism classes are independently checked by NetworkX directed VF2 after restricting candidate comparisons to identical four-motif histograms. Equality of motif histograms is only a necessary condition; VF2 verifies surviving graph equivalences.

## Exhaustive finite results

| order | supports | spectral classes | I_n classes | 3-motif classes | 4-motif classes | isomorphism classes |
|---:|---:|---:|---:|---:|---:|---:|
| 6 | 10 | 3 | 3 | 3 | 3 | 3 |
| 8 | 64 | 6 | 7 | 7 | 7 | 7 |
| 10 | 80 | 5 | 5 | 5 | 5 | 5 |
| 12 | 296 | 18 | 20 | 20 | 22 | 22 |
| 14 | 266 | 8 | 8 | 8 | 8 | 8 |
| 16 | 352 | 13 | 14 | 13 | 14 | 14 |

At order 12, 288 cospectral nonisomorphic **pairs of supports** remain indistinguishable by I_n; jointly retaining I_n plus the 3-motif histogram reduces these to 144; the 4-motif histogram reduces them to **zero**. The 3-motif histogram **alone** leaves 288 such pairs at order 12, due to different failures from I_n.

At order 16 the 3-motif histogram alone leaves 1,024 nonisomorphic cospectral support pairs indistinguishable; I_n does distinguish them, and 4-motifs also distinguish them. Hence **neither 3-motifs nor I_n dominates the other** as a standalone invariant in the selected corpus.

All 4-motif classes agree exactly with the true directed isomorphism classes at the six graph orders. This is a bounded finite observation, **not a theorem that 4-vertex motifs always suffice**.

## Counterexample witnesses preserved

- **D6, order 12:** connection sets {1,3,6} and {1,6,8} in the canonical D6 indexing from SPEC-OBS-07. Same characteristic polynomial, same all-horizon two-point walk fingerprint, same complete histogram of induced directed 3-vertex motifs, **different** histograms of induced directed 4-vertex motifs. An independent simple certificate: 30 versus 33 independent 4-vertex sets. The motif code for an edgeless induced quadruple is 0 and its recorded counts are 30 and 33.
- **A4, order 12:** connection sets {1,3,5} and {1,3,6} in the lexicographic even-permutation indexing of SPEC-OBS-07. Cospectral, same all-horizon I_n; already separated by induced directed 3-vertex motifs and also 4-vertex motifs.

Cross-checks: exact reassignment of vertex labels preserves the canonical histogram for k=3 and k=4; independent NetworkX directed graph isomorphism confirms both witnesses nonisomorphic. The results are obtained with integer counts. Four-vertex motif histograms are canonicalized over all 24 permutations of each quadruple; the three-vertex motifs over all six permutations.

## Reproduction and boundaries

Run `python3 reproducibility/verify_spec_obs_08.py output.json` (requires Python 3 and NetworkX; no NumPy dependency). Frozen summary: `reproducibility/results/spec_obs_08_exact_summary.json`. This summary contains per-order and per-group aggregate counts, motif-class statistics and witness difference lists; it does **not** archive every graph's complete motif table.

**Important distinction:** motifs on *unordered vertex subsets* and WL tuple refinements are different observables; no automatic equivalence to k-WL is asserted. The exact result establishes only a boundary for this corpus, not minimal arity in all graph families. Prior art not audited. No Lean proof or novel general theorem. Manuscript 10A6/10C3/10B1 and stable-release gate remain unchanged; PR #6 stays draft.
