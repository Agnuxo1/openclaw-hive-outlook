import httpx
r = httpx.get('https://api-production-ff1b.up.railway.app/agents')
if r.status_code == 200:
    agents = r.json()
    outlook = [a for a in agents if 'agnuxo' in a.get('id', '').lower()]
    print(f"Online: {len(outlook)}/10")
    for a in outlook:
        print(f" - {a.get('name')}")
else:
    print(f"Error: {r.status_code}")
