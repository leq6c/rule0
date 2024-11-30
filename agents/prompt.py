class Prompt:
    def __init__(self, role: str, prompt: str):
        self.role = role
        self.prompt = prompt
    
    def append(self, prompt: str) -> "Prompt":
        return Prompt(self.role, self.prompt + "\n" + prompt)
    
    def build(self, sender: str, args: dict[str, str]) -> str:
        prompt = self.prompt
        prompt = prompt.replace("{{SENDER}}", sender)
        if args is not None:
            for key, value in args.items():
                prompt = prompt.replace("{{" + key + "}}", value)
        return prompt

class Prompts:
    def __init__(self, prompts: list[Prompt]):
        self.prompts = prompts
    
    def build(self, sender: str, args: dict[str, str] = None) -> list[tuple[str, str]]:
        return [(prompt.role, prompt.build(sender, args)) for prompt in self.prompts]
