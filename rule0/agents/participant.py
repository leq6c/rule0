from ..prompts.loader import load_prompt

from .llm import LLM
from .state import State, Message
from .prompt import Prompt, Prompts

class ParticipantAgent:
    def __init__(self, name: str, law: str):
        self.name = name
        self.law = law
        self.system_prompt = load_prompt("participant", "system")
        self.note = load_prompt("participant", "note")
    
    def get_prompt(self, state: State) -> Prompts:
        return Prompts([
            Prompt("system", self.system_prompt).append(self.note),
            Prompt("user", state.stringify_history()),
        ])
    
    def run(self, state: State) -> State:
        # judge the propagated message
        llm = LLM()
        messages = self.get_prompt(state).build(self.name, {"LAW": self.law, "NAME": self.name})
        response = llm.invoke(messages)
        # process the action
        message = Message.parse(response, self.name)

        # update the state
        state.set_propagated_message(message)
        return state