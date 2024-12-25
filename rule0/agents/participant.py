import random

from ..orchestrator.action import Action
from ..orchestrator.llm import LLM
from ..orchestrator.message import Message
from ..orchestrator.prompt import Prompt, Prompts
from ..orchestrator.state import State


class ConditionalAction:
    def __init__(self, id: str, percentage: int, action: str):
        self.id = id
        self.percentage = percentage
        self.action = action

class ParticipantAgent:
    def __init__(self, name: str, role: str, law: str, base_system_prompt: str, system_prompt: str, move_prompt: str, conditional_actions: list[ConditionalAction], debug: bool = False):
        self.name = name
        self.role = role
        self.law = law
        self.base_system_prompt = base_system_prompt
        self.system_prompt = system_prompt
        self.move_prompt = move_prompt
        self.conditional_actions = conditional_actions
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

        conditional_action = self.choose_conditional_action()
        if conditional_action and conditional_action.action:
            prompts.append(Prompt("user", "You may use this strategy if you think you can use it on the current situation: \n" + conditional_action.action))

        if "voter" in self.name:
            prompts[-1].append(
                "You can only vote with $VOTE to choose one of the options."
            )

        return Prompts(prompts)
    
    def choose_conditional_action(self) -> ConditionalAction:
        if not self.conditional_actions:
            return None
        conditional_actions = self.conditional_actions.copy()
        total_percentage = sum(conditional_action.percentage for conditional_action in conditional_actions)
        if total_percentage < 100:
            conditional_actions.append(ConditionalAction("default", 100 - total_percentage, ""))
        random_number = random.randint(0, 100)
        for conditional_action in conditional_actions:
            if random_number < conditional_action.percentage:
                return conditional_action
            random_number -= conditional_action.percentage
        return None

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
