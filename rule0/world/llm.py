from langchain_openai import ChatOpenAI


class LLM:
    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0,
        debug: bool = False,
        token_limit: int = 100_000,
    ):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.debug = debug
        self.total_tokens = 0
        self.token_limit = token_limit

    def invoke(self, messages: list[tuple[str, str]]) -> str:
        if self.total_tokens > self.token_limit:
            raise Exception(f"Total tokens exceeded limit ({self.token_limit})")
        result = self.llm.invoke(messages)
        # tokens
        prompt_tokens = result.response_metadata["token_usage"]["prompt_tokens"]
        completion_tokens = result.response_metadata["token_usage"]["completion_tokens"]
        self.total_tokens += prompt_tokens + completion_tokens
        # debug
        if self.debug:
            print("[prompt]")
            print("system:")
            print(messages[0][1])
            print("user:")
            print(messages[1][1])
            print("->")
            print(result.content)
            input("Press Enter to continue...")
        return result.content
