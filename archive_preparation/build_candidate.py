#!/usr/bin/env python3
"""Create a local 0.1.x UNREVIEWED archive candidate from a frozen Git commit.
This script never uploads, publishes, creates a release, reserves a DOI, or creates a tag.
"""
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import zipfile

SOURCE_SHA = "5b5da644038452e9e6cce598b6703e713550e2a9"
REPOSITORY = "alexcour/cayley-prime-translation-cospectrality"
VERSION = "0.1.3-review"
ROOT = "cayley-prime-translation-cospectrality_0.1.3-review_UNREVIEWED_CANDIDATE"

def call(*argv):
    return subprocess.check_output(list(argv), text=True).strip()

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def js(raw):
    return (json.dumps(raw, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()

def main(source, output):
    source = Path(source).resolve()
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    sha = call("git", "-C", str(source), "rev-parse", "HEAD")
    assert sha == SOURCE_SHA, f"Refusing to package unexpected commit: {sha}"
    assert call("git", "-C", str(source), "status", "--porcelain") == "", "Dirty working tree"
    assert (source / "VERSION").read_text().strip() == VERSION
    names = [x.decode() for x in subprocess.check_output(["git", "-C", str(source), "ls-files", "-z"]).split(b"\x00") if x]
    assert len(names) == 59 and len(names) == len(set(names)), "Unexpected Git tree; do not publish"
    entries = {}
    for name in names:
        p = PurePosixPath(name)
        assert not p.is_absolute() and ".." not in p.parts and (source / name).is_file()
        entries[name] = (source / name).read_bytes()
    expected = {}
    for line in entries["SHA256SUMS.txt"].decode().splitlines():
        h, name = line.split("  ", 1)
        assert name not in expected and re.fullmatch(r"[a-f0-9]{64}", h)
        expected[name] = h
    assert len(expected) == 58 and set(expected) == set(names) - {"SHA256SUMS.txt"}
    assert all(digest(entries[name]) == h for name,h in expected.items()), "Repository manifest failed"
    assert b"NO-GO" in entries["docs/RELEASE_GATE.md"] and b"HOLD" in entries["docs/RELEASE_GATE.md"]
    assert b"NON AUDITEE" in entries["PUBLICATION_STATUS.md"]
    assert b"MIT" in entries["LICENSE.md"] and b"CC BY 4.0" in entries["LICENSE.md"]
    assert b"NOT PEER REVIEWED" in entries["docs/RELEASE_GATE.md"]
    assert "Huang" in entries["manuscript/structured_cayley.tex"].decode() and "Meng" in entries["manuscript/structured_cayley.tex"].decode()
    for name,raw in entries.items():
        if name.endswith(".json"):
            json.loads(raw)
    nested = []
    for name,raw in entries.items():
        if not name.endswith(".zip"):
            continue
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            assert z.testzip() is None, "Bad historical ZIP CRC"
            for member in z.infolist():
                p = PurePosixPath(member.filename)
                assert not p.is_absolute() and ".." not in p.parts
                if member.is_dir():
                    continue
                body = z.read(member)
                if member.filename.endswith(".json"):
                    json.loads(body)
                licence = "MIT (original code)" if member.filename.endswith(".py") else "CC BY 4.0 (original text/data)" if member.filename.endswith((".txt",".md",".json",".csv")) else "rights review required"
                nested.append({"zip":name,"member":member.filename,"bytes":len(body),"sha256":digest(body),"license_category":licence})
    security = []
    for name,raw in entries.items():
        if name.endswith((".pdf",".zip")):
            continue
        s = raw.decode("utf-8", "replace")
        for term,pattern in [
            ("private key",r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            ("GitHub token",r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
            ("Google API key",r"\bAIza[A-Za-z0-9_-]{30,}\b")
        ]:
            if re.search(pattern,s):
                security.append({"file":name,"kind":term})
    assert not security, "Potential secret in selected files"
    pdf_status = {"extraction":"not installed"}
    if shutil.which("pdfinfo") and shutil.which("pdftotext"):
        p = source / "manuscript/structured_cayley.pdf"
        info = call("pdfinfo", str(p))
        page = re.search(r"(?m)^Pages:\s*(\d+)", info)
        txt = call("pdftotext", "-layout", str(p), "-")
        pdf_status={"pages":int(page.group(1)) if page else None,"meng_mentioned":"Meng" in txt,"huang_mentioned":"Huang" in txt}
        assert pdf_status["pages"] == 10 and pdf_status["meng_mentioned"] and pdf_status["huang_mentioned"], pdf_status
    author = """# AUTHOR CONFIRMATION REQUIRED — no assumed answers

1. Confirm exact author name, affiliation and ORCID as listed in CITATION.cff.
2. Declare actual funding or affirm none, in the author's own words. UNANSWERED.
3. Declare actual financial/non-financial competing interests or affirm none. UNANSWERED.
4. Attest to ownership/licensing of original text, code, data and the contents of historical ZIP files. PENDING.
5. Personally clear the exact archive bytes for private data, FCI/patent material, restricted quotations and other third-party rights. PENDING.
6. Confirm the scope of the AI-assistance disclosure for this exact work. PENDING.
7. Approve exact archive checksum and final metadata separately before any deposit. NOT AUTHORIZED.

No DOI, release or external deposition is authorized by this candidate.
"""
    gate = """# GATE Z CANDIDATE — HOLD

1. Source/provenance: TECHNICAL PASS, exact 59 Git-tracked files; missing historical originals remain disclosed.
2. Manifest/data/ZIP integrity: TECHNICAL PASS for frozen source and candidate entries. See external ZIP SHA-256 and CI workflow replay. Mixed/416 and lengthy historical scans are not rerun by this minimal workflow.
3. E/N/Q and claim boundary: DOCUMENTED. E is internal proof status, N = NON AUDITEE; human mathematical review remains open. Finite checks do not prove a universal theorem.
4. Confidentiality/third-party rights: AUTOMATED SCREEN ONLY. Author's manual clearance remains OPEN.
5. MIT/CC BY 4.0 category licensing: DOCUMENTED; author verification, funding, competing interests, historical contents rights and AI disclosure confirmation remain OPEN.
6. Version/commit/author/keywords and ZIP checksum: RECORDED; actual repository mixed-license handling on Zenodo, final metadata, approval and any DOI remain OPEN.

OVERALL = HOLD. Not peer reviewed. No claim of novelty or priority. No permission for a release, tag, HAL/arXiv, stable v1.0.0 or Zenodo deposit.
"""
    metadata = {
        "archive_label": "UNREVIEWED RESEARCH ARCHIVE / NOT PEER REVIEWED",
        "title": "Cospectrality of a structured three-element support under prime cyclic translation — UNREVIEWED RESEARCH ARCHIVE / NOT PEER REVIEWED",
        "version": VERSION, "source_commit": SOURCE_SHA,
        "source_url": "https://github.com/"+REPOSITORY+"/commit/"+SOURCE_SHA,
        "creators": [{"name":"Couret, Alexandre","orcid":"0009-0000-8246-7146","affiliation":"Independent researcher, France","status":"from CITATION.cff; author to confirm"}],
        "keywords":["Cayley digraphs","cospectrality","roots of unity","finite abelian groups","circulants"],
        "language":"en", "resource_type":"unreviewed research work archive / working paper + finite verification code/data",
        "abstract":"Unreviewed working manuscript, theorem witness texts and supporting finite checks for a structured support-translation family in finite abelian groups. Known earlier overlap is disclosed. Human mathematical review and broader antecedence checks remain open.",
        "rights":{"original_project_code_workflows":"MIT","original_manuscript_proofs_docs_data":"CC BY 4.0","third_party":"rights retained","historical_zip":"per member as inventoried"},
        "peer_reviewed":False, "independent_review":"PENDING", "priority":"N = NON AUDITEE",
        "funding":None,"competing_interests":None,"doi":None,"zenodo_record_id":None,
        "publication_date":None,"author_clearance":"PENDING","gate_z":"HOLD",
        "note":"Metadata draft, not a valid Zenodo submission. A DOI, if later created by the author, identifies deposited bytes rather than validating mathematics."
    }
    rows=[]
    for name,raw in sorted(entries.items()):
        lic = "MIXED BY MEMBER" if name.endswith(".zip") else "MIT" if name.endswith(".py") or name.startswith(".github/") else "LICENSE DOCUMENT" if name.startswith("LICENSE") else "CC BY 4.0 — ORIGINAL CONTRIBUTIONS ONLY"
        role = "manuscript" if name.startswith("manuscript/") else "proof" if name.startswith("proofs/") else "code/results/provenance" if name.startswith("reproducibility/") else "status/licence/research"
        rows.append({"path":name,"bytes":len(raw),"sha256":digest(raw),"license_category":lic,"role":role,"source_commit":SOURCE_SHA})
    outcsv=io.StringIO(newline="")
    w=csv.DictWriter(outcsv,fieldnames=list(rows[0]),lineterminator="\n")
    w.writeheader();w.writerows(rows)
    readme = """UNREVIEWED RESEARCH ARCHIVE / NOT PEER REVIEWED — CANDIDATE ONLY

Source: https://github.com/""" + REPOSITORY + """/commit/""" + SOURCE_SHA + """
Version: """ + VERSION + """
All 59 tracked repository files have been preserved byte-for-byte.
This candidate retains manuscript, proof witnesses, exact-verification and reproduction scripts, finite results, examples, original historical containers, provenance, README/claim boundary/prior art/status, MIT and CC BY 4.0 licensing documents, CI workflow, and review instructions.

From extracted archive root: sha256sum -c archival/FILE_SHA256SUMS.txt
                       sha256sum -c SHA256SUMS.txt
                       python3 reproducibility/verify_exact.py --output /tmp/results_local.json
Additional optional drivers and missing-original distinctions: see REPRODUCIBILITY.md.

The archive hash is outside the ZIP in CANDIDATE_SHA256SUMS.txt.
No DOI, tag, stable release or deposit was created. Human independent proof review pending; N = NON AUDITEE.
Documented Brown / Monius overlap and pending Meng / Huang-Chang source comparisons are retained.
Funding/conflicts, author clearance and final licence mapping remain unanswered.
"""
    controls = {
       "archival/ARCHIVE_README.txt": readme.encode(),
       "archival/METADATA_DRAFT.json":js(metadata),
       "archival/AUTHOR_DECLARATIONS_REQUIRED.md":author.encode(),
       "archival/GATE_Z_CANDIDATE.md":gate.encode(),
       "archival/SOURCE_INVENTORY.csv":outcsv.getvalue().encode(),
       "archival/NESTED_ZIP_INVENTORY.json":js(nested),
       "archival/SENSITIVITY_PRELIMINARY.json":js({"high_confidence_secret_matches":security,"scope":"text files in tracked checkout; existing 2026-10-11 documentary audit covers historical ZIPs; no manual clearance","status":"PRELIMINARY_ONLY"}),
       "archival/PDF_SPOT_CHECK.json":js(pdf_status),
       "archival/build_candidate.py":Path(__file__).read_bytes()
    }
    entries.update(controls)
    entries["archival/FILE_SHA256SUMS.txt"]="".join(digest(raw)+"  "+name+"\n" for name,raw in sorted(entries.items())).encode()
    dest=output/(ROOT+".zip")
    with zipfile.ZipFile(dest,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(entries.items()):
            zi=zipfile.ZipInfo(ROOT+"/"+name,(1980,1,1,0,0,0))
            zi.create_system=3
            zi.external_attr=0o100644 << 16
            zi.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(zi,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None and len(z.namelist())==len(entries)
        for name,raw in entries.items():
            assert z.read(ROOT+"/"+name)==raw
    h=digest(dest.read_bytes())
    (output/"CANDIDATE_SHA256SUMS.txt").write_text(h+"  "+dest.name+"\n")
    build={"zip":dest.name,"archive_sha256":h,"bytes":dest.stat().st_size,"source_sha":sha,
           "source_files":len(names),"archive_entries":len(entries),"checked_repo_sha256":len(expected),
           "nested_zip_members":len(nested),"pdf_status":pdf_status,"python":sys.version,
           "gate_z":"HOLD","no_release_or_doi":True,
           "limitations":["Author funding/conflicts and rights statements missing","No independent mathematical review","Novelty and priority N = NON AUDITEE","No final manual sensitivity clearance","No Zenodo upload approval"]}
    (output/"BUILD_REPORT.json").write_bytes(js(build))
    print(json.dumps(build,indent=2))

if __name__ == "__main__":
    if len(sys.argv)!=3:
        raise SystemExit("Usage: python build_candidate.py EXACT_CHECKOUT OUTDIR")
    main(sys.argv[1],sys.argv[2])
