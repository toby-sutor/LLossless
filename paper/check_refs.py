#!/usr/bin/env python3
"""Refuse a bibliography entry nobody verified.

The rule: a citation written from recollection is either
verified against a stable identifier or deleted, together with the sentence
that cites it. This file is the "or the build fails" half of that.

Three things are checked:

  verified field   every entry carries `verified`, saying how and when. An
                   entry without one is a citation somebody typed.
  identifier       every entry carries `eprint`, an arXiv identifier in the
                   YYMM.NNNNN form.
  brace-protected  every `title` is wrapped in a second pair of braces. Without
                   them `plainnat` sentence-cases the title, and the PDF said
                   "Factscore", "Halueval", "Selfcheckgpt" and "llm-as-a-judge
                   with mt-bench" -- the entry held the record verbatim and the
                   reader saw a restyling of it, which is the half a
                   source-level comparison cannot see.
  cited            every entry is cited by some section, and every citation has
                   an entry. BibTeX refuses the second case loudly and drops
                   the first silently, which is why it is checked here.
  year agreement   `year` must match the year the identifier encodes. This is
                   the check that catches a mistyped or misremembered year
                   offline, without asking the network at build time -- an
                   arXiv id is self-dating, so the entry contradicts itself
                   and a program can see it.

Those three need no network and run on every commit.

`--online` is the fourth, and it is what makes `verified` a claim with a truth
value. Without it the field says a comparison happened on a date and nothing
can contradict it; a title that was wrong when it was typed stays wrong through
every green run, because the offline checks read the entry against itself and
never against the record. `--online` re-fetches each `eprint` from the arXiv
API and compares title, author list and year to what the entry says.

It is opt-in, and deliberately not in the suite. `tests/run_all.py` invokes this
file with no arguments, the suite is offline by construction, and a gate that
needs a third party to be reachable fails for reasons that are not about this
repository. So the offline checks gate the build and the online one is run by
hand before a release.

Everything except the socket is still checked on every commit. The fetch is one
line; `record_from_atom` and `compare` are pure, and `--self-test` seeds both to
fire and not to -- including the exact defect this project has actually made,
a title reading "Summarization" where the paper says "Summaries".

A passing `--online` run does not rewrite the `verified` field. Recording the
date is a manual act on purpose: a field the program maintains certifies that
the program ran, not that anybody checked, and it would go green against a
comparison nobody read. The run prints the line to paste.

Usage:
    paper/check_refs.py              # check refs.bib, offline
    paper/check_refs.py --self-test  # check the checker, offline
    paper/check_refs.py --online     # re-fetch every entry and compare
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

PAPER = Path(__file__).resolve().parent
ATOM = {"a": "http://www.w3.org/2005/Atom"}
API = "https://export.arxiv.org/api/query?id_list={}&max_results=1"
# arXiv asks for a pause between programmatic requests. Eight entries, so the
# whole run costs half a minute and there is nothing to gain by hurrying it.
PAUSE = 3.0
ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", re.S)
FIELD = re.compile(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\s*(?=\n\s*\w+\s*=|\n?$)", re.S)
ARXIV = re.compile(r"^(\d{2})(\d{2})\.\d{4,5}$")
SECTIONS = PAPER / "sections"
CITE = re.compile(r"\\cite[a-z]*\{([^}]*)\}")


def entries(text):
    """(key, fields) per entry. Comment lines are dropped first."""
    body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("%"))
    out = []
    for _kind, key, fields in ENTRY.findall(body):
        out.append((key, {k: " ".join(v.split()) for k, v in FIELD.findall(fields)}))
    return out


def problems(text):
    found = []
    for key, fields in entries(text):
        if not fields.get("verified"):
            found.append(f"{key}: no `verified` field -- unverified citation")
        title = fields.get("title", "")
        if not (title.startswith("{") and title.endswith("}")):
            found.append(f"{key}: `title` is not brace-protected -- write it "
                         f"{{{{like this}}}}, or the bibliography style will "
                         f"restyle it and the rendered title will not be the "
                         f"verified one")
        eprint = fields.get("eprint", "")
        stamp = ARXIV.match(eprint)
        if not stamp:
            found.append(f"{key}: `eprint` is not an arXiv identifier: {eprint!r}")
            continue
        implied = 2000 + int(stamp.group(1))
        year = fields.get("year", "")
        if year != str(implied):
            found.append(f"{key}: year {year!r} disagrees with eprint {eprint} "
                         f"(which encodes {implied})")
    return found


def cited(tex):
    """Every key cited by a blob of LaTeX, from `\\cite` in any of its forms."""
    return {k.strip() for group in CITE.findall(tex) for k in group.split(",")
            if k.strip()}


def unused(text, tex):
    """Entries nobody cites, and citations with no entry.

    BibTeX already refuses the second direction, loudly. The first it does not:
    an uncited entry is simply dropped from the typeset bibliography, so a
    reference that was researched and verified and then never wired into a
    sentence leaves no trace in the PDF and no complaint anywhere. Checked here
    because the header of `refs.bib` states the relation in one direction only,
    and a bibliography is the wrong place to keep something nothing reads.
    """
    keys = {key for key, _ in entries(text)}
    names = cited(tex)
    return ([f"{k}: verified and in refs.bib, but no section cites it"
             for k in sorted(keys - names)]
            + [f"{k}: cited by a section, but no entry in refs.bib"
               for k in sorted(names - keys)])


def tidy(value):
    """Whitespace collapsed, and BibTeX's own markup removed.

    Braces are capitalisation protection and ``like this\'\' is how LaTeX
    spells a quotation mark, so neither is part of the title. One title here
    really does contain quotation marks, and writing it with straight ones so
    that a string comparison passes would put a wrong-facing quote in the
    typeset bibliography -- the comparison is what should know about LaTeX.
    """
    value = value.replace("``", '"').replace("\'\'", '"')
    return " ".join(value.replace("{", "").replace("}", "").split())


def record_from_atom(blob, eprint):
    """The arXiv record for `eprint`, from one Atom feed. No network here.

    Raises `ValueError` rather than returning a partial record. A feed with no
    entry is what the API returns for an identifier that does not exist -- it
    is a 200 with `totalResults` 0, not an error status -- so a fetch that
    silently produced an empty record would report every field as agreeing
    with nothing.
    """
    entry = ET.fromstring(blob).find("a:entry", ATOM)
    if entry is None:
        raise ValueError(f"the API returned no entry for {eprint}; the "
                         f"identifier does not resolve")
    got = entry.findtext("a:id", "", ATOM)
    if f"/{eprint}v" not in got and not got.endswith(f"/{eprint}"):
        raise ValueError(f"asked for {eprint} and the feed answered about "
                         f"{got!r}")
    return {
        "title": tidy(entry.findtext("a:title", "", ATOM)),
        "authors": [tidy(a.findtext("a:name", "", ATOM))
                    for a in entry.findall("a:author", ATOM)],
        "year": entry.findtext("a:published", "", ATOM)[:4],
    }


def fetch(eprint, timeout=30):
    """`record_from_atom` over the wire. The only line in this file with a socket."""
    with urllib.request.urlopen(API.format(eprint), timeout=timeout) as response:
        return record_from_atom(response.read(), eprint)


def compare(fields, record):
    """Disagreements between one bib entry and the arXiv record. No network.

    Strict: the entries claim to hold the record verbatim, and all of them do,
    so a comparison that forgave case or punctuation would only forgive a
    future entry that does not. The author list is compared in order and by
    length, because a dropped last author is the shape of a citation typed
    from memory.
    """
    out = []
    title = tidy(fields.get("title", ""))
    if title != record["title"]:
        out.append(f"title disagrees\n      bib:   {title}\n      arXiv: {record['title']}")
    claimed = [tidy(a) for a in re.split(r"\s+and\s+", fields.get("author", "")) if a.strip()]
    if claimed != record["authors"]:
        out.append(f"author list disagrees ({len(claimed)} in bib, "
                   f"{len(record['authors'])} on arXiv)\n"
                   f"      bib:   {', '.join(claimed)}\n"
                   f"      arXiv: {', '.join(record['authors'])}")
    if fields.get("year", "") != record["year"]:
        out.append(f"year disagrees: bib {fields.get('year', '')!r}, "
                   f"arXiv record published {record['year']}")
    return out


def online(text, sleep=time.sleep):
    """Re-fetch every entry and compare. Prints a report, returns an exit code."""
    found = problems(text)
    if found:
        for line in found:
            print(f"  FAIL {line}")
        print("\n  refusing to go online: fix the entries above first, since "
              "an entry without a usable identifier has nothing to fetch.")
        return 1

    rows = entries(text)
    bad = 0
    for i, (key, fields) in enumerate(rows):
        if i:
            sleep(PAUSE)
        eprint = fields["eprint"]
        try:
            record = fetch(eprint)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {key} ({eprint}): could not fetch: "
                  f"{type(exc).__name__}: {exc}")
            bad += 1
            continue
        gaps = compare(fields, record)
        if gaps:
            bad += 1
            for gap in gaps:
                print(f"  FAIL {key} ({eprint}): {gap}")
        else:
            print(f"  ok   {key} ({eprint}): title, {len(record['authors'])} "
                  f"author(s) and year match the record")
    if bad:
        print(f"\n  {bad} of {len(rows)} entry(ies) disagree with the arXiv "
              f"record. Correct the entry from the record, or delete it with "
              f"the sentence that cites it.")
        return 1
    print(f"\n  {len(rows)} entry(ies) re-fetched, all agreeing on title, "
          f"author list and year.")
    print(f"  This run is not recorded anywhere. If you read the report above, "
          f"the field to paste is:\n"
          f"    verified      = {{arXiv API id_list, title and author list "
          f"compared {time.strftime('%Y-%m-%d')}}}")
    return 0


# The probes. A checker that has never fired is not known to work, and this
# project has shipped two detectors that were green while blind.
# Each probe carries the phrase its own defect must produce. Asserting only
# that `problems` said something lets a probe pass on an unrelated complaint,
# and one here did exactly that when the brace-protection clause was added:
# every fixture was written with a bare title, so all of them fired twice.
MUST_FIRE = {
    "no verified field": ("""@misc{probe,
  title  = {{A Paper}},
  author = {Nobody},
  year   = {2023},
  eprint = {2305.14251},
  archivePrefix = {arXiv}
}""", "no `verified` field"),
    "year disagrees with the identifier": ("""@misc{probe,
  title    = {{A Paper}},
  author   = {Nobody},
  year     = {2024},
  eprint   = {2305.14251},
  archivePrefix = {arXiv},
  verified = {checked somehow}
}""", "disagrees with eprint"),
    "eprint is not an arXiv identifier": ("""@misc{probe,
  title    = {{A Paper}},
  author   = {Nobody},
  year     = {2023},
  eprint   = {arXiv-2305.14251},
  archivePrefix = {arXiv},
  verified = {checked somehow}
}""", "is not an arXiv identifier"),
    "a title braced closed but not open": ("""@misc{probe,
  title    = {A Paper}},
  author   = {Nobody},
  year     = {2023},
  eprint   = {2305.14251},
  archivePrefix = {arXiv},
  verified = {checked somehow}
}""", "not brace-protected"),
    "a title braced open but not closed": ("""@misc{probe,
  title    = {{A Paper},
  author   = {Nobody},
  year     = {2023},
  eprint   = {2305.14251},
  archivePrefix = {arXiv},
  verified = {checked somehow}
}""", "not brace-protected"),
    "title left for the style to restyle": ("""@misc{probe,
  title    = {A Paper},
  author   = {Nobody},
  year     = {2023},
  eprint   = {2305.14251},
  archivePrefix = {arXiv},
  verified = {checked somehow}
}""", "not brace-protected"),
}
MUST_NOT_FIRE = """@misc{probe,
  title    = {{A Paper}},
  author   = {Nobody},
  year     = {2023},
  eprint   = {2305.14251},
  archivePrefix = {arXiv},
  verified = {arXiv API id_list, compared 2026-08-30}
}"""



# The online half's probes. Every one of them runs offline: the network is one
# line in `fetch`, and everything that decides a verdict is pure and seeded
# here. A mode that is only exercised when someone remembers to run it by hand
# is a mode nobody has run.
#
# `ATOM_REAL` and `ATOM_EMPTY` are the API's actual responses, captured from it:
# for an identifier that does not exist arXiv answers 200 with an entry-less
# feed, which is the reply a naive reader turns into a record that agrees with
# everything.
ATOM_REAL = b"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2004.04228v1</id>
    <title>Asking and Answering Questions to Evaluate the Factual Consistency
  of Summaries</title>
    <published>2020-04-08T20:01:09Z</published>
    <author><name>Alex Wang</name></author>
    <author><name>Kyunghyun Cho</name></author>
    <author><name>Mike Lewis</name></author>
  </entry>
</feed>"""
ATOM_EMPTY = b"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>arXiv Query: search_query=&amp;id_list=0000.00000</title>
</feed>"""
ATOM_OTHER = ATOM_REAL.replace(b"abs/2004.04228v1", b"abs/2305.14251v2")

# The bib side of the same entry, as `entries()` would hand it over.
BIB_TRUE = {
    "title": "Asking and Answering Questions to Evaluate the Factual Consistency of Summaries",
    "author": "Alex Wang and Kyunghyun Cho and Mike Lewis",
    "year": "2020",
}
# Each of these is one plausible way to get an entry wrong. The first is not
# hypothetical: it is the defect this bibliography actually had, caught by hand
# in August and invisible to every offline check in this file.
COMPARE_MUST_FIRE = {
    "a title off by one word (the real QAGS defect)":
        {**BIB_TRUE, "title": BIB_TRUE["title"].replace("Summaries", "Summarization")},
    "the last author dropped":
        {**BIB_TRUE, "author": "Alex Wang and Kyunghyun Cho"},
    "an author name misspelled":
        {**BIB_TRUE, "author": "Alex Wang and Kyunghyu Cho and Mike Lewis"},
    "the authors in a different order":
        {**BIB_TRUE, "author": "Mike Lewis and Alex Wang and Kyunghyun Cho"},
    "a year the identifier happens to agree with":
        {**BIB_TRUE, "year": "2021"},
}


def online_self_test():
    """The online mode's verdict logic, seeded both ways. Opens no socket."""
    bad = []
    try:
        record = record_from_atom(ATOM_REAL, "2004.04228")
    except ValueError as exc:
        return [f"record_from_atom refused a real feed: {exc}"]
    if record != {"title": BIB_TRUE["title"],
                  "authors": ["Alex Wang", "Kyunghyun Cho", "Mike Lewis"],
                  "year": "2020"}:
        bad.append(f"record_from_atom misread a real feed: {record}")

    for name, blob, eprint in [("a feed with no entry", ATOM_EMPTY, "0000.00000"),
                               ("a feed about another paper", ATOM_OTHER, "2004.04228")]:
        try:
            record_from_atom(blob, eprint)
            bad.append(f"record_from_atom accepted {name}")
        except ValueError:
            pass

    one = """@misc{probe,
  title         = {{A Paper}},
  author        = {Nobody},
  year          = {2023},
  eprint        = {2305.14251},
  archivePrefix = {arXiv},
  verified      = {a probe, not a citation}
}"""
    if unused(one, r"text \\citep{probe} more"):
        bad.append("unused fired on an entry that is cited")
    if unused(one, r"\\citet{probe}, and \\citep[see][]{probe}"):
        bad.append("unused fired on an entry cited by \\citet or \\citep[..]")
    if not unused(one, "a section citing nothing at all"):
        bad.append("unused stayed quiet on an entry nobody cites")
    if not unused(one, r"\\citep{probe,ghost}"):
        bad.append("unused stayed quiet on a citation with no entry")
    if not unused("", r"\\citep{ghost}"):
        bad.append("unused stayed quiet on an empty bibliography")
    # Two entries in one `\\citep`. The probes above still fire if the key list
    # is never split on the comma, so without this one the splitting is
    # unproved -- a must-fire probe that fires for the wrong reason is how a
    # blind check looks green.
    two = one + """

@misc{probe2,
  title         = {{Another Paper}},
  author        = {Nobody},
  year          = {2023},
  eprint        = {2305.14251},
  archivePrefix = {arXiv},
  verified      = {a probe, not a citation}
}"""
    if unused(two, r"\\citep{probe,probe2}"):
        bad.append("unused fired on two entries cited in one \\citep")

    for name, fields in COMPARE_MUST_FIRE.items():
        if not compare(fields, record):
            bad.append(f"compare stayed quiet on {name}")
    quiet = compare(BIB_TRUE, record)
    if quiet:
        bad.append(f"compare fired on an entry that matches the record: {quiet}")
    # Braces are BibTeX's, not the title's. An entry that protects its
    # capitalisation must not read as a disagreement.
    braced = {**BIB_TRUE, "title": BIB_TRUE["title"].replace("Factual", "{Factual}")}
    if compare(braced, record):
        bad.append("compare fired on a title whose capitalisation is braced")
    # A title that really contains quotation marks, spelled the LaTeX way.
    quoted = {"title": "Non-Determinism of ``Deterministic\'\' LLM Settings",
              "author": "Nobody", "year": "2024"}
    plain = {"title": 'Non-Determinism of "Deterministic" LLM Settings',
             "author": "Nobody", "year": "2024"}
    straight = {"title": plain["title"], "authors": ["Nobody"], "year": "2024"}
    if compare(quoted, straight):
        bad.append("compare fired on a title whose quotes are LaTeX\'s ``\'\'")
    if compare(plain, straight):
        bad.append("compare fired on a plainly-quoted title matching the record")
    if not compare({**quoted, "title": quoted["title"].replace("Non-", "Non")},
                   straight):
        bad.append("compare stayed quiet on a quoted title that is still wrong")
    return bad


def cli_self_test():
    """That `main` actually calls `unused`, proved through the command.

    Everything above tests functions. A function that is correct and never
    called is the defect this project has now found seven times, and no probe
    that imports the function can see it -- so this one runs the command over a
    seeded bibliography and requires the refusal to name the seeded entry. The
    real bibliography is not also run here: if it ever has a genuine problem,
    `self_test` returning first would hide the diagnostic that says what.
    """
    if os.environ.get("CHECK_REFS_CHILD"):
        return []  # the child below; without this the probe recurses forever
    # One field per line, because `FIELD` wants them that way. A compact entry
    # is malformed, and the first draft of this probe was passing on the
    # malformed-entry refusal rather than the uncited one -- which is why the
    # message is asserted below and not just the exit code.
    seeded = (PAPER / "refs.bib").read_text(encoding="utf-8") + """

@misc{probe_nobody_cites,
  title         = {{A Paper}},
  author        = {Nobody},
  year          = {2023},
  eprint        = {2305.14251},
  archivePrefix = {arXiv},
  verified      = {a probe, not a citation}
}
"""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "refs.bib"
        path.write_text(seeded, encoding="utf-8")
        done = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--bib", str(path)],
            capture_output=True, text=True,
            env={**os.environ, "CHECK_REFS_CHILD": "1"})
    want = "probe_nobody_cites: verified and in refs.bib, but no section cites it"
    if done.returncode == 1 and want in done.stdout:
        return []
    return [f"the command exited {done.returncode} on a bibliography carrying "
            f"an entry no section cites, without saying so. Wanted {want!r}; "
            f"got: {done.stdout.strip()[-300:]!r} {done.stderr[:200]!r}"]


def firing(blob, phrase):
    """Complaints unless `blob` produces a problem whose text contains `phrase`."""
    said = problems(blob)
    if not said:
        return ["stayed quiet"]
    if not any(phrase in line for line in said):
        return [f"fired for another reason: wanted {phrase!r}, got {said}"]
    return []


def self_test():
    bad = []
    for name, (blob, phrase) in MUST_FIRE.items():
        bad += [f"must-fire probe {name!r} {why}" for why in firing(blob, phrase)]
    # `firing` itself, both ways. Without this the phrase half is dead weight:
    # every probe here fires for the right reason already, so dropping the
    # comparison changes no result and no test notices.
    blob, phrase = MUST_FIRE["no verified field"]
    if firing(blob, phrase):
        bad.append("firing() complained about a probe that fires correctly")
    if not firing(blob, "a phrase no problem will ever contain"):
        bad.append("firing() does not check WHICH problem fired")
    if not firing(MUST_NOT_FIRE, "anything at all"):
        bad.append("firing() did not notice a clean entry staying quiet")
    if problems(MUST_NOT_FIRE):
        bad.append(f"must-not-fire probe fired: {problems(MUST_NOT_FIRE)}")
    bad += online_self_test()
    bad += cli_self_test()
    for line in bad:
        print(f"  FAIL {line}")
    if bad:
        return 1
    print(f"  self-test: {len(MUST_FIRE)} must-fire probe(s) fire, "
          f"must-not-fire is quiet")
    print(f"  self-test: --online's reader and comparator, "
          f"{len(COMPARE_MUST_FIRE) + 7} must-fire probe(s) and 9 must-not, "
          f"offline, and the call site through the command")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--online", action="store_true",
                    help="re-fetch every entry from arXiv and compare; opt-in, "
                         "and never run by tests/run_all.py")
    ap.add_argument("--bib", type=Path, default=PAPER / "refs.bib")
    args = ap.parse_args()

    if self_test():
        return 1
    if args.self_test:
        return 0

    text = args.bib.read_text(encoding="utf-8")
    if args.online:
        return online(text)

    tex = "".join(part.read_text(encoding="utf-8")
                  for part in sorted(SECTIONS.glob("*.tex")))
    found = problems(text) + unused(text, tex)
    for line in found:
        print(f"  FAIL {line}")
    if found:
        print(f"\n  {len(found)} problem(s). Verify the entry against a stable "
              f"identifier or delete it, with the sentence that cites it.")
        return 1
    print(f"  refs: {len(entries(text))} entry(ies), all verified, "
          f"self-consistent and cited")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
