# Nimbrel Probe stream name with unsupported symbols

Author: Rune Delacroix
Updated: 2026-01-29

Author: Marlowe Ferrante
Updated: 2026-02-03

### Topic

A stream name is a mandatory field for every Nimbrel Probe agent. Stream names cannot contain arbitrary symbols; the rule is documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name). A stream name containing a dot (.), for example` checkout.web` and other unsupported symbols, is refused. The stream name distinguishes one instrumented process from the next. Only letters, digits, spaces and hyphens are accepted; the rule is documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```

This behavior is working as intended for now. A customer wants the stream name retained exactly because it is the product name used throughout the organization, and reporting keys off it.

### Environment

All Nimbrel Probe agents

### Instructions/Answer

A workaround is available. No fix is available at present; rename the stream to remove unsupported symbols so the Nimbrel Probe agent registers. Carry the original name as a global tag so each trace links the real name to the renamed one: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags

{internal-notes}
https://tickets.nimbrel.example/700Bb00000QrmTD
{/internal-notes}
{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}