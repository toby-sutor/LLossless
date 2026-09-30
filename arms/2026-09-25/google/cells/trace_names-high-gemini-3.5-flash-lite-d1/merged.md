# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

### Topic

Stream name is one of the mandatory fields for every Nimbrel Probe agent and is what separates one instrumented process from the next. The stream name can not contain arbitrary symbols as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name). Stream names containing a . (dot) for example` checkout.web` along with a number of other symbols are refused by Nimbrel Probe. Only letters, digits, spaces and hyphens are accepted (it has to match ^[A-Za-z0-9 -]+$) as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

However, one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org and their reporting keyed off it when.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

A way round it that works

1) Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
2) Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one
https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

Working as intended for now

No fix at present, rename the stream without the refused symbol

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}