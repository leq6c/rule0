from ..prompts.loader import load_prompt
from ..world.action import Action
from ..world.llm import LLM
from ..world.message import Message
from ..world.prompt import Prompt, Prompts
from ..world.state import State


class ParticipantAgent:
    def __init__(self, name: str, law: str, debug: bool = False):
        self.name = name
        self.law = law
        self.system_prompt = load_prompt("participant", "system")
        self.move_prompt = load_prompt("participant", "move")
        self.note = load_prompt("participant", "note")
        self.debug = debug
        if "voter" in self.name:
            self.note = self.note.replace("_participant_", "_voter_")

    def get_prompt(self, state: State) -> Prompts:
        prompts = [
            Prompt("system", self.system_prompt).append(state.note).append(self.note),
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
                    prompts.append(Prompt("assistant", "$" + action.action.value + ":" + action.args))

        if current:
            prompts.append(Prompt("user", current))
        
        prompts.append(Prompt("user", self.move_prompt))

        if "voter" in self.name:
            prompts[-1].append("You can only vote with $VOTE to choose one of the options.")

        return Prompts(prompts)

    def run(self, state: State) -> State:
        # judge the propagated message
        llm = LLM(debug=self.debug)
        messages = self.get_prompt(state).build(
            self.name, {"LAW": self.law, "NAME": self.name}
        )
        response = llm.invoke(messages)
        # process the action
        message = Message.parse(response, self.name)
        # update the state
        state.put_message(message)

        return state
