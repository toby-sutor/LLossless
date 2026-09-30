# Nimbrel Probe stream name with unsupported symbols

Author: Marlowe Ferrante
Updated: 2026-02-03

### Topic

Stream name is a mandatory field for every Nimbrel Probe agent, and it separates one instrumented process from another. The stream name cannot contain arbitrary symbols. Stream names containing a dot (for example, `checkout.web`) and other characters are refused by Nimbrel Probe.

Stream names are validated against the pattern below before the agent registers. Only letters, digits, spaces and hyphens are accepted; anything else causes the agent to refuse to start. This behavior is working as intended.

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

See the documentation for details: [Java](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name), [Node.js](https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags), [Browser](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

One customer wanted to keep a stream name exactly as it stood because that string was their product name in use throughout their organization and their reporting depended on it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

Rename the stream to contain only supported symbols so the Nimbrel Probe agent will register. Then carry the original name along as a global tag, which allows each trace to maintain a link between the original name and the renamed one.

For details on configuring global tags, see the [Node.js documentation](https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags).

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}