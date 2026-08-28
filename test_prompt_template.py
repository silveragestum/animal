from langchain_core.prompts import PromptTemplate

from chat import create_llm

PROMPT_TEMPLATE = PromptTemplate.from_template(
    "Please explain {something} in 50 words in traditional Chinese"
)

_chain = None


def get_chain():
    global _chain
    if _chain is None:
        _chain = PROMPT_TEMPLATE | create_llm()
    return _chain


def explain_something(something: str) -> str:
    something = (something or "").strip()
    if not something:
        return "Please provide something to explain."
    response = get_chain().invoke({"something": something})
    return response.content


def main() -> None:
    topic = "Hong Kong"
    print(PROMPT_TEMPLATE.format(something=topic))
    print(explain_something(topic))


if __name__ == "__main__":
    main()
