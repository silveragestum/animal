from pathlib import Path

import gradio as gr
from langchain_community.chat_message_histories import SQLChatMessageHistory
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

DB_PATH = Path(__file__).resolve().parent / "chat_history.db"
CONNECTION = f"sqlite:///{DB_PATH}"
SESSION_ID = "gradio-sql-chat"

_histories: dict[str, SQLChatMessageHistory] = {}
_chain = None


def get_session_history(session_id: str) -> SQLChatMessageHistory:
    if session_id not in _histories:
        _histories[session_id] = SQLChatMessageHistory(
            session_id=session_id,
            connection=CONNECTION,
            table_name="message_store",
        )
    return _histories[session_id]


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
    _ = history
    text = _message_text(message)
    if not text:
        return "Please enter a message."
    return get_chain().invoke(
        {"input": text},
        config={"configurable": {"session_id": SESSION_ID}},
    )


demo = gr.ChatInterface(
    fn=chat,
    title="Point-form Chatbot (SQL history)",
    description=(
        "Same chatbot as before, but conversation history is stored with "
        "SQLChatMessageHistory in a local SQLite database (chat_history.db)."
    ),
    examples=["Where is Hong Kong?", "What did I just ask you?"],
    flagging_mode="never",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7866, share=True)
