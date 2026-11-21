# Provenance policy

The project distinguishes three artifact classes:

1. **Original archived artifact**: byte-level historical file recovered from the original working record.
2. **Reconstructed implementation**: a later implementation written to reproduce a historical computation.
3. **Current reproduction result**: output generated later from an available or reconstructed implementation.

A reconstructed or current reproduction artifact must never be renamed or described in a way that implies it is the original historical execution artifact.

The current public-review package is assembled from two Drive coordination/review ZIPs and current theorem witnesses. Coordination-only files, internal messages, blank review forms, and broad internal search evidence are deliberately excluded from the public candidate surface.

See `reproducibility/provenance/INVENTAIRE_ORIGINAUX.csv` and the JSON identity/validation files.


## 0.1.x snapshot lineage

| Snapshot | Recorded source and changes |
| --- | --- |
| 0.1.2-review | The public-review Drive ZIP labeled 0.1.2 carried an internal `VERSION` of `0.1.2-review`. The historical [staging report](STAGING_BUILD_REPORT.md) records that version. |
| 0.1.3-review | The [6 October preparation record](docs/CHANGES_0.1.3-review.md) documents the transition from the Drive ZIP, with licensing, review intake and CI changes. Subsequent [PDF synchronization](docs/PDF_SYNC_20261020.md) records the LaTeX and PDF hashes for the October revision. |
| 0.1.4-review | Descends from Git commit [8755f12](https://github.com/alexcour/cayley-prime-translation-cospectrality/commit/8755f12c979288592d53bb3b9f1a51cf5f4f26db). The version identifies the repository snapshot. The README, antecedence audit and manuscript discussion were updated for review and the PDF was rebuilt from the revised LaTeX source. |

The 0.1.2-review source ZIP was recorded in the handoff pack. The October staging and change records establish the documented lineage. A fresh byte-level comparison with that source ZIP remains open. The current checkout's `SHA256SUMS.txt` records the current files. The [historical inventory](reproducibility/provenance/INVENTAIRE_ORIGINAUX.csv) records originals still missing.

## Witnesses and reproductions

The original 10C3 Drive witness is preserved byte-for-byte as `proofs/original_witnesses/theorem_p3_10C3_original_2026-10-04.txt`. The original 10D1 audit source transcription is likewise kept under `proofs/original_witnesses/PRIOR_ART_SOURCE_10D1_original.txt`. The public-facing `proofs/theorem_p3_10C3.txt` applies only the two editorial synchronizations already present in the manuscript: unambiguous `3∣|H|` notation and the unit-chord coincidence clause for `a=-b`.

The `reproducibility/legacy_support/` directory contains historical support artifacts copied from Drive. It must not be confused with the canonical current reproduction layer.
