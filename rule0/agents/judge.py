from ..prompts.loader import load_prompt

from ..world.state import State
from ..world.message import Message
from ..world.action import Action
from ..world.prompt import Prompt, Prompts
from ..world.llm import LLM


class JudgeAgent:
    def __init__(self, debug: bool = False):
        self.name = "judge"
        self.system_prompt = load_prompt("judge", "system")
        self.move_prompt = load_prompt("judge", "move")
        self.debug = debug

    def get_prompt(self, state: State) -> Prompts:
        return Prompts(
            [
                Prompt("system", self.system_prompt),
                Prompt(
                    "user",
                    state.stringify_history()
                    + "\n"
                    + state.note
                    + "\n"
                    + self.move_prompt,
                ),
            ]
        )

    def accept_propagated_message(self, state: State) -> State:
        message = state.accept_propagated_message()
        next_speaker = message.next_speaker()
        if next_speaker is not None:
            print(f"next speaker: {next_speaker}")
            state.set_next_speaker(next_speaker)
        else:
            state.set_next_speaker("admin")
        return state

    def run(self, state: State) -> State:
        if state.propagated_message.sender == "admin":
            # admin's message is always accepted
            return self.accept_propagated_message(state)

        # judge the propagated message
        llm = LLM(model="gpt-4o", temperature=0, debug=self.debug)
        messages = self.get_prompt(state).build(
            state.propagated_message.sender,
            {"MESSAGE": str(state.propagated_message.first_action())},
        )
        response = llm.invoke(messages)
        # process the action
        judge_message = Message.parse(response, self.name, allow_multi_action=True)
        print(f"judge_message: {judge_message}")
        if (
            judge_message.first_action() is not None
            and judge_message.first_action().action == Action.ACCEPT
        ):
            state = self.accept_propagated_message(state)
        else:
            state.deny_propagated_message()
            state.set_next_speaker("admin")
        # update the state
        for action in judge_message.actions:
            if action.action == Action.UPDATE_STATE:
                state.note = action.args

        # automatically accept the self message without a doubt
        state.set_propagated_message(judge_message)
        state.accept_propagated_message()

        return state
