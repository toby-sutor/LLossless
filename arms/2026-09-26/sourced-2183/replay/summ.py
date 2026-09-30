import json,glob,os
tot=0
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),'*.out'))):
    lines=[l for l in open(f) if l.strip()]
    ev=[]
    for l in lines:
        try: ev.append(json.loads(l))
        except Exception: pass
    res=[e for e in ev if e.get('type')=='result']
    if not res: print(os.path.basename(f),'NO RESULT'); continue
    r=res[-1]; tot+=r.get('total_cost_usd') or 0
    ws=sum((v.get('webSearchRequests') or 0) for v in (r.get('modelUsage') or {}).values())
    tools=[c.get('name') for e in ev if e.get('type')=='assistant' for c in e['message'].get('content',[]) if c.get('type')=='tool_use']
    print(f"{os.path.basename(f):34s} turns={r.get('num_turns'):3} webSearchRequests={ws:3} tool_uses={len(tools)} {sorted(set(tools))} subtype={r.get('subtype')} usd={r.get('total_cost_usd'):.4f}")
print('total usd',round(tot,4))
