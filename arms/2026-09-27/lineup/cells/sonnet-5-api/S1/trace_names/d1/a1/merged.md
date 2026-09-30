# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

Stream name is one of the mandatory fields for every Nimbrel Probe agent, and it is what separates one instrumented process from the next. The stream name cannot contain arbitrary symbols, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name):

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

A stream name containing a . (dot) — for example `checkout.web` — along with a number of other symbols, is refused for this reason. This is expected behaviour rather than a bug, and there is no fix planned.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

There is no fix at present. Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. Where the original name matters — for instance when it is a product name already in use throughout the organization and referenced by existing reporting — carry it forward as a global tag, so each trace still keeps a link between the real name and the renamed one: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}
{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}