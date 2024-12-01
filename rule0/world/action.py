from enum import Enum


class Action(Enum):
    SPEAK = "SPEAK"
    MARKER = "MARKER"
    ACCEPT = "ACCEPT"
    DENY = "DENY"
    CALL = "CALL"
    PASS = "PASS"
    VOTE = "VOTE"
    UPDATE_STATE = "UPDATE_STATE"

    @staticmethod
    def has_action(action: str) -> bool:
        return action in [act.value for act in Action]

    @staticmethod
    def parse_action(action: str) -> "Action":
        action = action.strip()
        if ":" in action:
            action = action.split(":")[0]
        if "$" in action:
            action = action[1:]
        if "-" in action:
            action = action.replace("-", "_")

        if Action.has_action(action):
            return Action[action]
        else:
            return None
