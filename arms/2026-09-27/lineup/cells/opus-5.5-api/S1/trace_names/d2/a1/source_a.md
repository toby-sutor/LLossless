# Nimbrel Probe stream name  with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

Stream name is one of the mandatry field for every Nimbrel Probe agent.  The stream name cant contain arbitrary symbols as documented
[here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name)

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

However , one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org and their reporting keyed of it when

### Environment

All Nimbrel Probe agents

### Instructions/Answer

A way round it that works

1) Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
2) Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one
https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags


{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}
