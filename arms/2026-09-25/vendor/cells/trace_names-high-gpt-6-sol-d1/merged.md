# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

Author: Marlowe Ferrante
Updated: 2026-02-03

### Topic

A stream name is mandatory for every Nimbrel Probe agent. It distinguishes one instrumented process from another and cannot contain arbitrary symbols, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

The browser configuration documents this restriction [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name). A stream name containing a . (dot), such as ` checkout.web`, is refused by Nimbrel Probe; other unsupported symbols are also refused. The restriction works as intended for now.

A stream name may be a product name used throughout an organization, with reporting keyed to that name, so it may need to remain unchanged.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

No fix is available at present. The workaround is:

1) Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
2) Carry the original name as a global tag so each trace retains a link between the original name and the renamed stream. https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}