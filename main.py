import getpass
import os
from rule0.base import BaseAgent

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")


BaseAgent().run(debug=True)
