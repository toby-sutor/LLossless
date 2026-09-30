# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

The stream name is one of the mandatory fields for every Nimbrel Probe agent, and it is what separates one instrumented process from the next. It cannot contain arbitrary symbols: only letters, digits, spaces and hyphens are accepted (it has to match ^[A-Za-z0-9 -]+$), as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

A stream name containing a . (dot), for example` checkout.web`, along with a number of other symbols, is refused by Nimbrel Probe. This is working as intended for now.

The stream name is nevertheless often the product name in use everywhere in the organisation, with reporting keyed off it, so there is pressure to leave it exactly as it stands.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

There is no fix at present. A way round it that works:

1) Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
2) Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one
https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}