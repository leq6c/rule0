import getpass
import os

from rule0.builder import AgentConfig, Builder
from rule0.prompts.loader import load_prompt

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

builder = Builder(topic="Pizza or Sushi", agents=[
    AgentConfig("participantA", "Controversialist", "I like pizza", "normal"),
    AgentConfig("participantB", "Controversialist", "I like sushi", "normal"),
    AgentConfig("voterA", "Voter", "equal", "normal"),
    AgentConfig("voterB", "Voter", "equal", "normal"),
    AgentConfig("voterC", "Voter", "equal", "normal"),
], prompts={})

initial_note = load_prompt("state", "default")

for log in builder.run(initial_note):
    print(log)
