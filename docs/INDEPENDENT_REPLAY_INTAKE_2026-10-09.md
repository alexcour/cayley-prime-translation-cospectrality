# Independent replay report — intake, 9 October 2026

**Source:** an independent-agent report supplied by the author in conversation; **scripts, logs and raw datasets were not attached and were not located in Drive or this GitHub repository during this intake**. This is a *reported* result awaiting artifact-based replay, not a certified reproduction, peer review, or publication upgrade.

## Cayley statements — reported scan, unverified raw evidence

| Claim | Reported checks | Reported positives | Reported discrepancies |
|---|---:|---:|---:|
| 10A6, p=5,7,11, up to 150 vertices | 13,486 | 1,190 cospectral | 0 |
| 10C1/10C3, p=3, up to 120 vertices | 22,436 | 5,484 cospectral | 0 |
| 10B1, k<=200 | 67 eligible k | n/a | 0 collisions |

Reported methods: fresh implementation of traces of adjacency powers/closed walks with character-eigenvalue cross-check; VF2 isomorphism; cyclic injectivity test. Reported p>=5 computation changed to character method for speed after exact-walk comparison.

**Required release evidence:** source script with hash; exact group classification/enumeration policy and matrix/support orientation; data rows including witnesses (not just aggregate counts); polynomial/trace vs character equivalence tolerance or exact arithmetic domain; VF2 directed-graph handling, loops and edge multiplicities; k values actually eligible; executed versions, machine command, stdout, environment and commit. Include counterexample search coverage rather than infer universality. Do not claim an independent HUMAN review.

The report also asserts 190/190 cospectral non-isomorphic pairs from the beta regime up to 48 vertices and none in the homomorphism h regime. This is a scoped observation requiring row-level witnesses and a precise equivalence relation for counting pairs; retain it as **reported, not independently verified**.

## Proof and novelty gates

Claim 10A6 proof reportedly inspected but still requires human check of the Poonen–Rubinstein vanishing-sums argument, including possible repeated roots, hypotheses and multiplicities. 10B1 finite injectivity scans do not prove the infinite theorem. The prior-art status still records Brown/Mönius overlaps; Meng 1998 primary pages remain unavailable, Huang–Chang 2001 comparison incomplete. Novelty=N NON AUDITÉE. No new 1.0 release, DOI or stable review status.

## Separate Δ3 rigidity report (NOT F-001)

The same conversation reports a Dyson–Mehta spectral-rigidity Δ3 computation using supposedly the first 100,000 zeta-zero ordinates, with Δ3(L)=0.093,0.162,0.179 for L=2,10,30 and a fitted slope 0.043±0.001 against a comparison 0.378. No source code, unfolded ordinate list, window-averaging convention, fit ranges or result plot was supplied to this repository. Even its asserted 100,000-zero completeness is not independently certified by the described mpmath first-zero check.

**Distinct claim:** Journal F F-001 concerns historical *prime-residue proportion* 0.378 in {1,11,29} modulo 30; this Δ3 claim concerns a *spectral statistic*. The numerical coincidence of 0.378 is not a shared measurement and must never cross-invalidate the two records. The Δ3 result must receive its own identifier and complete definition/source before a dedicated falsification is admitted.

## Reviewer intake checklist

1. Obtain exact script+hashes, zero data including source/exhaustiveness and full Delta3 specification.
2. Replay Cayley scan with published Python requirements, full per-case table, and both invariant computations.
3. Check whether VF2 objects are directed adjacency graphs with loops and whether "190 pairs" counts ordered vs unordered and modulo which group/support symmetries.
4. Separate mathematical correctness from finite evidence and the still-open literature/priority audit.
5. Retain PUBLIC REVIEW 0.1.x and no general novelty claim until a checkable artifact and human review.

Status: **REPORTED / RAW ARTIFACTS NOT LOCATED / HUMAN REVIEW OPEN / NOVELTY OPEN.**
