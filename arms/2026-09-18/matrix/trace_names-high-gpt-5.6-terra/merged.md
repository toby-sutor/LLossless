# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

A stream name is a mandatory field for every Nimbrel Probe agent and distinguishes one instrumented process from the next.

A stream name containing a . (dot), for example` checkout.web`, is refused, as are other unsupported symbols.

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

The requirement is documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name). Browser-agent documentation is available [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

A stream name that is a product name used throughout an organization may need to remain unchanged because reporting is keyed to it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

The behavior is working as intended.

No fix is currently available. Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register. Then carry the original name as a global tag so each trace retains a link between the original and renamed names.
https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}