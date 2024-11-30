from ..prompts.loader import load_prompt

from langchain_openai import ChatOpenAI

from .state import State, Message
from .prompt import Prompt, Prompts

class ParticipantAgent:
    def __init__(self, name: str, law: str):
        self.name = name
        self.law = law
        self.system_prompt = load_prompt("participant", "system")
        self.move_prompt = load_prompt("participant", "move")
    
    def get_prompt(self, state: State) -> Prompts:
        return Prompts([
            Prompt("system", self.system_prompt),
            Prompt("user", state.stringify_history()),
        ])
    
    def run(self, state: State) -> State:
        # judge the propagated message
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        messages = self.get_prompt(state).build(self.name, {"LAW": self.law})
        response = llm.invoke(messages)
        # process the action
        message = Message.parse(response.content, self.name)

        # update the state
        state.set_propagated_message(message)
        return state