import gradio as gr

from chat import chat_with_user, create_llm

llm = create_llm()


def answer_question(question: str) -> str:
    question = (question or "").strip()
    if not question:
        return "Please enter a question."
    return chat_with_user(llm, question)


demo = gr.Interface(
    fn=answer_question,
    inputs=gr.Textbox(
        label="Your question",
        placeholder="where is Hong Kong, answer in 50 words",
        lines=4,
    ),
    outputs=gr.Textbox(label="Answer", lines=10),
    title="Ask Mistral",
    description="Type a question and submit. Answers come from a LangChain ChatMistralAI model.",
    examples=["where is Hong Kong, answer in 50 words"],
    flagging_mode="never",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
