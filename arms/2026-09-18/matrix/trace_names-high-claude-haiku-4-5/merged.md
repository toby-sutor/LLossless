# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

Stream name is one of the mandatory fields for every Nimbrel Probe agent. The stream name cannot contain arbitrary symbols. Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers: letters, digits, spaces and hyphens only, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

### Environment

All Nimbrel Probe agents

### Instructions/Answer

Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. Then carry the original name along as a global tag, so each trace keeps a link between the real name and the renamed one.

https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}