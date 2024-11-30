from .prompts.loader import load_prompt

class BaseAgent:
    def __init__(self):
        self.system_prompt = load_prompt("admin", "system")