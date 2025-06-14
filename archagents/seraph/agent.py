import os, json, logging, uuid
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential
from agents.common.retriable_openai import openai_chat_completion
from desktop_app.services.agent_manager import run_agent
from archagents import get_meta
from typing import Optional

MEM_DB = Path("seraph_memory.json")
log = logging.getLogger(__name__)

def _load_mem():
    if MEM_DB.exists():
        return json.loads(MEM_DB.read_text())
    return []

def _save_mem(history):
    MEM_DB.write_text(json.dumps(history, indent=2))

class Archagent:
    """Seraph – meta-orchestrator with simple JSON memory."""
    def __init__(self):
        self.history = _load_mem()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def _llm(self, prompt):
        return openai_chat_completion(
            system="You are Seraph, an orchestration angel.",
            user=prompt,
            temperature=0.2,
        )

    def run(self, *, intent: str = "orchestrate", message: Optional[str] = None, **kw):
        if message:
            self.history.append({"role": "user", "content": message})
            _save_mem(self.history)
        plan = self._llm(f"INTENT={intent} HISTORY={self.history[-5:]}").strip()
        # naive plan format: RUN:<arch_or_agent_id>:<payload>
        if plan.startswith("RUN:"):
            _, target, payload = plan.split(":", 2)
            result = run_agent(target, intent=payload or "default", target_id=str(uuid.uuid4())[:6])
            self.history.append({"role": "assistant", "content": f"Dispatched {target} -> {result}"})
            _save_mem(self.history)
            return result
        return "No action"
