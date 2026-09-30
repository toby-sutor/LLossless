# The six audience-coherence pairs

These are not the registered seven-pair corpus of `tests/pairs/`. Its primary
denominator is 7 pairs x 2 levels x 1 title not taken = 14, registered before
any arm ran and asserted in `tests/test_pairs.py`. Six more pairs there would
make it 26 and would retroactively change what the recorded arms were measured
against, so this corpus lives beside that one.

Two pairs have since been added to `tests/pairs/`, and the recorded denominator
stays at 14 because `tests/run_arm.py` names the seven as `M9_PAIRS`. That
mechanism did not exist when this corpus was placed here, so the arithmetic
above is no longer the reason these six live apart. The reason now is that they
are a different corpus with a different question and a fifth file,
`inverted.md`, that `tests/pairs/` has no place for.

They exist because of one merge. Arm C's `bike_docks` at `off` put a support
desk's escalation path under a field crew's title, lost nothing, invented
nothing, declared its title honestly, and scored clean on every metric the
reconciler rewards. The corpus was scoped to two pairs of the shape that must
fire and one of each of the four shapes that must not, and that is exactly what
is here.

## The distinguishing question

Not the title - the same title sits on the correct and the incorrect merge of
the same two documents. Not the content - both merges contain the same union of
facts. It is whether the merged document **marks the boundary**:

> Would a reader who is the title's stated audience attempt a step they cannot
> perform or are not authorised to perform?

## What each pair is

**incident_pager** *(shape 1, must fire)* - The pager procedure as written for
the on-call engineer and as written for the duty manager. They share how to
acknowledge a page and what to check first, and diverge on what each role is
allowed to do: the engineer restarts production services, the manager approves
customer notices and calls the executive sponsor. `inverted.md` keeps all of it
under the engineer's title with the role headings stripped, so the document
instructs an engineer to approve an external notice they have no authority over.

**sample_intake** *(shape 1, must fire)* - Collecting pathology samples, written
for the courier and for the laboratory technician. The courier's own document
says *"Do not open the box at any point"*; the technician's says to break the
tamper seal at the bench and record the seal number in LIMS. `inverted.md` puts
both under the courier's title. The reader is told to do a thing the same
document forbids them, and has no LIMS account to do it with.

**Shape 1 is two defects and they are recorded apart.** `sample_intake` is a
**self-contradiction**: the merged document forbids what it instructs, both
sentences are in it, and a checker needs no model of who a courier is to see
that they cannot both be followed. `incident_pager` is an **authority
mismatch**: nothing contradicts anything, and the only thing wrong is that the
stated reader lacks the standing - a fact that is in neither source. Each
`shape.json` carries `defect` and `audience_model_required`, and
`test_the_two_firing_pairs_are_two_different_defects` asserts one of each. A
predicate scoring 1 of 2 here is not a coin flip: which one it caught says
whether it read the text or modelled the reader.

**parking_permits** *(shape 6, must not fire)* - **The important control.** A
genuine two-audience merge, done correctly: staff renewals and visitor permits
both present, every audience-specific heading naming its reader, and the neutral
of the two titles chosen. A predicate that fires here fires on every legitimate
merge of two audiences, which is most of what this tool is for.

**fire_drill** *(shape 7, must not fire)* - `badge_access` and `freezer_alarm`'s
shape. One title carries an audience qualifier and the other is the general
*wording* of the same ground-floor content, not a wider document. Three of the
seven registered pairs are already this, which is why a naive predicate would look good
on that corpus while being wrong.

**kettle_descaling** *(shape 8, must not fire)* - Neither title names a reader.
A check that needs a qualifier to be present must be *silent* here, and silence
has to be seen to be deliberate: absent-by-accident and correctly-silent produce
the same output and only this fixture separates them.

**helpdesk_tickets** *(shape 9, must not fire)* - "Support Desk" against
"Service Desk": two names for one team, differing in wording and not in scope. A
predicate that fires here is a string comparison wearing a semantic label.
That predicate was rejected in advance and this pair is how the rejection is
enforced rather than remembered.

## The files

`source_a.md` and `source_b.md` are the inputs. `ideal.md` is a correct merge
and `ideal.json` records what it did to anything it did not keep word for word.
`shape.json` names the shape, whether it must fire, and which merged document is
under audit. The two shape-1 pairs also carry `inverted.md` and `inverted.json`:
the defect, built deliberately.

`inverted.md` is `ideal.md` with the heading qualifiers stripped and **nothing
else changed** - same line count, same section order, same sentences. Exactly
one variable separates the correct merge from the defective one, so a predicate
cannot score here by noticing that the sections moved.
`test_the_inversion_differs_from_the_ideal_in_one_variable` holds that: every
differing line must be a `##` heading whose ideal form is the inverted form plus
a trailing parenthesis.

**A claim made here when this corpus landed, and withdrawn.** The first version
of this file said the honest merge costs declarations and the dishonest one does
not. It does not, on these pairs: `ideal.json` and `inverted.json` are
byte-identical on both shape-1 pairs, one `superseded` record each for the
title, and `ideal.md` pays for its honesty in heading text rather than in
declared dispositions. The claim is true of a different remedy -
`tests/pairs/bike_docks/ideal.json` folds source B into the field crew's
sections and declares it in **eight** records - and false of the one used here.

Nothing here is taken from a real document. The names, numbers and wording were
all invented for these fixtures.

## What the audit checks, and what it cannot

`tests/test_attribution.py` runs the same answerability audit `test_pairs.py`
runs: `ideal.md` plus `ideal.json` through the reconciler at both fidelity
levels, zero findings required. All six pass.

Then it asserts the thing this corpus is for, which is a **blindness**:

    the ideal merge is answerable       checked
    the inverted merge is answerable    checked -- and that is the finding
    the inverted merge is wrong         NOT checked; no predicate exists

Both inverted merges draw zero findings at both levels and cover exactly what
their ideal merge covers. That assertion is written to **fail** the day an
audience predicate lands, which is the correct behaviour: the predicate is
built after the pairs, so the pairs have to be able to notice it arriving.

One further blindness, found while measuring these. `Order.stapled` is True of
`incident_pager`'s and `sample_intake`'s **ideal.md and inverted.md alike**, and
of `parking_permits/ideal.md`. It separates nothing here. An earlier version of
this file recorded it as True of the correct merges and False of the inversions,
which read as the measurement pointing the wrong way; that was the section
*order*, which the inversions no longer differ in, and not the qualifiers. The
staple measurement is reported and never judged, which is why neither
reading of it costs anything.

## Sizes

| Pair | Shape | Must fire | Source A | Source B | Segments | Sentences both sources state |
| --- | --- | --- | --- | --- | --- | --- |
| fire_drill | 7 | no | 13 segments, 127 words | 14 segments, 143 words | 27 | 5 |
| helpdesk_tickets | 9 | no | 14 segments, 142 words | 14 segments, 129 words | 28 | 5 |
| incident_pager | 1 | **yes** | 15 segments, 154 words | 14 segments, 140 words | 29 | 5 |
| kettle_descaling | 8 | no | 14 segments, 130 words | 14 segments, 125 words | 28 | 5 |
| parking_permits | 6 | no | 13 segments, 125 words | 12 segments, 124 words | 25 | 3 |
| sample_intake | 1 | **yes** | 14 segments, 130 words | 14 segments, 131 words | 28 | 5 |

The last column counts sentences only. Each pair also shares exactly two
headings, so the block a staple would repeat verbatim is two larger than the
figure shown - 7 segments, or 5 for `parking_permits`. That block is also what
`reconcile.order` excludes from `attributed`: a segment both sources state
identically is evidence about neither.

A "segment" is a title, a heading or a sentence. Every pair sits in the 25-29
band, close to the registered corpus's short six at 29-36 and deliberately nowhere near
`rate_limits` at 104: length is `rate_limits`' job and confounding the two would
mean a predicate measured on this corpus was also being measured on size.

Each pair's `ideal.json` declares one record, the superseded source title, so
none of them comes near the 5% declared-loss budget. That is on purpose too. A
pair where the budget binds tests the budget; these test one question each.
