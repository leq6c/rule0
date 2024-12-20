import copy

from .action import Action
from .message import ActionMessage, Message


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
        action.rejected = False
        self.history.append(action)

    def deny_action(self, action: ActionMessage):
        """
        Deny the action.
        """
        action.rejected = True
        self.history.append(action)
        # remove all actions with the same message_id
        while self.queue and self.queue[-1].message_id == action.message_id:
            print("removing", self.queue[-1])
            self.queue.pop()

    def stringify_history(self) -> str:
        """
        Stringify the history.
        """
        ret = ""
        for action in self.history:
            ret += action.readable()
        return ret

    def copy(self) -> "State":
        """
        Copy the state.
        """
        return copy.deepcopy(self)
