# Provenance policy

The project distinguishes three artifact classes:

1. **Original archived artifact**: byte-level historical file recovered from the original working record.
2. **Reconstructed implementation**: a later implementation written to reproduce a historical computation.
3. **Current reproduction result**: output generated later from an available or reconstructed implementation.

A reconstructed or current reproduction artifact must never be renamed or described in a way that implies it is the original historical execution artifact.

The current public-review package is assembled from two Drive coordination/review ZIPs and current theorem witnesses. Coordination-only files, internal messages, blank review forms, and broad internal search evidence are deliberately excluded from the public candidate surface.

See `reproducibility/provenance/INVENTAIRE_ORIGINAUX.csv` and the JSON identity/validation files.


## 0.1.x synchronization note

The original 10C3 Drive witness is preserved byte-for-byte as `proofs/original_witnesses/theorem_p3_10C3_original_2026-10-04.txt`. The original 10D1 audit source transcription is likewise kept under `proofs/original_witnesses/PRIOR_ART_SOURCE_10D1_original.txt`. The public-facing `proofs/theorem_p3_10C3.txt` applies only the two editorial synchronizations already present in the manuscript: unambiguous `3∣|H|` notation and the unit-chord coincidence clause for `a=-b`.

The `legacy_support/` directory contains historical support artifacts copied from Drive. It must not be confused with the canonical current reproduction layer.
