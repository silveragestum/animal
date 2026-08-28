import gradio as gr
from langchain_core.output_parsers import MarkdownListOutputParser
from langchain_core.prompts import ChatPromptTemplate

from chat import create_llm

LANGUAGES = ["Chinese", "English", "Japanese", "Korean"]

PARSER = MarkdownListOutputParser()
SYSTEM_ROLE = (
    "I am a funny person and like to make joke. Make every as a joke."
)

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_ROLE),
        (
            "human",
            "Please explain {something} in 50 words in traditional {language}.\n\n"
            "{format_instructions}",
        ),
    ]
).partial(format_instructions=PARSER.get_format_instructions())

_chain = None


def get_chain():
    global _chain
    if _chain is None:
        _chain = PROMPT_TEMPLATE | create_llm() | PARSER
    return _chain


def explain(something: str, language: str) -> str:
    something = (something or "").strip()
    if not something:
        return "Please enter something to explain."
    if language not in LANGUAGES:
        return "Please select a language."
    items = get_chain().invoke({"something": something, "language": language})
    if not items:
        return "The model did not return a Markdown list that could be parsed."
    return "\n".join(f"- {item}" for item in items)


demo = gr.Interface(
    fn=explain,
    inputs=[
        gr.Textbox(label="Something", placeholder="Hong Kong", lines=2),
        gr.Dropdown(
            choices=LANGUAGES,
            value="Chinese",
            label="Language",
        ),
    ],
    outputs=gr.Markdown(label="Parsed Markdown list"),
    title="Funny Markdown List",
    description=(
        "Uses ChatPromptTemplate with a system role that tells the model to make "
        "everything a joke. Type a topic, pick a language, and get a parsed Markdown list."
    ),
    examples=[
        ["Hong Kong", "Chinese"],
        ["Hong Kong", "English"],
        ["photosynthesis", "Japanese"],
        ["the Great Wall", "Korean"],
    ],
    flagging_mode="never",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7864, share=True)
