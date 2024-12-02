import copy
from .action import Action

from io import StringIO

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
                break # end of the state
            state += data
        
        return ActionMessage(None, Action.UPDATE_STATE, state.strip())
    
    @staticmethod
    def parse(raw: str, sender: str, allow_multi_action: bool = False) -> "Message":
        buf = StringIO(raw)
        actions = []
        current_message = ""
        while True:
            data = buf.readline()
            if data == "": # buf would contain the new line at the end if it is not empty
                break
            data = data.strip() # remove the new line at the end
            action = Action.parse_action(data)
            if action != None:
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
                    ret += f"judge accepted the action\n"
                elif action.action == Action.DENY:
                    ret += f"judge denied the action\n"
                else:
                    raise ValueError(f"Invalid action: {action.action}")
        return ret
    
    def copy(self) -> "State":
        """
        Copy the state.
        """
        return copy.deepcopy(self)
