# Project: openclaw-hive-outlook
# Author: Francisco Angulo de Lafuente
# ORCID: https://orcid.org/0009-0001-1634-7063
# Copyright year: 2026 (year of the first tracked commit)
# Attribution recorded: 2026-11-04
# License scope: unresolved; this header grants no license.

import asyncio
import os
from advanced_agent_base import AdvancedAgent
from identities import IDENTITIES

# This placeholder will be replaced by the deployment script
AGENT_KEY = "PLACEHOLDER_AGENT_KEY"

async def main():
    if AGENT_KEY not in IDENTITIES:
        print(f"Error: Agent key {AGENT_KEY} not found in identities.py")
        return
        
    info = IDENTITIES[AGENT_KEY]
    agent = AdvancedAgent(
        agent_id=info["name"].lower(),
        agent_name=info["name"],
        specialization=info["specialization"],
        soul_prompt=info["soul"]
    )
    await agent.run_loop()

if __name__ == "__main__":
    asyncio.run(main())
