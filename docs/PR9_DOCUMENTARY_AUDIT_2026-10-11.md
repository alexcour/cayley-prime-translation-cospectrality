# PR #9 documentary audit -- 11 October 2026

Scope: repository governance, file integrity, licensing documentation and the current public file surface. This is an internal documentary/technical audit, not independent human mathematical review or a legal ownership opinion.

## Candidate and authority

- PR: <https://github.com/alexcour/cayley-prime-translation-cospectrality/pull/9>.
- Audited starting head: `d394286b4254cf492d8a4d330e6e40334f409353`; base: `495a2c145d12c0ec6e50ea4e5cca192e52f5489d`.
- [verify run 38157976037](https://github.com/alexcour/cayley-prime-translation-cospectrality/actions/runs/38157976037): completed successfully for that head. Exact checks, all four workflow JSON checks, manifest and manuscript build passed. No reviews/comments were returned when inspected.
- General policy: [ZENODO_PRE_REVIEW_POLICY_2026-10-11.md at commit 482ce6f](https://github.com/alexcour/couret-finite-verifications/blob/482ce6f4cc6e5e2bcef6178d5b63e0042026b55f/ZENODO_PRE_REVIEW_POLICY_2026-10-11.md). It lifts only the review-based embargo on explicitly unreviewed archives and defers Cayley to its own release gate.
- Corrective changes are confined to governance/reproduction instructions, this audit, the SHA-256 manifest and the generated manuscript PDF. The proof witnesses, LaTeX source, scientific scripts, result data and historical ZIP bytes are unchanged. The correction commit and its CI run must be checked separately; the starting head's green run does not validate new files.

## Verifiable anomalies corrected

1. README still prohibited all Zenodo archiving and described that prohibition as current. It now follows Gate Z, while retaining the stable-release, HAL and arXiv prohibitions and stating the current HOLD explicitly.
2. Gate Z referred to an undefined D status and nonexistent stable-release Gates B/C. It now uses the project's E/N/Q doctrine and the actual stable-release checklist. The requirements are retained and made individually reviewable.
3. Earlier changelogs now identify their blanket Zenodo embargo as a historical decision. Historical witnesses and containers remain unchanged.
4. The historical reproduction command/identity records refer to an earlier source-pack layout. `REPRODUCIBILITY.md` now supplies executable commands using the current repository paths and distinguishes the current manifest from historical inventories. Missing originals are still recorded as missing.
5. The committed nine-page PDF omitted the source's Huang--Chang scope paragraph and the Meng/Huang--Chang bibliography entries. Two-pass compilation of the unchanged current LaTeX source produces the synchronized ten-page PDF. The source's independent-review and priority reservations remain present; the PDF is updated rather than changing the mathematics.
6. Every current publication entry point now distinguishes permission to merge a repository correction from permission to deposit an exact future archive. Funding/competing-interest declarations, final metadata and archive-specific checks remain prerequisites, with no assumed declarations or identifiers.

## Rights and sensitivity findings

The starting repository contained 58 tracked files. Its manifest listed all 57 files other than the manifest itself. The examination covered readable files, all ten member files in the two historical ZIPs, JSON data and the manuscript PDF text/metadata. Both ZIPs passed CRC and all eight internal SHA-256 entries. The PDF contained no embedded file attachments.

| Category | Existing grant / treatment | Audit finding |
|---|---|---|
| Original Python and GitHub configuration | MIT; `LICENSE.md` and full `LICENSES/MIT.txt` | Categories and attribution are documented; the stated author authorization is dated 5 October 2026. |
| Original manuscript, proofs, documentation, examples and data | CC BY 4.0; `LICENSE.md` links the licence and legal code | Code and research text/data remain separately licensed. |
| Historical ZIP members | Original code uses the code grant; original notes/results use the text/data grant; historical bytes and provenance retained | Contents are project scripts, notes, numerical certificates, readme texts and manifests. No bundled third-party article or vendored dependency was identified. |
| Bibliographic references and external dependencies | Third-party rights retained; no ownership transferred | References/links do not relicense cited publications. Legacy NetworkX imports do not bundle its source. |
| Author identity and AI assistance | Existing public author/affiliation/ORCID declarations; `AI_ASSISTANCE.md` and manuscript disclosure | Recorded, without claiming an independent identity verification or human review. |

Text and metadata inspection identified no FCI implementation, patent/industrial dossier, private correspondence, credentials, private email/phone details or private filesystem paths. Names in authorship/bibliographic citations are public scholarly attribution, not a clearance of unrelated personal records. Keyword/pattern checks support the content examination; they do not establish ownership, undisclosed patent status or clearance of uninspected external files. No newly recovered Drive material or internal correspondence is added by this PR.

This is sufficient documentary evidence for the bounded repository correction. The actual selected archive and any additional materials still require their own rights/sensitivity check under Gate Z. The existing licence grants are preserved, not expanded to unknown third-party content.

## Technical verification and limits

- Local Python 3.12.14 base verifier: all checks passed; p=3/5/7/11 bounds 120/30/20/12, respectively; 13,019 HNF cases with zero mismatches and nine exact matrix examples.
- All six tracked JSON files and both ZIP-contained result JSON files were parsed. Historical file/ZIP integrity checks passed before changes; the manifest is regenerated after the corrections and this audit are added.
- The current LaTeX source compiled twice successfully with `pdflatex`; the generated PDF is checked for its restored literature paragraph/references and rendered for visual inspection. No mathematical source is edited by this synchronization.
- Additional p3-to-120/mixed/416 reproduction commands are documented, but are not claimed to have been rerun in this audit. The current workflow does not execute those three commands or the long historical `inject.py` scan. Missing historical originals and reused-encoder limitations remain explicit.
- A final successful `verify` run on the correction head, including its manifest and build, is required before this PR is marked ready. Check PR head/base and mergeability again at that point; any later file change invalidates this readiness assessment until checked.

## Decision boundaries

| Action / status | Decision |
|---|---|
| Finalize governance PR for review / potential merge | GO once the correction head's checks pass and no new unresolved review or merge conflict appears. |
| Gate Z: upload or assign a Cayley DOI | HOLD. No frozen archival package, final metadata, archive checksum or complete author funding/competing-interest declarations are supplied here. |
| Independent human mathematical validation | OPEN. No reviewer approval is invented from CI, this audit or PR readiness. |
| General novelty / priority | N = NON AUDITEE. Known overlaps and the claim boundary remain explicit. |
| Stable scientific v1.0.0, HAL, arXiv | NO-GO under the existing stable-release and platform restrictions. |

No upload, DOI reservation/creation, GitHub release, tag or automatic archival integration is performed by this correction. Merge is a repository maintenance decision; it does not certify the general proofs, close the priority audit or approve a future Zenodo deposit.
