from ..orchestrator.action import Action
from ..orchestrator.llm import LLM
from ..orchestrator.message import Message
from ..orchestrator.prompt import Prompt, Prompts
from ..orchestrator.state import State


class AdminAgent:
    def __init__(self, base_system_prompt: str, system_prompt: str, move_prompt: str, debug: bool = False):
        self.name = "admin"
        self.base_system_prompt = base_system_prompt
        self.system_prompt = system_prompt
        self.move_prompt = move_prompt
        self.debug = debug

    def get_prompt(self, state: State) -> Prompts:
        prompts = [
            Prompt("system", self.base_system_prompt).append(self.system_prompt).append(state.note),
        ]

        current = ""

        for action in state.history:
            if action.sender != self.name:
                current += action.readable()
            else:
                if current:
                    prompts.append(Prompt("user", current))
                    current = ""

                if action.action == Action.SPEAK:
                    prompts.append(Prompt("assistant", action.args))
                else:
                    prompts.append(
                        Prompt(
                            "assistant", "$" + action.action.value + ":" + action.args
                        )
                    )

        if current:
            prompts.append(Prompt("user", current))

        prompts.append(Prompt("user", self.move_prompt))

        return Prompts(prompts)

    def run(self, state: State) -> State:
        # invoke the llm
        llm = LLM(debug=self.debug)
        messages = self.get_prompt(state).build(self.name)
        response = llm.invoke(messages)
        state.consume_tokens(llm.total_input_tokens, llm.total_output_tokens)
        # update the state
        state.put_message(Message.parse(response, self.name))

        return state
