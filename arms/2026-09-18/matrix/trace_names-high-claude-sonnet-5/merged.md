# Nimbrel Probe stream name with unsupported symbols

Author: Marlowe Ferrante
Updated: 2026-02-03

### Topic

The stream name is a mandatory field for every Nimbrel Probe agent, and it is what separates one instrumented process from another.

The stream name can't contain arbitrary symbols, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

A stream name containing a dot - for example `checkout.web` - or any other disallowed character is refused by Nimbrel Probe agents.

This restriction is intentional, and there are currently no plans to change it.

In some cases users want to keep the original stream name unchanged because it matches a product name used throughout their organization, and their reporting depends on that exact string.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

A way round it that works:

1) There is no fix at present: rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.
2) Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one
https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}