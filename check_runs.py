# Project: openclaw-hive-outlook
# Author: Francisco Angulo de Lafuente
# ORCID: https://orcid.org/0009-0001-1634-7063
# Copyright year: 2026 (year of the first tracked commit)
# Attribution recorded: 2026-11-04
# License scope: unresolved; this header grants no license.

import httpx
import json

TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Set via environment variable
OWNER = "Agnuxo-Outlook"
REPOS = [
    "agnuxo-neuro", "agnuxo-secure", "agnuxo-ethos", "agnuxo-quantum",
    "agnuxo-social", "agnuxo-genis", "agnuxo-cosmos", "agnuxo-fabric",
    "agnuxo-syntax", "agnuxo-gaia"
]

def get_runs(repo):
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    r = httpx.get(f"https://api.github.com/repos/{OWNER}/{repo}/actions/runs", headers=headers)
    if r.status_code == 200:
        return r.json().get("workflow_runs", [])
    return []

def main():
    print(f"{'Repository':<20} | {'Status':<15} | {'Conclusion':<15} | {'Updated At':<25}")
    print("-" * 80)
    for repo in REPOS:
        runs = get_runs(repo)
        if runs:
            run = runs[0]
            print(f"{repo:<20} | {run.get('status'):<15} | {str(run.get('conclusion')):<15} | {run.get('updated_at'):<25}")
        else:
            print(f"{repo:<20} | {'No runs found':<15} | {'N/A':<15} | {'N/A':<25}")

if __name__ == "__main__":
    main()
