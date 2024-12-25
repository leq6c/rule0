from rule0.builder import AgentConfig, Builder
from rule0.prompts.loader import load_prompt


def run():
    builder = Builder(topic="Pizza or Sushi", agents=[
        AgentConfig("participantA", "Controversialist", "I like pizza", "normal"),
        AgentConfig("participantB", "Controversialist", "I like sushi", "normal"),
        AgentConfig("voterA", "Voter", "equal", "normal"),
        AgentConfig("voterB", "Voter", "equal", "normal"),
        AgentConfig("voterC", "Voter", "equal", "normal"),
    ], prompts={
        "base": {
            "system": load_prompt("base", "system"),
        },
        "admin": {
            "system": load_prompt("admin", "system"),
            "move": load_prompt("admin", "move"),
        },
        "participant": {
            "system": load_prompt("participant", "system"),
            "move": load_prompt("participant", "move"),
        },
        "judge": {
            "system": load_prompt("judge", "system"),
            "move": load_prompt("judge", "move"),
        },
    })

    for log in builder.run():
        print(log)