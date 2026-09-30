import json,sys,urllib.request,urllib.error
key=[l.split('=',1)[1].strip().strip('\'"') for l in open('<home>/Documents/Dev/vibe-coding/claimcheck/.env') if l.strip().removeprefix('export ').startswith('GOOGLE_AI_API_KEY=')][0]
m=sys.argv[1]
r=urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent',data=json.dumps({"contents":[{"parts":[{"text":"Say hello in three words."}]}]}).encode(),headers={'Content-Type':'application/json','x-goog-api-key':key})
try:
    with urllib.request.urlopen(r,timeout=120) as x: s,b=x.status,x.read().decode()
except urllib.error.HTTPError as e: s,b=e.code,e.read().decode()
print('native',m,s,b[:1500])
