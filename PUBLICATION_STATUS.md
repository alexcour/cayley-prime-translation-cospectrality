# Publication status

Status date: 2026-10-07
Version: 0.1.3-review
Review channel: PUBLIC REVIEW / 0.1.x
Stable scientific release: NO-GO

## Scientific status (E)

- 10A6 (`p >= 5`): PROVED according to the current internal witness; independent human review remains open.
- 10C3 (`p = 3`): PROVED according to the current internal witness; the public-facing transcription is synchronized with the manuscript, while independent review remains open.
- 10B1 (cyclic injectivity): PROVED according to the current internal witness; independent review remains open.

Public review status does not upgrade E and is not evidence of external validation.

## Priority / antecedence status (N)

**N = NON AUDITEE** for the general claims unless explicitly narrowed below.

- C12 example: ANTECEDENT / PRIOR.
- Brown power-of-two cyclic subfamily: ANTECEDENT / OVERLAPPING.
- Mönius 2020, Theorem 10: OVERLAPPING for adjacency cospectrality when `p=3`, `H=C_k`, `3` not dividing `k`, `4|k`, `kappa=1`, `kappa'=mu=1+k/2`, including `k=4`; see `PRIOR_ART.md`. **N = NON AUDITEE** for the other involutions and the complete cyclic family; no antecedence conclusion for 10B1's injectivity or a nonisomorphism criterion follows from this comparison.
- General `p>=5` classification: NON AUDITEE TO CLOSURE.
- General `p=3` classification: NON AUDITEE TO CLOSURE.
- Cyclic injectivity theorem: NON AUDITEE TO CLOSURE.
- `C_m x C_6` family, `h` criterion, beta mechanism, I/II, `Psi_l`: priority not established.

Primary-source comparison remains open for Meng (1998). For Huang-Chang (2001), Liu-Zhou's 2022 survey restates the relevant theorem hypotheses: the cyclic specialization `n=3k`, with even `k` and `3` not dividing `k`, intersects the stated order families only for `k=2^a`. This removes Huang-Chang as a global blocker outside the power-of-two intersection, but primary full-text reading is still pending for an exact support-level comparison there. The Mönius 2020 primary article has been inspected for the explicit cospectrality overlap above; comparisons beyond that subfamily and the general `h`/`beta` classifications remain **N = NON AUDITEE**.

No priority or discovery wording is authorized while N remains open.

## Reproducibility / review status (Q)

Strong but incomplete historical provenance.

Available:
- publication verification script and aggregate results;
- original `inject.py` finite check cited by 10B1;
- historical U(210)/`C_m x C_6` support note, local-certificate script, and archived certificate ZIPs;
- independent/review HNF verifier;
- current p=3-to-120 row-level reproduction;
- current p>=5 416-case reproduction;
- current mixed-domain reproduction;
- file identity and validation metadata.

Not recovered as original historical artifacts:
- mixed_cp_scan.py / mixed_cp_scan_v2.py / mixed_general_scan.py;
- original row-level p=3-to-120 output;
- original 416-case extraction / audit_exact.py.

Reconstructed/current reproductions remain explicitly labeled and must not be described as original historical execution artifacts.

Independent human mathematical review remains OPEN.

## Publication state

- GitHub: **public as PUBLIC REVIEW / 0.1.x** for external checking, with all status warnings retained.
- Repository verification (2026-10-07): PR #1 merged at commit [`5e31912134fb6303639facedf4150d32255795bd`](https://github.com/alexcour/cayley-prime-translation-cospectrality/commit/5e31912134fb6303639facedf4150d32255795bd); [verify #4 (run 37585311793)](https://github.com/alexcour/cayley-prime-translation-cospectrality/actions/runs/37585311793) succeeded on that exact commit, with `exact-checks` and `manuscript-build` both passing.
- Stable release (`v1.0.0`): BLOCKED until the stable-release gates are closed.
- Zenodo: DO NOT CREATE a Cayley DOI in this review stage.
- HAL: DO NOT DEPOSIT in this review stage.
- arXiv: DO NOT SUBMIT in this review stage.
- ORCID: do not assert a Cayley archival work identifier before an eligible public identifier exists.
- Google Scholar: do not assert indexing before it actually occurs.

A public GitHub `0.1.x` review snapshot is a dissemination/review event, not a stable scientific publication claim.
