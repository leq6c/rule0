from ..prompts.loader import load_prompt

from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI

class AdminAgent:
    def __init__(self):
        self.system_prompt = load_prompt("admin", "system")
        self.first_prompt = load_prompt("admin", "first")
    
    