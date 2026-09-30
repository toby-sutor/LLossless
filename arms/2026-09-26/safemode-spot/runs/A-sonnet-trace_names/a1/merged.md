# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix, Marlowe Ferrante
Updated: 2026-02-03

### Topic

The stream name is a mandatory field for every Nimbrel Probe agent, and it is what separates one instrumented process from the next. It cannot contain arbitrary symbols, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

Only letters, digits, spaces and hyphens are accepted (the name has to match ^[A-Za-z0-9 -]+$). A stream name containing a . (dot), for example `checkout.web`, along with a number of other symbols, is refused. This is working as intended for now.

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

However, a customer may want the stream name left exactly as it stands because that string is the product name in use everywhere in the organisation and their reporting is keyed off it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

A way round it that works

There is no fix at present. Rename the stream without the refused symbol:

1) Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
2) Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one
https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}

{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}