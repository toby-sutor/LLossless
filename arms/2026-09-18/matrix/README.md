# Merged outputs, 2026-09-18 matrix

Four models over the nine pairs in `tests/pairs`, all at `high` fidelity,
all recorded at commit cf30209 on one day.

Each pair below lists the REFERENCE merge first, then each model's output.
`dev` is distance from the reference (lower is closer); `silent` is content
dropped without any disposition record, which is the disqualifying fault.

## badge_access  (33 segments, reference drops 1)

    sources    tests/pairs/badge_access/source_a.md  source_b.md
    REFERENCE  tests/pairs/badge_access/ideal.md
    why        tests/pairs/badge_access/ideal.json   (what it dropped, and why)

    dev 0   claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/badge_access-high-claude-haiku-4-5/merged.md
    dev 0   claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/badge_access-high-claude-opus-5/merged.md
    dev 0   claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/badge_access-high-claude-sonnet-5/merged.md
    dev 1   gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/badge_access-high-gpt-5.6-terra/merged.md

## bike_docks  (35 segments, reference drops 8)

    sources    tests/pairs/bike_docks/source_a.md  source_b.md
    REFERENCE  tests/pairs/bike_docks/ideal.md
    why        tests/pairs/bike_docks/ideal.json   (what it dropped, and why)

    dev 3   claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/bike_docks-high-claude-opus-5/merged.md
    dev 4   claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/bike_docks-high-claude-haiku-4-5/merged.md  SILENT LOSS 2
    dev 5   claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/bike_docks-high-claude-sonnet-5/merged.md
    dev 6   gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/bike_docks-high-gpt-5.6-terra/merged.md

## freezer_alarm  (33 segments, reference drops 5)

    sources    tests/pairs/freezer_alarm/source_a.md  source_b.md
    REFERENCE  tests/pairs/freezer_alarm/ideal.md
    why        tests/pairs/freezer_alarm/ideal.json   (what it dropped, and why)

    dev 2   gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/freezer_alarm-high-gpt-5.6-terra/merged.md
    dev 3   claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/freezer_alarm-high-claude-haiku-4-5/merged.md  SILENT LOSS 2
    dev 6   claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/freezer_alarm-high-claude-sonnet-5/merged.md
    dev 7   claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/freezer_alarm-high-claude-opus-5/merged.md

## index_429  (63 segments, reference drops 4)

    sources    tests/pairs/index_429/source_a.md  source_b.md
    REFERENCE  tests/pairs/index_429/ideal.md
    why        tests/pairs/index_429/ideal.json   (what it dropped, and why)

    dev 3   gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/index_429-high-gpt-5.6-terra/merged.md
    dev 5   claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/index_429-high-claude-opus-5/merged.md
    dev 20  claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/index_429-high-claude-haiku-4-5/merged.md  SILENT LOSS 1
    dev 21  claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/index_429-high-claude-sonnet-5/merged.md

## library_holds  (29 segments, reference drops 5)

    sources    tests/pairs/library_holds/source_a.md  source_b.md
    REFERENCE  tests/pairs/library_holds/ideal.md
    why        tests/pairs/library_holds/ideal.json   (what it dropped, and why)

    dev 8   claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/library_holds-high-claude-opus-5/merged.md
    dev 9   claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/library_holds-high-claude-haiku-4-5/merged.md
    dev 10  gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/library_holds-high-gpt-5.6-terra/merged.md
    dev 11  claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/library_holds-high-claude-sonnet-5/merged.md

## loading_dock  (36 segments, reference drops 8)

    sources    tests/pairs/loading_dock/source_a.md  source_b.md
    REFERENCE  tests/pairs/loading_dock/ideal.md
    why        tests/pairs/loading_dock/ideal.json   (what it dropped, and why)

    dev 2   claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/loading_dock-high-claude-sonnet-5/merged.md
    dev 2   gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/loading_dock-high-gpt-5.6-terra/merged.md
    dev 3   claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/loading_dock-high-claude-opus-5/merged.md
    dev 5   claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/loading_dock-high-claude-haiku-4-5/merged.md  SILENT LOSS 5

## payroll_cutoff  (33 segments, reference drops 0)

    sources    tests/pairs/payroll_cutoff/source_a.md  source_b.md
    REFERENCE  tests/pairs/payroll_cutoff/ideal.md
    why        tests/pairs/payroll_cutoff/ideal.json   (what it dropped, and why)

    dev 1   gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/payroll_cutoff-high-gpt-5.6-terra/merged.md
    dev 2   claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/payroll_cutoff-high-claude-opus-5/merged.md
    dev 3   claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/payroll_cutoff-high-claude-haiku-4-5/merged.md  SILENT LOSS 2
    dev 5   claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/payroll_cutoff-high-claude-sonnet-5/merged.md

## rate_limits  (104 segments, reference drops 38)

    sources    tests/pairs/rate_limits/source_a.md  source_b.md
    REFERENCE  tests/pairs/rate_limits/ideal.md
    why        tests/pairs/rate_limits/ideal.json   (what it dropped, and why)

    dev 7   claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/rate_limits-high-claude-haiku-4-5/merged.md  SILENT LOSS 5
    dev 12  gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/rate_limits-high-gpt-5.6-terra/merged.md  SILENT LOSS 1
    dev 26  claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/rate_limits-high-claude-opus-5/merged.md
    dev 29  claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/rate_limits-high-claude-sonnet-5/merged.md

## trace_names  (27 segments, reference drops 4)

    sources    tests/pairs/trace_names/source_a.md  source_b.md
    REFERENCE  tests/pairs/trace_names/ideal.md
    why        tests/pairs/trace_names/ideal.json   (what it dropped, and why)

    dev 7   claude-opus-5      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/trace_names-high-claude-opus-5/merged.md
    dev 8   claude-sonnet-5    <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/trace_names-high-claude-sonnet-5/merged.md
    dev 11  claude-haiku-4-5   <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/trace_names-high-claude-haiku-4-5/merged.md  SILENT LOSS 2
    dev 13  gpt-5.6-terra      <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-18-matrix/trace_names-high-gpt-5.6-terra/merged.md

