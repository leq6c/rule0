from ..prompts.loader import load_prompt

from .state import State, Message, CallMessage
from .action import Action
from .prompt import Prompt, Prompts

from .llm import LLM

class JudgeAgent:
    def __init__(self):
        self.name = "judge"
        self.system_prompt = load_prompt("judge", "system")
        self.move_prompt = load_prompt("judge", "move")
    
    def get_prompt(self, state: State) -> Prompts:
        return Prompts([
            Prompt("system", self.system_prompt),
            Prompt("user", state.stringify_history() + "\n" + state.note + "\n" + self.move_prompt),
        ])
    
    def run(self, state: State) -> State:
        # judge the propagated message
        llm = LLM()
        messages = self.get_prompt(state).build(state.propagated_message.sender, {"MESSAGE": state.propagated_message.raw})
        response = llm.invoke(messages)
        # process the action
        judge_message = Message.parse(response, self.name)
        if judge_message.action == Action.ACCEPT:
            message = state.accept_propagated_message()
            if isinstance(message, CallMessage):
                state.set_next_speaker(message.target)
            else:
                state.set_next_speaker("admin")
        else:
            state.deny_propagated_message()
            state.set_next_speaker("admin")

        # update the state
        state.set_propagated_message(judge_message)
        return state