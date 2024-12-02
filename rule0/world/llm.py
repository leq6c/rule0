from langchain_openai import ChatOpenAI


class LLM:
    def __init__(
        self, model: str = "gpt-4o", temperature: float = 0, debug: bool = False
    ):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.debug = debug

    def invoke(self, messages: list[tuple[str, str]]) -> str:
        result = self.llm.invoke(messages)
        if self.debug:
            print("[inference]")
            print(messages)
            print("->")
            print(result.content)
            input("Press Enter to continue...")
        return result.content
