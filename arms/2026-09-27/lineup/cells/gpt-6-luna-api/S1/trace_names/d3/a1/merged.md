# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

### Issue Description

A stream name is a required field for every Nimbrel Probe agent. It identifies what separates one instrumented process from the next. A name containing a dot—for example ` checkout.web`—or other unsupported symbols is refused. Stream names accept only letters, digits, spaces and hyphens and must match ^[A-Za-z0-9 -]+$. This is documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

A customer may need to retain the exact stream name when it is the product name used throughout the organization and reporting keys off it.

### Cause

This is working as intended for now.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

### Workaround

A workable workaround is:

1) Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.
2) Carry the original name as a global tag so each trace retains a link between the original and renamed names: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

### Resolution

There is no fix at present; renaming the stream without the refused symbol is the available workaround.

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}