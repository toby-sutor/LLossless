# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

Stream name is one of the mandatory fields for every Nimbrel Probe agent and separates one instrumented process from another. Stream names containing unsupported symbols—such as dots in `checkout.web` and others—are refused by Nimbrel Probe, as documented in the [Java](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [browser](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name) agent configuration references. Stream names are validated against `^[A-Za-z0-9 -]+$`: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

A way round it that works:

1. Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.
2. Then carry the original name along as a global tag, so each trace keeps a link between the real name and the renamed one, as documented [here](https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags).

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}