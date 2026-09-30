# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

Stream name is a mandatory field for every Nimbrel Probe agent. The stream name cannot contain arbitrary symbols as documented for [Java](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [browser](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name) agents.

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

The stream name separates one instrumented process from another. This constraint is intentional. Characters such as dots are refused; for example, stream names like checkout.web cannot be used. Some customers need the stream name to match their product name, which is used in reporting throughout their organization, but the validation constraint makes this impossible.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

Rename the stream to use only supported characters. Additionally, carry the original name as a global tag so each trace maintains a link between the renamed stream and the original name, as documented for [Node.js](https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags).

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}