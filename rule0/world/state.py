import copy
from .action import Action
from .message import Message, ActionMessage


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
        History is a list of action messages.
        """
        self.history: list[ActionMessage] = []
        """
        Queue is a list of action messages that are waiting to be processed.
        """
        self.queue: list[ActionMessage] = []
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

    def put_message(self, message: Message):
        """
        Put the message to the queue.
        """
        self.queue.extend(reversed(message.actions))

    def pop_action(self) -> ActionMessage:
        """
        Pop the action from the queue.
        """
        return self.queue.pop()

    def has_action(self) -> bool:
        """
        Check if the queue is not empty.
        """
        return len(self.queue) > 0

    def accept_action(self, action: ActionMessage):
        """
        Accept the action.
        """
        self.history.append(action)

    def stringify_history(self) -> str:
        """
        Stringify the history.
        """
        ret = ""
        for action in self.history:
            if action.action == Action.SPEAK:
                ret += f"{action.sender} said:\n {action.args}\n"
            elif action.action == Action.MARKER:
                ret += f"----- {action.args} -----\n"
            elif action.action == Action.CALL:
                ret += f"----- {action.sender} called {action.args}\n"
            elif action.action == Action.UPDATE_STATE:
                ret += f"{action.sender} updated the state\n"
            elif action.action == Action.PASS:
                ret += f"----- {action.sender} passed\n"
            elif action.action == Action.ACCEPT:
                ret += "----- judge accepted the action\n"
            elif action.action == Action.DENY:
                ret += "----- judge denied the action\n"
            elif action.action == Action.REJECT:
                ret += "----- judge rejected the action\n"
            elif action.action == Action.CALL_FOR_VOTE:
                ret += f"----- admin called for a vote: {action.args}\n"
            elif action.action == Action.VOTE:
                ret += f"** {action.sender} voted for {action.args}\n"
            else:
                raise ValueError(f"Invalid action: {action.action}")
        return ret

    def copy(self) -> "State":
        """
        Copy the state.
        """
        return copy.deepcopy(self)
