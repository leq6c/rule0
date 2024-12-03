from ..prompts.loader import load_prompt

from ..world.llm import LLM
from ..world.state import State
from ..world.message import Message
from ..world.prompt import Prompt, Prompts


class ParticipantAgent:
    def __init__(self, name: str, law: str, debug: bool = False):
        self.name = name
        self.law = law
        self.system_prompt = load_prompt("participant", "system")
        self.note = load_prompt("participant", "note")
        self.debug = debug
        if "voter" in self.name:
            self.note = self.note.replace("_participant_", "_voter_")

    def get_prompt(self, state: State) -> Prompts:
        return Prompts(
            [
                Prompt("system", self.system_prompt).append(self.note),
                Prompt("user", state.stringify_history()),
            ]
        )

    def run(self, state: State) -> State:
        # judge the propagated message
        llm = LLM(model="gpt-4o-mini", temperature=0.7, debug=self.debug)
        messages = self.get_prompt(state).build(
            self.name, {"LAW": self.law, "NAME": self.name}
        )
        response = llm.invoke(messages)
        # process the action
        message = Message.parse(response, self.name)
        # update the state
        state.put_message(message)

        return state
