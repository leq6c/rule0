from ..prompts.loader import load_prompt

from ..world.llm import LLM
from ..world.state import State
from ..world.message import Message
from ..world.prompt import Prompt, Prompts


class AdminAgent:
    def __init__(self, debug: bool = False):
        self.name = "admin"
        self.system_prompt = load_prompt("admin", "system")
        self.move_prompt = load_prompt("admin", "move")
        self.debug = debug

    def get_prompt(self, state: State) -> Prompts:
        return Prompts(
            [
                Prompt("system", self.system_prompt).append(state.note),
                Prompt(
                    "user", "# DISCUSSION HISTORY\n" + state.stringify_history() + "\n"
                ).append(self.move_prompt),
            ]
        )

    def run(self, state: State) -> State:
        # invoke the llm
        llm = LLM(debug=self.debug)
        messages = self.get_prompt(state).build(self.name)
        response = llm.invoke(messages)
        # update the state
        state.put_message(Message.parse(response, self.name))

        return state
