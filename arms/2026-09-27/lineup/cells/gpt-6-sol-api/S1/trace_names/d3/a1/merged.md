# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

Author: Marlowe Ferrante
Updated: 2026-02-03

### Topic

The stream name is a mandatory field for every Nimbrel Probe agent and separates one instrumented process from another. Stream names cannot contain arbitrary symbols, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

The same ^[A-Za-z0-9 -]+$ restriction is documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name). A stream name containing a . (dot), such as ` checkout.web`, is refused, as are names containing other unsupported symbols. This refusal is working as intended for now.

A customer may need the stream name to remain unchanged because it is the product name used throughout the organization and reporting keys off it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

No fix is available at present. The workaround is:

1) Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.
2) Carry the original name as a global tag so each trace retains a link between the original and renamed names.
https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}