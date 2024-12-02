import copy
from .action import Action
from .message import Message


class State:
    """
    State is a class that stores the state of the discussion.
    """

    def __init__(self, note: str = ""):
        """
        Note is a mutable note for the admin.
        """
        self.note: str = note
        """
        History is a list of messages.
        """
        self.history: list[Message] = []
        """
        Propagated message is the message that is propagated from the caller.
        """
        self.propagated_message: Message = None
        """
        Next speaker is the next speaker to speak.
        """
        self.next_speaker: str = None
        """
        Exited is a flag to indicate if the discussion is exited.
        """
        self.exited: bool = False

    def __repr__(self) -> str:
        return "__repr__\n" + self.stringify_history() + "\n================"

    def set_next_speaker(self, speaker: str):
        """
        Set the next speaker.
        """
        self.next_speaker = speaker

    def set_propagated_message(self, message: Message):
        """
        Set the propagated message.
        """
        self.propagated_message = message

    def reset_propagated_message(self):
        """
        Reset the propagated message.
        """
        self.propagated_message = None

    def accept_propagated_message(self) -> Message:
        """
        Accept the propagated message.
        """
        message = self.propagated_message
        self.reset_propagated_message()
        self.history.append(message)
        return message

    def deny_propagated_message(self) -> Message:
        """
        Deny the propagated message.
        """
        message = self.propagated_message
        self.reset_propagated_message()
        return message

    def stringify_history(self) -> str:
        """
        Stringify the history.
        """
        ret = ""
        for message in self.history:
            for action in message.actions:
                if action.action == Action.SPEAK:
                    ret += f"{message.sender} said:\n {action.args}\n"
                elif action.action == Action.MARKER:
                    ret += f"----- {action.args} -----\n"
                elif action.action == Action.CALL:
                    ret += f"{message.sender} called {action.args}\n"
                elif action.action == Action.UPDATE_STATE:
                    ret += f"{message.sender} updated the state\n"
                elif action.action == Action.PASS:
                    ret += f"{message.sender} passed\n"
                elif action.action == Action.ACCEPT:
                    ret += "judge accepted the action\n"
                elif action.action == Action.DENY:
                    ret += "judge denied the action\n"
                else:
                    raise ValueError(f"Invalid action: {action.action}")
        return ret

    def copy(self) -> "State":
        """
        Copy the state.
        """
        return copy.deepcopy(self)
