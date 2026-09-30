# The hand-written corpus

19 document pairs written by hand by the project's author over the year the tool was built, on ordinary subjects. 15 carry a `reference.md`, a merge the author wrote themselves; 4 are pairs that **should not be merged at all**, and their `meta.json` records why in the author's own words. The benchmark's planted-error documents, `voyager` and `bip39`, are two of them.

The author released the corpus for publication, and it is copied here byte for byte; each `meta.json` names its files' original names. It is under CC BY 4.0: see `LICENSE` in this directory. The repository root `LICENSE` (Elastic License 2.0) covers the code and does not cover this directory.

## Why this corpus exists beside the other two

`tests/pairs/` and `tests/fixtures/` were built for the tool. Their answer keys were written by the same process that wrote the thing they grade, and that is a known weakness of both.

Here both sides were written by a person, without a schema in front of them. That is the whole value, and it is also why the merges here break rules the other corpora keep: they reword freely, drop material, and in two cases simply staple the sources together, one of them three-way.

## `reference.md` is a reference, not an answer key

A `reference.md` is what one person thought a good merge looked like, and the deviation from it is scored **two-sided**: content the merge lost against the reference and content it added or repeated, as `tests/rank_arms.py` explains in its opening docstring. On `curry` the reference drops 22 of 60 segments. On `sepia` it is a byte concatenation, the exact defect the reconciler's staple check exists to catch. Neither 0% nor 100% agreement is the target.

Two consequences:

- **Do not add `tests/handwritten/*/reference.md` to the control set of the staple check in `tests/test_reconcile.py`.** That check's registration pins exactly two firings (`disjoint_domains`, `disjoint_sources`); `sepia` and `treecreeper` would each fire it too and void the registration.
- **Do not grade a run by agreement with a `reference.md`.** Report the deviation and its direction.

## The pairs

| pair | kind | A | B | C | reference |
|---|---|---|---|---|---|
| `bip39` | merge | 874 | 1,183 | - | 2,051 |
| `birthday` | merge | 564 | 595 | - | 701 |
| `chickens` | merge | 1,133 | 1,086 | - | 1,355 |
| `christianity` | merge | 1,172 | 1,116 | - | 1,229 |
| `curry` | merge | 1,179 | 1,392 | - | 1,562 |
| `duplicate` | merge | 691 | 743 | - | 893 |
| `fizzbuzz_c_cpp` | refusal | 340 | 357 | - | - |
| `fizzbuzz_csharp_java` | refusal | 425 | 442 | - | - |
| `gold_de_en` | refusal | 1,237 | 2,187 | - | - |
| `iphone_android` | merge | 1,867 | 1,699 | - | 2,629 |
| `linux` | merge | 1,196 | 1,368 | - | 1,357 |
| `mahjongg` | merge | 6,421 | 3,919 | 15,218 | 25,575 |
| `motorbike` | merge | 988 | 945 | - | 1,079 |
| `sepia` | merge | 3,408 | 5,801 | - | 9,211 |
| `subset` | merge | 4,844 | 1,169 | - | 4,844 |
| `treecreeper` | merge | 1,488 | 2,825 | 1,686 | 6,003 |
| `universe` | merge | 1,425 | 1,427 | - | 1,428 |
| `unrelated` | refusal | 3,668 | 1,734 | - | - |
| `voyager` | merge | 881 | 1,337 | - | 2,186 |

Sizes in bytes. `kind: refusal` pairs have no `reference.md`: the correct output is a declined merge, and `meta.json`'s `description` is the author's statement of why. `C` is empty for the seventeen two-source pairs; `mahjongg` and `treecreeper` are the only three-source pairs, named `source_a.md`, `source_b.md` and `source_c.md`.

The four refusal pairs are hand-written positives for the `disjoint_sources` and `disjoint_domains` guards and for the `mismatch` field in `meta.json`.

**The seeded-error pairs.** The author wrote both sources of `voyager` and `bip39` with factual errors on purpose, to test whether a merge catches or repeats them, and `reference.md` is the author's own correct merge. `meta.json` does not list the errors, since a list would be an answer key. `mahjongg` carries no seeded errors and is the negative control for fact correction: its sources are German, given out of order, and carry Chinese and Japanese characters, which the author called the hardest merge in the set.

## Why this is not under `tests/fixtures/` or `tests/pairs/`

Both of those are swept whole by tests that pin their size:

- `tests/test_pairs.py` pins `tests/pairs/` at exactly nine directories, each required to carry `ideal.md` and `ideal.json`, and an `ideal.md` must draw **zero** findings at both `off` and `high`. No merge here would pass that, by design.
- `tests/test_merge.py` pins `tests/fixtures/` at exactly 16, and those fixtures carry `expected.json` with per-probe ground truth.
- `tests/test_reconcile.py` pins the union of the two at 25.

None of those walk `tests/handwritten/`. Every file here must still be tracked by git: an untracked file in a corpus directory is a file no release scan reads.

## Scoring a merge against one of these pairs

    python3 tests/measure_merges.py --fixtures-root tests/handwritten --merges <dir>

`tests/measure_merges.py` handles a corpus with no `merged.md` answer key rather than crashing on it. `tests/league_table.py` does the same internally for recorded benchmark runs; see its docstring.

Every `source_<letter>.md` a pair has is read, from `source_a.md` with no gap, so `mahjongg` and `treecreeper` are measured against all three of their sources. A pair whose letters have a gap is refused, not measured short.
