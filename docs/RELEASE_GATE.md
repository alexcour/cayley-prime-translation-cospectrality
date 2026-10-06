# Release gate

Current decision: **GO PUBLIC REVIEW / 0.1.x; NO-GO STABLE v1.0.0.**

## Gate R -- public review 0.1.x

A `0.1.x` GitHub repository/tag may be public when all of the following remain true:

- `PUBLICATION_STATUS.md` states `PUBLIC REVIEW / 0.1.x` and `N = NON AUDITEE` for the general claims;
- `CLAIM_BOUNDARY.md` forbids priority/discovery wording while the antecedence audit is open;
- README and release notes state that the snapshot is unstable and intended for external review;
- reconstructed/current reproduction artifacts remain labeled by provenance;
- no workflow in this stage creates a Zenodo DOI, HAL deposit, arXiv submission, or stable scientific release;
- no `v1.0.0` tag is created in this stage.

**Gate R status: PASS for publication as a bounded public-review snapshot, subject to final repository-side file/commit verification.**

## Gates still open before stable v1.0.0

- Confirm by independent review that the synchronized 10C3 wording (`3∣|H|` and the chord-lemma coincidence clause) leaves every downstream argument valid.
- Obtain an independent human mathematical review of 10A6 and 10C3.
- Complete the targeted primary-source antecedence checks listed in `PRIOR_ART.md`.
- Authorship, independent affiliation, ORCID and original-contribution licenses are confirmed for the review series by the author. Document funding/conflict statements and final archival citation details before a later stable/archival step.
- Pass clean-checkout reproducibility and manuscript build checks from the exact stable candidate.
- Review all public metadata again for claim-boundary compliance.

Closing Gate R does not close any of these stable-release gates.

## Explicitly deferred actions

Until a later governance decision after the open review/antecedence gates:

- no `v1.0.0`;
- no Zenodo DOI;
- no HAL deposit;
- no arXiv submission;
- no presentation of the repository as a validated or stable scientific publication.
