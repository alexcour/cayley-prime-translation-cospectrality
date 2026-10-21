# D9 — explicit finite classification and spectral separation

**21 October 2026. Finite, computer-certified result; novelty not audited.** This extends the independent nauty replay in draft PR #15. It does not rerun VF2, change the historical VF2 files, promote a stable release or attribute a mathematical validation to Brendan McKay.

## Outcome and precise boundary

For the exact corpus of **all 594 generating identity-free three-element supports of D9**, with 18 vertices and arcs `g → g*s`:

- The **12 nauty classes coincide with the 12 orbits** under 54 explicit automorphisms of D9.
- Each of the **594 graphs has an explicit vertex permutation** to its listed representative; all 18² adjacency entries are checked under every map.
- The 12 representatives have **12 different integer characteristic polynomials**. Thus the spectrum alone distinguishes the isomorphism classes **within this corpus**. Adding the four-motif histogram gives 12 classes as well, with no further distinction here.
- There are only **10 four-motif histograms**, with the same two ambiguous pairs as before.
- The pair **(tr(A⁶), tr(A⁹))** distinguishes all 12 classes. This pair was selected after inspection, not preregistered and not claimed minimal among arbitrary statistics.
- The full trace prefix `tr(A),...,tr(A^h)` first distinguishes all classes at **h=9**; a specific pair agrees through h=8 and differs at h=9.

This is **not** a statement that these graphs are determined by their spectra among arbitrary digraphs, arbitrary connection sets or other groups. It is not a theorem for all dihedral orders, and it establishes no novelty or priority.

## Representatives and a compact separating table

Here `w_k` counts directed closed walks at one vertex. Vertex transitivity gives `tr(A^k)=18*w_k`. The certificates use global traces, which are isomorphism invariants without any chosen vertex.

| Class | Support | Supports in class | w₆ | w₉ |
| --- | --- | ---: | ---: | ---: |
| N01 | 1,2,9 | 54 | 51 | 1028 |
| N02 | 1,3,9 | 54 | 38 | 1103 |
| N03 | 1,4,9 | 54 | 52 | 1142 |
| N04 | 1,6,9 | 54 | 56 | 887 |
| N05 | 1,8,9 | 27 | 141 | 2 |
| N06 | 1,9,10 | 54 | 71 | 1570 |
| N07 | 1,9,11 | 54 | 104 | 76 |
| N08 | 1,9,12 | 54 | 64 | 865 |
| N09 | 1,9,13 | 54 | 68 | 778 |
| N10 | 3,9,10 | 54 | 63 | 1015 |
| N11 | 9,10,11 | 27 | 141 | 0 |
| N12 | 9,10,12 | 54 | 101 | 0 |

Every row has a different ordered pair. The archive also stores all 19 characteristic polynomial coefficients, traces through 18, complete four-motif histograms, all member maps, and a separating trace for each of the 66 representative pairs.

## Explicit maps and the certificate argument

Write an element as `(a,b)`, indexed `a+9*b`, with multiplication `(a,b)(c,d)=(a+(-1)^b*c mod 9,b+d mod 2)`. For a unit `u` modulo 9 and `v` modulo 9, use

`phi_(u,v)(a,b) = (u*a+v*b mod 9,b)`.

There are six unit choices and nine choices of v, hence 54 explicit maps. Each is a bijective homomorphism (equivalently `r ↦ r^u`, `s ↦ r^v*s` preserves the dihedral relations). Therefore it maps a right-Cayley graph for S onto the right-Cayley graph for `phi(S)`.

The producer enumerates these maps and chooses the lexicographically smallest support in the orbit. The certificate stores u, v, all 18 vertex images and the representative for every support. This orbit enumeration is not assumed to prove nonisomorphism between different orbits. That part is supplied independently by the distinct traces/characteristic polynomials of the 12 representatives.

The checker reconstructs all 594 generating supports, verifies all member permutations against all directed adjacency entries, and verifies all 66 representative separations. Together these checks provide a finite exhaustive classification certificate. The certificate is not based solely on trusting a graph-isomorphism engine.

## Two implementations and what each verifies

Producer: `reproducibility/build_d9_certificates.py`. It reuses only the pinned corpus definitions from the earlier replay, counts traces by group convolution and derives characteristic polynomials using exact integer Newton identities. The old nauty CSV is used only for a comparison of full partitions; it does not generate the member maps or nonisomorphism certificates.

Checker: `reproducibility/check_d9_certificates.py`. It imports **only Python standard-library modules**, not the producer, NetworkX, nauty, the old VF2 script or the earlier replay module. It reconstructs D9 by composing its 18 permutation actions on nine points and reconstructs the generating corpus by closure. It then checks:

1. **192,456 adjacency entries** under 594 explicit bijections.
2. Traces through order 18 by ordinary integer matrix multiplication, independently of the producer's convolution method.
3. Each degree-18 characteristic polynomial at **19 distinct integers**, comparing it with a fraction-free Bareiss determinant of `xI-A`: **228 exact determinant checks**. Two polynomials of degree at most 18 agreeing at 19 points coincide.
4. Four-motif histograms by directly considering all 24 relabellings of each of the 3060 quadruples per representative, rather than using the producer's canonical-code lookup table.
5. All 66 pair certificates and recomputed summary counts.

`test_d9_certificates.py` has nine tests, including rejection of missing/duplicate supports, a nonpermutation, a bijective map to the wrong graph, and corrupt polynomial, trace, motif and pair certificates. Bareiss row-swapping and singular-matrix controls are included.

## A structural explanation of one collision

For S={1,8,9}, the graph consists of **two 9-cycles joined vertex by vertex**. The vertices 0,1,...,8 give an explicit odd cycle. For T={9,10,11}, all support elements are reflections, so each arc changes b: the graph is **bipartite**, with parts 0..8 and 9..17. Thus S and T cannot be isomorphic, independently of any algorithmic GI verdict.

The first graph has exactly two closed walks of length 9 at each vertex (the two directions around its 9-cycle), so its ninth trace is 36. The second graph has no odd closed walk, so its ninth trace is 0. A length-9 closed walk in the first graph cannot use a matching edge: an even positive number of matching steps leaves fewer than nine and an odd number of ±1 cycle steps, which cannot sum to zero modulo 9. This explains these trace values directly. Their first eight traces agree, as independently checked, and their four-motif histograms also agree.

Both graphs additionally have explicit cyclic presentations on 18 vertices: maps `(a,b) ↦ 2a+9b mod 18` for S and `(a,b) ↦ 8a+b mod 18` for T give step sets {2,9,16} and {1,9,17}, respectively. The checker verifies both complete adjacency correspondences. A nonabelian Cayley presentation is therefore not an intrinsic label for these graphs.

The other ambiguous pair, {1,9,12}/{1,9,13}, already separates at trace order 6: 1152 versus 1224. The 9 October erratum remains correct: **neither of the two four-motif witness pairs is cospectral**. D9 supplies no counterexample to reconstruction by spectrum plus four-motifs in the declared corpus.

## Replay, provenance and remaining work

Initial artifacts: `reproducibility/results/d9_certificates_20261021/`. Scripts, commands, stdout/stderr, checker reports and SHA-256 manifests are conserved. CI runs the isolated checker, corruption tests and deterministic certificate rebuild in a job requiring no nauty installation, alongside the existing nauty replay.

```sh
python3 reproducibility/build_d9_certificates.py --out /tmp/d9-certificates
python3 -I reproducibility/check_d9_certificates.py \
  reproducibility/results/d9_certificates_20261021/certificate.json
python3 reproducibility/test_d9_certificates.py -v
```

The historical VF2 membership table is still missing. **Its equality to the nauty partition remains unestablished**, although the current partition is now certified by explicit maps and exact separating invariants. This new certificate is not to be retroactively labelled as an old VF2 output. COU-46 keeps this provenance reserve open.

Next research step: bounded D10 replay under the preregistration, checking whether automorphism orbits and isomorphism classes still coincide, whether spectra still separate all classes, and how early trace signatures fail. These are questions, not extrapolated results. No D10/D11/D12/S4 run is included here.
