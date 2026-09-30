# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

The stream name is a mandatory field for every Nimbrel Probe agent and is what separates one instrumented process from the next. It cannot contain arbitrary symbols: only letters, digits, spaces and hyphens are accepted, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

A stream name containing a . (dot), for example `checkout.web`, is refused by Nimbrel Probe, as are a number of other symbols. This is working as intended for now.

Renaming the stream is not always acceptable, for example when the existing string is the product name used everywhere in the organisation and reporting is keyed off it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

There is no fix at present. The following workaround works:

1. Rename the stream to drop the unsupported symbols so that the Nimbrel Probe agent registers.
2. Carry the original name along as a global tag, so that each trace keeps a link between the real name and the renamed one: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}