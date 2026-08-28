import gradio as gr
from langchain_core.prompts import PromptTemplate

from chat import create_llm

LANGUAGES = ["Chinese", "English", "Japanese", "Korean"]

PROMPT_TEMPLATE = PromptTemplate.from_template(
    "Please explain {something} in 50 words in traditional {language}"
)

_chain = None


def get_chain():
    global _chain
    if _chain is None:
        _chain = PROMPT_TEMPLATE | create_llm()
    return _chain


def explain(something: str, language: str) -> str:
    something = (something or "").strip()
    if not something:
        return "Please enter something to explain."
    if language not in LANGUAGES:
        return "Please select a language."
    response = get_chain().invoke({"something": something, "language": language})
    return response.content


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
    outputs=gr.Textbox(label="Explanation", lines=10),
    title="Explain in 50 Words",
    description=(
        "Type a topic and pick a language. The LangChain prompt is: "
        f'"{PROMPT_TEMPLATE.template}"'
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
    demo.launch(server_name="0.0.0.0", server_port=7862, share=True)
