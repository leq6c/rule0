from ..orchestrator.action import Action
from ..orchestrator.llm import LLM
from ..orchestrator.message import ActionMessage, Message
from ..orchestrator.prompt import Prompt, Prompts
from ..orchestrator.state import State


class JudgeAgent:
    def __init__(self, base_system_prompt: str, system_prompt: str, move_prompt: str, debug: bool = False):
        self.name = "judge"
        self.base_system_prompt = base_system_prompt
        self.system_prompt = system_prompt
        self.move_prompt = move_prompt
        self.debug = debug
        self.allow_always = True

    def get_prompt(self, state: State, next_action: ActionMessage) -> Prompts:
        prompts = [
            Prompt("system", self.base_system_prompt).append(self.system_prompt).append(state.note),
        ]

        current = ""

        history = state.history + [next_action]

        for action in history:
            prefix = f"{action.sender} requested:\n"
            if action.sender != self.name:
                current += prefix + "$" + action.action.value + ":" + action.args
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

    def grant(self, state: State, action: ActionMessage):
        state.accept_action(action)
        if action.action == Action.CALL:
            state.set_next_speaker(action.args)

    def grant_rest(self, state: State):
        while state.has_action():
            action = state.pop_action()
            state.accept_action(action)

    def deny(self, state: State, action: ActionMessage):
        state.deny_action(action)
        state.set_next_speaker(action.sender)

    def run(self, state: State) -> State:
        if not state.has_action():
            state.set_next_speaker("admin")
            return state

        # set self as the default next speaker
        state.set_next_speaker(self.name)

        action = state.pop_action()

        if self.allow_always:
            if "discussion end" in action.args.lower() and action.sender == "admin" and action.action == Action.MARKER:
                state.exited = True
            self.grant(state, action)
        else:
            # judge the action
            llm = LLM(debug=self.debug)
            messages = self.get_prompt(state, action).build(
                action.sender,
                {"MESSAGE": str(action)},
            )
            response = llm.invoke(messages)
            state.consume_tokens(llm.total_input_tokens, llm.total_output_tokens)
            # process the action
            judge_message = Message.parse(response, self.name)
            first_action = None
            if judge_message.first_action() is not None:
                first_action = judge_message.first_action().action
            if first_action == Action.ACCEPT:
                self.grant(state, action)
            elif first_action == Action.END:
                self.grant(state, action)
                self.grant_rest(state)
            else:
                self.deny(state, action)
            # update the state if the judge requests
            for action in judge_message.actions:
                if action.action == Action.UPDATE_STATE:
                    state.note = action.args
                if action.action == Action.END:
                    state.exited = True
                state.accept_action(action)

        return state
