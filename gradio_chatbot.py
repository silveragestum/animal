import gradio as gr
from langchain_core.chat_history import InMemoryChatMessageHistory as ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from chat import create_llm

SYSTEM_ROLE = (
    "I am a person who likes to answer in point form and short answers."
)

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_ROLE),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

chat_history = ChatMessageHistory()

_chain = None


def get_session_history(_session_id: str) -> ChatMessageHistory:
    return chat_history


def get_chain():
    global _chain
    if _chain is None:
        runnable = PROMPT_TEMPLATE | create_llm() | StrOutputParser()
        _chain = RunnableWithMessageHistory(
            runnable,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
    return _chain


def _message_text(message) -> str:
    if isinstance(message, dict):
        return (message.get("text") or message.get("content") or "").strip()
    return (message or "").strip()


def chat(message, history) -> str:
    text = _message_text(message)
    if not text:
        return "Please enter a message."
    if not history:
        chat_history.clear()
    return get_chain().invoke(
        {"input": text},
        config={"configurable": {"session_id": "gradio-chat"}},
    )


demo = gr.ChatInterface(
    fn=chat,
    title="Point-form Chatbot",
    description=(
        "Conversation chatbot using ChatPromptTemplate, ChatMistralAI, "
        "StrOutputParser, and ChatMessageHistory. "
        "The assistant answers in short point form."
    ),
    examples=["Where is Hong Kong?", "What did I just ask you?"],
    flagging_mode="never",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7865, share=True)
