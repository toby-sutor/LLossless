import json,glob,sys,os
tot=0
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__),'*.jsonl'))):
    ev=[json.loads(l) for l in open(f) if l.strip()]
    res=[e for e in ev if e.get('type')=='result']
    if not res: print(os.path.basename(f),'NO RESULT'); continue
    r=res[-1]; tot+=r.get('total_cost_usd') or 0
    ws=sum((v.get('webSearchRequests') or 0) for v in (r.get('modelUsage') or {}).values())
    tools=[c.get('name') for e in ev if e.get('type')=='assistant' for c in e['message'].get('content',[]) if c.get('type')=='tool_use']
    think=sum(1 for e in ev if e.get('type')=='assistant' for c in e['message'].get('content',[]) if c.get('type')=='thinking')
    print(f"{os.path.basename(f):32s} turns={r.get('num_turns'):3} webSearchRequests={ws:3} tool_uses={tools} thinking_blocks={think} usd={r.get('total_cost_usd'):.4f}")
print('total usd',round(tot,4))
