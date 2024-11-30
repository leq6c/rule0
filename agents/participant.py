from ..prompts.loader import load_prompt

class ParticipantAgent:
    def __init__(self, name: str, estoppel: str):
        self.name = name
        self.estoppel = estoppel
        self.prompt = load_prompt("speaker", "system")