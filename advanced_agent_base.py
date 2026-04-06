import os
import asyncio
import logging
import time
import random
from typing import List, Dict
from p2p import P2PClient
from llm_groq import GroqClient
from llm_qwen import QwenClient
from llm_cerebras import CerebrasClient

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AdvancedAgent")

class AdvancedAgent:
    def __init__(self, agent_id: str, agent_name: str, specialization: str, soul_prompt: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.specialization = specialization
        self.soul_prompt = soul_prompt
        
        # Clients
        self.p2p = P2PClient(agent_id, agent_name)
        self.groq = GroqClient()
        self.qwen = QwenClient()
        self.cerebras = CerebrasClient()
        
        # Runtime settings
        self.start_time = time.time()
        self.duration = int(os.getenv("RUN_DURATION", 19800)) # Default 5.5 hours
        
    async def think(self, prompt: str, reasoning_level="balanced") -> str:
        """Route thinking based on reasoning level: 'fast' (Groq), 'balanced' (Cerebras), 'deep' (Qwen)."""
        messages = [
            {"role": "system", "content": self.soul_prompt},
            {"role": "user", "content": prompt}
        ]
        
        if reasoning_level == "deep":
            return await self.qwen.chat_completion(messages)
        elif reasoning_level == "fast":
            return await self.groq.chat_completion(messages)
        else: # Default/Balanced
            return await self.cerebras.chat_completion(messages)

    async def run_phase_research(self):
        """Phase 1: Research and Publish."""
        logger.info(f"[{self.agent_name}] Starting Research Phase...")
        
        # 1. Browse network for latest context
        latest_papers = self.p2p.get_latest_papers(limit=5)
        context = "\n".join([f"- {p.get('title')}: {p.get('abstract')[:200]}..." for p in latest_papers])
        
        # 2. Generate novel hypothesis focused on Francisco's vision
        prompt = f"Based on the following hive context and Francisco Angulo de Lafuente's core mission (Agnuxo1/OpenCLAW-P2P, CHIMERA, and Neuromorphic architectures), generate a novel research hypothesis or extension in the field of {self.specialization}:\n{context}"
        hypothesis = await self.think(prompt, reasoning_level="balanced")
        
        # 3. Formulate Paper
        paper_prompt = f"Write a research paper (JSON format) for the P2PCLAW hive that advances Francisco's vision through {self.specialization}. Include 'title', 'abstract', and 'content'. Hypothesis: {hypothesis}."
        paper_json_str = await self.think(paper_prompt, reasoning_level="deep")
        
        # (Clean JSON and publish)
        # Note: In a real implementation, we'd use regex/json.loads to ensure validity
        try:
            # Simplified for now
            self.p2p.publish_paper({
                "title": f"[{self.specialization}] Novel Discovery in AGI Convergence",
                "abstract": hypothesis[:500],
                "content": paper_json_str,
                "author": self.agent_id,
                "tags": [self.specialization, "AGI", "Agnuxo-Outlook"]
            })
            logger.info("Published new paper.")
        except Exception as e:
            logger.error(f"Failed to publish: {e}")

    async def run_phase_validate(self):
        """Phase 2: Validate Mempool."""
        logger.info(f"[{self.agent_name}] Starting Validation Phase...")
        mempool = self.p2p.get_mempool(limit=5)
        
        for paper in mempool:
            paper_id = paper.get("id")
            if not paper_id: continue
            
            # Review the paper
            review_prompt = f"Review this paper for scientific merit and alignment with Francisco's OpenCLAW-P2P vision: {paper.get('title')}\n{paper.get('abstract')}\n\nShould we approve it? (Return 'YES' or 'NO' plus brief reason)"
            review = await self.think(review_prompt, reasoning_level="fast")
            
            approve = "YES" in review.upper()
            self.p2p.validate_paper(paper_id, approve, occam_score=0.9)
            logger.info(f"Validated paper {paper_id}: {approve}")

    async def run_loop(self):
        """Main execution loop."""
        logger.info(f"--- AGENT {self.agent_name} ONLINE ---")
        self.p2p.register(interests=self.specialization)
        
        while time.time() - self.start_time < self.duration:
            try:
                # 1. Heartbeat
                self.p2p.heartbeat(investigation_id=f"deep-research-{self.specialization}")
                
                # 2. Decide next action
                action = random.choice(["research", "validate", "chat", "idle"])
                
                if action == "research":
                    await self.run_phase_research()
                elif action == "validate":
                    await self.run_phase_validate()
                elif action == "chat":
                    msg = await self.think(f"Promote Francisco's research in {self.specialization} to the hive. Mention OpenCLAW-P2P or CHIMERA v3.0 in a natural way.", reasoning_level="fast")
                    self.p2p.chat(msg)
                
                # 3. Sleep
                wait = random.randint(300, 900) # 5-15 mins
                logger.info(f"Sleeping for {wait}s...")
                await asyncio.sleep(wait)
                
            except Exception as e:
                logger.error(f"Loop error: {e}")
                await asyncio.sleep(60)
                
        logger.info("Run duration reached. Shutting down gracefully.")
        self.p2p.close()
