# The `tests/handwritten/` corpus

Nineteen sets of documents on ordinary subjects: a recipe, two party invitations, an email and a memo about one topic. Seventeen sets are a pair of documents and two have three. Fifteen sets carry a `reference.md`, a merge the project's author wrote. The other four are sets the author judged should not be merged at all, and their `meta.json` says why in the author's words.

**Who wrote what.** The sources of fourteen sets were written by the author together with an AI assistant (Claude). The two sources of `voyager` are adapted from NASA's page on the Voyager 2 mission, and the author planted factual errors in them. They give no address for that page on purpose, so that a model has to search for it. Four sets (`gold_de_en`, `mahjongg`, `sepia` and `treecreeper`) are adapted from Wikipedia articles. The author wrote every `reference.md` alone. The directory keeps the name `handwritten` because published results cite its paths.

The benchmark's planted-error test uses three of the sets: `voyager` and `bip39` have factual errors planted in their sources (44 and 14), and `mahjongg` has none and is the control. See [The benchmark](../../docs/benchmark.md). You can also measure a merge of your own against any set; the commands are below.

**Two licences apply.** Fifteen sets are published under CC BY 4.0: see `LICENSE` in this directory, which also credits NASA as the source of `voyager`. Four sets (`gold_de_en`, `mahjongg`, `sepia` and `treecreeper`) are adapted from Wikipedia articles and are published under CC BY-SA 4.0, the licence of Wikipedia's text: see `LICENSE-CC-BY-SA` in this directory and the `LICENSE` in each of the four set directories. If you reuse one of those four, credit the Wikipedia contributors and publish what you build from it under CC BY-SA 4.0 as well. The repository's root `LICENSE` (Elastic License 2.0) covers the code and does not cover this directory.

## What this corpus is for

The other two test corpora, `tests/pairs/` and `tests/fixtures/`, were written for the tool. Every reference merge in `tests/pairs/` is required to pass the tool's own mechanical checks, the checks that compare text and use no model.

The reference merges here were written by a person, the project's author, with no such rule in front of them. They reword freely, they drop material, and two of them (`sepia` and `treecreeper`) simply paste the sources one after the other. That is what makes the corpus useful: it shows what a person does when asked to merge, which is not what the tool's rules describe.

## A `reference.md` is a reference, not an answer key

A `reference.md` is what one person thought a good merge looked like. Do not grade a merge by how closely it agrees with one. On `curry` the reference leaves out 22 of the sources' 60 segments. On `sepia` it is the two sources pasted together byte for byte, which is the shape the `Ordering:` line of a report exists to point out. Neither 0% nor 100% agreement is the target.

The scripts that compare a merge with a `reference.md` therefore report the difference in both directions: what the merge lost that the reference kept, and what the merge kept or repeated that the reference left out. `tests/rank_arms.py` explains the two figures in its opening docstring. A one-sided figure would rank a copy-everything merge first, because it cannot lose what the reference kept.

## The nineteen sets

| Set | Kind | A | B | C | Reference | What it is |
|---|---|---|---|---|---|---|
| `bip39` | merge | 874 | 1,183 | - | 2,051 | The BIP-39 seed-phrase standard, as two accounts. 14 planted errors. |
| `birthday` | merge | 564 | 595 | - | 701 | Two invitations to the same birthday party. |
| `chickens` | merge | 1,133 | 1,086 | - | 1,355 | Keeping backyard chickens, as a how-to and as a care sheet. |
| `christianity` | merge | 1,172 | 1,116 | - | 1,229 | An introduction to Christianity, as a short guide and as a fact list. |
| `curry` | merge | 1,179 | 1,392 | - | 1,562 | A vegetarian Thai green curry, as two recipes. |
| `duplicate` | merge | 691 | 743 | - | 893 | Woodworking and metalworking, in near-identical prose. |
| `fizzbuzz_c_cpp` | refusal | 340 | 357 | - | - | The FizzBuzz program in C and in C++. |
| `fizzbuzz_csharp_java` | refusal | 425 | 442 | - | - | The FizzBuzz program in C# and in Java. |
| `gold_de_en` | refusal | 1,237 | 2,187 | - | - | Two texts about gold, one in German and one in English. |
| `iphone_android` | merge | 1,867 | 1,699 | - | 2,629 | iPhone against Android, as two comparison tables. |
| `linux` | merge | 1,196 | 1,368 | - | 1,357 | What the name GNU/Linux means, as an email and as a memo. |
| `mahjongg` | merge | 6,421 | 3,919 | 15,218 | 25,575 | Mah-Jongg rules in German, from three sources. No planted errors: the control. |
| `motorbike` | merge | 988 | 945 | - | 1,079 | Motorbike against quad bike. |
| `sepia` | merge | 3,408 | 5,801 | - | 9,211 | Cuttlefish: anatomy, and the visual system. The reference is the two sources pasted together. |
| `subset` | merge | 4,844 | 1,169 | - | 4,844 | A long piece on China and a short one whose content it already contains. The reference is source A unchanged. |
| `treecreeper` | merge | 1,488 | 2,825 | 1,686 | 6,003 | The Eurasian treecreeper, as three sections. The reference is the three sources pasted together. |
| `universe` | merge | 1,425 | 1,427 | - | 1,428 | Deep time and scale, as two essays with the same title. |
| `unrelated` | refusal | 3,668 | 1,734 | - | - | A Japan travelogue and an essay on Chaplin. |
| `voyager` | merge | 881 | 1,337 | - | 2,186 | Voyager 2's flyby of Uranus in 1986, as two accounts adapted from NASA's page on the mission. 44 planted errors. |

Sizes are in bytes. A, B and C are `source_a.md`, `source_b.md` and `source_c.md`; only `mahjongg` and `treecreeper` have a third source.

Four sets are adapted from Wikipedia articles, which their sources cite: `gold_de_en` from "Gold" in the German and the English Wikipedia, `mahjongg` from "Mah-Jongg" in the German Wikipedia, `sepia` from "Cuttlefish" and `treecreeper` from "Eurasian treecreeper" in the English Wikipedia. These four are under CC BY-SA 4.0, and so is every merge made from them, including the `mahjongg` runs under `arms/`.

### The files in a set

| File | What it is |
|---|---|
| `source_a.md`, `source_b.md`, and `source_c.md` in two sets | The documents to merge. |
| `reference.md` | The author's merge. Present in the fifteen sets of kind `merge`, absent in the four of kind `refusal`. |
| `LICENSE` | Only in the four sets adapted from Wikipedia: the source article and the CC BY-SA 4.0 notice. |
| `meta.json` | `pair`: the set's name. `kind`: `merge` or `refusal`. `description`: one sentence on what the set is, or, for a refusal, why it should not be merged. `origin`: the name each file had in the author's own collection. `note`, in ten sets: what is unusual about the set. |

`meta.json` calls the author "the operator". It is the same person.

### The four sets that should not be merged

The author's judgement on `fizzbuzz_c_cpp`, `fizzbuzz_csharp_java`, `gold_de_en` and `unrelated` is that a model should decline: two programming languages, two human languages, two unrelated subjects. They have no `reference.md` because there is no correct merge to write.

LLossless does not decline them. It merges whatever it is given and reports what was lost. [Measured results](../../docs/results.md) describes, under "Known limits", what it did on `fizzbuzz_c_cpp` and on `unrelated`.

### The planted-error sets

The sources of `voyager` and `bip39` contain factual errors, put there on purpose by the author to test whether a merge corrects them or repeats them. Their `reference.md` has the correct facts. `mahjongg` has no planted errors and measures the opposite mistake: a merge that "corrects" a fact that was right. Its sources are in German, are given out of order, and carry Chinese and Japanese characters.

**The errors are not listed in any published file, and should not be.** The answer key is computed: `tests/score_planted.py` compares `reference.md` with the sources word by word, and every place that differs is a planted error. A typed list would be a second key that could disagree with the files. The one exception is in `bip39/meta.json`, which names the licence error because it was planted as a deliberate trap.

    python3 tests/score_planted.py --pair voyager --key              # print the computed key
    python3 tests/score_planted.py --pair voyager MERGED.md          # score a merge: errors fixed, kept, other
    python3 tests/score_planted.py --pair mahjongg --control MERGED.md   # count false corrections

## Measuring your own merge against a set

`tests/measure_merges.py` reports, for each merge, how many of the sources' segments are still present, and whether the merge is the sources pasted together. It makes no model call. Put the merged documents in one directory, each named `<set>-<label>-<number>.md` (for example `curry-high-0.md`), and run:

    python3 tests/measure_merges.py --fixtures-root tests/handwritten --merges DIR

The banner it prints was written for an older set of recordings; the columns mean the same here. It reads every source a set has, so `mahjongg` and `treecreeper` are measured against all three. A set whose source letters have a gap, `source_a.md` and `source_c.md` with no `source_b.md`, is refused.

## What else uses the corpus

- **The release benchmark.** `tests/run_lineup.py` merges `voyager`, `bip39` and `mahjongg` at `--fidelity open`, and `tests/score_planted.py` scores the results.
- **Earlier recorded runs.** `tests/rank_arms.py` and `tests/phase4_figures.py` score runs under `arms/` against the `reference.md` of `birthday`, `chickens`, `christianity` and `curry`. Those run directories use the sets' older names: `toby-test-1`, `-2`, `-4` and `-5`.
- **The corpus's own test.** `tests/test_handwritten.py` checks that every set is complete and that what this page says about `sepia`, `treecreeper` and `mahjongg` holds.

## If you change this corpus

- **Do not edit a source or a `reference.md`.** Published results were measured on these exact files.
- **Do not move a set into `tests/pairs/` or `tests/fixtures/`.** Those two directories have their sizes written into tests: nine pairs in `tests/test_pairs.py`, sixteen fixtures in `tests/test_merge.py`, and the twenty-five together in `tests/test_reconcile.py`. `tests/test_pairs.py` also requires every reference merge there to pass the mechanical checks with no finding at `verbatim` and at `high`, and most of the references here do not.
- **Do not add a `reference.md` from here to the documents `tests/test_reconcile.py` treats as correct merges.** One of its tests expects exactly two of those twenty-five documents, `disjoint_domains` and `disjoint_sources`, to read as sources pasted together. `sepia` and `treecreeper` would make it four. `tests/test_handwritten.py` fails if the word `handwritten` appears in `tests/test_reconcile.py`.
- **Name a reference `reference.md`, never `merged.md` or `ideal.md`.** The measuring scripts read a `merged.md` as an answer key.
- **Name sources `source_a.md`, `source_b.md`, `source_c.md` with no gap,** and list each one under `origin` in `meta.json`.
- **Add every new file to git.** The checks over the published files read only tracked files.
