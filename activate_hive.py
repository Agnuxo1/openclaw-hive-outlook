# Project: openclaw-hive-outlook
# Author: Francisco Angulo de Lafuente
# ORCID: https://orcid.org/0009-0001-1634-7063
# Copyright year: 2026 (year of the first tracked commit)
# Attribution recorded: 2026-11-04
# License scope: unresolved; this header grants no license.

import base64
import httpx
from nacl import encoding, public
import json
import time

TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Set via environment variable
OWNER = "Agnuxo-Outlook"
REPOS = [
    "agnuxo-neuro", "agnuxo-secure", "agnuxo-ethos", "agnuxo-quantum",
    "agnuxo-social", "agnuxo-genis", "agnuxo-cosmos", "agnuxo-fabric",
    "agnuxo-syntax", "agnuxo-gaia"
]

SECRETS = {
    "CEREBRAS_API_KEY": os.environ.get("CEREBRAS_API_KEY", ""),
    "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", ""),
    "QWEN_API_KEY": os.environ.get("QWEN_API_KEY", "")
}

def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key_obj = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key_obj)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def set_secret(repo, name, value):
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    # 1. Get public key
    r = httpx.get(f"https://api.github.com/repos/{OWNER}/{repo}/actions/secrets/public-key", headers=headers)
    r.raise_for_status()
    key_data = r.json()
    
    # 2. Encrypt
    encrypted_value = encrypt(key_data["key"], value)
    
    # 3. Put secret
    r = httpx.put(
        f"https://api.github.com/repos/{OWNER}/{repo}/actions/secrets/{name}",
        headers=headers,
        json={
            "encrypted_value": encrypted_value,
            "key_id": key_data["key_id"]
        }
    )
    r.raise_for_status()
    print(f"  Secret {name} set for {repo}")

def trigger_workflow(repo):
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    r = httpx.post(
        f"https://api.github.com/repos/{OWNER}/{repo}/actions/workflows/agent-loop.yml/dispatches",
        headers=headers,
        json={"ref": "main"}
    )
    if r.status_code == 204:
        print(f"  Workflow triggered for {repo}")
    else:
        print(f"  Failed to trigger workflow for {repo}: {r.status_code} {r.text}")

def main():
    for repo in REPOS:
        print(f"Activating {repo}...")
        try:
            for name, value in SECRETS.items():
                set_secret(repo, name, value)
            trigger_workflow(repo)
        except Exception as e:
            print(f"  Error activating {repo}: {e}")

if __name__ == "__main__":
    main()
