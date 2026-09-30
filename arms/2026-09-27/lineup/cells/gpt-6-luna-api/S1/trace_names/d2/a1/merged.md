# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

Author: Marlowe Ferrante
Updated: 2026-02-03

### Topic

The stream name is a mandatory field for every Nimbrel Probe agent. It distinguishes one instrumented process from another. A stream name cannot contain unsupported symbols: only letters, digits, spaces, and hyphens are accepted. A dot, as in ` checkout.web`, and other unsupported symbols are refused. The restriction is documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

A customer may need to preserve a stream name exactly when it is the product name used throughout the organization and reporting keys off it. The validation is working as intended for now.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

There is no fix at present. A working workaround is to:

1) Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.
2) Carry the original name as a global tag so each trace retains a link between the real name and the renamed one.
   https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}