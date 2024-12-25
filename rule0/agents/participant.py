from ..orchestrator.action import Action
from ..orchestrator.llm import LLM
from ..orchestrator.message import Message
from ..orchestrator.prompt import Prompt, Prompts
from ..orchestrator.state import State


class ParticipantAgent:
    def __init__(self, name: str, role: str, law: str, base_system_prompt: str, system_prompt: str, move_prompt: str, debug: bool = False):
        self.name = name
        self.role = role
        self.law = law
        self.base_system_prompt = base_system_prompt
        self.system_prompt = system_prompt
        self.move_prompt = move_prompt
        self.debug = debug

    def get_prompt(self, state: State) -> Prompts:
        prompts = [
            Prompt("system", self.base_system_prompt).append(self.system_prompt),
        ]

        current = ""

        for action in state.history:
            if action.sender == "judge":
                continue
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

        if "voter" in self.name:
            prompts[-1].append(
                "You can only vote with $VOTE to choose one of the options."
            )

        return Prompts(prompts)

    def run(self, state: State) -> State:
        # judge the propagated message
        llm = LLM(debug=self.debug)
        messages = self.get_prompt(state).build(
            self.name,
            {"LAW": self.law, "NAME": self.name, "STATE": state.note, "ROLE": self.role},
        )
        response = llm.invoke(messages)
        # process the action
        message = Message.parse(response, self.name)
        # update the state
        state.put_message(message)
        state.consume_tokens(llm.total_input_tokens, llm.total_output_tokens)
        return state
