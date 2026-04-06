import httpx
import json
import zipfile
import io
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Set via environment variable
OWNER = "Agnuxo-Outlook"
REPO = "agnuxo-neuro"

def main():
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    # 1. Get latest run
    r = httpx.get(f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs", headers=headers)
    runs = r.json().get("workflow_runs", [])
    if not runs:
        print("No runs found")
        return
    
    run_id = runs[0]["id"]
    print(f"Latest run ID: {run_id}")
    
    # 2. Get logs
    r = httpx.get(f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/logs", headers=headers, follow_redirects=True)
    if r.status_code != 200:
        print(f"Failed to get logs: {r.status_code}")
        return
        
    # 3. Extract and print
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for name in z.namelist():
            if "run-agent" in name.lower() or "run_agent" in name.lower() or "4_" in name: # Main step is usually 4_
                content = z.read(name).decode("utf-8", errors="ignore")
                if "error" in content.lower() or "exception" in content.lower() or "traceback" in content.lower():
                    print(f"\n--- LOG: {name} ---")
                    print(content[-3000:]) # Last 3k chars

if __name__ == "__main__":
    main()
