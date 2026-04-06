import httpx
import time
import json

REPOS = [
    "agnuxo-neuro", "agnuxo-secure", "agnuxo-ethos", "agnuxo-quantum",
    "agnuxo-social", "agnuxo-genis", "agnuxo-cosmos", "agnuxo-fabric",
    "agnuxo-syntax", "agnuxo-gaia"
]

def check_agents():
    try:
        r = httpx.get('https://api-production-ff1b.up.railway.app/agents')
        if r.status_code != 200:
            return []
        return r.json()
    except Exception:
        return []

def main():
    print("Verification started. Polling for agents...")
    start = time.time()
    found_set = set()
    
    # Poll for up to 5 minutes
    while time.time() - start < 300:
        agents = check_agents()
        for a in agents:
            aid = a.get("id", "").lower()
            if aid in REPOS and aid not in found_set:
                print(f"  [ONLINE] Agent found: {a.get('name')} ({aid})")
                found_set.add(aid)
        
        if len(found_set) == len(REPOS):
            print("\nSUCCESS: All 10 agents are ONLINE and registered!")
            return
            
        print(f"  (Found {len(found_set)}/10. Waiting 30s...)")
        time.sleep(30)
        
    print(f"\nVerification ended. Total found: {len(found_set)}/10")
    missing = [r for r in REPOS if r not in found_set]
    if missing:
        print(f"Missing: {', '.join(missing)}")

if __name__ == "__main__":
    main()
