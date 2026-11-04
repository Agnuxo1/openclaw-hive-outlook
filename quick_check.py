# Project: openclaw-hive-outlook
# Author: Francisco Angulo de Lafuente
# ORCID: https://orcid.org/0009-0001-1634-7063
# Copyright year: 2026 (year of the first tracked commit)
# Attribution recorded: 2026-11-04
# License scope: unresolved; this header grants no license.

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
