from ..prompts.loader import load_prompt

from .llm import LLM
from .state import State, Message
from .prompt import Prompt, Prompts

class AdminAgent:
    def __init__(self):
        self.name = "admin"
        self.system_prompt = load_prompt("admin", "system")
        self.move_prompt = load_prompt("admin", "move")
    
    def get_prompt(self, state: State) -> Prompts:
        return Prompts([
            Prompt("system", self.system_prompt).append(state.note),
            Prompt("user", state.stringify_history()).append(self.move_prompt),
        ])
    
    def run(self, state: State) -> State:
        # invoke the llm
        llm = LLM()
        messages = self.get_prompt(state).build(self.name)
        response = llm.invoke(messages)
        # update the state
        state.set_propagated_message(Message.parse(response, self.name))

        return state