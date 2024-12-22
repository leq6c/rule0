default = """
# State
## Topic
The topic is "{{topic}}".

## List of participants
```
{{agents}}
```
"""

class NotePrompt:
    def __init__(self, note: str = default):
        self.note = note.strip()
    
    def list_agents(self, agents: list[any]) -> str:
        header = "Name,Role"
        return "\n".join([header] + [f"{agent.name},({agent.role})" for agent in agents])
    
    def apply(self, topic: str, agents: list[any]) -> str:
        note = self.note.replace("{{topic}}", topic)
        note = note.replace("{{agents}}", self.list_agents(agents))
        return note