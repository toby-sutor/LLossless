# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

Stream names are mandatory fields for Nimbrel Probe agents and separate one instrumented process from another. Stream names are validated against a specific pattern:

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

Unsupported symbols such as dots (for example, `checkout.web`) cause the agent to refuse registration. Organizations often use product names that may contain unsupported characters. One customer wanted to preserve a product name exactly as it appeared in their reporting systems, requiring a workaround.

### Environment

All Nimbrel Probe agents

### Cause

This validation is working as intended.

### Instructions

Rename the stream to drop the unsupported symbols so the agent will register. Carry the original name along as a global tag, so each trace maintains a link between the real name and the renamed one: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}