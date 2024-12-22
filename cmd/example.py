from rule0.builder import AgentConfig, Builder
from rule0.prompts.loader import load_prompt


def run():
    builder = Builder(topic="Pizza or Sushi", agents=[
        AgentConfig("participantA", "Controversialist", "I like pizza", "normal"),
        AgentConfig("participantB", "Controversialist", "I like sushi", "normal"),
        AgentConfig("voterA", "Voter", "equal", "normal"),
        AgentConfig("voterB", "Voter", "equal", "normal"),
        AgentConfig("voterC", "Voter", "equal", "normal"),
    ], prompts={})

    for log in builder.run():
        print(log)