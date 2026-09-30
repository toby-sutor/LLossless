# Nimbrel Probe stream name with unsupported symbols

Author: Marlowe Ferrante
Updated: 2026-02-03

### Topic

The stream name is one of the mandatory fields for every Nimbrel Probe agent, and it is what separates one instrumented process from the next.

It cannot contain arbitrary symbols: only letters, digits, spaces and hyphens are accepted, and the value has to match ^[A-Za-z0-9 -]+$, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

A stream name containing a . (dot), for example `checkout.web`, is refused, as are a number of other symbols.

The existing name may nevertheless need to be kept exactly as it stands, where that string is the product name in use everywhere in the org and reporting keys off it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

This is working as intended for now; there is no fix at present, so the way round it is to rename the stream:

1) Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
2) Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one
https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}