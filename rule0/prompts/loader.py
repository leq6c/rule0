import os


def get_file_path(file_name: str) -> str:
    return f"{os.path.dirname(__file__)}/{file_name}"


def load_prompt(role: str, prompt_type: str) -> str:
    with open(get_file_path(f"{role}/{prompt_type}.md"), "r") as f:
        return f.read()
