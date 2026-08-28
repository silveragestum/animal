import gradio as gr

from test_prompt_template import PROMPT_TEMPLATE, explain_something


def explain(something: str) -> str:
    return explain_something(something)


demo = gr.Interface(
    fn=explain,
    inputs=gr.Textbox(
        label="Something",
        placeholder="Hong Kong",
        lines=2,
    ),
    outputs=gr.Textbox(label="Explanation (Traditional Chinese)", lines=10),
    title="Explain in Traditional Chinese",
    description=(
        "Enter only the topic. The LangChain prompt template fills in: "
        f'"{PROMPT_TEMPLATE.template}"'
    ),
    examples=["Hong Kong", "photosynthesis", "the Great Wall"],
    flagging_mode="never",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, share=True)
