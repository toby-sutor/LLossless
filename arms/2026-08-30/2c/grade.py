#!/usr/bin/env python3
"""Grade the three honesty arms over the PUBLIC pair. Numbers only.

Adapted from the 2026-08-28 sweep's own grader, so the two records are
comparable field for field. Two fields added, both absent from the original
because neither existed then: `digest`, the served model identity read from
`/api/ps` either side of the arm, and `tokens`, the normalised usage the run
now captures. `build_numbers.py` ignores both and reads the rest unchanged.

The numbers-only rule is kept even though this corpus is publishable, so that
the two records stay comparable: no claim text, no span, no evidence, no
finding detail. Only counts, ratios and byte totals leave this script.
"""
import json, pathlib, sys

SWEEP = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("<home>/Documents/Dev/vibe-coding/claimcheck")
PAIR = ROOT / "tests" / "pairs" / "index_429"
ARMS = ["A1-27b-default", "B1-70b-default", "C2-120b-think"]
SIZE = {"qwen3.8:27b": 27, "deepseek-r1:70b": 70, "gpt-oss:120b": 120}


def union_bytes(spans, haystack):
    """Bytes of `haystack` covered by the union of the spans found in it."""
    covered = []
    for span in spans:
        if not span:
            continue
        at = haystack.find(span)
        if at < 0:
            continue
        covered.append((at, at + len(span)))
    covered.sort()
    total, end_so_far = 0, -1
    for start, end in covered:
        start = max(start, end_so_far)
        if end > start:
            total += end - start
            end_so_far = end
    return total


def census(report, texts):
    """A.33's two span figures, per document: bytes per claim, union coverage."""
    out = {}
    for doc in sorted({c["source"] for c in report["claims"]}):
        claims = [c for c in report["claims"] if c["source"] == doc]
        spans = [c.get("span") or "" for c in claims]
        prose = texts.get(doc, "")
        out[doc] = {
            "claims": len(claims),
            "span_bytes_per_claim": round(sum(len(s) for s in spans) / len(claims), 1),
            "union_coverage": round(union_bytes(spans, prose) / len(prose), 4) if prose else None,
            "anchored": round(sum(1 for c in claims if c["anchored"]) / len(claims), 4),
        }
    return out


def grade(name):
    d = SWEEP / name
    report = json.loads((d / "report.json").read_text())
    merged = (d / "merged.md").read_text() if (d / "merged.md").exists() else ""
    texts = {
        "source_a.md": (PAIR / "source_a.md").read_text(),
        "source_b.md": (PAIR / "source_b.md").read_text(),
        "merged.md": merged,
    }
    prov, cov = report["provenance"], report["coverage"]
    verdicts = {}
    for v in report["verdicts"]:
        verdicts[v["verdict"]] = verdicts.get(v["verdict"], 0) + 1
    counts = prov["counts"]
    return {
        "arm": name,
        "model": prov["models"]["merge"],
        "size_b": SIZE[prov["models"]["merge"]],
        "thinking_requested": prov["decoding"]["thinking"],
        "reasoned_anyway": prov["decoding"].get("reasoned_anyway"),
        "field_order": prov["structured_output"]["field_order"],
        "tier": prov["structured_output"]["mode"],
        "exit_code": report["exit_code"],
        "merged_bytes": len(merged),
        "structural": {
            "ran": report["structural"]["ran"],
            "checks": report["structural"]["checks"],
            "segments": report["structural"]["segments"],
            "findings": len(report["structural"]["findings"]),
            # Kind and segment id only. A structural finding's `detail` quotes
            # the document it was found in, and no document text leaves here.
            "by_kind": {k: sum(1 for f in report["structural"]["findings"] if f["kind"] == k)
                        for k in sorted({f["kind"] for f in report["structural"]["findings"]})},
            "segments_hit": sorted({f["segment"] for f in report["structural"]["findings"]}),
        },
        "declared_loss": report["declared_loss"],
        "findings": len(report["findings"]),
        "findings_by_kind": {k: sum(1 for f in report["findings"] if f.get("verdict", f.get("kind")) == k)
                             for k in sorted({f.get("verdict", f.get("kind")) for f in report["findings"]})},
        "verdicts": verdicts,
        "extracted": cov["extracted"],
        "graded": cov["graded"],
        "grounded": cov["grounded"],
        "errored": cov["errored"],
        "review_queue": len(report["review_queue"]),
        "census": census(report, texts),
        "calls": counts["calls"],
        "schema_repairs": counts["schema_repairs"],
        "completion_tokens": counts["completion_tokens"],
        "seconds": prov["duration_seconds"],
        # New since the baseline. The served identity, asserted equal either
        # side of the arm: a model swapped mid-arm would otherwise be invisible.
        "digest": served_digest(d, prov["models"]["merge"]),
        "tokens": prov.get("tokens"),
        "tokens_described": prov.get("tokens_described"),
    }


def served_digest(d, model):
    """The digest from /api/ps before and after. Disagreement is a refusal."""
    seen = {}
    for when in ("before", "after"):
        path = d / f"ps-{when}.json"
        if not path.exists():
            continue
        for entry in json.loads(path.read_text()).get("models", []):
            if entry["name"] == model:
                seen[when] = entry["digest"]
    if len(set(seen.values())) > 1:
        raise SystemExit(f"{d.name}: {model} digest moved mid-arm: {seen}")
    return {"sha256": next(iter(seen.values()), None), "seen_at": sorted(seen)}


def main():
    rows = []
    for name in ARMS:
        if (SWEEP / name / "report.json").exists():
            rows.append(grade(name))
        else:
            rows.append({"arm": name, "status": "not run"})
    print(json.dumps(rows, indent=1))
    (SWEEP / "graded.json").write_text(json.dumps(rows, indent=1))
    # The paper reads this one. Named `sweep-pair429` so its keys land at
    # `sweep.pair429.<arm>.*`.
    (ROOT / "paper" / "records" / "sweep-pair429.json").write_text(
        json.dumps(rows, indent=1))


if __name__ == "__main__":
    sys.exit(main())
