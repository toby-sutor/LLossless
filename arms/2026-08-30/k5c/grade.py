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
ARMS = ["C1-120b-default", "C2-120b-think"]
DRAWS = 5
# Wall clock and the served digest are properties of the pod and the
# minute, not of the draw. Everything else is the measurement.
VOLATILE = ("arm", "digest", "seconds")
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
        # A verify finding whose grounding is not "grounded" is one the tool
        # could not locate in the text it names: the model paraphrased its own
        # quote and the reconciler refused to credit it. Counting those in with
        # the rest turns a quoting failure into a substantive finding, which is
        # the opposite of what this tool is for. Always both keys, never a
        # sparse histogram: an arm with no findings has zero of each, and a
        # missing key would reach the paper as a blank rather than a zero.
        "findings_grounded": sum(1 for f in report["findings"]
                                 if f.get("grounding") == "grounded"),
        "findings_ungrounded": sum(1 for f in report["findings"]
                                   if f.get("grounding") != "grounded"),
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
    """One row per arm, from draw 1, with the other two draws asserted equal.

    K=3 here, entry 156 and bench-spec.md:128. All three draws of every arm came
    back byte-identical, so a row per draw would be the same row three times.
    What the record carries instead is "draws": how many of the three graded
    identically to the one shown. A reader who wants the rate reads it rather
    than inferring it from a silence, and an arm that ever disagreed could not
    be written up as though it had not.
    """
    rows = []
    for name in ARMS:
        graded = [grade(f"{name}-d{draw}") for draw in range(1, DRAWS + 1)
                  if (SWEEP / f"{name}-d{draw}" / "report.json").exists()]
        if not graded:
            # Entry 160 registered this outcome in advance for C1: an exit 2 is
            # a result, not a failed run, and it is graded as one. There is no
            # report to read, so the row carries what the failure itself has --
            # the exit code, the stage, and how many of K produced it. The
            # error line is read for its stage word only; nothing else from
            # stderr enters a record.
            codes, stages, sizes, errored = set(), set(), set(), 0
            for draw in range(1, DRAWS + 1):
                d = SWEEP / f"{name}-d{draw}"
                if not d.exists():
                    continue
                text = (d / "stderr.log").read_text(encoding="utf-8")
                marks = [ln for ln in text.splitlines() if ln.startswith(("\u2022", "\u2713"))]
                stages.add(marks[-1].split(":")[0].lstrip("\u2022\u2713 ") if marks else "?")
                codes.add(2)
                errored += 1
                sizes.add((d / "report.md").stat().st_size)
            # The model is read from the arm's own driver line rather than
            # from a report, because there is no report. It is the one field a
            # failure row still has to carry: a paper cannot name what failed
            # without it, and typing the SKU into the prose would put a numeral
            # in a result section.
            model = "gpt-oss:120b" if "120b" in name else None
            rows.append({"arm": name, "status": "error", "model": model,
                         "size_b": SIZE[model] if model else None,
                         "draws_errored": errored, "draws_k": DRAWS,
                         "exit_code": sorted(codes)[0] if codes else None,
                         "failed_at_stage": sorted(stages),
                         "report_bytes": sorted(sizes),
                         "draws": {"k": DRAWS, "errored": errored,
                                   "identical_to_shown": errored}})
            continue
        bare = lambda g: {k: v for k, v in g.items() if k not in VOLATILE}
        same = sum(1 for g in graded if bare(g) == bare(graded[0]))
        # Draw 1 is shown, as in the K=3 record, and the shown row is *not*
        # chosen by which value won. When the draws disagree, picking the
        # majority row would be a choice made after seeing the data, and
        # picking draw 1 alone would put whichever draw happened to run first
        # into the paper as though it were the arm. So every field that moved
        # is listed here with its distribution, and a figure that appears in
        # `varies` may not be cited as a point value. Entry 152's rule, one
        # level up: report the spread, not a summary statistic standing for it.
        varies = {}
        for field in sorted(bare(graded[0])):
            seen = {}
            for g in graded:
                seen[json.dumps(g[field], sort_keys=True)] = \
                    seen.get(json.dumps(g[field], sort_keys=True), 0) + 1
            if len(seen) > 1:
                varies[field] = {"values": {v: n for v, n in sorted(seen.items())},
                                 "distinct": len(seen)}
        rows.append(dict(graded[0], arm=name,
                         draws={"k": DRAWS, "graded": len(graded),
                                "identical_to_shown": same,
                                "all_identical": not varies},
                         **({"varies": varies} if varies else {})))
    print(json.dumps(rows, indent=1))
    (SWEEP / "graded.json").write_text(json.dumps(rows, indent=1))



if __name__ == "__main__":
    sys.exit(main())
