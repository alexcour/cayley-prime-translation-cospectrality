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

### Historical ZIP verification

The retained copy of `cayley-prime-translation-cospectrality-public-review-0.1.2.zip` is 654,699 bytes with SHA-256 `9214e6f93df8eb81e1114b3ca87c54a5d61eae91d3fe4eacf8fde485bacfb468`. Its internal `VERSION` is `0.1.2-review`. On 21 November 2026, the ZIP passed its CRC check and all 49 entries in its internal SHA-256 manifest matched. After stripping the outer staging directory, all 50 files, including the manifest, matched the Git tree of [the historical import](https://github.com/alexcour/cayley-prime-translation-cospectrality/commit/caa541e9ad110713e4a0821c4f006b396fadc523) byte for byte. That import is an ancestor of the review candidate.

Against this source, the 0.1.4-review tree retains 34 files byte for byte, updates 16 and adds 10. The original source witnesses, public theorem witnesses, reproduction scripts, archived results and historical certificate ZIPs are among the identical files. The current checkout’s `SHA256SUMS.txt` covers the current paths. The [historical inventory](reproducibility/provenance/INVENTAIRE_ORIGINAUX.csv) still identifies unrecovered upstream originals.

## Witnesses and reproductions

The original 10C3 Drive witness is preserved byte-for-byte as `proofs/original_witnesses/theorem_p3_10C3_original_2026-10-04.txt`. The original 10D1 audit source transcription is likewise kept under `proofs/original_witnesses/PRIOR_ART_SOURCE_10D1_original.txt`. The public-facing `proofs/theorem_p3_10C3.txt` applies only the two editorial synchronizations already present in the manuscript: unambiguous `3∣|H|` notation and the unit-chord coincidence clause for `a=-b`.

The `reproducibility/legacy_support/` directory contains historical support artifacts copied from Drive. It must not be confused with the canonical current reproduction layer.
