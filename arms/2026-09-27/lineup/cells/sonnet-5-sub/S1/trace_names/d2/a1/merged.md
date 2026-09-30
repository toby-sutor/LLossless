# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

The stream name is a mandatory field for every Nimbrel Probe agent, and it is what separates one instrumented process from another. It cannot contain arbitrary symbols, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

For example, a stream name such as `checkout.web`, which contains a dot, along with a number of other symbols, is refused by Nimbrel Probe.

However, one customer wanted the stream name left exactly as it stood, because that string was the product name used everywhere in the organization and their reporting keyed off it.

### Cause

Working as intended for now.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

There is no fix planned at present. The workaround is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register, and then carry the original name along as a global tag so each trace keeps a link between the real name and the renamed one: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}