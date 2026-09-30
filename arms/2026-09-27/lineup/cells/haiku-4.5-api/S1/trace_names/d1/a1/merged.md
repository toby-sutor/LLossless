# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-02-03

### Topic

Stream name is one of the mandatory field for every Nimbrel Probe agent. The stream name cannot contain arbitrary symbols as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name)

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

Symbols such as dots (for example, checkout.web) are refused by Nimbrel Probe. One customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the organization and their reporting keyed off it.

### Environment

All Nimbrel Probe agents

### Workaround

Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}