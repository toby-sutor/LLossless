# Nimbrel Probe - dot in stream name is refused

Author: Marlowe Ferrante
Updated: 2026-02-03

### Issue Description

Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe

The Nimbrel Probe stream name is what seperates one instrumented process from the next. Only letters, digits, spaces and hyphens are accepted (it has to match ^[A-Za-z0-9 -]+$) as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)

### Cause

Working as intended for now

### Workaround

No fix at present , rename the stream without the refused symbol

### Resolution

No fix at present , rename the stream without the refused symbol


{internal-notes}
https://tickets.nimbrel.example/700Bb00000LnqWs
{/internal-notes}
