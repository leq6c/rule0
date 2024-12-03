from ..prompts.loader import load_prompt

from ..world.state import State
from ..world.message import Message, ActionMessage
from ..world.action import Action
from ..world.prompt import Prompt, Prompts
from ..world.llm import LLM


class JudgeAgent:
    def __init__(self, debug: bool = False):
        self.name = "judge"
        self.system_prompt = load_prompt("judge", "system")
        self.move_prompt = load_prompt("judge", "move")
        self.debug = debug
        self.allow_always = False

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

    def grant(self, state: State, action: ActionMessage):
        state.accept_action(action)
        if action.action == Action.CALL:
            state.set_next_speaker(action.args)

    def deny(self, state: State):
        state.set_next_speaker("admin")

    def run(self, state: State) -> State:
        if not state.has_action():
            state.set_next_speaker("admin")
            return state

        # set self as the default next speaker
        state.set_next_speaker(self.name)

        action = state.pop_action()

        if self.allow_always:
            self.grant(state, action)
        else:
            # judge the action
            llm = LLM(model="gpt-4o", temperature=0, debug=self.debug)
            messages = self.get_prompt(state).build(
                action.sender,
                {"MESSAGE": str(action)},
            )
            response = llm.invoke(messages)
            # process the action
            judge_message = Message.parse(response, self.name)
            if (
                judge_message.first_action() is not None
                and judge_message.first_action().action == Action.ACCEPT
            ):
                self.grant(state, action)
            else:
                self.deny(state)
            # update the state if the judge requests
            for action in judge_message.actions:
                if action.action == Action.UPDATE_STATE:
                    state.note = action.args
                state.accept_action(action)

        return state
