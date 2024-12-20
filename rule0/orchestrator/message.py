from io import StringIO

from .action import Action


class ActionMessage:
    def __init__(self, sender: str, action: Action, args: str):
        self.sender = sender
        self.action = action
        self.args = args.strip()
        self.rejected = False
        self.message_id = None

    def __str__(self):
        if self.rejected:
            return f"----- *rejected* ${self.action.value}:{self.args}"
        else:
            return f"${self.action.value}:{self.args}"

    def __repr__(self):
        return str(self)

    def readable(self) -> str:
        if self.action == Action.SPEAK:
            return f"{self.sender} said:\n {self.args}\n"
        elif self.action == Action.MARKER:
            return f"----- {self.args} -----\n"
        elif self.action == Action.CALL:
            return f"----- {self.sender} called {self.args}\n"
        elif self.action == Action.UPDATE_STATE:
            return f"----- {self.sender} updated the state\n"
        elif self.action == Action.PASS:
            return f"----- {self.sender} passed\n"
        elif self.action == Action.ACCEPT:
            return "----- judge accepted the action\n"
        elif self.action == Action.DENY:
            return "----- judge denied the action\n"
        elif self.action == Action.REJECT:
            return "----- judge rejected the action\n"
        elif self.action == Action.CALL_FOR_VOTE:
            return f"----- admin called for a vote: {self.args}\n"
        elif self.action == Action.VOTE:
            return f"** {self.sender} voted for {self.args}\n"
        elif self.action == Action.END:
            return "----- discussion ended\n"
        else:
            raise ValueError(f"Invalid action: {self.action}")


class Message:
    def __init__(self, sender: str, actions: list[ActionMessage]):
        self.sender = sender
        self.actions = actions
        self.id = id(self)
        for action in self.actions:
            action.message_id = self.id

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
            if data == "":
                break
            if marker in data:
                break

        # read the state
        state = ""
        while True:
            data = buf.readline()
            if data == "":
                break  # end of the state
            state += data

        if state.strip().endswith(marker):
            state = state.strip()[: -len(marker)]

        return ActionMessage(sender, Action.UPDATE_STATE, state.strip())
    
    @staticmethod
    def read_until_next_action(first_line: str, buf: StringIO, sender: str) -> ActionMessage:
        """
        This function allows you to read multiple lines of text until finding the next action.

        For example, you can read this `$CALL_FOR_VOTE` action properly:
        ```
        $CALL_FOR_VOTE:let's start voting
        option 1: something
        option 2: something else
        $CALL:judge
        ```

        And buf would be exactly at the beginning of the next `$CALL` action. So you can continue to read the next action.
        """
        ret = first_line

        while True:
            data = buf.readline()
            if data == "":
                break
            if Action.parse_action(data) is not None:
                # seek to previous line
                buf.seek(buf.tell() - len(data) - 1)
                break

            ret += "\n" + data
        
        action = Action.parse_action(ret)
        message = ret.split(":", 1)[1] if ":" in ret else ""

        return ActionMessage(sender, action, message)

    @staticmethod
    def parse(raw: str, sender: str) -> "Message":
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
                if current_message.strip() != "":
                    actions.append(ActionMessage(sender, Action.SPEAK, current_message))
                    current_message = ""
                if action == Action.UPDATE_STATE:
                    actions.append(Message.read_update_state_action(buf, sender))
                elif action == Action.CALL_FOR_VOTE:
                    actions.append(Message.read_until_next_action(data, buf, sender))
                else:
                    message = data.split(":", 1)[1] if ":" in data else ""
                    actions.append(ActionMessage(sender, action, message))
            else:
                current_message += data + "\n"
        if current_message.strip() != "":
            actions.append(ActionMessage(sender, Action.SPEAK, current_message))

        return Message(sender, actions)
