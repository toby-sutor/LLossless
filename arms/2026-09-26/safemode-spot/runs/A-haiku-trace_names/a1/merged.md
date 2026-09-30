# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

Stream name is one of the mandatory fields for every Nimbrel Probe agent and is what separates one instrumented process from the next. Stream names cannot contain arbitrary symbols—dots, for example—and can only use letters, digits, spaces and hyphens (validated against ^[A-Za-z0-9 -]+$ as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

This constraint is by design. However, where a product name in use across an organization does not conform to these restrictions, a workaround is available.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

Rename the stream to use only supported characters so the Nimbrel Probe agent will register. To maintain reporting continuity with the original product name, carry the original name as a global tag, preserving the link between the renamed stream and its actual name as documented [here](https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags).

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}