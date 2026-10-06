# Reproducibility

## Base review check

Reference environment in the current preparation pack: Python 3.12.x, standard library only.

Run:

```bash
python3 reproducibility/verify_exact.py --output /tmp/results_local.json
```

The verifier checks exact cyclotomic/HNF scans and finite matrix examples. A zero-mismatch finite scan is supporting evidence, not a proof of a universal theorem.

## Additional review reproductions

Selected review tools and outputs are included:

- `reproducibility/verify_lattice_independent.py`
- `reproducibility/check_cp_translation.py`
- `reproducibility/reproduce_available_sources.py`
- `reproducibility/results/p3_120_review_new.json`
- `reproducibility/results/pge5_416_review_new.json`
- `reproducibility/results/mixed_review_new.json`

These current results close practical checking gaps but do not recover the missing historical originals. Their provenance is recorded under `reproducibility/provenance/`.

## Historical support bundled

The package also includes a non-canonical `reproducibility/legacy_support/` area so that claims referenced by the public examples are not left without their historical support files:

- `inject.py`: original historical finite injectivity check cited by 10B1 (83 relevant even `k<=400`, zero collision according to the internal witness);
- `local_cayley_certificates.py`: standalone local certificates for the three U(210) primitive pairs;
- `noncyclic_circulant_audit.py`: historical cyclic-representation audit for those primitive pairs;
- `PROOF_FAMILY.txt`: written proof/certificate note for the three collisions and the `C_m x C_6` family;
- the two small archived certificate ZIPs from 2026-10-03.

These files are included for provenance and support, not because every historical script is part of the main theorem dependency chain. The long-range `inject.py` computation is not a CI requirement.

## Public-review gate

Before publishing or updating a `0.1.x` public-review snapshot:

1. run the base verifier from the exact candidate checkout;
2. run the selected review reproductions or document why a long run is excluded from CI;
3. regenerate `SHA256SUMS.txt` from that candidate;
4. compile the LaTeX manuscript twice when the TeX toolchain is available;
5. confirm `README.md`, `PUBLICATION_STATUS.md`, `CLAIM_BOUNDARY.md`, and `docs/RELEASE_GATE.md` are synchronized.

These checks authorize a bounded review snapshot only. Stable `v1.0.0` additionally requires the independent-review, antecedence, metadata/license, and stable-candidate gates listed in `docs/RELEASE_GATE.md`.
