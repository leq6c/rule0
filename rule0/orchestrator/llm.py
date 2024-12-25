import json

from langchain_openai import ChatOpenAI


class LLM:
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 1,
        debug: bool = False,
        token_limit: int = 100_000,
    ):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.debug = debug
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.token_limit = token_limit
        self.model = model

    def invoke(self, messages: list[tuple[str, str]]) -> str:
        if self.total_input_tokens + self.total_output_tokens > self.token_limit:
            raise Exception(f"Total tokens exceeded limit ({self.token_limit})")
        if "o1" in self.model:
            # o1 doesn't support system messages
            # so we need to replace all system messages with user messages
            for i in range(len(messages)):
                if messages[i][0] == "system":
                    messages[i] = ("user", messages[i][1])
        result = self.llm.invoke(messages)
        # tokens
        prompt_tokens = result.response_metadata["token_usage"]["prompt_tokens"]
        completion_tokens = result.response_metadata["token_usage"]["completion_tokens"]
        self.total_input_tokens += prompt_tokens
        self.total_output_tokens += completion_tokens
        # debug
        if self.debug:
            print("[prompt]")
            print(json.dumps(messages, indent=2))
            print("[response]")
            print(result.content)
            # input("Press Enter to continue...")
        return result.content
