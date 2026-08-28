import os
from pathlib import Path

from langchain_mistralai import ChatMistralAI
from rich.console import Console
from rich.panel import Panel


def load_env() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def create_llm() -> ChatMistralAI:
    load_env()
    if not os.environ.get("MISTRAL_API_KEY"):
        raise RuntimeError("Set MISTRAL_API_KEY in the environment or a local .env file.")
    return ChatMistralAI(model="mistral-small-latest", temperature=0.3)


def chat_with_user(llm: ChatMistralAI, question: str) -> str:
    response = llm.invoke(question)
    return response.content


def main() -> None:
    question = "where is Hong Kong, answer in 50 words"
    llm = create_llm()
    answer = chat_with_user(llm, question)

    console = Console()
    console.print(Panel(question, title="User"))
    console.print(Panel(answer, title="LLM"))


if __name__ == "__main__":
    main()
