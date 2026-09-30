#!/usr/bin/env python3
"""Phase 4 measurement run orchestrator. Never prints the API key or endpoint URL."""
import json, os, pathlib, re, shutil, subprocess, sys, time, urllib.request, urllib.error

REPO = pathlib.Path("<home>/Documents/Dev/vibe-coding/claimcheck")
SRC = REPO / "src"
PAIRS_ROOT = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck")
OUT_ROOT = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-16-phase4")
SCRATCH = pathlib.Path("/tmp/cc-phase4-run")
RESULTS_PATH = OUT_ROOT / "results.json"

PAIRS = [
    ("toby-test-2", "chickens_1.md", "chickens_2.md"),
    ("toby-test-4", "christianity_1.md", "christianity_2.md"),
    ("toby-test-5", "curry_1.md", "curry_2.md"),
]
LEVELS = ["low", "high"]

# endpoint key -> (model id, slug for directory names)
ENDPOINTS = [
    ("vllm", "Qwen/Qwen3.8-27B-FP8", "27b-fp8"),
    ("vllm-qwen3-8b", "qwen/qwen3-8b", "8b"),
]


def load_env_creds():
    text = (REPO / ".env").read_text()
    creds = {}
    for line in text.splitlines():
        name, _, val = line.strip().partition("=")
        name = name.strip()
        if name not in ("vllm", "vllm-qwen3-8b"):
            continue
        m_url = re.search(r"https://api\.<redacted>\.ai/v2/[a-z0-9]+", val)
        m_key = re.search(r"Bearer\s+([A-Za-z0-9_\-]+)", val)
        if not m_url or not m_key:
            raise RuntimeError(f"could not parse credentials for key {name!r}")
        creds[name] = (m_url.group(0), m_key.group(1))
    return creds


def health_check(base_url, api_key, tries=1, wait=10):
    """Return (ok: bool, detail: str) without ever printing the key."""
    url = base_url.rstrip("/") + "/health"
    last_detail = ""
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode())
            workers = body.get("workers", {})
            ready = workers.get("ready", None)
            last_detail = json.dumps(workers)
            if ready and ready > 0:
                return True, last_detail
        except Exception as e:
            last_detail = f"{type(e).__name__}: {e}"
        if attempt < tries - 1:
            time.sleep(wait)
    return False, last_detail


def append_result(record):
    if RESULTS_PATH.exists():
        data = json.loads(RESULTS_PATH.read_text())
    else:
        data = []
    data.append(record)
    RESULTS_PATH.write_text(json.dumps(data, indent=2))


def run_one(endpoint_key, base_url, api_key, model_id, model_slug, pair_id, a_name, b_name, level):
    run_dir_name = f"{pair_id}-{level}-{model_slug}"
    run_out = OUT_ROOT / run_dir_name
    run_out.mkdir(parents=True, exist_ok=True)

    work = SCRATCH / f"work-{run_dir_name}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    pair_src = PAIRS_ROOT / pair_id
    shutil.copy(pair_src / a_name, work / a_name)
    shutil.copy(pair_src / b_name, work / b_name)

    json_out = work / "report.json"
    md_out = work / "merged.md"

    cmd = [
        sys.executable, "-m", "claimcheck", "merge", a_name, b_name,
        "--base", a_name,
        "--fidelity", level,
        "--window", "32768",
        "--field-order", "any",
        "--timeout", "400",
        "--no-cache",
        "--json", str(json_out),
        "-o", str(md_out),
    ]

    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    env["CLAIMCHECK_API_KEY"] = api_key
    env["CLAIMCHECK_BASE_URL"] = base_url.rstrip("/") + "/openai/v1"
    env["CLAIMCHECK_MODEL"] = model_id
    env["CLAIMCHECK_MERGE_MODEL"] = model_id

    print(f">>> RUN {run_dir_name} starting", flush=True)
    # Generous ceiling: cold start alone is 230-345s, and a merge run makes
    # several sequential role calls (merge, one decompose per source, verify
    # batches), each allowed up to --timeout 400s. 2400s gives headroom for a
    # cold start plus several near-max-timeout calls without falsely reporting
    # a tooling timeout as an endpoint failure. Runs in its own process group
    # so a kill (ours or a manual one) always takes the whole tree, never
    # leaving an orphaned live call running against the endpoint.
    PROC_TIMEOUT = 2400
    t0 = time.time()
    proc = subprocess.Popen(
        cmd, cwd=work, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=PROC_TIMEOUT)
        exit_code = proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), 9)
        stdout, stderr = proc.communicate()
        exit_code = None
        timed_out = True
    wall_seconds = time.time() - t0

    # persist stdout/stderr and any produced artefacts into the output dir
    (run_out / "stdout.txt").write_text(stdout or "")
    (run_out / "stderr.txt").write_text(stderr or "")
    if json_out.exists():
        shutil.copy(json_out, run_out / "report.json")
    if md_out.exists():
        shutil.copy(md_out, run_out / "merged.md")

    record = {
        "run_dir": run_dir_name,
        "endpoint_key": endpoint_key,
        "model": model_id,
        "pair": pair_id,
        "fidelity": level,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "wall_seconds": round(wall_seconds, 1),
    }

    report = None
    if (run_out / "report.json").exists():
        try:
            report = json.loads((run_out / "report.json").read_text())
        except Exception as e:
            record["report_parse_error"] = f"{type(e).__name__}: {e}"

    if report is not None:
        prov = report.get("provenance") or {}
        record["endpoint_id"] = (prov.get("endpoint") or {}).get("id")
        tokens = prov.get("tokens") or {}
        record["tokens_in"] = tokens.get("input")
        record["tokens_out"] = tokens.get("output")
        calls_by_role = prov.get("calls_by_role") or {}
        record["calls_by_role"] = calls_by_role
        record["calls_by_role_has_zero"] = any(v == 0 for v in calls_by_role.values())
        record["errors"] = (prov.get("counts") or {}).get("errors")
        record["schema_repairs"] = (prov.get("counts") or {}).get("schema_repairs")

        coverage = report.get("coverage") or {}
        extracted = coverage.get("extracted")
        if isinstance(extracted, dict):
            record["claims_extracted"] = sum(extracted.values())
        else:
            record["claims_extracted"] = len(report.get("claims") or [])

        # findings split by kind, using reconcile's own frozensets
        sys.path.insert(0, str(SRC))
        from claimcheck.reconcile import DOCUMENT_FINDINGS, RECORD_FINDINGS  # noqa: E402
        structural_findings = ((report.get("structural") or {}).get("findings")) or []
        doc_from_structural = sum(1 for f in structural_findings if f.get("kind") in DOCUMENT_FINDINGS)
        rec_from_structural = sum(1 for f in structural_findings if f.get("kind") in RECORD_FINDINGS)
        other_structural = sum(
            1 for f in structural_findings
            if f.get("kind") not in DOCUMENT_FINDINGS and f.get("kind") not in RECORD_FINDINGS
        )
        claim_level_findings = report.get("findings") or []  # document faults by construction, no `kind`
        record["findings_document"] = doc_from_structural + len(claim_level_findings)
        record["findings_record"] = rec_from_structural
        if other_structural:
            record["findings_structural_unclassified"] = other_structural

    # merged_chars from the actual merged.md file, and combined source chars
    if (run_out / "merged.md").exists():
        record["merged_chars"] = len((run_out / "merged.md").read_text())
    combined = (work / a_name).read_text() if (work / a_name).exists() else ""
    combined += (work / b_name).read_text() if (work / b_name).exists() else ""
    record["combined_source_chars"] = len(combined)
    if record.get("merged_chars") and record["combined_source_chars"]:
        record["length_ratio"] = round(record["merged_chars"] / record["combined_source_chars"], 3)

    if not timed_out and exit_code not in (0, 1, 3):
        record["operational_error"] = True
        record["stderr_tail"] = (stderr or "")[-2000:]

    append_result(record)
    print(f"<<< RUN {run_dir_name} done: exit={exit_code} wall={wall_seconds:.0f}s "
          f"zero_role={record.get('calls_by_role_has_zero')}", flush=True)
    shutil.rmtree(work, ignore_errors=True)
    return record


def main():
    creds = load_env_creds()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    for endpoint_key, model_id, model_slug in ENDPOINTS:
        base_url, api_key = creds[endpoint_key]
        print(f"=== endpoint {endpoint_key} ({model_slug}): health check ===", flush=True)
        ok, detail = health_check(base_url, api_key, tries=3, wait=20)
        print(f"=== health: ok={ok} detail={detail} ===", flush=True)
        if not ok:
            print(f"=== endpoint {endpoint_key} not ready after retries; waiting longer ===", flush=True)
            ok, detail = health_check(base_url, api_key, tries=6, wait=60)
            print(f"=== health retry: ok={ok} detail={detail} ===", flush=True)

        for pair_id, a_name, b_name in PAIRS:
            for level in LEVELS:
                run_one(endpoint_key, base_url, api_key, model_id, model_slug,
                        pair_id, a_name, b_name, level)

    print("=== all runs complete ===", flush=True)


if __name__ == "__main__":
    main()
