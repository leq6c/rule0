from io import StringIO
from .action import Action


class ActionMessage:
    def __init__(self, sender: str, action: Action, args: str):
        self.sender = sender
        self.action = action
        self.args = args.strip()

    def __str__(self):
        return f"${self.action.value}:{self.args}"

    def __repr__(self):
        return f"${self.action.value}:{self.args}"


class Message:
    def __init__(self, sender: str, actions: list[ActionMessage]):
        self.sender = sender
        self.actions = actions

    def first_action(self) -> ActionMessage:
        return self.actions[0] if len(self.actions) > 0 else None

    def next_speaker(self) -> str:
        if len(self.actions) > 0 and self.actions[0].action == Action.CALL:
            return self.actions[0].args
        else:
            return None

    @staticmethod
    def read_update_state_action(buf: StringIO, sender: str) -> ActionMessage:
        marker = "```"

        # look for the start marker
        while True:
            data = buf.readline()
            if marker in data:
                break

        # read the state
        state = ""
        while True:
            data = buf.readline()
            if marker in data:
                break  # end of the state
            state += data

        return ActionMessage(None, Action.UPDATE_STATE, state.strip())

    @staticmethod
    def parse(raw: str, sender: str, allow_multi_action: bool = False) -> "Message":
        buf = StringIO(raw)
        actions = []
        current_message = ""
        while True:
            data = buf.readline()
            if (
                data == ""
            ):  # buf would contain the new line at the end if it is not empty
                break
            data = data.strip()  # remove the new line at the end
            action = Action.parse_action(data)
            if action is not None:
                if current_message != "":
                    actions.append(ActionMessage(sender, Action.SPEAK, current_message))
                    current_message = ""
                if action == Action.UPDATE_STATE:
                    actions.append(Message.read_update_state_action(buf, sender))
                else:
                    message = data.split(":")[1] if ":" in data else ""
                    actions.append(ActionMessage(sender, action, message))
            else:
                current_message += data + "\n"
        if current_message != "":
            actions.append(ActionMessage(sender, Action.SPEAK, current_message))

        # one action and one speak message is allowed
        if not allow_multi_action:
            new_actions = []
            has_speak = False
            has_action = False
            for action in actions:
                if action.action == Action.SPEAK and has_speak:
                    continue
                if action.action != Action.SPEAK and has_action:
                    continue

                if action.action == Action.SPEAK:
                    has_speak = True
                else:
                    has_action = True

                new_actions.append(action)
            actions = new_actions

        return Message(sender, actions)
