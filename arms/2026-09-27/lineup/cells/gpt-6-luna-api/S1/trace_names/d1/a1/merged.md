# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

The stream name is a mandatory field for every Nimbrel Probe agent and separates one instrumented process from the next. Only letters, digits, spaces and hyphens are accepted; a dot, as in ` checkout.web`, and other unsupported symbols are refused. The rules are documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

This validation behavior is working as intended for now. An organization may need to retain the exact stream name when it is the product name used throughout the organization and reporting keys off it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

There is no fix at present; rename the stream without the refused symbol. A working workaround is:

1) Rename the stream to remove unsupported symbols so the Nimbrel Probe agent registers.
2) Add the original name as a global tag so each trace keeps a link between the real name and the renamed one: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}