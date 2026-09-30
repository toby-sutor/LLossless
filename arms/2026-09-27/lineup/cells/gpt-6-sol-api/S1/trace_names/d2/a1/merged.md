# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

Author: Marlowe Ferrante
Updated: 2026-02-03

### Topic

Stream name is a mandatory field for every Nimbrel Probe agent. It distinguishes one instrumented process from another. A stream name cannot contain arbitrary symbols, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name). Only letters, digits, spaces and hyphens are permitted, as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name). Names containing a . (dot), such as ` checkout.web`, or other unsupported symbols are refused. The restriction is intentional for now.

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

A stream name may need to remain unchanged when it is the product name used throughout an organization and reporting keys off it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

There is no fix at present. The workaround is:

1) Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.
2) Carry the original name as a global tag so each trace retains a link between the product name and the renamed stream: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}