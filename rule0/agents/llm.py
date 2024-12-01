from langchain_openai import ChatOpenAI

class LLM:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    def invoke(self, messages: list[tuple[str, str]]) -> str:
        result = self.llm.invoke(messages)
        return result.content
