import copy
from .action import Action

class Message:
    def __init__(self, sender: str, message: str, action: Action, raw: str):
        self.sender = sender
        self.message = message
        self.action = action
        self.raw = raw
    
    @staticmethod
    def parse(raw: str, sender: str) -> "Message":
        message = raw
        # parse the action
        action = Action.SPEAK if message != "" else None

        if ":" in message.splitlines()[0]:
            idx = message.index(":")
            action = Action[message[:idx]]
            message = message[idx+1:]
        
        return Message(sender, message, action, raw)

class State:
    """
    State is a class that stores the state of the discussion.
    """
    def __init__(self):
        """
        Note is a mutable note for the admin.
        """
        self.note: str = ""
        """
        History is a list of messages.
        """
        self.history: list[Message] = []
        """
        Propagated message is the message that is propagated from the caller.
        """
        self.propagated_message: Message = None
    
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
        self.history.append(self.propagated_message)
        self.reset_propagated_message()

        return self.propagated_message
    
    def deny_propagated_message(self) -> Message:
        """
        Deny the propagated message.
        """
        self.reset_propagated_message()
        return self.propagated_message
    
    def stringify_history(self) -> str:
        """
        Stringify the history.
        """
        ret = ""
        for message in self.history:
            if message.action == Action.SPEAK:
                ret += f"{message.sender} said:\n {message.message}\n"
            elif message.action == Action.MARKER:
                ret += f"----- {message.message} -----\n"
            else:
                raise ValueError(f"Invalid action: {message.action}")
        return ret
    
    def copy(self) -> "State":
        """
        Copy the state.
        """
        return copy.deepcopy(self)
